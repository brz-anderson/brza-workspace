---
status: open
description: Os PRs #45594, #46346 e #46129 priorizam agentes prontos no new-tab picker, previnem submit espúrio de prompt pós-exit da CLI e oferecem Resume in New CLI.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#45594`](https://github.com/stablyai/orca/pull/45594),
[`stablyai/orca#46346`](https://github.com/stablyai/orca/pull/46346),
[`stablyai/orca#46129`](https://github.com/stablyai/orca/pull/46129),
além da issue [`stablyai/orca#46365`](https://github.com/stablyai/orca/issues/46365),
[`stablyai/orca#42309`](https://github.com/stablyai/orca/pull/42309) (resolve Issue [`#42308`](https://github.com/stablyai/orca/issues/42308)),
[`stablyai/orca#41354`](https://github.com/stablyai/orca/pull/41354) (resolve Issue [`#41351`](https://github.com/stablyai/orca/issues/41351)),
[`stablyai/orca#31595`](https://github.com/stablyai/orca/pull/31595),
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
6. **Expectativa implícita de reporte em lançamentos independentes de agentes pela CLI (`#41354`, resolve `#41351`):**
   Ao abrir chats ou terminais para outros agentes via `orca agent launch` ou `worktree create --agent`, os recibos retornavam
   `journaled` / `structured`. Usuários e scripts esperavam que o agente reportasse automaticamente o encerramento do trabalho,
   mas essas sessões eram independentes e não possuíam canal de retorno de coordenação.
7. **Ausência de suporte ao agente de terminal `loop` no catálogo e ciclo de vida (`#42309`, resolve `#42308`):**
   O agente `loop` executava como terminal comum, sem exibição de status no card de workspace, sem alertas de intervenção humana e sem suporte a retomada de sessão (`loop --session <id>`).
8. **Ordenação defasada do seletor de nova aba exibindo agentes não instalados antes dos prontos (`#45594`):**
   Ao abrir o seletor de nova aba ou executar arranque via CLI, agentes que exigem instalação ou configuração remota apareciam intercalados ou à frente dos agentes locais prontos para execução imediata no host.
9. **Submissão residual de prompts no shell após encerramento do processo da CLI do agente (`#46346`):**
   Quando a CLI do agente concluía ou encerrava abruptamente a execução, o terminal mantinha o prompt pendente no buffer de entrada e o submetia acidentalmente no shell do usuário.
10. **Inconsistência de superfície e preferências de lançamento em plugins (`#46365`):**
    Comandos de criação de workspace e lançamento de agentes chamados por extensões e plugins (`workspace.create` e `agent.launch`) não respeitavam a preferência global `Chat | CLI` do usuário e não aceitavam o parâmetro `surface`.

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
- **No PR `#41354` (resolve `#41351`):** explicita nos recibos de lançamento CLI `reporting: { automatic: false, guideCommand: "orca skills get orchestration" }`, esclarecendo que sessões independentes não reportam e direcionando para o fluxo supervisionado de workers.
- **No PR `#42309` (resolve `#42308`):** integra o agente terminal `loop` com normalização de eventos via rota `/hook/loop`, status em tempo real no workspace card e retomada de sessão com `loop --session <id>`.
- **No PR `#45594`:** particiona as entradas do seletor de nova aba agrupando por prontidão de runtime no host em vez de ordenação por posição, preservando o tipo de superfície de cada agente.
- **No PR `#46346`:** evita a injeção espúria de prompts pendentes no shell caso o processo CLI do agente termine ou seja abortado antes da submissão.
- **No PR `#46129`:** disponibiliza o comando "Resume in New CLI" diretamente no menu de cabeçalho do chat, permitindo transicionar a sessão para um terminal PTY novo.
- **Na issue `#46365`:** alinha as funções de extensão `workspace.create` e `agent.launch` para aceitar `surface` e respeitar o modo configurado pelo operador.

## O que fazer

- Priorizar agentes prontos no host no seletor de nova aba da interface e CLI (`#45594`).
- Impedir submissão de comandos no shell após encerramento do processo do agente CLI (`#46346`).
- Adicionar opção "Resume in New CLI" no menu de cabeçalho do chat (`#46129`).
- Suportar a preferência `Chat | CLI` e parâmetro `surface` em `workspace.create` e `agent.launch` para plugins (`#46365`).
- Portar o PR `#31595` (apoiado no PR `#38063`) para o `brza-studio`, habilitando a transição transparente entre o modo
  terminal e o Native Chat sem duplicação de abas, além de adotar `--command-agent` / `--view-mode chat` no `brza-workflow`.
- Explicitar metadados e orientações de reporte em lançamentos independentes de agentes pela CLI (`#41354`, resolve `#41351`).
- Suportar o agente `loop` com hooks nativos e retomada de sessão (`#42309`, resolve `#42308`).
