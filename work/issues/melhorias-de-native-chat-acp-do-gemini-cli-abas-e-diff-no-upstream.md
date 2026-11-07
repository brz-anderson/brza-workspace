---
status: open
description: Os PRs #39398, #39006, #33360 e as issues #39523, #39528, #39556, #39514 trazem correção de auth no macOS, isolamento de skills, launch de modelos e ACP do Gemini CLI.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#39398`](https://github.com/stablyai/orca/pull/39398) (Issue [`#39395`](https://github.com/stablyai/orca/issues/39395)),
[`stablyai/orca#39006`](https://github.com/stablyai/orca/pull/39006) (atendendo à Issue [`#38833`](https://github.com/stablyai/orca/issues/38833)),
[`stablyai/orca#39012`](https://github.com/stablyai/orca/pull/39012),
[`stablyai/orca#38976`](https://github.com/stablyai/orca/pull/38976) (Issue [`#38975`](https://github.com/stablyai/orca/issues/38975)),
[`stablyai/orca#38997`](https://github.com/stablyai/orca/pull/38997),
[`stablyai/orca#38872`](https://github.com/stablyai/orca/pull/38872),
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
[`stablyai/orca#39523`](https://github.com/stablyai/orca/issues/39523),
[`stablyai/orca#39528`](https://github.com/stablyai/orca/issues/39528),
[`stablyai/orca#39556`](https://github.com/stablyai/orca/issues/39556),
[`stablyai/orca#39514`](https://github.com/stablyai/orca/issues/39514),
[`stablyai/orca#38663`](https://github.com/stablyai/orca/issues/38663),
[`stablyai/orca#38100`](https://github.com/stablyai/orca/issues/38100),
[`stablyai/orca#38124`](https://github.com/stablyai/orca/issues/38124),
[`stablyai/orca#37983`](https://github.com/stablyai/orca/issues/37983),
[`stablyai/orca#37455`](https://github.com/stablyai/orca/issues/37455),
[`stablyai/orca#37436`](https://github.com/stablyai/orca/issues/37436),
[`stablyai/orca#37462`](https://github.com/stablyai/orca/issues/37462) e
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Execução do Antigravity Chat via `agy acp` nativo do host (`#39006`, atendendo `#38833`):**
   - Substitui o runtime empacotado gerenciado (`agy_acp_server.par`) sob `<userData>/antigravity-chat` pela invocação
     direta do comando oficial `agy acp` instalado no host (para versões `>= 1.5.0`);
   - Utiliza a conta e o armazenamento de conversas da própria CLI, unificando histórico, autenticações e permitindo a
     continuação bidirecional de chats em terminais sem discrepâncias de ambiente;
   - Mantém fallback gracioso para o runtime empacotado caso a CLI do host seja anterior a 1.5.0 ou falte compatibilidade.
2. **Recuperação de login com terminal em chats nativos deslogados (`#39012`):**
   - Quando sessões ACP do OpenCode, Pi ou OMP estão sem autenticação válida ou com tokens OAuth expirados, o chat exibia
     apenas um erro bloqueante sem oferecer caminho de recuperação na interface desktop;
   - O PR `#39012` adiciona um botão interativo "Sign in" diretamente nos avisos e linhas de mensagem recusada do chat,
     abrindo um terminal no workspace com o comando interativo de login correspondente (`/login`, etc.) e retendo a aba do chat.
3. **Resiliência contra erro transitório `-32603` na sondagem de catálogo ACP (`#38976`, resolve `#38975`):**
   - Falhas transitórias durante o handshake inicial `session/new` degradavam o seletor de modelos para um único modelo genérico;
   - O PR `#38976` introduz retentativas transparentes antes de concluir o inventário de modelos disponíveis.
4. **Perguntas interativas de múltipla escolha do OpenCode em cartões de chat (`#38872`):**
   - Nas versões recentes do OpenCode (>= 2.0.22), quando o agente faz perguntas estruturadas de escolha ou esclarecimento,
     o Chat UI informava falsamente que o popup não podia ser exibido;
   - O PR `#38872` declara suporte ao protocolo de formulários interativos ACP para o OpenCode, permitindo responder a
     perguntas de múltipla escolha diretamente nos cartões de chat, combinar seleções customizadas, digitar respostas livres
     ou cancelar a solicitação sem perda de contexto.
5. **Preservação de modelo salvo e redução síncrona de status ao reabrir chats ACP (`#38815`):**
   - Ao reabrir conversas salvas de agentes ACP, o app enviava uma troca de modelo redundante antes que o inventário de modelos
     do provedor estivesse carregado, gerando recusa prematura na primeira mensagem;
   - O PR `#38815` retém o modelo exato da conversa e atualiza as observações nativas de inicialização e permissão de forma
     síncrona na chegada de respostas validadas, evitando sobrescritas por respostas defasadas.
6. **Suporte a login Gemini Enterprise no Antigravity Chat (`#38737`, resolve `#38606`):**
   - O PR `#38737` adiciona na seção de contas Antigravity a escolha entre "Google account (personal)" e "Gemini Enterprise",
     permitindo configurar o Google Cloud project ID e location (região), persistindo a escolha por host de execução e
     usando a credencial enterprise tanto para novos chats quanto para retomadas e titulação automática.
7. **Liberação de memória em contabilidade de ferramentas e mensagens ACP (`#38767`):**
   - Elimina retenção desnecessária de chamadas de ferramentas e mensagens intermediárias obsoletas do protocolo ACP
     (Agent Client Protocol), aliviando o consumo de memória da thread principal do app.
8. **Tratamento de saída prematura do provedor OpenCode ACP (`#38663`):**
   - Investiga e mitiga interrupções espontâneas com exit code 0 durante streaming de respostas de agentes OpenCode ACP.
9. **Comando `/mcp` disponível no menu barra do Claude Code em Chat UI (`#38190`, resolve `#37906`):**
   - Adiciona o `/mcp` ao seletor de slash commands do Native Chat, permitindo inspecionar e gerenciar servidores MCP
     diretamente pela interface gráfica.
10. **Exibição de detalhes técnicos do modelo ao passar o mouse (`#38183`, resolve `#38115`):**
    - Hover card exibe contexto, custos por milhão de tokens e recursos suportados para cada modelo no picker do Native Chat.
11. **Renderização de diagramas Mermaid em comentários de PRs no Checks panel (`#38215`, resolve `#38185`):**
    - Passa a renderizar diagramas interativos diretamente dentro do painel Checks.
12. **Continuação correta em chats Codex (`#38094`, resolve `#38090`):**
    - Garante a leitura da continuação viva da conversa ao retomar sessões do Codex.
13. **Preservação de conversas de Native Chat Antigravity no Session History (`#38100`):**
    - Scanner de histórico passa a cobrir tanto o diretório de dados do chat quanto a raiz da CLI.
14. **Limpeza de comandos de barra na superfície Codex (`#37640`):**
    - Deixa de oferecer comandos curados exclusivos de terminal no menu barra (`/`) do Codex em modo Chat nativo.
15. **Suporte a blocos `server_tool_use` (advisor) do Claude (`#38124`):**
    - Corrige mensagem \"cannot display yet\" ao receber respostas com ferramentas do servidor / blocos de consultoria no Native Chat.
16. **Recuperação de respostas bloqueadas e isolamento de UI de plugins (`#37965`, `#37480`, `#37455`):**
    - Evita poluição visual no transcript do Native Chat por quadros de status de plugins do Claude Code.
17. **Exibição de arquivos propostos e diffs em aprovações Codex (`#37960`, `#37436`):**
    - Os cards de confirmação de escrita de ferramentas ACP/Codex exibem arquivos afetados e diff inline antes da aprovação.
18. **Navegação por abas com atalhos de teclado (`#37952`, `#37532`, `#37462`):**
    - Incorpora abas de Native Chat no ciclo de navegação `Ctrl+PageUp` / `Ctrl+PageDown`.
19. **Cache persistente de imagens em chats nativos (`#37932`):**
    - Retém imagens renderizadas em memória de cache durante rolagens longas de histórico ou alternâncias entre workspaces.
20. **Detecção correta de login no Antigravity Chat por arquivos de token do servidor (`#39398`, resolve `#39395`):**
    - O validador `hasManagedAntigravityChatSignIn` procurava por nomes terminados em `oauth-token`, enquanto o servidor oficial
      empacotado grava `acp_token.json` e `acp_business_token.json`;
    - Sem a correção, o app considerava o usuário deslogado e podia migrar indevidamente novos chats para a conta do host do `agy`.
21. **Descompasso de credenciais do Antigravity Chat no macOS (`#39523`):**
    - No macOS, a autenticação em Settings -> Accounts grava `acp_token.json` sob `<userData>/antigravity-chat/antigravity-acp/`,
      enquanto o servidor ACP gerenciado (`agy_acp_server`) usa `HybridCredentialStore` que lê exclusivamente o item do Keychain
      `service=gemini, account=antigravity-acp` sem fallback para o arquivo de token;
    - Como a chave no Keychain não existe, o servidor tenta login interativo no browser e é morto pelo timeout de ~6s do app,
      falhando com `provider-open-failed` (código JSON-RPC `-32603`).
22. **Isolamento de skills por redirecionamento de `GEMINI_HOME` (`#39528`):**
    - Ao lançar o Antigravity ACP, o runtime define `GEMINI_HOME="<userData>/antigravity-chat"`. O servidor busca skills
      exclusivamente em `antigravity-cli/skills` e `config/skills` dentro dessa pasta isolada;
    - Skills instaladas globalmente pelo usuário ou via comando de instalação (em `~/.gemini/config/skills` e
      `~/.gemini/antigravity-cli/skills`) ficam invisíveis nas sessões de Native Chat do Antigravity.
23. **Conflito entre `--model` e `--effort` no lançamento do Antigravity via terminal (`#39556`):**
    - Ao invocar um agente de terminal Antigravity passando tanto `--model` quanto `--effort`, o `agy` falha na resolução dos
      identificadores (cujos IDs já codificam o esforço, ex.: `claude-sonnet-5-5-medium`) e executa silenciosamente Gemini 4 Argon
      sem aviso ou erro.
24. **Execução nativa de chats Gemini CLI sobre ACP (`#33360`, atendendo `#39514`):**
    - Habilita sessões de chat nativo diretamente com a CLI Gemini via protocolo ACP, integrando ferramentas de inspeção,
      aprovações estruturadas e streaming de respostas na interface do usuário.

## O que fazer

- Implementar fallback no `HybridCredentialStore` para leitura de `acp_token.json` quando o item do Keychain não existir,
  ou sincronizar o token no Keychain do macOS durante o sign-in no `brza-studio` (`#39523`).
- Garantir symlink ou descoberta compartilhada das pastas globais de skills em `~/.gemini/` mesmo quando `GEMINI_HOME` for
  redirecionado para o diretório de dados do usuário (`#39528`).
- Ajustar a passagem de argumentos na CLI de lançamento de agentes para mapear ou omitir `--effort` redundante em modelos do
  Antigravity cujos identificadores já contêm o sufixo de esforço (`#39556`).
- Adotar o suporte a execução de Chat via `agy acp` nativo (`#39006`), eliminando a necessidade de gerenciar o runtime avulso
  `.par` e permitindo continuidade perfeita de histórico com a CLI Antigravity.
- Incorporar a detecção correta dos arquivos `acp_token.json` e `acp_business_token.json` para o runtime do Antigravity Chat (`#39398`).
- Implementar a recuperação de autenticação com atalho "Sign in" em chats nativos (`#39012`).
- Adotar o suporte a formulários interativos OpenCode (`#38872`) e a preservação de modelos ao restaurar sessões ACP (`#38815`).
- Adotar o suporte a Gemini Enterprise no Antigravity Chat (`#38737`) e chats Gemini CLI sobre ACP (`#33360`).
