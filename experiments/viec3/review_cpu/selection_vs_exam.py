"""Sample-accuracy change on the selection problems vs the held-out exam, both graded with V'
(same adapter and timeouts as regrade_all.py). Cited in the supplementary, Design P section.
    .venv/bin/python -m experiments.viec3.review_cpu.selection_vs_exam
"""
from __future__ import annotations

import json
from multiprocessing import Pool

from experiments.viec3.regrade_all import (OUT, RES, RETRY_TIMEOUT, RUNS, _adapter, _exam_keys, _grade_rec,
                                           verify_flag)

LABELS = ["A_5e-4_s1", "A_5e-4_s2", "A_1e-4_s1", "A_1e-5_s0", "A_1e-5_s1", "C_5e-4_s1", "C_1e-5_s0"]


def main() -> None:
    with Pool() as pool:
        for label in LABELS:
            d = RES / RUNS[label]
            man = json.loads((d / "manifest.json").read_text())
            recs = [json.loads(l) for l in (d / "generations.jsonl").open(encoding="utf-8")]
            exam = _exam_keys(man, recs)
            last = max(r["round"] for r in recs)
            sel = [r for r in recs if r["round"] in (0, last) and (r["dataset"], r["item_id"]) not in exam]
            graded = pool.map(_grade_rec, sel, chunksize=4)
            by = {(r["round"], r["dataset"], r["item_id"]): r for r in sel}
            ad = _adapter(RETRY_TIMEOUT)
            still = 0
            for g in graded:  # retry timeouts alone, as in regrade_all
                for i, why in enumerate(g["reason"]):
                    if why == "timeout":
                        rec = by[(g["round"], g["dataset"], g["item_id"])]
                        g["v"][i], to = verify_flag(ad, rec["gold"], rec["texts"][i])
                        still += to
            flags = json.loads((OUT / "flags" / f"{label}.json").read_text())["rows"]

            def acc(rows, rd):
                f = [v for g in rows if g["round"] == rd for v in g["v"]]
                return 100 * sum(f) / len(f)

            n = len({(g["dataset"], g["item_id"]) for g in graded})
            s = acc(graded, last) - acc(graded, 0)
            e = acc(flags, last) - acc(flags, 0)
            print(f"{label}: R0->R{last} selection (n={n}) {acc(graded, 0):.1f}->{acc(graded, last):.1f} "
                  f"({s:+.1f}); exam {acc(flags, 0):.1f}->{acc(flags, last):.1f} ({e:+.1f}); timeouts left {still}",
                  flush=True)


if __name__ == "__main__":
    main()
