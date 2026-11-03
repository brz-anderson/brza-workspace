---
status: open
description: Os PRs #33360, #37480, #37532, #37494 e #37503 do upstream trazem Gemini CLI sobre ACP, limpeza de frames de plugin no transcript, navegação de abas de chat e melhorias em abas e diff.
scope:
  - brza-studio
priority: low
opened: 2026-11-03
tags:
  - chat
  - design
---

# Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream

Rastreado dos PRs abertos no upstream [`stablyai/orca#33360`](https://github.com/stablyai/orca/pull/33360),
[`stablyai/orca#37480`](https://github.com/stablyai/orca/pull/37480),
[`stablyai/orca#37532`](https://github.com/stablyai/orca/pull/37532),
[`stablyai/orca#37494`](https://github.com/stablyai/orca/pull/37494) e
[`stablyai/orca#37503`](https://github.com/stablyai/orca/pull/37503), além da issue
[`stablyai/orca#37361`](https://github.com/stablyai/orca/issues/37361).

## Os itens no upstream

1. **Gemini CLI original no Native Chat sobre ACP (`#33360`):** adiciona o adaptador de lançamento e dialeto ACP para o
   Gemini CLI, reutilizando o fluxo de aprovação de permissões e tratamento de recusas de retomada do runtime ACP.
2. **Remoção de frames de UI de plugins da transcrição do chat (`#37480`):** evita que quadros `ui_status` de plugins do
   Claude Code sujem a transcrição exibida no Native Chat (resolve a issue `#37455`).
3. **Abas de Native Chat no ciclo `Ctrl+PageUp`/`PageDown` (`#37532`):** inclui as abas de chat nativo na navegação por
   atalho que antes percorria apenas terminais.
4. **Redimensionamento individual de cabeçalhos de abas (`#37494`):** permite arrastar a borda de uma aba para ajustar a
   largura do título sem afetar as demais.
5. **Visualização de arquivos novos sem tintura inteira no diff (`#37503`):** remove o fundo verde contínuo em arquivos
   inteiramente novos na diff view, melhorando a leitura da sintaxe.
6. **Busca reversa `Ctrl+R` no composer do Native Chat (`#37361`):** issue propondo busca no histórico de prompts
   enviados diretamente pelo composer do chat.

## O que fazer

Manter no radar para o próximo sync da `master` do `brza-studio` ou cherry-pick pontual dos consertos de UX (`#37480`,
`#37532` e `#37503`).
