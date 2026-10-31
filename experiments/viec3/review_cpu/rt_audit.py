# Kiểm toán r_t (lỗi lưu gold) cho bản sửa paper: r_t theo vòng + bootstrap theo bài cho thay đổi R0→cuối,
# r_t chỉ trên bài giải có \boxed, r_t trong các bài "dính lỗi", và tách bài có gold không parse được.
# Dữ liệu: patched/*.json (frac = verifier gốc, boxed = V' bọc gold) + results/viec3/<run>/generations.jsonl (văn bản).
import json, sys, random, collections
from pathlib import Path
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); sys.path.insert(0, str(REPO / "src"))
from dacntt.verify.adapter import MathVerifyAdapter
P = REPO / "experiments/viec3/review_cpu/patched"
RUNS = ["a-math500-lr-fixed", "a-math500-lr-fixed-seed2", "qwen15b-math500-a", "gold-math500-lr-fixed", "gold-math500-seed2"]
B = 2000

def load(run):
    pat = json.loads((P / f"{run}.json").read_text())
    texts, gold = {}, {}
    for l in open(REPO / f"results/viec3/{run}/generations.jsonl"):
        r = json.loads(l); texts[(r["round"], r["item_id"])] = r["texts"]; gold[r["item_id"]] = r["gold"]
    by = collections.defaultdict(dict)
    for r in pat:
        t = texts[(r["round"], r["item_id"])]
        by[r["round"]][r["item_id"]] = [(a, b, "\\boxed" in x) for a, b, x in zip(r["frac"], r["boxed"], t)]
    return by, gold

def counts(by, rd, items, boxed_only=False, first_only=False):
    n = d = 0
    for i in items:
        g = by[rd][i][:1] if first_only else by[rd][i]
        for a, b, bx in g:
            if boxed_only and not bx: continue
            if b: d += 1; n += (not a)
    return n, d

def rate(by, rd, items, **kw):
    n, d = counts(by, rd, items, **kw); return 100 * n / d if d else float("nan")

def ci(xs):
    xs = sorted(xs); return xs[int(.025 * len(xs))], xs[int(.975 * len(xs)) - 1]

a0 = MathVerifyAdapter("reward", timeout_seconds=5)
rng = random.Random(0)
for run in RUNS:
    by, gold = load(run); rounds = sorted(by); last = rounds[-1]; items = sorted(by[0])
    unp = {i for i in items if a0.verify(gold[i], "\\boxed{" + gold[i] + "}").gold_parsed_empty}
    elig = {i for rd in rounds for i in items if any(b and not a for a, b, _ in by[rd][i])}
    print(f"\n== {run}: {len(items)} problems, unparseable gold {len(unp)}, defect-eligible {len(elig)} "
          f"(of which unparseable {len(elig & unp)})")
    for name, kw, its in [("r_t all", {}, items), ("r_t boxed-only", {"boxed_only": True}, items),
                          ("r_t pass@1 (first sample)", {"first_only": True}, items),
                          ("r_t within eligible", {}, sorted(elig)), ("r_t excl. unparseable", {}, [i for i in items if i not in unp])]:
        vals = [rate(by, rd, its, **kw) for rd in rounds]
        bs = []
        for _ in range(B):
            s = [rng.choice(its) for _ in its]
            bs.append(rate(by, last, s, **kw) - rate(by, 0, s, **kw))
        lo, hi = ci(bs)
        print(f"  {name:28s} " + " → ".join(f"{v:.1f}" for v in vals) + f"   Δ {vals[-1]-vals[0]:+.1f} [{lo:+.1f}, {hi:+.1f}]")
    # Bài dính lỗi mà gold parse được: chỉ ở đây mô hình mới có cách viết để V chấp nhận.
    ep = sorted(elig - unp)
    vals = [rate(by, rd, ep) for rd in rounds]
    bs = []
    for _ in range(B):
        s = [rng.choice(ep) for _ in ep]; bs.append(rate(by, last, s) - rate(by, 0, s))
    lo, hi = ci(bs)
    print(f"  {'r_t eligible & parseable':28s} " + " → ".join(f"{v:.1f}" for v in vals)
          + f"   Δ {vals[-1]-vals[0]:+.1f} [{lo:+.1f}, {hi:+.1f}]  (n={len(ep)} problems)")
    # Áp lực huấn luyện: số mẫu V chấp nhận trên bài dính lỗi thuộc tập selection (= vào pool) ở mỗi vòng
    m = json.loads((REPO / f"results/viec3/{run}/manifest.json").read_text())
    ids = sorted(items); random.Random(m["seed"]).shuffle(ids); exam = set(ids[:150])
    pool_elig = [sum(a for i in elig - exam for a, _, _ in by[rd][i]) for rd in rounds]
    pool_all = [sum(a for i in set(items) - exam for a, _, _ in by[rd][i]) for rd in rounds]
    print(f"  pool examples on eligible problems (V-accepted, selection set) per round: {pool_elig} of pool {pool_all}")
    # \boxed share among V'-accepted, and share of eligible problems solved (V') per round
    for rd in rounds:
        acc = [(a, b, bx) for i in items for a, b, bx in by[rd][i] if b]
        solved = sum(1 for i in elig if any(b for _, b, _ in by[rd][i]))
        print(f"  R{rd}: V' accepts {len(acc)}, boxed share {100*sum(bx for *_, bx in acc)/len(acc):.1f}%, "
              f"eligible problems with ≥1 V' accept {solved}/{len(elig)}")
