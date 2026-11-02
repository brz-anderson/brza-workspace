---
name: brza-orca-coexistence
description: Decisões de 2026-10-27 sobre o BrzA Studio conviver com o Orca original (com.stablyai.orca) na mesma máquina
metadata:
  node_type: memory
  type: project
  originSessionId: 07842b4f-3613-4bd5-8ad8-3857a8a6c915
  modified: 2026-11-02T18:07:02.642Z
---

O BrzA Studio (fork do stablyai/orca) precisa rodar lado a lado com o Orca original do site. Constantes em `src/shared/brand-identity.ts`.

Decidido por Anderson em 2026-10-27:
- Muda: userData `brza-studio` (dev `brza-dev`/`brza-dev-wt`), Keychain `BrzA Studio Safe Storage`, comando `brza`, executável `BrzA Studio`, esquema `brza-studio://`, porta WS 6868/6869, raiz `%LOCALAPPDATA%\BrzA Studio`, NSIS por caminho.
- Fica Orca: `~/.orca`, hooks de usuário, `ORCA_*`, `*.onorca.dev`, identificadores de código, `orca://pair` (o app mobile do Orca só aceita esse).
- No sync da v1.4.246 (2026-11-02), Anderson decidiu (R3) que a raiz relocada do daemon no Windows passa a `%LOCALAPPDATA%\BrzA`, do tamanho de `Orca`, por causa do orçamento de caminho do conpty. O desinstalador limpa as duas raízes e não remove mais os hooks de `~/.orca`, que são compartilhados (R2).
- Linux/WSL ficam fora (ainda colidem). Agentes e textos seguem dizendo `orca`: o bundle leva um alias `orca` só para os terminais do app (Windows em `resources/terminal-bin`).
- Migração: começar limpo, sem copiar `Application Support/orca`.

**Why:** Anderson quer os dois apps abertos ao mesmo tempo sem dividir estado, mantendo merges do upstream com conflito pequeno.
**How to apply:** ao mesclar o upstream, conferir se surgiu uma cópia fixa nova de `orca` (userData, porta, esquema, exe) e apontá-la para `brand-identity.ts`. Superfície nova não coberta → perguntar a Anderson com opções e custo.
