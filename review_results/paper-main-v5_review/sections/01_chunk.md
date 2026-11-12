Mathematics or the Veriﬁer?
3
the design could detect. No arm improves, not even training on reference
solutions, so this is a null for the recipe, not a statement about self-training.
– A post hoc per-round false-reject audit of one veriﬁer defect (the RLVR
tracking [4,17] applied to oﬄine SFT; not a novel method). The rejected
share falls by 1.5–2.6 points with intervals reaching zero, tied to the falling
\boxed share by an identity; the audit is uninformative about adaptation,
and the two injected-bias runs are not valid positive controls (Section 5.3).
– A decomposition of an accuracy decline under a ﬁxed token cap into a
ﬁnished-accuracy part and a cap-share part: at the highest rate, ﬁnished
generations lose 5.5–10.6 points against the untrained model on the same
problem mix, and the cap-hit share rises only at that rate.
2
Related Work
Self-training and its limits. STaR [20] introduced the generate–ﬁlter–retrain
loop, and ReST [13], ReST-EM [12] and RFT [18] formalise it; ReST-EM, which
like us restarts from the base model each iteration, reports diminishing gains
after the ﬁrst round. Yue et al. [19] show that RL raises pass@1 while the base
model wins at large pass@k, and Teacher-Free Self-Training [14] concludes that
self-training “ampliﬁes but does not compound”. Training repeatedly on model-
generated data erodes distribution tails [11], and a narrow selector can accelerate
collapse [9].
RL with veriﬁable rewards at small scale. RLVR with GRPO reports large gains
near our model size: one training example lifts Qwen2.5-Math-1.5B on MATH-
500 from 36.0% to 73.6% [15], 7,000 examples lift DeepSeek-R1-Distill-Qwen-
1.5B on AMC23 from 63% to 80% [3], and zero-RL works on open base models
from 0.5B [21]. These studies improve accuracy, which our SFT loop does not;
of Wang et al.’s 37.6 points only 8.6 lie beyond format correction. Shao et al. [10]
show that it need not be reward learning (random rewards also help, via ampliﬁed
pre-existing behaviour). We do not compete with RLVR on accuracy; the audit
of Section 5.3 asks whether a loop has adapted to one veriﬁer defect, and we
apply it only to SFT.
Veriﬁer error. TinyV [17] ﬁnds that rule-based veriﬁers reject many correct
solutions; From Accuracy to Robustness [6] reports an average recall of 86%,
and 0.95 for math-verify on their MATH subset. Imperfect Veriﬁers [1] models
ﬁxed false-accept and false-reject rates. Egashira et al. [4] ﬁnd in RLVR that
systematic false negatives behave like random noise whereas false positives can
cause plateau or collapse. For format-based false negatives they see the policy
ﬁrst unlearn the triggering behaviour. Our setting diﬀers in paradigm (oﬄine
SFT with a fresh adapter per round) and task, and our controls cannot test
their ﬁndings (Section 4.3).

4
T. S. Nguyen and D. A. Tran
Auditing self-improvement. Xu et al. [16] audit LoRA self-training of Qwen3-
8B against a frozen control and identify seven measurement failures, including
training-seed variance and a ﬁxed token cap under style drift, that each invert
a ﬁnding when uncontrolled. This is the study closest to ours; it is why we
separate ﬁnished accuracy from termination (Section 4.5). We diﬀer in scale (a
1.5B model), in the veriﬁer (a rule-based one whose rejection defect we measured)
and in auditing what that veriﬁer’s ﬁltering does to the training pool, not only
whether accuracy moved. Kim et al. [8] show that self-distillation with a teacher
that sees the solution can cut accuracy, as our train-on-gold control does. Our
per-round false-reject measurement (Section 5.3) is not new (it is the per-step
tracking of Egashira et al. and TinyV, applied to oﬄine SFT and to a defect of
our own pipeline), and we claim neither it nor the patch control as a contribution.
The PRM800K grader [7] normalises \dfrac and \frac43 and could serve as
a second grader of the saved generations; we did not run it. Supplementary
Appendix A gives the full comparison.
3
Setup
3.1
The GVT Loop
Each round t has four steps. Generate: the current model samples k solutions per
problem. Verify: math-verify extracts the ﬁnal answer and compares it with the
gold. Select: accepted solutions are kept. Train: a fresh LoRA adapter is attached
to the base model and trained on the kept solutions for one epoch. Round 0 is
the untrained base model; the round-t model (t ≥1) is the base plus an adapter
trained on the pool accepted at round t −1. Adapters are not accumulated, so
earlier rounds aﬀect later ones only through the data they generate; conclusions
about (non-)compounding below apply to this restart-from-base design, which
gives compounding less room than continued training would.
3.2
The Veriﬁer and Its Directional Bias
A format probe that re-renders gold answers in individually valid forms shows
that \dfrac/\tfrac are rejected 100% of the time on both datasets (the com-
mand is not parsed). On real solutions (one public Qwen2.5-7B-Instruct solution
per problem for 200 MATH-500 problems, judged correct by a scripted nor-
malised comparison) the false-negative rate is 7.8% (10 of 128; Wilson interval
4.3–13.8%) on MATH-500 and 0% on GSM8K. Eight of the ten fail when the
whole solution is veriﬁed but pass when only the boxed answer is; most are com-
pound answers, so they are probably largely the gold-storage defect described
below rather than extraction of a wrong token. The audit inspected only rejec-
tions, so it gives no false-positive rate. The veriﬁer also cannot parse 51 of the
500 stored MATH-500 golds (10.2%); these problems always count as unsolved,
and can never enter the training pool. The oﬀset cancels in within-run diﬀerences
only if those problems would not otherwise change, which we did not check, and
not in ratios or levels across partitions (11–18 such problems per exam partition).