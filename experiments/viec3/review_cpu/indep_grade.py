"""Independent grader for the final-round runs: normalised string match of the LAST \\boxed{} against the gold.
No math-verify involved. Prints round0->last change (pass@1 = first sample, sample acc = mean over k) with a
paired problem-level bootstrap interval, for the exam dataset (math500).
    python experiments/viec3/review_cpu/indep_grade.py RUN_DIR [RUN_DIR ...]
"""
import json, random, re, sys
from pathlib import Path


def last_boxed(t):
    i = t.rfind("\\boxed")
    if i < 0:
        return None
    j = t.find("{", i)
    if j < 0:
        return None
    d = 0
    for k in range(j, len(t)):
        d += (t[k] == "{") - (t[k] == "}")
        if d == 0:
            return t[j + 1:k]
    return None


def norm(s):
    s = s.strip()
    m = re.fullmatch(r"\$+(.*?)\$+", s, re.S)
    s = m.group(1) if m else s
    b = last_boxed(s) if "\\boxed" in s else None
    s = b if b is not None else s
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\!", "").replace("\\,", "").replace("\\ ", "").replace("^\\circ", "").replace("^{\\circ}", "")
    s = re.sub(r"\\frac(\d)(\d)", r"\\frac{\1}{\2}", s)
    s = re.sub(r"\s+", "", s).rstrip(".")
    return s


def load(run):
    out = {}
    for l in (run / "generations.jsonl").open(encoding="utf-8"):
        d = json.loads(l)
        if d["dataset"] != "math500":
            continue
        g = norm(d["gold"])
        fl = []
        for t in d["texts"]:
            b = last_boxed(t)
            fl.append(b is not None and norm(b) == g)
        out.setdefault(d["round"], {})[d["item_id"]] = fl
    return out


def stat(r0, rl, ids):
    p1 = 100 * sum(rl[i][0] - r0[i][0] for i in ids) / len(ids)
    sa = 100 * sum(sum(rl[i]) / len(rl[i]) - sum(r0[i]) / len(r0[i]) for i in ids) / len(ids)
    return p1, sa


for a in sys.argv[1:]:
    run = Path(a)
    R = load(run)
    last = max(R)
    r0, rl = R[0], R[last]
    ids = sorted(set(r0) & set(rl))
    rng = random.Random(0)
    bs = [stat(r0, rl, [rng.choice(ids) for _ in ids]) for _ in range(2000)]
    p1, sa = stat(r0, rl, ids)
    ci = lambda k: (sorted(b[k] for b in bs)[50], sorted(b[k] for b in bs)[1949])
    acc0 = 100 * sum(sum(r0[i]) / len(r0[i]) for i in ids) / len(ids)
    print(f"{run.name}: n={len(ids)} round0 sample-acc {acc0:.1f} | d pass@1 {p1:+.1f} [{ci(0)[0]:+.1f},{ci(0)[1]:+.1f}] | d sample-acc {sa:+.1f} [{ci(1)[0]:+.1f},{ci(1)[1]:+.1f}]")
