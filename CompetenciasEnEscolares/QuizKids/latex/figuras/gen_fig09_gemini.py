"""
Ilustración 9: Extracto de integración de Gemini AI en Kiddy Quiz
Fragmento de código que muestra cómo se invoca la API de Gemini para generar feedback.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(13, 8.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')

COLOR_FONDO = "#1E1E1E"        # tema dark de editor
COLOR_BORDE = "#0F4C2A"
COLOR_TITULO = "#1F6E43"
COLOR_KEYWORD = "#569CD6"      # azul (keywords)
COLOR_STRING = "#CE9178"       # naranja (strings)
COLOR_FUNC = "#DCDCAA"         # amarillo (funciones)
COLOR_COMMENT = "#6A9955"      # verde (comentarios)
COLOR_TEXT = "#D4D4D4"         # blanco grisáceo
COLOR_TYPE = "#4EC9B0"         # turquesa (tipos / clases)
COLOR_NUM = "#B5CEA8"          # verde claro (números)

ax.text(8, 10.6, "Extracto de integración de Gemini AI en el backend (NestJS)",
        ha='center', va='center', fontsize=14, fontweight='bold', color=COLOR_TITULO)

# Marco del editor
editor = FancyBboxPatch((0.5, 0.5), 15.0, 9.7,
                         boxstyle="round,pad=0.04,rounding_size=0.12",
                         facecolor=COLOR_FONDO, edgecolor=COLOR_BORDE, linewidth=2)
ax.add_patch(editor)

# Tab del archivo
tab = FancyBboxPatch((0.7, 9.55), 4.5, 0.55,
                      boxstyle="round,pad=0.02,rounding_size=0.04",
                      facecolor='#2D2D30', edgecolor='#3F3F46', linewidth=1)
ax.add_patch(tab)
ax.text(0.95, 9.83, "feedback.service.ts", ha='left', va='center',
        fontsize=10, color=COLOR_TEXT, family='monospace')

# Líneas de código - cada una un (linea_num, segmentos[(texto, color)])
lineas = [
    (1,  [("import", COLOR_KEYWORD), (" { Injectable } ", COLOR_TEXT),
          ("from", COLOR_KEYWORD), (" '@nestjs/common';", COLOR_STRING)]),
    (2,  [("import", COLOR_KEYWORD), (" { GoogleGenerativeAI } ", COLOR_TEXT),
          ("from", COLOR_KEYWORD), (" '@google/generative-ai';", COLOR_STRING)]),
    (3,  [("", COLOR_TEXT)]),
    (4,  [("@Injectable()", COLOR_FUNC)]),
    (5,  [("export", COLOR_KEYWORD), (" ", COLOR_TEXT),
          ("class", COLOR_KEYWORD), (" ", COLOR_TEXT),
          ("FeedbackService", COLOR_TYPE), (" {", COLOR_TEXT)]),
    (6,  [("  ", COLOR_TEXT), ("private", COLOR_KEYWORD), (" genAI = ", COLOR_TEXT),
          ("new", COLOR_KEYWORD), (" ", COLOR_TEXT),
          ("GoogleGenerativeAI", COLOR_TYPE),
          ("(process.env.GEMINI_API_KEY);", COLOR_TEXT)]),
    (7,  [("", COLOR_TEXT)]),
    (8,  [("  ", COLOR_TEXT),
          ("// Genera retroalimentación motivacional para el estudiante", COLOR_COMMENT)]),
    (9,  [("  ", COLOR_TEXT), ("async", COLOR_KEYWORD), (" ", COLOR_TEXT),
          ("generarFeedback", COLOR_FUNC),
          ("(resultado: ", COLOR_TEXT),
          ("ResultadoEvaluacion", COLOR_TYPE), ("):", COLOR_TEXT),
          (" Promise<", COLOR_TEXT), ("string", COLOR_TYPE), ("> {", COLOR_TEXT)]),
    (10, [("    ", COLOR_TEXT), ("const", COLOR_KEYWORD), (" model = ", COLOR_TEXT),
          ("this", COLOR_KEYWORD),
          (".genAI.getGenerativeModel({", COLOR_TEXT)]),
    (11, [("      model: ", COLOR_TEXT), ("'gemini-1.5-flash'", COLOR_STRING),
          (" });", COLOR_TEXT)]),
    (12, [("", COLOR_TEXT)]),
    (13, [("    ", COLOR_TEXT), ("const", COLOR_KEYWORD),
          (" prompt = ", COLOR_TEXT),
          ("`Eres un tutor amable de matemáticas. ", COLOR_STRING)]),
    (14, [("      El estudiante obtuvo ${resultado.porcentaje}% en ", COLOR_STRING),
          ("${resultado.tema}.", COLOR_STRING)]),
    (15, [("      Genera un mensaje motivacional breve, con un tip ", COLOR_STRING),
          ("práctico y un emoji.`;", COLOR_STRING)]),
    (16, [("", COLOR_TEXT)]),
    (17, [("    ", COLOR_TEXT), ("const", COLOR_KEYWORD),
          (" response = ", COLOR_TEXT),
          ("await", COLOR_KEYWORD),
          (" model.", COLOR_TEXT),
          ("generateContent", COLOR_FUNC),
          ("(prompt);", COLOR_TEXT)]),
    (18, [("    ", COLOR_TEXT), ("return", COLOR_KEYWORD),
          (" response.response.", COLOR_TEXT),
          ("text", COLOR_FUNC), ("();", COLOR_TEXT)]),
    (19, [("  }", COLOR_TEXT)]),
    (20, [("}", COLOR_TEXT)]),
]

# Renderizar líneas
y_start = 9.0
y_step = 0.42
font_props = {'family': 'monospace', 'fontsize': 10}

for num, segmentos in lineas:
    y = y_start - (num - 1) * y_step
    # Número de línea
    ax.text(0.95, y, str(num).rjust(2), ha='left', va='center',
            color='#858585', **font_props)
    # Texto coloreado por segmentos
    x_cursor = 1.55
    for texto, color in segmentos:
        ax.text(x_cursor, y, texto, ha='left', va='center',
                color=color, **font_props)
        # Avance horizontal aproximado por carácter
        x_cursor += 0.085 * len(texto)

# Pie con anotación
ax.text(8, 0.3, "Servicio NestJS que invoca el modelo Gemini para producir feedback adaptativo basado en el desempeño",
        ha='center', va='center', fontsize=9, style='italic', color="#444")

plt.tight_layout()
plt.savefig('/home/claude/proyecto/latex/figuras/fig09_gemini_ai.pdf',
            format='pdf', bbox_inches='tight', dpi=300)
plt.close()
print("Figura 9 generada")
