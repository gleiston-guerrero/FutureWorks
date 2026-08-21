#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANALISIS DE LA AUDITORIA MULTIPUNTO
===================================

Lee todos los archivos resultados_<PUNTO>_r<PASADA>.json que encuentre en la
carpeta y produce:

  1. Un control de calidad por pasada (sitios cargados, fallos, ubicacion).
  2. Un analisis de ESTABILIDAD entre pasadas del mismo punto de observacion:
     responde a la critica de "una sola pasada" del informe de evaluacion.
  3. El consolidado por sitio y punto de observacion (regla de mayoria sobre
     las k pasadas).
  4. La prueba de McNEMAR exacta para cada par de puntos de observacion, que es
     la prueba correcta cuando se mide EL MISMO sitio en dos condiciones.
  5. La Q de COCHRAN para los tres puntos a la vez.
  6. La razon de momios para datos pareados (b/c) con intervalo de confianza.

Uso:
    python analizar_multipunto.py
    python analizar_multipunto.py --carpeta datos --salida analisis.txt

Requiere: pip install scipy numpy
"""

import argparse
import glob
import json
import math
import os
import sys
from collections import defaultdict

try:
    from scipy import stats
except ImportError:
    sys.exit("Falta scipy. Ejecute:  pip install scipy numpy")

# Indicadores binarios que se extraen de cada registro.
# Cada uno es una funcion que recibe el registro y devuelve True, False o None.
def _rastreo(r):
    c = r.get("cookies")
    return None if not c else (c.get("rastreo_pre", 0) > 0)

def _alguna_cookie(r):
    c = r.get("cookies")
    return None if not c else (c.get("total_pre", 0) > 0)

def _banner(r):
    c = r.get("cookies")
    return None if not c else bool(c.get("banner"))

def _cmp(r):
    c = r.get("cookies")
    return None if not c else (len(c.get("cmp", [])) > 0)

def _nivel_a(r):
    a = r.get("accesibilidad")
    return None if not a else (a.get("porNivel", {}).get("A", 0) == 0)

INDICADORES = {
    "rastreo_antes_del_consentimiento": _rastreo,
    "alguna_cookie_antes_del_consentimiento": _alguna_cookie,
    "banner_visible": _banner,
    "cmp_detectada": _cmp,
    "sin_fallo_de_nivel_A": _nivel_a,
}

ORDEN_PUNTOS = ["EC", "EU", "US"]


# ---------------------------------------------------------------- utilidades
def wilson(k, n, z=1.959963985):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * max(0.0, c - h), 100 * min(1.0, c + h)


def mcnemar_exacto(b, c):
    """Prueba de McNemar exacta (binomial) sobre los pares discordantes."""
    n = b + c
    if n == 0:
        return 1.0
    return float(stats.binomtest(b, n, 0.5, alternative="two-sided").pvalue)


def or_pareada(b, c):
    """Razon de momios para datos pareados = b/c, con IC 95 % (metodo de Wald
    sobre log(b/c) con correccion de continuidad si hay un cero)."""
    if b == 0 and c == 0:
        return None
    bb, cc = (b + 0.5, c + 0.5) if (b == 0 or c == 0) else (b, c)
    orr = bb / cc
    se = math.sqrt(1 / bb + 1 / cc)
    return orr, orr * math.exp(-1.96 * se), orr * math.exp(1.96 * se)


def cochran_q(tabla):
    """Q de Cochran para k condiciones medidas sobre los mismos sujetos.
    tabla: lista de listas, una por sujeto, con 0/1 por condicion."""
    n = len(tabla)
    if n == 0:
        return float("nan"), float("nan"), 0
    k = len(tabla[0])
    Cj = [sum(fila[j] for fila in tabla) for j in range(k)]
    Ri = [sum(fila) for fila in tabla]
    N = sum(Ri)
    num = (k - 1) * (k * sum(c * c for c in Cj) - N * N)
    den = k * N - sum(r * r for r in Ri)
    if den == 0:
        return float("nan"), 1.0, n
    Q = num / den
    p = 1 - stats.chi2.cdf(Q, k - 1)
    return Q, p, n


# ------------------------------------------------------------------- lectura
def cargar(carpeta):
    """Devuelve datos[punto][pasada][id_sitio] = registro, y la lista de metas."""
    datos = defaultdict(lambda: defaultdict(dict))
    metas = []
    patron = os.path.join(carpeta, "resultados_*_r*.json")
    archivos = sorted(glob.glob(patron))
    if not archivos:
        sys.exit(f"No se encontro ningun archivo que coincida con {patron}")
    for ruta in archivos:
        base = os.path.basename(ruta)
        cuerpo = base[len("resultados_"):-len(".json")]
        punto, _, pasada = cuerpo.partition("_r")
        with open(ruta, encoding="utf-8") as fh:
            for r in json.load(fh):
                datos[punto][int(pasada)][r["id"]] = r
        meta_ruta = os.path.join(carpeta, f"meta_{cuerpo}.json")
        if os.path.exists(meta_ruta):
            with open(meta_ruta, encoding="utf-8") as fh:
                metas.append(json.load(fh))
    return datos, metas, archivos


def consolidar(datos, punto, indicador):
    """Regla de mayoria sobre las pasadas. Devuelve dict id -> True/False/None
    y dict id -> (n_true, n_total) para el analisis de estabilidad."""
    fn = INDICADORES[indicador]
    votos = defaultdict(list)
    for pasada in sorted(datos[punto]):
        for sid, r in datos[punto][pasada].items():
            if r.get("ok"):
                v = fn(r)
                if v is not None:
                    votos[sid].append(bool(v))
    consolidado, detalle = {}, {}
    for sid, vs in votos.items():
        detalle[sid] = (sum(vs), len(vs))
        consolidado[sid] = (sum(vs) * 2 > len(vs)) if vs else None
    return consolidado, detalle


# -------------------------------------------------------------------- salida
def main():
    ap = argparse.ArgumentParser(description="Analisis de la auditoria multipunto")
    ap.add_argument("--carpeta", default=".", help="carpeta con los resultados_*.json")
    ap.add_argument("--salida", default="analisis_multipunto.txt", help="archivo de informe")
    ap.add_argument("--grupo", default=None,
                    help="filtrar por el campo 'grupo' de universidades.json (p. ej. mundo)")
    ap.add_argument("--paises", default=None,
                    help="filtrar por codigos de pais separados por comas (p. ej. DE,FR,ES,NL)")
    args = ap.parse_args()

    datos, metas, archivos = cargar(args.carpeta)
    puntos = [p for p in ORDEN_PUNTOS if p in datos] + \
             [p for p in sorted(datos) if p not in ORDEN_PUNTOS]

    filtro_paises = None
    if args.paises:
        filtro_paises = {c.strip().upper() for c in args.paises.split(",")}

    def admitido(sid):
        for p in datos:
            for pasada in datos[p]:
                r = datos[p][pasada].get(sid)
                if r:
                    if args.grupo and r.get("grupo") != args.grupo:
                        return False
                    if filtro_paises and (r.get("pais") or "").upper() not in filtro_paises:
                        return False
                    return True
        return False

    lin = []
    W = lin.append

    W("=" * 78)
    W("ANALISIS DE LA AUDITORIA MULTIPUNTO")
    W("=" * 78)
    W(f"Archivos leidos: {len(archivos)}")
    for a in archivos:
        W("   " + os.path.basename(a))
    if args.grupo:
        W(f"Filtro de grupo: {args.grupo}")
    if filtro_paises:
        W(f"Filtro de paises: {', '.join(sorted(filtro_paises))}")

    # ---- 1. Control de calidad por pasada ----
    W("")
    W("-" * 78)
    W("1. CONTROL DE CALIDAD POR PASADA")
    W("-" * 78)
    W(f"{'Punto':6s} {'Pasada':>7s} {'Sitios':>7s} {'OK':>6s} {'Fallos':>7s}  Ubicacion verificada")
    for p in puntos:
        for pasada in sorted(datos[p]):
            regs = list(datos[p][pasada].values())
            ok = sum(1 for r in regs if r.get("ok"))
            m = next((x for x in metas
                      if x.get("vantage") == p and x.get("run") == pasada), None)
            if m is None:
                ubic = "(sin meta_*.json)"
            else:
                paises = [g.get("pais") for g in m.get("geolocalizacion", []) if g.get("pais")]
                ubic = ("SI  " if m.get("coincide_con_vantage") else "NO! ") + \
                       (", ".join(paises) if paises else "sin lectura")
            W(f"{p:6s} {pasada:>7d} {len(regs):>7d} {ok:>6d} {len(regs)-ok:>7d}  {ubic}")
    W("")
    W("Si alguna fila dice NO! la pasada se midio desde un pais distinto del")
    W("declarado y NO debe usarse. Repitala con la VPN correctamente conectada.")

    # ---- 1b. CALIBRACION: el volumen total de cookies debe ser comparable ----
    W("")
    W("-" * 78)
    W("1b. CALIBRACION ENTRE PUNTOS (control de artefactos de medicion)")
    W("-" * 78)
    W("Las cookies TOTALES (funcionales incluidas) no deberian depender del pais")
    W("desde el que se mide. Si un punto deposita muchas menos, la pagina se cargo")
    W("de forma incompleta desde ahi y la medicion de rastreo NO es comparable.")
    W("")
    tot = defaultdict(dict)
    for p in puntos:
        for pasada in datos[p]:
            for sid, r in datos[p][pasada].items():
                if r.get("ok") and r.get("cookies") and admitido(sid):
                    tot[p].setdefault(sid, []).append(r["cookies"].get("total_pre", 0))
    comunes_cal = set.intersection(*[set(tot[p]) for p in puntos]) if puntos else set()
    medias = {}
    for p in puntos:
        vals = [sum(v) / len(v) for s, v in tot[p].items() if s in comunes_cal]
        medias[p] = sum(vals) / len(vals) if vals else 0.0
        W(f"  {p:4s}  cookies por sitio: media {medias[p]:6.2f}   total {sum(vals):8.0f}   n={len(vals)}")
    if medias:
        ref = max(medias.values())
        W("")
        for p in puntos:
            desv = 100 * (medias[p] - ref) / ref if ref else 0
            estado = "OK" if desv > -15 else "SOSPECHOSO"
            W(f"  {p:4s}  desviacion respecto al punto mas alto: {desv:+6.1f} %   -> {estado}")
        if any(100 * (medias[p] - ref) / ref < -15 for p in puntos if ref):
            W("")
            W("  *** AVISO GRAVE ***")
            W("  Al menos un punto deposita mas de un 15 % menos cookies que los demas.")
            W("  Eso apunta a un problema del nodo de salida de la VPN (bloqueo, latencia")
            W("  o perdida de contenido de terceros), NO a segmentacion geografica.")
            W("  Repita ese punto desde OTRO servidor del mismo pais antes de usar los")
            W("  resultados. Las diferencias de rastreo que vea ahora son inseguras.")

    # ---- 2. Estabilidad entre pasadas ----
    W("")
    W("-" * 78)
    W("2. ESTABILIDAD ENTRE PASADAS DEL MISMO PUNTO")
    W("-" * 78)
    W("Porcentaje de sitios que dieron el MISMO resultado en todas sus pasadas.")
    W("Responde a la critica de 'una sola pasada': si la estabilidad es alta, la")
    W("medida es fiable; si es baja, hay que informarlo como ruido de medicion.")
    W("")
    W(f"{'Indicador':42s} " + " ".join(f"{p:>10s}" for p in puntos))
    for ind in INDICADORES:
        fila = []
        for p in puntos:
            _, det = consolidar(datos, p, ind)
            det = {k: v for k, v in det.items() if admitido(k)}
            elegibles = [(t, n) for t, n in det.values() if n >= 2]
            if not elegibles:
                fila.append("     n/d  ")
                continue
            estables = sum(1 for t, n in elegibles if t == 0 or t == n)
            fila.append(f"{100*estables/len(elegibles):9.1f}%")
        W(f"{ind:42s} " + " ".join(fila))

    # ---- 3. Consolidado por punto ----
    W("")
    W("-" * 78)
    W("3. PROPORCIONES CONSOLIDADAS POR PUNTO DE OBSERVACION")
    W("-" * 78)
    W("Regla de mayoria sobre las pasadas. IC 95 % de Wilson.")
    W("")
    consolidados = {}
    for ind in INDICADORES:
        W(f"  {ind}")
        for p in puntos:
            cons, _ = consolidar(datos, p, ind)
            cons = {k: v for k, v in cons.items() if admitido(k)}
            consolidados[(ind, p)] = cons
            n = len(cons)
            k = sum(1 for v in cons.values() if v)
            lo, hi = wilson(k, n)
            W(f"      {p:4s}  {k:3d}/{n:<3d}  {100*k/n if n else float('nan'):5.1f}%  "
              f"[{lo:5.1f}, {hi:5.1f}]")
        W("")

    # ---- 4. McNemar por pares ----
    W("-" * 78)
    W("4. PRUEBA DE McNEMAR EXACTA, POR PARES DE PUNTOS")
    W("-" * 78)
    W("Solo se usan los sitios medidos con exito en AMBOS puntos.")
    W("a = si en los dos; b = si en el primero y no en el segundo;")
    W("c = no en el primero y si en el segundo; d = no en ninguno.")
    W("Los pares DISCORDANTES (b y c) son los que llevan toda la informacion.")
    W("")
    for ind in INDICADORES:
        W(f"  {ind}")
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                p1, p2 = puntos[i], puntos[j]
                c1, c2 = consolidados[(ind, p1)], consolidados[(ind, p2)]
                comunes = [s for s in c1 if s in c2 and c1[s] is not None and c2[s] is not None]
                a = sum(1 for s in comunes if c1[s] and c2[s])
                b = sum(1 for s in comunes if c1[s] and not c2[s])
                c = sum(1 for s in comunes if not c1[s] and c2[s])
                d = sum(1 for s in comunes if not c1[s] and not c2[s])
                pval = mcnemar_exacto(b, c)
                orp = or_pareada(b, c)
                orstr = "n/d" if orp is None else f"{orp[0]:.2f} [{orp[1]:.2f}, {orp[2]:.2f}]"
                sig = "  <-- SIGNIFICATIVO" if pval < 0.05 else ""
                W(f"      {p1} vs {p2}:  n={len(comunes):3d}  a={a:3d} b={b:3d} c={c:3d} d={d:3d}  "
                  f"discordantes={b+c:3d}  p={pval:.4f}  RM pareada={orstr}{sig}")
        W("")

    # ---- 5. Cochran Q ----
    if len(puntos) >= 3:
        W("-" * 78)
        W("5. Q DE COCHRAN (los tres puntos a la vez)")
        W("-" * 78)
        W("Contrasta si la proporcion es la misma en los tres puntos de observacion.")
        W("")
        for ind in INDICADORES:
            cs = [consolidados[(ind, p)] for p in puntos]
            comunes = set(cs[0])
            for c in cs[1:]:
                comunes &= set(c)
            comunes = [s for s in comunes if all(c[s] is not None for c in cs)]
            tabla = [[1 if c[s] else 0 for c in cs] for s in comunes]
            Q, p, n = cochran_q(tabla)
            if Q != Q:  # NaN: los tres puntos dieron exactamente lo mismo
                W(f"  {ind:42s}  n={n:3d}  Q= n/d      "
                  f"(sin discordancia entre puntos)")
                continue
            sig = "  <-- SIGNIFICATIVO" if p < 0.05 else ""
            W(f"  {ind:42s}  n={n:3d}  Q={Q:7.3f}  p={p:.4f}{sig}")
        W("")

    W("-" * 78)
    W("COMO SE INFORMA ESTO EN EL ARTICULO")
    W("-" * 78)
    W("El resultado central es la fila 'rastreo_antes_del_consentimiento' de la")
    W("seccion 4, restringida a las instituciones EUROPEAS del grupo de referencia:")
    W("   python analizar_multipunto.py --paises DE,FR,ES,NL,BE,SE,CH,GB")
    W("Si b (rastrea visto desde Ecuador, no rastrea visto desde la UE) es grande")
    W("y c es pequeno, eso ES la segmentacion geografica del cumplimiento, medida")
    W("de forma directa. Informe siempre b, c, n, el valor p exacto y la razon de")
    W("momios pareada, no solo el valor p.")
    W("")

    texto = "\n".join(lin)
    print(texto)
    with open(os.path.join(args.carpeta, args.salida), "w", encoding="utf-8") as fh:
        fh.write(texto + "\n")
    print(f"\nInforme guardado en {args.salida}")


if __name__ == "__main__":
    main()
