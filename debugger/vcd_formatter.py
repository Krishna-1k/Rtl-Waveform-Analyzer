
from vcdvcd import VCDVCD
import pandas as pd
import os
from .config import VIOLATION_WINDOW

def add_cycle_count(vcd_df, clock_signal):
    """
    Adds a 'Clock Cycle' column to the DataFrame based on the clock signal.
    The first rising edge of the clock signal is considered cycle 0.
    Currently unused
    """
    clock = vcd_df[clock_signal].astype(int)
    rising_edges = (clock == 1) & (clock.shift(fill_value=0) == 0)
    cycle_count = rising_edges.cumsum()


    vcd_df.insert(1, 'Clock_Cycle', cycle_count)

    return vcd_df

def extract_vcd_data(vcd_path, log_path):
    vcd = VCDVCD(vcd_path, store_tvs=True)

    # Violation times from log
    violation_times = []
    if log_path and os.path.exists(log_path):
        with open(log_path) as f:
            for line in f:
                if "VIOLATION at" in line:
                    try:
                        ts = float(line.split("VIOLATION at ")[1].split(" ps")[0])
                        violation_times.append(ts)
                    except:
                        continue

    dut_signals = list(vcd.signals)
    
    all_times = sorted({t for sig in dut_signals for t, _ in vcd[sig].tv})
    last_vals = {sig: None for sig in dut_signals}
    rows = []
    time_to_index = {}
    for idx, t in enumerate(all_times):
        row = [t]
        for sig in dut_signals:
            changes = [val for time, val in vcd[sig].tv if time == t]
            if changes:
                last_vals[sig] = changes[-1]
            row.append(last_vals[sig])
        rows.append(row)
        time_to_index[t] = idx  # Map time to row index. Useful for windowing later

    headers = ['Time'] + dut_signals
    vcd_df = pd.DataFrame(rows, columns=headers)

    #print(tabulate(rows, headers=headers, tablefmt="grid"))
    for sig in dut_signals:
        if vcd_df[sig].dtype == object:  # only convert binary strings
            try:
                vcd_df[sig] = vcd_df[sig].apply(lambda x: hex(int(x, 2)) if x is not None else None)
            except:
                continue  

    if violation_times:
        indices_to_keep = set()
        for t in violation_times:
            if t in time_to_index:  
                idx = time_to_index[t]
                start = max(0, idx - VIOLATION_WINDOW)
                end = min(len(vcd_df) - 1, idx + VIOLATION_WINDOW)
                indices_to_keep.update(range(start, end + 1))
        vcd_df = vcd_df.iloc[sorted(indices_to_keep)]

    vcd_df = vcd_df.loc[:, ~vcd_df.columns.str.startswith('$rootio')] #Duplicated signals, reduce vcd verbosity

    return vcd_df.to_csv(index=False)