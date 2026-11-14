---
scope:
  - brza-studio
  - brza-workflow
  - brza-cli
description: Os PRs #42410, #42360, #42349 e #42347 trazem separação de builds descartáveis de chat, comando de limpeza, estúdio de temas via CLI e herança de cores.
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

## Impacto no BrzA Studio

- **Higiene de Armazenamento:** Elimina o inchaço indefinido da pasta de perfil decorrente de múltiplos builds temporários de agentes, mantendo o histórico de relatórios intacto.
- **Autonomia em Design:** Agentes e desenvolvedores ganham ferramental via CLI para ajustar tokens visuais e testar paletas de cores e contraste ao vivo.
