import os

# Base project directory (auto-detect) TODO
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Default results directory
RESULTS_DIR = os.environ.get("RESULTS_DIR", os.path.join(BASE_DIR, "results"))

# Enable or disable AI debugger 
DEBUGGER_ENABLED = True

# Ollama model used
OLLAMA_MODEL = "mistral"

#Number of rows before and after violation time to keep in VCD extraction
VIOLATION_WINDOW = 10 