---
status: open
description: Os PRs #39769, #39733, #39722, #39692 e #39741 trazem agente Kiro via ACP no chat, janela destacada para Floating Workspaces e regras unificadas de CLI.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-08
tags:
  - chat
  - tooling
---

# Agente Kiro no Native Chat, janela flutuante e endereçamento de workspaces

Rastreado do PR aberto no upstream [`stablyai/orca#39769`](https://github.com/stablyai/orca/pull/39769) (resolve Issue [`#30095`](https://github.com/stablyai/orca/issues/30095)),
do PR [`stablyai/orca#39733`](https://github.com/stablyai/orca/pull/39733),
do PR [`stablyai/orca#39722`](https://github.com/stablyai/orca/pull/39722) (atendendo à Issue [`#22167`](https://github.com/stablyai/orca/issues/22167)),
do PR [`stablyai/orca#39692`](https://github.com/stablyai/orca/pull/39692) e
do PR [`stablyai/orca#39741`](https://github.com/stablyai/orca/pull/39741) (resolve Issue [`#39728`](https://github.com/stablyai/orca/issues/39728)).

## O problema

1. **Inexistência do Kiro como agente nativo de chat sobre ACP (`#39769`, `#30095`):**
   Usuários do Kiro precisavam recorrer a terminais PTY puros ou pontes manuais, sem integração estruturada
   ao Native Chat do Orca/BrzA Studio. Faltava seletor visual de modelos, suporte a níveis de esforço de raciocínio
   (reasoning effort), fluxo de permissões e aprovação de ferramentas estruturadas com a CLI `kiro-cli`.
2. **Ambiguidade e comportamentos divergentes na resolução de workspaces na CLI (`#39733`):**
   Diferentes subcomandos da CLI (`worktree`, `ps`, `show`, `rm`) aplicavam regras inconsistentes para determinar qual
   workspace correspondia ao diretório atual (`cwd`). Além disso, não era possível explicitar `--environment local`
   ou `--parent-environment` ao criar ou reconfigurar worktrees, o endereço de rede para pareamento e automação não vinha
   em formato facilmente copiável (`address:`), e comandos destrutivos como `worktree rm --worktree current` podiam
   auto-destruir acidentalmente o workspace em uso.
3. **Impossibilidade de destacar o terminal de Floating Workspaces em janela separada (`#39722`, `#22167`):**
   Sessões de Floating Workspaces (workspaces temporários desanexados da lista principal) ficavam presas dentro da
   mesma janela principal do Electron, impedindo fluxos multimonitor dedicados e forçando divisões de tela concorrentes
   com outros projetos.
4. **Falta de atalho para troca de branch no chat composer (`#39692`):**
   Abaixo da caixa de entrada de chat (*composer*), o nome do branch atual do workspace era exibido como texto estático.
   Para trocar de branch, o operador era forçado a navegar até a barra de status ou abrir a aba de controle de versão.
5. **Falha de pareamento mobile com bind fixado em interface de rede (`#39741`, `#39728`):**
   Em execuções de `orca serve` com bind associado a uma interface de rede específica (ex.: IP de Tailscale ou VPN),
   o serviço falhava na geração de credenciais e URL de pareamento, assumindo `127.0.0.1` ou abortando conexões remotas válidas.

## O que o upstream implementa

- **Integração do Kiro no Native Chat via ACP (`#39769`):**
  - Adiciona o Kiro como agente de primeira classe no Native Chat através de `kiro-cli chat --acp --protocol-version 3`;
  - Suporta seleção de modelos suportados pelo Kiro e 6 níveis de reasoning effort (Default, Low, Medium, High, Extra High, Max);
  - Implementa suporte a aprovações interativas de ferramentas, permissões e compatibilidade com a CLI instalada no host.
- **Regra unificada de enclosing workspace e melhorias na CLI (`#39733`):**
  - Implementa a função única `resolveEnclosingWorkspace` garantindo resolução determinística do workspace ativo baseada no `cwd`;
  - Adiciona suporte explícito a `--environment local` e `--parent-environment` nos comandos `worktree create` e `worktree set`;
  - Inclui linha formatada e copiável `address: <url>` na saída de `worktree ps` e `worktree show`;
  - Impede a destruição do workspace em execução rejeitando `worktree rm --worktree current|active` com erro explicativo.
- **Terminal destacado em janela própria para Floating Workspaces (`#39722`):**
  - Introduz a capacidade experimental de abrir o terminal ativo do Floating Workspace em sua própria janela independente do Electron,
    com sincronização de estado, ciclo de vida e redimensionamento desacoplado.
- **Abertura do seletor de branches diretamente sob o composer do chat (`#39692`):**
  - Torna o indicador de branch sob o composer em botão interativo que dispara o seletor rápido de branches da barra de status.
- **Correção de pareamento com binds de interface (`#39741`):**
  - Detecta a interface de rede especificada no bind do servidor `serve`, anunciando o endereço correto no QR code e payload de pareamento mobile.

## O que fazer

- Integrar o Kiro como agente selecionável no Native Chat via ACP com seletor de esforço (`#39769`).
- Adotar a regra unificada `resolveEnclosingWorkspace`, a flag `--parent-environment` e a proteção contra auto-remoção de worktrees na CLI (`#39733`).
- Avaliar e portar a janela independente para terminais de Floating Workspaces (`#39722`).
- Habilitar o clique no nome do branch sob o composer de chat para acionar o seletor de branches (`#39692`).
- Garantir que o `brza serve` suporte pareamento correto em binds fixados de rede/Tailscale (`#39741`).
