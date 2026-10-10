# Reproducibility notes

## Required raw files

Download CIC-IDS2017 from the Canadian Institute for Cybersecurity. The following CSVs are expected under `data/raw/cicids2017/`:

- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

The public repository intentionally excludes raw data and model checkpoint files.

## Run order

1. Start a fresh Jupyter kernel.
2. Run every cell in `notebooks/01_full_experiment_pipeline.ipynb` from top to bottom. Do not execute isolated cells using variables from older notebook sessions.
3. Run `notebooks/02_cicids2017_cleaning_audit.ipynb` separately to regenerate the dataset cleaning audit. It writes summary CSVs into `results/`.

The full experiment is memory- and compute-intensive. The notebook uses full-batch AE training, sampled GNN training/validation graphs of 100,000 nodes each, and a graph built over all held-out test flows. Hardware-dependent runtime and memory use are expected.

## What the published CSVs mean

- `results/final_model_metrics.csv`: recorded final AE–GNN–RF `[Z || H]` fusion run.
- `results/model_comparison.csv`: recorded ablation/fusion comparison. Metric scores are fractions from 0 to 1; TN, FP, FN and TP are counts.
- `results/cicids2017_*_audit.csv`: observed counts from the cleaning audit.

Notebook code is provided for transparency. The package was not re-executed end-to-end during preparation, so saved CSVs should be treated as the recorded project outputs, not as freshly verified outputs from this packaging step.
