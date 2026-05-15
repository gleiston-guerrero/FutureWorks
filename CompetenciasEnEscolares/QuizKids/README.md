# Proyecto Tecnológico Kiddy Quiz – UTEQ

**Autor:** Jeandavid Rodolfo Cabrera Guerra
**Director:** Ing. Gleiston Ciceron Guerrero Ulloa, PhD.
**Universidad:** Universidad Técnica Estatal de Quevedo
**Facultad:** Ciencias de la Ingeniería
**Carrera:** Software
**Año:** 2025

## Contenido

- `main.tex` — Archivo principal con preámbulo, geometría UTEQ, páginas
  preliminares (portada, declaración de autoría, certificación del
  director, certificado de plagio, tribunal, agradecimiento, dedicatoria,
  resumen, abstract, índices, código Dublin) y bibliografía IEEE.
- `cap_introduccion.tex` — Introducción.
- `cap1_marco_contextual.tex` — Capítulo I.
- `cap2_marco_teorico.tex` — Capítulo II.
- `cap3_metodologia.tex` — Capítulo III.
- `cap4_resultados.tex` — Capítulo IV.
- `cap5_conclusiones.tex` — Capítulo V (Conclusiones y recomendaciones).
- `cap_anexos.tex` — Anexos A–E.
- `referencias.bib` — 51 referencias IEEE verificadas y corregidas.
- `figuras/` — 13 figuras vectoriales en PDF y los scripts Python que
  las generaron.

## Compilación

Requisitos: TeX Live 2023 o superior con `biblatex`, `biber` y los
paquetes `texlive-bibtex-extra`, `texlive-publishers`.

```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

Producirá `main.pdf` (~86 páginas).

## Notas sobre las figuras

Las 13 figuras del cuerpo del documento fueron generadas con scripts
Python (matplotlib) y exportadas como PDF vectorial para garantizar la
máxima nitidez en cualquier nivel de zoom. Los scripts originales se
incluyen en `figuras/gen_fig*.py`. Si se desea sustituir alguna por
una imagen real (capturas de pantalla del sistema, fotos, etc.),
basta con reemplazar el archivo PDF correspondiente conservando el
nombre.

## Cumplimiento normativo UTEQ

- Times New Roman 12 pt, interlineado 1.5.
- Márgenes: izquierdo 3 cm; superior, inferior y derecho 2.5 cm.
- Páginas preliminares numeradas en romanos (i, ii, …).
- Cuerpo numerado en arábigos.
- Numeración inferior derecha.
- Redacción impersonal en todo el documento.
- Niveles 1.1 (negrita), 1.1.1 (cursiva + negrita).
- Citas en formato IEEE.
