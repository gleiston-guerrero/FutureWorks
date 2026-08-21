# Registro de cambios — informe de segunda ronda, manuscrito UAIS

Fecha: 14 de agosto de 2026. Afecta a `privacidad_UAIS_en.tex` (versión de envío),
`privacidad_UAIS_es.tex` (versión paralela), `privacidad_mundo.bib`, `figuras_uais.py`.

---

## 1. Cómo actualizar el proyecto

| Archivo del proyecto | Se reemplaza por | Notas |
|---|---|---|
| `claude_privacidad_UAIS_en.tex` | `privacidad_UAIS_en.tex` | 42 sustituciones |
| `claude_privacidad_UAIS_es.tex` | `privacidad_UAIS_es.tex` | 17 sustituciones + flotantes |
| `claude_privacidad_mundo.bib` | `privacidad_mundo.bib` | 60 → 62 entradas |
| `claude_figuras_uais.py` | `figuras_uais.py` | solo la Figura E1 |
| — | `kappa_uais.py` | archivo nuevo |

Orden de compilación en Windows, con `sn-jnl.cls` y `sn-basic.bst` en la carpeta
del documento:

```
python figuras_uais.py
pdflatex privacidad_UAIS_en
bibtex   privacidad_UAIS_en
pdflatex privacidad_UAIS_en
pdflatex privacidad_UAIS_en
```

---

## 2. P0 — correcciones antes del envío

### P0.1 · Referencias a versiones anteriores del propio artículo

Cinco pasajes reescritos. Ninguna cadena `earlier draft`, `earlier version`,
`earlier practice` ni `versión anterior` queda en ninguna de las dos versiones.

| Sección | Antes | Ahora |
|---|---|---|
| §3.4, párr. 2 | «All six institutions that an earlier draft … named individually» | «Six institutions of the benchmark group were re-examined manually …», con la selección declarada como intencional y no aleatoria |
| §3.4, párr. 2 | «raises … from 58 to 59»; «lowers … from 48 to 47» | «The corrected values are the ones used in every figure and table» |
| §3.7 (ética) | «all cells for institutions that an earlier draft named individually» | «every cell of the six institutions examined in the verification sub-study» |
| §4.1, nota Canadá | «the earlier practice … is corrected here» | «so describing a single Canadian regime would be inaccurate» |
| §4.4 | «Two statements that appeared in an earlier version …» | «Two readings of these results must be resisted …» |
| §5.2, párr. 1 | «An earlier version of this work explained …» | «A reading that recurs in the applied literature explains …» |

La nota de la Tabla 1 («Two cells … were corrected after manual re-verification»)
se mantuvo sin cambios: describe el procedimiento, no una versión previa.

### P0.2 · Opción de plantilla `iicol`

- Preámbulo: `\documentclass[pdflatex,sn-basic,Numbered,iicol]{sn-jnl}`.
- Tablas 1, 2, 3 y 4 → `table*`. Figuras 1, 2 y 3 → `figure*`.
- Figuras E1 y E2 a `0.72\textwidth`.
- **Los anexos se componen con `\onecolumn`**, insertado justo después de
  `\begin{appendices}`. Es obligatorio: `longtable` no funciona en modo de dos
  columnas, y las matrices de los Anexos A, B, C y D son `longtable`.

Verificar en la primera compilación: que `\onecolumn` no rompa la numeración de
la clase, que ninguna `table*` quede huérfana al final del artículo y que las
Figuras 1–3 no desborden el ancho de página. Si la clase se resistiera a
`\onecolumn`, la alternativa es trasladar los Anexos C y D al depósito
suplementario y dejar en el artículo solo los agregados.

### P0.3 · Referencias corregidas

```bibtex
@article{mutimukwe2026privacy,
	author  = {Mutimukwe, Chantal and Viberg, Olga and McGrath, Cormac and
	           Cerratto-Pargman, Teresa},
	title   = {Privacy in Online Proctoring Systems in Higher Education: Stakeholders'
	           Perceptions, Awareness and Responsibility},
	journal = {Journal of Computing in Higher Education},
	year    = {2026},
	volume  = {38},
	number  = {2},
	pages   = {732--761},
	doi     = {10.1007/s12528-025-09461-5}
}
```

Cambios: la clave pasa de `mutimukwe2025privacy` a `mutimukwe2026privacy` y el
año de 2025 a 2026. SpringerLink da «Volume 38, pages 732–761 (2026)»; julio de
2025 es solo la publicación anticipada en línea. El apellido ya constaba correcto
como Mutimukwe en el `.bib`; la errata «Mutinukwe» del PDF revisado procede de
otra fuente y no está en el archivo.

```bibtex
@incollection{acostavargas2020improve,
	author    = {Acosta-Vargas, Patricia and Ramos-Galarza, Carlos and Salvador-Ullauri, Luis
	             and Chanchi, Gabriel El{\'i}as and Jad{\'a}n-Guerrero, Janio},
	title     = {Improve Accessibility and Visibility of Selected University Websites},
	booktitle = {Advances in Human Factors and Systems Interaction ({AHFE} 2020)},
	editor    = {Nunes, Isabel L.},
	series    = {Advances in Intelligent Systems and Computing},
	volume    = {1207},
	year      = {2020},
	pages     = {229--235},
	publisher = {Springer},
	address   = {Cham},
	doi       = {10.1007/978-3-030-51369-6_31}
}
```

Cambios: añadidos `volume = {1207}`, `editor` y `address`. Verificado en
SpringerLink (AISC vol. 1207, Springer, Cham).

### P0.4 · Declaraciones — pendiente de los autores

Sigue en gris, en español, dentro del PDF:

1. **Supplementary information** — depositar en Zenodo u OSF y sustituir el
   marcador por el DOI. Es prerrequisito de *Data availability*, que hoy remite a
   un repositorio inexistente.
2. **Acknowledgements** — completar o eliminar el bloque.
3. **Funding** — declarar financiación o su ausencia.
4. **Competing interests** — confirmar si el Ministerio participó en diseño,
   financiación o aprobación.
5. **Author contributions** — validar el reparto CRediT propuesto.
6. **Use of generative artificial intelligence** — UAIS exige la declaración.
   Si hubo asistencia de IA en redacción o análisis, lo prudente es declararla
   con su alcance. Ocultarla es un riesgo editorial mayor que cualquier
   consideración estilística.
7. **ORCID** — los tres identificadores en el sistema de envío de Springer.

### P0.5 · Norma de referencia

§3.5: «together with the level-AAA rules of WCAG 2.1 [59], which subsume those of
WCAG 2.0». Corregido también el pie de la Figura 3, que repetía el error.

### P0.6 · Columna `Ckp.` del Anexo C

Párrafo nuevo al final de §4.1, con el conteo verificado celda a celda sobre la
matriz del Anexo C (14 de 63 = 22,2 %) y la razón por la que no se compara: la
ley ecuatoriana no articula una regla de almacenamiento y acceso equivalente al
artículo 5(3) de la Directiva sobre privacidad electrónica, que es lo que da
origen a esos documentos en la Unión Europea.

---

## 3. P1 — vulnerabilidades de fondo

### P1.1 · Doble codificación — pendiente, requiere un segundo codificador

No es un cambio de texto: hay que ejecutarla. `kappa_uais.py` calcula el κ de
Cohen por indicador a partir de dos CSV con el formato

```
id,grupo,notice,framework,rights,dpo,accessibility
1,benchmark,1,1,1,1,1
```

Valores admitidos: `1`, `0`, `P`, `NV`. El script informa κ bajo la convención
del artículo (P y NV cuentan como ausencia), κ sobre tres categorías para
comprobar si la convención altera la conclusión, intervalo de confianza del 95 %
por bootstrap, acuerdo bruto y la lista de celdas a reconciliar.

Uso: `python kappa_uais.py codificador_A.csv codificador_B.csv`

Con 38 sitios (30 % de 126) el trabajo es de días. Cuando tenga los resultados,
este párrafo sustituye al tercero de §3.4 y el primer ítem del trabajo futuro de
§6 desaparece:

```latex
An independent second coder recoded a random 30\% of the sample (38 sites, stratified by group) against the same codebook, blind to the first coding. Agreement per indicator was XX.X\% for the privacy notice, XX.X\% for the cited framework, XX.X\% for the enumeration of rights and XX.X\% for the privacy contact, with Cohen's $\kappa$ of 0.XX [0.XX, 0.XX], 0.XX [0.XX, 0.XX], 0.XX [0.XX, 0.XX] and 0.XX [0.XX, 0.XX] respectively. All discrepancies were reconciled by discussion against the live site, and the reconciled codes are the ones reported throughout. The indicator with the lowest agreement was XXX, which is the one requiring most judgement, and its results should be read with that in mind.
```

Mientras tanto, §3.4 y §5.5 declaran la limitación de forma explícita y añaden
que las seis instituciones del subestudio no se eligieron al azar, lo que es más
honesto que la formulación anterior.

### P1.2 · Anclaje en la literatura de acceso universal

Tres párrafos nuevos al inicio de §2.1, antes de la revisión de auditorías, con
la conexión explícita entre privacidad opaca y accesibilidad deficiente como dos
formas del mismo coste desigual de uso. Dos entradas nuevas en el `.bib`, ambas
publicadas en la propia revista:

```bibtex
@article{persson2015universal,
	author  = {Persson, Hans and {\AA}hman, Henrik and Yngling, Alexander Arvei
	           and Gulliksen, Jan},
	title   = {Universal Design, Inclusive Design, Accessible Design, Design for All:
	           Different Concepts---One Goal? On the Concept of Accessibility---Historical,
	           Methodological and Philosophical Aspects},
	journal = {Universal Access in the Information Society},
	year    = {2015},
	volume  = {14},
	number  = {4},
	pages   = {505--526},
	doi     = {10.1007/s10209-014-0358-z}
}

@article{liginlal2026digital,
	author  = {Liginlal, Divakaran and Al-Emadi, Sara},
	title   = {Digital Accessibility and Equity: The Need for Stronger Regulations
	           and the Imperative of Innovation},
	journal = {Universal Access in the Information Society},
	year    = {2026},
	volume  = {25},
	number  = {2},
	pages   = {37},
	doi     = {10.1007/s10209-025-01305-4}
}
```

`liginlal2026digital` es número de artículo, no rango de páginas: volumen 25,
artículo 37, número 2 de 2026, publicado en línea el 21 de enero de 2026.
Verificado en SpringerLink.

### P1.3 · Frase opaca de §5.5

«Two errors in 24 cells does not constitute a reliability estimate, and the six
institutions were not selected at random, but neither is the figure reassuring.»

---

## 4. P2 — pulido

- **`against` → `compared with`** en los ocho usos comparativos: resumen (dos),
  §4.1, §4.4 (tres), §6 (dos). Los diez `against` restantes son usos legítimos
  del inglés (`audited against WCAG 2.2`, `against the live site`,
  `benchmarking against an aspirational ceiling`, `conformance against
  pre-consent tracking`, `against a published matrix`) y se conservan.
  En la versión ES no se toca «frente a», que es la forma correcta en español.
- **Resto de Asia.** Frase nueva en §4.1. Aritmética comprobada sobre el Anexo C:
  China 6 + resto de Asia 5 = 11 de los 16 sitios de referencia sin declaración
  de accesibilidad; los 5 restantes son 2 de Estados Unidos, 2 de Europa
  continental y 1 de Australia.
- **`UPACÍFICO` → `UPACIFICO`** en la fila 50 del Anexo D. Es la sigla que usan
  tanto la SENESCYT como el propio sitio institucional; el nombre completo es
  Universidad del Pacífico Escuela de Negocios.
- **Tiempos verbales** unificados en presente en §2.2 para el conocimiento
  establecido (`establish`, `report`, `reach`, `find`). Los resultados propios
  siguen en pasado.
- **Figura E1** reordenada por región, en el mismo orden que la Tabla 2, con
  separadores punteados y el total de cada región rotulado al margen derecho.
  Pie de figura actualizado en ambas versiones.
- **Resumen** recortado de 249 a 245 palabras, para dejar margen bajo el límite
  de 250. El resumen de la versión ES no se recorta: no es el que se envía.

---

## 5. Verificaciones ejecutadas sobre los archivos entregados

- Entornos LaTeX balanceados y llaves cuadradas en ambas versiones.
- 62 claves citadas y 62 entradas en el `.bib`, sin faltantes ni huérfanas.
- Cero apariciones de las cadenas eliminadas en P0.1, P0.5 y P1.3.
- `figuras_uais.py` ejecutado: las cinco figuras se generan sin error.
- `kappa_uais.py` probado con datos sintéticos.
- Rastros de redacción automática: cero guiones largos Unicode, cero *delve*,
  *leverage*, *underscore*, *pivotal*, *crucial*, *realm*, *landscape*,
  *testament*; ninguna construcción *not merely … but*; ningún encadenamiento de
  *Moreover / Furthermore / Additionally*. Los tres `---` del archivo pertenecen
  a la lista CRediT.

## 6. Lo que no pude verificar aquí

No dispongo de `sn-jnl.cls`, de modo que el PDF no se compiló en este entorno.
Los dos puntos que exigen su comprobación en la primera compilación son el paso
a doble columna y el comportamiento de `\onecolumn` en los anexos.
