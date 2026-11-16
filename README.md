# Operação César

Serious game de tabuleiro sobre **criptografia**, feito para a disciplina **Resolução Discreta de Problemas** (CESUPA, Ciência da Computação, Prof. Pedro Girotto).

**Equipe:** Lucas Gomes · Pedro Passos · Natan Brasil

## O jogo

Belém, anos 60. Quatro agências de espionagem (Corvo, Raposa, Coruja e Jaguar) disputam os segredos da cidade. Cada jogador é um agente que:

1. pega missões nas Embaixadas e **cifra** a mensagem com a **Cifra de César** usando uma Roda de Cifra;
2. atravessa a cidade para entregar o envelope no seu QG, onde precisa **decifrá-lo** corretamente para pontuar;
3. intercepta envelopes dos rivais e tenta **quebrá-los** no Laboratório por **força bruta**, usando pistas de Informantes;
4. a partir da rodada 6, pode adotar o **Protocolo Substituição** (alfabeto embaralhado), que resiste à força bruta mas cai por **análise de frequência**.

Vence quem chegar primeiro a 12 Pontos de Inteligência. São 2 a 4 jogadores e a partida leva de 30 a 40 minutos.

## Conceitos de criptografia trabalhados

- Cifrar e decifrar: `C = (P + k) mod 26` e `P = (C - k) mod 26`
- O algoritmo é público e a segurança está na chave (princípio de Kerckhoffs)
- O espaço de chaves pequeno da Cifra de César (25) permite força bruta
- Troca periódica de chaves
- Cifra de substituição monoalfabética (26! chaves) e análise de frequência

## Arquivos

| Pasta | Conteúdo |
|---|---|
| `gdd/` | GDD do jogo (Game Design Document) |
| `regras/` | Manual de regras completo |
| `artes/tabuleiro_4xA4.pdf` | Tabuleiro em 4 folhas A4 paisagem para colar em 2x2 |
| `artes/tabuleiro_A2.pdf` | Tabuleiro numa folha A2 só (para gráfica) |
| `artes/cartas.pdf` | 113 cartas (Missão, Chave, Informante, Evento, Frequência e Substituição), com frente e verso |
| `artes/roda_de_cifra.pdf` | Roda de Cifra das 4 agências (disco externo e interno) |
| `artes/fichas_e_folhas.pdf` | Fichas de Agente, envelopes, folhas de criptoanálise e peões |
| `teste/` | Roteiro da sessão de teste, pré e pós-teste e formulário de feedback |
| `src/` | Scripts Python (ReportLab) que geram todos os PDFs |

## Como imprimir e montar

1. Imprima tudo em A4 e em **tamanho real (100%)**, sem "ajustar à página".
2. **Tabuleiro:** recorte as margens e cole as 4 folhas em 2x2. Se preferir, imprima `tabuleiro_A2.pdf` numa gráfica.
3. **Cartas:** imprima em frente e verso, virando pela borda longa, e recorte. Papel mais grosso (180 g) é melhor.
4. **Roda de Cifra:** recorte os dois discos, coloque o menor sobre o maior e prenda com um colchete (bailarina).
5. Separe também 2 dados de 6 faces, lápis e marcadores (moedas ou clipes).

## Como gerar os PDFs novamente

```bash
pip install reportlab pypdf
cd src
python arts.py ../artes      # tabuleiro, cartas, roda, fichas
python docs.py ../teste      # regras + teste (mova as regras para ../regras)
python gdd.py                # GDD
```
