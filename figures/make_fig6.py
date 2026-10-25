"""Regenerate fig6_scale.png (rendered as Figure 8).

Two defects. The y-axis read "baseline-best - tai_warmup", naming the
data-selected minimum baseline, while the plotted values are the contrast
against the PRE-REGISTERED baseline bitnet158 (verified against the manifest).
And the caption promises "the fitted slope and its confidence interval",
which the figure did not draw. Both are fixed here; the slope and interval are
the primary scale-mean OLS estimator the manifest records.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, math, statistics as st
import figlib as F

m = F.manifest()
logN = F.logN_by_scale()
L = {}
for r in m["main_results"]:
    L.setdefault(r["size"], {}).setdefault(r["method"], {})[r["seed"]] = r["val_loss"]
scales = sorted(L, key=lambda s: int(s[3:]))

xs, ys, lo, hi = [], [], [], []
for s in scales:
    b, a = L[s]["bitnet158"], L[s]["tai_warmup"]
    d = [b[k] - a[k] for k in sorted(set(b) & set(a))]
    mean, l, h = F.boot_ci(d, seed=int(s[3:]))
    xs.append(logN[s]); ys.append(mean); lo.append(mean - l); hi.append(h - mean)

est = m["h6_slope_estimators"]["scale_mean_ols"]
slope, (s_lo, s_hi) = est["slope"], est["ci"]
grid = np.linspace(min(xs), max(xs), 50)
xbar = st.mean(xs)

plt.rcParams.update(F.RC)
fig, ax = plt.subplots(figsize=(3.4, 2.5))
ybar = st.mean(ys)
ax.fill_between(grid, ybar + s_lo * (grid - xbar), ybar + s_hi * (grid - xbar),
                color="#0072B2", alpha=0.13, lw=0, zorder=1,
                label="95\u2009% CI of the slope")
ax.plot(grid, ybar + slope * (grid - xbar), color="#0072B2", lw=1.3,
        zorder=3, label=f"scale-mean OLS, {slope:+.4f} nats / ln-unit")
ax.errorbar(xs, ys, yerr=[lo, hi], ls="none", marker="o", ms=4,
            color="#0072B2", elinewidth=0.9, capsize=2, zorder=4)
ax.axhline(0, color="0.45", lw=0.8, ls=":", zorder=2)

ax.set_xlabel("non-embedding parameters  (natural log)")
ax.set_ylabel(r"$\Delta\mathcal{L}$ vs \texttt{bitnet158}" if False
              else "ΔL vs bitnet158 (nats)")
sec = ax.secondary_xaxis("top", functions=(lambda v: v, lambda v: v))
sec.set_xticks([math.log(v * 1e6) for v in (1.4, 10, 100, 352)])
sec.set_xticklabels(["1.4 M", "10 M", "100 M", "352 M"], fontsize=6.5)
sec.tick_params(length=2)
ax.tick_params(labelsize=7)
ax.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)
ax.legend(frameon=False, fontsize=6.5, loc="lower left", handlelength=1.6,
          borderpad=0.1, labelspacing=0.3)
fig.tight_layout(pad=0.4)
F.save(fig, "fig6_scale.png")
print("slope %+.4f CI [%+.4f, %+.4f] p=%.4f (%s)"
      % (slope, s_lo, s_hi, est["p"], m["scale_model"]["slope_estimator"]))
print("effects %+.4f .. %+.4f over %d scales" % (min(ys), max(ys), len(ys)))
