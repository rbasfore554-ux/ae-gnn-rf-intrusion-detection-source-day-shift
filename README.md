# Hybrid AE–GNN–RF IDS Research

A reproducible research repository for evaluating an Autoencoder + Graph Convolutional Network (GCN) + Random Forest pipeline for binary intrusion detection on CIC-IDS2017.

## Status

This repository documents completed experiments and includes notebooks, figures, metrics, and dataset-cleaning audit outputs. It does **not** claim that the AE–GNN–RF fusion model outperforms the AE+RF baseline on overall metrics. Further testing is needed to establish whether relational features provide a benefit under specific cybersecurity objectives.

## Key architecture

- **Input:** 72 numeric traffic features after cleaning and exclusion of identifier/time fields.
- **Autoencoder:** 72 → 128 → 32 encoder; decoder 32 → 128 → 72.
- **Graph:** k-nearest neighbours (k = 10, Euclidean distance) over the Autoencoder representation.
- **GCN:** 32 → 16 → 2; the 16-dimensional hidden representation is denoted by `H`.
- **Fusion:** `F = [Z || H]`, where `Z` is the 32-dimensional Autoencoder representation; fused dimension = 48.
- **Classifier:** Random Forest, 100 trees, maximum depth 15, `max_features=sqrt`, balanced class weights.
- **Decision threshold:** 0.4221, selected using validation data with F2 as the objective and then fixed for test evaluation.

## Reported final test result: `[Z || H]` fusion

| Metric | Result |
|---|---:|
| Accuracy | 97.8051% |
| Attack precision | 90.817% |
| Attack recall | 98.8429% |
| F1-score | 94.6601% |
| ROC-AUC | 0.998172 |
| Average precision (PR/AP) | 0.992614 |
| False-positive rate | 2.4492% |
| False-negative rate | 1.1571% |
| Balanced accuracy | 98.1968% |

Confusion matrix: TN = 443,100; FP = 11,125; FN = 1,288; TP = 110,023.

The test set contains 565,536 flows: 454,225 benign and 111,311 attack flows.

## Interpretation and scientific caution

The AE+RF baseline is slightly stronger overall in the experiments reported here (approximately 97.93% accuracy, 94.96% F1, and 1.05% FNR). The contribution examined here is whether graph-derived relational information can complement the AE representation, not a demonstrated overall performance win. Proposed follow-up experiments include comparing false-positive rates at a fixed target attack recall, per-attack analysis, and cross-day generalisation with strict train/validation/test separation.

## Repository layout

- `notebooks/01_full_experiment_pipeline.ipynb` — combined experiment and ablation notebook.
- `notebooks/02_cicids2017_cleaning_audit.ipynb` — source-file and cleaning audit notebook.
- `figures/` — architecture and final-fusion evaluation figures.
- `results/` — reported metrics, model comparison and audit CSVs.
- `docs/RESEARCH_STATUS.md` — completed work and outstanding limitations.
- `docs/REPRODUCIBILITY.md` — environment and reproduction notes.

## Reproduce

1. Use Python 3.10 or a compatible environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Download CIC-IDS2017 independently from its official distribution and place source CSVs in the local data directory described in the cleaning notebook.
4. Review the notebook's configuration paths before running.
5. Execute the cleaning audit, then the experiment notebook in order.

The raw dataset and trained model checkpoints are not committed. The reported notebook results are records of prior experiments and are not proof of a fresh rerun in every environment. The full experiment is memory-intensive; adjust chunk sizes and sampled graph sizes only when documenting the change and interpreting results.

## Data cleaning note

The reported merged input consisted of 3,119,345 rows and 85 columns (including the label). Rows containing missing or non-finite values were removed, constant columns were dropped, and 199 duplicate rows were removed, leaving 2,827,677 rows and 72 numeric model features. The Thursday Web Attacks source file had a substantial missing-label/missing-value issue in the audit; review the CSVs in `results/` and verify the dataset source/cleaning policy before treating the dataset as definitive.

## License

MIT. See `LICENSE`.
