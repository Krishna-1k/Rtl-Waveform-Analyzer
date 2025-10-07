import os
import cocotb
import logging
from .config import RESULTS_DIR, DEBUGGER_ENABLED
from .ollama_client import run_analysis


def setup_loggers(test_name: str):
    """Set up loggers for Cocotb and debugger."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    log_file = f"{RESULTS_DIR}/{test_name}.log"
    error_log_file = f"{RESULTS_DIR}/{test_name}_error.log"

    logger = logging.getLogger("cocotb")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # All logs
    fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
    logger.addHandler(fh)

    # Errors only
    eh = logging.FileHandler(error_log_file, mode="w", encoding="utf-8")
    eh.setLevel(logging.ERROR)
    eh.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
    logger.addHandler(eh)

    cocotb.log = logger
    return logger, log_file, error_log_file


def with_debug_tool(test_name):
    """Decorator that enables automatic debugging upon violations."""

    def decorator(test_func):
        @cocotb.test(name=test_name)
        async def wrapper(dut):
            logger, log_file, error_log_file = setup_loggers(test_name)
            dut._log = logger
            violations = []

            try:
                await test_func(dut, violations)
            finally:
                if DEBUGGER_ENABLED and violations:
                    #TODO why is vcd in cwd not results dir?
                    vcd_file = os.path.join(RESULTS_DIR, "../", "dump.vcd")
                    spec_file = os.path.join(os.getcwd(), "spec.txt") #Spec resides in same path as make
                    run_analysis(spec_file, vcd_file, error_log_file)
                if violations:
                    raise AssertionError(f"{len(violations)} violations detected in test '{test_name}'.")
        return wrapper

    return decorator
