
Mathematics or the Veriﬁer?
7
runs and seeds, not on single intervals. Single proportions use Wilson intervals.
Detectable eﬀects. From the interval half-widths h in Table 2, a change would be
detected with 80% power at the 5% level only if it exceeded about 2.8 h/1.96:
about 10 points of pass@1, 8–10 of pass@k and 3.5–5.5 of sample accuracy on
MATH-500. Because h omits training-seed variance (the replicate pair diﬀers
by 3.2 points and B minus A ﬂips from +5.3 to −7.3 on near-identical pools,
Section 4.4), these are lower bounds: a null here means no gain of at least that
size, probably larger (Supplementary Appendix C).
4
Results
4.1
Design P: An Apparent Collapse
In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 50.0% →18.6%, pass@8 72.6% →48.6%; Table S3, Supplementary
Appendix D), on both datasets (Table S2); the 0.5B decline is small. The ac-
cepted pool contracts every round and \boxed{} falls from 5,608 to 2,693 of
8,000 generations. This design cannot be read causally: one adapter trains on
both datasets’ pools; it scores on the problems it selects from; and it trains on
about 4.5× as many examples per round as the isolated MATH-500 run (3,962
against 872 at round 0). No run separates these explanations (Supplementary
Appendix D).
4.2
Design I at 10−5: Small Declines, a Larger One on GSM8K
On the held-out exam (Fig. S1 and Table S5 in Supplementary Appendix E)
pass@8 ends within 4 points of round 0 in every run. On MATH-500, pass@1
is 2.7–4.0 points lower at round 4, with every interval including zero (Table 2);
sample accuracy falls 1.2–3.2 points, with an interval excluding zero only for
B at seed 0 (A at seed 0 reaches 0.0), and matched ﬁnished accuracy 1.1–4.2,
with intervals that only just exclude zero for A and B at seed 0, which are close
to one replicate. We read this as a possible small decline, not an established
one; what we do not see is a gain of the size the design could detect. Run C
(GSM8K) declines more: pass@1 falls 12.7 points ([−21.3, −4.0]), almost all in
ﬁnished accuracy, but it took about twice Run A’s optimizer steps, so we do not
attribute this to the dataset alone. On MATH-500 two coarse output statistics,
length and cap-hit share, barely change, which is weak evidence that the adapter
did little (Supplementary Appendix E).
4.3
The Patch Control Could Not Detect an Eﬀect
Runs A and B diﬀer only in the \dfrac/\tfrac patch. At round 4, B minus
A is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and +0.0 [−2.7, +2.7] at
seed 1 (recomputed from the saved generations; Table 2 lists values from the
run logs that diﬀer by one problem, giving −0.7). This null is uninformative:


8
T. S. Nguyen and D. A. Tran
\dfrac appears in 0.50–0.73% of generations, so the kept pools diﬀer by 3–4
examples (under 0.5% of the 872-example pool), and at 10−5 the adapter changes
the outputs little anyway. Removing one rare format defect had no detectable
eﬀect, which a prevalence count alone predicts; the frequent gold-storage defect
is present in both arms.
4.4
Higher Learning Rates
Because 10−5 changed the MATH-500 outputs little, we reran Run A at 10−4
(three seeds), 2×10−4 (two) and 5×10−4 (two, with Run B), with three rounds
and k = 4 (Table 1). These runs diﬀer from the 10−5 runs in k, rounds, pool
size and the pass@k metric as well as rate, so only 10−4 to 5 × 10−4 isolates
the rate. At 5 × 10−4 every run declines: pass@1 falls 4.0–11.3 points and the
sample-accuracy intervals exclude zero in all four A/B runs, though same-seed A
and B are closer to two replicates than four. The decline may grow with the rate
on one seed: at seed 1 sample accuracy falls 1.5, 3.5 and 8.3 points across the
three rates, at seed 2 an almost ﬂat 3.7, 3.8 and 4.7. The cap-hit share rises only
at 5 × 10−4. The patch has no consistent eﬀect: B minus A in round-2 pass@1
is +5.3 at seed 1 and −7.3 [−14.0, −0.7] at seed 2, a sign ﬂip from pools that
diﬀer by 0–3 examples: trajectory noise. Style does not separate imitation from
drift: boxed share falls with the pool, which both would produce.
Table 1. Run A (MATH-500, original veriﬁer, k = 4, three rounds) across learning rates
and seeds: pass@1, pass@4 and sample accuracy (600 exam generations) at round 0
→round 2, the share of round-2 generations that hit the 512-token cap (decoded text
re-tokenised to ≥508 tokens; round 0 is 43.0–43.2%, 48.2% at seed 3), and problems
added/lost summed over rounds 1–2. The two 5×10−4 rows are the A rows of Table S6.
Rate
Seed
pass@1
pass@4
Sample acc. Cap-hit (R2) Added/lost
10−4
1
33.3 →34.0 50.0 →49.3 33.7 →32.2
42.7%
20/21
10−4
2
31.3 →28.0 51.3 →45.3 30.8 →27.2
42.8%
25/34
10−4
3
29.3 →26.7 40.0 →41.3 28.5 →27.5
45.7%
16/14
2 × 10−4 1
33.3 →31.3 50.0 →46.7 33.7 →30.2
40.8%
23/28
2 × 10−4 2
31.3 →25.3 51.3 →45.3 30.8 →27.0
39.7%
21/30
5 × 10−4 1
33.3 →23.3 50.0 →42.7 33.7 →25.3
46.2%
22/33
5 × 10−4 2
31.3 →27.3 51.3 →44.7 30.8 →26.2
51.2%
26/36
Two controls at 5 × 10−4. The no-ﬁlter run trains on all k samples of every
selection problem (1,400 examples per round), removing the veriﬁer; the train-
on-gold run trains on the 350 reference solutions every round (Table 3). Neither
is a single-variable control: no-ﬁlter takes 3–4× Run A’s optimizer steps, train-
on-gold about the same. Removing the ﬁlter is not better than keeping it beyond
noise and is lower on pass@4 at both seeds (round-2 diﬀerences −2.0 and −5.3