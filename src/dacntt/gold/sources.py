"""Public JSON/JSONL URLs for gold answers. No HuggingFace ``datasets`` client."""

from __future__ import annotations

from dataclasses import dataclass

GSM8K = "gsm8k"
MATH500 = "math500"
#: MATH train pool (PRM800K split: 12,000 problems, disjoint from MATH-500 by
#: id and by problem text, checked 2026-11-09). Not in DATASETS: selection
#: pool only, never an exam.
MATHTRAIN = "mathtrain"
DATASETS = (GSM8K, MATH500)


@dataclass(frozen=True)
class GoldSource:
    name: str
    url: str
    filename: str


SOURCES: dict[str, GoldSource] = {
    GSM8K: GoldSource(
        name=GSM8K,
        url=(
            "https://raw.githubusercontent.com/openai/grade-school-math/"
            "master/grade_school_math/data/test.jsonl"
        ),
        filename="gsm8k_test.jsonl",
    ),
    MATH500: GoldSource(
        name=MATH500,
        url=(
            "https://huggingface.co/datasets/HuggingFaceH4/MATH-500/"
            "resolve/main/test.jsonl"
        ),
        filename="math500_test.jsonl",
    ),
    MATHTRAIN: GoldSource(
        name=MATHTRAIN,
        url=(
            "https://media.githubusercontent.com/media/openai/prm800k/"
            "main/prm800k/math_splits/train.jsonl"
        ),
        filename="mathtrain.jsonl",
    ),
}
