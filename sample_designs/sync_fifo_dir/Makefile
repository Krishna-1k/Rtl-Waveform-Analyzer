# Makefile for sync_fifo cocotb testbench with Verilator

export PYTHONPATH := $(realpath ../..):$(PYTHONPATH)


TOPLEVEL        = sync_fifo
TOPLEVEL_LANG   = verilog
MODULE          = sync_fifo_tb
SIM             = verilator
VERILOG_SOURCES = sync_fifo.sv

# Export RESULTS_DIR and enable tracing
RESULTS_DIR ?= results
export RESULTS_DIR := $(abspath $(RESULTS_DIR))

WAVES = 1

# Use absolute path as verilator creates own sim_build directory
export TRACE_FILE := $(abspath $(RESULTS_DIR)/dump.vcd)

# Ensure the results directory is created
$(shell mkdir -p $(RESULTS_DIR))

EXTRA_ARGS += --trace --trace-structs

#TODO why SIM_ARGS not working? Unable to pass +trace+<file>
#SIM_ARGS += +trace+$(TRACE_FILE)

include $(shell cocotb-config --makefiles)/Makefile.sim

#TODO extend clean to remove results dir.
# clean:
# 	@rm -rf $(RESULTS_DIR)
