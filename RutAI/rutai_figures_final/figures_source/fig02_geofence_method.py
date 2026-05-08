"""
Figure 2 — Geofence experiment schematic.
Illustrates how a geofence is defined, what counts as TP/FP/TN/FN,
and how triggers are collapsed to independent observations.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5),
                          gridspec_kw={'width_ratios': [1.05, 1]})

# ════════════════════════════════════════════════════════
# LEFT PANEL: Geometry of TP / FP / TN
# ════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.4, 1.4)
ax.set_aspect('equal')
ax.set_title('(a) Geofence geometry and trigger labels',
             fontsize=11, fontweight='bold', pad=10)

# Geofence circle (radius = 1)
circle = Circle((0, 0), 1.0, fill=True, facecolor='#D5E8F0',
                edgecolor='#2E4057', linewidth=1.6, alpha=0.6)
ax.add_patch(circle)
# Center
ax.plot(0, 0, 'X', color='#2E4057', markersize=12, markeredgewidth=2)
ax.annotate('POI centroid', xy=(0, 0), xytext=(0.05, -0.20),
            fontsize=9, color='#1F2937', fontweight='bold')

# Radius indicator
ax.plot([0, 0.707], [0, 0.707], color='#2E4057', linewidth=1, linestyle='--')
ax.text(0.45, 0.50, 'R', fontsize=11, fontweight='bold', color='#2E4057',
        style='italic')

# Sample positions
positions = [
    # (x, y, label, color, marker, kind)
    (-0.55, 0.35, 'TP', '#2E7D32', 'o', 'inside, app fires'),
    (0.65, -0.35, 'TP', '#2E7D32', 'o', None),
    ( 1.10, 0.30, 'FP', '#C62828', '^', 'outside, app fires (boundary error)'),
    ( 0.90, -0.85, 'TP', '#2E7D32', 'o', None),
    (-1.25, 0.55, 'TN', '#1565C0', 's', 'outside, app silent'),
    (-1.20, -0.65, 'TN', '#1565C0', 's', None),
    ( 1.05, 0.85, 'TN', '#1565C0', 's', None),
]

for (x, y, lab, col, mk, descr) in positions:
    ax.scatter([x], [y], color=col, marker=mk, s=110,
               edgecolor='black', linewidth=0.6, zorder=5)
    if descr:
        # text annotation outside
        ax.annotate(f'{lab}: {descr}', xy=(x, y),
                    xytext=(x + (0.05 if x >= 0 else -0.05), y + 0.13),
                    fontsize=7.5, color=col, fontweight='bold',
                    ha='left' if x >= 0 else 'right')

ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)

# Legend
legend_items = [
    ('TP — true positive', '#2E7D32', 'o'),
    ('FP — false positive', '#C62828', '^'),
    ('TN — true negative', '#1565C0', 's'),
]
for i, (lab, col, mk) in enumerate(legend_items):
    ax.scatter([-1.45], [-1.05 + i*0.13], color=col, marker=mk,
               s=70, edgecolor='black', linewidth=0.5)
    ax.text(-1.35, -1.05 + i*0.13, lab, fontsize=8, va='center')

# ════════════════════════════════════════════════════════
# RIGHT PANEL: Pseudoreplication collapse
# ════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('(b) Trigger collapse to independent observations',
             fontsize=11, fontweight='bold', pad=10)

# Top: raw triggers timeline
ax.text(5, 9.3, 'Raw trigger stream during one POI × radius × session crossing',
        ha='center', fontsize=9.5, fontweight='bold', color='#2E4057')

t_positions = [1.0, 1.7, 2.4, 3.1, 3.8, 4.5, 5.2]
t_labels = ['t₁', 't₂', 't₃', 't₄', 't₅', 't₆', 't₇']
t_colors = ['#2E7D32']*5 + ['#C62828']*1 + ['#2E7D32']*1

for i, (x, lab, col) in enumerate(zip(t_positions, t_labels, t_colors)):
    ax.scatter([x], [7.8], color=col, marker='o', s=100,
               edgecolor='black', linewidth=0.5, zorder=4)
    ax.text(x, 7.45, lab, ha='center', fontsize=8, color='#374151')

# Time axis
ax.add_patch(FancyArrowPatch((0.6, 7.8), (5.7, 7.8), arrowstyle='->',
                              color='#9CA3AF', linewidth=0.8))
ax.text(6.2, 7.8, 'time', fontsize=8, color='#6B7280', va='center', style='italic')

# Annotation
ax.text(3.1, 7.05, '7 raw triggers (6 TP, 1 FP) — all within ~10 s',
        ha='center', fontsize=8, style='italic', color='#6B7280')

# Down arrow
ax.add_patch(FancyArrowPatch((5, 6.5), (5, 5.4), arrowstyle='->',
                              color='#2E4057', linewidth=2, mutation_scale=18))
ax.text(5.3, 5.95, 'collapse rule:\ndominant label per\n(POI × radius × session)',
        fontsize=8, color='#1F2937', va='center', style='italic')

# Bottom: collapsed observation
ax.add_patch(FancyBboxPatch((3.5, 3.6), 3, 1.4,
    boxstyle="round,pad=0.05,rounding_size=0.1",
    linewidth=1.4, edgecolor='#2E4057', facecolor='#E8F0D5'))
ax.text(5, 4.55, 'One independent observation',
        ha='center', fontsize=9.5, fontweight='bold', color='#1F2937')
ax.text(5, 4.10, 'label = TP  (dominant)',
        ha='center', fontsize=9, color='#2E7D32', fontweight='bold')
ax.text(5, 3.78, 'n_raw_triggers = 7',
        ha='center', fontsize=8, color='#6B7280', style='italic')

# Footer note
ax.text(5, 2.55, 'After collapsing: 139 raw triggers  →  78 independent observations',
        ha='center', fontsize=10, fontweight='bold', color='#2E4057',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3CD',
                  edgecolor='#D4A72C', linewidth=1.2))

ax.text(5, 1.50,
        'Wilson 95% CIs and McNemar tests reported on collapsed data.',
        ha='center', fontsize=8.5, color='#374151', style='italic')

plt.tight_layout()
plt.savefig('/home/claude/rutai_figures/Figure_02_geofence_method.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_02_geofence_method.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 2 generated.")
