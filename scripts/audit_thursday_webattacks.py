#!/usr/bin/env python3
"""Audit the CIC-IDS2017 Thursday Morning WebAttacks source CSV without retraining.

Usage:
  python scripts/audit_thursday_webattacks.py /path/to/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv --output-dir thursday_webattacks_audit
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

METADATA = {"flow id", "source ip", "destination ip", "timestamp"}


def label_text(value):
    if pd.isna(value):
        return "<MISSING_LABEL>"
    value = str(value).strip()
    return value if value else "<BLANK_LABEL>"


def audit(source: Path, out: Path, chunksize: int = 25000):
    if not source.is_file():
        raise FileNotFoundError(source)
    out.mkdir(parents=True, exist_ok=True)

    # Independent CSV-parser check: the header and every non-empty record
    # should have the same number of fields.
    width_counts = Counter()
    blank_records = 0
    with source.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.reader(f)
        try:
            header = [str(c).strip() for c in next(reader)]
        except StopIteration:
            raise ValueError("CSV is empty")
        for row in reader:
            if not row or all(str(v).strip() == "" for v in row):
                blank_records += 1
            else:
                width_counts[len(row)] += 1
    wrong_width = sum(n for width, n in width_counts.items() if width != len(header))

    totals = Counter()
    per_col = {}
    raw_labels = Counter()
    kept_labels = Counter()
    excluded_by_reason_label = Counter()
    hashes_seen = set()
    valid_hashes_seen = set()
    columns = None
    label_col = None
    numeric_cols = None

    # Read as strings so chunk-to-chunk dtype inference cannot change fingerprints.
    for chunk_no, df in enumerate(pd.read_csv(
        source, chunksize=chunksize, dtype="string", encoding="utf-8-sig",
        keep_default_na=True, on_bad_lines="error"
    )):
        df.columns = [str(c).strip() for c in df.columns]
        if columns is None:
            columns = list(df.columns)
            by_lower = {c.casefold(): c for c in columns}
            if len(by_lower) != len(columns):
                raise ValueError("Column names collide after trimming whitespace.")
            label_col = by_lower.get("label")
            if label_col is None:
                raise ValueError("Could not identify a Label column.")
            numeric_cols = [c for c in columns if c != label_col and c.casefold() not in METADATA]
            per_col = {c: Counter() for c in columns}
        elif list(df.columns) != columns:
            raise ValueError(f"Column schema changed in chunk {chunk_no}.")

        totals["rows"] += len(df)
        missing = df.isna()
        any_missing = missing.any(axis=1)
        totals["rows_any_missing"] += int(any_missing.sum())
        totals["missing_cells"] += int(missing.to_numpy().sum())

        whitespace_row = pd.Series(False, index=df.index)
        for c in columns:
            s = df[c]
            per_col[c]["missing_cells"] += int(s.isna().sum())
            per_col[c]["rows_with_missing"] += int(s.isna().sum())
            blank = s.eq("").fillna(False)
            whitespace = s.str.len().gt(0).fillna(False) & s.str.strip().eq("").fillna(False)
            per_col[c]["blank_string_cells"] += int(blank.sum())
            per_col[c]["whitespace_only_cells"] += int(whitespace.sum())
            whitespace_row |= whitespace
        totals["rows_any_whitespace_only"] += int(whitespace_row.sum())

        labels = df[label_col].map(label_text)
        raw_labels.update(labels.tolist())
        missing_label = labels.isin(["<MISSING_LABEL>", "<BLANK_LABEL>"])
        totals["rows_missing_or_blank_label"] += int(missing_label.sum())

        any_inf = pd.Series(False, index=df.index)
        for c in numeric_cols:
            values = pd.to_numeric(df[c], errors="coerce")
            floats = values.to_numpy(dtype="float64", na_value=np.nan)
            inf = pd.Series(np.isinf(floats), index=df.index)
            per_col[c]["infinite_values"] += int(inf.sum())
            per_col[c]["non_numeric_nonmissing_cells"] += int((df[c].notna() & values.isna()).sum())
            any_inf |= inf

        totals["rows_any_infinity"] += int(any_inf.sum())
        totals["rows_missing_and_infinity"] += int((any_missing & any_inf).sum())
        invalid = any_missing | any_inf
        totals["rows_invalid_union"] += int(invalid.sum())
        totals["rows_retained_before_dedup"] += int((~invalid).sum())
        kept_labels.update(labels.loc[~invalid].tolist())

        for reason, mask in [
            ("missing_only", any_missing & ~any_inf),
            ("infinity_only", any_inf & ~any_missing),
            ("missing_and_infinity", any_missing & any_inf),
        ]:
            counts = labels.loc[mask].value_counts(dropna=False)
            for lab, count in counts.items():
                excluded_by_reason_label[(reason, str(lab))] += int(count)

        # 64-bit fingerprints are memory-conscious duplicate candidates.
        # Report them as fingerprints, not as a mathematical proof of equality.
        row_hashes = pd.util.hash_pandas_object(df.fillna("<MISSING_CELL>"), index=False).to_numpy(dtype="uint64")
        valid_hashes = row_hashes[(~invalid).to_numpy()]
        for h in row_hashes:
            v = int(h)
            if v in hashes_seen:
                totals["repeated_fingerprints_raw"] += 1
            else:
                hashes_seen.add(v)
        for h in valid_hashes:
            v = int(h)
            if v in valid_hashes_seen:
                totals["repeated_fingerprints_retained"] += 1
            else:
                valid_hashes_seen.add(v)

    if columns is None:
        raise ValueError("No data rows parsed.")

    summary = {
        "source_file": str(source),
        "parsed_data_rows": int(totals["rows"]),
        "column_count": len(columns),
        "header_field_count": len(header),
        "rows_with_any_missing_value": int(totals["rows_any_missing"]),
        "missing_cells_total": int(totals["missing_cells"]),
        "rows_with_missing_or_blank_label": int(totals["rows_missing_or_blank_label"]),
        "rows_with_any_numeric_infinity": int(totals["rows_any_infinity"]),
        "rows_with_missing_and_infinity": int(totals["rows_missing_and_infinity"]),
        "rows_invalid_union_missing_or_infinity": int(totals["rows_invalid_union"]),
        "rows_retained_by_rule_before_dedup": int(totals["rows_retained_before_dedup"]),
        "raw_repeated_row_fingerprints_not_proven_exact": int(totals["repeated_fingerprints_raw"]),
        "retained_repeated_row_fingerprints_not_proven_exact": int(totals["repeated_fingerprints_retained"]),
        "rows_with_whitespace_only_cells": int(totals["rows_any_whitespace_only"]),
        "blank_csv_records": int(blank_records),
        "csv_rows_with_wrong_field_count": int(wrong_width),
        "label_column": label_col,
        "note": "Diagnostic only; does not modify source data or retrain models. Fingerprints are 64-bit hashes and are not proof of exact duplicate equality."
    }

    pd.DataFrame([{"metric": k, "value": v} for k, v in summary.items()]).to_csv(out / "row_filter_summary.csv", index=False)
    pd.DataFrame([
        {
            "column": c,
            "is_label_column": c == label_col,
            "missing_cells": per_col[c]["missing_cells"],
            "rows_with_missing": per_col[c]["rows_with_missing"],
            "blank_string_cells": per_col[c]["blank_string_cells"],
            "whitespace_only_cells": per_col[c]["whitespace_only_cells"],
            "infinite_values_numeric_candidate": per_col[c]["infinite_values"],
            "non_numeric_nonmissing_cells_numeric_candidate": per_col[c]["non_numeric_nonmissing_cells"],
        } for c in columns
    ]).to_csv(out / "column_missingness_and_numeric_audit.csv", index=False)
    labels_union = sorted(set(raw_labels) | set(kept_labels))
    pd.DataFrame([
        {
            "label": lab,
            "raw_rows": raw_labels.get(lab, 0),
            "retained_before_dedup_rows": kept_labels.get(lab, 0),
            "excluded_by_missing_or_infinity_rows": raw_labels.get(lab, 0) - kept_labels.get(lab, 0)
        } for lab in labels_union
    ]).to_csv(out / "label_counts_before_after_filter.csv", index=False)
    pd.DataFrame([
        {"exclusion_reason": reason, "label": lab, "rows": n}
        for (reason, lab), n in sorted(excluded_by_reason_label.items())
    ]).to_csv(out / "excluded_rows_by_reason_and_label.csv", index=False)
    (out / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "README.txt").write_text(
        "Audit outputs: row_filter_summary.csv; column_missingness_and_numeric_audit.csv; "
        "label_counts_before_after_filter.csv; excluded_rows_by_reason_and_label.csv; audit_summary.json.\\n"
        "This is a diagnostic audit. It does not modify the source CSV or retrain models. "
        "Whitespace-only cells are reported separately because pandas dropna does not remove them by default. "
        "Row fingerprints are 64-bit hashes, not proof of exact duplicate equality.\\n",
        encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("thursday_webattacks_audit"))
    parser.add_argument("--chunksize", type=int, default=25000)
    args = parser.parse_args()
    print(json.dumps(audit(args.csv_path, args.output_dir, args.chunksize), indent=2))
    print(f"Audit outputs written to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
