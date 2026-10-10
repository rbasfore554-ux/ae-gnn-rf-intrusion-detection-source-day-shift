# Research status

## Completed experiment

The reported binary intrusion-detection experiment uses CIC-IDS2017 with 72 numeric flow features. A 72-to-32 Autoencoder representation, Z, is combined with a 16-dimensional hidden representation, H, from a two-layer GCN trained on a k-nearest-neighbour graph constructed over Z. A Random Forest classifies the 48-dimensional concatenation [Z || H].

The reported operating threshold is 0.4221, selected using validation data with F2 as the objective and then frozen for test evaluation.

## Main result

The [Z || H] fusion result is: accuracy 97.8051%, attack precision 90.817%, attack recall 98.8429%, F1 94.6601%, ROC-AUC 0.998172, average precision 0.992614, FPR 2.4492%, and FNR 1.1571%. Test confusion matrix: TN 443100, FP 11125, FN 1288, TP 110023.

## Interpretation

The AE+RF baseline is slightly stronger overall on the current reported results: accuracy about 97.93%, F1 about 94.96%, and FNR about 1.05%. The evidence therefore does not support saying the GNN hybrid is the best model overall. The experiment investigates whether relational features can complement AE features and substantially recover the loss seen with RF(H) alone.

## Outstanding research questions

- Compare false-positive rate at a fixed, validation-selected target attack recall.
- Evaluate per-attack detection and identify attack categories missed by each model.
- Test cross-day generalisation with a strict split that prevents information leakage.
- Verify and document the source dataset/cleaning choice because the Thursday Web Attacks CSV had extensive missing-label/missing-value issues in the audit.
- Re-run the experiment from a clean environment before claiming independent reproducibility.

The submitted manuscript is outside the scope of this repository update and is not being revised here.
