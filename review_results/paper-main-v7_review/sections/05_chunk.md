

The gate fails. Training on reference solutions lowers pass@1 from 49.2% to
17.0%, and the model adopts the reference style ($-delimited spans in 60 of 1,600
generations at round 0, 1,577 at round 1, counted over the exam and selection
problems), as in the earlier train-on-gold arms. A rerun at 2 × 10−5 fails the
same way (49.2% → 20.6%, $-spans in 1,558 of 1,600 generations), so the failure
is not speciﬁc to the rate. It is not a format defect: on the 500 exam problems
the share of generations with a \boxed answer is unchanged (90.6 → 90.3%),
accuracy among them falls from 48.5 to 17.1%, and the median length drops
3.2× (1,332 → 414 characters; string-match grader; gate_anatomy.py). The
model imitates terse reference solutions and loses reasoning steps; the three
loop seeds show a diﬀerent pattern (median length 1,332–1,348 → 1,454–1,491

Mathematics or the Veriﬁer?

11

characters, boxed share −0.6, −0.6, −5.1 points, accuracy among boxed answers
−2.5, −5.7, −3.4), so their decline is not this eﬀect. The gate therefore fails to
validate the revised recipe. With no recipe known to raise accuracy, the loop’s
decline cannot be attributed to self-training or to the veriﬁer. The veriﬁer-ﬁltered
loop loses pass@1 in all three seeds (4.8, 3.2, 4.2 points; one interval excludes
zero and one reaches it) and sample accuracy in all three (all three intervals
exclude zero). The mean pass@1 change over the three seeds is −4.1 (t interval
[−6.1, −2.1]), and −4.5 for sample accuracy ([−8.0, −1.0]). The loop does not
help; the estimates are negative in all three seeds, but with three seeds, one exam
draw and one rate we do not claim that it costs accuracy or isolate the cause.
The detectable eﬀect is about 6 points of pass@1 (2.8h/1.96), against about 10
before.
Injected bias. As intended positive controls for the audit (neither turns out
to be one) we reran the loop once each (seed 1, 10−4 ) with a selection veriﬁer
that rejects \boxed answers (exam veriﬁer clean). In the ﬁrst, a hash-chosen
30% of problems are aﬀected: the \boxed share falls 4.9 points on them and 3.1
on the others (diﬀerence −1.8, [−7.4, 3.8]); a hash cannot be learned from the
problem, so this control could not elicit selective avoidance. In the second the
rule is visible: every \boxed answer is rejected when the gold contains \frac (49
of the 300 selection problems, 263 examples kept instead of 298; 70 of the 500
exam problems, where the shares are measured). The share on those problems
stays at 95.0% and on the others goes from 90.2% to 87.4% (diﬀerence +2.8,
[−2.8, +8.3]), against −3.7, −2.7 and −5.5 in the three unbiased seeds; pass@1
falls 7.0 points ([−11.2, −3.0]), more than in the unbiased seeds, which we do not
interpret (one run). In neither run does the \boxed share fall selectively where
boxing is penalised, so neither validates the audit.

5

Discussion

5.1

Answer to the Research Question

Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k with an interval excluding zero, at any rate; in the 500-problem ﬁnal
round pass@1 falls 3.2–4.8 points in each of three seeds. The sample-accuracy
ﬁgure of about 1.7 points is the largest upper limit among observed intervals, a
post hoc ﬁgure that omits seed variance, not a power statement; on the pre-set
measures the design could detect only about 10 points of pass@1 and 8–10 of
pass@k (6 and 5 in the ﬁnal round). Because no arm improves and the positive
gate failed, the null belongs to this recipe, and the study cannot say whether
self-training in general helps. Every score is graded by V ′ , the selecting veriﬁer
of the ﬁnal round, which the earlier runs did not use (Section 3). On every run
a second grader (normalised string match of the last \boxed against the gold,
no math-verify; indep_grade.py) gives, in the ﬁnal round, pass@1 changes
of −3.6, −2.2, −4.6 for the three seeds (−30.0 for the gold arm) and sampleaccuracy changes of −2.5, −5.5, −5.3 (same sign and size); in the isolated runs
it gives larger sample-accuracy falls than V ′ (Supplementary Table S5) because

12

D.-H. Vu et al.

the boxed share falls. It reads only the last \boxed, so a falling boxed share
lowers both graders; it does not rule out a format artefact in the gate.
Does it learn to write what the veriﬁer accepts? Undecided: the pre-set pattern requires pass@1 to rise, which never happens detectably (largest pass@1
change −1.3 [−8.7, +6.0]), no run varies the frequent gold-storage defect, and
the audit of Section 5.3 is too weak.
5.2

Interpretation

One explanation of the Design P curves is a self-reinforcing shrinking pool shaped
by the biased veriﬁer. The data neither support nor rule it out: the patch tests
a rare bias, and the no-ﬁlter control declines without a selection veriﬁer but
with more dose. Removing a rare format defect, or the ﬁlter entirely, made no
consistent diﬀerence; neither tests the systematic false positives Egashira et al.
ﬁnd harmful in RLVR.
5.3

A Proposed Audit for GVT with a Biased Veriﬁer

Our pre-set rule could not speak once accuracy fell. From post hoc analyses we
propose four checks for self-training with a rule-based veriﬁer (untested protocol).
(i) A per-round false-reject audit. Fix a repaired veriﬁer V ′ that corrects a
known defect class of the training veriﬁer V . At each round t, on the loop’s own
generations, compute
rt =

#{accepted by V ′ but rejected by V }
.
#{accepted by V ′ }