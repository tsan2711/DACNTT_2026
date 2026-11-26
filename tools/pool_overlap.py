"""Content-level overlap between the MATH-train pool (PRM800K split, 12,000)
and the MATH-500 exam: exact normalised match + shared 13-gram of problem text.

Usage: python3 tools/pool_overlap.py data/gold/mathtrain.jsonl data/gold/math500_test.jsonl
"""
import json, re, sys

def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9$\\{}^_=+\-*/()., ]", " ", t.lower())).strip()

def load(path):
    out = []
    for line in open(path):
        r = json.loads(line)
        out.append(r.get("problem") or r.get("question") or "")
    return out

def grams(t, n=13):
    w = norm(t).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}

train, exam = load(sys.argv[1]), load(sys.argv[2])
ex_norm = {norm(t): i for i, t in enumerate(exam)}
exact = [i for i, t in enumerate(train) if norm(t) in ex_norm]
index = {}
for j, t in enumerate(exam):
    for g in grams(t):
        index.setdefault(g, set()).add(j)
hit = set()
for i, t in enumerate(train):
    for g in grams(t):
        if g in index:
            hit.add(i); break
short = sum(1 for t in exam if len(norm(t).split()) < 13)
print(f"train={len(train)} exam={len(exam)} exact={len(exact)} 13gram_overlap_train_problems={len(hit)} exam_problems_shorter_than_13_words={short}")
