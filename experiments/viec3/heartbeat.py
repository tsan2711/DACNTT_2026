"""Background heartbeat for Kaggle runs: leaves a black-box recording.

    python experiments/viec3/heartbeat.py /kaggle/working/heartbeat.log &

Every 2s appends one line: time, memory, load, processes in uninterruptible
sleep (state D), disk use, GPU memory/util. If a session freezes (Run A hung
12h three times in a row at "Loading weights", and neither in-process
watchdogs nor an external supervisor could act, i.e. the whole container
looks frozen), the LAST lines of this file, downloaded after Kaggle cancels
the session, show what the machine looked like just before it stopped.
Linux-only fields degrade to "n/a" elsewhere.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time


def meminfo() -> str:
    try:
        info = {}
        for line in open("/proc/meminfo"):
            k, v = line.split(":", 1)
            info[k] = int(v.split()[0]) // 1024
        return f"mem_avail={info['MemAvailable']}MB dirty={info.get('Dirty', 0)}MB swap_free={info.get('SwapFree', 0)}MB"
    except OSError:
        return "mem=n/a"


def d_state_count() -> str:
    n, names = 0, []
    try:
        for pid in filter(str.isdigit, os.listdir("/proc")):
            try:
                stat = open(f"/proc/{pid}/stat").read()
            except OSError:
                continue
            comm = stat[stat.index("(") + 1 : stat.rindex(")")]
            if stat[stat.rindex(")") + 2] == "D":
                n += 1
                names.append(f"{pid}:{comm}")
        return f"D_procs={n}{names[:4]}"
    except OSError:
        return "D_procs=n/a"


def gpu() -> str:
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        return f"gpu={out or 'n/a'}"
    except (OSError, subprocess.TimeoutExpired):
        return "gpu=n/a"


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "heartbeat.log"
    root = os.path.dirname(os.path.abspath(path))
    with open(path, "a", buffering=1) as f:
        while True:
            du = shutil.disk_usage(root)
            load = os.getloadavg()[0] if hasattr(os, "getloadavg") else -1
            f.write(
                f"{time.strftime('%H:%M:%S')} {meminfo()} load={load:.1f} {d_state_count()} "
                f"disk_free={du.free // 2**20}MB {gpu()}\n"
            )
            f.flush()
            os.fsync(f.fileno())
            time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main())
