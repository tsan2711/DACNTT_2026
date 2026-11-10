### 4.5 Anatomy of the Decline
This subsection is post hoc and descriptive. Sample accuracy mixes whether a fin-
ished solution is right with whether the model finishes within the 512-token cap
at all. Re-tokenising the saved text, we call a generation cap-hit at ≥508 tokens.
The untrained model already hits the cap in 41–48% of MATH-500 generations,
so the cap binds from the start. An earlier character-length proxy for unfinished
generations overstated termination, because drifting prose crosses its threshold
within the same token budget. At 5 × 10−4, compared with the untrained model
on the same problem mix, finished generations lose 5.5–10.6 points, with inter-

Mathematics or the Verifier?
11
Table 6. Controls at 5×10−4 (MATH-500, k = 4, three rounds), on the exam partition
of Run A at the same seed. Pool is the number of training examples per round; optimizer
steps are half of it.
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
A (verifier-filtered)
440→326
33.3
32.7
23.3
50.0
49.3
42.7
No filter
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
A (verifier-filtered)
424→350
31.3
31.3
27.3
51.3
46.0
44.7
No filter
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
vals excluding zero in five of six runs, while the cap-hit share rises 2–14 points.
A three-part decomposition attributes 12–30% of the decline to the cap share at
seed 1 and 52–72% at seed 2 (Table 7). At 10−4 and 2 × 10−4 the cap-hit share
does not rise and finished accuracy carries the whole change. Train-on-gold is
different: responses shorten by more than half and finished accuracy collapses.
Retraining without truncated examples and re-scoring adapters at a 1,536-token
cap leave the picture unchanged, within the noise of single runs (Appendix H).
Table 7. Decomposition of the change in sample accuracy (points, round 0 →last
round, MATH-500 exam unless stated) into finished-accuracy, cap-share and cap-
accuracy parts, with the change in cap-hit share. Intervals: paired problem-level boot-
strap, 2,000 resamples. The share is the finished part over the whole change.
Run, seed
∆cap-hit
∆acc. Finished Cap-share Cap-acc.
Fin. share
5 × 10−4
A, 1
+3.0 [−1.7, 7.7]
−8.3
−6.0
−1.3
−1.0
73% [43, 108]
B, 1
+4.7 [0.2, 9.5]
−6.7
−4.2
−2.0
−0.5
62% [21, 100]
No filter, 1
+2.3 [−2.5, 6.8]
−8.2
−6.0
−1.0
−1.1
74% [46, 106]
A, 2
+8.2 [3.8, 12.3]
−4.7
−2.7
−3.4
+1.5
59% [−11, 114]
B, 2
+11.0 [6.2, 16.0]
−9.2
−3.6
−4.8
−0.8
39% [6, 64]
No filter, 2
+14.2 [9.3, 18.8] −10.2
−3.5
−6.1
−0.6
34% [5, 57]
A replicate, 1
−0.2 [−4.5, 4.3]
−5.2
−4.6
+0.1
−0.7
89% [41, 162]
A, 1024 limit, 1 +0.7 [−3.7, 5.2]
−5.7
−4.8
−0.3
−0.5
85% [42, 169]
C (GSM8K), 1
+11.2 [7.8, 14.7] −15.3
−7.8
−6.6
−0.9
51% [30, 66]
2 × 10−4 and 10−4
A, 2 × 10−4, 1
−2.3 [−6.7, 2.3]
−3.5
−4.3
+1.0
−0.2
124%
A, 2 × 10−4, 2
−3.3 [−7.7, 1.0]
−3.7
−5.2
+1.4
+0.1
142%
A, 10−4, 1
−0.5 [−4.5, 3.7]
−1.8
−3.1
+0.2
+1.0
169%
A, 10−4, 2
−0.2 [−4.3, 4.0]
−3.7
−3.4
+0.1
−0.3
93%
A, 10−4, 3
−2.5 [−6.3, 1.3]
−1.0
−1.4
+1.1
−0.7
139%

12
T. S. Nguyen and D. A. Tran