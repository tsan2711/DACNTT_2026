## 2 Related Work
Self-training and its limits. STaR [19] introduced the generate–filter–retrain
loop, and ReST [12], ReST-EM [11] and RFT [17] formalise it; ReST-EM, which
like us restarts from the base model each iteration, reports diminishing gains af-
ter the first round. None measures how the filter’s errors depend on the form of
the answer. Yue et al. [18] show that RL raises pass@1 while the base model wins
at large pass@k, and Teacher-Free Self-Training [13] concludes that self-training
“amplifies but does not compound”. Training repeatedly on model-generated
data erodes distribution tails [10], and a narrow selector can accelerate col-
lapse [8].
RL with verifiable rewards at small scale. RLVR with GRPO reports large gains
near our model size: one training example lifts Qwen2.5-Math-1.5B on MATH-
500 from 36.0% to 73.6% [14], about 7,000 examples lift DeepSeek-R1-Distill-
Qwen-1.5B on AMC23 from 63% to 80% [3], and zero-RL works across ten open
base models including Qwen2.5 from 0.5B [20]. These studies improve accuracy,
which our SFT loop does not, but they do not ask what the gain consists of.
Shao et al. [9] show that it need not be reward learning: random rewards raise
Qwen2.5-Math-7B by 21.4 points on MATH-500, which they trace to amplified
pre-existing behaviour, and the effect varies by model family. We do not compete
with RLVR on accuracy; the test we propose (Section 5.3) is meant to ask of
such gains whether the model has adapted to its verifier, and we apply it only
to SFT.

4
T. S. Nguyen and D. A. Tran
Verifier error. TinyV [16] finds that rule-based verifiers reject many correct
solutions; From Accuracy to Robustness [6] reports an average recall of 86%,
and 0.95 for math-verify on their MATH subset. Imperfect Verifiers [1] models
fixed false-accept and false-reject rates. Egashira et al. [4] find in RLVR that
systematic false negatives behave like random noise whereas false positives can
cause plateau or collapse. Our setting differs in paradigm (oﬄine SFT with a
fresh adapter per round) and task, and our controls cannot test their findings
(Section 4.3).
Auditing self-improvement. Xu et al. [15] audit LoRA self-training of Qwen3-
8B against a frozen control and identify seven measurement failures, including
training-seed variance and a fixed token cap under style drift, that each invert
a finding when uncontrolled. This is the study closest to ours; it is why we
separate finished accuracy from termination (Section 4.5). Kim et al. [7] show
that self-distillation on ground-truth solutions can cut accuracy while shortening
responses; our train-on-gold control shows a similar surface signature. We found
no multi-round study combining a measured format-biased rule-based verifier
with a patched-verifier control, but since our patch proved too weak (Section 4.3)
we do not claim this combination as the contribution. Nor did we find, in the
studies above, a per-round measurement of the verifier’s false-reject rate on the
loop’s own outputs, which is the test we propose in Section 5.3. Appendix A
gives the full comparison.