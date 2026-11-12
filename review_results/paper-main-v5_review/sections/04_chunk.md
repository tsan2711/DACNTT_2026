Mathematics or the Veriﬁer?
9
Table 2. Change from round 0 to the last round (percentage points) with 95%
paired problem-level bootstrap intervals over the 150 exam problems (10,000 resam-
ples; bootstrap_ci.py in the code repository). Last round is R4 at 10−5 (k = 8) and
R2 elsewhere (k = 4). “Finished, matched” is the last-round accuracy of generations
below the 512-token cap minus the untrained model’s accuracy on the same problem
mix (Section 4.5; 2,000 resamples, capanat.py in the repository). The intervals do not
include training-seed variance. Recomputed values match the reported ones except six
round values that diﬀer by one problem (Supplementary Appendix C), e.g. B, seed 1
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
No ﬁlter, 1
−6.0 [−12.7, 1.3]
−9.3 [−16.7, −2.7]
−8.2 [−12.2, −4.3]
−10.6 [−16.4, −5.5]
No ﬁlter, 2
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
while the model adopts the reference style ($-delimited spans 5% →98%). Post
hoc checks bound veriﬁer error from below only (about 2 points of sample accu-
racy among boxed answers), and the 14% of round-2 generations without \boxed
are not covered, so we think this fall is unlikely to be mainly veriﬁer error but
cannot bound it from above. That no arm, this one included, improves on the
untrained model means we have no positive reference: the nulls above may reﬂect
the recipe (LoRA on q/v projections, loss over the prompt, a 512-token limit)
rather than self-training. Run C at 5×10−4 (GSM8K, one run) falls 22.0 points of
pass@1, from both less accurate and more unﬁnished solutions (Supplementary
Appendix G).
4.5
Anatomy of the Decline
This subsection is post hoc and descriptive. Sample accuracy mixes whether a
ﬁnished solution is right with whether the model ﬁnishes within the 512-token
cap at all. Re-tokenising the saved text, we call a generation cap-hit at ≥508

10
T. S. Nguyen and D. A. Tran
Table 3. Controls at 5×10−4 (MATH-500, k = 4, three rounds), on the exam partition
of Run A at the same seed. Pool is the kept pool at round 0 →round 2; the round-
2 model trains on the round-1 pool (392 and 386 examples, about 195 steps) and
optimizer steps are half the pool size.
Run
Pool
pass@1
pass@4
R0
R1
R2
R0
R1
R2
Seed 1
A (veriﬁer-ﬁltered)
440→326
33.3
32.7
23.3
50.0
49.3
42.7
No ﬁlter
1400
33.3
26.7
27.3
50.0
49.3
40.7
Train on gold
350
33.3
18.0
15.3
50.0
33.3
29.3
Seed 2
A (veriﬁer-ﬁltered)
424→350
31.3
31.3
27.3
51.3
46.0
44.7
No ﬁlter
1400
31.3
34.7
22.7
51.3
48.7
39.3
Train on gold
350
31.3
8.7
10.0
51.3
28.7
30.7
tokens. At the rates where the share does not rise, 40–46% of round-2 MATH-500
generations already hit the cap (Table 1), so the cap binds from the start. At
5×10−4, compared with the untrained model on the same problem mix, ﬁnished
generations lose 5.5–10.6 points, with intervals excluding zero in ﬁve of six runs
(the six include two same-seed A/B pairs, which are close to replicates), while
the cap-hit share rises 2–14 points. The matched measure conditions on which
problems ﬁnish after training, so it is descriptive. A three-part decomposition
attributes 12–30% of the decline to the cap share in the three original seed-1
runs (and −2 and 5% in two further runs) and 52–72% at seed 2 (Table S9,
Supplementary Appendix H). At 10−4 and 2 × 10−4 the cap-hit share does not
rise and ﬁnished accuracy carries the whole change. Train-on-gold is diﬀerent:
responses shorten by more than half and ﬁnished accuracy collapses. Retraining
without truncated examples, or re-scoring at a 1,536-token cap, leaves the deﬁcit
in place (Supplementary Appendix H).
4.6
A Final Round with a Revised Recipe
Because no earlier arm improved, we ran one last round with seven recipe changes
made at once, aimed at the suspected causes (no ablation of any single one): loss
on the completion only, LoRA on all linear layers, a 1,024-token cap and training
limit, normalised gold answers, and a pool of 300 problems from the MATH
training split, so that the exam is all 500 MATH-500 problems. It is 10−4 with
k = 2 and a single adapter (round 0 to round 1); the loop has three seeds, the
gate one. We report no overlap check of the 300 pool problems against MATH-
500. The veriﬁer-ﬁltered loop (298 examples kept) is compared with training
on the 300 reference solutions, a positive gate that must raise accuracy for the
recipe to count as able to help.
The gate fails. Training on reference solutions lowers pass@1 from 49.2% to
17.0%, and the model adopts the reference style ($-delimited spans in 60 of 1,600