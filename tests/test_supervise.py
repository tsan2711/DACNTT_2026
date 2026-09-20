"""supervise: kills a child whose model load never finishes, from outside."""

import sys
import time

sys.path.insert(0, "experiments/viec3")
from supervise import supervise  # noqa: E402


def _child(body: str) -> list[str]:
    return [sys.executable, "-u", "-c", body]


def test_kills_child_stuck_in_load():
    body = (
        "import time\n"
        "print('[load-watchdog] X [generate]: exit after 180s without returning')\n"
        "time.sleep(60)\n"
    )
    t0 = time.time()
    assert supervise(_child(body), load_timeout=1, poll=0.2) == 3
    assert time.time() - t0 < 15


def test_lets_a_long_run_finish_once_load_is_done():
    body = (
        "import time\n"
        "print('[load-watchdog] X: exit after 180s without returning')\n"
        "print('[load-watchdog] X: loaded in 1s')\n"
        "time.sleep(3)\n"
        "print('train done')\n"
    )
    assert supervise(_child(body), load_timeout=1, poll=0.2) == 0


def test_passes_through_child_exit_code():
    assert supervise(_child("raise SystemExit(7)"), load_timeout=1, poll=0.2) == 7
