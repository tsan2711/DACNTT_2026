"""Watchdog for from_pretrained() calls that can hang indefinitely.

Kaggle T4 sessions have shown intermittent stalls mid weight-load (tqdm
"Loading weights: X%|... Materializing param=...") that never crash or
progress. Two full 12h Kaggle sessions were lost to this (Run A,
2026-09-18 and 2026-09-19) with zero output afterwards.

The stall can be inside native code that holds the GIL, so a Python-level
timer (a thread + join(timeout), or a signal handler) never gets to run:
a first version of this module used a daemon thread and was reproduced
raising only after the hung call finished on its own. faulthandler's
watchdog runs on a C thread that needs no GIL; with exit=True it dumps
every thread's traceback to stderr and terminates the process with
status 1. The traceback also shows where the load was stuck.

Nothing in-process can recover a stuck load, so failing fast is the goal:
a fresh Kaggle session can be retried in minutes instead of losing 12h.
train.py reloads the base model every round, so this guards every round.
"""

from __future__ import annotations

import faulthandler
import time
from typing import Callable, TypeVar

T = TypeVar("T")

DEFAULT_TIMEOUT_S = 180


def load_with_timeout(load_fn: Callable[[], T], *, what: str, timeout_s: float = DEFAULT_TIMEOUT_S) -> T:
    print(f"[load-watchdog] {what}: exit after {timeout_s}s without returning", flush=True)
    faulthandler.dump_traceback_later(timeout_s, exit=True)
    started = time.monotonic()
    try:
        result = load_fn()
    finally:
        faulthandler.cancel_dump_traceback_later()
    # experiments/viec3/supervise.py watches for this line from OUTSIDE the
    # process: in Run A 2026-09-20 the in-process watchdog above printed its
    # start line but never fired (process hung 12h anyway).
    print(f"[load-watchdog] {what}: loaded in {time.monotonic() - started:.0f}s", flush=True)
    return result
