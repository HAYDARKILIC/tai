"""Regenerate fig3_rho0_sweep.png (rendered as Figure 3).

The previous version plotted a single series, while the caption describes the
real sweep *and* the rho0-labelled placebo tai_negctrl. This adds the placebo,
which is the series the second half of the caption is about.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, statistics as st
import figlib as F

real = F.by_rho("rho0__dim384__tai__*")
plac = F.by_rho("rho0neg__dim384__tai_negctrl__*")
rhos = sorted(real)
plt.rcParams.update(F.RC)
fig, ax = plt.subplots(figsize=(3.4, 2.5))

for d, colour, marker, lab in [(real, "#0072B2", "o", "tai (real intervention)"),
                               (plac, "#D55E00", "s", "tai_negctrl (placebo)")]:
    mean = [st.mean(d[r].values()) * 100 for r in rhos]
    sd = [st.stdev(d[r].values()) * 100 for r in rhos]
    for r in rhos:
        ax.plot([r] * len(d[r]), [v * 100 for v in d[r].values()], ".",
                color=colour, ms=2.4, alpha=0.45, zorder=2)
    ax.errorbar(rhos, mean, yerr=sd, color=colour, marker=marker, ms=4, lw=1.2,
                elinewidth=0.8, capsize=2, zorder=3, label=lab)

ax.set_xlabel(r"imposed initial active fraction $\rho_0$")
ax.set_ylabel("final ternary sparsity (%)")
ax.tick_params(labelsize=7)
ax.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)
ax.legend(frameon=False, fontsize=7, loc="lower left", handlelength=1.6,
          borderpad=0.1, labelspacing=0.3)
fig.tight_layout(pad=0.4)
F.save(fig, "fig3_rho0_sweep.png")

rr = max(st.mean(real[r].values()) for r in rhos) - min(st.mean(real[r].values()) for r in rhos)
pr = max(st.mean(plac[r].values()) for r in rhos) - min(st.mean(plac[r].values()) for r in rhos)
print("real range %.4f pt | placebo range %.4f pt | ratio %.0f" % (rr*100, pr*100, rr/pr))
print("placebo span %.5f..%.5f" % (min(st.mean(plac[r].values()) for r in rhos),
                                   max(st.mean(plac[r].values()) for r in rhos)))
