## K Future Work
Separate the explanations of the pooled decline with a pooled run scored on
a held-out split and an isolated run matched in optimizer steps (by fixing the
step count per round rather than the number of epochs); save token counts
at generation time and test a larger generation cap during the loop, since the
untrained model already hits 512 tokens in 41–48% of MATH-500 generations;
refine the learning-rate grid and replicate Run C; and run a positive control (a
verifier biased against a frequent format) to show what effect size this design
can detect.
The gold-storage defect (Section B) is the natural next verifier control. We
implemented and unit-tested a patch that wraps the gold in \boxed{} whenever
the prediction contains one and the gold does not; re-scoring shows that in a
training run it would enlarge the round-0 kept pool by about a fifth (440 →542
and 872 →1,066), roughly 34–49 times the change made by the \dfrac patch,
so unlike Run B such a run would actually perturb the training data. Because
a larger pool also means more optimizer steps, the comparison should hold dose
fixed, either by subsampling the patched pool to the unpatched size or by fixing
the step count. Given that same-configuration runs end several points apart, it
needs several seeds per arm; a single seed would detect only a large effect.