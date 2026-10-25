# Figure captions (draft)

Plot titles in the notebook are working labels. Several assert a conclusion; a
caption should describe what is shown and let the text draw the inference.
Rewrite freely -- these are neutral starting points.

**fig1_convergence.png**

Training loss against optimisation step for each initialisation strategy at the primary confirmatory scale, averaged over 15 seeds at a matched 20M-token budget. Shaded bands are bootstrap 95% CIs.

**fig2_final_loss.png**

Final held-out loss by initialisation strategy at each confirmatory scale. Points are per-seed values; bars show the mean with a bootstrap 95% CI.

**fig3_rho0_sweep.png**

Final weight sparsity as a function of the initial active ratio rho0, for the TAI arm and the rho0-labelled placebo. The placebo holds the true split fixed at 0.69 while varying only the label, so any dependence it shows is measurement artifact.

**fig4_lmeval.png**

Zero-shot accuracy on ARC-Easy and HellaSwag (log-likelihood scoring) by initialisation strategy. Both plain and length-normalised accuracy are reported.

**fig5_pareto.png**

Quality against sparsity across the rho0 sweep. Each point is one operating point; the frontier shows the achievable trade-off at a fixed token budget.

**fig6_scale.png**

Effect size across the model-scale ladder, with the mixed-effects slope and its confidence interval. Depth-controlled points are shown separately.

**fig7_h3_falsification.png**

Pre-registered falsification for H3. Left: the real rho0 sweep against the placebo arm. Right: signal-to-noise ratio between them.

**fig8_init_ablation.png**

Decomposition of the effect into initialisation distribution versus threshold control, comparing TAI against the mechanism-matched gamma-offset arm.

**fig9_two_slope.png**

Scaling slope estimated with width and depth varying together, against the depth-controlled ladder in which depth is held fixed.

**fig10_mechanism.png**

Left: initial operating point reached by each mechanism. Right: paired difference between TAI and the gamma-offset control, with a 95% CI; an interval covering zero indicates the two mechanisms are matched.

