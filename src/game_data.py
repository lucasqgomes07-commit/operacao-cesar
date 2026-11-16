# Dados compartilhados do jogo Operação César
import random

NAVY = "#1B2333"; RED = "#B3261E"; CREAM = "#F4ECD8"; GOLD = "#C9A227"
AGENCIES = [
    # nome, cor, agente, letra, habilidade
    ("Corvo", "#2B2B2B", "Agente Noir", "C", "Uma vez por partida, evite uma abordagem (o atacante não rola)."),
    ("Raposa", "#E07A1F", "Agente Rubra", "R", "No Laboratório, teste 1 chave a mais do que o dado indicar."),
    ("Coruja", "#2F6FB3", "Agente Vigília", "O", "Ao comprar Informante, compre 2, fique com 1 e devolva a outra ao fundo."),
    ("Jaguar", "#2E8B57", "Agente Mata", "J", "Uma vez por partida, role 2 dados no movimento e some."),
]

# 40 casas, índice 0 = canto superior esquerdo, sentido horário
SIDE_PATTERN = ["rua", "informante", "embaixada", "rua", "tunel", "evento", "laboratorio", "rua", "x"]
STREETS = ["Av. Presidente Vargas", "Rua da Doca", "Trav. do Farol", "Rua do Comércio",
           "Av. Nazaré", "Rua dos Mercadores", "Boulevard Castilhos", "Rua da Estação",
           "Av. Portuária", "Rua do Teatro", "Trav. das Mangueiras", "Rua da Catedral",
           "Av. Almirante", "Rua do Cais"]
EMBASSIES = ["Embaixada do Norte", "Embaixada do Leste", "Embaixada do Sul", "Embaixada do Oeste"]
LABS = ["Laboratório da Universidade", "Laboratório do Porto", "Laboratório da Estação", "Laboratório do Observatório"]
INFORMANTS = ["Mercado Ver-o-Peso", "Café Central", "Banca de Jornal", "Feira do Açaí"]
EVENTS = ["Praça da República", "Estação Ferroviária", "Cais do Porto", "Teatro da Paz"]

def board_cells():
    cells = []
    st = iter(STREETS); em = iter(EMBASSIES); lb = iter(LABS); inf = iter(INFORMANTS); ev = iter(EVENTS)
    for side in range(4):
        cells.append(("qg", f"QG {AGENCIES[side][0]}", side))
        for k, t in enumerate(SIDE_PATTERN):
            idx = side * 10 + k + 1
            if t == "x":
                t = "esconderijo" if side in (0, 2) else "rua"
            if t == "rua": cells.append(("rua", next(st), None))
            elif t == "embaixada": cells.append(("embaixada", next(em), None))
            elif t == "laboratorio": cells.append(("laboratorio", next(lb), None))
            elif t == "informante": cells.append(("informante", next(inf), None))
            elif t == "evento": cells.append(("evento", next(ev), None))
            elif t == "tunel": cells.append(("tunel", "Túnel " + "ABAB"[side], None))
            elif t == "esconderijo": cells.append(("esconderijo", "Esconderijo", None))
    return cells

TYPE_STYLE = {
    "qg": ("QG", None),
    "rua": ("Rua", "#E9E2CF"),
    "embaixada": ("Embaixada", "#F2C94C"),
    "laboratorio": ("Laboratório", "#7FB3D5"),
    "informante": ("Informante", "#C39BD3"),
    "evento": ("Evento", "#F1948A"),
    "tunel": ("Túnel", "#A9A9A9"),
    "esconderijo": ("Esconderijo", "#82C99A"),
}

MISSIONS = ["AGENTE", "SENHA", "PORTO", "CHAVE", "RADIO", "MAPA", "ALVO", "PONTE", "TREM", "NAVIO",
            "COFRE", "CODIGO", "SINAL", "ESPIAO", "MERCADO", "PISTA", "DOSSIE", "ARQUIVO", "CAMERA", "FILME",
            "MALETA", "BALSA", "FAROL", "TUNEL", "PALACIO", "JANELA", "CHAPEU", "LUVA", "RECADO", "SEGREDO",
            "AVIAO", "CAIS", "BOIA", "ACAI", "BELEM", "IGARAPE", "ANTENA", "MOEDA", "RELOGIO", "BUSSOLA"]
assert len(MISSIONS) == 40 and all(4 <= len(w) <= 7 for w in MISSIONS)

INFORMANT_CARDS = [
    ("Paridade", "Pergunte a um rival: “Sua chave atual é PAR?” Ele responde sim ou não."),
    ("Metade", "Pergunte a um rival: “Sua chave atual é MAIOR que 12?” Ele responde sim ou não."),
    ("Faixa baixa", "Pergunte a um rival: “Sua chave está entre 1 e 8?” Ele responde sim ou não."),
    ("Faixa alta", "Pergunte a um rival: “Sua chave está entre 18 e 25?” Ele responde sim ou não."),
    ("Múltiplo de 3", "Pergunte a um rival: “Sua chave é múltiplo de 3?” Ele responde sim ou não."),
    ("Múltiplo de 5", "Pergunte a um rival: “Sua chave é múltiplo de 5?” Ele responde sim ou não."),
    ("Escuta", "Escolha um envelope que você interceptou: o dono revela a PRIMEIRA letra do texto claro."),
    ("Tamanho", "Um rival revela quantas chaves diferentes já usou na partida (quantas vezes trocou + 1)."),
]
INFORMANT_CARDS = INFORMANT_CARDS * 2  # 16

EVENT_CARDS = [
    ("Blecaute", "Até o fim da rodada ninguém pode fazer abordagens."),
    ("Vazamento de chave", "O jogador à sua esquerda diz se a chave dele é par ou ímpar."),
    ("Agente duplo", "Troque um envelope que você carrega por um envelope de um rival (sem olhar)."),
    ("Ventania no porto", "Todos os agentes que estão em casas de Rua voltam 2 casas."),
    ("Novo Protocolo", "A partir de agora, o Protocolo Substituição está liberado para todos."),
    ("Correio expresso", "Avance direto até o QG mais próximo da sua agência no sentido do movimento."),
    ("Operação pente-fino", "Todos que carregam 2 ou mais envelopes devolvem 1 à Embaixada mais próxima (descartado)."),
    ("Rádio grampeado", "Escolha um rival: ele deve trocar de chave no próximo turno ou perder 1 PI."),
    ("Noite sem lua", "Você pode mover-se 1 casa a mais ou a menos neste turno."),
    ("Criptoanalista convidado", "No seu próximo Laboratório, role 2 dados e some as chaves testadas."),
    ("Ponto de encontro", "Escolha um rival e mova o seu peão para a casa dele; faça uma abordagem."),
    ("Burocracia", "Pule o seu próximo turno, mas compre 1 Carta Informante agora."),
    ("Chave reutilizada", "Se você nunca trocou de chave, perde 1 PI. Se já trocou, ganhe 1 PI."),
    ("Mensageiro leal", "Proteção: na próxima abordagem contra você, o atacante precisa vencer por 2 ou mais."),
    ("Interferência", "Todos os jogadores passam 1 Carta Informante para o jogador à esquerda."),
    ("Promoção", "Ganhe 1 PI por organizar a rede da sua agência."),
]
assert len(EVENT_CARDS) == 16

FREQ_TEXT = ("Escolha um envelope interceptado cifrado por SUBSTITUIÇÃO. Aponte uma letra do texto cifrado: "
             "o dono revela qual letra do texto claro ela representa.")

def substitution_alphabets():
    rnd = random.Random(2026)
    alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    out = []
    while len(out) < 4:
        p = alph[:]; rnd.shuffle(p)
        if all(a != b for a, b in zip(alph, p)):
            out.append("".join(p))
    return out

PT_FREQ = [("A", 14.6), ("E", 12.6), ("O", 10.7), ("S", 7.8), ("R", 6.5), ("I", 6.2), ("N", 5.0),
           ("D", 5.0), ("M", 4.7), ("U", 4.6), ("T", 4.3), ("C", 3.9)]

def caesar(word, k):
    return "".join(chr((ord(c) - 65 + k) % 26 + 65) for c in word)
