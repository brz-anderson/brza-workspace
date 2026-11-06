---
status: open
description: Os PRs #38737, #38767, #38190, #38183 e #38215 e a issue #38606 trazem login Gemini Enterprise no Antigravity Chat, limpeza de memória ACP, /mcp no picker e Mermaid em PR comments.
scope:
  - brza-studio
priority: medium
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#38737`](https://github.com/stablyai/orca/pull/38737) (Issue [`#38606`](https://github.com/stablyai/orca/issues/38606)),
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
[`stablyai/orca#38663`](https://github.com/stablyai/orca/issues/38663),
[`stablyai/orca#38100`](https://github.com/stablyai/orca/issues/38100),
[`stablyai/orca#38124`](https://github.com/stablyai/orca/issues/38124),
[`stablyai/orca#37983`](https://github.com/stablyai/orca/issues/37983),
[`stablyai/orca#37455`](https://github.com/stablyai/orca/issues/37455),
[`stablyai/orca#37436`](https://github.com/stablyai/orca/issues/37436),
[`stablyai/orca#37462`](https://github.com/stablyai/orca/issues/37462) e
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Suporte a login Gemini Enterprise no Antigravity Chat (`#38737`, resolve `#38606`):**
   - O Antigravity Chat forçava autenticação pessoal Google OAuth (`oauth-personal`), bloqueando o uso de contas Gemini
     Enterprise corporativas mesmo quando o terminal ou CLI do desenvolvedor já possuía a licença corporativa ativa;
   - O PR `#38737` adiciona na seção de contas Antigravity a escolha entre "Google account (personal)" e "Gemini Enterprise",
     permitindo configurar o Google Cloud project ID e location (região), persistindo a escolha por host de execução e
     usando a credencial enterprise tanto para novos chats quanto para retomadas e titulação automática.
2. **Liberação de memória em contabilidade de ferramentas e mensagens ACP (`#38767`):**
   - Elimina retenção desnecessária de chamadas de ferramentas e mensagens intermediárias obsoletas do protocolo ACP
     (Agent Client Protocol), aliviando o consumo de memória da thread principal do app.
3. **Tratamento de saída prematura do provedor OpenCode ACP (`#38663`):**
   - Investiga e mitiga interrupções espontâneas com exit code 0 durante streaming de respostas de agentes OpenCode ACP.
4. **Comando `/mcp` disponível no menu barra do Claude Code em Chat UI (`#38190`, resolve `#37906`):**
   - O comando `/mcp` estava disponível apenas em terminais interativos do Claude Code. O PR `#38190` adiciona o `/mcp`
     ao seletor de slash commands do Native Chat, permitindo inspecionar e gerenciar servidores Model Context Protocol
     diretamente pela interface gráfica.
5. **Exibição de detalhes técnicos do modelo ao passar o mouse (`#38183`, resolve `#38115`):**
   - Ao passar o mouse sobre cada modelo no picker do Native Chat, uma janela de hover exibe a janela de contexto, custos
     por milhão de tokens e recursos suportados.
6. **Renderização de diagramas Mermaid em comentários de PRs no Checks panel (`#38215`, resolve `#38185`):**
   - Comentários de code review automatizados (ex.: Greptile) exibiam código-fonte bruto em blocos `mermaid`. O PR `#38215`
     passa a renderizar os diagramas interativos diretamente dentro do painel Checks.
7. **Continuação correta em chats Codex (`#38094`, resolve `#38090`):**
   - Ao importar e retomar conversas do Codex no Native Chat, o app lia um arquivo canônico estático defasado em vez de
     importar a continuação indexada mais recente. O PR `#38094` garante a leitura da continuação viva da conversa.
8. **Preservação de conversas de Native Chat Antigravity no Session History (`#38100`):**
   - Ao fechar uma conversa de Antigravity iniciada no Native Chat do app, a sessão sumia da lista de Agent Session History.
     O scanner de histórico procurava apenas na raiz CLI tradicional (`~/.gemini/antigravity-cli/brain`) e ignorava o
     diretório gerenciado pelo app (`antigravity-chat/antigravity-acp/brain/`), impedindo a reabertura de chats passados.
9. **Limpeza de comandos de barra na superfície Codex (`#37640`):**
   - Deixa de oferecer comandos curados exclusivos de terminal no menu barra (`/`) do Codex em modo Chat nativo.
10. **Suporte a blocos `server_tool_use` (advisor) do Claude (`#38124`):**
    - Corrige mensagem "cannot display yet" ao receber respostas com ferramentas do servidor / blocos de consultoria no Native Chat.
11. **Recuperação de respostas bloqueadas e isolamento de UI de plugins (`#37965`, `#37480`, `#37455`):**
    - Evita poluição visual no transcript do Native Chat por quadros de status de plugins do Claude Code e recupera
      respostas interrompidas em caso de bloqueio temporário de streaming.
12. **Exibição de arquivos propostos e diffs em aprovações Codex (`#37960`, `#37436`):**
    - Os cards de confirmação de escrita de ferramentas ACP/Codex agora exibem diretamente os arquivos afetados e o diff
      inline com highlight antes de o usuário clicar em "Aprovar".
13. **Navegação por abas com atalhos de teclado (`#37952`, `#37532`, `#37462`):**
    - Incorpora abas de Native Chat no ciclo de navegação `Ctrl+PageUp` / `Ctrl+PageDown`.
14. **Cache persistente de imagens em chats nativos (`#37932`):**
    - Retém imagens renderizadas em memória de cache durante rolagens longas de histórico ou alternâncias entre workspaces.

## O que fazer

- Adotar o suporte a Gemini Enterprise no Antigravity Chat (`#38737`) no `brza-studio`, permitindo uso corporativo do modelo.
- Incorporar a liberação de memória em contabilidade ACP (`#38767`).
- Adotar o comando `/mcp` no Native Chat (`#38190`) e a renderização de diagramas Mermaid (`#38215`) no `brza-studio`.
- Incorporar a rota de transcrições do Antigravity ACP (`#38100`) no histórico para reabertura de sessões passadas.
