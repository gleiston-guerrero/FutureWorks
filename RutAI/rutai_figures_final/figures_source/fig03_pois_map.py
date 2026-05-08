"""
Figure 3 — Geographic distribution of the 20 POIs in Quevedo, Ecuador.
Real coordinates from the geofence experiment data.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# Real coordinates from the dataset
pois = [
    ("Acoustic Shell",       -1.017889, -79.465611),
    ("San Camilo Stadium",   -1.035874, -79.467254),
    ("La Torta",             -1.031730, -79.471203),
    ("Monument to the Mother", -1.021722, -79.465709),
    ("Monument to Peace",    -1.025729, -79.463617),
    ("Rotary Park",          -1.013986, -79.467008),
    ("San Camilo Park",      -1.022484, -79.458822),
    ("Bocachico Park",       -1.030850, -79.462618),
    ("Airplane Park",        -1.038341, -79.474846),
    ("Sailboat Park",        -1.037482, -79.474180),
    ("Family Park",          -1.044289, -79.478957),
    ("Linear Park",          -1.026329, -79.464108),
    ("Civic Plaza",          -1.030848, -79.468084),
    ("Quadra",               -1.043237, -79.478494),
    ("Riverside Trail",      -1.005244, -79.447076),
    ("Shopping Mall",        -1.010470, -79.468376),
    ("Supermaxi",            -1.032318, -79.472641),
    ("UTB Campus",           -1.005100, -79.443424),
    ("UTEQ Campus",          -1.012732, -79.467218),
    ("Ventura Plaza",        -1.030007, -79.468759),
]

# Convert to numpy arrays
lats = np.array([p[1] for p in pois])
lons = np.array([p[2] for p in pois])
names = [p[0] for p in pois]

# Setup figure
fig, ax = plt.subplots(figsize=(10, 9))

# Compute bounds with padding
lat_pad, lon_pad = 0.005, 0.005
lat_min, lat_max = lats.min() - lat_pad, lats.max() + lat_pad
lon_min, lon_max = lons.min() - lon_pad, lons.max() + lon_pad

# Background — schematic urban grid
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.set_facecolor('#FAFAF7')

# Schematic "river" (Quevedo is on the Quevedo river, running approximately N-S)
# The real Quevedo river is east of UTB campus, around lon = -79.44
river_x = np.array([-79.4445, -79.4435, -79.4425, -79.4435, -79.4445])
river_y_top = np.array([-1.000, -1.010, -1.020, -1.035, -1.050])
ax.fill_betweenx(river_y_top,
                  np.full_like(river_y_top, -79.443),
                  np.full_like(river_y_top, -79.4365),
                  color='#B6D4E5', alpha=0.5, zorder=1)
ax.text(-79.4395, -1.025, 'Quevedo\nRiver', fontsize=8.5, color='#3A6B89',
        ha='center', va='center', style='italic', rotation=90)

# Schematic main avenues (rough N-S and E-W axes through downtown)
for lat0 in [-1.020, -1.030]:
    ax.axhline(lat0, color='#E5E5E5', linewidth=1.2, zorder=1)
for lon0 in [-79.470, -79.460, -79.450]:
    ax.axvline(lon0, color='#E5E5E5', linewidth=1.2, zorder=1)

# Plot POIs as numbered markers
for i, (name, lat, lon) in enumerate(pois, start=1):
    ax.scatter(lon, lat, s=200, c='#C62828', marker='o',
               edgecolor='white', linewidth=1.5, zorder=4)
    ax.text(lon, lat, str(i), color='white', fontsize=8,
            fontweight='bold', ha='center', va='center', zorder=5)

# Compass rose (top-right) — N points up by convention
compass_x = lon_max - 0.003
compass_y_base = lat_max - 0.005
ax.annotate('', xy=(compass_x, compass_y_base + 0.003),
            xytext=(compass_x, compass_y_base - 0.0005),
            arrowprops=dict(arrowstyle='-|>', color='#1F2937', lw=1.8))
ax.text(compass_x, compass_y_base + 0.0036, 'N', fontsize=11,
        fontweight='bold', ha='center', va='bottom', color='#1F2937')

# Scale bar (rough — at this latitude, 1 deg lon ≈ 111 km × cos(1°) ≈ 111 km;
# 0.005 deg ≈ 555 m → use 500 m scale bar)
scale_lon_start = lon_min + 0.002
scale_lon_end = scale_lon_start + (500 / 111000)  # ~0.0045 deg
scale_y = lat_min + 0.002
ax.plot([scale_lon_start, scale_lon_end], [scale_y, scale_y],
        color='#1F2937', linewidth=2.5, solid_capstyle='butt')
ax.text((scale_lon_start + scale_lon_end) / 2, scale_y + 0.0006,
        '500 m', ha='center', fontsize=8.5, fontweight='bold', color='#1F2937')

# Sample geofence radii drawn around one POI (UTEQ campus, idx 19)
utq_lat, utq_lon = -1.012732, -79.467218
# Convert meters to degrees: approximate at this latitude
m_per_deg_lat = 111000
m_per_deg_lon = 111000 * np.cos(np.radians(utq_lat))
for r_m, color, lab in [(50, '#1565C0', '50 m'),
                         (100, '#2E7D32', '100 m'),
                         (200, '#C62828', '200 m')]:
    r_deg_lat = r_m / m_per_deg_lat
    r_deg_lon = r_m / m_per_deg_lon
    # Approximate as ellipse using mean
    circle = Circle((utq_lon, utq_lat), r_deg_lat, fill=False,
                    edgecolor=color, linewidth=1.4, linestyle='--', zorder=3)
    ax.add_patch(circle)

# Inset legend for radii
from matplotlib.lines import Line2D
legend_elems = [
    Line2D([0], [0], color='#1565C0', linestyle='--', linewidth=1.5,
           label='R = 50 m'),
    Line2D([0], [0], color='#2E7D32', linestyle='--', linewidth=1.5,
           label='R = 100 m'),
    Line2D([0], [0], color='#C62828', linestyle='--', linewidth=1.5,
           label='R = 200 m'),
]
leg1 = ax.legend(handles=legend_elems, loc='lower right',
                  fontsize=9, framealpha=0.95, title='Geofence radii\n(shown around UTEQ)',
                  title_fontsize=9)
leg1.get_title().set_fontweight('bold')

# Labels
ax.set_xlabel('Longitude (°)', fontsize=10)
ax.set_ylabel('Latitude (°)', fontsize=10)
ax.set_title('Figure 3.  Twenty points of interest used in the geofence experiment, Quevedo, Ecuador',
             fontsize=11, fontweight='bold', pad=12)

# POI list as right-side legend table
poi_text_left = '  '.join([f'{i:>2}. {names[i-1]}' for i in range(1, 11)])
poi_text_right = '  '.join([f'{i:>2}. {names[i-1]}' for i in range(11, 21)])

# We will instead place a separate panel below the map
# POI list as bottom panel (three rows for 20 items)
fig.text(0.06, 0.038,
         '  '.join([f'{i+1}. {names[i]}' for i in range(0, 7)]),
         fontsize=8, color='#1F2937')
fig.text(0.06, 0.020,
         '  '.join([f'{i+1}. {names[i]}' for i in range(7, 14)]),
         fontsize=8, color='#1F2937')
fig.text(0.06, 0.002,
         '  '.join([f'{i+1}. {names[i]}' for i in range(14, 20)]),
         fontsize=8, color='#1F2937')

ax.grid(True, linestyle=':', alpha=0.3, zorder=0)
ax.set_aspect('auto')

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.savefig('/home/claude/rutai_figures/Figure_03_pois_map.png',
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/home/claude/rutai_figures/Figure_03_pois_map.pdf',
            bbox_inches='tight', facecolor='white')
plt.close()
print("Figure 3 generated.")
