"""Anatomy of a final-round run on the MATH-500 exam: boxed share, accuracy among boxed answers
(string-match grader of indep_grade.py), median generation length (characters), per round.
    python experiments/viec3/review_cpu/gate_anatomy.py RUN_DIR [RUN_DIR ...]
"""
import json, re, statistics as st, sys
from pathlib import Path

src = (Path(__file__).parent / "indep_grade.py").read_text().split("for a in sys.argv")[0]
exec(src)
for a in sys.argv[1:]:
    run = Path(a)
    rows = [json.loads(l) for l in (run / "generations.jsonl").open(encoding="utf-8")]
    print(run.name)
    for rd in sorted({r["round"] for r in rows}):
        n = bx = ok = 0
        L = []
        for r in rows:
            if r["round"] != rd or r["dataset"] != "math500":
                continue
            g = norm(r["gold"])
            for t in r["texts"]:
                n += 1
                L.append(len(t))
                b = last_boxed(t)
                if b is not None:
                    bx += 1
                    ok += norm(b) == g
        print(f"  round {rd}: n={n} boxed={100*bx/n:.1f}% acc|boxed={100*ok/max(bx,1):.1f}% median_len={st.median(L):.0f}")
