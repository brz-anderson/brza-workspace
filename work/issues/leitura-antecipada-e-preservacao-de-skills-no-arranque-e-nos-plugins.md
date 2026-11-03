---
status: open
description: Os PRs #35220, #36897 e #19680 do upstream aceleram a leitura de pastas de skills em 3x a 6x, preservam a descoberta no arranque e mantêm o prefixo plugin:skill no seletor /.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
---

# Leitura antecipada e preservação de skills no arranque e nos plugins

Rastreado dos PRs abertos no upstream [`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220),
[`stablyai/orca#36897`](https://github.com/stablyai/orca/pull/36897),
[`stablyai/orca#37659`](https://github.com/stablyai/orca/pull/37659) e
[`stablyai/orca#19680`](https://github.com/stablyai/orca/pull/19680), além da issue
[`stablyai/orca#14690`](https://github.com/stablyai/orca/issues/14690).

## O problema

1. **Lentidão na varredura de skills (`#35220`):** o processo principal lia uma pasta de skill por vez de forma
   sequencial (`src/main/skills/skill-root-file-walk.ts`). Quando o host está ocupado e há múltiplas árvores de skills e
   cache de plugins, a varredura chega a levar mais de 30 segundos.
2. **Perda de descoberta no arranque (`#36897`):** a confirmação de status após o startup descartava ou refazia a
   descoberta inicial de skills.
3. **Colisão de nomes no seletor `/` (`#19680`) e colisão com skills empacotadas (`#37659`):** skills vindas de plugins
   perdiam o namespace `plugin:skill` nos pickers de comando `/`; além disso, a skill bundled `computer use` colidia com
   ferramentas externas de mesmo nome.

## O que os PRs fazem

- **PR `#35220`:** introduz `src/main/skills/skill-directory-read-ahead.ts`, disparando a leitura das próximas pastas
  enquanto a atual é processada e mantendo a ordem determinística; reduz o tempo de varredura de 3x a 6x.
- **PR `#36897`:** preserva a lista de skills descobertas no arranque após a confirmação de status.
- **PR `#19680`:** mantém o identificador qualificado `plugin:skill` nos seletores `/` do chat.
- **PR `#37659`:** renomeia a skill empacotada para `orca-computer-use` na descoberta, configurações e documentação,
  mantendo links legados e aliases do CLI para evitar quebras.

## O que fazer

Aplicar primeiro o [`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220) (4 arquivos autocontidos em
`src/main/skills/`) no `brza-studio` e acompanhar o fechamento do `#19680`, `#36897` e `#37659` para incorporação.
