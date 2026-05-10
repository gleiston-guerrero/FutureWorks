# Kiddy Quiz - Proyecto LaTeX completo

Documento académico completo y compilable con los **cuatro capítulos**:

- Capítulo I — Marco contextual del proyecto tecnológico
- Capítulo II — Marco teórico del proyecto tecnológico
- Capítulo III — Metodología (XP, cronograma, indicadores)
- Capítulo IV — Resultados (15 casos de uso + arquitectura + SUS/TAM)

## Compilación rápida

```bash
cd latex/
pdflatex main.tex
pdflatex main.tex   # segunda pasada para TOC e índices
pdflatex main.tex   # tercera pasada para referencias cruzadas
```

Genera `main.pdf` (≈76 páginas con todas las imágenes reales del proyecto).

## Estructura

```
latex/
├── main.tex                      # Documento maestro: portada, preliminares, índices
├── cap1_marco_contextual.tex     # Capítulo I
├── cap2_marco_teorico.tex        # Capítulo II
├── cap3_metodologia.tex          # Capítulo III (con todas las tablas de indicadores)
├── cap4_resultados.tex           # Capítulo IV (auto-generado)
├── gen_casos_uso.py              # Generador del Cap. IV (datos + plantilla LaTeX)
├── README.md                     # Este archivo
└── figuras/                      # 69 archivos: PDFs + PNGs alternos
    ├── fig01_metodologia_xp.pdf  # Ilustración 3.1
    ├── fig02_cronograma.pdf      # Ilustración 3.2
    ├── fig03_casos_uso.pdf       # Ilustración 4.1
    ├── ...
    ├── seq_*.pdf                 # 15 diagramas de secuencia
    └── ui_*.pdf                  # 15+ interfaces de usuario
```

## Patrón aplicado a los 15 casos de uso

Cada caso de uso (Tablas 4.3 a 4.17 en el documento, originalmente 12 a 26)
usa el patrón validado del CU-003:

1. Encabezado con título completo del caso de uso.
2. Fila de **4 columnas**: Código | CU-XXX | Actores | Estudiante/Docente.
3. Filas etiqueta + contenido (4 cm + 11.2 cm) para Objetivo, Resumen,
   Tipo, Dependencias, Precondición, Postcondición, [Importancia].
4. Sección "Flujo normal de eventos" con DOS columnas IGUALES (7.4 cm
   cada una), implementadas como `tabular` interno dentro de `multicolumn`
   para garantizar el ancho equitativo.
5. Patrón escalonado: acción del actor → celda derecha vacía;
   respuesta del sistema → celda izquierda vacía.
6. Paso 1: "Este caso de uso inicia cuando..."
7. Último paso: "Este caso de uso termina cuando..."
8. Flujo alterno + diagrama de secuencia + interfaz de usuario + comentarios.

## Mapeo de figuras a casos de uso

| Tabla | CU      | Caso de uso             | Diagrama de secuencia       | Interfaz de usuario           |
| ----- | ------- | ----------------------- | --------------------------- | ----------------------------- |
| 4.3   | CU-003  | Ver evaluación          | seq_ver_eval                | ui_evaluaciones_estudiante    |
| 4.4   | CU-004  | Resolver evaluación     | seq_resolver_eval           | ui_resolver_eval_pictograma   |
| 4.5   | CU-005  | Ver retroalimentación   | seq_ver_retroalimentacion   | ui_retroalimentacion          |
| 4.6   | CU-006  | Gestionar panel docente | seq_panel_docente           | ui_panel_control_docente      |
| 4.7   | CU-008  | Crear examen            | seq_crear_examen            | ui_crear_examen               |
| 4.8   | CU-009  | Organizar preguntas     | seq_organizar_preguntas     | ui_gestionar_opciones         |
| 4.9   | CU-010  | Configurar contenido    | seq_configurar_contenido    | ui_nueva_pregunta             |
| 4.10  | CU-011  | Adjuntar multimedia     | seq_adjuntar_multimedia     | ui_arasaac_pictogramas        |
| 4.11  | CU-012  | Consultar alumnos       | seq_consultar_alumnos       | ui_listado_estudiantes        |
| 4.12  | CU-013  | Analizar calificaciones | seq_analizar_calificaciones | ui_rendimiento_alertas        |
| 4.13  | CU-014  | Identificar brechas     | seq_identificar_brechas     | ui_rendimiento_alertas        |
| 4.14  | CU-015  | Recibir consejos IA     | seq_recibir_consejos_ia     | ui_comentario_magico_ia       |
| 4.15  | CU-016  | Aplicar gamificación    | seq_aplicar_gamificacion    | ui_mapa_aventuras             |
| 4.16  | CU-017  | Ingresar a clase        | seq_ingresar_clase          | ui_ingresar_codigo            |
| 4.17  | CU-018  | Mapa de competencias    | seq_mapa_competencias       | ui_panel_docente_clases       |

## Modificación posterior

Para editar un caso de uso, abre `gen_casos_uso.py`, edita la lista `CASOS`
(cada CU es un diccionario con `flujo`, `objetivo`, `comentarios`, etc.) y
regenera:

```bash
python3 gen_casos_uso.py
pdflatex main.tex && pdflatex main.tex && pdflatex main.tex
```

Los Capítulos I, II y III son archivos `.tex` directos: edítalos a mano.

## Lo que falta personalizar

- **Portada**: en `main.tex` actualizar el nombre del director.
- **Páginas preliminares**: declaración de autoría, agradecimiento y
  dedicatoria son placeholders editables en `main.tex`.
- **Anexos**: la sección al final está vacía esperando contenido.
- **Bibliografía**: el documento original tenía referencias `[1]–[55]`;
  aquí no se incluyen — agregar `\usepackage{biblatex}` o `thebibliography`
  según preferencia.
