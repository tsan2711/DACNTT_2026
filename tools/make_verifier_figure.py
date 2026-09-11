"""Figure showing what the verifier actually gets wrong.

The deck used to print the strings \\frac and \\dfrac as raw text, which
reads as a rendering bug to anyone who does not already know LaTeX. What the
audience needs to see is that both spellings produce the *same fraction* and
the grader still rejects one of them - so render the maths properly and put
the two source spellings beside it.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "papers" / "figures"

INK, BODY, MUTED = "#16161A", "#3F4149", "#8A8D96"
GREEN, RED = "#0B7A5A", "#B3261E"
PANEL, PANEL_OK, PANEL_BAD = "#F5F5F7", "#EDF7F2", "#FDF0EF"
SANS = "Helvetica Neue"


def row(ax, y, *, source, verdict, note, ok):
    colour = GREEN if ok else RED
    face = PANEL_OK if ok else PANEL_BAD
    ax.add_patch(FancyBboxPatch(
        (0.035, y - 0.115), 0.93, 0.225,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor=face, edgecolor="none", transform=ax.transAxes, zorder=1))

    ax.text(0.075, y, "Model viết:", transform=ax.transAxes, fontsize=13,
            color=MUTED, va="center", zorder=2)
    ax.text(0.215, y, source, transform=ax.transAxes, fontsize=15,
            color=INK, va="center", family="monospace", zorder=2)
    ax.text(0.49, y, "hiện ra là", transform=ax.transAxes, fontsize=13,
            color=MUTED, va="center", zorder=2)
    ax.text(0.625, y, r"$\frac{1}{2}$", transform=ax.transAxes, fontsize=25,
            color=INK, va="center", zorder=2)
    ax.text(0.72, y + (0.028 if note else 0.0), verdict, transform=ax.transAxes,
            fontsize=15, color=colour, va="center", fontweight="bold", zorder=2)
    if note:
        ax.text(0.72, y - 0.055, note, transform=ax.transAxes, fontsize=12,
                color=colour, va="center", zorder=2)


def main() -> None:
    plt.rcParams.update({"font.family": SANS, "mathtext.fontset": "cm"})
    fig, ax = plt.subplots(figsize=(11.2, 3.0))
    ax.axis("off")

    ax.text(0.035, 0.93, "Đáp án đúng của bài là một nửa. Hai cách viết dưới đây "
                         "cho ra cùng một giá trị:",
            transform=ax.transAxes, fontsize=13.5, color=BODY, va="center")

    row(ax, 0.58, source=r"\frac{1}{2}", verdict="máy chấm: ĐÚNG",
        note="", ok=True)
    row(ax, 0.20, source=r"\dfrac{1}{2}", verdict="máy chấm: SAI",
        note="gạch 146/146 lần", ok=False)

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "deck_verifier_bug.png"
    fig.savefig(p, dpi=220, facecolor="white")
    print("wrote", p.name)


if __name__ == "__main__":
    main()
