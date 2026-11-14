---
priority: high
tags:
  - chat
  - tooling
  - infra
description: Os PRs #42437, #42482, #42476 e #42466 trazem diálogo unificado de Fork entre hosts/agentes, botão compartilhado Send notes, fechamento de abas sem foco e cores de saúde de cotas.
---

# Janela unificada de Fork cross-host e botão compartilhado de envio de notas

Rastreado dos PRs abertos no upstream [`stablyai/orca#42437`](https://github.com/stablyai/orca/pull/42437) (resolve Issue [`#42436`](https://github.com/stablyai/orca/issues/42436)),
[`stablyai/orca#42482`](https://github.com/stablyai/orca/pull/42482),
[`stablyai/orca#42476`](https://github.com/stablyai/orca/pull/42476) e
[`stablyai/orca#42466`](https://github.com/stablyai/orca/pull/42466).

## O que está quebrado ou faltando

1. **Inconsistência e dependência de cota remota no diálogo de Fork de conversas (`#42437`, resolve `#42436`):**
   O fluxo de Fork de chat variava entre desktop e mobile: no desktop dependia de chamadas pesadas ao backend para listar agentes remotos e falhava quando os créditos da conta terminavam, impedindo o usuário de bifurcar uma conversa localmente para outro agente ou host sem saldo online; no mobile a experiência era fragmentada e sem suporte a seleção de workspaces.
2. **Duplicação de botões de envio de notas e comentários de revisão (`#42482`):**
   A toolbar de Changes, o cabeçalho de diff, a aba de Source Control, a pré-visualização de Markdown e os comentários em PRs continham implementações isoladas de botões "Send notes", com contadores inconsistentes, falta de ações rápidas (Copy notes / Clear notes) e comportamento divergente ao submeter notas em lote para o chat do agente.
3. **Acúmulo de abas temporárias e não fixadas no editor (`#42476`):**
   Ao navegar rapidamente por arquivos em revisões de código ou pesquisas, abas limpas e temporárias permaneciam abertas indefinidamente no workspace, poluindo a barra de abas e forçando o fechamento manual repetitivo.
4. **Falta de pistas visuais de esgotamento de cota no status bar e roster (`#42466`):**
   O status bar e a lista de provedores/modelos mostravam apenas números absolutos ou percentuais brutos de uso sem indicação cromática de perigo (saúde da cota), dificultando identificar visualmente quando um modelo estava prestes a sofrer limitação de taxa ou corte de serviço.

## O que o upstream implementa

- **Diálogo unificado de Fork cross-host e cross-workspace (`#42437`, resolve `#42436`):**
  - Cria um componente modal unificado de Fork compartilhado entre desktop e mobile;
  - Introduz extensão de protocolo `ai-vault.chat-fork-import.v1` para exportar o snapshot local do histórico e importar em outro host de forma transparente;
  - Permite escolher destino (novo workspace, workspace ativo, outro agente ou host remoto);
  - Baseia a bifurcação no resumo local da conversa, funcionando perfeitamente mesmo sem créditos online remotos no agente de origem.
- **Componente compartilhado `SendNotesButton` com menu de ações (`#42482`):**
  - Unifica o botão "Send N notes" / "Send N comments" em toda a UI (toolbar de Changes, diff header, Source Control, markdown preview e PR comments);
  - Adiciona menu suspenso com opções de copiar notas formatadas para a área de transferência (*Copy notes*) ou limpar todas as notas pendentes (*Clear notes*);
  - Sincroniza o estado de contagem global de anotações ativas.
- **Configuração para fechar abas não fixadas ao perder foco (`#42476`):**
  - Adiciona a configuração `closeUnpinnedEditorTabsOnFocusLoss` que fecha automaticamente abas não modificadas (limpas) e não fixadas quando o foco sai do editor ou da tab bar;
  - Registra o comando e atalho de teclado `Mod+Alt+Shift+P` (`tab.togglePin`) para fixar ou desafixar rapidamente a aba ativa.
- **Cores de saúde de cotas e alternador de métricas (`#42466`):**
  - Implementa faixas de cores semânticas (verde, amarelo e vermelho) para a porcentagem de cota consumida no status bar e na lista de provedores;
  - Adiciona alternador de cabeçalho "Used ⇅ / Left ⇅" para inverter a visualização entre volume consumido e volume restante.

## O que fazer

- Adotar o diálogo unificado de Fork com protocolo `ai-vault.chat-fork-import.v1` no BrzA Studio (`#42437`).
- Integrar o componente compartilhado `SendNotesButton` nos diffs, revisões e preview de Markdown (`#42482`).
- Implementar a opção de fechar abas não fixadas no desfoque e atalho de pin (`#42476`).
- Adicionar cores de saúde de cota e alternância Used/Left no status bar do Studio (`#42466`).
