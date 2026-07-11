# Contributing to the Torddis reproducibility package

Thank you for your interest in contributing! This document explains how to report an issue, propose an improvement, or send a pull request.

## Code of conduct

By participating in this project you agree to abide by the terms of the [Contributor Covenant, v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Report any incident to the corresponding authors listed in the root `README.md`.

## Types of contributions welcomed

- **Bug reports**: open an issue with a minimal reproducer, the observed behaviour, and the expected behaviour.
- **Documentation improvements**: pull requests to `docs/`, the `README.md`, `CHANGELOG.md` or the licence texts.
- **Additional analysis notebooks**: send new notebooks that add value on top of the existing ones (e.g. an alternative test, a robustness check).
- **Reproducibility fixes**: fixes to pinned versions, notebooks that no longer execute cleanly, etc.
- **Translations of instruments** to languages other than Spanish and English.

## What is **not** in scope for this repository

- Changes to the paper's scientific claims. Those must be handled through the journal's peer-review or a formal correction/erratum.
- Additions of data that would need a fresh IRB approval.
- Merges of features from unrelated Torddis forks not authored by the study team.

## How to propose a change

1. Open an issue first, unless the change is trivial (typo, dead link).
2. Fork the repository and create a branch: `git checkout -b feature/my-change`.
3. Make your change. Follow the coding style used in the affected directory (PEP 8 for Python, Google Java Style for Android, `clang-format` with LLVM defaults for firmware).
4. If your change affects the analysis, add or update a test in the corresponding notebook or module.
5. Update `CHANGELOG.md` under `[Unreleased]`.
6. Open a pull request with a descriptive title and a summary that references the issue.

## Reviewers

Pull requests are reviewed by at least one of the corresponding authors. Expect a response within two weeks.

## Licences

By contributing to this repository you agree that your contributions will be licensed under the same terms as the rest of the repository:

- MIT for source code (`src/`, `analysis/`, `.github/`, and every code file).
- CC-BY 4.0 for documentation and data (`docs/`, `data/`, `instruments/`, `ethics/`).

## Contact

- General issues: <https://github.com/CarlosAlmeida2000/ProyectoTorddis/issues>
- Sensitive matters (privacy, ethics): please write directly to the corresponding authors listed in the root `README.md`.
