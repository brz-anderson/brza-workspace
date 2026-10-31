---
scope:
  - workspace
  - brza-studio
---

# O PLN-004: as sondas da R6 e o Desenho do Codex e do agy

A continuação do
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md),
na sessão `workspace`, depois da R6 de 2026-10-30. O dia anterior está em
[O PLN-004: a abertura do Codex e do agy no fluxo](2026-10-30-pln-004-a-abertura-do-codex-e-do-agy-no-fluxo.md).

## O que se fez

- **As sondas da R6.1**, pelo `collector`, num repositório descartável com `.codex/` e `.agents/` ligados por symlink,
  como o `brza tree` faria; o detalhe está no scratch da sessão, em `pln-004-sondas-r6.md`.
  - **O `agy` segue o symlink** da skill, da regra, do agente e do `hooks.json`, e o hook dispara em worktree não
    confiado; o cwd do hook é `<worktree>/.agents`. Acionar uma skill no `agy` é ler o `SKILL.md`; não há
    `${CLAUDE_SKILL_DIR}`.
  - **O `--settings '{"trustedWorkspaces":[…]}'`** do `agy` vale só para a sessão, e o `--sandbox` é aceito junto; o
    efeito isolado do `--sandbox` ficou sem medir, porque o sandbox já vinha ligado pelo `settings.json`.
  - **O `agy` 1.4.12 não dá busca nem leitura de URL ao agente principal**; os nomes velhos (`grep_search`,
    `find_by_name`, `list_dir`, `read_url_content`) só chegam ao subagente que os nomeia no `tools:`.
  - **O Codex carrega o `.codex/agents` por symlink** em `workspace-write`; o hook por symlink, sem confiança, é pulado
    em silêncio, e falta o `/hooks` de Anderson.
  - **O app:** o chat do Codex lê o `agentCmdOverrides.codex` como executável único e roda `<override> … app-server`
    (`brza-studio/src/main/codex/codex-structured-launch-resolution.ts:85`); o chat Antigravity é um servidor ACP
    gerenciado, que não é o `agy` e ignora o override (`brza-studio/src/main/acp/acp-launch-specs.ts:261-265`).
- **As memórias da sessão:** a edição renderizada, com o removido em callout, e o `---` depois de todo bloco de arquivo.
- **O `/hooks` de Anderson**, numa sessão Codex interativa no worktree da sonda, com o prompt que chama o `papel`. O
  papel carregou pelo `.codex/agents` em symlink e respondeu (rollout `01a18ff5-d9e7-…`), mas o espião do hook não
  gravou nada, e o `~/.codex/config.toml` não ganhou `hooks.state` para o `sondas2`.
- **A rodada 7**, no chat: o `codex-brza` tira o `--approve-for-me`; a memória do papel por caminho relativo; o
  `functions -c` no bloco BrzA do shell; um pedido à sessão do `studio` para ligar a issue ao plano.
- **A rodada 8**, no chat: a captura do `/hooks` mostrou só a tela do `PreToolUse`, com o hook do Orca, e não decidiu;
  o `brza tree` copia o `.codex/hooks.json`, e o resto segue por symlink; o scratch do Codex em
  `$TMPDIR/codex-scratch/<id da sessão>`.

## O que ficou

- **O Desenho**: o `designer` aplica a R6 a R8 ao rascunho, e o texto vai à aprovação na mensagem antes de ir a
  `PLN-004-design.md`.

## Fora do workspace

- **A confiança do segundo repositório das sondas, no `~/.codex/config.toml:268-270`**: o `codex exec` em
  `workspace-write` gravou `[projects."…/chat-scratch/f9a99dc712d9b2b01373911a721bf604/sondas2/repo"] trust_level =
  "trusted"`.
  - Risco: nenhum além de uma entrada morta quando o scratch sumir.
  - Estado: ativo.
  - Como desfazer: apagar as linhas.
- **Os rollouts das sondas**, em `~/.codex/sessions/2026/10/31/` — `01a18fe8-234a-7ad2-a8fc-02e0d7eae4e6` e
  `01a18fe8-95be-7ed2-a1c3-3f6891b33bfc` —, com os índices sqlite do Codex.
  - Risco: aparecem no histórico do Codex e numa medição que varra os rollouts.
  - Estado: ativo.
  - Como desfazer: `codex delete <id>` em cada um.
- **Os rollouts da sessão do `/hooks`**, em `~/.codex/sessions/2026/10/31/` — `01a18ff5-d9e7-7aa0-a82f-ddb0bf3c3ea0`
  e o do `papel`, `01a18ff7-6cc8-7c63-a445-262354977e72`.
  - Risco: os mesmos dos rollouts das sondas.
  - Estado: ativo.
  - Como desfazer: `codex delete <id>` em cada um.
- **Os transcripts das sondas do `agy`**, em `~/.gemini/antigravity-cli/brain/` — `11b4142a…`, `900bdb80…`,
  `e85791d9…`, `2f5ad589…`, `3d98786c…` e `0b2acc31…`.
  - Risco: aparecem no histórico do `agy` e numa medição que varra o `brain/`.
  - Estado: ativo.
  - Como desfazer: apagar os seis diretórios.
- **O plugin `skill-creator@claude-plugins-official` no escopo local do worktree `workspace`**, pelo
  `claude plugin install --scope local`: a versão `a7ba5b93db0c` no `~/.claude/plugins/cache/` e a entrada `local`, com
  o `projectPath` do worktree, no `~/.claude/plugins/installed_plugins.json`. O CLI gravou o `enabledPlugins` no
  `.claude/settings.local.json` do checkout da `master`; a entrada foi movida para o do worktree, e o da `master`, que
  só tinha ela, apagado.
  - Risco: só as sessões do worktree `workspace` carregam o plugin. O `brza note memory-setup` não apaga o
    `enabledPlugins`: o `set_auto_memory`, em `scripts/brza/brza_runtime.py:186`, relê o `settings.local.json`, troca
    só o `autoMemoryDirectory` e regrava as outras chaves.
  - Estado: ativo.
  - Como desfazer: `claude plugin uninstall skill-creator@claude-plugins-official --scope local` no worktree, e
    conferir que o `enabledPlugins` saiu do `.claude/settings.local.json` dele.
