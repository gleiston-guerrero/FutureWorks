"""
Figure 4 — Geofence accuracy by radius (Wilson 95% CIs).
Visualizes Table 1 in the paper.
"""
import matplotlib.pyplot as plt
import numpy as np

# Real values from collapsed dataset (n = 78)
radii = [50, 100, 200]
precision_mean = [0.818, 0.870, 1.000]
precision_lo = [0.615, 0.679, 0.839]
precision_hi = [0.927, 0.955, 1.000]

recall_mean = [1.000, 1.000, 1.000]
recall_lo = [0.824, 0.839, 0.839]
recall_hi = [1.000, 1.000, 1.000]

f1 = [0.900, 0.930, 1.000]

# n per radius
n_per = [28, 30, 20]
tp = [18, 20, 20]
fp = [4, 3, 0]
tn = [6, 7, 0]
fn = [0, 0, 0]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.8))

# ─── PANEL A: Precision and Recall with CIs ─────────────
ax = axes[0]
x = np.arange(len(radii))
w = 0.35

# Precision bars with error bars
prec_err_lo = [precision_mean[i] - precision_lo[i] for i in range(3)]
prec_err_hi = [precision_hi[i] - precision_mean[i] for i in range(3)]
ax.bar(x - w/2, precision_mean, width=w, color='#2E7D32', alpha=0.85,
       label='Precision', edgecolor='black', linewidth=0.6,
       yerr=[prec_err_lo, prec_err_hi], capsize=6,
       error_kw={'elinewidth': 1.5, 'ecolor': '#1F2937'})

# Recall bars with error bars
rec_err_lo = [recall_mean[i] - recall_lo[i] for i in range(3)]
rec_err_hi = [recall_hi[i] - recall_mean[i] for i in range(3)]
ax.bar(x + w/2, recall_mean, width=w, color='#1565C0', alpha=0.85,
       label='Recall', edgecolor='black', linewidth=0.6,
       yerr=[rec_err_lo, rec_err_hi], capsize=6,
       error_kw={'elinewidth': 1.5, 'ecolor': '#1F2937'})

# Reference line
ax.axhline(0.9, color='#6B7280', linestyle=':', linewidth=1, alpha=0.7)
ax.text(2.45, 0.905, '0.90', fontsize=8, color='#6B7280', va='bottom')

# Annotations on bars
for i, (xi, p, r) in enumerate(zip(x, precision_mean, recall_mean)):
    ax.text(xi - w/2, p + prec_err_hi[i] + 0.02, f'{p:.3f}',
            ha='center', fontsize=8.5, fontweight='bold', color='#2E7D32')
    ax.text(xi + w/2, r + rec_err_hi[i] + 0.02, f'{r:.3f}',
            ha='center', fontsize=8.5, fontweight='bold', color='#1565C0')

ax.set_xticks(x)
ax.set_xticklabels([f'{r} m' for r in radii])
ax.set_xlabel('Geofence radius', fontsize=10.5, fontweight='bold')
ax.set_ylabel('Metric value', fontsize=10.5, fontweight='bold')
ax.set_ylim(0.55, 1.10)
ax.set_yticks(np.arange(0.6, 1.11, 0.1))
ax.legend(loc='lower right', fontsize=9.5, framealpha=0.95)
ax.set_title('(a) Precision and recall with Wilson 95% CIs',
             fontsize=11, fontweight='bold')
ax.grid(True, axis='y', linestyle=':', alpha=0.3)
ax.set_axisbelow(True)

# Sample size annotations under x labels — placed in axis-coords below the labels
for i, (xi, n_i) in enumerate(zip(x, n_per)):
    ax.text(xi, -0.10, f'n = {n_i}', ha='center', fontsize=8, color='#6B7280',
            transform=ax.get_xaxis_transform())

# ─── PANEL B: Confusion matrix counts ───────────────────
ax = axes[1]
data = np.array([tp, fp, tn, fn])
labels = ['TP', 'FP', 'TN', 'FN']
colors_per_row = ['#2E7D32', '#C62828', '#1565C0', '#9E9E9E']

# Stacked bar chart with grouped layout
x = np.arange(len(radii))
bottom = np.zeros(len(radii))
for i, (vals, lab, col) in enumerate(zip(data, labels, colors_per_row)):
    bars = ax.bar(x, vals, bottom=bottom, color=col, alpha=0.85,
                   edgecolor='black', linewidth=0.6, label=lab, width=0.55)
    # Annotation
    for j, (v, b) in enumerate(zip(vals, bottom)):
        if v > 0:
            ax.text(j, b + v/2, str(int(v)),
                    ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
    bottom = bottom + vals

ax.set_xticks(x)
ax.set_xticklabels([f'{r} m' for r in radii])
ax.set_xlabel('Geofence radius', fontsize=10.5, fontweight='bold')
ax.set_ylabel('Number of independent observations', fontsize=10.5, fontweight='bold')
ax.set_title('(b) Confusion matrix counts (n = 78 collapsed)',
             fontsize=11, fontweight='bold')
ax.legend(loc='upper left', fontsize=9.5, ncol=4, framealpha=0.95)
ax.grid(True, axis='y', linestyle=':', alpha=0.3)
ax.set_axisbelow(True)
ax.set_ylim(0, 35)

# Total annotation per radius
for i, (xi, n_i, f1_i) in enumerate(zip(x, n_per, f1)):
    ax.text(xi, n_i + 0.7, f'F1 = {f1_i:.3f}', ha='center',
            fontsize=9, fontweight='bold', color='#1F2937',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFF3CD',
                      edgecolor='#D4A72C', linewidth=0.8))

# Suptitle
fig.suptitle('Figure 4.  Geofence detection performance by radius — RutAI evaluation in Quevedo, Ecuador',
             fontsize=11.5, fontweight='bold', y=1.00)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/claude/rutai_figures/Figure_04_geofence_results.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_04_geofence_results.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 4 generated.")
