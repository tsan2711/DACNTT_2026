### I.1 Answer to the Research Question
Does the model get better at mathematics? Not detectably. On held-out problems
no run raises pass@1 or pass@k by an amount whose interval excludes zero, at
any of four learning rates, and the sample-accuracy intervals exclude gains larger
than about 2.2 points. This bound is loose on three counts: it is read offthe
observed intervals, not a pre-specified equivalence test; it uses sample accuracy,
which we chose as primary after the runs (on the pre-set pass@1 and pass@k the
upper ends reach +8.0 and +7.3); and the intervals omit training-seed variance,
which is of the same size (a replicate of Run A at 5 × 10−4, seed 1, ends 3.2
points of sample accuracy away). In every MATH-500 run except 10−4 seed 3
(16/14) the problems lost over the rounds equal or outnumber the problems
gained (Table 4; 10−5 runs: 20/21 to 32/34 over four transitions), which restates
the sign of the pass@k change rather than adding evidence. Most per-problem
movement is churn: about 2 to 25 problems are gained and about as many lost
per round even where the averages barely move.
Does it learn to write what the verifier accepts? The data cannot settle this.
The pattern fixed in advance for this reading (pass@1 up, pass@k flat, style
converging) requires pass@1 to rise, so it cannot fire in runs where accuracy
falls, and pass@1 never rises detectably (the largest rise is +0.7 [−6.7, +8.0],
at 10−4, seed 1); the rule is one-sided and its silence is not evidence against
verifier-style learning. Its style leg, the pre-set \boxed share, was evaluated on
its own and also fails: in self-training the share does not converge but falls (all
2,000 generations per round: 52% →36% and 54% →37% at 5×10−4, Table 10;
the 600 exam generations: 55.5% →38.3% and 58.5% →42.5%). The post hoc
refinements do not settle it either. The kept pool (89–91% boxed at round 0) is
less boxed than the finished exam generations it is compared with (95.6% and
98.5%), and the finished share falls (69.7% and 82.9%) as the pool’s does (73–
77% by round 2). That is what imitation of the pool would predict as well as

32
T. S. Nguyen and D. A. Tran
what drift would, so the share does not discriminate. The one direct test we have
points away from adaptation for one defect class: the fraction of correct answers
the gold-storage defect rejects stays at 15.5–18.4% in every round (Section B).
It is also not a clean measure of what the verifier prefers, because the gold-
storage defect (Section B) penalises some \boxed answers. The one strong style
convergence ($ spans 5% →98%, \boxed 52% →86%) happens under train-
on-gold, with no verifier in the loop and with falling accuracy: style converging
alone, which by our rule says nothing about verifier-style learning.
What does change? In this post hoc description, most clearly at the highest
rate, the model gets less accurate on the solutions it does finish. The matched
intervals exclude zero in five of six MATH-500 runs at 5×10−4, in both GSM8K
runs (10−5 and 5 × 10−4) and, on MATH-500 at 10−5, only just, for A and
B at seed 0, which are close to one replicate; at 10−4 and 2 × 10−4 the point
estimates are negative but the intervals include zero (both GSM8K figures are
single runs). More generations run into the token cap only at 5 × 10−4: by 2–14
points in the four verifier-filtered runs and two no-filter controls on MATH-500,
with intervals excluding zero at seed 2 and for one run at seed 1, and not in
a replicate; the change in cap-hit share accounts for 12–30% of the decline at
seed 1 and 52–72% at seed 2 (Table 7). At lower rates the cap-hit share changes
by −3.3 to +1.1 points. The untrained model already hits the cap in 41–48% of
MATH-500 generations, so the cap limits every round.
What happened to the pooled collapse? It does not reproduce when each
dataset gets its own adapter and is scored on held-out problems. Because the
pooled design also trained on about 4.5× more examples per round, and our
higher-rate runs suggest (on one seed) that stronger training produces larger
declines, which are at least compatible with a dose effect (we did not apply the
measures of Section H to Design P, and its acceleration under shrinking pools
is not explained by dose, Section D), we cannot say whether pooling, selection-
set scoring or training dose produced it. We no longer claim that pooling and
selection-set scoring “manufactured” the collapse.