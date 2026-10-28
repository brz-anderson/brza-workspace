---
scope:
  - brza-workspace
date: 2026-10-27
tags:
  - tooling
---

# O brza-workspace nasce com a norma, o PLN-001, a medição e as skills de notas e de plano

Sessão `fixfy-9b`, aberta no workspace da Fixfy, em 2026-10-27. Anderson pediu duas coisas:

- "criei um repo pra servir de workspace do brza-studio, git: git@github.com:brz-anderson/brza-workspace.git - clone em
  Projects/ ao lado de brza-studio e envie o plano de melhorias do BrzA Studio para lá (brza-workspace)";
- "crie uma AGENTS.md e um CLAUDE.md no brza-workspace, adaptando o daqui, pra norma de notas, adapte e crie os
  scripts necessários lá tbm, incluindo telemetria, as medições que fazemos aqui, adaptadas para o contexto novo".

Depois, ele pediu que o código fosse para a sessão `brza-studio`, mas que esta sessão ficasse com o brza-workspace "até
que o projeto exista no disco, com git, pra mim abrir no BrzA Studio".

## O que foi feito

- **O clone**, em `~/Projects/brza-workspace`, pelo alias `personal`.
- **O plano.** O PLN-029 da Fixfy virou o
  [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md).
  Os pedidos de 2026-10-27 entraram como P42 a P53, e as rodadas como R29 a R32. Na Fixfy, o PLN-029 ficou como aviso de
  mudança.
- **A norma.** Feitos por subagentes:
  - o `work/README.md` e o `plans/README.md`, adaptados da Fixfy;
  - o `notes-checker` e a `plan-runner`, como skills de projeto.

  Os comandos estão no `README.md`.
- **O `AGENTS.md` e o `CLAUDE.md`**, com as seções escolhidas na rodada F.
- **A medição.** O `measure.py`, sem os modos de Codex e agy, e o `resume_guard.py`. Os dois estão ligados no
  `.claude/settings.json`, com cache de 1 h e 5 min, e há 25 testes. O resumo é o
  `scripts/summarize_measurements.py`.
- **A identidade e as funções.** O `env` do `settings.json` põe a identidade do `brz-anderson` e a chave `personal`. A
  função `claude` do `~/.zshrc` passa esse `settings.json` às sessões abertas aqui e no `brza-studio`.
- **Os commits.** O primeiro foi o `0bc2c77`, que levou também o P52 e o P53 da sessão
  `brza-studio-chat-blocos-120-colunas`. Os acertos da rodada G vieram no commit deste worklog.

## Rodadas

As rodadas de 2026-10-27, sessão `fixfy-9b`. A escolhida está marcada com ✅. A rodada D, do plano, está na R32 do
PLN-001.

### Rodada E — telemetria e configuração

Apresentado antes:
- o `measure.py` só depende da Fixfy pela raiz (`FIXFY_WORKSPACE`);
- o `settings.json` não passa de um diretório para outro, e quem o injeta é a função `fixfy_claude`, só dentro de
  `~/Projects/fixfy`;
- por isso o `brza-studio` precisava do `env -u` das cinco variáveis em cada commit.

**E1. Quais medições e hooks vão?** (múltipla)
- ✅ measure.py (Recomendado). Custo: ~1,5 h. Se paga: na primeira pergunta sobre o custo de uma sessão do BrzA Studio.
- ✅ Trava de retomada + TTL (Recomendado). Custo: ~0,4 h. Se paga: na primeira sessão grande parada que ela barrar.
- Statusline. Custo: ~0,5 h. Se paga: se você olha a cota durante o trabalho.
- Codex e agy. Custo: ~2 h. Se paga: só se usar Codex, agy ou a conta adm no BrzA Studio.

**E2. Como as sessões carregam a configuração?**
- ✅ Função no ~/.zshrc (Recomendado). Custo: ~0,3 h e uma mudança no `~/.zshrc`. Se paga: na primeira sessão do
  brza-studio.
- settings.local.json no brza-studio. Custo: ~0,2 h, mais uma cópia por worktree. Se paga: só se você não quiser mexer
  no `~/.zshrc`.
- Só no brza-workspace. Custo: zero. Se paga: nunca, para o código.

**E3. Qual identidade commita?**
- ✅ brz-anderson pelo env (Recomendado). Custo: ~0,2 h. Se paga: no primeiro commit.
- Manter o env -u. Custo: um commit errado a cada esquecimento. Se paga: nunca.

**E4. Quais skills de projeto?**
- ✅ notes-checker + plan-runner adaptados (Recomendado). Custo: ~1,5 h. Se paga: no próximo plano ou nota.
- Só o notes-checker. Custo: ~0,7 h. Se paga: agora, mas sem a entrevista e o molde.
- Habilitar o plugin fixfy. Custo: ~0,1 h, mas mistura a norma da Fixfy. Se paga: nunca.

### Rodada F — o AGENTS.md e o ferramental

Apresentado antes: quais seções do `AGENTS.md` da Fixfy são genéricas e quais são só da Fixfy.

**F1. Quais seções genéricas vão?** (múltipla)
- ✅ Rodadas e decisão explícita (Recomendado). Custo: ~0,2 h. Se paga: na primeira decisão.
- ✅ Modelo segue a tarefa (Recomendado). Custo: ~0,1 h. Se paga: no primeiro levantamento grande.
- ✅ Tarefa, sessão e worklog (Recomendado). Custo: ~0,2 h. Se paga: no fim da primeira tarefa.
- Sessão dona e worktree (Recomendado). Custo: ~0,2 h. Se paga: quando duas sessões editarem o brza-studio juntas.

**F2. Quais plugins?** (múltipla)
- ✅ context7 (Recomendado). Custo: um servidor MCP no arranque. Se paga: na primeira dúvida de API.
- frontend-design (Recomendado). Custo: uma linha de contexto. Se paga: nos passos de UI.
- figma. Custo: ~40 ferramentas no contexto. Se paga: só com design do BrzA Studio no Figma.
- karpathy + claude-code-setup. Custo: duas linhas de contexto. Se paga: no código, as diretrizes.

**F3. Servidores MCP?**
- ✅ Nenhum (Recomendado). Custo: zero. Se paga: agora.
- atlassian. Custo: login por conta. Se paga: só com um Jira do BrzA Studio.

### Rodada G — o que os subagentes deixaram em aberto

Apresentado antes:
- o primeiro commit já tinha saído com as opções recomendadas;
- a numeração R29–R32, as rodadas no plano, a data de 2026-10-28 do link do `## Worklogs`, o fim das regras de migração
  e a forma do achado ficaram como estavam;
- a norma de rodadas da `plan-runner` passou a apontar para o `AGENTS.md`.

**G1. Quais tags?**
- ✅ Somar chat e release (Recomendado). Custo: ~5 min. Se paga: no próximo worklog de chat.
- Manter como está. Custo: nenhum. Se paga: agora, mas chat e build se misturam em `tooling`.

**G2. Mudança no brza-studio entra no `## Fora do workspace`?**
- ✅ Não entra (Recomendado). Custo: nenhum. Se paga: no primeiro worklog de código.
- Entra. Custo: ruído em quase todo worklog. Se paga: nunca, provavelmente.

**G3. Os conectores do claude.ai sobem?**
- ✅ Desligar, como na Fixfy (Recomendado). Custo: os conectores somem dessas sessões. Se paga: em toda sessão.
- Deixar ligados. Custo: contexto em toda sessão. Se paga: só se você usar algum deles aqui.

**G4. Sem a `BRZA_WORKSPACE`, onde a medição grava?**
- ✅ No brza-workspace, sempre (Recomendado). Custo: ~10 min. Se paga: na primeira sessão aberta sem a função.
- Deixar como está. Custo: um `.measurements/` solto no brza-studio. Se paga: nunca.

## O que ficou aberto

- **Conferir a função numa sessão nova:** depois de `source ~/.zshrc`, abrir `claude --name <nome>` aqui.
  - O `git var GIT_AUTHOR_IDENT` tem de dar o noreply do `brz-anderson`.
  - Um turno tem de virar linha em `.measurements/measurements.jsonl`.
- **O P42 a P51 do PLN-001.** O pedido está em `/private/tmp/claude-501/brza-studio-pedido-chat-perguntou-e-icones.md`,
  e a sessão `brza-studio-chat-perguntou-e-icones` ainda não foi aberta.

## Fora do workspace

- **`~/.zshrc`, o bloco "Workspace BrzA"**:
  - **O quê e onde:** `BRZA_WORKSPACE`, `BRZA_STUDIO`, `brza_where` e `brza_claude`. A `claude()` escolhe entre
    `brza_claude` e `fixfy_claude`, e a `adm-claude()` passou a chamar `claude`. É o bloco de "Funções do shell" do
    `README.md`.
  - **O risco:** uma sessão aberta no brza-studio deixa de herdar a configuração da Fixfy.
  - **Estado:** ativo.
  - **Como desfazer:** apagar o bloco e voltar `claude()` e `adm-claude()` a chamar `fixfy_claude`.
