# `src/` — Source code

This directory hosts the complete source code of the three system layers. The code is a curated snapshot of the existing project at <https://github.com/CarlosAlmeida2000/ProyectoTorddis>, reorganised for clarity and augmented with build and test infrastructure.

## Structure

```
src/
├── mobile-app/                    ← renamed from AppMovilTorddis
│   ├── app/                       (Android modules)
│   ├── build.gradle
│   ├── settings.gradle
│   └── README.md                  ← how to build the APK
├── iot-device/
│   ├── esp32-cam/                 ← renamed from CameraTorddis (ESP32-CAM part)
│   │   ├── src/main.cpp
│   │   ├── platformio.ini
│   │   └── README.md              ← how to flash the ESP32-CAM
│   └── esp8266-nodemcu/           ← renamed from CameraTorddis (NodeMCU part)
│       ├── src/main.cpp
│       ├── platformio.ini
│       └── README.md              ← how to flash the NodeMCU
├── backend/                       ← renamed from WebServicesTorddis
│   ├── torddis/                   (Django project)
│   ├── requirements.txt
│   ├── docker-compose.yml
│   └── README.md                  ← how to start the back-end
└── ai-modules/                    ← extracted from backend/
    ├── person-recognition/        (Haar Cascade + LBPH)
    ├── facial-expression/         (CNN)
    ├── drowsiness-detection/      (EAR + CNN validator)
    ├── object-recognition/        (custom YOLO variant)
    ├── models/                    (pre-trained weights)
    ├── requirements.txt
    └── README.md
```

## Migration notes

The existing repository at <https://github.com/CarlosAlmeida2000/ProyectoTorddis> has the following top-level folders that must be moved into this `src/` directory before the release:

| Existing folder | Moves to |
|-----------------|----------|
| `AppMovilTorddis/` | `src/mobile-app/` |
| `CameraTorddis/`   | Split between `src/iot-device/esp32-cam/` and `src/iot-device/esp8266-nodemcu/` |
| `WebServicesTorddis/` | `src/backend/` |
| `Evaluación/`      | `../evaluation/` at repository root (not in `src/`) |

## Licence

All code in this directory is released under the **MIT** licence; see `../LICENSE-CODE`.
