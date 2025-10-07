import os
import ollama
from .config import OLLAMA_MODEL
from .vcd_formatter import extract_vcd_data

def create_system_prompt():
    return {
        'role': 'system',
        'content': """You are an expert in RTL waveform analysis and will be given three inputs from the user.
                      Waveform data in csv format marked by "WAVEFORM:" identifier.
                      Design specifications in text format marked by "SPECIFICATION:" identifier.
                      Violation description in text format marked by "VIOLATION:" identifier. 
                      Important notes about csv waveform data:
                        1. The first row indicates the signal names. The first column is simulation timing(unit is picoseconds unless otherwise specified). A row is added whenever a signal toggles. 
                        2. A toggle is strictly defined as a signal transition from 0->1 or 1->0. Do not infer toggles from outside the CSV data. 
                        3. If a clock signal is present, pay close attention to signal toggling in relation to clock values.
                        4. Values will likely be converted to hex format for ease of interpretation. Additionally, do not assume this is the complete waveform.
                      Your task is the following:
                      1. Interpret the data given design specifications and violation descriptions.
                      2. Suggest 3 possible reasons for the violations in order of highest to lowest confidence.
                      3. Return findings in a concise bulleted list format."""
    }

def run_analysis(specifications: str, vcd_file: str, log_file: str):
    """
    LLM analysis and appending results to log_file.
    """

    # Read specification
    with open(specifications, "r", encoding="utf-8") as f:
        specs = f.read().strip()

    # Extract waveform CSV from VCD
    waveform_csv = extract_vcd_data(vcd_file, log_file)

    # Read violation log
    violations = ""
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            violations = f.read().strip()
    if not violations:
        violations = "No violation found. Skip analysis"
    messages = [
        create_system_prompt(),
        {
            'role': 'user',
            'content': f"SPECIFICATION: {specs}\nWAVEFORM: {waveform_csv}\nVIOLATION: {violations}\nEnd of user input"
        }
    ]

    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n=== AI Analysis Output ===\n")
            f.write(response['message']['content'])
            f.write("\n=== End AI Analysis ===\n")
    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\nError: Failed to get response from Ollama - {str(e)}\n")



