### 5.1 Answer to the Research Question
Does the model get better at mathematics? Not detectably. No run raises pass@1
or pass@k by an amount whose interval excludes zero, at any rate, and the
sample-accuracy intervals exclude gains above about 2.2 points. The bound is
loose: it is read offobserved intervals rather than a pre-specified equivalence
test, uses a measure chosen after the runs (on pass@1 and pass@k the upper
ends reach +8.0 and +7.3), and omits training-seed variance. In every MATH-
500 run but one, the problems lost equal or outnumber those gained.
Does it learn to write what the verifier accepts? The data cannot settle this.
The pre-set pattern requires pass@1 to rise, which never happens detectably (the
largest rise is +0.7 [−6.7, +8.0]), so the rule’s silence is not evidence against
verifier-style learning. The \boxed share falls in a way imitation and drift would
both produce. The one direct test, the direction-free test of Section 5.3, points
away from adaptation for one defect class: the share of correct answers the gold-
storage defect rejects does not fall over rounds.
What happened to the pooled collapse? It does not reproduce when each
dataset has its own adapter and is scored on held-out problems. Because the
pooled design also trained on about 4.5× more examples per round, we cannot
say whether pooling, selection-set scoring or dose produced it.