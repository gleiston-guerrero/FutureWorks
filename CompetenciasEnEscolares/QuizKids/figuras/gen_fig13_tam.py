"""
Ilustración 13: Gráfico de brechas TAM (Dumbbell Plot)
Compara las medias de docentes y estudiantes en las tres dimensiones del modelo TAM.
Datos de Tabla 28:
- PU:   Docentes 4.45 / Estudiantes 4.85
- PEOU: Docentes 3.95 / Estudiantes 4.78
- IU:   Docentes 4.47 / Estudiantes 4.93
"""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6.5))

COLOR_DOC = "#2E5C8A"   # azul
COLOR_EST = "#1F6E43"   # verde
COLOR_BORDE = "#0F4C2A"
COLOR_LINE = "#888"

# Datos
dimensiones = [
    "Utilidad Percibida\n(PU)",
    "Facilidad de Uso\n(PEOU)",
    "Intención de Uso\n(IU)",
]
docentes    = [4.45, 3.95, 4.47]
estudiantes = [4.85, 4.78, 4.93]

y_pos = np.arange(len(dimensiones))

# Línea conectora (dumbbell)
for i in range(len(dimensiones)):
    ax.plot([docentes[i], estudiantes[i]], [y_pos[i], y_pos[i]],
            color=COLOR_LINE, linewidth=2.5, alpha=0.6, zorder=1)

# Puntos
ax.scatter(docentes, y_pos, s=400, color=COLOR_DOC,
           edgecolor=COLOR_BORDE, linewidth=1.8, zorder=3,
           label='Docentes (N=5)')
ax.scatter(estudiantes, y_pos, s=400, color=COLOR_EST,
           edgecolor=COLOR_BORDE, linewidth=1.8, zorder=3,
           label='Estudiantes (N=15)')

# Etiquetas de valor
for i in range(len(dimensiones)):
    # Docentes (a la izquierda del punto)
    ax.text(docentes[i] - 0.05, y_pos[i], f"{docentes[i]:.2f}",
            ha='right', va='center', fontsize=10.5, fontweight='bold',
            color=COLOR_DOC)
    # Estudiantes (a la derecha del punto)
    ax.text(estudiantes[i] + 0.05, y_pos[i], f"{estudiantes[i]:.2f}",
            ha='left', va='center', fontsize=10.5, fontweight='bold',
            color=COLOR_EST)
    # Brecha (en el centro del segmento)
    cx = (docentes[i] + estudiantes[i]) / 2
    brecha = abs(estudiantes[i] - docentes[i])
    ax.text(cx, y_pos[i] + 0.22, f"Δ {brecha:.2f}",
            ha='center', va='bottom', fontsize=9, style='italic',
            color="#444",
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor='none', alpha=0.9))

# Configuración del eje
ax.set_yticks(y_pos)
ax.set_yticklabels(dimensiones, fontsize=11)
ax.set_xlabel('Puntuación media (escala Likert 1-5)', fontsize=11, fontweight='bold')
ax.set_title('Gráfico de brechas TAM – Comparación docentes vs. estudiantes',
             fontsize=13, fontweight='bold', color=COLOR_BORDE, pad=14)
ax.set_xlim(3.5, 5.15)
ax.set_xticks(np.arange(3.5, 5.1, 0.25))
ax.invert_yaxis()
ax.grid(axis='x', linestyle=':', alpha=0.5)
ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)

# Línea de máximo absoluto
ax.axvline(x=5.0, color='#E74C3C', linestyle='--', linewidth=1.2, alpha=0.5)
ax.text(5.01, len(dimensiones) - 0.3, 'Máx.\nescala',
        fontsize=8, color='#E74C3C', style='italic')

ax.legend(loc='lower left', fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig13_grafico_tam.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 13 generada")
