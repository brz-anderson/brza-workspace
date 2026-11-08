---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
  - planning
refs:
  - PLN-004
  - PLN-010
  - PLN-011
  - PLN-012
  - PLN-013
  - PLN-014
  - PLN-017
  - issue:a-fase-do-painel-da-reuniao-no-brza-studio
  - issue:o-brza-sessions-para-a-reuniao-multiagente
---

# O fluxo de reunião multiagente vai a plano: as duas reuniões medidas e a rodada 1

O pedido de Anderson, em 2026-11-08, na sessão `workflow-improvements` (workstream `playground`): extrair os dados e as medições das reuniões "Carvão em Brasa" e "MCP remoto" de 2026-11-07 e levantar, em três frentes, o que melhora o fluxo: skills, `BrzA CLI` e `brza-orchestrator`, e a interface do BrzA Studio. O pedido inteiro está no [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md).

## O que se fez

### Os levantamentos

Cinco `collector` em paralelo, com o agregado no scratch da sessão (`/private/tmp/wf-improv/`, fora do git) e só o resumo na sessão:

| Frente | O que leu | O que achou de mais pesado |
| :----- | :-------- | :------------------------- |
| Ferramental | `brza-sessions`, `brza_runtime.py`, `brza_mcp/`, `agent-launch.ts`, `brza-shot` | cinco verbos, sem `read`, `wait` nem troca de modelo; `--model`/`--effort` não repassados; `send` sempre "sent"; worker do MCP dura uma tarefa; `brza shot` quebrado por `visualBaseCss(true)` |
| Studio | native chat, dashboard, `orchestration-crew`, gates, plugins, PLN-011 | o painel de equipe do Orca existe e está desligado por regressão de desempenho; gates só na CLI; plugin não contribui no chat; `::orca-visual` é estático |
| Protocolo e medições | `.sessions/` das duas reuniões, 18 worklogs de persona, `measurements.jsonl`, rollouts do Codex | 17 passos, 10 implícitos; a coordenação pesa 57% a 62% do custo medido; Grok e Antigravity sem medição; personas Grok gravaram memória em `~/.grok/memory-v2/…` |
| Narração em chat | os transcripts das duas coordenações | sem silêncio longo em nenhuma; a boa nomeava as personas, trazia posição e números por persona, mostrava o worklog e um painel visual |
| Planos vizinhos | PLN-004, 005, 009, 010, 012, 013, 015 | modelo por papel só no MCP (PLN-013); `read` e recibo parados no PLN-010 à espera do PLN-011; medição só do Claude e só em branch (PLN-012); esperar fim de turno, enviar a N e a rodada de decisão sem dono |

### A rodada 1

Quatro perguntas, respondidas por Anderson em 2026-11-08: um PLN no `playground`; as primitivas nascem no `brza sessions`; o painel da rodada vai gerado no chat, com uma investigação breve do custo de religar o `orchestration-crew`; a narração passa a trazer posição e confiança por persona e rodada, quem respondeu e quem falta, e as medições na hora, com a argumentação integral para a fase do painel. O texto das opções, com custo e quando se paga, está na Entrevista do PLN-017.

### O plugin `skill-creator` no `playground`

Pedido de Anderson, na mesma sessão: "instale o plugin skill-creator no escopo desse workstream, no settings.json versionado, e utilize a skill skill-creator para criar e revisar as skills desse plano e as que serão criadas futuramente nesse workstream". A norma põe plugin de workstream no `settings.local.json`, fora do git; aqui, por pedido explícito, ele foi ao `.claude/settings.json` da branch (`brza-workspace@b18f520`), com a chave `skill-creator@claude-plugins-official` ao lado do `context7`. O registro do escopo entrou em `.claude/rules/workspace.md`, na `master` (`brza-workspace@068a31d`), e a `master` foi mesclada neste worktree (`8edd4a5`); os outros workstreams a recebem pelo `brza note sync`. A regra ficou na memória `memory/skills-via-skill-creator.md` e nas Restrições do PLN-017. A sessão carrega plugins no arranque: esta sessão não vê a skill na lista, e o passo que escreve o `SKILL.md` de D1 roda numa sessão nova deste worktree. O processo da `skill-creator` (rascunho, casos de teste em `evals/evals.json`, rodadas com e sem a skill por subagentes, nota, visor e iteração, depois a otimização da descrição) foi lido do cache do plugin para alinhar o desenho de D1.

### O plano

Aberto pelo `brza note plan-open`: PLN-017, com o Pedido nas palavras de Anderson, a Cobertura, o Fora de escopo (a execução em cada repositório, o embrulho MCP, a argumentação integral, as issues travadas pelo PLN-014) e a rodada 1. Os desenhos D1 (skill), D2 (primitivas) e D3 (painel) foram pedidos a três `designer` em paralelo, com a investigação do `orchestration-crew` e a consolidação do Terreno a dois `collector`.

### Os desenhos

Três `designer` em paralelo, um por frente, com os levantamentos como terreno e as respostas da rodada 1 citadas; mais um `collector` para medir o custo de religar o painel de equipe do Orca e outro para consolidar o Terreno (83 fatos com fonte, em `PLN-017-design.md`). Cada desenho foi ao plano num arquivo próprio, com as alternativas, o custo e o "Em aberto" que virou rodada:

| Item | O que fixa | O que mudou o desenho |
| :--- | :--------- | :-------------------- |
| D1, a skill `meeting-runner` (`PLN-017-design-skill.md`) | 17 passos, oito references, quatro scripts, as regras de narração, a forma pela `skill-creator` | o `.sessions/` está no `.gitignore`, então a proposta final passa a ser copiada ao worklog; a contraprova do Carvão custou perto de US$ 9,8 e não 3,5; o "desconto do revisor" não vira regra, porque na v3.2 do MCP ele ficou acima da sala |
| D2, o `brza sessions` (`PLN-017-design-cli.md`) | os verbos `open --model`, `send` com recibo e `--operation`, `wait`, `read --last`, `model`, `usage`, `close --prefix`; a medição por runtime; o `brza shot` | o recibo de hoje esconde a recusa, porque o `rpc()` só erra quando o transporte falha; o contrato do `brza chat send` da branch do PLN-011 serve de forma; o `wait` fecha por estado, `updatedAt` e fila |
| D3, o painel da rodada (`PLN-017-design-painel.md`) | o `estado-rN.json` como contrato, o layout a 736 px, o ciclo de publicação, o gerador `scripts/panel.py` | o app relê o visual só quando uma mensagem nova o monta; o teto de altura é 2000 px e o painel da Carvão tinha 3900; os links do visual só saem para http |

O artboard do painel, com a rodada 3 real da reunião MCP (fechada e parcial, com o Régua faltando), foi conferido por PNG a 736 px nos dois temas e a 390 px, e ficou na pasta do plano. O painel de equipe do Orca lê o banco de orquestração, onde os chats do `brza sessions` não estão, e o upstream o desligou duas vezes em dois dias por amplificação de CPU; adaptá-lo custaria de 25 a 60 h.

### As rodadas 2 a 4

Respondidas por Anderson em 2026-11-08, com o texto das opções e dos custos na Entrevista do PLN-017:

- **R2, a skill:** protótipo na branch do `playground`, promovido ao `core/` depois de duas reuniões sem desvio (um desvio declarado da norma "o `.claude/` mora na `master`"); `SKILL.md`, oito references e quatro scripts; o revisor independente como número da confiança, com a contraprova por gatilho; na rodada final de decisão, o voto e o argumento mais forte a favor e contra por persona. A memória `consultant-debate-shown-in-full` foi emendada: vale só para consultores por `Agent`.
- **R3, o CLI e o painel:** "Recibo, --operation e read --last pelo rpc", fora da recomendada, que não tinha o `read`; é uma exceção de transição à R1.4 do PLN-010, a escrever lá. O `wait` completo, com latência no mapa e `usage` do Codex; um painel por rodada, republicado durante ela; o `orchestration-crew` não se religa.
- **R4, o corte:** "Dividir P4 em envio/espera e medição" (P4a 8 h, P4b 3,5 h), o que aceita o plano com nove passos e 32,75 h; e "P3 agora e abrir a sessão de P1+P2". O plano passou a `in_progress`, `phase: execution`.

### O P3: as duas issues

- [O `brza sessions` ganha os verbos da reunião multiagente: modelo na abertura, recibo, `wait`, `read --last`, `model`, `usage` e `close --prefix`](../issues/o-brza-sessions-para-a-reuniao-multiagente.md), ao `tools-kit`, com P4a, P4b, P5 (o `brza shot`, na `master` do `brza-workspace`), P6 (a emenda ao PLN-010) e as decisões citadas.
- [A fase do painel da reunião no BrzA Studio: argumentação por persona, abrir o chat, gate de decisão e atualização ao vivo](../issues/a-fase-do-painel-da-reuniao-no-brza-studio.md), ao `studio`, sem pedido de execução: o que a v1 não dá, o contrato que a fase lê, as superfícies candidatas e o porquê de não religar o `orchestration-crew`.

### As rodadas 5 e 6: o ciclo de vida das personas

Depois de o plano ser aceito e de a sessão `pln-017-skill` começar P1 e P2, Anderson acrescentou: "as sessões abertas pelo coordenador devem abrir como o `orca-orchestrator` faz, fechando sozinho 2min após não ser mais necessário, com o botão de `manter aberta` acima do input de conversa do chat". O requisito entrou como R5, decidido, e um `collector` mapeou o mecanismo no `brza-studio`: o prazo de 2 min (`WORKER_TERMINAL_AUTO_RELEASE_GRACE_MS`) só é armado por um `worker_done` aceito; o fim de turno de um chat sem `worker_done` não arma nada; a faixa com o botão só aparece em aba com Dispatch de orquestração; um chat aberto por `agent launch` não recebe nada disso sem 20 a 40 h de código no fork; o `worker-start --spec` cria o Run sozinho, exige identidade do chamador, segue o ajuste Chat|CLI por agente e entrega o prompt com o preâmbulo do Orca; o MCP do `brza-workflow` já abre workers por esse caminho. A R6 (2026-11-08) decidiu: "Testar a híbrida; se falhar, worker-start puro"; "Mensagem de mailbox por rodada; worker_done no fim"; "Claude, Codex, Grok e Antigravity em Chat".

O D2 ganhou a seção "Revisão pela R5 e R6" (o terreno do mecanismo em `arquivo:linha` e a tabela verbo a verbo: `open` pela via da sonda, `wait` sobre `check --wait`, `close` por `worker_done`, `worker-release` e `worker-keep-open`); o D1, a revisão dos passos 2, 3 e 7 (abertura com ciclo de vida, `brza orchestration send` por rodada, encerramento pedindo `worker_done`); o P4a ganhou a sonda P4a.0 e passou a 10 h (total do plano 34,75 h); a issue ao `tools-kit` ganhou a seção da revisão. A sessão `pln-017-skill` recebeu dois avisos pelo `brza sessions send`: o primeiro para não fechar o lançador antes de reler o plano, o segundo com o que mudou em P1 e P2.

## O que ficou

- **P1 e P2** (a skill e o gerador do painel) estão na sessão `pln-017-skill`, aberta por esta sessão pelo `brza sessions` com o pedido em arquivo, porque a `skill-creator` só carrega no arranque; a skill `meeting-runner` já apareceu na lista de skills deste worktree. **A sonda P4a.0** (a via híbrida ou o `worker-start` puro) é da sessão do `tools-kit` e decide como o `launch_persona.py` abre as personas. O material fora do git (o protótipo do gerador, os artboards, os rascunhos dos consultores, o levantamento do processo e a comparação da narração) ficou em `.sessions/pln-017/`.
- **P4a, P4b, P5 e P6** esperam as sessões do `tools-kit` e da `master`, a partir da issue; **P7** espera P1 e P2 e o pedido de Anderson; **P8** fecha o plano.
- **A colisão com o PLN-014:** as issues de 2026-11-03 do `playground` que tocam o tema não se emendam nem se portam antes da entrevista daquele plano; o PLN-017 e as duas issues novas só as citam.
- **Duas divergências de número nos worklogs de 2026-11-07**, registradas no Terreno e não corrigidas lá: a "nota dos colegas" da coordenação do Carvão exclui as notas da Faísca (Tição 8,5 e não 8,9; Fogareiro 6,6 e não 6,25; a ordem não muda), e a cota do Codex caiu às 21h37 pelo rollout, não às 21h41 do worklog do MCP.
- **Candidato à norma, sem mexer nela aqui:** a regra de narração da coordenação (quem respondeu e quem falta, posição e confiança por rodada, medição na hora) vale para qualquer sessão que coordene outras; hoje está na memória `coordination-narration-in-chat` e vai à skill.
- **Os fatos a conferir** (`scripts/fact_outcome.py --pending`) seguem sem desfecho: os custos dos desenhos (`C…`) se conferem quando P1, P2 e P4 rodarem.

## Fora do workspace

- **O quê e onde:** dois artboards do painel copiados ao scratch do chat do BrzA Studio, `~/Library/Application Support/brza-studio/chat-scratch/79c3333cffda4d7944a0dd689bf6f87a/pln017-painel-rodada-fechada.html` e `pln017-painel-rodada-parcial.html`, para a diretiva `::orca-visual` da rodada 3. **O risco:** nenhum; são HTML estáticos lidos pelo chat. **Estado:** ficam, como o app guarda os visuais de cada chat. **Como desfazer:** apagar os dois arquivos.
- **O quê e onde:** o link `/private/tmp/wf-improv` para a pasta de levantamentos do scratchpad desta sessão, para os subagentes copiarem o caminho sem erro. **O risco:** nenhum. **Estado:** some com o scratchpad. **Como desfazer:** `rm /private/tmp/wf-improv`.
- **O quê e onde:** o commit `068a31d` na `master` do `brza-workspace`, dentro do repositório mas fora deste workstream, registrando o plugin `skill-creator` no `playground` em `.claude/rules/workspace.md`; já no origin. **O risco:** os outros workstreams só o recebem pelo `brza note sync`, que não rodei para não mexer nos worktrees de outras sessões. **Estado:** feito. **Como desfazer:** `git revert 068a31d` na `master`.
