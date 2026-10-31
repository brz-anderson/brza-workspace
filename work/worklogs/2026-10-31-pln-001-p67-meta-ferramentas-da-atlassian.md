---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
---

# O P67 do PLN-001, as meta-ferramentas da Atlassian com ícone e título

Anderson pediu a fila de melhorias do workstream `studio` e escolheu o X20 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md):
"vamos ao X20". O passo novo, o P67, rodou na sessão do workstream `studio` do `brza-workspace`. Um `implementer`
(Sonnet) escreveu o código no worktree `.worktrees/pln-001-p67` do `brza-studio`, e a sessão revisou, commitou e deu
push direto na `master`, sem PR. A evidência detalhada está no passo, no plano.

## O levantamento

- **O código.** O `atlassianProduct` escolhia Jira ou Confluence só pelo nome da ferramenta, e o `match` do resolvedor
  recebia o input mas não o passava ao `matchesMcpTool`.
- **As chamadas reais.** Nos transcripts da Fixfy, o `executeRead` (53), o `executeWrite` (7) e o `executeDestructive`
  (9) levam `{ cloudId, name, inputs }`, com a ferramenta interna no `name`; o `discover` (49) leva só `{ query }`. O
  `executeDestructive` não estava no X20 e entrou junto.

## As rodadas

- **R55.1** — os `execute*` ganham o ícone do produto do `name` e o título com a ferramenta interna e a ação, sem chip.
  Anderson escolheu "Ícone e título curtos (Recomendado)", contra só o ícone e contra o chip com a chave do card.
- **R55.2** — o `discover` ganha o ícone do produto que a busca cita, e o título com a busca entre aspas. Anderson
  escolheu "Produto pela busca (Recomendado)", contra deixar sem categoria e contra um ícone genérico da Atlassian.
- **R56.1** — só os três nomes explícitos casam. Anderson escolheu "Os três nomes explícitos (Recomendado)", contra
  qualquer `execute*`.
- **R56.2** — a busca do `discover` vai inteira no título. Anderson escolheu "Inteira, sem cortar (Recomendado)",
  contra cortar em ~120 caracteres.

A R56 fechou as duas escolhas que o `implementer` fez sem lastro na R55.

## O P67

Commit `brza-studio@97a93f6ff57`.

- **O produto.** O `metaToolSubject`, em `brza-atlassian-tool.ts`, lê o `input.name` dos três `execute*` e a `query` do
  `discover`; o `productInText` fica com o produto citado primeiro.
- **O título.** "manageJiraSprint · start" nos `execute*`, e a busca entre aspas curvas no `discover`; nenhum dos dois
  tem chip.
- **O resolvedor.** O `matchesMcpTool` recebe o input como segundo argumento. Os chamadores do desktop e do mobile já o
  passavam, e não mudaram.
- **A identidade.** A sessão conferiu que ela chega crua pelos dois caminhos, o nome `mcp__atlassian__executeRead` do
  Claude e o `{ server, tool }` do Codex, e que a regex casa nos dois.
- **Os testes.** Antes do código, 11 failed e 26 passed nos dois arquivos de teste. Depois, 37 passed;
  `src/shared/native-chat` deu 1.182 passed; o `pnpm tc` e o `typecheck` do `mobile/` deram exit 0; o
  `check:changed` ficou só com o vermelho de antes, nas fronteiras de import do `external-subcommand.ts`.

O worktree e a branch saíram depois do push. A conferência no app vai junto do C6, com Anderson.

## A memória

O `implementer` gravou `.claude/agent-memory/implementer/brza-studio-native-chat-tools.md`, com o formatador, o comando
do vitest, os chamadores do resolvedor e a forma da identidade MCP. A sessão corrigiu o tempo do `check:changed`, que
levou ~2 min aqui, e não os ~10 min da nota.
