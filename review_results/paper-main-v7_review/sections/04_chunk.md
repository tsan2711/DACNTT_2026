

Learning rate 5×10−4
A, 1
−12.0 [−19.3, −4.7] −9.3 [−16.0, −2.7] −10.8 [−15.2, −6.7] −6.1 [−11.3, −0.8]
A, 2
−6.0 [−13.3, +2.0]
−7.3 [−14.0, −0.7]
−6.0 [−9.8, −2.2]
−1.5 [−7.4, +4.4]
B, 1
−6.7 [−14.7, +1.3]
−5.3 [−12.7, +1.3]
−8.7 [−12.8, −4.7]
−4.1 [−9.8, +1.7]
B, 2
−11.3 [−18.0, −4.7] −12.0 [−18.7, −5.3] −10.7 [−14.7, −6.7]
−3.2 [−9.2, +2.9]
No ﬁlter, 1 −8.7 [−16.0, −1.3] −13.3 [−21.3, −6.0] −11.7 [−16.2, −7.3] −9.0 [−14.8, −3.3]
No ﬁlter, 2 −10.7 [−18.7, −3.3] −12.0 [−19.3, −4.7] −12.3 [−16.7, −8.0]
−3.6 [−9.6, +2.5]
Gold, 1
−24.0 [−32.7, −15.3] −24.0 [−32.7, −15.3] −24.8 [−30.7, −19.0] −26.0 [−32.0, −20.0]
Gold, 2
−24.7 [−33.3, −16.0] −20.7 [−29.3, −12.0] −21.8 [−27.5, −16.3] −23.7 [−29.7, −17.9]
C, 1
−22.0 [−29.3, −15.3] −9.3 [−15.3, −3.3] −15.3 [−19.8, −11.0] −11.3 [−15.7, −7.0]

Two controls at 5 × 10−4 . The no-ﬁlter run trains on all k samples of every
selection problem (1,400 examples per round), removing the veriﬁer; the trainon-gold run trains on the 350 reference solutions every round (Table 3). Neither

Mathematics or the Veriﬁer?

9

is a single-variable control: no-ﬁlter takes 3–4× Run A’s optimizer steps, trainon-gold about the same. Removing the ﬁlter is not better than keeping it beyond
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
Run

4.5

Pool
R0

pass@1
R1
R2

R0

pass@4
R1
R2

Seed 1
A (veriﬁer-ﬁltered)
No ﬁlter
Train on gold

440→326
1400
350

40.0
40.0
40.0

40.0
34.0
18.7

28.0
31.3
16.0

60.0
60.0
60.0

58.7
58.0
36.0

50.7
46.7
36.0

Seed 2
A (veriﬁer-ﬁltered)
No ﬁlter
Train on gold

424→350
1400
350

38.0
38.0
38.0

38.7
40.0
11.3

32.0
27.3
13.3

60.0
60.0
60.0

56.0
58.0
34.0

52.7
48.0
39.3

Anatomy of the Decline

This subsection is post hoc and descriptive. Sample accuracy mixes whether a
ﬁnished solution is right with whether the model ﬁnishes within the 512-token
cap. Re-tokenising the saved text, we call a generation cap-hit at ≥ 508 tokens.
At the rates where the share does not rise, 40–46% of round-2 MATH-500 generations already hit the cap (Table 1), so the cap binds from the start. At 5×10−4 ,
compared with the untrained model on the same problem mix, ﬁnished generations lose 1.5–9.0 points, with intervals excluding zero in two of six runs (A and
no-ﬁlter at seed 1; the six include two same-seed A/B pairs, which are close to
replicates), while the cap-hit share rises 2–14 points. The matched measure conditions on which problems ﬁnish after training, so it is descriptive. A three-part
decomposition attributes 12–30% of the decline to the cap share in the three

10

D.-H. Vu et al.

original seed-1 runs (and −2 and 5% in two further runs) and 52–72% at seed 2
(Table S9, Supplementary Appendix H). At 10−4 and 2 × 10−4 the cap-hit share
does not rise and ﬁnished accuracy carries the whole change. Train-on-gold is
diﬀerent: responses shorten by more than half and ﬁnished accuracy collapses.
Retraining without truncated examples, or re-scoring at a 1,536-token cap, leaves
the deﬁcit in place (Supplementary Appendix H).
4.6

A Final Round with a Revised Recipe

Because no earlier arm improved, we ran one last round with several recipe
changes made at once, aimed at the suspected causes (no ablation of any single
one): loss on the completion only, LoRA on all linear layers, a 1,024-token cap
and training limit, normalised gold answers, and a pool of 300 problems from the
MATH training split, so that the exam is all 500 MATH-500 problems. It is 10−4
with k = 2 and a single adapter (round 0 to round 1); the loop has three seeds,
the gate one. The pool comes from the PRM800K training split [21], which is
the complement of MATH-500 within MATH, so it is disjoint by construction
(no content-level overlap check). The veriﬁer-ﬁltered loop (298 examples kept)
is compared with training on the 300 reference solutions, a positive gate that
must raise accuracy for the recipe to count as able to help.
Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4 ). Change from
each run’s own untrained round 0 to round 1 in points (round-0 pass@1 is 49.2, 46.8,
48.2 at seeds 1–3, from sampling), with 95% paired problem-level bootstrap intervals
that omit training-seed variance. The gold arm has one seed.

Arm
pass@1
pass@2
Sample acc.
Untrained (seed 1)
49.2
59.4
–
Loop, seed 1
−4.8 [−9.0, −0.6]
−3.0 [−6.8, +0.8]
−2.9 [−5.8, −0.1]
Loop, seed 2
−3.2 [−7.0, +0.6]
−6.2 [−10.0, −2.6]
−5.3 [−8.1, −2.4]
Loop, seed 3
−4.2 [−8.4, +0.0]
−5.6 [−9.4, −1.8]
−5.4 [−8.3, −2.5]
Loop, mean of seeds
−4.1
−4.9
−4.5
Train on gold
−32.2 [−37.0, −27.6] −32.0 [−36.6, −27.4] −30.2 [−33.8, −26.6]