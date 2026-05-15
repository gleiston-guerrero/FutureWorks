"""
Ilustración 10: Flujo de autenticación por JWT en Kiddy Quiz
Diagrama de secuencia que ilustra el proceso de login y validación de tokens.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(14, 8.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

COLOR_FRAME = "#1F6E43"
COLOR_BORDE = "#0F4C2A"
COLOR_BOX = "#1F6E43"
COLOR_LIFELINE = "#666"
COLOR_MSG = "#0F4C2A"
COLOR_NOTE = "#FFFBE6"

# Título
ax.text(8, 9.6, "Flujo de autenticación por JWT en Kiddy Quiz",
        ha='center', va='center', fontsize=15, fontweight='bold', color=COLOR_FRAME)

# Actores y componentes
componentes = [
    ("Cliente\n(Angular)", 1.5),
    ("API Gateway\n(NestJS)", 5.0),
    ("AuthService\n(Validación)", 8.5),
    ("PostgreSQL\n(Usuarios)", 12.0),
    ("JWT Module\n(Firma)", 14.5),
]

# Cabezas de los componentes
for nombre, x in componentes:
    box = FancyBboxPatch((x - 0.9, 8.3), 1.8, 0.7,
                          boxstyle="round,pad=0.04,rounding_size=0.1",
                          facecolor=COLOR_BOX, edgecolor=COLOR_BORDE, linewidth=1.4)
    ax.add_patch(box)
    ax.text(x, 8.65, nombre, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='white')
    # Línea de vida
    ax.plot([x, x], [8.3, 1.0], color=COLOR_LIFELINE,
            linewidth=1, linestyle='--', alpha=0.7)

# Mensajes (flechas) numerados
def mensaje(ax, x1, x2, y, etiqueta, retorno=False, num=None):
    color = COLOR_MSG
    style = '->' if not retorno else '-->'
    arr = FancyArrowPatch((x1, y), (x2, y),
                           arrowstyle='->', mutation_scale=14,
                           linewidth=1.5,
                           color=color,
                           linestyle='-' if not retorno else (0, (5, 3)))
    ax.add_patch(arr)
    cx = (x1 + x2) / 2
    label = etiqueta if num is None else f"{num}. {etiqueta}"
    ax.text(cx, y + 0.18, label, ha='center', va='bottom',
            fontsize=9, color=COLOR_MSG, style='italic',
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor='none', alpha=0.92))

# Secuencia de mensajes
mensaje(ax, 1.5, 5.0, 7.7, "POST /auth/login (correo, password)", num=1)
mensaje(ax, 5.0, 8.5, 7.1, "validateUser(credenciales)", num=2)
mensaje(ax, 8.5, 12.0, 6.5, "SELECT usuario WHERE correo=...", num=3)
mensaje(ax, 12.0, 8.5, 5.9, "Usuario + hash", retorno=True, num=4)

# Nota sobre comparación de hash
note = FancyBboxPatch((7.0, 4.9), 4.0, 0.6,
                       boxstyle="round,pad=0.04,rounding_size=0.08",
                       facecolor=COLOR_NOTE, edgecolor='#D4B106', linewidth=1.2)
ax.add_patch(note)
ax.text(9.0, 5.2, "bcrypt.compare(password, hash)", ha='center', va='center',
        fontsize=9, fontweight='bold', color='#5C3D00', family='monospace')

mensaje(ax, 8.5, 14.5, 4.4, "sign(payload, secret, expiresIn)", num=5)
mensaje(ax, 14.5, 8.5, 3.9, "JWT firmado", retorno=True, num=6)
mensaje(ax, 8.5, 5.0, 3.4, "Token + datos del usuario", retorno=True, num=7)
mensaje(ax, 5.0, 1.5, 2.9, "200 OK { access_token }", retorno=True, num=8)

# Sección de petición autenticada
ax.plot([0.5, 15.5], [2.4, 2.4], color='#999', linestyle=':', linewidth=1)
ax.text(0.5, 2.55, "Peticiones posteriores autenticadas:",
        ha='left', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_FRAME)

mensaje(ax, 1.5, 5.0, 1.9, "GET /clases  Header: Authorization: Bearer <token>", num=9)
mensaje(ax, 5.0, 8.5, 1.4, "verifyToken(token) → guard JWT", num=10)
mensaje(ax, 5.0, 1.5, 0.9, "200 OK + datos protegidos", retorno=True, num=11)

# Etiqueta del expirado
ax.text(15.7, 4.4, "Expira: 24h\n(refresh token: 7d)",
        ha='left', va='center', fontsize=8, style='italic', color="#555",
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F7F2',
                  edgecolor=COLOR_BORDE, linewidth=0.8))

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig10_jwt.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 10 generada")
