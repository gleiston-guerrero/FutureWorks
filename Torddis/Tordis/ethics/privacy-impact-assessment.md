# Privacy Impact Assessment (PIA) — Torddis

This Privacy Impact Assessment identifies the risks that the Torddis system poses to the privacy of the monitored children and their guardians, and documents the mitigation measures adopted at design time. The assessment follows the general framework of ISO/IEC 27001:2022 (Annex A) and of the applicable data-protection regulations.

## 1. Identification of data subjects

- **Primary data subjects:** the monitored children (aged 7–12), whose image is captured for real-time processing.
- **Secondary data subjects:** the guardians (tutors), whose authentication data, contact data and questionnaire responses are processed.

## 2. Identified risks

| ID | Risk | Likelihood | Impact | Overall |
|----|------|-----------|--------|---------|
| R-01 | Unauthorised access to raw video frames | Low (frames never leave RAM) | High (image of a minor) | Medium |
| R-02 | Re-identification of a guardian from questionnaire responses | Low | Medium | Low |
| R-03 | Re-identification of a guardian from an open-ended response | Medium | Medium | Medium |
| R-04 | Interception of TLS traffic | Low | Medium | Low |
| R-05 | Loss of the pseudonymisation key file | Medium | High | Medium |
| R-06 | Unauthorised access to the Django database at rest | Low | High | Medium |
| R-07 | Insider misuse by an authorised researcher | Low | High | Medium |
| R-08 | Child startled or made anxious by the alarm system | Medium | Low | Low |

## 3. Mitigations adopted

### R-01 — Unauthorised access to raw video frames

- Frames are held in RAM only, for the duration of the inference (< 500 ms), and immediately discarded.
- No frame ever reaches persistent storage.
- The ESP32-CAM MQTT topic is authorised per device certificate.

### R-02 and R-03 — Re-identification

- Guardian names are replaced by pseudonymous identifiers before deposit.
- Ages are bucketed to 5-year ranges.
- Open-ended responses are manually redacted to remove proper names, place names, school names, workplace names, phone numbers, e-mails and postal addresses (see `data-management-plan.md`).
- Two researchers independently review each redaction.

### R-04 — Interception of TLS traffic

- TLS 1.3 with modern cipher suites only.
- Certificate pinning in the Android application.
- HSTS enabled in the Django back-end.

### R-05 — Loss of the pseudonymisation key file

- Kept on paper only, in a locked cabinet at the host institution.
- Two authorised researchers only.
- Destroyed one year after publication of the manuscript.

### R-06 — Unauthorised access to the Django database at rest

- AES-256 full-disk encryption on the server.
- Per-tutor field-level encryption for sensitive columns (contact e-mail).
- PostgreSQL role-based access control.

### R-07 — Insider misuse

- Named access list; every access is audited.
- Data access is logged with the researcher's identity and reason.
- Ethics training required annually.

### R-08 — Child anxiety

- Alarm salience is escalating (LED first, buzzer only after two consecutive events; see ADR-03).
- Auditory alarm is 500 ms at 65 dB(A), designed as a soft chime rather than a shrill tone.
- Pre-session explanation to the child (see `minor-assent-template-ES.md`).
- Session can be interrupted at any moment by the guardian or the child.

## 4. Residual risks

After the mitigations, the residual risk profile is:

| ID | Residual likelihood | Residual impact | Residual overall |
|----|--------------------|-----------------|------------------|
| R-01 | Very low | Low (only in-RAM) | **Very low** |
| R-02 | Very low | Low | **Very low** |
| R-03 | Low | Low | **Low** |
| R-04 | Very low | Low | **Very low** |
| R-05 | Very low | Medium | **Low** |
| R-06 | Very low | Medium | **Low** |
| R-07 | Very low | Medium | **Low** |
| R-08 | Very low | Very low | **Very low** |

## 5. Review

This PIA is to be reviewed:

- Whenever a new type of data is captured (currently: no plan to add).
- Whenever a change to the AI pipeline could increase the residual risk (e.g. persisting frames).
- Annually if the system is in production use beyond the pilot.
