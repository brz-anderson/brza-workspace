# PLN-017 — Desenho: o painel da rodada (D3)

## D3 — O painel da rodada no chat da coordenação — `scripts/panel.py` da skill `meeting-runner`

Consultor: o papel `designer`, 2026-11-08. Marca: `[F# · tipo · confiança]`, `[C# · …]` para custo.
Abreviações: `WT` = `/Users/andepb/Projects/brza-workspace/.worktrees/playground`; `ST` = `~/Projects/brza-studio`;
`coordM` = `WT/work/worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md`.

- **Origem:** R1.3 ("opção 1 [Painel gerado no chat, sem código no app…], mas faça uma investigação breve para medirmos
  o custo X benefício da opção 3"), R1.4 ("Posição e confiança de cada persona por rodada", "Quem já respondeu e quem
  falta, em tempo real", "Os números e medições conferidos"; "argumentação integral fica pra fase do painel") e R1.2 (as
  primitivas nascem no `brza sessions`).
- **Contexto:** na reunião MCP remoto Anderson teve de abrir o chat de cada persona; a Carvão mostrou um painel só uma
  vez, no fim, montado à mão. O painel v1 mostra o estado da rodada no chat da coordenação, por `::orca-visual`, sem
  código no app.
- **Protótipo:** [a rodada 3 fechada, dados reais, a 736 px](PLN-017-painel-rodada.png) e [a mesma rodada às 21h29, com o Régua faltando](PLN-017-painel-rodada-parcial.png); o `.html` e o gerador do protótipo ficaram no scratch da sessão (`/private/tmp/wf-improv/desenho/painel-rodada.html`, `panel_proto.py`, `estado-r3.json`); tema escuro `painel-rodada-dark.html`/`.png`;
  a mesma rodada às 21h29:30, com o Régua faltando, `painel-rodada-parcial.html`/`.png`; a 390 px,
  `painel-rodada-390.png`. Gerador do protótipo: `panel_proto.py` + `estado-r3.json`, no mesmo diretório.

### O terreno

- **A base que existe:** o gerador da Carvão é
  `/private/tmp/claude-501/-Users-andepb-Projects-brza-workspace--worktrees-playground/4cbdb093-1f3d-40bc-b10e-a3f8680bae4c/scratchpad/painel.py`,
  117 linhas, com o caminho do worktree fixo e os números finais passados como JSON no `argv` (`painel.py:6-15`)
  [F1 · lido · 95]. Gerou `carvao-em-brasa-reuniao-4d2a.html` e `…-v2-8b1e.html` no
  `chat-scratch/c6630d553b34084f3dba922f7feaf17f/` [F2 · rodado · 95]. Foi escrito entre 20:27:48 e 20:41:21, pela
  coordenação Opus `xhigh` (`/private/tmp/wf-improv/chat/comparacao.md:121`) [F3 · lido · 90]. É uma síntese da
  reunião (paleta, matriz de 15 votos, contraprova), não um painel de rodada: nada nele mostra quem falta.
- **O painel da Carvão passou do teto de altura:** a captura `painel-v2.png` tem 736 × 3900 px [F4 · rodado · 95], e o
  frame do visual vai de 80 a 2000 px (`ST/src/shared/native-chat/native-chat-visual-shell.ts:55-56,304-308`, aplicado
  em `native-chat-visual-height-governor.ts:30`) [F5 · lido · 95]. Com a premissa de que o iframe rola por dentro
  acima do teto, Anderson viu o painel da Carvão numa janela de 2000 px com rolagem interna [F6 · inferido · 75].
- **O que o visual aceita:** um HTML por visual, < 512 KB, "with a new file name each time"; a diretiva numa linha
  própria, no máximo 8 por resposta; tokens do tema com valor de reserva (`ST/resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md:20,26-38,42-46`)
  [F7 · lido · 95]. O clique em link só sai para `http:`/`https:`; link `#` fica no frame; `submit` é cancelado
  (`native-chat-visual-shell.ts:145-158`) [F8 · lido · 95]. Caminho de arquivo, portanto, não abre: vai como texto.
- **Como o app relê o arquivo:** o visual é relido a cada montagem e depois de um salvamento pelo editor do app; não há
  observação do arquivo (`ST/src/renderer/src/components/native-chat/use-native-chat-visual-document.ts:74-131`;
  `native-chat-visual-read-client.ts:1`, "Revalidate every mount") [F9 · lido · 85] (premissa: não li o
  `NativeChatInlineVisual.tsx`, que decide quando `enabled` vale). Consequência: reescrever o mesmo `file` não atualiza o
  frame já montado; uma diretiva nova numa mensagem nova monta e mostra o conteúdo atual, e as menções antigas do mesmo
  nome passam a mostrar o atual quando remontam [F10 · inferido · 75].
- **O celular mostra o visual:** o app móvel extrai a diretiva e a renderiza
  (`ST/mobile/src/components/mobile-markdown-visual-lines.ts:23-46`; `mobile-markdown-blocks.tsx:225-233`)
  [F11 · lido · 90].
- **O que o `brza sessions list --json` dá hoje:** `name`, `title`, `chat`, `claude_session`, `provider_session`,
  `worktree`, `state` (o `chatStatus.state` da aba), `source`, `opened`
  (`~/Projects/brza-workflow/packages/client/bin/brza-sessions:293-310`) [F12 · lido · 95]. Não dá modelo, esforço nem
  latência, e não há verbo `wait` (`:376-391`: `list`, `send`, `title`, `close`) [F13 · lido · 95].
- **O mapa:** o `open` das personas `mcp-*` grava `model` e `effort`; o das personas Claude sai sem `agent`
  (`/Users/andepb/Projects/brza-workspace/.sessions/sessions.jsonl`, linhas `open` de 2026-11-07 21:19:25) [F14 · rodado · 95].
- **A rodada 3 da reunião MCP, os dados do protótipo:**
  - aberta às 21:28:13 (o `task_started` dos dois rollouts Codex); Régua respondeu às 21:30:48 (155 s), Atalho às
    21:28:48 (35 s) [F15 · rodado · 95];
  - Muralha terminou o turno às 21:28:55 (41 s, US$ 0,22), Plantão às 21:28:38 (24 s, US$ 0,03)
    (`/private/tmp/wf-improv/processo/agrega-saida.txt`, linhas 21:28) [F16 · lido · 90];
  - tokens Codex da rodada, pela diferença do `token_count` entre o 2º e o 3º turno: Régua 661.376 de entrada (654.976
    em cache) e 6.629 de saída; Atalho 244.547 (239.488) e 1.698 [F17 · rodado · 95];
  - Salto 0:26 e Cartógrafo 0:47, do envio ao marcador, pela coordenação (`coordM:143,145`) [F18 · lido · 95]; o Régua
    aparece ali com 2:02, contra 155 s do turno: as duas bases não batem (`coordM:141`) [F19 · lido · 90];
  - confiança no plano: Muralha 58, Régua 68, Atalho 55, Salto 55, Plantão 50, Cartógrafo 85 (a tabela `### Rodada 3` de
    cada worklog, `WT/work/worklogs/2026-11-07-reuniao-mcp-remoto-*.md`) [F20 · lido · 95]; média 61,8, mediana 56,5
    (saída do protótipo); sem o Cartógrafo, 57,2 [F21 · rodado · 95];
  - o molde da rodada 3 não tem voto (`WT/.sessions/reuniao-mcp-remoto/rodada-3.md:5-20`) [F22 · lido · 95]; o revisor
    deu 45 à v1 (`coordM:301`) [F23 · lido · 95];
  - custo da coordenação até 21:32:39, US$ 4,74, e do revisor, US$ 1,02 (`agrega-saida.txt`) [F24 · lido · 90].
- **Os worklogs das personas só chegam ao GitHub no fim:** o primeiro commit deles é o `b816b2d`, às 21:50 de 2026-11-07
  (`git log`) [F25 · rodado · 95]. Um link `https://github.com/…#rodada-3…` no painel daria 404 durante a reunião
  [F26 · inferido · 75].
- **Grok e Antigravity não gravam tokens nem custo** (`/private/tmp/wf-improv/processo/levantamento.md:190-191`)
  [F27 · lido · 85] (premissa: de segunda mão, do levantamento do processo; não procurei de novo).

### Como fica

#### 1. O modelo de dados

Um JSON por rodada, `estado-rN.json`, que o gerador monta e o render lê. A forma está em
`/private/tmp/wf-improv/desenho/estado-r3.json`.

| Campo | Fonte | Quando a fonte falta |
| :---- | :---- | :------------------- |
| `reuniao.id`, `tema`, `fim` | o `briefing.md` da reunião (cabeçalho) | obrigatório; sem ele o gerador recusa |
| `rodada.n`, `titulo`, `prazo` | a primeira linha do `rodada-N.md` ("# Rodada 3 — … (prazo: 21h40)") | sem prazo: a faixa de tempo some e ninguém vira "atrasado" |
| `rodada.aberta` | a hora do `brza sessions send` da rodada; até o R1.2 dar evento de envio, o `mtime` do `rodada-N.md` ou a hora passada pela coordenação | sem hora: "aberta —" e sem latência por marcador |
| `rodada.fechada` | o último marcador `<!-- fim-rodada-N -->` | rodada aberta |
| `rodada.tem_voto` | o molde tem bloco de voto | sem a coluna de voto |
| `persona.nome`, `papel` | `personas/<nome>.md` | obrigatório |
| `sessao`, `runtime`, `modelo`, `esforco` | o `brza sessions list --json` quando der (R1.2); hoje, o `open` do mapa (F14) e o prefixo do `chat` | "padrão" no Antigravity, que recusa modelo explícito |
| `estado` | `respondeu` pelo marcador na última linha do worklog; `falta` se não; `atrasado` se passou do prazo; `erro`/`sem cota` pelo `state` do `list` ou pelo erro do rollout | `falta` |
| `respondeu_as`, `latencia_s`, `latencia_fonte` | turno: `measurements.jsonl` (`turn.duration_s`, Claude) e `task_started/complete` do rollout (Codex); coordenação: envio → marcador (Grok, Antigravity) | marcado com "≈" quando é a base da coordenação (F19) |
| `confianca`, `confianca_r1` | a linha `**O plano inteiro**`/`Confiança` do bloco da rodada no worklog | "—" |
| `posicao` | a linha `**Posição:**` que o molde passa a pedir (≤ 100 caracteres); a coordenação sobrepõe no `sintese-N.json` | "aguardando a seção da rodada" |
| `voto` | a contagem apoio/ressalva/contra do bloco de voto | sem a etiqueta |
| `virada`, `virada_antes` | o campo "Mudou? virou" do placar; a virada anterior repete como etiqueta | sem a etiqueta |
| `custo_usd` / `tokens` | `measurements.jsonl` (`estimated_cost_usd`, Claude); `token_count` do rollout (Codex) | "sem medição" (Grok, Antigravity, F27) |
| `worklog`, `linha` | o `grep -n "### Rodada N"` no worklog | obrigatório |
| `sala.revisor` | `sintese-N.json` | "—" |
| `medicoes[]` (`tipo` medido/lido/conferido, `quem`, `texto`) | `sintese-N.json`, que a coordenação escreve | o bloco some |
| `sintese[]` (até 5) | `sintese-N.json` | o bloco some |
| `decisoes[]` (`pergunta`, `quem`, `recomendacao`, `votos?`) | `sintese-N.json` | o bloco some |
| `custos_coordenacao` | `measurements.jsonl` da sessão de coordenação e dos subagentes dela | o cartão some |

A média, a mediana, a soma de custo e a lista "sem medição" o render calcula; a coordenação não os escreve à mão.

#### 2. O layout a 736 px (o artboard)

1. **Cabeçalho:** "Reunião · <tema>", "Rodada N — <título>", "aberta 21:28 · prazo 21:40 · fechada às 21:30 · estado das
   21:32" ou "5 de 6 responderam · falta Régua"; uma faixa de tempo da abertura ao prazo, com um ponto por resposta e o
   traço do instante.
2. **Quatro cartões:** média da sala (n/6) e mediana; o revisor; o custo das personas na rodada (US$ do Claude e tokens
   do Codex); o custo da coordenação e do revisor até o instante.
3. **As personas, uma linha dupla por persona:** nome e runtime · modelo · esforço | estado (respondeu/falta/atrasado,
   a hora e a latência) | confiança em barra, com o delta contra a R1 | custo. Embaixo, a posição em uma linha e as
   etiquetas: voto, virada, e o `arquivo.md:linha` da seção (texto, não link, F8 e F26). A linha dupla foi escolhida
   porque a posição não cabe numa coluna de 270 px sem quebrar em três linhas.
4. **As medições da coordenação:** uma linha por medição, com a etiqueta medido/lido/conferido e quem mediu.
5. **A síntese:** até cinco linhas numeradas.
6. **Para Anderson decidir:** a pergunta, quem a levantou e a recomendação (e os votos, quando a rodada votou); a nota
   "as perguntas vão à rodada no chat da coordenação; o painel só mostra".
7. **Tema:** cada cor é `var(--token, var(--fb-…))`, com a reserva clara em `html` e a escura em `html.dark`, a classe
   que o shell do app alterna (`native-chat-visual-shell.ts:167`) [F28 · lido · 90]. Os tokens do Orca não são
   redefinidos em `:root`, como manda a skill (F7).
8. **Altura:** 1.595 px a 736 px; o parcial, 904 px [F29 · rodado · 95]. A 390 px, num iframe de 390 px, a seção de
   decisões começa por volta de 1.840 px e o total passa de 2.000 [F30 · rodado · 80] (premissa: medido pela captura,
   não pelo DOM; o caminho `--window-size=390` do Chrome não serve, porque a janela headless não fica abaixo de ~500 px).
   No celular, com a premissa de que o teto de 2000 px vale lá também, sobra ~200 px de rolagem interna
   [F31 · inferido · 60].

#### 3. O artboard real

`/private/tmp/wf-improv/desenho/painel-rodada.html`, 12,7 KB, gerado por `panel_proto.py estado-r3.json` [F32 · rodado · 95].
Conferido pelo PNG a 736 px (claro e escuro) e a 390 px: nenhuma coluna estourou, nenhum texto sobreposto. Corrigido
antes da devolução: a concordância "Régua e Atalho recomendam", e o `arquivo.md:linha` sumindo abaixo de 520 px.

#### 4. O ciclo de publicação

Recomendado (A1, abaixo): **um arquivo por rodada, republicado durante a rodada**. Nome `<reuniao>-rN-<hash>.html`,
fixo na rodada. A coordenação o publica na abertura (todos "falta"), a cada retorno do `wait` com resposta nova
(uma linha de texto e a diretiva: "4 de 6; falta Régua e Cartógrafo"), e no fechamento, já com medições, síntese e
decisões. A rodada seguinte ganha nome novo. No fim da reunião, um visual de síntese, nome novo, na linha do da Carvão.

Por que ele: cada mensagem nova monta o frame e mostra o estado atual (F9), e Anderson, no celular (F11), vê o
último painel no fim do chat. As menções antigas da mesma rodada convergem ao estado final quando remontam (F10), e as
das rodadas anteriores ficam como estavam. O que caiu no ataque: "republicar contraria a skill" (F7). A regra da skill
protege o histórico de visuais diferentes. Aqui a mutação fica dentro da rodada e é monotônica (só ganha respostas), e
o arquivo da rodada fechada não muda mais. O que sobreviveu: se o app passar a congelar o visual pelo nome, as menções
intermediárias ficam paradas no estado parcial, mas a última mensagem traz sempre a montagem nova. O limite de 8 por
resposta não aperta: é um visual por mensagem.

#### 5. Onde mora o gerador

Recomendado (B1): **`scripts/panel.py` da skill `meeting-runner`**, em dois estágios: `collect` (mapa, `list --json`,
worklogs, `sintese-N.json`, `measurements.jsonl`, rollouts Codex → `estado-rN.json`) e `render` (JSON → HTML, a forma
de `panel_proto.py`), mais `--at` para a prévia e o teste. O JSON é o contrato que a fase do painel (plugin ou nativo)
lê depois, sem o HTML.

Enquanto o R1.2 não entrega: o `collect` lê o estado da aba pelo `brza sessions list --json` (F12), o modelo e o
esforço pelo `open` do mapa (F14), o "respondeu" pelo marcador na última linha, e a hora de abertura que a coordenação
passa em `--opened`. Quando o `list` der latência e modelo, essas leituras saem do `collect`.

#### 6. O que a v1 não dá, e a fase do painel daria

| Falta na v1 | Por quê | Na fase do painel |
| :---------- | :------ | :---------------- |
| A argumentação integral por persona | R1.4; e a altura (F5) não comporta seis seções | seção recolhida por persona, lida do worklog |
| Abrir o chat da persona com um clique | o link só sai para http/https (F8) | `revealDashboardAgent`/`chat focus` a partir da linha |
| Botão de decisão | `submit` cancelado e sem mensagem de ação (F8) | gate (`gate-create`/`resolve`) ou cartão de pergunta |
| Atualização ao vivo | o frame não observa o arquivo (F9); só a mensagem nova atualiza | painel que ouve `agent.status.changed` e o estado da reunião |
| Link para a seção do worklog | os worklogs só chegam ao GitHub no commit (F25, F26) | abrir o arquivo local no editor do app |
| Custo do Grok e do Antigravity | os runtimes não gravam (F27) | depende do runtime, não do painel |

Um parêntese, sem reabrir o R1.4: um `<details>` por persona dentro do próprio visual custaria perto de meia hora, mas
a altura passaria do teto de 2000 px ao abrir dois ou três (F5). Fica para a fase do painel, como decidido.

### As alternativas

#### (4) O ciclo de publicação

**Decidido em R3.3 (2026-11-08): A1.**

##### A1 — Um arquivo por rodada, republicado durante a rodada (recomendada)

- **Custo:** 3 a 5 mensagens curtas da coordenação por rodada, uma diretiva cada; 0 h a mais no gerador, que é o mesmo
  [C1 · inferido · 70] · **Se paga:** na primeira reunião, porque é a única das três que dá "quem falta, em tempo real"
  (R1.4) sem código no app [C2 · inferido · 75] · **Reabre:** se o app passar a congelar o visual pelo nome (F9), as
  menções intermediárias ficam paradas; nesse caso, nome novo a cada publicação (A1') e o histórico da rodada cresce.

##### A2 — Um visual por rodada, só no fechamento, nome novo

- **Custo:** 1 mensagem por rodada; 0 h [C3 · inferido · 80] · **Se paga:** agora, mas não cobre "quem falta, em tempo
  real" (R1.4) · **Reabre:** o R1.4.

##### A3 — Um placar único da reunião, o mesmo arquivo republicado

- **Custo:** o do A1 nas mensagens, mais ~1 h no render para a trajetória persona × rodada caber em 736 px
  [C4 · inferido · 65] · **Se paga:** na primeira reunião · **Reabre:** a leitura do histórico: toda menção mostra o
  estado de agora, e o texto da coordenação "a R2 fechou com…" fica ao lado de um painel que já é da R5.

##### A4 — Os dois: placar fixo e um por rodada

- **Custo:** dois visuais por mensagem e o dobro de altura no celular; ~1 h a mais, a do A3 [C5 · inferido · 65] ·
  **Se paga:** nunca na v1; a trajetória cabe no próprio painel da rodada (o delta contra a R1 já está lá) ·
  **Reabre:** nada.

#### (5) Onde mora o gerador

**Assumido como recomendação, sem rodada: B1; e a posição em uma linha é escrita pela persona, na linha `**Posição:**` do molde, com a coordenação sobrepondo na síntese quando não serve.**

##### B1 — `scripts/panel.py` da skill `meeting-runner` (recomendada)

- **Custo:** 6 a 7 h, agora (a estimativa abaixo) [C6 · inferido · 65] · **Se paga:** na primeira reunião: a Carvão
  gastou 13,5 min da coordenação Opus `xhigh` num painel só (F3), e a MCP não gerou nenhum [C7 · inferido · 70] ·
  **Reabre:** quando o R1.2 der latência e modelo no `list`, parte do `collect` sai; quando vier a fase do painel, o
  `estado-rN.json` vira contrato.

##### B2 — Verbo do `brza sessions` (`brza sessions panel --meeting …`)

- **Custo:** as 6 a 7 h do B1, mais ~2 a 3 h de contrato, testes no `brza-workflow` e a semântica de rodada, confiança e
  molde dentro da CLI de sessões [C8 · inferido · 60] · **Se paga:** na fase do painel, se um segundo cliente (plugin,
  nativo) consumir o mesmo estado · **Reabre:** acopla a CLI ao protocolo da reunião; molde novo vira release da CLI.

##### B3 — À mão pela coordenação, como na Carvão

- **Custo:** 0 h agora; ~13 min de coordenação Opus por reunião (F3), e a qualidade varia: a MCP não fez
  [C9 · inferido · 70] · **Se paga:** nunca contra o B1 depois da primeira reunião · **Reabre:** nada.

### Estimado (B1 + A1)

| Peça | Horas | Base |
| :--- | ----: | :--- |
| `collect`: mapa, `list --json`, marcador, blocos do molde por regex, `measurements.jsonl`, rollouts Codex | 2,5 | as leituras já existem soltas: `agrega.py` (33 linhas) e as regex do levantamento do processo (F30 de lá) |
| `render`: endurecer `panel_proto.py` (188 linhas), estados `erro`/`sem cota`, voto | 1 | o protótipo desta execução |
| Testes `unittest` com o estado da R3 (fechada e às 21:29:30) e uma persona sem medição | 1,5 | dois casos já em `estado-r3.json` |
| Molde: linha `**Posição:**` nos pedidos de rodada, `sintese-N.json`, o ciclo A1 e a conferência por PNG na skill | 1 a 1,5 | três trechos de texto e um comando |
| **Total** | **6 a 6,5** | nenhuma peça foi medida; a ordem de grandeza bate com os 4 a 8 h da alternativa A do levantamento do Studio |

[C10 · inferido · 65]

### O que este desenho assume

- O painel v1 só mostra; a decisão vai à rodada no chat da coordenação (R1.3, e F8).
- A trajetória por persona é o delta contra a R1 dentro do painel da rodada, não um placar à parte (A4 descartada).
- A matriz de votos por proposta fica no visual de síntese do fim da reunião; o painel da rodada mostra a contagem
  apoio/ressalva/contra por persona (a matriz de 15 propostas da Carvão ocupa ~1.300 px dos 3.900 da captura, F4).
- O caminho do worklog vai como texto `arquivo.md:linha`; o link do GitHub, só no visual de síntese, depois do commit (F25).
- A latência mostra a base de cada número ("≈" para a da coordenação), porque as duas não batem (F19).
- A conferência por PNG usa o Chrome headless; o `brza shot` está quebrado.
- Abaixo de 520 px o `arquivo.md:linha` some; no celular o painel ainda passa de 2000 px (F30) e rola por dentro.

### O que as rodadas decidiram

R3, 2026-11-08: um arquivo por rodada, republicado na abertura, a cada resposta nova e no fechamento (A1); o painel de equipe do Orca não se religa, e a fase do painel por plugin fica registrada em issue ao `studio`. O gerador em `scripts/panel.py` e a posição escrita pela persona foram assumidos como recomendação. As perguntas, como foram feitas, ficam abaixo.

### Como foi perguntado (R3)

1. Quando o painel da rodada vai ao chat?
   1. **Um arquivo por rodada, republicado na abertura, a cada resposta nova e no fechamento (Recomendado).** Custo: 3 a
      5 mensagens curtas por rodada, 0 h a mais no gerador. Se paga: na primeira reunião; é a única que dá "quem falta,
      em tempo real".
   2. Um por rodada, só no fechamento. Custo: 1 mensagem por rodada, 0 h. Se paga: agora, mas sem o tempo real do R1.4.
   3. Um placar único da reunião, sempre o mesmo arquivo. Custo: o do 1, mais ~1 h no render. Se paga: na primeira
      reunião, perdendo o estado de cada rodada no histórico do chat.
2. Onde mora o gerador?
   1. **`scripts/panel.py` da skill `meeting-runner`, com `collect` e `render` e o JSON como contrato (Recomendado).**
      Custo: 6 a 6,5 h agora. Se paga: na primeira reunião (a Carvão gastou 13,5 min de Opus num painel só).
   2. Verbo do `brza sessions`. Custo: mais 2 a 3 h e a CLI acoplada ao molde. Se paga: na fase do painel, se outro
      cliente ler o mesmo estado.
   3. À mão pela coordenação. Custo: 0 h agora, ~13 min de Opus por reunião. Se paga: nunca, depois da primeira.
3. Quem escreve a posição em uma linha de cada persona?
   1. **A persona, numa linha `**Posição:**` do molde, e a coordenação a sobrepõe na síntese quando não serve
      (Recomendado).** Custo: uma linha a mais por persona e rodada; ~15 min no molde. Se paga: na primeira rodada; o
      painel parcial já traz a posição antes da síntese.
   2. A coordenação, na síntese. Custo: o turno da coordenação lê as seis seções antes de cada publicação; o painel
      parcial sai sem posição. Se paga: só se a linha das personas vier ruim na primeira reunião.
   3. O gerador corta a primeira frase do "erro que você vê". Custo: ~30 min de heurística. Se paga: nunca; a primeira
      frase da R3 do Régua é "*lido/inferido*, **97/100** — P, modo 2…".
4. O painel de equipe do Orca (`orchestration-crew`), pela investigação do Terreno (F81 a F83): a fonte dele é o banco
   de orquestração, os chats do `brza sessions` não apareceriam, e o upstream o desligou duas vezes em dois dias.
   1. **Não religar; seguir com o `::orca-visual` e reavaliar na fase do painel por plugin (Recomendado).** Custo: 0 h
      agora; o painel não é vivo, é republicado por rodada. Se paga: agora; revisão quando houver três ou mais reuniões e
      o artboard incomodar.
   2. Religar atrás de flag só para medir o desempenho. Custo: 1 a 3 h, e o painel sai vazio para chats do `brza
      sessions`. Se paga: nunca para a reunião; só como estudo.
   3. Religar e adaptar à reunião (grupo, estado por rodada lido de arquivo, abrir o chat). Custo: 25 a 60 h, no caminho
      que causou a regressão e numa pasta que o upstream refatora. Se paga: só se a reunião virar rotina diária e o
      plugin demorar mais de dois meses.
