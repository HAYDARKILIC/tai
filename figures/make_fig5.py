"""Regenerate fig5_pareto.png (rendered as Figure 5).

The previous version plotted only the tai arm, whose sparsity axis spans
2.6 points. Section 4.8 is about the contrast with the threshold-offset arm,
which traces a U-shaped frontier spanning 50 points with an interior optimum,
and that arm was missing. Both arms are now shown, at both swept scales.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statistics as st
import figlib as F

plt.rcParams.update(F.RC)
fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.8))
summary = {}

for ax, scale in zip(axes, ["dim384", "dim768"]):
    for arm, colour, marker, lab in [("tai", "#D55E00", "o", "tai (initialization)"),
                                     ("gamma_offset", "#009E73", "s", "gamma_offset (threshold)")]:
        sp = F.by_rho(f"rho0__{scale}__{arm}__*", "final_sparsity")
        ls = F.by_rho(f"rho0__{scale}__{arm}__*", "val_loss")
        rhos = sorted(sp)
        xs = [st.mean(sp[r].values()) * 100 for r in rhos]
        ys = [st.mean(ls[r].values()) for r in rhos]
        ax.plot(xs, ys, marker=marker, color=colour, ms=4, lw=1.2, label=lab, zorder=3)
        best = min(range(len(rhos)), key=lambda i: ys[i])
        ax.plot(xs[best], ys[best], marker="o", mfc="none", mec=colour, ms=10,
                mew=1.3, zorder=4)
        off, ha = ((-8, -2), "right") if arm == "tai" else ((0, 6), "center")
        for i, r in enumerate(rhos):
            ax.annotate(f"{r:.1f}", (xs[i], ys[i]), textcoords="offset points",
                        xytext=off, ha=ha, va="center" if arm == "tai" else "bottom",
                        fontsize=5.8, color="0.35")
        summary[(scale, arm)] = (min(xs), max(xs), rhos[best], ys[best])
    ax.set_xlabel("final ternary sparsity (%)")
    ax.set_title(f"\\texttt{{{scale}}}" if False else scale, fontsize=8.5, loc="left")
    ax.tick_params(labelsize=7.5)
    ax.grid(True, color="0.93", lw=0.6, zorder=0)
    ax.margins(x=0.09, y=0.14)
    ax.legend(frameon=False, fontsize=7, loc="upper center", handlelength=1.6,
              borderpad=0.1, labelspacing=0.3)

axes[0].set_ylabel("held-out loss (nats/token)")
fig.tight_layout(pad=0.4)
F.save(fig, "fig5_pareto.png")
for k, v in summary.items():
    print("%-22s sparsity span %5.1f..%5.1f pt (%4.1f wide), min at rho0=%.1f, L=%.4f"
          % (k, v[0], v[1], v[1] - v[0], v[2], v[3]))
