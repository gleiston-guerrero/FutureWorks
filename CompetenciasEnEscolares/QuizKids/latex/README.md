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
- `figuras/` — Figuras del documento, todas en PDF para máxima calidad.
- `figuras_originales/` — Imágenes originales en PNG provistas por el autor.
- `figuras_real/` — Versiones PDF de las imágenes reales (sin pérdida).
- `figuras_vectoriales_backup/` — Versiones vectoriales generadas
  inicialmente (mantenidas como respaldo).

## Compilación

Requisitos: TeX Live 2023 o superior con `biblatex`, `biber` y los
paquetes `texlive-bibtex-extra`, `texlive-publishers`.

```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

Producirá `main.pdf` (~108 páginas).

## Notas sobre las imágenes

Las imágenes principales del documento (logo UTEQ, metodología XP,
cronograma, diagrama de casos de uso, arquitectura tecnológica, modelo
de base de datos, prototipos Figma, capturas reales del sistema y
diagramas de secuencia de cada caso de uso) provienen directamente de
los archivos originales del autor. Se preservan sin pérdida mediante
conversión a PDF con `img2pdf`.

Las gráficas estadísticas (cumplimiento de plazos, SUS, TAM) sí son
generadas vectorialmente con matplotlib (los scripts Python están
disponibles en `figuras_vectoriales_backup/`).

## Cumplimiento normativo UTEQ

- Times New Roman 12 pt, interlineado 1.5.
- Márgenes: izquierdo 3 cm; superior, inferior y derecho 2.5 cm.
- Páginas preliminares numeradas en romanos (i, ii, …).
- Cuerpo numerado en arábigos.
- Numeración inferior derecha.
- Redacción impersonal en todo el documento.
- Etiquetas: "Tabla X", "Ilustración X" según norma UTEQ.
- Niveles 1.1 (negrita), 1.1.1 (cursiva + negrita).
- Citas en formato IEEE.

## Estructura del documento generado (108 páginas)

1. Portada con logo UTEQ.
2. Páginas preliminares (i–xiii, 13 páginas).
3. Introducción.
4. Capítulo I: Marco contextual del proyecto tecnológico.
5. Capítulo II: Marco teórico del proyecto tecnológico.
6. Capítulo III: Metodología.
7. Capítulo IV: Resultados (incluye 16 casos de uso con sus
   diagramas de secuencia y capturas de UI reales).
8. Capítulo V: Conclusiones y recomendaciones.
9. Bibliografía (formato IEEE).
10. Anexos A–E.
