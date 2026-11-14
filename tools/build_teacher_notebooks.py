"""Dựng 2 notebook Kaggle cho positive gate "teacher" (plan nước rút 2026-11-15, B1/B2).

    kaggle kernels pull tscute/notebook3132693bf1 -p /tmp/kmeta -m          # metadata (GPU T4, internet)
    python tools/build_teacher_notebooks.py b1 --meta /tmp/kmeta/kernel-metadata.json --out /tmp/nb_b1 \
        [--model Qwen/Qwen2.5-7B-Instruct]  # B1: sinh lời giải teacher (2xT4 -> chọn "GPU T4 x2" trong metadata)
    python tools/build_teacher_notebooks.py b2 --meta ... --out /tmp/nb_b2 \
        --teacher results/viec3/teacher-gen-7b/teacher_solutions.jsonl --seed 1

B1 = MỘT ô GPU duy nhất (teacher_gen.py, resumable, bọc kill-khi-GPU-0%).
B2 = MỘT ô GPU duy nhất (gate: SFT trên lời giải teacher, recipe vòng cuối) qua kaggle_driver, file teacher
nhúng trong overlay. Không có smoke cell (luật Kaggle của dự án).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_kaggle_notebook import MODEL, cell0, overlay_blob  # noqa: E402

B1_CELL = '''import subprocess, sys, os, json
os.environ.update(env)
sys.path.insert(0, "experiments/viec3")
from kaggle_driver import run_child, StallTracker
out = "/kaggle/working/results/viec3/{name}"
os.makedirs(out, exist_ok=True)
cmd = ["python", "-u", "-m", "experiments.viec3.teacher_gen", "--model", "{model}", "--out", out,
       "--seed", "{seed}", "--k", "4", "--max-tokens", "1024", "--keep", "298"]
for attempt in range(4):                       # resumable: a stalled/killed attempt continues where it stopped
    status = run_child(cmd, __import__("pathlib").Path("/kaggle/working/run_{name}.log"), StallTracker(30 * 60), poll=10.0)
    print("attempt", attempt, status, flush=True)
    if os.path.exists(out + "/summary.json"):
        break
print(open(out + "/summary.json").read() if os.path.exists(out + "/summary.json") else "NO SUMMARY")
'''

B2_ARGS = ["--n", "500", "--rounds", "2", "--k", "2", "--max-tokens", "1024", "--seed", "{seed}",
           "--learning-rate", "{lr}", "--fixed-pipeline", "--train-pool-n", "300", "--completion-only",
           "--lora-targets", "all-linear", "--max-seq-length", "1024", "--train-on-gold",
           "--teacher-solutions", "experiments/viec3/teacher_solutions.jsonl", "--max-train-examples", "298"]

B2_CELL = '''import subprocess, signal, os
out = "/kaggle/working/results/viec3/{name}"
cmd = ["python", "-u", "experiments/viec3/kaggle_driver.py", "--out", out, "--rounds", "2",
       "--log", "/kaggle/working/run_{name}.log", "--idle-minutes", "25", "--budget-hours", "5", "--",
       "python", "-u", "-m", "experiments.viec3.run", "--mode", "hf", "--model", "{model}", "--dataset", "math500",
       {args}, "--out", out]
p = subprocess.Popen(cmd, env=env, start_new_session=True)
try:
    code = p.wait(timeout=5.5 * 3600)
except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL); code = "TIMEOUT"
print("{name} driver exit:", code)
subprocess.run(["python", "experiments/viec3/review_cpu/gate_anatomy.py", out])
'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=["b1", "b2"])
    ap.add_argument("--meta", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--teacher", type=Path)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--lr", default="1e-4")
    ap.add_argument("--name", default=None)
    a = ap.parse_args()
    extra = {}
    if a.which == "b1":
        name = a.name or "teacher-gen-7b"
        cell1 = B1_CELL.format(name=name, model=a.model, seed=a.seed)
    else:
        if not a.teacher or not a.teacher.is_file():
            ap.error("b2 needs --teacher FILE")
        name = a.name or f"gate-teacher-s{a.seed}"
        extra["experiments/viec3/teacher_solutions.jsonl"] = a.teacher
        args = ", ".join(json.dumps(x.format(seed=a.seed, lr=a.lr)) for x in B2_ARGS)
        cell1 = B2_CELL.format(name=name, model=MODEL, args=args)
    compile(cell1, "cell1", "exec")
    meta = json.loads(a.meta.read_text())
    cells = [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": c.splitlines(True)}
             for c in (cell0(overlay_blob(extra)), cell1)]
    nb = {"cells": cells, "nbformat": 4, "nbformat_minor": 4,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}}}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / meta["code_file"]).write_text(json.dumps(nb), encoding="utf-8")
    shutil.copy(a.meta, a.out / "kernel-metadata.json")
    print("built", a.out, a.which, name)


if __name__ == "__main__":
    main()
