

– A post hoc per-round false-reject audit of one veriﬁer defect (the RLVR
tracking [4,16] applied to oﬄine SFT; not a novel method). The rejected
share falls by 1.5–2.6 points with intervals reaching zero, tied to the falling
\boxed share by an identity; the audit is uninformative about adaptation
(Section 5.3).
– A decomposition of an accuracy decline under a ﬁxed token cap into a
ﬁnished-accuracy part and a cap-share part: at the highest rate, ﬁnished
generations lose 5.5–10.6 points against the untrained model on the same
problem mix (A, B and no-ﬁlter runs; train-on-gold about 26).

2

Related Work

Self-training and its limits. STaR [19] introduced the generate–ﬁlter–retrain
loop, and ReST [12], ReST-EM [11] and RFT [17] formalise it; ReST-EM, which
like us restarts from the base model, reports diminishing gains after the ﬁrst
round. Yue et al. [18] show that RL raises pass@1 while the base model wins at
large pass@k; Teacher-Free Self-Training [13] concludes that self-training “ampliﬁes but does not compound”. Repeated training on model-generated data erodes
distribution tails [10], and a narrow selector can accelerate this [8].
RL with veriﬁable rewards at small scale. RLVR with GRPO reports large gains
near our model size: one training example lifts Qwen2.5-Math-1.5B on MATH500 from 36.0% to 73.6% [14], 7,000 examples lift DeepSeek-R1-Distill-Qwen1.5B on AMC23 from 63% to 80% [3], and zero-RL works on open base models
from 0.5B [20]. These studies improve accuracy, which our SFT loop does not,
though of Wang et al.’s 37.6 points only 8.6 lie beyond format correction, and
random rewards also help [9]. We do not compete with RLVR on accuracy.
Veriﬁer error. TinyV [16] ﬁnds that rule-based veriﬁers reject many correct
solutions; From Accuracy to Robustness [6] reports an average recall of 86%,
and 0.95 for math-verify on their MATH subset. Imperfect Veriﬁers [1] models
ﬁxed false-accept and false-reject rates. Egashira et al. [4] ﬁnd in RLVR that
systematic false negatives behave like random noise whereas false positives can
cause plateau or collapse, and that the policy ﬁrst unlearns format-triggering
behaviour. Our setting is oﬄine SFT with a fresh adapter per round, and our
controls cannot test their ﬁndings (Section 4.3).
Auditing self-improvement. Xu et al. [15] audit LoRA self-training of Qwen38B against a frozen control and identify seven measurement failures, including training-seed variance and a ﬁxed token cap under style drift. This is the
study closest to ours; it is why we separate ﬁnished accuracy from termination
(Section 4.5). We diﬀer in (i) model and recipe (Qwen2.5-1.5B-Instruct, rank16 LoRA, learning rate varied over 10−5 –5 × 10−4 , against Qwen3-8B at rank
32); (ii) evaluation (150 or 500 MATH-500 problems at k ≤ 8, against 200 at
k = 128); and (iii) the control (they distil from gpt-oss-120b; our positive control

4

D.-H. Vu et al.

is reference solutions, Section 4.6). Both grade with Math-Verify; we also patch
it and measure its false rejections. Kim et al. [7] show that self-distillation with a
teacher that sees the solution can cut accuracy; our train-on-gold drop resembles
this, but we did not test its cause. Our per-round false-reject measurement is not
new (it is the per-step tracking of Egashira et al. and TinyV, applied to oﬄine
SFT and to a defect of our own pipeline); we claim neither it nor the patch control as a contribution. The Supplementary (a separate ﬁle; supplementary.tex
in the repository) gives the full comparison in Appendix A.

3

Setup

3.1

The GVT Loop

Each round t has four steps. Generate: the current model samples k solutions per
problem. Verify: math-verify extracts the ﬁnal answer and compares it with the
gold. Select: accepted solutions are kept. Train: a fresh LoRA adapter is attached
to the base model and trained on the kept solutions for one epoch. Round 0 is
the untrained base model; the round-t model (t ≥ 1) is the base plus an adapter
trained on the pool accepted at round t − 1. Adapters are not accumulated, so
earlier rounds aﬀect later ones only through the data they generate; this restartfrom-base design gives compounding less room than continued training would.
3.2

The Veriﬁer and Its Directional Bias

A format probe that re-renders gold answers in valid forms shows that \dfrac
and \tfrac are always rejected, on both datasets. On real solutions (one public Qwen2.5-7B-Instruct solution for each of 200 MATH-500 problems, judged
correct by a normalised comparison) the false-negative rate is 7.8% (10 of 128;
Wilson interval 4.3–13.8%) on MATH-500 and 0% on GSM8K. Eight of the ten
fail when the whole solution is veriﬁed but pass when only the boxed answer is,
probably the gold-storage defect described below. The audit inspected only rejections, so it gives no false-positive rate. The veriﬁer also cannot parse 51 of the
500 stored MATH-500 golds (10.2%); under V these always count as unsolved
and never enter the training pool (V ′ makes 46 parseable for boxed predictions).
This cancels in within-run diﬀerences only if they would not otherwise change
(unchecked; 11–18 per exam partition).
The patch. For the control we rewrote \dfrac and \tfrac to \frac before
parsing, and nothing else.
The gold-storage defect (post hoc). Our pipeline stores the gold without a delimiter, and math-verify applies its full LATEX extraction only inside \boxed{}
or $...$, so a correct boxed prediction can fail against a bare gold (e.g. the
prediction \boxed{\frac{4}{3}} against the stored gold \frac43). Re-scoring
the saved generations with a veriﬁer V ′ that wraps the gold in \boxed{} when
the prediction contains one shows that this defect rejects 15.5–18.3% of the generations V ′ accepts. It would enlarge the round-0 kept pool by about a ﬁfth

Mathematics or the Veriﬁer?

5