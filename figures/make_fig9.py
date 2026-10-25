"""Regenerate fig9_two_slope.png (rendered as Figure 9).

The previous version put the main-ladder slope at -0.009, CI [-0.016,-0.004].
That value is not reproducible from the released artefact: the manifest's four
estimators give -0.0127 (scale-mean OLS, the primary), -0.0126 (clustered by
scale and by seed), and a run-level OLS gives -0.0126 as well. The manuscript
quotes -0.0126. The figure also labelled its x-axis log10 while quoting slopes
per natural log-unit. Both are corrected; the unit is now stated on the axis.
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

main_x, main_y = [], []
for s in L:
    b, a = L[s]["bitnet158"], L[s]["tai_warmup"]
    main_x.append(logN[s])
    main_y.append(st.mean(b[k] - a[k] for k in sorted(set(b) & set(a))))

est = m["h6_slope_estimators"]["scale_mean_ols"]
wc = m["scaling_law_widthctrl"]

plt.rcParams.update(F.RC)
fig, ax = plt.subplots(figsize=(3.4, 2.5))
ax.axhline(0, color="0.45", lw=0.8, ls=":", zorder=1)

for (xlo, xhi), slope, ci, ybar, colour, ls, lab in [
    ((min(main_x), max(main_x)), est["slope"], est["ci"], st.mean(main_y),
     "#0072B2", "-", "main ladder (width and depth)"),
    ((wc["x_min"], wc["x_max"]), wc["slope"], wc["slope_ci"], wc["mean_effect"],
     "#D55E00", "--", "depth-controlled (width only)")]:
    g = np.linspace(xlo, xhi, 50)
    xbar = (xlo + xhi) / 2
    ax.fill_between(g, ybar + ci[0] * (g - xbar), ybar + ci[1] * (g - xbar),
                    color=colour, alpha=0.13, lw=0, zorder=2)
    ax.plot(g, ybar + slope * (g - xbar), color=colour, ls=ls, lw=1.4, zorder=3,
            label=f"{lab}\n{slope:+.4f}  CI [{ci[0]:+.4f}, {ci[1]:+.4f}]")

ax.set_xlabel("non-embedding parameters  (natural log)")
ax.set_ylabel("ΔL vs bitnet158 (nats)")
sec = ax.secondary_xaxis("top", functions=(lambda v: v, lambda v: v))
sec.set_xticks([math.log(v * 1e6) for v in (1.4, 10, 100, 352)])
sec.set_xticklabels(["1.4 M", "10 M", "100 M", "352 M"], fontsize=6.5)
sec.tick_params(length=2)
ax.tick_params(labelsize=7)
ax.grid(True, axis="y", color="0.93", lw=0.6, zorder=0)
ax.legend(frameon=False, fontsize=6.2, loc="lower left", handlelength=1.8,
          borderpad=0.1, labelspacing=0.5)
fig.tight_layout(pad=0.4)
F.save(fig, "fig9_two_slope.png")
print("main ladder  %+.4f CI [%+.4f,%+.4f]" % (est["slope"], *est["ci"]))
print("width-only   %+.4f CI [%+.4f,%+.4f]" % (wc["slope"], *wc["slope_ci"]))
print("slopes are per natural log-unit of non-embedding parameters")
