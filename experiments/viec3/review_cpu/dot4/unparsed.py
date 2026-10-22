# Bao nhiêu trong 51 gold không parse được trở nên parse được khi bọc \boxed (re-score gold-storage)?
import json, sys
from pathlib import Path
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); sys.path.insert(0, str(REPO/"src"))
from dacntt.verify.adapter import MathVerifyAdapter
recs = {}
for l in open(REPO/"results/viec3/a-math500-lr-fixed/generations.jsonl"):
    r = json.loads(l); recs.setdefault(r["item_id"], r["gold"])
a0 = MathVerifyAdapter("reward", timeout_seconds=5)
a1 = MathVerifyAdapter("reward", timeout_seconds=5, normalize_gold_boxed=True)
n = un = fixed = 0
for iid, g in recs.items():
    n += 1
    if a0.verify(g, r"\boxed{" + g + "}").gold_parsed_empty:
        un += 1
        if not a1.verify(g, r"\boxed{" + g + "}").gold_parsed_empty and a1.verify(g, r"\boxed{" + g + "}").accepted:
            fixed += 1
print(f"items {n} unparseable {un} accepted-after-boxed-wrap {fixed}")
