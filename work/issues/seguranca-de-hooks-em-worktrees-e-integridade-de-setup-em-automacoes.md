---
status: open
description: Os PRs #37977, #37978, #37979, #38019, #38029 e #33492 do upstream reforçam a integridade de hooks, validação SHA-256 e padronização de agentes em automações.
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
[`stablyai/orca#38019`](https://github.com/stablyai/orca/pull/38019),
[`stablyai/orca#38029`](https://github.com/stablyai/orca/pull/38029),
[`stablyai/orca#33492`](https://github.com/stablyai/orca/pull/33492),
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
3. **Bloqueio espúrio em disparos manuais de automações (`#38029`):** ao clicar em "Run Now" no painel de Automações,
   o disparo falhava se a verificação da ferramenta de fonte do GitHub estivesse indisponível ou desconectada, mesmo quando
   a automação operava sobre arquivos e branches locais.
4. **Vazamento e retenção de agentes completados em automações (`#33492`):** agentes de automações anteriores mantidos
   abertos apenas para monitoramento de término não eram reutilizados eficientemente, gerando processos órfãos.
5. **Divergência de configuração de agentes entre superfícies (`#37941`, `#38019`):** enquanto o Chat padrão possuía
   seletor rico de modelo, esforço de raciocínio, perfil de permissões e argumentos, a autoria de mensagens no Source
   Control e disparos de automações usavam configurações engessadas.

## O que o upstream propõe e implementa

- **Validação criptográfica de integridade de hooks (`#37977`, `#37978`, `#37979`):**
  - Calcula o hash SHA-256 normalizado do script/comando de setup configurado;
  - Bloqueia a execução automática quando o conteúdo da branch diferir do script aprovado;
  - Adiciona o fluxo `worktrees:runApprovedSetup` para que o usuário aprove explicitamente a nova versão antes da execução;
  - Automações armazenam o hash aprovado do setup e ignoram silenciosamente ou abortam quando a branch trouxer alterações
    não homologadas.
- **Robustez e agilidade no runner de automações (`#38029`, `#33492`):**
  - Permite que o comando "Run Now" dispare imediatamente sem validação desnecessária da ferramenta de repositório remoto;
  - Reutiliza de forma limpa agentes completados que estavam retidos apenas para monitoramento de conclusão.
- **Seletor compartilhado de agentes no Source Control e Automações (`#37941`, `#38019`):**
  - Unifica a escolha de modelo, reasoning effort, permissões e argumentos em todas as superfícies operadas por IA.
- **Confirmação antes de rodar `.orca/issue-command` (`#37931`):** solicita aprovação interativa antes de executar
  qualquer script comitado na pasta `.orca/`.

## O que fazer

Portar as proteções de integridade de hooks (`#37977`, `#37978`, `#37979`) para o `brza-studio` e aplicar as melhorias
de disparo e reuso de agentes de automações (`#38029`, `#33492`) no agendador de 6h do `brza-workflow`.
