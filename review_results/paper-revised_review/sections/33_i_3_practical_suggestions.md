### I.3 Practical Suggestions
These suggestions come from one 1.5B model, one rule-based verifier, LoRA SFT
and at most three seeds per condition; some are general good practice that our
experience illustrates rather than findings. Hold out evaluation items and keep
one adapter per dataset if you report per-dataset trajectories, so the curves can
at least be read; our data do not rank these factors. Match training dose across
arms, or report optimizer steps: pool size changes with filtering, k and dataset,
and with one epoch it sets the number of updates. Check that the training step
changes the model (loss and output statistics after one round) before reading a
flat curve as stability. Count the prevalence of a suspected verifier defect in the
loop’s own outputs before building a control around it; a treatment that changes
0.5% of the pool cannot be detected with 150 problems. Save token counts and
report cap-hit directly, not a character-length proxy, and adjust any “accuracy
on finished solutions” for which problems still finish; our proxy misread a change
in text style as a change in termination. Report intervals, and track pass@k and
per-problem gains and losses alongside pass@1.