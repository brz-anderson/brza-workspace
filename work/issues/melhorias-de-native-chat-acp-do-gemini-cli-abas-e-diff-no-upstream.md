---
status: open
description: Os PRs #33360, #37965, #37960, #37952, #37932 e a issue #37983 trazem recuperação de respostas, diffs em aprovações Codex, cache de imagens e atalhos de chat.
scope:
  - brza-studio
priority: low
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#37965`](https://github.com/stablyai/orca/pull/37965),
[`stablyai/orca#37960`](https://github.com/stablyai/orca/pull/37960),
[`stablyai/orca#37952`](https://github.com/stablyai/orca/pull/37952),
[`stablyai/orca#37932`](https://github.com/stablyai/orca/pull/37932),
[`stablyai/orca#33360`](https://github.com/stablyai/orca/pull/33360),
[`stablyai/orca#37480`](https://github.com/stablyai/orca/pull/37480),
[`stablyai/orca#37532`](https://github.com/stablyai/orca/pull/37532),
[`stablyai/orca#37494`](https://github.com/stablyai/orca/pull/37494) e
[`stablyai/orca#37503`](https://github.com/stablyai/orca/pull/37503), além das issues
[`stablyai/orca#37983`](https://github.com/stablyai/orca/issues/37983),
[`stablyai/orca#37455`](https://github.com/stablyai/orca/issues/37455),
[`stablyai/orca#37436`](https://github.com/stablyai/orca/issues/37436),
[`stablyai/orca#37462`](https://github.com/stablyai/orca/issues/37462) e
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Recuperação de respostas bloqueadas e isolamento de UI de plugins (`#37965`, `#37480`, `#37455`):**
   - Evita poluição visual no transcript do Native Chat por quadros de status de plugins do Claude Code e recupera
     respostas interrompidas em caso de bloqueio temporário de streaming.
2. **Exibição de arquivos propostos e diffs em aprovações Codex (`#37960`, `#37436`):**
   - Os cards de confirmação de escrita de ferramentas ACP/Codex agora exibem diretamente os arquivos afetados e o diff
     inline com highlight antes de o usuário clicar em "Aprovar".
3. **Navegação por abas com atalhos de teclado (`#37952`, `#37532`, `#37462`):**
   - Incorpora abas de Native Chat no ciclo de navegação `Ctrl+PageUp` / `Ctrl+PageDown`, unificando a alternância entre
     terminais e chats abertos.
4. **Cache persistente de imagens em chats nativos (`#37932`):**
   - Retém imagens renderizadas em memória de cache durante rolagens longas de histórico ou alternâncias entre workspaces,
     evitando recarregamento e cintilações na tela.
5. **Classificação unificada no menu `/` do composer (`#37983`):**
   - Unifica a pontuação e ranking entre skills e comandos do menu barra (`/`), impedindo que apertar Enter execute um
     comando com match difuso quando o usuário digitava o prefixo de uma skill.
6. **Gemini CLI original no Native Chat sobre ACP (`#33360`):**
   - Adiciona o adaptador de lançamento e dialeto ACP para o Gemini CLI, reutilizando o fluxo de aprovação de permissões
     e tratamento de recusas de retomada do runtime ACP.
7. **Redimensionamento de abas e legibilidade de diff (`#37494`, `#37503`):**
   - Ajuste manual de largura de títulos de abas e remoção de tintura verde excessiva em arquivos novos na visualização
     de diff.

## O que fazer

Incorporar no `brza-studio` as correções de visualização de diffs em aprovações (`#37960`), a retenção de cache de
imagens (`#37932`) e o ranking unificado de skills no menu `/` (`#37983`).
