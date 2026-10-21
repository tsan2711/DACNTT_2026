import json, random, sys
from pathlib import Path
R = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/results/viec3")
SC = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu/scored")
TC = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu/tokcache")
BX = "\\boxed"


def exam(seed, ids):
    ids = sorted(ids); random.Random(seed).shuffle(ids); return set(ids[:150])


def load(run):
    m = json.loads((R / run / "manifest.json").read_text())
    flags = {(r["round"], r["item_id"]): r["flags"] for r in json.loads((SC / f"{run}.json").read_text())}
    toks = {tuple(json.loads(k)): v for k, v in json.loads((TC / f"{run}.json").read_text()).items()}
    gens = {}
    for l in open(R / run / "generations.jsonl"):
        r = json.loads(l); gens[(r["round"], r["item_id"])] = (r["gold"], r["texts"])
    ex = exam(m["seed"], [i for (rd, i) in flags if rd == 0])
    return m, flags, toks, gens, ex


def pct(a, b): return 100 * a / max(1, b)


RUNS = ["a-math500-lr-fixed", "b-math500-lr-fixed", "a-math500-lr-fixed-seed2", "b-math500-lr-fixed-seed2",
        "nofilter-math500-lr-fixed", "nofilter-math500-seed2", "a-lr2e4-seed1", "a-lr2e4-seed2",
        "a-math500-lr1e4", "a-lr1e4-seed2", "a-lr1e4-seed3", "qwen15b-math500-a", "qwen15b-math500-a-seed1",
        "gold-math500-lr-fixed", "gold-math500-seed2", "c-gsm8k-lr5e4", "qwen15b-gsm8k-c", "a-lr5e4-msl1024", "a-lr5e4-keep"]
for run in (sys.argv[1:] or RUNS):
    m, flags, toks, gens, ex = load(run); last = max(rd for rd, _ in flags)
    out = [run + f" R{last}"]
    for rd in (0, last):
        E = [(f, n, t) for i in ex for f, n, t in zip(flags[(rd, i)], toks[(rd, i)], gens[(rd, i)][1])]
        fin = [x for x in E if x[1] < 508]
        prox = [len(t) > 1500 and BX not in t for _, _, t in E]; cap = [n >= 508 for _, n, _ in E]
        both = sum(p and c for p, c in zip(prox, cap))
        sel = [f for (r2, i), fl in flags.items() if r2 == rd and i not in ex for f in fl]
        exa = [f for _, _, f in [(0, 0, x[0]) for x in E]]
        pool = [(n, t) for (r2, i), fl in flags.items() if r2 == rd and i not in ex
                for f, n, t in zip(fl, toks[(r2, i)], gens[(r2, i)][1]) if f]
        selgen = [(n, t) for (r2, i), fl in flags.items() if r2 == rd and i not in ex
                  for n, t in zip(toks[(r2, i)], gens[(r2, i)][1])]
        out.append(
            f"[R{rd}] boxed all {pct(sum(BX in t for _,_,t in E),len(E)):.1f} fin {pct(sum(BX in t for _,_,t in fin),len(fin)):.1f}"
            f" | proxy {pct(sum(prox),len(E)):.1f} cap {pct(sum(cap),len(E)):.1f} proxy&cap/proxy {pct(both,sum(prox)):.0f}% cap&proxy/cap {pct(both,sum(cap)):.0f}%"
            f" | >=500 {pct(sum(n>=500 for _,n,_ in E),len(E)):.1f} >=512 {pct(sum(n>=512 for _,n,_ in E),len(E)):.1f} n480-507 {sum(480<=n<508 for _,n,_ in E)} max {max(n for _,n,_ in E)}"
            f" | exam sacc {pct(sum(exa),len(exa)):.1f} sel sacc {pct(sum(sel),len(sel)):.1f}"
            f" | selgen boxed {pct(sum(BX in t for _,t in selgen),len(selgen)):.1f} pool n {len(pool)} boxed {pct(sum(BX in t for _,t in pool),len(pool)):.1f} caphit {pct(sum(n>=508 for n,_ in pool),len(pool)):.1f} ({sum(n>=508 for n,_ in pool)})"
            f" | len {sum(len(t) for _,_,t in E)/len(E):.0f} finacc {pct(sum(f for f,_,_ in fin),len(fin)):.1f}")
    excl = sum(1 for i in ex if all(n >= 508 for n in toks[(last, i)]))
    fb = sum(1 for i in ex if any(n < 508 for n in toks[(last, i)]) and all(n >= 508 for n in toks[(0, i)]))
    out.append(f"matched: excluded problems {excl}, fallback-R0 {fb}")
    print("\n  ".join(out), flush=True)
