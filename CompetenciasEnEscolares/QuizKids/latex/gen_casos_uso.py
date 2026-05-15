#!/usr/bin/env python3
"""Genera la sección de Casos de Uso del cap4 con formato exacto del autor."""

# Lista de los 15 casos de uso, en orden
# Cada CU es un dict con todos los campos necesarios
# Las imágenes corresponden a los PDFs ya existentes en figuras/

CASOS = [
    {
        "tabla": 12,
        "label": "tab:cu_ver_eval",
        "titulo": "Ver evaluación",
        "codigo": "CU-003",
        "actores": "Estudiante",
        "objetivo": "Permitir que el estudiante visualice de forma organizada y atractiva las pruebas que su docente ha habilitado para su resolución.",
        "resumen": "Al ingresar al sistema, el estudiante ve una cuadrícula de tarjetas que representan las evaluaciones activas, permitiéndole identificar temas y niveles de dificultad antes de comenzar.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-004 (Desarrollo de evaluación). \\par \\textbf{Depende de:} Base de datos de evaluaciones, Asociación estudiante-docente y Filtros por estado.",
        "precondicion": "El estudiante debe estar autenticado y vinculado a un docente; debe existir al menos una evaluación en estado ``Habilitada''.",
        "postcondicion": "El estudiante visualiza las tarjetas interactivas en pantalla y el sistema queda a la espera de la selección de una prueba.",
        "importancia": "Alta -- Es la interfaz principal de interacción y motivación para el estudiante.",
        "flujo": [
            ("a", "1.~El estudiante inicia sesión exitosamente en la plataforma (CU-001)."),
            ("s", "2.~El sistema consulta las evaluaciones vinculadas al ID del docente y del estudiante."),
            ("s", "3.~El sistema filtra únicamente aquellas evaluaciones que tengan el estado ``Habilitada''."),
            ("s", "4.~La aplicación renderiza una cuadrícula de tarjetas con imagen, tema, descripción y dificultad."),
            ("a", "5.~El estudiante identifica y revisa la información de las tarjetas disponibles."),
            ("a", "6.~El estudiante selecciona una evaluación haciendo clic en la tarjeta deseada."),
            ("s", "7.~La aplicación redirige al estudiante a la pantalla de inicio de prueba (CU-004)."),
        ],
        "alterno": "\\textbf{3.a.\\ Sin evaluaciones disponibles:} si el docente no ha habilitado pruebas, el sistema muestra un mensaje amigable indicando que no hay tareas pendientes por el momento. \\par \\textbf{4.a.\\ Error de carga multimedia:} si las imágenes de las tarjetas no cargan, el sistema muestra un ícono temático por defecto para no interrumpir la navegación.",
        "img_seq": "figuras/seq_ver_eval.pdf",
        "img_iu": "figuras/ui_evaluaciones_estudiante.pdf",
        "comentarios": "Las tarjetas deben cumplir con altos estándares de contraste y tamaño de fuente (WCAG 2.1) para asegurar la accesibilidad visual. En el \\textit{frontend} con Angular, se utiliza una tubería (\\textit{pipe}) o filtro para organizar dinámicamente las tarjetas por fecha o dificultad, mejorando la experiencia del niño.",
    },
    {
        "tabla": 13,
        "label": "tab:cu_resolver",
        "titulo": "Resolver evaluación",
        "codigo": "CU-004",
        "actores": "Estudiante",
        "objetivo": "Proporcionar un entorno interactivo y amigable para que el estudiante responda las preguntas de una evaluación de forma secuencial.",
        "resumen": "El estudiante accede a la prueba, lee las instrucciones y responde los ítems uno a uno. El sistema permite navegación asistida, control por voz opcional y guarda el progreso automáticamente.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-005 (Presentación de resultados al finalizar la evaluación). \\par \\textbf{Depende de:} Motor de evaluación, Base de datos de preguntas y respuestas.",
        "precondicion": "El estudiante debe haber seleccionado una evaluación válida y habilitada desde su panel de inicio (CU-003).",
        "postcondicion": "El sistema captura todas las respuestas y las envía al \\textit{backend} para su cálculo y registro definitivo en la base de datos de desempeño.",
        "importancia": "Muy alta -- Es el núcleo funcional para los estudiantes.",
        "flujo": [
            ("a", "1.~El estudiante selecciona una tarjeta de evaluación (CU-003)."),
            ("s", "2.~La aplicación muestra una pantalla de ``Pre-evaluación'' con instrucciones claras."),
            ("a", "3.~El estudiante hace clic en el botón ``Comenzar''."),
            ("s", "4.~El sistema presenta la primera pregunta con sus respectivas opciones de respuesta."),
            ("p", "5.~(Opcional) El estudiante activa el control por voz para escuchar el enunciado.", "6.~El sistema sintetiza el texto y reproduce el audio del ítem actual."),
            ("a", "7.~El estudiante selecciona una respuesta y hace clic en el botón ``Siguiente''."),
            ("s", "8.~El sistema guarda la respuesta temporalmente y carga el siguiente ítem secuencialmente."),
            ("a", "9.~El estudiante repite los pasos 7 y 8 hasta completar todos los ítems de la prueba."),
            ("a", "10.~Al finalizar la última pregunta, el estudiante hace clic en el botón ``Finalizar''."),
            ("s", "11.~El sistema procesa los datos y redirige a la pantalla de resultados (CU-005)."),
        ],
        "alterno": "\\textbf{4.a.\\ Evaluación con tiempo límite:} el sistema inicia un contador regresivo; si el tiempo se agota, se guarda lo avanzado y se finaliza la prueba automáticamente. \\par \\textbf{6.a.\\ Error de reproducción de voz:} si el navegador no soporta el audio, el sistema muestra una alerta sugiriendo continuar con la lectura visual. \\par \\textbf{8.a.\\ Desconexión de internet:} el sistema notifica la pérdida de conexión y mantiene las respuestas en caché local hasta que se restablezca el servicio.",
        "img_seq": "figuras/seq_resolver_eval.pdf",
        "img_iu": "figuras/ui_resolver_eval_pictograma.pdf",
        "comentarios": "La interfaz debe ser 100\\,\\% responsiva y optimizada para dispositivos táctiles (\\textit{tablets}), facilitando la interacción de niños de primaria. El uso de \\texttt{window.localStorage} en Angular asegura que el progreso no se pierda ante cierres accidentales de la pestaña del navegador.",
    },
    {
        "tabla": 14,
        "label": "tab:cu_retro",
        "titulo": "Ver retroalimentación",
        "codigo": "CU-005",
        "actores": "Estudiante",
        "objetivo": "Proporcionar al estudiante una visualización clara y motivadora de su desempeño académico inmediatamente después de completar una prueba.",
        "resumen": "El sistema calcula la calificación, el tiempo empleado y genera una retroalimentación gráfica y motivacional para informar al estudiante sobre sus logros.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} retorno a la pantalla principal (CU-003). \\par \\textbf{Depende de:} Módulo de corrección automática, Sistema gráfico de resultados y Base de datos de desempeño.",
        "precondicion": "El estudiante debe haber finalizado y enviado satisfactoriamente las respuestas de su evaluación (CU-004). El \\textit{backend} debe haber procesado y calculado la calificación final.",
        "postcondicion": "El estudiante visualiza su rendimiento y el estado de la evaluación cambia a ``Completada'' en la base de datos.",
        "importancia": "Alta -- Aporta retroalimentación y cierre al proceso de aprendizaje.",
        "flujo": [
            ("a", "1.~El estudiante hace clic en el botón ``Finalizar'' de la evaluación (CU-004)."),
            ("s", "2.~El sistema recibe las respuestas y ejecuta el algoritmo de calificación automática."),
            ("s", "3.~El sistema calcula el tiempo total empleado durante la sesión de prueba."),
            ("s", "4.~La aplicación renderiza una pantalla de resultados con el puntaje numérico obtenido."),
            ("s", "5.~El sistema genera y muestra un gráfico de desempeño (barras o pastel) con colores amigables."),
            ("s", "6.~El sistema muestra una imagen de \\textit{feedback} motivacional (medalla o estrella) basada en el rango de nota."),
            ("p", "7.~(Opcional) El estudiante selecciona ``Revisar respuestas'' si el docente habilitó la opción.", "8.~El sistema despliega el detalle de aciertos y errores cometidos."),
            ("a", "9.~El estudiante hace clic en ``Volver al inicio''."),
            ("s", "10.~La aplicación redirige al estudiante a su panel principal de evaluaciones (CU-003)."),
        ],
        "alterno": "\\textbf{2.a.\\ Error en el procesamiento:} si el cálculo de la nota falla, el sistema muestra un mensaje de error y guarda las respuestas para un reintento automático de calificación posterior. \\par \\textbf{8.a.\\ Revisión deshabilitada:} si el docente no permitió la revisión, el botón correspondiente no aparecerá en la interfaz de resultados.",
        "img_seq": "figuras/seq_ver_retroalimentacion.pdf",
        "img_iu": "figuras/ui_retroalimentacion.pdf",
        "comentarios": "Los mensajes motivacionales deben estar adaptados a niños de primaria (ej. ``¡Excelente!'', ``¡Sigue así!''). Técnicamente, Angular recibe el objeto de resultados procesado por NestJS y utiliza librerías de gráficos para pintar la información de forma dinámica y responsiva.",
    },
    {
        "tabla": 15,
        "label": "tab:cu_panel",
        "titulo": "Gestionar panel docente",
        "codigo": "CU-006",
        "actores": "Docente",
        "objetivo": "Visualizar todas las evaluaciones que el docente ha creado organizadas en formato de tarjetas informativas desde su pantalla principal.",
        "resumen": "El docente accede a su panel principal donde el sistema filtra y muestra exclusivamente sus evaluaciones creadas, permitiéndole conocer su estado de visibilidad y acceder a su edición.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-008 (Creación de evaluaciones) y CU-007 (Habilitación y deshabilitación). \\par \\textbf{Depende de:} Base de datos de evaluaciones, Autenticación y perfil docente.",
        "precondicion": "El docente debe haber iniciado sesión en el sistema y tener un \\textit{token} de autenticación válido.",
        "postcondicion": "El sistema despliega la lista de tarjetas correspondientes a las pruebas creadas por el docente, habilitando el acceso rápido a la edición de cada una.",
        "importancia": "Alta -- Facilita la gestión directa del contenido por parte del docente.",
        "flujo": [
            ("a", "1.~El docente inicia sesión exitosamente en la plataforma (CU-001)."),
            ("s", "2.~El sistema identifica el ID del docente autenticado en la base de datos."),
            ("s", "3.~El sistema filtra exclusivamente las evaluaciones asociadas a dicho ID."),
            ("s", "4.~La aplicación renderiza en el panel principal una cuadrícula con tarjetas informativas."),
            ("a", "5.~El docente revisa el nombre, descripción, nivel de dificultad y estado (habilitada/deshabilitada) de sus pruebas."),
            ("a", "6.~El docente selecciona el ícono de ``acceso rápido'' en una tarjeta específica."),
            ("s", "7.~La aplicación redirige al docente a la interfaz de edición de esa evaluación."),
        ],
        "alterno": "\\textbf{3.a.\\ Docente sin evaluaciones:} si el docente no ha creado contenido aún, el sistema muestra un mensaje indicando que la lista está vacía y ofrece un botón destacado para ``Crear nueva evaluación''. \\par \\textbf{4.a.\\ Error de carga de datos:} si el servidor no responde, la interfaz muestra una alerta de error de conexión y permite reintentar la carga del panel.",
        "img_seq": "figuras/seq_panel_docente.pdf",
        "img_iu": "figuras/ui_panel_docente_clases.pdf",
        "comentarios": "El diseño debe ser totalmente responsivo, garantizando que el docente pueda gestionar sus evaluaciones desde computadoras o dispositivos móviles. En la base de datos PostgreSQL se utiliza el ID del docente como llave foránea para asegurar que un profesor no pueda visualizar ni editar las pruebas de otro colega.",
    },
    {
        "tabla": 16,
        "label": "tab:cu_crear_examen",
        "titulo": "Crear examen",
        "codigo": "CU-008",
        "actores": "Docente",
        "objetivo": "Permitir al docente definir la estructura base de una nueva evaluación (tema, dificultad, descripción y duración) antes de agregar las preguntas.",
        "resumen": "El docente ingresa los datos generales de la prueba en un formulario; el sistema valida la información y crea el registro de la evaluación en la base de datos en estado inactivo o borrador.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-009 (Gestión de preguntas por evaluación). \\par \\textbf{Depende de:} Interfaz de gestión docente y Base de datos de evaluaciones.",
        "precondicion": "El docente debe haber iniciado sesión exitosamente, contar con los permisos adecuados y encontrarse en su panel de gestión.",
        "postcondicion": "La nueva evaluación queda registrada en la base de datos vinculada al docente, habilitando la interfaz para comenzar a agregarle preguntas.",
        "importancia": "Muy alta -- Es la funcionalidad base del sistema de evaluación.",
        "flujo": [
            ("a", "1.~El docente selecciona la opción ``Crear nueva evaluación''."),
            ("s", "2.~El sistema muestra el formulario vacío de creación de evaluación."),
            ("a", "3.~El docente completa los campos obligatorios: título/tema, nivel de dificultad, descripción y duración (minutos)."),
            ("a", "4.~El docente hace clic en el botón ``Crear evaluación''."),
            ("s", "5.~El sistema valida que los campos requeridos no estén vacíos y que la duración sea mayor a cero."),
            ("s", "6.~El sistema registra la nueva evaluación en la base de datos (PostgreSQL)."),
            ("s", "7.~La aplicación redirige al docente a la interfaz de gestión de preguntas (CU-009)."),
        ],
        "alterno": "\\textbf{5.a.} Si el docente deja campos obligatorios vacíos, el sistema resalta los errores en rojo y detiene el proceso de guardado. \\par \\textbf{5.b.} Si se ingresa una duración negativa o cero, el sistema solicita ingresar un número válido antes de continuar.",
        "img_seq": "figuras/seq_crear_examen.pdf",
        "img_iu": "figuras/ui_crear_examen.pdf",
        "comentarios": "Se recomienda agregar asistencia visual en la interfaz (como textos de ejemplo tenues en los campos vacíos o plantillas prediseñadas) para facilitar la carga de datos al docente.",
    },
    {
        "tabla": 17,
        "label": "tab:cu_org_preg",
        "titulo": "Organizar preguntas",
        "codigo": "CU-009",
        "actores": "Docente",
        "objetivo": "Permitir al docente gestionar la lista de preguntas asociadas a una evaluación específica mediante funciones de visualización, edición, eliminación y reordenamiento.",
        "resumen": "El docente accede al administrador de una prueba para ver y modificar las preguntas existentes. El sistema procesa estas acciones (CRUD y ordenamiento) y actualiza la estructura de la evaluación en la base de datos.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-010 (Creación de preguntas). \\par \\textbf{Depende de:} Evaluación previamente creada (CU-008) y base de datos de preguntas.",
        "precondicion": "El docente debe haber iniciado sesión y debe haber creado previamente al menos una evaluación.",
        "postcondicion": "El sistema actualiza la estructura de la evaluación en la base de datos, reflejando cualquier modificación, eliminación o cambio de orden.",
        "importancia": "Muy alta -- Fundamental para personalizar y estructurar las evaluaciones.",
        "flujo": [
            ("a", "1.~El docente selecciona una evaluación y da clic en ``Gestionar preguntas''."),
            ("s", "2.~El sistema consulta y muestra la lista editable con todas las preguntas asociadas a esa prueba."),
            ("a", "3.~El docente interactúa con la lista cambiando el orden de las preguntas (arrastrar y soltar)."),
            ("s", "4.~El sistema actualiza visualmente el orden de la lista en la pantalla."),
            ("a", "5.~El docente da clic en el botón de guardar o confirmar cambios."),
            ("s", "6.~El sistema registra el nuevo orden en la base de datos y muestra un mensaje de éxito."),
        ],
        "alterno": "\\textbf{2.a.} Si la evaluación aún no tiene preguntas, el sistema mostrará un mensaje indicando que la lista está vacía y destacará el botón para crear una nueva (CU-010). \\par \\textbf{3.a.} Si en lugar de ordenar, el docente elige ``Eliminar'' una pregunta, el sistema desplegará un \\textit{modal} de confirmación obligatoria. Si el docente cancela, la acción se aborta y la lista no sufre cambios.",
        "img_seq": "figuras/seq_organizar_preguntas.pdf",
        "img_iu": "figuras/ui_nueva_pregunta.pdf",
        "comentarios": "Se sugiere incluir botones de navegación amigables para moverse entre la lista de preguntas y la configuración general. Esta gestión se beneficia directamente de tener un control de versiones o historial de cambios.",
    },
    {
        "tabla": 18,
        "label": "tab:cu_config",
        "titulo": "Configurar contenido",
        "codigo": "CU-010",
        "actores": "Docente",
        "objetivo": "Permitir al docente crear preguntas estructuradas para una evaluación, definiendo el enunciado, el formato y las opciones de respuesta válidas.",
        "resumen": "El docente selecciona el tipo de pregunta (opción múltiple, verdadero/falso, etc.), redacta el enunciado y configura las opciones indicando cuál es la correcta. El sistema valida la integridad de la pregunta y la guarda.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-011 (Soporte multimedia en preguntas). \\par \\textbf{Depende de:} Evaluación existente e Interfaz de edición docente.",
        "precondicion": "El docente debe estar autenticado, haber seleccionado una evaluación previamente creada y encontrarse dentro de la interfaz de gestión de preguntas (CU-009).",
        "postcondicion": "La nueva pregunta, junto con su enunciado, tipo y estructura de respuestas, se registra exitosamente en la base de datos asociada al ID de la evaluación.",
        "importancia": "Muy alta -- Permite generar contenido pedagógico evaluativo y asegurar que el sistema califique automáticamente.",
        "flujo": [
            ("a", "1.~El docente da clic en la opción para agregar un nuevo ítem evaluativo."),
            ("s", "2.~El sistema provee un formulario con un campo de texto enriquecido para el enunciado y un selector de tipo de pregunta."),
            ("a", "3.~El docente ingresa el enunciado y selecciona el formato (múltiple, V/F o corta)."),
            ("s", "4.~El sistema adapta dinámicamente los campos inferiores para ingresar las opciones de respuesta."),
            ("a", "5.~El docente llena las opciones y marca explícitamente cuál es la correcta."),
            ("a", "6.~El docente hace clic en ``Guardar''."),
            ("s", "7.~El sistema verifica la información y registra la pregunta en la base de datos vinculada a la evaluación."),
            ("s", "8.~La aplicación actualiza la vista mostrando la nueva pregunta en la lista."),
        ],
        "alterno": "\\textbf{7.a.} Si el docente olvida marcar al menos una respuesta como correcta, el sistema aplica una validación automática que impide guardar la pregunta y resalta el error en pantalla. \\par \\textbf{5.a.} Antes de guardar, el docente puede seleccionar la opción de ``Vista previa'' y el sistema renderizará la pregunta tal como la verá el estudiante.",
        "img_seq": "figuras/seq_configurar_contenido.pdf",
        "img_iu": "figuras/ui_gestionar_opciones.pdf",
        "comentarios": "La validación de la respuesta correcta es crítica para que el motor de evaluación (CU-004) pueda funcionar. El campo de enunciado debe soportar texto enriquecido para dar formato a la lectura.",
    },
    {
        "tabla": 19,
        "label": "tab:cu_multimedia",
        "titulo": "Adjuntar archivos multimedia",
        "codigo": "CU-011",
        "actores": "Docente",
        "objetivo": "Permitir al docente cargar e integrar recursos multimedia (imágenes, GIFs o videos) en las preguntas para enriquecer visualmente la evaluación.",
        "resumen": "El docente sube un archivo multimedia al editor de preguntas. El sistema valida la extensión y el tamaño, muestra una vista previa y vincula la URL del archivo a la pregunta en la posición elegida.",
        "tipo": "Secundario (Extensión de CU-010)",
        "dependencias": "\\textbf{Invoca a:} ninguno directamente; es una extensión de CU-010. \\par \\textbf{Depende de:} Módulo de creación de preguntas y el Sistema de almacenamiento de archivos multimedia.",
        "precondicion": "El docente debe estar autenticado y encontrarse dentro de la interfaz de creación o edición de una pregunta específica (CU-010).",
        "postcondicion": "El archivo multimedia se procesa, se guarda de forma segura, y su ruta de acceso (URL) se vincula a la pregunta correspondiente en la base de datos, respetando la posición configurada por el docente.",
        "importancia": "Alta -- Aumenta la comprensión en alumnos con diferentes estilos de aprendizaje.",
        "flujo": [
            ("a", "1.~El docente interactúa con la zona de carga de archivos (tipo \\textit{Drag \\& Drop} o con botón de selección) en el editor de preguntas."),
            ("s", "2.~El sistema habilita la selección o recepción del recurso multimedia."),
            ("a", "3.~El docente selecciona un archivo e indica la posición deseada (arriba o abajo del enunciado)."),
            ("s", "4.~El sistema valida estrictamente que la extensión sea \\texttt{.jpg}, \\texttt{.png}, \\texttt{.gif} o \\texttt{.mp4} y que no exceda el límite de tamaño."),
            ("s", "5.~Al cargar el archivo con éxito, la interfaz genera y muestra una vista previa integrada en tiempo real."),
            ("a", "6.~El docente finaliza y guarda la pregunta."),
            ("s", "7.~El sistema almacena el recurso y vincula su URL a la pregunta en la base de datos."),
        ],
        "alterno": "\\textbf{4.a.\\ Formato no soportado:} si el archivo no es \\texttt{.jpg}, \\texttt{.png}, \\texttt{.gif} ni \\texttt{.mp4}, el sistema rechaza la carga y muestra un error indicando los formatos válidos. \\par \\textbf{4.b.\\ Exceso de tamaño:} si el archivo supera el límite máximo permitido (ej. 2~MB para imágenes/GIFs o 10~MB para videos), el sistema advierte sobre el límite y detiene la carga para asegurar el rendimiento del servidor.",
        "img_seq": "figuras/seq_adjuntar_multimedia.pdf",
        "img_iu": "figuras/ui_arasaac_pictogramas.pdf",
        "comentarios": "Se debe verificar la compatibilidad con dispositivos móviles y limitar el tamaño de los archivos para asegurar un buen rendimiento. Los recursos deben renderizarse de forma responsiva en el panel del estudiante, adaptando su tamaño a las pantallas móviles sin deformarse.",
    },
    {
        "tabla": 20,
        "label": "tab:cu_alumnos",
        "titulo": "Consultar alumnos",
        "codigo": "CU-012",
        "actores": "Docente",
        "objetivo": "Visualizar una lista completa y filtrable de los alumnos registrados y vinculados al docente, organizados por curso o grupo, para llevar un seguimiento de su estado en la plataforma.",
        "resumen": "El docente accede a la sección de estudiantes; el sistema consulta la base de datos y despliega una tabla con los alumnos del docente (nombre, curso, estado). El sistema permite filtrar resultados por nombre mediante un buscador.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-013 (Visualización de resultados generales y por prueba, al hacer clic en un estudiante específico). \\par \\textbf{Depende de:} Módulo de registro, Asociación alumno-docente y la Base de datos de usuarios.",
        "precondicion": "El docente debe haber iniciado sesión exitosamente en el sistema. Debe existir al menos un estudiante registrado y vinculado correctamente al código único de este docente (CU-002).",
        "postcondicion": "El sistema despliega correctamente la lista de alumnos según los filtros aplicados. El docente obtiene una vista clara de sus clases y el sistema queda a la espera de que seleccione un estudiante para consultar su rendimiento.",
        "importancia": "Alta -- Permite acceder rápidamente al seguimiento individual.",
        "flujo": [
            ("a", "1.~El docente accede a la sección de gestión de estudiantes."),
            ("s", "2.~El sistema identifica el ID del docente y consulta la base de datos buscando únicamente a los alumnos vinculados a él."),
            ("s", "3.~La aplicación muestra una lista o tabla organizada por curso, indicando obligatoriamente: nombre completo, curso/grupo y estado (activo/inactivo)."),
            ("s", "4.~El sistema muestra un indicador o contador del total de alumnos inscritos por cada grupo."),
            ("a", "5.~El docente utiliza el buscador ingresando el nombre de un alumno específico."),
            ("s", "6.~El sistema filtra los resultados en tiempo real y muestra las coincidencias exactas o parciales en la lista."),
            ("a", "7.~El docente selecciona a un estudiante de la lista."),
            ("s", "8.~El sistema redirige a la vista de perfil de rendimiento del estudiante seleccionado (CU-013)."),
        ],
        "alterno": "\\textbf{3.a.} Si el docente aún no tiene alumnos vinculados, el sistema muestra un mensaje indicando que no hay estudiantes registrados y le recuerda su código de vinculación para que lo comparta. \\par \\textbf{6.a.} Si la búsqueda no arroja coincidencias, el sistema muestra un mensaje de ``No se encontraron alumnos con ese nombre'' y permite limpiar el buscador.",
        "img_seq": "figuras/seq_consultar_alumnos.pdf",
        "img_iu": "figuras/ui_listado_estudiantes.pdf",
        "comentarios": "La interfaz debe ser limpia y responsiva, garantizando que la tabla o lista se adapte correctamente a pantallas de dispositivos móviles sin perder columnas de información.",
    },
    {
        "tabla": 21,
        "label": "tab:cu_analizar",
        "titulo": "Analizar calificaciones",
        "codigo": "CU-013",
        "actores": "Docente",
        "objetivo": "Acceder al perfil académico de un estudiante desde el listado general para visualizar su promedio global y el desglose de resultados por cada evaluación realizada.",
        "resumen": "El docente selecciona a un estudiante para evaluar su progreso individual. El sistema calcula y muestra el promedio acumulado junto con una lista detallada de cada prueba completada (puntaje, fecha, duración), utilizando colores o íconos para destacar el nivel de desempeño.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-014 (Curva de mejora individual) y CU-015 (Exportación de resultados a Excel). \\par \\textbf{Depende de:} Evaluaciones realizadas, Motor de análisis de resultados y acceso desde el listado de alumnos (CU-012).",
        "precondicion": "El docente debe estar autenticado, encontrarse en la lista de alumnos (CU-012) y seleccionar a un estudiante específico. El estudiante debe haber completado al menos una evaluación previamente para que existan datos que analizar.",
        "postcondicion": "El sistema presenta en pantalla el promedio general del estudiante y los resultados desglosados, mostrando explícitamente el puntaje, la fecha y la duración.",
        "importancia": "Muy alta -- Fundamental para evaluar el progreso del alumno, identificar su nivel de desempeño y compararlo dentro del grupo escolar.",
        "flujo": [
            ("a", "1.~El docente hace clic en un alumno específico desde la pantalla de ``Lista de alumnos'' (CU-012)."),
            ("s", "2.~El sistema consulta el historial de evaluaciones completadas por el estudiante seleccionado."),
            ("s", "3.~El sistema calcula el promedio general acumulado del estudiante."),
            ("s", "4.~La aplicación muestra el perfil del estudiante destacando visualmente el promedio global calculado."),
            ("s", "5.~El sistema despliega el desglose de cada evaluación, mostrando de forma obligatoria: el puntaje obtenido, la fecha de realización y la duración (tiempo empleado)."),
            ("s", "6.~El sistema aplica colores o íconos de desempeño a cada resultado (ej. verde para aprobado, rojo para bajo rendimiento) para facilitar la interpretación visual rápida."),
            ("a", "7.~El docente utiliza los controles de la interfaz para ordenar los resultados detallados (por ejemplo, por fecha o por puntaje)."),
            ("s", "8.~El sistema actualiza dinámicamente el orden de la lista en pantalla."),
        ],
        "alterno": "\\textbf{2.a.} Si el estudiante aún no ha completado ninguna evaluación, el sistema muestra el promedio general como ``0'' o ``N/A'' y despliega un mensaje amigable indicando que no hay registros históricos disponibles. \\par \\textbf{3.a.} Si ocurre un error de conexión al consultar la base de datos, el sistema muestra una alerta de error y sugiere recargar el perfil del alumno.",
        "img_seq": "figuras/seq_analizar_calificaciones.pdf",
        "img_iu": "figuras/ui_panel_control_docente.pdf",
        "comentarios": "Los resultados deben poder ordenarse y compararse de alguna forma sencilla entre alumnos del mismo curso. Esta vista es el paso previo ideal para la generación de gráficas (CU-014) o exportación de datos (CU-015).",
    },
    {
        "tabla": 22,
        "label": "tab:cu_brechas",
        "titulo": "Identificar brechas de aprendizaje",
        "codigo": "CU-016",
        "actores": "Docente / Estudiante",
        "objetivo": "Visualizar un análisis automático de los resultados categorizados por temas o competencias para identificar rápidamente las áreas de alto y bajo desempeño de los estudiantes (individual o grupal).",
        "resumen": "El sistema procesa el historial de evaluaciones, agrupa los aciertos y errores según la categoría temática de cada pregunta y presenta un resumen porcentual. Se utilizan colores semánticos e íconos para destacar visualmente el nivel de dominio en cada área.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-017 (Sugerencias generadas por IA, que se alimentará de estos datos). \\par \\textbf{Depende de:} Resultados por evaluación y Categorización temática de preguntas en la base de datos.",
        "precondicion": "El usuario (docente o estudiante) debe estar en la vista de análisis de rendimiento. Las evaluaciones realizadas deben contener preguntas previamente vinculadas a un tema o competencia curricular.",
        "postcondicion": "El sistema procesa la información y renderiza en pantalla el análisis por categoría temática y el porcentaje de aciertos por área, destacando los extremos de desempeño.",
        "importancia": "Alta -- Permite una intervención pedagógica más precisa y la planificación de refuerzos o tutorías.",
        "flujo": [
            ("a", "1.~El usuario (docente o estudiante) ingresa a la vista de análisis de áreas de desempeño (perfil individual o resumen del grupo)."),
            ("s", "2.~El sistema recopila las respuestas del historial y lee la categoría temática de cada pregunta evaluada."),
            ("s", "3.~El sistema calcula el porcentaje de aciertos agrupado por cada categoría o competencia."),
            ("s", "4.~La aplicación renderiza una lista, tabla o gráfico con las áreas evaluadas."),
            ("s", "5.~El sistema aplica colores semánticos (ej. verde para áreas con alto porcentaje, rojo para bajo desempeño) e íconos distintivos."),
            ("a", "6.~El usuario visualiza la información y evalúa las áreas que requieren atención."),
            ("s", "7.~El sistema habilita la consulta de recomendaciones IA (CU-017) basándose en estos resultados."),
        ],
        "alterno": "\\textbf{2.a.\\ Evaluaciones sin categorizar:} si las pruebas realizadas contienen preguntas que no fueron vinculadas a ningún tema, el sistema las agrupa bajo ``Categoría General'' o ``Sin clasificar'', o muestra una alerta al docente indicando que faltan metadatos para un análisis preciso.",
        "img_seq": "figuras/seq_identificar_brechas.pdf",
        "img_iu": "figuras/ui_rendimiento_alertas.pdf",
        "comentarios": "\\textbf{Dependencia crítica:} para que este cálculo sea posible, el motor de evaluación debe categorizar cada pregunta por tema en la base de datos al momento de crearla (CU-010).",
    },
    {
        "tabla": 23,
        "label": "tab:cu_consejos",
        "titulo": "Recibir consejos IA",
        "codigo": "CU-017",
        "actores": "Docente / Estudiante",
        "objetivo": "Recibir sugerencias automáticas basadas en el análisis de los patrones de error y evaluaciones anteriores para saber exactamente qué temas y competencias reforzar.",
        "resumen": "El sistema utiliza un modelo de IA para analizar el historial de resultados del estudiante, detectar áreas de bajo rendimiento y generar recomendaciones textuales breves y prácticas tanto para el autoestudio del alumno como para la planificación del docente.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} ninguno directamente. \\par \\textbf{Depende de:} Análisis de resultados (CU-016) y Modelo de recomendación IA.",
        "precondicion": "El estudiante debe contar con un historial de evaluaciones completadas y procesadas por el módulo de análisis de resultados (CU-016). El motor de IA debe tener acceso a los patrones de error y competencias evaluadas.",
        "postcondicion": "El sistema procesa la información y devuelve sugerencias textuales que cumplen con tener un formato breve, claro y práctico. Estas sugerencias se desglosan por estudiante y por competencia.",
        "importancia": "Alta -- Fomenta el aprendizaje adaptativo y personalizado.",
        "flujo": [
            ("a", "1.~El usuario (estudiante o docente) ingresa al panel de retroalimentación o resultados del alumno."),
            ("s", "2.~El sistema analiza automáticamente los resultados anteriores del estudiante para detectar competencias con bajo rendimiento."),
            ("s", "3.~El motor de IA procesa los patrones de error identificados en la base de datos."),
            ("s", "4.~El sistema genera sugerencias personalizadas por cada estudiante y por competencia específica."),
            ("s", "5.~La aplicación presenta las recomendaciones en pantalla mediante un formato de texto breve, claro y práctico."),
        ],
        "alterno": "\\textbf{2.a.\\ Historial insuficiente:} si el estudiante no tiene suficientes evaluaciones o errores para analizar, el sistema mostrará un mensaje indicando que se requiere más información de pruebas o que el estudiante mantiene un rendimiento óptimo general. \\par \\textbf{3.a.\\ Error del servicio de IA:} si la comunicación con el modelo de recomendación falla, el sistema oculta temporalmente la sección de sugerencias y muestra un mensaje amigable indicando que las recomendaciones no están disponibles en ese momento.",
        "img_seq": "figuras/seq_recibir_consejos_ia.pdf",
        "img_iu": "figuras/ui_comentario_magico_ia.pdf",
        "comentarios": "Las sugerencias pueden incluir frases directas como: ``Refuerza operaciones con fracciones'' o ``Revisa conceptos de geometría básica''. Estas recomendaciones deben ser visibles tanto en el panel del estudiante (para su autoestudio) como en la vista de resultados del docente (para su planificación).",
    },
    {
        "tabla": 24,
        "label": "tab:cu_gamificacion",
        "titulo": "Aplicar gamificación",
        "codigo": "CU-021",
        "actores": "Estudiante",
        "objetivo": "Otorgar insignias visuales y puntos al estudiante tras completar evaluaciones exitosamente o alcanzar metas de aprendizaje, para mantener un alto nivel de motivación.",
        "resumen": "El sistema evalúa el rendimiento y el progreso del alumno al finalizar una prueba. Si cumple ciertos criterios predefinidos (ej. nota perfecta, racha de tres pruebas seguidas), desbloquea un logro en su perfil, notificándole con una animación celebratoria.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} actualización del perfil del estudiante. \\par \\textbf{Depende de:} CU-005 (Presentación de resultados) y del motor de reglas de gamificación en el \\textit{backend}.",
        "precondicion": "El estudiante debe haber finalizado satisfactoriamente una evaluación (CU-004/CU-005). Deben existir insignias previamente configuradas en la base de datos con sus respectivas condiciones de desbloqueo.",
        "postcondicion": "El sistema registra el nuevo logro obtenido vinculándolo al ID del estudiante en la base de datos (PostgreSQL) y este pasa a estar visible de forma permanente en su ``vitrina de logros'' virtual.",
        "importancia": "Alta -- Esencial para retener la atención y fomentar el esfuerzo continuo en niños de primaria.",
        "flujo": [
            ("a", "1.~El estudiante finaliza su evaluación y llega a la pantalla de resultados (CU-005)."),
            ("s", "2.~El sistema recibe los resultados y los envía al motor de validación de logros."),
            ("s", "3.~El sistema compara el puntaje y el historial del alumno contra las reglas de las insignias bloqueadas."),
            ("s", "4.~El sistema determina que el estudiante ha cumplido la condición para un nuevo logro (ej. ``Genio Matemático'')."),
            ("s", "5.~El sistema registra el logro como ``desbloqueado'' en la base de datos para ese usuario."),
            ("s", "6.~La aplicación superpone una animación festiva y llamativa en pantalla anunciando la nueva medalla o insignia."),
            ("a", "7.~El estudiante hace clic en ``Continuar'' o ``Ver mis logros''."),
            ("s", "8.~El sistema redirige al estudiante a su panel principal o a su vitrina de insignias, actualizando su contador de recompensas."),
        ],
        "alterno": "\\textbf{4.a.} Si el estudiante no cumple con ninguna condición nueva tras la evaluación, el sistema simplemente omite la animación de desbloqueo y muestra únicamente la retroalimentación normal de la prueba. \\par \\textbf{6.a.} Si ocurre un fallo de conexión al intentar guardar el logro, el sistema lo almacena en caché temporalmente y reintenta la sincronización en segundo plano sin interrumpir la experiencia del alumno.",
        "img_seq": "figuras/seq_aplicar_gamificacion.pdf",
        "img_iu": "figuras/ui_pre_evaluacion.pdf",
        "comentarios": "Las insignias deben tener un diseño muy visual, tipo ``cartoon'' o videojuego, aprovechando Angular para las animaciones CSS. Se recomienda incluir una barra de progreso que le indique al niño cuánto le falta para su próxima recompensa.",
    },
    {
        "tabla": 25,
        "label": "tab:cu_ingresar",
        "titulo": "Ingresar a clase",
        "codigo": "CU-027",
        "actores": "Estudiante",
        "objetivo": "Permitir al estudiante vincularse a una clase o grupo específico administrado por su docente mediante la introducción de un código único.",
        "resumen": "El estudiante ingresa un código alfanumérico corto proporcionado por su profesor. El sistema valida este código y, de ser correcto, inscribe al alumno en el curso correspondiente, dándole acceso inmediato a sus evaluaciones.",
        "tipo": "Principal / Vinculación",
        "dependencias": "\\textbf{Invoca a:} afecta directamente al CU-003 (Visualización de evaluaciones disponibles), ya que habilitará nuevo contenido. \\par \\textbf{Depende de:} CU-001 (Inicio de sesión) y de que el docente haya generado y compartido el código previamente.",
        "precondicion": "El estudiante debe haber iniciado sesión exitosamente en su panel. El docente debe haber creado una clase en el sistema y el código de vinculación debe estar activo.",
        "postcondicion": "El estudiante queda asociado a la clase y al docente en la base de datos (PostgreSQL). El sistema actualiza el panel del estudiante, otorgándole acceso a las evaluaciones que estén habilitadas para ese curso específico.",
        "importancia": "Muy alta -- Es el mecanismo principal para estructurar los grupos de alumnos y conectar docentes con estudiantes.",
        "flujo": [
            ("a", "1.~El estudiante selecciona la opción ``Unirse a una clase'' en su panel principal."),
            ("s", "2.~El sistema despliega un \\textit{modal} o pantalla con un campo de texto simple y un botón de confirmación."),
            ("a", "3.~El estudiante ingresa el código único proporcionado por el docente y hace clic en ``Unirse''."),
            ("s", "4.~El sistema recibe el código y lo consulta en la base de datos de cursos."),
            ("s", "5.~El sistema verifica que el código es válido, corresponde a una clase activa y que el alumno no está previamente inscrito en ella."),
            ("s", "6.~El sistema crea la asociación (llaves foráneas) entre el ID del estudiante y el ID de la clase/docente."),
            ("s", "7.~La aplicación muestra una animación festiva y un mensaje de éxito indicando el nombre de la clase a la que se unió (ej. ``¡Bienvenido a 4to Grado de Matemáticas!'')."),
            ("a", "8.~El estudiante hace clic en ``Ir a mis pruebas''."),
            ("s", "9.~El sistema redirige al panel principal (CU-003), recargando la vista para mostrar las tarjetas de evaluaciones de su nueva clase."),
        ],
        "alterno": "\\textbf{5.a.\\ Código inválido o inactivo:} si el código no existe o el docente lo desactivó, el sistema muestra un mensaje amigable (ej. ``¡Ups! Ese código no funciona. Revisa si lo copiaste bien o pregúntale a tu profe'') y limpia el campo para reintentar. \\par \\textbf{5.b.\\ Alumno ya inscrito:} si el sistema detecta que el estudiante ya pertenece a ese grupo, muestra una alerta indicando ``¡Ya eres parte de esta clase!'' y cancela el proceso de vinculación redundante.",
        "img_seq": "figuras/seq_ingresar_clase.pdf",
        "img_iu": "figuras/ui_ingresar_codigo.pdf",
        "comentarios": "El campo para ingresar el código debe ser grande, con tipografía clara y estar configurado en Angular para no distinguir entre mayúsculas y minúsculas (\\textit{case-insensitive}), evitando así frustraciones comunes en niños de educación básica.",
    },
    {
        "tabla": 26,
        "label": "tab:cu_mapa",
        "titulo": "Ver mapa de competencias",
        "codigo": "CU-026",
        "actores": "Docente / Estudiante",
        "objetivo": "Mostrar un mapa visual por estudiante que refleje qué competencias curriculares han sido evaluadas y cuáles ha logrado alcanzar.",
        "resumen": "El sistema despliega una lista de competencias por módulo y nivel, indicando el estado de cada una (lograda, en proceso, no iniciada) mediante una visualización gráfica de cuadros, íconos y colores. Se habilita la opción de exportar este mapa en formato PDF o Excel.",
        "tipo": "Principal",
        "dependencias": "\\textbf{Invoca a:} CU-015 (Exportación de resultados) para la generación del PDF. \\par \\textbf{Depende de:} Motor de resultados y Base de datos de competencias curriculares.",
        "precondicion": "El estudiante debe haber completado evaluaciones que tengan competencias curriculares vinculadas. El usuario debe estar autenticado para acceder a su perfil o al de sus alumnos.",
        "postcondicion": "El sistema despliega una lista de competencias por módulo y nivel, indicando el estado de cada una mediante una visualización gráfica. Se habilita la opción de exportar este mapa en formato PDF o Excel.",
        "importancia": "Alta -- Refuerza el enfoque por competencias y la toma de decisiones pedagógicas.",
        "flujo": [
            ("a", "1.~El usuario (docente o estudiante) consulta el progreso académico en la plataforma."),
            ("s", "2.~El sistema recupera el historial de evaluaciones del alumno y consulta la base de datos de competencias curriculares."),
            ("s", "3.~El sistema calcula el estado actual de cada competencia evaluada."),
            ("s", "4.~El sistema despliega una lista de competencias organizadas por módulo y nivel."),
            ("s", "5.~La aplicación indica visualmente si la competencia está lograda, en proceso o no iniciada mediante cuadros, íconos y colores."),
            ("a", "6.~El usuario selecciona la opción para exportar el mapa de competencias."),
            ("s", "7.~El sistema invoca el módulo de exportación (CU-015) y genera el archivo en formato PDF o Excel."),
        ],
        "alterno": "\\textbf{2.a.\\ Sin datos previos:} si el estudiante no ha realizado ninguna evaluación con competencias vinculadas, el mapa mostrará todas las áreas en estado ``no iniciada'' y sugerirá realizar una prueba diagnóstica.",
        "img_seq": "figuras/seq_mapa_competencias.pdf",
        "img_iu": "figuras/ui_mapa_aventuras.pdf",
        "comentarios": "El mapa debe actualizarse en tiempo real tras cada evaluación. Puede usarse como excelente herramienta de comunicación directa con padres o representantes.",
    },
]


def gen_cu_table(cu):
    """Genera la tabla LaTeX completa de un caso de uso."""
    lines = []
    lines.append(f"\\begin{{table}}[H]")
    lines.append(f"\\centering")
    lines.append(f"\\caption{{Caso de uso ``{cu['titulo']}''.}}")
    lines.append(f"\\label{{{cu['label']}}}")
    lines.append(f"\\begin{{footnotesize}}")
    lines.append(f"\\renewcommand{{\\arraystretch}}{{1.25}}")
    lines.append(f"\\begin{{tabularx}}{{\\textwidth}}{{|>{{\\bfseries}}L{{2.6cm}}|X|>{{\\bfseries}}L{{2.4cm}}|X|}}")
    lines.append(f"\\hline")
    # Encabezado verde institucional
    lines.append(f"\\rowcolor{{tabhead}}\\multicolumn{{4}}{{|c|}}{{\\tabhead{{Caso de uso ``{cu['titulo']}''}}}}\\\\\\hline")
    # Código y Actores
    lines.append(f"Código: & {cu['codigo']} & Actores: & {cu['actores']}\\\\\\hline")
    # Objetivo, Resumen, Tipo, etc. (cada uno ocupa 2 columnas)
    lines.append(f"Objetivo: & \\multicolumn{{3}}{{X|}}{{{cu['objetivo']}}}\\\\\\hline")
    lines.append(f"Resumen: & \\multicolumn{{3}}{{X|}}{{{cu['resumen']}}}\\\\\\hline")
    lines.append(f"Tipo: & \\multicolumn{{3}}{{X|}}{{{cu['tipo']}}}\\\\\\hline")
    lines.append(f"Dependencias: & \\multicolumn{{3}}{{X|}}{{{cu['dependencias']}}}\\\\\\hline")
    lines.append(f"Precondición: & \\multicolumn{{3}}{{X|}}{{{cu['precondicion']}}}\\\\\\hline")
    lines.append(f"Postcondición: & \\multicolumn{{3}}{{X|}}{{{cu['postcondicion']}}}\\\\\\hline")
    lines.append(f"[Importancia]: & \\multicolumn{{3}}{{X|}}{{{cu['importancia']}}}\\\\\\hline")
    # Flujo normal de eventos -- cabecera
    lines.append(f"\\rowcolor{{tabhead2}}\\multicolumn{{4}}{{|c|}}{{\\textbf{{Flujo normal de eventos}}}}\\\\\\hline")
    # Subcabeceras de flujo (Acción del actor / Respuesta del sistema) — ahora en formato 2col
    # Necesito reorganizar: encabezado de subtabla de flujo
    lines.append(f"\\rowcolor{{tabhead2}}\\multicolumn{{2}}{{|>{{\\columncolor{{tabhead2}}}}c|}}{{\\textbf{{Acción del actor}}}} & \\multicolumn{{2}}{{>{{\\columncolor{{tabhead2}}}}c|}}{{\\textbf{{Respuesta del sistema}}}}\\\\\\hline")
    # Pasos del flujo
    for paso in cu['flujo']:
        if paso[0] == 'a':
            # Actor: ocupa columnas 1-2, las 3-4 vacías
            lines.append(f"\\multicolumn{{2}}{{|X|}}{{{paso[1]}}} & \\multicolumn{{2}}{{X|}}{{}}\\\\\\hline")
        elif paso[0] == 's':
            # Sistema: columnas 1-2 vacías, 3-4 con texto
            lines.append(f"\\multicolumn{{2}}{{|X|}}{{}} & \\multicolumn{{2}}{{X|}}{{{paso[1]}}}\\\\\\hline")
        elif paso[0] == 'p':
            # Paralelo: ambas columnas con contenido
            lines.append(f"\\multicolumn{{2}}{{|X|}}{{{paso[1]}}} & \\multicolumn{{2}}{{X|}}{{{paso[2]}}}\\\\\\hline")
    # Flujo alterno
    lines.append(f"\\rowcolor{{tabhead2}}\\multicolumn{{4}}{{|c|}}{{\\textbf{{Flujo alterno}}}}\\\\\\hline")
    lines.append(f"\\multicolumn{{4}}{{|X|}}{{{cu['alterno']}}}\\\\\\hline")
    # Diagrama de secuencia
    lines.append(f"\\rowcolor{{tabhead2}}\\multicolumn{{4}}{{|c|}}{{\\textbf{{Diagrama de secuencia}}}}\\\\\\hline")
    lines.append(f"\\multicolumn{{4}}{{|c|}}{{\\includegraphics[width=0.92\\textwidth,height=10cm,keepaspectratio]{{{cu['img_seq']}}}}}\\\\\\hline")
    # Interfaz de usuario
    lines.append(f"\\rowcolor{{tabhead2}}\\multicolumn{{4}}{{|c|}}{{\\textbf{{Interfaz de usuario}}}}\\\\\\hline")
    lines.append(f"\\multicolumn{{4}}{{|c|}}{{\\includegraphics[width=0.92\\textwidth,height=8cm,keepaspectratio]{{{cu['img_iu']}}}}}\\\\\\hline")
    # Comentarios
    lines.append(f"Comentarios: & \\multicolumn{{3}}{{X|}}{{{cu['comentarios']}}}\\\\\\hline")
    lines.append(f"\\end{{tabularx}}")
    lines.append(f"\\end{{footnotesize}}")
    lines.append(f"\\fuenteautor")
    lines.append(f"\\end{{table}}")
    return "\n".join(lines)


# Generar todo el archivo
output = []
output.append("% Casos de uso extendidos – formato exacto del documento original\n")
for cu in CASOS:
    output.append(gen_cu_table(cu))
    output.append("")  # blank line entre tablas

with open("/home/claude/proyecto/latex/casos_uso_generados.tex", "w") as f:
    f.write("\n".join(output))

print(f"Generados {len(CASOS)} casos de uso")
print("Archivo: /home/claude/proyecto/latex/casos_uso_generados.tex")
