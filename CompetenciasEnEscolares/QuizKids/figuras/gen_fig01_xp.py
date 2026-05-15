"""
Ilustración 1: Metodología XP (Programación Extrema) - Diagrama de fases
Basado en Ganney et al. y adaptado al contexto del proyecto.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# Paleta institucional (verdes UTEQ + apoyos)
COLOR_FASE = "#1F6E43"
COLOR_PRACT = "#E8F1EC"
COLOR_BORDE = "#0F4C2A"
COLOR_TEXT = "#1A1A1A"

# Título
ax.text(7, 8.5, "Metodología de Programación Extrema (XP)",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_BORDE)
ax.text(7, 8.05, "Adaptación al desarrollo individual del proyecto Kiddy Quiz",
        ha='center', va='center', fontsize=10, style='italic', color="#444")

# Fases principales
fases = [
    ("OBTENCIÓN DE\nREQUISITOS", 1.5, 5.5),
    ("DESARROLLO\nDE LA APLICACIÓN", 6.0, 5.5),
    ("PRUEBAS E\nIMPLEMENTACIÓN", 10.5, 5.5),
]
for nombre, x, y in fases:
    box = FancyBboxPatch((x, y), 2.8, 1.4,
                          boxstyle="round,pad=0.05,rounding_size=0.15",
                          facecolor=COLOR_FASE, edgecolor=COLOR_BORDE, linewidth=2)
    ax.add_patch(box)
    ax.text(x + 1.4, y + 0.7, nombre, ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

# Flechas entre fases
for x_start in [4.3, 8.8]:
    arr = FancyArrowPatch((x_start, 6.2), (x_start + 1.7, 6.2),
                           arrowstyle='->', mutation_scale=22,
                           linewidth=2.2, color=COLOR_BORDE)
    ax.add_patch(arr)

# Prácticas asociadas
practicas = [
    ("• Juego de Planificación\n• Historias de Usuario\n• Cliente en sitio\n  (expertos)", 1.5, 1.8),
    ("• Diseño Simple\n• TDD (parcial)\n• Refactorización\n• Control de versiones", 6.0, 1.8),
    ("• Lanzamientos pequeños\n• Pruebas de aceptación\n• Validación SUS / TAM\n• Retroalimentación", 10.5, 1.8),
]
for texto, x, y in practicas:
    box = FancyBboxPatch((x, y), 2.8, 2.4,
                          boxstyle="round,pad=0.05,rounding_size=0.1",
                          facecolor=COLOR_PRACT, edgecolor=COLOR_BORDE,
                          linewidth=1.4, linestyle='-')
    ax.add_patch(box)
    ax.text(x + 0.15, y + 2.15, texto, ha='left', va='top',
            fontsize=9.5, color=COLOR_TEXT)

# Conectores verticales fase -> prácticas
for x_c in [2.9, 7.4, 11.9]:
    ax.plot([x_c, x_c], [5.45, 4.25], color=COLOR_BORDE,
            linewidth=1.5, linestyle='--', alpha=0.7)

# Etiqueta inferior de iteración
ax.annotate("", xy=(12.6, 0.65), xytext=(1.4, 0.65),
            arrowprops=dict(arrowstyle='<->', color=COLOR_BORDE, lw=1.5))
ax.text(7, 0.35, "Ciclos iterativos e incrementales",
        ha='center', va='center', fontsize=10, style='italic', color=COLOR_BORDE)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig01_metodologia_xp.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 1 generada")
