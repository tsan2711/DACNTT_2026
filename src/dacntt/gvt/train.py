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

    def train(self, examples: Sequence[TrainExample]) -> None:
        """Update the generator from accepted solutions."""
        ...


class NoOpTrain:
    """Dry-run / tests: record pairs, do not load a model."""

    def __init__(self) -> None:
        self.examples: list[TrainExample] = []
        self.adapter_path: str | None = None

    def train(self, examples: Sequence[TrainExample]) -> None:
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

    def train(self, examples: Sequence[TrainExample]) -> None:
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
        learning_rate: float = 1e-5,
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
        self.examples: list[TrainExample] = []

    def train(self, examples: Sequence[TrainExample]) -> None:
        self.examples.extend(examples)
        if not examples:
            return
        data_dir = self.adapter_path.parent / "sft_data"
        _write_sft_jsonl(data_dir, examples)
        self.adapter_path.mkdir(parents=True, exist_ok=True)
        self._train_lora(data_dir / "train.jsonl")

    def _train_lora(self, train_jsonl: Path) -> None:
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
        model = AutoModelForCausalLM.from_pretrained(self.model_id, torch_dtype=dtype)
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
