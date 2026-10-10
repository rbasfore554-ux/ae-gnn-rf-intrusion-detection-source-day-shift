# Research status and next experiments

## Current supported conclusion

The recorded AE–GNN–RF `[Z || H]` fusion result achieves 97.81% accuracy, 98.84% attack recall and 94.66% F1. It improves substantially over an RF classifier using the GNN hidden embedding `H` alone. The AE+RF baseline remains slightly stronger on the current aggregate benchmark metrics, including FNR.

Therefore, the current evidence does not support a claim that GNN addition is universally beneficial or that the fusion model outperforms AE+RF overall.

## Planned follow-up work (not yet implemented/evaluated)

1. **Fixed-recall operating point:** choose a target attack recall on validation, then compare false-positive rates on held-out test data at that target. Report how many false alarms are introduced for the same detection objective.
2. **Attack-specific analysis:** report precision/recall/FNR by attack family and investigate whether the GNN recovers specific attacks missed by AE+RF.
3. **Cross-day/source-file generalization:** train/validate using one set of traffic periods and test on a disjoint day/source file.
4. **Independent final test:** after choosing variants/thresholds without test feedback, evaluate once on a truly untouched split or external dataset.

These are research plans, not completed results. The manuscript previously shared with the supervisor is not included or modified by this repository package.
