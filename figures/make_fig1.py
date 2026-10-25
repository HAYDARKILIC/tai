"""Regenerate fig1_convergence.png (rendered as Figure 1).

Four defects in the previous version: it plotted dim1536 while the caption
says the primary confirmatory scale (dim384); its y-axis was training loss
while the caption says held-out loss; its title claimed 15 seeds although
dim1536 was run with 5; and it drew no confidence bands although the caption
promises bootstrap 95% intervals. This version is the primary scale, the
held-out validation trace, all 15 seeds, all nine arms, with the bands.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import figlib as F

SCALE = "dim384"
rec = {}
for arm in F.ARM_ORDER:
    rs = F.runs(f"main__{SCALE}__{arm}__*")
    if rs:
        rec[arm] = rs

steps = rec["bitnet158"][0]["val_steps"]
plt.rcParams.update(F.RC)
fig, ax = plt.subplots(figsize=(3.4, 2.9))

for arm, rs in rec.items():
    traces = np.array([r["val_trace"] for r in rs], dtype=float)
    mean = traces.mean(axis=0)
    lo, hi = [], []
    for j in range(traces.shape[1]):
        _m, l, h = F.boot_ci(traces[:, j], seed=j)
        lo.append(l); hi.append(h)
    c = F.ARM_COLOUR[arm]
    ax.fill_between(steps, lo, hi, color=c, alpha=0.18, lw=0, zorder=2)
    ax.plot(steps, mean, color=c, lw=1.2, zorder=3, label=arm)

ax.set_xlabel("optimizer step")
ax.set_ylabel("held-out loss (nats/token)")
ax.set_xlim(0, max(steps) * 1.02)
ax.tick_params(labelsize=7)
ax.grid(True, color="0.93", lw=0.6, zorder=0)
ax.legend(frameon=False, fontsize=6.3, ncol=2, loc="upper right",
          handlelength=1.4, columnspacing=0.8, labelspacing=0.25,
          borderpad=0.0)

# An inset on the final third, where the arms separate.
ins = ax.inset_axes([0.46, 0.30, 0.52, 0.34])
k = [i for i, s in enumerate(steps) if s >= 0.62 * max(steps)]
for arm, rs in rec.items():
    traces = np.array([r["val_trace"] for r in rs], dtype=float)
    lo, hi = [], []
    for j in k:
        _m, l, h = F.boot_ci(traces[:, j], seed=j)
        lo.append(l); hi.append(h)
    xs = [steps[i] for i in k]
    ins.fill_between(xs, lo, hi, color=F.ARM_COLOUR[arm], alpha=0.22, lw=0)
    ins.plot(xs, traces.mean(axis=0)[k], color=F.ARM_COLOUR[arm], lw=1.1)
ins.tick_params(labelsize=5.5, pad=1)
ins.grid(True, color="0.93", lw=0.5)
for sp in ins.spines.values():
    sp.set_linewidth(0.5)

fig.tight_layout(pad=0.4)
F.save(fig, "fig1_convergence.png")
print("arms:", list(rec), "| seeds:", {a: len(r) for a, r in rec.items()})
print("probes:", len(steps), "final step:", steps[-1])
