"""Regenerate fig2_final_loss.png as a paired-difference chart.

The previous version plotted absolute held-out loss as bars anchored at zero,
so 0.06-0.20 nat effects were invisible. This plots the paired contrast the
paper actually reports, DeltaL = L(bitnet158) - L(arm), positive = better than
the pre-registered baseline, with bootstrap 95% CIs, across all eleven scales.
All values are computed from the released manifest; nothing is hand-entered.
"""
import json, io, math, statistics as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figlib as F
MANIFEST = F.MANIFEST
BASE = "bitnet158"
RNG = np.random.default_rng(0)

m = json.load(io.open(MANIFEST, encoding="utf-8"))

loss, logN = {}, {}
for r in m["main_results"]:
    loss.setdefault(r["size"], {}).setdefault(r["method"], {})[r["seed"]] = r["val_loss"]
for ln, _seed, _y, size, _tag in m["scale_model"]["points"]:
    logN[size] = ln

scales = sorted(loss, key=lambda s: int(s[3:]))
params_M = [math.exp(logN[s]) / 1e6 for s in scales]


def paired(size, arm):
    """Mean paired DeltaL and its bootstrap 95% CI, or None if the arm is absent."""
    if arm not in loss[size]:
        return None
    b, a = loss[size][BASE], loss[size][arm]
    seeds = sorted(set(b) & set(a))
    d = np.array([b[k] - a[k] for k in seeds])
    bs = RNG.choice(d, size=(5000, d.size), replace=True).mean(axis=1)
    return d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


# Okabe-Ito, colour-blind safe.
PANELS = [
    ("(a) Threshold-aware arms", [
        ("tai_warmup",   "#0072B2", "o", "-"),
        ("tai",          "#D55E00", "s", "-"),
        ("tai_star",     "#CC79A7", "D", "--"),
    ]),
    ("(b) Baselines and controls", [
        ("gamma_offset", "#009E73", "^", "-"),
        ("lsuv",         "#56B4E9", "v", "-"),
        ("standard",     "#666666", "P", "-"),
        ("sparse_sched", "#E69F00", "X", "-"),
        ("fp16_control", "#000000", "*", ":"),
    ]),
]

plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.7,
                     "xtick.direction": "in", "ytick.direction": "in"})
fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.9), sharey=True)

for ax, (title, arms) in zip(axes, PANELS):
    ax.axhline(0.0, color="0.25", lw=0.9, zorder=1)
    for arm, colour, marker, ls in arms:
        xs, ys, lo, hi = [], [], [], []
        for x, s in zip(params_M, scales):
            r = paired(s, arm)
            if r is None:
                continue
            xs.append(x); ys.append(r[0]); lo.append(r[0] - r[1]); hi.append(r[2] - r[0])
        ax.errorbar(xs, ys, yerr=[lo, hi], color=colour, marker=marker, ls=ls,
                    ms=3.6, lw=1.0, elinewidth=0.7, capsize=1.6,
                    label=arm.replace("_", r"\_") if False else arm, zorder=3)
    ax.set_xscale("log")
    ax.set_xlabel("non-embedding parameters (M)")
    ax.set_title(title, fontsize=8.5, loc="left")
    ax.grid(True, which="major", axis="y", color="0.9", lw=0.6, zorder=0)
    ax.set_xticks([1.4, 10, 100, 352])
    ax.set_xticklabels(["1.4", "10", "100", "352"])
    ax.tick_params(labelsize=7.5)
    first = title.startswith("(a)")
    ax.legend(frameon=False, fontsize=6.8, handlelength=1.6, borderpad=0.1,
              labelspacing=0.22, columnspacing=1.0,
              ncol=1 if first else 2,
              loc="lower left" if first else "upper left")

axes[0].set_ylabel("ΔL vs bitnet158 (nats)\npositive = better than baseline")
fig.tight_layout(pad=0.4)
F.save(fig, "fig2_final_loss.png")
print("written")

# Echo the plotted numbers so they can be checked against the tables.
for arm in ["tai_warmup", "tai", "fp16_control"]:
    vals = [paired(s, arm)[0] for s in scales if paired(s, arm)]
    print(f"{arm:14s} min {min(vals):+.4f}  max {max(vals):+.4f}  n={len(vals)}")
