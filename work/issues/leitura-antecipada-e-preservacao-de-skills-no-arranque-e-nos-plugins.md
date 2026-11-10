---
status: open
description: Os PRs #40812, #40788, #40214, #35220 trazem hashes estáveis de pacotes, hints de argumentos no picker, leitura antecipada e preservação no arranque.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
---

# Leitura antecipada e preservação de skills no arranque e nos plugins

Rastreado dos PRs abertos no upstream [`stablyai/orca#40812`](https://github.com/stablyai/orca/pull/40812),
[`stablyai/orca#40788`](https://github.com/stablyai/orca/pull/40788) (resolve Issue [`#40785`](https://github.com/stablyai/orca/issues/40785)),
[`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) (resolve Issue [`#40181`](https://github.com/stablyai/orca/issues/40181)),
[`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220),
[`stablyai/orca#36897`](https://github.com/stablyai/orca/pull/36897),
[`stablyai/orca#37659`](https://github.com/stablyai/orca/pull/37659) e
[`stablyai/orca#19680`](https://github.com/stablyai/orca/pull/19680), além das issues
[`stablyai/orca#14690`](https://github.com/stablyai/orca/issues/14690),
[`stablyai/orca#37875`](https://github.com/stablyai/orca/issues/37875) e
[`stablyai/orca#32573`](https://github.com/stablyai/orca/issues/32573).

## O problema

1. **Lentidão na varredura de skills (`#35220`):** o processo principal lia uma pasta de skill por vez de forma
   sequencial (`src/main/skills/skill-root-file-walk.ts`). Quando o host está ocupado e há múltiplas árvores de skills e
   cache de plugins, a varredura chega a levar mais de 30 segundos.
2. **Perda de descoberta no arranque (`#36897`):** a confirmação de status após o startup descartava ou refazia a
   descoberta inicial de skills.
3. **Colisão de nomes no seletor `/` (`#19680`) e colisão com skills empacotadas (`#37659`):** skills vindas de plugins
   perdiam o namespace `plugin:skill` nos pickers de comando `/`; além disso, a skill bundled `computer use` colidia com
   ferramentas externas de mesmo nome.
4. **Falta de ponto de contribuição para subagentes e skills em plugins (`#37875`, `#32573`):** plugins modernos
   (ex.: ecossistemas de Claude Code e Cursor) empacotam definições de subagentes (`agents/*.md`) junto às suas skills,
   disparando-os pelo nome de tipo do subagente. No runtime do app, `contributes` não aceitava subagentes nem entregava
   skills completas, quebrando plugins que delegam tarefas a subagentes específicos.
5. **Classificação falsa de bundled skills como editadas na presença de arquivos sidecar (`#40214`, resolve `#40181`):**
   Skills empacotadas distribuem apenas `SKILL.md`. O algoritmo de classificação em `bundled-skill-classification.ts` tratava
   o arquivo como atual ou lançado apenas quando `SKILL.md` era a única entrada na pasta. Como ferramentas como Codex geram
   arquivos auxiliares no mesmo diretório (ex.: `agents/openai.yaml` ou scripts locais), o digest do diretório não batia e um
   `SKILL.md` idêntico em bytes passava a ser classificado como `edited`, impedindo atualizações silenciosas automáticas.
6. **Inconsistência no hash de identidade de pacotes de skills por caminhos não ordenados (`#40812`):**
   O cálculo de identidade de pacotes de skills gerava hashes discrepantes para o mesmo conjunto de arquivos dependendo
   da ordem em que o sistema de arquivos retornava os manifestos, disparando alertas falsos de "skill out of date" e invalidações espúrias de cache.
7. **Omissão de dicas de argumentos (argument-hints) de skills no seletor do Native Chat (`#40788`, resolve `#40785`):**
   Ao abrir o picker `/` no chat para invocar uma skill (ex.: `/review`, `/test`), a interface descartava os metadados de
   `argument-hint` definidos no Claude Code, deixando o usuário sem saber quais parâmetros a ferramenta esperava.

## O que os PRs fazem

- **PR `#40812`:** ordena deterministamente os caminhos completos dos manifestos antes de computar o hash de identidade do pacote de skills, evitando discrepâncias entre sistemas de arquivos.
- **PR `#40788` (resolve `#40785`):** preserva e renderiza `argument-hint` no dropdown de seleção do Native Chat para skills do Claude Code e ferramentas de sessão.
- **PR `#40214` (resolve `#40181`):** compara o digest atual e os digests lançados especificamente para o arquivo `SKILL.md`,
  mesmo quando a pasta contém entradas adicionais. Um `SKILL.md` cujo digest não coincida com nenhum continua sendo classificado
  como `edited` apenas se o nome no frontmatter bater com a skill bundled.
- **PR `#35220`:** introduz `src/main/skills/skill-directory-read-ahead.ts`, disparando a leitura das próximas pastas
  enquanto a atual é processada e mantendo a ordem determinística; reduz o tempo de varredura de 3x a 6x.
- **PR `#36897`:** preserva a lista de skills descobertas no arranque após a confirmação de status.
- **PR `#19680`:** mantém o identificador qualificado `plugin:skill` nos seletores `/` do chat.
- **PR `#37659`:** renomeia a skill empacotada para `orca-computer-use` na descoberta, configurações e documentação,
  mantendo links legados e aliases do CLI para evitar quebras.
- **Issues `#37875` e `#32573`:** propõem expor pontos de contribuição declarativos `skills` e `subagents` no manifesto
  do plugin para carregar arquivos de agentes e skills embutidos.

## O que fazer

1. Adotar a correção de classificação de bundled skills do [`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) para não bloquear atualizações por presença de arquivos sidecar (`agents/openai.yaml`).
2. Aplicar o [`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220) (4 arquivos autocontidos em
   `src/main/skills/`) no `brza-studio`, incorporar o `#37659` e preparar o sistema de plugins para registrar subagentes
   nativos entregues por pacotes de terceiros.
3. Adotar a ordenação determinística de caminhos no cálculo de identidade de pacotes de skills (`#40812`).
4. Exibir dicas de argumentos (`argument-hint`) no seletor de comandos/skills do chat (`#40788`).
