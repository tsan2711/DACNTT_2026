
Mathematics or the Veriﬁer?
11
Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4). Change from
each run’s own untrained round 0 to round 1 in points (round-0 pass@1 is 49.2, 46.8,
48.2 at seeds 1–3, from sampling), with 95% paired problem-level bootstrap intervals
that omit training-seed variance. The gold arm has one seed.
Arm
pass@1
pass@2
Sample acc.
Untrained
49.2
59.4
–
Loop, seed 1
−4.8 [−9.0, −0.6]
−3.0 [−6.8, +0.6]
−2.9 [−5.8, 0.0]
Loop, seed 2
−3.2 [−6.8, +0.6]
−6.2 [−9.8, −2.4]
−5.3 [−8.1, −2.4]
Loop, seed 3
−4.2 [−8.4, −0.2]
−5.6 [−9.4, −1.6]
−5.4 [−8.3, −2.4]
Loop, mean of seeds
−4.1
−4.9
−4.5
Train on gold
−32.2 [−36.8, −27.6] −32.0 [−36.6, −27.2] −30.2 [−33.8, −26.6]
The gate fails. Training on reference solutions lowers pass@1 from 49.2% to
17.0%, and the model adopts the reference style ($-delimited spans in 60 of 1,600
generations at round 0, 1,577 at round 1, counted over the exam and selection
problems), as in the earlier train-on-gold arms. A rerun at 2 × 10−5 fails the
same way (49.2% →20.6%, $-spans in 1,558 of 1,600 generations), so the failure
is not speciﬁc to the rate; we attribute it to the reference style but did not
isolate it. The gate shows only that we have no recipe known to raise accuracy;
it neither validates nor refutes the loop. The veriﬁer-ﬁltered loop loses pass@1
in all three seeds (4.8, 3.2, 4.2 points; two intervals exclude zero) and sample
accuracy in all three (intervals exclude zero for seeds 2 and 3). The mean pass@1
change over the three seeds is −4.1 (t interval [−6.1, −2.1]), and −4.5 for sample
accuracy ([−8.1, −1.0]). The loop does not help and probably costs a few points;
we did not isolate the cause. The detectable eﬀect is about 6 points of pass@1
(2.8h/1.96), against about 10 before.
Injected bias. As positive controls for the audit we reran the loop once each
(seed 1, 10−4) with a selection veriﬁer that rejects \boxed answers (exam veriﬁer
clean). In the ﬁrst, a hash-chosen 30% of problems are aﬀected: the \boxed share
falls 4.9 points on them and 3.1 on the others (diﬀerence −0.1, [−6.1, 6.0]); a
hash cannot be learned from the problem, so this control could not elicit selective
avoidance. In the second the rule is visible: every \boxed answer is rejected when
the gold contains \frac (70 of 500 problems; 263 examples kept instead of 298).
The share on those problems stays at 95.0% and on the others goes from 90.2%
to 87.4% (diﬀerence +2.8, [−2.8, +8.3]), against −3.7, −2.7 and −5.5 for the
same split in the three unbiased seeds; pass@1 falls 7.0 points ([−11.2, −3.0]).
The model does not stop boxing where boxing is penalised, but neither control
shows an eﬀect, so neither validates the audit; we report no rt for them.
5
Discussion
5.1
Answer to the Research Question
Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k with an interval excluding zero, at any rate; in the 500-problem ﬁnal


12
T. S. Nguyen and D. A. Tran
round pass@1 falls 3.2–4.8 points in each of three seeds. The sample-accuracy
ﬁgure of about 2.2 points is the largest upper limit among observed intervals, a
post hoc ﬁgure for a measure chosen after the runs that omits seed variance, not
a power statement; on the pre-set measures the design could detect only about
10 points of pass@1 and 8–10 of pass@k (6 and 5 in the ﬁnal round). Because no
arm improves and the positive gate failed, the null belongs to this recipe, and
the study cannot say whether self-training in general helps.
Does it learn to write what the veriﬁer accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably (the
largest rise is +0.7 [−6.7, +8.0]), so the rule’s silence is not evidence against
veriﬁer-style learning. No run varies the frequent gold-storage defect, and the
post hoc audit of Section 5.3 is too weak to show or rule out adaptation to it.
What happened to the pooled collapse? It does not reproduce under isolation;
the pooled design also trained on about 4.5× more examples per round, so we
cannot say whether pooling, selection-set scoring or dose produced it.
5.2
Interpretation
One explanation of the Design P curves is a self-reinforcing shrinking pool shaped
by the biased veriﬁer. The data neither support nor rule it out: the patch tests
a rare bias, and the no-ﬁlter control declines without any veriﬁer but with more
dose. The defensible statement is narrow: removing a rare format defect, or the
ﬁlter entirely, made no consistent diﬀerence at this resolution. Neither control
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
If the model learns to write what V accepts, rt may fall over rounds, but it
also falls when fewer answers are boxed, so it is not a clean signal on its own.
This is the per-step tracking of RLVR studies [4,17] applied to oﬄine SFT;
overall rt is not enough on its own (Table 5; rt_audit.py in the repository).
For the gold-storage defect it falls in all three self-training runs we re-scored,
by 2.6, 2.6 and 1.5 points, with intervals reaching or just touching zero. But V ′
diﬀers from V only on boxed predictions, so unboxed correct answers enter only
the denominator, and the fall matches the falling \boxed share among correct