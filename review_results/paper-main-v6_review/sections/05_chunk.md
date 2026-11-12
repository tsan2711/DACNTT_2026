
Mathematics or the Veriﬁer?
11
4.6
A Final Round with a Revised Recipe
Because no earlier arm improved, we ran one last round with several recipe
changes made at once, aimed at the suspected causes (no ablation of any single
one): loss on the completion only, LoRA on all linear layers, a 1,024-token cap
and training limit, normalised gold answers, and a pool of 300 problems from
the MATH training split, so that the exam is all 500 MATH-500 problems. It
is 10−4 with k = 2 and a single adapter (round 0 to round 1); the loop has
three seeds, the gate one. We report no overlap check of the 300 pool problems
against MATH-500. The veriﬁer-ﬁltered loop (298 examples kept) is compared
with training on the 300 reference solutions, a positive gate that must raise
accuracy for the recipe to count as able to help.
Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4). Change from
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
problems), as in the earlier train-on-gold arms. A rerun at 2×10−5 fails the same
way (49.2% →20.6%, $-spans in 1,558 of 1,600 generations), so the failure is not
speciﬁc to the rate. We noticed the shift to the reference style but did not test
it as the cause. That style carries no \boxed answer, which both graders read,
and a collapse of this size from 300 reference solutions is also what a pipeline
defect would produce. The gate therefore fails to validate the revised recipe,
and the recipe cannot be called corrected. We have no recipe known to raise
accuracy, so the loop’s decline cannot be attributed to self-training or to the
veriﬁer. The veriﬁer-ﬁltered loop loses pass@1 in all three seeds (4.8, 3.2, 4.2
points; two intervals exclude zero) and sample accuracy in all three (intervals
exclude zero for seeds 2 and 3). The mean pass@1 change over the three seeds is
−4.1 (t interval [−6.1, −2.1]), and −4.5 for sample accuracy ([−8.1, −1.0]). The
loop does not help; the point estimates are negative in all three seeds, but the
sample is three seeds with one exam draw and one rate, so we do not claim that
it costs accuracy, and we did not isolate the cause. The detectable eﬀect is about
6 points of pass@1 (2.8h/1.96), against about 10 before.


12
T. S. Nguyen and D. A. Tran
Injected bias. As intended positive controls for the audit (neither turns out
to be one) we reran the loop once each (seed 1, 10−4) with a selection veriﬁer
that rejects \boxed answers (exam veriﬁer clean). In the ﬁrst, a hash-chosen
30% of problems are aﬀected: the \boxed share falls 4.9 points on them and 3.1
on the others (diﬀerence −1.8, [−7.4, 3.8]); a hash cannot be learned from the
problem, so this control could not elicit selective avoidance. In the second the
rule is visible: every \boxed answer is rejected when the gold contains \frac
(49 of the 300 selection problems, 263 examples kept instead of 298; 70 of the
500 exam problems, where the shares below are measured). The share on those
problems stays at 95.0% and on the others goes from 90.2% to 87.4% (diﬀerence
+2.8, [−2.8, +8.3]), against −3.7, −2.7 and −5.5 for the same split in the three
unbiased seeds, a shift in the direction opposite to avoidance; pass@1 falls 7.0
points ([−11.2, −3.0]), more than in the unbiased seeds, which we do not interpret
(one run). In neither run does the \boxed share fall selectively where boxing is
penalised, so neither validates the audit.
5
Discussion
5.1
Answer to the Research Question
Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k with an interval excluding zero, at any rate; in the 500-problem ﬁnal
round pass@1 falls 3.2–4.8 points in each of three seeds. The sample-accuracy
ﬁgure of about 2.2 points is the largest upper limit among observed intervals, a
post hoc ﬁgure that omits seed variance, not a power statement; on the pre-set
measures the design could detect only about 10 points of pass@1 and 8–10 of
pass@k (6 and 5 in the ﬁnal round). Because no arm improves and the positive
gate failed, the null belongs to this recipe, and the study cannot say whether
self-training in general helps. Every score except the ﬁnal-round check below
is graded by the veriﬁer that selects the data (re-scoring ﬁve runs, three self-
training and two train-on-gold, with V ′ leaves the decline in place, Section 3).
On the ﬁnal-round generations a second grader (normalised string match of the
last \boxed against the gold, no math-verify; indep_grade.py) gives pass@1
changes of −3.6, −2.2, −4.6 for the three seeds (−30.0 for the gold arm) and
sample-accuracy changes of −2.5, −5.5, −5.3 (same sign and size). It reads only
the last \boxed, so a falling boxed share lowers both graders, and it does not
rule out a format artefact in the gate. Earlier runs are not independently graded.
Does it learn to write what the veriﬁer accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably
(largest rise +0.7 [−6.7, +8.0]), so its silence is no evidence either way; no run
varies the frequent gold-storage defect, and the audit of Section 5.3 is too weak.
5.2
Interpretation
One explanation of the Design P curves is a self-reinforcing shrinking pool shaped
by the biased veriﬁer. The data neither support nor rule it out: the patch tests