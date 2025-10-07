## Waveform Analyzer 

An experimental waveform analyzer utilizing **Cocotb**, **Verilator**, and **LLM-based debugging** to analyze RTL simulation issues.  
When a testbench violation occurs, the tool will automatically run a LLM locally(via Ollama) to interpret logs and waveform traces.

---

## Overview

- Processes waveform VCD files into concise, LLM-readable CSV format  
- Works best with **Cocotb** testbenches (Python-based)  
- Uses **Verilator** for simulation and waveform dumps  
- Invokes **Ollama** (e.g., `mistral`) for natural-language analysis  
- Stores logs and AI findings under `results/*error.log` file 

---

## Structure

- WAVE_DEBUGGER
   - debugger
      - cocotb_utils.py #Debug utilities
      - config.py
      - ollama_client.py #To interface with LLM
      - vcd_formatter.py #Process VCD data into concise, csv file
   - sample_designs
      - sync_fifo_tb.py #cocotb testbench
      - sync_fifo.sv #RTL file
      - Makefile
      - results/ #Folder where logs/analysis is dumped


---

## Configuration Parameter Options
- DEBUGGER_ENABLED = True  
- OLLAMA_MODEL = "mistral" 


## Run Simulation

```bash
cd sample_designs/sync_fifo_dir
make TESTCASE=sync_fifo_basic_test


=== AI Analysis Output Example(check under sync_fifo_dir/results for real results)===
• FIFO underflow caused by early read enable
• Write pointer not reset correctly
=== End AI Analysis ===
```


## Tools Used

- Python 3.12
- SystemVerilog
- [Cocotb](https://github.com/cocotb/cocotb)
- [Verilator](https://github.com/verilator/verilator)
- Gtkwave (Optional waveform viewer)
- Ollama(with model, eg mistral) - [Documentation](https://github.com/ollama/ollama)

## Known issues and Enhancements

- Optimized for small, simple synchronous designs; large or complex designs will exceed LLM input limits.
- VCD waveform currently dumps to the working directory by default; no straightforward way to change this yet.
- Capturing the precise "violation window" from logs could be improved, potentially using design details (pipeline depth, etc.).
- Waveform visualization or GUI integration is not available yet.
- This is an experimental project; It will be good to try many other LLMs or fine-tuned models to compare analysis results.


