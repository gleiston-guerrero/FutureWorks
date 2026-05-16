"""
Ilustración 7: Módulo de estudiantes (Kiddy Quiz)
Pantalla de resolución de evaluación con pictograma y opciones múltiples.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Paleta
COLOR_FONDO = "#FFF7E6"
COLOR_NAV = "#1F6E43"
COLOR_OPCION = "#FFFFFF"
COLOR_OPCION_SEL = "#5BC290"
COLOR_BORDE = "#0F4C2A"

# Marco navegador
nav = FancyBboxPatch((0.3, 0.3), 15.4, 9.4,
                      boxstyle="round,pad=0.04,rounding_size=0.18",
                      facecolor=COLOR_FONDO, edgecolor="#888", linewidth=1.5)
ax.add_patch(nav)

# Header con barra de progreso
header = Rectangle((0.3, 8.2), 15.4, 1.5, facecolor=COLOR_NAV, edgecolor='none')
ax.add_patch(header)
ax.text(0.7, 9.2, "Kiddy Quiz - Evaluación: Sumas hasta 100", ha='left', va='center',
        fontsize=13, fontweight='bold', color='white')
ax.text(0.7, 8.7, "Pregunta 3 de 10", ha='left', va='center',
        fontsize=10, color='#E0E0E0')

# Barra de progreso
prog_bg = Rectangle((10.5, 8.55), 4.8, 0.3, facecolor='#FFFFFF20', edgecolor='white')
ax.add_patch(prog_bg)
prog = Rectangle((10.5, 8.55), 1.44, 0.3, facecolor='#FFD700', edgecolor='none')
ax.add_patch(prog)
ax.text(15.4, 8.7, "30%", ha='right', va='center', fontsize=10, color='white', fontweight='bold')

# Enunciado de la pregunta
enun = FancyBboxPatch((1.0, 6.0), 14.0, 1.7,
                       boxstyle="round,pad=0.05,rounding_size=0.15",
                       facecolor='white', edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(enun)
ax.text(8, 7.1, "Si Sofía tiene 25 manzanas y le regalan 18 más,",
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1A1A1A')
ax.text(8, 6.5, "¿cuántas manzanas tiene en total?",
        ha='center', va='center', fontsize=14, fontweight='bold', color='#1A1A1A')

# Pictograma de manzanas (apoyo visual)
def manzana(ax, cx, cy, r=0.18):
    body = Circle((cx, cy), r, facecolor='#E74C3C', edgecolor='#922B21', linewidth=1)
    ax.add_patch(body)
    # hoja
    leaf = Polygon([(cx, cy + r), (cx + r*0.6, cy + r*1.3), (cx + r*0.2, cy + r*1.4)],
                    closed=True, facecolor='#27AE60', edgecolor='#1E8449')
    ax.add_patch(leaf)

# Grupo 1: 5 manzanas
for i in range(5):
    manzana(ax, 3.0 + i*0.5, 5.3)
ax.text(2.0, 5.3, "25 +", ha='center', va='center', fontsize=22, fontweight='bold', color=COLOR_NAV)

# Grupo 2: 4 manzanas
for i in range(4):
    manzana(ax, 8.5 + i*0.5, 5.3)
ax.text(7.5, 5.3, "18 =", ha='center', va='center', fontsize=22, fontweight='bold', color=COLOR_NAV)
ax.text(11.5, 5.3, "?", ha='center', va='center', fontsize=28, fontweight='bold', color="#E67E22")

# Opciones de respuesta (4 botones grandes con pictogramas)
opciones = [
    ("A", "33", 1.5, 2.5, COLOR_OPCION, False),
    ("B", "43", 5.4, 2.5, COLOR_OPCION_SEL, True),  # seleccionada
    ("C", "45", 9.3, 2.5, COLOR_OPCION, False),
    ("D", "53", 13.2, 2.5, COLOR_OPCION, False),
]
for letra, valor, x, y, color, sel in opciones:
    edgecolor = COLOR_BORDE if not sel else "#FFD700"
    lw = 2 if not sel else 4
    box = FancyBboxPatch((x, y), 1.6, 1.6,
                          boxstyle="round,pad=0.04,rounding_size=0.18",
                          facecolor=color, edgecolor=edgecolor, linewidth=lw)
    ax.add_patch(box)
    text_color = '#1A1A1A' if not sel else 'white'
    ax.text(x + 0.8, y + 1.2, letra, ha='center', va='center',
            fontsize=11, fontweight='bold', color=text_color)
    ax.text(x + 0.8, y + 0.6, valor, ha='center', va='center',
            fontsize=22, fontweight='bold', color=text_color)

# Botón Siguiente
btn = FancyBboxPatch((12.5, 0.7), 2.8, 1.0,
                      boxstyle="round,pad=0.04,rounding_size=0.15",
                      facecolor='#FFD700', edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(btn)
ax.text(13.9, 1.2, "Siguiente →", ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_BORDE)

# Texto de ayuda
ax.text(0.8, 1.2, "Pista: Suma las manzanas que ves arriba.",
        ha='left', va='center', fontsize=10, style='italic', color='#666')

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig07_modulo_estudiante_eval.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 7 generada")
