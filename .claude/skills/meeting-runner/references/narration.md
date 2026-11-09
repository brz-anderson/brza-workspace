# A narração no chat da coordenação, e o painel

Anderson é o decisor e o mantenedor, e o tempo dele é curto. Na Carvão ele acompanhou a reunião pelo chat da
coordenação ("informou muito bem o desenrolar"); na MCP, pelo chat de cada filha ("deixou a desejar no acompanhamento dos
fatos"). A diferença não foi o silêncio (as duas ficaram no máximo 7m43 e 3m34 sem texto): foi o **conteúdo**. A Carvão
nomeou personas em 11 de 57 blocos e deu síntese com posição e números por persona; a MCP nomeou em 4 de 47, duas
personas nunca apareceram, e deu o agregado. A R1.4 do PLN-017 escolheu os três itens abaixo; a argumentação integral
fica para a fase do painel.

## As regras

| Quando | O quê | Forma | Por quê |
| :-- | :-- | :-- | :-- |
| As sessões abrem | quem é quem | tabela "Persona · papel · runtime · modelo · esforço" em uma mensagem | a persona é o sujeito; a Carvão abriu assim |
| Cada chegada (mensagem de fim de rodada, `wait_round.py`) | quem respondeu e quem falta, com o tempo da mais lenta | uma linha: "R2 · 4/6 — entregaram Lenha, Cinza, Tição, Fole; faltam Faísca (Grok, 5 min) e Fogareiro" | R1.4 (2) |
| Rodada aberta, sem chegada há 3 min | o mesmo status, com o que a coordenação está fazendo | uma linha | a espera longa sem texto é onde Anderson abre o chat da filha |
| Rodada fecha | a posição e a confiança de cada persona | a tabela do `tally.py --md`: Persona · posição · confiança (Δ R1) · mudou? · voto; abaixo, a sala (média, mediana, n), o revisor quando houver, as viradas nomeadas | R1.4 (1) |
| Rodada fecha | os números conferidos | lista curta "confere / diverge: ‹afirmação› — ‹comando ou fonte› → ‹resultado›" | R1.4 (3) |
| Rodada fecha | o painel | o `::orca-visual` abaixo, conferido por PNG, **depois** da tabela; o texto não depende dele | R1.3 |
| Prova da coordenação | o resultado que muda a sala | no máximo duas linhas; o erro de shell da própria coordenação não vai ao chat | ruído |
| Fechamento | o registro | o worklog da coordenação em `<details>`; os das personas por link | `AGENTS.md` |
| Rodada de decisão | as decisões de Anderson | em texto, abaixo da proposta inteira, `Custo: … Se paga: …`, e o voto das personas por opção (`closing.md`) | R2.4 |

**Exemplos literais** (da Carvão, às 20h03, e da MCP, na R3):

- Abertura: "Seis personas abertas: Tição (Claude · Opus 5.5 · high, o Narrador), Faísca (Grok · 4.7 · xhigh, a
  Provocadora), Cinza (Codex · sol · medium, a Medidora)…"
- Chegada: "R3 · 4/6 — entregaram Atalho (35 s), Salto (26 s), Plantão (24 s), Muralha (41 s); faltam Régua (Codex, há 1 min) e
  Cartógrafo (Antigravity)."
- Fechamento: tabela do `tally.py` e "Sala 57,2 (5/6, Antigravity à parte: 85); revisor 45. Viradas: Muralha C → A+D
  (M1/M2), Salto F → G."

**O que não vai ao chat:** a argumentação integral das personas (R1.4). Ela fica no worklog e, depois, no painel por
plugin (issue ao `studio`).

## O painel

O painel da rodada é um `::orca-visual` gerado por `scripts/panel.py` (D3). Mostra, em um HTML a 736 px: o estado da
rodada (abertura, prazo, quem respondeu), quatro cartões (média da sala, revisor, custo das personas, custo da
coordenação), uma linha por persona (estado, confiança com o delta contra a R1, custo, posição em uma linha, voto e virada),
as medições conferidas, a síntese e "Para Anderson decidir". A v1 só mostra: botão, link para o chat e atualização ao
vivo são da fase do painel.

### O ciclo de publicação (R3.3)

**Um arquivo por rodada, republicado durante ela.** O app relê o visual só quando uma mensagem nova o monta; reescrever o
arquivo não atualiza um frame já montado.

1. **Abertura da rodada:** gere o estado com todos "falta" e publique, com uma linha de texto.
2. **A cada chegada que o `wait_round.py` imprimir (com o aviso ⚠ se faltar o marcador):** gere de novo e publique, com uma linha ("4 de 6; falta
   Régua e Cartógrafo").
3. **No fechamento:** gere com as medições, a síntese e as decisões (`sintese-N.json`) e publique.
4. A rodada seguinte ganha **nome novo**. No fim da reunião, um visual de síntese, também com nome novo.

Os comandos (da raiz do worktree; `$S` e `$R` como no SKILL.md):

```bash
python3 -I .claude/skills/meeting-runner/scripts/panel.py collect 3 --reuniao .sessions/<reuniao>/reuniao.json --opened 21:28:13 --closed 21:30:48
python3 -I .claude/skills/meeting-runner/scripts/panel.py render .sessions/<reuniao>/estado-r3.json --publish-dir "$ORCA_CHAT_SCRATCH_DIR" --png /tmp/painel-r3.png
```

O `render --publish-dir` grava `<reuniao>-r3-<hash>.html` (nome fixo na rodada) e **imprime a linha `::orca-visual{…}`**
que vai numa linha própria da mensagem. Cada mensagem leva um visual; o limite de 8 por resposta não aperta.

### Confira por PNG antes de publicar

A coordenação não vê o chat. Com o `ORCA_CHAT_SCRATCH_DIR` ausente (fora do chat do Studio), o HTML vai ao scratch da
sessão e a rodada leva o caminho. A conferência usa o Chrome headless; o `brza shot` está quebrado até o P5 do PLN-017:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --force-device-scale-factor=1 \
  --window-size=736,2000 --screenshot="$TMPDIR/painel-r3.png" "file://<caminho do .html>"
```

Leia a imagem. Coluna estourada, corte ou texto sobreposto se corrige no gerador, não no HTML solto. Verifique também:
persona sem medição mostra "sem medição"; a média da sala exclui o Antigravity; a faixa de tempo não tem ponto fora do
prazo. Abaixo de 520 px o `arquivo.md:linha` some, por desenho; no celular o painel passa de 2000 px e rola por dentro.

### Limites conhecidos da v1

Sem argumentação integral, sem abrir o chat da persona por clique, sem botão de decisão, sem atualização ao vivo, sem link
para o worklog (ele só chega ao GitHub no commit, o `arquivo.md:linha` vai como texto) e sem custo para Grok e Antigravity
(os runtimes não gravam tokens). Ficam para a fase do painel, na issue ao `studio`.
