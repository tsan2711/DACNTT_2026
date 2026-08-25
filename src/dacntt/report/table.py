"""CSV + Markdown table for việc 1."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TableRow:
    dataset: str
    variant_id: str
    variant_label: str
    preset: str
    n_reject: int
    n: int
    reason_guess: str

    @property
    def rate(self) -> float:
        if self.n == 0:
            return 0.0
        return self.n_reject / self.n


def write_reports(rows: list[TableRow], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "table.csv"
    md_path = out_dir / "table.md"
    _write_csv(rows, csv_path)
    _write_markdown(rows, md_path)
    return csv_path, md_path


def majority_reasons(reasons: list[str]) -> str:
    if not reasons:
        return "—"
    counts = Counter(reasons)
    return ", ".join(f"{name} ({count})" for name, count in counts.most_common())


def _write_csv(rows: list[TableRow], path: Path) -> None:
    fieldnames = [
        "dataset",
        "variant_id",
        "variant_label",
        "preset",
        "n_reject",
        "n",
        "rate",
        "reason_guess",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "dataset": row.dataset,
                    "variant_id": row.variant_id,
                    "variant_label": row.variant_label,
                    "preset": row.preset,
                    "n_reject": row.n_reject,
                    "n": row.n,
                    "rate": f"{row.rate:.4f}",
                    "reason_guess": row.reason_guess,
                }
            )


def _write_markdown(rows: list[TableRow], path: Path) -> None:
    lines = [
        "# Việc 1 — lệch máy chấm vì cách viết",
        "",
        "Mỗi hàng = bộ bài × kiểu viết × preset. `False` = gạch nhầm (giá trị sách, chỉ đổi chữ).",
        "",
        "| Bộ bài | Kiểu viết | Preset | Số lần gạch / tổng | Tỷ lệ | Lý do đoán |",
        "|--------|-----------|--------|---------------------|-------|------------|",
    ]
    for row in rows:
        rate = "—" if row.n == 0 else f"{row.rate:.1%}"
        lines.append(
            f"| {row.dataset} | {row.variant_label} | {row.preset} "
            f"| {row.n_reject} / {row.n} | {rate} | {row.reason_guess} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
