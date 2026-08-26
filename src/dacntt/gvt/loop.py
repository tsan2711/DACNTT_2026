"""One GVT cycle: generate → verify → select → train, and measure."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
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
    on_round: Callable[[list[RoundRecord]], None] | None = None,
) -> list[RoundRecord]:
    """on_round, if given, runs after each round is appended — lets the
    caller write partial results to disk as it goes, so a long run (e.g.
    Kaggle, killed by a session time limit) doesn't lose everything if it
    doesn't reach the end."""
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
        if on_round is not None:
            on_round(records)
    if extra_exam:
        records.append(
            _one_exam(items, generator, exam_adapters, k, rounds, prev_flags, locked_exam)
        )
        if on_round is not None:
            on_round(records)
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
    generate_batch = getattr(generator, "generate_batch", None)
    if callable(generate_batch):
        generations = generate_batch([item.problem for item in items], k=k)
    else:
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
