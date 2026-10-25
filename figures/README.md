# Figure pipeline

Each script regenerates one figure of the paper from `../runs/` and
`../results/tai_manifest.json`, and writes it into `../manuscript/figures/`.
The filename says which PNG it produces, not which number the figure carries
in the paper — LaTeX numbers floats by source order:

| script | PNG | figure in the paper |
|---|---|---|
| `make_fig1.py` | `fig1_convergence.png` | Figure 1 |
| `make_fig2.py` | `fig2_final_loss.png` | Figure 2 |
| `make_fig3.py` | `fig3_rho0_sweep.png` | Figure 3 |
| `make_fig7.py` | `fig7_h3_falsification.png` | Figure 4 |
| `make_fig5.py` | `fig5_pareto.png` | Figure 5 |
| `make_fig10.py` | `fig10_mechanism.png` | Figure 6 |
| `make_fig8.py` | `fig8_init_ablation.png` | Figure 7 |
| `make_fig6.py` | `fig6_scale.png` | Figure 8 |
| `make_fig9.py` | `fig9_two_slope.png` | Figure 9 |
| `make_fig4.py` | `fig4_lmeval.png` | Figure 10 |

`figlib.py` holds the shared loaders, the per-arm colour map (Okabe-Ito,
colour-blind safe) and the bootstrap helper. It also defines `CALIB_SEEDS`,
the calibration seeds that are present in the run store but excluded from every
reported statistic; every loader drops them.

Each script prints the quantities it plotted, so its output can be checked
against the corresponding table in the paper without opening the figure.

```bash
pip install -r ../requirements.txt
for f in make_fig*.py; do python "$f"; done
```
