---
status: open
description: Vinte e uma lições repetidas nas memórias de `workspace`, `tools-kit`, `studio` e `brand` sobem à norma (AGENTS.md, as rules, os papéis, o plan-runner e o AGENTS.md do brza-studio), com o texto pronto por arquivo; as memórias que subiram ou envelheceram saem dos workstreams.
scope:
  - workspace
  - brza-workflow
  - brza-studio
opened: 2026-11-08
priority: high
tags:
  - tooling
---

# As memórias dos workstreams que valem para todos sobem à norma, com o texto pronto por arquivo

Pedido de Anderson em 2026-11-08, na sessão `workflow-improvements` (`playground`): "levante também memórias dos outros workstreams, que não foram a `master`, mas que podem ser úteis, e que são candidatas há subir". Dois `collector` leram as 76 memórias de `memory/` e `.claude/agent-memory/` das branches `workstream/workspace` (21), `tools-kit` (14), `studio` (29) e `brand` (12), pelo git, e conferiram cada uma contra a norma da `master` e contra o disco. Nenhuma está inteira na norma hoje. O registro está em [As memórias dos quatro workstreams, lidas contra a norma: o que sobe, o que sai](../worklogs/2026-11-08-memorias-dos-workstreams-candidatas-a-norma.md).

Esta issue é o pedido ao workstream `workspace`, que executa pela skill `agent-instructions-writer`: a norma comum se edita no `core/` do `brza-workflow` e chega pelo `brza sync`; o que é só deste workspace vai à `master`, no checkout da raiz; o `brza note sync` leva aos workstreams; cada workstream apaga ou enxuga as memórias que subiram no `close-task` seguinte. O bloco do `brza-studio` é do workstream `studio`.

## O que Anderson decidiu (2026-11-08, sessão `workflow-improvements`)

- **O que sobe:** "As regras de conduta no AGENTS.md", "As armadilhas e os testes nas rules", "As lições dos papéis" (as três opções marcadas).
- **As quatro contradições com a norma de hoje se resolvem a favor da memória:** "Edição em callout, não em cerca diff", "Suíte inteira uma vez, no merge", "Rodada delegada sem recomendação", "Commit ao fechar todo passo, para todos" (as quatro marcadas).
- **A norma de código do `brza-studio`:** "Bloco 'BrzA fork' no fim do AGENTS.md do studio".
- **Quem executa:** "Issue ao workspace, com os textos prontos".

## Os textos, por arquivo de destino

A frase-chave em negrito e a regra com o porquê, como manda a `agent-instructions-writer`; a seção vizinha já existe em todos os casos, e a regra nova reescreve ou acrescenta uma linha, não ganha seção própria, salvo as armadilhas do shell.

### `AGENTS.md` (core do `brza-workflow`)

1. **"Um workstream, uma sessão; uma tarefa, um worklog":** "**O push ou o aceite de Anderson fecha a tarefa:** a sessão aciona o `close-task` e commita o worklog pelo `brza note commit` na mesma resposta, sem oferecer nem perguntar; commit e push do código do `brza-studio` seguem pedindo a ordem." Fonte: `studio:memory/worklog-sem-pedir-autorizacao.md` (2026-11-02) e `brand:memory/fechar-a-tarefa-apos-o-push.md` (2026-11-03), a mesma correção de Anderson duas vezes.
2. **"A devolução do subagente":** "**Antes de devolver, reconfira `git log -3` e `git status` do alvo:** outra sessão pode ter commitado no meio; cite `arquivo:linha` do estado final, com o commit ou a versão quando a fonte anda." Fonte: `tools-kit:.claude/agent-memory/reviewer/estado-muda-durante-a-revisao.md` e as memórias do `collector` e do `designer` do `workspace` ("linha citada de cabeça erra"; "o `brza-studio` andou 854 commits").
3. **"O modelo segue a tarefa":** "**Revisão de código não desce à camada rápida só porque a cota do modelo forte acabou;** se descer, vale segunda revisão por modelo forte de outro fornecedor (PLN-011 P3: o Flash aprovou, o Grok achou o bug)." Fonte: `studio:memory/revisao-gemini-flash-perdeu-bug.md`; um caso, marcado como exemplo da regra "Alta, até a medição dizer que média basta".
4. **"Decisões pendentes vão em rodadas de perguntas":** "**A rodada delegada a outro agente, que não Anderson, vai sem a recomendação marcada e com as opções embaralhadas;** a sessão grava a sua recomendação antes. Se o agente discordar, discutem até o acordo, no máximo cinco rodadas, e depois o ponto vai a Anderson com as duas posições. A rodada a Anderson segue com a recomendada primeiro." Fonte: `studio:memory/rodadas-com-agy-as-cegas.md`, pedido de Anderson em 2026-11-03.
5. **A forma da edição na resposta** (hoje: "Edição: o trecho alterado em cerca `diff`"): "**Edição:** o trecho alterado renderizado, com o removido em callout `> [!CAUTION]`, sem cerca `diff`; o arquivo se edita por `Edit`/`Write`, nunca por script, e o `---` vem depois de cada bloco." Fonte: `workspace:memory/edicao-renderizada-com-o-removido-em-callout.md`, pedido de Anderson em 2026-10-31. O golden do `brza init` acompanha.

### `.claude/skills/plan-runner/references/conduct.md` (core), linha "Commite só com confirmação de Anderson"

"**Commite ao fechar o passo verde:** o pedido de executar o passo já inclui o commit, com `git add` por caminho." Fonte: `tools-kit:memory/commit-ao-fechar-todo-passo.md`, ordem de Anderson em 2026-11-03, alcance confirmado para todos em 2026-11-08. O `open-and-plan.md` já diz "o commit fecha a cada passo verde"; a frase do `conduct.md` passa a concordar.

### `.claude/agents/implementer.md` (core)

- Hoje "Rode a suíte inteira do que tocou até ficar verde" vira: "**Rode os testes dos arquivos tocados e vizinhos;** a suíte inteira só se o pedido disser, e com sessões paralelas ela roda uma vez, no merge, pela coordenação." Fonte: `studio:memory/suite-completa-uma-vez-no-merge.md` (a suíte do `brza-studio` leva ~16 min e satura os núcleos); o risco do bug que só a suíte pega (houve um no sync 251) fica com a coordenação.
- "**Para provar que o teste novo falha antes do conserto, não use `git stash`** (a pilha é compartilhada entre worktrees): `git archive HEAD | tar -x -C \"$(mktemp -d)\"`, copie os testes novos e rode lá." Fonte: `workspace:.claude/agent-memory/implementer/brza-workflow-layout-e-testes.md` e `tools-kit:.claude/agent-memory/implementer/brza-workflow-mcp-correcoes.md`.

### `.claude/agents/reviewer.md` (core)

- "**Achado em arquivo que alguém está editando cai:** reconfira cada achado com `git show :<caminho>` imediatamente antes do handback." Fonte: `studio:.claude/agent-memory/reviewer/reviewer-confidence-calibration.md`.
- "**Antes de afirmar que o teste passa sem o conserto, mute em cópia**, nunca no worktree." Fonte: as memórias do `reviewer` do `workspace` e do `tools-kit`.

### `.claude/agents/designer.md` (core)

- "**O artboard de interface parte do componente real:** abra o componente e o CSS e desenhe o 'Hoje' a partir deles, citando `arquivo:linha`; o que o artboard muda além da pergunta vira opção da rodada. Meça a ferramenta antes de pôr custo na opção." Fonte: `brand:memory/artboard-le-o-componente-antes.md` e `brand:.claude/agent-memory/designer/licao-artboard-sobre-o-componente.md` (sessão e papel, PLN-007); a última frase também em `brand:.claude/agent-memory/designer/ferramental-vetor-e-fonte.md`.
- "**Premissa de ferramenta, versão ou modelo se confere na fonte viva antes da rodada** (o PATH das sessões, `~/.codex/models_cache.json`, `grok models`); versões e SHAs vão junto da linha citada." Fonte: `workspace:.claude/agent-memory/designer/feedback_medir-antes-de-desenhar.md`, `project_pln-006-rodadas-e-sondas.md`; `tools-kit:.claude/agent-memory/designer/custos-e-premissas-que-erraram.md`.
- "**Padrão observado em PLN-004, PLN-006 e PLN-013, a confirmar na rodada:** Anderson troca a recomendada barata pela opção nativa do runtime, uniforme entre runtimes ou de estado visível; recomende essa e ponha o contorno barato como alternativa. 'Uso baixo hoje' sozinho não corta." Fonte: sete memórias do `designer` em `workspace` e `tools-kit` (`feedback_mecanismo-nativo-do-runtime.md`, `anderson-prefere-cobertura-uniforme.md`, as recusas do PLN-004); inferência do critério, marcada como tal.

### `.claude/rules/workspace.md` (`master` do `brza-workspace`)

- Na seção dos testes: "**As suítes do `brza-workflow` rodam com `env -u BRZA_WORKSPACE -u BRZA_STUDIO -u BRZA_WORKFLOW`:** a variável da sessão dispara o `foreign_cwd` e dá cerca de 20 falhas que não são regressão. O `tests/cli` leva de 150 a 500 s: rode em segundo plano, com a saída em arquivo." Fonte: cinco memórias de três papéis em `workspace` e `tools-kit`; confirmado em 2026-11-08 pelo `designer` do PLN-017 (47 testes passam com `env -u`, quatro falham com a variável).
- Seção nova "Armadilhas do shell das sessões": "**No zsh do macOS,** `echo ===` e glob sem aspas (`--include=*.ts`) falham; `git show $rev:arq` lê `:a` como modificador, use `\"${rev}:arq\"`; `${=VAR}` divide uma lista; o `sed -i` pede `''`; não há `timeout`. **O runtime barra `rm -rf` com glob relativo:** crie um `mktemp -d` por experimento e apague o caminho exato." Fonte: doze memórias de três papéis nos quatro workstreams.
- "**Modelo local (Ollama) só classifica e roteia:** o `tev1:4b` acerta cerca de 9 em 10 em camada de texto, com volta ao Haiku abaixo do limiar; nenhum local revisa nem aplica regra numérica (o `qwen2.5:14b` deu recall 0 de 7, 15 GB e swap)." Fonte: `workspace:memory/llm-local-fora-da-revisao-avaliar-em-outros-fluxos.md`; dado desta máquina, por isso aqui e não no core.

### `.claude/rules/brza-client.md` (core do pacote `client`)

- "**No chat do BrzA Studio o cwd da sessão e dos subagentes é o scratch:** o pedido a `implementer` ou `collector` leva o caminho absoluto da memória do papel (`<workspace>/.worktrees/<ws>/.claude/agent-memory/<papel>/`), e a sessão confere na devolução onde ela caiu." Fonte: `brand:memory/implementer-grava-memoria-no-cwd.md`.
- No bullet do artboard: "**O `.html` fica na raiz do `ORCA_CHAT_SCRATCH_DIR`, e `file=` leva só o nome:** subpasta não renderiza." Fonte: `brand:memory/artboard-fica-na-raiz-do-scratch.md`.
- "**O `dispatch` do `brza-mcp` só vale de um chat do Studio,** por HTTP com o Bearer de `~/.brza/runtime/mcp.token` e os headers `X-Brza-Session` e `X-Brza-Client`; sessão com `--mcp-config` fora do Studio cai em `session_caller_unknown`." Fonte: `studio:memory/brza-mcp-coordena-de-um-chat-do-studio.md`; o `.mcp.json` do `brza-studio` segue só com o do upstream.
- "**A ponte entre o chat do `brza sessions` e a medição é o `claude_session` do `list --json`:** o id `claude_<uuid>` é o do chat, não o da sessão. Sessão fora do `--settings` do workspace, Codex e Antigravity não têm linha." Fonte: `workspace:memory/o-chat-do-brza-sessions-nao-e-o-session-id-da-medicao.md`.

### `AGENTS.md` do `brza-studio` (workstream `studio`), bloco "BrzA fork" no fim do arquivo

O arquivo é o texto do upstream; o bloco no fim é um hunk de conflito por sync, aceito por Anderson.

- "**Worktree novo: `pnpm install --offline --frozen-lockfile`;** nunca symlink do `node_modules`, que reescreve os links do pnpm na raiz (quebrou o checkout em 2026-10-27)." Fonte: `studio:memory/worktree-node-modules-no-symlink.md`.
- "**Teste novo vai em `*.test.ts(x)`:** os `.spec.ts` de `src/shared` não rodam nem são tipados (`UNIT_INCLUDE` em `config/scripts/ci/unit-selection/dependency-graph/ci-unit-files.mjs`)." **Confirmar antes de generalizar:** a memória só provou `src/shared`, e há 946 `.spec.ts` rastreados. Fonte: `studio:memory/shared-spec-files-do-not-run.md`.
- "**Ao mesclar o upstream, procure cópia fixa de userData, porta, esquema ou executável `orca`** e aponte para `src/shared/brand-identity.ts`; `~/.orca`, `ORCA_*` e `orca://pair` ficam." Fonte: `studio:memory/brza-orca-coexistence.md`.

## O que sai de cada workstream, no `close-task` seguinte ao sync

- **`workspace`:** já obsoletas, `.claude/agent-memory/collector/reference_brza-norma-acoplamento-atalhos.md` ("antes da migração") e `.claude/agent-memory/implementer/hooks-do-claude-testes.md` (o caminho `.claude/hooks/tests` não existe; a devolução no `SubagentHandback` já está no `CLAUDE.md`). Depois de subir: `memory/edicao-renderizada-com-o-removido-em-callout.md`, `memory/llm-local-fora-da-revisao-avaliar-em-outros-fluxos.md`, `memory/o-chat-do-brza-sessions-nao-e-o-session-id-da-medicao.md`, `.claude/agent-memory/designer/feedback_mecanismo-nativo-do-runtime.md` e `feedback_medir-antes-de-desenhar.md`. A citar `src/main/agent-trust-presets.ts`, que sumiu do Studio: `collector/reference_codex-agy-sondas-armadilhas.md`.
- **`tools-kit`:** já envelhecida, `memory/cada-passo-revisado-pelo-agy.md` (PLN-009 fechado, agy 1.5.3). Depois de subir: `memory/commit-ao-fechar-todo-passo.md`, `.claude/agent-memory/designer/anderson-prefere-cobertura-uniforme.md`, `.claude/agent-memory/reviewer/estado-muda-durante-a-revisao.md`, e as linhas gerais de `implementer/brza-workflow-mcp.md` e `brza-workflow-mcp-correcoes.md` (o resto é do MCP e fica).
- **`studio`:** tarefa fechada ou fonte velha, `.claude/agent-memory/implementer/brza-studio-sync-251-lessons.md`, `-sync-251-fixes.md`, `-sync-251-review-fixes.md` (depois de levar o que é geral ao guia), `-sync-test-failures.md` (v1.4.246) e `.claude/agent-memory/collector/reference_studio_fork_quality_audit_tricks.md`. Depois de subir: `memory/worklog-sem-pedir-autorizacao.md`, `rodadas-com-agy-as-cegas.md`, `revisao-gemini-flash-perdeu-bug.md`, `suite-completa-uma-vez-no-merge.md`, `brza-mcp-coordena-de-um-chat-do-studio.md`, a primeira regra de `.claude/agent-memory/reviewer/reviewer-confidence-calibration.md`, e as três do fork quando o bloco entrar no `AGENTS.md` do studio. **Caminhos a corrigir** em nove memórias: `config/scripts/run-vitest.mjs` virou `config/scripts/test-runtime/execution-policy/run-vitest.mjs`; `ci-unit-files.mjs` e `MarkdownPreviewBody.tsx` mudaram de pasta; `config/scripts/orca-dev.mjs` sumiu. **As doze memórias do ciclo de sync do upstream** ficam no `studio`, candidatas a um guia `wiki/guides/` de lá.
- **`brand`:** fonte velha, `.claude/agent-memory/implementer/brza-studio-cli-help-testes.md` (cita `orca-dev.mjs`). Depois de subir: `memory/fechar-a-tarefa-apos-o-push.md`, `implementer-grava-memoria-no-cwd.md`, `artboard-fica-na-raiz-do-scratch.md`, `artboard-le-o-componente-antes.md`, `.claude/agent-memory/designer/licao-artboard-sobre-o-componente.md`, e a última frase de `designer/ferramental-vetor-e-fonte.md`.

## O que fica local, de propósito

Os mapas e sondas de Codex, agy e Grok do `workspace` (PLN-004 aberto), os padrões de erro do `reviewer` do `tools-kit` (código do MCP e scripts de medição), o ciclo de sync do `studio`, os ativos e o sistema de plugins do `brand`, "toda lacuna vira issue" (uma fonte só) e "não renumere os `D` citados por rodada" (uma fonte só).

## Como se prova

- `grep` das frases-chave na `master` e no `core/` depois do `brza sync`: cada uma das 21 em um arquivo só, sem duplicata entre `AGENTS.md`, `CLAUDE.md`, papéis e rules.
- O golden do `brza init` verde depois da troca da cerca `diff` pelo callout.
- `python3 .claude/skills/notes-checker/scripts/check_notes.py` verde nos quatro workstreams depois de as memórias saírem e o `memory/MEMORY.md` e os `MEMORY.md` dos papéis acompanharem.
