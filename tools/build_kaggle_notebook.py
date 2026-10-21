"""Dựng notebook Kaggle chạy các run GVT qua experiments/viec3/kaggle_driver.py.

    # lấy metadata kernel hiện có (id, GPU T4, internet...)
    kaggle kernels pull tscute/notebook3132693bf1 -p /tmp/kmeta -m
    python tools/build_kaggle_notebook.py --meta /tmp/kmeta/kernel-metadata.json \
        --out /tmp/nb_next --runs '[["name", "dataset", seed, "lr", ["--extra", "flag"]], ...]'
    kaggle kernels push -p /tmp/nb_next

Code chưa push lên GitHub được nhúng vào cell 0 dưới dạng tar.gz base64 (ghi đè
lên bản clone), nên notebook luôn chạy đúng code đang có trên máy.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import shutil
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OVERLAY = [
    "src/dacntt/gvt/state.py",
    "src/dacntt/gvt/loop.py",
    "experiments/viec3/run.py",
    "experiments/viec3/kaggle_driver.py",
    "experiments/viec3/reeval.py",
]
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"


def overlay_blob() -> str:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for rel in OVERLAY:
            tar.add(REPO / rel, arcname=rel)
    return base64.b64encode(buf.getvalue()).decode()


def cell0(blob: str) -> str:
    return f'''%pip install -q "math-verify[antlr4_13_2]==0.9.0" torch \\
  "transformers==5.0.0" "trl==1.10.0" "peft==0.19.1" \\
  accelerate datasets "torchao>=0.16.0"

import subprocess, os, sys, base64, io, tarfile
os.chdir("/kaggle/working")
subprocess.run(["rm", "-rf", "/kaggle/working/DACNTT_2026"])
if subprocess.run(["git", "clone", "https://github.com/tsan2711/DACNTT_2026.git", "/kaggle/working/DACNTT_2026"]).returncode != 0:
    raise SystemExit("git clone thất bại")
os.chdir("/kaggle/working/DACNTT_2026")
BLOB = "{blob}"
tarfile.open(fileobj=io.BytesIO(base64.b64decode(BLOB)), mode="r:gz").extractall(".")
env = os.environ.copy()
env["PYTHONPATH"] = "src:."
env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
heartbeat = subprocess.Popen(
    [sys.executable, "-u", "experiments/viec3/heartbeat.py", "/kaggle/working/heartbeat.log"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
print("setup xong")
'''


def run_block(name: str, dataset: str, seed: int, lr: str, extra: list[str], rounds: int, k: int) -> str:
    args = ["--n", "500", "--rounds", str(rounds), "--k", str(k), "--max-tokens", "512", "--seed", str(seed),
            "--holdout-frac", "0.3", "--learning-rate", lr, *extra]
    return f'''
out = "/kaggle/working/results/viec3/{name}"
cmd = ["python", "-u", "experiments/viec3/kaggle_driver.py", "--out", out, "--rounds", "{rounds}",
       "--log", "/kaggle/working/run_{name}.log", "--idle-minutes", "20", "--budget-hours", "4", "--",
       "python", "-u", "-m", "experiments.viec3.run", "--mode", "hf",
       "--model", "{MODEL}", "--dataset", "{dataset}", {", ".join(json.dumps(a) for a in args)},
       "--out", out]
p = subprocess.Popen(cmd, env=env, start_new_session=True)
try:
    code = p.wait(timeout=4.5*3600)
except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL); code = "TIMEOUT"
print("{name} driver exit:", code)'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--meta", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--runs", required=True, help="JSON: [[name, dataset, seed, lr, [extra flags]], ...]")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--k", type=int, default=4)
    args = ap.parse_args()
    runs = json.loads(args.runs)
    cell1 = "import subprocess, signal, os\n" + "\n".join(
        run_block(n, d, s, lr, ex, args.rounds, args.k) for n, d, s, lr, ex in runs
    )
    compile(cell1, "cell1", "exec")
    meta = json.loads(args.meta.read_text())
    cells = [
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": c.splitlines(True)}
        for c in (cell0(overlay_blob()), cell1)
    ]
    nb = {"cells": cells, "nbformat": 4, "nbformat_minor": 4,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}}}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / meta["code_file"]).write_text(json.dumps(nb), encoding="utf-8")
    shutil.copy(args.meta, args.out / "kernel-metadata.json")
    print("built", args.out, f"({len(runs)} runs)")


if __name__ == "__main__":
    main()
