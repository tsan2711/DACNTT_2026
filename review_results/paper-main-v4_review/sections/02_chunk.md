
Mathematics or the Veriﬁer?
5
below rather than extraction of a wrong token. The audit inspected only rejec-
tions, so it gives no false-positive rate. The veriﬁer also cannot parse 51 of the
500 stored MATH-500 golds (10.2%); these problems always count as unsolved,
and can never enter the training pool. The oﬀset cancels in within-run diﬀerences
only if those problems would not otherwise change, which we did not check, and
not in ratios or levels across partitions (11–18 such problems per exam partition).
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


6
T. S. Nguyen and D. A. Tran
and two adapters, so the round-2 model is a single adapter (about 195 optimizer
steps for Run A at 5×10−4) trained on the round-1 pool. All runs use one model
family, Qwen2.5.
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
1.10.0 SFTTrainer; rank 16, α = 32, on q_proj and v_proj, LoRA dropout and
weight decay at the library defaults; batch size 2; one epoch; AdamW with linear
learning-rate decay and no warmup; loss over the whole chat sequence, prompt
included; fp16 on one Kaggle T4), with a training sequence limit of 512 tokens
that includes the prompt. Because this limit equals the generation cap but also
holds the prompt, any kept solution longer than about 512 tokens minus the
prompt length is cut in training and loses its ﬁnal answer and end-of-sequence
token (24–26% of the round-0 pool; Section 4.5). All kept solutions are used, so
the number of optimizer steps per round is half the pool size. The learning rate
is 10−5 unless stated otherwise; this value was the default of our training code
and was not tuned (Section 4.4). Metrics per round, on the exam set: pass@1
is the correctness of the ﬁrst of the k samples (one draw per problem, so it
carries sampling noise); pass@k; sample accuracy, the mean over all k samples;
style counts over all generations (boxed, dfrac, dollar, . . . ); and per-problem
added/lost counts between consecutive rounds, where a problem is solved in a
round if at least one of its k samples is accepted. Added minus lost therefore
equals 150 × ∆pass@k, so these counts add only the gross churn behind the net
change, not an independent test. pass@1 was ﬁxed in advance; sample accuracy
was not among the pre-set measures, but it estimates the same quantity from
all k samples with less variance, so after the runs we chose it as the primary
accuracy measure. Claims that rest on it, including the 2.2-point bound, are
therefore post hoc in the choice of measure. “Correct” always means accepted
by the veriﬁer (preset reward), the same veriﬁer that selects the training data.
Uncertainty. For every within-run change (round 0 against the last round) and
every paired comparison of two runs on the same exam partition we report a
95% interval from a paired problem-level bootstrap (10,000 resamples of the
150 exam problems; 2,000 for the matched and audit columns), which respects
the clustering of the k samples within a problem. These intervals do not cover
training-seed variance, which we see only across two or three seeds: the one same-
conﬁguration replicate pair we have ends 3.2 points of sample accuracy apart.
We make no multiplicity correction, so we rest conclusions on patterns across