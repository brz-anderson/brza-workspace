---
status: open
description: A issue #37833 e os PRs #37567, #37568 e #37569 trazem chaveamento preventivo de contas Claude a 90% da cota, polling em hosts headless e manutenção/compactação de prompt cache em chats ociosos.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Gestão de contas Claude, chaveamento de cota e preservação de prompt cache

Rastreado da issue aberta no upstream [`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833) e dos PRs
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569).

## O problema

1. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
   janela de cache de prompt (1 hora em contextos ≥ 200k tokens). No CLI do Claude Code, a compactação ociosa
   (`idleCompaction`) roda automaticamente antes do cache expirar. Porém, dentro do runtime gráfico/desktop essa
   rotina é completamente desarmada porque o Claude roda sem TTY interativo (`stream-json`), seu ponto de entrada é
   identificado como `sdk-ts` e leva `CLAUDE_CODE_CHILD_SESSION=1`. Ao enviar a mensagem seguinte, todo o histórico é
   reenviado como entrada fria, multiplicando o custo e tempo de inferência.
2. **Estouro de cota sem chaveamento preventivo (`#37567`):** tarefas longas de agentes interrompem bruscamente com
   erro de limite de taxa (`rate limit` / janela de 5 horas ou semanal). Falta ao runtime um registro de qual conta
   pertence a cada painel (`pane account registry`) e uma troca proativa antes da interrupção.
3. **Contas inativas e servidores headless sem leitura de cota (`#37568`, `#37569`):** servidores remotos de background
   (`orca serve` / `brza serve`) sem janela aberta não consultavam os limites de uso de contas salvas, e tokens de
   acesso de contas ociosas expiravam sem renovação em segundo plano.

## O que o upstream propõe e implementa

- **Prevenção de estouro de cota (`#37567`, `#37568`, `#37569`):**
  - Implementa registro de contas por painel: grava `{ ptyId, accountId, configDir, launchedAt, source }` e expõe a
    contagem de sessões ativas por conta em `orca account list`;
  - Adiciona chaveamento automático preventivo ("Switch before a usage limit"): ao atingir 90% da janela de 5h ou
    semanal, o runtime seleciona automaticamente a conta disponível com mais folga (com cooldown de 5 minutos);
  - Adiciona polling contínuo de quotas para hosts sem janela desktop (`pollWithoutWindow`) e renovação de tokens
    inativos.
- **Manutenção de prompt cache (`#37833`):**
  - Propõe que o runtime do app monitore o tempo ocioso de chats com contexto grande e dispare keep-warm sintético ou
    uma ação explícita de compactação antes do vencimento da janela de cache de 1h.

## O que fazer

Portar o suporte de `pane account registry` e alternância preventiva de contas para o `brza-studio`, além de implementar
no `brza-workflow` o monitoramento e compactação preventiva de chats ociosos para preservar o cache de prompt e mitigar
custos de tokens em turnos sequenciais.
