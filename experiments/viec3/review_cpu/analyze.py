"""CPU analyses for REVIEW-VERIFIED.md, on scratchpad/scored/*.json (re-verified flags)."""
import json, random, math, statistics as st
from pathlib import Path

REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026")
SC = Path(__file__).parent / "scored"
RES = REPO / "results/viec3"
DEG = 1500
B = 4000  # bootstrap reps


def load(run):
    m = json.loads((RES / run / "manifest.json").read_text())
    rows = json.loads((SC / f"{run}.json").read_text())
    by = {}
    for r in rows:
        by.setdefault(r["round"], {})[r["item_id"]] = r
    return m, by


def exam_ids(m, by):
    if not m.get("holdout_frac"):
        return sorted(by[0])
    ids = sorted(by[0])  # single dataset runs
    rng = random.Random(m["seed"] if m.get("seed") is not None else 0)
    rng.shuffle(ids)
    return set(ids[: max(1, round(len(ids) * m["holdout_frac"]))])


def deg(l, b):
    return l > DEG and not b


def stats(by, rnd, ids):
    recs = [by[rnd][i] for i in ids]
    p1 = sum(r["flags"][0] for r in recs) / len(recs)
    pk = sum(any(r["flags"]) for r in recs) / len(recs)
    fl = [f for r in recs for f in r["flags"]]
    L = [x for r in recs for x in r["lens"]]
    D = [deg(l, b) for r in recs for l, b in zip(r["lens"], r["boxed"])]
    fin = [f for f, d in zip(fl, D) if not d]
    dg = [f for f, d in zip(fl, D) if d]
    return dict(p1=p1, pk=pk, sacc=sum(fl) / len(fl), len=st.mean(L), deg=sum(D) / len(D),
                facc=sum(fin) / len(fin) if fin else None,
                dacc=(sum(dg) / len(dg)) if dg else None, ndeg=len(dg))


def per_item(by, rnd, ids):
    out = {}
    for i in ids:
        r = by[rnd][i]
        D = [deg(l, b) for l, b in zip(r["lens"], r["boxed"])]
        out[i] = dict(f=r["flags"], d=D)
    return out


def boot(fn, ids, reps=B, seed=0):
    ids = list(ids)
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        s = [ids[rng.randrange(len(ids))] for _ in ids]
        vals.append(fn(s))
    vals.sort()
    return vals[int(0.025 * reps)], vals[int(0.975 * reps)]


def fmt(x):
    return f"{100*x:.1f}"


def main():
    import sys
    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))
    runs = {
        "A5e-4 s1": "a-math500-lr-fixed", "A5e-4 s2": "a-math500-lr-fixed-seed2",
        "B5e-4 s1": "b-math500-lr-fixed", "B5e-4 s2": "b-math500-lr-fixed-seed2",
        "NF s1": "nofilter-math500-lr-fixed", "NF s2": "nofilter-math500-seed2",
        "GOLD s1": "gold-math500-lr-fixed", "GOLD s2": "gold-math500-seed2",
        "A1e-4 s1": "a-math500-lr1e4", "A1e-4 s2": "a-lr1e4-seed2", "A1e-4 s3": "a-lr1e4-seed3",
        "A2e-4 s1": "a-lr2e4-seed1", "A2e-4 s2": "a-lr2e4-seed2",
        "A5e-4 keep s1": "a-lr5e4-keep", "A5e-4 msl1024 s1": "a-lr5e4-msl1024",
        "C5e-4 s1": "c-gsm8k-lr5e4",
        "A1e-5 s0": "qwen15b-math500-a", "A1e-5 s1": "qwen15b-math500-a-seed1",
        "B1e-5 s0": "qwen15b-math500-b", "B1e-5 s1": "qwen15b-math500-b-seed1",
        "C1e-5 s0": "qwen15b-gsm8k-c",
    }
    data = {}
    P("## 1. Kiểm lại pass@1/pass@k/anatomy trên exam (re-verify bằng MathVerifyAdapter reward)")
    P("| run | dir | round | pass@1 | pass@k | sample acc | mean len | degenerate | finished acc | degen acc (n) |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for lab, run in runs.items():
        if not (SC / f"{run}.json").exists():
            continue
        m, by = load(run)
        ex = exam_ids(m, by)
        data[lab] = (m, by, ex)
        for rnd in sorted(by):
            s = stats(by, rnd, ex)
            P(f"| {lab} | {run} | {rnd} | {fmt(s['p1'])} | {fmt(s['pk'])} | {fmt(s['sacc'])} | {s['len']:.0f} | {fmt(s['deg'])} | {fmt(s['facc']) if s['facc'] is not None else '-'} | {fmt(s['dacc']) if s['dacc'] is not None else '-'} ({s['ndeg']}) |")

    # ---- bootstrap paired R0 -> last
    P("\n## 2. Bootstrap 95% CI (paired over exam problems, 4000 reps) cho thay đổi R0→R_last")
    P("| run | Δpass@1 [CI] | Δpass@k [CI] | Δsample acc [CI] | Δdegenerate [CI] |")
    P("|---|---|---|---|---|")
    for lab, (m, by, ex) in data.items():
        last = max(by)
        a0, a1 = per_item(by, 0, ex), per_item(by, last, ex)
        def d(metric):
            def f(s):
                if metric == "p1":
                    g = lambda a: sum(a[i]["f"][0] for i in s) / len(s)
                elif metric == "pk":
                    g = lambda a: sum(any(a[i]["f"]) for i in s) / len(s)
                elif metric == "sacc":
                    g = lambda a: sum(sum(a[i]["f"]) for i in s) / sum(len(a[i]["f"]) for i in s)
                else:
                    g = lambda a: sum(sum(a[i]["d"]) for i in s) / sum(len(a[i]["d"]) for i in s)
                return g(a1) - g(a0)
            return f
        cells = []
        for metric in ("p1", "pk", "sacc", "deg"):
            f = d(metric)
            pt = f(list(ex))
            lo, hi = boot(f, ex, reps=2000)
            cells.append(f"{100*pt:+.1f} [{100*lo:+.1f}, {100*hi:+.1f}]")
        P(f"| {lab} (R0→R{last}) | " + " | ".join(cells) + " |")

    # ---- between-run differences at last round (same partition)
    P("\n## 3. Khác biệt giữa hai run cùng partition ở vòng cuối (bootstrap qua đề)")
    pairs = [("B5e-4 s1", "A5e-4 s1"), ("B5e-4 s2", "A5e-4 s2"), ("NF s1", "A5e-4 s1"), ("NF s2", "A5e-4 s2"),
             ("A5e-4 keep s1", "A5e-4 s1"), ("A5e-4 msl1024 s1", "A5e-4 s1"), ("B1e-5 s0", "A1e-5 s0"), ("B1e-5 s1", "A1e-5 s1")]
    P("| X − Y | Δpass@1 [CI] | Δpass@k [CI] | Δsample acc [CI] | Δdegenerate [CI] |")
    P("|---|---|---|---|---|")
    for x, y in pairs:
        if x not in data or y not in data: continue
        mx, bx, ex = data[x]; my, byy, _ = data[y]
        last = max(bx)
        ax, ay = per_item(bx, last, ex), per_item(byy, last, ex)
        cells = []
        for metric in ("p1", "pk", "sacc", "deg"):
            def f(s, metric=metric):
                if metric == "p1":
                    g = lambda a: sum(a[i]["f"][0] for i in s) / len(s)
                elif metric == "pk":
                    g = lambda a: sum(any(a[i]["f"]) for i in s) / len(s)
                elif metric == "sacc":
                    g = lambda a: sum(sum(a[i]["f"]) for i in s) / sum(len(a[i]["f"]) for i in s)
                else:
                    g = lambda a: sum(sum(a[i]["d"]) for i in s) / sum(len(a[i]["d"]) for i in s)
                return g(ax) - g(ay)
            pt = f(list(ex)); lo, hi = boot(f, ex, reps=2000)
            cells.append(f"{100*pt:+.1f} [{100*lo:+.1f}, {100*hi:+.1f}]")
        P(f"| {x} − {y} (R{last}) | " + " | ".join(cells) + " |")

    # ---- difficulty adjustment (issue 5)
    P("\n## 4. Điều chỉnh độ khó cho 'non-degenerate accuracy' (issue 5)")
    P("p0_all = acc vòng 0 của đề i trên cả 4 mẫu; p0_fin = acc vòng 0 trên mẫu vòng-0 không degenerate (fallback p0_all nếu không có). Trọng số = số mẫu finished của đề i ở vòng cuối.")
    P("| run | finished acc R0 | finished acc R_last | R0 reweighted (p0_all) | R0 reweighted (p0_fin) | Δ (R_last − rw p0_fin) [CI] | đề ≥2/4 degenerate ở R_last: acc R0 (n) | còn lại: acc R0 (n) |")
    P("|---|---|---|---|---|---|---|---|")
    for lab in ["A5e-4 s1", "A5e-4 s2", "B5e-4 s1", "B5e-4 s2", "NF s1", "NF s2", "A2e-4 s1", "A2e-4 s2", "A1e-4 s1", "A1e-4 s2", "A1e-4 s3", "C5e-4 s1", "A5e-4 keep s1", "A5e-4 msl1024 s1"]:
        if lab not in data: continue
        m, by, ex = data[lab]; last = max(by)
        a0, a1 = per_item(by, 0, ex), per_item(by, last, ex)
        def comp(s):
            num2 = den2 = 0; rw_all = rw_fin = 0
            for i in s:
                f1 = [f for f, d in zip(a1[i]["f"], a1[i]["d"]) if not d]
                n = len(f1)
                if n == 0:
                    continue
                num2 += sum(f1); den2 += n
                pa = sum(a0[i]["f"]) / len(a0[i]["f"])
                f0 = [f for f, d in zip(a0[i]["f"], a0[i]["d"]) if not d]
                pf = sum(f0) / len(f0) if f0 else pa
                rw_all += n * pa; rw_fin += n * pf
            return num2 / den2, rw_all / den2, rw_fin / den2
        acc2, rwa, rwf = comp(list(ex))
        lo, hi = boot(lambda s: (lambda t: t[0] - t[2])(comp(s)), ex, reps=2000)
        s0 = stats(by, 0, ex)
        hard = [i for i in ex if sum(a1[i]["d"]) >= 2]; easy = [i for i in ex if sum(a1[i]["d"]) < 2]
        acc0 = lambda S: sum(sum(a0[i]["f"]) for i in S) / (4 * len(S)) if S else float("nan")
        P(f"| {lab} | {fmt(s0['facc'])} | {fmt(acc2)} | {fmt(rwa)} | {fmt(rwf)} | {100*(acc2-rwf):+.1f} [{100*lo:+.1f}, {100*hi:+.1f}] | {fmt(acc0(hard))} ({len(hard)}) | {fmt(acc0(easy))} ({len(easy)}) |")

    # ---- counterfactual 35.7 (issue 5)
    P("\n## 5. Counterfactual 'giữ degenerate share ở mức R0' (Run A s1, 5e-4)")
    m, by, ex = data["A5e-4 s1"]
    s0, s2 = stats(by, 0, ex), stats(by, 2, ex)
    cf = (1 - s0["deg"]) * s2["facc"] + s0["deg"] * s2["dacc"]
    P(f"naive = (1-d0)*facc2 + d0*dacc2 = {fmt(cf)}% (paper 35.7%); R0 sample acc {fmt(s0['sacc'])}%")
    # difficulty-adjusted: per problem, round-2 finished acc on that problem applied to round-0's finished-count
    a0, a2 = per_item(by, 0, ex), per_item(by, 2, ex)
    num = den = 0; miss = 0
    for i in ex:
        f2 = [f for f, d in zip(a2[i]["f"], a2[i]["d"]) if not d]
        d2 = [f for f, d in zip(a2[i]["f"], a2[i]["d"]) if d]
        n0f = 4 - sum(a0[i]["d"])
        if f2:
            pf = sum(f2) / len(f2)
        else:
            miss += 1
            pf = sum(a0[i]["f"]) / 4 * (s2["facc"] / s0["facc"])  # fallback: scaled R0 acc
        pdg = s2["dacc"]
        num += n0f * pf + (4 - n0f) * pdg; den += 4
    P(f"per-problem counterfactual (R2 finished acc của chính đề đó × số mẫu finished ở R0) = {fmt(num/den)}% ; {miss} đề không còn mẫu finished ở R2 (dùng fallback)")

    # ---- Run C decomposition (issue 6)
    P("\n## 6. Phân rã độ giảm sample accuracy: phần do degenerate tăng vs phần do finished acc giảm")
    P("Δacc = [d-share effect] + [finished-acc effect], tách theo trung điểm (Shapley 2 yếu tố)")
    for lab in ["A5e-4 s1", "A5e-4 s2", "B5e-4 s1", "B5e-4 s2", "NF s1", "NF s2", "C5e-4 s1", "GOLD s1", "GOLD s2", "C1e-5 s0"]:
        if lab not in data: continue
        m, by, ex = data[lab]; last = max(by)
        s0, s1 = stats(by, 0, ex), stats(by, last, ex)
        da0 = s0["dacc"] or 0; da1 = s1["dacc"] or 0
        tot = s1["sacc"] - s0["sacc"]
        # acc = (1-d) fa + d da
        fa_eff = ((1 - s0["deg"]) + (1 - s1["deg"])) / 2 * (s1["facc"] - s0["facc"])
        d_eff = tot - fa_eff
        P(f"- {lab}: Δsample acc {100*tot:+.1f} = degenerate/termination {100*d_eff:+.1f} + finished-acc {100*fa_eff:+.1f}")

    # ---- degenerate heuristic checks (issue 29, 41)
    P("\n## 7. Heuristic degenerate (issue 29)")
    m, by, ex = data["A5e-4 s1"]
    for rnd in (0, 2):
        recs = [by[rnd][i] for i in ex]
        L = [l for r in recs for l in r["lens"]]; Bx = [b for r in recs for b in r["boxed"]]; F = [f for r in recs for f in r["flags"]]
        nob = sum(not b for b in Bx) / len(Bx)
        short_nob = [f for l, b, f in zip(L, Bx, F) if l <= DEG and not b]
        P(f"- A s1 R{rnd}: không \\boxed {fmt(nob)}%; ngắn(≤1500) & không boxed {fmt(len(short_nob)/len(L))}% (acc {fmt(sum(short_nob)/len(short_nob))}%); max len {max(L)}")
        for thr in (1200, 1500, 1800, 2000):
            D = [l > thr and not b for l, b in zip(L, Bx)]
            fin = [f for f, d in zip(F, D) if not d]
            P(f"    thr {thr}: degenerate {fmt(sum(D)/len(D))}%, finished acc {fmt(sum(fin)/len(fin))}%")

    # ---- step counts
    P("\n## 8. Pool & length growth")
    for lab, (m, by, ex) in data.items():
        last = max(by)
        s0, s1 = stats(by, 0, ex), stats(by, last, ex)
        P(f"- {lab}: len {s0['len']:.0f}→{s1['len']:.0f} ({100*(s1['len']/s0['len']-1):+.1f}%)")

    # ---- selection vs exam (issue 0 merged)
    P("\n## 9. Selection-set vs exam sample accuracy theo vòng (Design I) — selection-set scoring có thổi phồng không?")
    for lab in ["A1e-5 s0", "A1e-5 s1", "C1e-5 s0", "A5e-4 s1", "A5e-4 s2", "C5e-4 s1"]:
        if lab not in data: continue
        m, by, ex = data[lab]
        sel = [i for i in by[0] if i not in ex]
        row = []
        for rnd in sorted(by):
            se, xe = stats(by, rnd, sel), stats(by, rnd, ex)
            row.append(f"R{rnd} sel {fmt(se['sacc'])}/exam {fmt(xe['sacc'])} (p@1 sel {fmt(se['p1'])}/exam {fmt(xe['p1'])})")
        P(f"- {lab}: " + "; ".join(row))

    # ---- sign tests, Wilson
    P("\n## 10. Sign test / Wilson")
    P(f"- 4/4 cùng dấu, một phía: p = {0.5**4:.4f}; 2/2: p = {0.5**2:.2f}")
    n, x, z = 128, 10, 1.96
    ph = x / n; den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    P(f"- Wilson 95% CI cho 10/128 = {fmt(ph)}%: [{fmt(c-h)}%, {fmt(c+h)}%]")
    (Path(__file__).parent / "analysis.md").write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
