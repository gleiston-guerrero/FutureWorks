# Validación manual WCAG — estado tras la segunda tanda (corte 24 de agosto de 2026)

Submuestra prevista: 15 sitios × 3 criterios (1.1.1 alt adecuado, 1.4.3 contraste mínimo AA, 2.4.4 nombre de enlace).
Finalidad en el manuscrito: trabajo futuro n.º 7 (validación humana experta de una submuestra WCAG) y n.º 2 (doble codificación con κ de Cohen).
Entregas: 1.ª tanda — Taipe, Fajardo, Beltrán, Mariscal, Cajas, Castro, Zamora. 2.ª tanda — Farinango, Gaibor, Sánchez, Villamarín.
Consolidados: `validacion_manual_wcag_consolidado.xlsx` (lote completo) y `doble_evaluacion_unificada.xlsx` (los 5 sitios de control, con dictamen por celda).

## Veredicto

**Sigue sin ser publicable, pero ya se sabe exactamente por qué y cuánto falta.** 11 de las 15 celdas de la muestra de control quedan firmes tras el dictamen; 4 siguen provisionales.

## 0. Regla de emparejamiento (fijada por el director)

Primera evaluación = hoja «Validación» de la 1.ª tanda, **solo las filas de los 5 ids de control** (7, 14, 83, 95, 96). Segunda evaluación = hoja «Doble evaluación» de la 2.ª tanda. Los solapamientos de reparto de la hoja «Validación» en Northwestern, Manchester y UTPL **no** son doble evaluación y quedan fuera del cálculo. Cuando un sitio tiene evaluadores de sobra en un lado, se generan todos los pares posibles.

Resultado: 3 de los 5 sitios aportan par (UCL con 2 pares, USECIPOL con 2, UNESUM con 1) → **15 juicios pareados**. Berkeley (falta la 2.ª) e IAEN (falta la 1.ª) no aportan ninguno.

## 1. Cobertura: 12 de 15 sitios

- Sin ninguna evaluación: **Cornell (15), UTI (114), ECOTEC (124)**.
- IAEN (96) deja de estar vacío: lo evaluó Villamarín, pero sigue sin par.
- Con dos o más evaluadores: 6 sitios. UCL y USECIPOL tienen **tres** cada uno.
- La hoja «Doble evaluación» la usaron correctamente Farinango, Gaibor y Sánchez; Villamarín la corrigió en su reenvío.

## 2. Fiabilidad: κ = −0,115 → 0,000 solo aclarando el libro de códigos

| Escenario | Coincidencias | po | pe | κ |
|---|---|---|---|---|
| A — códigos tal como se entregaron | 4 / 15 | 0,267 | 0,342 | **−0,115** |
| B — tras aclarar dos reglas | 6 / 15 | 0,400 | 0,400 | **0,000** |

Las dos reglas del escenario B: (i) el `alt` que repite el texto contiguo es redundancia (técnica H2), no ausencia de alternativa, y por tanto **no** es fallo de 1.1.1; (ii) 1.4.3 se juzga con 3:1 en texto grande y 4,5:1 en texto normal, y 1.4.6 no se evalúa. Ninguna exige volver a medir nada.

El desacuerdo que queda ya no es de criterio sino **asimétrico**: un evaluador encuentra fallos que el otro no miró. No se arregla con más evaluadores, sino fijando la lista de elementos a inspeccionar, idéntica para ambos.

## 3. El caso UCL: 4, 5 y 17 fallos para el mismo criterio

Fajardo declaró f=4 en 1.1.1, Gaibor f=5 y Farinango f=17. Abiertas las 27 capturas de los tres, **todas documentan el mismo fenómeno**: tarjetas de noticia y de pódcast cuyo `alt` repite el titular contiguo. La imagen sí tiene alternativa textual. Dictamen: **1** para los tres. Con esa sola regla pasan de discrepar a coincidir.

En 1.4.3 los tres coinciden en f=0; reserva: axe dejó 302 nodos sin decidir y se inspeccionaron 25 (8,3 %). En 2.4.4 solo Fajardo inspeccionó los botones de vídeo *oembed* y halló 2 sin nombre accesible; los otros dos solo aportan capturas de imágenes, así que su f=0 no lo refuta. Dictamen: **P**, pendiente de reponer la captura de Fajardo (archivo de 0 KB).

## 4. El caso USECIPOL: Sánchez acierta en los tres

- **1.4.3**: Beltrán declaró f=0 y Mariscal f=7. Sánchez documenta 2,09 en el titular hero sobre vídeo (umbral 3:1 por texto grande), 1,44 en «Rector» y 1,70 en dos etiquetas «Noticia» (umbral 4,5:1). Único evaluador del lote que aplica los dos umbrales. Dictamen: **P**.
- **2.4.4**: los otros dos buscaron nombres accesibles vacíos, no destinos engañosos. Sánchez halló enlaces de redes que apuntan a `https://www.google.com`. **Verificado contra el sitio en vivo: están ahí, en cabecera y pie.** Dictamen: **P**.
- **1.1.1**: los tres convergen en **P** una vez descontada la redundancia.

## 5. El caso Berkeley: un falso positivo corregido

Taipe es la única evaluadora. Su 1.1.1 = 0 queda **confirmado**: en su captura se ve que las tarjetas de noticia (`div.bg-image-wrap` dentro de `a.wrap-link`) llevan `img` sin atributo `alt`. Su 2.4.4 = P se **corrige a 1**: el único fallo que declaró son dos enlaces «Libraries», uno en el menú Research y otro en el pie, que apuntan al mismo destino; enlaces de igual texto con el mismo propósito **cumplen** 2.4.4. Reserva de método: su ventana estaba a 1280×720 pero con zoom al 75 %, no al 100 %.

## 6. El caso IAEN: los tres códigos confirmados

Villamarín es el único evaluador. Sus tres códigos (0, 0, 0) quedan confirmados:

- **1.1.1**: el logotipo de cabecera carece de `alt`. Confirmado en su captura y contra el sitio en vivo.
- **2.4.4**: tres botones distintos rotulados todos «Haz clic aquí». Contra el sitio en vivo el problema es **mayor** de lo que declaró: «Clic aquí» aparece más de diez veces y «Haz clic aquí» más de cinco, con destinos distintos. Su f=6 sobre n=13 subestima.
- **1.4.3**: su captura muestra el h2 «VIDEOS INSTITUCIONALES» con el token `--e-global-color-primary` `#6EC1E4` sobre blanco → **2,02:1**, que falla incluso el umbral de 3:1 de texto grande. Y el token de texto global `#7A7A7A` sobre blanco da **4,29:1**, por debajo de 4,5:1. Los dos fallos son reales y el segundo afecta al cuerpo de texto de todo el sitio.

Reparo único: midió con **n=6, 6 y 13** en vez de 25 y con la ventana a **1920×1080** en vez de 1280×720. Como el fallo de contraste está en el color de texto global, con n=25 el f subiría y el código 0 se mantendría.

**Corrección de un error del auditor:** en un informe anterior se dijo que `IAEN_1-4-3_01.png` estaba corrupto. No lo estaba. El archivo pesa 876 702 bytes y mi extracción del `.rar` lo cortó en 786 432 bytes (768 KiB exactos, un límite de búfer). Recuperado desde el `.zip` de reenvío, abre sin problema. El fallo fue de la herramienta de extracción, no de la entrega.

## 7. Errores de constructo confirmados en todo el lote

1. **Redundancia de `alt` contada como fallo de 1.1.1** — Fajardo, Gaibor, Farinango y Sánchez. El más extendido y el que más ruido mete en κ.
2. **Confusión 1.4.3 (AA) con 1.4.6 (AAA)** — Taipe en UNESUM: 3,46 en texto grande, con «AA: 3.0 ✓» visible en su propia captura.
3. **Contraste medido contra fondo transparente** — Castro en ULVR: reporta «1:1» sobre `background: rgba(0,0,0,0)` en texto blanco sobre azul oscuro.
4. **Enlaces idénticos con el mismo propósito contados como fallo de 2.4.4** — Taipe en Berkeley.

## 8. Lo que falta para cerrar

1. Emitir las aclaraciones del libro de códigos (§2 y §7.4) y renombrar la columna «1.1.1 alt adecuado» como «1.1.1 alt presente y no engañoso», que es lo que de verdad se mide.
2. Fijar la lista de elementos a inspeccionar por sitio, idéntica para ambos evaluadores, en orden de documento y con los 25 primeros.
3. Cubrir Cornell, UTI y ECOTEC.
4. Conseguir segunda evaluación de UC Berkeley (7) e IAEN (96): sin ellas esos dos sitios no entran en κ.
5. Repetir IAEN con n=25 a 1280×720 (los hallazgos ya están validados; falta solo el tamaño de muestra).
6. Reponer la captura de 2.4.4 de UCL (Fajardo, archivo de 0 KB).
7. Recalcular κ. Mientras no llegue a 0,60 el manuscrito debe seguir declarando la doble codificación como pendiente.
