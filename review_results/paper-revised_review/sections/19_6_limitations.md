## 6 Limitations
Unequal training doses confound every cross-arm comparison. The controls are
underpowered: the patch changes 0–4 training examples, and the no-filter and
train-on-gold controls have two seeds each. Intervals cover only problem draw
and sampling, not training-seed variance; several conditions have one seed, and
no multiplicity correction is applied. The learning-rate grid is coarse, with three
rounds and k = 4. Cap-hit is reconstructed from decoded text. The verifier
audit used other models’ solutions and inspected only rejections; the gold-storage
defect was measured afterwards and ran unvaried through every run, and the
same verifier both selects and grades. The 512-token cap binds from the start.
Scope: one model size in Design I, one verifier, one LoRA recipe with loss over
the prompt, a restart-from-base design that leaves compounding little room,
and possible test-set contamination. No arm improves on round 0, so we have no
positive reference showing this recipe can help a 1.5B model. Appendix J gives
the full list.

14
T. S. Nguyen and D. A. Tran