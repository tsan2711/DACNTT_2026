### 4.2 Design I at 10−5: Small Declines, a Larger One on GSM8K
On the held-out exam (Fig. 1, Table 3) pass@8 ends within 4 points of round 0
in every run. On MATH-500, pass@1 is 2.7–4.0 points lower at round 4, with
every interval including zero (Table 5); sample accuracy falls 1.2–3.2 points and
matched finished accuracy 1.1–4.2, with intervals that only just exclude zero for
A and B at seed 0, which are close to one replicate. We read this as a possible
small decline, not an established one; what we do not see is a gain. Run C
(GSM8K) declines more: pass@1 falls 12.7 points ([−21.3, −4.0]), almost all in
finished accuracy, but it took about twice Run A’s optimizer steps, so we do
not attribute this to the dataset alone. At this rate the training loss falls, but
on MATH-500 the adapter barely changes the outputs (length and cap-hit share
are essentially unchanged), so a flat curve there shows that this training step
did little, not that GVT is stable (Appendix E).

8
T. S. Nguyen and D. A. Tran
Fig. 1. Design I at 10−5: pass@1 (left) and pass@8 (right) on the held-out exam set,
by round. Colour identifies the run, line style the seed, marker the run again, so the
figure survives greyscale printing. Runs A and B track each other closely at both seeds.
pass@8 stays within a few points in every run. The one large visible movement is
Run C’s pass@1 in the final round.
Table 3. Design I: pass@1 and pass@8 on the held-out exam set (150 problems),
Qwen2.5-1.5B, learning rate 10−5. Runs A and B differ only in the \dfrac/\tfrac
patch. Each seed draws its own exam partition, so round-0 values differ between seeds.
Run
Metric
R0
R1
R2
R3
R4
∆
A, seed 0 (MATH-500, orig.)
pass@1 32.0% 29.3% 28.0% 29.3% 29.3% −2.7 pt
A, seed 0 (MATH-500, orig.)
pass@8 57.3% 56.7% 54.7% 57.3% 56.0% −1.3 pt
A, seed 1 (MATH-500, orig.)
pass@1 36.7% 32.7% 32.7% 31.3% 33.3% −3.3 pt
A, seed 1 (MATH-500, orig.)
pass@8 58.7% 60.7% 59.3% 59.3% 58.7%
0.0 pt
B, seed 0 (MATH-500, patched) pass@1 32.0% 28.7% 28.7% 28.7% 28.7% −3.3 pt
B, seed 0 (MATH-500, patched) pass@8 57.3% 55.3% 52.0% 57.3% 53.3% −4.0 pt
B, seed 1 (MATH-500, patched) pass@1 37.3% 32.0% 32.7% 31.3% 33.3% −4.0 pt
B, seed 1 (MATH-500, patched) pass@8 59.3% 60.7% 58.0% 58.7% 58.7% −0.7 pt
C, seed 0 (GSM8K, orig.)
pass@1 66.7% 66.7% 65.3% 63.3% 54.0% −12.7 pt
C, seed 0 (GSM8K, orig.)
pass@8 92.7% 90.7% 93.3% 90.0% 90.0% −2.7 pt