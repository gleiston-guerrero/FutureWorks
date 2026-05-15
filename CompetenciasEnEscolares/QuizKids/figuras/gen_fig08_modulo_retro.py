"""
Ilustración 8: Módulo de estudiantes (Kiddy Quiz) - Pantalla de retroalimentación
Pantalla post-evaluación con resultado y mensaje motivacional generado por IA.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Wedge
import numpy as np

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Paleta
COLOR_FONDO = "#F0FFF4"
COLOR_NAV = "#1F6E43"
COLOR_BORDE = "#0F4C2A"
COLOR_GOLD = "#FFD700"

# Marco navegador
nav = FancyBboxPatch((0.3, 0.3), 15.4, 9.4,
                      boxstyle="round,pad=0.04,rounding_size=0.18",
                      facecolor=COLOR_FONDO, edgecolor="#888", linewidth=1.5)
ax.add_patch(nav)

# Header
header = Rectangle((0.3, 8.6), 15.4, 1.1, facecolor=COLOR_NAV, edgecolor='none')
ax.add_patch(header)
ax.text(0.7, 9.15, "Kiddy Quiz - Resultados de tu evaluación", ha='left', va='center',
        fontsize=14, fontweight='bold', color='white')

# Tarjeta del resultado (lado izquierdo) - puntaje circular
score_card = FancyBboxPatch((0.8, 4.0), 6.0, 4.2,
                             boxstyle="round,pad=0.05,rounding_size=0.18",
                             facecolor='white', edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(score_card)

ax.text(3.8, 7.85, "Tu puntaje", ha='center', va='center',
        fontsize=14, fontweight='bold', color=COLOR_NAV)

# Donut chart simulado
center = (3.8, 5.7)
radio_ext = 1.1
radio_int = 0.75
porcentaje = 80  # 8 de 10
# Wedge correcto (verde)
wedge1 = Wedge(center, radio_ext, 90, 90 - 360 * porcentaje/100,
                width=radio_ext - radio_int, facecolor='#5BC290',
                edgecolor=COLOR_BORDE, linewidth=1.2)
# Wedge incorrecto (gris)
wedge2 = Wedge(center, radio_ext, 90 - 360 * porcentaje/100, 90,
                width=radio_ext - radio_int, facecolor='#E0E0E0',
                edgecolor=COLOR_BORDE, linewidth=1.2)
ax.add_patch(wedge1)
ax.add_patch(wedge2)
ax.text(center[0], center[1] + 0.1, "8/10", ha='center', va='center',
        fontsize=22, fontweight='bold', color=COLOR_NAV)
ax.text(center[0], center[1] - 0.35, "80%", ha='center', va='center',
        fontsize=12, color="#555")

# Estrellas decorativas
def estrella(ax, cx, cy, size=0.18, color=COLOR_GOLD):
    angles = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, 11)
    pts = []
    for i, a in enumerate(angles):
        r = size if i % 2 == 0 else size * 0.45
        pts.append((cx + r*np.cos(a), cy + r*np.sin(a)))
    star = Polygon(pts, closed=True, facecolor=color,
                    edgecolor=COLOR_BORDE, linewidth=1)
    ax.add_patch(star)

for i in range(4):
    estrella(ax, 1.8 + i*1.0, 4.4, size=0.22)
estrella(ax, 5.8, 4.4, size=0.22, color='#E0E0E0')  # estrella vacía

# Tarjeta de retroalimentación IA (lado derecho)
ai_card = FancyBboxPatch((7.4, 4.0), 7.9, 4.2,
                          boxstyle="round,pad=0.05,rounding_size=0.18",
                          facecolor='white', edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(ai_card)

# Encabezado de la tarjeta IA
ai_head = Rectangle((7.4, 7.55), 7.9, 0.65, facecolor=COLOR_NAV, edgecolor='none')
ax.add_patch(ai_head)
ax.text(11.35, 7.88, "Mensaje de Gemini AI", ha='center', va='center',
        fontsize=12, fontweight='bold', color='white')

ax.text(7.7, 7.0, "¡Hola, Sofía!", ha='left', va='center',
        fontsize=13, fontweight='bold', color=COLOR_NAV)

# Mensaje generado por IA
mensaje = (
    "¡Excelente trabajo! Resolviste 8 de 10 sumas correctamente.\n"
    "Notamos que las preguntas con números mayores a 50 te tomaron\n"
    "un poquito más de tiempo. ¡No te preocupes! Sigue practicando\n"
    "con los ejercicios del módulo \"Sumas grandes\".\n\n"
    "Tip: cuando sumes números grandes, descompónlos en decenas\n"
    "y unidades. ¡Tú puedes lograrlo, sigue así!"
)
ax.text(7.7, 6.5, mensaje, ha='left', va='top', fontsize=10,
        color='#1A1A1A', linespacing=1.4)

# Barras de áreas evaluadas (parte inferior)
ax.text(0.8, 3.4, "Áreas evaluadas:", ha='left', va='center',
        fontsize=12, fontweight='bold', color=COLOR_NAV)

areas = [
    ("Sumas hasta 50",     95, '#5BC290'),
    ("Sumas hasta 100",    70, '#FFD700'),
    ("Resta básica",       85, '#5BC290'),
    ("Razonamiento lógico", 60, '#FFA500'),
]
y_base = 2.7
for i, (nombre, pct, color) in enumerate(areas):
    y = y_base - i * 0.5
    ax.text(0.8, y, nombre, ha='left', va='center', fontsize=10, color='#1A1A1A')
    bg = Rectangle((4.5, y - 0.18), 8.0, 0.35, facecolor='#E8E8E8',
                    edgecolor='#999', linewidth=0.8)
    ax.add_patch(bg)
    barra = Rectangle((4.5, y - 0.18), 8.0 * pct/100, 0.35,
                       facecolor=color, edgecolor=COLOR_BORDE, linewidth=0.8)
    ax.add_patch(barra)
    ax.text(13.0, y, f"{pct}%", ha='left', va='center',
            fontsize=10, fontweight='bold', color=COLOR_NAV)

# Botones inferiores
btn1 = FancyBboxPatch((4.0, 0.55), 3.5, 0.7,
                       boxstyle="round,pad=0.04,rounding_size=0.12",
                       facecolor='white', edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(btn1)
ax.text(5.75, 0.9, "Volver al inicio", ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_NAV)

btn2 = FancyBboxPatch((8.5, 0.55), 3.5, 0.7,
                       boxstyle="round,pad=0.04,rounding_size=0.12",
                       facecolor=COLOR_GOLD, edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(btn2)
ax.text(10.25, 0.9, "Practicar más →", ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_BORDE)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig08_modulo_estudiante_retro.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 8 generada")
