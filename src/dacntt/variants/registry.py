"""Writing-style registry. Add a kiểu = add one rewrite function + one spec row."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from dacntt.gold.sources import GSM8K
from dacntt.variants import rewrite

RewriteFn = Callable[[str], str | None]


@dataclass(frozen=True)
class VariantSpec:
    id: str
    label: str
    rewrite: RewriteFn
    datasets: frozenset[str] | None = None


# Mục 6 list. ``int_float`` is GSM8K-only (18 vs 18.0).
# Thập phân is two specs so ``0.5`` and ``0.50`` both show up in the table.
VARIANTS: tuple[VariantSpec, ...] = (
    VariantSpec("plain", "Số trần", rewrite.rewrite_plain),
    VariantSpec("decimal", "Thập phân", rewrite.rewrite_decimal),
    VariantSpec("decimal_trailing", "Thập phân (0.50)", rewrite.rewrite_decimal_trailing),
    VariantSpec("frac", "LaTeX thường", rewrite.rewrite_frac),
    VariantSpec("dfrac", "LaTeX khác lệnh (dfrac)", rewrite.rewrite_dfrac),
    VariantSpec("tfrac", "LaTeX khác lệnh (tfrac)", rewrite.rewrite_tfrac),
    VariantSpec("boxed", "Có hộp", rewrite.rewrite_boxed),
    VariantSpec("dollar", "Có dấu đô la", rewrite.rewrite_dollar),
    VariantSpec("sentence", "Có câu", rewrite.rewrite_sentence),
    VariantSpec("assignment", "Có ẩn", rewrite.rewrite_assignment),
    VariantSpec("unit", "Có đơn vị", rewrite.rewrite_unit),
    VariantSpec(
        "int_float",
        "Số nguyên tương đương",
        rewrite.rewrite_int_float,
        datasets=frozenset({GSM8K}),
    ),
)


def variants_for(dataset: str | None = None) -> tuple[VariantSpec, ...]:
    if dataset is None:
        return tuple(spec for spec in VARIANTS if spec.datasets is None)
    return tuple(
        spec
        for spec in VARIANTS
        if spec.datasets is None or dataset in spec.datasets
    )


def apply_all(gold: str, dataset: str | None = None) -> list[tuple[VariantSpec, str]]:
    """Rewrite ``gold``. Specs that cannot apply are omitted (not counted in n)."""
    rows: list[tuple[VariantSpec, str]] = []
    for spec in variants_for(dataset):
        text = spec.rewrite(gold)
        if text is None:
            continue
        rows.append((spec, text))
    return rows
