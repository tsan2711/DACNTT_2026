Because no earlier arm improved, we ran one last round with the recipe changes
a reviewer asked for: loss on the completion only, LoRA on all linear layers, a
1,024-token cap and training limit, normalised gold answers, and a pool of 300
problems from the MATH training split, so that the exam is all 500 MATH-500
problems. It is one seed at 10−4 with k = 2 and two rounds. The veriﬁer-
ﬁltered loop (298 examples kept) is compared with training on the 300 reference
solutions, a positive gate that must raise accuracy for the recipe to count as
able to help. Intervals are paired problem-level bootstrap intervals over the 500
problems (10,000 resamples).


Table 4. Final round, MATH-500 (500 exam problems, k = 2, 10−4 , one seed). Change
from the untrained model to round 1 in points, with 95% paired problem-level bootstrap
intervals that omit training-seed variance.

Arm                       pass@1               pass@2            Sample acc.
Untrained                   49.2                 59.4                  –
Veriﬁer-ﬁltered loop −4.8 [−9.0, −0.6]    −3.0 [−6.8, +0.6]     −2.9 [−5.8, 0.0]
Train on gold       −32.2 [−36.8, −27.6] −32.0 [−36.6, −27.2] −30.2 [−33.8, −26.6]



    The gate fails. Training on reference solutions lowers pass@1 from 49.2%
to 17.0%, and the model adopts the reference style ($-delimited spans in 60 of
1,600 generations at round 0, 1,577 at round 1), as in the earlier train-on-gold
arms. An earlier gate at 5 × 10−4 with the same recipe also failed (−30.5 points
of pass@1). The corrected recipe therefore still has no positive reference, so we
stopped. The veriﬁer-ﬁltered loop loses 4.8 points of pass@1, with an interval
that only just excludes zero and a pass@2 interval that includes it; with one seed
we read it as no gain and a possible small decline, as at 10−5 . Half-widths of
about 4 points of pass@1 give a detectable eﬀect of about 6 points (2.8h/1.96),
against about 10 on the 150-problem exams.


5     Discussion

5.1   Answer to the Research Question

Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k by an amount whose interval excludes zero, at any rate; in the 500-
problem ﬁnal round (Section 4.6) pass@1 falls 4.8 points. On the 150-problem
exams the sample-accuracy intervals exclude gains above about 2.2 points, but
that bound is read oﬀ observed intervals, uses a measure chosen after the runs
and omits training-seed variance; on the pre-set measures the design could detect
only about 10 points of pass@1 and 8–10 of pass@k (6 and 4 in the ﬁnal round).
Because no arm improves, and training on reference solutions failed the positive
12      T. S. Nguyen and D. A. Tran

gate twice, the null may be a property of this LoRA recipe rather than of self-
training.
    Does it learn to write what the veriﬁer accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably (the
largest rise is +0.7 [−6.7, +8.0]), so the rule’s silence is not evidence against
veriﬁer-style learning. The \boxed share falls in a way imitation and drift would
both produce. The post hoc audit of Section 5.3 ﬁnds no sign of adaptation to
the gold-storage defect, but it is too weak to rule adaptation out.
    What happened to the pooled collapse? It does not reproduce when each
dataset has its own adapter and is scored on held-out problems; since the pooled
design also trained on about 4.5× more examples per round, we cannot say
whether pooling, selection-set scoring or dose produced it.


5.2   Interpretation

An earlier version explained the Design P curves by a self-reinforcing shrinking
pool shaped by the biased veriﬁer. The data neither support nor rule it out: the
patch tests how strong a rare bias is, not whether a frequent bias compounds,
and the no-ﬁlter control declines without any veriﬁer but with more dose. The
defensible statement is narrow: removing a format defect present in under 1% of
generations, or removing the ﬁlter entirely, made no consistent diﬀerence at the
resolution of this setup. The frequent gold-storage defect was never varied, and
the no-ﬁlter control admits unstructured wrong answers, not the systematic false
positives Egashira et al. ﬁnd harmful, so neither tests their ﬁndings for RLVR.
Untested practices are listed in Supplementary Appendix ??.


5.3   A Proposed Audit for GVT with a Biased Veriﬁer

Our pre-set reading rule failed in a predictable way: it tied “learning the veriﬁer’s
style” to rising accuracy, so it could not speak once accuracy fell. From the
analyses we added after the runs we propose four checks for self-training with
a rule-based veriﬁer. All four were deﬁned post hoc here; we oﬀer them as a
protocol for future studies, not as tested methods.
    (i) A per-round false-reject audit. Fix a repaired veriﬁer V ′ that corrects a
known defect class of the training veriﬁer V . At each round t, on the loop’s own
generations, compute

                          #{accepted by V ′ but rejected by V }
                   rt =                                         .
                                  #{accepted by V ′ }

If the model learns to write what V accepts, rt should fall over rounds, whatever
happens to accuracy. This is the per-step false-negative tracking of RLVR stud-
ies [4,16] applied to oﬄine SFT. Our data show that overall rt is not enough on
its own (Table 5; rt_audit.py in the repository). For the gold-storage defect it
falls in all three self-training runs we re-scored, by 2.6, 2.6 and 1.5 points, with
intervals reaching or just touching zero. But V ′ diﬀers from V only on boxed
                                                       Mathematics or the Veriﬁer?         13

predictions, so unboxed correct answers enter only the denominator, and the
fall matches the falling \boxed share among correct answers (91 → 76% and
93 → 78% at 5 × 10−4 ). On boxed answers alone rt is ﬂat (changes −0.4 to +0.7
points). The defect is also bound to the problem: it ﬁres on only 54–62 of the
500 problems, where it rejects 94–98% of correct answers in every round, and
29–34 of them have a gold that V cannot parse, so no answer form could escape
it there. On the 24–28 aﬀected problems where some form could, rt moves by
−5.5, −1.6 and −0.2 points, with intervals 10–26 points wide. A model adapting
to the defect would have to write these answers unboxed, and the training pool
holds only 2–12 examples per round from these problems that do so. Under SFT
the pressure to adapt is therefore weak, and we have no positive control showing
the audit would detect adaptation that did occur. We conclude only that we
see no adaptation to this defect, in one defect class, three runs and three to ﬁve
rounds. Train-on-gold, with no veriﬁer in the loop, gives rt rises of 2.1–3.3 points
as its outputs become more boxed, a reminder that rt moves with format for
reasons unrelated to the veriﬁer. For the test to be informative, rt should be
reported on the subset of answers and problems where V and V ′ can diﬀer and
an accepted form exists, with a count of the training examples that could teach
the avoidance.



Table 5. The false-reject audit for the gold-storage defect (post hoc), in percent (all 500
problems), round 0 → last round, with the change and a 95% problem-level bootstrap
interval (2,000 resamples). “Boxed only” restricts to predictions containing \boxed;
“aﬀected, parseable” to problems where the defect ever ﬁres and V can parse the gold.
Pool: examples per round from aﬀected problems that V accepts (and so avoid the
defect).