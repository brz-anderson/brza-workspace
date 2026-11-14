---
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
description: Os PRs #42479, #42418, #42410, #42360, #42349 e #42347 trazem retenção de diários, resiliência de cache de uso, separação de builds temporários e estúdio de temas via CLI.
opened: 2026-11-14
status: open
priority: high
tags:
  - tooling
  - infra
  - design
---

# Isolamento de artefatos temporários de chat e estúdio de temas via CLI

Rastreia melhorias críticas de ciclo de vida de arquivos em chats de agentes, comandos de limpeza de armazenamento em disco e capacidades de criação e inspeção em tempo real de temas visuais via CLI e skills no BrzA Studio / Orca:

1. **Separação de builds descartáveis de agentes dos artefatos persistentes de chat ([PR #42410](https://github.com/stablyai/orca/pull/42410) — resolve [Issue #42404](https://github.com/stablyai/orca/issues/42404)):**
   - Introduz a variável de ambiente `ORCA_CHAT_TEMP_DIR` ao lado de `ORCA_CHAT_SCRATCH_DIR` nas sessões de Native Chat com a skill de recursos visuais.
   - Permite que agentes executem testes, compilações pesadas e clonagem de pacotes em um diretório temporário isolado descartável, preservando os artefatos e relatórios intencionais em `ORCA_CHAT_SCRATCH_DIR`.
   - Implementa rotina de limpeza segura (`reclaim-chat-temp`) que varre e remove pastas temporárias após o encerramento do processo e ausência de alterações por 7 dias, protegendo diretórios com metadados Git, links simbólicos ou dados ilegíveis.
   - Disponibiliza o comando `storage:overview` para análise comparativa de bytes alocados e referenciados com contabilidade de hardlinks.
2. **Estúdio de temas em tempo real via CLI e skills ([PR #42360](https://github.com/stablyai/orca/pull/42360)):**
   - Adiciona o grupo de comandos `orca theme` à CLI e atualiza a skill `orca-cli` com guias de autoria de temas.
   - Permite que agentes e desenvolvedores gerem rascunhos de temas, pré-visualizem mudanças instantaneamente na janela do Studio sem reiniciar, e executem verificações automáticas de contraste e conformidade de tokens de cores (OKLCH).
   - Facilita a criação e customização de temas diretamente durante sessões interativas de design de UI.
3. **Cor de seleção do editor de código configurável por tema ([PR #42349](https://github.com/stablyai/orca/pull/42349)):**
   - Expõe tokens de tema para estilizar explicitamente a cor de destaque e seleção de texto no editor de código integrado, harmonizando a seleção com a paleta do tema ativo.
4. **Herança do tema da aplicação em janelas pop-out ([PR #42347](https://github.com/stablyai/orca/pull/42347)):**
   - Assegura que janelas destacadas (*pop-out windows*, como terminais desanexados e visualizadores auxiliares) sigam imediatamente o tema ativo da janela principal da aplicação, evitando discrepâncias visuais.
5. **Retenção indefinida de arquivos de diário e WAL de chat ([PR #42479](https://github.com/stablyai/orca/pull/42479)):**
   - Isenta arquivos de diário (`.journal`, WAL, SHM) e bancos relacionais locais da política de expiração automática de 7 dias de arquivos temporários, evitando corrupção de sessões arquivadas e mantendo a integridade histórica.
6. **Descarte e regeneração automática de caches corrompidos de uso de tokens ([PR #42418](https://github.com/stablyai/orca/pull/42418) — resolve [Issue #42413](https://github.com/stablyai/orca/issues/42413)):**
   - Ao detectar entradas malformadas ou corrompidas no cache de leitura de fontes de uso (`readUsageSourceCache`), o sistema descarta com segurança a entrada inválida e a reconstrói em vez de propagar exceções e travar permanentemente as varreduras de telemetria em Codex, OpenCode e Muse.

## Impacto no BrzA Studio

- **Higiene de Armazenamento:** Elimina o inchaço indefinido da pasta de perfil decorrente de múltiplos builds temporários de agentes, mantendo o histórico de relatórios intacto.
- **Resiliência de Telemetria e Armazenamento:** Preserva diários locais SQLite sem deleções prematuras (`#42479`) e previne travamentos no rastreamento de uso de cotas por caches corrompidos (`#42418`).
- **Autonomia em Design:** Agentes e desenvolvedores ganham ferramental via CLI para ajustar tokens visuais e testar paletas de cores e contraste ao vivo.
