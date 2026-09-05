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
    train_item_ids: frozenset[str] | None = None,
    test_item_ids: frozenset[str] | None = None,
    select_all: bool = False,
) -> list[RoundRecord]:
    """on_round, if given, runs after each round is appended — lets the
    caller write partial results to disk as it goes, so a long run (e.g.
    Kaggle, killed by a session time limit) doesn't lose everything if it
    doesn't reach the end.

    ``train_item_ids``/``test_item_ids`` (Giai đoạn 2): if given, restrict
    training examples to ``train_item_ids`` and pass@*/styles-ABC scoring to
    ``test_item_ids`` — a held-out split, instead of both using every item in
    ``items``. Generation still runs over all of ``items`` either way (same
    generate cost, just partitioned after). Leave both ``None`` for the old
    behaviour (select and exam share the same full set).

    ``select_all`` (Giai đoạn 4 ablation): skip the verifier gate at select
    time, train on every generated solution regardless of correctness — see
    ``select_batch``.
    """
    records: list[RoundRecord] = []
    prev_flags: list[list[bool]] | None = None
    for index in range(rounds):
        record = _one_exam(
            items,
            generator,
            exam_adapters,
            k,
            index,
            prev_flags,
            locked_exam,
            test_item_ids=test_item_ids,
        )
        examples = _select_examples(
            items,
            record.generations,
            select_adapter,
            train_item_ids=train_item_ids,
            select_all=select_all,
        )
        record.n_selected = len(examples)
        if train:
            trainer.train(examples, round=index)
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
            _one_exam(
                items,
                generator,
                exam_adapters,
                k,
                rounds,
                prev_flags,
                locked_exam,
                test_item_ids=test_item_ids,
            )
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
    *,
    test_item_ids: frozenset[str] | None = None,
) -> RoundRecord:
    generate_batch = getattr(generator, "generate_batch", None)
    if callable(generate_batch):
        generations = generate_batch([item.problem for item in items], k=k)
    else:
        generations = [generator.generate(item.problem, k=k) for item in items]

    if test_item_ids is None:
        exam_items, exam_generations = items, generations
    else:
        paired = [
            (item, texts)
            for item, texts in zip(items, generations)
            if _item_key(item) in test_item_ids
        ]
        exam_items = [p[0] for p in paired]
        exam_generations = [p[1] for p in paired]

    flags: dict[str, list[list[bool]]] = {}
    for preset, adapter in exam_adapters.items():
        flags[preset] = [
            [adapter.verify(item.gold, text).accepted for text in texts]
            for item, texts in zip(exam_items, exam_generations)
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
    *,
    train_item_ids: frozenset[str] | None = None,
    select_all: bool = False,
) -> list[TrainExample]:
    examples: list[TrainExample] = []
    for item, texts in zip(items, generations):
        if train_item_ids is not None and _item_key(item) not in train_item_ids:
            continue
        for solution in select_batch(item.gold, texts, adapter, select_all=select_all):
            examples.append(TrainExample(item.problem, solution))
    return examples


def _item_key(item: GoldItem) -> str:
    return f"{item.dataset}:{item.item_id}"
