## 7 Conclusion
We asked whether generate–verify–select–train iterations make a 1.5B model
better at mathematics or only teach it to write what a rule-based verifier accepts.
On a held-out exam, the first answer is no: on the four measures fixed in advance
no run improves detectably, and the intervals for sample accuracy (a primary
measure chosen after the runs) exclude gains above about 2.2 points, a loose
bound because they omit training-seed variance and are not an equivalence test.
The second stays open, because our pre-set rule for it could only fire if accuracy
rose, and the post hoc \boxed share falls in a way that imitation of the less-boxed
training pool and drift would both produce. The direction-free test we propose,
the per-round share of the loop’s own correct solutions that a verifier defect
rejects, answers it for one defect: that share does not fall, so the model does not
learn to avoid it. In a post hoc description, most clearly at the highest rate, the
model becomes less accurate on the solutions it does finish; more generations hit
the token cap only at the highest rate, and clearly only at one of its two seeds,
where the change in cap-hit share accounts for 12–30% of the decline at seed 1
and 52–72% at seed 2; a character-length heuristic we first used overstated that
part. Reference-solution training degrades the model more, with much shorter
answers. Patching a rare verifier defect and removing the filter made no difference
of consistent sign across measures and seeds (pass@1 flips sign between seeds;
removing the filter lowers pass@4 at both seeds, within noise; single-seed intervals
sometimes exclude zero), neither control could have detected a small effect, and
a frequent defect in our gold storage, which rejects about one in six correct
solutions, ran unvaried through every experiment. A sharp decline seen in an
earlier pooled design does not reproduce under isolation and held-out scoring,
and because that design also trained several times longer per round, we leave
its cause open. We report the earlier readings that did not hold up because the
designs that produced them are common.
A rising score, in self-training or in RLVR, does not by itself show that a
model learned mathematics rather than its verifier. The per-round false-reject
test we propose asks that question directly and works whether accuracy rises or
falls; the natural next step is to apply it to public RLVR checkpoints. Future
work, including a dose-matched control for the gold-storage defect, is outlined
in Appendix K.
Acknowledgments. This work was carried out as an undergraduate research project.
No external funding was received.
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.