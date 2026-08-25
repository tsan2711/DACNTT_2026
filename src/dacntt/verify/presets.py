"""Parse presets. Gold is always parsed with the default extractor."""

from __future__ import annotations

from typing import Any

PRESET_DEFAULT = "default"
PRESET_REWARD = "reward"
PRESETS = (PRESET_DEFAULT, PRESET_REWARD)


def extraction_config(preset: str) -> list[Any] | None:
    """Return ``parse(..., extraction_config=...)`` for a writing-style string.

    ``None`` means math-verify's own default (Latex + Expr).
    """
    if preset == PRESET_DEFAULT:
        return None
    if preset == PRESET_REWARD:
        return _reward_extraction_config()
    raise ValueError(f"unknown preset {preset!r}; expected one of {PRESETS}")


def _reward_extraction_config() -> list[Any]:
    from math_verify import ExprExtractionConfig, LatexExtractionConfig, LatexNormalizationConfig

    return [
        LatexExtractionConfig(
            boxed_match_priority=0,
            normalization_config=LatexNormalizationConfig(
                basic_latex=True,
                units=True,
                malformed_operators=False,
                nits=False,
                boxed="all",
                equations=False,
            ),
        ),
        ExprExtractionConfig(),
    ]
