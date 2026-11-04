---
status: open
description: Os PRs #38094, #37640 e #37965 e as issues #38100, #38124 e #38115 trazem continuidade em chats Codex, recuperação de sessões Antigravity no histórico e melhorias de UX.
scope:
  - brza-studio
priority: low
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#38094`](https://github.com/stablyai/orca/pull/38094) (Issue
[`#38090`](https://github.com/stablyai/orca/issues/38090)),
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
[`stablyai/orca#38100`](https://github.com/stablyai/orca/issues/38100),
[`stablyai/orca#38124`](https://github.com/stablyai/orca/issues/38124),
[`stablyai/orca#38115`](https://github.com/stablyai/orca/issues/38115),
[`stablyai/orca#37983`](https://github.com/stablyai/orca/issues/37983),
[`stablyai/orca#37455`](https://github.com/stablyai/orca/issues/37455),
[`stablyai/orca#37436`](https://github.com/stablyai/orca/issues/37436),
[`stablyai/orca#37462`](https://github.com/stablyai/orca/issues/37462) e
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Continuação correta em chats Codex (`#38094`, resolve `#38090`):**
   - Ao importar e retomar conversas do Codex no Native Chat, o app lia um arquivo canônico estático defasado em vez de
     importar a continuação indexada mais recente. O PR `#38094` garante a leitura da continuação viva da conversa.
2. **Preservação de conversas de Native Chat Antigravity no Session History (`#38100`):**
   - Ao fechar uma conversa de Antigravity iniciada no Native Chat do app, a sessão sumia da lista de Agent Session History.
     O scanner de histórico procurava apenas na raiz CLI tradicional (`~/.gemini/antigravity-cli/brain`) e ignorava o
     diretório gerenciado pelo app (`antigravity-chat/antigravity-acp/brain/`), impedindo a reabertura de chats passados.
3. **Limpeza de comandos de barra na superfície Codex (`#37640`):**
   - Deixa de oferecer comandos curados exclusivos de terminal no menu barra (`/`) do Codex em modo Chat nativo.
4. **Suporte a blocos `server_tool_use` (advisor) do Claude (`#38124`):**
   - Corrige mensagem "cannot display yet" ao receber respostas com ferramentas do servidor / blocos de consultoria no Native Chat.
5. **Detalhes do modelo em hover no seletor de Chat (`#38115`):**
   - Exibe janela flutuante com dados de contexto, custo e capacidade técnica ao passar o mouse sobre cada modelo no picker.
6. **Recuperação de respostas bloqueadas e isolamento de UI de plugins (`#37965`, `#37480`, `#37455`):**
   - Evita poluição visual no transcript do Native Chat por quadros de status de plugins do Claude Code e recupera
     respostas interrompidas em caso de bloqueio temporário de streaming.
7. **Exibição de arquivos propostos e diffs em aprovações Codex (`#37960`, `#37436`):**
   - Os cards de confirmação de escrita de ferramentas ACP/Codex agora exibem diretamente os arquivos afetados e o diff
     inline com highlight antes de o usuário clicar em "Aprovar".
8. **Navegação por abas com atalhos de teclado (`#37952`, `#37532`, `#37462`):**
   - Incorpora abas de Native Chat no ciclo de navegação `Ctrl+PageUp` / `Ctrl+PageDown`.
9. **Cache persistente de imagens em chats nativos (`#37932`):**
   - Retém imagens renderizadas em memória de cache durante rolagens longas de histórico ou alternâncias entre workspaces.
10. **Classificação unificada no menu `/` do composer (`#37983`):**
    - Unifica pontuação e ranking entre skills e comandos do menu barra (`/`).

## O que fazer

- Incorporar a rota de transcrições do Antigravity ACP (`#38100`) no histórico do `brza-studio` para que sessões nativas
  possam ser reabertas normalmente.
- Adotar as correções de continuidade do Codex (`#38094`), blocos advisor (`#38124`) e cache de imagens (`#37932`).
