import json, random, sys, statistics
sys.path.insert(0, "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/src")
from dacntt.verify.adapter import MathVerifyAdapter

R = "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/results/viec3/"

def split(ids, seed, frac=0.3):
    rng = random.Random(seed)
    ids = sorted(ids); rng.shuffle(ids)
    return set(ids[:max(1, round(len(ids) * frac))])

for run in sys.argv[1:]:
    man = json.load(open(R + run + "/manifest.json"))
    patch = man.get("patch_verifier", False)
    v = MathVerifyAdapter("reward", timeout_seconds=3, normalize_frac_commands=patch)
    recs = [json.loads(l) for l in open(R + run + "/generations.jsonl")]
    rounds = sorted({r["round"] for r in recs})
    ids = {r["item_id"] for r in recs if r["round"] == 0}
    exam = split(ids, man["seed"]) if man.get("holdout_frac", 0) > 0 else ids
    for rd in rounds:
        rows = [r for r in recs if r["round"] == rd and r["item_id"] in exam]
        flags, texts = [], []
        for r in rows:
            f = [v.verify(r["gold"], t).accepted for t in r["texts"]]
            flags.append(f); texts += r["texts"]
        flat = [x for f in flags for x in f]
        deg = [len(t) > 1500 and "\\boxed" not in t for t in texts]
        done = [x for x, d in zip(flat, deg) if not d]
        degacc = [x for x, d in zip(flat, deg) if d]
        print(run, "seed", man["seed"], "r", rd, "n_items", len(rows), "n", len(flat),
              "p1 %.1f" % (100 * sum(f[0] for f in flags) / len(flags)),
              "pk %.1f" % (100 * sum(any(f) for f in flags) / len(flags)),
              "sacc %.2f" % (100 * sum(flat) / len(flat)),
              "len %.0f" % statistics.mean(len(t) for t in texts),
              "deg %.2f" % (100 * sum(deg) / len(deg)),
              "nd_acc %.2f" % (100 * sum(done) / len(done)),
              "deg_acc %.2f" % (100 * sum(degacc) / max(1, len(degacc))), flush=True)
