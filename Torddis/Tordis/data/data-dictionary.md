# Data dictionary

This document describes every dataset shared in the `data/` directory. All datasets are pseudonymised: no personal identifier is present. The pseudonymisation protocol is documented in `../ethics/data-management-plan.md`.

Every table below lists the column name, its data type, its unit or coding, and a short description.

---

## `raw/sus-responses.csv`

Responses of the 12 guardians to the ten-item System Usability Scale (SUS) questionnaire, administered after a 30-minute pilot session with Torddis.

| Column | Type | Coding | Description |
|--------|------|--------|-------------|
| `participant_id` | string | G01…G12 | Pseudonymous guardian identifier. |
| `sus_1` | int | 1–5 | I think I would like to use this system frequently. |
| `sus_2` | int | 1–5 | I found the system unnecessarily complex. (reverse-scored) |
| `sus_3` | int | 1–5 | I thought the system was easy to use. |
| `sus_4` | int | 1–5 | I think I would need the support of a technical person to be able to use this system. (reverse-scored) |
| `sus_5` | int | 1–5 | I found the various functions in this system were well integrated. |
| `sus_6` | int | 1–5 | I thought there was too much inconsistency in this system. (reverse-scored) |
| `sus_7` | int | 1–5 | I would imagine that most people would learn to use this system very quickly. |
| `sus_8` | int | 1–5 | I found the system very cumbersome to use. (reverse-scored) |
| `sus_9` | int | 1–5 | I felt very confident using the system. |
| `sus_10` | int | 1–5 | I needed to learn a lot of things before I could get going with this system. (reverse-scored) |

Likert scale: 1 = strongly disagree, 5 = strongly agree.

---

## `raw/likert-effectiveness.csv`

Demographic data and answers to the seven-item Likert effectiveness questionnaire (Statements 1–7), collected from the same 12 guardians after the pilot session.

| Column | Type | Coding | Description |
|--------|------|--------|-------------|
| `participant_id` | string | G01…G12 | Pseudonymous guardian identifier. |
| `tutor_age` | int | 25–65 (bucketed to 5-year ranges) | Age of the guardian. |
| `tutor_gender` | int | 1 = female, 2 = male, 3 = other | Gender of the guardian. |
| `tutor_education` | int | 1 = primary, 2 = secondary, 3 = tertiary | Highest completed education level. |
| `residence_area` | int | 1 = urban, 2 = rural | Area of residence. |
| `occupation` | int | 1 = paid work, 2 = unpaid domestic, 3 = student, 4 = retired | Guardian's main occupation. |
| `internet_type` | int | 1 = fibre, 2 = ADSL, 3 = mobile, 4 = mixed | Domestic internet connection. |
| `supervision_time` | float | hours per day | Average daily time devoted by the guardian to supervising the child's schoolwork. |
| `student_age` | int | 7–12 | Age of the monitored child. |
| `statement_1` | int | 1–5 | The device was perceived by the student as appealing. |
| `statement_2` | int | 1–5 | The mobile application accurately recorded the events that occurred. |
| `statement_3` | int | 1–5 | The student did not perceive the presence of the device as intrusive. |
| `statement_4` | int | 1–5 | The device was used throughout the effective time devoted to school tasks. |
| `statement_5` | int | 1–5 | After discontinuing use of the device, the student demonstrated improvement in self-regulation and concentration while completing homework. |
| `statement_6` | int | 1–5 | Although the device usage time was short, it is expected to significantly contribute to task completion and academic performance. |
| `statement_7` | int | 1–5 | You would be willing to continue using the device. |

Likert scale: 1 = strongly disagree, 5 = strongly agree.

---

## `raw/recognition-latencies.csv`

Latency measurements collected by the IoT device during the 16 controlled sessions reported in Table 6 of the manuscript. Latencies are wall-clock times from frame capture to event emission.

| Column | Type | Coding | Description |
|--------|------|--------|-------------|
| `session_id` | int | 1–16 | Session sequence number. |
| `person_latency_s` | float | seconds | Person-recognition latency (0.00 if the module failed to recognise the child). |
| `person_success` | int | 0 = fail, 1 = success | Whether person recognition succeeded. |
| `facial_latency_s` | float | seconds | Facial-expression recognition latency (0.00 on failure). |
| `facial_success` | int | 0/1 | Facial-expression success flag. |
| `drowsiness_latency_s` | float | seconds | Drowsiness-detection latency (0.00 on failure). |
| `drowsiness_success` | int | 0/1 | Drowsiness-detection success flag. |
| `object_latency_s` | float | seconds | Object-recognition latency (0.00 on failure). |
| `object_success` | int | 0/1 | Object-recognition success flag. |

---

## `raw/open-ended-responses.csv`

Anonymised free-text responses to the eight open-ended questions attached to the SUS questionnaire. Any potentially identifying detail (proper name, geographical reference finer than the district level, place of work, name of school) was manually redacted and replaced with a bracketed token such as `[NAME]`, `[PLACE]`, `[SCHOOL]`. The redaction protocol is described in `../ethics/data-management-plan.md`.

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Pseudonymous guardian identifier. |
| `question_number` | int | 1–8. |
| `question_text` | string | The open-ended question as it appeared on the questionnaire (see `../instruments/open-ended-questions-ES.md`). |
| `response_text` | string | The guardian's free-text response, after redaction. |

---

## `processed/*.csv`

The processed datasets are derived from the raw datasets by the notebooks in `../analysis/`. Every processed file starts with a comment row (`#`) that references the notebook and cell that produced it, so full provenance can be traced.
