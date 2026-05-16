"""
Figure 1 — System architecture of RutAI (3-layer client-server design)
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

# Color palette (academic, restrained)
C_PRES = "#D5E8F0"
C_BIZ = "#E8F0D5"
C_DATA = "#F0E0D5"
C_BORDER = "#2E4057"
C_TEXT = "#1F2937"
C_EXT = "#F5F5F5"

def box(x, y, w, h, color, label, sub=None, fontsize=9.5):
    bp = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.04,rounding_size=0.08",
                         linewidth=1.4, edgecolor=C_BORDER,
                         facecolor=color)
    ax.add_patch(bp)
    if sub:
        ax.text(x + w/2, y + h*0.62, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=C_TEXT)
        ax.text(x + w/2, y + h*0.30, sub, ha='center', va='center',
                fontsize=fontsize-1.5, color=C_TEXT, style='italic')
    else:
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=C_TEXT)

def title(x, y, text):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=11, fontweight='bold', color=C_BORDER)

def arrow(x1, y1, x2, y2, color=C_BORDER, style='->'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                   arrowstyle=style, color=color,
                                   mutation_scale=14, linewidth=1.4))

# ============ MOBILE CLIENT (left) ============
client_x, client_y, client_w, client_h = 0.5, 0.6, 5.5, 8.7
ax.add_patch(FancyBboxPatch((client_x, client_y), client_w, client_h,
    boxstyle="round,pad=0.05,rounding_size=0.15",
    linewidth=1.8, edgecolor=C_BORDER, facecolor='white', linestyle='--'))
ax.text(client_x + client_w/2, client_y + client_h - 0.35,
        "Android Mobile Client",
        ha='center', va='center', fontsize=12, fontweight='bold', color=C_BORDER)

# Presentation
title(client_x + client_w/2, client_y + client_h - 0.95, "Presentation Layer")
box(client_x + 0.3, client_y + 6.6, 2.4, 0.6, C_PRES, "Jetpack Compose UI", fontsize=8.5)
box(client_x + 2.85, client_y + 6.6, 2.4, 0.6, C_PRES, "ViewModels (StateFlow)", fontsize=8.5)

# Business logic
title(client_x + client_w/2, client_y + 6.15, "Business Logic Layer")
box(client_x + 0.3, client_y + 4.85, 2.4, 0.55, C_BIZ, "Geofence service", fontsize=8.5)
box(client_x + 2.85, client_y + 4.85, 2.4, 0.55, C_BIZ, "Route generator", fontsize=8.5)
box(client_x + 0.3, client_y + 4.20, 2.4, 0.55, C_BIZ, "Foreground GPS service", fontsize=8.5)
box(client_x + 2.85, client_y + 4.20, 2.4, 0.55, C_BIZ, "WS client", fontsize=8.5)

# Data layer
title(client_x + client_w/2, client_y + 3.75, "Data Layer")
box(client_x + 0.3, client_y + 2.45, 2.4, 0.55, C_DATA, "Room (SQLite)", fontsize=8.5)
box(client_x + 2.85, client_y + 2.45, 2.4, 0.55, C_DATA, "Retrofit (REST)", fontsize=8.5)
box(client_x + 0.3, client_y + 1.80, 2.4, 0.55, C_DATA, "OkHttp WebSocket", fontsize=8.5)
box(client_x + 2.85, client_y + 1.80, 2.4, 0.55, C_DATA, "osmdroid (maps)", fontsize=8.5)

# Sensors
box(client_x + 0.3, client_y + 0.85, 4.95, 0.55, "#FCFCFC",
    "GPS · AlarmManager · Notifications · FCM",
    fontsize=8.5)

# ============ NETWORK ============
arrow(client_x + client_w + 0.05, client_y + client_h/2 + 0.3,
      client_x + client_w + 1.30, client_y + client_h/2 + 0.3)
ax.text(client_x + client_w + 0.7, client_y + client_h/2 + 0.55,
        "HTTPS / REST", ha='center', fontsize=8.5, style='italic', color=C_BORDER)

arrow(client_x + client_w + 1.30, client_y + client_h/2 - 0.3,
      client_x + client_w + 0.05, client_y + client_h/2 - 0.3)
ax.text(client_x + client_w + 0.7, client_y + client_h/2 - 0.55,
        "WSS / WebSocket", ha='center', fontsize=8.5, style='italic', color=C_BORDER)

# ============ BACKEND (right) ============
back_x, back_y, back_w, back_h = 7.4, 0.6, 5.5, 8.7
ax.add_patch(FancyBboxPatch((back_x, back_y), back_w, back_h,
    boxstyle="round,pad=0.05,rounding_size=0.15",
    linewidth=1.8, edgecolor=C_BORDER, facecolor='white', linestyle='--'))
ax.text(back_x + back_w/2, back_y + back_h - 0.35,
        "Cloud Backend (FastAPI)",
        ha='center', va='center', fontsize=12, fontweight='bold', color=C_BORDER)

# Routers
title(back_x + back_w/2, back_y + back_h - 0.95, "Router Layer")
box(back_x + 0.3, back_y + 6.6, 2.4, 0.6, C_PRES, "REST endpoints", fontsize=8.5)
box(back_x + 2.85, back_y + 6.6, 2.4, 0.6, C_PRES, "WebSocket endpoints", fontsize=8.5)

# Services
title(back_x + back_w/2, back_y + 6.15, "Service Layer")
box(back_x + 0.3, back_y + 4.85, 2.4, 0.55, C_BIZ, "Thompson Sampling", fontsize=8.5)
box(back_x + 2.85, back_y + 4.85, 2.4, 0.55, C_BIZ, "Safety / Ray casting", fontsize=8.5)
box(back_x + 0.3, back_y + 4.20, 2.4, 0.55, C_BIZ, "Group manager", fontsize=8.5)
box(back_x + 2.85, back_y + 4.20, 2.4, 0.55, C_BIZ, "Authentication (JWT)", fontsize=8.5)

# Repositories
title(back_x + back_w/2, back_y + 3.75, "Repository Layer")
box(back_x + 0.3, back_y + 2.45, 2.4, 0.55, C_DATA, "PostgreSQL", fontsize=8.5)
box(back_x + 2.85, back_y + 2.45, 2.4, 0.55, C_DATA, "Redis (Upstash)", fontsize=8.5)
box(back_x + 0.3, back_y + 1.80, 5.0, 0.55, C_DATA, "SQLAlchemy ORM", fontsize=8.5)

# External services
title(back_x + back_w/2, back_y + 1.40, "External services")
box(back_x + 0.3, back_y + 0.40, 1.55, 0.55, C_EXT, "OpenRouteService", fontsize=8)
box(back_x + 2.0, back_y + 0.40, 1.55, 0.55, C_EXT, "OpenStreetMap", fontsize=8)
box(back_x + 3.7, back_y + 0.40, 1.55, 0.55, C_EXT, "Firebase FCM", fontsize=8)

# Title (top of figure)
ax.text(7, 9.7, "Figure 1.  System architecture of RutAI — three-layer client-server design",
        ha='center', va='center', fontsize=11, fontweight='bold', color=C_BORDER)

plt.tight_layout()
plt.savefig('/home/claude/rutai_figures/Figure_01_architecture.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_01_architecture.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 1 generated.")
