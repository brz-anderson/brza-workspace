---
status: open
description: As issues #37833 e os PRs #37567, #37568, #37569, #37943 e #37998 trazem chaveamento e reinício imediato de contas Claude, novo sign-in no Antigravity e gestão de cache.
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
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569).

## O problema

1. **Queima de conta esgotada após troca (`#37943`):** ao alternar para uma nova conta Claude nas configurações, sessões
   e subagentes em execução em segundo plano continuavam vinculados à conta esgotada antiga até serem reiniciados
   manualmente, gerando falhas em cascata de rate limit.
2. **Reuso persistente de credenciais inválidas no Antigravity Chat (`#37998`):** o comando de troca de conta do Antigravity
   Chat reaproveitava silenciosamente tokens de autenticação armazenados em cache local, impedindo um fluxo de sign-in
   completamente limpo para nova identidade.
3. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
   janela de cache de prompt (1 hora em contextos ≥ 200k tokens). No CLI do Claude Code, a compactação ociosa
   (`idleCompaction`) roda automaticamente antes do cache expirar. Porém, dentro do runtime gráfico/desktop essa
   rotina é completamente desarmada porque o Claude roda sem TTY interativo (`stream-json`), seu ponto de entrada é
   identificado como `sdk-ts` e leva `CLAUDE_CODE_CHILD_SESSION=1`. Ao enviar a mensagem seguinte, todo o histórico é
   reenviado como entrada fria, multiplicando o custo e tempo de inferência.
4. **Estouro de cota sem chaveamento preventivo (`#37567`):** tarefas longas de agentes interrompem bruscamente com
   erro de limite de taxa (`rate limit` / janela de 5 horas ou semanal). Falta ao runtime um registro de qual conta
   pertence a cada painel (`pane account registry`) e uma troca proativa antes da interrupção.
5. **Contas inativas e servidores headless sem leitura de cota (`#37568`, `#37569`):** servidores remotos de background
   (`orca serve` / `brza serve`) sem janela aberta não consultavam os limites de uso de contas salvas, e tokens de
   acesso de contas ociosas expiravam sem renovação em segundo plano.

## O que o upstream propõe e implementa

- **Reinício imediato na troca de conta (`#37943`):** reinicia instantaneamente as sessões e workers do Claude na nova
  conta ao confirmar a troca, abortando turnos bloqueados na conta antiga.
- **Login limpo no Antigravity Chat (`#37998`):** o menu "Change account" descarta credenciais em cache e força um novo fluxo
  de autorização via navegador.
- **Opção Ultracode no seletor de esforço do Claude (`#38010`):** disponibiliza o nível de esforço `Ultracode` no seletor
  de modelos/raciocínio do Claude.
- **Prevenção de estouro de cota (`#37567`, `#37568`, `#37569`):**
  - Implementa registro de contas por painel: grava `{ ptyId, accountId, configDir, launchedAt, source }` e expõe a
    contagem de sessões ativas por conta em `orca account list`;
  - Adiciona chaveamento automático preventivo ("Switch before a usage limit"): ao atingir 90% da janela de 5h ou
    semanal, o runtime seleciona automaticamente a conta disponível com mais folga (com cooldown de 5 minutos);
  - Adiciona polling contínuo de quotas para hosts sem janela desktop (`pollWithoutWindow`) e renovação de tokens
    inativos.
- **Manutenção de prompt cache (`#37833`):**
  - Monitora a ociosidade de chats com contexto grande e dispara compactação antes da expiração da janela de 1h.

## O que fazer

Portar o suporte de `pane account registry`, alternância preventiva e reinício instantâneo de sessões (`#37943`, `#37998`)
para o `brza-studio`, protegendo as automações de 6h e execuções longas do `brza-workflow` contra interrupções de cota.
