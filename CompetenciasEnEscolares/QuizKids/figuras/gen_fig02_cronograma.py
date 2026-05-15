"""
Ilustración 2: Cronograma de actividades - Diagrama de Gantt
Cronograma de 32 semanas distribuidas en las fases del proyecto.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(13, 7.5))

# Paleta institucional
COLOR_FASE1 = "#1F6E43"  # Análisis
COLOR_FASE2 = "#2A8B5A"  # Diseño
COLOR_FASE3 = "#3FAA73"  # Desarrollo
COLOR_FASE4 = "#5BC290"  # Pruebas
COLOR_FASE5 = "#7FD2A8"  # Documentación
COLOR_BORDE = "#0F4C2A"

actividades = [
    # (nombre, semana_inicio, duración, color)
    ("Análisis y estructuración del tema",     1,  3,  COLOR_FASE1),
    ("Revisión bibliográfica y marco teórico", 1,  6,  COLOR_FASE1),
    ("Entrevistas a expertos / psicopedagogos", 3,  3,  COLOR_FASE1),
    ("Levantamiento de requisitos",            5,  3,  COLOR_FASE1),
    ("Diseño de historias de usuario",         6,  3,  COLOR_FASE2),
    ("Diseño de arquitectura del sistema",     7,  3,  COLOR_FASE2),
    ("Diseño de base de datos",                8,  2,  COLOR_FASE2),
    ("Prototipado de interfaces",              8,  3,  COLOR_FASE2),
    ("Desarrollo del backend (NestJS)",       10,  9,  COLOR_FASE3),
    ("Desarrollo del frontend (Angular)",     11,  9,  COLOR_FASE3),
    ("Integración de Gemini AI",              17,  3,  COLOR_FASE3),
    ("Implementación de seguridad (JWT)",     18,  2,  COLOR_FASE3),
    ("Pruebas unitarias y de integración",    20,  3,  COLOR_FASE4),
    ("Pruebas de usabilidad (SUS)",           23,  2,  COLOR_FASE4),
    ("Pruebas de aceptación tecnológica (TAM)", 24, 2,  COLOR_FASE4),
    ("Análisis de resultados",                26,  2,  COLOR_FASE5),
    ("Redacción del documento final",         27,  5,  COLOR_FASE5),
    ("Revisión y ajustes finales",            31,  2,  COLOR_FASE5),
]

# Invertir para que la primera tarea quede arriba
actividades = list(reversed(actividades))

y_positions = np.arange(len(actividades))

for i, (nombre, inicio, dur, color) in enumerate(actividades):
    ax.barh(i, dur, left=inicio - 0.5, height=0.62,
            color=color, edgecolor=COLOR_BORDE, linewidth=0.8)

ax.set_yticks(y_positions)
ax.set_yticklabels([a[0] for a in actividades], fontsize=9)
ax.set_xlim(0, 33)
ax.set_xticks(np.arange(0, 33, 2))
ax.set_xlabel("Semanas del proyecto", fontsize=11, fontweight='bold')
ax.set_title("Cronograma de actividades del proyecto Kiddy Quiz (32 semanas)",
             fontsize=13, fontweight='bold', color=COLOR_BORDE, pad=14)

# Cuadrícula vertical sutil
ax.grid(axis='x', linestyle=':', alpha=0.5, color='gray')
ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)

# Leyenda de fases
legend_handles = [
    mpatches.Patch(color=COLOR_FASE1, label="Fase 1: Análisis y requisitos"),
    mpatches.Patch(color=COLOR_FASE2, label="Fase 2: Diseño"),
    mpatches.Patch(color=COLOR_FASE3, label="Fase 3: Desarrollo"),
    mpatches.Patch(color=COLOR_FASE4, label="Fase 4: Pruebas y validación"),
    mpatches.Patch(color=COLOR_FASE5, label="Fase 5: Documentación"),
]
ax.legend(handles=legend_handles, loc='lower right', fontsize=8.5,
          framealpha=0.95, ncol=1)

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig02_cronograma.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 2 generada")
