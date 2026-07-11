# ISO/IEC 25010:2023 — Product-quality checklist for Torddis

This document evaluates the Torddis system against the eight product-quality characteristics of ISO/IEC 25010:2023. For each characteristic, the applicable sub-characteristics are listed together with the corresponding evidence in this repository and in the manuscript.

The 2023 edition renames the former "Usability" characteristic as **Interaction Capability** and introduces the new characteristics **Flexibility** and **Safety** with respect to the 2011 edition.

Legend: ✅ addressed, ⚠ partially addressed, ❌ not applicable.

---

## 1. Functional Suitability

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Functional Completeness | All seven functional requirements (FR-01…FR-07) implemented; see traceability matrix. | ✅ |
| Functional Correctness | Recognition results reported in Table 6 of the manuscript; system tests TC-SY-01 and TC-SY-02 pass. | ✅ |
| Functional Appropriateness | Every FR maps to at least one stakeholder concern C-01…C-07. | ✅ |

## 2. Performance Efficiency

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Time Behaviour | NFR-05 measured (mean latency Person Recognition = 0.803 s; Drowsiness Detection = 3.202 s). Reported in Table 7 of the manuscript. | ✅ |
| Resource Utilization | ESP32-CAM operates at ≤ 220 mA; back-end memory footprint ≤ 1.5 GB on Raspberry Pi 4. | ⚠ (measured informally; no ISO/IEC 25023 formal profiling yet) |
| Capacity | The tested configuration supports 1 concurrent monitored child per IoT device; the back-end can serve up to 16 concurrent tutors. | ⚠ |

## 3. Compatibility

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Co-existence | The Django back-end coexists with other services on the same Docker host through container isolation. | ✅ |
| Interoperability | MQTT and REST/JSON standards are used at every interface; the AI modules conform to a common `RecognitionModule` interface (see ADR-04). | ✅ |

## 4. Interaction Capability (formerly Usability)

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Appropriateness Recognisability | Interviews with 12 guardians confirmed that all icons and screens matched their expectations. | ✅ |
| Learnability | New guardians completed the first configuration workflow (FR-01 → FR-03) in ≤ 10 minutes on average. | ✅ |
| Operability | The mobile-app UI follows Material Design guidelines. | ✅ |
| User Error Protection | Confirmation dialogs precede irreversible actions (delete child, revoke session). | ✅ |
| User Engagement | NFR-02 measured (mean rating = 4.42/5 on the non-intrusiveness Likert item). | ✅ |
| Inclusivity | Font-size, contrast and colour choices are WCAG-AA compliant; language selector supports ES and EN. | ✅ |
| User Assistance | In-app help pane and this reproducibility package's `docs/user-manual/`. | ✅ |
| Self-Descriptiveness | Every screen has a title bar and contextual help. | ✅ |

## 5. Reliability

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Faultlessness | System tests observed 0 fatal failures over 30 hours of accumulated operation. | ⚠ (limited evaluation window) |
| Availability | NFR-03: the IoT device recovers within 30 s from a mains-power outage. | ✅ |
| Fault Tolerance | Ring buffer (20 frames) tolerates Wi-Fi glitches of up to 10 s. | ✅ |
| Recoverability | Session state is persisted every 60 s; on restart, the session resumes from the last checkpoint. | ✅ |

## 6. Security

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Confidentiality | NFR-04: TLS 1.3 in transit, AES-256 at rest; see `docs/standards-compliance/ISO-IEC-27001-2022-controls.md`. | ✅ |
| Integrity | HMAC-SHA256 signature on every MQTT payload; JWT with RS256 for the mobile-app session. | ✅ |
| Non-Repudiation | Every event carries an immutable timestamp and a signature from the emitting IoT device. | ✅ |
| Accountability | The back-end audit log records every authenticated action with the tutor's identity. | ✅ |
| Authenticity | Devices are provisioned with a per-device certificate signed by the deployment CA. | ✅ |
| Resistance | Rate-limiting on the REST API; MQTT topics are authorised per device certificate. | ⚠ (no external penetration test yet) |

## 7. Maintainability

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Modularity | Django apps and Android modules follow the single-responsibility principle. | ✅ |
| Reusability | AI-model service classes conform to a common interface (see ADR-04). | ✅ |
| Analysability | Structured logging (JSON) throughout the back-end; Android app uses Timber. | ✅ |
| Modifiability | ADR-04 confirms that any AI model can be swapped without redeployment. | ✅ |
| Testability | Test-plan and test-case specifications in `docs/testing/`. | ✅ |

## 8. Flexibility (new in 2023)

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Adaptability | The mobile app runs on any Android SDK 33+ device; the back-end runs on any x86-64 or ARMv8 host with Docker. | ✅ |
| Scalability | The back-end supports horizontal scaling of AI workers (Django + Celery). | ⚠ (design; not yet load-tested at scale) |
| Installability | `docker compose up -d` installs and starts the whole back-end. | ✅ |
| Replaceability | The mobile app can be replaced by any REST client that implements the API contract in `docs/architecture/api-contract.md`. | ✅ |

## 9. Safety (new in 2023)

| Sub-characteristic | Evidence | Status |
|--------------------|----------|--------|
| Operational Constraint | The IoT device operates only within the physical envelope of the child's study area. | ✅ |
| Risk Identification | See `ethics/privacy-impact-assessment.md`. | ✅ |
| Fail Safe | On any AI-worker failure the system enters an "observation only" mode with no alarms. | ✅ |
| Hazard Warning | The LED signals degraded connectivity to the tutor and the child. | ✅ |
| Safe Integration | The IoT device uses low-voltage USB-C power supply; no exposed high-voltage components. | ✅ |

---

## Summary

Of the 40 applicable sub-characteristics of ISO/IEC 25010:2023, Torddis fully addresses **33** and partially addresses **7** (with the partial ones being either due to limited-scope pilot studies or design decisions that would require additional load/security testing to be formally certified).
