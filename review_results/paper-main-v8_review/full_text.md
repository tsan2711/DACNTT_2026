    Mathematics or the Veriﬁer? A Null Result for
    One Veriﬁer-Filtered Self-Training Recipe on a
                     1.5B Model

            Dinh-Hong Vu1 , Tan Sang Nguyen2 , and Duy Anh Tran2
1
  Natural Language Processing and Knowledge Discovery Research Group, Faculty of
  Information Technology, Ton Duc Thang University, Ho Chi Minh City, Vietnam
2
  Faculty of Information Technology, Ton Duc Thang University, Ho Chi Minh City,
                                     Vietnam
            vudinhhong@tdtu.edu.vn, 52300057@student.tdtu.edu.vn,
                         52300006@student.tdtu.edu.vn
      Corresponding author: 52300057@student.tdtu.edu.vn (Tan Sang Nguyen)



       Abstract. Self-training and reinforcement learning with veriﬁable re-
       wards report large gains for small language models, but a rising score
       does not show that a model learned mathematics rather than what its
       veriﬁer accepts. We study the cheapest form of the loop, generate–verify–
       select–train with oﬄine LoRA SFT, on Qwen2.5-1.5B-Instruct with the
       rule-based veriﬁer math-verify, on held-out MATH-500 and GSM8K ex-
       ams (150 problems; 500 in a ﬁnal round). No pass@1 or pass@k gain at
       any of four learning rates has a problem-level bootstrap interval exclud-
       ing zero; in the ﬁnal round, with a revised recipe, pass@1 falls 3.2–4.8
       points in each of three seeds (mean −4.1). The design detects only gains
       of about 10 points of pass@1 (6 in the ﬁnal round). Two gates disagree.
       Training on terse reference solutions lowers pass@1 by 32.2 points (solu-
       tions shorten 3.2×), but training on 228–237 veriﬁed full solutions from
       Qwen2.5-7B-Instruct leaves it unchanged in two seeds (+0.2 [−4.0, +4.6],
       +3.2 [−0.8, +7.0]), while the loop loses 4.8 and 3.2 (diﬀerences +5.0
       [+0.8, +9.2], +6.4 [+2.2, +10.6]). The pipeline alone thus does not cause
       the decline, but nothing raises accuracy, so the null concerns this recipe
       only. All runs are graded by one patched veriﬁer and a string-match
       check, so neither the mathematics nor the veriﬁer question is answered;
       a post hoc audit of a gold-storage defect (about 15–18% of correct solu-
       tions rejected) is uninformative about adaptation.

       Keywords: self-training · self-improvement · veriﬁer bias · mathe-
       matical reasoning · small language models · veriﬁable rewards · null
       result.


1    Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on
2         D.-H. Vu et al.

them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [19], ReST [12], ReST-EM [11] and rejection-sampling ﬁne-
tuning [17]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such
as math-verify3 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
    The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR): only 8.6 of one study’s 37.6 points lie beyond format correction [14],
and GRPO with random rewards raises Qwen2.5-Math-7B by 21.4 points on
MATH-500, against 29.1 with ground-truth rewards [9]. A rising score does not
by itself show that a model learned to solve more problems rather than to surface
behaviour it had or to produce what its reward accepts. We study the question
in a cheap and common form of the loop, oﬄine rejection-sampling SFT, where
a false reject removes a training example, and apply a per-round false-reject
measurement there, post hoc, for one defect of our pipeline.
    We ask: after several GVT rounds, is the model better at mathematics, or has
it only learned to write what the veriﬁer accepts? We ﬁxed four measures in ad-
vance: (i) pass@1; (ii) pass@k; (iii) output style, chieﬂy the share of generations
containing \boxed; and (iv) per-problem transitions (problems added and lost
between rounds). The pre-set reading rule was that “learning the veriﬁer’s style”
requires pass@1 to rise, pass@k to stay ﬂat and style to converge at once. In
hindsight the rule is one-sided: it can only ﬁre when accuracy rises (Section 5.1).
The higher learning rates, the controls, sample accuracy as primary measure,
the termination measures, the re-scoring and the ﬁnal 500-problem round (Sec-
tion 4.6) were added after seeing earlier runs; all are post hoc.
    We detect no improvement at any learning rate, though gains below about 10
points of pass@1 or 4–6.5 of sample accuracy could have been missed (intervals
omit training-seed variance), and no arm of this recipe improves, so the result
concerns the recipe. The second branch is untested: no run varies the frequent
veriﬁer defect, scores are graded by a veriﬁer of the selecting family (V ′ , with
a string-match check), and the post hoc audit of Section 5.2 is uninformative
about adaptation. Most clearly at the highest rate, accuracy falls on the solu-
tions the model does ﬁnish, though on one seed the cap share carries more of
it (Section 4.5). A sharp pooled decline is absent in the isolated runs at 10−5 ,
which train on about 4.5× fewer examples; dose and pooling are confounded.

Contributions.

    – For a 1.5B model, LoRA SFT and one rule-based veriﬁer, no gain is de-
      tectable on a held-out exam at any learning rate we tried (a coarse grid that
      also changes k and rounds), with bootstrap intervals and the smallest eﬀects
      the design could detect. No arm improves, not even training on reference
      solutions, so this is a null for the recipe, not a statement about self-training.
3
    https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
    work.
                                              Mathematics or the Veriﬁer?       3

 – A post hoc per-round false-reject audit of one veriﬁer defect (the RLVR
   tracking [4,16] applied to oﬄine SFT; not a novel method). The rejected
   share falls by 1.5–2.6 points with intervals reaching zero, tied to the falling
   \boxed share by an identity; the audit is uninformative about adaptation
   (Section 5.2).
 – A decomposition of an accuracy decline under a ﬁxed token cap into a
   ﬁnished-accuracy part and a cap-share part: at the highest rate, ﬁnished
   generations lose 1.5–9.0 points against the untrained model on the same
   problem mix (A, B and no-ﬁlter runs, two of six intervals excluding zero;
   train-on-gold about 24–26).


2   Related Work

Self-training and its limits. STaR [19] introduced the generate–ﬁlter–retrain
loop, and ReST [12], ReST-EM [11] and RFT [17] formalise it; ReST-EM, which
like us restarts from the base model, reports diminishing gains after the ﬁrst
round. Yue et al. [18] show that RL raises pass@1 while the base model wins at
large pass@k; Teacher-Free Self-Training [13] concludes that self-training “ampli-
ﬁes but does not compound”. Repeated training on model-generated data erodes
distribution tails [10], and a narrow selector can accelerate this [8].

RL with veriﬁable rewards at small scale. RLVR with GRPO reports large gains
near our model size: one training example lifts Qwen2.5-Math-1.5B on MATH-
500 from 36.0% to 73.6% [14], 7,000 examples lift DeepSeek-R1-Distill-Qwen-
1.5B on AMC23 from 63% to 80% [3], and zero-RL works on open base models
from 0.5B [20]. These studies improve accuracy, which our SFT loop does not,
though of Wang et al.’s 37.6 points only 8.6 lie beyond format correction, and
random rewards also help [9].

Veriﬁer error. TinyV [16] ﬁnds that rule-based veriﬁers reject many correct
solutions; From Accuracy to Robustness [6] reports an average recall of 86%,
and 0.95 for math-verify on their MATH subset. Imperfect Veriﬁers [1] models
ﬁxed false-accept and false-reject rates. Egashira et al. [4] ﬁnd in RLVR that
systematic false negatives behave like random noise whereas false positives can
cause plateau or collapse, and that the policy ﬁrst unlearns format-triggering
behaviour. Our setting is oﬄine SFT with a fresh adapter per round, and our
controls cannot test their ﬁndings (Section 4.3).

Auditing self-improvement. Xu et al. [15] audit LoRA self-training of Qwen3-
8B against a frozen control and identify seven measurement failures, includ-
ing training-seed variance and a ﬁxed token cap under style drift. This is the
study closest to ours; it is why we separate ﬁnished accuracy from termination
(Section 4.5). We diﬀer in (i) model and recipe (Qwen2.5-1.5B-Instruct, rank-
16 LoRA, learning rate varied over 10−5 –5 × 10−4 , against Qwen3-8B at rank
32); (ii) evaluation (150 or 500 MATH-500 problems at k ≤ 8, against 200 at
4       D.-H. Vu et al.

k = 128); and (iii) the control (they distil from gpt-oss-120b; ours are refer-
ence solutions and Qwen2.5-7B-Instruct solutions, Section 4.6). Both grade with
Math-Verify; we also patch it. Kim et al. [7] show that self-distillation with a
teacher that sees the solution can cut accuracy; our train-on-gold drop resembles
this, but we did not test its cause. Our per-round false-reject measurement is not
new (per-step tracking as in Egashira et al. and TinyV, applied to oﬄine SFT);
we claim neither it nor the patch control. The Supplementary (a separate ﬁle;
supplementary.tex in the repository) gives the full comparison in Appendix A.


3     Setup

3.1   The GVT Loop

Each round t has four steps. Generate: the current model samples k solutions per
problem. Verify: math-verify extracts the ﬁnal answer and compares it with the
gold. Select: accepted solutions are kept. Train: a fresh LoRA adapter is attached
to the base model and trained on the kept solutions for one epoch. Round 0 is
the untrained base model; the round-t model (t ≥ 1) is the base plus an adapter
trained on the pool accepted at round t − 1. Adapters are not accumulated, so
earlier rounds aﬀect later ones only through the data they generate; this restart-
from-base design gives compounding less room than continued training would.


3.2   The Veriﬁer and Its Directional Bias

A format probe that re-renders gold answers in valid forms shows that \dfrac
and \tfrac are always rejected, on both datasets. On real solutions (one pub-
lic Qwen2.5-7B-Instruct solution for each of 200 MATH-500 problems, judged
correct by a normalised comparison) the false-negative rate is 7.8% (10 of 128;
Wilson interval 4.3–13.8%) on MATH-500 and 0% on GSM8K. Eight of the ten
fail when the whole solution is veriﬁed but pass when only the boxed answer is,
probably the gold-storage defect described below. The audit inspected only re-
jections, so it gives no false-positive rate. The veriﬁer also cannot parse 51 of the
500 stored MATH-500 golds (10.2%); under V these always count as unsolved
and never enter the training pool (V ′ makes 46 parseable for boxed predictions).
This cancels in within-run diﬀerences only if they would not otherwise change
(unchecked; 11–18 per exam partition).
    The patch. For the control we rewrote \dfrac and \tfrac to \frac before
parsing, and nothing else.
    The gold-storage defect (post hoc). Our pipeline stores the gold without a de-
limiter, and math-verify applies its full LATEX extraction only inside \boxed{}
or $...$, so a correct boxed prediction can fail against a bare gold (e.g. the
prediction \boxed{\frac{4}{3}} against the stored gold \frac43). Re-scoring
the saved generations with a veriﬁer V ′ that wraps the gold in \boxed{} when
the prediction contains one shows that this defect rejects 15.5–18.3% of the gen-
erations V ′ accepts. It would enlarge the round-0 kept pool by about a ﬁfth
                                              Mathematics or the Veriﬁer?       5

to a quarter (440 → 542, +23%; selection problems only, so its 18.8% rejected
share diﬀers from the 15.5–18.3% over all 500), against 0–4 examples for the
\dfrac patch, and it lowers absolute pass@1 by 4.7–8.0 points in self-training.
It is bound to the problem, not to the answer: on the 54–62 problems where
it ever ﬁres, it rejects 94–98% of correct answers in every round, and 29–34 of
these problems have a gold the original veriﬁer cannot parse at all, so no answer
form avoids it there. Every table grades all runs with V ′ , which the loop used
only in the ﬁnal round, so round-0 values are higher than in the original run logs
(pass@1 40.0 against 33.3 for Run A at seed 1), and the declines remain. Time-
outs of math-verify, which version 0.9.0 reports only as a log message, were
detected and retried at 60 s. Supplementary Appendix B gives the full analysis.

3.3   Two Experimental Designs
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
repeated at a second seed. A “seed” sets the exam partition, the selection set and
the training randomness at once, so a repetition draws a diﬀerent 150-problem
exam set. Most of the later evidence comes from higher-rate runs (Section 4.4;
Table S4 in Supplementary Appendix E lists every run). “Five rounds” means
round 0 (the untrained model) and four adapters; “three rounds” means round 0
and two adapters, so the round-2 model is a single adapter (about 195 optimizer
steps for Run A at 5 × 10−4 ) trained on the round-1 pool.

3.4   Models, Data, Training, Metrics
We use Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct (Design P uses both,
Design I the 1.5B model only) and the ﬁrst 500 problems of the GSM8K test
split [2] and MATH-500, the 500-problem subset of MATH [5]. The prompt is a
single user turn: “Solve the math problem. Put the ﬁnal answer in \boxed{}.”
followed by the problem. Generation samples at temperature 0.8 with a cap of
512 new tokens; the other decoding settings come from the checkpoint’s gen-
eration conﬁguration (top-p 0.8, top-k 20, repetition penalty 1.1). Training is
LoRA SFT (transformers 5.0.0, peft 0.19.1, TRL 1.10.0 SFTTrainer; rank 16,
α = 32, on q_proj and v_proj, LoRA dropout 0, weight decay 0, gradient clip-
ping 1.0 and trainer seed 42, all library defaults read from the pinned sources;
batch size 2, no accumulation; one epoch; AdamW with linear learning-rate de-
cay and no warmup; loss over the whole chat sequence, prompt included; fp16 on
6       D.-H. Vu et al.

one Kaggle T4), with a training sequence limit of 512 tokens that includes the
prompt. Because this limit equals the generation cap but also holds the prompt,
any kept solution longer than about 512 tokens minus the prompt length is cut
in training and loses its ﬁnal answer and end-of-sequence token (24–26% of the
round-0 pool; Section 4.5). All kept solutions are used, so the number of op-
timizer steps per round is half the pool size. The learning rate is 10−5 unless
stated otherwise; this value was our code’s default and was not tuned. Metrics
per round, on the exam set: pass@1 is the correctness of the ﬁrst of the k samples
(one draw per problem, so it carries sampling noise); pass@k; sample accuracy,
the mean over all k samples; style counts over all generations (boxed, dfrac, dol-
lar, . . . ); and per-problem added/lost counts between consecutive rounds, where
a problem is solved in a round if at least one of its k samples is accepted. Added
minus lost therefore equals 150 × ∆pass@k: the counts show gross churn, not an
independent test. pass@1 was ﬁxed in advance; sample accuracy was not, but it
estimates the same quantity from all k samples with less variance, so after the
runs we chose it as the primary accuracy measure (claims resting on it, including
the 1.7-point bound, are post hoc in the choice of measure). “Correct” always
means accepted by the veriﬁer (preset reward), the same veriﬁer that selects the
training data.

Uncertainty. For every within-run change (round 0 against the last round) and
every paired comparison of two runs on the same exam partition we report a
95% interval from a paired problem-level bootstrap (10,000 resamples of the
150 exam problems; 2,000 for the audit table), which respects the clustering
of the k samples within a problem. These intervals do not cover training-seed
variance, which we see only across two or three seeds: the replicate pair we use
as a gauge ends 3.8 points of sample accuracy apart (a seed also changes the
exam partition, so such pairs mix training and partition variance). We make
no multiplicity correction and the runs are not independent (they share exam
partitions and round-0 draws), so patterns across runs are descriptive, not tests.
Single proportions use Wilson intervals. Detectable eﬀects. From the interval
half-widths h in Table 2, a change would be detected with 80% power at the
5% level only if it exceeded about 2.8 h/1.96: about 10 points of pass@1, 8–
10 of pass@k and 4–6.5 of sample accuracy on MATH-500. Because h omits
training-seed variance (the replicate pair diﬀers by 3.8 points and B minus A
ﬂips from +5.3 to −5.3 on near-identical pools, Section 4.4), these are optimistic
thresholds, not bounds: even with h as the whole error, a gain at that size is
missed 20% of the time, and probably more often (Supplementary Appendix C).


4     Results

4.1   Design P: An Apparent Collapse

In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 53.6% → 19.2%, pass@8 77.8% → 51.0%; Table S3, Supplementary
                                               Mathematics or the Veriﬁer?       7

Appendix D), on both datasets (Table S2); the 0.5B decline is small. The ac-
cepted pool contracts every round and \boxed{} falls from 5,608 to 2,693 of
8,000 generations. This design cannot be read causally: one adapter trains on
both pools, it scores on the problems it selects from, and it trains on about 4.5×
as many examples per round as the isolated MATH-500 run (3,962 against 872
at round 0) (Supplementary Appendix D).

4.2   Design I at 10−5 : Small Declines, a Larger One on GSM8K
On the held-out exam (Fig. S1 and Table S5 in Supplementary Appendix E)
pass@8 ends within 6 points of round 0 in every run. On MATH-500, pass@1 is
3.3–4.7 points lower at round 4, with every interval including zero (Table 2); sam-
ple accuracy falls 2.6–4.2 points, with an interval excluding zero for three of the
four runs (not B at seed 1, [−5.4, +0.2]), and matched ﬁnished accuracy changes
by −1.3 to +2.3, with every interval including zero. We read this as a possible
small decline, not an established one; we see no gain of the size the design could
detect. Run C (GSM8K) declines more: pass@1 falls 12.7 points ([−22.0, −3.3]),
but it took about twice Run A’s optimizer steps, so we do not attribute this to
the dataset alone. Length and cap-hit share barely change on MATH-500, weak
evidence that the adapter did little (Supplementary Appendix E).

4.3   The Patch Control Could Not Detect an Eﬀect
At round 4, B minus A is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and
+0.7 [−2.0, +3.3] at seed 1 (Table 2, all runs graded by the same veriﬁer). This
null is uninformative: \dfrac appears in 0.50–0.73% of generations, so the kept
pools diﬀer by at most 4 examples (under 0.5% of 872), and at 10−5 the adapter
changes the outputs little anyway; the frequent gold-storage defect is in both
arms.

4.4   Higher Learning Rates
Because 10−5 changed the MATH-500 outputs little, we reran Run A at 10−4
(three seeds), 2 × 10−4 (two) and 5 × 10−4 (two, with Run B), with three rounds
and k = 4 (Table 1). These runs also diﬀer from the 10−5 runs in k, rounds,
pool size and metric, so only 10−4 to 5 × 10−4 isolates the rate. At 5 × 10−4
every A/B run declines: pass@1 falls 6.0–12.0 points and the sample-accuracy
intervals exclude zero in all four A/B runs, though same-seed A and B are closer
to two replicates. The decline may grow with the rate on one seed: at seed 1
sample accuracy falls 3.7, 6.0 and 10.8 points across the three rates, at seed 2
4.7, 6.0 and 6.0. The cap-hit share rises only at 5 × 10−4 . The patch has no
consistent eﬀect: B minus A in round-2 pass@1 is +5.3 [−2.0, +12.7] at seed 1
and −5.3 [−12.0, +1.3] at seed 2, a sign ﬂip from pools diﬀering by 0–3 examples:
trajectory noise. Style does not separate imitation from drift: boxed share falls
with the pool, which both would produce, and the no-ﬁlter and gold arms decline
with no veriﬁer in the selection step (they are still scored by it), so generic SFT
damage ﬁts as well.
8          D.-H. Vu et al.

Table 1. Run A (MATH-500, k = 4, three rounds) across learning rates and seeds:
pass@1, pass@4 and sample accuracy at round 0 → round 2, the share of round-2
generations that hit the 512-token cap (re-tokenised to ≥ 508 tokens; round 0 is 43.0–
43.2%, 48.2% at seed 3), and problems added/lost over rounds 1–2. The 5 × 10−4 rows
are the A rows of Table S6.

    Rate       Seed       pass@1      pass@4      Sample acc. Cap-hit (R2) Added/lost
      −4
    10         1        40.0 → 38.7 60.0 → 56.0 41.0 → 37.3           42.7%          19/25
    10−4       2        38.0 → 34.7 60.0 → 54.7 37.7 → 33.0           42.8%          25/33
    10−4       3        35.3 → 30.7 46.0 → 48.0 34.5 → 32.2           45.7%          17/14
    2 × 10−4   1        40.0 → 37.3 60.0 → 55.3 41.0 → 35.0           40.8%          24/31
    2 × 10−4   2        38.0 → 30.0 60.0 → 53.3 37.7 → 31.7           39.7%          22/32
    5 × 10−4   1        40.0 → 28.0 60.0 → 50.7 41.0 → 30.2           46.2%          22/36
    5 × 10−4   2        38.0 → 32.0 60.0 → 52.7 37.7 → 31.7           51.2%          26/37

Table 2. Change from round 0 to the last round (percentage points) with 95%
paired problem-level bootstrap intervals over the 150 exam problems (10,000 resamples;
bootstrap_ci.py in the code repository). Last round is R4 at 10−5 (k = 8) and R2
elsewhere (k = 4). “Finished, matched” is the last-round accuracy of generations be-
low the 512-token cap minus the untrained model’s accuracy on the same problem mix
(Section 4.5; 10,000 resamples). The intervals do not include training-seed variance. A,
0: equal entries (same 5 problems). Every run is regraded from its saved generations
with the same veriﬁer (Supplementary Appendix C).

Run, seed          ∆pass@1             ∆pass@k            ∆sample acc.        Finished, matched
                   −5
Learning rate 10
A, 0        −3.3 [−10.7, +4.0]     −3.3 [−10.7, +4.0]    −3.3 [−5.9, −0.7]   −0.7 [−4.4, +3.2]
A, 1        −4.7 [−12.0, +2.7]     −1.3 [−7.3, +4.7]     −3.1 [−6.0, −0.2]   +0.8 [−3.5, +5.2]
B, 0        −4.0 [−11.3, +4.0]     −5.3 [−12.0, +2.0]    −4.2 [−7.1, −1.2]   −1.3 [−5.5, +3.0]
B, 1        −4.0 [−11.3, +2.7]     −2.0 [−8.0, +4.0]     −2.6 [−5.4, +0.2]   +2.3 [−1.9, +6.5]
C, 0       −12.7 [−22.0, −3.3]     −2.7 [−8.0, +2.0]    −13.0 [−16.5, −9.6] −12.2 [−15.8, −8.8]
Learning rate 10−4
A, 1         −1.3 [−8.7, +6.0]     −4.0 [−10.0, +2.0]    −3.7 [−7.8, +0.5]    −1.3 [−6.9, +4.4]
A, 2        −3.3 [−10.0, +3.3]     −5.3 [−12.0, +1.3]    −4.7 [−8.7, −0.8]    −0.6 [−6.2, +5.1]
A, 3        −4.7 [−12.0, +2.7]     +2.0 [−4.0, +8.0]     −2.3 [−6.5, +1.7]    −1.0 [−7.5, +5.4]
Learning rate 2×10−4
A, 1         −2.7 [−9.3, +4.0]     −4.7 [−11.3, +2.0]   −6.0 [−10.0, −2.0]    −2.6 [−8.1, +2.9]
A, 2        −8.0 [−15.3, +0.0]     −6.7 [−13.3, +0.0]   −6.0 [−10.3, −1.7]    −3.2 [−9.5, +3.1]
Learning rate 5×10−4
A, 1        −12.0 [−19.3, −4.7] −9.3 [−16.0, −2.7] −10.8 [−15.2, −6.7] −6.1 [−11.3, −0.8]
A, 2         −6.0 [−13.3, +2.0]   −7.3 [−14.0, −0.7]   −6.0 [−9.8, −2.2]    −1.5 [−7.4, +4.4]
B, 1         −6.7 [−14.7, +1.3]   −5.3 [−12.7, +1.3]   −8.7 [−12.8, −4.7]   −4.1 [−9.8, +1.7]
B, 2        −11.3 [−18.0, −4.7] −12.0 [−18.7, −5.3] −10.7 [−14.7, −6.7]     −3.2 [−9.2, +2.9]
No ﬁlter, 1 −8.7 [−16.0, −1.3] −13.3 [−21.3, −6.0] −11.7 [−16.2, −7.3] −9.0 [−14.8, −3.3]
No ﬁlter, 2 −10.7 [−18.7, −3.3] −12.0 [−19.3, −4.7] −12.3 [−16.7, −8.0]     −3.6 [−9.6, +2.5]
Gold, 1     −24.0 [−32.7, −15.3] −24.0 [−32.7, −15.3] −24.8 [−30.7, −19.0] −26.0 [−32.0, −20.0]
Gold, 2     −24.7 [−33.3, −16.0] −20.7 [−29.3, −12.0] −21.8 [−27.5, −16.3] −23.7 [−29.7, −17.9]
C, 1        −22.0 [−29.3, −15.3] −9.3 [−15.3, −3.3] −15.3 [−19.8, −11.0] −11.3 [−15.7, −7.0]




Two controls at 5 × 10−4 . The no-ﬁlter run trains on all k samples of every
selection problem (1,400 examples per round), removing the veriﬁer; the train-
on-gold run trains on the 350 reference solutions every round (Table 3). Neither
                                                Mathematics or the Veriﬁer?        9

is a single-variable control: no-ﬁlter takes 3–4× Run A’s optimizer steps, train-
on-gold about the same. Removing the ﬁlter is not better than keeping it beyond
noise and is lower on pass@4 at both seeds (round-2 diﬀerences −4.0 and −4.7
points, intervals including zero), but the dose diﬀerence means this cannot be
attributed to the ﬁlter; the no-ﬁlter pool is also truncated far more often in
training (62.4% against 24.5% at round 0). Training on reference solutions is
followed by a much larger decline (pass@4 down 24.0 and 20.7 points at the two
seeds) while the model adopts the reference style ($-delimited spans 5% → 98%).
Post hoc checks bound veriﬁer error from below only (about 2 points of sample
accuracy among boxed answers), so we cannot bound it from above. That no
arm, this one included, improves on the untrained model means we have no
positive reference: the nulls above may reﬂect the recipe (LoRA on q/v, loss
over the prompt, a 512-token limit) rather than self-training. Run C at 5 × 10−4
(GSM8K) falls 22.0 points of pass@1 (Supplementary Appendix G).


Table 3. Controls at 5×10−4 (MATH-500, k = 4, three rounds), on the exam partition
of Run A at the same seed. Pool is the kept pool at round 0 → round 2; the round-2
model trains on the round-1 pool (392 and 386 examples, about 195 steps).

       Run                    Pool            pass@1                pass@4
                                       R0       R1   R2      R0       R1   R2
       Seed 1
       A (veriﬁer-ﬁltered)   440→326   40.0    40.0   28.0   60.0    58.7   50.7
       No ﬁlter                1400    40.0    34.0   31.3   60.0    58.0   46.7
       Train on gold           350     40.0    18.7   16.0   60.0    36.0   36.0
       Seed 2
       A (veriﬁer-ﬁltered)   424→350   38.0    38.7   32.0   60.0    56.0   52.7
       No ﬁlter                1400    38.0    40.0   27.3   60.0    58.0   48.0
       Train on gold           350     38.0    11.3   13.3   60.0    34.0   39.3




4.5   Anatomy of the Decline
This subsection is post hoc and descriptive. Sample accuracy mixes whether a
ﬁnished solution is right with whether the model ﬁnishes within the 512-token
cap. Re-tokenising the saved text, we call a generation cap-hit at ≥ 508 tokens.
At the rates where the share does not rise, 40–46% of round-2 MATH-500 gener-
ations already hit the cap (Table 1), so the cap binds from the start. At 5×10−4 ,
compared with the untrained model on the same problem mix, ﬁnished gener-
ations lose 1.5–9.0 points, with intervals excluding zero in two of six runs (A
and no-ﬁlter at seed 1; the six include two same-seed A/B pairs, which are close
to replicates), while the cap-hit share rises 2–14 points. The matched measure
conditions on which problems ﬁnish after training, so it is descriptive. A three-
part decomposition attributes 12–30% of the decline to the cap share in the
10      D.-H. Vu et al.

three original seed-1 runs (and −2 and 5% in two further runs) and 52–72% at
seed 2 (Table S9, Supplementary Appendix H). At 10−4 and 2×10−4 the cap-hit
share does not rise; the decline sits in ﬁnished accuracy, though matched ﬁnished
changes are small and their intervals include zero. Train-on-gold is diﬀerent: re-
sponses shorten by more than half and ﬁnished accuracy collapses. Retraining
without truncated examples, or re-scoring at a 1,536-token cap, leaves the deﬁcit
in place (Supplementary Appendix H).

4.6   A Final Round with a Revised Recipe
Because no earlier arm improved, we ran one last round with several recipe
changes made at once, aimed at the suspected causes (no ablation of any single
one): loss on the completion only, LoRA on all linear layers, a 1,024-token cap
and training limit, normalised gold answers, and a pool of 300 problems from the
MATH training split, so that the exam is all 500 MATH-500 problems. It is 10−4
with k = 2 and a single adapter (round 0 to round 1); the loop has three seeds,
each gate one. The pool comes from the PRM800K training split [21], which is
the complement of MATH-500 within MATH, so it is disjoint by construction
(no content-level overlap check). The veriﬁer-ﬁltered loop (298 examples kept) is
compared with two positive gates: training on the 300 reference solutions, and on
full solutions from Qwen2.5-7B-Instruct (4 samples per problem at temperature
0.8, cap 1,024; one sample accepted by both V ′ and the string match is kept,
teacher_gen.py). Teacher sample accuracy is 73.7% and 70.8% at seeds 1 and
2, and 237 and 228 of the 300 problems have an accepted solution, so these arms’
doses are 20% and 23% below the loop’s.


Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4 ). Change from
each run’s own untrained round 0 to round 1 in points (round-0 pass@1 is 49.2, 46.8,
48.2 at seeds 1–3, from sampling), with 95% paired problem-level bootstrap intervals
that omit training-seed variance. The gold arm has one seed, each teacher arm one.

Arm                        pass@1               pass@2            Sample acc.
Untrained (seed 1)           49.2                 59.4                  –
Loop, seed 1          −4.8 [−9.0, −0.6]    −3.0 [−6.8, +0.8]    −2.9 [−5.8, −0.1]
Loop, seed 2          −3.2 [−7.0, +0.6]    −6.2 [−10.0, −2.6]   −5.3 [−8.1, −2.4]
Loop, seed 3          −4.2 [−8.4, +0.0]    −5.6 [−9.4, −1.8]    −5.4 [−8.3, −2.5]
Loop, mean of seeds         −4.1                 −4.9                 −4.5
Train on gold        −32.2 [−37.0, −27.6] −32.0 [−36.6, −27.4] −30.2 [−33.8, −26.6]
Teacher (237), seed 1 +0.2 [−4.0, +4.6]    −0.8 [−4.6, +2.8]    −0.2 [−3.2, +2.7]
Teacher (228), seed 2 +3.2 [−0.8, +7.0]    −1.6 [−5.0, +1.8]    +0.2 [−2.5, +2.8]


    The reference-solution gate fails: pass@1 falls from 49.2% to 17.0% and the
model adopts the reference style ($-delimited spans in 60 of 1,600 generations
at round 0, 1,577 at round 1); a rerun at 2 × 10−5 fails the same way (20.6%).
It is not mainly a format defect (not fully excluded): the \boxed share is un-
changed (90.6 → 90.3%), accuracy among boxed answers falls 48.5 → 17.1%
                                               Mathematics or the Veriﬁer?      11

and the median length drops 3.2× (1,332 → 414 characters; string-match grader;
gate_anatomy.py). The model plausibly imitates terse references and drops rea-
soning steps (not tested); the loop seeds diﬀer (length 1,332–1,348 → 1,454–1,491
characters, boxed share −0.6, −0.6, −5.1, accuracy among boxed answers −2.5,
−5.7, −3.4), so their decline is not this eﬀect. The teacher gate does not fail
in either seed: pass@1 goes 49.2 → 49.4% and 46.8 → 50.0%, the \boxed share
90.6 → 94.3% and 91.5 → 92.6%, accuracy among boxed answers 48.5 → 47.1%
and 49.8 → 49.2%, the median length 1,332 → 1,279 and 1,338 → 1,304 charac-
ters. The same pipeline thus trains without harm on full solutions, and the loop
ends 5.0 and 6.4 points of pass@1 below it ([+0.8, +9.2], [+2.2, +10.6]; paired,
same exam). A pipeline defect alone is therefore a less likely cause of the loop’s
decline, but these are two seeds, smaller doses and a same-family teacher; it
separates neither self-training nor the veriﬁer and is a no-collapse control, not a
gain control. The veriﬁer-ﬁltered loop loses pass@1 in all three seeds (4.8, 3.2,
4.2 points; one interval excludes zero and one reaches it) and sample accuracy
in all three (all intervals exclude zero). The three-seed mean change is −4.1 (t
interval [−6.1, −2.1]) for pass@1 and −4.5 ([−8.0, −1.0]) for sample accuracy.
With three seeds, one exam draw and one rate we do not claim that the loop
costs accuracy or isolate the cause; the detectable eﬀect is about 6 points of
pass@1.
    Injected bias. As intended positive controls for the audit (neither turns out
to be one) we reran the loop once each (seed 1, 10−4 ) with a selection veriﬁer
that rejects \boxed answers (exam veriﬁer clean). In the ﬁrst, a hash-chosen
30% of problems are aﬀected: the \boxed share falls 4.9 points on them and 3.1
on the others (diﬀerence −1.8, [−7.4, 3.8]); a hash cannot be learned from the
problem, so this control could not elicit selective avoidance. In the second the
rule is visible: every \boxed answer is rejected when the gold contains \frac (49
of the 300 selection problems, 263 examples kept instead of 298; 70 of the 500
exam problems, where the shares are measured). The share on those problems
stays at 95.0% and on the others goes from 90.2% to 87.4% (diﬀerence +2.8,
[−2.8, +8.3]); pass@1 falls 7.0 points ([−11.2, −3.0]), more than in the unbiased
seeds, which we do not interpret (one run). In neither run does the \boxed share
fall selectively where boxing is penalised, so neither validates the audit.


5     Discussion
5.1   Answer to the Research Question
Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k with an interval excluding zero, at any rate; in the 500-problem ﬁnal
round pass@1 falls 3.2–4.8 points in each of three seeds. The sample-accuracy
ﬁgure of about 1.7 points is the largest upper limit among observed intervals, a
post hoc ﬁgure that omits seed variance, not a power statement; on the pre-set
measures the design could detect only about 10 points of pass@1 and 8–10 of
pass@k (6 and 5 in the ﬁnal round). Because no arm improves, and the gate that
does not collapse (teacher solutions, two seeds) does not improve either, the null
12      D.-H. Vu et al.

belongs to this recipe, and the study cannot say whether self-training in general
helps. Every score is graded by V ′ , the selecting veriﬁer of the ﬁnal round, which
the earlier runs did not use (Section 3). On every run a second grader (string
match of the last \boxed against the gold, no math-verify; indep_grade.py)
gives ﬁnal-round pass@1 changes of −3.6, −2.2, −4.6 for the three seeds (−30.0
for the gold arm) and sample-accuracy changes of −2.5, −5.5, −5.3: the same
sign and size. Both graders read only the last \boxed, so a falling boxed share
lowers both, and a format artefact in the gate is not excluded.
    Does it learn to write what the veriﬁer accepts? Undecided: the pre-set pat-
tern requires pass@1 to rise, which never happens detectably (pass@1 changes
are all negative, from −1.3 [−8.7, +6.0] to −12.0), no run varies the frequent
gold-storage defect, and the audit of Section 5.2 is too weak. Whether a pool
shaped by the biased veriﬁer drives the Design P curves is neither supported
nor ruled out: the patch tests a rare bias, and the no-ﬁlter control declines with
more dose.

5.2   A Proposed Audit for GVT with a Biased Veriﬁer
Our pre-set rule could not speak once accuracy fell. From post hoc analyses we
propose four checks for self-training with a rule-based veriﬁer (untested proto-
col).
    (i) A per-round false-reject audit. Fix a repaired veriﬁer V ′ that corrects a
known defect class of the training veriﬁer V . At each round t, on the loop’s own
generations, compute
                          #{accepted by V ′ but rejected by V }
                   rt =                                         .
                                  #{accepted by V ′ }
If the model learns to write what V accepts, rt may fall over rounds, but it also
falls when fewer answers are boxed: since V ′ diﬀers from V only on boxed predic-
tions, rt = rtboxed × (boxed share among V ′ -accepted) holds as an identity. This
is the per-step tracking of RLVR studies [4,16] applied to oﬄine SFT (Table 5;
rt_audit.py). For the gold-storage defect it falls in all three self-training runs
we re-scored, by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching
zero. The fall is accounted for by the falling \boxed share among correct answers
(91 → 76% and 93 → 78% at 5 × 10−4 ): an identity, not a test, so adaptation
is not excluded. The defect is bound to the problem: it ﬁres on 54–62 problems,
rejecting 94–98% of correct answers, and 29–34 of them have an unparseable
gold. On the 24–28 aﬀected problems where some form could, rt moves by −5.5,
−1.6 and −0.2 points (intervals 10–26 wide), and the pool holds only 2–12 such
examples per round, so we expect weak pressure to adapt (untested). The two
injected-bias runs (Section 4.6) show no selective avoidance, but cannot tell us
whether the audit would detect it. Train-on-gold, with no veriﬁer in the loop,
gives rt rises of 2.1–3.3 points (Table 5), with intervals that include zero, so the
observed falls are not distinguishable from drift. It should be reported on the
answers and problems where V and V ′ can diﬀer, with the count of training
examples that could teach avoidance.
                                                      Mathematics or the Veriﬁer?         13

Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all
500 problems, selection problems included), round 0 → last round, with the change
and a 95% problem-level bootstrap interval (2,000 resamples). “Boxed only” restricts
to predictions containing \boxed; “aﬀected, parseable” to problems where the defect
ever ﬁres and V can parse the gold. Pool: examples per round from aﬀected problems
that V accepts.

    Run                  rt subset              R0 Last          ∆ 95% interval Pool
                −4
    A, 5 × 10    , seed 1 all                  18.3     15.7   −2.6    [−5.3, 0.3] 3–5
                          boxed only           20.0     20.7   +0.7    [−2.9, 4.3]
                          aﬀected, parseable   92.8     87.2   −5.5   [−20.1, 6.3]
    A, 5 × 10−4 , seed 2 all                   18.1     15.5   −2.6    [−5.2, 0.1] 2–3
                          boxed only           19.4     19.8   +0.4    [−2.8, 3.4]
                          aﬀected, parseable   95.1     93.5   −1.6   [−14.7, 9.5]
    A, 10−5 , seed 0      all                  18.3     16.8   −1.5    [−2.9, 0.0] 9–12
                          boxed only           19.9     19.5   −0.4    [−2.0, 1.2]
                          aﬀected, parseable   92.3     92.0   −0.2    [−4.9, 4.6]
    Gold, seed 1          all                  18.2     21.5   +3.3    [−1.2, 8.1] —
                          boxed only           20.0     22.8   +2.8    [−2.0, 7.7]
                          aﬀected, parseable   95.5     94.7   −0.7    [−9.1, 6.2]
    Gold, seed 2          all                  18.0     20.2   +2.1    [−2.2, 6.7] —
                          boxed only           19.4     21.1   +1.7    [−3.3, 6.5]
                          aﬀected, parseable   95.1     97.6   +2.5   [−4.8, 11.9]



    (ii) Decompose declines under a ﬁxed cap. Report the change in sample accu-
racy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Supple-
mentary Appendix H). The split is descriptive: at 5×10−4 the cap share accounts
for 12–30% of the decline in the three seed-1 runs and 52–72% at seed 2.
    (iii) Check the dose of a control ﬁrst (our \dfrac patch changed 0–4 exam-
ples) and (iv) match dose across designs.


6    Limitations

Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem
draw and sampling, not training-seed variance; the ﬁnal-round loop has three
seeds, the gold gate and the bias controls one, the teacher gate two, and there
is no multiplicity correction. The learning-rate grid is coarse and changes k,
rounds and dose with the rate. Power is limited (about 10 points of pass@1
with 150 exam problems, about 6 in Section 4.6), and the adaptation audit is
weak (24–28 problems, no positive control that raises accuracy). The veriﬁer
audit used other models’ solutions and inspected only rejections; the gold-storage
defect ran unvaried through every earlier run, whose numbers are graded by V ′ ,
which is not independent of the selecting veriﬁer, and the string-match grader
14      D.-H. Vu et al.

shares the \boxed dependence. The ﬁnal-round decline and the reference-solution
gate failure cannot be attributed to one recipe change. Truncation: the 512-
token cap binds from the start (a quarter of the pool is cut). Scope: one model
family and size, all instruction-tuned, one veriﬁer, a restart-from-base design (no
continued training), unquantiﬁed Qwen2.5 contamination on MATH/GSM8K,
and a default repetition penalty (1.1).


7    Conclusion
The design detected no pass@1 or pass@k gain at any rate (it could see only gains
of about 10 and 8–10 points; 6 in a ﬁnal 500-problem round, where pass@1 falls
3.2–4.8 points in all three seeds). Training on reference solutions lowers pass@1
by about 30 points, whereas veriﬁed full teacher solutions leave it unchanged
(+0.2, +3.2 in two seeds) while the loop loses 4.8 and 3.2; no arm raises accuracy,
so this is a null for this recipe and says little about self-training; since scores are
graded by a veriﬁer of the selecting family (and a string-match check that shares
the \boxed dependence), neither branch of the question is answered. The post
hoc false-reject audit is uninformative about adaptation: its fall is tied to the
falling \boxed share by an identity.
    Next come a dose-matched control for the gold-storage defect, a gate that
raises accuracy, and a second grader (Supplementary Appendix K).

Disclosure of Interests. The authors have no competing interests. This undergrad-
uate research project received no external funding.

Code availability Code, saved generations and analysis scripts are at https://github.
com/tsan2711/DACNTT_2026 (tag paper-2026-11b). Generation-time token counts,
Design P’s training logs and the 1,536-token re-scoring outputs were not saved.

Use of AI tools The authors used Claude (Anthropic) to help write the manuscript
and the analysis and training scripts, and to run automated reviews. The authors
designed the study, ran the experiments and take responsibility for the content.


References
 1. Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., Sugiyama, M.: Reinforce-
    ment Learning with Veriﬁable yet Noisy Rewards under Imperfect Veriﬁers.
    arXiv:2510.00915 (2025)
 2. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,
    M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training Veriﬁers
    to Solve Math Word Problems. arXiv:2110.14168 (2021)
 3. Dang, Q.-A., Ngo, C.: Reinforcement Learning for Reasoning in Small LLMs: What
    Works and What Doesn’t. arXiv:2503.16219 (2025)
 4. Egashira, K., Vero, M., Dekoninck, J., Dörner, F.E., Staab, R., Vechev, M.: Delay,
    Plateau, or Collapse: Evaluating the Impact of Systematic Veriﬁcation Error on
    RLVR. arXiv:2605.02909 (2026)
                                                  Mathematics or the Veriﬁer?        15

 5. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song,
    D., Steinhardt, J.: Measuring Mathematical Problem Solving With the MATH
    Dataset. arXiv:2103.03874 (2021)
 6. Huang, Y., Zeng, W., Zeng, X., Zhu, Q., He, J.: From Accuracy to Robust-
    ness: A Study of Rule- and Model-based Veriﬁers in Mathematical Reasoning.
    arXiv:2505.22203 (2025)
 7. Kim, J., Luo, X., Kim, M., Lee, S., Kim, D., Jeon, J., Li, D., Yang, Y.: Why
    Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
    arXiv:2603.24472 (2026)
 8. Qiao, X., Du, X., Liu, W., Zhang, J., Mai, P., Zhang, M., Pang, Y.: When Sample
    Selection Bias Precipitates Model Collapse. arXiv:2606.13732 (2026)
 9. Shao, R., Li, S.S., Xin, R., Geng, S., Wang, Y., Oh, S., Du, S.S., Lambert, N., Min,
    S., Krishna, R., Tsvetkov, Y., Hajishirzi, H., Koh, P.W., Zettlemoyer, L.: Spurious
    Rewards: Rethinking Training Signals in RLVR. arXiv:2506.10947 (2025)
10. Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., Gal, Y.: AI
    models collapse when trained on recursively generated data. Nature (2024). https:
    //doi.org/10.1038/s41586-024-07566-y
11. Singh, A., Co-Reyes, J.D., Agarwal, R., et al.: Beyond Human Data: Scaling Self-
    Training for Problem-Solving with Language Models. arXiv:2312.06585 (2023)
12. Gulcehre, C., Le Paine, T., Srinivasan, S., et al.: Reinforced Self-Training (ReST)
    for Language Modeling. arXiv:2308.08998 (2023)
13. Strozzi, I.L.: Teacher-Free Self-Training Ampliﬁes but Does Not Compound: A
    Pass@k Crossover on a Free-Veriﬁer Domain. arXiv:2606.07856 (2026)
14. Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B., Cheng, H., He, X., Wang,
    K., Gao, J., Chen, W., Wang, S., Du, S.S., Shen, Y.: Reinforcement Learning for
    Reasoning in Large Language Models with One Training Example. In: NeurIPS
    (2025). arXiv:2504.20571
15. Xu, C., Yan, N., Chen, L., Kechadi, M.-T.: Phantom Gains: Auditing Self-
    Improvement Against a Measured Null. arXiv:2608.20290 (2026)
16. Xu, Z., Li, Y., Jiang, F., Ramasubramanian, B., Niu, L., Lin, B., Poovendran, R.:
    TinyV: Reducing False Negatives in Veriﬁcation Improves RL for LLM Reasoning.
    arXiv:2505.14625 (2025)
17. Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou, C., Zhou, J.: Scaling
    Relationship on Learning Mathematical Reasoning with Large Language Models.
    arXiv:2308.01825 (2023)
18. Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song, S., Huang, G.: Does
    Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond
    the Base Model? arXiv:2504.13837 (2025)
19. Zelikman, E., Wu, Y., Mu, J., Goodman, N.D.: STaR: Bootstrapping Reasoning
    With Reasoning. arXiv:2203.14465 (2022)
20. Zeng, W., Huang, Y., Liu, Q., Liu, W., He, K., Ma, Z., He, J.: SimpleRL-Zoo:
    Investigating and Taming Zero Reinforcement Learning for Open Base Models in
    the Wild. arXiv:2503.18892 (2025)
21. Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J.,
    Schulman, J., Sutskever, I., Cobbe, K.: Let’s Verify Step by Step. In: ICLR (2024).
    arXiv:2305.20050
