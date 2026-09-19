"""Train: teach the same SLM on selected (problem, solution) pairs."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from dacntt.gvt.generate import user_prompt


@dataclass(frozen=True)
class TrainExample:
    problem: str
    solution: str


@runtime_checkable
class Train(Protocol):
    """Dạy lại chính SLM bằng những bài được giữ, rồi lặp."""

    def train(self, examples: Sequence[TrainExample], *, round: int | None = None) -> None:
        """Update the generator from accepted solutions.

        ``round`` (Giai đoạn 5, optional): the GVT round index, so an
        implementation that logs per-round training loss (see
        ``HfLoraSftTrain``) can namespace its output. Ignored otherwise.
        """
        ...


class NoOpTrain:
    """Dry-run / tests: record pairs, do not load a model."""

    def __init__(self) -> None:
        self.examples: list[TrainExample] = []
        self.adapter_path: str | None = None

    def train(self, examples: Sequence[TrainExample], *, round: int | None = None) -> None:
        self.examples.extend(examples)


class MlxLoraTrain:
    """Mac toy: short LoRA SFT via mlx-lm. Not GRPO; not paper numbers."""

    def __init__(
        self,
        model_id: str,
        adapter_path: Path,
        *,
        iters: int = 30,
        batch_size: int = 1,
        num_layers: int = 8,
        max_seq_length: int = 512,
        learning_rate: float = 1e-5,
    ) -> None:
        self.model_id = model_id
        self.adapter_path = adapter_path
        self.iters = iters
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.max_seq_length = max_seq_length
        self.learning_rate = learning_rate
        self.examples: list[TrainExample] = []
        self.last_returncode: int | None = None

    def train(self, examples: Sequence[TrainExample], *, round: int | None = None) -> None:
        self.examples.extend(examples)
        if not examples:
            return
        data_dir = self.adapter_path.parent / "sft_data"
        _write_sft_jsonl(data_dir, examples)
        self.adapter_path.mkdir(parents=True, exist_ok=True)
        iters = max(1, min(self.iters, max(4, len(examples))))
        cmd = [
            sys.executable,
            "-m",
            "mlx_lm",
            "lora",
            "--model",
            self.model_id,
            "--data",
            str(data_dir),
            "--train",
            "--iters",
            str(iters),
            "--batch-size",
            str(self.batch_size),
            "--num-layers",
            str(self.num_layers),
            "--adapter-path",
            str(self.adapter_path),
            "--max-seq-length",
            str(self.max_seq_length),
            "--learning-rate",
            str(self.learning_rate),
            "--save-every",
            str(iters),
            "--steps-per-eval",
            str(iters + 1),
            "--val-batches",
            "0",
            "--mask-prompt",
        ]
        completed = subprocess.run(cmd, check=False)
        self.last_returncode = completed.returncode
        if completed.returncode != 0:
            raise RuntimeError(
                f"mlx-lm lora failed with code {completed.returncode}; "
                "see experiments/viec3/KAGGLE.md for the GPU path"
            )


class HfLoraSftTrain:
    """Kaggle T4: same SFT-on-selected-examples design as MlxLoraTrain, via
    transformers + peft + TRL SFTTrainer instead of mlx-lm. Each round trains a
    fresh LoRA adapter from the base model on only that round's selected
    examples (no cross-round accumulation) — matches MlxLoraTrain's semantics
    so Mac-toy and Kaggle rounds mean the same thing. Not runnable on Mac
    (no CUDA/torch here); see experiments/viec3/KAGGLE.md.
    """

    def __init__(
        self,
        model_id: str,
        adapter_path: Path,
        *,
        epochs: float = 1.0,
        batch_size: int = 2,
        lora_r: int = 16,
        lora_alpha: int = 32,
        target_modules: Sequence[str] = ("q_proj", "v_proj"),
        max_seq_length: int = 512,
        # 1e-5 (old default) barely moves LoRA r=16 on this model/task —
        # confirmed via experiments/viec3/diagnose_lr.py 2026-09-17: loss
        # stayed flat/noisy (0.84->0.72) at 1e-5 over 1 epoch/120 examples,
        # vs a clean drop (0.63->0.24) at 5e-4. Literature checked live
        # 2026-09-19: arXiv 2602.04998 sweeps LoRA lr over 1e-6..1e-3 with
        # its best cells around 1e-4..1e-3 (no single "5e-4" recommendation);
        # arXiv 2609.01244 reports an optimal LoRA lr near 1e-3, ~33x the
        # full-fine-tuning optimum (3e-5). 5e-4 is inside that range.
        # All prior A/B/C runs used the 1e-5 default — their "no
        # improvement" result may be this, not a genuine finding.
        learning_rate: float = 5e-4,
        log_dir: Path | None = None,
    ) -> None:
        self.model_id = model_id
        self.adapter_path = adapter_path
        self.epochs = epochs
        self.batch_size = batch_size
        self.lora_r = lora_r
        self.lora_alpha = lora_alpha
        self.target_modules = tuple(target_modules)
        self.max_seq_length = max_seq_length
        self.learning_rate = learning_rate
        # Giai đoạn 5: per-round trainer.state.log_history (loss/epoch/step),
        # so a later pass can compare how fast 0.5B vs 1.5B fit each round's
        # shrinking, skewed pool — see papers/KE-HOACH-MO-RONG.md.
        self.log_dir = log_dir or (adapter_path.parent / "train_logs")
        self.examples: list[TrainExample] = []

    def train(self, examples: Sequence[TrainExample], *, round: int | None = None) -> None:
        self.examples.extend(examples)
        if not examples:
            return
        data_dir = self.adapter_path.parent / "sft_data"
        _write_sft_jsonl(data_dir, examples)
        self.adapter_path.mkdir(parents=True, exist_ok=True)
        self._train_lora(data_dir / "train.jsonl", round=round)

    def _train_lora(self, train_jsonl: Path, *, round: int | None = None) -> None:
        from datasets import load_dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from trl import SFTConfig, SFTTrainer

        import torch

        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        # T4 (Turing) has no bf16 tensor cores; "auto" picks the checkpoint's
        # dtype (bf16 for Qwen2.5), which runs on T4 via a slow fp32
        # emulation path. fp16 is the fast path on this GPU (see generate.py).
        dtype = torch.float16 if torch.cuda.is_available() else "auto"
        # low_cpu_mem_usage=True (transformers default since 4.30) lazily
        # materializes each tensor one at a time (tqdm "Loading weights:
        # X%|... Materializing param=...") — seen hanging indefinitely
        # partway through on Kaggle (intermittent, not reproducible every
        # run). RAM isn't the constraint here (confirmed 26GB+ free on the
        # T4 notebook), so force the plain, fully-materialize-then-copy
        # path instead, which doesn't use that lazy loader.
        from dacntt.gvt._load_timeout import load_with_timeout

        model = load_with_timeout(
            lambda: AutoModelForCausalLM.from_pretrained(
                self.model_id, torch_dtype=dtype, low_cpu_mem_usage=False
            ),
            what=f"AutoModelForCausalLM.from_pretrained({self.model_id}) [train]",
        )
        if torch.cuda.is_available():
            model = model.to("cuda")
        peft_config = LoraConfig(
            r=self.lora_r,
            lora_alpha=self.lora_alpha,
            target_modules=list(self.target_modules),
            task_type="CAUSAL_LM",
        )
        train_dataset = load_dataset("json", data_files=str(train_jsonl), split="train")
        args = SFTConfig(
            output_dir=str(self.adapter_path),
            per_device_train_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            learning_rate=self.learning_rate,
            max_length=self.max_seq_length,
            fp16=torch.cuda.is_available(),
            report_to=[],
            save_strategy="no",
            logging_steps=10,
        )
        trainer = SFTTrainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            peft_config=peft_config,
            processing_class=tokenizer,
        )
        trainer.train()
        trainer.model.save_pretrained(str(self.adapter_path))
        tokenizer.save_pretrained(str(self.adapter_path))
        if round is not None:
            self._save_train_log(trainer.state.log_history, round)

    def _save_train_log(self, log_history: list[dict], round: int) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        path = self.log_dir / f"round_{round}.json"
        path.write_text(json.dumps(log_history, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_sft_jsonl(data_dir: Path, examples: Sequence[TrainExample]) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "messages": [
                {"role": "user", "content": user_prompt(ex.problem)},
                {"role": "assistant", "content": ex.solution},
            ]
        }
        for ex in examples
    ]
    train_path = data_dir / "train.jsonl"
    valid_path = data_dir / "valid.jsonl"
    _dump_jsonl(train_path, rows)
    _dump_jsonl(valid_path, rows[:1])


def _dump_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
