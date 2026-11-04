---
status: done
scope:
  - brza-studio
opened: 2026-11-03
completed: 2026-11-03
tags:
  - chat
  - tooling
refs:
  - PLN-011
---

# REV-009: P3 do PLN-011, `chat read` com cursor, ids e reset

Revisão independente do P3 do
[PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md),
contra D3, D6, a Cobertura e a Regressão. O primeiro commit, `brza-studio@77a1cca1af2`, recebeu pareceres independentes
do Antigravity (aprova, sem achados) e do Grok 4.7 (aprova com A1–A3, todos com destino corrigido aqui). O corretivo
`brza-studio@a7099022850` foi reavaliado pelo Grok 4.7; ele confirmou a resolução dos três achados e não encontrou
outros com confiança >= 80.

## Veredito

Aprova. A implementação e os testes do P3 seguem D3/D6. Os três achados abaixo foram corrigidos no commit separado
`brza-studio@a7099022850c003f340a0a8cacec0d13b256c15c`, sobre `77a1cca1af2`.

### A1 — O `nextCursor` sem `--cursor` usava a página `before` final

> bug · importante · confiança 95 · → corrigido aqui

**Evidência:** a primeira revisão refez a leitura e observou em `src/cli/handlers/chat.ts:110-147` que o laço `before`
substituía `page`, e o `nextCursor` saía do cursor dessa página posterior. O D3 exige o `liveCursor` da primeira `tail`,
ou o `window.newest` dela, ou `epoch:0` (`PLN-011-design.md:273,277-278`). Em `a7099022850`, `chat.ts:111-112` captura
esse cursor antes do laço e `:147` o devolve. Os novos testes em `chat.test.ts:176-240` cobrem cursor vivo avançado na
página `before` e fallback `window.newest` da primeira `tail`; ambos preservam `nextCursor` em `e:10` e `e:9`,
respectivamente.

### A2 — A ajuda de `chat read --cursor` descrevia o cursor de linha

> desvio · sugestão · confiança 92 · → corrigido aqui

**Evidência:** `src/cli/command-scoped-flag-help.ts:6-8` dá a `chat read` a descrição `--cursor <epoch:sequence> Continue
reading from a chat journal cursor`. `src/cli/help.ts:83-88` resolve a descrição específica antes da genérica. O texto
global `Line cursor from a previous read` continua em `src/cli/flag-help-text.ts:9`; o diff corretivo não muda a ajuda
dos comandos de terminal. O Grok confirmou via `formatCommandHelp` a ajuda de ambos: `chat read` mostra epoch:sequence;
`terminal read` mantém o cursor de linha.

### A3 — Dois testes não provavam os casos pedidos no P3

> lacuna · sugestão · confiança 88 · → corrigido aqui

**Evidência:** a primeira revisão confirmou que o parse isolado de `a:b:7` não provava o argumento recebido pelo handler,
e que o reset repetido conferia saída 2, mas não `entries` e `nextCursor` em ambas as leituras. Em `a7099022850`,
`chat.test.ts:282-296` verifica `direction: 'after'`, `cursor: { epoch: 'a:b', sequence: 7 }` e `limit: 200`; `:362-403`
confere nas duas leituras do reset `cursor_compacted` as entries da `tail`, `nextCursor: 'fresh:3'` igual ao
`liveCursor` e `process.exitCode === 2`.

## Revisão corretiva

O Grok 4.7 revisou adversariamente o corretivo `a7099022850c003f340a0a8cacec0d13b256c15c` sobre `77a1cca1af2` no
worktree `/Users/andepb/Projects/brza-studio/.worktrees/pln-011-chat-cli`, branch `feat/pln-011-chat-cli`. O intervalo
tem um commit, três arquivos alterados (+104/−5), autoria e commit de Anderson Pereira Brzezinski
<brz.anderson.pereira@gmail.com>, e árvore limpa. O veredito foi “aprova”, sem achados novos com confiança >= 80.

## O que rodou e o que deu

- Worker Codex `ctx_20ff2ea3b24e`: teste alvo `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/cli/handlers/chat.test.ts src/cli/brza/chat-cursor.test.ts --maxWorkers=2` → 2 arquivos, 31/31 passed.
- Worker Codex: `pnpm verify:bundled-skill-guides`, `pnpm tc:cli`, `pnpm check:changed --base=origin/master --maxWorkers=2 --force` (22/22), `pnpm exec oxlint` nos três arquivos alterados e `pnpm exec oxfmt --check` nos arquivos de código → todos passaram.
- Grok refez o teste alvo → 31 passed; conferiu a ajuda com `formatCommandHelp`, a identidade, o diff e o estado limpo.
- Revisões do commit inicial: Antigravity → aprova sem achados; Grok → aprova com A1–A3 acima.
