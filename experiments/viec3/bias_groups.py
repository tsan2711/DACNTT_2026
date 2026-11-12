"""Boxed share on biased vs other problems, round 0 -> last, per run.

    .venv/bin/python -m experiments.viec3.bias_groups RUN_DIR [--B 5000]

For the content-learnable injected bias (--inject-bias-content) the select
verifier rejects every \\boxed answer whose gold contains \\frac/\\dfrac. A model
that learns the verifier should stop boxing on those problems more than on the
rest. Reports, per group, the share of generations containing \\boxed in round
0 and the last round, the change, and a paired problem-level bootstrap interval
for the change. The difference-in-differences (biased minus other) is the
quantity to compare with an unbiased run (pass --ref RUN_DIR2). CPU only; no
verification needed, so it is fast.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

BIASED = re.compile(r"\\[dt]?frac")
BOXED = re.compile(r"\\boxed")


def load(run: Path) -> dict[int, dict[str, tuple[bool, list[bool]]]]:
    out: dict[int, dict[str, tuple[bool, list[bool]]]] = {}
    for line in (run / "generations.jsonl").open(encoding="utf-8"):
        d = json.loads(line)
        if d.get("dataset") != "math500":
            continue
        out.setdefault(d["round"], {})[d["item_id"]] = (
            bool(BIASED.search(d["gold"])),
            [bool(BOXED.search(t)) for t in d["texts"]],
        )
    return out


def share(items: list[tuple[bool, list[bool]]], grp: bool) -> float:
    xs = [b for g, bs in items if g == grp for b in bs]
    return sum(xs) / len(xs) if xs else float("nan")


def stats(rounds: dict, last: int, ids: list[str]) -> dict[str, float]:
    r0 = [rounds[0][i] for i in ids]
    r1 = [rounds[last][i] for i in ids]
    out = {}
    for name, grp in (("biased", True), ("other", False)):
        out[name] = 100 * (share(r1, grp) - share(r0, grp))
    out["did"] = out["biased"] - out["other"]
    return out


def boot(rounds: dict, last: int, B: int, seed: int = 0) -> dict[str, tuple[float, float]]:
    ids = sorted(set(rounds[0]) & set(rounds[last]))
    rng = random.Random(seed)
    acc: dict[str, list[float]] = {"biased": [], "other": [], "did": []}
    for _ in range(B):
        s = stats(rounds, last, [rng.choice(ids) for _ in ids])
        for k in acc:
            acc[k].append(s[k])
    return {k: (sorted(v)[int(0.025 * B)], sorted(v)[int(0.975 * B)]) for k, v in acc.items()}


def report(run: Path, B: int) -> None:
    rounds = load(run)
    last = max(rounds)
    ids = sorted(set(rounds[0]) & set(rounds[last]))
    n_b = sum(rounds[0][i][0] for i in ids)
    s = stats(rounds, last, ids)
    ci = boot(rounds, last, B)
    r0 = [rounds[0][i] for i in ids]
    r1 = [rounds[last][i] for i in ids]
    print(f"{run.name}: {n_b} biased / {len(ids) - n_b} other problems")
    for g, lab in ((True, "biased"), (False, "other ")):
        print(
            f"  {lab} boxed share {100 * share(r0, g):.1f}% -> {100 * share(r1, g):.1f}% "
            f"(change {s['biased' if g else 'other']:+.1f}, 95% CI "
            f"[{ci['biased' if g else 'other'][0]:+.1f}, {ci['biased' if g else 'other'][1]:+.1f}])"
        )
    print(f"  biased minus other: {s['did']:+.1f} [{ci['did'][0]:+.1f}, {ci['did'][1]:+.1f}]")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--B", type=int, default=5000)
    a = ap.parse_args()
    for r in a.runs:
        report(r, a.B)


if __name__ == "__main__":
    main()
