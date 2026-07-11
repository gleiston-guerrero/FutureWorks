# Stakeholders and concerns (ISO/IEC/IEEE 42010:2022)

The Torddis architecture is described following the architecture-description framework of ISO/IEC/IEEE 42010:2022. This document identifies the stakeholders of the system, their concerns, and the architecture views that address each concern.

## Stakeholders

### S1 — Tutor (guardian)

The adult (parent, older sibling, hired care-taker) who is nominally responsible for supervising the child's homework. In a majority of Ecuadorian households represented in the pilot study, the tutor performs domestic and paid work in parallel and cannot dedicate uninterrupted attention to the child. This is the primary customer of the system and the user of the mobile application.

### S2 — Monitored child

A primary-school or lower-secondary student, aged 7 to 12 years, who performs school-assigned homework at home. This actor does not interact directly with the mobile application; nevertheless, the design must protect his/her privacy, avoid causing anxiety, and not disrupt the study routine.

### S3 — Development team

The engineers and researchers who design, build, deploy and maintain the system: two developers (mobile app and IoT firmware), one AI engineer (recognition models), one software architect (back-end + system integration) and one methodologist (evaluation and pedagogical evaluation).

## Concerns

Each concern is a matter of interest that one or more stakeholders have about the system, and that the architecture must address.

| Concern ID | Concern | Held by | Priority |
|-----------|---------|---------|----------|
| C-01 | The system must detect distractions and inform the tutor within a few seconds, even when the tutor is not physically next to the child. | S1 | Critical |
| C-02 | The IoT device must not be perceived as intrusive or threatening by the child; its physical form-factor should resemble an everyday object (e.g. a toy). | S2, S1 | Critical |
| C-03 | Personal data (child's name, photograph, event history) must be protected end-to-end; only the tutor may access them. | S1, S2 | Critical |
| C-04 | The system must operate correctly on modest domestic Wi-Fi networks and be recoverable within seconds from short outages. | S1, S3 | High |
| C-05 | The system components must be maintainable: replacing an AI model, a hardware component or a software module must not require a full redeployment. | S3 | High |
| C-06 | The event history must support later pedagogical analysis by the tutor (statistical graphs over configurable time windows). | S1 | Medium |
| C-07 | The alarms must be salient but not startle-inducing; visual and auditory cues must be coordinated so that the child recognises them as a supportive signal, not as a punishment. | S2, S1 | Medium |

## Views

The architecture is documented through two complementary views. Each view is a representation of a whole system from the perspective of a related set of concerns.

### V1 — Deployment view

The deployment view (Figure 3 of the manuscript, `docs/architecture/02-deployment-view.pdf`) describes the physical distribution of the components across three nodes:

- The **IoT device node** (ESP32-CAM + NodeMCU ESP8266 + buzzer + LED) sits on the child's desk and captures video and short peripheral signals.
- The **back-end node** (Django server + PostgreSQL + AI worker processes) runs on a modest single-board computer (e.g. Raspberry Pi 4 or a home mini-PC) inside the home or on a small cloud instance.
- The **mobile-app node** (Android smartphone) is used by the tutor from anywhere with mobile-data or Wi-Fi coverage.

**Concerns addressed by V1:** C-01, C-02, C-03, C-04.

### V2 — Logical view

The logical view (Figure 5 of the manuscript, `docs/architecture/03-logical-view.pdf`) describes the class structure of the mobile application and the back-end services: authentication, child registration, allowed-object configuration, monitoring, event history and statistical reporting. Every relationship between classes is annotated with cardinality and the AI-model service interfaces are marked as pluggable to support future replacements without redeployment.

**Concerns addressed by V2:** C-05, C-06.

## Correspondence

- Concern C-07 (salient but not startle-inducing alarms) is addressed by a design decision at the firmware level (see `05-rationale.md`, ADR-03) rather than by a view.
- Every requirement in `docs/requirements/` is traced back to one or more concerns; the mapping is maintained in `docs/requirements/traceability-matrix.csv`.

## Model kinds used

- UML 2.5 deployment diagrams for V1.
- UML 2.5 class diagrams for V2.
- Textual architecture decision records (ADRs) for the rationale.
