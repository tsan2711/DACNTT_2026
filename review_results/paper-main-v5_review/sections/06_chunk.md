Mathematics or the Veriﬁer?
13
generations, compute
rt = #{accepted by V ′ but rejected by V }
#{accepted by V ′}
.
If the model learns to write what V accepts, rt may fall over rounds, but it
also falls when fewer answers are boxed: since V ′ diﬀers from V only on boxed
predictions, rt = rboxed
t
×(boxed share among V ′-accepted) holds as an identity.
This is the per-step tracking of RLVR studies [4,17] applied to oﬄine SFT;
overall rt is not enough on its own (Table 5; rt_audit.py in the repository).
For the gold-storage defect it falls in all three self-training runs we re-scored,
by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching zero. But
V ′ diﬀers from V only on boxed predictions, so unboxed correct answers enter
only the denominator, and the fall is accounted for by the falling \boxed share
among correct answers (91 →76% and 93 →78% at 5×10−4). That accounting
is an identity, not a test, and it does not exclude adaptation. On boxed answers
alone the changes (−0.4 to +0.7 points) have intervals (≈±3) that contain the
whole −2.6 fall, so “ﬂat” means not detected. The defect is also bound to the
problem: it ﬁres on 54–62 problems, rejecting 94–98% of correct answers (87–98%
where V parses the gold), and 29–34 of them have an unparseable gold, so no
answer form escapes it. On the 24–28 aﬀected problems where some form could,
rt moves by −5.5, −1.6 and −0.2 points (intervals 10–26 wide), and the training
pool holds only 2–12 examples per round that write these answers unboxed. We
expect the pressure to adapt under SFT to be weak, but we did not test this
(no dose–response). Our two injected-bias runs (Section 4.6) show no selective
avoidance either, but one cannot elicit it and the other is a single run without
rt, so we cannot tell whether the audit would detect adaptation. Train-on-gold,
with no veriﬁer in the loop, gives rt rises of 2.1–3.3 points, and even rt on boxed
answers alone rises by 2.8 and 1.7 (Table 5), so rt drifts by about as much as
the falls we observe for reasons unrelated to the veriﬁer. It should be reported
on the answers and problems where V and V ′ can diﬀer and an accepted form
exists, with the count of training examples that could teach avoidance.
(ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Sup-
plementary Appendix H). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.
(iii) Check the dose of a control before running it: our \dfrac patch changed
0–4 examples, the unvaried gold-storage defect a ﬁfth to a quarter of the pool
(440 →542).
(iv) Match training dose across designs (examples, steps and rate): the pooled
design’s decline cannot be attributed to pooling.
Check (i) in RLVR. A false reject gives zero reward there; we have not run
the audit on RLVR checkpoints.

14
T. S. Nguyen and D. A. Tran
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
6
Limitations
Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem draw
and sampling, not training-seed variance; the ﬁnal-round loop has three seeds,
the gate and the bias controls one, and no multiplicity correction is applied. The
learning-rate grid is coarse and changes k, rounds, dose and metric along with the
rate. Power is limited (about 10 points of pass@1 with 150 exam problems, about
6 in Section 4.6). The adaptation audit is weak: 24–28 problems, 2–12 avoidance
examples per round, and no valid positive control. The ﬁnal-round loop has no
no-ﬁlter arm. The veriﬁer audit used other models’ solutions and inspected only
rejections; the gold-storage defect was measured afterwards and ran unvaried
through every run before the ﬁnal round, and every headline number is graded by
the biased veriﬁer that also selects the data. Truncation: the 512-token cap binds
from the start (a quarter of the pool is cut). Scope: one model family and size,
all instruction-tuned (no base model), one veriﬁer, a restart-from-base design
that leaves compounding little room (no continued training), and possible test-
set contamination of Qwen2.5 on MATH/GSM8K (unquantiﬁed), and a default