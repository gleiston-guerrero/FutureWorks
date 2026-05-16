"""
Figure 7 — Schematic mockups of the three main RutAI screens.
Since real screenshots are not available, this figure presents an annotated
schematic of the user interface for each of the three core modules.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(13, 8.5))

C_PHONE = '#FAFAFA'
C_PHONE_BORDER = '#1F2937'
C_HEADER = '#2E4057'
C_PRIMARY = '#1565C0'
C_ACCENT = '#2E7D32'
C_DANGER = '#C62828'
C_TEXT = '#1F2937'
C_MUTED = '#6B7280'

def draw_phone(ax, title):
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 12)
    ax.set_aspect('equal')
    ax.axis('off')

    # Phone outer
    phone = FancyBboxPatch((-0.3, -0.3), 4.6, 11.6,
                            boxstyle='round,pad=0.05,rounding_size=0.4',
                            linewidth=2.2, edgecolor=C_PHONE_BORDER,
                            facecolor=C_PHONE)
    ax.add_patch(phone)

    # Speaker/notch
    ax.add_patch(Rectangle((1.6, 10.85), 0.8, 0.18, color=C_PHONE_BORDER))

    # Status bar
    ax.add_patch(Rectangle((-0.2, 10.35), 4.4, 0.40, color='#E5E7EB', linewidth=0))
    ax.text(0.0, 10.55, '● ● ●', fontsize=6, color=C_TEXT, va='center')
    ax.text(2.0, 10.55, '11:42', fontsize=8, color=C_TEXT, ha='center', va='center', fontweight='bold')
    ax.text(3.95, 10.55, '⚡ 87 %', fontsize=6.5, color=C_TEXT, ha='right', va='center')

    # Header
    ax.add_patch(Rectangle((-0.2, 9.55), 4.4, 0.80, color=C_HEADER, linewidth=0))
    ax.text(2.0, 9.95, title, fontsize=9.5, color='white',
            ha='center', va='center', fontweight='bold')

    return ax

# ════════════════════════════════════════════════════════════
# PANEL A — Route recommendation screen
# ════════════════════════════════════════════════════════════
ax = axes[0]
draw_phone(ax, 'Alternative Routes')

# Map area (top)
ax.add_patch(Rectangle((0, 5.0), 4.0, 4.4,
                        facecolor='#E8F0E0', edgecolor=C_MUTED, linewidth=0.5))

# Schematic streets
for y0 in [5.6, 6.5, 7.4, 8.3]:
    ax.axhline(y0, xmin=0.05, xmax=0.95, color='#D1D5DB', linewidth=1.2,
               clip_on=False, zorder=0)
for x0 in [0.5, 1.4, 2.3, 3.2]:
    ax.axvline(x0, ymin=0.42, ymax=0.79, color='#D1D5DB', linewidth=1.2,
               clip_on=False, zorder=0)

# Three routes — distinct colors
# Route 1 (fastest) — blue
ax.plot([0.6, 1.3, 2.1, 2.8, 3.5], [5.5, 6.4, 7.0, 7.7, 8.5],
        color=C_PRIMARY, linewidth=2.5, marker='', zorder=3)
# Route 2 (shortest) — orange
ax.plot([0.6, 1.5, 2.3, 3.1, 3.5], [5.5, 6.0, 7.3, 8.0, 8.5],
        color='#FB8C00', linewidth=2.5, linestyle='--', zorder=3)
# Route 3 (recommended by Thompson Sampling) — green, thicker
ax.plot([0.6, 1.0, 1.7, 2.5, 3.4, 3.5], [5.5, 6.5, 6.9, 7.5, 8.2, 8.5],
        color=C_ACCENT, linewidth=3.2, zorder=4)

# Origin and destination
ax.scatter([0.6], [5.5], s=80, color=C_PRIMARY, marker='o',
           edgecolor='white', linewidth=1.5, zorder=5)
ax.text(0.4, 5.3, 'A', fontsize=8, color=C_PRIMARY, fontweight='bold', ha='center')
ax.scatter([3.5], [8.5], s=80, color=C_DANGER, marker='v',
           edgecolor='white', linewidth=1.5, zorder=5)
ax.text(3.7, 8.7, 'B', fontsize=8, color=C_DANGER, fontweight='bold')

# Danger zone (small red shaded area on right)
from matplotlib.patches import Wedge
danger = Circle((2.0, 6.5), 0.5, facecolor=C_DANGER, alpha=0.25,
                 edgecolor=C_DANGER, linewidth=1, linestyle='--')
ax.add_patch(danger)
ax.text(2.0, 6.5, '!', fontsize=11, color=C_DANGER, fontweight='bold',
        ha='center', va='center')

# Route cards (bottom)
cards = [
    (4.65, 'Recommended', '8 min · 2.1 km',  C_ACCENT, '★', True),
    (3.55, 'Fastest',       '7 min · 2.4 km',  C_PRIMARY, '⚡', False),
    (2.45, 'Shortest',      '9 min · 1.9 km',  '#FB8C00',  '↘', False),
]
for (y, name, info, col, icon, sel) in cards:
    bg = '#E8F5E9' if sel else 'white'
    bd = col if sel else '#E5E7EB'
    bw = 2.0 if sel else 1.0
    ax.add_patch(FancyBboxPatch((0.15, y - 0.45), 3.7, 0.85,
                                   boxstyle='round,pad=0.02,rounding_size=0.10',
                                   facecolor=bg, edgecolor=bd, linewidth=bw))
    ax.text(0.45, y, icon, fontsize=14, color=col, ha='center', va='center')
    ax.text(0.85, y + 0.16, name, fontsize=9, fontweight='bold', color=C_TEXT, va='center')
    ax.text(0.85, y - 0.18, info, fontsize=7.5, color=C_MUTED, va='center')
    if sel:
        ax.text(3.5, y, '✓', fontsize=12, color=col, fontweight='bold',
                ha='center', va='center')

# Bottom navigation
ax.add_patch(Rectangle((-0.2, -0.2), 4.4, 0.65, color='#F3F4F6', linewidth=0))
nav_x = [0.5, 1.3, 2.1, 2.9, 3.7]
nav_l = ['Home', 'Routes', 'Reminders', 'Groups', 'Profile']
for x_, l_ in zip(nav_x, nav_l):
    ax.text(x_, 0.20, '◯', fontsize=8, color=C_MUTED, ha='center', va='center')
    ax.text(x_, -0.05, l_, fontsize=6.5, color=C_MUTED, ha='center', va='center')

ax.set_title('(a) Route recommendation', fontsize=11, fontweight='bold', pad=8)

# ════════════════════════════════════════════════════════════
# PANEL B — Geofence reminder configuration
# ════════════════════════════════════════════════════════════
ax = axes[1]
draw_phone(ax, 'New Reminder · Step 3 / 4')

# Map area
ax.add_patch(Rectangle((0, 5.5), 4.0, 3.9,
                        facecolor='#E8F0E0', edgecolor=C_MUTED, linewidth=0.5))

# Geofence circle
geo = Circle((2.0, 7.4), 1.1, facecolor=C_PRIMARY, alpha=0.18,
              edgecolor=C_PRIMARY, linewidth=1.6, linestyle='--')
ax.add_patch(geo)
# Center pin
ax.scatter([2.0], [7.4], s=120, color=C_DANGER, marker='v',
           edgecolor='white', linewidth=1.5, zorder=5)
# R label
ax.plot([2.0, 2.78], [7.4, 7.4], color=C_PRIMARY, linewidth=1, linestyle=':')
ax.text(2.4, 7.55, 'R = 100 m', fontsize=8, color=C_PRIMARY,
        fontweight='bold', ha='center', va='bottom')

# Configuration card
ax.add_patch(FancyBboxPatch((0.15, 0.7), 3.7, 4.6,
                               boxstyle='round,pad=0.02,rounding_size=0.10',
                               facecolor='white', edgecolor='#E5E7EB', linewidth=1))

ax.text(0.35, 4.95, 'Trigger type', fontsize=8.5, fontweight='bold', color=C_TEXT)
# Three pills
pills = [(0.3, 'Location', True), (1.5, 'Time', False), (2.7, 'Both', False)]
for (x, lab, sel) in pills:
    bg = C_PRIMARY if sel else 'white'
    fg = 'white' if sel else C_TEXT
    bd = C_PRIMARY if sel else '#D1D5DB'
    ax.add_patch(FancyBboxPatch((x + 0.05, 4.40), 1.15, 0.40,
                                   boxstyle='round,pad=0.02,rounding_size=0.18',
                                   facecolor=bg, edgecolor=bd, linewidth=1.2))
    ax.text(x + 0.625, 4.60, lab, ha='center', va='center', fontsize=8.5, color=fg)

# Slider — radius
ax.text(0.35, 3.95, 'Radius:  100 m', fontsize=8.5, fontweight='bold', color=C_TEXT)
ax.add_patch(Rectangle((0.35, 3.55), 3.3, 0.10, color='#E5E7EB'))
ax.add_patch(Rectangle((0.35, 3.55), 1.3, 0.10, color=C_PRIMARY))
ax.scatter([1.65], [3.60], s=60, color=C_PRIMARY, edgecolor='white',
            linewidth=1.5, zorder=5)
ax.text(0.35, 3.30, '50 m', fontsize=7, color=C_MUTED)
ax.text(3.65, 3.30, '500 m', fontsize=7, color=C_MUTED, ha='right')

# Trigger condition
ax.text(0.35, 2.85, 'Trigger when:', fontsize=8.5, fontweight='bold', color=C_TEXT)
opts = [(0.3, 'Entering', True), (1.5, 'Leaving', False), (2.7, 'Both', False)]
for (x, lab, sel) in opts:
    bg = C_ACCENT if sel else 'white'
    fg = 'white' if sel else C_TEXT
    bd = C_ACCENT if sel else '#D1D5DB'
    ax.add_patch(FancyBboxPatch((x + 0.05, 2.30), 1.15, 0.40,
                                   boxstyle='round,pad=0.02,rounding_size=0.18',
                                   facecolor=bg, edgecolor=bd, linewidth=1.2))
    ax.text(x + 0.625, 2.50, lab, ha='center', va='center', fontsize=8.5, color=fg)

# Buttons (Back / Next)
ax.add_patch(FancyBboxPatch((0.30, 1.0), 1.6, 0.65,
                              boxstyle='round,pad=0.02,rounding_size=0.20',
                              facecolor='white', edgecolor=C_MUTED, linewidth=1.2))
ax.text(1.10, 1.32, 'Back', ha='center', va='center', fontsize=9.5, color=C_MUTED)
ax.add_patch(FancyBboxPatch((2.10, 1.0), 1.6, 0.65,
                              boxstyle='round,pad=0.02,rounding_size=0.20',
                              facecolor=C_PRIMARY, edgecolor=C_PRIMARY, linewidth=0))
ax.text(2.90, 1.32, 'Next →', ha='center', va='center', fontsize=9.5,
        color='white', fontweight='bold')

ax.set_title('(b) Geofence reminder setup', fontsize=11, fontweight='bold', pad=8)

# ════════════════════════════════════════════════════════════
# PANEL C — Collaborative tracking map
# ════════════════════════════════════════════════════════════
ax = axes[2]
draw_phone(ax, 'Group: Family · Live Map')

# Map area
ax.add_patch(Rectangle((0, 1.8), 4.0, 7.6,
                        facecolor='#E8F0E0', edgecolor=C_MUTED, linewidth=0.5))

# Schematic streets
for y0 in [3.0, 4.5, 6.0, 7.5]:
    ax.axhline(y0, xmin=0.05, xmax=0.95, color='#D1D5DB', linewidth=1.0,
               clip_on=False, zorder=0)
for x0 in [0.7, 1.7, 2.7, 3.5]:
    ax.axvline(x0, ymin=0.13, ymax=0.74, color='#D1D5DB', linewidth=1.0,
               clip_on=False, zorder=0)

# 4 group members at different locations
members = [
    (1.2, 6.5, 'M', '#1565C0', 'Mom'),
    (2.8, 4.8, 'D', '#2E7D32', 'Dad'),
    (3.4, 7.2, 'A', '#E91E63', 'Ana'),
    (1.8, 3.2, 'P', '#FB8C00', 'You'),
]
for (x, y, init, col, name) in members:
    # Pulse circle
    pulse = Circle((x, y), 0.35, facecolor=col, alpha=0.18, linewidth=0)
    ax.add_patch(pulse)
    # Avatar
    avatar = Circle((x, y), 0.20, facecolor=col, edgecolor='white', linewidth=1.5)
    ax.add_patch(avatar)
    ax.text(x, y, init, fontsize=8, color='white', ha='center', va='center',
            fontweight='bold')
    # Name label
    ax.add_patch(FancyBboxPatch((x - 0.4, y + 0.30), 0.8, 0.30,
                                   boxstyle='round,pad=0.02,rounding_size=0.10',
                                   facecolor='white', edgecolor=col, linewidth=1.2))
    ax.text(x, y + 0.45, name, ha='center', va='center', fontsize=7.5,
            color=col, fontweight='bold')

# Members panel (bottom)
ax.add_patch(FancyBboxPatch((0.15, 0.65), 3.7, 1.10,
                              boxstyle='round,pad=0.02,rounding_size=0.10',
                              facecolor='white', edgecolor='#E5E7EB', linewidth=1))
ax.text(0.30, 1.55, 'Sharing live · 4 members', fontsize=8.5,
        fontweight='bold', color=C_TEXT)

# Member dots
for i, (_, _, init, col, _) in enumerate(members):
    cx = 0.45 + i * 0.45
    ax.add_patch(Circle((cx, 1.05), 0.12, facecolor=col, edgecolor='white', linewidth=1))
    ax.text(cx, 1.05, init, fontsize=6, color='white', ha='center', va='center',
            fontweight='bold')

# Action button
ax.add_patch(FancyBboxPatch((2.4, 0.85), 1.45, 0.55,
                              boxstyle='round,pad=0.02,rounding_size=0.18',
                              facecolor=C_DANGER, edgecolor=C_DANGER, linewidth=0))
ax.text(3.125, 1.13, 'Stop sharing', ha='center', va='center', fontsize=8,
        color='white', fontweight='bold')

# WebSocket indicator
ax.text(0.30, 9.30, '● Live · WebSocket', fontsize=7, color=C_ACCENT,
        fontweight='bold', va='center')

ax.set_title('(c) Collaborative tracking', fontsize=11, fontweight='bold', pad=8)

# Suptitle
fig.suptitle('Figure 7.  RutAI user interface — schematic mockups of the three core modules',
             fontsize=11.5, fontweight='bold', y=1.00)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('/home/claude/rutai_figures/Figure_07_ui_mockups.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_07_ui_mockups.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 7 generated.")
