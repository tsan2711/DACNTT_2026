## H Anatomy of the Decline in Full
Everything in this subsection is post hoc: the cap-hit measure, the matched
metric and the decomposition were defined after the runs, to explain the de-
clines, and they describe the declines rather than identify causes. Sample-level
accuracy mixes two things: whether a model that finishes a solution gets it
right, and whether it finishes within the 512-token cap at all. Token counts were
not saved at generation time, so we re-tokenised the saved decoded text with
the model’s tokenizer and call a generation cap-hit if it has at least 508 to-
kens (experiments/viec3/review_cpu/caphit.py, capanat.py); the margin
allows for small differences between generated and re-encoded token sequences.
The threshold matters little: few generations fall near it (at most 37 of 600 per
run and round have 480–507 tokens), a threshold of 500 raises the cap-hit share
by at most about 2 points and one of 512 lowers it by at most about 4.0, and
with either the share still rises only at 5 × 10−4. The untrained model already

28
T. S. Nguyen and D. A. Tran
Table 11. What the decline consists of (MATH-500, exam generations, round 0 →
last round). “Cap-hit” is the share of generations whose decoded text re-tokenises to
≥508 tokens; “finished acc.” is sample accuracy on the other generations, unadjusted;
“matched ∆” is last-round finished accuracy minus the untrained model’s finished
accuracy on the same problem mix (intervals in Table 5). “Trunc.” is the percentage of
the round-0 training pool longer than the 512-token training limit. The first six rows
are at 5 × 10−4, then 2 × 10−4 and 10−4; the 10−5 rows are the original runs (k = 8,
round 0 →round 4, not comparable in dose); the last two rows (train on gold) are at
5 × 10−4.
Run
Seed Length (chars) Cap-hit (%) Fin. acc. (%) Matched ∆Trunc.
A (orig.)
1
1175 →1678
43.2 →46.2
54.0 →43.0
−9.1
24.5
B (patched)
1
1175 →1659
43.2 →47.8
54.0 →46.3
−6.8
24.6
A (orig.)
2
1154 →1641
43.0 →51.2
50.6 →45.4
−5.5
24.5
B (patched)
2
1154 →1728
43.0 →54.0
51.2 →44.2
−5.9
24.5
No filter
1
1175 →1668
43.2 →45.5
54.0 →43.1
−10.6
62.4
No filter
2
1154 →1755
43.0 →57.2
50.6 →43.6
−6.6
—
A, 2 × 10−4
1
1175 →1433
43.2 →40.8
54.0 →46.5
−4.0
24.5
A, 2 × 10−4
2
1154 →1431
43.0 →39.7
50.6 →41.7
−4.7
24.5
A, 10−4
1
1175 →1276
43.2 →42.7
54.0 →48.5
−4.3
24.5
A, 10−4
2
1154 →1284
43.0 →42.8
50.6 →44.6
−3.5
24.5
A, 10−4
3
1178 →1355
48.2 →45.7
50.2 →47.5
−0.6
—
A, 10−5
0
1158 →1147
46.9 →47.4
54.8 →51.0
−3.8
—
A, 10−5
1
1158 →1146
40.7 →41.8
55.2 →54.3
−2.3
—
Train on gold
1
1175 →485
43.2 →7.2
54.0 →14.7
−25.6
17.4
Train on gold
2
1154 →516
43.0 →8.3
50.6 →12.5
−25.9
—
hits the cap in 40.7–48.2% of its MATH-500 exam generations, depending on
partition and sampling (43.0–43.2% on the k = 4 seed-1 and seed-2 partitions;
3.5–3.8% on GSM8K), and only 4–7% of those are accepted. The 512-token cap
is therefore binding from the start, not a consequence of training.
An earlier proxy overstated termination. Earlier versions of this paper called
a generation degenerate if it was longer than 1,500 characters and contained
no \boxed, and read its rise (9.8% →41.3% for Run A, seed 1) as a growing
failure to finish. Measured against cap-hit, the proxy flags only 9.8% of round-0
generations when 43.2% hit the cap, and its rise mostly tracks a change in the
text rather than in termination: proxy-flagged generations have 3.3 characters
per token at round 0 and 4.9–5.0 at round 2, against 2.7–3.0 for the rest, so
drifting prose crosses 1,500 characters within the same token budget. At round 0
every proxy-flagged generation is a cap-hit (at round 2, 80–98% are), but the
proxy catches only 19–25% of cap-hits at round 0 and 58–75% at round 2 (at
5 × 10−4), so its rise is largely a rise in the share of cap-hits it can see. At 10−4
and 2 × 10−4 the proxy share grows 2.0–2.6× (at seed 1, 9.8% →19.5% at 10−4
and 9.8% →25.0% at 2 × 10−4) while cap-hit stays flat or falls.
At the highest rate, finished solutions are less accurate. In all six self-training
runs at 5 × 10−4 (Table 11) mean length grows by 41–52%, but the cap-hit

Mathematics or the Verifier?
29
share rises by only 2.3–14.2 points, while accuracy on the generations that fin-
ish falls from 50.6–54.0% to 43.0–46.3%. Because the problems that still finish
change, we compared last-round finished accuracy with the untrained model’s
finished accuracy on the same problem mix, weighting each problem’s round-0
finished accuracy by the number of finished last-round samples it has. Prob-
lems with no finished last-round sample drop out (22–45 of the 150 per run);
where a problem had no finished round-0 sample we use its accuracy over all
round-0 samples (6–21 problems, 34–37 in the gold runs), which, being mostly
cap-hit accuracy, biases the baseline down for those problems; intervals use 2,000
problem-level bootstrap resamples. Because training changes which problems
finish, the matched metric conditions on an outcome of training and is descrip-
tive, not a causal effect. On that matched basis finished generations lose 5.5–
10.6 points, with intervals excluding zero in five of the six runs (Table 5). We
also split the change in sample accuracy symmetrically into a finished-accuracy
part ¯s ∆f, a cap-share part ∆s ( ¯f −¯c) and a cap-accuracy part (1 −¯s) ∆c,
where s is the share of finished generations, f and c the accuracy of finished
and cap-hit generations, and bars denote round-0/last-round means. Only the
cap-share part measures termination; the cap-accuracy part is a change in how
often unfinished text is still accepted. Table 7 gives the three parts and paired
bootstrap intervals (2,000 resamples) for the cap-hit change and for the finished-
accuracy share (experiments/viec3/review_cpu/dot4/boot.py). This decom-
position uses the unmatched finished accuracy, so its finished part still contains
the shift in which problems finish.
At 5 × 10−4 the cap-hit rise has an interval excluding zero in all three seed-2
runs and in B at seed 1; at seed 1 the other rises (+2.3 and +3.0) are about the
size of two samplings of the untrained model on the same partition (43.2% at
k = 4 against 40.7% at k = 8), and the replicate and the 1,024-limit run do not
rise at all. The cap-share part is 12–30% of the decline at seed 1 and 52–72%
at seed 2; the cap-accuracy part is small (−1.1 to +1.5 points). The finished-
accuracy shares have wide intervals, and they split by seed (every seed-1 run
62–74%, every seed-2 run 34–59%); since seed sets the partition, this may be
partition variation rather than run-specific anatomy. What the table supports is
qualitative: at 5 × 10−4 both parts contribute, in a balance that differs by parti-
tion. At 10−4 and 2×10−4 the cap-hit share does not rise, the finished-accuracy
part exceeds the whole (smaller) change in four of the five runs and is 93% of it
in the fifth, and matched finished accuracy falls by 0.6 to 4.7 points with inter-
vals including zero. Termination therefore contributes materially to the decline
only at the highest rate, and clearly only at one seed (at 10−5 the declines are
too small to divide reliably). The long generations that remain open as ordinary
solutions and then drift into loosely related prose (e.g. “. . . acknowledged hur-
dles acknowledged setbacks . . . ”), with low exact repetition (mean word 5-gram
repeat ratio about 0.02, similar to other generations, though the decoding repe-
tition penalty of 1.1 suppresses exact repeats by itself); this description rests on
inspection of examples, not on a systematic annotation. Train-on-gold is differ-
ent: responses shorten by 55–59%, cap-hit falls from 43% to 7–8%, and finished

30
T. S. Nguyen and D. A. Tran
Table 12. Adapters re-scored on the same exam problems (seed-1 partition, k = 4, 150
problems) under a 512- and a 1,536-token generation cap. Round-2 adapters from runs
at 5 × 10−4 (“replicate” keeps the 512-token training limit, “1024 limit” trains with
no truncated example) and 2 × 10−4, against the untrained model. One adapter per
row; re-scoring the same adapter moves pass@1 by 2.7–6.7 points against the run’s own
round-2 value. Only summary statistics were saved for these re-scorings, so no bootstrap
intervals and no cap-hit counts are available; “Degenerate” and “Acc. finished” use the
character proxy of Section H, which undercounts cap hits, and are shown only for
completeness. Sample accuracy rests on 600 samples clustered in 150 problems.
Model
Cap
pass@1 pass@4 Sample acc. Degenerate Acc. finished
Untrained
512
36.0%
52.0%
36.3%
8.7%
39.2%
1536
40.7%
59.3%
43.2%
2.5%
44.1%
5 × 10−4, replicate
512
29.3%
46.7%
28.3%
30.0%
38.1%
1536
35.3%
52.0%
34.2%
23.0%
43.3%
5 × 10−4, 1024 limit 512
26.0%
45.3%
27.5%
37.2%
40.8%
1536
30.7%
50.7%
29.5%
32.7%
41.3%
2 × 10−4
512
27.3%
48.7%
28.5%
28.7%
37.9%
1536
32.0%
52.7%
32.0%
23.7%
40.8%
accuracy collapses (−25.6 and −25.9 points matched). This collapse may owe
something to the training recipe rather than to the data alone: the loss is taken
over the prompt as well as the response, and reference solutions are short and
terse, so even one epoch on 350 of them per round can pull the model far from
its own reasoning style; we did not test a response-only loss.
Two checks of the pipeline. The training limit (max_length= 512 tokens, prompt
included) equals the generation cap, so 24–26% of the kept pool (108 of 440 ex-
amples in Run A at round 0) is truncated in training: it loses its final answer and
end-of-sequence token and could teach the model not to stop. We reran Run A
at seed 1 and 5 × 10−4 once with a training limit of 1,024 tokens, together with
a matched replicate that keeps the 512-token limit. Removing the truncation
changed little in this one run: the round-2 cap-hit share is 43.8% with the longer
limit, 43.0% in the replicate and 46.2% in the original Run A, and matched
finished accuracy falls by 5.7, 5.0 and 9.1 points. The differences between the
three arms are within the spread of the one same-configuration pair we have
(the original and the replicate, which are themselves two of the three arms, 4.1
points apart matched), so this pair is a poor estimate of replicate noise; and the
longer limit does not remove every unterminated example: 43 of the 440 accepted
round-0 examples (9.8%) are cap-hit generations, which have no end-of-sequence
token under any training limit. With one run per arm this can only exclude a
truncation effect much larger than the 4-point gap between the pair. The repli-
cate reproduces the direction of Run A’s decline (pass@1 33.3 →31.3 →25.3%,
pass@4 50.0 →48.0 →44.0%).
Re-scoring the same adapters under a 1,536-token cap, with everything else
fixed (Table 12), is consistent with the 512-token cap not being the whole story,

Mathematics or the Verifier?
31
though with one adapter per row and no intervals it does not establish it. The
untrained model gains more from the larger cap than the adapters do (sample
accuracy +6.8 points, against +5.8, +2.0 and +3.5), so the adapters’ deficit
does not close: −8.0, −8.8 and −7.8 points at 512 tokens and −9.0, −13.7 and
−11.2 at 1,536. This does not separate less accurate solutions from generations
that do not stop: at 1,536 tokens the proxy’s “Acc. finished” is close for all
four rows (40.8–44.1%) while its “Degenerate” share is 2.5% for the untrained
model and 23–33% for the adapters, which points to non-termination, though
the proxy undercounts cap hits. Since re-scoring the same adapter moves pass@1
by up to 6.7 points, differences of one to three points between rows, including
the comparison of gains, are not interpretable. The data suggest that the gap
persists at a tripled cap, whether from less accurate solutions or from generations
that do not stop, for single adapters on one partition; they do not show what a
still larger cap would do.