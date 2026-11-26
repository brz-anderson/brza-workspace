---
scope:
  - brza-studio
tags:
  - release
  - chat
refs:
  - PLN-011
sessions:
  - 5f596faf-ab1f-41f4-91fc-9ab63eb31c3a
---

# O sync das v1.4.263 e v1.4.278 do upstream, com o limite do bundle mobile

O pedido de Anderson, em 2026-11-18: "sync da ultima tag do upstream", repetido em 2026-11-26 depois de dois reinícios do
app. Começou na `v1.4.263` e terminou na `v1.4.278`, a tag do dia, mesclada por cima da primeira. Feito na sessão do
workstream `studio`, no worktree `brza-studio/.worktrees/sync-v1.4.263`, como no
[sync da v1.4.256](2026-11-11-sync-da-v1-4-256-do-upstream.md).

## O que se fez

Push direto na `master` do `brza-studio`, `c470dda8a46..609bfbffaba`, por fast-forward da branch `sync/v1.4.278`:
- `84bacddbd09`: "Merge tag 'v1.4.263'", com `--no-verify`.
- `1c4897ed851`: "Merge tag 'v1.4.278'", por cima do anterior, com `--no-verify`.
- `d30500644ee`: "fix: finish the v1.4.263 and v1.4.278 syncs" — rebrand, R2, typecheck, lint e ratchets.
- `9b93796a198`: os 5 vermelhos da primeira CI da branch.
- `d618b1d4245`: os achados da revisão e a R3.
- `609bfbffaba`: o limite do bundle web do mobile (R4).

**O tamanho.**
- A `v1.4.263` estava 1.766 commits à frente da `v1.4.256`. O merge deu 528 arquivos em conflito. Por script saíram 131
  só de rebrand, 195 `UD` só de rebrand, 11 catálogos e o `package.json`. Cinco `implementer` resolveram os 201
  restantes.
- A `v1.4.278` saiu uma semana depois, 2.702 commits à frente da 263. Mesclada sobre o merge da 263, deu 375 conflitos;
  sobre a `master`, daria 808. Por script saíram 86 só de rebrand, 169 `UD` só de rebrand, 8 catálogos, o `package.json` e
  o lockfile. Quatro `implementer` resolveram os 110 restantes e 73 chaves de idioma.
- Depois, dois `implementer` (conserto e varredura do rebrand), um `reviewer` e um `implementer` para os achados.

**As rodadas**, respondidas por Anderson, pelo AskUserQuestion, nesta sessão:
- **R1, 2026-11-18:**
  - decisões: "Repetir as do 256 (Recomendado)";
  - PLN-011: "Mesclar ao fim do sync (Recomendado)";
  - push: "Logo depois da CI, como no 256 (Recomendado)".
- **R2, 2026-11-26:** "Aplicar as 7 (Recomendado)":
  1. a troca de conta (P36/P79) fica portada para o journal em SQLite do upstream, com o `account-switch` no recibo de
     mutação e a divisória como item do journal;
  2. o contraste do chat fica com a fórmula do fork;
  3. o `acp-live-permission-mode.ts` do fork sai;
  4. o P72 segue o upstream (o chat que chama é reconhecido só pela CLI local);
  5. a prévia de Markdown fica com a coluna de notas do upstream (#46198);
  6. o P73 fica com o painel de workers do upstream;
  7. os helpers de teste do chat que o upstream cortou (#46786) voltam como `*.brza.test-*`, e a perda dos testes de
     identidade (launcher `brza`, `~/.brza/jira-tokens`, `switchAccount` na fiação cross-version) é aceita.
  A R2 tinha sido perguntada em 2026-11-18 e de novo em 2026-11-25; as duas vezes se perderam (o app reiniciou; Anderson
  recusou a segunda).
- **R3, 2026-11-26** (premissa da decisão 3 corrigida, achados da revisão):
  - Antigravity: "Fica o do upstream (Recomendado)" — o acesso total só no lançamento; trocar exige reiniciar o chat.
    Na R2 a sessão tinha dito que o upstream já fazia o mesmo que o fork; não fazia;
  - mobile: "Aceitar e registrar a exceção (Recomendado)" — ver abaixo;
  - bots: "Em ~/.brza/bots (Recomendado)".
- **R4, 2026-11-26:** bundle web do mobile: "Subir o limite em +128 KiB (Recomendado)".

## O que do fork caiu ou mudou

- **A troca de conta de um chat** foi refeita sobre o journal em SQLite, em
  `src/main/runtime/agent-session/brza/brza-account-switch-mutation.ts`, com duas linhas em arquivos do upstream.
- **Saíram:** o modo de permissão ao vivo do Antigravity, o tipo do agente na linha da faixa de tarefas (P73), a coluna
  de notas do fork na prévia de Markdown, a entrada do resolver de comandos na CLI empacotada e o divisor antigo
  `journal-account-switch.ts`.
- **A faixa da pergunta (P69/P70)** foi para `brza/BrzaPromptCollapse.tsx` e `brza/BrzaPromptStrip.tsx`, porque o
  upstream criou um `NativeChatStructuredPromptCard` com o mesmo nome.
- **O P79** ficou na linha de limite nova do upstream, `usage/NativeChatUsageLimitRow.tsx`.
- **O pino de conta** virou assíncrono por causa do ratchet novo de helpers bloqueantes; o `isUpdaterEnabled` e o
  arranque do Windows ganharam linhas no baseline, com o aval do revisor.
- **O bloco de código da prévia de Markdown** voltou a ficar sem fundo (P78), que tinha se perdido no CSS do upstream.
- **Os bots** ficam em `~/.brza/bots` (`BRAND_BOTS_DIR_NAME` no `brand-identity.ts`); perfis isolados seguem o upstream.
- **As credenciais novas da 278** (Google, bots) vão para `~/.brza`, pelo P75.
- **Os comparadores de mensagem** da CLI, do limite de uso e dos erros de plugin aceitam "Orca" e "BrzA Studio".
- **O repositório do fork** no menu de ajuda, na estrela e no feed de pré-release é `brz-anderson/brza-studio`; o merge
  tinha deixado `brz-anderson/orca`, que não existe.
- **A exceção do mobile (R3):** 19 chaves do catálogo do mobile (16 em `pt` e `de`) dizem "BrzA Studio", porque vêm de
  fontes compartilhadas com o desktop e os testes de paridade exigem o mesmo texto: `bots.templates.unreviewed-work.
  {firstChat,watches}`, `bots.templates.workspace-cleanup.watches`, as 10 de `bots.failures`,
  `auto.components.status.bar.tooltip.{a37e8c15d4,d1b7f509ac,cursor.expired.message}`,
  `bots.firstScreen.{projectsNone,projectsReading}` e `bots.tools.signInFailure.desktopOnly`. O resto do mobile fica Orca.
- **O limite do bundle web do mobile (R4)** é 11 MiB + 128 KiB em `verify-mobile-web-app-bundle.mjs`. A tag pura usa
  11.530.466 de 11.534.336 bytes; o fork soma ~16 KB, quase tudo dos títulos e ícones de ferramenta de
  `src/shared/native-chat/tools/brza/`.

## Os testes

- **Linha de base, na tag pura:** lint com 1 vermelho de 48/49 (`check:code-quality:changed`, falta `origin/main`). Na
  CI, a `v1.4.263` deu 1 vermelho do upstream (`relay-control-origin-failover`, rodada 44416929952) e a `v1.4.278` passou
  inteira (rodada 45864175950).
- **Na branch, pela CI:**
  - em `d30500644ee`, rodada 45870597257: 9 shards e 6 arquivos vermelhos. Cinco eram do sync (rebrand em testes, o
    fundo do bloco de código, o teste do padrão da retomada automática) e foram consertados em `9b93796a198`; o
    `structured-worker-slow-start` é instável e passou 6 vezes isolado;
  - em `d618b1d4245`, rodada 45876221868: verde.
- **No HEAD, no Mac:** typecheck com 0 erros; lint igual à tag pura; os quatro gates de idioma verdes; `pnpm build:mac
  --dmg` com exit 0 e a identidade BrzA (`com.brzanderson.brzastudio`, esquema `brza-studio`).
- **Um `implementer` rodou a suíte inteira uma vez por engano** (cerca de 5 min, 2 workers): um glob vazio no zsh deixou a
  lista de arquivos vazia. Os briefs seguintes pedem `bash -c` e lista conferida.

## O PLN-011

Pela R1, a `master` nova foi mesclada em `feat/pln-011-chat-cli`, com o merge `02e800c8d63` (`--no-verify`) já no origin.
Doze conflitos, todos da reorganização de `src/cli` do upstream (`handlers/` → `agents/`, `workspaces/`, `discovery/`,
`dispatch/`). O `chat list|read|send` foi para `src/cli/agents/`, ao lado do `chat rename` do upstream; o
`agentSession.send` entrou no `SESSION_EVIDENCE_METHODS` do upstream. Typecheck com 0 erros; `src/cli` com 291 testes
verdes. O C1 precisa de um app de dev recompilado dessa branch.

## O que ficou

- **A conferência no app**, com Anderson, pelo DMG `~/Downloads/brza-studio-1.4.278-macos-arm64.dmg` (sha256
  `00c67f5bde5ca6eb44ff45b6f9aeb079a7fa6814065a56e2fd694b3ae30df57d`). O roteiro do sync da v1.4.256 vale, mais a troca de
  conta (a divisória "Account switched"), a faixa da pergunta, o Antigravity reiniciando para acesso total e os bots em
  `~/.brza/bots`.
- **O PR #1 do `brza-studio`** foi avaliado, fechado e refeito na `master`: [O PR #1 do brza-studio, fechado e refeito na master](2026-11-26-pr-1-do-brza-studio-fechado-e-refeito-na-master.md).
- **Os 267 commits do `upstream/main` depois da `v1.4.278`** entram no próximo sync.

## Fora do workspace

- **`pnpm install` nos worktrees do sync e da base**, e `pnpm -C mobile install` na `base-v1.4.278`.
  - **Onde:** o store global do pnpm, `~/Library/pnpm`.
  - **Risco:** nenhum para os outros checkouts; o store só cresce.
  - **Estado:** ativo.
  - **Como desfazer:** `pnpm store prune`.
- **As tags `v1.4.263` e `v1.4.278` e a branch `sync/v1.4.278` no origin (`brz-anderson/brza-studio`)**, para a CI, e
  quatro rodadas do `node-next-compat.yml` disparadas à mão.
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** `git push origin --delete sync/v1.4.278` e `git push origin :refs/tags/<tag>`.
- **O DMG em `~/Downloads/brza-studio-1.4.278-macos-arm64.dmg`.**
  - **Risco:** nenhum; é build local assinado ad hoc.
  - **Estado:** ativo.
  - **Como desfazer:** apagar o arquivo.
- **Os worktrees `sync-v1.4.263`, `base-v1.4.263` e `base-v1.4.278` do `brza-studio`**, criados e removidos no sync; as
  branches `sync/*` ficam.
- **Cópia do brief e das rodadas** em `~/Library/Application Support/brza-studio/chat-scratch/d2b1b1fb0ad353b4ca07993e8c8d65cd/sync-278/`,
  porque o scratch em `/private/tmp` se perdeu duas vezes com os reinícios.
  - **Risco:** nenhum.
  - **Estado:** ativo.
  - **Como desfazer:** apagar a pasta.

## Custo da tarefa

Corrido 188 h 29 min — agente 54 min, quem pediu 3 h 10 min, pausa 184 h 25 min · US$ 104,52 (turnos 28,26, subagentes 76,26) · CPU 4 min do `claude` e 2 h 58 min dos comandos, RSS até 556 MB · 26 turnos, 1 sessão · dividida com 1 outro worklog do commit · até 17:03 de 2026-11-26, pelo `brza note commit`
