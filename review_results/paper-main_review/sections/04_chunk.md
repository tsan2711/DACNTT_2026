
4.5   Anatomy of the Decline
This subsection is post hoc and descriptive. Sample accuracy mixes whether a ﬁn-
ished solution is right with whether the model ﬁnishes within the 512-token cap
at all. Re-tokenising the saved text, we call a generation cap-hit at ≥ 508 tokens.
The untrained model already hits the cap in 41–48% of MATH-500 generations,
so the cap binds from the start. An earlier character-length proxy for unﬁnished
generations overstated termination, because drifting prose crosses its threshold
within the same token budget. At 5 × 10−4 , compared with the untrained model
on the same problem mix, ﬁnished generations lose 5.5–10.6 points, with in-
tervals excluding zero in ﬁve of six runs (the six include two same-seed A/B
pairs, which are close to replicates), while the cap-hit share rises 2–14 points.
The matched measure assumes that a problem’s round-0 ﬁnished accuracy is
the right baseline for the samples that still ﬁnish, and it conditions on which
problems ﬁnish after training, so it is descriptive. A three-part decomposition
attributes 12–30% of the decline to the cap share in the three original seed-1 runs
(and −2 and 5% in the replicate and the 1,024-limit run) and 52–72% at seed 2
(Table ??, Supplementary Appendix ??). At 10−4 and 2×10−4 the cap-hit share
does not rise and ﬁnished accuracy carries the whole change. Train-on-gold is
diﬀerent: responses shorten by more than half and ﬁnished accuracy collapses.
Retraining without truncated examples changes little within the noise of single
                                              Mathematics or the Veriﬁer?      11

runs; re-scoring adapters at a 1,536-token cap leaves their deﬁcit in place, and
the character proxy there points to generations that do not stop rather than to
less accurate ﬁnished ones (Supplementary Appendix ??).


5     Discussion

5.1   Answer to the Research Question

Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k by an amount whose interval excludes zero, at any rate, and the
sample-accuracy intervals exclude gains above about 2.2 points. The bound is
loose: it is read oﬀ observed intervals rather than a pre-speciﬁed equivalence
test, uses a measure chosen after the runs (on pass@1 and pass@k the upper
ends reach +8.0 and +7.3), and omits training-seed variance. On the pre-set
measures the design could detect only gains of about 10 points of pass@1 and
8–10 of pass@k, so “no gain” means no gain of that size. In every MATH-500
run but one the problems lost equal or outnumber those gained, which restates
the sign of the pass@k change rather than adding evidence. Because no arm
improves, including training on reference solutions, the null may be a property
of this LoRA recipe rather than of self-training.
    Does it learn to write what the veriﬁer accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably (the
largest rise is +0.7 [−6.7, +8.0]), so the rule’s silence is not evidence against
veriﬁer-style learning. The \boxed share falls in a way imitation and drift would
both produce. The post hoc audit of Section 5.3 ﬁnds no sign of adaptation to
the gold-storage defect, but it is too weak to rule adaptation out.
    What happened to the pooled collapse? It does not reproduce when each
dataset has its own adapter and is scored on held-out problems. Because the
pooled design also trained on about 4.5× more examples per round, we cannot
say whether pooling, selection-set scoring or dose produced it.


5.2   Interpretation

An earlier version explained the Design P curves by a self-reinforcing shrinking
pool shaped by the biased veriﬁer. The data neither support nor rule it out: the
patch tests how strong a rare bias is, not whether a frequent bias compounds;
the no-ﬁlter control declines without any veriﬁer but with more dose. The de-
fensible statement is narrow: removing a format defect present in under 1% of
generations, or removing the ﬁlter entirely, made no consistent diﬀerence at the
resolution of this setup. The frequent gold-storage defect was never varied, so
whether systematic false negatives are harmless in general, as Egashira et al. ﬁnd
for RLVR, our data cannot say; and the no-ﬁlter control admits unstructured
wrong answers, not the systematic false positives they ﬁnd harmful, so it does
not test that side either. Practices our experience suggests, none of them tested
here, are listed in Supplementary Appendix ??.
12      T. S. Nguyen and D. A. Tran

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
its own (Table 4; rt_audit.py in the repository). For the gold-storage defect it
falls in all three self-training runs we re-scored, by 2.6, 2.6 and 1.5 points, with
intervals reaching or just touching zero. But V ′ diﬀers from V only on boxed
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
    (ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table ??, Sup-
plementary Appendix ??). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.
    (iii) Check the dose of a control before running it. Count how many training
examples the treatment changes. Our \dfrac patch changed 0–4 examples, while
the unvaried gold-storage defect would have changed about a ﬁfth of the pool
                                                        Mathematics or the Veriﬁer?         13