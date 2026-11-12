Mathematics or the Veriﬁer? A Null Result for
One Veriﬁer-Filtered Self-Training Recipe on a
1.5B Model
Tan Sang Nguyen1 and Duy Anh Tran1
Ton Duc Thang University, Ho Chi Minh City, Vietnam
52300057@student.tdtu.edu.vn, 52300006@student.tdtu.edu.vn
Abstract. Self-training and reinforcement learning with veriﬁable re-
wards report large gains for small language models, but a rising score
does not show that a model learned mathematics rather than what its
veriﬁer accepts. We study the cheapest form of the loop, generate–verify–
select–train with oﬄine LoRA SFT, on Qwen2.5-1.5B-Instruct with the
rule-based veriﬁer math-verify, on held-out MATH-500 and GSM8K ex-
ams (150 problems; 500 in a ﬁnal round) at four learning rates on MATH-
500 and two on GSM8K. No pass@1 or pass@k gain has a problem-level
bootstrap interval excluding zero; in the ﬁnal round, with a revised (not
validated) recipe, pass@1 falls 3.2–4.8 points in each of three seeds (mean
−4.1; two of three intervals exclude zero). The design detects only gains
of about 10 points of pass@1 (6 in the ﬁnal round; 80% power, intervals
without seed variance, so likely more). A positive gate fails: training on
reference solutions lowers pass@1 by 32.2 points, which points to a de-
fect in the pipeline, so the null concerns this recipe only and cannot show
that self-training fails. All accuracies are graded by the same veriﬁer that
selects the data, so neither the mathematics nor the veriﬁer question is
answered. As a post hoc audit we track the share of the loop’s own cor-
rect solutions that a storage defect in our pipeline rejects (about one
in six). It falls by 1.5–2.6 points with intervals reaching zero; this fall
is tied to the falling \boxed share by an identity, so it is no evidence
of adaptation. Two injected-bias runs, one learnable from the problem,
show no selective avoidance but are not valid positive controls (one can-
not elicit avoidance by construction, the other is a single run without rt),
so the audit is uninformative about adaptation. Two controls, patching
a rarer defect and removing the ﬁlter, show no consistent diﬀerence but
are dose-confounded or too small to detect one. Scores before the ﬁnal
round use the veriﬁer with the defect.
Keywords: self-training · self-improvement · veriﬁer bias · mathe-
matical reasoning · small language models · veriﬁable rewards · null
result.
1
Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its

2
T. S. Nguyen and D. A. Tran
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on
them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [20], ReST [13], ReST-EM [12] and rejection-sampling ﬁne-
tuning [18]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such
as math-verify1 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR), which reports large gains at this scale [15,3,21], though only 8.6 of
one study’s 37.6 points lie beyond format correction. Shao et al. [10] ﬁnd that
GRPO with random rewards raises Qwen2.5-Math-7B by 21.4 points on MATH-
500, against 29.1 with ground-truth rewards. A rising score therefore does not
by itself show that a model has learned to solve more problems, rather than to
surface behaviour it already had or to produce what its reward accepts. In RLVR,
per-step false-negative rates on the policy’s own rollouts have been tracked [4,17];
we study the question in a cheap and common form of the loop, oﬄine rejection-
sampling SFT, where a false reject only removes a training example, and apply a
per-round false-reject measurement there, post hoc, for one defect of our pipeline.
We ask: after several GVT rounds, is the model better at mathematics, or
has it only learned to write what the veriﬁer accepts? We ﬁxed four measures
in advance: (i) pass@1; (ii) pass@k; (iii) output style, chieﬂy the share of gen-
erations containing \boxed; and (iv) per-problem transitions (problems added
and lost between rounds). The pre-set reading rule was that “learning the ver-
iﬁer’s style” requires pass@1 to rise, pass@k to stay ﬂat and style to converge
at once. In hindsight the rule is one-sided: it can only ﬁre when accuracy rises
(Section 5.1). The higher learning rates, the controls, the round count and k
at those rates, sample accuracy as primary measure, the termination measures
and the re-scoring for a second veriﬁer defect, and the ﬁnal 500-problem round
(Section 4.6) were all added after seeing earlier runs; all are post hoc.
We detect no improvement at any learning rate, though gains below about 10
points of pass@1 or 3.5–5.5 of sample accuracy could have been missed (intervals
omit training-seed variance), and no arm of this recipe improves, so the result
concerns the recipe. The second branch is untested: no run varies the frequent
veriﬁer defect, every score is graded by the selecting veriﬁer, and the post hoc
audit of Section 5.3 is uninformative about adaptation. What appears, most
clearly at the highest rate, is lower accuracy on the solutions the model does
ﬁnish. A sharp pooled decline does not reproduce under isolation (Section 4.1),
where dose and pooling are confounded.
Contributions.
– For a 1.5B model, LoRA SFT and one rule-based veriﬁer, no gain is de-
tectable on a held-out exam at any learning rate we tried (a coarse grid that
also changes k and rounds), with bootstrap intervals and the smallest eﬀects
1 https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
work.

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

Mathematics or the Veriﬁer?
5
The patch. For the control we rewrote \dfrac and \tfrac to \frac before
parsing, removing the 100%-rejection class and nothing else.
The gold-storage defect (post hoc). Our pipeline stores the gold without a de-
limiter, and math-verify applies its full LATEX extraction only inside \boxed{}
or $...$, so a correct boxed prediction can fail against a bare gold (e.g. the
prediction \boxed{\frac{4}{3}} against the stored gold \frac43). Re-scoring
the saved generations with a veriﬁer V ′ that wraps the gold in \boxed{} when
the prediction contains one shows that this defect rejects 15.5–18.3% of the gen-
erations V ′ accepts. It would enlarge the round-0 kept pool by about a ﬁfth to
a quarter (440 →542, +23%), against 0–4 examples for the \dfrac patch, and
it lowers absolute pass@1 by 4.7–8.0 points in self-training. It is bound to the
problem, not to the answer: on the 54–62 problems where it ever ﬁres, it rejects
94–98% of correct answers in every round (87–98% where V parses the gold),
and 29–34 of these problems have a gold the original veriﬁer cannot parse at all,
so no answer form avoids it there. Re-scored, sample accuracy still falls in all
ﬁve runs we re-scored; the original-veriﬁer changes are 0.73–0.85 of the re-scored
ones, an observed ratio that we do not use to rescale other numbers or intervals.
All tables keep the original veriﬁer, the one the loop trained with. Section 5.3
uses this defect for the adaptation audit; Supplementary Appendix B gives the
full analysis.
3.3
Two Experimental Designs
Design P (pooled) loads both datasets (500 problems each) together and trains
one adapter per round on the union of accepted solutions, with selection and
evaluation on the same 1,000 problems. Design I (isolated) uses one dataset and
one adapter per run, and holds out 30% of the 500 problems (150) as an exam
set; generation runs on all 500 problems each round, but only the other 350 can
enter the training pool, and all Design I pass rates are on the exam set. Table S1
summarises them.
Design I has three runs, all Qwen2.5-1.5B-Instruct, ﬁve rounds, k = 8, diﬀer-
ing in one respect each: Run A (MATH-500, original veriﬁer), Run B (MATH-
500, patched veriﬁer) and Run C (GSM8K, original veriﬁer). Runs A and B were
repeated at a second seed; since the seed also sets the train/exam partition, the
repetition draws a diﬀerent 150-problem exam set. Most of the later evidence
comes from higher-rate runs introduced in Section 4.4; Table S4 (Supplementary
Appendix E) lists every run. A “seed” sets the exam partition, the selection set
and the training randomness at once; runs with the same seed share the par-
tition. “Five rounds” means round 0 (the untrained model) and four adapters,
each trained once on the previous round’s pool; “three rounds” means round 0
and two adapters, so the round-2 model is a single adapter (about 195 optimizer
steps for Run A at 5×10−4) trained on the round-1 pool. All runs use one model
family, Qwen2.5.

6
T. S. Nguyen and D. A. Tran
3.4
Models, Data, Training, Metrics
We use Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct (Design P uses both,
Design I the 1.5B model only) and the ﬁrst 500 problems of the GSM8K test
split [2] and MATH-500, the 500-problem subset of MATH [5]. The prompt is
a single user turn in the model’s chat template: “Solve the math problem. Put
the ﬁnal answer in \boxed{}.” followed by the problem. Generation samples at
temperature 0.8 with a cap of 512 new tokens; the other decoding settings come
from the checkpoint’s generation conﬁguration (top-p 0.8, top-k 20, repetition
penalty 1.1). Training is LoRA SFT (transformers 5.0.0, peft 0.19.1, TRL
1.10.0 SFTTrainer; rank 16, α = 32, on q_proj and v_proj, LoRA dropout
0, weight decay 0, gradient clipping 1.0 and trainer seed 42, all library defaults
read from the pinned sources; batch size 2, no accumulation; one epoch; AdamW
with linear learning-rate decay and no warmup; Python and torch seeds set
from the run seed; loss over the whole chat sequence, prompt included; fp16 on
one Kaggle T4), with a training sequence limit of 512 tokens that includes the
prompt. Because this limit equals the generation cap but also holds the prompt,
any kept solution longer than about 512 tokens minus the prompt length is cut
in training and loses its ﬁnal answer and end-of-sequence token (24–26% of the
round-0 pool; Section 4.5). All kept solutions are used, so the number of optimizer
steps per round is half the pool size. The learning rate is 10−5 unless stated
otherwise; this value was the default of our training code and was not tuned
(Section 4.4). Metrics per round, on the exam set: pass@1 is the correctness
of the ﬁrst of the k samples (one draw per problem, so it carries sampling
noise); pass@k; sample accuracy, the mean over all k samples; style counts over
all generations (boxed, dfrac, dollar, . . . ); and per-problem added/lost counts
between consecutive rounds, where a problem is solved in a round if at least one
of its k samples is accepted. Added minus lost therefore equals 150×∆pass@k, so
these counts add only the gross churn behind the net change, not an independent
test. pass@1 was ﬁxed in advance; sample accuracy was not among the pre-
set measures, but it estimates the same quantity from all k samples with less
variance, so after the runs we chose it as the primary accuracy measure. Claims
that rest on it, including the 2.2-point bound, are therefore post hoc in the choice
of measure. “Correct” always means accepted by the veriﬁer (preset reward), the
same veriﬁer that selects the training data.
Uncertainty. For every within-run change (round 0 against the last round) and
every paired comparison of two runs on the same exam partition we report a
95% interval from a paired problem-level bootstrap (10,000 resamples of the
150 exam problems; 2,000 for the matched and audit columns), which respects
the clustering of the k samples within a problem. These intervals do not cover
training-seed variance, which we see only across two or three seeds: the one same-
conﬁguration replicate pair we have ends 3.2 points of sample accuracy apart.
We make no multiplicity correction and the runs are not independent (they share
exam partitions and round-0 draws), so patterns across runs are descriptive, not
tests; we apply the same reading to declines and to gains. Single proportions use

Mathematics or the Veriﬁer?
7
Wilson intervals. Detectable eﬀects. From the interval half-widths h in Table 2,
a change would be detected with 80% power at the 5% level only if it exceeded
about 2.8 h/1.96: about 10 points of pass@1, 8–10 of pass@k and 3.5–5.5 of
sample accuracy on MATH-500. Because h omits training-seed variance (the
replicate pair diﬀers by 3.2 points and B minus A ﬂips from +5.3 to −7.3 on
near-identical pools, Section 4.4), these are lower bounds: a null here means no
gain of at least that size, probably larger (Supplementary Appendix C).
4
Results
4.1
Design P: An Apparent Collapse
In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 50.0% →18.6%, pass@8 72.6% →48.6%; Table S3, Supplementary
Appendix D), on both datasets (Table S2); the 0.5B decline is small. The ac-
cepted pool contracts every round and \boxed{} falls from 5,608 to 2,693 of
8,000 generations. This design cannot be read causally: one adapter trains on
both datasets’ pools, it scores on the problems it selects from, and it trains on
about 4.5× as many examples per round as the isolated MATH-500 run (3,962
against 872 at round 0); no run separates these (Supplementary Appendix D).
4.2
Design I at 10−5: Small Declines, a Larger One on GSM8K
On the held-out exam (Fig. S1 and Table S5 in Supplementary Appendix E)
pass@8 ends within 4 points of round 0 in every run. On MATH-500, pass@1
is 2.7–4.0 points lower at round 4, with every interval including zero (Table 2);
sample accuracy falls 1.2–3.2 points, with an interval excluding zero only for B
at seed 0 (A at seed 0 reaches 0.0), and matched ﬁnished accuracy 1.1–4.2, with
intervals that only just exclude zero for A and B at seed 0, which are close to one
replicate. We read this as a possible small decline, not an established one; what
we do not see is a gain of the size the design could detect. Run C (GSM8K)
declines more: pass@1 falls 12.7 points ([−21.3, −4.0]), almost all in ﬁnished
accuracy, but it took about twice Run A’s optimizer steps, so we do not attribute
this to the dataset alone. Length and cap-hit share barely change on MATH-500,
weak evidence that the adapter did little (Supplementary Appendix E).
4.3
The Patch Control Could Not Detect an Eﬀect
Runs A and B diﬀer only in the \dfrac/\tfrac patch. At round 4, B minus A
is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and +0.0 [−2.7, +2.7] at seed 1
(recomputed from the saved generations; Table 2 lists run-log values that diﬀer
by one problem and give −0.7 at seed 1). This null is uninformative: \dfrac
appears in 0.50–0.73% of generations, so the kept pools diﬀer by 3–4 examples
(under 0.5% of the 872-example pool), and at 10−5 the adapter changes the
outputs little anyway, so a null is what prevalence alone predicts; the frequent
gold-storage defect is in both arms.

8
T. S. Nguyen and D. A. Tran
4.4
Higher Learning Rates
Because 10−5 changed the MATH-500 outputs little, we reran Run A at 10−4
(three seeds), 2×10−4 (two) and 5×10−4 (two, with Run B), with three rounds
and k = 4 (Table 1). These runs diﬀer from the 10−5 runs in k, rounds, pool
size and the pass@k metric as well as rate, so only 10−4 to 5 × 10−4 isolates
the rate. At 5 × 10−4 every run declines: pass@1 falls 4.0–11.3 points and the
sample-accuracy intervals exclude zero in all four A/B runs, though same-seed
A and B are closer to two replicates than four. The decline may grow with the
rate on one seed (sample-accuracy changes at 10−5 and 10−4 are similar, −1.2 to
−3.2 and −1.0 to −3.7): at seed 1 sample accuracy falls 1.5, 3.5 and 8.3 points
across the three rates, at seed 2 an almost ﬂat 3.7, 3.8 and 4.7. The cap-hit
share rises only at 5 × 10−4. The patch has no consistent eﬀect: B minus A in
round-2 pass@1 is +5.3 at seed 1 and −7.3 [−14.0, −0.7] at seed 2, a sign ﬂip
from pools diﬀering by 0–3 examples: trajectory noise. Style does not separate
imitation from drift: boxed share falls with the pool, which both would produce,
and the no-ﬁlter and gold arms decline with no veriﬁer at all, so generic SFT
damage ﬁts as well.
Table 1. Run A (MATH-500, original veriﬁer, k = 4, three rounds) across learning rates
and seeds: pass@1, pass@4 and sample accuracy (600 exam generations) at round 0
→round 2, the share of round-2 generations that hit the 512-token cap (decoded text
re-tokenised to ≥508 tokens; round 0 is 43.0–43.2%, 48.2% at seed 3), and problems
added/lost summed over rounds 1–2. The two 5×10−4 rows are the A rows of Table S6.
Rate
Seed
pass@1
pass@4
Sample acc. Cap-hit (R2) Added/lost
10−4
1
33.3 →34.0 50.0 →49.3 33.7 →32.2
42.7%
20/21
10−4
2
31.3 →28.0 51.3 →45.3 30.8 →27.2
42.8%
25/34
10−4
3
29.3 →26.7 40.0 →41.3 28.5 →27.5
45.7%
16/14
2 × 10−4 1
33.3 →31.3 50.0 →46.7 33.7 →30.2
40.8%
23/28
2 × 10−4 2
31.3 →25.3 51.3 →45.3 30.8 →27.0
39.7%
21/30
5 × 10−4 1
33.3 →23.3 50.0 →42.7 33.7 →25.3
46.2%
22/33
5 × 10−4 2
31.3 →27.3 51.3 →44.7 30.8 →26.2
51.2%
26/36
Two controls at 5 × 10−4. The no-ﬁlter run trains on all k samples of every
selection problem (1,400 examples per round), removing the veriﬁer; the train-
on-gold run trains on the 350 reference solutions every round (Table 3). Neither
is a single-variable control: no-ﬁlter takes 3–4× Run A’s optimizer steps, train-
on-gold about the same. Removing the ﬁlter is not better than keeping it beyond
noise and is lower on pass@4 at both seeds (round-2 diﬀerences −2.0 and −5.3
points, intervals including zero), but the dose diﬀerence means this cannot be
attributed to the ﬁlter; the no-ﬁlter pool is also truncated far more often in
training (62.4% against 24.5% at round 0). Training on reference solutions is
followed by a much larger decline (pass@4 down about 21 points at both seeds)

Mathematics or the Veriﬁer?
9
Table 2. Change from round 0 to the last round (percentage points) with 95%
paired problem-level bootstrap intervals over the 150 exam problems (10,000 resam-
ples; bootstrap_ci.py in the code repository). Last round is R4 at 10−5 (k = 8) and
R2 elsewhere (k = 4). “Finished, matched” is the last-round accuracy of generations
below the 512-token cap minus the untrained model’s accuracy on the same problem
mix (Section 4.5; 2,000 resamples, capanat.py in the repository). The intervals do not
include training-seed variance. Recomputed values match the reported ones except six
round values that diﬀer by one problem (Supplementary Appendix C), e.g. B, seed 1
at 10−5, whose round-4 pass@8 is 58.0% against 58.7%; the matched column uses the
separate re-scoring described there.
Run, seed
∆pass@1
∆pass@k
∆sample acc.
Finished, matched
Learning rate 10−5
A, 0
−2.7 [−9.3, 4.0]
−1.3 [−8.0, 5.3]
−2.4 [−4.8, 0.0]
−3.8 [−7.2, −0.5]
A, 1
−3.3 [−10.0, 3.3]
+0.0 [−6.0, 6.0]
−1.5 [−4.1, 1.0]
−2.3 [−5.9, 1.2]
B, 0
−3.3 [−10.0, 3.3]
−4.0 [−10.7, 2.7]
−3.2 [−5.9, −0.6]
−4.2 [−7.8, −0.9]
B, 1
−4.0 [−10.7, 2.7]
−1.3 [−7.3, 4.7]
−1.2 [−3.7, 1.3]
−1.1 [−4.6, 2.6]
C, 0
−12.7 [−21.3, −4.0]
−2.7 [−7.3, 2.0]
−13.1 [−16.7, −9.8]
−12.8 [−16.5, −9.4]
Learning rate 10−4
A, 1
+0.7 [−6.7, 8.0]
−0.7 [−6.0, 4.7]
−1.5 [−5.3, 2.2]
−4.3 [−9.6, 1.1]
A, 2
−3.3 [−9.3, 2.7]
−6.0 [−12.7, 0.7]
−3.7 [−7.3, −0.2]
−3.5 [−9.2, 2.3]
A, 3
−2.7 [−10.0, 4.0]
+1.3 [−4.7, 7.3]
−1.0 [−4.3, 2.2]
−0.6 [−6.0, 4.7]
Learning rate 2×10−4
A, 1
−2.0 [−8.0, 4.0]
−3.3 [−10.0, 2.7]
−3.5 [−7.2, 0.0]
−4.0 [−8.9, 0.5]
A, 2
−6.0 [−12.7, 0.7]
−6.0 [−12.7, 0.7]
−3.8 [−7.5, −0.2]
−4.7 [−10.1, 1.0]
Learning rate 5×10−4
A, 1
−10.0 [−16.7, −3.3]
−7.3 [−14.0, 0.0]
−8.3 [−12.3, −4.5]
−9.1 [−14.2, −4.2]
A, 2
−4.0 [−11.3, 3.3]
−6.7 [−13.3, 0.0]
−4.7 [−8.2, −1.2]
−5.5 [−11.7, 0.1]
B, 1
−4.7 [−12.0, 2.7]
−2.0 [−8.7, 4.7]
−6.7 [−10.5, −2.8]
−6.8 [−12.4, −1.0]
B, 2
−11.3 [−17.3, −5.3]
−11.3 [−18.0, −4.7]
−9.2 [−12.8, −5.5]
−5.9 [−10.9, −1.0]
No ﬁlter, 1
−6.0 [−12.7, 1.3]
−9.3 [−16.7, −2.7]
−8.2 [−12.2, −4.3]
−10.6 [−16.4, −5.5]
No ﬁlter, 2
−8.7 [−16.0, −1.3]
−12.0 [−19.3, −4.7]
−10.2 [−14.2, −6.3]
−6.6 [−11.4, −2.0]
Gold, 1
−18.0 [−26.7, −10.0] −20.7 [−28.7, −12.7] −19.7 [−25.3, −14.2] −25.6 [−32.1, −18.9]
Gold, 2
−21.3 [−28.7, −14.0] −20.7 [−29.3, −12.7] −18.7 [−23.7, −13.7] −25.9 [−31.7, −20.0]
C, 1
−22.0 [−29.3, −15.3]
−9.3 [−15.3, −3.3]
−15.3 [−19.8, −11.2] −12.1 [−16.6, −7.9]
while the model adopts the reference style ($-delimited spans 5% →98%). Post
hoc checks bound veriﬁer error from below only (about 2 points of sample accu-
racy among boxed answers), and the 14% of round-2 generations without \boxed
are not covered, so we think this fall is unlikely to be mainly veriﬁer error but
cannot bound it from above. That no arm, this one included, improves on the
untrained model means we have no positive reference: the nulls above may reﬂect
the recipe (LoRA on q/v projections, loss over the prompt, a 512-token limit)
rather than self-training. Run C at 5×10−4 (GSM8K, one run) falls 22.0 points of
pass@1, from both less accurate and more unﬁnished solutions (Supplementary
Appendix G).
4.5
Anatomy of the Decline
This subsection is post hoc and descriptive. Sample accuracy mixes whether a
ﬁnished solution is right with whether the model ﬁnishes within the 512-token
cap at all. Re-tokenising the saved text, we call a generation cap-hit at ≥508

10
T. S. Nguyen and D. A. Tran
Table 3. Controls at 5×10−4 (MATH-500, k = 4, three rounds), on the exam partition
of Run A at the same seed. Pool is the kept pool at round 0 →round 2; the round-
2 model trains on the round-1 pool (392 and 386 examples, about 195 steps) and
optimizer steps are half the pool size.
Run
Pool
pass@1
pass@4
R0
R1
R2
R0
R1
R2
Seed 1
A (veriﬁer-ﬁltered)
440→326
33.3
32.7
23.3
50.0
49.3
42.7
No ﬁlter
1400
33.3
26.7
27.3
50.0
49.3
40.7
Train on gold
350
33.3
18.0
15.3
50.0
33.3
29.3
Seed 2
A (veriﬁer-ﬁltered)
424→350
31.3
31.3
27.3
51.3
46.0
44.7
No ﬁlter
1400
31.3
34.7
22.7
51.3
48.7
39.3
Train on gold
350
31.3
8.7
10.0
51.3
28.7
30.7
tokens. At the rates where the share does not rise, 40–46% of round-2 MATH-500
generations already hit the cap (Table 1), so the cap binds from the start. At
5×10−4, compared with the untrained model on the same problem mix, ﬁnished
generations lose 5.5–10.6 points, with intervals excluding zero in ﬁve of six runs
(the six include two same-seed A/B pairs, which are close to replicates), while
the cap-hit share rises 2–14 points. The matched measure conditions on which
problems ﬁnish after training, so it is descriptive. A three-part decomposition
attributes 12–30% of the decline to the cap share in the three original seed-1
runs (and −2 and 5% in two further runs) and 52–72% at seed 2 (Table S9,
Supplementary Appendix H). At 10−4 and 2 × 10−4 the cap-hit share does not
rise and ﬁnished accuracy carries the whole change. Train-on-gold is diﬀerent:
responses shorten by more than half and ﬁnished accuracy collapses. Retraining
without truncated examples, or re-scoring at a 1,536-token cap, leaves the deﬁcit
in place (Supplementary Appendix H).
4.6
A Final Round with a Revised Recipe
Because no earlier arm improved, we ran one last round with seven recipe changes
made at once, aimed at the suspected causes (no ablation of any single one): loss
on the completion only, LoRA on all linear layers, a 1,024-token cap and training
limit, normalised gold answers, and a pool of 300 problems from the MATH
training split, so that the exam is all 500 MATH-500 problems. It is 10−4 with
k = 2 and a single adapter (round 0 to round 1); the loop has three seeds, the
gate one. We report no overlap check of the 300 pool problems against MATH-
500. The veriﬁer-ﬁltered loop (298 examples kept) is compared with training
on the 300 reference solutions, a positive gate that must raise accuracy for the
recipe to count as able to help.
The gate fails. Training on reference solutions lowers pass@1 from 49.2% to
17.0%, and the model adopts the reference style ($-delimited spans in 60 of 1,600

Mathematics or the Veriﬁer?
11
Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4). Change from
each run’s own untrained round 0 to round 1 in points (round-0 pass@1 is 49.2, 46.8,
48.2 at seeds 1–3, from sampling), with 95% paired problem-level bootstrap intervals
that omit training-seed variance (the t intervals over three seeds also omit problem-
sampling error shared across seeds). The gold arm has one seed.
Arm
pass@1
pass@2
Sample acc.
Untrained (seed 1)
49.2
59.4
–
Loop, seed 1
−4.8 [−9.0, −0.6]
−3.0 [−6.8, +0.6]
−2.9 [−5.8, 0.0]
Loop, seed 2
−3.2 [−6.8, +0.6]
−6.2 [−9.8, −2.4]
−5.3 [−8.1, −2.4]
Loop, seed 3
−4.2 [−8.4, −0.2]
−5.6 [−9.4, −1.6]
−5.4 [−8.3, −2.4]
Loop, mean of seeds
−4.1
−4.9
−4.5
Train on gold
−32.2 [−36.8, −27.6] −32.0 [−36.6, −27.2] −30.2 [−33.8, −26.6]
generations at round 0, 1,577 at round 1, counted over the exam and selection
problems), as in the earlier train-on-gold arms. A rerun at 2×10−5 fails the same
way (49.2% →20.6%, $-spans in 1,558 of 1,600 generations), so the failure is not
speciﬁc to the rate. We noticed the shift to the reference style but did not test
it as the cause; a collapse of this size from 300 reference solutions is also what
a pipeline defect would produce. The gate therefore fails to validate the revised
recipe, and the recipe cannot be called corrected. We have no recipe known to
raise accuracy, so the loop’s decline cannot be attributed to self-training or to
the veriﬁer. The veriﬁer-ﬁltered loop loses pass@1 in all three seeds (4.8, 3.2, 4.2
points; two intervals exclude zero) and sample accuracy in all three (intervals
exclude zero for seeds 2 and 3). The mean pass@1 change over the three seeds is
−4.1 (t interval [−6.1, −2.1]), and −4.5 for sample accuracy ([−8.1, −1.0]). The
loop does not help; the point estimates are negative in all three seeds, but the
sample is three seeds with one exam draw and one rate, so we do not claim that
it costs accuracy, and we did not isolate the cause. The detectable eﬀect is about
6 points of pass@1 (2.8h/1.96), against about 10 before.
Injected bias. As intended positive controls for the audit (neither turns out
to be one) we reran the loop once each (seed 1, 10−4) with a selection veriﬁer
that rejects \boxed answers (exam veriﬁer clean). In the ﬁrst, a hash-chosen
30% of problems are aﬀected: the \boxed share falls 4.9 points on them and 3.1
on the others (diﬀerence −0.1, [−6.1, 6.0]); a hash cannot be learned from the
problem, so this control could not elicit selective avoidance. In the second the
rule is visible: every \boxed answer is rejected when the gold contains \frac
(49 of the 300 selection problems, 263 examples kept instead of 298; 70 of the
500 exam problems, where the shares below are measured). The share on those
problems stays at 95.0% and on the others goes from 90.2% to 87.4% (diﬀerence
+2.8, [−2.8, +8.3]), against −3.7, −2.7 and −5.5 for the same split in the three
unbiased seeds, a shift in the direction opposite to avoidance; pass@1 falls 7.0
points ([−11.2, −3.0]), more than in the unbiased seeds, which we do not interpret
(one run). The model does not stop boxing where boxing is penalised, but neither
run shows selective avoidance, so neither validates the audit; we report no rt and
no count of avoidance examples for them.

12
T. S. Nguyen and D. A. Tran
5
Discussion
5.1
Answer to the Research Question
Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k with an interval excluding zero, at any rate; in the 500-problem ﬁnal
round pass@1 falls 3.2–4.8 points in each of three seeds. The sample-accuracy
ﬁgure of about 2.2 points is the largest upper limit among observed intervals, a
post hoc ﬁgure for a measure chosen after the runs that omits seed variance, not
a power statement; on the pre-set measures the design could detect only about
10 points of pass@1 and 8–10 of pass@k (6 and 5 in the ﬁnal round). Because no
arm improves and the positive gate failed, the null belongs to this recipe, and the
study cannot say whether self-training in general helps. Every score is graded by
the veriﬁer that selects the data (re-scoring ﬁve runs with V ′ leaves the decline
in place, Section 3). On the ﬁnal-round generations a stricter independent grader
(normalised string match of the last \boxed against the gold, no math-verify;
indep_grade.py) gives pass@1 changes of −3.6, −2.2, −4.6 for the three seeds
(−30.0 for the gold arm) and sample-accuracy changes of −2.5, −5.5, −5.3 (same
sign and size; intervals exclude zero for seed 3 on pass@1, seeds 2–3 on sample
accuracy). Earlier runs are not independently graded.
Does it learn to write what the veriﬁer accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably (the
largest rise is +0.7 [−6.7, +8.0]), so the rule’s silence is not evidence against
veriﬁer-style learning. No run varies the frequent gold-storage defect, and the
post hoc audit of Section 5.3 is too weak to show or rule out adaptation to it.
What happened to the pooled collapse? We cannot say whether pooling,
selection-set scoring or the 4.5× larger dose produced it.
5.2
Interpretation
One explanation of the Design P curves is a self-reinforcing shrinking pool shaped
by the biased veriﬁer. The data neither support nor rule it out: the patch tests
a rare bias, and the no-ﬁlter control declines without any veriﬁer but with more
dose. At this resolution, removing a rare format defect, or the ﬁlter entirely, made
no consistent diﬀerence; neither tests the systematic false positives Egashira et
al. ﬁnd harmful in RLVR.
5.3
A Proposed Audit for GVT with a Biased Veriﬁer
Our pre-set rule tied “learning the veriﬁer’s style” to rising accuracy, so it could
not speak once accuracy fell. From post hoc analyses we propose four checks for
self-training with a rule-based veriﬁer, as a protocol for future studies, not as
tested methods.
(i) A per-round false-reject audit. Fix a repaired veriﬁer V ′ that corrects a
known defect class of the training veriﬁer V . At each round t, on the loop’s own

Mathematics or the Veriﬁer?
13
generations, compute
rt = #{accepted by V ′ but rejected by V }
#{accepted by V ′}
.
If the model learns to write what V accepts, rt may fall over rounds, but it
also falls when fewer answers are boxed: since V ′ diﬀers from V only on boxed
predictions, rt = rboxed
t
×(boxed share among V ′-accepted) holds as an identity.
This is the per-step tracking of RLVR studies [4,17] applied to oﬄine SFT;
overall rt is not enough on its own (Table 5; rt_audit.py in the repository).
For the gold-storage defect it falls in all three self-training runs we re-scored,
by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching zero. But
V ′ diﬀers from V only on boxed predictions, so unboxed correct answers enter
only the denominator, and the fall is accounted for by the falling \boxed share
among correct answers (91 →76% and 93 →78% at 5×10−4). That accounting
is an identity, not a test, and it does not exclude adaptation. On boxed answers
alone the changes (−0.4 to +0.7 points) have intervals (≈±3) that contain the
whole −2.6 fall, so “ﬂat” means not detected. The defect is also bound to the
problem: it ﬁres on 54–62 problems, rejecting 94–98% of correct answers (87–98%
where V parses the gold), and 29–34 of them have an unparseable gold, so no
answer form escapes it. On the 24–28 aﬀected problems where some form could,
rt moves by −5.5, −1.6 and −0.2 points (intervals 10–26 wide), and the training
pool holds only 2–12 examples per round that write these answers unboxed. We
expect the pressure to adapt under SFT to be weak, but we did not test this
(no dose–response). Our two injected-bias runs (Section 4.6) show no selective
avoidance either, but one cannot elicit it and the other is a single run without
rt, so we cannot tell whether the audit would detect adaptation. Train-on-gold,
with no veriﬁer in the loop, gives rt rises of 2.1–3.3 points, and even rt on boxed
answers alone rises by 2.8 and 1.7 (Table 5), so rt drifts by about as much as
the falls we observe for reasons unrelated to the veriﬁer. It should be reported
on the answers and problems where V and V ′ can diﬀer and an accepted form
exists, with the count of training examples that could teach avoidance.
(ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Sup-
plementary Appendix H). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.
(iii) Check the dose of a control before running it: our \dfrac patch changed
0–4 examples, the unvaried gold-storage defect a ﬁfth to a quarter of the pool
(440 →542).
(iv) Match training dose across designs (examples, steps and rate): the pooled
design’s decline cannot be attributed to pooling.
Check (i) in RLVR. A false reject gives zero reward there; we have not run
the audit on RLVR checkpoints.

14
T. S. Nguyen and D. A. Tran
Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all 500
problems), round 0 →last round, with the change and a 95% problem-level bootstrap
interval (2,000 resamples). “Boxed only” restricts to predictions containing \boxed;
“aﬀected, parseable” to problems where the defect ever ﬁres and V can parse the gold.
Pool: examples per round from aﬀected problems that V accepts (and so avoid the
defect).
Run
rt subset
R0
Last
∆
95% interval
Pool
A, 5 × 10−4, seed 1
all
18.3
15.7
−2.6
[−5.3, 0.3]
3–5
boxed only
20.0
20.7
+0.7
[−2.9, 4.3]
aﬀected, parseable
92.8
87.2
−5.5
[−20.1, 6.3]
A, 5 × 10−4, seed 2
all
18.1
15.5
−2.6
[−5.2, 0.1]
2–3
boxed only
19.4
19.8
+0.4
[−2.8, 3.4]
aﬀected, parseable
95.1
93.5
−1.6
[−14.7, 9.5]
A, 10−5, seed 0
all
18.3
16.8
−1.5
[−2.9, 0.0]
9–12
boxed only
19.9
19.5
−0.4
[−2.0, 1.2]
aﬀected, parseable
92.3
92.0
−0.2
[−4.9, 4.6]
Gold, seed 1
all
18.2
21.5
+3.3
[−1.2, 8.1]
—
boxed only
20.0
22.8
+2.8
[−2.0, 7.7]
aﬀected, parseable
95.5
94.7
−0.7
[−9.1, 6.2]
Gold, seed 2
all
18.0
20.2
+2.1
[−2.2, 6.7]
—
boxed only
19.4
21.1
+1.7
[−3.3, 6.5]
aﬀected, parseable
95.1
97.6
+2.5
[−4.8, 11.9]
6
Limitations
Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem draw
and sampling, not training-seed variance; the ﬁnal-round loop has three seeds,
the gate and the bias controls one, and no multiplicity correction is applied. The
learning-rate grid is coarse and changes k, rounds, dose and metric along with the
rate. Power is limited (about 10 points of pass@1 with 150 exam problems, about
6 in Section 4.6). The adaptation audit is weak: 24–28 problems, 2–12 avoidance
examples per round, and no valid positive control. The ﬁnal-round loop has no
no-ﬁlter arm. The veriﬁer audit used other models’ solutions and inspected only
rejections; the gold-storage defect was measured afterwards and ran unvaried
through every run before the ﬁnal round, and every headline number is graded by
the biased veriﬁer that also selects the data. Truncation: the 512-token cap binds
from the start (a quarter of the pool is cut). Scope: one model family and size,
all instruction-tuned (no base model), one veriﬁer, a restart-from-base design
that leaves compounding little room (no continued training), and possible test-
set contamination of Qwen2.5 on MATH/GSM8K (unquantiﬁed), and a default

Mathematics or the Veriﬁer?
15
repetition penalty (1.1) that may depress the baseline. No positive reference: no
arm improves on round 0 and the gate failed even with the revised recipe.
7
Conclusion
We asked whether generate–verify–select–train iterations make a 1.5B model
better at mathematics or only teach it to write what a rule-based veriﬁer accepts.
The design detected no pass@1 or pass@k gain at any rate (it could see only
gains of about 10 and 8–10 points; 6 in a ﬁnal 500-problem round, where pass@1
falls 3.2–4.8 points in all three seeds). Because training on reference solutions
lowers pass@1 by about 30 points even with a revised recipe, this is a null for
the recipe and says little about self-training, and since every score is graded by
the selecting veriﬁer, neither branch of the question is answered. The post hoc
false-reject audit is uninformative about adaptation: its fall is tied to the falling
\boxed share by an identity, and with about 25 aﬀected problems, a handful
of avoidance examples per round and two injected-bias runs that are not valid
positive controls, it has little power. At the highest rate the model is less accurate
on the solutions it ﬁnishes. The pooled design’s decline does not reproduce under
isolation, though dose and pooling are confounded.
A dose-matched control for the gold-storage defect, a recipe that passes the
positive gate, and a second grader come ﬁrst (Supplementary Appendix K).
Acknowledgments. This work was carried out as an undergraduate research project.
No external funding was received.
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.
Code availability Code, saved generations and analysis scripts are at https://github.
com/tsan2711/DACNTT_2026 (tag paper-2026-11b). Generation-time token counts,
Design P’s training logs and the 1,536-token re-scoring outputs were not saved.
Use of AI tools The authors used Claude (Anthropic), through Claude Code, to help
write the manuscript, the analysis and training scripts, and to run automated reviews.
The authors designed the study, ran the experiments and take responsibility for the
content.
References
1. Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., Sugiyama, M.: Reinforce-
ment Learning with Veriﬁable yet Noisy Rewards under Imperfect Veriﬁers.
arXiv:2510.00915 (2025)
2. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,
M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training Veriﬁers
to Solve Math Word Problems. arXiv:2110.14168 (2021)

16
T. S. Nguyen and D. A. Tran
3. Dang, Q.-A., Ngo, C.: Reinforcement Learning for Reasoning in Small LLMs: What
Works and What Doesn’t. arXiv:2503.16219 (2025)
4. Egashira, K., Vero, M., Dekoninck, J., Dörner, F.E., Staab, R., Vechev, M.: Delay,
Plateau, or Collapse: Evaluating the Impact of Systematic Veriﬁcation Error on
RLVR. arXiv:2605.02909 (2026)
5. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song,
D., Steinhardt, J.: Measuring Mathematical Problem Solving With the MATH
Dataset. arXiv:2103.03874 (2021)
6. Huang, Y., Zeng, W., Zeng, X., Zhu, Q., He, J.: From Accuracy to Robust-
ness: A Study of Rule- and Model-based Veriﬁers in Mathematical Reasoning.
arXiv:2505.22203 (2025)
7. Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J.,
Schulman, J., Sutskever, I., Cobbe, K.: Let’s Verify Step by Step. arXiv:2305.20050
(2023)
8. Kim, J., Luo, X., Kim, M., Lee, S., Kim, D., Jeon, J., Li, D., Yang, Y.: Why
Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
arXiv:2603.24472 (2026)
9. Qiao, X., Du, X., Liu, W., Zhang, J., Mai, P., Zhang, M., Pang, Y.: When Sample
Selection Bias Precipitates Model Collapse. arXiv:2606.13732 (2026)
10. Shao, R., Li, S.S., Xin, R., Geng, S., Wang, Y., Oh, S., Du, S.S., Lambert, N., Min,
S., Krishna, R., Tsvetkov, Y., Hajishirzi, H., Koh, P.W., Zettlemoyer, L.: Spurious
Rewards: Rethinking Training Signals in RLVR. arXiv:2506.10947 (2025)
11. Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., Gal, Y.: AI
models collapse when trained on recursively generated data. Nature (2024). https:
//doi.org/10.1038/s41586-024-07566-y
12. Singh, A., Co-Reyes, J.D., Agarwal, R., et al.: Beyond Human Data: Scaling Self-
Training for Problem-Solving with Language Models. arXiv:2312.06585 (2023)
13. Gulcehre, C., Le Paine, T., Srinivasan, S., et al.: Reinforced Self-Training (ReST)
for Language Modeling. arXiv:2308.08998 (2023)
14. Strozzi, I.L.: Teacher-Free Self-Training Ampliﬁes but Does Not Compound: A
Pass@k Crossover on a Free-Veriﬁer Domain. arXiv:2606.07856 (2026)
15. Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B., Cheng, H., He, X., Wang,
K., Gao, J., Chen, W., Wang, S., Du, S.S., Shen, Y.: Reinforcement Learning for
Reasoning in Large Language Models with One Training Example. In: NeurIPS
(2025). arXiv:2504.20571
16. Xu, C., Yan, N., Chen, L., Kechadi, M.-T.: Phantom Gains: Auditing Self-
Improvement Against a Measured Null. arXiv:2608.20290 (2026)
17. Xu, Z., Li, Y., Jiang, F., Ramasubramanian, B., Niu, L., Lin, B., Poovendran, R.:
TinyV: Reducing False Negatives in Veriﬁcation Improves RL for LLM Reasoning.
arXiv:2505.14625 (2025)
18. Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou, C., Zhou, J.: Scaling
Relationship on Learning Mathematical Reasoning with Large Language Models.
arXiv:2308.01825 (2023)
19. Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song, S., Huang, G.: Does
Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond
the Base Model? arXiv:2504.13837 (2025)
20. Zelikman, E., Wu, Y., Mu, J., Goodman, N.D.: STaR: Bootstrapping Reasoning
With Reasoning. arXiv:2203.14465 (2022)
21. Zeng, W., Huang, Y., Liu, Q., Liu, W., He, K., Ma, Z., He, J.: SimpleRL-Zoo:
Investigating and Taming Zero Reinforcement Learning for Open Base Models in
the Wild. arXiv:2503.18892 (2025)
