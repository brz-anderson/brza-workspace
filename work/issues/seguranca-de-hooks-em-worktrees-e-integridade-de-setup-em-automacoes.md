---
status: open
description: Os PRs #38128, #37977, #37978, #37979, #38019 e #38029 do upstream reforçam a integridade de hooks, teardown limpo de worktrees e padronização de agentes em automações.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38128`](https://github.com/stablyai/orca/pull/38128) (Issue
[`#37902`](https://github.com/stablyai/orca/issues/37902)),
[`stablyai/orca#37977`](https://github.com/stablyai/orca/pull/37977),
[`stablyai/orca#37978`](https://github.com/stablyai/orca/pull/37978),
[`stablyai/orca#37979`](https://github.com/stablyai/orca/pull/37979),
[`stablyai/orca#38019`](https://github.com/stablyai/orca/pull/38019),
[`stablyai/orca#38029`](https://github.com/stablyai/orca/pull/38029),
[`stablyai/orca#33492`](https://github.com/stablyai/orca/pull/33492),
[`stablyai/orca#37941`](https://github.com/stablyai/orca/pull/37941) e
[`stablyai/orca#37931`](https://github.com/stablyai/orca/pull/37931).

## O problema

1. **Falha espúria na remoção de worktrees externos por negação de acesso no watcher (`#38128`, `#37902`):** ao remover
   worktrees situados fora da pasta principal do workspace, o `git worktree remove` concluía com sucesso, mas o encerramento
   do observador de arquivos (`closeFileExplorerWatchersForPath`) tentava re-autorizar o caminho já desregistrado pelo Git.
   Isso disparava `PATH_ACCESS_DENIED_MESSAGE` e abortava com erro a rotina de exclusão, deixando o usuário em estado inconsistente.
2. **Execução cega de scripts de setup em branches untrusted (`#37977`, `#37978`):** ao alternar branches ou criar
   worktrees vinculados a PRs externos, comandos definidos em `orca.yaml` (ou ganchos equivalentes de inicialização de
   worktree) eram disparados automaticamente. Isso abria vetor de execução arbitrária de código (RCE) caso uma branch
   ou fork malicioso alterasse o script de setup.
3. **Automações e runners executando hooks alterados sem validação (`#37979`):** o runner de automações não persistia o
   hash do script de setup previamente aprovado pelo usuário. Se uma automação baixasse ou fizesse checkout de uma branch
   com hook adulterado, o hook rodava com as permissões do app.
4. **Bloqueio espúrio em disparos manuais de automações (`#38029`):** ao clicar em "Run Now" no painel de Automações,
   o disparo falhava se a verificação da ferramenta de fonte do GitHub estivesse indisponível ou desconectada.
5. **Vazamento e retenção de agentes completados em automações (`#33492`):** agentes de automações anteriores mantidos
   abertos apenas para monitoramento de término não eram reutilizados eficientemente, gerando processos órfãos.

## O que o upstream propõe e implementa

- **Teardown limpo de observadores sem re-autorização pós-exclusão (`#38128`, resolve `#37902`):**
  - Trata `PATH_ACCESS_DENIED_MESSAGE` no teardown de watchers como indicativo de caminho já removido, ignorando a falha
    e permitindo que `worktree.remove` conclua sem erros espúrios em layouts de worktrees irmãos.
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

Portar as proteções de integridade de hooks (`#37977`, `#37978`, `#37979`) e o conserto de remoção de worktrees (`#38128`)
para o `brza-studio`, além de aplicar o reuso de agentes de automações (`#38029`, `#33492`) no agendador de 6h do `brza-workflow`.
