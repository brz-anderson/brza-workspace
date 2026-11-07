---
name: logi-options-disk
description: Onde ficam as configurações do Logi Options+ / Actions Ring no macOS e quais fontes de doc responderam
metadata:
  type: reference
---

- `~/Library/Application Support/LogiOptionsPlus/settings.db` (SQLite, tabela `data`, 1 BLOB JSON; copiar com -wal/-shm para o scratch, `writefile()` do sqlite3 extrai). Botões do mouse ficam na chave `profile-<uuid>.assignments`; tem serial/udid.
- Ring/Smart Actions: `~/Library/Application Support/Logi/LogiPluginService/Applications/Loupedeck72/<bundle id>/Profiles/<id>/ProfileInfo.json` (texto, 8 controles por página). `Applications.Backups/*.zip` é backup local do Plugin Service.
- Doc oficial que respondeu: hub.sync.logitech.com (backup na nuvem, MX Master 4), support.logi.com/hc/articles/14307858722327 (ações de Smart Action), logitech.github.io/actions-sdk-docs. WebFetch de support.logi.com/34377296585111 só trata de Easy-Switch.
- A WebSearch não abre artigos do support.logi.com que o WebFetch lê; páginas de "Actions Ring" da Logitech são marketing, sem número de slots.
