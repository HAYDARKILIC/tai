"""Regenerate fig8_init_ablation.png (rendered as Figure 7).

The previous version carried a footer reading "~0 in FP16 + positive in
Ternary => benefit is ternary operating-point control", which is the
pre-registered expectation, not the result: the plotted bars were -0.086 and
-0.090, so neither was near zero and neither was positive. It also labelled
those nats values "d=", as if they were Cohen's d, carried the harness's
internal "(#3)" title, and showed no uncertainty. This version plots the two
initialization effects and their difference with paired 95% confidence
intervals, which is what Table 12 reports and what the section argues.
Everything is recomputed from the released per-run records.
"""
import json, io, glob, math, statistics as st
from scipy import stats as sps
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figlib as F
RUNS = F.RUNS


def load(pattern):
    out = {}
    for f in glob.glob(RUNS + pattern):
        j = json.load(io.open(f, encoding="utf-8"))
        out[j["seed"]] = j["val_loss"]
    return out


tai_fp16 = load("fp16abl__dim384__fp16_taiinit__*")
std_fp16 = load("main__dim384__fp16_control__*")
std_tern = load("main__dim384__standard__*")
tai_tern = load("main__dim384__tai__*")
seeds = sorted(tai_fp16)
n = len(seeds)
tcrit = sps.t.ppf(0.975, n - 1)


def ci(d):
    mean = st.mean(d)
    half = tcrit * st.stdev(d) / math.sqrt(n)
    return mean, mean - half, mean + half


eff_fp16 = [std_fp16[s] - tai_fp16[s] for s in seeds]
eff_tern = [std_tern[s] - tai_tern[s] for s in seeds]
diff = [b - a for a, b in zip(eff_fp16, eff_tern)]   # ternary minus full precision

rows = [("Full precision\n(\\texttt{bfloat16})" if False else "Full precision\n(bfloat16)",
         eff_fp16, "#666666"),
        ("Ternary\n(absmean)", eff_tern, "#0072B2"),
        ("Difference\nbetween precisions", diff, "#D55E00")]

plt.rcParams.update({"font.size": 8, "axes.linewidth": 0.7,
                     "xtick.direction": "in", "ytick.direction": "in"})
fig, ax = plt.subplots(figsize=(3.4, 2.3))
ax.axvline(0.0, color="0.25", lw=0.9, zorder=1)

for y, (lab, d, colour) in enumerate(rows):
    mean, lo, hi = ci(d)
    ax.plot(d, [y + 0.20] * n, ".", color=colour, ms=3, alpha=0.45, zorder=2)
    ax.errorbar([mean], [y], xerr=[[mean - lo], [hi - mean]], color=colour,
                marker="o", ms=5, lw=0, elinewidth=1.1, capsize=2.5, zorder=3)
    ax.text(hi + 0.008, y, "%+.4f" % mean, va="center", fontsize=7, color="0.25")

ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows], fontsize=7)
ax.set_ylim(len(rows) - 0.45, -0.55)
ax.set_xlabel(r"$\mathcal{L}$(standard init) $-$ $\mathcal{L}$(TAI init)   [nats]")
ax.set_xlim(-0.165, 0.128)
ax.tick_params(labelsize=7)
ax.grid(True, axis="y", color="0.94", lw=0.6, zorder=0)
ax.annotate("TAI init worse", xy=(-0.160, -0.42), fontsize=6.8, color="0.40")
ax.annotate("TAI init better", xy=(0.012, -0.42), fontsize=6.8, color="0.40")
fig.tight_layout(pad=0.4)
F.save(fig, "fig8_init_ablation.png")

for lab, d, _ in rows:
    mean, lo, hi = ci(d)
    print("%-22s %+.4f  CI [%+.4f, %+.4f]"
          % (lab.replace("\n", " "), mean, lo, hi))
print("paired p: fp16 %.4f | ternary %.4f | difference %.4f  (n=%d)"
      % (sps.ttest_1samp(eff_fp16, 0).pvalue, sps.ttest_1samp(eff_tern, 0).pvalue,
         sps.ttest_1samp(diff, 0).pvalue, n))
