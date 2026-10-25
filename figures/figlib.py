"""Shared loading helpers for the figure scripts.

Everything is read from the released per-run JSON store; nothing is typed in
by hand. Keeping the loaders in one place means every figure reports the same
quantity under the same name.
"""
import json, io, glob, re, math, collections, os
import numpy as np

# Paths are resolved from this file, so the scripts run from anywhere.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs") + os.sep
MANIFEST = os.path.join(ROOT, "results", "tai_manifest.json")
FIGDIR = os.path.join(ROOT, "manuscript", "figures")

# Okabe-Ito, colour-blind safe; one colour per arm, used by every figure.
ARM_COLOUR = {
    "fp16_control": "#000000", "standard": "#666666", "lsuv": "#56B4E9",
    "bitnet158": "#CC79A7", "sparse_sched": "#E69F00",
    "gamma_offset": "#009E73", "tai": "#D55E00", "tai_warmup": "#0072B2",
    "tai_star": "#AA4499",
}
ARM_ORDER = ["fp16_control", "standard", "lsuv", "bitnet158", "sparse_sched",
             "gamma_offset", "tai", "tai_warmup", "tai_star"]

RC = {"font.size": 8, "axes.linewidth": 0.7,
      "xtick.direction": "in", "ytick.direction": "in"}


# Calibration seeds (Section 3.16, S_calib). They live in the run store but are
# disjoint from the reporting seeds by design and are excluded from every
# reported statistic, so they must be excluded from every figure too.
CALIB_SEEDS = {100001, 100002, 100003}


def runs(pattern, drop_calib=True):
    """Every reporting run matching the glob, as a list of parsed records."""
    out = []
    for f in sorted(glob.glob(RUNS + pattern)):
        j = json.load(io.open(f, encoding="utf-8"))
        if drop_calib and j["seed"] in CALIB_SEEDS:
            continue
        out.append(j)
    return out


def by_seed(pattern, field="val_loss"):
    return {j["seed"]: j[field] for j in runs(pattern)}


def by_rho(pattern, field="final_sparsity"):
    """{rho0: {seed: value}} for the sweep-style run names."""
    out = collections.defaultdict(dict)
    for f in sorted(glob.glob(RUNS + pattern)):
        j = json.load(io.open(f, encoding="utf-8"))
        if j["seed"] in CALIB_SEEDS:
            continue
        out[float(re.search(r"__r([0-9.]+)\.json", f).group(1))][j["seed"]] = j[field]
    return dict(out)


def manifest():
    return json.load(io.open(MANIFEST, encoding="utf-8"))


def logN_by_scale():
    m = manifest()
    return {size: ln for ln, _s, _y, size, _t in m["scale_model"]["points"]}


def boot_ci(values, n=5000, seed=0, lo=2.5, hi=97.5):
    """Percentile bootstrap interval of the mean."""
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    bs = rng.choice(v, size=(n, v.size), replace=True).mean(axis=1)
    return float(v.mean()), float(np.percentile(bs, lo)), float(np.percentile(bs, hi))


def save(fig, name):
    os.makedirs(FIGDIR, exist_ok=True)
    fig.savefig(os.path.join(FIGDIR, name), dpi=400)
    print("wrote", os.path.relpath(os.path.join(FIGDIR, name), os.getcwd()))
