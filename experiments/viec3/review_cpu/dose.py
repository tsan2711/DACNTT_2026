import json, random
from pathlib import Path
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); P = Path(__file__).parent
for run in ["a-math500-lr-fixed","a-math500-lr-fixed-seed2","gold-math500-lr-fixed","gold-math500-seed2","qwen15b-math500-a"]:
    m = json.loads((REPO/"results/viec3"/run/"manifest.json").read_text())
    base = {(r["round"],r["item_id"]): r["flags"] for r in json.loads((P/"scored"/f"{run}.json").read_text())}
    pat = {(r["round"],r["item_id"]): r for r in json.loads((P/"patched"/f"{run}.json").read_text())}
    ids = sorted({i for (rd,i) in base if rd==0}); random.Random(m["seed"]).shuffle(ids)
    n_ex = round(len(ids)*m.get("holdout_frac",0.3)); ex=set(ids[:n_ex]); sel=[i for i in ids if i not in ex]
    for rd in sorted({rd for rd,_ in base}):
        out=[]
        for v in ("frac","boxed","both"):
            kb = sum(sum(base[(rd,i)]) for i in sel); kp = sum(sum(pat[(rd,i)][v]) for i in sel)
            ntot = sum(len(base[(rd,i)]) for i in sel)
            p1b = sum(base[(rd,i)][0] for i in ex)/len(ex); p1p = sum(pat[(rd,i)][v][0] for i in ex)/len(ex)
            sb = sum(sum(base[(rd,i)]) for i in ex)/sum(len(base[(rd,i)]) for i in ex); sp = sum(sum(pat[(rd,i)][v]) for i in ex)/sum(len(base[(rd,i)]) for i in ex)
            out.append(f"{v}: pool {kb}->{kp} (+{kp-kb}, {100*(kp-kb)/kb:.1f}% of kept, {100*(kp-kb)/ntot:.2f}% of sel gens); exam p@1 {100*p1b:.1f}->{100*p1p:.1f}, sample acc {100*sb:.1f}->{100*sp:.1f}")
        print(run, "R", rd, "|", " || ".join(out))
