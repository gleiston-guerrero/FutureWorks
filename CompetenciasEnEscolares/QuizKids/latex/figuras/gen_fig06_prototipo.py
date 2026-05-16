"""
Ilustración 6: Prototipo final de la aplicación web Kiddy Quiz
Mockup de la pantalla de inicio del estudiante (vista principal con pictogramas).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
import numpy as np

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Paleta amigable infantil
COLOR_FONDO = "#F5F8FF"
COLOR_NAV = "#1F6E43"
COLOR_PRIM = "#FFB347"   # naranja cálido
COLOR_SEC = "#5BC290"    # verde
COLOR_INFO = "#5DADE2"   # azul
COLOR_TEXT = "#1A1A1A"
COLOR_BORDE = "#0F4C2A"

# Marco navegador
nav = FancyBboxPatch((0.3, 0.3), 15.4, 9.4,
                      boxstyle="round,pad=0.04,rounding_size=0.18",
                      facecolor=COLOR_FONDO, edgecolor="#888", linewidth=1.5)
ax.add_patch(nav)

# Barra superior del navegador (botones)
top_bar = Rectangle((0.3, 9.1), 15.4, 0.6, facecolor="#E8E8E8",
                     edgecolor="#888", linewidth=1.0)
ax.add_patch(top_bar)
for i, c in enumerate(["#FF6B6B", "#FFD93D", "#6BCB77"]):
    Circle((0.7 + i*0.35, 9.4), 0.13, facecolor=c, edgecolor='none')
    ax.add_patch(Circle((0.7 + i*0.35, 9.4), 0.13, facecolor=c, edgecolor='none'))
ax.text(8, 9.4, "https://kiddyquiz.app/dashboard", ha='center', va='center',
        fontsize=8.5, color="#555", family='monospace',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#CCC'))

# Header de la app
header = Rectangle((0.3, 8.1), 15.4, 1.0, facecolor=COLOR_NAV, edgecolor='none')
ax.add_patch(header)
ax.text(0.7, 8.6, "Kiddy Quiz", ha='left', va='center',
        fontsize=18, fontweight='bold', color='white')
ax.text(13.0, 8.6, "Hola, Sofía  |  Cerrar sesión", ha='left', va='center',
        fontsize=9, color='white')

# Saludo central
ax.text(8, 7.4, "¡Bienvenida! ¿Qué quieres hacer hoy?",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_NAV)

# Tarjetas con pictogramas grandes (3 botones principales)
def tarjeta(ax, x, y, w, h, color, icono_dibujo, titulo):
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.04,rounding_size=0.2",
                          facecolor=color, edgecolor=COLOR_BORDE, linewidth=2)
    ax.add_patch(box)
    icono_dibujo(ax, x + w/2, y + h*0.62)
    ax.text(x + w/2, y + 0.55, titulo, ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')

# Pictograma 1: lápiz (Hacer evaluación)
def picto_lapiz(ax, cx, cy):
    poly = Polygon([(cx-0.25, cy-0.55), (cx+0.05, cy+0.45),
                    (cx+0.4, cy+0.35), (cx+0.1, cy-0.65)],
                    closed=True, facecolor='white', edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(poly)
    # punta
    poly2 = Polygon([(cx-0.25, cy-0.55), (cx-0.05, cy-0.85), (cx+0.1, cy-0.65)],
                    closed=True, facecolor='#444', edgecolor=COLOR_BORDE, linewidth=1.2)
    ax.add_patch(poly2)

# Pictograma 2: trofeo (Ver resultados)
def picto_trofeo(ax, cx, cy):
    cup = FancyBboxPatch((cx-0.4, cy-0.3), 0.8, 0.7,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          facecolor='#FFD700', edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(cup)
    base = Rectangle((cx-0.2, cy-0.7), 0.4, 0.18, facecolor='#FFD700',
                      edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(base)
    base2 = Rectangle((cx-0.35, cy-0.85), 0.7, 0.15, facecolor='#FFD700',
                       edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(base2)
    ax.text(cx, cy + 0.05, "★", ha='center', va='center',
            fontsize=18, color=COLOR_BORDE)

# Pictograma 3: libro (Mis clases)
def picto_libro(ax, cx, cy):
    book = FancyBboxPatch((cx-0.5, cy-0.4), 1.0, 0.85,
                           boxstyle="round,pad=0.02,rounding_size=0.05",
                           facecolor='white', edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(book)
    # Línea central
    ax.plot([cx, cx], [cy-0.4, cy+0.45], color=COLOR_BORDE, linewidth=1.5)
    # Líneas de texto simuladas
    for dy in [0.2, 0.05, -0.1, -0.25]:
        ax.plot([cx-0.35, cx-0.1], [cy+dy, cy+dy], color="#999", linewidth=1)
        ax.plot([cx+0.1, cx+0.35], [cy+dy, cy+dy], color="#999", linewidth=1)

tarjeta(ax, 1.0, 2.0, 4.2, 4.6, COLOR_PRIM, picto_lapiz, "Hacer evaluación")
tarjeta(ax, 5.9, 2.0, 4.2, 4.6, COLOR_SEC, picto_trofeo, "Ver mis logros")
tarjeta(ax, 10.8, 2.0, 4.2, 4.6, COLOR_INFO, picto_libro, "Mis clases")

# Footer
ax.text(8, 1.0, "Diseño con pictogramas grandes y colores cálidos para navegación autónoma",
        ha='center', va='center', fontsize=9, style='italic', color="#555")

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig06_prototipo_final.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 6 generada")
