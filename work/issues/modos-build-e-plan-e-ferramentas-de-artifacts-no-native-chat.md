---
status: open
description: Os PRs #43606, #38286, #38248, #38574, #38498 e as issues #43603, #43602 trazem modo Plan no OpenCode, visibilidade de prosa prévia a perguntas e modos Build/Plan.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#43606`](https://github.com/stablyai/orca/pull/43606) (resolve Issue [`#43603`](https://github.com/stablyai/orca/issues/43603)),
além da issue [`stablyai/orca#43602`](https://github.com/stablyai/orca/issues/43602),
[`stablyai/orca#38574`](https://github.com/stablyai/orca/pull/38574),
[`stablyai/orca#38498`](https://github.com/stablyai/orca/pull/38498),
[`stablyai/orca#38495`](https://github.com/stablyai/orca/pull/38495),
[`stablyai/orca#38510`](https://github.com/stablyai/orca/pull/38510),
[`stablyai/orca#38286`](https://github.com/stablyai/orca/pull/38286),
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
3. **Ausência de chats nativos na busca e lista de recentes do Cmd+J (`#38574`):**
   O seletor rápido universal (Cmd+J) e a busca de novas abas montavam sua lista de abas a partir de uma enumeração rígida
   de tipos (terminal, editor, diff), omitindo completamente sessões abertas de Native Chat.
4. **Falta de visibilidade prévia de modelo e esforço em chats de pasta (`#38498`):**
   Ao iniciar uma sessão de chat em um folder workspace, os controles de seleção de modelo e nível de esforço de raciocínio
   só apareciam após a submissão do primeiro prompt.
5. **Links de arquivo inertes em cartões de aprovação de plano (`#38495`, `#38510`):**
   Arquivos referenciados nos cartões de aprovação de planos (tanto no Native Chat desktop quanto no mobile) eram renderizados
   como texto estático em vez de links clicáveis que abrem o arquivo diretamente no editor.
6. **Fricção ao referenciar arquivos, previews de Markdown ou seleção de terminal no chat (`#38251`):**
   Para discutir trechos selecionados no terminal, documentos em visualização Markdown ou arquivos abertos no editor,
   o usuário precisava copiar e colar manualmente ou digitar o caminho completo com `@arquivo`.
7. **Falta de visibilidade do branch vinculado à conversa no composer (`#38253`):**
   Ao trabalhar com múltiplos branches e worktrees, era fácil enviar prompts a uma sessão de chat acreditando estar em um
   branch diferente do workspace onde a sessão foi iniciada.
8. **Esforço de raciocínio travado após a primeira resposta (`#38272`):**
   O seletor de esforço (thinking/reasoning effort) ficava congelado e desabilitado após o primeiro turno de conversa com
   o Claude, impedindo o usuário de elevar o esforço em turnos subsequentes mais complexos ou reduzir para economizar tokens.
9. **Ausência de suporte ao modo Plan no OpenCode em chat nativo (`#43606`, resolve `#43603`):**
   Usuários do OpenCode e OpenCode2 não tinham acesso ao comando `/plan` nem ao chip de alternância entre Plan e Build
   dentro do Native Chat estruturado, restringindo o fluxo de planejamento aos terminais TUI.
10. **Ocultação de prosa e rascunhos redigidos antes de perguntas interativas (`#43602`):**
    Quando um agente (como o Claude Code) emite explicações, comparações ou estimativas textuais e logo em seguida invoca
    `AskUserQuestion` no mesmo turno, a interface do chat oculta o texto precedente enquanto o card da pergunta está aberto,
    privando o desenvolvedor do contexto necessário para tomar a decisão.

## O que o upstream implementa

- **Seletor de modos Build e Plan no Chat Composer (`#38286`):**
  - Adiciona controle toggle/dropdown no rodapé do composer de chat para alternar entre `Build` (execução completa, edição
    de arquivos e comandos) e `Plan` (análise, arquitetura, proposição sem escrita destrutiva);
  - Suporta agentes Claude e Codex com persistência da preferência por conversa e entre reinicializações do app.
- **Habilitação de ferramentas de Artifacts para sessões Claude (`#38248`):**
  - Injeta `CLAUDE_CODE_ARTIFACT=1` no ambiente de execução das sessões de Native Chat, disponibilizando ferramentas de
    criação e manipulação estruturada de artifacts para o agente Claude.
- **Integração de Native Chats no Cmd+J e busca de abas (`#38574`):**
  - Inclui abas de chat nativo na paleta de recentes ordenada por último foco, pesquisa por título e ícone do provedor.
- **Exibição antecipada de modelo e esforço antes do primeiro turno (`#38498`):**
  - Mostra os controles de modelo e esforço antes do envio de qualquer mensagem em chats de pasta.
- **Links clicáveis em aprovações de plano (`#38495`, `#38510`):**
  - Torna referências a arquivos diretamente acionáveis no desktop e cliente móvel.
- **Ação "Add to Chat" a partir do editor, markdown preview e terminal (`#38251`):**
  - Expõe menus de contexto e atalhos rápidos para enviar a seleção de texto atual do terminal, o arquivo ativo no editor
    ou o preview de Markdown diretamente como contexto anexado ao composer do chat ativo.
- **Indicador de branch de conversa abaixo do composer (`#38253`):**
  - Exibe o branch git correspondente ao workspace da conversa logo abaixo da caixa de texto do composer, prevenindo
    comandos acidentais em branches incorretos.
- **Manutenção do seletor de esforço editável (`#38272`):**
  - Mantém o dropdown de esforço do Claude interativo e mutável mesmo após o envio da primeira mensagem e recebimento da
    resposta inicial.
- **Suporte ao modo Plan no OpenCode em Native Chat (`#43606`, resolve `#43603`):**
  - Habilita o comando local `/plan` e o chip visual de Plan para `opencode` e `opencode2` no chat nativo;
  - Exibe qual agente o OpenCode está executando e permite alternar de volta para Build através do chip de modo.
- **Exibição contínua de prosa e rascunhos durante perguntas interativas (`#43602`):**
  - Mantém a prévia da resposta textual gerada visível acima do cartão de pergunta interativa, garantindo que o usuário consulte os dados antes de responder.

## O que fazer

- Suportar o modo Plan para OpenCode e OpenCode2 no Native Chat estruturado (`#43606`, resolve `#43603`).
- Garantir a visibilidade contínua de explicações e rascunhos emitidos antes de chamadas `AskUserQuestion` (`#43602`).
- Integrar as melhorias de UX do composer (`#38286`, `#38251`, `#38253` e `#38272`) no `brza-studio`.
- Adotar a inclusão de chats nativos no Cmd+J (`#38574`) e exibição prévia de modelo/esforço (`#38498`).
- Assegurar a propagação de `CLAUDE_CODE_ARTIFACT=1` (`#38248`) no runtime de Native Chat do `brza-studio` e nos adaptadores
  do `brza-workflow`.
