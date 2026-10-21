import json, re, random, collections
from pathlib import Path
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); P = Path(__file__).parent
run="a-math500-lr-fixed"
pat = {(r["round"],r["item_id"]): r for r in json.loads((P/"patched"/f"{run}.json").read_text())}
def lastbox(t):
    i=t.rfind("\\boxed{"); 
    if i<0: return None
    j=i+7; d=1; s=j
    while j<len(t) and d: 
        d+= {'{':1,'}':-1}.get(t[j],0); j+=1
    return t[s:j-1]
fl=[]; golds=collections.Counter()
for l in open(REPO/"results/viec3"/run/"generations.jsonl"):
    r=json.loads(l)
    if r["round"]!=0: continue
    p=pat[(0,r["item_id"])]
    for t,a,b in zip(r["texts"],p["frac"],p["boxed"]):
        if b and not a: fl.append((r["gold"], lastbox(t))); golds[r["gold"]]+=1
print(len(fl), "flips; distinct golds", len(golds))
random.Random(0).shuffle(fl)
for g,b in fl[:30]: print(repr(g)," | ",repr(b))
