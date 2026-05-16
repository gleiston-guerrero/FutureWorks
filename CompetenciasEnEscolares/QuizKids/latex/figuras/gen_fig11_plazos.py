"""
Ilustración 11: Cumplimiento de plazos Kiddy Quiz
Gráfico que muestra el porcentaje de tareas completadas en cada fase del proyecto.
"""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6.5))

COLOR_PLAN = "#B8B8B8"
COLOR_REAL = "#1F6E43"
COLOR_BORDE = "#0F4C2A"

fases = [
    "Análisis y\nrequisitos",
    "Diseño",
    "Desarrollo",
    "Pruebas y\nvalidación",
    "Documentación",
]
planificado = [100, 100, 100, 100, 100]
real        = [100, 95, 92, 100, 96]

x = np.arange(len(fases))
width = 0.36

bars_plan = ax.bar(x - width/2, planificado, width,
                    label='Planificado (%)', color=COLOR_PLAN,
                    edgecolor=COLOR_BORDE, linewidth=1.0)
bars_real = ax.bar(x + width/2, real, width,
                    label='Real (%)', color=COLOR_REAL,
                    edgecolor=COLOR_BORDE, linewidth=1.0)

# Etiquetas en las barras
for bars, vals in [(bars_plan, planificado), (bars_real, real)]:
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val}%", ha='center', va='bottom',
                fontsize=10, fontweight='bold',
                color=COLOR_BORDE)

# Línea de criterio mínimo (90%)
ax.axhline(y=90, color='#E67E22', linestyle='--', linewidth=1.5,
           label='Criterio de éxito (90%)')

ax.set_xticks(x)
ax.set_xticklabels(fases, fontsize=10)
ax.set_ylabel('Porcentaje de cumplimiento (%)', fontsize=11, fontweight='bold')
ax.set_title('Cumplimiento de plazos por fase del proyecto Kiddy Quiz',
             fontsize=13, fontweight='bold', color=COLOR_BORDE, pad=12)
ax.set_ylim(0, 115)
ax.set_yticks(np.arange(0, 116, 10))
ax.grid(axis='y', linestyle=':', alpha=0.5)
ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)

ax.legend(loc='lower right', fontsize=10, framealpha=0.95)

# Anotación final
ax.text(2, 108, 'Cumplimiento promedio global: 96.6%',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color=COLOR_BORDE,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F1EC',
                  edgecolor=COLOR_BORDE, linewidth=1.2))

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig11_cumplimiento_plazos.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 11 generada")
