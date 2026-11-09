# Early warning screening of public procurement in Kazakhstan (pilot)

Code and aggregate results for the pilot study *"Big Data-Driven Early Warning System for Detecting Anomalous Competitive Behavior in Public Procurement Using Machine Learning and Graph-Based Analysis"* (Research Methods and Tools, Astana IT University).

Authors: Zhan Tabuldinov, Almas Nurkaliyev, Daulet Kazmukhambetov.

## Version and citation

The reported pilot was committed as [`d4ab268d8914a893f4cdadf4bbe625b0ab30a025`](https://github.com/zzkhxyz/kz-procurement-early-warning/tree/d4ab268d8914a893f4cdadf4bbe625b0ab30a025) on 25 October 2026 (UTC+05:00). The MIT code license and CC BY 4.0 aggregate-results license were added in the later commit [`0b8facfbe45dbf6ef2b491ab0bb734d4eccfc8bf`](https://github.com/zzkhxyz/kz-procurement-early-warning/commit/0b8facfbe45dbf6ef2b491ab0bb734d4eccfc8bf). [Release `v1.0.0`](https://github.com/zzkhxyz/kz-procurement-early-warning/releases/tag/v1.0.0) archives commit [`f55ccd3508084e203f8e9aedf0c48544670df155`](https://github.com/zzkhxyz/kz-procurement-early-warning/commit/f55ccd3508084e203f8e9aedf0c48544670df155), including the license-bearing code and public aggregate results. Cite the **version-specific DOI** [10.5281/zenodo.24089663](https://doi.org/10.5281/zenodo.24089663) for this archive. The DOI identifies the published code-and-results archive; the SHA-256 in `run_log.json` identifies the private source export manifest. This README was updated after the immutable `v1.0.0` tag and is not part of that archived version. See `CITATION.cff` for citation metadata.

## What the pilot does

Three ranking methods are compared on the same held-out test cohort of Mitwork procurement lots:

1. a five-flag red-flag baseline,
2. a tabular Isolation Forest,
3. a graph-enriched Isolation Forest (supplier co-bidding features).

Cohort: 115,177 lots with bid deadlines from 1 Oct 2025 to 30 Sep 2026. Chronological split: train Oct 2025 – Jun 2026 (80,293), validation Jul 2026 (12,535), test Aug – Sep 2026 (22,349).

The results are **preliminary**. Blinded manual review of the selected cases is pending, so Precision@K and Lift@K are not reported yet. The graph-enriched model uses participants observed in the current lot and is a conditional retrospective variant, not a validated real-time system.

## Repository structure

```
notebooks/procurement_screening_pilot_v3.ipynb   full pipeline (outputs cleared)
results/audit/       data audit: row counts, key checks, missingness, monthly coverage
results/pilot_v3/    model results used in the article
figures/             article figures and the script that draws them
data/                empty; raw data are not distributed (see below)
```

The article uses only **Part XIII and later** of the notebook (the specification-aligned v3 run). Parts IV–XII are an earlier exploratory version and are kept for transparency only.

| File in `results/pilot_v3/` | Used in the article |
|---|---|
| `tab_data_account.csv` | Table I (partitions, observed participation) |
| `synthetic_recovery.csv` | Table III, Fig. 1 |
| `tab_contrasts.csv` | Table IV |
| `tab_main.csv`, `seed_jaccard_45pairs.csv` | Table V, Fig. 2 |
| `tuning_validation.csv` | validation selection (200 trees, `max_samples=128`) |
| `window_sensitivity.csv` | graph-window sensitivity (Table V) |
| `run_log.json` | seeds, parameters, environment, data-manifest hash |

## Data availability

The public aggregate CSV and JSON files are in `results/` and are licensed CC BY 4.0 under `results/LICENSE.md`. The code is MIT licensed under the root `LICENSE`. The source export manifest SHA-256 is `3448f1f77b8c60f5f161f26e2bc814b1e13197a3f97a218f95a08773f1c5b011`; it identifies the private source export manifest, not a public data archive. No raw Mitwork records, participant identifiers, lot-level rankings, or manual-review workbook are distributed.

The pipeline runs on a private export of the Mitwork procurement database (tables `mw_buys`, `mw_lots`, `mw_offers`, `mw_subjects`, exported 24 Oct 2026). Raw records, lot-level rankings and the blinded review workbook contain administrative identifiers and are **not** included. Access may be requested from the authors, subject to permission from the data holder. The SHA-256 hash of the export manifest is recorded in `results/pilot_v3/run_log.json`.

To rerun the notebook, place the four Parquet files and `export_manifest.json` in `data/raw/` and run all cells in order.

## Environment

The pilot notebook metadata and `run_log.json` record Python 3.13.9. `requirements.txt` pins pandas 2.3.3 and NetworkX 3.5; the original versions of scikit-learn, NumPy, SciPy, Matplotlib, seaborn and PyArrow were not preserved in the public run metadata. The unchanged pilot environment is unavailable here, so there is no historical `requirements-lock.txt`. Installing `requirements.txt` today creates a new environment and has not been shown to reproduce the reported results. Running the complete notebook also requires access to the restricted source export.

Python 3.13.9 on Windows 11 (Intel CPU). See `requirements.txt`. Seeds: 42–51 for Isolation Forest, 20261013 for the synthetic insertion and the bootstrap.

To redraw the article figures from the aggregate results:

```
python figures/make_figs.py results/pilot_v3 figures
```
