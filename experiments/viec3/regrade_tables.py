"""A1: LaTeX rows for the paper tables from results/viec3/regrade/ (run regrade_all first).
Writes results/viec3/regrade/tables.tex and prints it."""
from __future__ import annotations
import csv, json, statistics as st
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "results" / "viec3" / "regrade"
CI = json.loads((OUT / "ci.json").read_text())
SUM = {}
for r in csv.DictReader((OUT / "summary.csv").open()):
    SUM[(r["run"], int(r["round"]))] = r
FL = {}


def flags(label):
    if label not in FL:
        FL[label] = json.loads((OUT / "flags" / f"{label}.json").read_text())
    return FL[label]


def added_lost(label):
    """sum over consecutive rounds of problems newly solved / newly lost at pass@k (V')."""
    rows = {}
    for g in flags(label)["rows"]:
        rows.setdefault(g["round"], {})[(g["dataset"], g["item_id"])] = any(g["v"])
    rds = sorted(rows)
    a = c = 0
    for r0, r1 in zip(rds, rds[1:]):
        for k, v in rows[r1].items():
            p = rows[r0][k]
            a += v and not p
            c += p and not v
    return a, c


def m(s):
    return "$" + s.replace("-", "-") + "$"


def sgn(x):
    return f"{x:+.1f}".replace("-", "$-$").replace("+", "$+$") if False else f"{x:+.1f}"


def tx(v):  # [obs, lo, hi] -> math string
    f = lambda x: f"{x:+.1f}".replace("+", "") if False else (f"{x:.1f}")
    o = f"{v[0]:+.1f}"
    return f"${o}$ [${v[1]:+.1f},{v[2]:+.1f}$]".replace("+-", "-")


def lr_row(rate, seed, label):
    r0, rl = SUM[(label, 0)], SUM[(label, max(r for (l, r) in SUM if l == label))]
    a, c = added_lost(label)
    return (f"{rate} & {seed} & ${r0['pass1_v']}\\to{rl['pass1_v']}$ & ${r0['passk_v']}\\to{rl['passk_v']}$ & "
            f"${r0['sacc_v']}\\to{rl['sacc_v']}$ & ${rl['cap_hit_pct']}\\%$ & ${a}/{c}$ \\\\")


L = ["% ---- tab:lrseries rows (V', cap-hit round-2, added/lost over all rounds)"]
for rate, lbl in [("$10^{-4}$", "1e-4"), ("$2\\times10^{-4}$", "2e-4"), ("$5\\times10^{-4}$", "5e-4")]:
    for s in (1, 2, 3):
        k = f"A_{lbl}_s{s}"
        if (k, 0) in SUM:
            L.append(lr_row(rate, s, k))
L += ["", "% ---- tab:ci rows: dpass1 | dpassk | dsacc | matched-finished"]


def ci_row(name, label):
    e = CI["within"][label]
    mf = tx(e["matched_fin_v"]) if "matched_fin_v" in e else "--"
    return f"{name} & {tx(e['d_pass1_v'])} & {tx(e['d_passk_v'])} & {tx(e['d_sacc_v'])} & {mf} \\\\"


groups = [("Learning rate $10^{-5}$", [("A, 0", "A_1e-5_s0"), ("A, 1", "A_1e-5_s1"), ("B, 0", "B_1e-5_s0"), ("B, 1", "B_1e-5_s1"), ("C, 0", "C_1e-5_s0")]),
          ("Learning rate $10^{-4}$", [("A, 1", "A_1e-4_s1"), ("A, 2", "A_1e-4_s2"), ("A, 3", "A_1e-4_s3")]),
          ("Learning rate $2\\!\\times\\!10^{-4}$", [("A, 1", "A_2e-4_s1"), ("A, 2", "A_2e-4_s2")]),
          ("Learning rate $5\\!\\times\\!10^{-4}$", [("A, 1", "A_5e-4_s1"), ("A, 2", "A_5e-4_s2"), ("B, 1", "B_5e-4_s1"), ("B, 2", "B_5e-4_s2"),
                                                     ("No filter, 1", "NF_5e-4_s1"), ("No filter, 2", "NF_5e-4_s2"), ("Gold, 1", "G_5e-4_s1"),
                                                     ("Gold, 2", "G_5e-4_s2"), ("C, 1", "C_5e-4_s1")])]
for i, (h, rows) in enumerate(groups):
    if i:
        L.append("\\midrule")
    L.append(f"\\multicolumn{{5}}{{l}}{{\\emph{{{h}}}}} \\\\")
    L += [ci_row(n, l) for n, l in rows]

L += ["", "% ---- tab:controls (pass@1, pass@4 at R0,R1,R2) + pool"]
for s in (1, 2):
    L.append(f"% seed {s}")
    for name, k in [("A (verifier-filtered)", f"A_5e-4_s{s}"), ("No filter", f"NF_5e-4_s{s}"), ("Train on gold", f"G_5e-4_s{s}")]:
        r = [SUM[(k, i)] for i in range(3)]
        L.append(f"{name} & -- & " + " & ".join(x["pass1_v"] for x in r) + " & " + " & ".join(x["passk_v"] for x in r) + " \\\\")

L += ["", "% ---- tab:final"]
u = SUM[("FINAL_loop_s1", 0)]
L.append(f"Untrained (seed 1) & {u['pass1_v']} & {u['passk_v']} & -- \\\\")
for s in (1, 2, 3):
    e = CI["within"][f"FINAL_loop_s{s}"]
    L.append(f"Loop, seed {s} & {tx(e['d_pass1_v'])} & {tx(e['d_passk_v'])} & {tx(e['d_sacc_v'])} \\\\")
mean = lambda key: sum(CI["within"][f"FINAL_loop_s{s}"][key][0] for s in (1, 2, 3)) / 3
L.append(f"Loop, mean of seeds & ${mean('d_pass1_v'):+.1f}$ & ${mean('d_passk_v'):+.1f}$ & ${mean('d_sacc_v'):+.1f}$ \\\\")
for name, k in [("Train on gold", "FINAL_gold_1e-4"), ("Gold, $2\\times10^{-5}$", "FINAL_gold_2e-5")]:
    e = CI["within"][k]
    L.append(f"{name} & {tx(e['d_pass1_v'])} & {tx(e['d_passk_v'])} & {tx(e['d_sacc_v'])} \\\\")
import math
for key in ("d_pass1_v", "d_sacc_v"):
    xs = [CI["within"][f"FINAL_loop_s{s}"][key][0] for s in (1, 2, 3)]
    mu, sd = st.mean(xs), st.stdev(xs)
    h = 4.303 * sd / math.sqrt(3)
    L.append(f"% mean {key}: {mu:+.1f}  t-interval [{mu-h:+.1f}, {mu+h:+.1f}]")
L += ["", "% round-0 pass@1 final seeds: " + ", ".join(SUM[(f'FINAL_loop_s{s}', 0)]['pass1_v'] for s in (1, 2, 3)),
      "% cap-hit R0 (A runs): " + ", ".join(f"{k}:{SUM[(k,0)]['cap_hit_pct']}" for k in ("A_1e-4_s1", "A_1e-4_s2", "A_1e-4_s3"))]
txt = "\n".join(L) + "\n"
(OUT / "tables.tex").write_text(txt)
print(txt)
