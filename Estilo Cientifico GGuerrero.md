# Perfil de estilo científico — Gleiston Guerrero-Ulloa (y equipo: Hornos, Rodríguez-Domínguez)

Extraído del análisis de artículos propios (carpeta `Propios`) y refinado con 11 artículos del equipo (TDDM4IoTS, TDDT4IoTS, Validation case study, Agile review, IdeAir, Indoor Air Quality, Plant care, Medicine Dispenser, Elderly care, Classroom access, BellChat). Guía para reescribir manuscritos en la voz auténtica del autor. Corregir siempre los errores nativos (no reproducirlos).

## Voz y persona
- Primera persona plural: "we present", "we have developed", "we propose", "our proposal", "to the best of our knowledge".
- "This paper / this article / this work" como agente: "this paper proposes…", "This paper has presented…".
- Conclusiones abren con "This paper has presented…"; heading SIEMPRE combinado: "Conclusions and Future Work".
- Trabajo futuro: "As future work…", "In the future…".

## Marca registrada del equipo: humildad y "proof of concept" (CLAVE para EAIT)
El equipo NUNCA afirma validación; presenta el sistema como **"proof of concept" / "first prototype"** y el estudio como **"first evaluation"**, y difiere las afirmaciones fuertes al futuro. Fórmulas auténticas a reutilizar:
- "As a proof of concept, we (have) developed a first prototype of the system."
- "It is still too early to guarantee the success of our proposal."
- "We are optimistic … due to the favourable [perceptions/expressions] [expressed by the participants]."
- "Preliminary results … show a high level of acceptance by potential users."
- "Our proposal has to be tested with real users in their own homes."
Esta humildad coincide EXACTAMENTE con la reposición honesta que exige el informe de revisión: aplicar su estilo refuerza la honestidad. Ya aplicado en Torddis (intro + conclusiones).

## TDDM4IoTS (cómo lo enmarca el equipo)
- Expansión completa + acrónimo: "Test-Driven Development Methodology for IoT-based Systems (TDDM4IoTS)".
- "gathers ideas from … Model-Driven Engineering and Test-Driven Development … incorporating agile principles"; "covers the whole life cycle"; alineada con ISO/IEC/IEEE.
- 11 fases enumeradas inline: (1) Preliminary Analysis … (11) Maintenance.
- Aplicación iterativa/negociada: "the order and frequency of application will depend on the nature of the project."

## Arquitectura (patrón de descripción del sistema)
- Stack de 3 capas, cada una en cursiva en su primer uso: *User interaction layer* (web+móvil), *Cloud computing layer* (conectividad/procesamiento/almacenamiento), *Physical and preprocessing layer* (sensores+actuadores).
- Componentes enumerados inline con lista de letras ligada a una figura: "Its components are (see Figure~X): (a) …, to …; (b) …, to …".
- Sensores por número de parte (ESP32-CAM, NodeMCU ESP8266, MQ135…). Tabla "componente seleccionado vs. alternativas + criterio" (coste, curva de aprendizaje, popularidad).
- Flujo de datos narrado aparte ("… sent to the cloud via ESP8266 using RESTful Web Services").

## Presentación de la evaluación
- Figura/tabla primero → una frase interpretativa → un caveat que explica a los disidentes.
- SUS: "The mean SUS score was 81.46 out of 100 (SD = 11.65), indicating a 'Good' level of usability according to Bangor et al.".
- Porcentajes con 2 decimales; a veces agrupan "agree + strongly agree".
- Hedging fuerte: could/may/might/would.

## Estructura y hoja de ruta
Abstract → Introduction (cierra con contribuciones numeradas + hoja de ruta) → Related Work (cierra con "drawbacks of all reviewed works") → Proposed System (Motivation & Objectives, Architecture, Design/Implementation, Development Methodology) → Assessment/Evaluation → Discussion → Conclusions and Future Work.
- Hoja de ruta fija: "The remainder of this [paper] is organised as follows. Section~2 presents… Finally, Section~N outlines our conclusions and future work."

## Conectores favoritos
However, Therefore, In addition, Moreover, Furthermore, Thus, Consequently, On the other hand, Likewise, In fact, Nonetheless, Nevertheless, Finally, Regarding, Nowadays, Hence, It should be noted that, To counteract the disadvantages of…

## Convenciones de formato
- Acrónimos: "Term (ACRONYM)". Ortografía británica (organised, behaviour, favourable).
- Referencias cruzadas: "Table~X", "Figure~X shows…", "Section~X". Números pequeños en palabra; porcentajes 2 decimales.

## Errores nativos a CORREGIR (no reproducir)
- "such us"→"such as"; "indoor quality air"→"indoor air quality"; "The remaining of the paper"→"The remainder".
- Concordancia ("this work analysis"→"analyses"); artículo omitido ("development of system"→"of the system").
- Comas empalmadas; punto antes de "However". Barras de género → they/their. Coma decimal española → punto. Mantener británica.