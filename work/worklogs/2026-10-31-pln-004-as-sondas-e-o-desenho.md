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

## O que ficou

- **O `/hooks` de Anderson**, no worktree da sonda, para ver se o hook do Codex por symlink roda.
- **A rodada 7**, no chat: o `--approve-for-me` do app, a memória do papel por caminho relativo, a função da Fixfy no
  shell e a issue do `studio`.

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
- **Os transcripts das sondas do `agy`**, em `~/.gemini/antigravity-cli/brain/` — `11b4142a…`, `900bdb80…`,
  `e85791d9…`, `2f5ad589…`, `3d98786c…` e `0b2acc31…`.
  - Risco: aparecem no histórico do `agy` e numa medição que varra o `brain/`.
  - Estado: ativo.
  - Como desfazer: apagar os seis diretórios.
