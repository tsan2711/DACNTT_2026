## C Uncertainty in Full
Uncertainty. For every within-run change (round 0 against the last round)
and every paired comparison of two runs on the same exam partition we re-
port a 95% interval from a paired problem-level bootstrap: we resample the
150 exam problems with replacement (10,000 times), recompute the statistic
for both rounds or runs on the same resampled problems, and take the 2.5th
and 97.5th percentiles. Resampling problems rather than samples respects the
clustering of the k samples within a problem. The per-sample correctness was
recomputed from the saved generations with the same verifier; it reproduces
the reported pass rates except for six round values that differ by one prob-
lem (0.6–0.7 points), most likely because of math-verify comparison timeouts
(experiments/viec3/bootstrap_ci.py). The post hoc measures of Section H
(Table 11, the matched column of Table 5 and the decomposition) use a sep-
arate re-scoring of the same generations (review_cpu/scored/), which differs
from the values behind Tables 4 and 5 by up to one problem in some further
rounds (e.g. 10−4, seed 1, round 2: pass@1 33.3 against 34.0%); no conclusion de-
pends on these differences. These intervals cover the choice of problems and the
sampling of generations for a given trained adapter; they do not cover training-
seed variance, which we can only see informally across our two or three seeds, so
they understate the uncertainty of run-level conclusions. Our own data suggest
by how much: a replicate of Run A at 5 × 10−4, seed 1, with the same configu-
ration, ends 3.2 points of sample accuracy away from the original (Section H);
and at seed 2 Runs A and B, whose round-0 training pools are identical (424
examples each), end 7.3 points apart in round-2 pass@1 (interval [−14.0, −0.7],
Section G), though that is a single interval near zero. A single interval that ex-
cludes zero is therefore not suﬃcient evidence of a reproducible effect, and one
that includes zero does not rule an effect out. We also make no correction for
multiplicity: Table 5 alone holds 76 intervals and the text about ten more, and
at the 95% level about four of the 76 would exclude zero by chance if nothing
changed (fewer or more, since they are not independent), so we rest conclusions
on patterns across runs and seeds, not on any single interval. Single proportions
use Wilson intervals.

Mathematics or the Verifier?
21
Table 8. The two designs. They differ in more than the intended variables; the most
quantifiable unintended difference is the training dose per round (about 4.5× as many
optimizer steps in Design P).
Design P (pooled)
Design I (isolated)
Datasets per run
GSM8K + MATH-500 one only
Adapter
one, shared
one per dataset
Training mixture
≈69% GSM8K
single-domain
Evaluation items
same as selection
held-out 30%
Training examples, round 0 (1.5B) 3,962
872 (A), 1,901 (C)
Verifier control
none
Run B (patched)
Models
0.5B and 1.5B
1.5B
Table 9. Design P, 1.5B, split by dataset, recomputed from the saved generations
(preset reward, the one used for selection; the default preset differs only at MATH-
500 round-3 pass@8, 45.0%). Pooled, the recomputed round-3 pass@8 is 63.5% (reward)
and 63.6% (default), against 63.6% in Table 2.
Dataset
Metric
R0
R1
R2
R3
R4
∆
GSM8K
pass@1 69.6% 62.0% 61.0% 45.6% 26.6% −43.0 pt
GSM8K
pass@8 91.4% 90.4% 89.0% 82.2% 65.8% −25.6 pt
MATH-500 pass@1 30.4% 30.4% 28.0% 19.2% 10.6% −19.8 pt
MATH-500 pass@8 53.8% 52.6% 51.4% 44.8% 31.4% −22.4 pt