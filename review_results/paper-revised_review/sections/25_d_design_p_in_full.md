## D Design P in Full
Table 2 reports pass@1 and pass@8 for both models over five rounds of the
pooled design, as computed during the run (where the two verifier presets gave
identical pooled values; a later per-dataset recomputation differs by one prob-
lem, see Table 9). The 1.5B decline is severe and accelerating; the 0.5B decline
is small (−3.7 and −5.6 points). Splitting the 1.5B run by dataset (Table 9)
shows both datasets falling heavily, although GSM8K has a measured 0% false-
negative rate, though that rate was measured on external solutions in the un-
trained model’s style, not on Design P’s late-round outputs. The accepted pool
also contracts every round (1.5B: 3,962, 3,730, 3,395, 2,638, 1,566; 0.5B: 2,533 to
2,123; experiments/viec3/review_cpu/dot4/poolP.py) and the 1.5B output
style shifts, with \boxed{} falling from 5,608 to 2,693 of 8,000 generations while
dollar-delimited math rises from 1,453 to 3,406.
Design P cannot be interpreted causally, for three reasons. First, each round
trains one adapter on the union of both datasets’ accepted solutions, of which
GSM8K supplies 68.4–70.2% in every round, so either dataset’s trajectory is a
joint function of both pools. Second, it scores each round on the problems it
also used to select training data. We expected this to raise later-round scores,
if anything. Design I lets us check that expectation, since it also generates on
its 350 selection problems: there, Run A’s sample accuracy on the selection

22
T. S. Nguyen and D. A. Tran
problems falls as much as or more than on the exam at the two higher rates
(e.g. Run A at 5 × 10−4: −8.2 and −5.3 points against −8.3 and −4.7 on the
exam; at 10−4, seed 1: −6.2 against −1.5; no intervals); at 10−5 it falls slightly
less (−1.0 and −1.1 against −2.4 and −1.4), and Run C’s selection problems
fall less at 5 × 10−4 (−11.3 against −15.4) and slightly more at 10−5 (−13.8
against −13.0). Training on a problem’s own accepted solutions therefore did
not protect it, so selection-set scoring is unlikely to have masked a decline; since
the selection problems sometimes fall more, it may have enlarged one, and it
remains a candidate contributor. Third, and not anticipated when we designed
the follow-up, Design P trains on far more examples per round: 3,962 at round 0
for the 1.5B model, against 872 for the isolated MATH-500 run at the same
learning rate. With one epoch and the same batch size this is about 4.5× as
many optimizer steps (Design P’s training logs were not saved, so this is inferred
from pool size). Section G suggests, on the evidence of one seed, that a higher
learning rate produces more decline, with a falling \boxed share as here (pass@1
falls faster than pass@k in only two of its four runs at 5 × 10−4), and Run C,
which takes about twice Run A’s steps per round at the same rate, is the one
10−5 run that declines clearly. One reading consistent with these data is that
Design P’s adapter changed the model more. It rests on two assumptions we have
not tested: that more optimizer steps act like a higher learning rate, and that
Run C’s decline comes from its dose rather than its dataset (a single comparator).
Dose also explains at most the level of the decline, not its time course: with a
fresh adapter each round, the round-t model is trained on the round-(t −1)
pool alone, and the pools shrink, yet the largest pass@1 drops (−12.1 and −13.8
points) come from the two smallest pools (3,395 and 2,638). Something carried
through the data, such as pool composition or style, fits this acceleration better.
The 0.5B model, trained on 2,533 examples at round 0 (about 2.9× Run A),
declines only a little, though it is a different model. Pooling or scoring may also
have contributed; no run separates these explanations.