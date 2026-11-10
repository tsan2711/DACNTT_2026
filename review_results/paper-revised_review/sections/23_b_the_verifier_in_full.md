## B The Verifier in Full
Format probe. We re-rendered gold answers from GSM8K and MATH-500 in
individually valid formats (bare number, trailing-zero decimal, \frac, \dfrac,
\tfrac, boxed, dollar-delimited, sentence, with units) and asked the verifier to
grade them against the original gold. On GSM8K plain rewrites are never re-
jected, while \dfrac/\tfrac are rejected 200/200 (the command is not parsed).
On MATH-500, \dfrac/\tfrac are rejected 146/146 (100%), trailing-zero dec-
imals 13/22, and boxed forms 41/200. Of those 41, 24 are gold answers our
pipeline stores in forms the verifier cannot parse at all, so part of this figure
measures our gold storage, not the verifier. The other 17 (17 of the 200 boxed
probes, 8.5%) are compound answers such as 3
√
13: the gold is stored with-
out a delimiter, and math-verify applies its full LATEX extraction only inside
\boxed{} or $...$, so the bare gold is parsed to its first number and no longer
matches a correct boxed prediction.
False-negative rate on real solutions. We took one public solution per problem
for the first 200 problems of each dataset (teacher traces for GSM8K, Qwen2.5-
7B-Instruct rollouts for MATH-500), not the 1.5B model’s own outputs. Correct-
ness was established by a scripted comparison of the boxed answer with the gold
string after normalisation (src/dacntt/read.py: delimiters, braces, spaces and
commas removed, \dfrac/\tfrac read as \frac, simple fractions compared by
value), and we then counted how many of these correct solutions the verifier re-
jects. The false-negative rate is 7.8% on MATH-500 (10 of 128 correct solutions;
24 problems with unparseable gold excluded) and 0% on GSM8K (0/200; 95%
Wilson interval 0–1.9%, one-sided upper bound 1.3%), identical for the default
and reward extraction presets of math-verify. Of the ten MATH-500 cases,
eight are rejected when the whole solution is verified but accepted when only
the boxed answer is, which we labelled wrong-token extraction from a long so-
lution, and two are rewrites the normalisation equates but the verifier does not
match (e.g. 6 + 9i for 6+9i). Most of the eight are compound answers (3
√
13,
6 −5i, 11
√
2, a list, a polynomial), so they overlap with the compound class of
the format probe; the two labels describe where the failure shows, not exclu-
sive causes. The 7.8% estimates the false-negative rate on Qwen2.5-7B-Instruct
solutions for problems whose gold the verifier can parse, among answers our
normalisation recognises as correct. Correct answers in forms it does not equate
are left out of the denominator, and the 24 problems with unparseable gold are
counted as a separate defect below; relative to the loop’s own rate, where the
1.5B model writes longer and, after training, less boxed solutions, the direction
of the difference is not known. The audit also inspected only rejected solutions,
so it cannot measure the false-positive rate; that the verifier rarely accepts wrong
answers is an assumption here, not a measurement.

Mathematics or the Verifier?
19
Unparseable gold in the loop. Over all 500 MATH-500 problems the verifier
cannot parse 51 stored gold answers (10.2%); 11–18 of them fall in each 150-
problem exam partition. The loop keeps these problems: every sample is rejected,
so they never enter the training pool and always count as unsolved. They lower
absolute pass rates by up to 12 points but are constant within a partition, so
they cancel in within-run and same-partition comparisons. Wrapping the gold
in \boxed{}, the re-score described below, makes 46 of these 51 golds parseable,
so the two corrections overlap and should not be added (experiments/viec3/
review_cpu/dot4/unparsed.py).
The patch. For the control we repaired the most severe identified failure
mode with a normalisation pass that rewrites \dfrac and \tfrac to \frac
before parsing, removing the 100%-rejection class and nothing else. The patched
verifier is therefore still biased: it keeps the wrong-token extractions (8 of the 10
audited false negatives) and the gold-storage defect.
The gold-storage defect in the loop’s own outputs (post hoc). After the runs
we re-scored the saved generations with a second normalisation that wraps
the gold in \boxed{} when the prediction contains one and the gold does not
(experiments/viec3/review_cpu/: patch_dose.py, dose.py, flips.py). This
defect is far more frequent than the \dfrac class. Over all 500 problems it rejects
15.5–18.4% of the generations the re-scored verifier accepts (Run A at 5 × 10−4,
seeds 1 and 2, and at 10−5, seed 0, every round). The kept pool covers only
the 350 selection problems, where the share is about the same (17.8–18.8% at
round 0): accepting these generations would enlarge the round-0 pool by about
a fifth (Run A at seed 1: 440 →542, +23%; at 10−5: 872 →1,066, +22%),
against 0–4 examples (under 1%) for the \dfrac patch. In a hand check of 30
random flips, 29 pairs were the same value written differently (e.g. \frac43 and
\frac{4}{3}; one prediction had an empty box). The 15.5–18.4% assumes that
the re-scored verifier itself accepts no wrong answer, which we did not measure.
On the exam set the defect lowers absolute pass@1 by 6.7–8.0 points at round 0
and throughout the 10−5 runs, by 4.7 points at round 2 under 5 × 10−4, and
by 0.7–3.3 points for train-on-gold after round 0. The absolute offset is there-
fore not constant, but as a share of re-scored pass@1 it roughly is (6.7/40.0 and
4.7/28.0, both 17%, for Run A at seed 1; 20% throughout at 10−5): the defect
rejects about the same fraction of correct answers in every round, and the ab-
solute offset shrinks because accuracy falls. Two consequences follow. With the
original verifier the declines below are understated, by a factor of about 0.73–
0.78 (the ratios of original to re-scored sample-accuracy changes below), and the
same factor shrinks every original-verifier difference and interval, including the
2.2-point bound on gains, which on the re-scored scale is nearer 3 points. And
the fraction of correct answers this defect rejects does not fall over the rounds,
so for this one defect class the model does not learn to avoid what the verifier
rejects; this is the only direct test of verifier adaptation we have, and it covers
one defect. We keep the original verifier’s numbers in every table, since that is
the verifier the loop trained with; they are therefore 4.7–8.0 points too low in
absolute terms for self-training. Re-scored, with paired bootstrap intervals as in

20
T. S. Nguyen and D. A. Tran
Section 3.4, sample accuracy changes by −10.7 [−14.8, −6.7] and −6.0 [−9.7,
−2.2] points for Run A at 5 × 10−4 (seeds 1 and 2; original verifier −8.3 and
−4.7), by −3.3 [−5.9, −0.7] for Run A at 10−5, seed 0 (original −2.4), and
by −24.7 and −22.0 for train-on-gold. In pass@1 the same runs go from 40.0%
to 28.0% and from 38.0% to 32.0% (interval [−14.0, +2.0] for the latter), from
40.0% to 36.7%, and from 40.0% to 16.0% and from 38.0% to 13.3%. Only these
five runs were re-scored, three of them self-training; that the other runs’ declines
would also survive a re-score is an extrapolation from these three. Both arms of
the patch control (Section F) carry this defect.