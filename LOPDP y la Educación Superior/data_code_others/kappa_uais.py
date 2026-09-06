# -*- coding: utf-8 -*-
"""
kappa_uais.py — Fiabilidad entre codificadores para los indicadores documentales.

Calcula, por indicador: acuerdo bruto, kappa de Cohen, intervalo de confianza
del 95 % por bootstrap y la lista de discrepancias que hay que reconciliar.
Tambien calcula el kappa global sobre todas las celdas.

USO (Windows, desde la carpeta que contiene los dos CSV):
    python kappa_uais.py

    o bien, indicando rutas:
    python kappa_uais.py doble_codificacion_codificador_A.csv doble_codificacion_codificador_B.csv

REQUISITOS:
    pip install numpy

CODIGOS ADMITIDOS en cada celda de indicador:
    1  presente        (cumple la definicion operativa del Apendice A)
    0  ausente
    P  parcial         (ambito limitado o marco generico)
    NV no verificable  (no se pudo recuperar el sitio o no es legible por maquina)

Para el kappa se sigue la convencion del articulo: P y NV se tratan como 0
(no cumple). El script informa ademas el kappa de tres categorias (1 / P / 0)
para que la eleccion de convencion sea transparente y no quede oculta.
"""

import csv
import sys
import random

try:
    import numpy as np
except ImportError:
    sys.exit("Falta numpy. Instalelo con:  pip install numpy")

INDICADORES = ["aviso", "marco", "derechos", "dpd", "accesibilidad"]
NOMBRES = {
    "aviso": "Aviso de privacidad publicado",
    "marco": "Marco legal citado",
    "derechos": "Derechos enumerados",
    "dpd": "Contacto de privacidad o DPD",
    "accesibilidad": "Declaracion de accesibilidad",
}


def leer(ruta):
    filas = {}
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            filas[int(r["id"])] = r
    return filas


def normaliza(v, binario=True):
    """Devuelve el codigo normalizado, o None si la celda esta vacia."""
    v = (v or "").strip().upper()
    if v == "":
        return None
    if v in ("1", "SI", "SÍ", "S", "Y", "YES", "TRUE"):
        return "1"
    if v in ("0", "NO", "N", "FALSE"):
        return "0"
    if v == "P":
        return "0" if binario else "P"
    if v in ("NV", "N/V", "ND"):
        return "0" if binario else "NV"
    return None


def kappa(a, b):
    """Kappa de Cohen para dos listas de etiquetas de igual longitud."""
    n = len(a)
    if n == 0:
        return float("nan"), float("nan")
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        # Acuerdo perfecto con una sola categoria: kappa indefinido.
        return po, float("nan")
    return po, (po - pe) / (1 - pe)


def bootstrap_ic(a, b, reps=5000, semilla=20260817):
    rnd = random.Random(semilla)
    n = len(a)
    vals = []
    for _ in range(reps):
        idx = [rnd.randrange(n) for _ in range(n)]
        ka = kappa([a[i] for i in idx], [b[i] for i in idx])[1]
        if ka == ka:  # descarta NaN
            vals.append(ka)
    if len(vals) < 100:
        return float("nan"), float("nan")
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def interpreta(k):
    if k != k:
        return "indefinido (una sola categoria)"
    if k < 0.00:
        return "peor que el azar"
    if k < 0.20:
        return "leve"
    if k < 0.40:
        return "aceptable"
    if k < 0.60:
        return "moderado"
    if k < 0.80:
        return "sustancial"
    return "casi perfecto"


def main():
    ra = sys.argv[1] if len(sys.argv) > 1 else "doble_codificacion_codificador_A.csv"
    rb = sys.argv[2] if len(sys.argv) > 2 else "doble_codificacion_codificador_B.csv"
    A, B = leer(ra), leer(rb)

    ids = sorted(set(A) & set(B))
    if not ids:
        sys.exit("Los dos archivos no comparten ningun id. Compruebe que no se altero la columna id.")
    if set(A) != set(B):
        print(f"AVISO: los archivos no cubren los mismos sitios. Se usan los {len(ids)} comunes.\n")

    print("=" * 74)
    print(f"  FIABILIDAD ENTRE CODIFICADORES  —  {len(ids)} sitios en comun")
    print(f"  A: {ra}")
    print(f"  B: {rb}")
    print("=" * 74)
    print()

    incompletas = 0
    todas_a, todas_b, discrepancias = [], [], []

    print(f"{'Indicador':32s} {'n':>4s} {'acuerdo':>8s} {'kappa':>7s} {'IC 95%':>16s}  interpretacion")
    print("-" * 100)

    for ind in INDICADORES:
        a, b, disc = [], [], []
        for i in ids:
            va, vb = normaliza(A[i].get(ind)), normaliza(B[i].get(ind))
            if va is None or vb is None:
                incompletas += 1
                continue
            a.append(va)
            b.append(vb)
            if va != vb:
                disc.append((i, A[i].get("sigla", ""), A[i].get("url", ""), va, vb))
        if not a:
            print(f"{NOMBRES[ind]:32s}  sin celdas completas")
            continue
        po, k = kappa(a, b)
        lo, hi = bootstrap_ic(a, b)
        ic = f"[{lo:.2f}, {hi:.2f}]" if lo == lo else "no calculable"
        print(f"{NOMBRES[ind]:32s} {len(a):4d} {100*po:7.1f}% {k:7.3f} {ic:>16s}  {interpreta(k)}")
        todas_a += a
        todas_b += b
        discrepancias += [(NOMBRES[ind],) + d for d in disc]

    print("-" * 100)
    if todas_a:
        po, k = kappa(todas_a, todas_b)
        lo, hi = bootstrap_ic(todas_a, todas_b)
        ic = f"[{lo:.2f}, {hi:.2f}]" if lo == lo else "no calculable"
        print(f"{'GLOBAL (todas las celdas)':32s} {len(todas_a):4d} {100*po:7.1f}% {k:7.3f} {ic:>16s}  {interpreta(k)}")

    if incompletas:
        print(f"\nAVISO: {incompletas} celdas quedaron vacias en uno de los dos archivos y se excluyeron.")
        print("       Complete la codificacion antes de dar por buenos estos valores.")

    print()
    print("=" * 74)
    print(f"  DISCREPANCIAS A RECONCILIAR: {len(discrepancias)}")
    print("=" * 74)
    if not discrepancias:
        print("  Ninguna. Acuerdo completo.")
    else:
        print(f"{'Indicador':32s} {'id':>4s} {'sigla':14s} {'A':>3s} {'B':>3s}  url")
        for nom, i, sig, url, va, vb in discrepancias:
            print(f"{nom:32s} {i:4d} {sig[:14]:14s} {va:>3s} {vb:>3s}  {url}")
        with open("discrepancias.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.writer(fh)
            w.writerow(["indicador", "id", "sigla", "url", "codigo_A", "codigo_B", "codigo_final", "motivo"])
            for nom, i, sig, url, va, vb in discrepancias:
                w.writerow([nom, i, sig, url, va, vb, "", ""])
        print("\n  Escrito discrepancias.csv: resuelva cada fila y anote el motivo.")
        print("  El codigo final acordado es el que debe entrar en la matriz del articulo.")

    print()
    print("Para el manuscrito, comunique por indicador: n, acuerdo bruto, kappa e IC del 95 %,")
    print("y el numero de discrepancias reconciliadas. Un kappa por debajo de 0,60 en algun")
    print("indicador obliga a revisar su definicion operativa en el Apendice A, no solo a")
    print("reconciliar los casos.")


if __name__ == "__main__":
    main()
