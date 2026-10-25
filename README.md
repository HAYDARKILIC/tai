# The Ternary Operating Point

Research artefact for **“The Ternary Operating Point: Threshold Control and Annealing in 1.58-Bit Language Models.”**

Haydar Kilic, Department of Artificial Intelligence Engineering, Ostim Technical University, Ankara, Türkiye — <haydar.kilic@ostimteknik.edu.tr> · [ORCID 0000-0002-2551-3772](https://orcid.org/0000-0002-2551-3772)

---

## What the study found

Under the absmean ternary rule the initial active weight fraction is pinned at **ρ₀ = 0.6899** for every zero-mean initializer, independently of initialization scale. The paper derives the closed-form map between the threshold constant and the operating point it induces, then asks which of two interventions actually controls that operating point once training starts.

The answer is not the one the study was built to confirm:

- A fifty-percentage-point manipulation of initial sparsity leaves **fifty** points at the threshold (retention 1.003–1.006) and **two to four** at the initializer (0.052–0.069). Both produce near-perfect monotone trends, so the ordinal evidence this literature usually reports would have supported a strong causal claim that the retention regression refutes.
- Briefly annealing the threshold early in training lowers held-out loss by **0.060 to 0.201 nats** at **all eleven scales**, and reduces steps-to-target at all eleven.
- The proposed initializer is beaten by its own mechanism-matched control and carries an almost identical penalty in full precision, which is the signature of a generically weaker initializer rather than of failed operating-point control.

All quality claims are token-equal at a fixed 20 M-token budget, at which no run had converged. The paper is explicit about this and about every other structural limitation.

## What is in here

```
manuscript/     the paper: LaTeX source with the bibliography embedded, the
                compiled PDF, ref.bib, the elsarticle class and style, the
                ten figures, highlights, author biography and photograph
figures/        the scripts that generate every figure from the run store
results/        tai_manifest.json (full provenance), tidy per-run and
                per-cell CSVs, the LaTeX table fragments, draft captions
runs/           3,016 per-run JSON records — the source of truth
logs/           mirrored console output, including the H1–H8 verdicts
data/           the lm-eval task definitions and the corpus metadata
code/           TAI_fast.ipynb, the harness that produced the runs
```

Every table and figure in the paper derives from `runs/`. Nothing is hand-entered.

## Reproducing the analysis (no GPU needed)

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd figures && python make_fig1.py                     # and make_fig2.py … make_fig10.py
```

The scripts read `runs/` and `results/tai_manifest.json` and write the PNGs into `manuscript/figures/`. Each one prints the quantities it plotted so they can be checked against the tables in the paper.

Two conventions the scripts enforce, and that any reanalysis must keep:

- **Calibration seeds are excluded.** Seeds `100001–100003` are in the run store but are disjoint from the reporting seeds by design (Section 3.16). `figlib.CALIB_SEEDS` drops them. Including them silently changes the `standard` arm at the four confirmatory scales.
- **Sparsity is read under the live threshold.** Any arm whose mechanism is a threshold shift is mismeasured by an instrument hard-coded to c = 1, and the failure is silent.

## Rebuilding the paper

```bash
cd manuscript && pdflatex manuscript && pdflatex manuscript
```

The bibliography is embedded in `manuscript.tex`, so no BibTeX pass is required. `ref.bib` is shipped for the production editor.

## Reproducing the training runs

`code/TAI_fast.ipynb` is the harness. It expects the tokenized corpus at `data/corpus_gpt2bpe_48000000.npy`, which is **not** in this repository: it is 92 MB and fully regenerable, being the public FineWeb-EDU `sample-10BT` stream tokenized with the public GPT-2 byte-pair encoder to 48 M tokens (`data/corpus_gpt2bpe_48000000.npy.meta.json` records the parameters). The notebook rebuilds it on first run.

The grid was executed on a single NVIDIA A100-SXM4-40GB under Python 3.13.15, PyTorch 2.11.0+cu128 and CUDA 12.8, consuming 50.9 A100-hours in aggregate. It ran in throughput mode, so reruns are **statistically** reproducible, not bit-identical; setting a single flag restores the stronger guarantee. Section 5.10 documents a harness defect in this area — the compiled/eager execution path was not pinned per arm — and quantifies its effect.

Manifest hash: `3e7a849df17d63d7`.

## Citing

See `CITATION.cff`, or cite the paper once it has a DOI.

## Licence

Code (`figures/`, `code/`) is under the MIT Licence; the artefact (`runs/`, `results/`, `logs/`, `data/`, `manuscript/`) is under CC BY 4.0. See `LICENSE` and `LICENSE-DATA`.
