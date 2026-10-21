"""kaggle_driver: stall detection from outside, and the one-round-per-process resume loop."""

import json
import sys

sys.path.insert(0, "experiments/viec3")
from kaggle_driver import StallTracker, drive, run_child  # noqa: E402


def test_tracker_needs_continuous_idle():
    t = StallTracker(10)
    assert not t.update(0, 0)
    assert not t.update(5, 0)
    assert not t.update(7, 90)  # busy again: clock resets
    assert not t.update(8, 0)
    assert not t.update(17, 0)
    assert t.update(18, 0)


def test_tracker_ignores_missing_gpu():
    t = StallTracker(1)
    assert not t.update(0, None)
    assert not t.update(100, None)


def test_kills_a_child_whose_gpu_went_idle(tmp_path):
    body = "import time; time.sleep(60)"
    status = run_child(
        [sys.executable, "-c", body],
        tmp_path / "log",
        StallTracker(0.3),
        poll=0.1,
        stack_wait=0.1,
        gpu_fn=lambda: 0,
    )
    assert status == "stalled"


def test_busy_child_is_left_alone(tmp_path):
    body = "import time; time.sleep(1)"
    status = run_child(
        [sys.executable, "-c", body],
        tmp_path / "log",
        StallTracker(0.3),
        poll=0.1,
        gpu_fn=lambda: 99,
    )
    assert status == "ok"


def _fake_round_child(out, hang_marker):
    # Appends one "round" to state.json per process; the first process that
    # would produce round 2 hangs forever (once), like the real Run A.
    return [
        sys.executable,
        "-c",
        (
            "import json, os, sys, time\n"
            f"out, marker = {str(out)!r}, {str(hang_marker)!r}\n"
            "p = os.path.join(out, 'state.json')\n"
            "recs = json.load(open(p))['records'] if os.path.exists(p) else []\n"
            "if len(recs) == 2 and not os.path.exists(marker):\n"
            "    open(marker, 'w').write('x'); time.sleep(600)\n"
            "recs.append({'round': len(recs)})\n"
            "json.dump({'records': recs}, open(p, 'w'))\n"
        ),
    ]


def test_drive_resumes_after_a_stalled_round(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    code = drive(
        _fake_round_child(out, tmp_path / "hung"),
        out_dir=out,
        rounds=4,
        log_path=tmp_path / "run.log",
        idle_seconds=0.3,
        budget_seconds=3600,
        max_consecutive_failures=3,
        poll=0.1,
        gpu_fn=lambda: 0,
    )
    assert code == 0
    assert len(json.loads((out / "state.json").read_text())["records"]) == 4


def test_drive_gives_up_after_repeated_failures(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    code = drive(
        [sys.executable, "-c", "raise SystemExit(1)"],
        out_dir=out,
        rounds=2,
        log_path=tmp_path / "run.log",
        idle_seconds=60,
        budget_seconds=3600,
        max_consecutive_failures=2,
        poll=0.05,
        gpu_fn=lambda: 50,
    )
    assert code == 2
