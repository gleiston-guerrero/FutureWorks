"""
Figure 6 — Cumulative regret of bandit policies for route-type recommendation.
Recreates the regret curves with English labels and the RutAI naming.
Uses the actual data from bandit_regret_timesteps.csv.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('/mnt/user-data/uploads/ucb_timesteps.csv')

# English labels for the policies
label_map = {
    'Random': 'Random',
    'Greedy': 'Greedy',
    'ε-greedy (ε=0.1)': 'ε-greedy (ε=0.1)',
    'ε-greedy (ε=0.2)': 'ε-greedy (ε=0.2)',
    'Thompson': 'Thompson Sampling (deployed)',
    'LinUCB': 'LinUCB',
    'UCB + Entropía (RutAI)': 'UCB1 + entropy (deprecated)',
}

# Color scheme
colors = {
    'Random': '#9E9E9E',
    'Greedy': '#FB8C00',
    'ε-greedy (ε=0.1)': '#FFC107',
    'ε-greedy (ε=0.2)': '#B8860B',
    'Thompson': '#2E7D32',
    'LinUCB': '#1565C0',
    'UCB + Entropía (RutAI)': '#7E57C2',
}

linestyles = {
    'Thompson': '-',
    'ε-greedy (ε=0.1)': '-',
    'ε-greedy (ε=0.2)': ':',
    'LinUCB': '--',
    'UCB + Entropía (RutAI)': '-.',
    'Greedy': '--',
    'Random': '-',
}

linewidths = {
    'Thompson': 3.0,
    'ε-greedy (ε=0.1)': 2.0,
    'ε-greedy (ε=0.2)': 1.6,
    'UCB + Entropía (RutAI)': 1.6,
    'LinUCB': 1.6,
    'Greedy': 1.6,
    'Random': 1.6,
}

fig, ax = plt.subplots(figsize=(11, 6.2))

# Plot order — Thompson last so its line is on top
plot_order = ['Random', 'Greedy', 'LinUCB', 'UCB + Entropía (RutAI)',
              'ε-greedy (ε=0.2)', 'ε-greedy (ε=0.1)', 'Thompson']

for algo in plot_order:
    sub = df[df['algorithm'] == algo].sort_values('timestep')
    ax.plot(sub['timestep'], sub['regret_mean'],
            label=label_map[algo],
            color=colors[algo],
            linestyle=linestyles[algo],
            linewidth=linewidths[algo],
            alpha=0.95)
    ax.fill_between(sub['timestep'], sub['ci_lower'], sub['ci_upper'],
                     color=colors[algo], alpha=0.10)

ax.set_xlabel('Interactions (t)', fontsize=11.5, fontweight='bold')
ax.set_ylabel('Cumulative regret (mean ± 95 % bootstrap CI)',
              fontsize=11.5, fontweight='bold')
ax.set_title('Figure 6.  Bandit policy comparison for route-type recommendation in RutAI '
             '(T = 500, 100 seeds)',
             fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, linestyle=':', alpha=0.35)
ax.set_axisbelow(True)
ax.set_xlim(0, 500)
ax.set_ylim(0, 75)

# Legend — order by performance (best first)
handles, labels = ax.get_legend_handles_labels()
order = [labels.index(label_map[a]) for a in
         ['Thompson', 'ε-greedy (ε=0.1)', 'ε-greedy (ε=0.2)',
          'UCB + Entropía (RutAI)', 'LinUCB', 'Greedy', 'Random']]
ax.legend([handles[i] for i in order], [labels[i] for i in order],
           loc='upper left', fontsize=9.5, framealpha=0.95,
           title='Policy (sorted by final regret)',
           title_fontsize=10).get_title().set_fontweight('bold')

# Final regret annotations on the right side
final_vals = [
    ('Thompson Sampling', 13.41, '#2E7D32', 13.4),
    ('ε-greedy (0.1)', 16.58, '#FFC107', 16.6),
    ('ε-greedy (0.2)', 19.91, '#B8860B', 19.9),
    ('UCB1 + entropy', 32.82, '#7E57C2', 32.8),
    ('LinUCB / Greedy', 40.5, '#1565C0', 40.5),
    ('Random', 66.65, '#9E9E9E', 66.7),
]

plt.tight_layout()
plt.savefig('/home/claude/rutai_figures/Figure_06_bandit_regret.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_06_bandit_regret.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 6 generated.")
