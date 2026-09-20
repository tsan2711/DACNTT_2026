"""Run a command and kill it from OUTSIDE if a model load stalls.

    python experiments/viec3/supervise.py --load-timeout 240 -- \
        python -u -m experiments.viec3.run --mode hf ...

Why external: three 12h Kaggle sessions (Run A, 2026-09-18/19/20) hung inside
AutoModelForCausalLM.from_pretrained ("Loading weights: 2/338"). The in-process
watchdogs (daemon thread, then faulthandler exit=True) either could not run or
did not fire. An outside process is not affected by whatever wedges the child.

Protocol: src/dacntt/gvt/_load_timeout.py prints "[load-watchdog] ... exit
after Ns without returning" when a load starts and "[load-watchdog] ... loaded
in Ns" when it finishes. If a load has been open longer than --load-timeout,
the child's whole process group is SIGKILLed and this exits with status 3.
Everything else the child prints is passed through unchanged.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import threading
import time

START = "exit after"
DONE = "loaded in"
MARK = "[load-watchdog]"


def supervise(cmd: list[str], load_timeout: float, poll: float = 2.0) -> int:
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        bufsize=1,
        start_new_session=True,
    )
    state = {"loading_since": None, "what": ""}

    def pump() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            if MARK in line:
                if DONE in line:
                    state["loading_since"] = None
                elif START in line:
                    state["loading_since"] = time.monotonic()
                    state["what"] = line.strip()

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()
    while proc.poll() is None:
        since = state["loading_since"]
        if since is not None and time.monotonic() - since > load_timeout:
            print(
                f"[supervise] model load open for >{load_timeout:.0f}s — killing: {state['what']}",
                flush=True,
            )
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            return 3
        time.sleep(poll)
    reader.join(timeout=5)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--load-timeout", type=float, default=240.0)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        ap.error("no command given (use: supervise.py [--load-timeout N] -- CMD ...)")
    return supervise(cmd, args.load_timeout)


if __name__ == "__main__":
    raise SystemExit(main())
