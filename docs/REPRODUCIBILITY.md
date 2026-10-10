# Reproducibility notes

## Environment

Use a clean Python environment. Install dependencies with:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

For macOS, activate with `.venv/bin/activate`. Install the TensorFlow and PyTorch versions suitable for your installed Python version and hardware if the generic dependency installation fails.

## Data

Obtain CIC-IDS2017 from its official distribution. Keep raw data locally under `data/raw/`; the dataset is intentionally not committed because of size and provenance considerations. Confirm the exact eight source CSVs and the Thursday Web Attacks file's condition before running any experiment.

## Reported split and preprocessing

The reported final cleaned data contains 2,827,677 rows. The split counts are train 1,809,712; validation 452,429; test 565,536. The numeric model feature count is 72. The imputer and scaler are fit on training data only. The decision threshold 0.4221336 was selected on validation data using F2 and held fixed for test evaluation.

## Model configuration recorded for the reported run

- Autoencoder: 72 -> 128 -> 32 encoder; decoder 32 -> 128 -> 72; ReLU, Adam learning rate 0.001, MSE, 10 epochs.
- k-NN graph: k=10, Euclidean distance, constructed over Z.
- GCN: 32 -> 16 -> 2, cross-entropy, Adam learning rate 0.01, 20 epochs.
- Random Forest: 100 trees, maximum depth 15, `max_features="sqrt"`, balanced class weights, random state 42.
- Fusion: `[Z || H]`, 48 features.

## Caution

These notes record the reported experiment configuration and metrics. They do not assert that a clean rerun was performed from this repository. Runtime and memory use are substantial; document any batching, sampling, library-version, or split changes and do not silently equate changed runs with the reported result.
