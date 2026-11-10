---
status: open
phase: interview
origin: request
description: Mede se as skills distribuídas ao Codex bastam e desenha os verbos com invariante e os MCP prompts do brza-orchestrator, para que plano, tarefa, notas e migração rodem igual em Codex, Cursor e Gemini.
ready: "não — falta a sonda do Codex, que decide quanto do pedido o MCP ainda precisa cobrir, e o corte dos verbos"
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

- **Retomar:** R1 e R2 respondidas em 2026-11-09. Próximo: a sonda do Codex (o Codex lê as skills distribuídas e roda o `notes-checker` e o `close-task` até o commit?), que entra no Terreno; depois, a R3, o corte dos verbos determinísticos e das sugestões.

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
| `Pedido 6` (`check_notes`) | O `check_notes` devolve os achados do `check_notes.py` estruturados, do mesmo motor | a planejar | `tests/mcp/` (unidade) |
| `Pedido 7` ("novas sugestões") | Cada sugestão da R1 (`index_query`, `decision_record`, `round_record`, `fact_outcome`, `task_pending`, `note_move`, `norm_sync`) entra no corte da R3 com custo e quando se paga, e a que fica vira item `D` | a planejar | a rodada (registro) |

### Fora de escopo

- **A execução no `brza-workflow`.** O código do `brza-orchestrator` é do workstream `tools-kit` (o [PLN-009: O servidor MCP residente coordena o fluxo de trabalho nos dois clients](../PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md)); daqui sai por issue, como no PLN-017 (R2.1).
- **O plugin `brza:` com as skills para o BrzA Studio e o Orca.** É o P4 do [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md); este plano o cita e não o reabre.
- **Expor as ferramentas novas fora do Mac.** É do [O proxy remoto de autorização no brza-mcp](../../work/issues/proxy-remoto-de-autorizacao-no-brza-mcp.md); o desenho daqui só classifica cada verbo para a política dele.
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

## Worklogs

- 2026-11-09 — a discussão da ideia, R1 e R2; o plano aberto. Parou antes da sonda do Codex.
  [As ferramentas MCP dos fluxos vão a plano: a discussão e as rodadas 1 e 2](../../work/worklogs/2026-11-09-as-ferramentas-mcp-dos-fluxos-vao-a-plano.md)
