### 3.3 Two Experimental Designs
Design P (pooled) loads both datasets (500 problems each) together and trains
one adapter per round on the union of accepted solutions, with selection and
evaluation on the same 1,000 problems. Design I (isolated) uses one dataset and
one adapter per run, and holds out 30% of the 500 problems (150) as an exam
set; generation runs on all 500 problems each round, but only the other 350 can
enter the training pool, and all Design I pass rates are on the exam set. Table 8
summarises them.
Design I has three runs, all Qwen2.5-1.5B-Instruct, five rounds, k = 8, differ-
ing in one respect each: Run A (MATH-500, original verifier), Run B (MATH-
500, patched verifier) and Run C (GSM8K, original verifier). Runs A and B
were repeated at a second seed; since the seed also sets the train/exam parti-
tion, the repetition draws a different 150-problem exam set. Most of the later
evidence comes from higher-rate runs introduced in Section 4.4; Table 1 lists
every run. A “seed” sets the exam partition, the selection set and the training
randomness at once; runs with the same seed share the partition.