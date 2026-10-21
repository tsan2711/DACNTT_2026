import json, random
from pathlib import Path
R = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/results/viec3")
P = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu/patched")
SC = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu/scored")
def exam(seed, ids):
    ids = sorted(ids); random.Random(seed).shuffle(ids); return ids[:150]
for run in ["a-math500-lr-fixed","a-math500-lr-fixed-seed2","qwen15b-math500-a","gold-math500-lr-fixed","gold-math500-seed2"]:
    m = json.loads((R/run/"manifest.json").read_text())
    pf = {(r["round"], r["item_id"]): r["boxed"] for r in json.loads((P/f"{run}.json").read_text())}
    of = {(r["round"], r["item_id"]): r["flags"] for r in json.loads((SC/f"{run}.json").read_text())}
    ex = exam(m["seed"], [i for (rd,i) in pf if rd==0]); last = max(rd for rd,_ in pf)
    def stats(fl, s, rd):
        p1 = sum(fl[(rd,i)][0] for i in s)/len(s); sa = sum(sum(fl[(rd,i)]) for i in s)/sum(len(fl[(rd,i)]) for i in s)
        pk = sum(any(fl[(rd,i)]) for i in s)/len(s); return p1, pk, sa
    rng = random.Random(0); bs = {"p1":[], "pk":[], "sa":[]}
    for _ in range(10000):
        s = [rng.choice(ex) for _ in ex]
        a, b = stats(pf, s, 0), stats(pf, s, last)
        for j,kk in enumerate(["p1","pk","sa"]): bs[kk].append(b[j]-a[j])
    a, b = stats(pf, ex, 0), stats(pf, ex, last); o0, o1 = stats(of, ex, 0), stats(of, ex, last)
    out=[]
    for j,kk in enumerate(["p1","pk","sa"]):
        v = sorted(bs[kk]); out.append(f"{kk} {100*a[j]:.1f}->{100*b[j]:.1f} d {100*(b[j]-a[j]):+.1f} [{100*v[250]:+.1f},{100*v[9749]:+.1f}] (orig {100*o0[j]:.1f}->{100*o1[j]:.1f})")
    print(run, f"R{last}", " | ".join(out))
