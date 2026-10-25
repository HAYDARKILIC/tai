"""Regenerate fig4_lmeval.png.

Two defects in the previous version: it plotted dim1536 while the text
announces it as showing the primary-scale metrics of Table 12, and it drew
zero-anchored bars so that accuracies in [0.22, 0.31] were indistinguishable
against a chance rate of 0.25. This version plots the primary scale and shows
each accuracy against the chance rate and the sampling-noise band of a
300-item subset, which is the comparison the section actually argues.
All values are computed from the released manifest.
"""
import json, io, math, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figlib as F
MANIFEST = F.MANIFEST
SCALE = "dim384"          # the primary confirmatory scale, as in Table 12
CHANCE = 0.25
N_ITEMS = 300             # three seeds x 100 items, per the table caption
SE = math.sqrt(CHANCE * (1 - CHANCE) / N_ITEMS)

m = json.load(io.open(MANIFEST, encoding="utf-8"))
finite = lambda v: v is not None and not (isinstance(v, float) and math.isnan(v))

ARMS = ["fp16_control", "standard", "lsuv", "bitnet158", "sparse_sched",
        "gamma_offset", "tai", "tai_warmup"]
METRICS = [("arc_easy_acc", "ARC-Easy acc", "#0072B2", "o"),
           ("arc_easy_acc_norm", "ARC-Easy acc_norm", "#56B4E9", "s"),
           ("hellaswag_acc", "HellaSwag acc", "#D55E00", "^"),
           ("hellaswag_acc_norm", "HellaSwag acc_norm", "#E69F00", "D")]

acc = {}
for a in ARMS:
    rs = [r for r in m["main_results"]
          if r["size"] == SCALE and r["method"] == a and finite(r["arc_easy_acc"])]
    acc[a] = {k: st.mean(r[k] for r in rs) for k, _, _, _ in METRICS}
    acc[a]["n"] = len(rs)

plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.7,
                     "xtick.direction": "in", "ytick.direction": "in"})
fig, ax = plt.subplots(figsize=(3.4, 3.1))

ax.axvspan(CHANCE - 1.96 * SE, CHANCE + 1.96 * SE, color="0.90", zorder=0)
ax.axvline(CHANCE, color="0.45", lw=0.9, ls="--", zorder=1)

ys = range(len(ARMS))
for y, a in zip(ys, ARMS):
    ax.axhline(y, color="0.94", lw=0.6, zorder=0)
    for key, _lab, colour, marker in METRICS:
        ax.plot(acc[a][key], y, marker=marker, ms=4, mfc=colour, mec=colour,
                ls="none", zorder=3)

ax.set_yticks(list(ys))
ax.set_yticklabels(ARMS, fontfamily="monospace", fontsize=7)
ax.invert_yaxis()
ax.set_xlabel("log-likelihood accuracy")
ax.set_xlim(0.20, 0.32)
ax.set_xticks([0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32])
ax.tick_params(labelsize=7)
import matplotlib.transforms as mtransforms
_tr = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
ax.text(CHANCE - 0.003, 0.985, "chance", rotation=90, va="top", ha="right",
        transform=_tr, fontsize=6.5, color="0.40")

import matplotlib.patches as mpatches
handles = [plt.Line2D([], [], marker=mk, color=c, ls="none", ms=4, label=lab)
           for _k, lab, c, mk in METRICS]
handles.append(mpatches.Patch(color="0.90",
                              label=r"chance $\pm\,1.96$ SE (300 items)"))
ax.legend(handles=handles, frameon=False, fontsize=6.5, loc="upper left",
          bbox_to_anchor=(-0.16, 1.26), ncol=2, handletextpad=0.3,
          columnspacing=0.9, borderpad=0.0, labelspacing=0.3)
fig.tight_layout(pad=0.4)
F.save(fig, "fig4_lmeval.png")
print("written; n per cell =", {a: acc[a]["n"] for a in ARMS})
lo = min(acc[a][k] for a in ARMS for k, _, _, _ in METRICS)
hi = max(acc[a][k] for a in ARMS for k, _, _, _ in METRICS)
print("accuracy range %.3f..%.3f   chance band %.3f..%.3f"
      % (lo, hi, CHANCE - 1.96 * SE, CHANCE + 1.96 * SE))
