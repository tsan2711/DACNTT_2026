
Mathematics or the Veriﬁer?
13
a rare bias, and the no-ﬁlter control declines without any selection veriﬁer but
with more dose (and, with a constant pool, cannot test the shrinking pool). At
this resolution, removing a rare format defect, or the ﬁlter entirely, made no
consistent diﬀerence (no ﬁlter is lower on pass@k at 3–4× the dose); neither
tests the systematic false positives Egashira et al. ﬁnd harmful in RLVR.
5.3
A Proposed Audit for GVT with a Biased Veriﬁer
Our pre-set rule tied “learning the veriﬁer’s style” to rising accuracy, so it could
not speak once accuracy fell. From post hoc analyses we propose four checks for
self-training with a rule-based veriﬁer, as a protocol for future studies, not as
tested methods.
(i) A per-round false-reject audit. Fix a repaired veriﬁer V ′ that corrects a
known defect class of the training veriﬁer V . At each round t, on the loop’s own
generations, compute
rt = #{accepted by V ′ but rejected by V }
#{accepted by V ′}
.
If the model learns to write what V accepts, rt may fall over rounds, but it also
falls when fewer answers are boxed: since V ′ diﬀers from V only on boxed predic-
tions, rt = rboxed
t
× (boxed share among V ′-accepted) holds as an identity. This
is the per-step tracking of RLVR studies [4,16] applied to oﬄine SFT (Table 5;
rt_audit.py). For the gold-storage defect it falls in all three self-training runs
we re-scored, by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching
zero. The fall is accounted for by the falling \boxed share among correct answers
(91 →76% and 93 →78% at 5 × 10−4): an identity, not a test, which does not
exclude adaptation. On boxed answers alone the changes (−0.4 to +0.7 points)
have intervals (≈±3) that contain the overall fall of the same run (−2.6, −2.6,
−1.5), so “ﬂat” means not detected. The defect is bound to the problem: it
ﬁres on 54–62 problems, rejecting 94–98% of correct answers, and 29–34 of them
have an unparseable gold, so no answer form escapes it. On the 24–28 aﬀected
problems where some form could, rt moves by −5.5, −1.6 and −0.2 points (in-
tervals 10–26 wide), and the pool holds only 2–12 such unboxed examples per
round, so we expect weak pressure to adapt (untested; no dose–response). The
two injected-bias runs (Section 4.6) show no selective avoidance, but neither can
tell us whether the audit would detect it. Train-on-gold, with no veriﬁer in the
loop, gives rt rises of 2.1–3.3 points (2.8 and 1.7 on boxed answers alone; Ta-
ble 5), so rt drifts as much as the falls we observe, unrelated to the veriﬁer. It
should be reported on the answers and problems where V and V ′ can diﬀer and
an accepted form exists, with the count of training examples that could teach
avoidance.
(ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Sup-
plementary Appendix H). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.


14
T. S. Nguyen and D. A. Tran
Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all
500 problems, selection problems included), round 0 →last round, with the change
and a 95% problem-level bootstrap interval (2,000 resamples). “Boxed only” restricts
to predictions containing \boxed; “aﬀected, parseable” to problems where the defect
ever ﬁres and V can parse the gold. Pool: examples per round from aﬀected problems
that V accepts (and so avoid the defect).
Run
rt subset
R0
Last
∆
95% interval
Pool
A, 5 × 10−4, seed 1
all
18.3
15.7
−2.6
[−5.3, 0.3]
3–5
boxed only
20.0
20.7
+0.7
[−2.9, 4.3]
aﬀected, parseable
92.8
87.2
−5.5
[−20.1, 6.3]
A, 5 × 10−4, seed 2
all
18.1
15.5
−2.6
[−5.2, 0.1]
2–3
boxed only
19.4
19.8
+0.4
[−2.8, 3.4]
aﬀected, parseable
95.1
93.5
−1.6
[−14.7, 9.5]
A, 10−5, seed 0
all
18.3
16.8
−1.5
[−2.9, 0.0]
9–12
boxed only
19.9
19.5
−0.4
[−2.0, 1.2]
aﬀected, parseable
92.3
92.0
−0.2
[−4.9, 4.6]
Gold, seed 1
all
18.2
21.5
+3.3
[−1.2, 8.1]
—
boxed only
20.0
22.8
+2.8
[−2.0, 7.7]
aﬀected, parseable
95.5
94.7
−0.7
[−9.1, 6.2]
Gold, seed 2
all
18.0
20.2
+2.1
[−2.2, 6.7]
—
boxed only
19.4
21.1
+1.7
[−3.3, 6.5]
aﬀected, parseable
95.1
97.6
+2.5
[−4.8, 11.9]
(iii) Check the dose of a control ﬁrst (our \dfrac patch changed 0–4 exam-
ples; the unvaried defect a ﬁfth to a quarter of the pool) and (iv) match dose
across designs, which the pooled design did not.
6
Limitations
Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem
draw and sampling, not training-seed variance; the ﬁnal-round loop has three
seeds, the gate and the bias controls one, and no multiplicity correction is ap-
plied. The learning-rate grid is coarse and changes k, rounds and dose with the
rate. Power is limited (about 10 points of pass@1 with 150 exam problems,
about 6 in Section 4.6). The adaptation audit is weak: 24–28 problems, 2–12
avoidance examples per round, and no valid positive control. The ﬁnal-round
loop has no no-ﬁlter arm. The veriﬁer audit used other models’ solutions and
inspected only rejections; the gold-storage defect ran unvaried through every
earlier run, whose headline numbers are graded by the biased veriﬁer that also
selects the data, and the ﬁnal-round string-match grader shares the \boxed de-
pendence. The ﬁnal-round decline and the gate failure cannot be attributed to