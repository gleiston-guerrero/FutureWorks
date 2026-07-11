# Encuesta demográfica — versión en español

Datos demográficos recolectados de cada tutor antes de la sesión piloto. Todos los campos se responden en formato de opciones cerradas o rangos, y se pseudonimizan antes de ser depositados en el repositorio (véase `../data/data-dictionary.md`).

## Datos del tutor

| Campo | Formato | Categorías |
|-------|---------|------------|
| Edad | rango de 5 años | 25–29, 30–34, 35–39, 40–44, 45–49, 50–54, 55–59, 60–65 |
| Género | opción única | Femenino, Masculino, Otro/prefiero no responder |
| Nivel educativo alcanzado | opción única | Primaria, Secundaria, Superior (técnico), Superior (universitario), Postgrado |
| Ocupación principal | opción única | Trabajo remunerado, Trabajo doméstico no remunerado, Estudiante, Jubilado/a |
| Área de residencia | opción única | Urbana, Rural |
| Tipo de conexión a internet en el domicilio | opción única | Fibra óptica, ADSL, Datos móviles, Mixta |
| Tiempo diario dedicado a supervisar las tareas escolares del/de la niño/a | horas | Valor decimal 0.5 a 4 h |

## Datos del/de la estudiante monitoreado/a

| Campo | Formato | Categorías |
|-------|---------|------------|
| Edad | años cumplidos | 7 a 12 |
| Nivel escolar | opción única | Primaria (1º–6º), Secundaria básica (7º–8º) |

## Notas de aplicación

- La encuesta se aplicó en formato papel al inicio de la sesión.
- No se solicitaron nombres, apellidos, documentos de identidad, direcciones, teléfonos ni correos electrónicos.
- Los datos se transcribieron a un archivo `likert-effectiveness.csv` (véase `../data/raw/`) con el identificador pseudónimo `G01`…`G12`.
