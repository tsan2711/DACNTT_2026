
Mathematics or the Veriﬁer?
13
answers (91 →76% and 93 →78% at 5 × 10−4), a match that adaptation
to the defect would also produce. On boxed answers alone rt is ﬂat (changes
−0.4 to +0.7 points). The defect is also bound to the problem: it ﬁres on 54–
62 problems, rejecting 94–98% of correct answers (87–98% where V parses the
gold), and 29–34 of them have an unparseable gold, so no answer form escapes
it. On the 24–28 aﬀected problems where some form could, rt moves by −5.5,
−1.6 and −0.2 points, with intervals 10–26 points wide. A model adapting to the
defect would have to write these answers unboxed, and the training pool holds
only 2–12 examples per round from these problems that do so. Under SFT the
pressure to adapt is therefore weak. Our two injected-bias controls (Section 4.6)
show no selective avoidance either, so without a control that shows an eﬀect
we cannot tell whether the audit would detect adaptation. We see none, in one
defect class, but it had little power to see any. Train-on-gold, with no veriﬁer in
the loop, gives rt rises of 2.1–3.3 points as its outputs become more boxed, so
rt moves with format for reasons unrelated to the veriﬁer. It should be reported
on the answers and problems where V and V ′ can diﬀer and an accepted form
exists, with the count of training examples that could teach avoidance.
Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all 500
problems), round 0 →last round, with the change and a 95% problem-level bootstrap
interval (2,000 resamples). “Boxed only” restricts to predictions containing \boxed;
“aﬀected, parseable” to problems where the defect ever ﬁres and V can parse the gold.
Pool: examples per round from aﬀected problems that V accepts (and so avoid the
defect).
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


14
T. S. Nguyen and D. A. Tran
(ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Sup-
plementary Appendix H). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.
(iii) Check the dose of a control before running it. Count how many training
examples the treatment changes. Our \dfrac patch changed 0–4 examples, while
the unvaried gold-storage defect would have changed about a ﬁfth to a quarter
of the pool (440 →542 at round 0); the ﬁrst number alone shows the patch
control could not detect an eﬀect.
(iv) Match training dose across designs. Our pooled design trained on about
4.5× more examples per round than the isolated one, so its sharp decline cannot
be attributed to pooling.
Check (i) in RLVR. A false reject gives zero reward there, a direct pressure
that SFT lacks; we have not run the audit on public RLVR checkpoints.
6
Limitations
Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem draw
and sampling, not training-seed variance; the ﬁnal-round loop has three seeds,
the gate and the bias controls one, and no multiplicity correction is applied. The
learning-rate grid is coarse and changes k, rounds, dose and metric along with the
rate. The power is limited: with 150 exam problems only gains of about 10 points
of pass@1 would be detected (about 6 with the 500 problems of Section 4.6,
k = 2, two rounds). The adaptation audit is weak: 24–28 problems, 2–12 training
examples per round that could teach avoidance, and two positive controls with
no eﬀect. The veriﬁer audit used other models’ solutions and inspected only
rejections; the gold-storage defect was measured afterwards and ran unvaried
through every run before the ﬁnal round, and every headline number is graded
by the biased veriﬁer that also selects the data. Truncation: the 512-token cap
binds from the start and truncates a quarter of the pool in the main runs. Scope:
one model family and size, all instruction-tuned (no base model), one veriﬁer,
a restart-from-base design that leaves compounding little room (no continued
training), and possible test-set contamination. No arm improves on round 0,
and the gate on reference solutions failed even with the corrected recipe, so we
have no positive reference showing that any recipe can help a 1.5B model here.
7
Conclusion
We asked whether generate–verify–select–train iterations make a 1.5B model
better at mathematics or only teach it to write what a rule-based veriﬁer accepts.
On held-out exams the ﬁrst answer is no gain that this design could detect: no run
shows a pass@1 or pass@k gain whose interval excludes zero, though gains below