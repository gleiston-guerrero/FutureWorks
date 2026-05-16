# Proyecto LaTeX dividido

Se dividió `paginas.tex` en archivos parciales, uno por asunto, dentro de:

```text
caps/preliminares/
```

El archivo maestro `caps/preliminares.tex` incluye las páginas preliminares en este orden:

1. Portada
2. Declaración de autoría y cesión de derechos
3. Certificación de culminación
4. Certificado de prevención de coincidencia/plagio
5. Certificado de aprobación por tribunal
6. Agradecimiento
7. Dedicatoria
8. Resumen
9. Abstract

La hoja 10, `10_tabla_contenido_manual.tex`, se conservó separada, pero no se incluye en `main.tex`, porque `main.tex` ya genera automáticamente `\tableofcontents`, `\listoftables` y `\listoffigures`.

Para compilar, mantenga esta estructura:

```text
main.tex
caps/
  preliminares.tex
  preliminares/
    01_portada.tex
    02_declaracion_autoria.tex
    ...
```

Se añadió `\usepackage{ragged2e}` al preámbulo de `main.tex`, porque las páginas extraídas usan `\justifying`.
