---
status: open
description: O PR #38026, a issue #38052 e os PRs #37943, #37567 e #37568 trazem recuperação de usage-limit em terminais, herança de conta por subagentes e gestão de cota Claude.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38026`](https://github.com/stablyai/orca/pull/38026),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569), além das issues
[`stablyai/orca#38052`](https://github.com/stablyai/orca/issues/38052),
[`stablyai/orca#38024`](https://github.com/stablyai/orca/issues/38024),
[`stablyai/orca#38085`](https://github.com/stablyai/orca/issues/38085) e
[`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833).

## O problema

1. **Parada sem feedback em usage limits de terminais (`#38026`):** agentes Claude e Codex rodando em terminais paravam
   abruptamente ao bater no teto de uso da conta sem exibir quando a cota seria resetada nem oferecer um meio interativo de
   retomada sem ter que digitar novamente no terminal ou reiniciar o processo.
2. **Subagentes disparados via CLI não herdam a conta do chamador (`#38052`):** quando um agente coordenador dispara um
   subagente ou revisor via CLI (`orca worktree create --agent claude`, `agent launch` ou `orchestration worker-start`), o
   novo agente inicia na conta globalmente selecionada no app naquele instante, e não na conta do painel chamador. Se o
   usuário tiver alternado de conta para outra tarefa, subagentes de trabalho usam cotas de contas pessoais sem aviso.
3. **Queima de conta esgotada após troca (`#37943`):** ao alternar para uma nova conta Claude nas configurações, sessões
   e subagentes em execução em segundo plano continuavam vinculados à conta esgotada antiga até serem reiniciados
   manualmente, gerando falhas em cascata de rate limit.
4. **Reuso persistente de credenciais inválidas no Antigravity Chat (`#37998`):** o comando de troca de conta do Antigravity
   Chat reaproveitava silenciosamente tokens de autenticação armazenados em cache local, impedindo um fluxo de sign-in
   completamente limpo para nova identidade.
5. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
   janela de cache de prompt (1 hora em contextos ≥ 200k tokens), multiplicando custos e tempo de resposta.

## O que o upstream propõe e implementa

- **Recuperação de usage-limit direto na pane do terminal (`#38026`):**
  - Exibe cartão integrado no painel do terminal informando o horário exato de reset da cota e botão "Continue now";
  - Valida o turno falho antes do reenvio, recusa drafts residuais e preserva prompts de plugins;
  - Mantém o estado minimizável sem interferir na entrada padrão do terminal.
- **Herança de conta Claude por subagentes da CLI (`#38052`):**
  - Propõe que invocações feitas a partir de um terminal Orca repassem o perfil/`CLAUDE_CONFIG_DIR` do painel chamador
    para o novo agente filho, mantendo workstreams isolados em suas respectivas contas com opção de override via `--account`.
- **Reinício imediato na troca de conta (`#37943`):** reinicia instantaneamente as sessões e workers do Claude na nova
  conta ao confirmar a troca, abortando turnos bloqueados na conta antiga.
- **Login limpo no Antigravity Chat (`#37998`):** o menu "Change account" descarta credenciais em cache e força um novo fluxo
  de autorização via navegador.
- **Prevenção proativa de estouro de cota (`#37567`, `#37568`, `#37569`):** registro de contas por painel, alternância
  automática preventiva aos 90% da cota e polling contínuo para hosts headless.

## O que fazer

Portar o cartão de recuperação de usage-limit (`#38026`) para o `brza-studio`, implementar a herança de conta do painel
chamador em subagentes CLI (`#38052`) e sincronizar o chaveamento preventivo no `brza-workflow`.
