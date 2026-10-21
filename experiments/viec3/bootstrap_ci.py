"""Confidence intervals for the paper's comparisons, from the saved generations.

    .venv/bin/python -m experiments.viec3.bootstrap_ci            # all runs
    .venv/bin/python -m experiments.viec3.bootstrap_ci --B 2000   # faster

CPU only, no new generation: every number comes from the
``results/viec3/<run>/generations.jsonl`` files that the Kaggle runs saved.

Steps:
1. For each run, rebuild the exam partition exactly as run.py did
   (``_split_train_test`` with the run's seed and holdout_frac), then
   re-verify every exam sample with the same ``MathVerifyAdapter`` ("reward"
   preset, the locked exam preset; frac patch on for Run B). The per-sample
   flags are cached under ``results/viec3/ci/flags/``.
2. Check that the re-verified pass@1 / pass@k reproduce the run's metrics.csv.
   A run that does not reproduce is reported and left out.
3. Paired problem-level bootstrap: resample the 150 exam problems with
   replacement (B times) and recompute every statistic on the same resampled
   problems for every round and every run that shares the partition. Report
   the observed value and the 2.5/97.5 percentiles. Resampling problems, not
   samples, respects the clustering of k samples within a problem.
   What this interval covers: which problems were drawn and the sampling of
   generations, given one trained adapter per round. It does NOT cover
   training-seed (fit-to-fit) variance, so it is a lower bound on the real
   uncertainty of a run-level comparison.
4. Wilson 95% intervals for single proportions (verifier audit).

Writes results/viec3/ci/ci.md and ci.json.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT))

RES = _REPO_ROOT / "results" / "viec3"
OUT = RES / "ci"
DEGENERATE_CHARS = 1500  # same rule as experiments/viec3/reeval.py

# name -> (directory, patched verifier?)
RUNS = {
    # 1e-5, k=8, five rounds
    "A_1e-5_s0": ("qwen15b-math500-a", False),
    "A_1e-5_s1": ("qwen15b-math500-a-seed1", False),
    "B_1e-5_s0": ("qwen15b-math500-b", True),
    "B_1e-5_s1": ("qwen15b-math500-b-seed1", True),
    "C_1e-5_s0": ("qwen15b-gsm8k-c", False),
    # corrected rates, k=4, three rounds
    "A_5e-4_s1": ("a-math500-lr-fixed", False),
    "A_5e-4_s2": ("a-math500-lr-fixed-seed2", False),
    "B_5e-4_s1": ("b-math500-lr-fixed", True),
    "B_5e-4_s2": ("b-math500-lr-fixed-seed2", True),
    "NF_5e-4_s1": ("nofilter-math500-lr-fixed", False),
    "NF_5e-4_s2": ("nofilter-math500-seed2", False),
    "G_5e-4_s1": ("gold-math500-lr-fixed", False),
    "G_5e-4_s2": ("gold-math500-seed2", False),
    "A_1e-4_s1": ("a-math500-lr1e4", False),
    "A_1e-4_s2": ("a-lr1e4-seed2", False),
    "A_1e-4_s3": ("a-lr1e4-seed3", False),
    "A_2e-4_s1": ("a-lr2e4-seed1", False),
    "A_2e-4_s2": ("a-lr2e4-seed2", False),
    "A_5e-4_s1_rep": ("a-lr5e4-keep", False),
    "A_5e-4_s1_msl1024": ("a-lr5e4-msl1024", False),
    "C_5e-4_s1": ("c-gsm8k-lr5e4", False),
}

# Paired run-vs-run contrasts at the last round (same seed => same partition).
CONTRASTS = [
    ("B_1e-5_s0", "A_1e-5_s0"),
    ("B_1e-5_s1", "A_1e-5_s1"),
    ("B_5e-4_s1", "A_5e-4_s1"),
    ("B_5e-4_s2", "A_5e-4_s2"),
    ("NF_5e-4_s1", "A_5e-4_s1"),
    ("NF_5e-4_s2", "A_5e-4_s2"),
    ("G_5e-4_s1", "A_5e-4_s1"),
    ("G_5e-4_s2", "A_5e-4_s2"),
    ("A_5e-4_s1_rep", "A_5e-4_s1"),
    ("A_5e-4_s1_msl1024", "A_5e-4_s1_rep"),
]


def is_degenerate(text: str) -> bool:
    return len(text) > DEGENERATE_CHARS and "\\boxed" not in text


def wilson(x: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = x / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


# ---------------------------------------------------------------- re-verify

def _verify_run(name: str) -> dict | None:
    from experiments.viec3.run import _split_train_test
    from dacntt.gold.load import load_gold
    from dacntt.verify.adapter import MathVerifyAdapter

    rdir, patched = RUNS[name]
    path = RES / rdir
    cache = OUT / "flags" / f"{name}.json"
    if cache.is_file():
        return json.loads(cache.read_text())
    man = json.loads((path / "manifest.json").read_text())
    ds = man["datasets"]
    items = []
    for d in ds:
        items += load_gold(d, man["n"], _REPO_ROOT / "data" / "gold", fetch=False)
    _, test_ids = _split_train_test(items, man["holdout_frac"], man["seed"])
    verifier = MathVerifyAdapter(
        man.get("locked_exam", "reward"), timeout_seconds=3, normalize_frac_commands=patched
    )
    rounds: dict[int, dict[str, dict]] = {}
    with (path / "generations.jsonl").open() as fh:
        for line in fh:
            rec = json.loads(line)
            key = f"{rec['dataset']}:{rec['item_id']}"
            if key not in test_ids:
                continue
            texts = rec["texts"]
            flags = [bool(verifier.verify(rec["gold"], t).accepted) for t in texts]
            rounds.setdefault(int(rec["round"]), {})[key] = {
                "flags": flags,
                "degen": [is_degenerate(t) for t in texts],
                "chars": [len(t) for t in texts],
            }
    out = {"k": man["k"], "seed": man["seed"], "dataset": ds,
           "rounds": {str(r): v for r, v in sorted(rounds.items())}}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out))
    return out


def _reported(name: str) -> dict[int, tuple[float, float]]:
    """pass@1, pass@k per round from the run's metrics.csv (locked 'reward')."""
    import csv

    rdir, _ = RUNS[name]
    rows = {}
    with (RES / rdir / "metrics.csv").open() as fh:
        for row in csv.DictReader(fh):
            if row.get("preset", "reward") == "reward":
                rows[int(row["round"])] = (float(row["pass_at_1"]), float(row["pass_at_k"]))
    return rows


# ---------------------------------------------------------------- statistics

def per_problem(rnd: dict, ids: list[str]) -> list[tuple]:
    """(first correct, any correct, n correct, n samples, n degen, n finished, n finished correct)."""
    rows = []
    for i in ids:
        f = rnd[i]["flags"]
        dg = rnd[i]["degen"]
        fin = [c for c, d in zip(f, dg) if not d]
        rows.append((f[0], any(f), sum(f), len(f), sum(dg), len(fin), sum(fin)))
    return rows


def stats(rows: list[tuple]) -> dict[str, float]:
    n = len(rows)
    ns = sum(r[3] for r in rows)
    nfin = sum(r[5] for r in rows)
    return {
        "pass1": 100 * sum(r[0] for r in rows) / n,
        "passk": 100 * sum(r[1] for r in rows) / n,
        "sacc": 100 * sum(r[2] for r in rows) / ns,
        "degen": 100 * sum(r[4] for r in rows) / ns,
        "fin_acc": 100 * sum(r[6] for r in rows) / nfin if nfin else float("nan"),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261018)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv)

    data: dict[str, dict] = {}
    repro: list[str] = []
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        verified = dict(zip(RUNS, pool.map(_verify_run, RUNS)))
    for name in RUNS:
        d = verified[name]
        rep = _reported(name)
        ok = True
        for r_str, rnd in d["rounds"].items():
            ids = sorted(rnd)
            s = stats(per_problem(rnd, ids))
            want = rep.get(int(r_str))
            if want is None:
                continue
            if abs(s["pass1"] - 100 * want[0]) > 0.05 or abs(s["passk"] - 100 * want[1]) > 0.05:
                ok = False
                repro.append(f"{name} R{r_str}: got {s['pass1']:.1f}/{s['passk']:.1f}, "
                             f"metrics.csv {100*want[0]:.1f}/{100*want[1]:.1f}")
        d["reproduces"] = ok
        data[name] = d
        print(f"{name}: reproduces={ok}", flush=True)

    import numpy as np

    rng = np.random.default_rng(args.seed)
    results: dict = {"B": args.B, "within_run": {}, "contrasts": {}, "matched_finished": {},
                     "wilson": {}, "reproduction_mismatches": repro}

    def metrics_from_sums(S, n):
        # S[..., j] are column sums of per_problem rows over the n problems
        with np.errstate(invalid="ignore", divide="ignore"):
            return {
                "pass1": 100 * S[..., 0] / n,
                "passk": 100 * S[..., 1] / n,
                "sacc": 100 * S[..., 2] / S[..., 3],
                "degen": 100 * S[..., 4] / S[..., 3],
                "fin_acc": 100 * S[..., 6] / S[..., 5],
            }

    def ci(obs, vals):
        vals = vals[~np.isnan(vals)]
        return [float(obs), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]

    # group runs by partition (same dataset + seed => same exam ids)
    groups: dict[tuple, list[str]] = {}
    for name, d in data.items():
        groups.setdefault((tuple(d["dataset"]), d["seed"]), []).append(name)

    for key, names in groups.items():
        ids = sorted(data[names[0]]["rounds"]["0"])
        for nm in names:
            assert sorted(data[nm]["rounds"]["0"]) == ids, nm
        n = len(ids)
        idx = rng.integers(0, n, size=(args.B, n))  # same resample for every run in the group
        X = {(nm, r): np.array(per_problem(data[nm]["rounds"][r], ids), dtype=float)
             for nm in names for r in data[nm]["rounds"]}
        obsM = {kk: metrics_from_sums(v.sum(axis=0), n) for kk, v in X.items()}
        bootM = {kk: metrics_from_sums(v[idx].sum(axis=1), n) for kk, v in X.items()}

        def delta(a, b, metric):
            return ci(obsM[b][metric] - obsM[a][metric], bootM[b][metric] - bootM[a][metric])

        for nm in names:
            rs = sorted(data[nm]["rounds"], key=int)
            last = rs[-1]
            entry = {"n_problems": n, "k": data[nm]["k"], "last_round": int(last),
                     "levels": {r: {m: float(v) for m, v in obsM[(nm, r)].items()} for r in rs}}
            for metric in ("pass1", "passk", "sacc", "degen", "fin_acc"):
                entry[f"d_{metric}_R0_R{last}"] = delta((nm, "0"), (nm, last), metric)
            if "1" in rs and last != "1":
                entry["d_pass1_R0_R1"] = delta((nm, "0"), (nm, "1"), "pass1")
            results["within_run"][nm] = entry

            # difficulty-matched finished accuracy
            r0, rL = X[(nm, "0")], X[(nm, last)]
            wacc = (r0[:, 2] / r0[:, 3]) * rL[:, 5]          # per problem: R0 acc x finished count
            obs_m = 100 * wacc.sum() / rL[:, 5].sum()
            boot_m = 100 * wacc[idx].sum(axis=1) / rL[:, 5][idx].sum(axis=1)
            obs_f = obsM[(nm, last)]["fin_acc"]
            results["matched_finished"][nm] = {
                "fin_acc_R0": float(obsM[(nm, "0")]["fin_acc"]), "fin_acc_last": float(obs_f),
                "R0_matched_to_last_mix": float(obs_m),
                "diff": ci(obs_f - obs_m, bootM[(nm, last)]["fin_acc"] - boot_m)}

        for treat, ctrl in CONTRASTS:
            if treat in names and ctrl in names:
                last = sorted(data[treat]["rounds"], key=int)[-1]
                assert last == sorted(data[ctrl]["rounds"], key=int)[-1]
                e = {"round": int(last)}
                for metric in ("pass1", "passk", "sacc", "degen"):
                    e[metric] = delta((ctrl, last), (treat, last), metric)
                results["contrasts"][f"{treat} - {ctrl}"] = e

    for label, x, n in [("FN MATH-500 audit", 10, 128), ("FN GSM8K audit", 0, 200)]:
        results["wilson"][label] = [100 * x / n, *(100 * v for v in wilson(x, n))]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ci.json").write_text(json.dumps(results, indent=1))
    _write_md(results)
    return 0


def _f(v):
    return f"{v[0]:+.1f} [{v[1]:+.1f}, {v[2]:+.1f}]"


def _write_md(res: dict) -> None:
    L = [f"# 95% bootstrap CIs (paired, resampling the 150 exam problems, B={res['B']})", "",
         "Generated by `experiments/viec3/bootstrap_ci.py`. Interval = 2.5/97.5 percentiles.",
         "Covers problem draw + generation sampling for the given adapters; does NOT cover",
         "training-seed variance. Points are percentage points.", ""]
    if res["reproduction_mismatches"]:
        L += ["**Reproduction mismatches:**", *[f"- {m}" for m in res["reproduction_mismatches"]], ""]
    else:
        L += ["Re-verified pass@1/pass@k reproduce every run's metrics.csv exactly.", ""]
    L += ["## Within run, round 0 -> last round", "",
          "| Run | k | dpass@1 | dpass@k | dsample acc | ddegenerate | dfinished acc | dpass@1 R0->R1 |",
          "|---|---|---|---|---|---|---|---|"]
    for nm, e in res["within_run"].items():
        last = e["last_round"]
        r1 = _f(e["d_pass1_R0_R1"]) if "d_pass1_R0_R1" in e else "-"
        L.append(f"| {nm} | {e['k']} | {_f(e[f'd_pass1_R0_R{last}'])} | {_f(e[f'd_passk_R0_R{last}'])} | "
                 f"{_f(e[f'd_sacc_R0_R{last}'])} | {_f(e[f'd_degen_R0_R{last}'])} | "
                 f"{_f(e[f'd_fin_acc_R0_R{last}'])} | {r1} |")
    L += ["", "## Paired run contrasts at the last round (treatment - control)", "",
          "| Contrast | pass@1 | pass@k | sample acc | degenerate |", "|---|---|---|---|---|"]
    for c, e in res["contrasts"].items():
        L.append(f"| {c} (R{e['round']}) | {_f(e['pass1'])} | {_f(e['passk'])} | {_f(e['sacc'])} | {_f(e['degen'])} |")
    L += ["", "## Difficulty-matched finished accuracy (review issue 5)", "",
          "Finished = not degenerate. 'R0 matched' = untrained model's per-problem accuracy weighted",
          "by how many finished samples each problem has at the last round.", "",
          "| Run | finished acc R0 | finished acc last | R0 matched to last mix | last - matched |",
          "|---|---|---|---|---|"]
    for nm, e in res["matched_finished"].items():
        L.append(f"| {nm} | {e['fin_acc_R0']:.1f} | {e['fin_acc_last']:.1f} | "
                 f"{e['R0_matched_to_last_mix']:.1f} | {_f(e['diff'])} |")
    L += ["", "## Wilson 95% intervals", ""]
    for k, v in res["wilson"].items():
        L.append(f"- {k}: {v[0]:.1f}% [{v[1]:.1f}, {v[2]:.1f}]")
    (OUT / "ci.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
