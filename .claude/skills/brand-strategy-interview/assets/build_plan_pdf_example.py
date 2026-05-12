#!/usr/bin/env python3
"""
Concrete Authority — strategic brand plan PDF for Electriclick.
A4 portrait, editorial agency layout, type-led, no decoration.
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

# ──────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────
OUT = Path("/Users/erikgamboa/Documents/CMO/projects/electro-shop/01-plan-estrategico.pdf")
FONT_DIR = Path.home() / ".claude/skills/canvas-design/canvas-fonts"

# Palette — rationed, considered for weeks
INK      = HexColor("#0F1A2B")   # navy authority
PAPER    = HexColor("#F4EFE7")   # warm archival off-white
COPPER   = HexColor("#B85C2C")   # single industrial accent
CHARCOAL = HexColor("#3A3A3A")   # secondary text
RULE     = HexColor("#C8BCA9")   # faint divider
WHISPER  = HexColor("#7A7264")   # captions, metadata
SUBPAPER = HexColor("#EAE2D4")   # subtle inset panels

PAGE_W, PAGE_H = A4
MARGIN_X = 22 * mm
MARGIN_TOP = 26 * mm
MARGIN_BOTTOM = 26 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

# ──────────────────────────────────────────────────────────────────────────
# FONTS
# ──────────────────────────────────────────────────────────────────────────
FONTS = {
    "Display":           "Gloock-Regular.ttf",              # monumental serif
    "Body":              "CrimsonPro-Regular.ttf",          # reading serif
    "BodyItalic":        "CrimsonPro-Italic.ttf",           # body italic
    "BodyBold":          "CrimsonPro-Bold.ttf",             # body bold
    "Sans":              "InstrumentSans-Regular.ttf",      # geometric sans
    "SansBold":          "InstrumentSans-Bold.ttf",
    "SansItalic":        "InstrumentSans-Italic.ttf",
    "Mono":              "DMMono-Regular.ttf",              # metadata
    "Numeral":           "Gloock-Regular.ttf",              # large serif numerals
}
for name, fn in FONTS.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / fn)))


# ──────────────────────────────────────────────────────────────────────────
# CANVAS HELPERS
# ──────────────────────────────────────────────────────────────────────────
def fill_paper(c: rl_canvas.Canvas):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(INK)

def hairline(c, x1, y, x2, color=RULE, width=0.4):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)

def vrule(c, x, y1, y2, color=RULE, width=0.4):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x, y1, x, y2)

def running_header(c, label, section_num=None):
    """Top-of-page rail. Tiny, structural, never decorative."""
    y = PAGE_H - MARGIN_TOP + 10 * mm
    c.setFillColor(WHISPER)
    c.setFont("Mono", 6.5)
    c.drawString(MARGIN_X, y, "ELECTRICLICK  ·  PLAN ESTRATÉGICO DE MARCA")
    c.drawRightString(PAGE_W - MARGIN_X, y, "VERSIÓN 1  ·  2026")
    hairline(c, MARGIN_X, y - 2.5*mm, PAGE_W - MARGIN_X, RULE, 0.35)

def folio(c, page_num, section_label=None):
    """Bottom rail. Page number + section pulse."""
    y = MARGIN_BOTTOM - 12 * mm
    hairline(c, MARGIN_X, y + 4*mm, PAGE_W - MARGIN_X, RULE, 0.35)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 6.5)
    if section_label:
        c.drawString(MARGIN_X, y, section_label.upper())
    c.setFont("Sans", 8)
    c.setFillColor(INK)
    c.drawRightString(PAGE_W - MARGIN_X, y, f"{page_num:02d}")

def section_numeral(c, num, x, y, size=92, color=None):
    """Massive serif numeral — gravestone marker."""
    c.setFillColor(color or INK)
    c.setFont("Numeral", size)
    c.drawString(x, y, num)
    c.setFillColor(INK)

def wrap_text(c, text, font, size, max_w):
    """Word-wrap returning list of lines."""
    words = text.split()
    lines = []
    current = []
    c.setFont(font, size)
    for w in words:
        candidate = (" ".join(current + [w])).strip()
        if pdfmetrics.stringWidth(candidate, font, size) <= max_w:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines

def draw_paragraph(c, text, x, y, font, size, leading, max_w, color=INK):
    """Returns y of last baseline."""
    c.setFillColor(color)
    lines = wrap_text(c, text, font, size, max_w)
    c.setFont(font, size)
    cy = y
    for line in lines:
        c.drawString(x, cy, line)
        cy -= leading
    return cy + leading  # baseline of last line


# ──────────────────────────────────────────────────────────────────────────
# PAGE 1 — COVER
# ──────────────────────────────────────────────────────────────────────────
def page_cover(c, page_num):
    fill_paper(c)

    # Top rail — minimal, archival
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 24*mm, "DOCUMENTO 01  /  03")
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 24*mm, "EDICIÓN VERSIÓN 1")
    hairline(c, MARGIN_X, PAGE_H - 27*mm, PAGE_W - MARGIN_X, INK, 0.6)

    # Eyebrow
    c.setFillColor(CHARCOAL)
    c.setFont("Sans", 9)
    c.drawString(MARGIN_X, PAGE_H - 60*mm, "PLAN ESTRATÉGICO DE MARCA")
    c.setFillColor(COPPER)
    c.setFont("SansBold", 9)
    c.drawString(MARGIN_X + 65*mm, PAGE_H - 60*mm, "—  CLUB DEL ELECTRICISTA")

    # Massive wordmark
    c.setFillColor(INK)
    c.setFont("Display", 96)
    c.drawString(MARGIN_X - 2*mm, PAGE_H - 130*mm, "Electri")
    c.drawString(MARGIN_X - 2*mm, PAGE_H - 168*mm, "click.")

    # Hairline beneath wordmark
    hairline(c, MARGIN_X, PAGE_H - 178*mm, PAGE_W - MARGIN_X, INK, 0.6)

    # Sub-statement
    c.setFillColor(CHARCOAL)
    c.setFont("BodyItalic", 14)
    sub_lines = wrap_text(c,
        "El club online del electricista mexicano. Material a tu obra, beneficios que crecen contigo.",
        "BodyItalic", 14, CONTENT_W - 40*mm)
    sy = PAGE_H - 192*mm
    for line in sub_lines:
        c.drawString(MARGIN_X, sy, line)
        sy -= 18

    # Footer — three-column index
    fy = MARGIN_BOTTOM + 28*mm
    hairline(c, MARGIN_X, fy + 12*mm, PAGE_W - MARGIN_X, RULE, 0.35)

    col_w = CONTENT_W / 3
    cols = [
        ("PREPARADO PARA", "Founder · Equipo fundador\nElectriclick"),
        ("PREPARADO POR", "CMO Agency\nBrand Strategy Practice"),
        ("FECHA DE EDICIÓN", "12 de mayo, 2026\nGuadalajara, México"),
    ]
    for i, (label, content) in enumerate(cols):
        cx = MARGIN_X + i * col_w
        c.setFillColor(WHISPER)
        c.setFont("Mono", 6.5)
        c.drawString(cx, fy + 2*mm, label)
        c.setFillColor(INK)
        c.setFont("Sans", 9)
        for j, line in enumerate(content.split("\n")):
            c.drawString(cx, fy - 4*mm - j*11, line)

    # Closing rail
    hairline(c, MARGIN_X, MARGIN_BOTTOM - 4*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 6.5)
    c.drawString(MARGIN_X, MARGIN_BOTTOM - 9*mm, "CONFIDENCIAL  ·  USO INTERNO  ·  NO DISTRIBUIR SIN AUTORIZACIÓN")
    c.drawRightString(PAGE_W - MARGIN_X, MARGIN_BOTTOM - 9*mm, f"PÁGINA {page_num:02d}")

    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 2 — TABLA DE CONTENIDOS
# ──────────────────────────────────────────────────────────────────────────
TOC = [
    ("01", "Misión",                     "El propósito que sostiene la operación."),
    ("02", "Visión",                     "El futuro al que nos comprometemos."),
    ("03", "Valores de marca",           "Cinco principios accionables, no decorativos."),
    ("04", "Propuesta de valor",         "Qué prometemos, a quién, contra qué alternativas."),
    ("05", "Posicionamiento",            "El espacio que ocupamos en la mente del electricista."),
    ("06", "Público objetivo",           "Tres círculos concéntricos de clientes."),
    ("07", "Quién no es cliente",        "La disciplina del foco."),
    ("08", "Buyer Persona",              "Don Memo, el maestro electricista."),
    ("09", "Personalidad de marca",      "El compa que sabe."),
    ("10", "Tono de voz",                "Cómo hablamos, cómo no."),
    ("11", "Anexo",                      "Decisiones de negocio y pendientes."),
]

def page_toc(c, page_num):
    fill_paper(c)
    running_header(c, "Tabla de contenidos")

    # Section header
    section_numeral(c, "00", MARGIN_X, PAGE_H - 80*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 38)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 70*mm, "Contenido")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 76*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 81*mm, "ÍNDICE DE SECCIONES  ·  11 ENTRADAS")

    # TOC entries — tighter rhythm so all 11 fit comfortably above the folio
    y = PAGE_H - 112*mm
    row_h = 14.5*mm
    for num, title, sub in TOC:
        # Number
        c.setFillColor(COPPER)
        c.setFont("Numeral", 20)
        c.drawString(MARGIN_X, y, num)
        # Title
        c.setFillColor(INK)
        c.setFont("Display", 16)
        c.drawString(MARGIN_X + 16*mm, y, title)
        # Subtitle
        c.setFillColor(WHISPER)
        c.setFont("BodyItalic", 10.5)
        c.drawString(MARGIN_X + 16*mm, y - 5.2*mm, sub)
        # Hairline
        hairline(c, MARGIN_X + 16*mm, y - 9*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        y -= row_h

    folio(c, page_num, "Contenido")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 3 — MISIÓN + VISIÓN (spread, but single page A4)
# ──────────────────────────────────────────────────────────────────────────
def page_mission_vision(c, page_num):
    fill_paper(c)
    running_header(c, "Misión y visión")

    # ── MISIÓN ──
    c.setFillColor(COPPER)
    c.setFont("Numeral", 96)
    c.drawString(MARGIN_X, PAGE_H - 75*mm, "01")
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 42*mm, PAGE_H - 50*mm, "SECCIÓN")
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 42*mm, PAGE_H - 62*mm, "Misión")
    hairline(c, MARGIN_X + 42*mm, PAGE_H - 68*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 42*mm, PAGE_H - 73*mm, "QUÉ HACEMOS, PARA QUIÉN, CON QUÉ VALOR")

    mision_text = ("Hacer que cualquier electricista o contratista en México pueda mantener su obra en marcha "
                   "sin parar a comprar — entregándole el material eléctrico que necesita, al lugar donde está "
                   "trabajando, con beneficios crecientes por ser parte del club.")
    draw_paragraph(c, mision_text, MARGIN_X + 42*mm, PAGE_H - 92*mm,
                   "Body", 15, 22, CONTENT_W - 42*mm, INK)

    # Divider band
    hairline(c, MARGIN_X, PAGE_H/2 - 6*mm, PAGE_W - MARGIN_X, INK, 0.8)

    # ── VISIÓN ──
    vy_top = PAGE_H/2 - 22*mm
    c.setFillColor(COPPER)
    c.setFont("Numeral", 96)
    c.drawString(MARGIN_X, vy_top - 25*mm, "02")
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 42*mm, vy_top, "SECCIÓN")
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 42*mm, vy_top - 12*mm, "Visión")
    hairline(c, MARGIN_X + 42*mm, vy_top - 18*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 42*mm, vy_top - 23*mm, "EL FUTURO AL QUE NOS COMPROMETEMOS")

    vision_text = ("Convertirnos en la plataforma que profesionaliza y dignifica al electricista mexicano — el "
                   "lugar donde no solo encuentra todo lo que necesita para su obra, sino donde crece como "
                   "profesional, se conecta con su gremio y construye un futuro mejor para su oficio.")
    draw_paragraph(c, vision_text, MARGIN_X + 42*mm, vy_top - 42*mm,
                   "Body", 15, 22, CONTENT_W - 42*mm, INK)

    folio(c, page_num, "01–02  ·  Misión / Visión")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 4 — VALORES DE MARCA
# ──────────────────────────────────────────────────────────────────────────
VALORES = [
    ("01", "Tu tiempo vale más que un viaje a la ferretería",
     "No prometemos entrega en 2 horas — prometemos que mientras tu pedido viaja, tú sigues trabajando y "
     "facturando. Te ahorramos los traslados, las filas, los \"no hay stock\", los recorridos a 3 ferreterías "
     "para juntar todo. En 2-4 días llega lo que necesitas, completo, a donde estás. Tu tiempo es tu activo "
     "más caro: lo cuidamos."),
    ("02", "Respeto al oficio",
     "Tratamos al electricista como el profesional que es, no como un consumidor más. Hablamos su lenguaje, "
     "conocemos sus marcas, entendemos su día. No simplificamos en exceso ni le explicamos lo obvio."),
    ("03", "Curaduría, no catálogo infinito",
     "No vendemos todo lo que existe — vendemos lo que un electricista profesional realmente necesita y puede "
     "confiar. Calidad sobre cantidad. Una marca menos pero mejor que diez con baja rotación."),
    ("04", "El club crece contigo",
     "Mientras más trabajas con nosotros, más recibes: descuentos, capacitaciones, cashback, acceso. La "
     "membresía es una relación a largo plazo, no una transacción suelta. Premiamos la lealtad porque la "
     "valoramos."),
    ("05", "Aliados, no proveedores",
     "Las marcas (Schneider, Steren, Volteck, Cooper, Bticino, etc.) no son catálogo — son aliados "
     "estratégicos. Las traemos a capacitar, a co-crear contenido, a desarrollar al electricista. Eso eleva "
     "la categoría completa."),
]

def page_valores(c, page_num):
    fill_paper(c)
    running_header(c, "Valores")

    # Section header
    section_numeral(c, "03", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Valores de marca")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "CINCO PRINCIPIOS ACCIONABLES  ·  CÓMO SE MANIFIESTAN EN OPERACIÓN")

    # Values stack
    y = PAGE_H - 88*mm
    for num, title, body in VALORES:
        # Number column
        c.setFillColor(COPPER)
        c.setFont("Numeral", 26)
        c.drawString(MARGIN_X, y, num)
        # Title
        c.setFillColor(INK)
        c.setFont("Display", 16)
        title_lines = wrap_text(c, title, "Display", 16, CONTENT_W - 22*mm)
        ty = y
        for line in title_lines:
            c.drawString(MARGIN_X + 22*mm, ty, line)
            ty -= 19
        # Body
        body_y = ty - 4
        body_y = draw_paragraph(c, body, MARGIN_X + 22*mm, body_y,
                                "Body", 10, 13.5, CONTENT_W - 22*mm, CHARCOAL)
        # Divider
        hairline(c, MARGIN_X, body_y - 6*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        y = body_y - 12*mm

    folio(c, page_num, "03  ·  Valores")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 5 — PROPUESTA DE VALOR
# ──────────────────────────────────────────────────────────────────────────
def page_propuesta(c, page_num):
    fill_paper(c)
    running_header(c, "Propuesta de valor")

    section_numeral(c, "04", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Propuesta de valor")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "QUÉ PROMETEMOS  ·  A QUIÉN  ·  CONTRA QUÉ ALTERNATIVAS")

    # Eyebrow: full version
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 84*mm, "VERSIÓN COMPLETA  ·  USO INTERNO")
    hairline(c, MARGIN_X, PAGE_H - 86*mm, MARGIN_X + 80*mm, INK, 0.4)

    full_text = ("Para electricistas y contratistas en México que pierden tiempo y dinero recorriendo ferreterías "
                 "para conseguir material, Electriclick es el club online de material eléctrico que te entrega "
                 "lo que necesitas directo a tu obra y te recompensa por ser socio — con descuentos por nivel, "
                 "capacitaciones de marca y cashback. A diferencia de las ferreterías tradicionales y los "
                 "marketplaces genéricos, no solo te vendemos: invertimos en hacerte crecer como profesional.")
    bottom_y = draw_paragraph(c, full_text, MARGIN_X, PAGE_H - 94*mm,
                              "Body", 13, 19, CONTENT_W, INK)

    # Short version — pull quote
    short_y_top = bottom_y - 22*mm
    hairline(c, MARGIN_X, short_y_top + 5*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, short_y_top - 2*mm, "VERSIÓN CORTA  ·  WEB / ADS")

    c.setFillColor(INK)
    c.setFont("BodyItalic", 22)
    quote_lines = wrap_text(c,
        "El club online del electricista mexicano. Material a tu obra, beneficios que crecen contigo.",
        "BodyItalic", 22, CONTENT_W - 10*mm)
    qy = short_y_top - 16*mm
    for line in quote_lines:
        c.drawString(MARGIN_X + 5*mm, qy, line)
        qy -= 28

    # Tagline
    tag_y = qy - 14*mm
    hairline(c, MARGIN_X, tag_y + 8*mm, PAGE_W - MARGIN_X, RULE, 0.4)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, tag_y, "TAGLINE  ·  ULTRA-CORTO")
    c.setFillColor(COPPER)
    c.setFont("Display", 18)
    c.drawString(MARGIN_X, tag_y - 12*mm, "Material eléctrico, en un click. Beneficios, en cada compra.")

    folio(c, page_num, "04  ·  Propuesta de valor")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 6 — POSICIONAMIENTO
# ──────────────────────────────────────────────────────────────────────────
COMPETIDORES = [
    ("Ferretería de barrio",
     "Cercana, lenta, surtido limitado.",
     "Te ahorra el viaje y tiene siempre lo que pides."),
    ("Home Depot / Sodimac",
     "Surtida, pero hecha para el dueño de casa.",
     "Hecha 100% para el pro, no el amateur."),
    ("Mercado Libre / Amazon",
     "Variedad infinita, sin curaduría, calidad inconsistente.",
     "Curado, marcas certificadas, asesoría real."),
    ("Distribuidores mayoristas",
     "Buenos precios, piden volumen.",
     "Atendemos al \"uno-uno\" sin pedir mínimos."),
]

def page_posicionamiento(c, page_num):
    fill_paper(c)
    running_header(c, "Posicionamiento")

    section_numeral(c, "05", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Posicionamiento")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "EL ESPACIO QUE OCUPAMOS EN LA MENTE DEL CLIENTE")

    # Statement
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 84*mm, "STATEMENT COMPLETO")
    hairline(c, MARGIN_X, PAGE_H - 86*mm, MARGIN_X + 60*mm, INK, 0.4)

    stmt = ("Electriclick es la única plataforma en México diseñada exclusivamente para el electricista "
            "profesional, no para el consumidor final ni para grandes empresas. Mientras las ferreterías te "
            "hacen ir, las grandes superficies te tratan como amateur, y los marketplaces te dejan solo, "
            "nosotros te entregamos material curado a tu obra y te integramos a un club donde mientras más "
            "trabajas, más ganas.")
    after_stmt = draw_paragraph(c, stmt, MARGIN_X, PAGE_H - 94*mm,
                                 "Body", 12, 18, CONTENT_W, INK)

    # Pull quote
    pq_top = after_stmt - 16*mm
    hairline(c, MARGIN_X, pq_top + 4*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, pq_top - 3*mm, "FRASE CORTA  ·  PITCH")
    c.setFillColor(COPPER)
    c.setFont("BodyItalic", 18)
    pq_lines = wrap_text(c,
        "El primer club online en México hecho exclusivamente para el electricista y contratista profesional.",
        "BodyItalic", 18, CONTENT_W - 6*mm)
    py = pq_top - 14*mm
    for line in pq_lines:
        c.drawString(MARGIN_X + 3*mm, py, line)
        py -= 23

    # Competitive map
    map_top = py - 14*mm
    hairline(c, MARGIN_X, map_top + 4*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, map_top - 3*mm, "MAPA COMPETITIVO")

    # Three-column header
    th_y = map_top - 14*mm
    col1_x = MARGIN_X
    col2_x = MARGIN_X + 55*mm
    col3_x = MARGIN_X + 115*mm
    c.setFillColor(INK)
    c.setFont("SansBold", 8)
    c.drawString(col1_x, th_y, "JUGADOR")
    c.drawString(col2_x, th_y, "PERCEPCIÓN ACTUAL")
    c.drawString(col3_x, th_y, "POR QUÉ ELECTRICLICK GANA")
    hairline(c, MARGIN_X, th_y - 3*mm, PAGE_W - MARGIN_X, INK, 0.5)

    # Rows
    row_y = th_y - 10*mm
    for who, perception, win in COMPETIDORES:
        c.setFillColor(INK)
        c.setFont("BodyBold", 10)
        who_lines = wrap_text(c, who, "BodyBold", 10, 50*mm)
        for i, line in enumerate(who_lines):
            c.drawString(col1_x, row_y - i*13, line)

        c.setFillColor(CHARCOAL)
        c.setFont("Body", 10)
        perc_lines = wrap_text(c, perception, "Body", 10, 56*mm)
        for i, line in enumerate(perc_lines):
            c.drawString(col2_x, row_y - i*13, line)

        c.setFillColor(INK)
        c.setFont("BodyItalic", 10)
        win_lines = wrap_text(c, win, "BodyItalic", 10, CONTENT_W - 115*mm + MARGIN_X)
        for i, line in enumerate(win_lines):
            c.drawString(col3_x, row_y - i*13, line)

        max_lines = max(len(who_lines), len(perc_lines), len(win_lines))
        row_y -= max_lines * 13 + 4*mm
        hairline(c, MARGIN_X, row_y + 1*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        row_y -= 4*mm

    folio(c, page_num, "05  ·  Posicionamiento")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 7 — PÚBLICO OBJETIVO
# ──────────────────────────────────────────────────────────────────────────
def page_publico(c, page_num):
    fill_paper(c)
    running_header(c, "Público objetivo")

    section_numeral(c, "06", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Público y nicho")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "TRES CÍRCULOS CONCÉNTRICOS DE CLIENTES  ·  GEOGRAFÍA / MODELO")

    # Geo + modelo strip
    strip_y = PAGE_H - 84*mm
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, strip_y, "GEOGRAFÍA")
    c.drawString(MARGIN_X + 95*mm, strip_y, "MODELO")
    hairline(c, MARGIN_X, strip_y - 2*mm, MARGIN_X + 60*mm, INK, 0.4)
    hairline(c, MARGIN_X + 95*mm, strip_y - 2*mm, MARGIN_X + 95*mm + 60*mm, INK, 0.4)

    c.setFillColor(INK)
    c.setFont("Body", 10.5)
    geo_lines = wrap_text(c,
        "México, arranque desde Guadalajara (Bajío + Occidente con cobertura nacional vía paquetería). "
        "Expansión natural a CDMX, Monterrey, Querétaro.",
        "Body", 10.5, 85*mm)
    for i, line in enumerate(geo_lines):
        c.drawString(MARGIN_X, strip_y - 9*mm - i*14, line)

    mod_lines = wrap_text(c,
        "B2B-pro 100% al usuario final del oficio (electricista o contratista), sin venta a ferreterías "
        "para reventa.",
        "Body", 10.5, 75*mm)
    for i, line in enumerate(mod_lines):
        c.drawString(MARGIN_X + 95*mm, strip_y - 9*mm - i*14, line)

    # Tiers
    tier_top = strip_y - 9*mm - max(len(geo_lines), len(mod_lines))*14 - 14*mm
    hairline(c, MARGIN_X, tier_top + 6*mm, PAGE_W - MARGIN_X, INK, 0.6)

    tiers = [
        ("70%", "Cliente primario", "EL MAESTRO ELECTRICISTA",
         "Electricista profesional independiente o con cuadrilla pequeña (1-5 personas), 28-50 años, "
         "hombre, basado en zonas urbanas de México. Factura entre $20K y $150K MXN al mes, "
         "principalmente trabajos residenciales y comerciales medianos: instalaciones nuevas, "
         "remodelaciones, mantenimientos, tableros. Tiene WhatsApp todo el día, usa Facebook y YouTube "
         "para tutoriales, compra hoy en ferreterías de confianza pero ya pidió cosas por Mercado Libre. "
         "No es novato — lleva 5+ años en el oficio."),
        ("20%", "Cliente secundario", "EL CONTRATISTA",
         "Contratista o constructor pequeño/mediano que subcontrata electricistas o tiene su propio "
         "equipo. 35-55 años. Lleva obras de $300K-$5M MXN. Compra material por proyecto, necesita "
         "facturas formales, valora la confiabilidad y entrega coordinada más que el precio."),
        ("10%", "Cliente terciario", "DELEGADO  ·  LISTA DEL MAESTRO",
         "Cliente final del electricista (ama de casa, dueño de obra, administrador) que entra a comprar "
         "SOLO porque su electricista le compartió una lista predefinida (funcionalidad \"Lista del Maestro\" "
         "— fase 2 del producto). Le hablamos en lenguaje claro, le explicamos que está comprando lo "
         "correcto porque \"tu electricista lo eligió\"."),
    ]

    y = tier_top
    for pct, label, sub, body in tiers:
        # Percentage hero
        c.setFillColor(COPPER)
        c.setFont("Numeral", 38)
        c.drawString(MARGIN_X, y - 10*mm, pct)
        # Label
        c.setFillColor(INK)
        c.setFont("Display", 16)
        c.drawString(MARGIN_X + 32*mm, y - 4*mm, label)
        c.setFillColor(WHISPER)
        c.setFont("Mono", 7)
        c.drawString(MARGIN_X + 32*mm, y - 9*mm, sub)
        # Body
        by = y - 16*mm
        by = draw_paragraph(c, body, MARGIN_X + 32*mm, by,
                            "Body", 9.5, 13, CONTENT_W - 32*mm, CHARCOAL)
        # Divider
        hairline(c, MARGIN_X, by - 5*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        y = by - 10*mm

    folio(c, page_num, "06  ·  Público y nicho")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 8 — QUIÉN NO ES CLIENTE
# ──────────────────────────────────────────────────────────────────────────
NO_CLIENTES = [
    ("El ama de casa que cambia un foco",
     "Consumidor amateur — no es nuestro foco. Hay otros canales que lo atienden bien."),
    ("El \"hazlo tú mismo\" amateur",
     "El DIY ocasional no construye un club; nuestra economía depende de la frecuencia profesional."),
    ("Las grandes constructoras corporativas",
     "Compran por licitación, no por club. Es otro modelo de negocio, otra fuerza comercial."),
    ("Las ferreterías que quieren revender",
     "Somos B2B-pro al usuario final. Reventa diluye la curaduría y la promesa."),
]

def page_no_cliente(c, page_num):
    fill_paper(c)
    running_header(c, "Quién no es cliente")

    section_numeral(c, "07", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Quién no es cliente")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "LA DISCIPLINA DEL FOCO  ·  CUATRO EXCLUSIONES DELIBERADAS")

    # Intro
    c.setFillColor(CHARCOAL)
    c.setFont("BodyItalic", 13)
    intro = ("Una marca se define tanto por a quién atiende como por a quién decide no atender. Estas "
             "cuatro audiencias quedan deliberadamente fuera del foco; cualquier desviación dispersa la "
             "propuesta.")
    intro_lines = wrap_text(c, intro, "BodyItalic", 13, CONTENT_W - 10*mm)
    iy = PAGE_H - 84*mm
    for line in intro_lines:
        c.drawString(MARGIN_X + 5*mm, iy, line)
        iy -= 19

    # Strikethrough cards
    y = iy - 18*mm
    hairline(c, MARGIN_X, y + 6*mm, PAGE_W - MARGIN_X, INK, 0.6)

    for who, rationale in NO_CLIENTES:
        # The "no" mark — tasteful cross
        c.setFillColor(COPPER)
        c.setLineWidth(0.8)
        c.setStrokeColor(COPPER)
        c.line(MARGIN_X, y - 4*mm, MARGIN_X + 8*mm, y - 4*mm)

        c.setFillColor(INK)
        c.setFont("Display", 17)
        who_lines = wrap_text(c, who, "Display", 17, CONTENT_W - 14*mm)
        ty = y
        for line in who_lines:
            c.drawString(MARGIN_X + 14*mm, ty, line)
            # Subtle line-through of the title — only on the first line
            if line == who_lines[0]:
                lw = pdfmetrics.stringWidth(line, "Display", 17)
                c.setStrokeColor(COPPER)
                c.setLineWidth(0.6)
                c.line(MARGIN_X + 14*mm, ty + 5, MARGIN_X + 14*mm + lw, ty + 5)
            ty -= 22

        c.setFillColor(CHARCOAL)
        c.setFont("Body", 11)
        rat_y = ty - 2
        rat_y = draw_paragraph(c, rationale, MARGIN_X + 14*mm, rat_y,
                               "Body", 11, 15, CONTENT_W - 14*mm, CHARCOAL)
        hairline(c, MARGIN_X, rat_y - 6*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        y = rat_y - 12*mm

    folio(c, page_num, "07  ·  Quién no es cliente")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 9 — BUYER PERSONA
# ──────────────────────────────────────────────────────────────────────────
PERSONA = [
    ("DEMOGRAFÍA",
     "38 años, casado, 2 hijos, vive en Tlaquepaque (zona conurbada GDL). Carrera técnica en electricidad "
     "(CONALEP/CECATI) + 15 años en el oficio. Ingreso $35K-$60K MXN/mes brutos. Camioneta Nissan NP300 "
     "2017 equipada con herramienta."),
    ("PSICOGRAFÍA",
     "Orgulloso de su oficio. Pragmático, no le gusta perder tiempo. Lealtad a marcas que le han "
     "funcionado. Aspiracional — quiere tener su propio \"negocio\" (3-4 cuadrillas) algún día. Valora el "
     "respeto y odia que lo traten como amateur."),
    ("GOALS",
     "(1) Sacar más obras al mes sin trabajar más horas. (2) Que sus clientes lo recomienden y dejen de "
     "regatear. (3) Que su hijo mayor entre a la prepa. (4) Tener su propio negocio con varias cuadrillas. "
     "(5) Que las marcas grandes (Schneider, Bticino, Steren) lo certifiquen."),
    ("PAIN POINTS",
     "(1) Pierde 4-6 horas/semana en ferreterías. (2) Ferretería local no siempre tiene el calibre "
     "exacto. (3) Cuando le falta algo a media obra, manda al ayudante y pierde productividad de los dos. "
     "(4) Clientes nuevos siempre regatean. (5) No sabe facturar formalmente — pierde corporativos. "
     "(6) Compró en Mercado Libre y le llegaron piratas."),
    ("COMPORTAMIENTO",
     "Compra 6-12 veces al mes, ticket $1,500-$4,000 MXN. Marcas que respeta: Condumex, Schneider, "
     "Bticino, Steren, Volteck, Truper, Cooper, IUSA. Decide rápido si confía. Paga 70% efectivo, 20% "
     "transfer, 10% tarjeta. Pide factura solo cuando el cliente se la pide (~40% de las veces)."),
    ("OBJECIONES",
     "\"¿Y si me llega pirata?\" — marcas reconocidas, fotos reales. \"¿Y si no llega a tiempo?\" — fechas "
     "claras. \"¿Y si está más caro que la ferretería?\" — ahorro de tiempo cuantificado. \"¿Y si me "
     "equivoco de medida?\" — asesoría rápida vía WhatsApp. \"¿Y si no me dan factura?\" — facturación "
     "inmediata."),
    ("CANALES",
     "WhatsApp (#1, todo el día), Facebook (grupos de electricistas, marketplace), YouTube (tutoriales "
     "técnicos), TikTok (consume tips/memes del oficio, no publica), Instagram (poco), Google (busca "
     "por nombre técnico)."),
    ("MENSAJE CLAVE",
     "\"Memo, mientras tú facturas otra obra, nosotros te llevamos lo que pediste a donde estás. Cable "
     "Condumex, marca certificada, factura al instante, llega en 2-3 días. Y entre más nos compras, más "
     "beneficios desbloqueas. Esto es para los profesionales como tú.\""),
]

def page_persona_a(c, page_num):
    """Page 9: dossier card — demografía, psicografía, goals, pain points."""
    fill_paper(c)
    running_header(c, "Buyer Persona")

    section_numeral(c, "08", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Buyer Persona")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "DOSSIER PRIMARIO  ·  EL MAESTRO ELECTRICISTA")

    # Name + label
    name_y = PAGE_H - 86*mm
    c.setFillColor(INK)
    c.setFont("Display", 30)
    c.drawString(MARGIN_X, name_y, "Don Memo")
    c.setFillColor(COPPER)
    c.setFont("BodyItalic", 16)
    c.drawString(MARGIN_X, name_y - 9*mm, "Guillermo \"Memo\" Hernández  ·  El Maestro Electricista")

    hairline(c, MARGIN_X, name_y - 14*mm, PAGE_W - MARGIN_X, INK, 0.6)

    # 4 sections on this page
    y = name_y - 26*mm
    for label, body in PERSONA[:4]:
        c.setFillColor(WHISPER)
        c.setFont("Mono", 7)
        c.drawString(MARGIN_X, y, label)
        c.setFillColor(COPPER)
        c.setLineWidth(0.6)
        c.setStrokeColor(COPPER)
        c.line(MARGIN_X, y - 2*mm, MARGIN_X + 18*mm, y - 2*mm)
        c.setFillColor(INK)

        by = draw_paragraph(c, body, MARGIN_X, y - 7*mm,
                            "Body", 10.5, 14.5, CONTENT_W, INK)
        y = by - 8*mm

    folio(c, page_num, "08  ·  Buyer Persona (1/2)")
    c.showPage()


def page_persona_b(c, page_num):
    """Page 10: continuation — comportamiento, objeciones, canales, mensaje."""
    fill_paper(c)
    running_header(c, "Buyer Persona — continuación")

    # Light header
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 50*mm, "DOSSIER  ·  CONTINUACIÓN")
    c.setFillColor(INK)
    c.setFont("Display", 26)
    c.drawString(MARGIN_X, PAGE_H - 62*mm, "Don Memo — comportamiento y mensaje")
    hairline(c, MARGIN_X, PAGE_H - 68*mm, PAGE_W - MARGIN_X, INK, 0.6)

    y = PAGE_H - 84*mm
    for label, body in PERSONA[4:]:
        c.setFillColor(WHISPER)
        c.setFont("Mono", 7)
        c.drawString(MARGIN_X, y, label)
        c.setFillColor(COPPER)
        c.setLineWidth(0.6)
        c.setStrokeColor(COPPER)
        c.line(MARGIN_X, y - 2*mm, MARGIN_X + 18*mm, y - 2*mm)

        # MENSAJE CLAVE is the manifesto-style pull
        if label == "MENSAJE CLAVE":
            c.setFillColor(INK)
            c.setFont("BodyItalic", 14)
            mes_lines = wrap_text(c, body, "BodyItalic", 14, CONTENT_W - 6*mm)
            my = y - 9*mm
            for line in mes_lines:
                c.drawString(MARGIN_X + 3*mm, my, line)
                my -= 19
            y = my - 8*mm
        else:
            by = draw_paragraph(c, body, MARGIN_X, y - 7*mm,
                                "Body", 10.5, 14.5, CONTENT_W, INK)
            y = by - 8*mm

    folio(c, page_num, "08  ·  Buyer Persona (2/2)")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 11 — PERSONALIDAD
# ──────────────────────────────────────────────────────────────────────────
RASGOS = [
    ("01", "Profesional, no acartonado", "Sabe del oficio, pero habla relajado."),
    ("02", "Honesto con ventaja",        "Te dice: \"este cable es más caro pero te aguanta 3× más\"."),
    ("03", "Cercano, no servil",         "Te trata como igual. Dice \"qué onda, maestro\" — no \"estimado cliente\"."),
    ("04", "Práctico, no teórico",       "Te resuelve, no te explica el manual."),
    ("05", "Orgulloso del oficio",       "Entiende que ser electricista es un oficio digno, valioso, técnico."),
]

SOMOS_NO = [
    ("El compa que sabe",        "El vendedor que adula"),
    ("Técnico con calle",        "Ingeniero de corbata"),
    ("Pro mexicano",             "Marketplace gringo traducido"),
    ("Club, gremio, comunidad",  "Tienda fría, transaccional"),
    ("Honestos directos",        "Cuidadores de la susceptibilidad"),
    ("Curados y selectivos",     "\"Tenemos de todo\""),
    ("Orgullosos del oficio",    "Condescendientes con el oficio"),
    ("Modernos, digitales",      "Tradicionales, anclados al mostrador"),
    ("Aliados a largo plazo",    "Vendedores de una sola compra"),
    ("Mexicanos con sangre local", "Genéricos sin ubicación"),
]

def page_personalidad(c, page_num):
    fill_paper(c)
    running_header(c, "Personalidad")

    section_numeral(c, "09", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    # Title sized to fit: "Personalidad de marca" is long — reduce to 30 to clear right margin
    c.setFont("Display", 30)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Personalidad de marca")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "ARQUETIPO  ·  RASGOS  ·  CONTRASTES")

    # Hero positioning
    c.setFillColor(INK)
    c.setFont("Display", 44)
    c.drawString(MARGIN_X, PAGE_H - 92*mm, "El compa que sabe.")
    c.setFillColor(CHARCOAL)
    c.setFont("BodyItalic", 13)
    sub_lines = wrap_text(c,
        "Mexicano, 35-40 años, profesional con 15 años en la industria eléctrica, conoce a todos los maestros, "
        "sabe qué marca jala y cuál no, te dice las cosas como son. Te trata de tú, te da consejos prácticos "
        "sin sermones, y cuando te recomienda algo es porque sí funciona — no porque le pagan.",
        "BodyItalic", 13, CONTENT_W)
    sy = PAGE_H - 105*mm
    for line in sub_lines:
        c.drawString(MARGIN_X, sy, line)
        sy -= 18

    hairline(c, MARGIN_X, sy - 4*mm, PAGE_W - MARGIN_X, INK, 0.6)

    # Five traits — compact column
    rasgos_y = sy - 16*mm
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, rasgos_y, "CINCO RASGOS CENTRALES")
    hairline(c, MARGIN_X, rasgos_y - 2*mm, MARGIN_X + 60*mm, INK, 0.4)

    ry = rasgos_y - 9*mm
    col_w_l = (CONTENT_W - 6*mm) / 2
    for i, (num, name, desc) in enumerate(RASGOS):
        col = i % 2
        row = i // 2
        cx = MARGIN_X + col * (col_w_l + 6*mm)
        cy = ry - row * 22*mm
        c.setFillColor(COPPER)
        c.setFont("Numeral", 18)
        c.drawString(cx, cy, num)
        c.setFillColor(INK)
        c.setFont("BodyBold", 11)
        c.drawString(cx + 10*mm, cy + 1, name)
        c.setFillColor(CHARCOAL)
        c.setFont("BodyItalic", 10)
        desc_lines = wrap_text(c, desc, "BodyItalic", 10, col_w_l - 10*mm)
        dy = cy - 5*mm
        for line in desc_lines:
            c.drawString(cx + 10*mm, dy, line)
            dy -= 13

    # Arquetipo strip at bottom
    arq_y = MARGIN_BOTTOM + 16*mm
    hairline(c, MARGIN_X, arq_y + 14*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, arq_y + 9*mm, "ARQUETIPO")
    c.setFillColor(INK)
    c.setFont("Display", 16)
    c.drawString(MARGIN_X, arq_y + 1*mm, "El Sabio · 60%")
    c.drawString(MARGIN_X + 70*mm, arq_y + 1*mm, "El Hombre Común · 40%")
    c.setFillColor(CHARCOAL)
    c.setFont("BodyItalic", 9.5)
    c.drawString(MARGIN_X, arq_y - 6*mm, "El que sabe, el que asesora, el que enseña.")
    c.drawString(MARGIN_X + 70*mm, arq_y - 6*mm, "Sin pretensión, sin elitismo — uno más.")

    folio(c, page_num, "09  ·  Personalidad (1/2)")
    c.showPage()


def page_somos_no(c, page_num):
    fill_paper(c)
    running_header(c, "Somos / No somos")

    # Light header
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 50*mm, "PERSONALIDAD  ·  CONTRASTES")
    c.setFillColor(INK)
    c.setFont("Display", 30)
    c.drawString(MARGIN_X, PAGE_H - 62*mm, "Somos / No somos")
    hairline(c, MARGIN_X, PAGE_H - 68*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 73*mm, "DIEZ POLARIDADES  ·  CADA UNA DICE QUIÉN SOMOS Y CONTRA QUÉ NOS DEFINIMOS")

    # Column headers
    col_l_x = MARGIN_X
    col_div = PAGE_W / 2
    col_r_x = col_div + 4*mm

    th_y = PAGE_H - 92*mm
    c.setFillColor(INK)
    c.setFont("SansBold", 9)
    c.drawString(col_l_x, th_y, "SOMOS")
    c.setFillColor(WHISPER)
    c.drawString(col_r_x, th_y, "NO SOMOS")
    hairline(c, MARGIN_X, th_y - 3*mm, col_div - 4*mm, INK, 0.6)
    hairline(c, col_r_x, th_y - 3*mm, PAGE_W - MARGIN_X, RULE, 0.5)

    row_y = th_y - 12*mm
    for somos, no_somos in SOMOS_NO:
        # SOMOS — bold, ink
        c.setFillColor(INK)
        c.setFont("BodyBold", 12)
        c.drawString(col_l_x, row_y, somos)
        # Center mark — single delicate stroke
        c.setStrokeColor(COPPER)
        c.setLineWidth(0.5)
        c.line(col_div - 6*mm, row_y + 2, col_div - 1*mm, row_y + 2)
        # NO — italic, faded
        c.setFillColor(WHISPER)
        c.setFont("BodyItalic", 12)
        c.drawString(col_r_x, row_y, no_somos)
        hairline(c, MARGIN_X, row_y - 5*mm, PAGE_W - MARGIN_X, RULE, 0.3)
        row_y -= 12*mm

    # Brand DNA strip
    dna_y = MARGIN_BOTTOM + 14*mm
    hairline(c, MARGIN_X, dna_y + 14*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, dna_y + 9*mm, "MARCAS CON ADN PARECIDO  ·  REFERENCIA, NO COMPETENCIA")
    c.setFillColor(INK)
    c.setFont("Display", 18)
    c.drawString(MARGIN_X, dna_y, "Truper  ·  Husqvarna  ·  DeWalt  ·  REI  ·  Costco")

    folio(c, page_num, "09  ·  Personalidad (2/2)")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 13 — TONO DE VOZ (dimensiones + reglas)
# ──────────────────────────────────────────────────────────────────────────
DIMENSIONS = [
    ("Formal",        "Casual",       8,  "Tuteo siempre, expresiones mexicanas naturales."),
    ("Reservado",     "Entusiasta",   7,  "Orgullo del gremio, sin lirismo barato."),
    ("Serio",         "Divertido",    5,  "Más serio en producto/técnico, más relajado en redes."),
    ("Respetuoso",    "Irreverente",  3,  "Respeto al oficio siempre, nunca burla del electricista."),
    ("Sofisticado",   "Sencillo",     8,  "Frases cortas, cero corporativismo."),
]

def page_tono_dimensions(c, page_num):
    fill_paper(c)
    running_header(c, "Tono de voz")

    section_numeral(c, "10", MARGIN_X, PAGE_H - 60*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Tono de voz")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "CINCO DIMENSIONES  ·  REGLAS  ·  EJEMPLOS POR CANAL")

    # Dimensions plot
    plot_top = PAGE_H - 88*mm
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, plot_top, "DIMENSIONES DE VOZ  ·  POSICIÓN EN ESCALA 0—10")
    hairline(c, MARGIN_X, plot_top - 2*mm, MARGIN_X + 80*mm, INK, 0.4)

    row_h = 18*mm
    bar_left_x = MARGIN_X + 35*mm
    bar_right_x = PAGE_W - MARGIN_X - 35*mm
    bar_w = bar_right_x - bar_left_x

    y = plot_top - 14*mm
    for left, right, pos, note in DIMENSIONS:
        # Left label
        c.setFillColor(CHARCOAL)
        c.setFont("Body", 10)
        c.drawRightString(bar_left_x - 4*mm, y, left)
        # Right label
        c.drawString(bar_right_x + 4*mm, y, right)
        # Track
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(bar_left_x, y + 2, bar_right_x, y + 2)
        # Tick marks
        for tick in range(11):
            tx = bar_left_x + (tick / 10) * bar_w
            c.line(tx, y + 0.5, tx, y + 3.5)
        # Position marker
        mx = bar_left_x + (pos / 10) * bar_w
        c.setFillColor(COPPER)
        c.circle(mx, y + 2, 2.4, stroke=0, fill=1)
        # Value label
        c.setFont("Mono", 7.5)
        c.drawCentredString(mx, y + 8, f"{pos}/10")
        # Note
        c.setFillColor(WHISPER)
        c.setFont("BodyItalic", 9.5)
        note_lines = wrap_text(c, note, "BodyItalic", 9.5, CONTENT_W)
        ny = y - 5*mm
        for line in note_lines:
            c.drawString(MARGIN_X, ny, line)
            ny -= 12
        y -= row_h

    # Rules strip
    rules_y = y - 4*mm
    hairline(c, MARGIN_X, rules_y + 4*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, rules_y - 2*mm, "REGLAS NO NEGOCIABLES")

    col_w_r = (CONTENT_W - 6*mm) / 2
    si_x = MARGIN_X
    no_x = MARGIN_X + col_w_r + 6*mm

    ry = rules_y - 12*mm
    c.setFillColor(INK)
    c.setFont("SansBold", 9)
    c.drawString(si_x, ry, "SÍ HACEMOS")
    c.setFillColor(WHISPER)
    c.drawString(no_x, ry, "NO HACEMOS")
    hairline(c, si_x, ry - 2*mm, si_x + 40*mm, INK, 0.4)
    hairline(c, no_x, ry - 2*mm, no_x + 40*mm, RULE, 0.4)

    si_items = [
        "Tuteo (tú, te, contigo)",
        "\"Maestro\", \"compa\", \"qué tal\"",
        "Frases cortas (10-15 palabras)",
        "Verbos en presente activo",
        "Cifras concretas, marcas reales",
    ]
    no_items = [
        "\"Estimado cliente\", \"atentamente\"",
        "Adjetivos vacíos (increíble, asombroso)",
        "Jerga corporativa (ecosistema, UX)",
        "Anglicismos innecesarios",
        "Tratar al electricista como amateur",
    ]
    item_y = ry - 9*mm
    for i in range(5):
        c.setFillColor(INK)
        c.setFont("Body", 9.5)
        c.drawString(si_x, item_y, "·  " + si_items[i])
        c.setFillColor(CHARCOAL)
        c.setFont("BodyItalic", 9.5)
        c.drawString(no_x, item_y, "—  " + no_items[i])
        item_y -= 12

    folio(c, page_num, "10  ·  Tono de voz (1/2)")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 14 — TONO DE VOZ (ejemplos por canal)
# ──────────────────────────────────────────────────────────────────────────
EJEMPLOS = [
    ("WEB  ·  HERO",
     "Material eléctrico, en un click. Directo a tu obra."),
    ("ANUNCIOS PAGADOS  ·  HEADLINE",
     "Mientras vas a la ferretería, no facturas.  /  Pídelo. Llega. Sigues trabajando."),
    ("WHATSAPP  ·  SERVICIO",
     "Qué onda Memo. Tu pedido de cable Condumex calibre 12 + 3 placas Bticino ya salió de almacén. "
     "Llega entre martes y jueves. Te aviso con el tracking en cuanto lo tengamos."),
    ("EMPAQUE  ·  SOLAPA INTERIOR",
     "Maestro: tu material llegó completo y revisado. Si algo no jala, mándanos un WhatsApp y lo "
     "arreglamos. Sigue facturando."),
    ("INSTAGRAM  ·  TIKTOK",
     "3 errores que veo cada semana cuando reviso instalaciones residenciales: calibre incorrecto en "
     "circuito de 20A. Ahorrarse $80 en el cable y arriesgar la casa entera no vale la pena. Cable 12 "
     "mínimo, sin excepciones."),
    ("EMAIL  ·  POST-COMPRA",
     "Memo, esperamos que el material te sirva para sacar la obra. Si eres electricista pro, queremos "
     "invitarte a la lista del Electriclick Club — descuentos por nivel, capacitaciones con marcas y "
     "cashback. Aún no abrimos, pero los primeros en la lista entran sin filtros. ¿Te apunto?"),
]

def page_tono_ejemplos(c, page_num):
    fill_paper(c)
    running_header(c, "Tono — ejemplos por canal")

    # Light header
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 50*mm, "TONO DE VOZ  ·  EJEMPLOS POR CANAL")
    c.setFillColor(INK)
    c.setFont("Display", 30)
    c.drawString(MARGIN_X, PAGE_H - 62*mm, "Cómo hablamos, en práctica")
    hairline(c, MARGIN_X, PAGE_H - 68*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 73*mm, "SEIS PIEZAS DE COPY APROBADAS  ·  CADA UNA EJECUTA LAS REGLAS DE LA PÁGINA ANTERIOR")

    y = PAGE_H - 90*mm
    for label, copy in EJEMPLOS:
        c.setFillColor(WHISPER)
        c.setFont("Mono", 7)
        c.drawString(MARGIN_X, y, label)
        c.setFillColor(COPPER)
        c.setLineWidth(0.6)
        c.setStrokeColor(COPPER)
        c.line(MARGIN_X, y - 2*mm, MARGIN_X + 18*mm, y - 2*mm)

        c.setFillColor(INK)
        c.setFont("BodyItalic", 12)
        copy_lines = wrap_text(c, copy, "BodyItalic", 12, CONTENT_W - 6*mm)
        cy = y - 9*mm
        for line in copy_lines:
            c.drawString(MARGIN_X + 3*mm, cy, line)
            cy -= 16
        y = cy - 8*mm

    folio(c, page_num, "10  ·  Tono de voz (2/2)")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 15 — ANEXO
# ──────────────────────────────────────────────────────────────────────────
def page_anexo(c, page_num):
    fill_paper(c)
    running_header(c, "Anexo")

    # Section opener — numeral lowered slightly so the digit "1" base doesn't get cut
    section_numeral(c, "11", MARGIN_X, PAGE_H - 70*mm, size=110, color=COPPER)
    c.setFillColor(INK)
    c.setFont("Display", 36)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 50*mm, "Anexo")
    hairline(c, MARGIN_X + 60*mm, PAGE_H - 56*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X + 60*mm, PAGE_H - 61*mm, "DECISIONES DE NEGOCIO  ·  PENDIENTES  ·  REFERENCIAS")

    # Producto / negocio
    y = PAGE_H - 88*mm
    c.setFillColor(WHISPER); c.setFont("Mono", 7)
    c.drawString(MARGIN_X, y, "DECISIONES DE PRODUCTO Y NEGOCIO")
    hairline(c, MARGIN_X, y - 2*mm, MARGIN_X + 70*mm, INK, 0.4)

    bullets = [
        ("Operación día 1.",
         "eCommerce simple (catálogo, carrito, checkout, envío). Nacional con almacén único en Guadalajara. SLA realista de paquetería: 2-4 días."),
        ("Fase 2  ·  6-12 meses post-lanzamiento.",
         "Electriclick Club — membresía por tiers según consumo mensual, descuentos por nivel, capacitaciones directas con marcas, cashback."),
        ("Fase 2  ·  funcionalidad clave: Lista del Maestro.",
         "El electricista arma una lista en su cuenta y le manda un link único a su cliente final. El cliente paga y recibe el material; el electricista gana puntos/cashback. Growth loop B2B2C."),
        ("Lenguaje desde día 1.",
         "La marca habla como club aunque la funcionalidad llegue en fase 2. Día 1 captura emails de \"pre-acceso al club\" para construir lista de espera."),
    ]
    by = y - 10*mm
    for head, body in bullets:
        c.setFillColor(INK); c.setFont("BodyBold", 10.5)
        c.drawString(MARGIN_X, by, head)
        by -= 13
        by = draw_paragraph(c, body, MARGIN_X, by, "Body", 10, 13.5, CONTENT_W, CHARCOAL)
        by -= 6*mm

    # Marcas referente
    hairline(c, MARGIN_X, by + 2*mm, PAGE_W - MARGIN_X, RULE, 0.4)
    by -= 6*mm
    c.setFillColor(WHISPER); c.setFont("Mono", 7)
    c.drawString(MARGIN_X, by, "MARCAS REFERENTE DEL CATÁLOGO  ·  ANCLA DE CREDIBILIDAD")
    by -= 8*mm
    # Two-row layout so nothing clips — these are the 8 brands the catalog hangs on
    c.setFillColor(INK); c.setFont("Display", 14)
    c.drawString(MARGIN_X, by,        "Schneider Electric  ·  Bticino  ·  Steren  ·  Volteck")
    c.drawString(MARGIN_X, by - 8*mm, "Cooper  ·  Condumex  ·  IUSA  ·  Truper")
    by -= 18*mm

    # Pendientes
    hairline(c, MARGIN_X, by + 4*mm, PAGE_W - MARGIN_X, RULE, 0.4)
    c.setFillColor(WHISPER); c.setFont("Mono", 7)
    c.drawString(MARGIN_X, by - 2*mm, "PENDIENTES DEL FUNDADOR  ·  FUERA DEL SCOPE DE MARCA")
    by -= 12*mm

    pendientes = [
        "Verificar disponibilidad de dominios: electriclick.com, electriclick.mx, electriclick.com.mx.",
        "Verificar handles en redes: @electriclick (Instagram, TikTok, Facebook).",
        "Búsqueda fonética en IMPI (clase 35 servicios de venta + clase 9 productos eléctricos).",
        "Reservar dominio y handles antes de invertir en branding pesado.",
    ]
    c.setFillColor(INK); c.setFont("Body", 10.5)
    for item in pendientes:
        c.setFillColor(COPPER); c.setFont("BodyBold", 11)
        c.drawString(MARGIN_X, by, "·")
        c.setFillColor(CHARCOAL); c.setFont("Body", 10.5)
        item_lines = wrap_text(c, item, "Body", 10.5, CONTENT_W - 6*mm)
        for i, line in enumerate(item_lines):
            c.drawString(MARGIN_X + 5*mm, by, line)
            by -= 13
        by -= 2*mm

    folio(c, page_num, "11  ·  Anexo")
    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# PAGE 16 — CIERRE
# ──────────────────────────────────────────────────────────────────────────
def page_cierre(c, page_num):
    fill_paper(c)

    # Top rail
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, PAGE_H - 24*mm, "CIERRE  ·  MANIFIESTO")
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 24*mm, "FIN DEL DOCUMENTO")
    hairline(c, MARGIN_X, PAGE_H - 27*mm, PAGE_W - MARGIN_X, INK, 0.6)

    # Manifesto
    c.setFillColor(INK)
    c.setFont("Display", 38)
    manifesto_lines = [
        "Esto no es una",
        "tienda. Es un",
        "club. Y el club",
        "crece contigo.",
    ]
    my = PAGE_H - 90*mm
    for line in manifesto_lines:
        c.drawString(MARGIN_X, my, line)
        my -= 46

    # Sub-statement
    c.setFillColor(CHARCOAL)
    c.setFont("BodyItalic", 14)
    closing_lines = wrap_text(c,
        "Para el electricista mexicano que dejó de ser ayudante hace años y quiere que su oficio se respete "
        "como lo que es: un trabajo técnico, exigente, indispensable. Para el contratista que coordina obras "
        "y entiende que el material a tiempo es la mitad del proyecto. Para el gremio que viene construyendo "
        "este país desde el cable hacia arriba.",
        "BodyItalic", 14, CONTENT_W - 6*mm)
    cy = my - 22*mm
    for line in closing_lines:
        c.drawString(MARGIN_X, cy, line)
        cy -= 20

    # Bottom block
    hairline(c, MARGIN_X, MARGIN_BOTTOM + 32*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 7)
    c.drawString(MARGIN_X, MARGIN_BOTTOM + 27*mm, "ELECTRICLICK  ·  PLAN ESTRATÉGICO DE MARCA")
    c.setFillColor(INK)
    c.setFont("Display", 26)
    c.drawString(MARGIN_X, MARGIN_BOTTOM + 16*mm, "Electriclick.")
    c.setFillColor(COPPER)
    c.setFont("BodyItalic", 12)
    c.drawString(MARGIN_X, MARGIN_BOTTOM + 8*mm, "Versión 1  ·  Edición de mayo de 2026  ·  Guadalajara, México")

    hairline(c, MARGIN_X, MARGIN_BOTTOM - 4*mm, PAGE_W - MARGIN_X, INK, 0.6)
    c.setFillColor(WHISPER)
    c.setFont("Mono", 6.5)
    c.drawString(MARGIN_X, MARGIN_BOTTOM - 9*mm, "DOCUMENTO PREPARADO POR CMO AGENCY · BRAND STRATEGY PRACTICE")
    c.drawRightString(PAGE_W - MARGIN_X, MARGIN_BOTTOM - 9*mm, f"PÁGINA {page_num:02d}")

    c.showPage()


# ──────────────────────────────────────────────────────────────────────────
# BUILD
# ──────────────────────────────────────────────────────────────────────────
def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = rl_canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Plan Estratégico de Marca — Electriclick")
    c.setAuthor("CMO Agency · Brand Strategy Practice")
    c.setSubject("Strategic Brand Plan — Version 1")
    c.setCreator("Concrete Authority — canvas-design")
    c.setKeywords(["Electriclick", "brand strategy", "plan estratégico", "Mexico", "electrical trade"])

    pages = [
        page_cover,           # 1
        page_toc,             # 2
        page_mission_vision,  # 3
        page_valores,         # 4
        page_propuesta,       # 5
        page_posicionamiento, # 6
        page_publico,         # 7
        page_no_cliente,      # 8
        page_persona_a,       # 9
        page_persona_b,       # 10
        page_personalidad,    # 11
        page_somos_no,        # 12
        page_tono_dimensions, # 13
        page_tono_ejemplos,   # 14
        page_anexo,           # 15
        page_cierre,          # 16
    ]
    for n, fn in enumerate(pages, start=1):
        fn(c, n)

    c.save()
    print(f"OK: {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
