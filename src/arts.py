import math, sys
sys.path.insert(0, ".")
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import simpleSplit
from game_data import *

OUTDIR = sys.argv[1]
W2, H2 = 594 * mm, 420 * mm  # A2 paisagem

def wrap(c, text, x, y, w, font="Helvetica", size=9, leading=None, center=False, color=NAVY):
    leading = leading or size * 1.25
    c.setFont(font, size); c.setFillColor(HexColor(color))
    for line in simpleSplit(text, font, size, w):
        if center: c.drawCentredString(x + w / 2, y, line)
        else: c.drawString(x, y, line)
        y -= leading
    return y

def emblem(c, x, y, r, ag):
    name, col, _, letter, _ = ag
    c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor(CREAM)); c.setLineWidth(r * 0.08)
    c.circle(x, y, r, fill=1, stroke=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", r * 1.1)
    c.drawCentredString(x, y - r * 0.38, letter)

def icon(c, t, x, y, s):
    """Ícones geométricos simples por tipo de casa."""
    c.setStrokeColor(HexColor(NAVY)); c.setFillColor(HexColor(NAVY)); c.setLineWidth(s * 0.08)
    if t == "embaixada":  # envelope
        c.rect(x - s, y - s * 0.6, 2 * s, 1.2 * s, fill=0)
        p = c.beginPath(); p.moveTo(x - s, y + s * 0.6); p.lineTo(x, y - s * 0.1); p.lineTo(x + s, y + s * 0.6)
        c.drawPath(p, fill=0)
    elif t == "laboratorio":  # lupa
        c.circle(x - s * 0.2, y + s * 0.2, s * 0.6, fill=0)
        c.line(x + s * 0.25, y - s * 0.25, x + s * 0.9, y - s * 0.9)
    elif t == "informante":  # balão de fala
        c.roundRect(x - s, y - s * 0.4, 2 * s, 1.1 * s, s * 0.3, fill=0)
        p = c.beginPath(); p.moveTo(x - s * 0.4, y - s * 0.4); p.lineTo(x - s * 0.7, y - s); p.lineTo(x, y - s * 0.4)
        c.drawPath(p, fill=0)
    elif t == "evento":  # estrela/exclamação
        c.setFont("Helvetica-Bold", s * 2.2); c.drawCentredString(x, y - s * 0.75, "!")
    elif t == "tunel":
        p = c.beginPath(); p.moveTo(x - s, y - s * 0.7); p.lineTo(x - s, y); p.arcTo(x - s, y - s, x + s, y + s, 180, -180)
        p.lineTo(x + s, y - s * 0.7); c.drawPath(p, fill=0)
    elif t == "esconderijo":  # casa
        p = c.beginPath(); p.moveTo(x - s, y - s * 0.7); p.lineTo(x - s, y + s * 0.1); p.lineTo(x, y + s * 0.9)
        p.lineTo(x + s, y + s * 0.1); p.lineTo(x + s, y - s * 0.7); p.close(); c.drawPath(p, fill=0)
    elif t == "rua":
        c.setDash(s * 0.3, s * 0.2); c.line(x - s, y, x + s, y); c.setDash()

# ------------------------------------------------------------------ TABULEIRO
def draw_board(c):
    c.setFillColor(HexColor(CREAM)); c.rect(0, 0, W2, H2, fill=1, stroke=0)
    m = 12 * mm
    cw = (W2 - 2 * m) / 11; ch = (H2 - 2 * m) / 11
    cells = board_cells()
    pos = []
    for i in range(11): pos.append((m + i * cw, H2 - m - ch))             # topo 0..10
    for i in range(1, 10): pos.append((m + 10 * cw, H2 - m - ch - i * ch))  # direita 11..19
    for i in range(11): pos.append((m + (10 - i) * cw, m))                # base 20..30
    for i in range(1, 10): pos.append((m, m + i * ch))                    # esquerda 31..39
    centers = {}
    for idx, ((t, name, side), (x, y)) in enumerate(zip(cells, pos)):
        centers[idx] = (x + cw / 2, y + ch / 2)
        if t == "qg":
            ag = AGENCIES[side]
            c.setFillColor(HexColor(ag[1])); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1.5)
            c.rect(x, y, cw, ch, fill=1, stroke=1)
            emblem(c, x + cw / 2, y + ch * 0.58, ch * 0.22, ag)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(x + cw / 2, y + ch * 0.14, f"QG {ag[0].upper()}")
            continue
        label, col = TYPE_STYLE[t]
        c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1.2)
        c.rect(x, y, cw, ch, fill=1, stroke=1)
        c.setFillColor(HexColor(NAVY)); c.rect(x, y + ch - 7 * mm, cw, 7 * mm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + cw / 2, y + ch - 5 * mm, label.upper())
        icon(c, t, x + cw / 2, y + ch * 0.45, 4.2 * mm)
        wrap(c, name, x + 2 * mm, y + 6 * mm, cw - 4 * mm, size=7, center=True)
        c.setFont("Helvetica", 6); c.setFillColor(HexColor(NAVY)); c.drawString(x + 1.5 * mm, y + 1.5 * mm, str(idx))
    # setas de sentido
    c.setFillColor(HexColor(RED)); c.setFont("Helvetica-Bold", 10)
    c.drawString(m + 1.2 * cw, H2 - m + 3 * mm, "SENTIDO DO MOVIMENTO  >>>")
    inner = (m + cw, m + ch, W2 - m - cw, H2 - m - ch)
    ix, iy, ix2, iy2 = inner
    # legenda dos locais
    leg = [("embaixada", "Embaixada: compre Missão e cifre"), ("laboratorio", "Laboratório: quebre envelopes"),
           ("informante", "Informante: pista sobre chave"), ("evento", "Evento: compre carta"),
           ("esconderijo", "Esconderijo: troque a chave"), ("tunel", "Túnel A leva ao A, B leva ao B")]
    lw = (ix2 - ix - 30 * mm) / 3
    for k, (t, txt) in enumerate(leg):
        lx = ix + 15 * mm + (k % 3) * lw; ly = iy + 100 * mm - (k // 3) * 14 * mm
        c.setFillColor(HexColor(TYPE_STYLE[t][1])); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1)
        c.rect(lx, ly, 14 * mm, 10 * mm, fill=1, stroke=1)
        icon(c, t, lx + 7 * mm, ly + 5 * mm, 3 * mm)
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 11); c.drawString(lx + 17 * mm, ly + 3.5 * mm, txt)
    # miolo
    c.setFillColor(HexColor(NAVY)); c.roundRect(ix + 8 * mm, iy2 - 52 * mm, ix2 - ix - 16 * mm, 44 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(W2 / 2, iy2 - 30 * mm, "OPERAÇÃO CÉSAR")
    c.setFillColor(HexColor(GOLD)); c.setFont("Courier-Bold", 14)
    c.drawCentredString(W2 / 2, iy2 - 43 * mm, "RSHUDFDR FHVDU  ·  k = 3  ·  CONFIDENCIAL")
    # pilhas de cartas
    decks = [("MISSÃO", "#F2C94C"), ("INFORMANTE", "#C39BD3"), ("EVENTO", "#F1948A"), ("FREQUÊNCIA", "#7FB3D5"), ("CHAVES", "#D5D8DC")]
    dw, dh = 63 * mm * 0.75, 88 * mm * 0.75
    gap = ((ix2 - ix) - 5 * dw) / 6
    for k, (n, col) in enumerate(decks):
        x = ix + gap + k * (dw + gap); y = iy2 - 60 * mm - dh
        c.setFillColor(HexColor(col)); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1); c.setDash(4, 3)
        c.roundRect(x, y, dw, dh, 3 * mm, fill=1, stroke=1); c.setDash()
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + dw / 2, y + dh / 2, n)
    # faixa do alfabeto (referência César)
    y0 = iy + 46 * mm
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    bw = (ix2 - ix - 30 * mm) / 26
    c.setFont("Helvetica-Bold", 9); c.setFillColor(HexColor(NAVY))
    c.drawString(ix + 15 * mm, y0 + 12 * mm, "Régua de posições (A=0 … Z=25)  ·  Cifrar: C = (P + k) mod 26   ·   Decifrar: P = (C - k) mod 26")
    for i, ch_ in enumerate(alph):
        x = ix + 15 * mm + i * bw
        c.setFillColor(white); c.setStrokeColor(HexColor(NAVY)); c.rect(x, y0, bw, 9 * mm, fill=1, stroke=1)
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 11); c.drawCentredString(x + bw / 2, y0 + 3.2 * mm, ch_)
        c.setFont("Helvetica", 7); c.drawCentredString(x + bw / 2, y0 - 4 * mm, str(i))
    # resumo do turno
    y = iy + 30 * mm
    c.setFillColor(HexColor(RED)); c.setFont("Helvetica-Bold", 12)
    c.drawString(ix + 15 * mm, y, "TURNO:")
    c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica", 11)
    c.drawString(ix + 35 * mm, y, "1. Role o dado e mova   2. Faça a ação da casa   3. Abordagem (se houver agente na mesma casa)")
    c.drawString(ix + 15 * mm, y - 7 * mm, "Vitória: 12 PI   ·   Túneis: pare na entrada e use sua ação para sair no outro lado   ·   Protocolo Substituição: a partir da rodada 6")
    # contador de rodadas
    c.setFont("Helvetica-Bold", 10); c.setFillColor(HexColor(NAVY))
    c.drawString(ix + 15 * mm, iy + 12 * mm, "RODADA:")
    for r in range(12):
        x = ix + 35 * mm + r * 12 * mm
        c.setFillColor(HexColor("#FFF7E0") if r < 5 else HexColor("#D6EAF8"))
        c.circle(x, iy + 13.5 * mm, 4.5 * mm, fill=1, stroke=1)
        c.setFillColor(HexColor(NAVY)); c.drawCentredString(x, iy + 12 * mm, str(r + 1))
    c.setFont("Helvetica", 8); c.drawString(ix + 35 * mm + 12 * 12 * mm, iy + 12 * mm, "(azul = Substituição liberada)")

def board_files():
    # A2 inteiro
    c = canvas.Canvas(f"{OUTDIR}/tabuleiro_A2.pdf", pagesize=(W2, H2)); c.setTitle("Tabuleiro A2 - Operação César")
    draw_board(c); c.showPage(); c.save()
    # 4 folhas A4 paisagem (A2 = 4 x A3... -> escala 50% numa grade 2x2 de A4 paisagem = A2*0.5)
    from reportlab.graphics import renderPDF
    from pypdf import PdfReader, PdfWriter, Transformation, PageObject
    src = PdfReader(f"{OUTDIR}/tabuleiro_A2.pdf").pages[0]
    Aw, Ah = landscape(A4)
    scale = (2 * Aw) / W2  # board ocupa 2x2 folhas A4 paisagem
    wr = PdfWriter()
    names = ["superior esquerda", "superior direita", "inferior esquerda", "inferior direita"]
    for k, (cx, cy) in enumerate([(0, 1), (1, 1), (0, 0), (1, 0)]):
        pg = PageObject.create_blank_page(width=Aw, height=Ah)
        pg.merge_transformed_page(src, Transformation().scale(scale).translate(-cx * Aw, -cy * Ah))
        wr.add_page(pg)
    # rótulos de montagem
    tmp = f"{OUTDIR}/_labels.pdf"
    cl = canvas.Canvas(tmp, pagesize=(Aw, Ah))
    for n in names:
        cl.setFont("Helvetica", 7); cl.setFillColor(HexColor("#888888"))
        cl.drawString(4 * mm, 3 * mm, f"Operação César · tabuleiro · folha {n} · imprimir em A4 paisagem, 100% (sem ajustar à página), recortar e colar 2x2")
        cl.showPage()
    cl.save()
    lab = PdfReader(tmp)
    for p, l in zip(wr.pages, lab.pages): p.merge_page(l)
    with open(f"{OUTDIR}/tabuleiro_4xA4.pdf", "wb") as f: wr.write(f)
    import os; os.remove(tmp)

# ------------------------------------------------------------------ CARTAS
CW, CH = 63 * mm, 88 * mm
def card_grid():
    Pw, Ph = A4
    mx = (Pw - 3 * CW) / 2; my = (Ph - 3 * CH) / 2
    return [(mx + (i % 3) * CW, Ph - my - (i // 3 + 1) * CH) for i in range(9)]

def card_frame(c, x, y, col, kind):
    c.setFillColor(HexColor(CREAM)); c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.4)
    c.rect(x, y, CW, CH, fill=1, stroke=1)
    c.setFillColor(HexColor(col)); c.roundRect(x + 3 * mm, y + 3 * mm, CW - 6 * mm, CH - 6 * mm, 3 * mm, fill=0, stroke=0)
    c.setFillColor(HexColor(col)); c.rect(x + 3 * mm, y + CH - 15 * mm, CW - 6 * mm, 12 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + CW / 2, y + CH - 10.5 * mm, kind)
    c.setStrokeColor(HexColor(col)); c.setLineWidth(1.5); c.rect(x + 3 * mm, y + 3 * mm, CW - 6 * mm, CH - 6 * mm, fill=0, stroke=1)

def card_back(c, x, y, col, kind):
    c.setFillColor(HexColor(NAVY)); c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.4)
    c.rect(x, y, CW, CH, fill=1, stroke=1)
    c.setStrokeColor(HexColor(col)); c.setLineWidth(2); c.rect(x + 4 * mm, y + 4 * mm, CW - 8 * mm, CH - 8 * mm, fill=0, stroke=1)
    c.setFillColor(HexColor(col)); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(x + CW / 2, y + CH / 2 + 6 * mm, "OPERAÇÃO")
    c.drawCentredString(x + CW / 2, y + CH / 2 - 1 * mm, "CÉSAR")
    c.setFont("Courier-Bold", 10); c.drawCentredString(x + CW / 2, y + CH / 2 - 14 * mm, kind)

def deck(c, items, col, kind, draw_fn):
    grid = card_grid()
    for start in range(0, len(items), 9):
        chunk = items[start:start + 9]
        for (x, y), it in zip(grid, chunk):
            card_frame(c, x, y, col, kind); draw_fn(c, x, y, it)
        c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888"))
        c.drawString(10 * mm, 5 * mm, f"Operação César · cartas de {kind.lower()} · frente")
        c.showPage()
        # verso espelhado (para impressão frente e verso, virar pela borda longa)
        Pw = A4[0]
        for (x, y), it in zip(grid, chunk):
            card_back(c, Pw - x - CW, y, col, kind)
        c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888"))
        c.drawString(10 * mm, 5 * mm, f"Operação César · cartas de {kind.lower()} · verso")
        c.showPage()

def cards_file():
    c = canvas.Canvas(f"{OUTDIR}/cartas.pdf", pagesize=A4); c.setTitle("Cartas - Operação César")
    def mission(c, x, y, w):
        c.setFillColor(HexColor(NAVY)); c.setFont("Courier-Bold", 22 if len(w) < 7 else 19)
        c.drawCentredString(x + CW / 2, y + CH / 2 + 2 * mm, w)
        wrap(c, "Cifre esta palavra com a sua chave atual e escreva o texto cifrado num envelope. "
                "Guarde esta carta virada para baixo e anote nela o nº do envelope e a chave usada.",
             x + 6 * mm, y + 26 * mm, CW - 12 * mm, size=6.5, center=True)
        c.setFont("Helvetica", 7); c.drawCentredString(x + CW / 2, y + 7 * mm, f"{len(w)} letras  ·  Envelope nº ____  ·  k = ____")
    deck(c, MISSIONS, "#F2C94C", "MISSÃO", mission)
    def key(c, x, y, k):
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(x + CW / 2, y + CH / 2 - 4 * mm, str(k))
        c.setFont("Courier-Bold", 9)
        c.drawCentredString(x + CW / 2, y + 22 * mm, f"A > {chr(65 + k)}    B > {chr(65 + (k + 1) % 26)}")
        wrap(c, "Mantenha em segredo. Troque no Esconderijo.", x + 6 * mm, y + 13 * mm, CW - 12 * mm, size=6.5, center=True)
    deck(c, list(range(1, 26)), "#D5D8DC", "CHAVE", key)
    def info(c, x, y, it):
        t, d = it
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + CW / 2, y + CH - 26 * mm, t)
        wrap(c, d, x + 6 * mm, y + CH - 36 * mm, CW - 12 * mm, size=9, center=True)
        wrap(c, "Use no seu turno e descarte. O rival deve responder a verdade.", x + 6 * mm, y + 10 * mm, CW - 12 * mm, size=6.5, center=True)
    deck(c, INFORMANT_CARDS, "#C39BD3", "INFORMANTE", info)
    def ev(c, x, y, it):
        t, d = it
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + CW / 2, y + CH - 26 * mm, t)
        wrap(c, d, x + 6 * mm, y + CH - 36 * mm, CW - 12 * mm, size=9, center=True)
        wrap(c, "Resolva imediatamente e descarte.", x + 6 * mm, y + 10 * mm, CW - 12 * mm, size=6.5, center=True)
    deck(c, EVENT_CARDS, "#F1948A", "EVENTO", ev)
    def freq(c, x, y, it):
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + CW / 2, y + CH - 26 * mm, "Análise de Frequência")
        wrap(c, FREQ_TEXT, x + 6 * mm, y + CH - 35 * mm, CW - 12 * mm, size=8, center=True)
        c.setFont("Courier-Bold", 7.5)
        s = "  ".join(f"{l}{v:.0f}%" for l, v in PT_FREQ[:6])
        c.drawCentredString(x + CW / 2, y + 14 * mm, s)
        c.setFont("Helvetica", 6.5); c.drawCentredString(x + CW / 2, y + 9 * mm, "Letras mais comuns do português")
    deck(c, list(range(12)), "#7FB3D5", "FREQUÊNCIA", freq)
    def subst(c, x, y, alpha):
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + CW / 2, y + CH - 22 * mm, "Alfabeto secreto")
        plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for row in range(2):
            for i in range(13):
                j = row * 13 + i
                xx = x + 6.5 * mm + i * 3.9 * mm; yy = y + CH - 34 * mm - row * 16 * mm
                c.setFont("Courier-Bold", 8); c.setFillColor(HexColor(NAVY)); c.drawCentredString(xx, yy, plain[j])
                c.setFillColor(HexColor(RED)); c.drawCentredString(xx, yy - 5 * mm, alpha[j])
        wrap(c, "Linha de cima: texto claro. Linha vermelha: texto cifrado. Mantenha em segredo.",
             x + 6 * mm, y + 18 * mm, CW - 12 * mm, size=6.5, center=True)
    deck(c, substitution_alphabets(), "#82C99A", "SUBSTITUIÇÃO", subst)
    c.save()

# ------------------------------------------------------------------ RODA DE CIFRA
def wheels_file():
    c = canvas.Canvas(f"{OUTDIR}/roda_de_cifra.pdf", pagesize=A4); c.setTitle("Roda de Cifra - Operação César")
    Pw, Ph = A4
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def disc(cx, cy, R, r_text, fill, title, numbers, inner_text_r=None, tcol=NAVY):
        c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1.2)
        c.circle(cx, cy, R, fill=1, stroke=1)
        for i, ch_ in enumerate(alph):
            ang = 90 - i * 360 / 26
            a = math.radians(ang); a2 = math.radians(ang + 180 / 26)
            c.setLineWidth(0.5)
            c.setStrokeColor(HexColor(tcol)); c.line(cx + (R - 16 * mm) * math.cos(a2), cy + (R - 16 * mm) * math.sin(a2), cx + R * math.cos(a2), cy + R * math.sin(a2))
            c.saveState(); c.translate(cx + r_text * math.cos(a), cy + r_text * math.sin(a)); c.rotate(ang - 90)
            c.setFillColor(HexColor(tcol)); c.setFont("Helvetica-Bold", 13); c.drawCentredString(0, -4, ch_)
            if numbers:
                c.setFont("Helvetica", 6); c.drawCentredString(0, -12, str(i))
            c.restoreState()
        c.setFillColor(HexColor(NAVY)); c.circle(cx, cy, 1.5 * mm, fill=1, stroke=0)
        if inner_text_r:
            c.setFont("Helvetica-Bold", 9); c.drawCentredString(cx, cy + inner_text_r, title)
    for ag in AGENCIES:
        R1, R2 = 76 * mm, 56 * mm
        cx = Pw / 2
        cy1 = Ph - 10 * mm - R1
        disc(cx, cy1, R1, R1 - 8 * mm, "#FFFFFF", "", True)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(HexColor(NAVY))
        c.drawCentredString(cx, cy1 + 30 * mm, "DISCO EXTERNO — TEXTO CLARO")
        emblem(c, cx, cy1 + 10 * mm, 9 * mm, ag)
        c.setFont("Helvetica", 7); c.drawCentredString(cx, cy1 - 12 * mm, f"Roda da agência {ag[0]}")
        cy2 = 9 * mm + R2
        disc(cx, cy2, R2, R2 - 8 * mm, ag[1], "", False, tcol="#FFFFFF")
        c.setFillColor(white); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(cx, cy2 + 22 * mm, "DISCO INTERNO — TEXTO CIFRADO")
        c.drawCentredString(cx, cy2 - 24 * mm, "Gire k casas no sentido anti-horário:")
        c.drawCentredString(cx, cy2 - 28 * mm, "o A externo aponta para a letra cifrada do A.")
        c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888"))
        c.drawString(8 * mm, 5 * mm, "Recorte os dois discos, coloque o menor sobre o maior e prenda no centro com um colchete (bailarina).")
        c.showPage()
    c.save()

# ------------------------------------------------------------------ FICHAS, ENVELOPES, FOLHAS, PEÕES
def sheets_file():
    c = canvas.Canvas(f"{OUTDIR}/fichas_e_folhas.pdf", pagesize=A4); c.setTitle("Fichas e folhas - Operação César")
    Pw, Ph = A4
    # Fichas de agente: 2 por página
    for p in range(2):
        for k in range(2):
            ag = AGENCIES[p * 2 + k]
            y0 = Ph / 2 if k == 0 else 0
            x0 = 10 * mm; w = Pw - 20 * mm; h = Ph / 2 - 12 * mm; y = y0 + 6 * mm
            c.setFillColor(HexColor(CREAM)); c.setStrokeColor(HexColor(ag[1])); c.setLineWidth(3)
            c.roundRect(x0, y, w, h, 5 * mm, fill=1, stroke=1)
            c.setFillColor(HexColor(ag[1])); c.rect(x0, y + h - 22 * mm, w, 22 * mm, fill=1, stroke=0)
            emblem(c, x0 + 14 * mm, y + h - 11 * mm, 8 * mm, ag)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 18)
            c.drawString(x0 + 27 * mm, y + h - 10 * mm, f"AGÊNCIA {ag[0].upper()}")
            c.setFont("Helvetica", 11); c.drawString(x0 + 27 * mm, y + h - 17 * mm, ag[2] + "  ·  FICHA DE AGENTE")
            yy = wrap(c, "Habilidade (modo avançado): " + ag[4], x0 + 6 * mm, y + h - 30 * mm, w - 12 * mm, size=9.5)
            # trilha de PI
            c.setFont("Helvetica-Bold", 10); c.setFillColor(HexColor(NAVY))
            c.drawString(x0 + 6 * mm, y + h - 44 * mm, "PONTOS DE INTELIGÊNCIA (PI)")
            for i in range(13):
                bx = x0 + 6 * mm + i * 13.5 * mm; by = y + h - 60 * mm
                c.setFillColor(HexColor(GOLD) if i == 12 else white); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1)
                c.rect(bx, by, 12 * mm, 12 * mm, fill=1, stroke=1)
                c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 12); c.drawCentredString(bx + 6 * mm, by + 4 * mm, str(i))
            # área de missões
            c.setFont("Helvetica-Bold", 10); c.drawString(x0 + 6 * mm, y + h - 70 * mm, "MISSÕES EM ANDAMENTO (cartas viradas para baixo aqui)")
            for i in range(3):
                bx = x0 + 6 * mm + i * 30 * mm
                c.setDash(3, 2); c.rect(bx, y + 8 * mm, 26 * mm, 36 * mm, fill=0, stroke=1); c.setDash()
                c.setFont("Helvetica", 8); c.drawCentredString(bx + 13 * mm, y + 26 * mm, f"Envelope {i + 1}")
            # resumo do turno
            tx = x0 + 100 * mm
            c.setFont("Helvetica-Bold", 10); c.drawString(tx, y + 44 * mm, "RESUMO DO TURNO")
            lines = ["1. Role 1 dado e mova no sentido horário.",
                     "2. Ação da casa: Embaixada (missão), QG (entregar),",
                     "   Laboratório (quebrar), Informante, Evento,",
                     "   Esconderijo (trocar chave / Substituição), Túnel.",
                     "3. Abordagem: dado vs dado, empate = defensor.",
                     "QG: decifre seu envelope certo = 3 PI (errado = 1 PI).",
                     "Lab: quebrou envelope rival = +2 PI e ele perde 1 PI."]
            c.setFont("Helvetica", 8.5)
            for i, l in enumerate(lines): c.drawString(tx, y + 38 * mm - i * 4.4 * mm, l)
        c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888")); c.drawString(10 * mm, 2 * mm, "Operação César · fichas de agente · recorte na linha do meio")
        c.showPage()
    # Envelopes: 8 por página, 2 páginas
    for p in range(2):
        ew, eh = (Pw - 20 * mm) / 2, (Ph - 20 * mm) / 4
        for i in range(8):
            x = 10 * mm + (i % 2) * ew; y = Ph - 10 * mm - (i // 2 + 1) * eh
            c.setFillColor(HexColor("#FBF6EA")); c.setStrokeColor(HexColor("#999999")); c.setLineWidth(0.5); c.setDash(3, 2)
            c.rect(x, y, ew, eh, fill=1, stroke=1); c.setDash()
            c.setFillColor(HexColor(RED)); c.setFont("Helvetica-Bold", 11)
            c.drawString(x + 5 * mm, y + eh - 9 * mm, "ENVELOPE CONFIDENCIAL")
            c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica", 9)
            c.drawString(x + 5 * mm, y + eh - 17 * mm, "Agência: ______________   Nº: ____")
            c.drawString(x + 5 * mm, y + eh - 25 * mm, "Cifra:  [  ] César    [  ] Substituição")
            c.drawString(x + 5 * mm, y + eh - 33 * mm, "Texto cifrado:")
            for j in range(7):
                c.rect(x + 5 * mm + j * 11 * mm, y + 6 * mm, 10 * mm, 12 * mm, fill=0, stroke=1)
        c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888")); c.drawString(10 * mm, 4 * mm, "Operação César · envelopes · imprima várias cópias ou use papel de rascunho")
        c.showPage()
    # Folha de criptoanálise: 2 por página
    for k in range(2):
        y0 = Ph / 2 if k == 0 else 0
        x0 = 10 * mm; y = y0 + 8 * mm; w = Pw - 20 * mm; h = Ph / 2 - 14 * mm
        c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1); c.rect(x0, y, w, h, fill=0, stroke=1)
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica-Bold", 14)
        c.drawString(x0 + 5 * mm, y + h - 10 * mm, "FOLHA DE CRIPTOANÁLISE — força bruta")
        c.setFont("Helvetica", 9)
        c.drawString(x0 + 5 * mm, y + h - 17 * mm, "Envelope de: __________  Nº: ___   Texto cifrado: ____________________")
        c.drawString(x0 + 5 * mm, y + h - 23 * mm, "Pistas do Informante: ___________________________________________________")
        cols = 5; cwid = (w - 10 * mm) / cols; rh = 8.5 * mm
        for i in range(25):
            cx = x0 + 5 * mm + (i // 5) * cwid; cy = y + h - 35 * mm - (i % 5) * rh
            c.rect(cx, cy, 4 * mm, 4 * mm, fill=0, stroke=1)
            c.setFont("Helvetica-Bold", 9); c.drawString(cx + 6 * mm, cy + 0.5 * mm, f"k={i + 1:>2}")
            c.setFont("Helvetica", 9); c.drawString(cx + 17 * mm, cy + 0.5 * mm, "__________")
        c.setFont("Helvetica", 8)
        c.drawString(x0 + 5 * mm, y + 6 * mm, "Marque a caixa de cada chave testada e escreva o resultado. Uma palavra que faz sentido indica a chave certa.")
    c.setFont("Helvetica", 7); c.setFillColor(HexColor("#888888")); c.drawString(10 * mm, 2 * mm, "Operação César · folhas de criptoanálise")
    c.showPage()
    # Peões dobráveis
    for i, ag in enumerate(AGENCIES):
        x = 20 * mm + (i % 2) * 90 * mm; y = Ph - 30 * mm - (i // 2 + 1) * 90 * mm
        pw, ph = 40 * mm, 35 * mm
        for half in (0, 1):
            yy = y + half * ph
            c.setFillColor(HexColor(ag[1])); c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(1)
            c.rect(x, yy, pw, ph, fill=1, stroke=1)
            c.saveState()
            if half == 1:
                c.translate(x + pw, yy + ph); c.rotate(180); ox, oy = 0, 0
            else:
                c.translate(x, yy); ox, oy = 0, 0
            emblem(c, pw / 2, ph * 0.58, 9 * mm, ag)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 9); c.drawCentredString(pw / 2, 4 * mm, ag[2].upper())
            c.restoreState()
        c.setFillColor(HexColor("#DDDDDD")); c.rect(x, y - 12 * mm, pw, 12 * mm, fill=1, stroke=1)
        c.setFillColor(HexColor("#DDDDDD")); c.rect(x, y + 2 * ph, pw, 12 * mm, fill=1, stroke=1)
        c.setFillColor(HexColor(NAVY)); c.setFont("Helvetica", 7)
        c.drawCentredString(x + pw / 2, y - 7 * mm, "base (dobrar)"); c.drawCentredString(x + pw / 2, y + 2 * ph + 5 * mm, "base (dobrar)")
    c.setFont("Helvetica-Bold", 14); c.setFillColor(HexColor(NAVY)); c.drawString(20 * mm, Ph - 20 * mm, "PEÕES DE AGENTE — recorte, dobre no meio e nas bases, cole as bases")
    c.showPage()
    c.save()

board_files(); cards_file(); wheels_file(); sheets_file()
print("ok")
