import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.clock import Clock
from debugger.cocotb_utils import with_debug_tool

@with_debug_tool("sync_fifo_basic_test")
async def sync_fifo_basic_test(dut, violations):
    """Basic test for synchronous FIFO"""
    cocotb.start_soon(Clock(dut.clk, 10, units="ps").start())

    # Reset
    dut.rst_n.value = 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.din.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    # Write data into FIFO
    for i in range(4):
        dut.wr_en.value = 1
        dut.din.value = i + 1
        await FallingEdge(dut.clk)
    dut.wr_en.value = 0

    # Read data from FIFO and capture violations
    for i in range(4):
        dut.rd_en.value = 1
        await FallingEdge(dut.clk)
        ts = cocotb.utils.get_sim_time('ps')
        cocotb.log.info(f"Read data: {dut.dout.value}")
        if int(dut.dout.value) != i + 1:
            msg = f"Read data mismatch: got {int(dut.dout.value)}, expected {i+1}"
            cocotb.log.error(f"VIOLATION at {ts} ps: {msg}")
            violations.append((ts, msg))
    dut.rd_en.value = 0

    await Timer(10, units="ns")


@with_debug_tool("sync_fifo_overflow_underflow_test")
async def sync_fifo_overflow_underflow_test(dut, violations):
    """Test FIFO overflow and underflow conditions"""
    cocotb.start_soon(Clock(dut.clk, 10, units="ps").start())

    # Reset
    dut.rst_n.value = 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.din.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    # Underflow check
    dut.rd_en.value = 1
    await FallingEdge(dut.clk)
    ts = cocotb.utils.get_sim_time('ps')
    cocotb.log.info(f"Empty value: {dut.empty.value}")
    if int(dut.empty.value) != 1:
        msg = f"Underflow: empty expected 1, got {int(dut.empty.value)}"
        cocotb.log.error(f"VIOLATION at {ts} ps: {msg}")
        violations.append((ts, msg))
    dut.rd_en.value = 0
    await FallingEdge(dut.clk)

    # Fill FIFO to full
    for i in range(4):
        dut.wr_en.value = 1
        dut.din.value = i + 2
        await FallingEdge(dut.clk)
    dut.wr_en.value = 0

    ts = cocotb.utils.get_sim_time('ps')
    cocotb.log.info(f"Full value: {dut.full.value}")
    if int(dut.full.value) != 1:
        msg = f"Full flag expected 1 after writes, got {int(dut.full.value)}"
        cocotb.log.error(f"VIOLATION at {ts} ps: {msg}")
        violations.append((ts, msg))

    # Attempt overflow
    dut.wr_en.value = 1
    dut.din.value = 5
    await FallingEdge(dut.clk)
    ts = cocotb.utils.get_sim_time('ps')
    cocotb.log.info(f"Full value after write attempt: {dut.full.value}")
    if int(dut.full.value) != 1:
        msg = f"Overflow: full should remain 1 after write attempt, got {int(dut.full.value)}"
        cocotb.log.error(f"VIOLATION at {ts} ps: {msg}")
        violations.append((ts, msg))
    dut.wr_en.value = 0

    # Empty the FIFO
    for _ in range(4):
        dut.rd_en.value = 1
        await FallingEdge(dut.clk)
    dut.rd_en.value = 0

    ts = cocotb.utils.get_sim_time('ps')
    cocotb.log.info(f"Empty value: {dut.empty.value}")
    if int(dut.empty.value) != 1:
        msg = f"Empty expected 1 after reads, got {int(dut.empty.value)}"
        cocotb.log.error(f"VIOLATION at {ts} ps: {msg}")
        violations.append((ts, msg))

    await Timer(10, units="ns")