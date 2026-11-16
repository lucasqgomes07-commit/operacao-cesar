import sys
sys.path.insert(0, ".")
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from game_data import caesar, PT_FREQ

OUTDIR = sys.argv[1]
INK = colors.HexColor("#1B2333"); ACC = colors.HexColor("#B3261E"); SOFT = colors.HexColor("#EEF1F6")
ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6)
lft = ParagraphStyle("lft", parent=body, alignment=0)
bul = ParagraphStyle("bul", parent=body, alignment=0, leftIndent=14, bulletIndent=2, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=ACC, spaceBefore=12, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=INK, spaceBefore=8, spaceAfter=4)
title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=32, leading=38, alignment=TA_CENTER, textColor=INK)
sub = ParagraphStyle("s", fontName="Helvetica", fontSize=13, leading=18, alignment=TA_CENTER, textColor=ACC)
center = ParagraphStyle("c", parent=body, alignment=TA_CENTER)
cell = ParagraphStyle("cell", parent=body, fontSize=9.5, leading=13, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
box = ParagraphStyle("box", parent=body, backColor=SOFT, borderPadding=8, borderColor=colors.HexColor("#C9CFDA"), borderWidth=0.6, spaceBefore=6, spaceAfter=10)

def P(t, s=body): return Paragraph(t, s)
def B(items): return [Paragraph(i, bul, bulletText="•") for i in items]
def N(items): return [Paragraph(i, bul, bulletText=f"{k}.") for k, i in enumerate(items, 1)]
def table(rows, widths, header=True):
    data = [[Paragraph(str(c), cellb if (header and r == 0) or (c_i == 0 and not header) else cell) for c_i, c in enumerate(row)] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CFDA")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    st += [("BACKGROUND", (0, 0), (-1, 0), SOFT)] if header else [("BACKGROUND", (0, 0), (0, -1), SOFT)]
    t.setStyle(TableStyle(st)); return t
def footer_for(name):
    def f(c, d):
        c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
        c.drawString(2 * cm, 1.2 * cm, f"Operação César — {name}"); c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {d.page}")
        c.restoreState()
    return f
def build(path, story, name, ttl):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            title=ttl, author="Lucas Gomes, Pedro Passos, Natan Brasil")
    doc.build(story, onFirstPage=footer_for(name), onLaterPages=footer_for(name))

TEAM = "Lucas Gomes · Pedro Passos · Natan Brasil"

# =============================================================== REGRAS
s = [Spacer(1, 3 * cm), P("OPERAÇÃO CÉSAR", title), Spacer(1, 6), P("Manual de Regras", sub), Spacer(1, 0.8 * cm),
     P("2 a 4 jogadores · 30 a 40 minutos · a partir de 15 anos", center),
     P("Um jogo de tabuleiro sobre Criptografia: Cifra de César e Cifra de Substituição", center),
     Spacer(1, 1.5 * cm), P(f"Equipe: {TEAM}", center),
     P("CESUPA · Ciência da Computação · Resolução Discreta de Problemas · Prof. Pedro Girotto", center),
     PageBreak()]

s += [P("1. A história", h1),
      P("Belém, anos 60. Quatro agências de espionagem — <b>Corvo, Raposa, Coruja e Jaguar</b> — disputam os segredos "
        "que circulam pela cidade. Cada jogador é o melhor agente da sua agência. Sua missão: buscar informações nas "
        "Embaixadas, <b>cifrá-las</b>, levá-las até o seu QG sem que sejam roubadas e, ao mesmo tempo, interceptar e "
        "<b>quebrar</b> as mensagens dos rivais."),
      P("2. Objetivo", h1),
      P("Ser o primeiro agente a juntar <b>12 Pontos de Inteligência (PI)</b>. Se ninguém chegar a 12 até o fim da "
        "rodada 12, vence quem tiver mais PI (desempate: quem quebrou mais envelopes no Laboratório)."),
      P("3. A Cifra de César em 1 minuto", h1),
      P("Na Cifra de César, cada letra da mensagem é trocada pela letra que está <b>k posições à frente</b> no alfabeto. "
        "O número k é a <b>chave</b>. Depois do Z, volta para o A. Para decifrar, ande k posições para trás."),
      table([["Texto claro", "A", "G", "E", "N", "T", "E"], ["Chave k = 3", "+3", "+3", "+3", "+3", "+3", "+3"],
             ["Texto cifrado", "D", "J", "H", "Q", "W", "H"]], [3.4 * cm] + [1.6 * cm] * 6),
      Spacer(1, 4),
      P("Em matemática: cifrar é <b>C = (P + k) mod 26</b> e decifrar é <b>P = (C - k) mod 26</b>, contando A = 0, B = 1, …, Z = 25."),
      P("<b>Usando a Roda de Cifra:</b> gire o disco interno até que, embaixo do A do disco externo, apareça a letra "
        "que fica k casas depois do A (para k = 3, a letra D). Agora, para cifrar, procure a letra no disco externo e leia a letra "
        "de baixo; para decifrar, faça o caminho inverso.", box),
      P("<b>Por que isso importa no jogo?</b> Só existem 25 chaves úteis. Por isso um espião rival pode simplesmente testar todas "
        "(<b>ataque de força bruta</b>). Proteger a sua chave, trocá-la de vez em quando e, mais tarde, usar uma cifra mais forte é "
        "o que separa um bom agente de um agente descoberto.")]

s += [P("4. Componentes", h1),
      table([["Componente", "Qtd.", "Arquivo para imprimir"],
             ["Tabuleiro da cidade (40 casas)", "1", "tabuleiro_4xA4.pdf (4 folhas A4 paisagem) ou tabuleiro_A2.pdf"],
             ["Roda de Cifra (2 discos + colchete)", "4", "roda_de_cifra.pdf (1 página por agência)"],
             ["Cartas de Missão", "40", "cartas.pdf"], ["Cartas de Chave (1 a 25)", "25", "cartas.pdf"],
             ["Cartas Informante", "16", "cartas.pdf"], ["Cartas de Evento", "16", "cartas.pdf"],
             ["Cartas de Frequência", "12", "cartas.pdf"], ["Cartas de Substituição (alfabeto secreto)", "4", "cartas.pdf"],
             ["Fichas de Agente (com trilha de PI)", "4", "fichas_e_folhas.pdf"],
             ["Envelopes confidenciais", "16+", "fichas_e_folhas.pdf (ou papel de rascunho)"],
             ["Folhas de Criptoanálise", "2+", "fichas_e_folhas.pdf"], ["Peões de agente", "4", "fichas_e_folhas.pdf"],
             ["Dados de 6 faces", "2", "—"], ["Marcadores (moedas/clipes) para PI e rodada", "5", "—"], ["Lápis", "4", "—"]],
            [6.2 * cm, 1.4 * cm, 8.4 * cm]),
      P("Dica de impressão: imprima as cartas em frente e verso (virar pela borda longa) ou só a frente e cole num papel mais firme. "
        "Imprima sempre em 100% (sem “ajustar à página”).", box)]

s += [P("5. Preparação", h1),
      *N(["Monte o tabuleiro e coloque as pilhas embaralhadas de Missão, Informante, Evento e Frequência nos espaços do centro. "
          "Separe as Cartas de Substituição ao lado.",
          "Cada jogador escolhe uma agência e pega: peão, Roda de Cifra, Ficha de Agente, envelopes, uma Folha de Criptoanálise e um lápis.",
          "Embaralhe as Cartas de Chave. Cada jogador compra 1, olha em segredo e a guarda virada para baixo. Essa é a sua <b>chave atual</b>.",
          "Todos começam no seu QG com 0 PI. Coloque o marcador de rodada no 1.",
          "Começa quem mandou a última mensagem no celular; o jogo segue no sentido horário."]),
      P("6. O turno", h1),
      P("Na sua vez, faça os passos abaixo, nesta ordem:"),
      *N(["<b>Mover:</b> role 1 dado e ande essa quantidade de casas no sentido horário (o sentido indicado no tabuleiro). "
          "Passar por outros peões é permitido.",
          "<b>Ação da casa:</b> faça a ação do local onde parou (veja a seção 7). Ações são opcionais.",
          "<b>Abordagem (opcional):</b> se houver outro agente na mesma casa, você pode tentar interceptá-lo (seção 8)."]),
      P("Quando todos tiverem jogado, avance o marcador de rodada.")]

s += [P("7. Os locais da cidade", h1),
      table([["Local", "Ação"],
             ["Embaixada", "Compre 1 Carta de Missão (se tiver menos de 3 envelopes). Cifre a palavra com a sua chave atual e escreva o "
              "texto cifrado num envelope, marcando a sua agência e o nº do envelope (1, 2 ou 3). Coloque a Carta de Missão virada "
              "para baixo no espaço de mesmo número da sua Ficha e anote nela o nº do envelope e a chave usada."],
             ["QG da sua agência", "Entregue quantos envelopes quiser. Para cada um, decifre em voz alta: se acertar a palavra da Carta de "
              "Missão, ganhe <b>3 PI</b> (<b>4 PI</b> se foi cifrado por Substituição). Se errar, a mensagem chegou corrompida: <b>1 PI</b>. "
              "Descarte a Missão. O QG é seguro: ninguém pode fazer abordagem dentro dele."],
             ["QG de outra agência", "Funciona como uma rua comum."],
             ["Laboratório", "Tente quebrar <b>um</b> envelope que você interceptou (seção 9)."],
             ["Informante", "Compre 1 Carta Informante. Você pode usá-la agora ou guardar para outro turno (máximo de 3 na mão)."],
             ["Evento", "Compre 1 Carta de Evento e resolva imediatamente."],
             ["Esconderijo", "Troque a sua chave: devolva a sua Carta de Chave ao fundo da pilha e compre outra. "
              "<i>Ou</i>, se o Protocolo Substituição estiver liberado, adote-o (seção 10)."],
             ["Túnel", "Se parar exatamente aqui, pode usar a sua ação para sair no outro túnel com a mesma letra (A leva ao A, B leva ao B)."],
             ["Rua", "Sem ação. Só abordagem, se houver alguém."]],
            [3.6 * cm, 12.4 * cm])]

s += [P("8. Abordagem (interceptação)", h1),
      P("Se você termina o movimento na mesma casa de um agente que carrega envelopes, pode abordá-lo (uma vez por turno). "
        "Os dois rolam 1 dado. Se o seu resultado for <b>maior</b>, você pega 1 envelope dele à sua escolha (sem olhar a Carta de Missão). "
        "Empate ou resultado menor: a abordagem falha. A Carta de Missão continua com o dono, virada para baixo — é ela que confirma "
        "se você quebrou a cifra."),
      P("9. Laboratório: quebrando cifras", h1),
      P("<b>Contra a Cifra de César (força bruta):</b> role 1 dado. Você pode testar esse número de chaves diferentes no envelope, "
        "usando a sua Roda e marcando cada chave testada na Folha de Criptoanálise. As chaves marcadas continuam valendo nos próximos "
        "turnos, então você nunca precisa repetir uma. Quando uma chave produzir uma palavra que faz sentido, anuncie-a."),
      *B(["Se a palavra for igual à da Carta de Missão do dono: você ganha <b>2 PI</b>, o dono perde <b>1 PI</b> (mínimo 0) e descarta a Missão.",
          "Se estiver errada: nada acontece; continue tentando em outro turno no Laboratório."]),
      P("<b>Exemplo.</b> A Raposa interceptou o envelope <b>ZLUOH</b> do Corvo. Uma Carta Informante revelou que a chave do Corvo é "
        "“menor que 8”. No Laboratório ela rola 4 e testa k = 1 (YKTNG), 2 (XJSMF), 3 (WIRLE) e 4 (VHQKD): nada faz sentido. "
        "No próximo Laboratório rola 3 e testa k = 5 (UGPJC), 6 (TFOIB) e 7: <b>SENHA</b>! Ela anuncia, o Corvo confirma pela Carta "
        "de Missão, e a Raposa ganha 2 PI.", box),
      P("<b>Cuidado com as pistas:</b> as Cartas Informante falam da chave <b>atual</b> do rival. Se ele trocou de chave no Esconderijo, "
        "os envelopes antigos ainda usam a chave antiga — é assim que a troca de chave protege as mensagens.")]

freq = "  ·  ".join(f"{l} {v:.1f}%" for l, v in PT_FREQ)
s += [P("10. Protocolo Substituição (Nível 2)", h1),
      P("A partir da <b>rodada 6</b> (ou antes, com o Evento “Novo Protocolo”), qualquer agente parado num Esconderijo pode adotar "
        "o Protocolo Substituição: pegue uma Carta de Substituição. Ela tem um alfabeto embaralhado — cada letra do texto claro "
        "vira a letra vermelha embaixo dela. A partir daí, todos os seus envelopes novos são cifrados com esse alfabeto "
        "(marque “Substituição” no envelope)."),
      *B(["<b>Custo:</b> cifrar com um alfabeto inteiro dá mais trabalho — você perde o seu próximo turno de movimento.",
          "<b>Benefício:</b> existem 26! (mais de 400 septilhões) alfabetos possíveis, então força bruta não funciona. Entregar um envelope de Substituição no QG vale <b>4 PI</b>.",
          "<b>Como atacar:</b> no Laboratório, contra um envelope de Substituição, em vez de rolar o dado você compra 1 Carta de "
          "Frequência e a usa: aponte uma letra cifrada e o dono revela a letra clara correspondente. Com algumas letras reveladas "
          "e o tamanho da palavra, tente adivinhar a Missão (mesma recompensa: +2 PI / -1 PI)."]),
      P(f"Frequência das letras no português: {freq}. Na vida real, a análise de frequência é exatamente como as cifras de "
        "substituição foram quebradas: as letras mais comuns da mensagem cifrada provavelmente são A, E, O, S…", box),
      P("11. Pontuação (resumo)", h1),
      table([["Ação", "PI"],
             ["Entregar envelope de César no seu QG e decifrar certo", "+3"],
             ["Entregar envelope de Substituição no seu QG e decifrar certo", "+4"],
             ["Entregar envelope mas decifrar errado", "+1"],
             ["Quebrar envelope de um rival no Laboratório", "+2 (o rival perde 1)"],
             ["Cartas de Evento", "variável"]], [12 * cm, 4 * cm]),
      P("12. Variantes", h1),
      *B(["<b>Modo iniciante:</b> use só as Cartas de Chave de 1 a 10, só Missões de até 5 letras e jogue sem o Protocolo Substituição.",
          "<b>Modo avançado:</b> cada agência usa a sua habilidade especial (descrita na Ficha de Agente).",
          "<b>Partida rápida (20 min):</b> vitória com 8 PI e Substituição liberada desde a rodada 3."]),
      P("13. Dúvidas frequentes", h1),
      table([["Pergunta", "Resposta"],
             ["Posso olhar a Carta de Missão de um envelope que interceptei?", "Não. Só o dono vê. Ela serve para conferir a palavra que você anunciar."],
             ["E se duas chaves gerarem palavras que fazem sentido?", "Vale apenas a palavra exatamente igual à da Carta de Missão. Se errar, tente de novo em outro turno."],
             ["Posso carregar mais de 3 envelopes?", "Não. Envelopes interceptados de rivais também contam no limite de 3."],
             ["Posso trocar de chave e também adotar Substituição no mesmo turno?", "Não. No Esconderijo você escolhe uma das duas ações."],
             ["Posso mentir para uma Carta Informante?", "Não. O agente secreto mente para o inimigo, mas não para as regras."],
             ["O que acontece com um envelope quebrado?", "Vai para o descarte, junto com a Carta de Missão correspondente do dono."]],
            [7 * cm, 9 * cm]),
      P("14. O que o jogo ensina", h1),
      *B(["Cifrar e decifrar com a Cifra de César e com uma cifra de substituição monoalfabética.",
          "O algoritmo é conhecido por todos; a segurança está na chave (princípio de Kerckhoffs).",
          "A Cifra de César tem só 25 chaves e cai por força bruta; pistas sobre a chave reduzem ainda mais o espaço de busca.",
          "Trocar de chave periodicamente limita o estrago de um vazamento.",
          "A substituição tem um espaço de chaves enorme, mas cai por análise de frequência."])]
build(f"{OUTDIR}/regras_operacao_cesar.pdf", s, "Manual de Regras", "Regras - Operação César")

# =============================================================== TESTE / FEEDBACK
t = [P("Sessão de Teste e Feedback", title), Spacer(1, 6), P("Operação César · roteiro para a sessão com colegas", sub), Spacer(1, 12),
     P(f"Equipe: {TEAM}", center),
     P("1. Roteiro da sessão (cerca de 50 min)", h1),
     table([["Tempo", "Etapa", "Responsável"],
            ["5 min", "Boas-vindas e pré-teste (folha individual, abaixo)", "Lucas"],
            ["5 min", "Explicação rápida: Cifra de César com a Roda + resumo do turno", "Pedro"],
            ["30 min", "Partida em mesas de 3 ou 4 jogadores; um integrante observa cada mesa e anota", "Natan / Pedro"],
            ["5 min", "Pós-teste (mesmos exercícios, valores diferentes)", "Lucas"],
            ["5 min", "Formulário de feedback + conversa aberta", "Equipe"]], [2.2 * cm, 10.3 * cm, 3.5 * cm]),
     P("Registrar: fotos das mesas (com autorização), duração real da partida, placar final, dúvidas que apareceram e regras que foram mal interpretadas.", box),
     P("2. Ficha de observação (para o integrante da equipe)", h1),
     table([["Item", "Anotações"], ["Mesa / nº de jogadores", ""], ["Duração da partida", ""], ["Rodada em que a Substituição apareceu", ""],
            ["Dúvidas de regra (quais?)", ""], ["Momentos de maior diversão", ""], ["Momentos parados ou confusos", ""],
            ["Os jogadores usaram força bruta corretamente?", ""], ["Placar final", "<br/>"]], [7 * cm, 9 * cm]),
     PageBreak(),
     P("3. Pré-teste (antes de jogar)", h1),
     P("Nome (opcional): ______________________________", lft),
     *N([f"Cifre a palavra <b>MAPA</b> com a Cifra de César, chave k = 4: ______________",
         f"Decifre <b>FKDYH</b>, sabendo que foi cifrado com k = 3: ______________",
         "Quantas chaves diferentes existem na Cifra de César (sem contar k = 0)? ______",
         "Em uma frase: por que a Cifra de César é considerada fraca? ____________________________________________"]),
     P("4. Pós-teste (depois de jogar)", h1),
     P("Nome (opcional): ______________________________", lft),
     *N([f"Cifre a palavra <b>PORTO</b> com a Cifra de César, chave k = 5: ______________",
         f"Decifre <b>ZLUOH</b> (dica: a chave é menor que 8): ______________",
         "O que é um ataque de força bruta? ____________________________________________",
         "Por que a cifra de substituição é mais forte que a de César, e como ela pode ser quebrada? ____________________________"]),
     P(f"Gabarito (para a equipe): pré-teste 1) QETE · 2) CHAVE · 3) 25. Pós-teste 1) {caesar('PORTO', 5)} · 2) SENHA (k = 7).", box),
     PageBreak(),
     P("5. Formulário de feedback", h1),
     P("Marque de 1 (discordo totalmente) a 5 (concordo totalmente)."),
     table([["Afirmação", "1", "2", "3", "4", "5"],
            ["As regras foram fáceis de entender.", "", "", "", "", ""],
            ["O jogo foi divertido.", "", "", "", "", ""],
            ["O jogo foi desafiador na medida certa.", "", "", "", "", ""],
            ["A duração da partida foi adequada.", "", "", "", "", ""],
            ["Agora sei cifrar e decifrar com a Cifra de César.", "", "", "", "", ""],
            ["Entendi por que a Cifra de César é fraca (força bruta).", "", "", "", "", ""],
            ["Entendi por que a substituição é mais forte e como pode ser atacada.", "", "", "", "", ""],
            ["A Roda de Cifra ajudou.", "", "", "", "", ""],
            ["Eu jogaria de novo.", "", "", "", "", ""]], [10 * cm] + [1.2 * cm] * 5),
     Spacer(1, 10),
     P("O que você mais gostou? ______________________________________________________________", lft),
     P("O que foi confuso ou chato? ___________________________________________________________", lft),
     P("Que regra você mudaria? ______________________________________________________________", lft),
     P("6. Resultados e mudanças (preencher depois do teste)", h1),
     table([["Feedback recebido", "Mudança feita no jogo"]] + [["<br/><br/>", ""]] * 5, [8 * cm, 8 * cm]),
     P("Média de acertos: pré-teste ____ / 4   ·   pós-teste ____ / 4", lft)]
build(f"{OUTDIR}/teste_e_feedback.pdf", t, "Sessão de teste e feedback", "Teste e feedback - Operação César")
print("ok")
