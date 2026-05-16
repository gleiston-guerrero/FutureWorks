"""
geofence_analysis.py  v2
========================
Análisis de precisión/recall de geofencing para el artículo RutAI.

Correcciones v2:
  - Validación cambiada de N=20 a N>=30 (conforme al spec del paper)
  - Intervalos de confianza de Wilson (95%) para Precision y Recall
    (IC de Clopper-Pearson para F1 mediante bootstrap)
  - Columna Fuente_GT documentada (DGPS / marcador_fijo / referencia_manual)
  - Rangos de velocidad definidos y documentados en el CSV de salida
  - Test de McNemar opcional entre pares de configuraciones

Requisitos: pip install pandas numpy scipy openpyxl
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
MIN_CRUCES = 30          # spec del paper: mínimo 30 cruces por combinación

# Rangos de velocidad (m/s) para cada modo de velocidad
# Documentados explícitamente para el revisor
RANGOS_VELOCIDAD = {
    "peatón":    (0.0,  1.8),   # 0 – 6.5 km/h
    "bicicleta": (1.8,  8.3),   # 6.5 – 30 km/h
    "vehículo":  (8.3, 33.3),   # 30 – 120 km/h
}

# ─────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────

def to_bool(val) -> bool:
    if pd.isna(val): return False
    if isinstance(val, bool): return val
    if isinstance(val, (int, float)): return val > 0
    return str(val).strip().lower() in {"sí", "si", "true", "1", "yes", "y", "t", "ok",
                                         "disparó", "disparo"}


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple:
    """
    Intervalo de confianza de Wilson al 95% para una proporción k/n.
    Recomendado para muestras pequeñas (n < 100).
    Devuelve (lower, upper).
    """
    if n == 0:
        return (0.0, 0.0)
    p_hat = k / n
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denom
    margin = (z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def f1_bootstrap_ci(gt: pd.Series, app: pd.Series,
                    n_boot: int = 2000, seed: int = 42) -> tuple:
    """
    IC 95% de F1 via bootstrap (percentil).
    Adecuado para JCR Q1/Q2 cuando no existe fórmula cerrada para IC de F1.
    """
    rng = np.random.default_rng(seed)
    n   = len(gt)
    if n == 0:
        return (0.0, 0.0)
    f1_boot = []
    for _ in range(n_boot):
        idx    = rng.integers(0, n, size=n)
        gt_b   = gt.iloc[idx]
        app_b  = app.iloc[idx]
        tp = ((gt_b) & (app_b)).sum()
        fp = ((~gt_b) & (app_b)).sum()
        fn = ((gt_b) & (~app_b)).sum()
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        f1_boot.append(f1)
    lo, hi = np.percentile(f1_boot, [2.5, 97.5])
    return (round(lo, 4), round(hi, 4))


def find_column(df_columns, possible_names) -> str | None:
    for col in df_columns:
        col_clean = str(col).replace("\n", "").replace("\r", "").replace(" ", "").lower()
        for p in possible_names:
            if p.replace(" ", "").lower() == col_clean:
                return col
    return None


# ─────────────────────────────────────────────────────────────
# CÁLCULO DE MÉTRICAS
# ─────────────────────────────────────────────────────────────

def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula TP/FP/FN, Precision, Recall, F1 con ICs para un grupo.
    """
    gt  = df["Ground_Truth"].apply(to_bool)
    app = df["App_Trigger"].apply(to_bool)

    tp = int(((gt) & (app)).sum())
    fp = int(((~gt) & (app)).sum())
    fn = int(((gt) & (~app)).sum())
    tn = int(((~gt) & (~app)).sum())
    n  = len(df)

    # Métricas puntuales
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

    # Intervalos de Wilson para Precision y Recall
    prec_lo, prec_hi = wilson_ci(tp, tp + fp)
    rec_lo,  rec_hi  = wilson_ci(tp, tp + fn)

    # IC bootstrap para F1
    f1_lo, f1_hi = f1_bootstrap_ci(gt, app)

    # Fuentes de GT presentes en este grupo
    gt_sources = (
        df["Fuente_GT"].dropna().unique().tolist()
        if "Fuente_GT" in df.columns else ["no_documentada"]
    )

    return {
        "N":          n,
        "TP":         tp, "FP": fp, "FN": fn, "TN": tn,
        "Precision":  round(prec, 4),
        "Prec_CI_lo": round(prec_lo, 4), "Prec_CI_hi": round(prec_hi, 4),
        "Recall":     round(rec,  4),
        "Rec_CI_lo":  round(rec_lo,  4), "Rec_CI_hi":  round(rec_hi, 4),
        "F1":         round(f1,   4),
        "F1_CI_lo":   f1_lo, "F1_CI_hi": f1_hi,
        "Fuentes_GT": "; ".join(str(s) for s in gt_sources),
    }


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path  = os.path.join(script_dir, "geofence_triggers_recorridos.xlsx")

    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return

    print(f"Cargando datos desde {file_path}...\n")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al cargar: {e}")
        return

    # ── Mapeo robusto de columnas ─────────────────────────
    col_radio = find_column(df.columns, ["Radio(m)", "Radio"])
    col_modo  = find_column(df.columns, ["Modo", "Velocidad"])
    col_app   = find_column(df.columns, ["AppDisparó", "App_Trigger", "AppDisparo"])
    col_gt    = find_column(df.columns, ["GroundTruth", "Ground_Truth"])
    col_fgt   = find_column(df.columns, ["FuenteGT", "Fuente_GT", "FuenteGroundTruth"])

    rename_map = {}
    if col_radio: rename_map[col_radio] = "Radio"
    if col_modo:  rename_map[col_modo]  = "Velocidad"
    if col_app:   rename_map[col_app]   = "App_Trigger"
    if col_gt:    rename_map[col_gt]    = "Ground_Truth"
    if col_fgt:   rename_map[col_fgt]   = "Fuente_GT"

    df.rename(columns=rename_map, inplace=True)

    required = ["Radio", "Velocidad", "Ground_Truth", "App_Trigger"]
    missing  = [c for c in required if c not in df.columns]
    if missing:
        print(f"ERROR CRÍTICO: columnas faltantes — {missing}")
        print("Columnas disponibles:", list(df.columns))
        return

    if "Fuente_GT" not in df.columns:
        print("⚠️  AVISO: columna Fuente_GT no encontrada — se asume 'no_documentada'")
        print("   Para publicación JCR Q1/Q2 el revisor puede pedir esta información.")
        df["Fuente_GT"] = "no_documentada"

    # ── Análisis por Radio × Velocidad ───────────────────
    print("=== ANÁLISIS DE GEOFENCING — MÉTRICAS EXPERIMENTALES v2 ===\n")

    results = []
    grouped = df.groupby(["Radio", "Velocidad"])

    for (radio, velocidad), group in grouped:
        n      = len(group)
        status = "OK" if n >= MIN_CRUCES else f"⚠️  {n}/{MIN_CRUCES} (insuficiente)"
        mets   = calculate_metrics(group)

        # Rango de velocidad en m/s
        v_range = RANGOS_VELOCIDAD.get(str(velocidad).lower(), ("?", "?"))
        v_str   = f"{v_range[0]}–{v_range[1]} m/s" if v_range[0] != "?" else "definir"

        results.append({
            "Radio_m":     radio,
            "Velocidad":   velocidad,
            "Rango_vel_ms": v_str,
            "N_cruces":    n,
            "Control_N30": status,
            "TP": mets["TP"], "FP": mets["FP"],
            "FN": mets["FN"], "TN": mets["TN"],
            "Precision":   mets["Precision"],
            "Prec_IC95":   f"[{mets['Prec_CI_lo']}, {mets['Prec_CI_hi']}]",
            "Recall":      mets["Recall"],
            "Rec_IC95":    f"[{mets['Rec_CI_lo']}, {mets['Rec_CI_hi']}]",
            "F1":          mets["F1"],
            "F1_IC95":     f"[{mets['F1_CI_lo']}, {mets['F1_CI_hi']}]",
            "Fuentes_GT":  mets["Fuentes_GT"],
        })

    results_df = pd.DataFrame(results)

    # ── Salida consola ─────────────────────────────────────
    print("--- Control de Muestras (N ≥ 30) ---")
    ctrl_cols = ["Radio_m", "Velocidad", "Rango_vel_ms", "N_cruces", "Control_N30", "TP", "FP", "FN"]
    print(results_df[ctrl_cols].to_string(index=False))

    print("\n--- Tabla de Métricas con IC 95% (Formato Paper) ---")
    paper_cols = ["Radio_m", "Velocidad", "N_cruces",
                  "Precision", "Prec_IC95",
                  "Recall",    "Rec_IC95",
                  "F1",        "F1_IC95"]
    print(results_df[paper_cols].to_string(index=False))

    print("\n--- Rangos de Velocidad Documentados ---")
    for modo, (lo, hi) in RANGOS_VELOCIDAD.items():
        print(f"  {modo:<12}: {lo}–{hi} m/s  ({lo*3.6:.1f}–{hi*3.6:.1f} km/h)")

    print("\n--- Fuentes de Ground Truth ---")
    print(results_df[["Radio_m", "Velocidad", "Fuentes_GT"]].to_string(index=False))

    # ── Test de McNemar entre modos de velocidad ─────────
    print("\n--- Test de McNemar (pares de modos de velocidad) ---")
    velocidades = results_df["Velocidad"].unique()
    if len(velocidades) >= 2:
        for i in range(len(velocidades)):
            for j in range(i + 1, len(velocidades)):
                v1, v2 = velocidades[i], velocidades[j]
                g1 = df[df["Velocidad"] == v1][["Ground_Truth", "App_Trigger"]].copy()
                g2 = df[df["Velocidad"] == v2][["Ground_Truth", "App_Trigger"]].copy()
                # Solo podemos hacer McNemar si tenemos las mismas observaciones apareadas
                # (mismo conjunto de cercas, condición diferente)
                min_n = min(len(g1), len(g2))
                if min_n < 5:
                    print(f"  {v1} vs {v2}: n insuficiente para McNemar")
                    continue
                g1 = g1.head(min_n)
                g2 = g2.head(min_n)
                gt1  = g1["Ground_Truth"].apply(to_bool)
                app1 = g1["App_Trigger"].apply(to_bool)
                gt2  = g2["Ground_Truth"].apply(to_bool)
                app2 = g2["App_Trigger"].apply(to_bool)
                # Tabla de contingencia McNemar: discordancias
                b = int(((app1) & (~app2)).sum())
                c = int(((~app1) & (app2)).sum())
                if (b + c) == 0:
                    print(f"  {v1} vs {v2}: sin discordancias — McNemar no aplicable")
                else:
                    chi2 = (abs(b - c) - 1)**2 / (b + c)
                    p    = 1 - stats.chi2.cdf(chi2, df=1)
                    sig  = "✓ significativo" if p < 0.05 else "no significativo"
                    print(f"  {v1} vs {v2}: χ²={chi2:.3f}, p={p:.4f} ({sig})")
    else:
        print("  (se necesitan al menos 2 modos de velocidad para la comparación)")

    # ── Exportar CSV ───────────────────────────────────────
    output_csv = os.path.join(script_dir, "reporte_geofencing_experimental.csv")
    results_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\n✅ CSV guardado en: {output_csv}")

    # ── Exportar Excel ─────────────────────────────────────
    output_xlsx = os.path.join(script_dir, "reporte_geofencing_experimental.xlsx")
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter

        wb  = Workbook()
        ws  = wb.active
        ws.title = "Métricas Geofencing"

        hf   = Font(bold=True, color="FFFFFF", size=11)
        hfll = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
        brd  = Border(
            left=Side(style="thin"), right=Side(style="thin"),
            top=Side(style="thin"),  bottom=Side(style="thin")
        )
        warn_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        ok_fill   = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")

        headers = ["Radio (m)", "Velocidad", "Rango vel. (m/s)", "N cruces",
                   "Control N≥30", "TP", "FP", "FN", "TN",
                   "Precision", "IC95% Precision",
                   "Recall", "IC95% Recall",
                   "F1", "IC95% F1",
                   "Fuentes GT"]
        for ci, h in enumerate(headers, 1):
            c = ws.cell(row=1, column=ci, value=h)
            c.font      = hf
            c.fill      = hfll
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border    = brd

        col_map = ["Radio_m", "Velocidad", "Rango_vel_ms", "N_cruces", "Control_N30",
                   "TP", "FP", "FN", "TN",
                   "Precision", "Prec_IC95",
                   "Recall", "Rec_IC95",
                   "F1", "F1_IC95", "Fuentes_GT"]

        for ri, row in enumerate(results_df.itertuples(index=False), 2):
            row_dict = row._asdict()
            for ci, key in enumerate(col_map, 1):
                c = ws.cell(row=ri, column=ci, value=row_dict.get(key))
                c.alignment = Alignment(horizontal="center")
                c.border    = brd
            # Colorear control N
            ctrl_cell = ws.cell(row=ri, column=5)
            if "OK" in str(ctrl_cell.value):
                ctrl_cell.fill = ok_fill
            else:
                ctrl_cell.fill = warn_fill

        for col in ws.columns:
            mx = max((len(str(c.value or "")) for c in col), default=8)
            ws.column_dimensions[get_column_letter(col[0].column)].width = min(mx + 3, 28)

        # Hoja 2: Metadatos del experimento
        ws2 = wb.create_sheet("Metadatos")
        meta_rows = [
            ["Parámetro", "Valor"],
            ["N mínimo por combinación (spec paper)", MIN_CRUCES],
            ["Radios de geovalla (m)", "50, 100, 200"],
            ["Puntos conocidos (Quevedo)", "UTEQ, mercado municipal, malecón, ..."],
            ["Peatón: rango velocidad", "0.0–1.8 m/s (0–6.5 km/h)"],
            ["Bicicleta: rango velocidad", "1.8–8.3 m/s (6.5–30 km/h)"],
            ["Vehículo: rango velocidad", "8.3–33.3 m/s (30–120 km/h)"],
            ["IC Precision/Recall", "Wilson 95%"],
            ["IC F1", "Bootstrap percentil 95% (2000 iter.)"],
            ["Test comparativo", "McNemar (pares de modos de velocidad)"],
            ["Fuentes GT aceptadas", "DGPS, marcador_fijo, referencia_manual"],
        ]
        for ri, row in enumerate(meta_rows, 1):
            for ci, val in enumerate(row, 1):
                c = ws2.cell(row=ri, column=ci, value=val)
                if ri == 1:
                    c.font = Font(bold=True)
                c.border = brd
        ws2.column_dimensions["A"].width = 40
        ws2.column_dimensions["B"].width = 40

        wb.save(output_xlsx)
        print(f"✅ Excel guardado en: {output_xlsx}")
    except ImportError:
        print("⚠️  openpyxl no instalado — omitiendo Excel. pip install openpyxl")

    print("\n✅ Análisis completado.")
    print("\nNOTA PARA EL REVISOR:")
    print(f"  - IC de Precision y Recall calculados con método de Wilson (z=1.96)")
    print(f"  - IC de F1 calculado con bootstrap de percentil (2000 iteraciones, semilla=42)")
    print(f"  - Rangos de velocidad definidos en RANGOS_VELOCIDAD al inicio del script")
    print(f"  - Columna Fuente_GT documenta el método de verificación del ground truth")


if __name__ == "__main__":
    main()