# PLN-017 — Desenho: a skill (D1)

## D1 — A skill de reunião multiagente com personas — `.claude/skills/meeting-runner/`

Consultor: o papel `designer`, 2026-11-08. Marca: `[F# · tipo · confiança]` para fato, `[C# · tipo · confiança]` para custo e "se paga". Abreviações: `PROC` =
`/private/tmp/wf-improv/processo/levantamento.md`; `CHAT` = `/private/tmp/wf-improv/chat/comparacao.md`; `WF` =
`/private/tmp/wf-improv/workflow/levantamento.md`; `WT` = `/Users/andepb/Projects/brza-workspace/.worktrees/playground`.
Fato tirado de um levantamento e não refeito aqui leva a premissa "segundo o levantamento" na frase.

- **Origem:** R1.1 ("Um PLN no playground"), R1.2 ("brza sessions primeiro"), R1.3 (painel como `::orca-visual`, D3),
  R1.4 (as três faltas no chat da coordenação; "argumentação integral fica pra fase do painel"); a issue
  `work/issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md`, linha 21 ("Decidir se o fluxo vira skill").
- **Contexto:** duas reuniões em 2026-11-07 rodaram o mesmo fluxo de memória e de briefing copiado; 15 dos 32 itens que
  ele precisa ficaram implícitos, e a segunda perdeu 4 rodadas no tema errado e 2 papéis na cota do Codex.

### Levantamento que pesa no desenho

- F1: o `brza sync` só apaga caminho que está no `core.lock` ou na lista `RETIRED`; arquivo novo em `.claude/skills/`
  fora do lock sobrevive ao sync (`~/Projects/brza-workflow/bin/brza-sync:233-241`). [F1 · lido · 92]
- F2: a norma diz que o `.claude/` mora na `master` e que o workstream recebe a norma pelo merge e guarda só as notas e
  a memória (`WT/AGENTS.md:35-40`). [F2 · lido · 95]
- F3: o `README.md` define o `playground` como "onde se testam fluxos de trabalho antes de entrarem na norma ou no
  ferramental" (`WT/README.md:12-13`). [F3 · lido · 95]
- F4: o `brza note commit` aceita qualquer caminho numa branch `workstream/*`; não recusa `.claude/skills/`
  (`~/Projects/brza-workflow/bin/brza-note:688-713`). [F4 · lido · 90]
- F5: o `.sessions/` está no `.gitignore` (`WT/.gitignore:5`; `git check-ignore` rodado): briefing, pedidos de rodada,
  sínteses e propostas das duas reuniões não estão no git; a MCP copiou a proposta v3.3 para o worklog da coordenação
  (`WT/work/worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md:44,173`). [F5 · rodado · 95]
- F6: o gerador do painel da Carvão mora só no scratchpad de `/private/tmp` da sessão `4cbdb093`, tem 117 linhas e é
  fixo na reunião (lista de personas, 15 propostas e paleta escritas no código, `painel.py:9-23`). [F6 · lido · 92]
- F7: `brza quota --json` responde hoje com o uso por janela dos quatro runtimes (claude, codex, grok, antigravity).
  [F7 · rodado · 95]
- F8: o `brza sessions` tem `open/list/send/title/close`, sem `--model`, `wait` nem `read`, segundo o levantamento
  (`WF:8-10`). [F8 · lido · 88]
- F9: o `send` volta "sent" incondicional e entrega `queue-if-active`; na MCP a mensagem chegou ~12 min depois, na
  virada de turno, segundo o levantamento (`WF:14-15`; `PROC:112`). [F9 · lido · 85]
- F10: o lançador da MCP tem 21 linhas e só repassa `--model/--effort` e grava no mapa (`WT/.sessions/reuniao-mcp-remoto/launch.py:1-21`). [F10 · lido · 98]
- F11: a agregação de custo do levantamento tem 33 linhas (`/private/tmp/wf-improv/processo/agrega.py`). [F11 · rodado · 95]
- F12: a conta à mão errou: a média de "nota dos colegas" da Carvão só bate excluindo as notas da Faísca, e a MCP tem
  "18 de 18" e "24 de 24" na mesma frase, segundo o levantamento (`PROC:102,117`). [F12 · lido · 85]
- F13: o revisor ficou 11,8 abaixo da sala na Carvão (74 × 85,8) e 16,8 abaixo na MCP v1 (45 × 61,8), mas 3,25
  **acima** na MCP v3 (68 na v3.2 × 64,75 da sala na v3, versões diferentes), segundo o levantamento (`PROC:118`).
  [F13 · lido · 85]
- F14: a contraprova da Carvão: sessões novas 77,7 contra autores 85,8; Fogareiro 89 → 67 ao sair do Gemini Flash
  (High) para o Haiku `low`; personas Claude US$ 3,51, dos quais 3,07 do Fable, segundo o levantamento
  (`PROC:160,163,178`). [F14 · lido · 85]
- F15: o turno `resume` da coordenação Carvão, de 802 s, custou US$ 6,28 (`PROC:171`); a janela da contraprova foi de
  20:43:24 a 20:56:47 (`CHAT:21`), ~13,4 min. A premissa é que o turno de 802 s é a contraprova inteira, o que dá à
  contraprova ~US$ 9,8 em Claude, não 3,5. [F15 · lido · 80]
- F16: a coordenação pesou 62% (Carvão, Opus `xhigh`, US$ 22,67) e 57% (MCP, Opus `high`, US$ 6,03) do custo Claude da
  reunião, segundo o levantamento (`PROC:182`). [F16 · lido · 85]
- F17: o Antigravity foi o mais confiante e o de pior nota dos colegas nas duas, num papel de usuário (Fogareiro, 6,6) e
  num técnico (Cartógrafo, 6,0); o chat dele recusa modelo explícito, segundo o levantamento (`PROC:104,108`).
  [F17 · lido · 85]
- F18: a Carvão nomeou personas em 11 de 57 blocos de chat; a MCP em 4 de 47, e duas personas nunca apareceram; o
  intervalo sem texto não distingue as duas (7m43 contra 3m34), segundo a comparação (`CHAT:42,64`). [F18 · lido · 88]
- F19: a memória `consultant-debate-shown-in-full` manda pôr a argumentação completa de cada consultor no chat antes da
  pergunta (`WT/memory/consultant-debate-shown-in-full.md:8`); a R1.4 tira a argumentação integral das personas do chat
  da coordenação na v1. As duas regras colidem na rodada final de decisão. [F19 · lido · 90]
- F20: a coordenação ficou ociosa sem texto até 7m43 durante rodadas (`CHAT:17`), e a regra de status nomeado custa só
  uma linha por chegada. [F20 · lido · 88]
- F21: as personas Claude rodam no mesmo checkout do `playground` e veriam a skill na lista delas; a descrição que fala
  em "reunião multiagente" pode acioná-la numa persona cujo prompt começa com "Você é uma persona numa reunião
  multiagente" (`WT/.sessions/reuniao-mcp-remoto/prompt-regua.txt:1`). [F21 · inferido · 70]
- F22: tamanho da forma de referência: o `plan-runner` tem 762 linhas (SKILL.md 211 + 4 references), o `close-task` 70;
  o material das duas reuniões (briefings, pedidos, sínteses) soma 977 linhas. [F22 · rodado · 95]

### As alternativas

#### (a) Onde a skill nasce

**Decidido em R2.1 (2026-11-08): A1.**

##### A1 — Protótipo em `.claude/skills/meeting-runner/` na branch `workstream/playground` (Recomendada)

- **Custo:** foge da regra "o `.claude/` mora na `master`" (F2), declarado no PLN como desvio de norma; a skill só
  existe no worktree do `playground`, e reunião em outro workstream copia ou espera a promoção. A promoção ao `core/`
  custa uma rodada de sync depois. [C1 · inferido · 70]
- **Se paga:** agora: as duas reuniões rodaram no `playground` (F3), a execução fica dentro deste PLN sem issue a outro
  workstream (R1.1), e cada correção depois de uma reunião é um commit de nota, sem `brza sync`. [C2 · inferido · 70]
- **Reabre:** quando uma reunião precisar rodar fora do `playground`, ou depois de duas reuniões sem desvio de fluxo
  (o critério de promoção).

##### A2 — Na `master` do `brza-workspace`, fora do `core.lock`, como norma local

- **Custo:** cada ajuste vai à `master` por sessão do workstream `workspace` (issue daqui) e chega aos worktrees pelo
  `brza note sync`; o v1 vai mudar depois de cada reunião, e cada mudança vira esse ciclo. [C3 · inferido · 65]
- **Se paga:** quando uma segunda frente (o `brand`, o `tools-kit`) pedir reunião antes da promoção ao `core/`.
  [C4 · inferido · 60]
- **Reabre:** a regra "o que é só deste workspace vai à `.claude/rules/workspace.md` ou ao `README.md`"
  (`WT/AGENTS.md:64-65`), que não lista skill local.

##### A3 — Direto no `core/` do `brza-workflow`, por sessão do workstream `workspace`

- **Custo:** cada correção do v1 é commit no `brza-workflow` + `brza sync` + `brza note sync`; a skill chega a todo
  workspace que sincroniza o núcleo, com dependências do pacote `client` e dos quatro runtimes que nem todo workspace
  tem. [C5 · inferido · 65]
- **Se paga:** só depois de o fluxo estabilizar; antes, nunca. [C6 · inferido · 65]
- **Reabre:** a fronteira núcleo × local (o que o `core.lock` segue).

##### A4 — Guia em `wiki/guides/`, sem skill

- **Custo:** sem gatilho por descrição e sem scripts; a agregação segue à mão, com os erros de F12. ~3 h de escrita.
  [C7 · inferido · 60]
- **Se paga:** nunca para o lançador e para a agregação; serve só como texto de leitura. [C8 · inferido · 65]
- **Reabre:** a decisão da issue (linha 21).

**O que sobreviveu ao ataque (A1):** o `playground` existe para isto (F3), o sync não apaga a pasta (F1), e o laço
"reunião → correção" fica sem ciclo de sync. **O que caiu:** "a skill no `playground` não atrapalha ninguém" — as
personas Claude do mesmo checkout a veem (F21); vale para A1, A2 e A3, e se resolve na descrição ("não use se você é
uma persona da reunião") e no prompt de abertura da persona.

#### (b) O escopo da v1

**Decidido em R2.2 (2026-11-08): B1.**

##### B1 — SKILL.md + references + três scripts (Recomendada)

`launch_persona.py` (do `launch.py`, sobre um manifesto), `wait_round.py` (marcador + `state` do `list`) e `tally.py`
(lê as tabelas dos worklogs e a medição, e grava o `estado-rN.json` que a tabela do chat e o painel do D3 consomem). O
gerador do painel é do D3; a skill só o chama com o JSON.

- **Custo:** ~10,5 h (o "Estimado" abaixo); `launch_persona.py` e `wait_round.py` (~1,25 h) morrem quando o CLI ganhar
  `--model` e `wait`. [C9 · inferido · 60]
- **Se paga:** na 1ª reunião pela skill: o `tally.py` substitui a conta à mão que errou (F12) e é a fonte da tabela por
  persona que a R1.4 pede em toda rodada. [C10 · inferido · 70]
- **Reabre:** quando o CLI chegar (R1.2), os dois scripts saem e a skill troca a linha "v1" pela "v2".

##### B2 — SKILL.md + references, sem scripts

- **Custo:** ~6 h; a coordenação reescreve o lançador a cada reunião e soma as tabelas à mão, e a tabela por persona a
  cada rodada (R1.4) vira trabalho manual de ~6 personas × N rodadas. [C11 · inferido · 60]
- **Se paga:** só se o CLI chegar antes da próxima reunião. [C12 · inferido · 60]
- **Reabre:** B1 na primeira reunião que errar a conta.

##### B3 — SKILL.md mínimo (o protocolo em uma página)

- **Custo:** ~2 h; os moldes continuam a ser copiados da reunião anterior, que é o que deixou 15 itens implícitos.
  [C13 · inferido · 60]
- **Se paga:** nunca: repete a forma das duas reuniões, que é o problema. [C14 · inferido · 65]
- **Reabre:** tudo.

**Sobreviveu (B1):** o `tally.py` não morre com o CLI — o CLI não vai ler tabela de worklog de persona —, e é ele que
sustenta a regra de narração. **Caiu:** "o gerador do painel entra na v1 da skill" — o da Carvão é fixo na reunião
(F6), e o desenho dele é do D3; a skill fixa o contrato de dados (`estado-rN.json`), não o painel.

#### (c) O número de confiança do plano

**Decidido em R2.3 (2026-11-08): C-1.**

##### C-1 — O do revisor independente é "a confiança do plano"; a sala vai ao lado, com média, mediana, n e a faixa (Recomendada)

- **Custo:** um revisor por versão revisada, US$ 2,4–3,8 por reunião, segundo o levantamento (`PROC:172,175`).
  [C15 · lido · 85]
- **Se paga:** na primeira reunião: o revisor achou nas duas o que mudou o desenho (`PROC:118`). [C16 · inferido · 75]
- **Reabre:** se o revisor ficar acima da sala de novo (já aconteceu uma vez, F13): aí o número é um só modelo, e a
  contraprova (d) é a segunda amostra.

##### C-2 — A média da sala

- **Custo:** zero de US$; superestima 12–17 pontos em duas de três medições (F13). [C17 · lido · 85]
- **Se paga:** nunca para decisão de Anderson. [C18 · inferido · 70]
- **Reabre:** —

##### C-3 — Os dois, com a regra de desconto medida (sala − 12 a 17)

- **Custo:** a regra nasce de 3 pontos, e o sinal já virou no terceiro (+3,25, F13); um desconto fixo esconderia isso.
  [C19 · lido · 85]
- **Se paga:** depois de ~5 reuniões com revisor, se a diferença ficar estável. [C20 · inferido · 55]
- **Reabre:** a cada reunião.

**Sobreviveu (C-1):** o número de quem não escreveu o plano é o que achou erro nas duas. **Caiu:** "o revisor fica
sempre abaixo" — na MCP v3.2 ficou acima, e a comparação mistura versões; por isso nenhum desconto vira regra, e a
skill registra a diferença sala × revisor em toda reunião para medir.

#### (d) A contraprova

**Decidido em R2.3 (2026-11-08): D-1.**

##### D-1 — Opcional, com gatilho, em modelos baratos (Recomendada)

Gatilho: a proposta vai a aprovação **e** (a decisão é cara de reverter **ou** sala e revisor divergem mais de 10
pontos). Formato: R1 às cegas + confiança na proposta; Haiku `low`, Sonnet `medium`, Grok Fast `low`, Codex Terra
`medium`; sem Fable.

- **Custo:** ~US$ 1 nas personas Claude (Haiku 0,03 + Sonnet 0,41, F14) mais a coordenação, que na Carvão pagou ~US$
  6,28 pelo turno da contraprova (F15); ~13 min. [C21 · inferido · 70]
- **Se paga:** quando o gatilho vale; foi a contraprova que mostrou que a confiança é do modelo (F14). [C22 · inferido · 70]
- **Reabre:** quando o (e) já tira o Antigravity da média, o achado principal dela vira regra, e o gatilho pode
  apertar.

##### D-2 — Sempre

- **Custo:** ~US$ 10 em Claude e ~13 min por reunião, se repetir a da Carvão (F15). [C23 · inferido · 70]
- **Se paga:** só em decisão cara de reverter. [C24 · inferido · 65]
- **Reabre:** —

##### D-3 — Nunca; o revisor basta

- **Custo:** perde a segunda amostra independente quando o revisor discorda da sala. [C25 · inferido · 65]
- **Se paga:** se o revisor ficar estável abaixo da sala; hoje não está (F13). [C26 · inferido · 65]
- **Reabre:** a primeira reunião em que sala e revisor divergirem sem explicação.

**Caiu:** "a contraprova custa US$ 3,5" — o custo das personas é a parte pequena; a coordenação que a conduz custou
quase o dobro (F15).

#### (e) O Antigravity

**Assumido como recomendação, sem rodada: E-1.**

##### E-1 — No máximo uma cadeira, em papel de ideação ou de usuário; a confiança dele sai da média e do número do plano, relatada à parte; o número que ele trouxer passa pela conferência antes da síntese (Recomendada)

- **Custo:** um parágrafo na skill e uma coluna a mais no `tally.py`. [C27 · inferido · 75]
- **Se paga:** agora: o viés apareceu nas duas reuniões (F17). [C28 · inferido · 75]
- **Reabre:** quando o chat aceitar modelo explícito (F17) e uma contraprova mostrar outro modelo calibrado.

##### E-2 — Fora da reunião (a cadeira vai a Haiku `low`)

- **Custo:** perde o quarto runtime, a busca na web do Cartógrafo (`coordM:53`) e a redundância de runtime contra
  queda de cota. [C29 · inferido · 70]
- **Se paga:** se a diversidade de runtime deixar de ser objetivo (`memory/meeting-model-per-role.md:11-12` diz o
  contrário). [C30 · inferido · 70]
- **Reabre:** a memória de diversificar.

##### E-3 — Livre

- **Custo:** o viés entra na média (83,8 → 88 na MCP). [C31 · lido · 85]
- **Se paga:** nunca. [C32 · inferido · 75]
- **Reabre:** —

**Caiu:** "restringir ao papel de usuário corrige" — na Carvão ele já estava no papel de usuário e trouxe o único número
errado (F17). O que corrige é tirar a confiança dele da conta, não mudar o papel.

### Como fica

#### `SKILL.md` — esqueleto (H2 e as regras, uma linha cada)

```markdown
---
name: meeting-runner
description: >-
  Use na sessão que COORDENA uma reunião multiagente com personas — "monte uma reunião sobre X", "reunião com
  personas", "replique a reunião" —: N chats do BrzA Studio em runtimes e modelos diversos, conduzidos pelo
  `brza sessions`, com rodadas, síntese, revisor e a rodada de decisões para Anderson. Não use se você é uma persona
  da reunião (o seu prompt diz "você é uma persona"), nem para consultores em paralelo por `Agent`.
---
# Reunião multiagente — preparar, conduzir, sintetizar e fechar

### Quando usar e quem é quem
- A coordenação é a sessão principal: pergunta, sintetiza, grava; as personas escrevem só no worklog delas.
- Consultor em paralelo por `Agent` não é reunião: é o laço consultor do `plan-runner`.
- A norma de rodadas é a do `AGENTS.md`; a skill não a repete.

### Passo 0 — o gate do tema (antes de qualquer arquivo)
- Rodada com Anderson: o objeto em uma frase, o que está fora, a saída esperada, a hora fim; a leitura da coordenação vai como primeira opção.
- A resposta literal vai ao topo do briefing; sem resposta, nenhuma sessão abre.
- Correção de tema no meio: a rodada em curso fecha, o material fora do tema é descartado por escrito na síntese.

### Passo 1 — preparar
- Levantamento longo vai ao `collector`, em paralelo à preparação; a R1 não espera por ele.
- Briefing pelo molde (`references/briefing.md`); restrição do tema (segurança da sala) é um slot, não improviso.
- Personas pelo molde (`references/persona.md`): arquétipo, runtime · modelo · esforço, valores, fala, decisão, vícios, "na sala".
- Modelo e esforço pelo papel, nunca dois papéis no mesmo modelo e esforço (memória `meeting-model-per-role`).
- O manifesto `reuniao.json` (nome, papel, runtime, modelo, esforço, fallback) é a fonte do lançamento e das tabelas.
- Orçamento de cota: `brza quota --json` antes de abrir; runtime acima de 55% na janela de sessão não hospeda papel crítico.
- Redundância: o medidor/cético e o de segurança ficam em dois runtimes diferentes; cada persona tem `fallback` no manifesto.
- Esqueleto do worklog de cada persona pelo molde, criado pela coordenação antes de abrir a sessão.

### Passo 2 — abrir as sessões
- v1: `launch_persona.py reuniao.json`; v2: `brza sessions open --model --effort` (ou o verbo de manifesto).
- Prompt de abertura de uma linha por persona, guardado em `prompt-<persona>.txt`.
- Antigravity sem modelo explícito; Codex `exec` com `< /dev/null`.
- A coordenação narra a abertura (ver "A narração").

### Passo 3 — conduzir uma rodada
- O pedido de rodada sai do molde (`references/round-request.md`), com duração ("~5 min"), não hora.
- Envio: uma linha que aponta o arquivo da rodada; só para persona com `state` fora de `working` (a fila entrega na virada do turno, ~12 min).
- Sinal de fim: só o marcador; regra única "acrescente no fim; a última linha é `<!-- fim-rodada-N -->`".
- v1: `wait_round.py N`; v2: `brza sessions wait --marker`.
- Rodada-tipo: R1 independente; R2 debate (disputas D#, ataque, concessão, placar com "Mudou?"); R3 voto e notas; última: confiança final e autoavaliação.
- Isolamento da R1: o pedido proíbe ler os worklogs dos colegas; a coordenação confere por `grep` do nome das outras personas na R1 de cada uma.

### Passo 4 — o atrasado e a queda de runtime
- Timeout da rodada: 2× a mediana das que entregaram, no mínimo 3 min; a síntese fecha sem quem falta e o diz.
- O atrasado entra pela rodada anterior, rotulado, e pode juntar duas rodadas numa só seção.
- Duas rodadas perdidas ou erro de cota: a persona reabre no `fallback` do manifesto, com o worklog dela como contexto.

### Passo 5 — sintetizar
- `tally.py N` antes de escrever: o `estado-rN.json` traz status, posição, confiança, voto, nota e medição por persona.
- A síntese segue o molde (`references/synthesis.md`): convergências C#, fatos medidos M#, disputas D#, propostas P#.
- A coordenação confere os números das personas por comando e mede o que a sala não mediu.
- Disputa técnica ou visual: prova de conceito ou evidência renderizada antes do voto; nada exposto sem auth; derruba o que subir.

### Passo 6 — a proposta, o revisor e a contraprova
- Proposta pelo molde (`references/proposal.md`): origem (R#, revisor, contraprova) e evidência (`[medido]`, `[lido]`, `[inferido]`) em cada linha; "não aprovada".
- Revisor independente (`reviewer`) em toda versão que vai a Anderson, com as cinco conferências da memória do revisor.
- Confiança do plano: o número do revisor independente (R2.3); a sala ao lado, com média, mediana, n e faixa; o Antigravity à parte; a diferença sala × revisor registrada.
- Contraprova (R2.3): só quando a proposta vai a aprovação e é cara de reverter, ou sala e revisor divergem mais de 10 pontos; modelos baratos, sem Fable.

### Passo 7 — fechar
- Rodada de decisões para Anderson pelo molde (`references/closing.md`), em texto, com o texto da proposta à vista; por opção, o voto de cada persona e o argumento mais forte a favor e contra, uma linha cada, com o link do worklog (R2.4).
- Issues para o que sobra; worklog da coordenação com a proposta copiada (o `.sessions/` não vai ao git).
- Memória de runtime fora do repositório: `find` nos diretórios do script de encerramento (Grok `~/.grok/memory-v2/`), para `## Fora do workspace`.
- `brza sessions close` de cada persona; `brza note commit` dos worklogs e issues.

### A narração no chat da coordenação
- A tabela da seção "A narração" da reference `references/narration.md` (ver abaixo); cada fechamento de rodada sai do `estado-rN.json`.

### v1 e v2
- Tabela passo × comando de hoje × verbo do CLI que vem (R1.2).

### Invariantes
- A persona nunca pergunta, nunca commita, só escreve no worklog dela.
- A coordenação não decide: a rodada de Anderson decide; decisão só com a frase explícita.
- Nenhum número entra no chat sem a fonte (`tally.py`, comando, worklog).

### Arquivos
- Tabela reference × quando ler.
```

#### `references/`

| Arquivo | O que fixa | Base |
| :-- | :-- | :-- |
| `briefing.md` | objetivo com a resposta literal do gate, estado atual com fonte, alternativas de partida, pauta numerada, restrições do tema, regras da sala (incluindo a régua 0–100, *medido/lido/suposto*, o marcador, "não grave memória do runtime") | `WT/.sessions/reuniao-mcp-remoto/briefing.md` |
| `persona.md` | o molde e a tabela papel → runtime · modelo · esforço | `personas/atalho.md`; memória `meeting-model-per-role` |
| `persona-worklog.md` | o esqueleto: frontmatter, H1 "Reunião X: a participação de …", "Este é o registro de…", `## O que se fez`; sem `## O que ficou` (ficou vazio nas seis da Carvão, `PROC:82`) | worklogs das personas |
| `round-request.md` | o molde comum e os quatro tipos (R1 independente, debate, voto e notas, confiança final e autoavaliação), com o limite de linhas | `rodada-1..3.md` das duas |
| `synthesis.md` | C#, M#, D# com opções, P#, a tabela por persona do `estado-rN.json`, "quem ficou fora" | `reuniao-brasa/sintese-2.md` |
| `proposal.md` | proposta com origem e evidência, a confiança do plano pela regra (c), "Para Anderson decidir" | `proposta-v2.1.md`, `plano-proposta.md` |
| `closing.md` | a rodada de decisão em texto, o worklog da coordenação (tabela de rodadas, de modelos, de medição), o encerramento e a verificação de memória | worklogs da coordenação |
| `narration.md` | as regras de narração (abaixo) com um exemplo literal bom de cada | `CHAT` |

**A régua da confiança 0–100** (no briefing): 90 ou mais, medido por comando ou lido na fonte nesta reunião; 70 a 89,
lido com a premissa escrita; 50 a 69, inferência plausível sem fonte; abaixo de 50, palpite ou contra. É a mesma faixa
da marca de fato do `designer` e do `collector`, para que a auditoria futura compare. **Sem lastro**: nenhuma reunião
mediu se a régua muda a calibração. [F23 · inferido · 60]

**O voto:** `apoio`, `apoio com ressalva`, `contra`, por proposta P#, com a ressalva em uma linha e a confiança.
**A nota aos colegas:** tabela "Persona | contribuição mais útil em uma linha | nota 0–10", as outras N−1.
**A autoavaliação:** até três linhas, em que foi fiel à persona e em que saiu dela.

#### `scripts/`

| Script | O que faz | Morre quando |
| :-- | :-- | :-- |
| `launch_persona.py <reuniao.json> [persona]` | o `launch.py` generalizado: lê o manifesto, repassa `--model/--effort`, grava no mapa, guarda o `prompt-<persona>.txt` | o `brza sessions open --model --effort` (R1.2) |
| `wait_round.py <N> [--timeout]` | espera a última linha `<!-- fim-rodada-N -->` em cada worklog e o `state` fora de `working`; imprime quem chegou, quem falta e há quanto tempo, em uma linha por chegada | o `brza sessions wait` |
| `tally.py <N>` | extrai as tabelas (placar, voto, confiança do plano, notas) dos worklogs, junta `measurements.jsonl` (Claude) e o `token_count` dos rollouts do Codex, marca Grok e Antigravity "sem medição", grava `.sessions/<reuniao>/estado-rN.json` e imprime a tabela Markdown do chat | não morre; a parte de custo passa a chamar o `brza sessions usage` quando existir |
| `runtime_memory_check.py <início>` | lista arquivos novos nas memórias de runtime fora do repositório | não morre |

Teste de aceite do `tally.py`: refazer, a partir dos worklogs de 2026-11-07, as tabelas por persona de `PROC:126-150`
(que já conferiram com as da coordenação, salvo F12).

#### As regras de narração (`references/narration.md`)

| Quando | O quê | Forma | Fonte |
| :-- | :-- | :-- | :-- |
| As sessões abrem | quem é quem | tabela "Persona · papel · runtime · modelo · esforço" em uma mensagem | P1; Carvão 20:01:02 |
| Cada chegada de marcador | quem respondeu e quem falta, com o tempo da mais lenta | uma linha: "R2 · 4/6 — entregaram Lenha, Cinza, Tição, Fole; faltam Faísca (Grok, 5 min) e Fogareiro" | R1.4 (2); P1 |
| Rodada aberta sem chegada há 3 min | o mesmo status, com o que a coordenação está fazendo | uma linha | F20 |
| Rodada fecha | a posição e a confiança de cada persona | tabela "Persona · posição em uma linha · confiança · mudou? · voto", do `estado-rN.json`; abaixo, número da sala (média, mediana, n), revisor quando houver, as viradas nomeadas | R1.4 (1); P2 |
| Rodada fecha | os números conferidos | lista curta "confere / diverge: <afirmação> — <comando ou fonte> → <resultado>" | R1.4 (3) |
| Rodada fecha | o painel | o `::orca-visual` do D3, conferido por PNG, depois da tabela; o texto não depende dele | R1.3; P4 |
| Prova da coordenação | o resultado que muda a sala | no máximo duas linhas; o erro de shell da própria coordenação não vai ao chat | P6 |
| Fechamento | o registro | o worklog da coordenação em `<details>` (tabela de rodadas aberta/fechada/produziu, de modelos, de medição por persona); os worklogs das personas por link, não por inteiro | P3; R1.4 ("argumentação integral fica pra fase do painel") |
| Rodada de decisão | as decisões de Anderson | em texto, abaixo da proposta inteira, opções desenhadas (artboard quando visual), `Custo: … Se paga: …`, o voto das personas por opção | P5; `WT/AGENTS.md:191` |

O que não vai ao chat da coordenação na v1: a argumentação integral das personas (R1.4); ela fica no worklog e, no D3,
no painel.

#### v1 × v2

| Passo | v1 (hoje) | v2 (os verbos de R1.2) |
| :-- | :-- | :-- |
| Abrir com modelo | `launch_persona.py` | `brza sessions open --model --effort` |
| Enviar a N | laço de `brza sessions send`, depois do `wait` | `send` a N com recibo |
| Esperar | `wait_round.py` | `brza sessions wait` |
| Ler | o worklog; o chat, só abrindo a aba | `brza sessions read` para a persona travada |
| Trocar modelo | fechar e reabrir no `fallback` | `brza sessions model` |
| Medir | `tally.py` (Claude + Codex) | `tally.py` sobre o `usage` |
| Fechar | laço de `brza sessions close` | o mesmo |

### Estimado

~10,5 h na alternativa recomendada (A1 + B1), sem o painel (D3) e sem o CLI (issue ao `tools-kit`):
SKILL.md 2 h; oito references 2,5 h, adaptadas das 977 linhas de material (F22); `launch_persona.py` 0,5 h (de 21
linhas, F10); `wait_round.py` 0,75 h; `tally.py` 2 h (de 33 linhas de agregação, F11, mais a extração por regex que o
levantamento já rodou); o teste de aceite do `tally.py` 1 h; uma reunião curta de verificação (3 personas, 2 rodadas)
1,25 h e ~US$ 5; a revisão 0,5 h e ~US$ 3. [C33 · inferido · 60] Base: o tamanho da forma (F22) e dos scripts que já
existem; nenhuma escrita de skill deste workspace tem duração medida.

### Revisão pela R5 e R6: a abertura, o sinal de fim e o encerramento (2026-11-08)

O requisito da R5 e a via da R6 mudam três passos do esqueleto acima e dois scripts; o resto fica.

- **Passo 2, abrir as sessões:** cada persona abre com o ciclo de vida dos workers do Orca, pela via que a sonda P4a.0 do plano decidir (a híbrida: `agent launch --surface chat` e `worker-start --terminal orca_session_id:<chat>`; ou a via A: `worker-start --spec --agent --model --effort --worktree path:`). O `launch_persona.py` v1 implementa a via e grava `dispatch_id` e `orca_session_id` no mapa, além de modelo e esforço; quando o `brza sessions open` ganhar a via (D2, P4a), o script sai. O prompt da persona chega depois do preâmbulo do Orca, como turno do coordenador: o briefing diz à persona que o `worker_done` que o preâmbulo pede é o do encerramento, não o de cada rodada.
- **Passo 3, o sinal de fim de rodada (R6.2):** ao fechar a seção da rodada no worklog, a persona roda `brza orchestration send --to <coordenação> "fim-rodada-N"`; a coordenação espera por `brza orchestration check --wait --types message` (v1: `wait_round.py` embrulha o `check --wait` e imprime quem chegou e quem falta, em uma linha por chegada; v2: `brza sessions wait`). O marcador `<!-- fim-rodada-N -->` na última linha do worklog continua, como registro escrito que o `tally.py` lê, não como sinal.
- **Passo 7, fechar:** a mensagem de encerramento da coordenação diz "a reunião acabou; envie `worker_done`"; o host arma os 2 min e o botão "manter aberta" aparece no chat de cada persona, para Anderson guardar a que quiser consultar; quem não responder é liberado por `brza orchestration worker-release`. O `brza sessions close` de cada persona sai do passo. A contraprova e a "rodada a mais se as decisões pedirem" acontecem antes do encerramento, ou reabrem a persona pelo `fallback`.
- **A narração:** a linha de status por chegada sai do `check --wait`, não do `grep`; o resto da tabela de narração vale igual.
- **O que a persona precisa poder fazer:** rodar dois comandos de shell (`brza orchestration send` por rodada e `worker_done` no fim); as personas das duas reuniões escreveram arquivos, logo têm shell. O briefing traz os dois comandos prontos, com o destinatário preenchido.
- **Assumido sem rodada:** a sonda roda antes da primeira reunião pela skill (P4a.0 antes de P7); até lá, o `launch_persona.py` aceita `--via agent-launch` para abrir como hoje, sem ciclo de vida, só para testar o resto da skill.

### O que as rodadas decidiram

R2, 2026-11-08: A1 (protótipo na branch do `playground`), B1 (`SKILL.md`, oito references e quatro scripts), C-1 (o revisor como número), D-1 (contraprova por gatilho) e, na rodada final de decisão, o voto e o argumento mais forte a favor e contra por persona. **R5 e R6, 2026-11-08:** as personas abrem com o ciclo de vida dos workers do Orca; o fim de rodada é `brza orchestration send` da persona; o `worker_done` só no encerramento (seção "Revisão pela R5 e R6"). As perguntas, como foram feitas, ficam abaixo; o texto das respostas está na Entrevista do plano.

### Como foi perguntado (R2)

**1. Onde a skill nasce?**
1. **(Recomendado)** Protótipo em `.claude/skills/meeting-runner/` na branch do `playground`, promovido ao `core/` depois
   de duas reuniões sem desvio de fluxo. Custo: um desvio de norma declarado (o `.claude/` mora na `master`) e uma
   rodada de sync na promoção. Se paga: agora; correção depois de cada reunião é commit de nota.
2. Na `master`, fora do `core.lock`. Custo: cada ajuste por issue ao `workspace` e `brza note sync`. Se paga: quando
   outra frente pedir reunião antes da promoção.
3. Direto no `core/` do `brza-workflow`. Custo: cada correção do v1 é um ciclo de sync em todo workspace. Se paga: só
   depois de estabilizar.
4. Guia em `wiki/guides/`. Custo: sem scripts e sem gatilho; a conta à mão continua. Se paga: nunca para a agregação.

**2. O escopo da v1?**
1. **(Recomendado)** SKILL.md, oito references e quatro scripts (`launch_persona`, `wait_round`, `tally`,
   `runtime_memory_check`); o painel é do D3. Custo: ~10,5 h; ~1,25 h morrem com o CLI. Se paga: na 1ª reunião pela
   skill, pela tabela por persona a cada rodada (R1.4) sem conta à mão.
2. SKILL.md e references, sem scripts. Custo: ~6 h; a tabela por rodada fica manual. Se paga: só se o CLI chegar antes
   da próxima reunião.
3. SKILL.md mínimo. Custo: ~2 h. Se paga: nunca; repete os implícitos.

**3. Que número é "a confiança do plano"?**
1. **(Recomendado)** O do revisor independente; a sala ao lado (média, mediana, n, faixa), o Antigravity à parte, e a
   diferença sala × revisor registrada para medir. Custo: US$ 2,4–3,8 de revisor por reunião. Se paga: na primeira, pelo
   erro que ele acha.
2. A média da sala. Custo: zero; superestima em duas de três medições. Se paga: nunca para decisão.
3. Os dois, com desconto fixo de 12–17. Custo: regra de três pontos, com o sinal já virado num deles. Se paga: depois de
   ~5 reuniões, se a diferença estabilizar.

**4. A contraprova?**
1. **(Recomendado)** Opcional, com gatilho (vai a aprovação e é cara de reverter, ou sala e revisor divergem mais de
   10), em modelos baratos, sem Fable. Custo: ~US$ 1 nas personas mais ~US$ 6 de coordenação e ~13 min quando
   dispara. Se paga: quando o gatilho vale.
2. Sempre. Custo: ~US$ 10 e ~13 min por reunião. Se paga: só em decisão cara de reverter.
3. Nunca. Custo: perde a segunda amostra quando o revisor discorda da sala. Se paga: se o revisor ficar estável.

**5. Na rodada final de decisão, quanto da argumentação das personas vai ao chat?** (a memória
`consultant-debate-shown-in-full` pede tudo; a R1.4 tira a argumentação integral do chat na v1)
1. **(Recomendado)** Por opção: o voto de cada persona e o argumento mais forte a favor e contra, uma linha cada, com o
   nome e o link do worklog; o integral fica no worklog e, depois, no painel. Custo: a regra da memória fica suspensa
   na reunião, por escrito na skill. Se paga: agora; a rodada cabe numa tela.
2. A argumentação completa, como a memória manda. Custo: a rodada de 6 personas × 4 decisões passa de várias telas, o
   que a R1.4 recusou. Se paga: quando a decisão é uma só e disputada.
3. Só o placar dos votos. Custo: Anderson volta aos chats das filhas para ver o porquê, que foi a queixa da MCP. Se
   paga: nunca.

### O que este desenho assume (decidido como recomendação, sem rodada)

- O Antigravity pela E-1 (uma cadeira, confiança fora da conta). Fonte: F17.
- O gate do tema é Passo 0 obrigatório. Fonte: `PROC:114`.
- O prazo de rodada é duração, e o sinal de fim é só o marcador. Fonte: `PROC:84`.
- O envio da rodada seguinte espera o `state` fora de `working`. Fonte: F9.
- A proposta final é copiada para o worklog da coordenação, porque o `.sessions/` não vai ao git. Fonte: F5.
- A coordenação roda em Opus `high`, não `xhigh`: a da Carvão (`xhigh`) custou 3,8 vezes a da MCP (`high`), mas a
  reunião foi mais longa e escreveu o painel, e a parte do esforço não está isolada (F16). [F24 · inferido · 55]
- O corte de 55% da janela de sessão para papel crítico é o `soft` do orquestrador (`WF:33`), não medido em reunião.
  [F25 · lido · 80]
- O timeout de 2× a mediana, mínimo 3 min, é chute; a Carvão teve o Grok a 4–7 min contra 1–2 min dos outros
  (`PROC:101`). [F26 · inferido · 55]
- A régua 0–100 copia a faixa da marca de fato (F23).

### Os desvios da reunião de verificação (P7, 2026-11-09)

A primeira reunião pela skill, contra o Studio real, teve três personas (Claude, Grok e Antigravity) pela via
`worker-start`. Ela rodou do gate ao encerramento, mas teve 19 desvios e **não conta** para as duas reuniões sem desvio do
critério de promoção. A lista inteira, com a hora de cada um, está em
[Reunião CI no chat: a coordenação da reunião de verificação do PLN-017](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-coordenacao.md).
Os que pedem mudança na skill antes da próxima reunião:

| X | Onde | O desvio | A correção que ele pede |
| :-- | :-- | :-- | :-- |
| X19 | `briefing.md`, `launch_persona.py` (molde), SKILL.md Passo 7 | o `worker_done` sem `--task-id`/`--dispatch-id` é rejeitado ("worker_done requires taskId") | o prompt de abertura leva os ids do recibo, ou o briefing manda copiar os do preâmbulo do Orca |
| X1 | `launch_persona.py`, `tally.py` | o recibo do `worker-start` não traz a sessão do provedor; o Claude fica "sem medição" | achar o transcript pelo prompt da persona, ou esperar o `brza sessions open` da v2 |
| X10 | Passo 3, rodadas-tipo | o fato decisivo de uma persona chegou na última rodada; as outras votaram sem ele | R8.1, opção 2: sintetizar os fatos anteriores antes do voto; se um fato novo da própria rodada de voto contradizer a premissa de algum voto, compartilhar o fato e executar automaticamente rodada extra de voto informado. R9.1, opção 3: a coordenação escolhe participantes caso a caso e registra o motivo antes do disparo, sem composição fixa. Sem gatilho, nenhuma rodada adicional. Decisão final continua com Anderson; 3–5 min são estimativa e custo financeiro não foi medido |
| X8 | Passo 1, `briefing.md` | o "O que existe hoje" do briefing levou um número errado (1.352 em vez de 163), e duas personas o herdaram | conferir os números do briefing por comando antes de abrir |
| X12, X18 | `panel.py` | `decisoes[].quem` sai como "recomendam"; a rodada para parte da sala não fecha e esconde a síntese | renomear o rótulo; aceitar o subconjunto de personas na rodada |
| X17 | `round-request.md` | o molde da rodada extra foi improvisado e o `tally.py` não leu o voto | um tipo "rodada extra" no molde |
| X3, X9 | `narration.md`, `launch_persona.py --send` | a escalação "Worker stopped without reporting" a cada rodada e o "Re: rodada" | dizer que se ignoram; enviar com `--type status` e outro assunto |
| X5, X6, X4, X11 | `wait_round.py`, Passo 4, briefing | "caixa vazia" com Run ligado; timeout × duração anunciada; medição chega no `Stop`; hora errada no worklog | ler o Run antes da caixa; o timeout respeita a duração anunciada; esperar o `Stop`; pedir `date` no worklog |

O que a reunião **verificou**: o `worker-start` em três agentes num Run único; o sinal `fim-rodada-N` por mailbox; o
ciclo da R5 (5 h parada sem fechar, `autoReleaseAt` ~2 min depois do `worker_done` aceito); o `tally.py`; o painel por
rodada conferido por PNG; o isolamento da R1; o revisor independente achando o fato que corrigiu a proposta.
