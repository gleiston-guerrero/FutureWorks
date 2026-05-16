"""
Ilustración 5: Diagrama de Base de datos Kiddy Quiz
Modelo entidad-relación de las principales tablas del sistema.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

COLOR_HEADER = "#1F6E43"
COLOR_BG = "#FFFFFF"
COLOR_BORDE = "#0F4C2A"
COLOR_PK = "#0F4C2A"
COLOR_FK = "#5BC290"

ax.text(8, 11.6, "Modelo de base de datos – Kiddy Quiz",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_HEADER)

def tabla(ax, x, y, nombre, campos, w=2.8):
    """Dibuja una tabla del MER con encabezado y campos."""
    h_header = 0.45
    h_field = 0.30
    h_total = h_header + len(campos) * h_field

    # Fondo
    rect = Rectangle((x, y - h_total), w, h_total,
                      facecolor=COLOR_BG, edgecolor=COLOR_BORDE, linewidth=1.4)
    ax.add_patch(rect)
    # Header
    header = Rectangle((x, y - h_header), w, h_header,
                        facecolor=COLOR_HEADER, edgecolor=COLOR_BORDE, linewidth=1.4)
    ax.add_patch(header)
    ax.text(x + w/2, y - h_header/2, nombre, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='white')

    # Campos
    for i, (tipo, campo) in enumerate(campos):
        y_field = y - h_header - (i + 0.5) * h_field
        marker = ""
        color_txt = "#1A1A1A"
        weight = "normal"
        if tipo == "PK":
            marker = "PK  "
            color_txt = COLOR_PK
            weight = "bold"
        elif tipo == "FK":
            marker = "FK  "
            color_txt = "#3C7B5F"
        ax.text(x + 0.15, y_field, f"{marker}{campo}", ha='left', va='center',
                fontsize=8.5, color=color_txt, fontweight=weight)
    return (x, y, w, h_total)

# Definir tablas (posicionadas en una grilla 3x3)
t_usuario = tabla(ax, 0.5, 10.7, "USUARIO", [
    ("PK", "id_usuario"),
    ("",   "nombres"),
    ("",   "apellidos"),
    ("",   "correo"),
    ("",   "password_hash"),
    ("FK", "id_rol"),
    ("",   "fecha_creacion"),
])

t_rol = tabla(ax, 0.5, 6.2, "ROL", [
    ("PK", "id_rol"),
    ("",   "nombre"),
    ("",   "descripcion"),
])

t_clase = tabla(ax, 4.5, 10.7, "CLASE", [
    ("PK", "id_clase"),
    ("",   "nombre"),
    ("",   "codigo_acceso"),
    ("FK", "id_docente"),
    ("",   "grado_escolar"),
    ("",   "fecha_creacion"),
])

t_inscripcion = tabla(ax, 4.5, 6.2, "INSCRIPCION", [
    ("PK", "id_inscripcion"),
    ("FK", "id_clase"),
    ("FK", "id_estudiante"),
    ("",   "fecha_inscripcion"),
])

t_evaluacion = tabla(ax, 8.5, 10.7, "EVALUACION", [
    ("PK", "id_evaluacion"),
    ("",   "titulo"),
    ("",   "descripcion"),
    ("FK", "id_clase"),
    ("",   "competencia"),
    ("",   "duracion_min"),
    ("",   "fecha_publicacion"),
])

t_pregunta = tabla(ax, 8.5, 6.2, "PREGUNTA", [
    ("PK", "id_pregunta"),
    ("FK", "id_evaluacion"),
    ("",   "enunciado"),
    ("",   "tipo"),
    ("",   "url_multimedia"),
    ("",   "categoria_tema"),
    ("",   "puntaje"),
])

t_opcion = tabla(ax, 12.5, 10.7, "OPCION", [
    ("PK", "id_opcion"),
    ("FK", "id_pregunta"),
    ("",   "texto"),
    ("",   "es_correcta"),
])

t_respuesta = tabla(ax, 12.5, 6.2, "RESPUESTA", [
    ("PK", "id_respuesta"),
    ("FK", "id_pregunta"),
    ("FK", "id_estudiante"),
    ("FK", "id_opcion"),
    ("",   "es_correcta"),
    ("",   "tiempo_resp"),
])

t_resultado = tabla(ax, 4.5, 1.5, "RESULTADO", [
    ("PK", "id_resultado"),
    ("FK", "id_evaluacion"),
    ("FK", "id_estudiante"),
    ("",   "puntaje_total"),
    ("",   "porcentaje"),
    ("",   "fecha"),
])

t_consejo = tabla(ax, 8.5, 1.5, "CONSEJO_IA", [
    ("PK", "id_consejo"),
    ("FK", "id_resultado"),
    ("",   "texto"),
    ("",   "tipo_destino"),
    ("",   "fecha_generado"),
])

# Función para dibujar relaciones (líneas con cardinalidad)
def relacion(ax, x1, y1, x2, y2, c1="1", c2="N"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle='-', color=COLOR_BORDE, lw=1.2))
    # cardinalidades
    ax.text(x1 + (x2 - x1) * 0.12, y1 + (y2 - y1) * 0.12, c1,
            fontsize=8.5, fontweight='bold', color=COLOR_BORDE)
    ax.text(x1 + (x2 - x1) * 0.88, y1 + (y2 - y1) * 0.88, c2,
            fontsize=8.5, fontweight='bold', color=COLOR_BORDE)

# Relaciones
relacion(ax, 1.9, 7.6, 1.9, 5.95)             # Usuario - Rol
relacion(ax, 3.3, 9.6, 4.5, 9.6)              # Usuario - Clase (docente)
relacion(ax, 3.3, 8.0, 4.5, 7.7)              # Usuario - Inscripcion
relacion(ax, 7.3, 9.6, 8.5, 9.6)              # Clase - Evaluacion
relacion(ax, 9.9, 8.4, 9.9, 6.45)             # Evaluacion - Pregunta
relacion(ax, 11.3, 8.5, 12.5, 9.6)            # Pregunta - Opcion
relacion(ax, 11.3, 5.5, 12.5, 7.6)            # Pregunta - Respuesta
relacion(ax, 9.9, 3.7, 9.9, 1.85, c1="1", c2="1")  # Resultado - ConsejoIA
relacion(ax, 5.9, 5.5, 5.9, 2.95)             # Inscripcion - Resultado (vía estudiante)

# Leyenda
ax.text(0.5, 0.5, "PK = Clave primaria    FK = Clave foránea",
        fontsize=9, style='italic', color=COLOR_HEADER)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig05_base_datos.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 5 generada")
