---
status: open
phase: design
origin: request
description: Mede se as skills distribuídas ao Codex bastam e desenha os verbos com invariante e os MCP prompts do brza-orchestrator, para que plano, tarefa, notas e migração rodem igual em Codex, Cursor e Gemini.
ready: "não — o Desenho de D1 a D6 aguarda as R5 a R8, de Anderson"
priority: medium
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

- **Retomar:** R1 a R4 respondidas; o Desenho de D1 a D6 rascunhado por dois consultores, com o Terreno (M1–M11, T1–T25), em 2026-11-09. Próximo: enviar a R5, depois a R6, a R7 e a R8, que estão na Entrevista, preparadas e não enviadas; depois, gravar o vigente no Desenho e planejar os passos.
- **Dividido:** [PLN-020 — Desenho](PLN-020-design.md)

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
| `Pedido 1–3` (`run_plan`, `run_meeting`, `run_migration`) | Os fluxos longos rodam nos outros clients pelas skills distribuídas, sem verbo nem MCP prompt (R4.1); o `plan-runner` ativa no Codex pelo gatilho natural | a planejar | "vamos planejar X" no Codex, no workspace real, depois do symlink (manual) |
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

- **Uma fonte só por fluxo.** O CLI `brza note` é o motor, o verbo MCP (D3–D6) é um adaptador sobre ele e a skill chama o verbo, com o CLI de reserva (R1.2, "há uma fonte só", mantida na R4.1 para os verbos que ficaram); nenhum fluxo ganha uma terceira implementação.
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

   **Decidido — verbos com invariante e MCP prompts.** **→ reaberta em R4.1**

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

### Rodada 4 — os fluxos longos e a prioridade (enviada 2026-11-09)

**Apresentado antes:** o fim da R3. O roteiro das skills chega ao Codex, ao Cursor e ao Antigravity com o symlink
(M2–M4, M7, M8), e o que nenhum deles faz sozinho já está em D3–D6. O `brza note commit` avisa que falta `priority`.

Respondida em 2026-11-09, nesta sessão.

1. **Os verbos de plano e migração e os MCP prompts da R1.2.**
   - saem do plano: os fluxos longos ficam nas skills distribuídas, e o MCP tem só D3–D6 (recomendada) — custo: zero;
     reabre se aparecer um client sem skill; se paga: agora, com o plano ~2 dias menor;
   - só os verbos, sem prompts (`plan_open`, `plan_round_record`, `migration_open`) — custo: estimativa ~1,5 dia no
     `tools-kit`; se paga: quando o modelo de outro client pular um passo de plano, o que a sonda não viu;
   - a R1.2 inteira — custo: estimativa ~2,5 dias, e o prompt duplica a skill; se paga: só num client que lê MCP e
     não lê skill, e nenhum foi medido.

   **Decidido — saem do plano.** Reabre a R1.2: os `Pedido 1–3` ficam cobertos pelas skills distribuídas.

2. **A prioridade.**
   - `medium` (recomendada) — custo: D1 e D2, de ~1 h cada, esperam atrás dos `high` do `tools-kit`; se paga: quando
     o Codex for usado no workspace;
   - `high` — custo: disputa com o P4 do PLN-003; se paga: agora, se o Codex já trabalha no workspace;
   - `low` — custo: Codex e Antigravity seguem sem as skills até lá; se paga: só se outro client não for usado tão
     cedo.

   **Decidido — `medium`.**

### Rodada 5 — D1 e D2: o link e a identidade (preparada em 2026-11-09, não enviada)

**Apresentado antes:** o Desenho (`PLN-020-design.md`), D1 e D2.
- **O sync:** o `brza sync` não leva symlink — grava arquivo com o texto do alvo e quebra no sync seguinte (T3–T5).
- **A identidade:** o `brza doctor` só confere e não grava (T12), e a fonte da identidade é o `[author]` do manifesto
  (T11).
- **As estimativas:** D1 e D2 passam de ~1 h para 2 h cada, porque viram código com testes.

1. **D1 — O que o `brza sync` faz quando o workspace já tem um `.agents/skills` que não é o link do núcleo?** Hoje
   nenhum workspace tem `.agents/`.
   - recusa com mensagem: o link de outro alvo se troca com `--force`, e o diretório real nunca se apaga, nem com
     `--force` (recomendada) — custo: incluído nas 2 h; o workspace com diretório real fica com o sync em saída 1 até
     mover à mão; se paga: agora, porque nenhum dado se perde;
   - mescla, com um link por skill dentro do diretório real — custo: +~1,5 h e uma entrada no lock por skill, e a skill
     que só a branch tem some; se paga: nunca, enquanto nenhum workspace tiver skills próprias em `.agents/`;
   - avisa e segue sem o link — custo: zero agora, e o workspace fica sem as skills no Codex sem erro visível; se
     paga: nunca, pelo objetivo da R3.1.
2. **D1 — Onde fica a linha de norma do link?**
   - `core/AGENTS.md`, na lista da `master` e na seção do ferramental (recomendada) — custo: ~10 min, dentro do D1;
     se paga: agora, porque o Codex lê o `AGENTS.md` e saberá onde criar skill;
   - `core/CLAUDE.md`, como mecânica de runtime — custo: o mesmo, e o Codex e o Antigravity não o leem; se paga: nunca
     para os outros clients;
   - só na docstring do `brza-sync` — custo: zero; se paga: só se ninguém criar skill fora do Claude Code.
3. **D2 — Quem grava a identidade no `.git/config`?** A R3.3 disse "o `brza doctor`/`install`".
   - `brza install --identity` grava, e o doctor ganha a conferência `config`, que aponta esse comando (recomendada) —
     custo: ~2 h com os testes; se paga: agora, no primeiro commit de outro client, e o doctor continua só lendo;
   - `brza doctor --fix` grava só a identidade — custo: o mesmo, e o doctor passa a escrever, o que muda o contrato
     dele; se paga: só se mais conferências ganharem conserto automático;
   - o doctor grava sempre que diverge, sem flag — custo: ~1,5 h, e um diagnóstico muda o `.git/config` sem pedir; se
     paga: nunca, pelo contrato do doctor.
4. **D2 — O que fazer quando o `.git/config` já tem outro valor?** É o caso do workspace hoje, com o noreply.
   - sobrescreve e mostra `antigo -> novo`, com `--dry-run` para só mostrar (recomendada) — custo: zero além do D2; se
     paga: agora, porque o caso real é o divergente;
   - recusa sem `--force` — custo: um comando a mais por repositório, ~0,25 h; se paga: só se um workspace tiver
     identidade local diferente de propósito, e nenhum foi medido;
   - só grava quando a chave está vazia — custo: zero, e o M10 não se resolve neste workspace; se paga: nunca, aqui.

### Rodada 6 — D2 e D3: o workspace novo e o `close_task` (preparada em 2026-11-09, não enviada)

**Apresentado antes:** o Desenho de D2 e D3 e o padrão comum dos verbos. O verbo chama o `brza note … --json`, e a
sessão vem num argumento, `session: {runtime, id}`. Há um fato novo: 7 tarefas do Codex de hoje, no log real, saíram
com `session_id` null (T20).

1. **D2 — O `brza init` grava a identidade no workspace que nasce?**
   - sim, chamando o `set_identity` depois do commit inicial (recomendada) — custo: ~0,25 h e um teste; se paga: no
     primeiro workspace novo usado por outro client;
   - não, e o `brza install --identity` vai aos próximos passos que o init imprime — custo: ~5 min, e quem pula o passo
     commita com o global; se paga: agora, pelo escopo menor.
2. **D3 — A entrada do `close_task`.** O critério de aceite diz "recebe o worklog estruturado".
   - os caminhos dos arquivos que o client já escreveu (recomendada) — custo: nenhum além do adaptador, e diverge da
     redação do critério; se paga: agora, e o client `read-only` não ganha escrita pelo servidor (M9);
   - o texto Markdown inteiro no argumento — custo: ~1 h, e um client `read-only` passa a escrever nota pelo servidor;
     se paga: só com client sem disco, fora de escopo;
   - os campos estruturados — custo: ~3 a 4 h, uma segunda forma do worklog e um schema que muda com a norma; se paga:
     nunca, enquanto o checador não exigir seções.
3. **D3 — A sessão fora do Claude.**
   - o client declara `session {runtime, id}`, o motor ganha `--session` e `--runtime`, e o worklog sem linha `turn`
     ganha "Não medida" (recomendada) — custo: ~2 h no motor, e o Codex segue não medido até o hook do PLN-004; se
     paga: na primeira tarefa do Codex com a linha `turn` gravada;
   - igual, mas o worklog sem linha `turn` fica sem a seção, como hoje — custo: ~2 h, e o worklog não diz que não foi
     medido; se paga: agora, se a seção for ruído;
   - o servidor acha a sessão pelo rollout mais recente do cwd — custo: ~2 h, e erra com duas sessões no mesmo
     worktree; se paga: só num client que não sabe o próprio id.
4. **D3 e D6 — A identidade no motor.**
   - o motor avisa, sem recusar, quando o e-mail do commit não é o do `[author]` (recomendada) — custo: ~0,5 h depois
     do D2; se paga: no primeiro commit de um client sem o `.git/config` certo;
   - não conferir — custo: zero; se paga: agora, se o D2 bastar;
   - recusar o commit com o e-mail errado — custo: ~0,5 h, e quebra o commit à mão de quem não rodou o install; se
     paga: só se o e-mail errado voltar ao GitHub.

### Rodada 7 — D4, D5 e D6: o briefing, o índice e a frase (preparada em 2026-11-09, não enviada)

**Apresentado antes:** o Desenho de D4 a D6.
- **O Codex:** o PLN-018 fechou, mas a linha `turn` do Codex não se grava (T21).
- **O índice:** o motor e o servidor o reduzem por regras diferentes (T23).
- **A frase de confirmação:** se acha no transcript do Claude e do Codex, e não no dos outros clients (T24).

1. **D4 — O marco do `start_task`.**
   - o briefing agora, sem gravar, e o marco espera a linha `turn` do Codex (recomendada) — custo: ~4 h, e o critério
     de aceite perde "grava o marco" até lá; se paga: agora, nos clients que não leem a memória do workstream;
   - o briefing e o marco, num evento `task_start` — custo: ~7 h, e reabre a forma que a R1.1 do PLN-012 recusou; se
     paga: no Codex, depois do PLN-004; no Claude, quase nunca.
2. **D4 — Quem aciona o `start_task`.**
   - uma linha no `core/AGENTS.md` — "antes de começar, `start_task` ou `brza note brief`" — no lugar do laço de
     `blocks` (recomendada) — custo: ~0,5 h e uma emenda de norma comum; se paga: agora, em todo client que lê o
     `AGENTS.md`;
   - uma skill `start-task` pela `skill-creator` — custo: ~2 a 3 h com os evals, que empatam com o baseline quando não
     há regra nova; se paga: quando o modelo pular a linha da norma, o que não foi medido;
   - ninguém: o modelo acha o verbo pela descrição — custo: zero; se paga: só se a descrição bastar, o que não foi
     medido.
3. **D5 — A fonte do `index_query`.**
   - o `brza note ls` ganha `--json`, os filtros e a página, e o verbo o chama (recomendada) — custo: ~4 h; se paga:
     agora, com uma redução só;
   - o verbo lê pelo `git_index_reader` e o `reduce_index` — custo: ~2,5 h e uma segunda redução, que pode divergir;
     se paga: nunca, pela restrição de uma fonte só.
4. **D6 — A conferência da frase de confirmação.**
   - o motor procura a frase no transcript da sessão, Claude e Codex, e recusa o `done` sem ela (recomendada) — custo:
     ~2,5 h, e do Antigravity, do Grok e do Cursor a decisão só sai `open`; se paga: na primeira decisão gravada por
     subagente ou outra sessão;
   - a frase como declarada, sem conferência — custo: nenhum; se paga: nunca, contra o erro da norma;
   - o gate do `dispatch` — custo: ~1,5 h; se paga: nunca, porque quem aprova é a mesma sessão.

### Rodada 8 — D6 e as condições dos verbos (preparada em 2026-11-09, não enviada)

**Apresentado antes:**
- **O daemon:** está de novo carregado sem processo, e o `KeepAlive` só religa em erro (T17).
- **Os clients:** nenhum tem o servidor configurado (T18).
- **A chave do push:** tem senha e depende do agente (T25).

1. **D6 — Onde mora a frase.**
   - só no corpo da decisão, na linha "Decidido por … em …" de hoje (recomendada) — custo: nenhum na norma; se paga:
     agora;
   - também num campo `confirmation_quote` no frontmatter — custo: ~1 h, com a tabela de propriedades, o checador e o
     índice; se paga: quando alguém consultar decisões pela frase.
2. **A classificação para o proxy remoto.**
   - `index_query` e o briefing do `start_task` remotos; `close_task`, `decision_record` e o marco só no Mac
     (recomendada) — custo: ~0,5 h, um atributo `remote` no registro; se paga: quando o proxy existir;
   - os quatro só no Mac — custo: zero, e a sessão Cloud fica sem o índice; se paga: agora.
3. **O daemon parado e os clients sem o servidor**, que é a condição dos quatro verbos.
   - uma issue ao `tools-kit`, com o `KeepAlive` incondicional e um `brza install --codex-mcp` que grava o
     `brza-orchestrator` no `~/.codex/config.toml` (recomendada) — custo: ~2 a 3 h lá; se paga: no primeiro
     `close_task` do Codex;
   - a reserva do CLI cobre — custo: zero; se paga: nunca para o M9, porque com o daemon fora o Codex volta a pedir
     escalada.

## Worklogs

- 2026-11-09 — a discussão da ideia, R1 e R2; o plano aberto. Parou antes da sonda do Codex.
  [As ferramentas MCP dos fluxos vão a plano: a discussão e as rodadas 1 e 2](../../work/worklogs/2026-11-09-as-ferramentas-mcp-dos-fluxos-vao-a-plano.md)
- 2026-11-09 — a sonda (M1–M11), a R3 e a R4. Parou antes do Desenho.
  [A sonda dos clients e a R3 do PLN-020: as skills chegam por symlink, e o MCP fica para o que o client não faz](../../work/worklogs/2026-11-09-a-sonda-dos-clients-e-a-r3-do-pln-020.md)
- 2026-11-09 — o Desenho de D1 a D6, rascunhado por dois consultores, e as R5 a R8 preparadas. Parou antes de enviar a R5.
  [O desenho de D1 a D6 do PLN-020: dois consultores, e as rodadas 5 a 8 prontas para enviar](../../work/worklogs/2026-11-09-o-desenho-de-d1-a-d6-do-pln-020.md)
