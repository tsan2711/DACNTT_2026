"""Token-cap hit rate vs the 1500-char/no-boxed proxy, on exam generations (Qwen tokenizer, CPU)."""
import json, random, sys
from pathlib import Path
from tokenizers import Tokenizer
import glob, os

REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026")
tok = Tokenizer.from_file(glob.glob(os.path.expanduser(
    "~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/*/tokenizer.json"))[0])
SC = Path(__file__).parent / "scored"


def exam(m, ids):
    ids = sorted(ids)
    random.Random(m["seed"]).shuffle(ids)
    return set(ids[:150])


for run in sys.argv[1:]:
    m = json.loads((REPO / "results/viec3" / run / "manifest.json").read_text())
    recs = [json.loads(l) for l in open(REPO / "results/viec3" / run / "generations.jsonl")]
    flags = {(r["round"], r["item_id"]): r["flags"] for r in json.loads((SC / f"{run}.json").read_text())}
    ex = exam(m, {r["item_id"] for r in recs if r["round"] == 0})
    for rnd in sorted({r["round"] for r in recs}):
        rows = []
        for r in recs:
            if r["round"] != rnd or r["item_id"] not in ex:
                continue
            for t, f in zip(r["texts"], flags[(rnd, r["item_id"])]):
                n = len(tok.encode(t, add_special_tokens=False).ids)
                rows.append((n, len(t), "\\boxed" in t, f))
        cap = [n >= 508 for n, *_ in rows]
        prox = [l > 1500 and not b for n, l, b, f in rows]
        both = sum(c and p for c, p in zip(cap, prox))
        cap_nob = sum(c and not b for c, (n, l, b, f) in zip(cap, rows))
        fin_cap = [f for c, (n, l, b, f) in zip(cap, rows) if not c]
        degc = [n_l for c, n_l in zip(prox, rows) if c]
        cpt = (sum(l for n, l, b, f in degc) / max(1, sum(n for n, l, b, f in degc))) if degc else float("nan")
        cpt_f = sum(l for (n, l, b, f), p in zip(rows, prox) if not p) / max(1, sum(n for (n, l, b, f), p in zip(rows, prox) if not p))
        print(f"{run} R{rnd}: n={len(rows)} cap-hit(>=508 tok) {100*sum(cap)/len(rows):.1f}% | proxy {100*sum(prox)/len(rows):.1f}% | "
              f"proxy∩cap {both} | cap-hit & no boxed {100*cap_nob/len(rows):.1f}% | acc on non-cap-hit {100*sum(fin_cap)/len(fin_cap):.1f}% | "
              f"chars/token degenerate {cpt:.2f} vs others {cpt_f:.2f}", flush=True)
