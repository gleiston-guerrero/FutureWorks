# UC-04 — Real-time distraction monitoring

## Identification

| Field | Value |
|-------|-------|
| **Use Case ID** | UC-04 |
| **Title** | Real-time distraction monitoring |
| **Related requirement(s)** | FR-04 (essential) |
| **Primary actor** | IoT device (Torddis camera) |
| **Secondary actors** | Guardian (via mobile app); back-end web service |
| **Priority** | Essential |
| **Frequency** | Continuous during a study session (typically 30–60 min) |
| **Standards** | ISO/IEC/IEEE 29148:2018 clause 9.4 |

## Preconditions

- The IoT device is powered on and connected to the domestic Wi-Fi network.
- The tutor is authenticated in the mobile application (see UC-01).
- At least one child is registered (see UC-02) and the list of allowed objects has been configured (see UC-03).
- The child is seated in the study area within the field-of-view of the ESP32-CAM.

## Main success scenario

1. The tutor starts a monitoring session from the mobile app.
2. The mobile app sends `POST /api/v1/sessions/start` to the back-end.
3. The back-end forwards the session-start instruction to the IoT device via MQTT.
4. Every 500 ms, the ESP32-CAM captures a frame and streams it to the back-end.
5. For each incoming frame the back-end pipeline invokes, in order:
    1. `person-recognition` (LBPH on Haar-Cascade candidates) — identifies the registered child.
    2. `facial-expression` (CNN) — classifies the expression into one of the seven basic emotions.
    3. `drowsiness-detection` (eye-aspect-ratio + CNN validator) — decides whether the child is drowsy.
    4. `object-recognition` (custom YOLO variant) — detects objects in the study area and matches them against the list of allowed objects.
6. If any of steps 5.2–5.4 flags a distraction, the back-end persists the event (timestamp, category, confidence) and pushes a notification to the mobile app.
7. If step 5.3 flags drowsiness OR step 5.1 fails to detect the child for more than 5 s, the back-end also instructs the IoT device (via MQTT) to activate the buzzer and LED (see UC-06).
8. When the tutor stops the session (or a preconfigured timeout elapses), the back-end sends `POST /api/v1/sessions/stop`, the ESP32-CAM stops streaming and the collected events are consolidated into the history log.

## Alternative flows

- **A1 — Child leaves the study area.** After 5 s without a valid person-recognition, the flow branches to step 7 (alarm activation). The mobile app receives an "abandonment" notification.
- **A2 — Wi-Fi disconnection.** The IoT device queues frames in a 20-frame ring buffer for up to 10 s. When connectivity is restored, the queued frames are streamed with an "offline" flag. If disconnection persists beyond 10 s, the IoT device activates the LED alone (no buzzer) to signal degraded operation to the tutor.

## Exception flows

- **E1 — Camera hardware failure.** The ESP32-CAM sets an error flag in its MQTT status topic; the back-end notifies the tutor's app; the session is aborted.
- **E2 — Back-end service unavailable.** The IoT device attempts three reconnections at 2 s intervals; if all fail, it activates the LED and stops streaming; the tutor sees an "offline" state in the app.

## Post-conditions

- All events detected during the session are persisted with their timestamps in the back-end database.
- The child's cumulative distraction counters are updated for use in UC-05 (history) and UC-07 (statistical graphs).
- No raw video frames are stored; only the derived events and their confidence scores.

## Non-functional constraints

- **Time behaviour (NFR-05):** person-recognition latency ≤ 1.5 s (mean); drowsiness-detection latency ≤ 5.0 s (mean).
- **Confidentiality (NFR-04):** frames travel over TLS 1.3; events at rest are encrypted with AES-256.
- **Availability (NFR-03):** the pipeline must resume within 30 s after a mains-power interruption.

## Verification criteria

- **Test case TC-SY-01** (see `docs/testing/test-case-specifications/`) exercises the full pipeline over a 30-minute controlled session with 16 induced events per category. The pass criterion is the aggregated recognition table reported as Table 6 of the manuscript.
