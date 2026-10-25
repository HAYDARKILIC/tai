"""Regenerate fig10_mechanism.png (rendered as Figure 6).

The panel content was right but the caption called the left panel the INITIAL
operating point, while the plotted quantity is the FINAL learned sparsity.
The locked-baseline annotation was also overlapped by the tai line, and the
titles carried the harness's internal "(R6)" label. Content unchanged in
substance; recomputed from the run store.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statistics as st
import figlib as F

SCALE = "dim384"
sp = {a: F.by_rho(f"rho0__{SCALE}__{a}__*", "final_sparsity")
      for a in ("tai", "gamma_offset")}
ls = {a: F.by_rho(f"rho0__{SCALE}__{a}__*", "val_loss")
      for a in ("tai", "gamma_offset")}
rhos = sorted(sp["tai"])
LOCKED = 1 - 0.6899357          # analytic locked sparsity, Proposition 1

plt.rcParams.update(F.RC)
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.1, 2.6))

axL.axhline(LOCKED * 100, color="0.45", lw=0.9, ls=":", zorder=1)
axL.annotate(f"locked baseline, {LOCKED*100:.1f}\\%" if False
             else f"locked baseline, {LOCKED*100:.1f}%",
             xy=(rhos[-1], LOCKED * 100), xytext=(-2, -9),
             textcoords="offset points", ha="right", fontsize=6.5, color="0.40")
for arm, colour, marker, lab in [("tai", "#D55E00", "o", "tai (shapes the initializer)"),
                                 ("gamma_offset", "#009E73", "s", "gamma_offset (shifts the threshold)")]:
    axL.errorbar(rhos, [st.mean(sp[arm][r].values()) * 100 for r in rhos],
                 yerr=[st.stdev(sp[arm][r].values()) * 100 for r in rhos],
                 color=colour, marker=marker, ms=4, lw=1.2, elinewidth=0.8,
                 capsize=2, zorder=3, label=lab)
axL.set_xlabel(r"target $\rho_0$")
axL.set_ylabel("final ternary sparsity (%)")
axL.set_title("(a) Where each mechanism ends up", fontsize=8.5, loc="left")
axL.tick_params(labelsize=7.5)
axL.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)
axL.legend(frameon=False, fontsize=6.8, loc="upper right", handlelength=1.6,
           borderpad=0.1, labelspacing=0.3)

means, los, his = [], [], []
for r in rhos:
    seeds = sorted(set(ls["tai"][r]) & set(ls["gamma_offset"][r]))
    d = [ls["tai"][r][k] - ls["gamma_offset"][r][k] for k in seeds]
    mn, lo, hi = F.boot_ci(d, seed=int(r * 10))
    means.append(mn); los.append(lo); his.append(hi)
axR.axhline(0, color="#CC79A7", lw=1.0, ls="--", zorder=1)
axR.fill_between(rhos, los, his, color="0.75", alpha=0.45, lw=0, zorder=2,
                 label="95 % bootstrap CI")
axR.plot(rhos, means, color="0.25", marker="o", ms=4, lw=1.2, zorder=3)
axR.set_xlabel(r"target $\rho_0$")
axR.set_ylabel("ΔL: tai − gamma_offset (nats)")
axR.set_title("(b) Which mechanism reaches it at lower loss", fontsize=8.5, loc="left")
axR.annotate("tai worse", xy=(0.03, 0.90), xycoords="axes fraction", fontsize=6.8, color="0.40")
axR.annotate("tai better", xy=(0.03, 0.05), xycoords="axes fraction", fontsize=6.8, color="0.40")
axR.tick_params(labelsize=7.5)
axR.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)
axR.legend(frameon=False, fontsize=6.8, loc="upper right", borderpad=0.1)

fig.tight_layout(pad=0.4)
F.save(fig, "fig10_mechanism.png")
print("tai sparsity span %.2f pt | gamma_offset %.2f pt"
      % ((max(st.mean(sp['tai'][r].values()) for r in rhos)
          - min(st.mean(sp['tai'][r].values()) for r in rhos)) * 100,
         (max(st.mean(sp['gamma_offset'][r].values()) for r in rhos)
          - min(st.mean(sp['gamma_offset'][r].values()) for r in rhos)) * 100))
print("pooled mean dL %+.4f over %d cells" % (st.mean(means) , 6))
