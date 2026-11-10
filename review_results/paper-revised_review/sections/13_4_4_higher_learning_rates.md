### 4.4 Higher Learning Rates
Because 10−5 changed the MATH-500 outputs little, we reran Run A at 10−4
(three seeds), 2×10−4 (two) and 5×10−4 (two, with Run B), with three rounds
and k = 4 (Table 4). At 5×10−4 every run declines: pass@1 falls 4.0–11.3 points
and the sample-accuracy intervals exclude zero in all four A/B runs, though
same-seed A and B are closer to two replicates than four. The decline may grow
with the rate on one seed: at seed 1 sample accuracy falls 1.5, 3.5 and 8.3 points
across the three rates, at seed 2 an almost flat 3.7, 3.8 and 4.7. The cap-hit share
rises only at 5 × 10−4. The patch has no consistent effect: B minus A in round-2
pass@1 is +5.3 at seed 1 and −7.3 [−14.0, −0.7] at seed 2, a sign flip from pools
that differ by 0–3 examples, which illustrates trajectory noise. Style does not
separate imitation from drift: finished exam generations start more boxed than
the verifier-accepted pool and fall below it as the pool falls too, which imitation
of the pool and drift would both produce.
Table 4. Run A (MATH-500, original verifier, k = 4, three rounds) across learning rates
and seeds: pass@1, pass@4 and sample accuracy (600 exam generations) at round 0
→round 2, the share of round-2 generations that hit the 512-token cap (decoded text
re-tokenised to ≥508 tokens; round 0 is 43.0–43.2%, 48.2% at seed 3), and problems
added/lost summed over rounds 1–2. The two 5×10−4 rows are the A rows of Table 10.
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
Two controls at 5 × 10−4. The no-filter run trains on all k samples of every
selection problem (1,400 examples per round), removing the verifier; the train-
on-gold run trains on the 350 reference solutions every round (Table 6). Neither
is a single-variable control: no-filter takes 3–4× Run A’s optimizer steps, train-
on-gold about the same. Removing the filter is never better than keeping it
beyond noise and is worse on pass@4 at both seeds (round-2 differences −2.0
and −5.3 points, intervals including zero), but the dose difference means this
cannot be attributed to the filter. Training on reference solutions is followed

10
T. S. Nguyen and D. A. Tran
Table 5. Change from round 0 to the last round (percentage points) with 95%
paired problem-level bootstrap intervals over the 150 exam problems (10,000 resam-
ples; experiments/viec3/bootstrap_ci.py). Last round is R4 at 10−5 (k = 8) and
R2 elsewhere (k = 4). “Finished, matched” is the last-round accuracy of generations
below the 512-token cap minus the untrained model’s accuracy on the same problem
mix (Section 4.5; 2,000 resamples, experiments/viec3/review_cpu/capanat.py). The
intervals do not include training-seed variance. Recomputed values match the reported
ones except six round values that differ by one problem (Section 3.4), e.g. B, seed 1
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
No filter, 1
−6.0 [−12.7, 1.3]
−9.3 [−16.7, −2.7]
−8.2 [−12.2, −4.3]
−10.6 [−16.4, −5.5]
No filter, 2
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
by a much larger decline (pass@4 down about 21 points at both seeds) while
the model adopts the reference style ($-delimited spans 5% →98%); post hoc
checks suggest this fall is mostly real rather than verifier error. Run C at 5×10−4
(GSM8K, one run) falls 22.0 points of pass@1, from both less accurate and more
unfinished solutions (Appendix G).