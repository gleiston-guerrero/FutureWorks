"""
Ilustración 3: Diagrama de casos de uso de Kiddy Quiz
Representa interacciones entre los actores (Estudiante, Docente) y el sistema.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle
import numpy as np

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

COLOR_USE = "#E8F1EC"
COLOR_BORDE_USE = "#1F6E43"
COLOR_ACTOR = "#0F4C2A"
COLOR_FRAME = "#1F6E43"

# Título
ax.text(8, 11.5, "Diagrama de casos de uso – Kiddy Quiz",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_FRAME)

# Frame del sistema
system_box = Rectangle((3.5, 0.8), 9, 10, linewidth=2.2,
                        edgecolor=COLOR_FRAME, facecolor='none', linestyle='-')
ax.add_patch(system_box)
ax.text(8, 10.55, "Sistema Kiddy Quiz", ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_FRAME, style='italic')

# Función para dibujar actor (stick figure)
def dibujar_actor(ax, x, y, etiqueta):
    # Cabeza
    head = plt.Circle((x, y + 1.0), 0.18, color=COLOR_ACTOR, fill=False, linewidth=2)
    ax.add_patch(head)
    # Cuerpo
    ax.plot([x, x], [y + 0.82, y + 0.25], color=COLOR_ACTOR, linewidth=2)
    # Brazos
    ax.plot([x - 0.35, x + 0.35], [y + 0.65, y + 0.65], color=COLOR_ACTOR, linewidth=2)
    # Piernas
    ax.plot([x, x - 0.25], [y + 0.25, y - 0.1], color=COLOR_ACTOR, linewidth=2)
    ax.plot([x, x + 0.25], [y + 0.25, y - 0.1], color=COLOR_ACTOR, linewidth=2)
    # Etiqueta
    ax.text(x, y - 0.4, etiqueta, ha='center', va='center',
            fontsize=11, fontweight='bold', color=COLOR_ACTOR)

# Actores
dibujar_actor(ax, 1.5, 5.5, "Estudiante")
dibujar_actor(ax, 14.5, 5.5, "Docente")

# Casos de uso del estudiante (lado izquierdo del frame)
casos_estudiante = [
    ("Ingresar a clase", 5.0, 9.3),
    ("Ver evaluación", 5.0, 8.3),
    ("Resolver evaluación", 5.0, 7.3),
    ("Ver retroalimentación", 5.0, 6.3),
    ("Ver mapa de competencias", 5.0, 5.3),
    ("Aplicar gamificación", 5.0, 4.3),
]

# Casos de uso del docente (lado derecho del frame)
casos_docente = [
    ("Gestionar panel docente", 11.0, 9.3),
    ("Crear examen", 11.0, 8.3),
    ("Organizar preguntas", 11.0, 7.3),
    ("Configurar contenido", 11.0, 6.3),
    ("Adjuntar archivos\nmultimedia", 11.0, 5.3),
    ("Consultar alumnos", 11.0, 4.3),
    ("Analizar calificaciones", 11.0, 3.3),
    ("Identificar brechas\nde aprendizaje", 11.0, 2.3),
    ("Recibir consejos IA", 11.0, 1.3),
]

def dibujar_caso(ax, x, y, etiqueta, ancho=2.4, alto=0.55):
    el = Ellipse((x, y), ancho, alto, facecolor=COLOR_USE,
                  edgecolor=COLOR_BORDE_USE, linewidth=1.4)
    ax.add_patch(el)
    ax.text(x, y, etiqueta, ha='center', va='center', fontsize=8.5,
            color="#1A1A1A")

for nombre, x, y in casos_estudiante:
    dibujar_caso(ax, x, y, nombre)
    # Línea conectora desde el actor estudiante
    ax.plot([2.0, x - 1.2], [5.5, y], color=COLOR_ACTOR,
            linewidth=0.8, alpha=0.55)

for nombre, x, y in casos_docente:
    dibujar_caso(ax, x, y, nombre, ancho=2.6, alto=0.65)
    # Línea conectora desde el actor docente
    ax.plot([14.0, x + 1.3], [5.5, y], color=COLOR_ACTOR,
            linewidth=0.8, alpha=0.55)

# Relación <<include>> entre "Resolver evaluación" y "Ver retroalimentación"
ax.annotate("", xy=(5.0, 6.6), xytext=(5.0, 7.0),
            arrowprops=dict(arrowstyle='->', linestyle='--', color="#666"))
ax.text(5.55, 6.85, "«include»", fontsize=7.5, style='italic', color="#666")

# Relación <<include>> entre "Identificar brechas" y "Recibir consejos IA"
ax.annotate("", xy=(11.0, 1.6), xytext=(11.0, 2.0),
            arrowprops=dict(arrowstyle='->', linestyle='--', color="#666"))
ax.text(11.55, 1.85, "«include»", fontsize=7.5, style='italic', color="#666")

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig03_casos_uso.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 3 generada")
