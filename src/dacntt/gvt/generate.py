"""Generate: SLM writes k solutions for one problem. Does not grade."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol, runtime_checkable

from dacntt.variants import rewrite

MATH_USER = "Solve the math problem. Put the final answer in \\boxed{{}}.\n\n{problem}"


@runtime_checkable
class Generate(Protocol):
    """Máy giải toán: đọc đề, sinh k lời giải. Không chấm."""

    def generate(self, problem: str, *, k: int = 1) -> list[str]:
        """Return ``k`` solution texts for ``problem``."""
        ...


def user_prompt(problem: str) -> str:
    return MATH_USER.format(problem=problem)


class ScriptedGenerate:
    """Dry-run generator: fixed texts per problem. No model download."""

    def __init__(self, scripts: Mapping[str, Sequence[str]]) -> None:
        self.scripts = {key: list(value) for key, value in scripts.items()}

    def generate(self, problem: str, *, k: int = 1) -> list[str]:
        rows = self.scripts.get(problem) or ["MISSING"]
        out: list[str] = []
        while len(out) < k:
            out.extend(rows)
        return out[:k]

    @classmethod
    def from_gold(cls, items: Sequence[object], k: int) -> "ScriptedGenerate":
        scripts = {}
        for item in items:
            problem = getattr(item, "problem")
            gold = getattr(item, "gold")
            scripts[problem] = scripted_from_gold(gold, k)
        return cls(scripts)


def scripted_from_gold(gold: str, k: int) -> list[str]:
    """Mix việc-1 styles plus one wrong string so select has something to drop."""
    dfrac = rewrite.rewrite_dfrac(gold)
    decimal = rewrite.rewrite_decimal(gold)
    candidates = [
        rf"\boxed{{{gold}}}",
        f"The answer is {gold}",
        dfrac if dfrac is not None else rf"\dfrac{{{gold}}}{{1}}",
        decimal if decimal is not None else f"{gold}.0",
        "99999",
        f"x = {gold}",
        f"{gold} apples",
        rf"\frac{{{gold}}}{{1}}" if "/" not in gold else gold,
    ]
    out: list[str] = []
    while len(out) < k:
        out.extend(candidates)
    return out[:k]


class MlxGenerate:
    """Qwen (or any mlx-lm chat model). Reload after LoRA so the next round uses new weights."""

    def __init__(
        self,
        model_id: str,
        *,
        adapter_path: str | None = None,
        max_tokens: int = 96,
        temp: float = 0.8,
    ) -> None:
        self.model_id = model_id
        self.adapter_path = adapter_path
        self.max_tokens = max_tokens
        self.temp = temp
        self._model = None
        self._tokenizer = None

    def reload(self, adapter_path: str | None = None) -> None:
        if adapter_path is not None:
            self.adapter_path = adapter_path
        self._model = None
        self._tokenizer = None
        self._ensure()

    def generate(self, problem: str, *, k: int = 1) -> list[str]:
        model, tokenizer = self._ensure()
        from mlx_lm import generate as mlx_generate
        from mlx_lm.sample_utils import make_sampler
        import mlx.core as mx

        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": user_prompt(problem)}],
            add_generation_prompt=True,
            tokenize=False,
        )
        sampler = make_sampler(temp=self.temp)
        texts: list[str] = []
        for index in range(k):
            mx.random.seed(index + 1)
            texts.append(
                mlx_generate(
                    model,
                    tokenizer,
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    sampler=sampler,
                    verbose=False,
                )
            )
        return texts

    def _ensure(self):
        if self._model is None or self._tokenizer is None:
            from mlx_lm import load

            self._model, self._tokenizer = load(
                self.model_id,
                adapter_path=self.adapter_path,
            )
        return self._model, self._tokenizer


class HfGenerate:
    """Kaggle T4: transformers generate, LoRA adapter reload after each round.
    Same role as MlxGenerate but for the GPU path — not runnable on Mac here
    (no CUDA/torch). See experiments/viec3/KAGGLE.md.
    """

    def __init__(
        self,
        model_id: str,
        *,
        adapter_path: str | None = None,
        max_tokens: int = 96,
        temp: float = 0.8,
        gen_batch_size: int = 8,
    ) -> None:
        self.model_id = model_id
        self.adapter_path = adapter_path
        self.max_tokens = max_tokens
        self.temp = temp
        self.gen_batch_size = gen_batch_size
        self._model = None
        self._tokenizer = None

    def reload(self, adapter_path: str | None = None) -> None:
        self.adapter_path = adapter_path
        self._model = None
        self._tokenizer = None
        self._ensure()

    def generate(self, problem: str, *, k: int = 1) -> list[str]:
        return self.generate_batch([problem], k=k)[0]

    def generate_batch(self, problems: Sequence[str], *, k: int = 1) -> list[list[str]]:
        """Batch several problems into one model.generate() call. T4 sits mostly
        idle generating one problem at a time (batch dim = k only); grouping
        problems into gen_batch_size-sized chunks keeps the GPU fed and is the
        main lever for wall-clock time at n=500 (see KAGGLE.md).
        """
        import torch

        model, tokenizer = self._ensure()
        results: list[list[str]] = []
        for start in range(0, len(problems), self.gen_batch_size):
            chunk = problems[start : start + self.gen_batch_size]
            prompts = [
                tokenizer.apply_chat_template(
                    [{"role": "user", "content": user_prompt(p)}],
                    add_generation_prompt=True,
                    tokenize=False,
                )
                for p in chunk
            ]
            inputs = tokenizer(prompts, return_tensors="pt", padding=True).to(model.device)
            with torch.no_grad():
                out = model.generate(
                    **inputs,
                    max_new_tokens=self.max_tokens,
                    do_sample=True,
                    temperature=self.temp,
                    num_return_sequences=k,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
            prompt_len = inputs["input_ids"].shape[1]
            decoded = [
                tokenizer.decode(row[prompt_len:], skip_special_tokens=True) for row in out
            ]
            # generate() with batch>1 and num_return_sequences=k repeats each
            # input k times contiguously (repeat_interleave on the batch dim),
            # so decoded[i*k:(i+1)*k] are chunk[i]'s k samples, in chunk order.
            for i in range(len(chunk)):
                results.append(decoded[i * k : (i + 1) * k])
        return results

    def _ensure(self):
        if self._model is None or self._tokenizer is None:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer

            self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            # left padding is required for batched decoder-only generation:
            # right padding would leave the new tokens misaligned across rows.
            self._tokenizer.padding_side = "left"

            # T4 (Turing) has no bf16 tensor cores; "auto" picks the
            # checkpoint's dtype, which for Qwen2.5 is bf16 and runs on T4 via
            # a slow fp32 emulation path. fp16 is the fast path on this GPU.
            dtype = torch.float16 if torch.cuda.is_available() else "auto"
            model = AutoModelForCausalLM.from_pretrained(
                self.model_id, torch_dtype=dtype, device_map="auto"
            )
            if self.adapter_path:
                from peft import PeftModel

                model = PeftModel.from_pretrained(model, self.adapter_path)
            self._model = model
        return self._model, self._tokenizer
