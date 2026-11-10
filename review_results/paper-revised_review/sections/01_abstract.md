## Abstract
Abstract. Self-training and reinforcement learning with verifiable re-
wards report large gains for small language models, but a rising score
does not show that a model learned mathematics rather than what its
verifier accepts; RL with random rewards has been shown to raise ac-
curacy too. We propose a test that separates the two without assum-
ing accuracy rises: per checkpoint, the share of the model’s own correct
solutions that a known verifier defect rejects, which should fall if the
model adapts to the verifier. It needs no retraining, so it applies to RL
checkpoints as well. We apply it, post hoc, to generate–verify–select–
train self-training of Qwen2.5-1.5B-Instruct with LoRA SFT and the
rule-based verifier math-verify. A storage defect makes the verifier re-
ject 15.5–18.4% of correct solutions, and that share does not fall over
rounds: the model does not adapt to this defect. Nor does it improve.
On a held-out exam of 150 problems, at four learning rates on MATH-
500 and two on GSM8K, no pass@1 or pass@k gain has a problem-level
bootstrap interval excluding zero, and sample-accuracy intervals exclude
gains above 2.2 points, a loose bound that omits training-seed variance.
At the highest rate accuracy falls in every run, and finished solutions be-
come 5–11 points less accurate. Our pre-set rule for verifier-style learning
could fire only if accuracy rose, which motivates the new test. Controls
that patch a rarer defect or remove the filter are underpowered and show
no consistent difference.
Keywords: self-training · self-improvement · verifier bias · mathe-
matical reasoning · small language models · verifiable rewards · neg-
ative result.