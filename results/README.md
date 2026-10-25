# TAI results — generated 2026-08-22 09:01

| file | what it is |
|---|---|
| `tai_manifest.json` | full provenance: config, every revision R0-R31 with its reasoning, per-cell analysis summary, diverged-run list, reproducibility class, SHA hash |
| `results_all_runs.csv` | one tidy row per completed run — the data availability artifact |
| `analysis_summary.csv` | per-(scale, method) aggregates behind the figures |
| `results_main.tex` | main results table, LaTeX |
| `results_controls.tex` | control-arm table, LaTeX |
| `figure_captions.md` | draft captions for fig1-fig10 |
| `../figures/*.png` | 300 dpi figures |
| `../runs/*.json` | raw per-run records (source of truth; every table above is derived from these) |
| `../logs/console_*.log` | mirrored console, including the H1-H8 verdicts printed by the statistics cell |

Reproducing the analysis needs no GPU: the run store is complete, so the
statistics, figure and export cells can be re-run from it at any time.
