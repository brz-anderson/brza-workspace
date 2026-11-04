---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
---

# O PLN-003 P2: a CLI brza unificada e o despacho nos dois clients

Na sessão `tools-kit` de 2026-11-03, em continuidade ao [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
executou-se o passo **P2** (D1 / B1, B2, B3, B5, M23): a unificação da CLI `brza`, o despacho automático entre os dois
clients (`BrzA Studio` e `Orca`), a generalização dos comandos `tree` e `test` para qualquer repositório, e a instalação do
app via release pública do GitHub por padrão com flag `--from-source`.

## O que se implementou e testou

1. **M23 — `SHELL_SESSIONS_DISABLE=1` no `brza-run`:**
   - Adicionada a exportação `SHELL_SESSIONS_DISABLE='1'` em `packages/client/bin/brza-run` no repositório `brza-workflow`,
     eliminando saídas espúrias de sessão do zsh em terminals automatizados.
   - Teste unitário `test_run_sets_shell_sessions_disable` adicionado em `tests/cli/test_brza_scripts.py`.
   - Commitado e publicado na branch `master` de `brza-workflow` (commit `26b95fc`).

2. **B1 — CLI `brza` unificada e despacho nos dois clients:**
   - Criado o executável [brza](../../scripts/brza/brza) em Python puro (stdlib, sem dependências externas).
   - Implementada a detecção dinâmica de client em `detect_client()`:
     - 1. Variável de ambiente `BRZA_CLIENT` (`studio` ou `orca`);
     - 2. Variáveis de ambiente herdadas do client (`ORCA_USER_DATA_PATH`, `ORCA_WORKSPACE_NAME`, etc.);
     - 3. Processos em execução via `pgrep` procurando `BrzA Studio` ou `Orca`;
     - 4. Fallback padrão: `studio`.
   - Despacho hierárquico em `resolve_subcommand_executable()`:
     - Procura executável `brza-<subcomando>` no diretório local (`scripts/brza/`), em `runtime.WORKFLOW / 'bin'`, e no `PATH`.
     - Se não encontrar executável prefixado, despacha para a CLI do client ativo (`orca <subcomando>` ou CLI interna do Studio).
   - Suíte de testes dedicada em [test_brza_cli.py](../../scripts/brza/tests/test_brza_cli.py) (9 testes cobrindo todas as regras).

3. **B2 — `brza-tree` e `brza-test` generalizados:**
   - **`brza-tree`:** generalizado para operar sobre qualquer repositório git. Identifica a raiz via `git rev-parse --show-toplevel`.
     Mantém convenção `.worktrees/<nome>` com branch `feat/<nome>` em repositórios gerais, e trata repositórios de notas
     do `brza-workspace` redirecionando para o Studio.
   - **`brza-test`:** adicionada detecção automática do framework de teste (`detect_test_command()`) para repositórios genéricos
     (Rust com `cargo test`, Go com `go test`, Node/TS com `pnpm test`/`yarn test`/`npm test`, Python com `pytest`, ou `make test`).
     Quando executado em worktrees do `brza-studio`, preserva 100% da suíte especializada `vitest` + `baseline` da `origin/master`
     + conferência `check:changed`.
   - Testes unitários em [test_brza_tree.py](../../scripts/brza/tests/test_brza_tree.py) (31 testes) e
     [test_brza_test.py](../../scripts/brza/tests/test_brza_test.py) (17 testes).

4. **B5 — `brza-app install` via release do GitHub e `--from-source`:**
   - Atualizado [brza-app](../../scripts/brza/brza-app):
     - Padrão (`brza app install`): busca a release mais recente em `brz-anderson/brza-studio/releases/latest` via GitHub API,
       baixa o DMG correspondente à arquitetura (com preferência para arm64 no Apple Silicon), monta via `hdiutil attach`,
       solicita confirmação informando a versão atual instalada e a nova, substitui o `/Applications/BrzA Studio.app` usando `ditto`
       e desmonta a imagem.
     - `--from-source` (ou `--from <checkout>`): mantém o comportamento de compilar o código fonte da `origin/master` (ou do checkout
       especificado) num worktree temporário.
     - Suporta `--yes` para ignorar confirmação e `--dmg` para disponibilizar o arquivo DMG em `~/Downloads`.
   - Testes unitários atualizados em [test_brza_app.py](../../scripts/brza/tests/test_brza_app.py) (18 testes).

5. **Regressão:**
   - Suíte completa em `scripts/brza/tests/` executada com sucesso total:
     ```
     Ran 113 tests in 25.536s
     OK
     ```
