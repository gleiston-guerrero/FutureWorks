PAQUETE PARA UNIVERSAL ACCESS IN THE INFORMATION SOCIETY (Springer)
===================================================================
Dos versiones del manuscrito sobre la plantilla oficial sn-jnl (opcion
sn-basic, referencias NUMERADAS, como usa la revista):

  privacidad_es.tex   -> version en ESPAÑOL  (captions en español)
  privacidad_en.tex   -> version en INGLÉS   (captions en inglés)

Ambas comparten:
  references.bib      -> misma bibliografia (.bib) para las dos versiones
  4 figuras PDF       -> mismas imagenes; el TEXTO INTERNO de los graficos
                         esta en INGLÉS en ambas versiones (mapa_calor_paises,
                         linea_tiempo_leyes, fig_cookies_live, fig_wcag_niveles)
  sn-jnl.cls, sn-basic.bst -> clase y estilo de la plantilla de Springer

COMPILACION (Windows/MikTeX o TeX Live), archivo principal = privacidad_es.tex
o privacidad_en.tex:
  pdflatex privacidad_es
  bibtex   privacidad_es
  pdflatex privacidad_es
  pdflatex privacidad_es
(igual para privacidad_en)

NOTAS
- Referencias: estilo numerado Springer Basic (sn-basic, opcion Numbered),
  que es el que usa UAIS.
- La version en español desactiva los "shorthands" de babel
  (es-noshorthands) para no chocar con la macro \sur de la plantilla.
- Es un unico .tex por version (sin \input), como exige Springer.
