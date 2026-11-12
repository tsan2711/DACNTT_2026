"""Split the final-round exam by whether math-verify can parse the gold, and report pass@1 change per group.
Grader: math-verify (default parse of gold, default parse of the generation, verify).
    PYTHONPATH=src python experiments/viec3/review_cpu/unparse_split.py RUN_DIR [...]
"""
import json, sys
from pathlib import Path
from dacntt.verify.adapter import MathVerifyAdapter

# the final-round exam verifier (manifest: preset reward, patch_verifier + patch_verifier_boxed)
V = MathVerifyAdapter("reward", normalize_frac_commands=True, normalize_gold_boxed=True)


for a in sys.argv[1:]:
    run = Path(a)
    rows = {}
    for l in (run / "generations.jsonl").open(encoding="utf-8"):
        d = json.loads(l)
        if d["dataset"] != "math500":
            continue
        rows.setdefault(d["round"], {})[d["item_id"]] = d
    last = max(rows)
    ids = sorted(set(rows[0]) & set(rows[last]))
    # a gold is "unparseable" if V reports gold_parsed_empty when verified against a plain (unboxed) probe
    gp = {i: not V.verify(rows[0][i]["gold"], "The answer is x").gold_parsed_empty for i in ids}
    groups = {"all": ids, "parseable": [i for i in ids if gp[i]], "unparseable": [i for i in ids if not gp[i]]}
    out = [f"{run.name}: n={len(ids)}"]
    for name, g in groups.items():
        if not g:
            continue
        r0 = sum(V.verify(rows[0][i]["gold"], rows[0][i]["texts"][0]).accepted for i in g)
        rl = sum(V.verify(rows[last][i]["gold"], rows[last][i]["texts"][0]).accepted for i in g)
        out.append(f"{name} n={len(g)} pass@1 {100*r0/len(g):.1f}->{100*rl/len(g):.1f} ({100*(rl-r0)/len(g):+.1f})")
    print(" | ".join(out))
