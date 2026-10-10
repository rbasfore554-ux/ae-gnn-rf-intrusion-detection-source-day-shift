# Hybrid AE–GNN–RF Intrusion Detection (CIC-IDS2017)

An experimental research implementation of network intrusion detection using an Autoencoder (AE), a k-nearest-neighbour (k-NN) graph, a Graph Convolutional Network (GCN), and a Random Forest (RF) classifier.

> **Research status:** experimental benchmark code. The manuscript has been shared with the academic supervisor for review; this repository does not claim peer-reviewed publication, production readiness, or generalization to unseen networks. The current results do **not** show that GNN fusion outperforms the AE+RF baseline overall.

## Architecture

![AE–GNN–RF feature-fusion architecture](figures/architecture_72d_zh_fusion.png)

The principal fused model is:

`72 numeric flow features → AE encoder → Z (32-D) → k-NN graph (k=10) → GCN hidden embedding H (16-D) → concatenate [Z || H] (48-D) → RF → benign / attack`

The notebook also evaluates an H-only RF baseline and a supplementary `[Z || reconstruction error || H]` (49-D) variant.

## Recorded result for `[Z || H]`

The final recorded fusion run evaluated **565,536 test flows** using a validation-selected decision threshold of **0.4221336**.

| Metric | Result |
|---|---:|
| Accuracy | 97.8051% |
| Attack precision | 90.8170% |
| Attack recall | 98.8429% |
| Attack F1-score | 94.6601% |
| ROC-AUC | 0.998172 |
| Average Precision (AP) | 0.992614 |
| False-positive rate | 2.4492% |
| False-negative rate | 1.1571% |
| Balanced accuracy | 98.1968% |

Confusion matrix (rows = actual; columns = predicted):

| | Predicted benign | Predicted attack |
|---|---:|---:|
| Actual benign | 443,100 | 11,125 |
| Actual attack | 1,288 | 110,023 |

![Confusion matrix](figures/final_zh_confusion_matrix.png)

![ROC curve](figures/final_zh_roc_curve.png)

![Precision–recall curve](figures/final_zh_precision_recall_curve.png)

*Metric note:* the stored `PR_AUC` value was computed with scikit-learn's `average_precision_score`, so this README calls it **Average Precision (AP)** rather than implying trapezoidal integration of the precision–recall curve.

## Ablation and fusion comparison

All metrics below come from the recorded benchmark runs. The `model_comparison.csv` file stores metric scores as fractions from 0 to 1, and confusion-matrix entries as counts.

| Model | Accuracy | Precision | Attack recall | F1 | ROC-AUC | FNR |
|---|---:|---:|---:|---:|---:|---:|
| AE | 34.09% | 22.74% | 97.99% | 36.92% | 0.6646 | 2.01% |
| AE+GNN | 73.89% | 42.47% | 92.16% | 58.15% | 0.8755 | 7.84% |
| AE+RF | **97.93%** | **91.28%** | **98.95%** | **94.96%** | **0.9984** | **1.05%** |
| AE+GNN+RF `[H]` | 96.12% | 84.82% | 97.80% | 90.85% | 0.9952 | 2.20% |
| AE+GNN+RF `[Z || H]` | 97.81% | 90.82% | 98.84% | 94.66% | 0.9982 | 1.16% |

![Model comparison chart](figures/model_comparison.png)

**Interpretation:** adding `Z` back to the GNN embedding substantially improves the H-only hybrid in the recorded experiment. However, **AE+RF remains slightly stronger overall** on accuracy, precision, recall, F1, ROC-AUC, and FNR. We therefore do not claim general superiority for the GNN. The next research step is to test the models at a fixed target recall, compare per-attack performance, and evaluate on traffic from a different day/source.

## Dataset and preprocessing audit

The public CIC-IDS2017 CSVs are **not bundled** in this repository. Download them from the [Canadian Institute for Cybersecurity's CIC-IDS2017 page](https://www.unb.ca/cic/datasets/ids-2017.html), then place the eight source files in:

`data/raw/cicids2017/`

The recorded preprocessing audit is:

| Stage | Count |
|---|---:|
| Merged source data | 3,119,345 rows; 85 columns including label |
| After replacing ±infinity with missing and dropping rows with any missing value | 2,827,876 rows |
| Exact duplicate rows removed | 199 |
| Final rows | 2,827,677 |
| Benign rows after deduplication | 2,271,122 |
| Attack rows after deduplication | 556,555 |
| Model input features | 72 numeric features |

The 76 non-constant feature columns exclude four non-numeric identifiers/time fields (`Flow ID`, `Source IP`, `Destination IP`, `Timestamp`), leaving 72 numeric model inputs.

### Data-quality caveat

The recorded audit of `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` found 458,968 raw rows, including 288,602 rows with missing labels, 288,622 rows with at least one missing value, and 135 rows containing infinity in numeric columns (20 overlapping rows). Under the implemented union of invalid-row rules, 288,737 rows were removed and 170,231 retained from that file. Rows with missing labels were omitted; no missing labels were inferred. This source-file anomaly should be reviewed when reproducing or extending the study.

Audit CSVs in `results/` document the observed counts. Do not upload the raw dataset files or generated large model files to GitHub.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_full_experiment_pipeline.ipynb
│   └── 02_cicids2017_cleaning_audit.ipynb
├── figures/
│   ├── architecture_72d_zh_fusion.png
│   ├── final_zh_confusion_matrix.png
│   ├── final_zh_roc_curve.png
│   ├── final_zh_precision_recall_curve.png
│   └── model_comparison.png
├── results/
│   ├── final_model_metrics.csv
│   ├── model_comparison.csv
│   └── CIC-IDS2017 audit CSVs
└── docs/
    ├── REPRODUCIBILITY.md
    └── RESEARCH_STATUS.md
```

## Run the experiment

1. Use Python 3.10 or 3.11 in a fresh environment.
2. Install PyTorch for your operating system using the [official PyTorch installation selector](https://pytorch.org/get-started/locally/), then install the dependencies in `requirements.txt`. If your platform requires a platform-specific PyTorch Geometric wheel or setup, follow the [PyTorch Geometric installation guide](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html).
3. Download the eight CIC-IDS2017 CSVs from the official source and place them in `data/raw/cicids2017/`.
4. Open `notebooks/01_full_experiment_pipeline.ipynb` and run every cell from the top in a fresh kernel. The notebook writes plots and metric CSVs under `figures/` and `results/`, and optional checkpoint files under `outputs/models/` (ignored by Git).
5. Run `notebooks/02_cicids2017_cleaning_audit.ipynb` to reproduce the cleaning counts and audit CSVs.

The experiment is computationally heavy: the AE processes the training split in full-batch mode, and the final test graph contains all test flows. Depending on hardware, RAM and runtime may be limiting. The reported results are recorded outputs from the project run; this package was not re-executed end-to-end during packaging.

## Reproducibility and limitations

- Seed: `42`; one recorded random stratified split.
- 64% training, 16% validation, 20% test under the nested split.
- Imputer and scaler fit on training data only.
- Thresholds selected on validation data by maximizing F2.
- 100,000 sampled GNN training nodes and 100,000 validation graph nodes; all 565,536 test flows in the test graph.
- The GNN uses a k-NN graph computed within each split. The test evaluation therefore represents a graph over the held-out test cohort, not a fully streaming per-flow production evaluation.
- The held-out test partition was used to compare multiple ablation/fusion variants. Consequently, treat the reported table as an exploratory benchmark; a new source-day-held-out or external test is needed for a strong unbiased estimate after model selection.
- Per-attack breakdowns, multiple-seed confidence intervals, latency, throughput, and adversarial robustness have not been established.
- The AE was trained on the full training split, which contains both benign and attack traffic; it was **not trained exclusively on benign traffic** in this experiment.

See [Reproducibility](docs/REPRODUCIBILITY.md) and [Research status](docs/RESEARCH_STATUS.md) for workflow and next steps.
