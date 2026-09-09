# Evaluaciones manuales y capturas — LOPDP y la Educación Superior

Extraído de `gleiston-guerrero/FutureWorks`, carpeta `LOPDP y la Educación Superior`,
el 8 de septiembre de 2026. Nada de esto está hoy en el depósito público
`wcag-preconsent-tracking-university-websites` ni en Zenodo.

## capturas/ — 45 ficheros

Quince sitios, tres criterios WCAG, una captura por criterio y sitio.

- raíz: criterio **1.1.1**, contenido no textual (15 PNG)
- `1.4.3/`: contraste mínimo AA (15 PNG)
- `2.4.4/`: propósito del enlace en su contexto (15 PNG)

Sitios: UC Berkeley, UCL, Cornell, NUS, Northwestern, Manchester, HKUST del grupo
de referencia; UNESUM, USECIPOL, IAEN, ULVR, UTPL, UPS, UTI (indoamerica) y ECOTEC
del censo ecuatoriano.

## evaluaciones_para_deposito/ — 7 ficheros

Marcados como «listo para el depósito» en `MANIFIESTO.csv`. Sin nombres de evaluador:
usan códigos E01, E02, E08, D01.

- `wcag_validacion_15_sitios.csv` — 45 filas, una por sitio y criterio, con código,
  n, f, evaluador codificado, fecha, duración, capturas y dictamen técnico
- `codificacion_manual_15_universidades.csv` — 15 filas; **todas dicen
  «un solo codificador»** en las tres columnas de estado
- `wcag_pares_kappa.csv` — pares primera/segunda codificación con columna de acuerdo
- `wcag_doble_evaluacion_5_sitios.csv` — segunda evaluación sobre 5 sitios, con
  justificación por celda
- `recodificacion_143.csv`, `recodificacion_244.csv`
- `wcag_validacion_anonimizado.xlsx`

## evaluaciones_con_nombres_NO_PUBLICAR/ — 5 ficheros

Las mismas evaluaciones con los nombres reales de los evaluadores. El `MANIFIESTO.csv`
las marca «no va al depósito público». Consérvelas fuera del repositorio.

## notas_internas/ — 5 ficheros

Notas de trabajo, incluida `respuesta-observaciones-uais.md` (18,9 KB) y
`hallazgos-validacion-manual-wcag.md` (7,6 KB). No publicables.

## scripts_listos_para_deposito/ — 4 ficheros

`estudio.py`, `kappa_wcag.py`, `qa_cookies.py`, `reconciliar.py`. Marcados como listos
y no subidos.

## Rastro de sesiones anteriores

`MANIFIESTO.csv` registra trece ficheros con prefijo `claude_` en su columna de origen,
renombrados al copiarlos a su destino. Seis conservan el prefijo en
`data_code_others/`: `claude_analizar_multipunto.py`, `claude_auditar.js`,
`claude_auditar_multipunto.js`, `claude_figuras_uais.py`, `claude_seleccion63-mundo.json`
y `claude_stats_uais.py`.
