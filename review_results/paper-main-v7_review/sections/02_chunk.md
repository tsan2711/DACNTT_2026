

to a quarter (440 → 542, +23%; selection problems only, so its 18.8% rejected
share diﬀers from the 15.5–18.3% over all 500), against 0–4 examples for the
\dfrac patch, and it lowers absolute pass@1 by 4.7–8.0 points in self-training.
It is bound to the problem, not to the answer: on the 54–62 problems where
it ever ﬁres, it rejects 94–98% of correct answers in every round, and 29–34 of
these problems have a gold the original veriﬁer cannot parse at all, so no answer
form avoids it there. Every table grades all runs with V ′ , which the loop used
only in the ﬁnal round, so round-0 values are higher than in the original run logs
(pass@1 40.0 against 33.3 for Run A at seed 1), and the declines remain. Timeouts of math-verify, which version 0.9.0 reports only as a log message, were
detected and retried at 60 s. Supplementary Appendix B gives the full analysis.
3.3

Two Experimental Designs

Design P (pooled) loads both datasets (500 problems each) together and trains
one adapter per round on the union of accepted solutions, with selection and
evaluation on the same 1,000 problems. Design I (isolated) uses one dataset and
one adapter per run, and holds out 30% of the 500 problems (150) as an exam
set; generation runs on all 500 problems each round, but only the other 350 can
enter the training pool, and all Design I pass rates are on the exam set. Table S1
summarises them.
Design I has three runs, all Qwen2.5-1.5B-Instruct, ﬁve rounds, k = 8, diﬀering in one respect each: Run A (MATH-500, original veriﬁer), Run B (MATH500, patched veriﬁer) and Run C (GSM8K, original veriﬁer). Runs A and B were
repeated at a second seed. A “seed” sets the exam partition, the selection set and
the training randomness at once, so a repetition draws a diﬀerent 150-problem
exam set. Most of the later evidence comes from higher-rate runs (Section 4.4;
Table S4 in Supplementary Appendix E lists every run). “Five rounds” means
round 0 (the untrained model) and four adapters; “three rounds” means round 0
and two adapters, so the round-2 model is a single adapter (about 195 optimizer
steps for Run A at 5 × 10−4 ) trained on the round-1 pool.
3.4

Models, Data, Training, Metrics

We use Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct (Design P uses both,
Design I the 1.5B model only) and the ﬁrst 500 problems of the GSM8K test
split [2] and MATH-500, the 500-problem subset of MATH [5]. The prompt is a
single user turn: “Solve the math problem. Put the ﬁnal answer in \boxed{}.”
followed by the problem. Generation samples at temperature 0.8 with a cap of
512 new tokens; the other decoding settings come from the checkpoint’s generation conﬁguration (top-p 0.8, top-k 20, repetition penalty 1.1). Training is
LoRA SFT (transformers 5.0.0, peft 0.19.1, TRL 1.10.0 SFTTrainer; rank 16,
α = 32, on q_proj and v_proj, LoRA dropout 0, weight decay 0, gradient clipping 1.0 and trainer seed 42, all library defaults read from the pinned sources;
batch size 2, no accumulation; one epoch; AdamW with linear learning-rate decay and no warmup; loss over the whole chat sequence, prompt included; fp16 on

6

D.-H. Vu et al.

one Kaggle T4), with a training sequence limit of 512 tokens that includes the
prompt. Because this limit equals the generation cap but also holds the prompt,
any kept solution longer than about 512 tokens minus the prompt length is cut
in training and loses its ﬁnal answer and end-of-sequence token (24–26% of the
round-0 pool; Section 4.5). All kept solutions are used, so the number of optimizer steps per round is half the pool size. The learning rate is 10−5 unless
stated otherwise; this value was our code’s default and was not tuned. Metrics
per round, on the exam set: pass@1 is the correctness of the ﬁrst of the k samples
(one draw per problem, so it carries sampling noise); pass@k; sample accuracy,
the mean over all k samples; style counts over all generations (boxed, dfrac, dollar, . . . ); and per-problem added/lost counts between consecutive rounds, where
a problem is solved in a round if at least one of its k samples is accepted. Added
minus lost therefore equals 150 × ∆pass@k: the counts show gross churn, not an
independent test. pass@1 was ﬁxed in advance; sample accuracy was not, but it
estimates the same quantity from all k samples with less variance, so after the
runs we chose it as the primary accuracy measure (claims resting on it, including
the 2.2-point bound, are post hoc in the choice of measure). “Correct” always
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

4

Results

4.1