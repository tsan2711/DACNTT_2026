### 3.2 The Verifier and Its Directional Bias
A format probe that re-renders gold answers in individually valid forms shows
that \dfrac/\tfrac are rejected 100% of the time on both datasets (the com-
mand is not parsed). On real solutions (one public Qwen2.5-7B-Instruct solution
per problem for 200 MATH-500 problems, judged correct by a scripted nor-
malised comparison) the false-negative rate is 7.8% (10 of 128) on MATH-500
and 0% on GSM8K; most failures are wrong-token extraction from a long solu-
tion. The audit inspected only rejections, so it gives no false-positive rate. The

Mathematics or the Verifier?
5
verifier also cannot parse 51 of the 500 stored MATH-500 golds (10.2%); these
problems always count as unsolved, which lowers absolute pass rates but cancels
within a partition.
The patch. For the control we rewrote \dfrac and \tfrac to \frac before
parsing, removing the 100%-rejection class and nothing else.
The gold-storage defect (post hoc). Our pipeline stores the gold without a de-
limiter, and math-verify applies its full LATEX extraction only inside \boxed{}
or $...$, so a correct boxed prediction can fail against a bare gold (e.g. \frac43
against \boxed{\frac{4}{3}}). Re-scoring the saved generations with the gold
wrapped in \boxed{} shows that this defect rejects 15.5–18.4% of the genera-
tions the re-scored verifier accepts, in every round. It would enlarge the round-0
kept pool by about a fifth (440 →542), against 0–4 examples for the \dfrac
patch, and it lowers absolute pass@1 by 4.7–8.0 points in self-training. Two
consequences follow. With the original verifier the declines reported below are
understated (by a factor of about 0.73–0.78), and re-scored, sample accuracy still
falls in all five runs we re-scored. And the share of correct answers the defect
rejects does not fall over rounds, so for this one defect the model does not learn
to avoid what the verifier rejects. All tables keep the original verifier, the one
the loop trained with. Appendix B gives the full analysis.