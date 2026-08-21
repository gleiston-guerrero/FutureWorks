#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fiabilidad intercodificadores para la doble codificacion del 30 % de la muestra.

Uso:
    python kappa_uais.py codificador_A.csv codificador_B.csv

Formato esperado de cada CSV (mismas filas, mismo orden, cabecera obligatoria):
    id,grupo,notice,framework,rights,dpo,accessibility
    1,benchmark,1,1,1,1,1
    2,benchmark,1,0,1,1,1
    ...
Valores admitidos por indicador: 1 (presente), 0 (ausente), P (parcial), NV
(no verificable). P y NV se recodifican a 0 antes del calculo, que es la misma
convencion aplicada en el analisis principal del articulo (Seccion 5.5); el
script informa ademas del kappa calculado sobre las tres categorias 1/0/NV
para que se vea si la convencion altera la conclusion.

Salida: kappa de Cohen por indicador con intervalo de confianza del 95 % por
bootstrap, porcentaje de acuerdo bruto, y la lista de celdas discrepantes que
hay que reconciliar antes de fijar la matriz definitiva.

Sin dependencias mas alla de la biblioteca estandar.
"""
import csv
import random
import sys
from collections import Counter

INDICADORES = ["notice", "framework", "rights", "dpo", "accessibility"]
BOOTSTRAP = 5000
SEMILLA = 20260814


def leer(ruta):
    with open(ruta, newline="", encoding="utf-8-sig") as fh:
        filas = list(csv.DictReader(fh))
    if not filas:
        sys.exit("El archivo %s esta vacio." % ruta)
    faltan = [c for c in ["id"] + INDICADORES if c not in filas[0]]
    if faltan:
        sys.exit("Faltan columnas en %s: %s" % (ruta, ", ".join(faltan)))
    return filas


def binario(v):
    """Convencion del articulo: parcial y no verificable cuentan como ausencia."""
    v = (v or "").strip().upper()
    return 1 if v in ("1", "SI", "YES", "TRUE") else 0


def tres(v):
    v = (v or "").strip().upper()
    if v in ("1", "SI", "YES", "TRUE"):
        return "1"
    if v in ("NV", "N/V", "NA"):
        return "NV"
    return "0"


def kappa(a, b):
    """Kappa de Cohen para dos listas de etiquetas de igual longitud."""
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(1 for x, y in zip(a, b) if x == y) / float(n)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[k] / float(n)) * (cb[k] / float(n)) for k in set(ca) | set(cb))
    if pe == 1.0:
        return float("nan")
    return (po - pe) / (1.0 - pe)


def ic_bootstrap(a, b, reps=BOOTSTRAP):
    rnd = random.Random(SEMILLA)
    n = len(a)
    muestras = []
    for _ in range(reps):
        idx = [rnd.randrange(n) for _ in range(n)]
        k = kappa([a[i] for i in idx], [b[i] for i in idx])
        if k == k:                      # descarta NaN
            muestras.append(k)
    if len(muestras) < reps * 0.5:
        return (float("nan"), float("nan"))
    muestras.sort()
    lo = muestras[int(0.025 * len(muestras))]
    hi = muestras[int(0.975 * len(muestras)) - 1]
    return (lo, hi)


def interpretar(k):
    if k != k:
        return "no estimable"
    if k < 0.40:
        return "pobre"
    if k < 0.60:
        return "moderado"
    if k < 0.80:
        return "sustancial"
    return "casi perfecto"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    A, B = leer(sys.argv[1]), leer(sys.argv[2])
    if len(A) != len(B):
        sys.exit("Los dos archivos tienen distinto numero de filas: %d y %d."
                 % (len(A), len(B)))
    ids_a = [f["id"] for f in A]
    ids_b = [f["id"] for f in B]
    if ids_a != ids_b:
        sys.exit("Los identificadores no coinciden fila a fila.")

    print("Sitios doblemente codificados: %d" % len(A))
    print("")
    print("%-16s %7s %7s %7s %18s  %s"
          % ("Indicador", "acuerdo", "kappa", "k(3cat)", "IC 95 % boot", "lectura"))
    print("-" * 78)

    discrepancias = []
    for ind in INDICADORES:
        a2 = [binario(f[ind]) for f in A]
        b2 = [binario(f[ind]) for f in B]
        a3 = [tres(f[ind]) for f in A]
        b3 = [tres(f[ind]) for f in B]
        acuerdo = sum(1 for x, y in zip(a2, b2) if x == y) / float(len(a2))
        k2 = kappa(a2, b2)
        k3 = kappa(a3, b3)
        lo, hi = ic_bootstrap(a2, b2)
        print("%-16s %6.1f%% %7.3f %7.3f  [%6.3f, %6.3f]  %s"
              % (ind, 100 * acuerdo, k2, k3, lo, hi, interpretar(k2)))
        for fa, fb in zip(A, B):
            if tres(fa[ind]) != tres(fb[ind]):
                discrepancias.append((fa["id"], ind, fa[ind], fb[ind]))

    total_celdas = len(A) * len(INDICADORES)
    print("-" * 78)
    print("Celdas comparadas: %d | discrepantes: %d (%.1f %%)"
          % (total_celdas, len(discrepancias),
             100.0 * len(discrepancias) / total_celdas))

    if discrepancias:
        print("")
        print("Celdas a reconciliar (id, indicador, codificador A, codificador B):")
        for d in discrepancias:
            print("  %-6s %-14s A=%-4s B=%-4s" % d)
    else:
        print("")
        print("Sin discrepancias: no hay nada que reconciliar.")


if __name__ == "__main__":
    main()
