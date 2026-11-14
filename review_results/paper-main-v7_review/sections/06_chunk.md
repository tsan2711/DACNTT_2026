

If the model learns to write what V accepts, rt may fall over rounds, but it also
falls when fewer answers are boxed: since V ′ diﬀers from V only on boxed predictions, rt = rtboxed × (boxed share among V ′ -accepted) holds as an identity. This
is the per-step tracking of RLVR studies [4,16] applied to oﬄine SFT (Table 5;
rt_audit.py). For the gold-storage defect it falls in all three self-training runs
we re-scored, by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching
zero. The fall is accounted for by the falling \boxed share among correct answers
(91 → 76% and 93 → 78% at 5 × 10−4 ): an identity, not a test, so adaptation is
not excluded. On boxed answers alone the changes (−0.4 to +0.7) have intervals
that contain the overall fall of the same run, so “ﬂat” means not detected. The
defect is bound to the problem: it ﬁres on 54–62 problems, rejecting 94–98%
of correct answers, and 29–34 of them have an unparseable gold. On the 24–28
aﬀected problems where some form could, rt moves by −5.5, −1.6 and −0.2
points (intervals 10–26 wide), and the pool holds only 2–12 such examples per
round, so we expect weak pressure to adapt (untested). The two injected-bias
runs (Section 4.6) show no selective avoidance, but cannot tell us whether the
audit would detect it. Train-on-gold, with no veriﬁer in the loop, gives rt rises of
2.1–3.3 points (Table 5), so rt drifts as much as the falls we observe, unrelated

Mathematics or the Veriﬁer?

13

Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all
500 problems, selection problems included), round 0 → last round, with the change
and a 95% problem-level bootstrap interval (2,000 resamples). “Boxed only” restricts
to predictions containing \boxed; “aﬀected, parseable” to problems where the defect
ever ﬁres and V can parse the gold. Pool: examples per round from aﬀected problems
that V accepts.
Run
A, 5 × 10

rt subset
−4

, seed 1 all
boxed only
aﬀected, parseable
A, 5 × 10−4 , seed 2 all
boxed only
aﬀected, parseable
A, 10−5 , seed 0
all
boxed only
aﬀected, parseable
Gold, seed 1
all
boxed only
aﬀected, parseable
Gold, seed 2
all
boxed only
aﬀected, parseable

R0 Last
18.3
20.0
92.8
18.1
19.4
95.1
18.3
19.9
92.3
18.2
20.0
95.5
18.0
19.4
95.1

15.7
20.7
87.2
15.5
19.8
93.5
16.8
19.5
92.0
21.5
22.8
94.7
20.2
21.1
97.6

∆ 95% interval Pool
−2.6
+0.7
−5.5
−2.6
+0.4
−1.6
−1.5
−0.4
−0.2
+3.3
+2.8
−0.7
+2.1
+1.7
+2.5

[−5.3, 0.3] 3–5
[−2.9, 4.3]
[−20.1, 6.3]
[−5.2, 0.1] 2–3
[−2.8, 3.4]
[−14.7, 9.5]
[−2.9, 0.0] 9–12
[−2.0, 1.2]
[−4.9, 4.6]
[−1.2, 8.1] —
[−2.0, 7.7]
[−9.1, 6.2]
[−2.2, 6.7] —
[−3.3, 6.5]
[−4.8, 11.9]

to the veriﬁer. It should be reported on the answers and problems where V and
V ′ can diﬀer, with the count of training examples that could teach avoidance.
(ii) Decompose declines under a ﬁxed cap. Report the change in sample accuracy split into a ﬁnished-accuracy part and a cap-share part (Table S9, Supplementary Appendix H). The split is descriptive: at 5×10−4 the cap share accounts
for 12–30% of the decline in the three seed-1 runs and 52–72% at seed 2.
(iii) Check the dose of a control ﬁrst (our \dfrac patch changed 0–4 examples) and (iv) match dose across designs.

6

Limitations

Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem
draw and sampling, not training-seed variance; the ﬁnal-round loop has three
seeds, the gate and the bias controls one, and there is no multiplicity correction.
The learning-rate grid is coarse and changes k, rounds and dose with the rate.
Power is limited (about 10 points of pass@1 with 150 exam problems, about
6 in Section 4.6), and the adaptation audit is weak (24–28 problems, no valid
positive control). The veriﬁer audit used other models’ solutions and inspected
only rejections; the gold-storage defect ran unvaried through every earlier run,

14

D.-H. Vu et al.

whose numbers are graded by V ′ , which is not independent of the selecting
veriﬁer, and the string-match grader shares the \boxed dependence. The ﬁnalround decline and the gate failure cannot be attributed to one recipe change.
Truncation: the 512-token cap binds from the start (a quarter of the pool is
cut). Scope: one model family and size, all instruction-tuned (no base model),
one veriﬁer, a restart-from-base design that leaves compounding little room (no
continued training), unquantiﬁed Qwen2.5 contamination on MATH/GSM8K,
and a default repetition penalty (1.1).

7

Conclusion