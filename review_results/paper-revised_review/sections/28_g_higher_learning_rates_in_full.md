## G Higher Learning Rates in Full
Because 10−5 changed the MATH-500 outputs little, we reran the MATH-500
runs at higher rates with a smaller budget (three rounds, k = 4, so pass@4
replaces pass@8 and the pools are about half as large): Runs A and B at 5×10−4
at two seeds, and Run A at 10−4 at three seeds and at 2 × 10−4 at two. Seed 1
shares the exam partition of the seed-1 runs above and seeds 2 and 3 draw new

Mathematics or the Verifier?
25
Table 10. Runs A and B at 5×10−4 (MATH-500, k = 4, three rounds), held-out exam
set of 150 problems. B differs from A only in the verifier patch; each seed draws its
own exam partition. “Kept pool” is the number of training examples (= 2× optimizer
steps). “Boxed” is the share of the 2,000 generations in each round containing \boxed.
Run, seed
Round
pass@1
pass@4
Kept pool
Boxed
A (orig.), 1
0
33.3%
50.0%
440
52%
1
32.7%
49.3%
391
51%
2
23.3%
42.7%
326
36%
B (patched), 1
0
33.3%
50.7%
443
52%
1
35.3%
50.0%
392
49%
2
28.7%
48.7%
328
41%
A (orig.), 2
0
31.3%
51.3%
424
54%
1
31.3%
46.0%
386
50%
2
27.3%
44.7%
350
37%
B (patched), 2
0
31.3%
52.0%
424
54%
1
31.3%
44.7%
398
50%
2
20.0%
40.7%
332
38%
ones. These runs are not directly comparable with the k = 8, five-round runs in
metric or training dose. Within round 0 the loss falls from about 0.5 to 0.25 at
5 × 10−4 and from about 0.6 to 0.28 at 10−4 over about 220 steps.
At 5 × 10−4 every run declines, with wide intervals. By round 2 pass@1 has
fallen 10.0 and 4.0 points (A) and 4.7 and 11.3 points (B), and pass@4 7.3, 6.7,
2.0 and 11.3 points (Table 10). The bootstrap intervals (Table 5) exclude zero for
two of the four pass@1 changes and one (two more reach zero at their upper end)
of the four pass@4 changes, and for the sample accuracy of all four. A and B at
the same seed share the partition, the round-0 generations and almost the whole
first pool, so the four runs are closer to two independent replicates than four. We
read this as a consistent but imprecisely measured decline. The style shift does
not separate imitation from drift. The verifier-accepted pool is 89–91% \boxed
at round 0, far more than all generations (52–54%, Table 10), because unfinished
generations are rarely boxed and rarely accepted. But the right comparison is
with finished generations, and these start more boxed than the pool (95.6% and
98.5% on the exam at seeds 1 and 2; the pool also holds truncated and cap-hit
examples that lose their final \boxed). Among finished exam generations the
share falls to 69.7% (A, seed 1) and 82.9% (A, seed 2), from above the round-0
pool to below it, while the pool, drawn from these generations, falls too (73–77%
by round 2). A model imitating its less-boxed training data would move the same
way, so this share cannot separate imitation of the pool from drift.
The decline may depend on the learning rate, on the evidence of one seed.
Only seeds 1 and 2 were run at all three higher rates. At seed 1, sample accuracy
at round 2 falls by 1.5, 3.5 and 8.3 points at 10−4, 2 × 10−4 and 5 × 10−4; at
seed 2 by 3.7, 3.8 and 4.7, which is almost flat (Table 5; seed 3, run only at 10−4,
gives −1.0). The seed-1 series is monotone, the seed-2 series barely so, and at

26
T. S. Nguyen and D. A. Tran
10−4 and 2×10−4 the individual changes are about the size of re-sampling noise,
so the rate dependence is suggestive, not established. The share of generations
that hit the token cap does not follow the rate: it is flat or falls at 10−4 and
2 × 10−4 and rises only at 5 × 10−4 (Table 4).
The patch has no consistent effect. At round 2, B minus A is +5.3 [−2.0,
+12.0] points of pass@1 at seed 1 and −7.3 [−14.0, −0.7] at seed 2. The sign
flips with the seed, and the seed-2 interval excludes zero although the patch
changes the first training pool by 0–3 examples. Same-seed runs that start from
almost the same pool can thus end several points apart once the adapter moves
(their later pools differ by 1–18 examples as the trajectories separate). This is
one pass@1 interval whose upper end only just clears zero, so on its own it is
weak evidence of trajectory noise; the replicate of Run A at seed 1 (Section H),
which ends 3.2 points of sample accuracy and 4.1 points of matched finished
accuracy away from the original, points the same way.
Two controls at 5 × 10−4. The no-filter run trains on all k samples of every
selection problem regardless of correctness (1,400 examples per round), removing
the verifier from the loop. The train-on-gold run ignores the model’s generations
and trains on the 350 reference solutions, identical every round. Both were run
at two seeds, on the partitions of Run A at the same seeds. Neither is a single-
variable control: per round, no-filter takes 700 optimizer steps and train-on-gold
175, against 220, 196 and 163 for Run A at seed 1 (and 212, 193, 175 at seed 2).
Train-on-gold is thus close to Run A in optimizer steps, so its comparison is
mainly one of data; no-filter takes 3–4× as many steps, and since dose may
matter (the rate dependence above is suggestive), dose and data differ at once
in that comparison.
Removing the filter is never better than keeping it on any measure beyond
noise, and is worse on pass@4 at both seeds, but the dose difference means
this cannot be attributed to the filter. At round 2, no-filter minus Run A is +4.0
[−2.7, +10.7] (seed 1) and −4.7 [−12.0, +2.7] (seed 2) points of pass@1, of mixed
sign, and −2.0 [−8.7, +4.7] and −5.3 [−12.0, +1.3] points of pass@4, negative at
both seeds, so pass@4 weakly favours keeping the filter; for sample accuracy the
difference is +0.2 [−3.3, +3.7] at seed 1 and −5.5 [−9.2, −1.8] at seed 2, so one
single-seed interval excludes zero, in favour of the filter, and the other is centred
on zero. The verifier gate keeps 30–31% of the samples at round 0 and 23–25% by
round 2. With two seeds, a 3–4× larger training dose for no-filter, and intervals of
this width, we can only say that effects of a few points in either direction are not
excluded. Training on reference solutions is followed by a much larger decline:
pass@1 falls to 18.0% and 15.3% (seed 1) and 8.7% and 10.0% (seed 2), and
pass@4 by about 21 points by round 2 at both seeds ([−29.3, −12.7] at worst),
while the model adopts the reference style (generations with a $-delimited span
go from 5% to 98%, with \boxed from 52% to 86%). That accuracy is graded by
the same verifier after a large format shift, so part of this drop could be verifier
error. We checked this in two ways after the runs (post hoc). First, among the
round-2 answers the verifier rejects, those whose final \boxed content equals the
stored gold string after light normalisation are 14 of 600 generations at seed 1 and

Mathematics or the Verifier?
27
11 of 600 at seed 2; counting them correct would raise round-2 sample accuracy
by about 2 points. This is a lower bound: exact string match misses equivalent
forms, and the about 14% of round-2 generations with no \boxed at all are
not covered. Second, the gold-storage re-score of Section B makes the sample-
accuracy decline larger, not smaller (−24.7 and −22.0 points against −19.7 and
−18.7), because the defect penalises round 0 more; but it repairs one defect and
does not test whether answers in the new style are parsed correctly. Neither
check is a hand audit. Even several times the first bound would be far below a
fall of about 19 points, and finished accuracy falls to 12–15%, so we think the fall
is mostly real, but a format-shift error is not measured. Its rounds are replicate
fine-tunes on identical data (their final training losses agree to three decimals), so
the difference between its rounds 1 and 2 mainly reflects generation sampling. No
verifier-filtered self-training run at this rate shows a pass@k gain; their pass@4
falls by 2.0–11.3 points (no-filter 9.3 and 12.0), whereas train-on-gold falls by
about 21.
Run C at 5 × 10−4. We also reran Run C (GSM8K, seed 1, three rounds, k = 4)
at 5 × 10−4, once. pass@1 falls 70.7% →64.7% →48.7% (interval for the round-
0-to-2 change [−29.3, −15.3]) and pass@4 86.0% →86.0% →76.7%. The cap-hit
share rises from 3.8% to 15.0% and mean length from 958 to 1,313 characters,
and accuracy on the finished generations falls clearly (71.9% →63.3%; −12.1
points matched). In the three-part split of Section H, about half of this run’s
sample-accuracy decline (51%) is in the finished-accuracy part and 43% in the
cap-share part (Table 7), so on GSM8K, in this single run, the loss is both less
accurate solutions and more unfinished ones. This run uses a different partition,
k and round count from the 10−5 Run C, so the two can be compared only
through their within-run changes (−1.3 points of pass@1 by round 2 at 10−5,
−22.0 at 5 × 10−4; the 10−5 run falls further later, to −12.7 by round 4). That
is suggestive of a rate dependence on GSM8K too, from one run per rate.