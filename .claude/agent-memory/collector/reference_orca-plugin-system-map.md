---
name: reference-orca-plugin-system-map
description: Onde mora cada assunto do sistema de plugins do Orca no clone brza-studio (docs, código, skill, upstream) e atalhos que poupam leitura
metadata:
  type: reference
---

Mapa conferido em 2026-11-02 (base v1.4.246; `upstream/main` busca em `~/Projects/brza-studio`, remoto `upstream`).

- **Docs**: `docs/reference/plugin-{authoring,manifest,host-api,isolated-frames,declarative-ui,catalog,listing-policy,themes,theme-tokens,syntax}.md`. `manifest`, `catalog`, `host-api` são GERADOS (`pnpm generate:plugin-schemas`) e têm coluna `Since`; `authoring` é a narrativa. Para (B) use `git diff v1.4.246 upstream/main -- docs/reference/plugin-*.md`: o diff é o jeito mais curto de listar recursos novos.
- **Skill**: `skills/orca-plugin-authoring/SKILL.md` é só um stub; o guia real é `skill-guides/orca-plugin-authoring.md` + `skill-guides/orca-plugin-authoring/references/*.md` (cli/workflow/recipes/testing/manifest/host-api/events/components). `recipes.md` tem os exemplos concretos de hooks, status bar, editor rico (só em upstream). Embutido no binário via `src/cli/bundled-skill-guides.ts`.
- **Código**: ponto de entrada `src/main/startup/main-process-plugins.ts`; `src/main/plugins/{catalog,installation,panels,workers,view,contributions}`; `src/shared/plugins/*`; UI em `src/renderer/src/components/plugins/` e `settings/PluginsSettingsSection.tsx`; CLI em `src/cli/plugin-*` e `src/cli/plugin-handler-groups.ts`. (B) hooks em `src/main/plugins/hooks/` e README em `src/main/agent-hooks/README.md` (tabela por agente do PreToolUse).
- **Serviços externos**: `onorca.dev/plugins/{kill-list,stats}.json` (só empacotado), catálogos Git `stablyai/orca-plugins` e `orca-community-plugins` (`marketplace.ts:228`, `plugin-install-link.ts:14`), telemetria `src/main/telemetry/plugin-install-telemetry.ts` (só build oficial com chave).
- **Fork**: `src/shared/brand-identity.ts` (CLI `brza`, esquema `brza-studio://`); `git diff v1.4.246 master -- src/main/plugins src/shared/plugins` mostra só rebrand de strings. Testes de marca de plugin em `src/shared/plugins/catalog/brza/`.
- **Gate**: `pluginHostVersion` (`src/shared/plugins/installation/plugin-host-version.ts`) — plugin com `engines.orca >=1.4.248` não carrega no fork na base 1.4.246.

Armadilhas desta máquina:
- `git grep` / `grep -r --include=*.ts` no zsh: glob sem aspas dá "no matches found" e aborta o comando; use `--include='*.ts'` ou `git grep ... -- 'src/**'`.
- `echo ====` no zsh falha ("= not found"); use `echo "----"`.
- O app instalado em `/Applications/BrzA Studio.app` pode estar numa versão mais nova que a dita no pedido (estava `1.4.246-alpha.1`, não 1.4.242): confira com `defaults read ".../Contents/Info.plist" CFBundleShortVersionString`.
- `upstream/main:package.json` diz `1.4.214` (placeholder, não serve de régua); a versão futura vem dos `Since` da doc (1.4.248).
- `/private/tmp/plugins-orca` já existe como dir de scratch vazio no início; o Write grava nele sem problema.
