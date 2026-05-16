"""
Ilustración 12: Gráfico de barras SUS - Resultados de usabilidad
Compara puntuaciones de docentes y estudiantes contra el umbral mínimo de 68 (SUS).
Datos de Tabla 27: Estudiantes media=87.7, mediana=87.5; Docentes media=81.0, mediana=82.5
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(11, 6.8))

COLOR_EST = "#1F6E43"
COLOR_DOC = "#5BC290"
COLOR_BORDE = "#0F4C2A"

# Categorías y datos
metricas = ["Media", "Mediana", "Valor mínimo", "Valor máximo"]
estudiantes = [87.7, 87.5, 80.0, 95.0]
docentes    = [81.0, 82.5, 67.5, 95.0]

x = np.arange(len(metricas))
width = 0.36

bars_est = ax.bar(x - width/2, estudiantes, width,
                   label='Estudiantes (N=15)', color=COLOR_EST,
                   edgecolor=COLOR_BORDE, linewidth=1.2)
bars_doc = ax.bar(x + width/2, docentes, width,
                   label='Docentes (N=5)', color=COLOR_DOC,
                   edgecolor=COLOR_BORDE, linewidth=1.2)

# Etiquetas sobre las barras
for bars, vals in [(bars_est, estudiantes), (bars_doc, docentes)]:
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f"{val:.1f}", ha='center', va='bottom',
                fontsize=10.5, fontweight='bold', color=COLOR_BORDE)

# Línea de umbral mínimo SUS = 68
ax.axhline(y=68, color='#E74C3C', linestyle='--', linewidth=1.8,
           label='Umbral mínimo aceptable (68)')

# Banda de "Excelente" (>= 80.3 según Bangor et al.)
ax.axhspan(80.3, 100, alpha=0.10, color='#27AE60')
ax.text(3.4, 92, 'Zona de\nexcelencia', ha='center', va='center',
        fontsize=8.5, style='italic', color='#27AE60',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='#27AE60', linewidth=0.8))

ax.set_xticks(x)
ax.set_xticklabels(metricas, fontsize=11)
ax.set_ylabel('Puntuación SUS (escala 0-100)', fontsize=11, fontweight='bold')
ax.set_title('Resultados del cuestionario SUS – Aplicación Kiddy Quiz',
             fontsize=13, fontweight='bold', color=COLOR_BORDE, pad=14)
ax.set_ylim(0, 105)
ax.set_yticks(np.arange(0, 106, 10))
ax.grid(axis='y', linestyle=':', alpha=0.5)
ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)

ax.legend(loc='lower right', fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig12_grafico_sus.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 12 generada")
