"""One GVT cycle: generate → verify → select → train, and measure."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from dacntt.gold.load import GoldItem
from dacntt.gvt.generate import Generate
from dacntt.gvt.measure import abc_shift, count_styles, pass_at
from dacntt.gvt.select import select_batch
from dacntt.gvt.train import Train, TrainExample
from dacntt.verify.adapter import MathVerifyAdapter


@dataclass
class RoundRecord:
    round: int
    pass_at: dict[int, dict[str, float]]
    styles: dict[str, int]
    n_selected: int
    abc: dict[str, int] | None
    flags: dict[str, list[list[bool]]] = field(default_factory=dict)
    generations: list[list[str]] = field(default_factory=list)
    n_examples_trained: int = 0


def run_rounds(
    items: Sequence[GoldItem],
    *,
    generator: Generate,
    trainer: Train,
    select_adapter: MathVerifyAdapter,
    exam_adapters: Mapping[str, MathVerifyAdapter],
    rounds: int,
    k: int,
    train: bool = True,
    extra_exam: bool = False,
    locked_exam: str = "reward",
) -> list[RoundRecord]:
    records: list[RoundRecord] = []
    prev_flags: list[list[bool]] | None = None
    for index in range(rounds):
        record = _one_exam(items, generator, exam_adapters, k, index, prev_flags, locked_exam)
        examples = _select_examples(items, record.generations, select_adapter)
        record.n_selected = len(examples)
        if train:
            trainer.train(examples)
            record.n_examples_trained = len(examples)
            if examples:
                reload = getattr(generator, "reload", None)
                adapter_path = getattr(trainer, "adapter_path", None)
                if callable(reload) and adapter_path:
                    reload(str(adapter_path))
        records.append(record)
        prev_flags = record.flags.get(locked_exam)
    if extra_exam:
        records.append(
            _one_exam(items, generator, exam_adapters, k, rounds, prev_flags, locked_exam)
        )
    return records


def _one_exam(
    items: Sequence[GoldItem],
    generator: Generate,
    exam_adapters: Mapping[str, MathVerifyAdapter],
    k: int,
    round_index: int,
    prev_flags: list[list[bool]] | None,
    locked_exam: str,
) -> RoundRecord:
    generations = [generator.generate(item.problem, k=k) for item in items]
    flags: dict[str, list[list[bool]]] = {}
    for preset, adapter in exam_adapters.items():
        flags[preset] = [
            [adapter.verify(item.gold, text).accepted for text in texts]
            for item, texts in zip(items, generations)
        ]
    ks = sorted({1, k})
    pass_table = {
        kind: {preset: pass_at(rows, kind) for preset, rows in flags.items()}
        for kind in ks
    }
    flat = [text for texts in generations for text in texts]
    locked = flags.get(locked_exam)
    abc = abc_shift(prev_flags, locked) if prev_flags is not None and locked is not None else None
    return RoundRecord(
        round=round_index,
        pass_at=pass_table,
        styles=count_styles(flat),
        n_selected=0,
        abc=abc,
        flags=flags,
        generations=generations,
    )


def _select_examples(
    items: Sequence[GoldItem],
    generations: Sequence[Sequence[str]],
    adapter: MathVerifyAdapter,
) -> list[TrainExample]:
    examples: list[TrainExample] = []
    for item, texts in zip(items, generations):
        for solution in select_batch(item.gold, texts, adapter):
            examples.append(TrainExample(item.problem, solution))
    return examples
