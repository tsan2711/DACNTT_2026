## E Design I at 10−5 in Full
Table 3 reports the isolated runs on their held-out exam sets. pass@8 ends within
4 points of its round-0 value in every run. On MATH-500, pass@1 is 2.7–5.3
points lower at round 1 than at round 0 and roughly flat afterwards, and 2.7–4.0
points lower at round 4; the bootstrap intervals for these round-0-to-round-4
changes are between [−10.7, +2.7] and [−9.3, +4.0], all including zero (Table 5).
With one first-sample draw per problem per round, a step at round 1 cannot be
distinguished from noise around a flat or slightly negative trend, so we claim only
that there is no evidence of compounding on MATH-500 at this rate (Run C,
below, loses most of its pass@1 in its last round), not that the first round has
a one-offcost. The less noisy measures do move: sample accuracy falls by 1.2–
3.2 points in these four runs, with one interval (B, seed 0) excluding zero, and
the (post hoc) matched finished accuracy falls by 1.1–4.2 points, with intervals
excluding zero at seed 0 for both A and B. These seed-0 intervals only just

Mathematics or the Verifier?
23
exclude zero (upper ends −0.6 and 0.0 for sample accuracy, −0.5 and −0.9
matched), A and B at seed 0 share their round-0 generations and almost all of
their first pool, so they are close to one replicate, and at seed 1 nothing excludes
zero. With about four of the 76 intervals in Table 5 expected to exclude zero by
chance, we read this as a possible small decline at this rate, not an established
one; what we do not see is a gain. Run C (GSM8K) declines more: pass@1 falls
12.7 points, 9.3 of them in the final round (63.3% →54.0%; interval for the whole
change [−21.3, −4.0]), and sample accuracy 13.1 points, while pass@8 falls 2.7
points (interval including zero) and the cap-hit share rises only from 3.5% to
4.2%. Finished accuracy falls 12.8 points matched, and the decomposition of
Section H puts 97% of the sample-accuracy decline in finished accuracy, so this
decline is not a termination effect. It is a single run, and it took about twice as
many optimizer steps per round as Run A (951 against 436 at round 0), so we
do not attribute it to the dataset alone.
How much training happened at 10−5. The training loss does fall at this rate:
within round 0 of Run A it goes from 0.72 to 0.38 (seed 0) and from 0.70 to
0.40 (seed 1) over about 420 steps, with an epoch mean of 0.47, against epoch
means of 0.24–0.30 at 10−4–5 × 10−4. The adapter therefore learns, but slowly,
and it changes the outputs little: mean length and the share of generations that
hit the token cap are essentially unchanged from round 0 to round 4 (cap-hit
46.9 →47.4% at seed 0 and 40.7 →41.8% at seed 1 for Run A; Table 11). This
holds for the MATH-500 runs at about 420–436 steps per round; Run C at the
same rate, with about twice the steps, does change its outputs. “Little change”
is therefore a property of rate and steps together, not of the rate alone. A flat
pass@k curve in the MATH-500 runs is evidence that this training step did little,
not evidence that GVT is stable.
Noise. Round 0 is the untrained base model, so round-0 differences between
seeds mostly measure how hard each partition is: round-0 pass@1 is 32.0% at
seed 0 and 36.7% at seed 1, and on the third partition used later round-0 pass@4
is 40.0% against 50.0% and 51.3% on the other two (Table 4). These levels cancel
in within-run changes. Noise in the changes themselves is better seen elsewhere:
re-sampling the same model on the same problems moves pass@1 by up to 6.7
points (Section H), and a single 150-problem pass@1 has a standard error of
about 3.8 points. Agreement across seeds tests partition and training variance
together; training variance alone is seen only in same-partition pairs (A against
B at the same seed, Section G, and the replicate of Section H). We therefore
report the bootstrap intervals above rather than judge differences against one
“noise floor”.