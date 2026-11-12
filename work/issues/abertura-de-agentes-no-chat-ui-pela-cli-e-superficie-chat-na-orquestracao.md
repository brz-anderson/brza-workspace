---
status: open
description: Os PRs #31595, #37710, #38001 e #37984 e as issues #37701 e #37707 trazem alternância in-place entre Chat UI e Terminal sem forking, abertura via CLI e split adjacente.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#31595`](https://github.com/stablyai/orca/pull/31595),
[`stablyai/orca#37710`](https://github.com/stablyai/orca/pull/37710),
[`stablyai/orca#38001`](https://github.com/stablyai/orca/pull/38001) e
[`stablyai/orca#37984`](https://github.com/stablyai/orca/pull/37984), além das issues
[`stablyai/orca#37701`](https://github.com/stablyai/orca/issues/37701),
[`stablyai/orca#37707`](https://github.com/stablyai/orca/issues/37707) e
[`stablyai/orca#37733`](https://github.com/stablyai/orca/issues/37733).

## O problema

1. **Bifurcação e duplicação de abas ao alternar entre Chat UI e Terminal (`#31595`):** até então, as ações "Continue in
   Chat UI" ou "Continue with Terminal Agent" criavam uma nova aba cópia ao lado da existente, duplicando processos e
   poluindo a barra de abas. Faltava um mecanismo para trocar a superfície do chat no mesmo slot, aproveitando o mesmo
   espaço e estado conversacional.
2. **Agentes criados via CLI forçados em PTY terminal (`#37710`):** ao rodar `brza terminal create --command ...` com
   scripts wrapper, variáveis de ambiente ou argumentos de permissão customizados, a aba abre sempre como terminal
   cru. O comando `agent launch --surface chat` não atende porque o runtime reconstrói o comando do agente e ignora
   o comando exato do chamador.
3. **Orquestração sem paridade de superfície (`#37701`):** `orchestration worker-start` não aceitava `--surface chat|terminal`,
   ficando em desacordo com `agent launch --surface` e impedindo que workers de tópicos fossem iniciados com a interface
   gráfica de chat por padrão.
4. **Falha na transição de TUI para Chat UI sem transcript salvo (`#37707`, `#38001`):** no Claude Code, alternar de TUI
   para Chat UI falhava com recusa de lançamento estruturado quando uma conversa retomada via CLI não continha transcript
   prévio persistido em disco.
5. **Comportamento inadequado ao dividir painel de Chat UI (`#37984`):** acionar split horizontal/vertical a partir de uma
   aba de Chat UI tentava clonar uma sessão de chat vazia sem agente, em vez de abrir um terminal shell adjacente para apoio.

## O que o upstream propõe e implementa

- **Alternância in-place entre Chat UI e Terminal sem forking (`#31595`):**
  - Implementa "Switch to Chat UI" e "Switch to Terminal" no cabeçalho do painel, tab hover card e histórico;
  - Troca a interface diretamente no mesmo slot da aba, preservando posição e pin do usuário em uma única gravação de layout;
  - Para o agente de forma ordenada com prova de encerramento (`Stop with proof first`), importa a transcrição registrada
    pelo terminal e exibe a interface de destino sem bifurcar nem abrir abas duplicadas;
  - Trata turnos interrompidos com a etiqueta limpa `"Interrupted"`.
- **No PR `#37710`:** adiciona `--command-agent <agent> --view-mode chat` ao `terminal create`, valida compatibilidade
  via capability `terminal.create-view-mode.v1` e preserva o comando original enquanto renderiza a aba no Chat UI.
- **No PR `#38001` (resolve `#37707`):** inicia automaticamente uma sessão de chat limpa quando a sessão CLI retomada não
  possuir histórico persistido, eliminando a tela de erro fatal no Native Chat.
- **No PR `#37984`:** ao dividir (`split`) uma aba de Native Chat, abre um terminal de linha de comando no mesmo diretório
  de trabalho, proporcionando ergonomia natural de desenvolvimento sem duplicar sessões de IA desnecessariamente.
- **Na issue `#37701`:** propõe `orchestration worker-start ... [--surface chat|terminal]` com eco no receipt (`surface`,
  `terminal` handle), garantindo paridade entre workers e agentes isolados.

## O que fazer

Portar o PR `#31595` (apoiado no PR `#38063`) para o `brza-studio`, habilitando a transição transparente entre o modo
terminal e o Native Chat sem duplicação de abas, além de adotar `--command-agent` / `--view-mode chat` no `brza-workflow`.
