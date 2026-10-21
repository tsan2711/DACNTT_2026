"""Anatomy with the DIRECT finish signal: cap-hit = decoded text re-tokenizes to >=508 tokens (gen cap 512).
Per run: cap-hit share, accuracy on non-cap-hit, difficulty-reweighted R0 baseline, bootstrap CI."""
import json, random, sys, glob, os
from pathlib import Path
from tokenizers import Tokenizer
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); SC = Path(__file__).parent / "scored"
TC = Path(__file__).parent / "tokcache"; TC.mkdir(exist_ok=True)
tok = Tokenizer.from_file(glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/*/tokenizer.json"))[0])
CAP = 508
def exam(seed, ids):
    ids = sorted(ids); random.Random(seed).shuffle(ids); return ids[:150]
def load(run):
    m = json.loads((REPO / "results/viec3" / run / "manifest.json").read_text())
    flags = {(r["round"], r["item_id"]): r["flags"] for r in json.loads((SC / f"{run}.json").read_text())}
    cf = TC / f"{run}.json"
    if cf.exists(): toks = {tuple(json.loads(k)): v for k, v in json.loads(cf.read_text()).items()}
    else:
        toks = {}
        for l in open(REPO / "results/viec3" / run / "generations.jsonl"):
            r = json.loads(l)
            toks[(r["round"], r["item_id"])] = [len(e.ids) for e in tok.encode_batch(r["texts"], add_special_tokens=False)]
        cf.write_text(json.dumps({json.dumps(list(k)): v for k, v in toks.items()}))
    ex = exam(m["seed"], [i for (rd, i) in flags if rd == 0])
    return m, flags, toks, ex
def comp(flags, toks, s, r0, r1):
    num = den = rw = 0
    for i in s:
        f1 = [f for f, n in zip(flags[(r1, i)], toks[(r1, i)]) if n < CAP]
        if not f1: continue
        f0 = [f for f, n in zip(flags[(r0, i)], toks[(r0, i)]) if n < CAP]
        p0 = sum(f0) / len(f0) if f0 else sum(flags[(r0, i)]) / len(flags[(r0, i)])
        num += sum(f1); den += len(f1); rw += len(f1) * p0
    return num / den, rw / den
def rstats(flags, toks, ex, rd):
    F = [f for i in ex for f in flags[(rd, i)]]; N = [n for i in ex for n in toks[(rd, i)]]
    fin = [f for f, n in zip(F, N) if n < CAP]; capf = [f for f, n in zip(F, N) if n >= CAP]
    return 100 * sum(n >= CAP for n in N) / len(N), 100 * sum(fin) / len(fin), 100 * sum(capf) / max(1, len(capf)), 100 * sum(F) / len(F)
print("| run | cap-hit R0→R_last | finished(non-cap) acc R0→R_last | cap-hit acc R0→R_last | R0 reweighted to R_last finished mix | Δ finished vs reweighted [95% CI] |")
print("|---|---|---|---|---|---|")
for run in sys.argv[1:]:
    m, flags, toks, ex = load(run); last = max(rd for rd, _ in flags)
    a0, a1 = rstats(flags, toks, ex, 0), rstats(flags, toks, ex, last)
    acc, rw = comp(flags, toks, ex, 0, last)
    rng = random.Random(0); ds = []
    for _ in range(2000):
        s = [rng.choice(ex) for _ in ex]; x, y = comp(flags, toks, s, 0, last); ds.append(x - y)
    ds.sort()
    print(f"| {run} (R{last}) | {a0[0]:.1f}→{a1[0]:.1f} | {a0[1]:.1f}→{a1[1]:.1f} | {a0[2]:.1f}→{a1[2]:.1f} | {100*rw:.1f} | {100*(acc-rw):+.1f} [{100*ds[50]:+.1f}, {100*ds[1949]:+.1f}] |", flush=True)
