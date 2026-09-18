"""Figures for Design P (pooled runs) — reads table.md, writes two PNGs.

    .venv/bin/python papers/figures/make_design_p_figures.py

Writes pass_at_k_by_round.png (Fig. 1) and selected_pool_by_round.png
(Fig. 2). Same style and CVD-safe palette as make_isolated_figure.py; blue
= 0.5B, dark orange = 1.5B, with distinct markers so the figures survive
greyscale printing.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "results" / "viec3"

# label -> (directory, colour, marker)
MODELS = [
    ("0.5B", "qwen05b-n500", "#0173B2", "o"),
    ("1.5B", "qwen15b-n500", "#B85C00", "s"),
]

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#d8d8d6"


def read_table(run_dir: Path) -> dict[int, tuple[float, float, int]]:
    """Return {round: (pass@1 %, pass@8 %, kept)} for the `reward` preset.

    Parses the first markdown table of table.md; only columns 0-4
    (round, preset, pass@1, pass@8, kept) are used, so the localized
    header text of the remaining columns does not matter.
    """
    rows: dict[int, tuple[float, float, int]] = {}
    for line in (run_dir / "table.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit() or cells[1] != "reward":
            continue
        rows[int(cells[0])] = (
            float(cells[2].rstrip("%")),
            float(cells[3].rstrip("%")),
            int(cells[4]),
        )
    return rows


def style_axes(ax) -> None:
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xlim(-0.25, 4.25)
    ax.set_xlabel("GVT round")
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def plot_series(ax, rounds, ys, colour, marker, label) -> None:
    ax.plot(
        rounds,
        ys,
        color=colour,
        marker=marker,
        markersize=4.5,
        linewidth=1.6,
        markeredgecolor="white",
        markeredgewidth=0.6,
        label=label,
        zorder=3,
    )


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

    data = {name: read_table(RESULTS / dirname) for name, dirname, _, _ in MODELS}

    # Figure 1: pass@1 and pass@8, one panel each, shared y range.
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9), sharey=True)
    for name, _, colour, marker in MODELS:
        rounds = sorted(data[name])
        plot_series(axes[0], rounds, [data[name][r][0] for r in rounds], colour, marker, name)
        plot_series(axes[1], rounds, [data[name][r][1] for r in rounds], colour, marker, name)
    for ax, title in ((axes[0], "pass@1"), (axes[1], "pass@8")):
        ax.set_title(title, fontsize=9.5, pad=6)
        ax.set_ylim(0, 80)
        style_axes(ax)
    axes[0].set_ylabel("accuracy on selection set (%)")
    axes[1].legend(frameon=False, loc="upper right", fontsize=8)
    fig.tight_layout()

    # Figure 2: number of solutions kept for training, per round.
    fig2, ax2 = plt.subplots(figsize=(4.4, 3.0))
    for name, _, colour, marker in MODELS:
        rounds = sorted(data[name])
        kept = [data[name][r][2] for r in rounds]
        change = (kept[-1] - kept[0]) / kept[0] * 100
        plot_series(
            ax2, rounds, kept, colour, marker, f"{name} ({change:+.0f}%)".replace("-", "−")
        )
    style_axes(ax2)
    ax2.set_ylabel("solutions kept for training")
    ax2.legend(frameon=False, loc="upper right", fontsize=8)
    fig2.tight_layout()

    targets = [REPO / "papers" / "figures", REPO / "papers" / "latex"]
    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        for f, name in ((fig, "pass_at_k_by_round.png"), (fig2, "selected_pool_by_round.png")):
            path = target / name
            f.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
            print(f"wrote {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
