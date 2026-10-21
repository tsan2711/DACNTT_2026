"""String-identity audit of rejected exam answers: how many rejected generations have a final boxed answer
that equals the gold after light normalisation (a lower bound on verifier false negatives)."""
import json, random, re
from pathlib import Path
R = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/results/viec3")
SC = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu/scored")


def exam(seed, ids):
    ids = sorted(ids); random.Random(seed).shuffle(ids); return set(ids[:150])


def last_boxed(t):
    i = t.rfind("\\boxed{")
    if i < 0: return None
    j = i + 7; d = 1; s = j
    while j < len(t) and d:
        d += {"{": 1, "}": -1}.get(t[j], 0); j += 1
    return t[s:j - 1] if d == 0 else None


def norm(s):
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\!", "").replace("\\,", "").replace("^\\circ", "").replace("^{\\circ}", "").replace("$", "")
    s = re.sub(r"\\text\{\s*([^}]*)\}", r"\1", s)
    s = re.sub(r"\s+", "", s).rstrip(".")
    return s


for run in ["gold-math500-lr-fixed", "gold-math500-seed2", "a-math500-lr-fixed", "a-math500-lr-fixed-seed2"]:
    m = json.loads((R / run / "manifest.json").read_text())
    flags = {(r["round"], r["item_id"]): r["flags"] for r in json.loads((SC / f"{run}.json").read_text())}
    gens = {}
    for l in open(R / run / "generations.jsonl"):
        r = json.loads(l); gens[(r["round"], r["item_id"])] = (r["gold"], r["texts"])
    ex = exam(m["seed"], [i for (rd, i) in flags if rd == 0])
    for rd in (0, 2):
        rej = nob = match = tot = 0
        for i in ex:
            g, ts = gens[(rd, i)]
            for f, t in zip(flags[(rd, i)], ts):
                tot += 1
                if f: continue
                rej += 1
                b = last_boxed(t)
                if b is None: nob += 1; continue
                if norm(b) == norm(g): match += 1
        print(f"{run} R{rd}: gens {tot} rejected {rej} no-box {nob} boxed==gold(norm) {match} ({100*match/max(1,rej):.1f}% of rejected)")
