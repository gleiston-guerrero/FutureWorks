#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anade la columna id_auditoria a las tablas de validacion manual WCAG.

Las tablas de validacion usan una numeracion de sitios distinta de la del
resto del deposito: ambas cubren las mismas 126 instituciones, pero ordenan
los dos grupos al reves. La columna id original se conserva, porque es la que
aparece en el manuscrito y en las entregas de los revisores; se anade
id_auditoria para poder unir con resultados.json y con las tablas derivadas.

La correspondencia se establece por URL de portada, con la sigla como
respaldo. El script aborta si algun sitio no se resuelve.

Uso:
    python anadir_id_auditoria.py <dir_datos> <dir_validacion>
"""
import csv
import json
import re
import sys
from pathlib import Path

ARCHIVOS = ["wcag_validacion_15_sitios.csv",
            "wcag_doble_evaluacion_5_sitios.csv",
            "wcag_pares_kappa.csv"]


def norm(u):
    return re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()).rstrip("/").split("/")[0]


def main(dir_datos, dir_val):
    dd, dv = Path(dir_datos), Path(dir_val)
    raw = json.loads((dd / "resultados.json").read_text(encoding="utf-8"))
    by_url = {norm(r["url"]): str(r["id"]) for r in raw}
    by_sig = {r["sigla"].strip().lower(): str(r["id"]) for r in raw}

    # La tabla de pares no lleva url; se resuelve por sigla contra la principal.
    with (dv / ARCHIVOS[0]).open(encoding="utf-8-sig") as f:
        base = {r["sigla"].strip().lower(): r["url"] for r in csv.DictReader(f)}

    for nombre in ARCHIVOS:
        ruta = dv / nombre
        with ruta.open(encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
            cab = list(rows[0].keys())
        if "id_auditoria" in cab:
            print("  ya tiene la columna:", nombre)
            continue

        sin = []
        for r in rows:
            url = r.get("url") or base.get(r["sigla"].strip().lower(), "")
            cid = by_url.get(norm(url)) or by_sig.get(r["sigla"].strip().lower())
            if not cid:
                sin.append(r["sigla"])
            r["id_auditoria"] = cid or ""
        if sin:
            raise SystemExit("ABORTA: sin correspondencia en %s -> %s" % (nombre, sorted(set(sin))))

        cab.insert(cab.index("id") + 1, "id_auditoria")
        with ruta.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cab)
            w.writeheader()
            w.writerows(rows)
        print("  %-38s %d filas, columna anadida" % (nombre, len(rows)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos",
         sys.argv[2] if len(sys.argv) > 2 else "validacion_wcag")
