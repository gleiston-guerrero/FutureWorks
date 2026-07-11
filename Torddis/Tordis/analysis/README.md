# `analysis/` — Statistical analysis notebooks

This directory contains the Jupyter notebooks that regenerate every statistical result reported in the Results section of the manuscript. All notebooks are self-contained: each notebook loads its input dataset from `../data/raw/` or `../data/processed/` and writes its derived tables and figures to `../data/processed/` and to inline outputs.

## Environment

Two equivalent ways to install the environment are provided:

### Conda (recommended)

```bash
conda env create -f environment.yml
conda activate torddis
```

### pip

```bash
python3.11 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

The exact package versions are pinned in both files to guarantee bit-identical outputs across platforms.

## Notebooks

| Notebook | Purpose | Reproduces |
|----------|---------|------------|
| `01-normality-tests.ipynb` | Shapiro–Wilk and Kolmogorov–Smirnov normality tests for every numeric variable | Table 10 |
| `02-pearson-correlation.ipynb` | Pearson correlation of Statement (5) with the other variables; Pearson correlation matrix of recognition latencies | Tables 8, 11 |
| `03-anova-analysis.ipynb` | One-way ANOVA of each variable against Statement (5) | Table 12 |
| `04-post-hoc-tests.ipynb` | Tukey HSD post-hoc for the significant ANOVA results | Tables 13–16 |
| `05-spearman-correlation.ipynb` | Spearman rank-order correlation for the non-parametric variables | Table 17 (Spearman columns) |
| `06-kruskal-wallis.ipynb` | Kruskal–Wallis H-test for the categorical variables against Statement (5) | Table 17 (KW columns) |
| `07-sus-score-computation.ipynb` | SUS score computation with reverse-scoring, 0–100 scaling and Bangor et al. (2008) qualitative interpretation | Figure 8 (bar chart with error bars) |

## How to run all notebooks

To regenerate every table and figure in one pass:

```bash
jupyter execute analysis/*.ipynb
```

Or interactively:

```bash
jupyter lab
```

and then open each notebook in order.

## Provenance

Every processed CSV in `../data/processed/` starts with a `# provenance` comment line that identifies the notebook and cell that produced it. This makes it possible to trace each numeric value in the manuscript back to a specific cell of a specific notebook.

## Reproducibility guarantees

- All random seeds are pinned to `42`.
- All numeric libraries are pinned to specific versions (see `environment.yml`).
- Notebooks are stored with metadata stripped so that `git diff` is stable.
