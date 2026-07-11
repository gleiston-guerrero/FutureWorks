# Architecture rationale — Decision records

This document captures the main architectural decisions of the Torddis system, following the pattern of Architecture Decision Records (ADRs). Each record explains what was decided, the context that motivated it, the alternatives that were considered, and the consequences.

---

## ADR-01 — Distributed three-tier architecture over on-device processing

**Status:** Accepted

**Context.** The IoT device is intentionally constrained (ESP32-CAM with 4 MB flash, 520 KB RAM). Running the four AI recognition modules on-device would exceed both the memory budget and the real-time latency requirement.

**Decision.** The IoT device streams the captured frames to a back-end node (Django + Python AI workers) that performs recognition. Results are relayed back to the device via MQTT for alarm actuation and to the mobile app via HTTPS for user notification.

**Alternatives considered.**
- **On-device inference with TensorFlow Lite Micro.** Rejected: models for facial-expression + object recognition exceed the available flash.
- **All-cloud architecture.** Rejected: introduces mandatory internet connectivity even for local alerting, breaking NFR-03 (mains-powered continuous operation).

**Consequences.**
- (+) Sufficient computing power on the back-end for four concurrent AI modules.
- (+) The back-end can be updated without touching the IoT devices.
- (−) A local back-end node must be reachable; this is mitigated by shipping the back-end as a Docker Compose stack that can run on a Raspberry Pi 4.

---

## ADR-02 — MQTT for device-to-back-end telemetry; HTTPS for mobile-to-back-end

**Status:** Accepted

**Context.** The IoT device emits telemetry at 2 Hz and needs a lightweight, publish-subscribe channel. The mobile application, in contrast, performs request/response operations against the back-end.

**Decision.** MQTT (Mosquitto broker inside the back-end Docker stack) for the IoT ↔ back-end channel; HTTPS + JSON REST for the mobile ↔ back-end channel.

**Alternatives considered.**
- **WebSockets everywhere.** Rejected: an MQTT broker offers finer-grained topic authorisation and QoS levels that fit the sensor use case better.
- **CoAP.** Rejected: less tooling support in Django and the ESP-IDF stack.

**Consequences.**
- (+) Lightweight and battery-friendly for the IoT device (though the device is mains-powered, this reduces buffer requirements during Wi-Fi glitches).
- (+) HTTPS REST is directly consumable by the Android app with standard libraries.

---

## ADR-03 — Alarm salience: LED first, buzzer only after two consecutive events

**Status:** Accepted

**Context.** Concern C-07 (alarms must be salient but not startle-inducing). A one-shot loud buzzer for every event was reported by two guardians during the preliminary interviews as potentially anxiety-inducing.

**Decision.** For every detected distraction the LED blinks amber for 3 s. Only if a second distraction is detected within 60 s of the first does the buzzer emit a single 500-ms tone at 65 dB(A). This escalating pattern communicates severity without startling.

**Alternatives considered.**
- **Always buzzer + LED.** Rejected: too intrusive during focused work.
- **Only LED, never buzzer.** Rejected: fails to catch the child's attention when he/she is not looking at the device.

**Consequences.**
- (+) Preserves the child's concentration flow while still recovering from distractions.
- (−) Slightly delayed intervention in the worst case (60 s).

---

## ADR-04 — Pluggable AI-model service interfaces

**Status:** Accepted

**Context.** Concern C-05 (maintainability) and the anticipated evolution of AI models over time.

**Decision.** Each of the four AI modules (`person-recognition`, `facial-expression`, `drowsiness-detection`, `object-recognition`) is implemented as a Django service class that conforms to a common `RecognitionModule` interface (`recognize(frame) -> RecognitionResult`). The concrete implementation is selected at runtime via a configuration file (`config/ai-modules.yaml`), and models can be swapped without restarting the back-end.

**Alternatives considered.**
- **Hard-coded model imports.** Rejected: incompatible with the maintainability concern.
- **gRPC micro-services per model.** Rejected: adds network overhead that does not pay off inside a single Docker Compose deployment.

**Consequences.**
- (+) A future revision of any model is a configuration change.
- (+) The `docs/standards-compliance/ISO-IEC-25010-2023-checklist.md` maintainability characteristic is materially satisfied.

---

## ADR-05 — Store events only, never raw frames

**Status:** Accepted

**Context.** Concern C-03 (privacy of the child). The system captures video of a minor at home.

**Decision.** No raw frame is ever persisted. The AI pipeline returns only the derived event (timestamp, category, confidence). Frames are held in RAM during processing and discarded immediately afterwards. Only the event log is stored, and it is stored encrypted at rest (AES-256, keyed per tutor).

**Alternatives considered.**
- **Persist frames for a rolling 24 h window.** Rejected: the marginal value for the tutor was rated as low by all interviewed guardians while the privacy risk was rated as very high.

**Consequences.**
- (+) The privacy-impact assessment (`ethics/privacy-impact-assessment.md`) is materially improved.
- (−) It is not possible to reprocess a session with a different model; each session's ground truth is bound to the version of the model deployed at capture time.
