from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUT = "../gdd/GDD_Operacao_Cesar.pdf"
INK = colors.HexColor("#1B2333")
ACC = colors.HexColor("#B3261E")
SOFT = colors.HexColor("#EEF1F6")

ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5,
                      leading=15, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6)
bul = ParagraphStyle("bul", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15,
                    textColor=ACC, spaceBefore=14, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
                    textColor=INK, spaceBefore=8, spaceAfter=4)
title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=34, leading=40,
                       alignment=TA_CENTER, textColor=INK)
sub = ParagraphStyle("s", fontName="Helvetica", fontSize=13, leading=18,
                     alignment=TA_CENTER, textColor=ACC)
center = ParagraphStyle("c", parent=body, alignment=TA_CENTER)
cell = ParagraphStyle("cell", parent=body, fontSize=9.5, leading=13, alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")

def P(t, s=body): return Paragraph(t, s)
def B(items): return [Paragraph(i, bul, bulletText="•") for i in items]
def table(rows, widths, header=True):
    data = [[Paragraph(str(c), cellb if (header and r == 0) or c_i == 0 and not header else cell)
             for c_i, c in enumerate(row)] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9CFDA")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), SOFT)]
    else:
        st += [("BACKGROUND", (0, 0), (0, -1), SOFT)]
    t.setStyle(TableStyle(st))
    return t

def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(2 * cm, 1.2 * cm, "Operação César — GDD · Resolução Discreta de Problemas · CESUPA")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {d.page}")
    c.restoreState()

s = []
# ---------- Capa ----------
s += [Spacer(1, 4.5 * cm), P("OPERAÇÃO CÉSAR", title), Spacer(1, 8),
      P("Serious Game de tabuleiro sobre Criptografia", sub), Spacer(1, 1.2 * cm),
      P("Game Design Document (GDD)", center), Spacer(1, 2.2 * cm),
      table([["Instituição", "Centro Universitário do Estado do Pará (CESUPA)"],
             ["Curso", "Ciência da Computação"],
             ["Disciplina", "Resolução Discreta de Problemas"],
             ["Professor", "Pedro Girotto"],
             ["Equipe", "Lucas Gomes<br/>Pedro Passos<br/>Natan Brasil"],
             ["Tipo de implementação", "Lúdica (jogo de tabuleiro físico)"]],
            [5 * cm, 10 * cm], header=False),
      PageBreak()]

# ---------- Título e descrição ----------
s += [P("Título do Jogo", h1), P("<b>Operação César</b>"),
      P("Curta descrição", h1),
      P("Jogo de tabuleiro competitivo para 2 a 4 jogadores em que cada um comanda um agente secreto "
        "de uma agência de espionagem. Os agentes cifram mensagens com a <b>Cifra de César</b>, "
        "atravessam a cidade para entregá-las ao seu QG e tentam interceptar e <b>quebrar</b> as "
        "mensagens dos rivais. Quem melhor cifrar, proteger e decifrar informações vence.")]

s += [P("Objetivos educacionais", h1),
      P("Ao final de uma partida, o jogador deve ser capaz de:"),
      *B(["<b>Cifrar e decifrar</b> mensagens usando a Cifra de César (deslocamento de k posições no alfabeto, "
          "com volta de Z para A).",
          "Entender o papel da <b>chave</b>: o algoritmo é público, a segurança está só na chave.",
          "Perceber a <b>fraqueza da Cifra de César</b>: existem apenas 25 chaves úteis, então um ataque de "
          "<b>força bruta</b> (testar todas) é viável.",
          "Compreender a <b>cifra de substituição monoalfabética</b> (alfabeto embaralhado) como evolução: "
          "ela tem um número enorme de chaves, mas ainda pode ser atacada por <b>análise de frequência</b>.",
          "Relacionar boas práticas: <b>troca periódica de chave</b> e não reutilizar a mesma chave por muito tempo."]),
      P("Conceito central — exemplo usado no manual", h2),
      table([["Texto claro", "A", "G", "E", "N", "T", "E"],
             ["Chave k = 3", "+3", "+3", "+3", "+3", "+3", "+3"],
             ["Texto cifrado", "D", "J", "H", "Q", "W", "H"]],
            [3.4 * cm] + [1.6 * cm] * 6),
      Spacer(1, 4),
      P("Cifrar: C = (P + k) mod 26. Decifrar: P = (C - k) mod 26. Os jogadores fazem essa conta "
        "fisicamente com a <b>Roda de Cifra</b> (dois discos de papel sobrepostos).")]

# ---------- Identidade ----------
s += [P("Identidade do jogo", h1),
      P("Belém dos anos 60, auge da Guerra Fria. Uma rede de agências de espionagem disputa segredos que "
        "circulam pela cidade: no Porto, na Estação, no Mercado e nas Embaixadas. Cada jogador é o melhor "
        "agente de sua agência e recebe missões que precisam chegar ao QG <b>sem que o inimigo as leia</b>. "
        "Para isso, toda mensagem viaja cifrada. Mas os rivais também têm laboratórios de criptoanálise, "
        "e uma mensagem interceptada pode ser quebrada se a chave for fraca ou ficar tempo demais em uso. "
        "Proteja seus segredos, roube os dos outros e torne-se o <b>Agente Mestre</b> da cidade.")]

# ---------- Mecânica ----------
s += [P("Descrição da mecânica", h1),
      P("Gênero: tabuleiro de movimentação com rolagem de dados, coleta e entrega (pick-up and deliver), "
        "interação direta entre jogadores (interceptação) e dedução (quebra de cifras). <b>Não há perguntas "
        "e respostas</b>: o conteúdo de criptografia <i>é</i> a própria mecânica — para pontuar é preciso "
        "cifrar, proteger e decifrar de verdade."),
      P("Preparação", h2),
      *B(["Cada jogador escolhe uma agência, pega seu peão, sua Roda de Cifra, 3 envelopes e uma Ficha de Agente.",
          "Cada jogador compra uma <b>Carta de Chave</b> (valores de 1 a 25) e a mantém em segredo. Essa é sua chave atual.",
          "Embaralhe os baralhos de Missão, Evento e Informante e coloque-os nos espaços indicados do tabuleiro.",
          "Todos começam no seu QG com 0 Pontos de Inteligência (PI)."]),
      P("Turno do jogador", h2),
      *B(["<b>1. Mover:</b> role 1 dado (d6) e ande pelo circuito da cidade; atalhos (túneis) podem ser usados ao parar na entrada.",
          "<b>2. Agir no local</b> onde parou (ver tabela de locais).",
          "<b>3. Abordagem:</b> se parar na mesma casa de outro agente que carrega envelopes, pode tentar interceptar: "
          "ambos rolam 1 dado; quem tirar mais alto vence (empate favorece quem defende). O vencedor atacante pega 1 envelope à escolha."]),
      P("Locais do tabuleiro", h2),
      table([["Local", "O que acontece"],
             ["Embaixada (4)", "Compre 1 Carta de Missão (uma palavra de 4 a 7 letras, ex.: PORTO, SENHA, RADIO). "
              "Cifre a palavra com sua chave atual, escreva o texto cifrado num envelope e coloque a carta virada "
              "para baixo embaixo da sua Ficha de Agente. Você carrega o envelope."],
             ["QG da sua agência", "Entregue envelopes. Para pontuar, decifre seu próprio envelope em voz alta: se a palavra "
              "bater com a Carta de Missão, ganhe <b>3 PI</b>. Se errar, a mensagem foi corrompida: 1 PI."],
             ["Laboratório (4)", "Tente quebrar um envelope interceptado: role 1 dado e teste esse número de chaves diferentes "
              "na sua Roda (anote na Folha de Criptoanálise as chaves já testadas). Ao encontrar uma palavra válida, "
              "anuncie-a: se o dono confirmar pela Carta de Missão, ganhe <b>2 PI</b> e o dono perde 1 PI."],
             ["Esconderijo (2)", "Troque sua chave: devolva a Carta de Chave e compre outra. Envelopes novos usam a chave nova "
              "(boa prática de rotação de chaves)."],
             ["Informante (4)", "Compre 1 Carta Informante: dicas sobre a chave de um rival (ex.: “a chave é par”, "
              "“a chave é maior que 12”). Reduzem o espaço de busca da força bruta."],
             ["Evento (4)", "Compre 1 Carta de Evento (blecaute, apagão no porto, agente duplo, vazamento de chave etc.)."],
             ["Túneis", "Atalhos entre bairros: custam a ação do turno, mas encurtam o caminho."]],
            [3.6 * cm, 12.4 * cm]),
      P("Nível 2 — Protocolo Substituição", h2),
      P("A partir da rodada 6 (ou ao comprar a carta de Evento “Novo Protocolo”), um jogador no Esconderijo pode "
        "adotar o <b>Protocolo Substituição</b>: recebe uma Carta de Alfabeto embaralhado e passa a cifrar com "
        "substituição monoalfabética. Custo: perde o próximo turno de movimento (cifrar é mais trabalhoso). "
        "Benefício: entregas cifradas por substituição valem 4 PI e o Laboratório não pode mais usar força bruta contra esses envelopes; o atacante precisa de "
        "Cartas de <b>Análise de Frequência</b> (cada uma revela a correspondência de uma letra, priorizando as "
        "mais comuns do português: A, E, O, S, R). Assim o jogador sente, na prática, por que a substituição é "
        "mais forte que César e por que ainda não é perfeita."),
      P("Fim de jogo e vitória", h2),
      P("O primeiro agente a alcançar <b>12 PI</b> vence. Se após 12 rodadas ninguém chegar lá, vence quem tiver mais PI; "
        "empate é decidido por mais envelopes quebrados no Laboratório.")]

# ---------- Características ----------
s += [P("Características", h1),
      *B(["Ambientação de espionagem retrô em uma Belém fictícia dos anos 60 (Porto, Mercado, Estação, Embaixadas).",
          "Aprendizado ativo: toda pontuação exige cifrar ou decifrar de verdade com a Roda de Cifra.",
          "Tensão entre <b>velocidade</b> (correr ao QG) e <b>segurança</b> (trocar chave, adotar Substituição).",
          "Interação direta: interceptações e informantes fazem os jogadores pensarem como atacantes e defensores.",
          "Progressão de dificuldade em dois níveis (César > Substituição), refletindo a evolução histórica.",
          "Partidas curtas (30 a 40 minutos), adequadas à sessão de teste em sala.",
          "Componentes imprimíveis em papel A4, com custo baixo e fácil reprodução."])]

# ---------- Arte ----------
s += [P("Arte", h1),
      P("Jogo físico 2D, com arte digital vetorial em estilo <b>retrô de cartaz de espionagem</b> (anos 60): "
        "paleta limitada de azul-marinho, vermelho, creme e preto, silhuetas de agentes, carimbos de "
        "“CONFIDENCIAL” e tipografia de máquina de escrever. Cada agência tem uma cor e um símbolo próprios. "
        "O tabuleiro é um mapa estilizado da cidade com o circuito de casas; as cartas seguem o formato de "
        "fichas de arquivo. A Roda de Cifra é impressa em dois discos (externo: texto claro; interno: texto "
        "cifrado) presos por um colchete. Ferramentas previstas: Canva/Figma para artes e impressão em A4.")]

# ---------- Música ----------
s += [P("Música/Trilha Sonora", h1),
      P("Por ser um jogo de tabuleiro, a trilha é opcional e tocada como ambientação durante a partida "
        "(playlist instrumental). Referências de estilo:"),
      *B(["“Mission: Impossible Theme” — Lalo Schifrin (espionagem clássica, ritmo de tensão).",
          "“Peter Gunn” — Henry Mancini (jazz de suspense dos anos 60).",
          "Trilhas instrumentais da série de jogos <i>Hitman</i> (suspense discreto, furtividade).",
          "Playlists de “spy jazz” / “60s spy music” no YouTube para o clima retrô."]),
      P("Sugestão de uso: música mais calma durante a movimentação e uma faixa curta de 1 minuto como "
        "“cronômetro” opcional para tentativas no Laboratório.")]

# ---------- Interface ----------
s += [KeepTogether([P("Interface/Controles", h1),
      P("Não há teclas ou toque: as “ações” são físicas e feitas com os componentes."),
      table([["Componente", "Quantidade", "Uso"],
             ["Tabuleiro (mapa da cidade)", "1 (4 folhas A4 unidas)", "Circuito com 40 casas, 4 QGs, Embaixadas, Laboratórios, Esconderijos, túneis"],
             ["Peões de agente", "4", "Um por agência (Corvo, Raposa, Coruja, Jaguar)"],
             ["Roda de Cifra", "4", "Ferramenta para cifrar/decifrar César"],
             ["Cartas de Chave", "25", "Valores 1 a 25, mantidas em segredo"],
             ["Cartas de Missão", "40", "Palavras temáticas de 4 a 7 letras"],
             ["Cartas Informante", "16", "Pistas sobre chaves rivais"],
             ["Cartas de Evento", "16", "Acontecimentos que mudam a rodada"],
             ["Cartas de Alfabeto (Substituição)", "4", "Alfabetos embaralhados do Nível 2"],
             ["Cartas de Análise de Frequência", "12", "Revelam uma letra de uma cifra de substituição"],
             ["Envelopes + Folhas de Criptoanálise", "Bloco", "Para escrever mensagens e registrar chaves testadas"],
             ["Ficha de Agente + marcador de PI", "4", "Trilha de pontos de 0 a 12"],
             ["Dado de 6 faces", "2", "Movimento, abordagem e tentativas no Laboratório"]],
            [5.2 * cm, 3.6 * cm, 7.2 * cm])]),
      Spacer(1, 4),
      P("Mesa: cada jogador mantém à sua frente a Ficha de Agente (com as Cartas de Missão viradas para baixo), "
        "a Carta de Chave escondida e sua Roda de Cifra. Um resumo de turno é impresso no verso da Ficha.")]

# ---------- Dificuldade ----------
s += [P("Dificuldade", h1),
      *B(["<b>Inimigos:</b> os outros jogadores, que podem interceptar envelopes e quebrar suas cifras.",
          "<b>Puzzles:</b> cada envelope interceptado é um quebra-cabeça de criptoanálise (força bruta guiada por dado e pistas).",
          "<b>Elementos de cenário:</b> túneis, Laboratórios e Esconderijos espalhados obrigam a planejar a rota.",
          "<b>Eventos:</b> blecaute (ninguém intercepta na rodada), vazamento de chave (um jogador revela se sua chave é par ou ímpar), "
          "agente duplo (troque um envelope com um rival) etc.",
          "<b>Curva de dificuldade:</b> rodadas 1–5 só César; a partir da rodada 6, o Protocolo Substituição torna as defesas mais fortes e exige novas estratégias de ataque.",
          "<b>Modo iniciante:</b> chaves limitadas de 1 a 10 e palavras de 4 letras, para turmas que estão vendo o conteúdo pela primeira vez."])]

# ---------- Personagem ----------
s += [KeepTogether([P("Personagem", h1),
      P("Cada jogador controla o agente principal de uma das quatro agências rivais:"),
      table([["Agência", "Agente", "Perfil / habilidade especial (opcional, modo avançado)"],
             ["Corvo (preto)", "Agente Noir", "Mestre da discrição: uma vez por partida, evita uma abordagem."],
             ["Raposa (laranja)", "Agente Rubra", "Criptoanalista: no Laboratório, soma +1 às chaves testadas."],
             ["Coruja (azul)", "Agente Vigília", "Rede de informantes: compra 2 Cartas Informante e fica com 1."],
             ["Jaguar (verde)", "Agente Mata", "Velocista: uma vez por partida, rola 2 dados no movimento."]],
            [3.4 * cm, 3.2 * cm, 9.4 * cm])])]

# ---------- Cronograma ----------
s += [P("Cronograma", h1),
      P("Entrega final no Classroom: <b>11/12/2026, 08:00</b>."),
      table([["Período", "Meta", "Responsáveis"],
             ["16–19/11", "Conceito, GDD e definição das regras base", "Equipe"],
             ["20–25/11", "Regras v1, lista de cartas e protótipo em papel (rascunho)", "Equipe"],
             ["26–27/11", "Teste interno do grupo e primeiros ajustes de balanceamento", "Equipe"],
             ["28/11–02/12", "Sessão de teste com colegas da turma + formulário de feedback", "Equipe"],
             ["03–06/12", "Iteração das regras a partir do feedback; artes finais (tabuleiro, cartas, Roda)", "Equipe"],
             ["07–09/12", "Repositório GitHub (PDF de regras + artes), slides da apresentação", "Equipe"],
             ["10/12", "Revisão geral e ensaio da apresentação", "Equipe"],
             ["11/12", "Entrega no Classroom e apresentação", "Equipe"]],
            [3 * cm, 10 * cm, 3 * cm])]

# ---------- Teste ----------
s += [P("Plano de teste e feedback", h1),
      P("Conforme exigido, faremos pelo menos uma sessão de teste com colegas da turma (público-alvo). "
        "Cada mesa terá 3 ou 4 jogadores e um membro da equipe como observador. Coletaremos:"),
      *B(["Antes e depois: cifrar e decifrar uma palavra curta com chave dada (mede o aprendizado).",
          "Formulário (escala 1–5): clareza das regras, diversão, desafio, duração e se entenderam por que César é fraca.",
          "Anotações do observador: dúvidas frequentes, regras confusas, tempo de cada etapa.",
          "Resultado: lista de mudanças aplicadas na versão final, apresentada nos slides."])]

# ---------- Definições gerais ----------
s += [KeepTogether([P("Definições gerais", h1),
      table([["Gênero", "Tabuleiro competitivo de espionagem; coleta e entrega com dedução (serious game educacional)"],
             ["Plataformas", "Jogo físico impresso (A4); arquivos e regras disponíveis no GitHub"],
             ["Quantidade de níveis", "2 níveis: Nível 1 — Cifra de César; Nível 2 — Protocolo Substituição (+ modo iniciante opcional)"],
             ["Quantidade de vilões/inimigos", "Até 3 agências rivais (os outros jogadores) e 16 eventos de cenário"],
             ["Público alvo", "Estudantes de Computação e áreas afins (a partir de 15 anos) iniciando em criptografia; 2 a 4 jogadores; 30–40 min"],
             ["Puzzles", "Quebra de cifras de César por força bruta guiada (dado + pistas) e de substituição por análise de frequência"]],
            [4.6 * cm, 11.4 * cm], header=False)])]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=2 * cm, bottomMargin=2 * cm,
                        title="GDD — Operação César", author="Lucas Gomes, Pedro Passos, Natan Brasil")
doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=footer)
print("ok")
