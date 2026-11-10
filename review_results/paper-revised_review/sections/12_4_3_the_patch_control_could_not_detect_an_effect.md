### 4.3 The Patch Control Could Not Detect an Effect
Runs A and B differ only in the \dfrac/\tfrac patch. At round 4, B minus A
is −0.7 [−3.3, +2.0] points of pass@1 at seed 0 and +0.0 [−2.7, +2.7] at seed 1.
This null is uninformative: \dfrac appears in 0.50–0.73% of generations, so the
kept pools differ by 3–4 examples (under 0.5%), and at 10−5 the adapter changes
the outputs little anyway. Removing one rare format defect had no detectable
effect, which a prevalence count alone predicts; the frequent gold-storage defect

Mathematics or the Verifier?
9
is present in both arms. The pre-filter share of problems on which all k samples
agree falls in every run, but it is mechanically tied to accuracy, so we draw no
conclusion from it (Appendix F).