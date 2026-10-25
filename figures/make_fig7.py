"""Regenerate fig7_h3_falsification.png (rendered as Figure 4).

Earlier defects: the left panel was a boxplot of two degenerate distributions
and rendered as bare lines; the title foregrounded the signed sign test, which
Section 4.7 sets aside as uninterpretable; and the real-versus-placebo
magnitude ratio, which the section calls the interpretable result, was absent.
The sweep itself now lives in Figure 3, so this figure carries the two
falsification statistics instead: the per-seed rank coefficients and the three
magnitudes. The placebo's per-seed coefficients are computed from its own runs.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, statistics as st
from scipy import stats as sps
import figlib as F

real = F.by_rho("rho0__dim384__tai__*", "final_sparsity")
plac = F.by_rho("rho0neg__dim384__tai_negctrl__*", "final_sparsity")
rhos = sorted(real)


def per_seed_rho(d):
    seeds = sorted(set.intersection(*[set(d[r]) for r in rhos]))
    return [sps.spearmanr(rhos, [d[r][s] for r in rhos]).correlation for s in seeds]


rho_real, rho_plac = per_seed_rho(real), per_seed_rho(plac)
rng = lambda d: max(st.mean(d[r].values()) for r in rhos) - min(st.mean(d[r].values()) for r in rhos)
real_range, plac_range = rng(real), rng(plac)
noise = st.mean(st.stdev(real[r].values()) for r in rhos)

plt.rcParams.update(F.RC)
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.1, 2.5),
                               gridspec_kw={"width_ratios": [1, 1.3]})

# (a) per-seed rank coefficients
rngen = np.random.default_rng(0)
for x, vals, colour, lab in [(0, rho_real, "#0072B2", "tai (real)"),
                             (1, rho_plac, "#D55E00", "tai_negctrl\n(placebo)")]:
    axL.plot(x + rngen.uniform(-0.09, 0.09, len(vals)), vals, "o", ms=3.4,
             mfc=colour, mec="none", alpha=0.6, zorder=2)
    axL.plot([x - 0.22, x + 0.22], [st.mean(vals)] * 2, color=colour, lw=2, zorder=3)
    axL.annotate(f"mean {st.mean(vals):+.3f}", xy=(x, st.mean(vals)),
                 xytext=(0, 9), textcoords="offset points", ha="center",
                 fontsize=6.8, color=colour)
axL.axhline(0, color="0.45", lw=0.8, ls=":", zorder=1)
axL.set_xticks([0, 1]); axL.set_xticklabels(["tai (real)", "tai_negctrl\n(placebo)"], fontsize=7)
axL.set_xlim(-0.5, 1.5); axL.set_ylim(-1.12, 0.62)
axL.set_ylabel(r"per-seed Spearman $\rho_0$ vs sparsity")
axL.set_title("(a) Rank association, one point per seed", fontsize=8.5, loc="left")
axL.tick_params(labelsize=7.5)
axL.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)

# (b) the three magnitudes
items = [("real intervention\n(across-$\\rho_0$ range)", real_range * 100, "#0072B2",
          "%.2f pt" % (real_range * 100)),
         ("seed nuisance\n(within-$\\rho_0$ SD)", noise * 100, "0.55",
          "%.4f pt  (1/%.1f of the effect)" % (noise * 100, real_range / noise)),
         ("placebo\n(across-label range)", plac_range * 100, "#D55E00",
          "%.4f pt  (1/%.0f)" % (plac_range * 100, real_range / plac_range))]
for y, (lab, v, c, note) in enumerate(items):
    axR.barh(y, v, height=0.52, color=c, zorder=3)
    axR.text(v * 1.45, y, note, va="center", fontsize=6.8, color="0.25")
axR.set_yticks(range(len(items)))
axR.set_yticklabels([i[0] for i in items], fontsize=7)
axR.invert_yaxis()
axR.set_xscale("log"); axR.set_xlim(5e-3, 400)
axR.set_xticks([1e-2, 1e-1, 1e0, 1e1])
axR.set_xlabel("magnitude (percentage points, log scale)")
axR.set_title("(b) Effect, nuisance and placebo", fontsize=8.5, loc="left")
axR.tick_params(labelsize=7.5)
axR.grid(True, axis="x", color="0.92", lw=0.6, zorder=0)

fig.tight_layout(pad=0.4)
F.save(fig, "fig7_h3_falsification.png")
print("per-seed Spearman: real mean %+.4f (n=%d) | placebo mean %+.4f (n=%d)"
      % (st.mean(rho_real), len(rho_real), st.mean(rho_plac), len(rho_plac)))
print("real range %.4f pt | noise %.4f pt | placebo %.4f pt" %
      (real_range * 100, noise * 100, plac_range * 100))
print("SNR %.1f | real/placebo %.0f" % (real_range / noise, real_range / plac_range))
