# Paper Summary: Mathematics or the Verifier? A Null Result for One Verifier-Filtered Self-Training Recipe on a 1.5B Model

## Research Question
After several generate-verify-train (GVT) rounds with a rule-based verifier (math-verify), is a 1.5B model better at mathematics or only at what the verifier accepts?

## Core Thesis
No pass@1/pass@k gain at any learning rate with interval excluding zero; final 500-problem round loses 3.2-4.8 pass@1 in 3 seeds (mean -4.1); positive gate (train on reference solutions) fails (-32.2), so null concerns this recipe only; neither question is answered.

## Methodology
Qwen2.5-1.5B-Instruct, offline rejection-sampling LoRA SFT, fresh adapter per round, MATH-500/GSM8K exams (150 problems; 500 in final round), paired problem-level bootstrap. All runs regraded with one patched verifier V' plus a string-match grader. Post hoc audit of a gold-storage defect.

## Key Numbers
- Detectable effect ~10 pts pass@1 (150 problems), ~6 final round. Training-seed variance not covered by intervals.
- Final round: loop pass@1 -4.8/-3.2/-4.2; gold -32.2; boxed share 90.6->90.3; acc|boxed 48.5->17.1; length 3.2x shorter.
- Table 1-3 values from regrade (V'), cap-hit 512 tokens.

## Section Map
Chunks 0-1: abstract, intro, related work; chunks 2-3: setup/methods, verifier; chunks 4-5: results (design P, I, controls, higher LR, anatomy, final round); chunks 6-7: audit, discussion, limitations, conclusion, references.
