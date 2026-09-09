"""Figure for Design I (isolated runs A/B/C) — reads metrics.csv, writes PNG.

    .venv/bin/python papers/figures/make_isolated_figure.py

Encoding is deliberately redundant so the figure survives greyscale printing,
which LNCS proceedings often are:
  colour      -> which run   (A / B / C)
  line style  -> which seed  (0 solid, 1 dashed)
  marker      -> which run again (o / s / ^)

Palette validated CVD-safe (all six checks pass, light surface): blue
#0173B2, dark orange #B85C00, green #029E73.

Two panels rather than one dual-axis plot: pass@1 and pass@8 live on very
different levels, and a second y-scale would make the two unreadable
against each other. Both panels share one y range so the panels stay
comparable.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "results" / "viec3"

# label -> (directory, colour, linestyle, marker)
RUNS = [
    ("A seed 0 — MATH-500, orig.", "qwen15b-math500-a", "#0173B2", "-", "o"),
    ("A seed 1 — MATH-500, orig.", "qwen15b-math500-a-seed1", "#0173B2", "--", "o"),
    ("B seed 0 — MATH-500, patched", "qwen15b-math500-b", "#B85C00", "-", "s"),
    ("B seed 1 — MATH-500, patched", "qwen15b-math500-b-seed1", "#B85C00", "--", "s"),
    ("C seed 0 — GSM8K, orig.", "qwen15b-gsm8k-c", "#029E73", "-", "^"),
]

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#d8d8d6"


def read_metrics(run_dir: Path) -> tuple[list[int], list[float], list[float]]:
    """Return (rounds, pass@1 %, pass@8 %) for the locked `reward` preset."""
    rounds: list[int] = []
    p1: list[float] = []
    p8: list[float] = []
    with (run_dir / "metrics.csv").open() as fh:
        for row in csv.DictReader(fh):
            if row["preset"] != "reward":
                continue
            rounds.append(int(row["round"]))
            p1.append(float(row["pass_at_1"]) * 100)
            p8.append(float(row["pass_at_k"]) * 100)
    order = sorted(range(len(rounds)), key=lambda i: rounds[i])
    return ([rounds[i] for i in order], [p1[i] for i in order], [p8[i] for i in order])


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "font.size": 8.5,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
        }
    )

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9), sharey=True)

    series = []
    for label, dirname, colour, ls, marker in RUNS:
        run_dir = RESULTS / dirname
        if not (run_dir / "metrics.csv").exists():
            print(f"  skip (missing): {dirname}")
            continue
        rounds, p1, p8 = read_metrics(run_dir)
        series.append((label, colour, ls, marker))
        for ax, ys in ((axes[0], p1), (axes[1], p8)):
            ax.plot(
                rounds,
                ys,
                color=colour,
                linestyle=ls,
                marker=marker,
                markersize=4.5,
                linewidth=1.6,
                markeredgecolor="white",
                markeredgewidth=0.6,
                zorder=3,
            )

    for ax, title in ((axes[0], "pass@1"), (axes[1], "pass@8")):
        ax.set_title(title, fontsize=9.5, pad=6)
        ax.set_xlabel("GVT round")
        ax.set_xticks([0, 1, 2, 3, 4])
        ax.set_ylim(20, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    axes[0].set_ylabel("accuracy on held-out exam set (%)")

    # Band labels: which dataset each cluster belongs to. Kept inside the
    # axes and in empty regions, so both panels can share one x range —
    # otherwise the panels' x-scales differ and their slopes stop being
    # comparable, which is the whole point of showing them side by side.
    axes[1].text(
        2.0, 82.0, "GSM8K", color="#029E73", fontsize=8, va="center", ha="center"
    )
    axes[1].text(
        2.0, 44.0, "MATH-500", color="#0173B2", fontsize=8, va="center", ha="center"
    )
    for ax in axes:
        ax.set_xlim(-0.25, 4.25)

    handles = [
        Line2D(
            [],
            [],
            color=c,
            linestyle=ls,
            marker=m,
            markersize=4.5,
            linewidth=1.6,
            markeredgecolor="white",
            markeredgewidth=0.6,
            label=label,
        )
        for label, c, ls, m in series
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        frameon=False,
        fontsize=7.6,
        bbox_to_anchor=(0.5, -0.14),
        handlelength=2.6,
        columnspacing=1.4,
    )

    fig.tight_layout()

    out_names = ["isolated_by_round.png"]
    targets = [REPO / "papers" / "figures", REPO / "papers" / "latex"]
    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        for name in out_names:
            path = target / name
            fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
            print(f"wrote {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
