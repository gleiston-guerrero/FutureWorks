# Test plan (ISO/IEC/IEEE 29119-1:2022)

## 1. Introduction

This document is the master test plan for the Torddis system, prepared in accordance with the general concepts of ISO/IEC/IEEE 29119-1:2022. It covers the four test levels applied during the development life-cycle: unit, integration, system and acceptance.

## 2. Scope

- **In scope:** the mobile application, the ESP32-CAM and NodeMCU ESP8266 firmware, the Django back-end, the four AI recognition modules, and their integration.
- **Out of scope:** third-party libraries, the domestic Wi-Fi network, the Android operating system, and the users' smartphones themselves.

## 3. Test items

| Test item | Version | Owner |
|-----------|---------|-------|
| `src/mobile-app/` | v1.0.0 | Mobile-app team |
| `src/iot-device/esp32-cam/` | v1.0.0 | Firmware team |
| `src/iot-device/esp8266-nodemcu/` | v1.0.0 | Firmware team |
| `src/backend/` | v1.0.0 | Back-end team |
| `src/ai-modules/` | v1.0.0 | AI team |

## 4. Test levels and approaches

### 4.1 Unit tests

- **Owner:** each module owner.
- **Approach:** each function or class is tested with mocked dependencies.
- **Tooling:** JUnit + Espresso (Android); pytest (Python); Unity + Ceedling (C).
- **Pass criterion:** ≥ 80 % branch coverage; 0 failing tests.

### 4.2 Integration tests

- **Owner:** software architect.
- **Approach:** interactions between components (mobile ↔ back-end via REST; IoT ↔ back-end via MQTT; back-end ↔ database).
- **Pass criterion:** 0 failing tests; every REST endpoint documented in `docs/architecture/api-contract.md` is exercised.

### 4.3 System tests

- **Owner:** methodologist.
- **Approach:** end-to-end scenarios in an ideal test environment; measurement of the four AI-module latencies over 16 sessions (Table 6 of the manuscript).
- **Pass criterion:** mean latency below the NFR-05 thresholds (person < 1.5 s; drowsiness < 5 s).

### 4.4 Acceptance tests

- **Owner:** end-user (guardian) with the methodologist as observer.
- **Approach:** five acceptance test cases exercising the main happy paths (see `test-case-specifications/`).
- **Pass criterion:** the guardian confirms that each test case matches his/her expectations.

## 5. Test environment

### 5.1 Ideal environment (used for system tests)

- Well-lit study area (400 lux ambient).
- 5.0 GHz Wi-Fi with < 20 ms RTT to the back-end.
- ESP32-CAM at 40 cm from the child, at eye level.

### 5.2 Real-world environment (used for acceptance tests)

- The guardian's home, with whatever illumination and Wi-Fi are usually available.
- The IoT device is placed as the guardian sees fit.

## 6. Roles and responsibilities

| Role | Responsibility |
|------|-----------------|
| Test manager | Owns the test plan; coordinates with each team owner. |
| Module owner | Writes the unit tests; participates in integration tests. |
| Methodologist | Designs, runs and reports the system tests. |
| Guardian | Runs the acceptance tests. |

## 7. Deliverables

- Test-design specifications (`test-design-specifications/`).
- Test-case specifications (`test-case-specifications/`).
- Test-execution reports (`test-execution-reports/`).
- Latency data in `../../data/raw/recognition-latencies.csv`.

## 8. Exit criteria

- All planned test cases executed.
- 0 open blocker or critical defects.
- Acceptance test signed off by the guardian and the methodologist.

## 9. Risks and contingencies

| Risk | Mitigation |
|------|-------------|
| Wi-Fi unreliable at a participant's home | Use mobile-data hotspot as back-up. |
| Child refuses to participate | Reschedule; the guardian's assent is revocable at any time. |
| AI-model false positives on darker-skinned children (bias risk) | Explicitly include diverse participants in the pilot; document any bias observed in the results. |
