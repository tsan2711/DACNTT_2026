### 3.4 Models, Data, Training, Metrics
We use Qwen2.5-0.5B-Instruct and Qwen2.5-1.5B-Instruct (Design P uses both,
Design I the 1.5B model only) and the first 500 problems of the GSM8K test
split [2] and MATH-500, the 500-problem subset of MATH [5]. The prompt is
a single user turn in the model’s chat template: “Solve the math problem. Put
the final answer in \boxed{}.” followed by the problem. Generation samples at
temperature 0.8 with a cap of 512 new tokens; the other decoding settings come

6
T. S. Nguyen and D. A. Tran
Table 1. All runs (Qwen2.5-1.5B-Instruct unless stated). Design P was run once per
model. “Pool” is the round-0 kept pool (training examples; optimizer steps are half of
it).
Design / run
Data
Rate
k, rounds Seeds
Pool
P (0.5B, 1.5B)
GSM8K+MATH-500 10−5
8, 5
one run each 2,533, 3,962
I: A, B
MATH-500
10−5
8, 5
0, 1
872, 833 (A)
I: C
GSM8K
10−5
8, 5
0
1,901
I: A
MATH-500
10−4
4, 3
1, 2, 3
424–455
I: A
MATH-500
2 × 10−4 4, 3
1, 2
440, 424
I: A, B
MATH-500
5 × 10−4 4, 3
1, 2
440, 424
I: no filter, gold
MATH-500
5 × 10−4 4, 3
1, 2
1,400, 350
I: A replicate, 1024 limit MATH-500
5 × 10−4 4, 3
1
440
I: C
GSM8K
5 × 10−4 4, 3
1
971
from the checkpoint’s generation configuration (top-p 0.8, top-k 20, repetition
penalty 1.1). Training is LoRA SFT (transformers 5.0.0, peft 0.19.1, TRL
1.10.0 SFTTrainer; rank 16, α = 32, on q_proj and v_proj, LoRA dropout and
weight decay at the library defaults; batch size 2; one epoch; AdamW with linear
learning-rate decay and no warmup; loss over the whole chat sequence, prompt
included; fp16 on one Kaggle T4), with a training sequence limit of 512 tokens
that includes the prompt; all kept solutions are used, so the number of optimizer
steps per round is half the pool size. The learning rate is 10−5 unless stated
otherwise; this value was the default of our training code and was not tuned
(Section 4.4). Metrics per round, on the exam set: pass@1 is the correctness
of the first of the k samples (one draw per problem, so it carries sampling
noise); pass@k; sample accuracy, the mean over all k samples; style counts over
all generations (boxed, dfrac, dollar, . . . ); and per-problem added/lost counts
between consecutive rounds, where a problem is solved in a round if at least one
of its k samples is accepted. Added minus lost therefore equals 150×∆pass@k, so
these counts add only the gross churn behind the net change, not an independent
test. pass@1 was fixed in advance; sample accuracy was not among the pre-
set measures, but it estimates the same quantity from all k samples with less
variance, so after the runs we chose it as the primary accuracy measure. Claims
that rest on it, including the 2.2-point bound, are therefore post hoc in the choice
of measure. “Correct” always means accepted by the verifier (preset reward), the
same verifier that selects the training data.
Uncertainty. For every within-run change (round 0 against the last round) and
every paired comparison of two runs on the same exam partition we report a
95% interval from a paired problem-level bootstrap (10,000 resamples of the 150
exam problems), which respects the clustering of the k samples within a problem.
These intervals do not cover training-seed variance, which we see only across two
or three seeds: a same-configuration replicate ends 3.2 points of sample accuracy
away. We make no multiplicity correction, so we rest conclusions on patterns

Mathematics or the Verifier?
7
across runs and seeds, not on single intervals. Single proportions use Wilson
intervals. Details are in Appendix C.