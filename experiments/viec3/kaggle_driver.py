"""Run the GVT loop one round per process; kill and resume a stalled child.

    python -u experiments/viec3/kaggle_driver.py --out DIR --rounds 3 \
        --log /kaggle/working/run.log -- \
        python -u -m experiments.viec3.run --mode hf ... --out DIR

The driver appends --resume --rounds-per-process 1 to the command. Why:
Run A hung on Kaggle six times (never one the same way twice) once a single
process had reloaded the model several times, and every in-process watchdog
failed because it had to print to a pipe, or needed the stuck process to
cooperate. Here the child writes only to a file, a fresh process handles each
round (round 0 — three loads — is the case known to work), and stalls are
detected from outside by one signal that needs no marker line and no
cooperation: the GPU sitting at 0% for --idle-minutes while the child is
alive (generate and train keep it near 100%; loads and CPU-side verification
last seconds to a few minutes).

On a stall the child gets SIGUSR1 (run.py dumps all thread stacks to
out/stacks.log — the evidence that was missing every time before), then
SIGKILL, and the next process resumes from out/state.json.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path


class StallTracker:
    """True once GPU utilization has been 0% continuously for idle_seconds.
    ``None`` (no nvidia-smi) never counts as idle, so CPU-only runs are safe."""

    def __init__(self, idle_seconds: float) -> None:
        self.idle_seconds = idle_seconds
        self._idle_since: float | None = None

    def update(self, now: float, gpu_util: int | None) -> bool:
        if gpu_util is None or gpu_util > 0:
            self._idle_since = None
            return False
        if self._idle_since is None:
            self._idle_since = now
        return now - self._idle_since >= self.idle_seconds


def gpu_util() -> int | None:
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout.split()
        return int(out[0])
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return None


def run_child(
    cmd: list[str],
    log_path: Path,
    stall: StallTracker,
    *,
    poll: float = 5.0,
    stack_wait: float = 3.0,
    gpu_fn: Callable[[], int | None] = gpu_util,
) -> str:
    """Returns "ok", "failed" (non-zero exit) or "stalled" (killed by us)."""
    with log_path.open("ab") as log:
        proc = subprocess.Popen(
            cmd,
            stdout=log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        while proc.poll() is None:
            time.sleep(poll)
            if proc.poll() is None and stall.update(time.monotonic(), gpu_fn()):
                try:
                    os.kill(proc.pid, signal.SIGUSR1)
                    time.sleep(stack_wait)
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass  # already gone (SIGUSR1's default action is terminate)
                proc.wait()
                return "stalled"
        return "ok" if proc.returncode == 0 else "failed"


def rounds_done(out_dir: Path) -> int:
    path = out_dir / "state.json"
    if not path.exists():
        return 0
    return len(json.loads(path.read_text(encoding="utf-8"))["records"])


def drive(
    cmd: list[str],
    *,
    out_dir: Path,
    rounds: int,
    log_path: Path,
    idle_seconds: float,
    budget_seconds: float,
    max_consecutive_failures: int,
    poll: float = 5.0,
    gpu_fn: Callable[[], int | None] = gpu_util,
) -> int:
    started = time.monotonic()
    round_seconds: list[float] = []
    failures = 0
    full_cmd = [*cmd, "--resume", "--rounds-per-process", "1"]
    while True:
        done = rounds_done(out_dir)
        if done >= rounds:
            print(f"[driver] all {rounds} rounds done", flush=True)
            return 0
        elapsed = time.monotonic() - started
        if round_seconds and elapsed + max(round_seconds) * 1.15 > budget_seconds:
            print(
                f"[driver] budget: {elapsed / 3600:.1f}h used, slowest round "
                f"{max(round_seconds) / 3600:.1f}h — stopping at {done}/{rounds} rounds",
                flush=True,
            )
            return 2
        began = time.monotonic()
        status = run_child(
            full_cmd, log_path, StallTracker(idle_seconds), poll=poll, gpu_fn=gpu_fn
        )
        after = rounds_done(out_dir)
        print(
            f"[driver] round {done} attempt: {status}, rounds done {done} -> {after}, "
            f"{(time.monotonic() - began) / 60:.0f} min",
            flush=True,
        )
        if after > done:
            round_seconds.append(time.monotonic() - began)
            failures = 0
        else:
            failures += 1
            if failures >= max_consecutive_failures:
                print(f"[driver] {failures} failures in a row — giving up at {done}/{rounds}", flush=True)
                return 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True, help="same --out the child uses (holds state.json)")
    ap.add_argument("--rounds", type=int, required=True)
    ap.add_argument("--log", type=Path, required=True, help="child stdout+stderr go here, never to a pipe")
    ap.add_argument("--idle-minutes", type=float, default=20.0)
    ap.add_argument("--budget-hours", type=float, default=11.0)
    ap.add_argument("--max-failures", type=int, default=3)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        ap.error("no command given (use: kaggle_driver.py [opts] -- CMD ...)")
    args.out.mkdir(parents=True, exist_ok=True)
    return drive(
        cmd,
        out_dir=args.out,
        rounds=args.rounds,
        log_path=args.log,
        idle_seconds=args.idle_minutes * 60,
        budget_seconds=args.budget_hours * 3600,
        max_consecutive_failures=args.max_failures,
    )


if __name__ == "__main__":
    sys.exit(main())
