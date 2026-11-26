"""A1 (plan 2026-11-15): re-grade EVERY viec3 run from its saved generations.jsonl with ONE grader pair, so the
paper has a single set of numbers (no mixed "run-log" values).

Graders (identical for every run, whatever verifier the run used at training time):
  V'      = MathVerifyAdapter('reward', normalize_frac_commands=True, normalize_gold_boxed=True), fixed timeout
            (TIMEOUT s; any generation that times out is re-graded alone at RETRY_TIMEOUT s, so no
            result depends on machine load);
  string  = normalised string match of the last \\boxed{} against the gold (review_cpu/indep_grade.py).
Primary number in the paper = V'; string match is the robustness check ("both" = both graders accept).

    .venv/bin/python -m experiments.viec3.regrade_all            # grade (cached) + write summary/ci
    .venv/bin/python -m experiments.viec3.regrade_all --B 2000

Writes results/viec3/regrade/{flags/<run>.json, summary.csv, ci.md, ci.json}.
Exam set: the held-out 150 (seed-shuffled, as run.py) for holdout runs; every MATH-500 problem for the final round.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import random
import re
import sys
from multiprocessing import Pool
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

RES = REPO / "results" / "viec3"
OUT = RES / "regrade"
TIMEOUT = 10
RETRY_TIMEOUT = 60
CAP_TOK = 508  # generation cap 512; re-tokenised >= 508 => cap-hit
DEGEN_CHARS = 1500

# label -> directory
RUNS = {
    "A_1e-5_s0": "qwen15b-math500-a", "A_1e-5_s1": "qwen15b-math500-a-seed1",
    "B_1e-5_s0": "qwen15b-math500-b", "B_1e-5_s1": "qwen15b-math500-b-seed1",
    "C_1e-5_s0": "qwen15b-gsm8k-c",
    "A_1e-4_s1": "a-math500-lr1e4", "A_1e-4_s2": "a-lr1e4-seed2", "A_1e-4_s3": "a-lr1e4-seed3",
    "A_2e-4_s1": "a-lr2e4-seed1", "A_2e-4_s2": "a-lr2e4-seed2",
    "A_5e-4_s1": "a-math500-lr-fixed", "A_5e-4_s2": "a-math500-lr-fixed-seed2",
    "B_5e-4_s1": "b-math500-lr-fixed", "B_5e-4_s2": "b-math500-lr-fixed-seed2",
    "NF_5e-4_s1": "nofilter-math500-lr-fixed", "NF_5e-4_s2": "nofilter-math500-seed2",
    "G_5e-4_s1": "gold-math500-lr-fixed", "G_5e-4_s2": "gold-math500-seed2",
    "A_5e-4_s1_rep": "a-lr5e4-keep", "A_5e-4_s1_msl1024": "a-lr5e4-msl1024",
    "C_5e-4_s1": "c-gsm8k-lr5e4",
    "P_1.5B": "qwen15b-n500", "P_0.5B": "qwen05b-n500",
    "FINAL_loop_s1": "gvt-s1-lr1e4", "FINAL_loop_s2": "gvt-s2-lr1e4", "FINAL_loop_s3": "gvt-s3-lr1e4",
    "FINAL_gold_1e-4": "gate-gold-lr1e4", "FINAL_gold_2e-5": "gate-gold-lr2e5", "FINAL_teacher_s1": "gate-teacher-s1", "FINAL_teacher_s2": "gate-teacher-s2",
    "G3_mathteacher_s1": "gate-mathteacher-s1", "G3_mathteacher_s2": "gate-mathteacher-s2",
}

CONTRASTS = [("B_1e-5_s0", "A_1e-5_s0"), ("B_1e-5_s1", "A_1e-5_s1"), ("B_5e-4_s1", "A_5e-4_s1"),
             ("B_5e-4_s2", "A_5e-4_s2"), ("NF_5e-4_s1", "A_5e-4_s1"), ("NF_5e-4_s2", "A_5e-4_s2"),
             ("G_5e-4_s1", "A_5e-4_s1"), ("G_5e-4_s2", "A_5e-4_s2"), ("A_5e-4_s1_rep", "A_5e-4_s1"),
             ("A_5e-4_s1_msl1024", "A_5e-4_s1_rep"),
             ("FINAL_teacher_s1", "FINAL_loop_s1"), ("FINAL_teacher_s2", "FINAL_loop_s2"),
             ("G3_mathteacher_s1", "FINAL_loop_s1"), ("G3_mathteacher_s2", "FINAL_loop_s2")]


# ---------------------------------------------------------------- string-match grader (same as indep_grade.py)
def last_boxed(t):
    i = t.rfind("\\boxed")
    if i < 0:
        return None
    j = t.find("{", i)
    if j < 0:
        return None
    d = 0
    for k in range(j, len(t)):
        d += (t[k] == "{") - (t[k] == "}")
        if d == 0:
            return t[j + 1:k]
    return None


def norm(s):
    s = s.strip()
    m = re.fullmatch(r"\$+(.*?)\$+", s, re.S)
    s = m.group(1) if m else s
    b = last_boxed(s) if "\\boxed" in s else None
    s = b if b is not None else s
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("\\left", "").replace("\\right", "")
    s = s.replace("\\!", "").replace("\\,", "").replace("\\ ", "").replace("^\\circ", "").replace("^{\\circ}", "")
    s = re.sub(r"\\frac(\d)(\d)", r"\\frac{\1}{\2}", s)
    s = re.sub(r"\s+", "", s).rstrip(".")
    return s


def string_ok(gold, text):
    b = last_boxed(text)
    return b is not None and norm(b) == norm(gold)


# ---------------------------------------------------------------- grading
# math-verify 0.9.0 swallows a comparison timeout (returns False, logs "Timeout during comparison"), so
# AdapterResult.reason never says "timeout". We catch the warning to know which verdicts depended on the clock.
import logging


class _TimeoutCatcher(logging.Handler):
    def __init__(self):
        super().__init__(logging.WARNING)
        self.hit = False

    def emit(self, record):
        if "Timeout during comparison" in record.getMessage():
            self.hit = True


_CATCH = _TimeoutCatcher()
logging.getLogger("math_verify.grader").addHandler(_CATCH)
logging.getLogger("math_verify.grader").propagate = False


def verify_flag(ad, gold, text):
    """(accepted, timed_out)"""
    _CATCH.hit = False
    r = ad.verify(gold, text)
    return bool(r.accepted), (_CATCH.hit or r.reason_guess == "timeout")


_AD = {}


def _adapter(timeout):
    if timeout not in _AD:
        from dacntt.verify.adapter import MathVerifyAdapter
        _AD[timeout] = MathVerifyAdapter("reward", timeout_seconds=timeout,
                                         normalize_frac_commands=True, normalize_gold_boxed=True)
    return _AD[timeout]


def _grade_rec(rec):
    ad = _adapter(TIMEOUT)
    v, reasons = [], []
    for t in rec["texts"]:
        ok, to = verify_flag(ad, rec["gold"], t)
        v.append(ok)
        reasons.append("timeout" if to else "ok")
    return {"round": rec["round"], "dataset": rec["dataset"], "item_id": rec["item_id"],
            "v": v, "reason": reasons, "s": [string_ok(rec["gold"], t) for t in rec["texts"]],
            "boxed": ["\\boxed" in t for t in rec["texts"]], "chars": [len(t) for t in rec["texts"]]}


def _exam_keys(man, recs):
    """Set of (dataset,item_id) that make up the exam."""
    r0 = [r for r in recs if r["round"] == 0]
    if man.get("holdout_frac", 0) and man["holdout_frac"] > 0:
        by = {}
        for r in r0:
            by.setdefault(r["dataset"], []).append(r["item_id"])
        rng = random.Random(man["seed"] if man.get("seed") is not None else 0)
        keys = set()
        for ds, ids in by.items():
            ids = sorted(ids)
            rng.shuffle(ids)
            n = max(1, round(len(ids) * man["holdout_frac"]))
            keys |= {(ds, i) for i in ids[:n]}
        return keys
    # holdout 0: final round => exam = math500 only (selection pool is mathtrain); P runs => everything
    ds_set = {r["dataset"] for r in r0}
    if "mathtrain" in ds_set:
        return {(r["dataset"], r["item_id"]) for r in r0 if r["dataset"] == "math500"}
    return {(r["dataset"], r["item_id"]) for r in r0}


def _tokenizer_path():
    tj = [os.environ.get("TOKENIZER_JSON", "")] + glob.glob(os.path.expanduser(
        "~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/*/tokenizer.json"))
    return next((t for t in tj if t and os.path.isfile(t)), None)


def _add_ntok(out):
    """Add re-tokenised lengths to a cached grade (needs the Qwen tokenizer; set TOKENIZER_JSON)."""
    tp = _tokenizer_path()
    if not tp:
        return
    from tokenizers import Tokenizer
    tk = Tokenizer.from_file(tp)
    by = {}
    for l in (RES / out["dir"] / "generations.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        by[(r["round"], r["dataset"], r["item_id"])] = r["texts"]
    for g in out["rows"]:
        g["ntok"] = [len(e.ids) for e in tk.encode_batch(by[(g["round"], g["dataset"], g["item_id"])], add_special_tokens=False)]


def grade_run(label, pool):
    cache = OUT / "flags" / f"{label}.json"
    if cache.is_file():
        out = json.loads(cache.read_text())
        if out.get("max_tokens") == 512 and out["rows"] and "ntok" not in out["rows"][0]:
            _add_ntok(out)
            cache.write_text(json.dumps(out))
        return out
    d = RES / RUNS[label]
    man = json.loads((d / "manifest.json").read_text())
    recs = [json.loads(l) for l in (d / "generations.jsonl").open(encoding="utf-8")]
    keys = _exam_keys(man, recs)
    recs = [r for r in recs if (r["dataset"], r["item_id"]) in keys]
    graded = pool.map(_grade_rec, recs, chunksize=4)
    # re-grade timeouts alone, longer, sequentially (load-independent)
    n_to = 0
    by = {(r["round"], r["dataset"], r["item_id"]): r for r in recs}
    ad = _adapter(RETRY_TIMEOUT)
    still = 0
    for g in graded:
        for idx, why in enumerate(g["reason"]):
            if why == "timeout":
                n_to += 1
                rec = by[(g["round"], g["dataset"], g["item_id"])]
                ok, to = verify_flag(ad, rec["gold"], rec["texts"][idx])
                g["v"][idx] = ok
                g["reason"][idx] = "timeout" if to else "ok"
                still += to
    ntok = None
    tj = glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/*/tokenizer.json"))
    if tj and man.get("max_tokens") == 512:
        from tokenizers import Tokenizer
        tk = Tokenizer.from_file(tj[0])
        for g in graded:
            rec = by[(g["round"], g["dataset"], g["item_id"])]
            g["ntok"] = [len(e.ids) for e in tk.encode_batch(rec["texts"], add_special_tokens=False)]
    out = {"label": label, "dir": RUNS[label], "k": man["k"], "seed": man.get("seed"),
           "max_tokens": man.get("max_tokens"), "datasets": man["datasets"],
           "timeouts_first_pass": n_to, "timeouts_after_retry": still, "rows": graded}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out))
    print(f"graded {label}: {len(graded)} records, timeouts {n_to} -> {still} after retry", flush=True)
    return out


# ---------------------------------------------------------------- statistics
def pp_rows(rows_r, ids, grader):
    """per problem: first, any, n_ok, n, n_boxed, n_boxed_ok, ncap, ncap_free_ok, n_capfree"""
    out = []
    for i in ids:
        g = rows_r[i]
        f = g["v"] if grader == "v" else g["s"] if grader == "s" else [a and b for a, b in zip(g["v"], g["s"])]
        nt = g.get("ntok")
        capfree = [not (n >= CAP_TOK) for n in nt] if nt else [True] * len(f)
        out.append((f[0], any(f), sum(f), len(f), sum(g["boxed"]),
                    sum(a and b for a, b in zip(f, g["boxed"])),
                    sum(not c for c in capfree), sum(c and a for c, a in zip(capfree, f)), sum(capfree)))
    return out


def metrics(M):
    import numpy as np
    n = M.shape[-2]
    S = M.sum(axis=-2)
    with np.errstate(invalid="ignore", divide="ignore"):
        return {"pass1": 100 * S[..., 0] / n, "passk": 100 * S[..., 1] / n, "sacc": 100 * S[..., 2] / S[..., 3],
                "boxed": 100 * S[..., 4] / S[..., 3], "acc_boxed": 100 * S[..., 5] / S[..., 4],
                "cap": 100 * S[..., 6] / S[..., 3], "fin_acc": 100 * S[..., 7] / S[..., 8]}


def ci(obs, vals):
    import numpy as np
    vals = vals[~np.isnan(vals)]
    return [float(obs), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def f_ci(v):
    return f"{v[0]:+.1f} [{v[1]:+.1f}, {v[2]:+.1f}]"


def main():
    import numpy as np
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261114)
    ap.add_argument("--workers", type=int, default=7)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    data = {}
    with Pool(args.workers) as pool:
        for label in RUNS:
            if not (RES / RUNS[label] / "generations.jsonl").is_file():
                print("skip (no generations)", label)
                continue
            data[label] = grade_run(label, pool)

    # structure: label -> round -> item key -> row
    S = {}
    for label, d in data.items():
        rr = {}
        for g in d["rows"]:
            rr.setdefault(g["round"], {})[f'{g["dataset"]}:{g["item_id"]}'] = g
        S[label] = rr

    # ---- summary.csv
    with (OUT / "summary.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["run", "dir", "round", "n_problems", "k", "pass1_v", "passk_v", "sacc_v", "pass1_s", "passk_s",
                    "sacc_s", "sacc_both", "boxed_pct", "acc_given_boxed_v", "cap_hit_pct", "median_chars",
                    "timeouts_first_pass", "timeouts_after_retry"])
        import statistics as st
        for label, rr in S.items():
            for rd in sorted(rr):
                ids = sorted(rr[rd])
                mv = metrics(np.array(pp_rows(rr[rd], ids, "v"), dtype=float))
                ms = metrics(np.array(pp_rows(rr[rd], ids, "s"), dtype=float))
                mb = metrics(np.array(pp_rows(rr[rd], ids, "b"), dtype=float))
                med = st.median([c for i in ids for c in rr[rd][i]["chars"]])
                has_cap = "ntok" in rr[rd][ids[0]]
                w.writerow([label, data[label]["dir"], rd, len(ids), data[label]["k"],
                            f'{mv["pass1"]:.1f}', f'{mv["passk"]:.1f}', f'{mv["sacc"]:.1f}',
                            f'{ms["pass1"]:.1f}', f'{ms["passk"]:.1f}', f'{ms["sacc"]:.1f}', f'{mb["sacc"]:.1f}',
                            f'{mv["boxed"]:.1f}', f'{mv["acc_boxed"]:.1f}',
                            f'{mv["cap"]:.1f}' if has_cap else "", f"{med:.0f}",
                            data[label]["timeouts_first_pass"], data[label]["timeouts_after_retry"]])

    # ---- paired bootstrap, group by identical exam id sets
    rng = np.random.default_rng(args.seed)
    groups = {}
    for label in S:
        groups.setdefault(tuple(sorted(S[label][0])), []).append(label)
    res = {"B": args.B, "within": {}, "contrasts": {}}
    for ids_t, labels in groups.items():
        ids = list(ids_t)
        n = len(ids)
        idx = rng.integers(0, n, size=(args.B, n))
        X = {}
        for label in labels:
            for rd in S[label]:
                for gr in ("v", "s"):
                    X[(label, rd, gr)] = np.array(pp_rows(S[label][rd], ids, gr), dtype=float)
        obs = {k: metrics(v) for k, v in X.items()}
        boot = {k: metrics(v[idx]) for k, v in X.items()}

        def delta(a, b, m):
            return ci(obs[b][m] - obs[a][m], boot[b][m] - boot[a][m])

        for label in labels:
            last = max(S[label])
            e = {"n": n, "k": data[label]["k"], "last": last, "levels": {}}
            for rd in sorted(S[label]):
                e["levels"][rd] = {gr: {m: float(obs[(label, rd, gr)][m]) for m in obs[(label, rd, gr)]}
                                   for gr in ("v", "s")}
            for gr in ("v", "s"):
                for m in ("pass1", "passk", "sacc", "boxed", "acc_boxed", "cap"):
                    e[f"d_{m}_{gr}"] = delta((label, 0, gr), (label, last, gr), m) if (label, last, gr) in obs else None
                if "ntok" in S[label][0][ids[0]]:
                    # difficulty-matched finished accuracy: R0 per-problem accuracy weighted by last-round finished count
                    r0, rl = X[(label, 0, gr)], X[(label, last, gr)]
                    with np.errstate(invalid="ignore", divide="ignore"):
                        w0 = (r0[:, 2] / r0[:, 3]) * rl[:, 8]
                    m_obs = 100 * w0.sum() / rl[:, 8].sum()
                    m_boot = 100 * w0[idx].sum(axis=1) / rl[:, 8][idx].sum(axis=1)
                    e[f"matched_fin_{gr}"] = ci(obs[(label, last, gr)]["fin_acc"] - m_obs,
                                                boot[(label, last, gr)]["fin_acc"] - m_boot)
            if 1 in S[label] and last != 1:
                e["d_pass1_R0_R1_v"] = delta((label, 0, "v"), (label, 1, "v"), "pass1")
            res["within"][label] = e
        for t, c in CONTRASTS:
            if t in labels and c in labels:
                last = max(S[t])
                res["contrasts"][f"{t} - {c}"] = {
                    "round": last, **{f"{m}_{gr}": delta((c, last, gr), (t, last, gr), m)
                                      for gr in ("v", "s") for m in ("pass1", "passk", "sacc")}}
    (OUT / "ci.json").write_text(json.dumps(res, indent=1, default=lambda o: float(o)))

    L = [f"# A1 — single grading, 95% paired bootstrap (B={args.B}, resampling exam problems)", "",
         "Grader V' (primary) and string match (robustness); same for every run. Points. Generated by "
         "`experiments/viec3/regrade_all.py`; interval excludes training-seed variance.", "",
         "| Run | k | R0 → last (sample acc, V') | Δpass@1 | Δpass@k | Δsample acc | Δsample acc (string) | matched finished |",
         "|---|---|---|---|---|---|---|---|"]
    for label, e in res["within"].items():
        l0, ll = e["levels"][0]["v"], e["levels"][e["last"]]["v"]
        mf = f_ci(e["matched_fin_v"]) if "matched_fin_v" in e else "-"
        L.append(f"| {label} | {e['k']} | {l0['sacc']:.1f} → {ll['sacc']:.1f} | {f_ci(e['d_pass1_v'])} | {f_ci(e['d_passk_v'])} | "
                 f"{f_ci(e['d_sacc_v'])} | {f_ci(e['d_sacc_s'])} | {mf} |")
    L += ["", "## Contrasts (treatment − control, last round)", "", "| Contrast | pass@1 | pass@k | sample acc |", "|---|---|---|---|"]
    for c, e in res["contrasts"].items():
        L.append(f"| {c} (R{e['round']}) | {f_ci(e['pass1_v'])} | {f_ci(e['passk_v'])} | {f_ci(e['sacc_v'])} |")
    (OUT / "ci.md").write_text("\n".join(L) + "\n")
    print("wrote", OUT / "summary.csv", OUT / "ci.md")


if __name__ == "__main__":
    main()
