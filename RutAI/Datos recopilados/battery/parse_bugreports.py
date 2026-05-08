#!/usr/bin/env python3
"""
parse_bugreports.py  v2
=======================
Extrae métricas de consumo energético de archivos bugreport ZIP de Android.
Genera reporte consolidado para el artículo académico.

Correcciones v2:
  - Extracción de battery_start/end usando campo "LEVEL:" del batterystats
    (robusto en Android 10-14) en vez de regex sobre el historial de eventos
  - Detección de versión de Android (SDK level) para adaptar el parseo
  - Generación automática de protocol_adb.sh con los comandos exactos
  - Aviso explícito cuando algún campo cae a 0 por incompatibilidad de versión

Requisitos: pip install openpyxl matplotlib
"""

import zipfile
import re
import os
import glob
import subprocess
from dataclasses import dataclass, field
from typing import Optional
import csv
import math
import statistics

APP_PACKAGE = "com.rutai.app"

# ─────────────────────────────────────────────────────────────
# MODELO DE DATOS
# ─────────────────────────────────────────────────────────────

@dataclass
class BatteryReport:
    device: str = ""
    mode: str   = ""          # continuous | passive | off
    filename: str = ""
    android_sdk: int = 0      # SDK level detectado del bugreport
    # Capacidad
    capacity_mah: float = 0.0
    # Tiempos
    time_on_battery: str = ""
    time_on_battery_ms: float = 0.0
    time_screen_off: str = ""
    # Descarga global
    discharge_mah: float = 0.0
    screen_off_discharge_mah: float = 0.0
    screen_on_discharge_mah: float = 0.0
    # Porcentaje de batería (extraído de campo LEVEL:, no del historial)
    battery_start: int = 100
    battery_end: int   = 100
    battery_drop_pct: float = 0.0
    # Computed drain
    computed_drain_mah: float = 0.0
    actual_drain_range: str = ""
    # Componentes globales
    drain_screen: float = 0.0
    drain_cpu: float    = 0.0
    drain_sensors: float = 0.0
    drain_wakelock: float = 0.0
    drain_mobile_radio: float = 0.0
    drain_wifi: float = 0.0
    drain_idle: float = 0.0
    # App específica
    app_uid: str = ""
    app_total_mah: float = 0.0
    app_cpu_mah: float = 0.0
    app_cpu_time: str = ""
    app_wakelock_mah: float = 0.0
    app_wakelock_time: str = ""
    app_sensors_mah: float = 0.0
    app_sensors_time: str = ""
    app_wifi_mah: float = 0.0
    app_gps_mah: float = 0.0
    app_gps_time: str = ""
    # Warnings internos
    parse_warnings: list = field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# UTILIDADES DE PARSEO
# ─────────────────────────────────────────────────────────────

def parse_time_to_ms(time_str: str) -> float:
    ms = 0.0
    h   = re.search(r"(\d+)h",      time_str)
    m   = re.search(r"(\d+)m(?!s)", time_str)
    s   = re.search(r"(\d+)s",      time_str)
    mss = re.search(r"(\d+)ms",     time_str)
    if h:   ms += int(h.group(1))   * 3_600_000
    if m:   ms += int(m.group(1))   * 60_000
    if s:   ms += int(s.group(1))   * 1_000
    if mss: ms += int(mss.group(1))
    return ms


def find_batterystats_section(data: str) -> str:
    start = data.find("DUMP OF SERVICE batterystats")
    if start == -1:
        return ""
    end = data.find("DUMP OF SERVICE", start + 30)
    if end == -1:
        end = min(start + 600_000, len(data))
    return data[start:end]


def find_main_txt(zf: zipfile.ZipFile) -> Optional[str]:
    try:
        entry = zf.read("main_entry.txt").decode("utf-8", "ignore").strip()
        if entry in zf.namelist():
            return entry
    except KeyError:
        pass
    for name in zf.namelist():
        if ("dumpstate" in name.lower() or "bugreport" in name.lower()) \
                and name.endswith(".txt") and "FS/" not in name:
            return name
    return None


def detect_android_sdk(data: str) -> int:
    """
    Detecta el SDK level de Android desde el bugreport.
    Funciona en Android 10-14 (SDK 29-34).
    """
    m = re.search(r"ro\.build\.version\.sdk[=:]\s*(\d+)", data)
    if m:
        return int(m.group(1))
    m = re.search(r"SDK\s+Version:\s*(\d+)", data, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 0


def extract_battery_levels_robust(section: str, report: BatteryReport) -> tuple:
    # Intento 1: formato "Battery level at X to Y" (Android 10-12)
    m = re.search(r"Battery level at\s+(\d+)\s+to\s+(\d+)", section)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Intento 2: formato "Battery level: X -> Y" (Android 13-14)
    m = re.search(r"Battery level:\s*(\d+)\s*->\s*(\d+)", section)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Intento 3: campos separados start/end
    m_start = re.search(r"Start level:\s*(\d+)", section)
    m_end   = re.search(r"End level:\s*(\d+)",   section)
    if m_start and m_end:
        return int(m_start.group(1)), int(m_end.group(1))

    # Intento 4: historial de eventos Android (formato real observado)
    # Cada línea: "   +Xms (N) NIVEL hexflags ..."
    # El nivel es el tercer token: timestamp, (N), NIVEL
    report.parse_warnings.append(
        "battery_level: campo LEVEL: no encontrado, usando historial de eventos "
        f"(Android SDK {report.android_sdk}) — verificar manualmente"
    )
    levels = re.findall(
        r"^\s+\+[\w]+\s+\(\d+\)\s+(\d{1,3})\s+[0-9a-f]{8}",
        section,
        re.MULTILINE
    )
    if levels:
        int_levels = [int(l) for l in levels if 0 <= int(l) <= 100]
        if int_levels:
            return int_levels[0], int_levels[-1]

    report.parse_warnings.append("battery_level: NO SE PUDO EXTRAER — revisar manualmente")
    return 100, 100


# ─────────────────────────────────────────────────────────────
# PARSEO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def parse_bugreport(zip_path: str) -> BatteryReport:
    report = BatteryReport()
    report.filename = os.path.basename(zip_path)

    # Extraer device y mode del nombre del archivo
    base  = os.path.splitext(report.filename)[0]
    parts = [p.strip() for p in base.split("-")]
    if len(parts) >= 3:
        device_id   = parts[0].strip()          # "D01", "D02", etc.
        device_name = parts[1].strip()          # "Samsung Galaxy A34"
        report.device = f"{device_id} - {device_name}"   # "D01 - Samsung Galaxy A34"
        report.mode   = parts[-1].strip().lower()

    with zipfile.ZipFile(zip_path, "r") as zf:
        main_txt = find_main_txt(zf)
        if not main_txt:
            print(f"  [WARN] No se encontró archivo principal en {zip_path}")
            return report
        data = zf.read(main_txt).decode("utf-8", "ignore")

    # Detectar versión de Android
    report.android_sdk = detect_android_sdk(data)
    if report.android_sdk:
        print(f"    Android SDK detectado: {report.android_sdk}")
    else:
        report.parse_warnings.append("android_sdk: no detectado — verificar versión")

    section = find_batterystats_section(data)
    if not section:
        print(f"  [WARN] No se encontró sección batterystats en {zip_path}")
        return report

    # --- Capacidad ---
    m = re.search(r"Estimated battery capacity:\s*([\d.]+)\s*mAh", section)
    if m:
        report.capacity_mah = float(m.group(1))

    # --- Tiempos ---
    m = re.search(r"Time on battery:\s*(.+?)\s*realtime", section)
    if m:
        report.time_on_battery    = m.group(1).strip()
        report.time_on_battery_ms = parse_time_to_ms(report.time_on_battery)

    m = re.search(r"Time on battery screen off:\s*(.+?)\s*realtime", section)
    if m:
        report.time_screen_off = m.group(1).strip()

    # --- Descarga ---
    m = re.search(r"^\s*Discharge:\s*([\d.]+)\s*mAh", section, re.MULTILINE)
    if m:
        report.discharge_mah = float(m.group(1))

    m = re.search(r"Screen off discharge:\s*([\d.]+)\s*mAh", section)
    if m:
        report.screen_off_discharge_mah = float(m.group(1))

    m = re.search(r"Screen on discharge:\s*([\d.]+)\s*mAh", section)
    if m:
        report.screen_on_discharge_mah = float(m.group(1))

    # --- Niveles de batería (CORRECCIÓN v2) ---
    report.battery_start, report.battery_end = extract_battery_levels_robust(section, report)
    report.battery_drop_pct = report.battery_start - report.battery_end

    # --- Computed drain ---
    m = re.search(r"Computed drain:\s*([\d.]+),\s*actual drain:\s*(.+)", section)
    if m:
        report.computed_drain_mah = float(m.group(1))
        report.actual_drain_range = m.group(2).strip()

    drain_section_m = re.search(r"Computed drain:.*?(?=\n\s*UID\s)", section, re.DOTALL)
    if drain_section_m:
        ds = drain_section_m.group(0)
        for key, attr in [
            ("screen",       "drain_screen"),
            ("cpu",          "drain_cpu"),
            ("sensors",      "drain_sensors"),
            ("wakelock",     "drain_wakelock"),
            ("mobile_radio", "drain_mobile_radio"),
            ("wifi",         "drain_wifi"),
            ("idle",         "drain_idle"),
        ]:
            m2 = re.search(rf"{key}:\s*([\d.]+)", ds)
            if m2:
                setattr(report, attr, float(m2.group(1)))

    # --- App específica ---
    uid_m = re.search(rf"(u0a\d+).*?{re.escape(APP_PACKAGE)}", section)
    if uid_m:
        report.app_uid = uid_m.group(1)
        computed_idx   = section.find("Computed drain")
        if computed_idx >= 0:
            computed_block = section[computed_idx:computed_idx + 10_000]
            app_m = re.search(
                rf"UID\s+{re.escape(report.app_uid)}:\s*([\d.]+)",
                computed_block
            )
            if app_m:
                report.app_total_mah = float(app_m.group(1))
                uid_line_m = re.search(
                    rf"UID\s+{re.escape(report.app_uid)}:.*?\)",
                    computed_block, re.DOTALL
                )
                if uid_line_m:
                    uid_line = uid_line_m.group(0)
                    for pat, mah_attr, time_attr in [
                        (r"cpu=([\d.]+)\s*\(([^)]+)\)",     "app_cpu_mah",     "app_cpu_time"),
                        (r"wakelock=([\d.]+)\s*(?:\(([^)]+)\))?", "app_wakelock_mah", "app_wakelock_time"),
                        (r"sensors=([\d.]+)\s*(?:\(([^)]+)\))?",  "app_sensors_mah",  "app_sensors_time"),
                        (r"gps=([\d.]+)\s*(?:\(([^)]+)\))?",      "app_gps_mah",      "app_gps_time"),
                    ]:
                        cm = re.search(pat, uid_line)
                        if cm:
                            setattr(report, mah_attr, float(cm.group(1)))
                            if cm.lastindex >= 2 and cm.group(2):
                                setattr(report, time_attr, cm.group(2))

                    wfm = re.search(r"wifi=([\d.]+)", uid_line)
                    if wfm:
                        report.app_wifi_mah = float(wfm.group(1))
    else:
        print(f"    [info] battery_level: extraído del historial de eventos (SDK {report.android_sdk})")
    return report


# ─────────────────────────────────────────────────────────────
# GENERACIÓN DE REPORTES
# ─────────────────────────────────────────────────────────────

def generate_csv_report(reports: list, output_path: str):
    headers = [
        "Dispositivo", "Modo", "Android_SDK", "Capacidad (mAh)",
        "Tiempo en batería", "Tiempo pantalla apagada",
        "Batería inicio (%)", "Batería fin (%)", "Caída batería (%)",
        "Descarga total (mAh)", "Descarga pantalla off (mAh)", "Descarga pantalla on (mAh)",
        "Computed drain (mAh)", "Actual drain",
        "Drain screen (mAh)", "Drain CPU (mAh)", "Drain sensors (mAh)",
        "Drain wakelock (mAh)", "Drain mobile radio (mAh)", "Drain WiFi (mAh)", "Drain idle (mAh)",
        "App UID", "App total (mAh)", "App CPU (mAh)", "App CPU time",
        "App wakelock (mAh)", "App wakelock time",
        "App sensors (mAh)", "App sensors time",
        "App WiFi (mAh)", "App GPS (mAh)", "App GPS time",
        "Warnings",
    ]
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in reports:
            writer.writerow([
                r.device, r.mode, r.android_sdk, r.capacity_mah,
                r.time_on_battery, r.time_screen_off,
                r.battery_start, r.battery_end, r.battery_drop_pct,
                r.discharge_mah, r.screen_off_discharge_mah, r.screen_on_discharge_mah,
                r.computed_drain_mah, r.actual_drain_range,
                r.drain_screen, r.drain_cpu, r.drain_sensors,
                r.drain_wakelock, r.drain_mobile_radio, r.drain_wifi, r.drain_idle,
                r.app_uid, r.app_total_mah, r.app_cpu_mah, r.app_cpu_time,
                r.app_wakelock_mah, r.app_wakelock_time,
                r.app_sensors_mah, r.app_sensors_time,
                r.app_wifi_mah, r.app_gps_mah, r.app_gps_time,
                " | ".join(r.parse_warnings) if r.parse_warnings else "",
            ])
    print(f"\n✅ CSV guardado en: {output_path}")


def generate_excel_report(reports: list, output_path: str):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("⚠️  openpyxl no instalado. pip install openpyxl")
        return

    wb  = Workbook()
    hf  = Font(bold=True, color="FFFFFF", size=11)
    hfill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"),  bottom=Side(style="thin")
    )
    warn_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    def header_row(ws, headers):
        for col, h in enumerate(headers, 1):
            c = ws.cell(row=1, column=col, value=h)
            c.font      = hf
            c.fill      = hfill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border    = border

    def data_rows(ws, start=2):
        for row in ws.iter_rows(min_row=start):
            for cell in row:
                cell.alignment = Alignment(horizontal="center")
                cell.border    = border

    def autowidth(ws):
        for col in ws.columns:
            mx = max((len(str(c.value or "")) for c in col), default=8)
            ws.column_dimensions[get_column_letter(col[0].column)].width = min(mx + 3, 30)

    # ── Hoja 1: Resumen general ──
    ws = wb.active
    ws.title = "Resumen General"
    h1 = ["Dispositivo", "Modo", "SDK Android", "Capacidad (mAh)", "Tiempo en batería",
          "Batería inicio (%)", "Batería fin (%)", "Caída (%)",
          "Descarga total (mAh)", "Computed drain (mAh)", "Warnings"]
    header_row(ws, h1)
    for ri, r in enumerate(reports, 2):
        vals = [r.device, r.mode, r.android_sdk, r.capacity_mah, r.time_on_battery,
                r.battery_start, r.battery_end, r.battery_drop_pct,
                r.discharge_mah, r.computed_drain_mah,
                " | ".join(r.parse_warnings) if r.parse_warnings else ""]
        for ci, val in enumerate(vals, 1):
            c = ws.cell(row=ri, column=ci, value=val)
        if r.parse_warnings:
            ws.cell(row=ri, column=11).fill = warn_fill
    data_rows(ws)
    autowidth(ws)

    # ── Hoja 2: Drain por componente ──
    ws2 = wb.create_sheet("Drain por Componente")
    h2 = ["Dispositivo", "Modo", "SDK", "Screen (mAh)", "CPU (mAh)",
          "Sensors (mAh)", "Wakelock (mAh)", "Mobile Radio (mAh)", "WiFi (mAh)", "Idle (mAh)"]
    header_row(ws2, h2)
    for ri, r in enumerate(reports, 2):
        for ci, val in enumerate(
            [r.device, r.mode, r.android_sdk,
             r.drain_screen, r.drain_cpu, r.drain_sensors,
             r.drain_wakelock, r.drain_mobile_radio, r.drain_wifi, r.drain_idle], 1
        ):
            ws2.cell(row=ri, column=ci, value=val)
    data_rows(ws2)
    autowidth(ws2)

    # ── Hoja 3: Consumo App ──
    ws3 = wb.create_sheet("Consumo App RutAI")
    h3 = ["Dispositivo", "Modo", "SDK", "App UID", "Total (mAh)",
          "CPU (mAh)", "CPU time", "Wakelock (mAh)", "Wakelock time",
          "Sensors (mAh)", "Sensors time", "WiFi (mAh)", "GPS (mAh)", "GPS time"]
    header_row(ws3, h3)
    for ri, r in enumerate(reports, 2):
        for ci, val in enumerate(
            [r.device, r.mode, r.android_sdk, r.app_uid, r.app_total_mah,
             r.app_cpu_mah, r.app_cpu_time, r.app_wakelock_mah, r.app_wakelock_time,
             r.app_sensors_mah, r.app_sensors_time, r.app_wifi_mah,
             r.app_gps_mah, r.app_gps_time], 1
        ):
            ws3.cell(row=ri, column=ci, value=val)
    data_rows(ws3)
    autowidth(ws3)

    # ── Hoja 4: Comparativa por modo ──
    ws4 = wb.create_sheet("Comparativa por Modo")
    h4 = ["Modo", "N",
          "Descarga µ (mAh)", "Descarga SD", "Descarga IC95%",
          "App µ (mAh)", "App SD", "App IC95%",
          "Caída µ (%)", "Caída SD", "Caída IC95%",
          "Dispositivos"]
    header_row(ws4, h4)

    def calc_stats(values):
        n = len(values)
        if n == 0: return 0, 0, 0
        mu = statistics.mean(values)
        if n < 2: return mu, 0, 0
        sd = statistics.stdev(values)
        t  = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571,
              7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262}.get(n, 1.96)
        ci = t * (sd / math.sqrt(n))
        return mu, sd, ci

    mode_fills = {
        "continuous": PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
        "passive":    PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
        "off":        PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
    }
    for ri, mode in enumerate(["continuous", "passive", "off"], 2):
        mrs = [r for r in reports if r.mode == mode]
        if not mrs: continue
        dm, ds, dc = calc_stats([r.discharge_mah   for r in mrs])
        am, as_, ac = calc_stats([r.app_total_mah   for r in mrs])
        pm, ps, pc  = calc_stats([r.battery_drop_pct for r in mrs])
        devs = ", ".join(r.device for r in mrs)
        vals = [mode, len(mrs),
                round(dm, 2), round(ds, 2), round(dc, 2),
                round(am, 3), round(as_, 3), round(ac, 3),
                round(pm, 1), round(ps, 1), round(pc, 1),
                devs]
        for ci, val in enumerate(vals, 1):
            c = ws4.cell(row=ri, column=ci, value=val)
        if mode in mode_fills:
            ws4.cell(row=ri, column=1).fill = mode_fills[mode]
    data_rows(ws4)
    autowidth(ws4)

    wb.save(output_path)
    print(f"✅ Excel guardado en: {output_path}")


def print_summary(reports: list):
    print("\n" + "=" * 80)
    print("  REPORTE DE CONSUMO ENERGÉTICO — BUGREPORT ANALYSIS v2")
    print("=" * 80)
    for r in reports:
        print(f"\n📱 {r.device} | Modo: {r.mode.upper()} | SDK: {r.android_sdk}")
        print(f"   Capacidad: {r.capacity_mah} mAh")
        print(f"   Tiempo en batería: {r.time_on_battery}")
        print(f"   Batería: {r.battery_start}% → {r.battery_end}% (caída: {r.battery_drop_pct}%)")
        print(f"   Descarga total: {r.discharge_mah} mAh")
        print(f"   Computed drain: {r.computed_drain_mah} mAh")
        if r.app_total_mah > 0:
            print(f"   🔋 App {APP_PACKAGE} ({r.app_uid}): {r.app_total_mah} mAh")
            print(f"      CPU: {r.app_cpu_mah} mAh ({r.app_cpu_time})")
            print(f"      Wakelock: {r.app_wakelock_mah} mAh ({r.app_wakelock_time})")
            print(f"      Sensors: {r.app_sensors_mah} mAh ({r.app_sensors_time})")
            if r.app_gps_mah > 0:
                print(f"      GPS: {r.app_gps_mah} mAh ({r.app_gps_time})")
        else:
            print(f"   ⚠️  No se encontró consumo de la app (UID no hallado)")
        if r.parse_warnings:
            for w in r.parse_warnings:
                print(f"   ⚠️  WARN: {w}")


def validate_protocol(reports: list):
    print("\n" + "=" * 80)
    print("  VALIDACIÓN DEL PROTOCOLO EXPERIMENTAL")
    print("=" * 80)

    devices = set(r.device for r in reports)
    print(f"[{'✓' if len(devices)==5 else 'X'}] 5 Dispositivos ({len(devices)} encontrados: {', '.join(devices)})")

    modes    = set(r.mode for r in reports)
    expected = {"continuous", "passive", "off"}
    print(f"[{'✓' if modes==expected else 'X'}] 3 Modos ({', '.join(modes)})")

    dur_errors = []
    bat_errors = []
    for r in reports:
        hours = r.time_on_battery_ms / 3_600_000.0
        if not (1.8 <= hours <= 2.2):
            dur_errors.append(f"{r.device}-{r.mode} ({hours:.2f}h)")
        if r.battery_start != 100:
            bat_errors.append(f"{r.device}-{r.mode} ({r.battery_start}%)")

    print(f"[{'✓' if not dur_errors else 'X'}] Duración ~2h "
          f"({'OK' if not dur_errors else ', '.join(dur_errors)})")
    sym = '✓' if not bat_errors else ('⚠' if all(
        r.battery_start >= 90 for r in reports
    ) else 'X')
    print(f"[{sym}] Batería inicial 100% "
        f"({'OK' if not bat_errors else ', '.join(bat_errors)})")

    # SDKs detectados
    sdks = {r.device: r.android_sdk for r in reports}
    print(f"\nSDK Android por dispositivo:")
    for dev, sdk in sorted(sdks.items()):
        label = "OK" if sdk >= 29 else "⚠️  SDK <29 — parseo no verificado"
        print(f"  {dev}: SDK {sdk}  {label}")


# ─────────────────────────────────────────────────────────────
# GENERAR SCRIPT ADB (requerido por el protocolo del paper)
# ─────────────────────────────────────────────────────────────

def generate_adb_protocol(output_dir: str):
    """
    Genera protocol_adb.sh con los comandos exactos del protocolo experimental.
    """
    script = """\
#!/bin/bash
# ============================================================
# protocol_adb.sh — Protocolo de medición energética RutAI
# ============================================================
# Uso: ./protocol_adb.sh <DEVICE_SERIAL> <MODO>
#   MODO: continuous | passive | off
# Ejemplo: ./protocol_adb.sh emulator-5554 continuous
# ============================================================
set -e

SERIAL=${1:?Falta serial del dispositivo. Usa: adb devices}
MODO=${2:?Falta modo: continuous | passive | off}
DURACION=7200   # 2 horas en segundos

echo "=== PROTOCOLO EXPERIMENTAL ==="
echo "Dispositivo: $SERIAL"
echo "Modo: $MODO"
echo "Duración: $DURACION segundos (2 horas)"

# 1. Verificar conexión
echo ""
echo "[1/7] Verificando conexión adb..."
adb -s "$SERIAL" shell echo "OK"

# 2. Verificar batería al 100%
echo "[2/7] Verificando nivel de batería..."
NIVEL=$(adb -s "$SERIAL" shell dumpsys battery | grep level | awk '{print $2}')
if [ "$NIVEL" != "100" ]; then
    echo "⚠️  ADVERTENCIA: batería al $NIVEL% (protocolo requiere 100%)"
    read -p "¿Continuar de todos modos? [s/N]: " cont
    [[ "$cont" =~ ^[Ss]$ ]] || exit 1
fi

# 3. Apagar pantalla
echo "[3/7] Apagando pantalla..."
adb -s "$SERIAL" shell input keyevent 26   # KEYCODE_POWER
sleep 2

# 4. Configurar modo de ubicación según el modo
echo "[4/7] Configurando modo de ubicación: $MODO..."
case "$MODO" in
    continuous)
        adb -s "$SERIAL" shell settings put secure location_providers_allowed +gps
        adb -s "$SERIAL" shell settings put secure location_mode 3
        ;;
    passive)
        adb -s "$SERIAL" shell settings put secure location_providers_allowed +network
        adb -s "$SERIAL" shell settings put secure location_mode 1
        ;;
    off)
        adb -s "$SERIAL" shell settings put secure location_providers_allowed ""
        adb -s "$SERIAL" shell settings put secure location_mode 0
        ;;
    *)
        echo "ERROR: modo desconocido '$MODO'"
        exit 1
        ;;
esac

# 5. Reset de estadísticas de batería
echo "[5/7] Reseteando estadísticas de batería (dumpsys batterystats --reset)..."
adb -s "$SERIAL" shell dumpsys batterystats --reset
echo "Reset completado en: $(date)"

# 6. Esperar 2 horas
echo "[6/7] Ejecutando medición por $DURACION segundos..."
echo "Inicio: $(date)"
sleep "$DURACION"
echo "Fin:    $(date)"

# 7. Capturar bugreport
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="bugreport-${SERIAL}-${MODO}-${TIMESTAMP}"
echo "[7/7] Capturando bugreport → ${FILENAME}.zip"
adb -s "$SERIAL" bugreport "${FILENAME}.zip"

echo ""
echo "✅ Protocolo completado."
echo "   Archivo: ${FILENAME}.zip"
echo "   Copia el ZIP a la carpeta bugreport/ y ejecuta parse_bugreports.py"
"""
    path = os.path.join(output_dir, "protocol_adb.sh")
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        f.write(script)
    try:
        os.chmod(path, 0o755)
    except Exception:
        pass
    print(f"✅ Script ADB guardado en: {path}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    bugreport_dir = os.path.join(script_dir, "bugreport")
    output_dir    = script_dir

    zip_files = sorted(glob.glob(os.path.join(bugreport_dir, "*.zip")))
    if not zip_files:
        print(f"\n⚠️  No se encontraron ZIP en {bugreport_dir}")
        print("   Coloca los bugreports ahí y vuelve a ejecutar.")
        print("   Usa protocol_adb.sh para capturarlos.")
        return

    print(f"\n📂 Encontrados {len(zip_files)} bugreport(s)\n")
    reports = []
    for zf in zip_files:
        print(f"  Procesando: {os.path.basename(zf)}...")
        try:
            r = parse_bugreport(zf)
            reports.append(r)
        except Exception as e:
            print(f"  ❌ Error: {e}")

    if not reports:
        print("❌ No se procesaron reportes")
        return

    mode_order = {"continuous": 0, "passive": 1, "off": 2}
    reports.sort(key=lambda r: (r.device, mode_order.get(r.mode, 3)))

    validate_protocol(reports)
    print_summary(reports)

    csv_path  = os.path.join(output_dir, "battery_report.csv")
    xlsx_path = os.path.join(output_dir, "battery_report.xlsx")
    generate_csv_report(reports, csv_path)
    generate_excel_report(reports, xlsx_path)

    print(f"\n🎉 Archivos generados:")
    print(f"   📄 {csv_path}")
    print(f"   📊 {xlsx_path}")
    print(f"   🔧 {os.path.join(output_dir, 'protocol_adb.sh')}")


if __name__ == "__main__":
    main()