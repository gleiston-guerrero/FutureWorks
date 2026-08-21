# Respuesta punto por punto al informe de evaluación (UAIS)

Fecha: 14 de agosto de 2026. Archivos afectados: `privacidad_UAIS_en.tex`, `privacidad_UAIS_es.tex`, `privacidad_mundo.bib`, cinco figuras PDF, `figuras.py`, `stats.py`.

Leyenda: **ATENDIDO** = resuelto en el manuscrito · **PARCIAL** = resuelto hasta donde permiten los datos existentes, con la limitación declarada en el texto · **PENDIENTE** = exige medición nueva y queda escrito como trabajo futuro.

---

## 1. Los seis problemas que bloqueaban la publicación

| # | Observación | Estado | Cómo se atendió |
|---|---|---|---|
| 1 | Contradicciones entre resumen, conclusiones y tablas | **ATENDIDO** | Reescritos resumen, resultados y conclusiones. Se declara explícitamente en §4.4 que las dos afirmaciones anteriores eran falsas y se sustituyen por el enunciado que los datos sí sostienen (difiere la *distribución* de fallos, no su presencia). |
| 2 | Incumplimiento formal de las instrucciones de UAIS | **ATENDIDO** | Resumen estructurado (Purpose/Methods/Results/Conclusion, 249 palabras); 6 palabras clave con WCAG incluida; bloque completo *Statements and Declarations*; *Data* y *Code availability*; ORCID señalado; declaración de uso de IA generativa. |
| 3 | Irreproducibilidad de la medición | **ATENDIDO** | §3.5 declara navegador, banderas de lanzamiento, *viewport* (1280×720), agente de usuario, `waitUntil`, timeout, reintentos, espera fija de 4 s, `ignoreHTTPSErrors`, ausencia de *scroll*, etiquetas exactas de axe-core, `resultTypes` y reglas derivadas. La taxonomía completa de cookies de rastreo y el método de detección de CMP y banner están en el Anexo A. |
| 4 | Aceptación de hipótesis nulas sin prueba | **ATENDIDO** | Reanálisis completo: Wilson, Newcombe, razones de momios de Woolf, Fisher exacto, corrección de Holm, TOST a 10/15/20 pp, MDE y tamaño muestral necesario, IC de Fisher-z para ρ. El texto ahora dice "no se encontró evidencia de diferencia y no hubo potencia para establecer equivalencia". |
| 5 | Error jurídico sobre el ámbito del RGPD | **ATENDIDO** | Nueva §5.2 completa: art. 3(1) y 3(2), Directrices 3/2018 del CEPD, y reconducción del punto defendible al art. 5(3) ePrivacy con las Directrices 2/2023. Discusión y conclusiones reescritas: segmentación geográfica del cumplimiento, no laguna legal. |
| 6 | Calidad del inglés y registro | **ATENDIDO** | Texto reescrito de cero en inglés académico. Ver §6 de esta tabla para el detalle de calcos, tiempos verbales y retórica. |

---

## 2. Las veinte inconsistencias internas (C1–C20)

| Cód. | Estado | Resolución |
|---|---|---|
| C1 "ninguna institución libre de fallos" | **ATENDIDO** | Corregido y desmentido de forma expresa: 6 instituciones de referencia (9,5 %) no produjeron fallo automático alguno. |
| C2 "el mundo solo tropieza en AAA" | **ATENDIDO** | Corregido: el 60,3 % de los sitios de referencia produce al menos un fallo de nivel A. |
| C3 Hong Kong "cumple sin fisuras" | **ATENDIDO** | Eliminada la frase; el Cuadro 2 se lee ahora como descriptivo y se advierte que con *n* = 3 el IC supera los 50 pp. |
| C4 Harvard/Michigan/WUSTL | **ATENDIDO** | Se retiran los nombres del cuerpo del texto. Además se verificó manualmente cada celda (ver §5 abajo). |
| C5 "nueve de diez citan el RGPD" | **ATENDIDO** | Corregido: dos de las diez son suizas y están sujetas a la nLPD, no al RGPD. |
| C6 Fudan y Shanghai Jiao Tong | **ATENDIDO** | Retirados los nombres del cuerpo; la regla de agregación del código P se declara en el Anexo A. |
| C7 Cambridge sin política | **ATENDIDO** | Falso negativo confirmado por verificación manual; celda corregida (58 → 59) y la corrección se documenta en §3.4. |
| C8 "dos anexos" | **ATENDIDO** | Hay cinco anexos (A–E) y así se anuncia. |
| C9 numeración B1/C2 | **ATENDIDO** | `\thetable` redefinido por anexo con contador reiniciado: A1, B1, C1, D1, E1–E2. |
| C10 "hoja de ruta" no entregada | **ATENDIDO** | La §5.3 y la §5.4 contienen implicaciones separadas para práctica y política; el anuncio del índice coincide con el contenido. |
| C11 comprobaciones de revisión manual | **ATENDIDO** | Se declara que se registran por sitio y que no se analizan aquí; la promesa incumplida desaparece. |
| C12 Figura 4 suma 101 % | **ATENDIDO** | Regla de redondeo declarada en §3.6 y en la nota del Cuadro 3. |
| C13 código de país "UN" | **ATENDIDO** | Todos los códigos son ISO 3166-1 alfa-2; "UK" pasó a "GB". |
| C14 "Paris-Sacaly" | **ATENDIDO** | Verificado como "Paris-Saclay". |
| C15 etiquetas erróneas de la Figura 2 | **ATENDIDO** | Figura regenerada con PDPO, APPI, PIPA y nLPD correctas, más PIPEDA. |
| C16 columna "Cook." con dos significados | **ATENDIDO** | En el grupo de referencia pasa a "Ckp." con definición explícita; en el censo ecuatoriano se elimina y las medidas en vivo se informan solo agregadas. |
| C17 tres nombres para accesibilidad | **ATENDIDO** | "Acc." con una única definición en los dos anexos y en el libro de códigos. |
| C18 columna LOTAIP nunca analizada | **ATENDIDO** | Se analiza en §4.3: 47 de 63 (74,6 %), con la advertencia de que no tiene contrapartida en el grupo de referencia. |
| C19 columna "Cook." llena de n/d | **ATENDIDO** | Eliminada, con justificación explícita en la leyenda del Anexo D. |
| C20 "30 % accesibles que rastrean" | **ATENDIDO** | Sustituido por la tabla cruzada completa 2×2 por grupo (Cuadro 4), con denominadores explícitos. |

---

## 3. Rigor metodológico

- **Censo frente a élite** — **ATENDIDO**: §3.1 declara que es un ejercicio de referenciación contra un techo aspiracional y que recursos y jurisdicción están plenamente confundidos; en ningún punto se atribuye causalidad al país. El tercer estrato queda como limitación.
- **Confusores no medidos** — **ATENDIDO** como limitación explícita (§5.5); el análisis por tipo de institución se propone como trabajo futuro de mayor valor local.
- **n = 63 sin justificación de potencia** — **ATENDIDO**: MDE de 23,7 pp, n ≈ 1412 para detectar 5 pp, n ≈ 278 para equivalencia a ±10 pp.
- **Regla de imputación 76 sin sensibilidad** — **PENDIENTE**: las tres decisiones arbitrarias se enumeran y se declara que no se variaron (§3.2 y §5.5). Repetir el *pipeline* con reglas alternativas exige rehacer la selección.
- **Diagrama de flujo de la muestra ecuatoriana** — **PARCIAL**: se declara la fuente (SENESCYT/CES), la fecha de consulta y la inclusión de las IES creadas en 2024–2025, marcadas con ‡ en el Anexo D.
- **Unidad de análisis mal definida** — **ATENDIDO**: §3.1 la define como la portada y el aviso de primer nivel enlazado desde ella, con la regla de "un clic".
- **Libro de códigos inexistente** — **ATENDIDO**: Anexo A completo, con definiciones operativas, umbrales y tratamiento de casos ambiguos.
- **Fiabilidad entre codificadores** — **PARCIAL**: no hay κ porque no hubo doble codificación, y así se declara. Se añade un subestudio de verificación dirigida (24 celdas, 2 errores) que acota el problema y lo hace visible. La doble codificación del 30 % es el primer punto del trabajo futuro.
- **Código P y códigos n/a en el denominador** — **ATENDIDO** como limitación declarada con la dirección del sesgo señalada (deprime específicamente los porcentajes ecuatorianos).
- **Configuración de axe-core y hallazgo AAA** — **ATENDIDO**: se declara que `INCLUIR_AAA = true` y se publican las ocho etiquetas exactas. Se confirma la sospecha del informe: sí se activaron reglas AAA de WCAG 2.0 y 2.1. La Figura 3 informa ahora la distribución **con y sin** reglas AAA; la ordenación se mantiene (46,3 % frente a 60,8 % en nivel A).
- **Versión de WCAG indeterminada** — **ATENDIDO**: norma de referencia WCAG 2.2 niveles A y AA, más reglas AAA de 2.0 y 2.1; se explica que axe-core 4.13 no implementa AAA de 2.2. La referencia [wcag22] es la Recomendación fechada del 12 de diciembre de 2024.
- **Protocolo de navegación** — **ATENDIDO** en su totalidad (ver punto 3 de la tabla 1).
- **Una sola pasada / solo la portada / sin repositorio** — **PARCIAL**: declarados como amenazas a la validez con su dirección, y convertidos en puntos concretos del trabajo futuro. El depósito en Zenodo u OSF queda marcado como acción pendiente de los autores.
- **Taxonomía de cookies sin declarar** — **ATENDIDO**: lista completa de patrones en el Anexo A, con la advertencia de que es conservadora (cotas inferiores).
- **Solo cookies** — **ATENDIDO** como limitación: `localStorage`, `IndexedDB`, *fingerprinting*, píxeles sin cookie y etiquetado del lado del servidor quedan fuera; se propone el recuento de dominios de terceros como métrica más robusta.
- **Firma del CMP sin método** — **ATENDIDO**: se describen las tres vías de detección (`src`, globales, `__tcfapi`) y se admite que la tasa de falsos negativos no se midió.

---

## 4. Análisis estadístico

Todo el bloque está **ATENDIDO** salvo lo que exige datos por sitio que no están disponibles:

- ρ de Spearman: ahora con *n*, *p* = 0,657, IC de Fisher-z [−0,14, +0,21] y correlación mínima detectable (0,25). Se retira la afirmación de independencia.
- **Paradoja de Simpson**: resuelta. El Cuadro 4 da la asociación **dentro de cada grupo** (RM 0,54 y 1,17, ambas no significativas) y la estimación de Mantel–Haenszel ajustada (0,66). Este era uno de los puntos más fuertes del informe y el resultado por grupo cambia la lectura: el ρ agrupado de 0,04 enmascaraba una asociación ligeramente negativa dentro del grupo de referencia.
- TOST con tres márgenes y declaración de que no fueron preespecificados.
- Pruebas inferenciales y tamaños de efecto para los doce indicadores, con Holm. Tres diferencias no sobreviven a la corrección (derechos, sin fallo alguno, TLS) y el texto las degrada explícitamente a indicios.
- Comparaciones múltiples: controladas y declaradas.
- Subgrupos regionales: el Cuadro 2 se presenta sin porcentajes ni inferencia, con la razón escrita.
- "Apenas el 3 % logra ambas": se muestra que 2/63 es exactamente lo esperado por azar (1,8).
- **Seudorreplicación y composicionalidad de la Figura 3**: ambas declaradas en §4.4; se indica que las medidas por sitio son las inferencialmente seguras.
- **PENDIENTE** (exige `resultados.json` por sitio): recálculo con el sitio como unidad o GLMM, normalización por complejidad de página, inferencia robusta por conglomerados de CMS y diagrama de dispersión.

---

## 5. Validez de constructo, ética y verificación manual

- **TLS** — **ATENDIDO**: reclasificado como seguridad del transporte, con la advertencia de que un certificado impecable no impide la exfiltración, y se explica que la auditoría usaba `ignoreHTTPSErrors`, por lo que el indicador se verificó aparte.
- **Rastreo previo aplicado a once jurisdicciones** — **ATENDIDO**: Anexo B con el mapeo indicador × jurisdicción × obligación. Se afirma expresamente que en la mayoría de las jurisdicciones estudiadas depositar una cookie de rastreo antes del consentimiento **no es ilícito**, y que el indicador mide exposición, no cumplimiento.
- **Un solo punto de observación** — **ATENDIDO** como amenaza declarada: §4.2 dice que el resultado confunde dos posibilidades de lectura jurídica opuesta, y §5.2 y §6 convierten el experimento multipunto en el trabajo futuro principal.
- **Cruce accesibilidad declarada × conformidad medida** — **PARCIAL**: se realiza el cruce conformidad × rastreo (Cuadro 4). El cruce declarada × medida y CMP × rastreo exige los datos por sitio.
- **"Reaches level A"** — **ATENDIDO**: renombrado a "sin fallo de nivel A detectado" en todas partes, con nota de que no es una afirmación de conformidad.
- **Nombrar instituciones incumplidoras** — **ATENDIDO**: no se nombra ninguna en el cuerpo. Además se realizó la verificación manual que pedía el informe, con estos resultados:

| Institución | Celda | Resultado de la verificación |
|---|---|---|
| Cambridge | Aviso de privacidad = ausente | **FALSO NEGATIVO**. Hay aviso enlazado en el pie de la portada. Celda corregida a presente. |
| Harvard | Marco legal = presente | **FALSO POSITIVO**. El *Privacy Statement* no nombra GDPR, CCPA, FERPA ni ninguna norma; solo fórmulas genéricas. Celda corregida a ausente. |
| Michigan | Derechos y marco = ausentes | Correcto **a profundidad 1**; el contenido existe un clic más abajo. Es una propiedad de la unidad de análisis, no un error, y así se declara. |
| WUSTL | Cuatro celdas | Confirmadas, con dos redirecciones 302 en la ruta. |
| Fudan, SJTU | Sin política central | **Confirmado**. Existen políticas en subdominios de facultad, no enlazadas desde la portada. |

  Las dos correcciones cambian: aviso 58 → **59/63 (93,7 %)**; marco 48 → **47/63 (74,6 %)**. Cuadro 2 regional: Reino Unido aviso 6 → 7; EE. UU. marco 18 → 17. Todas las cifras, figuras y pruebas se recalcularon. Ninguna conclusión cambia de signo.

- **Conflicto de interés UTEQ / Ministerio** — **ATENDIDO**: declarado de forma expresa en *Competing interests*, con la recomendación de que un tercero independiente reproduzca la codificación de la UTEQ.
- **Declaraciones obligatorias de Springer** — **ATENDIDO** (con marcadores en gris donde solo los autores pueden completar).
- **Efecto de publicar una tabla de cumplimiento** — **ATENDIDO**: §5.4 advierte que un indicador que se convierte en objetivo se satisface en la superficie, con el banner de cookies como ejemplo.

---

## 6. Escritura

**ATENDIDO en su totalidad.** El texto se reescribió, no se corrigió.

- Falsos amigos: *affirmative action* → *accessibility statement*; *treatment notice* → *privacy notice*; *treatment* → *processing*; *the reference* → *the benchmark group*; *houses* → *institutions*; *census* → *complete population*; y el resto de la tabla del informe.
- Tiempos verbales: métodos y resultados propios en pasado en todo el artículo; interpretación y referencias a cuadros en presente. Se elimina "no university on the planet".
- Registro: retiradas las más de veinte figuras retóricas. "Consent theatre" desaparece; se usa la terminología citable de *dark patterns in consent interfaces*.
- Puntuación: sin rayas al modo español; sin verbos frasales partidos por incisos.
- Terminología: *controller* frente a *data protection officer* distinguidos de forma expresa en §3.3; una sola etiqueta por objeto; *choropleth* sustituido por un gráfico de barras accesible.
- Acrónimos: SENESCYT, CES, HEI, LOPDP, LOTAIP, TLS, CMP, WCAG, ADA y los nueve marcos jurídicos se expanden en su primera aparición; el Anexo B da la correspondencia sigla–norma–jurisdicción.
- Voz unificada: se usa "we" de forma consistente donde corresponde.

---

## 7. Figuras y tablas

**ATENDIDO.** Las cinco figuras se generaron de nuevo con `figuras.py`:

1. **Figura 1 (nueva)** — *forest plot* de diferencias de riesgo con IC del 95 %, agrupado por dominio. Sustituye a la narración selectiva.
2. **Figura 2** — cookies previas al consentimiento **con barras de error** de Wilson.
3. **Figura 3** — nodos por nivel, en dos paneles: con y sin reglas AAA (el análisis de sensibilidad que pedía el informe).
4. **Figura E1** — composición por país en barras horizontales; sustituye al mapa coroplético, que codificaba solo por color.
5. **Figura E2** — cronología vertical con las etiquetas normativas corregidas.

Todas: patrones de trama además del color (`//` y `xx`), dos tintas con contraste ≈ 11,4:1 y ≈ 7,3:1 sobre blanco, fuentes incrustadas (Type 42), tamaño calibrado al ancho de columna real de `sn-jnl` (372 pt) para que el texto se lea a tamaño de impresión, y leyenda fuera del área de datos. Las figuras contextuales pasaron al Anexo E.

Cuadro 1 con IC y valores ajustados; Cuadro 2 sin porcentajes por la razón declarada; Cuadro 3 con la distribución en ambas convenciones; Cuadro 4 nuevo con la tabla cruzada. La definición operativa que estaba enterrada en el pie del Cuadro 1 se trasladó a Métodos.

---

## 8. Referencias

**ATENDIDO.** El `.bib` se reconstruyó por completo:

- Doce anotaciones en español eliminadas.
- Mayúsculas de gentilicios, topónimos y siglas protegidas con llaves.
- WCAG 2.1 sustituida como norma de referencia por **WCAG 2.2**, Recomendación del 12 de diciembre de 2024 (verificado: la primera Recomendación es del 5 de octubre de 2023 y la vigente es la republicación de diciembre de 2024). Se conserva la entrada de 2.1 porque las reglas AAA ejecutadas son de 2.0 y 2.1.
- Literatura de medición de privacidad web incorporada y verificada campo a campo: Englehardt & Narayanan (CCS 2016), Libert (IJoC 2015), Sanchez-Rola et al. (AsiaCCS 2019), Matte, Bielova & Santos (IEEE S&P 2020), Trevisan et al. (PoPETs 2019), Bollinger et al. (USENIX Security 2022).
- Autoridad jurídica añadida: Directrices 3/2018 y 2/2023 del CEPD; PIPEDA; FIPPA de Columbia Británica; citas oficiales corregidas de ADA, Sección 508, nLPD suiza y el Reglamento de la LOPDP (Decreto Ejecutivo 904, RO Sup. 435 de 13 de noviembre de 2023).
- Dos artículos más de la propia UAIS: Fakrudeen (2025) sobre portales universitarios del Golfo y Hermosa-Ramírez (2025) sobre diseño universal como marco conceptual, que es exactamente la fundamentación teórica que el informe echaba en falta.
- Total: 61 entradas, de las cuales 22 son artículos de investigación (antes 13) y 9 son de UAIS o de acceso universal.

Advertencias de verificación que conviene conocer: el número de versión de las Directrices 3/2018 del CEPD no pudo confirmarse en fuente primaria (el PDF oficial devolvió 503) y se omitió; el título del artículo de Libert difiere entre el PDF publicado ("Hidden Web") y los metadatos del editor ("Invisible Web"), y se usó el del PDF.

---

## 9. Lo que queda fuera de esta pasada

Estos puntos exigen medición nueva o los datos por sitio (`resultados.json`), y están escritos en el manuscrito como amenazas a la validez y como trabajo futuro numerado:

1. Auditoría multipunto (Ecuador / UE / EE. UU.) con medidas repetidas y prueba de McNemar. Es el punto que más cambiaría lo que el artículo puede afirmar.
2. Doble codificación del 30 % con κ de Cohen por indicador.
3. Al menos cinco páginas por sitio, incluida una ruta de admisión o matrícula, con el sitio como efecto aleatorio.
4. k ≥ 3 pasadas en días distintos con estadísticos de estabilidad.
5. Métricas de rastreo más robustas que la cookie.
6. Análisis interno del Ecuador por tipo, tamaño y plataforma.
7. Validación humana experta de una submuestra WCAG.
8. Análisis de sensibilidad de la regla de agregación de rankings.
9. Depósito en Zenodo u OSF y sustitución del marcador por el DOI.
