RL with veriﬁable rewards at small scale. RLVR with GRPO reports large gains
near our model size: one training example lifts Qwen2.5-Math-1.5B on MATH-
500 from 36.0% to 73.6% [14], about 7,000 examples lift DeepSeek-R1-Distill-
Qwen-1.5B on AMC23 from 63% to 80% [3], and zero-RL works across ten open
base models including Qwen2.5 from 0.5B [20]. These studies improve accuracy,
which our SFT loop does not; Wang et al. separate out format correction and
report only 8.6 of their 37.6 points as lying beyond it, but the studies mostly do
not ask what the rest consists of. Shao et al. [9] show that it need not be reward
learning: random rewards raise Qwen2.5-Math-7B by 21.4 points on MATH-
500, which they trace to ampliﬁed pre-existing behaviour, and the eﬀect varies
by model family. We do not compete with RLVR on accuracy; the audit of
Section 5.3 asks of a loop whether the model has adapted to one veriﬁer defect,
and we apply it only to SFT.

Veriﬁer error. TinyV [16] ﬁnds that rule-based veriﬁers reject many correct
solutions; From Accuracy to Robustness [6] reports an average recall of 86%,
and 0.95 for math-verify on their MATH subset. Imperfect Veriﬁers [1] models
ﬁxed false-accept and false-reject rates. Egashira et al. [4] ﬁnd in RLVR that
systematic false negatives behave like random noise whereas false positives can
cause plateau or collapse. They also track the false-negative rate on the policy’s
4      T. S. Nguyen and D. A. Tran

own rollouts per training step and observe that the policy ﬁrst unlearns the
behaviour that triggers false negatives; TinyV likewise tracks the share of false
negatives across GRPO steps. Our setting diﬀers in paradigm (oﬄine SFT with
a fresh adapter per round) and task, and our controls cannot test their ﬁndings
(Section 4.3).

Auditing self-improvement. Xu et al. [15] audit LoRA self-training of Qwen3-
8B against a frozen control and identify seven measurement failures, including
training-seed variance and a ﬁxed token cap under style drift, that each invert
a ﬁnding when uncontrolled. This is the study closest to ours; it is why we
separate ﬁnished accuracy from termination (Section 4.5). We diﬀer in scale (a
1.5B model), in the veriﬁer (a rule-based one whose rejection defect we mea-
sured) and in auditing what that veriﬁer’s ﬁltering does to the training pool,
not only whether accuracy moved. Kim et al. [7] show that self-distillation on
ground-truth solutions can cut accuracy while shortening responses; our train-
on-gold control shows a similar surface signature. We found no multi-round study
combining a measured format-biased rule-based veriﬁer with a patched-veriﬁer
control, but since our patch proved too weak (Section 4.3) we do not claim
this combination as the contribution. The per-round false-reject measurement
of Section 5.3 is not new either: it is the per-step tracking of Egashira et al.
and TinyV, applied here to oﬄine SFT self-training and to a defect of our own
pipeline. Supplementary Appendix ?? gives the full comparison.


3     Setup

3.1   The GVT Loop

Each round t has four steps. Generate: the current model samples k solutions per
problem. Verify: math-verify extracts the ﬁnal answer and compares it with the
gold. Select: accepted solutions are kept. Train: a fresh LoRA adapter is attached
to the base model and trained on the kept solutions for one epoch. Round 0 is
the untrained base model; the round-t model (t ≥ 1) is the base plus an adapter
trained on the pool accepted at round t − 1. Adapters are not accumulated, so
earlier rounds aﬀect later ones only through the data they generate; conclusions
about (non-)compounding below apply to this restart-from-base design, which
gives compounding less room than continued training would.


3.2   The Veriﬁer and Its Directional Bias

A format probe that re-renders gold answers in individually valid forms shows
that \dfrac/\tfrac are rejected 100% of the time on both datasets (the com-
mand is not parsed). On real solutions (one public Qwen2.5-7B-Instruct solution
per problem for 200 MATH-500 problems, judged correct by a scripted nor-
malised comparison) the false-negative rate is 7.8% (10 of 128; Wilson interval
4.3–13.8%) on MATH-500 and 0% on GSM8K. Eight of the ten fail when the
                                              Mathematics or the Veriﬁer?       5

whole solution is veriﬁed but pass when only the boxed answer is; most are com-
pound answers, so they are probably largely the gold-storage defect described
below rather than extraction of a wrong token. The audit inspected only rejec-
tions, so it gives no false-positive rate. The veriﬁer also cannot parse 51 of the
500 stored MATH-500 golds (10.2%); these problems always count as unsolved.
That is a constant oﬀset in counts within a partition, so it cancels in within-run
and same-partition diﬀerences, but not in ratios or in levels compared across
partitions (11–18 such problems per exam partition).
    The patch. For the control we rewrote \dfrac and \tfrac to \frac before
parsing, removing the 100%-rejection class and nothing else.
    The gold-storage defect (post hoc). Our pipeline stores the gold without a de-
limiter, and math-verify applies its full LATEX extraction only inside \boxed{}
or $...$, so a correct boxed prediction can fail against a bare gold (e.g. the
prediction \boxed{\frac{4}{3}} against the stored gold \frac43). Re-scoring
the saved generations with a veriﬁer V ′ that wraps the gold in \boxed{} when
the prediction contains one shows that this defect rejects 15.5–18.3% of the gen-
erations V ′ accepts. It would enlarge the round-0 kept pool by about a ﬁfth
to a quarter (440 → 542, +23%), against 0–4 examples for the \dfrac patch,
and it lowers absolute pass@1 by 4.7–8.0 points in self-training. It is bound to
the problem, not to the answer: on the 54–62 problems where it ever ﬁres, it
rejects 94–98% of correct answers in every round, and 29–34 of these problems
have a gold the original veriﬁer cannot parse at all, so no answer form avoids
it there. Re-scored, sample accuracy still falls in all ﬁve runs we re-scored; the
original-veriﬁer changes are 0.73–0.85 of the re-scored ones, an observed ratio
that we do not use to rescale other numbers or intervals. All tables keep the
original veriﬁer, the one the loop trained with. Section 5.3 uses this defect for
the adaptation audit; Supplementary Appendix ?? gives the full analysis.

3.3   Two Experimental Designs
Design P (pooled) loads both datasets (500 problems each) together and trains
one adapter per round on the union of accepted solutions, with selection and
evaluation on the same 1,000 problems. Design I (isolated) uses one dataset and
one adapter per run, and holds out 30% of the 500 problems (150) as an exam
set; generation runs on all 500 problems each round, but only the other 350 can
enter the training pool, and all Design I pass rates are on the exam set. Table ??
summarises them.
    Design I has three runs, all Qwen2.5-1.5B-Instruct, ﬁve rounds, k = 8, diﬀer-
ing in one respect each: Run A (MATH-500, original veriﬁer), Run B (MATH-
500, patched veriﬁer) and Run C (GSM8K, original veriﬁer). Runs A and B were
repeated at a second seed; since the seed also sets the train/exam partition, the
repetition draws a diﬀerent 150-problem exam set. Most of the later evidence
comes from higher-rate runs introduced in Section 4.4; Table ?? (Supplementary
Appendix ??) lists every run. A “seed” sets the exam partition, the selection set
and the training randomness at once; runs with the same seed share the par-
tition. “Five rounds” means round 0 (the untrained model) and four adapters,
6      T. S. Nguyen and D. A. Tran

each trained once on the previous round’s pool; “three rounds” means round 0
and two adapters, so the round-2 model is a single adapter (about 195 optimizer
steps for Run A at 5 × 10−4 ) trained on the round-1 pool. All runs use one model
family, Qwen2.5.