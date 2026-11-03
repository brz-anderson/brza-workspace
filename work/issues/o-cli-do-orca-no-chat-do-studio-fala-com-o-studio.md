---
status: open
description: O CLI do Orca, rodado de dentro de uma sessão do BrzA Studio, fala com o Studio, porque o ORCA_USER_DATA_PATH herdado escolhe o app; a detecção do client pela R2.1 do PLN-003 erra do mesmo jeito.
scope:
  - workspace
  - brza-studio
opened: 2026-11-03
tags:
  - tooling
---

# O CLI do Orca no chat do Studio fala com o Studio

Achado no spike do C5 do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), em 2026-11-03, ao
carregar o plugin no Orca a partir do chat do BrzA Studio.

## O que falhou

Com o Orca `1.4.246` aberto (pid 6802), o CLI dele respondeu como o BrzA Studio:

```bash
"/Applications/Orca.app/Contents/Resources/bin/orca" status --json
```

```text
"pid": 2819,
"appVersion": "1.4.246-alpha.1",
```

O ambiente do chat traz `ORCA_USER_DATA_PATH=/Users/andepb/Library/Application Support/brza-studio`,
`ORCA_CLI_COMMAND` e `ORCA_CLI_BIN_DIR` do Studio, e o CLI segue o `ORCA_USER_DATA_PATH` antes do próprio app. Com
`env -i HOME=… PATH=…`, o mesmo comando achou o Orca (`"pid": 6802`, `"appVersion": "1.4.246"`) e o `plugin dev load`
foi para ele.

## Por que importa

- **A R2.1 do PLN-003** acha o client "pelo env do app, depois `BRZA_CLIENT`, depois o app vivo". Numa sessão aberta
  pelo Studio, o env sempre aponta o Studio, mesmo quando o pedido é para o Orca. O B1 e o `--client studio|orca|all`
  do B3 precisam limpar ou sobrescrever o `ORCA_*` ao chamar o CLI do outro app.
- **Erro silencioso:** o comando não falha; ele age no app errado. O `plugin dev load` de um teste "no Orca" teria
  gravado o `devPluginPaths` do Studio.

## O que fazer

Levar ao Desenho do PLN-003, no B1: o `brza` que chama o CLI de um client passa a ele só o env daquele client. Conferir
no código do CLI a ordem de resolução do app (`ORCA_USER_DATA_PATH` contra o binário que roda).
