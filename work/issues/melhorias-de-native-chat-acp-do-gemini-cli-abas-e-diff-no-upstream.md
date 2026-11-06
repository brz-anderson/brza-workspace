---
status: open
description: Os PRs #38872, #38815, #38737 e as issues #38833 e #38606 trazem perguntas interativas OpenCode, preservação de modelo ACP, transição para agy acp e login Gemini Enterprise.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#38872`](https://github.com/stablyai/orca/pull/38872),
[`stablyai/orca#38815`](https://github.com/stablyai/orca/pull/38815),
[`stablyai/orca#38737`](https://github.com/stablyai/orca/pull/38737) (Issue [`#38606`](https://github.com/stablyai/orca/issues/38606)),
[`stablyai/orca#38767`](https://github.com/stablyai/orca/pull/38767),
[`stablyai/orca#38190`](https://github.com/stablyai/orca/pull/38190) (Issue [`#37906`](https://github.com/stablyai/orca/issues/37906)),
[`stablyai/orca#38183`](https://github.com/stablyai/orca/pull/38183) (Issue [`#38115`](https://github.com/stablyai/orca/issues/38115)),
[`stablyai/orca#38215`](https://github.com/stablyai/orca/pull/38215) (Issue [`#38185`](https://github.com/stablyai/orca/issues/38185)),
[`stablyai/orca#38094`](https://github.com/stablyai/orca/pull/38094) (Issue [`#38090`](https://github.com/stablyai/orca/issues/38090)),
[`stablyai/orca#37640`](https://github.com/stablyai/orca/pull/37640),
[`stablyai/orca#37965`](https://github.com/stablyai/orca/pull/37965),
[`stablyai/orca#37960`](https://github.com/stablyai/orca/pull/37960),
[`stablyai/orca#37952`](https://github.com/stablyai/orca/pull/37952),
[`stablyai/orca#37932`](https://github.com/stablyai/orca/pull/37932),
[`stablyai/orca#33360`](https://github.com/stablyai/orca/pull/33360),
[`stablyai/orca#37480`](https://github.com/stablyai/orca/pull/37480),
[`stablyai/orca#37532`](https://github.com/stablyai/orca/pull/37532),
[`stablyai/orca#37494`](https://github.com/stablyai/orca/pull/37494) e
[`stablyai/orca#37503`](https://github.com/stablyai/orca/pull/37503), além das issues
[`stablyai/orca#38833`](https://github.com/stablyai/orca/issues/38833),
[`stablyai/orca#38663`](https://github.com/stablyai/orca/issues/38663),
[`stablyai/orca#38100`](https://github.com/stablyai/orca/issues/38100),
[`stablyai/orca#38124`](https://github.com/stablyai/orca/issues/38124),
[`stablyai/orca#37983`](https://github.com/stablyai/orca/issues/37983),
[`stablyai/orca#37455`](https://github.com/stablyai/orca/issues/37455),
[`stablyai/orca#37436`](https://github.com/stablyai/orca/issues/37436),
[`stablyai/orca#37462`](https://github.com/stablyai/orca/issues/37462) e
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Perguntas interativas de múltipla escolha do OpenCode em cartões de chat (`#38872`):**
   - Nas versões recentes do OpenCode (>= 2.0.22), quando o agente faz perguntas estruturadas de escolha ou esclarecimento,
     o Chat UI informava falsamente que o popup não podia ser exibido;
   - O PR `#38872` declara suporte ao protocolo de formulários interativos ACP para o OpenCode, permitindo responder a
     perguntas de múltipla escolha diretamente nos cartões de chat, combinar seleções customizadas, digitar respostas livres
     ou cancelar a solicitação sem perda de contexto.
2. **Preservação de modelo salvo e redução síncrona de status ao reabrir chats ACP (`#38815`):**
   - Ao reabrir conversas salvas de agentes ACP, o app enviava uma troca de modelo redundante antes que o inventário de modelos
     do provedor estivesse carregado, gerando recusa prematura na primeira mensagem;
   - O PR `#38815` retém o modelo exato da conversa e atualiza as observações nativas de inicialização e permissão de forma
     síncrona na chegada de respostas validadas, evitando sobrescritas por respostas defasadas.
3. **Migração do Antigravity Chat para o binário nativo `agy acp` do host (`#38833`):**
   - O Antigravity Chat ainda opera em um runtime empacotado separado (`agy_acp_server.par`) com diretório de conta próprio
     sob `<userData>/antigravity-chat`, gerando problemas de compatibilidade multiplataforma e impedindo a continuação de
     sessões de chat em terminais CLI ("Continue with Terminal Agent");
   - A issue `#38833` propõe migrar a execução do chat para `agy acp` oficial da CLI instalada no host (versões >= 1.5.0),
     unificando o armazenamento de conversas, autenticações e histórico entre a interface gráfica e o terminal.
4. **Suporte a login Gemini Enterprise no Antigravity Chat (`#38737`, resolve `#38606`):**
   - O Antigravity Chat forçava autenticação pessoal Google OAuth (`oauth-personal`), bloqueando o uso de contas Gemini
     Enterprise corporativas mesmo quando o terminal ou CLI do desenvolvedor já possuía a licença corporativa ativa;
   - O PR `#38737` adiciona na seção de contas Antigravity a escolha entre "Google account (personal)" e "Gemini Enterprise",
     permitindo configurar o Google Cloud project ID e location (região), persistindo a escolha por host de execução e
     usando a credencial enterprise tanto para novos chats quanto para retomadas e titulação automática.
5. **Liberação de memória em contabilidade de ferramentas e mensagens ACP (`#38767`):**
   - Elimina retenção desnecessária de chamadas de ferramentas e mensagens intermediárias obsoletas do protocolo ACP
     (Agent Client Protocol), aliviando o consumo de memória da thread principal do app.
6. **Tratamento de saída prematura do provedor OpenCode ACP (`#38663`):**
   - Investiga e mitiga interrupções espontâneas com exit code 0 durante streaming de respostas de agentes OpenCode ACP.
7. **Comando `/mcp` disponível no menu barra do Claude Code em Chat UI (`#38190`, resolve `#37906`):**
   - Adiciona o `/mcp` ao seletor de slash commands do Native Chat, permitindo inspecionar e gerenciar servidores MCP
     diretamente pela interface gráfica.
8. **Exibição de detalhes técnicos do modelo ao passar o mouse (`#38183`, resolve `#38115`):**
   - Hover card exibe contexto, custos por milhão de tokens e recursos suportados para cada modelo no picker do Native Chat.
9. **Renderização de diagramas Mermaid em comentários de PRs no Checks panel (`#38215`, resolve `#38185`):**
   - Passa a renderizar diagramas interativos diretamente dentro do painel Checks.
10. **Continuação correta em chats Codex (`#38094`, resolve `#38090`):**
    - Garante a leitura da continuação viva da conversa ao retomar sessões do Codex.
11. **Preservação de conversas de Native Chat Antigravity no Session History (`#38100`):**
    - Scanner de histórico passa a cobrir tanto o diretório de dados do chat quanto a raiz da CLI.
12. **Limpeza de comandos de barra na superfície Codex (`#37640`):**
    - Deixa de oferecer comandos curados exclusivos de terminal no menu barra (`/`) do Codex em modo Chat nativo.
13. **Suporte a blocos `server_tool_use` (advisor) do Claude (`#38124`):**
    - Corrige mensagem \"cannot display yet\" ao receber respostas com ferramentas do servidor / blocos de consultoria no Native Chat.
14. **Recuperação de respostas bloqueadas e isolamento de UI de plugins (`#37965`, `#37480`, `#37455`):**
    - Evita poluição visual no transcript do Native Chat por quadros de status de plugins do Claude Code.
15. **Exibição de arquivos propostos e diffs em aprovações Codex (`#37960`, `#37436`):**
    - Os cards de confirmação de escrita de ferramentas ACP/Codex exibem arquivos afetados e diff inline antes da aprovação.
16. **Navegação por abas com atalhos de teclado (`#37952`, `#37532`, `#37462`):**
    - Incorpora abas de Native Chat no ciclo de navegação `Ctrl+PageUp` / `Ctrl+PageDown`.
17. **Cache persistente de imagens em chats nativos (`#37932`):**
    - Retém imagens renderizadas em memória de cache durante rolagens longas de histórico ou alternâncias entre workspaces.

## O que fazer

- Adotar o suporte a formulários interativos OpenCode (`#38872`) e a preservação de modelos ao restaurar sessões ACP (`#38815`).
- Avaliar e preparar o runtime do `brza-studio` para migrar de `agy_acp_server.par` para `agy acp` nativo (`#38833`),
  unificando as sessões de chat com os terminais do workspace.
- Adotar o suporte a Gemini Enterprise no Antigravity Chat (`#38737`) no `brza-studio`, permitindo uso corporativo do modelo.
- Incorporar a liberação de memória em contabilidade ACP (`#38767`).
