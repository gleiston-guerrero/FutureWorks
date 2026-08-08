# Plantilla LaTeX no oficial para Enfoque UTE (IEEE — Formato Revista 2026)

Réplica en LaTeX del template Word oficial `Template_Enfoque_UTE_IEEE__FORMATO_REVISTA_2026-OTH.docx`.
Preserva todas las convenciones tipográficas del original (US Letter, dos columnas, IEEEtran, logo institucional, resumen bilingüe y las tres declaraciones obligatorias de la versión 2026).

## Archivos del paquete

| Archivo | Descripción |
|---|---|
| `main.tex` | Documento principal con estructura de artículo (introducción, related work, metodología, resultados, discusión, conclusión, apéndice, acknowledgment, funding/conflict/AI statement, referencias). |
| `references.bib` | Archivo BibTeX de ejemplo con las nueve tipologías más comunes en IEEE. |
| `enfoque_ute_logo.png` | Logo institucional extraído del template oficial. |
| `README.md` | Este archivo. |

## Requisitos en Windows

Se requiere una distribución LaTeX completa. Cualquiera de las dos funciona:

- **MiKTeX** (recomendado): descarga desde `https://miktex.org/download`. MiKTeX instala paquetes faltantes automáticamente al compilar.
- **TeX Live**: descarga desde `https://tug.org/texlive/`.

Paquetes LaTeX usados (todos en la distribución básica):
`IEEEtran`, `inputenc`, `fontenc`, `babel` (con soporte `english` y `spanish`), `geometry`, `graphicx`, `amsmath`, `amssymb`, `amsfonts`, `algorithmic`, `array`, `booktabs`, `multirow`, `longtable`, `textcomp`, `xcolor`, `listings`, `url`, `hyperref`, `cite`, `cleveref`.

## Compilación en Windows

Desde la carpeta del proyecto, en `cmd` o `PowerShell`:

```
pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex
```

O usando `latexmk` (más simple, resuelve las pasadas automáticamente):

```
latexmk -pdf main.tex
```

Con TeXstudio o TeXworks, basta con presionar F5 o el botón de compilación (asegúrese de que la herramienta de compilación esté configurada como `pdflatex + bibtex + pdflatex x 2`).

## Cómo adaptar la plantilla a un artículo real

1. **Título y autores**: edite el bloque `\title{...}` y `\author{...}`. Cada `\thanks{...}` corresponde a una nota al pie de la primera página (usualmente afiliaciones y correo del autor).
2. **Cabecera bibliográfica** (`\markboth{...}{...}`): actualice con el volumen, número y mes reales cuando reciba la asignación editorial.
3. **Abstract y Resumen**: escriba directamente dentro de los entornos `\begin{abstract}...\end{abstract}` y `\begin{resumen}...\end{resumen}` respectivamente.
4. **Palabras clave**: dos líneas — `\begin{IEEEkeywords}...\end{IEEEkeywords}` (inglés) y `\palabrasclave{...}` (español).
5. **Contenido**: reemplace las secciones de ejemplo por su contenido real. Todas las secciones estándar están numeradas con romanos automáticamente por IEEEtran.
6. **Figuras**: colóquelas en la carpeta `./figures/` (o en el mismo directorio del `.tex`). Use `\includegraphics[width=\columnwidth]{nombre.png}` dentro de un entorno `figure` para figuras de una columna, o `figure*` para figuras a doble columna.
7. **Tablas**: use el patrón mostrado en `\begin{table}...\end{table}` con `\toprule`, `\midrule`, `\bottomrule` (paquete `booktabs`). Para tablas a doble columna, use `\begin{table*}...\end{table*}`.
8. **Ecuaciones**: use `\begin{equation}...\end{equation}` con `\label{eq:...}` para poder referenciarlas con `\eqref{eq:...}` o `\cref{eq:...}`.
9. **Referencias**: añada entradas al archivo `references.bib` siguiendo los ejemplos incluidos. Cite con `\cite{clave}`.
10. **Declaraciones obligatorias**: en la sección final, elija exactamente una opción para cada declaración (`\seccionfunding{...}`, `\seccionconflicto{...}`, `\seccioniadeclaracion{...}`).

## Notas sobre el estilo Enfoque UTE 2026

- La revista exige que los manuscritos se remitan **solo en inglés**, con abstract adicional en español y palabras clave en ambos idiomas.
- Las tres declaraciones finales (FUNDING, CONFLICT OF INTEREST, ARTIFICIAL INTELLIGENCE STATEMENT) son **obligatorias** desde la versión 2026 del formato. Elija exactamente una de las opciones propuestas para cada una.
- Enfoque UTE es una revista Diamond Open Access (sin APC).
- Indexada en Web of Science ESCI, Redalyc, SciELO, REDIB, Latindex.

## Contacto y soporte

- Sitio oficial: `https://ingenieria.ute.edu.ec/index.php/revista`
- Directrices para autores: `https://ingenieria.ute.edu.ec/index.php/revista/about/submissions`

Esta plantilla es **no oficial** y se ofrece como conveniencia para quienes prefieren LaTeX. Verifique siempre las últimas directrices en el sitio de la revista antes del envío final.
