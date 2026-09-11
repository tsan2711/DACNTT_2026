"""Charts for the week 2-3 deck.

Two charts carry the two claims the tables state in numbers:
  1. pass@8 collapses under the pooled design and does not under the isolated
     one - the headline result.
  2. Runs A and B lie on top of each other - the null control, which is far
     more convincing seen than read.

Palette is the CVD-safe trio already validated for the paper figure, so the
deck and the paper agree visually: blue #0173B2, orange #B85C00, green
#029E73. Colour here encodes the *design* (pooled vs isolated), because that
is the distinction both charts exist to draw.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "papers" / "figures"

BLUE, ORANGE, GREEN = "#0173B2", "#B85C00", "#029E73"
INK, BODY, MUTED, GRID = "#16161A", "#3F4149", "#8A8D96", "#E6E6EA"
FONT = "Helvetica Neue"

ROUNDS = [0, 1, 2, 3, 4]

# pooled design (--dataset both, scored on the selection set)
POOLED_GSM8K_P8 = [91.4, 90.4, 89.0, 82.2, 65.8]
POOLED_MATH_P8 = [53.8, 52.6, 51.4, 45.0, 31.4]
# isolated design (one adapter per dataset, held-out exam set)
ISO_A_P8 = [57.3, 56.7, 54.7, 57.3, 56.0]
ISO_A1_P8 = [58.7, 60.7, 59.3, 59.3, 58.7]
ISO_C_P8 = [92.7, 90.7, 93.3, 90.0, 90.0]

A0_P1 = [32.0, 29.3, 28.0, 29.3, 29.3]
B0_P1 = [32.0, 28.7, 28.7, 28.7, 28.7]
A1_P1 = [36.7, 32.7, 32.7, 31.3, 33.3]
B1_P1 = [37.3, 32.0, 32.7, 31.3, 33.3]


def style(ax, *, ylim, yticks, ylabel=None):
    ax.set_xticks(ROUNDS)
    ax.set_xlim(-0.15, 4.35)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ax.grid(axis="y", color=GRID, linewidth=0.9, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0, labelsize=11)
    ax.set_xlabel("vòng", color=MUTED, fontsize=11, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED, fontsize=11, labelpad=10)


def line(ax, ys, colour, *, dashed=False, marker="o", width=2.6, z=3):
    ax.plot(ROUNDS, ys, color=colour, linewidth=width, zorder=z,
            linestyle=(0, (5, 2.4)) if dashed else "-",
            marker=marker, markersize=6.5,
            markeredgecolor="white", markeredgewidth=1.6)


def endlabel(ax, ys, text, colour, *, dy=0.0, weight="bold", size=11.5):
    ax.annotate(text, xy=(4, ys[-1]), xytext=(8, dy), textcoords="offset points",
                color=colour, fontsize=size, fontweight=weight,
                va="center", ha="left")


def chart_collapse():
    plt.rcParams.update({"font.family": FONT, "font.size": 11})
    fig, ax = plt.subplots(figsize=(10.6, 4.5))

    for ys in (POOLED_GSM8K_P8, POOLED_MATH_P8):
        line(ax, ys, ORANGE, marker="s", z=4)
    for ys, dash in ((ISO_A_P8, False), (ISO_A1_P8, True)):
        line(ax, ys, BLUE, dashed=dash)
    line(ax, ISO_C_P8, GREEN, marker="^")

    endlabel(ax, ISO_C_P8, "GSM8K cô lập", GREEN, dy=6)
    endlabel(ax, POOLED_GSM8K_P8, "GSM8K gộp", ORANGE, dy=-4)
    endlabel(ax, ISO_A_P8, "MATH-500 cô lập", BLUE, dy=4)
    endlabel(ax, POOLED_MATH_P8, "MATH-500 gộp", ORANGE, dy=-2)

    style(ax, ylim=(20, 100), yticks=[20, 40, 60, 80, 100], ylabel="pass@8  (%)")
    ax.annotate("thiết kế gộp:\nmất 22–26 điểm", xy=(3.55, 48), color=ORANGE,
                fontsize=11.5, fontweight="bold", ha="center", va="center")
    ax.annotate("cô lập: đi ngang", xy=(1.35, 65.5), color=BLUE,
                fontsize=11.5, fontweight="bold", ha="center", va="center")
    fig.subplots_adjust(left=0.075, right=0.80, top=0.96, bottom=0.14)
    p = OUT / "deck_collapse.png"
    fig.savefig(p, dpi=220, facecolor="white")
    print("wrote", p.name)
    plt.close(fig)


def chart_control():
    plt.rcParams.update({"font.family": FONT, "font.size": 11})
    fig, ax = plt.subplots(figsize=(10.6, 4.3))

    line(ax, A0_P1, BLUE)
    line(ax, B0_P1, ORANGE, marker="s")
    line(ax, A1_P1, BLUE, dashed=True)
    line(ax, B1_P1, ORANGE, dashed=True, marker="s")

    endlabel(ax, A1_P1, "seed 1", MUTED, dy=9, weight="normal")
    endlabel(ax, A0_P1, "seed 0", MUTED, dy=-8, weight="normal")
    # From round 2 at seed 1 the two runs report identical pass@1, so only the
    # last-drawn line is visible. Say so, or it reads as a missing series.
    ax.annotate("từ vòng 2: hai đường trùng khít", xy=(3.0, 35.0), color=BODY,
                fontsize=11, ha="center", va="center")

    style(ax, ylim=(24, 42), yticks=[24, 28, 32, 36, 40], ylabel="pass@1  (%)")
    handles = [
        plt.Line2D([], [], color=BLUE, linewidth=2.6, marker="o", markersize=6.5,
                   markeredgecolor="white", markeredgewidth=1.6, label="A — verifier gốc"),
        plt.Line2D([], [], color=ORANGE, linewidth=2.6, marker="s", markersize=6.5,
                   markeredgecolor="white", markeredgewidth=1.6, label="B — verifier ĐÃ VÁ"),
    ]
    leg = ax.legend(handles=handles, loc="upper right", frameon=False,
                    fontsize=12, handlelength=2.4, ncol=2)
    for t in leg.get_texts():
        t.set_color(BODY)
    fig.subplots_adjust(left=0.075, right=0.88, top=0.96, bottom=0.15)
    p = OUT / "deck_control.png"
    fig.savefig(p, dpi=220, facecolor="white")
    print("wrote", p.name)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    chart_collapse()
    chart_control()
