"""
Figure 8 — TAM acceptance pilot summary (complementary, n=25).
Single compact visualization combining construct means with CIs and
distribution information, transparently flagging discriminant validity.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/mnt/user-data/uploads/participantes.csv', encoding='utf-8-sig')

constructs = {
    'PU':   ['PU1','PU2','PU3','PU4','PU5'],
    'PEOU': ['PEOU1','PEOU2','PEOU3','PEOU4','PEOU5'],
    'ATU':  ['ATU1','ATU2','ATU3','ATU4','ATU5'],
    'ITU':  ['ITU1','ITU2','ITU3','ITU4','ITU5'],
    'PS':   ['PS1','PS2','PS3','PS4','PS5'],
}

construct_long = {
    'PU': 'Perceived\nUsefulness',
    'PEOU': 'Perceived Ease\nof Use',
    'ATU': 'Attitude\nToward Use',
    'ITU': 'Intention\nto Use',
    'PS': 'Perceived\nSecurity'
}

# Compute construct scores per participant
for c, items in constructs.items():
    df[c] = df[items].mean(axis=1)

# Stats
n = len(df)
means = {c: df[c].mean() for c in constructs}
sds = {c: df[c].std(ddof=1) for c in constructs}
sems = {c: sds[c] / np.sqrt(n) for c in constructs}
ci95 = {c: 1.96 * sems[c] for c in constructs}

fig, axes = plt.subplots(1, 2, figsize=(13, 5.6),
                          gridspec_kw={'width_ratios': [1.3, 1]})

# ─── PANEL A: Means with 95% CIs (acceptance threshold reference) ───
ax = axes[0]
construct_keys = list(constructs.keys())
x = np.arange(len(construct_keys))
mean_vals = [means[c] for c in construct_keys]
ci_vals = [ci95[c] for c in construct_keys]

# Acceptance threshold band
ax.axhspan(3.5, 5.0, color='#E8F5E9', alpha=0.5, zorder=0)
ax.axhline(3.5, color='#2E7D32', linestyle=':', linewidth=1.2, alpha=0.7, zorder=1)
ax.text(0.05, 3.45, 'Acceptance threshold (3.5)',
        fontsize=8, color='#2E7D32', va='top', style='italic',
        transform=ax.get_yaxis_transform())

# Bars
bar_colors = ['#1565C0', '#2E7D32', '#FB8C00', '#7E57C2', '#C62828']
bars = ax.bar(x, mean_vals, color=bar_colors, alpha=0.85,
               edgecolor='black', linewidth=0.6,
               yerr=ci_vals, capsize=8,
               error_kw={'elinewidth': 1.5, 'ecolor': '#1F2937'})

# Annotations
for i, (xi, m, c) in enumerate(zip(x, mean_vals, construct_keys)):
    ax.text(xi, m + ci_vals[i] + 0.10, f'{m:.2f}',
            ha='center', fontsize=10, fontweight='bold', color='#1F2937')
    # Cronbach annotation
    cron = {'PU': 0.888, 'PEOU': 0.942, 'ATU': 0.974, 'ITU': 0.963, 'PS': 0.964}[c]
    ax.text(xi, 0.18, f'α = {cron:.3f}',
            ha='center', fontsize=8, color='#6B7280',
            transform=ax.get_xaxis_transform())

ax.set_xticks(x)
ax.set_xticklabels([construct_long[c] for c in construct_keys], fontsize=9.5)
ax.set_ylim(0, 5.3)
ax.set_ylabel('Mean construct score (1–5 Likert)',
              fontsize=10.5, fontweight='bold')
ax.set_title(f'(a) TAM construct means (n = {n}) with 95 % CIs',
             fontsize=11, fontweight='bold')
ax.grid(True, axis='y', linestyle=':', alpha=0.3)
ax.set_axisbelow(True)

# Note about pilot
ax.text(0.5, -0.16,
        'Pilot study — exploratory complementary evidence.  See §6.3 for limitations.',
        ha='center', fontsize=8, color='#6B7280', style='italic',
        transform=ax.transAxes)

# ─── PANEL B: Construct correlations heatmap (with discriminant validity flag) ───
ax = axes[1]
corr = df[construct_keys].corr()

im = ax.imshow(corr, cmap='RdYlGn_r', vmin=0.5, vmax=1.0, aspect='equal')

# Annotations
for i in range(5):
    for j in range(5):
        v = corr.iloc[i, j]
        # Flag discriminant validity issues: r > 0.95 (excluding diagonal)
        flag = '⚠' if (v > 0.95 and i != j) else ''
        col = 'white' if v < 0.65 or v > 0.92 else 'black'
        ax.text(j, i, f'{v:.2f}{flag}', ha='center', va='center',
                fontsize=9, color=col, fontweight='bold')

ax.set_xticks(range(5))
ax.set_yticks(range(5))
ax.set_xticklabels(construct_keys, fontsize=10)
ax.set_yticklabels(construct_keys, fontsize=10)
ax.set_title('(b) Pearson correlations between constructs',
             fontsize=11, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Pearson r', fontsize=9)

# Note about discriminant validity
ax.text(0.5, -0.17,
        '⚠ flags r > 0.95 — discriminant validity not achieved (see §6.3)',
        ha='center', fontsize=8, color='#C62828', style='italic',
        fontweight='bold', transform=ax.transAxes)

# Suptitle
fig.suptitle('Figure 8.  TAM acceptance pilot — complementary evidence with documented limitations',
             fontsize=11.5, fontweight='bold', y=1.00)

plt.tight_layout(rect=[0, 0.02, 1, 0.96])
plt.savefig('/home/claude/rutai_figures/Figure_08_tam_summary.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_08_tam_summary.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 8 generated.")
