"""
Ilustración 4: Diagrama de arquitectura de Kiddy Quiz
Arquitectura cliente-servidor con Angular, NestJS, PostgreSQL y Gemini AI.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 15)
ax.set_ylim(0, 10)
ax.axis('off')

# Paleta
COLOR_CLIENTE = "#3FAA73"
COLOR_SERVIDOR = "#1F6E43"
COLOR_DATOS = "#0F4C2A"
COLOR_EXTERNO = "#5BC290"
COLOR_BORDE = "#0F4C2A"
COLOR_BG_CAPA = "#F0F7F2"

# Título
ax.text(7.5, 9.5, "Arquitectura del sistema Kiddy Quiz",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_BORDE)

# Capas (rectángulos de fondo)
capas = [
    ("CAPA DE PRESENTACIÓN", 0.5, 7.0, 14, 1.6),
    ("CAPA DE LÓGICA DE NEGOCIO", 0.5, 4.4, 14, 1.9),
    ("CAPA DE DATOS Y SERVICIOS EXTERNOS", 0.5, 1.2, 14, 2.3),
]
for nombre, x, y, w, h in capas:
    bg = Rectangle((x, y), w, h, facecolor=COLOR_BG_CAPA,
                    edgecolor=COLOR_BORDE, linewidth=1.0, linestyle='--')
    ax.add_patch(bg)
    ax.text(x + 0.15, y + h - 0.22, nombre, fontsize=8.5, fontweight='bold',
            color=COLOR_BORDE, style='italic')

# Componentes capa de presentación
def caja(ax, x, y, w, h, texto, color, color_texto='white', tam=10):
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.04,rounding_size=0.12",
                          facecolor=color, edgecolor=COLOR_BORDE, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, texto, ha='center', va='center',
            fontsize=tam, fontweight='bold', color=color_texto)

# Presentación
caja(ax, 2.5, 7.3, 4.2, 1.0, "Frontend Angular\n(Estudiante)", COLOR_CLIENTE)
caja(ax, 8.3, 7.3, 4.2, 1.0, "Frontend Angular\n(Docente)", COLOR_CLIENTE)

# Lógica de negocio
caja(ax, 1.0, 5.4, 2.6, 0.7, "Auth\n(JWT)", COLOR_SERVIDOR, tam=9)
caja(ax, 4.0, 5.4, 2.6, 0.7, "Evaluaciones", COLOR_SERVIDOR, tam=9)
caja(ax, 7.0, 5.4, 2.6, 0.7, "Reportes", COLOR_SERVIDOR, tam=9)
caja(ax, 10.0, 5.4, 2.6, 0.7, "Gestión de\nusuarios", COLOR_SERVIDOR, tam=9)
ax.text(13.5, 5.75, "API REST\nNestJS", ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_BORDE, style='italic')

# Datos y servicios externos
caja(ax, 1.5, 1.7, 4.0, 1.4, "PostgreSQL\nBase de datos relacional", COLOR_DATOS)
caja(ax, 6.5, 1.7, 3.5, 1.4, "Gemini AI\nRetroalimentación", COLOR_EXTERNO)
caja(ax, 11.0, 1.7, 3.0, 1.4, "Storage\nMultimedia", COLOR_EXTERNO)

# Flechas de comunicación
def flecha(x1, y1, x2, y2, etiqueta="", offset_x=0, offset_y=0):
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='<->', mutation_scale=14,
                           linewidth=1.6, color=COLOR_BORDE)
    ax.add_patch(arr)
    if etiqueta:
        ax.text((x1 + x2)/2 + offset_x, (y1 + y2)/2 + offset_y, etiqueta,
                fontsize=8, style='italic', color="#555",
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor='none', alpha=0.85))

# Cliente -> API
flecha(4.6, 7.3, 4.6, 6.1, "HTTPS / JSON", offset_x=-0.7)
flecha(10.4, 7.3, 10.4, 6.1, "HTTPS / JSON", offset_x=0.7)

# API -> Datos
flecha(3.5, 5.4, 3.5, 3.1, "ORM / SQL", offset_x=-0.55)
flecha(8.3, 5.4, 8.3, 3.1, "API key", offset_x=0.55)
flecha(12.5, 5.4, 12.5, 3.1, "S3 / FS", offset_x=0.5)

# Etiquetas auxiliares
ax.text(0.5, 0.5, "Pictogramas + accesibilidad infantil",
        ha='left', va='center', fontsize=9, style='italic', color="#444")
ax.text(14.5, 0.5, "Roles: Estudiante / Docente / Admin",
        ha='right', va='center', fontsize=9, style='italic', color="#444")

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig04_arquitectura.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 4 generada")
