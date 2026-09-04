# Hallazgos de la auditoría en vivo (axe-core 4.13 + cookies), agosto 2026

Auditoría en navegador real (Playwright/Chromium) desde Ecuador, 126 sitios (63 Ecuador + 63 mundo), 126/126 OK.
Fuente de datos: `resultados.json` / `resultados.csv` (recolector `auditar.js`). Análisis: `analisis.py`.

## Accesibilidad (WCAG)
- Sitios sin ningún fallo automático: Mundo 9,5 % (6/63) vs Ecuador 0 % (0/63).
- Alcanzan nivel A (sin fallos A automáticos): Mundo 39,7 % (25/63) vs Ecuador 7,9 % (5/63).
- Mediana de violaciones/sitio: Mundo 2, Ecuador 4.
- Distribución de nodos con fallo por nivel: Mundo A19/AA22/AAA60 %; Ecuador A45/AA29/AAA26 %.
  → El mundo falla en la excelencia (AAA, contraste realzado); Ecuador en el piso (nivel A).
- Regla estrella: enlaces sin nombre (2.4.4, A): Ecuador 81,0 % (51/63) vs Mundo 23,8 % (15/63).
- Contraste (1.4.3, AA): Ecuador 79,4 % vs Mundo 25,4 %. Imágenes sin alt (1.1.1, A): Ecuador 30,2 % vs Mundo 15,9 %.
- Sin atributo lang: Ecuador 0/63; Mundo 6/63 (chinos, McGill).
- Principio más incumplido: perceptible (contraste) en ambos; Ecuador suma déficit operable.

## Privacidad (previo al consentimiento) — CORRIGE la cifra anterior
- Rastreo antes de consentir: Ecuador 63,5 % (40/63) vs Mundo 68,3 % (43/63) → CASI IGUAL, mundo algo mayor.
- La cifra previa del manuscrito (Ecuador 68,3 % vs mundo 19,0 %) NO se reprodujo.
- Motivo: medición desde Ecuador; los sitios del RGPD no muestran banner ni bloquean ante visitante no-UE.
  → "Consentimiento de fachada" es GLOBAL; el RGPD no protege al visitante ecuatoriano.
- ≥1 cookie: EC 87,3 % / Mundo 88,9 %. CMP: EC 22,2 % / Mundo 19,0 %. Banner: EC 23,8 % / Mundo 34,9 %.

## Cruce accesibilidad × privacidad (pregunta del artículo)
- Correlación Spearman (nodos accesibilidad vs cookies de rastreo, N=126): ρ = 0,04 → DESACOPLADAS.
- Ecuador: 3 % logra ambas; 33 % privacidad sin accesibilidad; 59 % ninguna.
- Conclusión: accesibilidad y privacidad son compromisos éticos independientes; ninguna universidad resuelve las dos.

## Decisión tomada
El usuario eligió "adoptar cifras nuevas": el manuscrito (privacidad_mundo.tex) se actualizó con estas cifras,
nueva sección "Conformidad WCAG medida" (Figura 4 fig_wcag_niveles + Cuadro 3 tab:wcag), Figura 3 de cookies
recalculada, abstract/discusión/conclusiones reformulados. 14 págs, compila limpio.
