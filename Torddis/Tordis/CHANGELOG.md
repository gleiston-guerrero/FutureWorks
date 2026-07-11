# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-01-15

First public release accompanying the manuscript submission to
*Education and Information Technologies*.

### Added

- Complete source code of the three system layers:
  - Android mobile application (Java 11, SDK 33+) in `src/mobile-app/`.
  - ESP32-CAM and NodeMCU ESP8266 firmware (C/C++, PlatformIO) in `src/iot-device/`.
  - Django REST back-end (Python 3.11, Django 4.2) in `src/backend/`.
  - AI recognition modules (Python 3.11, OpenCV, TensorFlow, PyTorch) in `src/ai-modules/`.
- Pseudonymised experimental datasets in `data/raw/`:
  - `sus-responses.csv` (12 guardians × 10 SUS items).
  - `likert-effectiveness.csv` (12 guardians × 7 effectiveness Likert items + demographics).
  - `recognition-latencies.csv` (16 sessions × 4 AI modules × latency + success flag).
  - `open-ended-responses.csv` (anonymised free-text responses).
- Derived tables in `data/processed/` matching those reported in the manuscript.
- Data dictionary in `data/data-dictionary.md`.
- Jupyter notebooks in `analysis/` that regenerate every statistical result
  reported in the Results section of the manuscript.
- Requirements specification in `docs/requirements/` following
  ISO/IEC/IEEE 29148:2018, with functional requirements (`FR-01…FR-07`),
  non-functional requirements (`NFR-01…NFR-05` classified per
  ISO/IEC 25010:2023), semi-structured use cases and a full
  traceability matrix.
- Architecture description in `docs/architecture/` following
  ISO/IEC/IEEE 42010:2022, with stakeholders, concerns, deployment view,
  logical view and rationale.
- Testing artefacts in `docs/testing/` following ISO/IEC/IEEE 29119-1:2022:
  test plan, test-design specifications, test-case specifications and
  test-execution reports.
- Standards-compliance checklists in `docs/standards-compliance/` for
  ISO/IEC 25010:2023, ISO/IEC 27001:2022, ISO/IEC/IEEE 29148:2018 and
  ISO/IEC/IEEE 42010:2022.
- Data-collection instruments in `instruments/` (SUS, demographic survey,
  effectiveness Likert questionnaire, open-ended questions).
- Ethics documentation and templates in `ethics/` (informed consent,
  minor assent, data-management plan, privacy-impact assessment).
- Continuous-integration workflows in `.github/workflows/`.
- Dual-licence scheme: MIT for code, CC-BY 4.0 for documentation.
- `CITATION.cff` and `.zenodo.json` for automatic DOI generation on Zenodo.

### Standards followed

- ISO/IEC/IEEE 12207:2017 (software life-cycle processes)
- ISO/IEC/IEEE 15288:2023 (system life-cycle processes)
- ISO/IEC/IEEE 29148:2018 (requirements engineering)
- ISO/IEC 25010:2023 (product quality model)
- ISO/IEC/IEEE 42010:2022 (architecture description)
- ISO/IEC/IEEE 29119-1:2022 (software testing --- general concepts)
- ISO/IEC 27001:2022 (information security management)
- FAIR Data Principles (2016)

[1.0.0]: https://github.com/CarlosAlmeida2000/ProyectoTorddis/releases/tag/v1.0.0
