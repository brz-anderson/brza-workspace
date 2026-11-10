---
status: open
phase: interview
origin: request
description: Mede se as skills distribuídas ao Codex bastam e desenha os verbos com invariante e os MCP prompts do brza-orchestrator, para que plano, tarefa, notas e migração rodem igual em Codex, Cursor e Gemini.
ready: "não — falta a R4 e o Desenho de D1 a D6"
scope:
  - workspace
  - brza-workflow
opened: 2026-11-09
owner: Anderson
tags:
  - tooling
  - planning
---

# PLN-020: Os fluxos do workspace rodam em qualquer client, pelas skills distribuídas e por verbos do brza-orchestrator

- **Retomar:** R1 a R3 respondidas e a sonda no Terreno (M1–M11) em 2026-11-09. Próximo: a R4 (os verbos de plano e migração e os MCP prompts da R1.2, que a sonda enfraqueceu) e o Desenho de D1 (symlink no `core/`), D2 (identidade no `brza doctor`), D3 (`close_task`), D4 (`start_task`), D5 (`index_query`) e D6 (`decision_record`).

## Pedido

- **Origem:** pedido livre, na sessão do workstream `playground` de 2026-11-09.

"MCP `brza-orchestrator` tem:

- `run_plan`: o equivalente a skill `plan-runner`;
- `run_meeting`: equivalente a `meeting-runner`;
- `run_migration`: equivalente a `migration-runner`;
- `start_task`: usado para iniciar um passo/tarefa, análogo ao que é o `close-task` usado para encerrar uma tarefa;
- `close_task`: equivalente a `close-task`;
- `check_notes`: equivalente a `notes-checker`;

vamos discutir sobre a ideia, faça críticas nos pontos que você discordar, faça novas sugestões de uso, seguindo a mesma linha"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| R1.1 (portabilidade) | A sonda diz, com o comando e a saída, se o Codex carrega as skills do workspace e roda o `notes-checker` e o `close-task` até o `brza note commit`; o resultado decide quanto dos itens abaixo segue | a planejar | a sonda num worktree de teste (manual) |
| `Pedido 1–3` (`run_plan`, `run_meeting`, `run_migration`) | Cada fluxo longo vira verbos com invariante no servidor e um MCP prompt com o roteiro, sem ferramenta `run_*` que conduza o fluxo inteiro (R1.2); os verbos da reunião esperam a ordem da PLN-017/R1.2 (R2.2) | a planejar | `tests/mcp/` do `brza-workflow` (unidade); um fluxo rodado do Codex (manual) |
| `Pedido 4` (`start_task`) | O `start_task` grava o marco de início da tarefa e devolve o briefing: os bloqueios em vigor, o `Retomar` do plano e a memória do workstream; sem ele, o corte implícito do evento `task` continua valendo | a planejar | `tests/mcp/` e `tests/hooks/` (unidade) |
| `Pedido 5` (`close_task`) | O `close_task` recebe o worklog estruturado, valida contra a norma de `work/worklogs/` e faz o commit, o índice e o evento `task` com a identidade, a sessão e o workstream do chamador, e não do ambiente do daemon; com o daemon fora, a skill cai no CLI | a planejar | `tests/mcp/` (unidade); o `/compact` passando depois do `close_task` (manual) |
| `Pedido 6` (`check_notes`) | O `notes-checker` roda em Codex, Cursor e Antigravity pela skill distribuída, sem verbo MCP (R3.2) | a planejar | a sonda M7 refeita no workspace real, depois do symlink (manual) |
| `Pedido 7` ("novas sugestões") | `index_query` e `decision_record` viram itens `D` (R3.2); as outras sugestões ficam fora | a planejar | `tests/mcp/` (unidade) |
| R3.1 (distribuição) | O `core/` do `brza-workflow` leva o symlink `.agents/skills -> ../.claude/skills`, e o Codex e o Antigravity listam as skills no workspace real | a planejar | `tests/cli/` do `brza sync` (unidade); o catálogo no Codex (manual) |
| R3.3 (identidade) | O `brza doctor` grava a identidade da norma no `.git/config` do workspace e do `brza-studio`, e um commit sem o `env` do Claude sai com o e-mail da norma | a planejar | `tests/cli/` do `brza doctor` (unidade); `git var GIT_AUTHOR_IDENT` fora do Claude (manual) |

### Fora de escopo

- **A execução no `brza-workflow`.** O código do `brza-orchestrator` é do workstream `tools-kit` (o [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md)); daqui sai por issue, como no PLN-017 (R2.1).
- **O plugin `brza:` com as skills para o BrzA Studio e o Orca.** É o P4 do [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md); este plano o cita e não o reabre.
- **Expor as ferramentas novas fora do Mac.** É do [O proxy remoto de autorização no brza-mcp](../../work/issues/proxy-remoto-de-autorizacao-no-brza-mcp.md); o desenho daqui só classifica cada verbo para a política dele.
- **O `check_notes` como verbo MCP.** Cortado na R3.2: a skill já roda no Codex (M7).
- **As skills que o Antigravity corta por orçamento** (`meeting-runner`, `agent-instructions-writer`). Aceito na R3.4:
  o Antigravity entra como persona; reabre se ele coordenar.
- **Os verbos da reunião antes de duas reuniões sem desvio.** Esperam a [A meeting-runner chega ao core depois de duas reuniões sem desvio](../../work/issues/promocao-da-meeting-runner-apos-duas-reunioes-sem-desvio.md), pela PLN-017/R1.2 e pela R2.2.

## Restrições

- **Uma fonte só por fluxo.** O CLI `brza note` é o motor, o verbo MCP é um adaptador sobre ele e a skill chama o verbo, com o CLI de reserva (R1.2, "há uma fonte só"); nenhum fluxo ganha uma terceira implementação.
- **Toda skill deste plano se cria e se revisa pela `skill-creator`**, pela regra do `playground` de 2026-11-08 (PLN-017, Restrições).

## Entrevista

### Rodada 1 — o motor e a forma (enviada 2026-11-09)

**Apresentado antes:** o servidor de hoje tem três ferramentas, `dispatch`, `status` e `config`, e o valor dele é o gate: pedido que não seja de consultor volta como proposta e só roda aprovado (`brza-workflow/packages/mcp/brza_mcp/tools.py:1-8`, `:535-546`). As skills são de dois tipos: determinísticas (o `notes-checker`, a metade final do `close-task`) e de conversa (`plan-runner`, `meeting-runner`, `migration-runner`). As críticas:

1. um `run_*` monolítico fere "quem pergunta e grava é a sessão principal" (`AGENTS.md`), porque o MCP não abre pergunta com opções, e sofre com timeout e com a narração por rodada;
2. o MCP tem prompts e resources para o roteiro e a norma, e `~/.codex/skills` e `~/.agents/skills` já existem nesta máquina, o que enfraquece a portabilidade como motivo;
3. skill e ferramenta "equivalentes" divergem na primeira mudança de norma;
4. o daemon do launchd não tem o `env` da sessão (`GIT_AUTHOR_*`, `CLAUDE_CODE_SESSION_ID`, o cwd do workstream);
5. em 2026-11-07, o agente do launchd estava carregado sem processo (Reunião MCP remoto: a coordenação), então o `close-task` precisa de reserva no CLI;
6. as ferramentas que escrevem git e abrem chats pagos entram na classificação do gate e dos tetos;
7. o `start_task` vale pelo marco de início e pelo briefing;
8. o `close_task` não escreve o worklog: recebe-o estruturado e valida.

As sugestões: `index_query`, `decision_record` (com `confirmation_quote`), `round_record`, `fact_outcome`, `task_pending`, `note_move` e `norm_sync` sob gate.

Respondida em 2026-11-09, nesta sessão, em texto: "ambos recomendado".

1. **O motor da ideia.**
   - portabilidade entre clients (Codex, Cursor, Gemini) (recomendada) — custo: primeiro testar se as skills distribuídas ao Codex já resolvem, uma sessão curta; se paga: logo, ao evitar construir o que talvez não precise;
   - acesso remoto (Cloud, outra máquina) — custo: depende do proxy de autorização, que ainda está em aberto; se paga: só depois que o proxy existir;
   - invariantes no servidor, independentes do client — custo: refatorar o `brza note` para virar biblioteca chamável pelo daemon; se paga: na primeira vez que o modelo pularia um passo da skill.

   **Decidido — portabilidade entre clients**, com a sonda do Codex antes de construir.

2. **A forma dos fluxos longos (plano, reunião, migração).**
   - verbos com invariante, mais MCP prompts como roteiro (recomendada) — custo: mais ferramentas pequenas, e a skill passa a chamá-las; se paga: na primeira mudança de norma, porque há uma fonte só;
   - um `run_*` monolítico — custo: conflita com "quem pergunta é a sessão principal", e sofre com timeout e com a narração; se paga: nunca, na leitura atual da norma;
   - os fluxos longos ficam só como skills, e o MCP recebe apenas as determinísticas — custo: o fluxo longo fica preso aos clients que leem skill; se paga: logo, pelo escopo menor.

   **Decidido — verbos com invariante e MCP prompts.**

### Rodada 2 — o destino e a ordem (enviada 2026-11-09)

**Apresentado antes:** o PLN-017 está `done` e não aceita anexo; ele fixou que "o embrulho MCP das primitivas vem depois de o CLI rodar duas reuniões" (PLN-017/R1.2), e nenhuma reunião completa rodou ainda pela integração v2. O `brza-orchestrator` é do `tools-kit` (PLN-009, `done`). O P4 do PLN-003 (`in_progress`, no `tools-kit`) é um plugin do Claude com as skills sob `brza:`, um `.mcp.json` para o orquestrador e um `agents/codex.json`, mas para o BrzA Studio e o Orca, não para Codex, Cursor ou Gemini como clients.

Respondida em 2026-11-09, nesta sessão.

1. **Destino.**
   - PLN novo no `playground` (recomendada) — custo: abrir o plano nesta sessão, ~15 min, e uma issue de saída no fim; se paga: no desenho, porque a sonda e as rodadas ficam junto da discussão de hoje;
   - PLN novo no `tools-kit` — custo: a sessão nova relê a norma e o PLN-003, o arranque que a medição diz ser metade do gasto; se paga: na execução, sem issue intermediária;
   - anexar ao PLN-003/P4 — custo: reabre o desenho de um plano em execução e mistura Studio/Orca com Codex/Cursor/Gemini; se paga: só se o P4 for executado logo.

   **Decidido — PLN novo no `playground`**: este, PLN-020.

2. **A ordem dos verbos da reunião.**
   - respeitar a PLN-017/R1.2 (recomendada) — custo: o verbo da reunião atrasa até as duas reuniões; se paga: quando a reunião estabilizar, porque não se embrulha fluxo que ainda muda;
   - reabrir a R1.2 — custo: desenhar sobre um fluxo com 19 desvios no P7 do PLN-017 e nenhuma reunião completa pela v2, com chance de refazer; se paga: só se a reunião não mudar mais.

   **Decidido — respeitar a R1.2**: o plano começa pela sonda e pelos verbos determinísticos.

### Rodada 3 — a sonda e o corte (enviada 2026-11-09)

**Apresentado antes:** o Terreno M1–M11. O Codex e o Antigravity só leem `.agents/skills`, e o Cursor lê o
`.claude/skills`. No Codex, as skills rodam pelo gatilho natural até o `brza note commit`. O que quebra é o ambiente:
o sandbox barra o `.git`, a identidade sai do `.git/config` e a tarefa não é medida. A leitura: o roteiro já chega
pelas skills, e o MCP vale onde o servidor faz o que o client não faz.

Respondida em 2026-11-09, nesta sessão.

1. **Distribuição das skills.**
   - symlink `.agents/skills -> ../.claude/skills` no `core/` do `brza-workflow`, pelo `brza sync` e pelo `brza note sync` (recomendada) — custo: ~1 h no `tools-kit`, uma linha de norma; se paga: agora, para Codex e Antigravity em todo workspace;
   - symlink só neste workspace, registrado em `.claude/rules/workspace.md` — custo: ~15 min; se paga: agora, mas o próximo workspace repete;
   - cópia pelo `brza sync` — custo: duas cópias que divergem; se paga: só se algum client não seguir symlink, e nenhum foi medido.

   **Decidido — symlink no `core/`.**

2. **Os verbos que entram no Desenho** (seleção múltipla).
   - `close_task` (recomendada) — custo: estimativa ~1 dia no `tools-kit`, sobre o `brza note`; se paga: na primeira tarefa fechada pelo Codex sem escalada (M9–M11);
   - `start_task` — custo: estimativa ~0,5 dia; se paga: quando a medição por tarefa do Codex existir (PLN-018);
   - `check_notes` — custo: estimativa ~2 h; se paga: nunca, enquanto a skill rodar em todo client (M7);
   - `index_query` e `decision_record` — custo: estimativa ~1 dia os dois; se paga: quando houver coordenação fora do Claude Code.

   **Decidido — `close_task`, `start_task`, `index_query` e `decision_record`.** O `check_notes` sai: o `Pedido 6`
   fica coberto pela skill distribuída.

3. **A identidade do commit fora do Claude Code** (M10).
   - o `brza doctor`/`install` grava `user.name` e `user.email` da norma no `.git/config` do workspace e do
     `brza-studio`, e o `AGENTS.md` deixa de dizer que a identidade não depende dele (recomendada) — custo: ~1 h e uma
     emenda na norma; se paga: agora, para todo client e para o commit à mão;
   - só pelo `close_task` — custo: zero além do verbo; se paga: só quando o verbo existir, e o commit fora dele segue
     com o e-mail errado.

   **Decidido — o `brza doctor` grava o config.**

4. **O corte do catálogo no Antigravity** (M4).
   - aceitar e registrar: o Antigravity entra como persona, e a persona não usa a `meeting-runner` (recomendada) —
     custo: zero; se paga: agora; reabre se o Antigravity coordenar;
   - encurtar as duas descrições pela `skill-creator` — custo: ~1 h cada, com o risco de piorar o gatilho no Claude;
     se paga: só quando o Antigravity coordenar.

   **Decidido — aceitar e registrar.**

**O que a R3 não cobriu:** os verbos de plano e de migração e os MCP prompts da R1.2. Com M2, M3, M7 e M8, o roteiro
já chega aos clients pelas skills, e o prompt pode não ter mais função. Vai à R4.

## Desenho

### O que este desenho assume

- **R1.1:** o motor é a portabilidade entre clients, e a sonda vem antes de construir.
- **R1.2:** os fluxos longos viram verbos com invariante e MCP prompts, sem `run_*`.
- **R2.2:** os verbos da reunião esperam duas reuniões sem desvio.

### Terreno

A sonda de 2026-11-09 rodou num clone isolado no scratch da sessão: repositório bare como `origin`, a `master` e os
worktrees dos workstreams, com `BRZA_WORKSPACE` e `MEASURE_DIR` apontando para o clone. As saídas brutas (`a.jsonl` a
`k.txt`) ficaram no scratch, fora do git.

#### O catálogo de skills em cada client

- **M1 — Codex sem distribuição não vê as skills do workspace.** Codex CLI `0.166.0`, `codex exec -s read-only`: o
  catálogo trouxe as de usuário (`~/.codex/skills`), as de sistema e as de plugin, e "do repositório: nenhuma". [medido]
- **M2 — Codex vê as seis com um symlink.** `.agents/skills -> ../.claude/skills`, no worktree: as seis no catálogo,
  com a descrição. [medido]
- **M3 — Cursor lê o `.claude/skills` sem nada.** `cursor-agent 2026.10.22`, `--mode ask`: as seis, com e sem o
  `.agents/`. [medido]
- **M4 — Antigravity precisa do `.agents/skills` e corta por orçamento.** `agy --mode plan --sandbox`: sem o symlink,
  nenhuma; com ele, quatro. `meeting-runner` (896 caracteres de descrição) e `agent-instructions-writer` (636) saem
  "excluded due to context budget limits", na disputa com as skills de `~/.gemini/`. [medido]
- **M5 — O Gemini CLI não está instalado**; não medido.
- **M6 — O `brza-workflow` não distribui skill a outro client.** A busca por `.agents/skills` e `codex/skills` no
  repositório não achou nada. [lido]

#### O fluxo pelo Codex

- **M7 — O gatilho natural ativa a skill.** "confere as notas", sem o nome da skill: o Codex leu o `SKILL.md` do
  `notes-checker`, rodou a busca de `blocks` do `AGENTS.md` e o `check_notes.py --detail`, e relatou os achados sem
  editar. 112.816 tokens de entrada, 93.184 em cache. [medido]
- **M8 — O Codex segue o `close-task` até o commit.** Pedido "crie a issue … depois fecha a tarefa":
  - leu o `work/README.md` e os dois `SKILL.md`;
  - conferiu o `CLAUDE_CODE_SESSION_ID` (ausente);
  - rodou o `fact_outcome.py --pending`, o checador e o `brza note commit`;
  - relatou fielmente o que barrou.

  497.963 tokens de entrada nos dois turnos, 460.544 em cache. [medido]
- **M9 — O sandbox padrão do Codex barra o commit.** `workspace-write`: o `git add` falha em
  `.git/worktrees/playground/index.lock` com `Operation not permitted`, mesmo com o clone em `--add-dir`. Com a
  configuração de Anderson (`approval_policy = "on-request"`), cada `brza note commit` pede escalada. O modo sem
  sandbox foi barrado nesta sessão pelo classificador, e o commit foi rodado pela sessão com o comando e o ambiente do
  Codex. [medido]
- **M10 — A identidade do commit não é a da norma.** Sem `GIT_AUTHOR_*` no ambiente, o commit sai com o `user.email`
  do repositório, `240569289+brz-anderson@users.noreply.github.com`, e não com o `brz.anderson.pereira@gmail.com` que o
  `CLAUDE.md` fixa pelo `env`. [medido]
- **M11 — A tarefa do Codex não é medida.** O evento `task` sai com `session_id: null` (e o `chat_id` que veio do
  ambiente desta sessão, não do Codex), e o worklog fica sem a seção `## Custo da tarefa`. A linha de turno do Codex é
  do PLN-018, em revisão no `tools-kit`. [medido]

## Worklogs

- 2026-11-09 — a discussão da ideia, R1 e R2; o plano aberto. Parou antes da sonda do Codex.
  [As ferramentas MCP dos fluxos vão a plano: a discussão e as rodadas 1 e 2](../../work/worklogs/2026-11-09-as-ferramentas-mcp-dos-fluxos-vao-a-plano.md)
- 2026-11-09 — a sonda (M1–M11) e a R3. Parou antes da R4.
  [A sonda dos clients e a R3 do PLN-020: as skills chegam por symlink, e o MCP fica para o que o client não faz](../../work/worklogs/2026-11-09-a-sonda-dos-clients-e-a-r3-do-pln-020.md)
