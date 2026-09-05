"""Giai đoạn 5 (papers/KE-HOACH-MO-RONG.md): direct evidence for or against
the "bigger model overfits the shrinking pool faster" hypothesis in
Discussion §5.2 of the paper draft, currently only argued in prose.

Two cheap measurements, both computed from files a Kaggle run already
produces (no new GPU run needed once `generations.jsonl` and
`train_logs/round_*.json` are downloaded — see run.py's module docstring):

- pre-filter output diversity per round, from `generations.jsonl`
- final training loss per round, from `train_logs/round_*.json`
  (`HfLoraSftTrain` writes these when `run_rounds` is given a round index)
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from dacntt.read import extract_final, normalize_math


@dataclass(frozen=True)
class RoundDiversity:
    round: int
    n_items: int
    mean_unique_text_ratio: float  # avg over items of (unique raw texts among k) / k
    mean_unique_answer_ratio: float  # avg over items of (unique normalized answers among k) / k
    all_same_answer_frac: float  # fraction of items where all k give the same normalized answer


def diversity_by_round(generations_path: Path) -> list[RoundDiversity]:
    """Pre-filter diversity: how much do the k samples for one problem differ
    from each other, before the verifier ever sees them. Read straight from
    `generations.jsonl` — one line per (round, item), `texts` is the k
    samples. A model that collapses onto one output per problem *before*
    filtering points at the model itself, not the verifier, as the source of
    narrowing; verifier filtering would then only be amplifying an
    already-narrow distribution.

    Two metrics, because raw-text uniqueness is a poor proxy on its own: at
    temperature>0, k samples are almost always byte-different even when the
    model has fully converged on one *answer* (different token choices in the
    reasoning steps, same final boxed value) — confirmed empirically on both
    real Kaggle runs (mean_unique_text_ratio stayed ~0.999-1.000 every round
    for both 0.5B and 1.5B, despite pass@k and style collapsing hard by round
    4). ``mean_unique_answer_ratio``/``all_same_answer_frac`` extract each
    sample's final answer (same `extract_final`/`normalize_math` the style
    counters use) before comparing, so they catch answer-level convergence
    that raw-text uniqueness cannot.
    """
    by_round: dict[int, list[list[str]]] = {}
    for row in _read_jsonl(generations_path):
        by_round.setdefault(row["round"], []).append(row["texts"])

    out: list[RoundDiversity] = []
    for round_index in sorted(by_round):
        rows = by_round[round_index]
        text_ratios = []
        answer_ratios = []
        all_same_answer = 0
        for texts in rows:
            if not texts:
                continue
            text_ratios.append(len(set(texts)) / len(texts))
            answers = [normalize_math(extract_final(text) or text) for text in texts]
            unique_answers = len(set(answers))
            answer_ratios.append(unique_answers / len(answers))
            if unique_answers == 1:
                all_same_answer += 1
        n = len(text_ratios)
        out.append(
            RoundDiversity(
                round=round_index,
                n_items=n,
                mean_unique_text_ratio=sum(text_ratios) / n if n else 0.0,
                mean_unique_answer_ratio=sum(answer_ratios) / n if n else 0.0,
                all_same_answer_frac=all_same_answer / n if n else 0.0,
            )
        )
    return out


@dataclass(frozen=True)
class RoundTrainLoss:
    round: int
    final_loss: float | None
    n_log_steps: int


def train_loss_by_round(log_dir: Path) -> list[RoundTrainLoss]:
    """Final `SFTTrainer` loss per round, from the `trainer.state.log_history`
    dumps `HfLoraSftTrain` writes to `train_logs/round_{n}.json`. A model
    fitting the (shrinking, skewed) pool faster/tighter each round should
    show a lower final loss earlier, relative to a model that fits more
    slowly — the direct test for Discussion §5.2's "bigger model overfits
    faster" hypothesis.
    """
    out: list[RoundTrainLoss] = []
    for path in sorted(log_dir.glob("round_*.json"), key=_round_index_of):
        round_index = _round_index_of(path)
        history = json.loads(path.read_text(encoding="utf-8"))
        losses = [entry["loss"] for entry in history if "loss" in entry]
        out.append(
            RoundTrainLoss(
                round=round_index,
                final_loss=losses[-1] if losses else None,
                n_log_steps=len(losses),
            )
        )
    return out


def _round_index_of(path: Path) -> int:
    # "round_3.json" -> 3
    return int(path.stem.split("_")[-1])


def _read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)
