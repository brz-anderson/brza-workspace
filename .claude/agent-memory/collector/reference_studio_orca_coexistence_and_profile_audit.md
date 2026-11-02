---
name: studio-orca-coexistence-and-profile-audit
description: Onde achar rápido os restos da Orca em runtime, a config de build/updater e o formato do perfil do BrzA Studio; armadilhas de shell e de leitura do perfil real
metadata:
  type: reference
---

Atalhos para levantamentos do tipo "o que ainda é Orca e quebra em runtime" e "migração do perfil" no `~/Projects/brza-studio`.

- **Identidade/coexistência**: `src/shared/brand-identity.ts` é o índice (userData, comando, esquema, portas). `grep BRAND_` mostra quem usa. O que NÃO passa por ali é o que dá achado: `~/.orca` (credenciais, hooks, `host-settings`), `ORCA_*`.
- **Build/updater**: `config/electron-builder.config.cjs` (publish ~L775, mac ~L589, `ORCA_MAC_TEAM_ID` L238); `src/main/updater/updater-enabled.ts` (guarda por sufixo `-local.<ts>.<commit>`), `updater-setup.ts` (feed), `updater-nudge.ts`/`updater-changelog.ts` (ainda `onorca.dev`). `config/dev-app-update.yml` é morto. Evidência de runtime do updater ligado: breadcrumb `updater_macos_installer_scheduling_configured` em `userData/logs/main.trace.ndjson`.
- **Perfil real** (`~/Library/Application Support/brza-studio`): `orchestration.db` (user_version 46), `agent-session-journal.db` (user_version 4, mas linhas `v:5 kind:outcomes` são o ponto sem volta), `profiles/local-default/profile-state.db` (tabela `profile_state_documents(domain,payload,...)`: settings em `domain='settings'`). Backups manuais `brza-studio.bak-1.4.242*` no mesmo diretório; o app guarda só 5 backups horários do profile-state.
- **Ler banco do perfil**: copiar `.db`+`-wal`+`-shm` para o scratch e `sqlite3 -readonly`; cópia de db WAL sem wal só abre com `sqlite3 "file:x.db?mode=ro&immutable=1"`. Apagar a cópia no fim (tem histórico de chat). Keychain: `security find-generic-password -s "<nome> Safe Storage"` sem `-w` mostra só metadado (Orca = `orca Safe Storage`, BrzA = `BrzA Studio Safe Storage`).
- **Catálogos i18n**: `src/renderer/src/i18n/locales/*.json` (aninhado; achatar antes de comparar chaves). Faltas em `pt` são ~273 e vêm do upstream, não do sync.
- **Armadilha de shell (zsh)**: `git show $R:caminho` quebra (`$R:c` vira modificador); use `${R}:caminho` ou aspas `"${t}:caminho"`.
- **Armadilha de permissão**: imprimir valor de `ORCA_PAIRING_CODE`/token é barrado pelo classificador; ler só nomes de chave e tamanhos.
- **Fonte velha**: `/private/tmp/pln-003-plugins-levantamento.md` já cobre o sistema de plugins em profundidade (frames, aprovação, worker sem sandbox); não refazer.
