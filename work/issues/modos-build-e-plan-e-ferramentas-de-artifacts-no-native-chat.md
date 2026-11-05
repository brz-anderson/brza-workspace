---
status: open
description: Os PRs #38286, #38248, #38251, #38253 e #38272 trazem seletores de modo Build/Plan, suporte a artifacts no chat nativo e anexos contextuais rápidos.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
---

# Modos Build e Plan e ferramentas de artifacts no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#38286`](https://github.com/stablyai/orca/pull/38286),
[`stablyai/orca#38248`](https://github.com/stablyai/orca/pull/38248),
[`stablyai/orca#38251`](https://github.com/stablyai/orca/pull/38251),
[`stablyai/orca#38253`](https://github.com/stablyai/orca/pull/38253) e
[`stablyai/orca#38272`](https://github.com/stablyai/orca/pull/38272).

## O problema

1. **Ausência de distinção entre modos Build e Plan no Chat UI (`#38286`):**
   Usuários de Claude e Codex precisavam instruir manualmente o modelo a não editar arquivos diretamente ou alternar
   prompts de sistema customizados para tarefas de planejamento. Não existia um seletor visual e persistente no composer
   de chat para definir a postura operacional do agente (somente leitura e plano de execução versus edição e construção direta).
2. **Desativação de ferramentas de Artifacts no Claude em chats nativos (`#38248`):**
   Nas sessões de Native Chat, o Claude Code era instanciado sem a variável de ambiente `CLAUDE_CODE_ARTIFACT=1`, fazendo
   com que as ferramentas de artifacts (`Artifacts`, `ArtifactComments`, `ArtifactData`) ficassem desabilitadas por padrão
   no chat nativo, ao contrário do terminal direto ou de integrações web.
3. **Fricção ao referenciar arquivos, previews de Markdown ou seleção de terminal no chat (`#38251`):**
   Para discutir trechos selecionados no terminal, documentos em visualização Markdown ou arquivos abertos no editor,
   o usuário precisava copiar e colar manualmente ou digitar o caminho completo com `@arquivo`.
4. **Falta de visibilidade do branch vinculado à conversa no composer (`#38253`):**
   Ao trabalhar com múltiplos branches e worktrees, era fácil enviar prompts a uma sessão de chat acreditando estar em um
   branch diferente do workspace onde a sessão foi iniciada.
5. **Esforço de raciocínio travado após a primeira resposta (`#38272`):**
   O seletor de esforço (thinking/reasoning effort) ficava congelado e desabilitado após o primeiro turno de conversa com
   o Claude, impedindo o usuário de elevar o esforço em turnos subsequentes mais complexos ou reduzir para economizar tokens.

## O que o upstream implementa

- **Seletor de modos Build e Plan no Chat Composer (`#38286`):**
  - Adiciona controle toggle/dropdown no rodapé do composer de chat para alternar entre `Build` (execução completa, edição
    de arquivos e comandos) e `Plan` (análise, arquitetura, proposição sem escrita destrutiva);
  - Suporta agentes Claude e Codex com persistência da preferência por conversa e entre reinicializações do app.
- **Habilitação de ferramentas de Artifacts para sessões Claude (`#38248`):**
  - Injeta `CLAUDE_CODE_ARTIFACT=1` no ambiente de execução das sessões de Native Chat, disponibilizando ferramentas de
    criação e manipulação estruturada de artifacts para o agente Claude.
- **Ação "Add to Chat" a partir do editor, markdown preview e terminal (`#38251`):**
  - Expõe menus de contexto e atalhos rápidos para enviar a seleção de texto atual do terminal, o arquivo ativo no editor
    ou o preview de Markdown diretamente como contexto anexado ao composer do chat ativo.
- **Indicador de branch de conversa abaixo do composer (`#38253`):**
  - Exibe o branch git correspondente ao workspace da conversa logo abaixo da caixa de texto do composer, prevenindo
    comandos acidentais em branches incorretos.
- **Manutenção do seletor de esforço editável (`#38272`):**
  - Mantém o dropdown de esforço do Claude interativo e mutável mesmo após o envio da primeira mensagem e recebimento da
    resposta inicial.

## O que fazer

- Integrar as melhorias de UX do composer (`#38286`, `#38251`, `#38253` e `#38272`) no `brza-studio`.
- Assegurar a propagação de `CLAUDE_CODE_ARTIFACT=1` (`#38248`) no runtime de Native Chat do `brza-studio` e nos adaptadores
  do `brza-workflow`.
