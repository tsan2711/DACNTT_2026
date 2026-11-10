3.4   Models, Data, Training, Metrics
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
150 exam problems), which respects the clustering of the k samples within a
problem. These intervals do not cover training-seed variance, which we see only
across two or three seeds: the one same-conﬁguration replicate pair we have
ends 3.2 points of sample accuracy apart. We make no multiplicity correction,
so we rest conclusions on patterns across runs and seeds, not on single intervals.
Single proportions use Wilson intervals. Detectable eﬀects. From the interval
                                              Mathematics or the Veriﬁer?      7

half-widths h in Table 2, a change would be detected with 80% power at the
5% level only if it exceeded about 2.8 h/1.96: about 10 points of pass@1, 8–10
of pass@k and 3.5–5.5 of sample accuracy on MATH-500. A null in this paper
means no gain of roughly that size. Details are in Supplementary Appendix ??.

Reproducibility. The analysis scripts named in the paper and the saved gener-
ations of every run are in our project repository. Token counts at generation
time, Design P’s training logs and the per-sample outputs of the 1,536-token re-
scorings were not saved. Every accuracy number in the paper is graded by the
same biased veriﬁer that selects the training data, except the re-scored ﬁgures
of Supplementary Appendix ??.


4     Results

4.1   Design P: An Apparent Collapse

In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 50.0% → 18.6%, pass@8 72.6% → 48.6%; Table ??, Supplementary
Appendix ??), on both datasets (Table ??); the 0.5B decline is small. The ac-
cepted pool contracts every round and \boxed{} falls from 5,608 to 2,693 of
8,000 generations. This design cannot be read causally: one adapter trains on
both datasets’ pools; it scores on the problems it selects from; and it trains on
about 4.5× as many examples per round as the isolated MATH-500 run (3,962
against 872 at round 0). No run separates these explanations (Supplementary
Appendix ??).


4.2   Design I at 10−5 : Small Declines, a Larger One on GSM8K

On the held-out exam (Fig. ?? and Table ?? in Supplementary Appendix ??)
pass@8 ends within 4 points of round 0 in every run. On MATH-500, pass@1
is 2.7–4.0 points lower at round 4, with every interval including zero (Table 2);
sample accuracy falls 1.2–3.2 points, with an interval excluding zero only for
B at seed 0 (A at seed 0 reaches 0.0), and matched ﬁnished accuracy 1.1–4.2,
with intervals that only just exclude zero for A and B at seed 0, which are close
to one replicate. We read this as a possible small decline, not an established
one; what we do not see is a gain of the size the design could detect. Run C
(GSM8K) declines more: pass@1 falls 12.7 points ([−21.3, −4.0]), almost all in
ﬁnished accuracy, but it took about twice Run A’s optimizer steps, so we do not
attribute this to the dataset alone. At this rate the training loss falls, but on
MATH-500 two coarse output statistics, length and cap-hit share, barely change;
we did not measure a ﬁner one, so this is weak evidence that the adapter did
little, and a ﬂat curve there does not show that GVT is stable (Supplementary
Appendix ??).
8      T. S. Nguyen and D. A. Tran

4.3   The Patch Control Could Not Detect an Eﬀect

Runs A and B diﬀer only in the \dfrac/\tfrac patch. At round 4, B minus A
is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and +0.0 [−2.7, +2.7] at seed 1.
This null is uninformative: \dfrac appears in 0.50–0.73% of generations, so the
kept pools diﬀer by 3–4 examples (under 0.5%), and at 10−5 the adapter changes
the outputs little anyway. Removing one rare format defect had no detectable
eﬀect, which a prevalence count alone predicts; the frequent gold-storage defect
is present in both arms. The pre-ﬁlter share of problems on which all k samples
agree falls in each of the four runs where we measured it (Design P 1.5B and the
seed-0 10−5 runs, over all 500 items), but it is mechanically tied to accuracy, so
we draw no conclusion from it (Supplementary Appendix ??).


4.4   Higher Learning Rates

Because 10−5 changed the MATH-500 outputs little, we reran Run A at 10−4
(three seeds), 2 × 10−4 (two) and 5 × 10−4 (two, with Run B), with three rounds
and k = 4 (Table 1). These runs therefore diﬀer from the 10−5 runs in k, round
count, pool size (and so optimizer steps) and the pass@k metric as well as in
rate, so only the comparison among 10−4 , 2 × 10−4 and 5 × 10−4 isolates the
rate. At 5×10−4 every run declines: pass@1 falls 4.0–11.3 points and the sample-
accuracy intervals exclude zero in all four A/B runs, though same-seed A and
B are closer to two replicates than four. The decline may grow with the rate
on one seed: at seed 1 sample accuracy falls 1.5, 3.5 and 8.3 points across the
three rates, at seed 2 an almost ﬂat 3.7, 3.8 and 4.7. The cap-hit share rises
only at 5 × 10−4 . The patch has no consistent eﬀect: B minus A in round-2
pass@1 is +5.3 at seed 1 and −7.3 [−14.0, −0.7] at seed 2, a sign ﬂip from pools
that diﬀer by 0–3 examples, which illustrates trajectory noise. Style does not
separate imitation from drift: ﬁnished exam generations start more boxed than
the veriﬁer-accepted pool and fall below it as the pool falls too, which imitation
of the pool and drift would both produce.