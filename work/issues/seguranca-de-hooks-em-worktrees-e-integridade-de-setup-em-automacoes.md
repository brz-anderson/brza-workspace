---
status: open
description: Os PRs #37977, #37978, #37979, #37941 e #37931 do upstream reforçam a segurança de hooks de setup em worktrees e automações, validando hash SHA-256 antes da execução de scripts e prevenindo RCE de branches não confiáveis.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
---

# Segurança de hooks em worktrees e integridade de setup em automações

Rastreado dos PRs abertos no upstream [`stablyai/orca#37977`](https://github.com/stablyai/orca/pull/37977),
[`stablyai/orca#37978`](https://github.com/stablyai/orca/pull/37978),
[`stablyai/orca#37979`](https://github.com/stablyai/orca/pull/37979),
[`stablyai/orca#37941`](https://github.com/stablyai/orca/pull/37941) e
[`stablyai/orca#37931`](https://github.com/stablyai/orca/pull/37931).

## O problema

1. **Execução cega de scripts de setup em branches untrusted (`#37977`, `#37978`):** ao alternar branches ou criar
   worktrees vinculados a PRs externos, comandos definidos em `orca.yaml` (ou ganchos equivalentes de inicialização de
   worktree) eram disparados automaticamente. Isso abria vetor de execução arbitrária de código (RCE) caso uma branch
   ou fork malicioso alterasse o script de setup.
2. **Automações e runners executando hooks alterados sem validação (`#37979`):** o runner de automações não persistia o
   hash do script de setup previamente aprovado pelo usuário. Se uma automação baixasse ou fizesse checkout de uma branch
   com hook adulterado, o hook rodava com as permissões do app.
3. **Execução de comandos arbitrários de issue sem confirmação (`#37931`):** scripts commitados sob `.orca/issue-command`
   eram invocados automaticamente sem consentimento explícito do operador humano.
4. **Falta de seletor padronizado de agente e permissões em automações (`#37941`):** o agendador de automações usava
   parâmetros simplificados, sem paridade com o seletor compartilhado de agentes (modelo, reasoning effort, perfil de
   permissões, modo Fast e argumentos).

## O que o upstream propõe e implementa

- **Validação criptográfica de integridade de hooks (`#37977`, `#37978`, `#37979`):**
  - Calcula o hash SHA-256 normalizado (trimmed) do script/comando de setup configurado;
  - Bloqueia a execução automática quando o conteúdo da branch diferir do script aprovado;
  - Adiciona o fluxo `worktrees:runApprovedSetup` para que o usuário aprove explicitamente a nova versão antes da execução;
  - Automações armazenam o hash aprovado do setup e ignoram silenciosamente ou abortam quando a branch trouxer alterações
    não homologadas.
- **Confirmação antes de rodar `.orca/issue-command` (`#37931`):** solicita aprovação interativa antes de executar
  qualquer script comitado na pasta `.orca/`.
- **Seletor compartilhado em automações (`#37941`):** unifica a seleção de agente nas automações, permitindo configurar
  modelo, effort, permissões e argumentos com a mesma interface do launch padrão.

## O que fazer

Portar as proteções de integridade de hooks (`#37977`, `#37978`, `#37979`, `#37931`) para o runtime do `brza-studio` e
para os comandos de worktree do `brza-workflow`, garantindo que automações periódicas e checkouts de branches externas
nunca executem scripts de inicialização arbitrários sem aprovação de hash.
