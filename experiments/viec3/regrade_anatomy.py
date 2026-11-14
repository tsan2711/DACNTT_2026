"""A1: anatomy + decomposition rows (supplementary Tables anatomy, decomp) from regrade flags (V')."""
import json, numpy as np
OUT = "results/viec3/regrade/"
CAP = 508
CI = json.load(open(OUT + "ci.json"))["within"]

def load(label):
    f = json.load(open(OUT + f"flags/{label}.json")); R = {}
    for g in f["rows"]:
        R.setdefault(g["round"], {})[(g["dataset"], g["item_id"])] = g
    return R

def arr(R, rd, ids):
    # per problem: n, ncorrect, nfin, nfin_ok, ncap, ncap_ok, chars_sum
    A = []
    for i in ids:
        g = R[rd][i]; nt = np.array(g["ntok"]); v = np.array(g["v"]); fin = nt < CAP
        A.append([len(v), v.sum(), fin.sum(), (v & fin).sum(), (~fin).sum(), (v & ~fin).sum(), sum(g["chars"])])
    return np.array(A, float)

def stats(a0, a1):
    n0, n1 = a0[:, 0].sum(), a1[:, 0].sum()
    cap0, cap1 = a0[:, 4].sum() / n0, a1[:, 4].sum() / n1
    s0, s1 = 1 - cap0, 1 - cap1
    f0, f1 = a0[:, 3].sum() / a0[:, 2].sum(), a1[:, 3].sum() / a1[:, 2].sum()
    c0 = a0[:, 5].sum() / max(a0[:, 4].sum(), 1); c1 = a1[:, 5].sum() / max(a1[:, 4].sum(), 1)
    da = a1[:, 1].sum() / n1 - a0[:, 1].sum() / n0
    sb, fb, cb = (s0 + s1) / 2, (f0 + f1) / 2, (c0 + c1) / 2
    fin = sb * (f1 - f0); cs = (s1 - s0) * (fb - cb); ca = (1 - sb) * (c1 - c0)
    return dict(dcap=100 * (cap1 - cap0), da=100 * da, fin=100 * fin, cs=100 * cs, ca=100 * ca, share=100 * fin / da if da else np.nan,
                cap0=100 * cap0, cap1=100 * cap1, f0=100 * f0, f1=100 * f1, len0=a0[:, 6].sum() / n0, len1=a1[:, 6].sum() / n1)

def run(label, B=2000):
    R = load(label); last = max(R); ids = sorted(set(R[0]) & set(R[last]))
    a0, a1 = arr(R, 0, ids), arr(R, last, ids); o = stats(a0, a1)
    rng = np.random.default_rng(1); b = []
    for _ in range(B):
        ix = rng.integers(0, len(ids), len(ids)); b.append(stats(a0[ix], a1[ix]))
    q = lambda k: np.nanpercentile([x[k] for x in b], [2.5, 97.5])
    return o, q("dcap"), q("share")

anat = [("A (orig.)", 1, "A_5e-4_s1"), ("B (patched)", 1, "B_5e-4_s1"), ("A (orig.)", 2, "A_5e-4_s2"), ("B (patched)", 2, "B_5e-4_s2"),
        ("No filter", 1, "NF_5e-4_s1"), ("No filter", 2, "NF_5e-4_s2"), ("A, $2\\times10^{-4}$", 1, "A_2e-4_s1"), ("A, $2\\times10^{-4}$", 2, "A_2e-4_s2"),
        ("A, $10^{-4}$", 1, "A_1e-4_s1"), ("A, $10^{-4}$", 2, "A_1e-4_s2"), ("A, $10^{-4}$", 3, "A_1e-4_s3"),
        ("A, $10^{-5}$", 0, "A_1e-5_s0"), ("A, $10^{-5}$", 1, "A_1e-5_s1"), ("Train on gold", 1, "G_5e-4_s1"), ("Train on gold", 2, "G_5e-4_s2")]
print("%% anatomy")
res = {}
for name, sd, lab in anat:
    o, qc, qs = run(lab); res[lab] = (o, qc, qs)
    mf = CI[lab]["matched_fin_v"][0]
    print(f"{name} & {sd} & ${o['len0']:.0f}\\to{o['len1']:.0f}$ & ${o['cap0']:.1f}\\to{o['cap1']:.1f}$ & ${o['f0']:.1f}\\to{o['f1']:.1f}$ & ${mf:+.1f}$ \\\\")
print("%% decomp")
dec = [("A, 1", "A_5e-4_s1"), ("B, 1", "B_5e-4_s1"), ("No filter, 1", "NF_5e-4_s1"), ("A, 2", "A_5e-4_s2"), ("B, 2", "B_5e-4_s2"), ("No filter, 2", "NF_5e-4_s2"),
       ("A replicate, 1", "A_5e-4_s1_rep"), ("A, 1024 limit, 1", "A_5e-4_s1_msl1024"), ("C (GSM8K), 1", "C_5e-4_s1"),
       ("A, $2\\times10^{-4}$, 1", "A_2e-4_s1"), ("A, $2\\times10^{-4}$, 2", "A_2e-4_s2"), ("A, $10^{-4}$, 1", "A_1e-4_s1"), ("A, $10^{-4}$, 2", "A_1e-4_s2"), ("A, $10^{-4}$, 3", "A_1e-4_s3")]
for name, lab in dec:
    if lab not in res: res[lab] = run(lab)
    o, qc, qs = res[lab]
    sh = f"${o['share']:.0f}\\%$" + (f" [${qs[0]:.0f},{qs[1]:.0f}$]" if lab.split('_')[1] == '5e-4' else "")
    print(f"{name} & ${o['dcap']:+.1f}$ [${qc[0]:.1f},{qc[1]:.1f}$] & ${o['da']:+.1f}$ & ${o['fin']:+.1f}$ & ${o['cs']:+.1f}$ & ${o['ca']:+.1f}$ & {sh} \\\\")
