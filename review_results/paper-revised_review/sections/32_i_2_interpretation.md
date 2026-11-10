### I.2 Interpretation
An earlier version of this work explained the Design P curves with a self-
reinforcing shrinking-pool mechanism: the biased verifier accepts a smaller, more
style-skewed set each round and the skew compounds. The data give it no sup-
port, but they do not rule it out either. The patch removes a severe but rare bias
and changes the pool by a handful of examples, so it tests how strong the bias is
per answer, not whether a frequent bias compounds; the no-filter control declines
without any verifier, as much as Run A at seed 1 and more at seed 2 (sample
accuracy −10.2 against −4.7), but it also trains on 3–4× more examples, so its
decline is confounded with dose; and the training-dose difference between the
designs offers a simpler account that we have not tested directly either. Pool size
is also partly definitional (it is sample accuracy on the selection items times the
number of samples), so its co-movement with accuracy, which holds on pass@1

Mathematics or the Verifier?
33
in Design I as well (Run C: pool −20%, pass@1 −12.7; Run A: −3%, −2.7), says
little about mechanism.
Design I differs from Design P in at least four respects at once (isolation, a
held-out split, n per run falling from 1,000 pooled problems to 500, and the train-
ing dose), so the P/I contrast is descriptive. The clean comparisons are internal
to Design I and its higher-rate counterparts, and even there the controls differ in
dose. The defensible statement about the verifier is narrow: removing a format
defect present in under 1% of generations, or removing the filter entirely, made
no consistent difference at the resolution of this setup. The one frequent system-
atic false negative we measured, the gold-storage defect, was present in every
run and was never varied, so whether systematic false negatives are harmless in
general, as Egashira et al. find for RLVR, our data cannot say.