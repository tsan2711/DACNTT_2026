

Design P: An Apparent Collapse

In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 53.6% → 19.2%, pass@8 77.8% → 51.0%; Table S3, Supplementary

Mathematics or the Veriﬁer?

7

Appendix D), on both datasets (Table S2); the 0.5B decline is small. The accepted pool contracts every round and \boxed{} falls from 5,608 to 2,693 of
8,000 generations. This design cannot be read causally: one adapter trains on
both pools, it scores on the problems it selects from, and it trains on about 4.5×
as many examples per round as the isolated MATH-500 run (3,962 against 872
at round 0) (Supplementary Appendix D).
4.2

Design I at 10−5 : Small Declines, a Larger One on GSM8K

On the held-out exam (Fig. S1 and Table S5 in Supplementary Appendix E)
pass@8 ends within 4 points of round 0 in every run. On MATH-500, pass@1 is
3.3–4.7 points lower at round 4, with every interval including zero (Table 2); sample accuracy falls 2.6–4.2 points, with an interval excluding zero for three of the
four runs (not B at seed 1, [−5.4, +0.2]), and matched ﬁnished accuracy changes
by −1.3 to +2.3, with every interval including zero. We read this as a possible
small decline, not an established one; we see no gain of the size the design could
detect. Run C (GSM8K) declines more: pass@1 falls 12.7 points ([−22.0, −3.3]),
but it took about twice Run A’s optimizer steps, so we do not attribute this to
the dataset alone. Length and cap-hit share barely change on MATH-500, weak
evidence that the adapter did little (Supplementary Appendix E).
4.3

The Patch Control Could Not Detect an Eﬀect

At round 4, B minus A is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and
+0.7 [−2.0, +3.3] at seed 1 (Table 2, all runs graded by the same veriﬁer). This
null is uninformative: \dfrac appears in 0.50–0.73% of generations, so the kept
pools diﬀer by at most 4 examples (under 0.5% of 872), and at 10−5 the adapter
changes the outputs little anyway; the frequent gold-storage defect is in both
arms.
4.4

Higher Learning Rates

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

8

D.-H. Vu et al.

Table 1. Run A (MATH-500, k = 4, three rounds) across learning rates and seeds:
pass@1, pass@4 and sample accuracy at round 0 → round 2, the share of round-2
generations that hit the 512-token cap (re-tokenised to ≥ 508 tokens; round 0 is 43.0–
43.2%, 48.2% at seed 3), and problems added/lost over rounds 1–2. The 5 × 10−4 rows
are the A rows of Table S6.
Rate
−4

10
10−4
10−4
2 × 10−4
2 × 10−4
5 × 10−4
5 × 10−4

Seed

pass@1

pass@4

Sample acc. Cap-hit (R2) Added/lost

40.0 → 38.7 60.0 → 56.0 41.0 → 37.3
38.0 → 34.7 60.0 → 54.7 37.7 → 33.0
35.3 → 30.7 46.0 → 48.0 34.5 → 32.2
40.0 → 37.3 60.0 → 55.3 41.0 → 35.0
38.0 → 30.0 60.0 → 53.3 37.7 → 31.7
40.0 → 28.0 60.0 → 50.7 41.0 → 30.2
38.0 → 32.0 60.0 → 52.7 37.7 → 31.7

1
2
3
1
2
1
2

42.7%
42.8%
45.7%
40.8%
39.7%
46.2%
51.2%

19/25
25/33
17/14
24/31
22/32
22/36
26/37

Table 2. Change from round 0 to the last round (percentage points) with 95%
paired problem-level bootstrap intervals over the 150 exam problems (10,000 resamples; bootstrap_ci.py in the code repository). Last round is R4 at 10−5 (k = 8) and
R2 elsewhere (k = 4). “Finished, matched” is the last-round accuracy of generations
below the 512-token cap minus the untrained model’s accuracy on the same problem
mix (Section 4.5; 10,000 resamples). The intervals do not include training-seed variance.
Every run is regraded from its saved generations with the same veriﬁer (Supplementary
Appendix C).
Run, seed

∆pass@1

∆pass@k

∆sample acc.

Finished, matched

−5

Learning rate 10
A, 0
−3.3 [−10.7, +4.0]
A, 1
−4.7 [−12.0, +2.7]
B, 0
−4.0 [−11.3, +4.0]
B, 1
−4.0 [−11.3, +2.7]
C, 0
−12.7 [−22.0, −3.3]

−3.3 [−10.7, +4.0]
−1.3 [−7.3, +4.7]
−5.3 [−12.0, +2.0]
−2.0 [−8.0, +4.0]
−2.7 [−8.0, +2.0]

−3.3 [−5.9, −0.7]
−0.7 [−4.4, +3.2]
−3.1 [−6.0, −0.2]
+0.8 [−3.5, +5.2]
−4.2 [−7.1, −1.2]
−1.3 [−5.5, +3.0]
−2.6 [−5.4, +0.2]
+2.3 [−1.9, +6.5]
−13.0 [−16.5, −9.6] −12.2 [−15.8, −8.8]

Learning rate 10−4
A, 1
−1.3 [−8.7, +6.0]
A, 2
−3.3 [−10.0, +3.3]
A, 3
−4.7 [−12.0, +2.7]

−4.0 [−10.0, +2.0]
−5.3 [−12.0, +1.3]
+2.0 [−4.0, +8.0]

−3.7 [−7.8, +0.5]
−4.7 [−8.7, −0.8]
−2.3 [−6.5, +1.7]

−1.3 [−6.9, +4.4]
−0.6 [−6.2, +5.1]
−1.0 [−7.5, +5.4]

Learning rate 2×10−4
A, 1
−2.7 [−9.3, +4.0]
A, 2
−8.0 [−15.3, +0.0]

−4.7 [−11.3, +2.0]
−6.7 [−13.3, +0.0]

−6.0 [−10.0, −2.0]
−6.0 [−10.3, −1.7]

−2.6 [−8.1, +2.9]
−3.2 [−9.5, +3.1]