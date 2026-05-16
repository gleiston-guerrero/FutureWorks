#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera cap4_resultados.tex con los 15 casos de uso del Capítulo IV
de Kiddy Quiz aplicando el patrón validado del CU-003:

- Cabecera de 4 columnas: Código | CU-XXX | Actores | <Actor>
- Filas etiqueta+contenido: Objetivo, Resumen, Tipo, Dependencias,
  Precondición, Postcondición, [Importancia]
- Sección "Flujo normal de eventos" con 2 columnas IGUALES (7.4 cm
  cada una) implementadas como tabular interno dentro de \multicolumn.
- Paso 1 inicia con: "Este caso de uso inicia cuando..."
- Último paso termina con: "Este caso de uso termina cuando..."
- Flujo alterno
- Diagrama de secuencia (imagen)
- Interfaz de usuario (imagen)
- Comentarios

Layout: ancho útil ≈ 15.2 cm
- Etiqueta: 4 cm
- Contenido (multicolumn 1 columna): 11.2 cm aprox
- Mitad de flujo: 7.4 cm + 7.4 cm
"""

# Cada paso es ('a', texto) -> acción del actor
#                ('s', texto) -> respuesta del sistema

CASOS = [
    # ==================== CU-003 ====================
    {
        "tabla": 12,
        "label": "tab:cu003",
        "titulo": "Ver evaluación",
        "codigo": "CU-003",
        "actores": "Estudiante",
        "objetivo": "Permitir que el estudiante visualice de forma organizada y atractiva las pruebas que su docente ha habilitado para su resolución.",
        "resumen": "Al ingresar al sistema, el estudiante ve una cuadrícula de tarjetas que representan las evaluaciones activas, permitiéndole identificar temas y niveles de dificultad antes de comenzar.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-004 (Desarrollo de evaluación). \textbf{Depende de:} Base de datos de evaluaciones, Asociación estudiante-docente y Filtros por estado.",
        "precondicion": "El estudiante debe estar autenticado y vinculado a un docente; debe existir al menos una evaluación en estado «Habilitada».",
        "postcondicion": "El estudiante visualiza las tarjetas interactivas en pantalla y el sistema queda a la espera de la selección de una prueba.",
        "importancia": "Alta -- Es la interfaz principal de interacción y motivación para el estudiante.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el estudiante inicia sesión exitosamente en la plataforma (CU-001)."),
            ('s', r"El sistema consulta las evaluaciones vinculadas al ID del docente y del estudiante."),
            ('s', r"El sistema filtra únicamente aquellas evaluaciones que tengan el estado «Habilitada»."),
            ('s', r"La aplicación renderiza una cuadrícula de tarjetas con imagen, tema, descripción y dificultad."),
            ('a', r"El estudiante identifica y revisa la información de las tarjetas disponibles."),
            ('a', r"El estudiante selecciona una evaluación haciendo clic en la tarjeta deseada."),
            ('s', r"Este caso de uso termina cuando la aplicación redirige al estudiante a la pantalla de inicio de prueba (CU-004)."),
        ],
        "flujo_alterno": r"\textbf{3.a. Sin evaluaciones disponibles:} si el docente no ha habilitado pruebas, el sistema muestra un mensaje amigable indicando que no hay tareas pendientes. \textbf{4.a. Error de carga multimedia:} si las imágenes de las tarjetas no cargan, el sistema muestra un ícono temático por defecto.",
        "img_seq": "seq_ver_eval.pdf",
        "img_ui":  "ui_evaluaciones_estudiante.pdf",
        "comentarios": r"Las tarjetas deben cumplir con altos estándares de contraste y tamaño de fuente (WCAG 2.1). En Angular se utiliza un \textit{pipe} o filtro para organizar dinámicamente las tarjetas por fecha o dificultad.",
    },
    # ==================== CU-004 ====================
    {
        "tabla": 13,
        "label": "tab:cu004",
        "titulo": "Resolver evaluación",
        "codigo": "CU-004",
        "actores": "Estudiante",
        "objetivo": "Proporcionar un entorno interactivo y amigable para que el estudiante responda las preguntas de una evaluación de forma secuencial.",
        "resumen": "El estudiante accede a la prueba, lee las instrucciones y responde los ítems uno a uno. El sistema permite navegación asistida, control por voz opcional y guarda el progreso automáticamente.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-005 (Presentación de resultados al finalizar la evaluación). \textbf{Depende de:} Motor de evaluación, Base de datos de preguntas y respuestas.",
        "precondicion": "El estudiante debe haber seleccionado una evaluación válida y habilitada desde su panel de inicio (CU-003).",
        "postcondicion": "El sistema captura todas las respuestas y las envía al \\textit{backend} para su cálculo y registro definitivo en la base de datos de desempeño.",
        "importancia": "Muy alta -- Es el núcleo funcional para los estudiantes.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el estudiante selecciona una tarjeta de evaluación (CU-003)."),
            ('s', r"La aplicación muestra una pantalla de «Pre-evaluación» con instrucciones claras."),
            ('a', r"El estudiante hace clic en el botón «Comenzar»."),
            ('s', r"El sistema presenta la primera pregunta con sus respectivas opciones de respuesta."),
            ('a', r"(Opcional) El estudiante activa el control por voz para escuchar el enunciado."),
            ('s', r"El sistema sintetiza el texto y reproduce el audio del ítem actual."),
            ('a', r"El estudiante selecciona una respuesta y hace clic en el botón «Siguiente»."),
            ('s', r"El sistema guarda la respuesta temporalmente y carga el siguiente ítem secuencialmente."),
            ('a', r"El estudiante repite los pasos 7 y 8 hasta completar todos los ítems de la prueba."),
            ('a', r"Al finalizar la última pregunta, el estudiante hace clic en el botón «Finalizar»."),
            ('s', r"Este caso de uso termina cuando el sistema procesa los datos y redirige a la pantalla de resultados (CU-005)."),
        ],
        "flujo_alterno": r"\textbf{4.a. Evaluación con tiempo límite:} el sistema inicia un contador regresivo; si el tiempo se agota, se guarda lo avanzado y se finaliza la prueba automáticamente. \textbf{6.a. Error de reproducción de voz:} si el navegador no soporta el audio, el sistema muestra una alerta sugiriendo continuar con la lectura visual. \textbf{8.a. Desconexión de internet:} el sistema notifica la pérdida de conexión y mantiene las respuestas en caché local hasta que se restablezca el servicio.",
        "img_seq": "seq_resolver_eval.pdf",
        "img_ui":  "ui_resolver_eval_pictograma.pdf",
        "comentarios": r"La interfaz debe ser 100\,\% responsiva y optimizada para dispositivos táctiles. El uso de \texttt{window.localStorage} en Angular asegura que el progreso no se pierda ante cierres accidentales de la pestaña del navegador.",
    },
    # ==================== CU-005 ====================
    {
        "tabla": 14,
        "label": "tab:cu005",
        "titulo": "Ver retroalimentación",
        "codigo": "CU-005",
        "actores": "Estudiante",
        "objetivo": "Mostrar al estudiante una retroalimentación inmediata, motivacional y constructiva al finalizar la evaluación, generada por la IA Gemini.",
        "resumen": "Tras completar una prueba, el sistema envía las respuestas al servicio de IA, que genera mensajes personalizados de refuerzo según los aciertos y errores del estudiante.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Depende de:} Motor de evaluación (CU-004), API de Gemini AI y Base de datos de competencias.",
        "precondicion": "El estudiante debe haber finalizado una evaluación con resultados registrados.",
        "postcondicion": "El estudiante visualiza la retroalimentación y los puntajes obtenidos; la información de progreso queda almacenada para el módulo de seguimiento.",
        "importancia": "Alta -- Refuerza la motivación y la mejora continua del estudiante.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el estudiante finaliza una evaluación (CU-004)."),
            ('s', r"El sistema procesa las respuestas y calcula la calificación global y por competencia."),
            ('s', r"El sistema envía el resumen de desempeño al servicio Gemini AI mediante una petición segura."),
            ('s', r"Gemini AI devuelve un texto motivacional adaptado al perfil de logros y errores."),
            ('s', r"La aplicación muestra una pantalla con la calificación, el detalle por pregunta y el mensaje de refuerzo."),
            ('a', r"El estudiante revisa los aciertos y errores señalados visualmente con colores e íconos."),
            ('a', r"Este caso de uso termina cuando el estudiante presiona «Volver al panel» o cierra la pantalla de retroalimentación."),
        ],
        "flujo_alterno": r"\textbf{3.a. Servicio IA no disponible:} si Gemini AI no responde, el sistema muestra un mensaje genérico de felicitación y registra el error para revisión. \textbf{4.a. Latencia alta:} mientras se espera la respuesta de la IA, el sistema muestra una animación amigable de «Cargando refuerzo».",
        "img_seq": "seq_ver_retroalimentacion.pdf",
        "img_ui":  "ui_retroalimentacion.pdf",
        "comentarios": r"El \textit{prompt} enviado a Gemini debe filtrarse para evitar exposiciones de datos personales del estudiante. Se recomienda cachear las respuestas frecuentes para reducir costos de API.",
    },
    # ==================== CU-006 ====================
    {
        "tabla": 15,
        "label": "tab:cu006",
        "titulo": "Gestionar panel docente",
        "codigo": "CU-006",
        "actores": "Docente",
        "objetivo": "Proporcionar al docente un panel central que centralice el acceso a las herramientas de gestión de clases, evaluaciones y reportes.",
        "resumen": "Al iniciar sesión, el docente accede a un panel con accesos directos a cada módulo, indicadores rápidos y notificaciones del sistema.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-007 (Gestión de clases), CU-008 (Crear examen), CU-012 (Consultar alumnos). \textbf{Depende de:} Servicio de autenticación y Base de datos del docente.",
        "precondicion": "El docente debe estar autenticado con credenciales válidas y rol asignado.",
        "postcondicion": "El docente visualiza el panel principal listo para iniciar cualquier acción de gestión académica.",
        "importancia": "Muy alta -- Es el punto de partida de la experiencia del docente.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente inicia sesión correctamente en la plataforma."),
            ('s', r"El sistema valida el rol del usuario y carga el panel de gestión docente."),
            ('s', r"La aplicación consulta las clases, evaluaciones recientes y métricas del docente."),
            ('s', r"El panel muestra tarjetas con accesos rápidos: «Mis clases», «Crear examen», «Reportes», «Estudiantes»."),
            ('a', r"El docente revisa los indicadores y notificaciones desplegados."),
            ('a', r"El docente selecciona la herramienta o módulo que desea utilizar."),
            ('s', r"Este caso de uso termina cuando el sistema redirige al docente al módulo seleccionado."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sesión expirada:} si el token JWT está vencido, el sistema redirige a la pantalla de inicio de sesión. \textbf{3.a. Sin clases creadas:} el panel muestra un \textit{onboarding} guiado para crear la primera clase.",
        "img_seq": "seq_panel_docente.pdf",
        "img_ui":  "ui_panel_control_docente.pdf",
        "comentarios": r"El panel debe optimizarse con \textit{lazy loading} para que su carga inicial sea inferior a 2 segundos, cumpliendo con el RNF-03.",
    },
    # ==================== CU-008 ====================
    {
        "tabla": 16,
        "label": "tab:cu008",
        "titulo": "Crear examen",
        "codigo": "CU-008",
        "actores": "Docente",
        "objetivo": "Permitir al docente registrar una nueva evaluación con sus datos generales antes de configurar las preguntas.",
        "resumen": "El docente ingresa los datos generales de la prueba en un formulario; el sistema valida la información y crea el registro de la evaluación en la base de datos en estado inactivo o borrador.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-009 (Gestión de preguntas por evaluación). \textbf{Depende de:} Interfaz de gestión docente y Base de datos de evaluaciones.",
        "precondicion": "El docente debe haber iniciado sesión exitosamente, contar con los permisos adecuados y encontrarse en su panel de gestión.",
        "postcondicion": "La nueva evaluación queda registrada en la base de datos vinculada al docente, habilitando la interfaz para comenzar a agregarle preguntas.",
        "importancia": "Muy alta -- Es la funcionalidad base del sistema de evaluación.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente selecciona la opción «Crear nueva evaluación»."),
            ('s', r"El sistema muestra el formulario vacío de creación de evaluación."),
            ('a', r"El docente completa los campos obligatorios: título o tema, nivel de dificultad, descripción y duración (minutos)."),
            ('a', r"El docente hace clic en el botón «Crear evaluación»."),
            ('s', r"El sistema valida que los campos requeridos no estén vacíos y que la duración sea mayor a cero."),
            ('s', r"El sistema registra la nueva evaluación en la base de datos (PostgreSQL)."),
            ('s', r"Este caso de uso termina cuando la aplicación redirige al docente a la interfaz de gestión de preguntas (CU-009)."),
        ],
        "flujo_alterno": r"\textbf{5.a. Campos vacíos:} si el docente deja campos obligatorios vacíos, el sistema resalta los errores en rojo y detiene el proceso de guardado. \textbf{5.b. Duración inválida:} si se ingresa una duración negativa o cero, el sistema solicita ingresar un número válido antes de continuar.",
        "img_seq": "seq_crear_examen.pdf",
        "img_ui":  "ui_crear_examen.pdf",
        "comentarios": r"Se recomienda agregar asistencia visual en la interfaz (textos de ejemplo tenues en los campos vacíos o plantillas prediseñadas) para facilitar la carga de datos al docente.",
    },
    # ==================== CU-009 ====================
    {
        "tabla": 17,
        "label": "tab:cu009",
        "titulo": "Organizar preguntas",
        "codigo": "CU-009",
        "actores": "Docente",
        "objetivo": "Permitir al docente gestionar la lista de preguntas asociadas a una evaluación específica mediante funciones de visualización, edición, eliminación y reordenamiento.",
        "resumen": "El docente accede al administrador de una prueba para ver y modificar las preguntas existentes. El sistema procesa estas acciones (CRUD y ordenamiento) y actualiza la estructura de la evaluación en la base de datos.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-010 (Creación de preguntas). \textbf{Depende de:} Evaluación previamente creada (CU-008) y base de datos de preguntas.",
        "precondicion": "El docente debe haber iniciado sesión y debe haber creado previamente al menos una evaluación.",
        "postcondicion": "La estructura de preguntas de la evaluación queda actualizada según las acciones realizadas por el docente.",
        "importancia": "Alta -- Es esencial para el armado de pruebas significativas.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente accede al administrador de una evaluación específica."),
            ('s', r"El sistema consulta las preguntas asociadas a la evaluación seleccionada."),
            ('s', r"La aplicación despliega la lista ordenada de preguntas con opciones de edición, eliminación y reordenamiento."),
            ('a', r"El docente puede arrastrar para reordenar, editar el contenido o eliminar una pregunta."),
            ('s', r"El sistema actualiza la posición o el contenido en la base de datos."),
            ('a', r"El docente puede invocar la creación de una nueva pregunta (CU-010)."),
            ('s', r"Este caso de uso termina cuando el docente sale del administrador o todas las acciones quedan persistidas correctamente."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sin preguntas:} si no existen preguntas, el sistema invita al docente a crear la primera. \textbf{5.a. Error de guardado:} si la red falla al actualizar el orden, el sistema reintenta automáticamente y avisa al docente.",
        "img_seq": "seq_organizar_preguntas.pdf",
        "img_ui":  "ui_gestionar_opciones.pdf",
        "comentarios": r"El reordenamiento utiliza la librería \textit{Angular CDK Drag\&Drop}. Se persiste un campo \texttt{orden} entero en la tabla de preguntas para mantener la secuencia.",
    },
    # ==================== CU-010 ====================
    {
        "tabla": 18,
        "label": "tab:cu010",
        "titulo": "Configurar contenido",
        "codigo": "CU-010",
        "actores": "Docente",
        "objetivo": "Permitir al docente registrar una nueva pregunta dentro de una evaluación, definiendo su enunciado, opciones, respuesta correcta y configuraciones de visualización.",
        "resumen": "El docente accede al editor de preguntas, completa el formulario con el enunciado y las opciones, marca la respuesta correcta y guarda. El sistema valida y persiste la información.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-011 (Adjuntar archivos multimedia). \textbf{Depende de:} CU-009 (Organizar preguntas) y Base de datos de preguntas.",
        "precondicion": "Debe existir una evaluación seleccionada por el docente y este debe encontrarse en el editor de preguntas.",
        "postcondicion": "La pregunta queda registrada y vinculada a la evaluación, lista para ser presentada al estudiante.",
        "importancia": "Alta -- Define la calidad pedagógica de las pruebas.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente selecciona «Agregar nueva pregunta»."),
            ('s', r"El sistema despliega el editor con campos para enunciado, tipo y opciones."),
            ('a', r"El docente escribe el enunciado y selecciona el tipo de pregunta (opción única, múltiple, verdadero/falso)."),
            ('a', r"El docente añade las opciones de respuesta y marca la(s) correcta(s)."),
            ('a', r"(Opcional) El docente adjunta material multimedia (CU-011)."),
            ('a', r"El docente hace clic en «Guardar»."),
            ('s', r"El sistema valida que existan al menos dos opciones y una respuesta correcta marcada."),
            ('s', r"Este caso de uso termina cuando el sistema persiste la pregunta y la añade al final de la lista de la evaluación."),
        ],
        "flujo_alterno": r"\textbf{7.a. Sin respuesta correcta:} el sistema impide guardar y resalta el campo. \textbf{7.b. Enunciado vacío:} el sistema marca el campo como obligatorio y detiene el guardado.",
        "img_seq": "seq_configurar_contenido.pdf",
        "img_ui":  "ui_nueva_pregunta.pdf",
        "comentarios": r"El editor utiliza un componente \textit{rich text} ligero para permitir formato básico (negritas, listas) sin complicar al docente.",
    },
    # ==================== CU-011 ====================
    {
        "tabla": 19,
        "label": "tab:cu011",
        "titulo": "Adjuntar archivos multimedia",
        "codigo": "CU-011",
        "actores": "Docente",
        "objetivo": "Permitir al docente adjuntar imágenes, audios o videos a una pregunta para enriquecer la experiencia del estudiante.",
        "resumen": "El docente sube un archivo desde su dispositivo; el sistema lo valida, lo almacena en Cloudinary y lo vincula a la pregunta correspondiente.",
        "tipo": "Secundario",
        "dependencias": r"\textbf{Depende de:} CU-010 (Configurar contenido), API de Cloudinary, Base de datos de preguntas.",
        "precondicion": "Debe existir una pregunta en edición y el docente debe contar con permisos de carga.",
        "postcondicion": "El archivo multimedia queda almacenado en Cloudinary y referenciado por URL en la pregunta.",
        "importancia": "Media -- Mejora la calidad pedagógica y la accesibilidad.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente, en el editor de pregunta, selecciona la opción «Adjuntar multimedia»."),
            ('s', r"El sistema abre un cuadro de diálogo de selección de archivo."),
            ('a', r"El docente elige una imagen, audio o video desde su dispositivo."),
            ('s', r"El sistema valida el formato y el tamaño máximo permitido."),
            ('s', r"El sistema sube el archivo a Cloudinary y obtiene la URL pública."),
            ('s', r"La aplicación previsualiza el archivo dentro del editor."),
            ('a', r"El docente confirma el adjunto."),
            ('s', r"Este caso de uso termina cuando el sistema vincula la URL del archivo a la pregunta y guarda la referencia."),
        ],
        "flujo_alterno": r"\textbf{4.a. Formato no permitido:} el sistema notifica al docente y aborta la carga. \textbf{5.a. Error de Cloudinary:} si el servicio externo falla, el sistema muestra un mensaje de reintento.",
        "img_seq": "seq_adjuntar_multimedia.pdf",
        "img_ui":  "ui_arasaac_pictogramas.pdf",
        "comentarios": r"Se aplica un límite de 10\,MB por archivo. Las imágenes se optimizan automáticamente con transformaciones de Cloudinary.",
    },
    # ==================== CU-012 ====================
    {
        "tabla": 20,
        "label": "tab:cu012",
        "titulo": "Consultar alumnos",
        "codigo": "CU-012",
        "actores": "Docente",
        "objetivo": "Permitir al docente consultar el listado completo de estudiantes inscritos en sus clases y revisar su información básica.",
        "resumen": "El docente accede al módulo de estudiantes, visualiza el listado por clase y puede filtrar, buscar y consultar el detalle de cada alumno.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-013 (Analizar calificaciones). \textbf{Depende de:} CU-007 (Gestión de clases) y Base de datos de estudiantes.",
        "precondicion": "El docente debe haber iniciado sesión y tener al menos una clase con estudiantes inscritos.",
        "postcondicion": "El docente visualiza la información actualizada del listado de estudiantes asignados.",
        "importancia": "Alta -- Es la base para la analítica académica.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente selecciona el módulo «Mis estudiantes»."),
            ('s', r"El sistema consulta las clases del docente y los estudiantes asociados."),
            ('s', r"La aplicación muestra una tabla con nombre, código, clase y estado de cada estudiante."),
            ('a', r"El docente puede filtrar por clase o buscar por nombre o código."),
            ('s', r"El sistema actualiza dinámicamente la tabla según los filtros aplicados."),
            ('a', r"El docente selecciona un estudiante para ver el detalle (CU-013)."),
            ('s', r"Este caso de uso termina cuando el sistema redirige a la vista de calificaciones del estudiante seleccionado."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sin estudiantes:} si la clase no tiene inscritos, el sistema sugiere compartir el código de clase para que se unan.",
        "img_seq": "seq_consultar_alumnos.pdf",
        "img_ui":  "ui_listado_estudiantes.pdf",
        "comentarios": r"Se utiliza paginación del lado del servidor para clases con más de 50 estudiantes, mejorando el rendimiento.",
    },
    # ==================== CU-013 ====================
    {
        "tabla": 21,
        "label": "tab:cu013",
        "titulo": "Analizar calificaciones",
        "codigo": "CU-013",
        "actores": "Docente",
        "objetivo": "Permitir al docente revisar las calificaciones obtenidas por los estudiantes en cada evaluación y obtener métricas estadísticas.",
        "resumen": "El docente accede al detalle de calificaciones de un estudiante o grupo, observa estadísticas generales y puede exportar los reportes.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-014 (Identificar brechas) y CU-015 (Recibir consejos IA). \textbf{Depende de:} CU-004 (Resolver evaluación) y Base de datos de resultados.",
        "precondicion": "Deben existir evaluaciones resueltas por al menos un estudiante.",
        "postcondicion": "El docente dispone de información agregada y detallada de las calificaciones para tomar decisiones pedagógicas.",
        "importancia": "Muy alta -- Es la entrada del análisis pedagógico.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente selecciona un estudiante o evaluación desde el módulo de analíticas."),
            ('s', r"El sistema recupera las calificaciones, fechas y porcentajes de aciertos del registro elegido."),
            ('s', r"La aplicación muestra un dashboard con gráficos de barras, promedios y desviaciones."),
            ('a', r"El docente revisa los indicadores y puede filtrar por evaluación, mes o competencia."),
            ('a', r"(Opcional) El docente exporta el reporte en PDF o Excel."),
            ('s', r"El sistema genera y entrega el archivo solicitado."),
            ('s', r"Este caso de uso termina cuando el docente cierra el dashboard o navega a otro módulo."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sin datos:} si el estudiante no ha completado evaluaciones, el sistema muestra un estado vacío con sugerencia de asignar pruebas.",
        "img_seq": "seq_analizar_calificaciones.pdf",
        "img_ui":  "ui_rendimiento_alertas.pdf",
        "comentarios": r"Las gráficas se renderizan con \textit{Chart.js}. Los reportes en PDF se generan con \textit{Puppeteer} en el backend.",
    },
    # ==================== CU-014 ====================
    {
        "tabla": 22,
        "label": "tab:cu014",
        "titulo": "Identificar brechas de aprendizaje",
        "codigo": "CU-014",
        "actores": "Docente",
        "objetivo": "Detectar automáticamente las áreas o competencias en las que los estudiantes presentan dificultades, basándose en los resultados de las evaluaciones.",
        "resumen": "El sistema procesa las respuestas, agrupa los errores por competencia y muestra un mapa visual con las áreas críticas de cada estudiante o grupo.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Depende de:} CU-013 (Analizar calificaciones) y motor de competencias.",
        "precondicion": "Deben existir resultados consolidados de al menos una evaluación por competencia.",
        "postcondicion": "El docente visualiza las áreas con menor dominio para focalizar el refuerzo académico.",
        "importancia": "Alta -- Es clave para la atención diferenciada.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente selecciona la opción «Identificar brechas»."),
            ('s', r"El sistema consulta las evaluaciones del estudiante o clase seleccionada."),
            ('s', r"El sistema agrupa los errores por competencia curricular."),
            ('s', r"La aplicación calcula el porcentaje de dominio por competencia."),
            ('s', r"El sistema muestra un mapa de calor con las áreas críticas y satisfactorias."),
            ('a', r"El docente revisa el mapa e identifica las competencias prioritarias para reforzar."),
            ('s', r"Este caso de uso termina cuando el docente cierra la vista o solicita los consejos de IA (CU-015)."),
        ],
        "flujo_alterno": r"\textbf{2.a. Datos insuficientes:} si la muestra es menor a tres evaluaciones, el sistema advierte que los resultados son indicativos.",
        "img_seq": "seq_identificar_brechas.pdf",
        "img_ui":  "ui_rendimiento_alertas.pdf",
        "comentarios": r"Se utiliza una escala cromática verde-amarillo-rojo para facilitar la lectura visual rápida del docente.",
    },
    # ==================== CU-015 ====================
    {
        "tabla": 23,
        "label": "tab:cu015",
        "titulo": "Recibir consejos IA",
        "codigo": "CU-015",
        "actores": "Docente",
        "objetivo": "Generar recomendaciones pedagógicas automáticas mediante Gemini AI, basadas en las brechas detectadas en los estudiantes.",
        "resumen": "El docente solicita un análisis con IA; el sistema envía el contexto a Gemini, que devuelve sugerencias didácticas y de refuerzo personalizadas.",
        "tipo": "Secundario",
        "dependencias": r"\textbf{Depende de:} CU-014 (Identificar brechas) y API de Gemini AI.",
        "precondicion": "Debe existir un análisis de brechas calculado previamente.",
        "postcondicion": "El docente recibe sugerencias prácticas para aplicar en clase y reforzar competencias.",
        "importancia": "Media -- Es un valor añadido del sistema.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el docente, dentro del análisis de brechas, hace clic en «Recibir consejos IA»."),
            ('s', r"El sistema construye un \textit{prompt} contextualizado con los datos de las brechas detectadas."),
            ('s', r"El sistema envía la petición segura a la API de Gemini."),
            ('s', r"Gemini AI devuelve un listado de recomendaciones pedagógicas adaptadas al perfil del grupo."),
            ('s', r"La aplicación muestra las sugerencias en formato de tarjetas claras y accionables."),
            ('a', r"El docente revisa las recomendaciones y puede copiarlas o exportarlas."),
            ('s', r"Este caso de uso termina cuando el docente cierra la vista de consejos."),
        ],
        "flujo_alterno": r"\textbf{3.a. Servicio IA no disponible:} si Gemini falla, el sistema muestra recomendaciones generales basadas en una base local de buenas prácticas.",
        "img_seq": "seq_recibir_consejos_ia.pdf",
        "img_ui":  "ui_comentario_magico_ia.pdf",
        "comentarios": r"Las consultas a Gemini se cachean por 24 horas para reducir costos y mejorar tiempos de respuesta.",
    },
    # ==================== CU-016 ====================
    {
        "tabla": 24,
        "label": "tab:cu016",
        "titulo": "Aplicar gamificación",
        "codigo": "CU-016",
        "actores": "Estudiante",
        "objetivo": "Motivar al estudiante mediante elementos lúdicos como insignias, niveles, puntajes y rankings que recompensan su progreso.",
        "resumen": "El sistema otorga puntos y reconocimientos al estudiante al completar evaluaciones, alcanzar metas o superar competencias específicas.",
        "tipo": "Secundario",
        "dependencias": r"\textbf{Depende de:} CU-004 (Resolver evaluación) y Base de datos de progreso.",
        "precondicion": "El estudiante debe haber completado al menos una evaluación o desafío.",
        "postcondicion": "El estudiante recibe la recompensa correspondiente y observa su avance en el panel de logros.",
        "importancia": "Media -- Refuerza la motivación y la constancia del estudiante.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el estudiante completa una evaluación o supera una competencia."),
            ('s', r"El sistema verifica las reglas de gamificación aplicables (puntos, insignias, niveles)."),
            ('s', r"El sistema calcula los nuevos puntajes y reconocimientos otorgados."),
            ('s', r"La aplicación despliega una animación celebratoria con la insignia o nivel obtenido."),
            ('a', r"El estudiante revisa su perfil y observa los logros desbloqueados."),
            ('s', r"Este caso de uso termina cuando el estudiante cierra el panel de gamificación o continúa navegando."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sin nuevos logros:} si el desempeño no alcanza los umbrales, el sistema muestra mensajes motivacionales sin otorgar insignias.",
        "img_seq": "seq_aplicar_gamificacion.pdf",
        "img_ui":  "ui_mapa_aventuras.pdf",
        "comentarios": r"Las insignias se generan en SVG y se animan con \textit{Lottie} para una experiencia atractiva sin penalizar el rendimiento.",
    },
    # ==================== CU-017 ====================
    {
        "tabla": 25,
        "label": "tab:cu017",
        "titulo": "Ingresar a clase",
        "codigo": "CU-017",
        "actores": "Estudiante",
        "objetivo": "Permitir al estudiante unirse a una clase del docente mediante un código único de acceso.",
        "resumen": "El estudiante introduce el código compartido por el docente; el sistema valida y lo inscribe automáticamente en la clase, dándole acceso a sus evaluaciones.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Depende de:} CU-007 (Gestión de clases) y Base de datos de inscripciones.",
        "precondicion": "El estudiante debe estar autenticado y disponer de un código de clase válido.",
        "postcondicion": "El estudiante queda inscrito en la clase y la visualiza en su panel principal.",
        "importancia": "Alta -- Es el punto de acceso del estudiante al ecosistema del docente.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el estudiante selecciona la opción «Unirse a una clase»."),
            ('s', r"El sistema muestra un campo para ingresar el código de la clase."),
            ('a', r"El estudiante introduce el código proporcionado por el docente y confirma."),
            ('s', r"El sistema valida la existencia del código y verifica que no haya inscripción previa."),
            ('s', r"El sistema registra al estudiante en la clase correspondiente."),
            ('s', r"La aplicación muestra una confirmación con el nombre de la clase."),
            ('a', r"El estudiante hace clic en «Continuar»."),
            ('s', r"Este caso de uso termina cuando el sistema redirige al panel de clases del estudiante con la nueva clase visible."),
        ],
        "flujo_alterno": r"\textbf{4.a. Código inválido:} el sistema muestra un mensaje de error y permite reintentar. \textbf{4.b. Inscripción duplicada:} el sistema avisa que ya está inscrito y lo redirige al panel.",
        "img_seq": "seq_ingresar_clase.pdf",
        "img_ui":  "ui_ingresar_codigo.pdf",
        "comentarios": r"Los códigos de clase son alfanuméricos de 6 caracteres, generados con baja probabilidad de colisión. Se desactivan tras 30 días de inactividad.",
    },
    # ==================== CU-018 ====================
    {
        "tabla": 26,
        "label": "tab:cu018",
        "titulo": "Ver mapa de competencias",
        "codigo": "CU-018",
        "actores": "Estudiante / Docente",
        "objetivo": "Presentar de forma visual el estado de las competencias curriculares evaluadas, indicando cuáles están logradas, en proceso o no iniciadas.",
        "resumen": "El usuario consulta su mapa de competencias; el sistema procesa el historial de evaluaciones y muestra una matriz visual con el estado de cada competencia, exportable en PDF o Excel.",
        "tipo": "Principal",
        "dependencias": r"\textbf{Invoca a:} CU-015 (Exportación de resultados) para la generación del PDF. \textbf{Depende de:} Motor de resultados y Base de datos de competencias curriculares.",
        "precondicion": "El estudiante debe haber completado evaluaciones que tengan competencias curriculares vinculadas. El usuario debe estar autenticado.",
        "postcondicion": "El sistema despliega una lista de competencias por módulo y nivel, indicando el estado de cada una mediante una visualización gráfica. Se habilita la opción de exportar el mapa.",
        "importancia": "Alta -- Refuerza el enfoque por competencias y la toma de decisiones pedagógicas.",
        "flujo": [
            ('a', r"Este caso de uso inicia cuando el usuario (docente o estudiante) consulta el progreso académico en la plataforma."),
            ('s', r"El sistema recupera el historial de evaluaciones del alumno y consulta la base de datos de competencias curriculares."),
            ('s', r"El sistema calcula el estado actual de cada competencia evaluada."),
            ('s', r"El sistema despliega una lista de competencias organizadas por módulo y nivel."),
            ('s', r"La aplicación indica visualmente si la competencia está lograda, en proceso o no iniciada mediante cuadros, íconos y colores."),
            ('a', r"El usuario selecciona la opción para exportar el mapa de competencias."),
            ('s', r"Este caso de uso termina cuando el sistema invoca el módulo de exportación (CU-015) y genera el archivo en formato PDF o Excel."),
        ],
        "flujo_alterno": r"\textbf{2.a. Sin datos previos:} si el estudiante no ha realizado ninguna evaluación con competencias vinculadas, el mapa muestra todas las áreas en estado «no iniciada» y sugiere realizar una prueba diagnóstica.",
        "img_seq": "seq_mapa_competencias.pdf",
        "img_ui":  "ui_panel_docente_clases.pdf",
        "comentarios": r"El mapa debe actualizarse en tiempo real tras cada evaluación. Puede usarse como herramienta de comunicación directa con padres o representantes.",
    },
]


def gen_cu_table(cu):
    """Genera el LaTeX de una tabla CU completa con el patrón de 4 columnas iguales en flujo."""
    L = []
    L.append(r"% =====================================================")
    L.append(r"% Tabla {n}: CU {codigo} - {titulo}".format(n=cu['tabla'], codigo=cu['codigo'], titulo=cu['titulo']))
    L.append(r"% =====================================================")
    L.append(r"\begingroup")
    L.append(r"\setlength{\LTpre}{6pt}\setlength{\LTpost}{6pt}")
    L.append(r"\renewcommand{\arraystretch}{1.20}")
    L.append(r"\footnotesize")
    L.append(r"\begin{longtable}{|p{4cm}|p{11.2cm}|}")
    # Caption + label
    L.append(r"\caption{{Caso de uso ``{0}''.}}\label{{{1}}}\\".format(cu['titulo'], cu['label']))
    L.append(r"\hline")
    L.append(r"\rowcolor{{headblue}}\multicolumn{{2}}{{|c|}}{{\textbf{{Caso de uso ``{0}''}}}} \\\hline".format(cu['titulo']))
    L.append(r"\endfirsthead")
    L.append(r"\hline\rowcolor{{headblue}}\multicolumn{{2}}{{|c|}}{{\textbf{{Caso de uso ``{0}'' (continuación)}}}} \\\hline".format(cu['titulo']))
    L.append(r"\endhead")
    L.append(r"\hline\multicolumn{2}{r}{\footnotesize\itshape continúa $\rightarrow$}\\")
    L.append(r"\endfoot")
    L.append(r"\hline")
    L.append(r"\endlastfoot")
    # Cabecera Código + Actores en 4 columnas
    L.append(r"\textbf{{Código:}} {0} & \textbf{{Actores:}} {1} \\\hline".format(cu['codigo'], cu['actores']))
    L.append(r"\textbf{{Objetivo:}}        & {0} \\\hline".format(cu['objetivo']))
    L.append(r"\textbf{{Resumen:}}         & {0} \\\hline".format(cu['resumen']))
    L.append(r"\textbf{{Tipo:}}            & {0} \\\hline".format(cu['tipo']))
    L.append(r"\textbf{{Dependencias:}}    & {0} \\\hline".format(cu['dependencias']))
    L.append(r"\textbf{{Precondición:}}    & {0} \\\hline".format(cu['precondicion']))
    L.append(r"\textbf{{Postcondición:}}   & {0} \\\hline".format(cu['postcondicion']))
    L.append(r"\textbf{{[Importancia]}}    & {0} \\\hline".format(cu['importancia']))

    # Cabecera del flujo
    L.append(r"\multicolumn{2}{|c|}{\cellcolor{grpgray}\textbf{Flujo normal de eventos}} \\\hline")

    # Sub-cabezado con 2 columnas IGUALES (7.4cm + 7.4cm)
    L.append(r"\multicolumn{2}{|p{15.2cm}|}{%")
    L.append(r"  \begin{tabular}{|p{7.4cm}|p{7.4cm}|}")
    L.append(r"    \hline")
    L.append(r"    \cellcolor{grpgray}\centering\textbf{Acción del actor} & \cellcolor{grpgray}\centering\textbf{Respuesta del sistema} \tabularnewline\hline")
    # Pasos numerados con escalonamiento
    for idx, (tipo, texto) in enumerate(cu['flujo'], start=1):
        if tipo == 'a':
            L.append(r"    {0}.~{1} & \tabularnewline\hline".format(idx, texto))
        else:
            L.append(r"     & {0}.~{1} \tabularnewline\hline".format(idx, texto))
    L.append(r"  \end{tabular}%")
    L.append(r"} \\\hline")

    # Flujo alterno
    L.append(r"\textbf{{Flujo alterno}} & {0} \\\hline".format(cu['flujo_alterno']))
    # Diagrama de secuencia (imagen)
    L.append(r"\textbf{Diagrama de secuencia} &")
    L.append(r"  \begin{{center}}\includegraphics[width=0.95\linewidth,keepaspectratio]{{{0}}}\end{{center}} \\\hline".format(cu['img_seq']))
    # Interfaz de usuario
    L.append(r"\textbf{Interfaz de usuario} &")
    L.append(r"  \begin{{center}}\includegraphics[width=0.95\linewidth,keepaspectratio]{{{0}}}\end{{center}} \\\hline".format(cu['img_ui']))
    # Comentarios
    L.append(r"\textbf{{Comentarios:}} & {0} \\\hline".format(cu['comentarios']))
    L.append(r"\end{longtable}")
    L.append(r"\noindent\textbf{Elaboración:} \textit{Autor}")
    L.append(r"\endgroup")
    L.append(r"\bigskip")
    L.append(r"")
    return "\n".join(L)


def main():
    out = []
    out.append(r"% =============================================================")
    out.append(r"% CAPÍTULO IV - RESULTADOS")
    out.append(r"% Auto-generado: cap4_resultados.tex")
    out.append(r"% =============================================================")
    out.append(r"")
    out.append(r"\section{Producto tecnológico desarrollado}")
    out.append(r"")
    out.append(r"\subsection{Obtención de requisitos}")
    out.append(r"Luego de realizar las entrevistas y el trabajo de validación continua con el docente especialista para conocer sus opiniones, necesidades operativas y experiencias en la evaluación por competencias, y una vez analizada toda la información recopilada, se definió el alcance del sistema. Esta información fue complementada con los lineamientos pedagógicos extraídos de la revisión bibliográfica para asegurar un enfoque adecuado hacia los estudiantes de educación básica.")
    out.append(r"")
    out.append(r"Dado que el desarrollo se rigió bajo la metodología ágil de Programación Extrema (XP), la lista de requerimientos del sistema no se estructuró de forma tradicional, sino que se documentó directamente a través de Historias de Usuario. A continuación, en la Tabla~\ref{tab:hu} se muestra el listado consolidado de las historias de usuario que conforman el núcleo funcional de la aplicación.")
    out.append(r"")
    # Tabla 10 — Historias de usuario
    out.append(r"\begin{small}")
    out.append(r"\begin{longtable}{|>{\bfseries}p{2.1cm}|p{3.2cm}|p{1.7cm}|p{4cm}|p{3.5cm}|}")
    out.append(r"\caption{Historias de usuario de la aplicación web Kiddy Quiz.}\label{tab:hu}\\")
    out.append(r"\hline\rowcolor{headblue}\multicolumn{5}{|c|}{\textbf{Aplicación web Kiddy Quiz}}\\\hline")
    out.append(r"\rowcolor{grpgray}\textbf{ID} & \textbf{Título} & \textbf{Como} & \textbf{Quiero (Acción)} & \textbf{Para (Beneficio)}\\\hline")
    out.append(r"\endfirsthead")
    out.append(r"\hline\rowcolor{headblue}\multicolumn{5}{|c|}{\textbf{Aplicación web Kiddy Quiz (continuación)}}\\\hline")
    out.append(r"\rowcolor{grpgray}\textbf{ID} & \textbf{Título} & \textbf{Como} & \textbf{Quiero (Acción)} & \textbf{Para (Beneficio)}\\\hline")
    out.append(r"\endhead")
    out.append(r"\hline\endlastfoot")
    hus = [
        ("HU-001.1-F", "Inicio de sesión y redirección", "Usuario", "Iniciar sesión con correo o usuario y contraseña.", "Acceder al panel correspondiente según perfil."),
        ("HU-001.2-F", "Cierre de sesión seguro", "Usuario", "Cerrar sesión activa mediante un botón.", "Proteger la información personal."),
        ("HU-002.1-F", "Registro unificado", "Docente", "Crear una cuenta eligiendo rol (Docente/Estudiante).", "Acceder sin necesidad de usar correo."),
        ("HU-002.2-F", "Creación manual de alumnos", "Docente", "Crear cuentas directamente para mis alumnos.", "Facilitar el acceso y la vinculación automática."),
        ("HU-003.1-F", "Panel de tarjetas (Estudiante)", "Estudiante", "Ver evaluaciones asignadas en tarjetas visuales.", "Identificar rápidamente tema y dificultad."),
        ("HU-004.1-F", "Ejecución de evaluación", "Estudiante", "Responder preguntas de forma secuencial.", "Completar la prueba en un entorno amigable."),
        ("HU-004.2-F", "Soporte de control por voz", "Estudiante", "Activar funciones de voz en la evaluación.", "Interactuar de forma sencilla y autónoma."),
        ("HU-005.1-F", "Feedback motivacional", "Estudiante", "Ver puntaje, tiempo y gráfico con mensaje de ánimo.", "Sentirse motivado a mejorar."),
        ("HU-006.1-F", "Panel de gestión (Docente)", "Docente", "Ver mis evaluaciones creadas en tarjetas.", "Gestionar contenido y ver visibilidad rápido."),
        ("HU-006.2-F", "Habilitación rápida (Toggle)", "Docente", "Activar o desactivar pruebas con un interruptor.", "Controlar el acceso de los alumnos al examen."),
        ("HU-006.3-F", "Estructura base de evaluación", "Docente", "Definir tema, descripción, dificultad y duración.", "Establecer la configuración antes de las preguntas."),
        ("HU-06.4-F",  "Modo lúdico (Gamificado)", "Estudiante", "Realizar evaluaciones en formato de juego.", "Aprender divirtiéndose con recompensas."),
        ("HU-06.5-F",  "Programación temporal", "Docente", "Definir fechas de inicio y fin para las pruebas.", "Planificar el calendario académico."),
        ("HU-06.6-F",  "Control de versiones", "Docente", "Mantener un historial de modificaciones.", "Restaurar versiones en caso de errores."),
        ("HU-06.7-F",  "Evaluaciones diagnósticas", "Docente", "Marcar pruebas como ``diagnósticas'' iniciales.", "Conocer el nivel previo sin afectar el promedio."),
        ("HU-007.1-F", "Gestión CRUD de preguntas", "Docente", "Editar, eliminar y reordenar preguntas (Drag\\&Drop).", "Estructurar el contenido pedagógico de la prueba."),
        ("HU-07.2-F",  "Creación de preguntas", "Docente", "Especificar enunciado, formato y respuestas.", "Asegurar que el sistema califique automáticamente."),
        ("HU-07.3-F",  "Carga multimedia", "Docente", "Integrar imágenes, GIFs o videos en preguntas.", "Brindar apoyo visual a los estudiantes."),
        ("HU-07.4-F",  "Preguntas interactivas", "Docente", "Configurar formatos como unir columnas o secuencias.", "Promover el pensamiento activo en el niño."),
        ("HU-08.1-F",  "Lista de alumnos filtrable", "Docente", "Ver lista de alumnos por curso y buscador.", "Llevar un seguimiento del estado de los alumnos."),
        ("HU-08.2-F",  "Panel de resultados detallados", "Docente", "Ver promedio global y desglose por evaluación.", "Evaluar el progreso individual de manera precisa."),
        ("HU-08.3-F",  "Curva de mejora gráfica", "Docente", "Ver gráfica de líneas cronológica de puntajes.", "Identificar tendencias de aprendizaje del niño."),
        ("HU-08.4-F",  "Exportación a Excel", "Docente", "Descargar archivo .xlsx de rendimiento.", "Mantener respaldos o reportes administrativos."),
        ("HU-08.5-F",  "Áreas fuertes y débiles", "Docente", "Ver análisis por categorías temáticas.", "Planificar refuerzos pedagógicos precisos."),
        ("HU-09.1-F",  "Sugerencias con IA", "Usuario", "Recibir sugerencias basadas en patrones de error.", "Saber qué temas y competencias reforzar."),
        ("HU-010.1-F", "Modo de lectura accesible", "Estudiante", "Que el sistema lea enunciados y opciones (TTS).", "Ser autónomo sin depender solo de la lectura."),
        ("HU-011.1-F", "Ayudas contextuales", "Estudiante", "Acceder a pistas o definiciones junto a la pregunta.", "Comprender lenguaje abstracto o símbolos."),
        ("HU-012.1-F", "Alertas de bajo rendimiento", "Docente", "Recibir notificaciones por notas bajo el umbral.", "Intervenir pedagógicamente a tiempo."),
        ("HU-013.1-F", "Mapa de competencias", "Usuario", "Ver mapa visual de competencias alcanzadas.", "Tener seguimiento claro del progreso académico."),
        ("HU-014.1-F", "Ejercicios personalizados", "Estudiante", "Recibir ejercicios según resultados anteriores.", "Reforzar áreas específicas individualmente."),
    ]
    for (hid, titulo, como, quiero, para) in hus:
        out.append(r"{0} & {1} & {2} & {3} & {4} \\\hline".format(hid, titulo, como, quiero, para))
    out.append(r"\end{longtable}")
    out.append(r"\end{small}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"En la Tabla~\ref{tab:rnf} se puede visualizar el listado de requerimientos no funcionales que se obtuvo mediante revisión bibliográfica y las entrevistas.")
    out.append(r"")
    # Tabla 11 — RNF
    out.append(r"\begin{table}[H]\centering")
    out.append(r"\caption{Requerimientos no funcionales de la aplicación web Kiddy Quiz.}\label{tab:rnf}")
    out.append(r"\footnotesize\renewcommand{\arraystretch}{1.2}")
    out.append(r"\begin{tabularx}{\textwidth}{|>{\bfseries}p{1.5cm}|p{4.2cm}|X|p{1.5cm}|}")
    out.append(r"\hline\rowcolor{headblue}\textbf{ID} & \textbf{Nombre del requerimiento} & \textbf{Descripción técnica} & \textbf{Prioridad}\\\hline")
    rnfs = [
        ("RNF-01", "Interfaz accesible e intuitiva", "Uso de lenguaje simple, botones grandes y cumplimiento con la norma WCAG 2.1 nivel AA para inclusión.", "Alta"),
        ("RNF-02", "Seguridad y protección de datos", "Cifrado de contraseñas, protección contra ataques (XSS, SQL Injection) y cumplimiento de GDPR.", "Crítica"),
        ("RNF-03", "Rendimiento y concurrencia", "Tiempo de respuesta < 2 segundos y soporte para al menos 200 usuarios concurrentes simultáneos.", "Media"),
        ("RNF-04", "Mantenibilidad del sistema", "Código modular, separación de lógica (NestJS) y presentación (Angular) con control de versiones Git.", "Media"),
        ("RNF-05", "Escalabilidad del sistema", "Arquitectura desacoplada preparada para añadir nodos y uso potencial de Docker/Kubernetes.", "Media"),
        ("RNF-06", "Usabilidad para docentes", "Panel con accesos rápidos y creación de evaluaciones mediante pasos guiados.", "Alta"),
    ]
    for (rid, nombre, desc, prio) in rnfs:
        out.append(r"{0} & {1} & {2} & {3} \\\hline".format(rid, nombre, desc, prio))
    out.append(r"\end{tabularx}\end{table}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Diagrama de casos de uso}")
    out.append(r"")
    out.append(r"En la Ilustración \ref{fig:cu} se puede visualizar el diagrama de casos de uso que contempla las funcionalidades centrales del sistema, representando el ``núcleo'' operativo de la aplicación web Kiddy Quiz. Este esquema refleja las interacciones principales entre la plataforma y los actores involucrados, los cuales corresponden al estudiante y al docente, quienes ejecutan acciones fundamentales para el desarrollo de la evaluación por competencias.")
    out.append(r"")
    out.append(r"El estudiante interactúa con la aplicación principalmente para visualizar las clases a las que pertenece, unirse a nuevas clases mediante un código de acceso, y desarrollar las evaluaciones estructuradas por el docente. Por su parte, el docente utiliza el sistema para crear y gestionar clases, administrar el listado de estudiantes y emplear un editor completo para la creación de evaluaciones.")
    out.append(r"")
    out.append(r"\begin{figure}[H]")
    out.append(r"  \centering")
    out.append(r"  \includegraphics[width=0.9\textwidth]{fig03_casos_uso.pdf}")
    out.append(r"  \caption{Diagrama de casos de uso.}")
    out.append(r"  \label{fig:cu}")
    out.append(r"\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Descripción de los casos de uso extendidos}")
    out.append(r"")
    out.append(r"En el siguiente apartado se especifican los casos de uso derivados de la Ilustración~\ref{fig:cu}. Para ello, se han seleccionado las interacciones más significativas del sistema, haciendo especial énfasis en las funcionalidades relacionadas con la evaluación de las competencias.")
    out.append(r"")
    # Generar las 15 tablas
    for cu in CASOS:
        out.append(gen_cu_table(cu))
    out.append(r"")
    # Continuar con resto del Capítulo IV
    out.append(r"\subsection{Diagrama de arquitectura}")
    out.append(r"")
    out.append(r"En la Ilustración~\ref{fig:arq} se expone la arquitectura implementada en la aplicación web. Para su desarrollo, se adoptó un modelo cliente-servidor con el propósito de establecer una clara separación de responsabilidades entre la interfaz de usuario (Frontend) y la lógica del sistema (Backend).")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.9\textwidth]{fig04_arquitectura.pdf}\caption{Diagrama de arquitectura de Kiddy Quiz.}\label{fig:arq}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"El Frontend, desarrollado mediante Angular, gestiona la interacción directa con los usuarios finales (estudiantes y docentes) y controla la presentación de las interfaces gráficas. El Backend, implementado con NestJS, centraliza la lógica de negocio, la gestión de datos y los protocolos de seguridad. A nivel de persistencia, el sistema emplea PostgreSQL. Adicionalmente, la arquitectura se complementa con Gemini IA, utilizado para la generación de retroalimentación académica automatizada, y Cloudinary, empleado para el almacenamiento de los recursos multimedia.")
    out.append(r"")
    out.append(r"\subsection{Diagrama de base de datos}")
    out.append(r"")
    out.append(r"En la Ilustración~\ref{fig:bd} se presenta el modelo físico de la base de datos, estructurado bajo un enfoque relacional. Cada tabla representa una entidad específica del sistema Kiddy Quiz, y sus relaciones se encuentran claramente definidas mediante llaves foráneas, lo cual garantiza la integridad referencial y una correcta normalización de los datos.")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.9\textwidth]{fig05_base_datos.pdf}\caption{Diagrama de base de datos de Kiddy Quiz.}\label{fig:bd}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Diseño del prototipo}")
    out.append(r"")
    out.append(r"En este apartado se exponen los resultados correspondientes a la fase de diseño visual del sistema. Cabe destacar que, en congruencia con la metodología de Programación Extrema (XP), el diseño no fue estático.")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig06_prototipo_final.pdf}\caption{Prototipo final de la aplicación web Kiddy Quiz.}\label{fig:proto}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig07_modulo_estudiante_eval.pdf}\caption{Módulo de estudiantes -- Evaluación (Kiddy Quiz).}\label{fig:est}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig08_modulo_estudiante_retro.pdf}\caption{Módulo de estudiantes -- Retroalimentación (Kiddy Quiz).}\label{fig:doc}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Integración de Gemini AI}")
    out.append(r"")
    out.append(r"El proyecto Kiddy Quiz integra Gemini AI para generar retroalimentación motivacional automatizada tras cada evaluación. La Ilustración~\ref{fig:gemini} muestra un extracto de la integración mediante la API de Google.")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig09_gemini_ai.pdf}\caption{Extracto de integración de Gemini AI en Kiddy Quiz.}\label{fig:gemini}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Seguridad y autenticación}")
    out.append(r"")
    out.append(r"Para garantizar la protección de los datos y el correcto control de roles, se implementaron medidas de seguridad mediante autenticación con tokens JWT. La Ilustración~\ref{fig:jwt} muestra el flujo de autenticación implementado.")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.9\textwidth]{fig10_jwt.pdf}\caption{Flujo de autenticación por JWT en Kiddy Quiz.}\label{fig:jwt}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\section{Comprobación}")
    out.append(r"")
    out.append(r"\subsection{Cumplimiento de plazos}")
    out.append(r"")
    out.append(r"En la Ilustración~\ref{fig:plazos} se observa el cumplimiento de plazos del proyecto Kiddy Quiz, donde se constata que el 90\,\% de las actividades planificadas fueron completadas dentro de los plazos ajustados.")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig11_cumplimiento_plazos.pdf}\caption{Cumplimiento de plazos Kiddy Quiz.}\label{fig:plazos}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsection{Nivel de aceptación de usuario}")
    out.append(r"")
    out.append(r"\subsubsection*{Resultados de las evaluaciones de usabilidad (SUS)}")
    out.append(r"")
    out.append(r"Las preguntas estructuradas para detectar barreras de usabilidad --tales como la complejidad innecesaria, la inconsistencia del sistema o la necesidad de soporte técnico externo-- registraron puntuaciones mínimas. Este comportamiento ratifica que la curva de aprendizaje de Kiddy Quiz es sumamente reducida.")
    out.append(r"")
    # Tabla 27 SUS
    out.append(r"\begin{table}[H]\centering")
    out.append(r"\caption{Resultado del cuestionario SUS - Kiddy Quiz.}\label{tab:sus}")
    out.append(r"\footnotesize\renewcommand{\arraystretch}{1.25}")
    out.append(r"\begin{tabularx}{\textwidth}{|>{\bfseries}X|c|c|}")
    out.append(r"\hline\rowcolor{headblue}\textbf{Métrica estadística} & \textbf{Estudiantes} & \textbf{Docentes} \\\hline")
    out.append(r"Media               & 87.7 & 81.0 \\\hline")
    out.append(r"Mediana             & 87.5 & 82.5 \\\hline")
    out.append(r"Desviación estándar & 7.8  & 9.4  \\\hline")
    out.append(r"Valor mínimo        & 80.0 & 67.5 \\\hline")
    out.append(r"Valor máximo        & 95.0 & 95.0 \\\hline")
    out.append(r"\end{tabularx}\end{table}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.7\textwidth]{fig12_grafico_sus.pdf}\caption{Gráfico de barras SUS.}\label{fig:sus}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\subsubsection*{Resultados del Modelo de Aceptación Tecnológica (TAM)}")
    out.append(r"")
    out.append(r"Para complementar la evaluación de usabilidad, se aplicó el Modelo de Aceptación Tecnológica (TAM) con el objetivo de medir empíricamente la viabilidad pedagógica y el nivel de adopción de la plataforma Kiddy Quiz. Este instrumento evalúa tres dimensiones fundamentales: la Utilidad Percibida (PU), la Facilidad de Uso Percibida (PEOU) y la Intención de Uso (IU), valoradas mediante una escala de Likert de 1 a 5.")
    out.append(r"")
    out.append(r"El análisis revela una aceptación excepcional de la herramienta, destacando una tendencia muy positiva por parte del grupo de estudiantes de educación básica elemental. Los niños perciben una mayor facilidad al navegar por la plataforma (media de 4.78) en comparación con los docentes (media de 3.95). El hallazgo más significativo recae en la dimensión de Intención de Uso (IU): el grupo de estudiantes registró una media de 4.93 y una mediana perfecta de 5.0, demostrando un nivel de motivación intrínseca sobresaliente.")
    out.append(r"")
    # Tabla 28 TAM
    out.append(r"\begin{table}[H]\centering")
    out.append(r"\caption{Resultados del cuestionario TAM - Kiddy Quiz.}\label{tab:tam}")
    out.append(r"\footnotesize\renewcommand{\arraystretch}{1.25}")
    out.append(r"\begin{tabularx}{\textwidth}{|>{\bfseries}p{3.5cm}|p{3.5cm}|c|c|X|}")
    out.append(r"\hline\rowcolor{headblue}\textbf{Dimensión TAM} & \textbf{Grupo} & \textbf{Media} & \textbf{Desv.} & \textbf{Interpretación}\\\hline")
    tams = [
        ("Utilidad percibida (PU)",  "Docentes (N=5)",    "4.45", "0.33", "Muy alta percepción de utilidad pedagógica."),
        ("",                          "Estudiantes (N=15)", "4.85", "0.22", "Percepción de utilidad cercana al máximo."),
        ("Facilidad de uso (PEOU)",   "Docentes (N=5)",    "3.95", "0.27", "Facilidad de uso alta, requiere mínimo esfuerzo."),
        ("",                          "Estudiantes (N=15)", "4.78", "0.23", "Interfaz extremadamente intuitiva."),
        ("Intención de uso (IU)",     "Docentes (N=5)",    "4.47", "0.38", "Fuerte disposición a integrar la herramienta."),
        ("",                          "Estudiantes (N=15)", "4.93", "0.14", "Intención de uso casi unánime y máxima."),
    ]
    for (dim, grupo, media, sd, interp) in tams:
        out.append(r"{0} & {1} & {2} & {3} & {4} \\\hline".format(dim, grupo, media, sd, interp))
    out.append(r"\end{tabularx}\end{table}")
    out.append(r"\elaboracion")
    out.append(r"")
    out.append(r"\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{fig13_grafico_tam.pdf}\caption{Gráfico de brechas TAM.}\label{fig:tam}\end{figure}")
    out.append(r"\elaboracion")
    out.append(r"")

    out_text = "\n".join(out)
    with open("/home/claude/proyecto/latex/cap4_resultados.tex", "w", encoding="utf-8") as f:
        f.write(out_text)
    print(f"Generado cap4_resultados.tex con {len(CASOS)} casos de uso.")


if __name__ == "__main__":
    main()
