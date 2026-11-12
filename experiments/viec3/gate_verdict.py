"""Positive-control gate: did a run improve over its own round 0?

    .venv/bin/python -m experiments.viec3.gate_verdict <run_dir> [--B 10000]

Reads <run_dir>/generations.jsonl, re-verifies every sample with the patched
verifier (V': \\dfrac->\\frac, gold wrapped in \\boxed{}), and prints per-round
pass@1 / pass@k / sample accuracy with a paired problem-level bootstrap
interval for the change against round 0. The gate is "passed" when the final
round's pass@1 change is positive AND its interval excludes zero; "weak" when
only the point estimate is positive; "failed" otherwise.
CPU only.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from dacntt.gold.extract import normalise_math_gold  # noqa: E402
from dacntt.verify.adapter import MathVerifyAdapter  # noqa: E402

FIX_GOLD = False  # set by --fix-gold: apply the final round's gold normalisation


def load_flags(path: Path, patch: bool) -> dict[int, dict[str, list[bool]]]:
    ad = MathVerifyAdapter(
        "reward", normalize_frac_commands=patch, normalize_gold_boxed=patch
    )
    out: dict[int, dict[str, list[bool]]] = {}
    for line in path.open():
        rec = json.loads(line)
        if rec["dataset"] == "mathtrain":  # selection pool, not the exam
            continue
        out.setdefault(rec["round"], {})[rec["item_id"]] = [
            ad.verify(normalise_math_gold(rec["gold"]) if FIX_GOLD else rec["gold"], t).accepted for t in rec["texts"]
        ]
    return out


def stat(rows: list[list[bool]]) -> tuple[float, float, float]:
    n = len(rows)
    p1 = sum(r[0] for r in rows) / n  # pass@1 = first sample, as in table.md
    pk = sum(any(r) for r in rows) / n
    sa = sum(sum(r) / len(r) for r in rows) / n  # sample accuracy
    return p1, pk, sa


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--no-patch", action="store_true")
    ap.add_argument("--fix-gold", action="store_true", help="normalise gold as run.py --fix-gold does")
    a = ap.parse_args()
    global FIX_GOLD
    FIX_GOLD = a.fix_gold
    flags = load_flags(a.run_dir / "generations.jsonl", not a.no_patch)
    rounds = sorted(flags)
    ids = sorted(set.intersection(*(set(flags[r]) for r in rounds)))
    print(f"{len(ids)} exam problems common to rounds {rounds}")
    rng = random.Random(0)
    draws = [[rng.randrange(len(ids)) for _ in ids] for _ in range(a.B)]
    base = [flags[rounds[0]][i] for i in ids]
    print("round | pass@1 | pass@k | d_pass@1 [95% CI] | d_pass@k [95% CI]")
    last = None
    for r in rounds:
        cur = [flags[r][i] for i in ids]
        p1, pk, _ = stat(cur)
        if r == rounds[0]:
            print(f"{r:5d} | {100*p1:6.1f} | {100*pk:6.1f} | (baseline)")
            continue
        d1, dk, ds = [], [], []
        for d in draws:
            c = [cur[j] for j in d]
            b = [base[j] for j in d]
            d1.append(stat(c)[0] - stat(b)[0])
            dk.append(stat(c)[1] - stat(b)[1])
            ds.append(stat(c)[2] - stat(b)[2])
        d1.sort(), dk.sort(), ds.sort()
        lo, hi = int(0.025 * a.B), int(0.975 * a.B)
        b1, bk = stat(base)[0], stat(base)[1]
        last = (p1 - b1, d1[lo], d1[hi])
        print(
            f"{r:5d} | {100*p1:6.1f} | {100*pk:6.1f} | {100*(p1-b1):+.1f} "
            f"[{100*d1[lo]:+.1f}, {100*d1[hi]:+.1f}] | {100*(pk-bk):+.1f} "
            f"[{100*dk[lo]:+.1f}, {100*dk[hi]:+.1f}] | sample acc {100*(stat(cur)[2]-stat(base)[2]):+.1f} "
            f"[{100*ds[lo]:+.1f}, {100*ds[hi]:+.1f}]"
        )
    if last:
        delta, lo_, hi_ = last
        verdict = "PASSED" if lo_ > 0 else ("WEAK (point estimate only)" if delta > 0 else "FAILED")
        print(f"\nGATE: {verdict} (final-round d_pass@1 = {100*delta:+.1f}, CI [{100*lo_:+.1f}, {100*hi_:+.1f}])")


if __name__ == "__main__":
    main()
