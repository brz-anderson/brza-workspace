---
status: open
description: O PR #38149, o PR #38026 e a issue #38052 trazem perfis de pasta para Claude, recuperação de limite em terminais e herança de conta por subagentes.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38149`](https://github.com/stablyai/orca/pull/38149),
[`stablyai/orca#38026`](https://github.com/stablyai/orca/pull/38026),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569), além das issues
[`stablyai/orca#38134`](https://github.com/stablyai/orca/issues/38134),
[`stablyai/orca#38116`](https://github.com/stablyai/orca/issues/38116),
[`stablyai/orca#38052`](https://github.com/stablyai/orca/issues/38052),
[`stablyai/orca#38024`](https://github.com/stablyai/orca/issues/38024),
[`stablyai/orca#38085`](https://github.com/stablyai/orca/issues/38085) e
[`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833).

## O problema

1. **Perfis customizados de Claude atrelados a diretórios do usuário (`#38149`):** desenvolvedores que mantêm múltiplas
   instalações/contas locais de Claude (ex.: `~/.claude-trabalho`, `~/.claude-pessoal`) não tinham como cadastrá-las no app
   como opções persistentes no menu de agentes da barra de abas sem sobrescrever o diretório padrão `~/.claude`.
2. **Parada sem feedback em usage limits de terminais (`#38026`):** agentes Claude e Codex rodando em terminais paravam
   abruptamente ao bater no teto de uso da conta sem exibir quando a cota seria resetada nem oferecer um meio interativo de
   retomada sem ter que digitar novamente no terminal ou reiniciar o processo.
3. **Subagentes disparados via CLI não herdam a conta do chamador (`#38052`):** quando um agente coordenador dispara um
   subagente ou revisor via CLI (`orca worktree create --agent claude`, `agent launch` ou `orchestration worker-start`), o
   novo agente inicia na conta globalmente selecionada no app naquele instante, e não na conta do painel chamador.
4. **Falta de visão global de consumo e estado de hosts remotos (`#38134`, `#38116`):** em arquiteturas com múltiplos
   workspaces e hosts SSH pareados, o app não oferecia dashboard unificado de cotas/limites de uso nem mantinha o computador
   acordado (`keep-awake`) ao detectar agentes trabalhando em servidores SSH remotos.
5. **Queima de conta esgotada após troca (`#37943`):** ao alternar para uma nova conta Claude nas configurações, sessões
   e subagentes em execução em segundo plano continuavam vinculados à conta esgotada antiga.
6. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
   janela de cache de prompt (1 hora em contextos ≥ 200k tokens), multiplicando custos e tempo de resposta.

## O que o upstream propõe e implementa

- **Lançamento de Claude em perfis locais definidos pelo usuário (`#38149`):**
  - Adiciona suporte a `claudeConfigProfiles` nas configurações (`Settings > AI Provider Accounts > Claude > Claude Profiles`),
    permitindo cadastrar diretórios absolutos (ex.: `~/.claude-a`);
  - Expõe entradas no menu de agentes da barra de abas ("Claude · a", "Claude · b");
  - Injeta `ORCA_CLAUDE_CONFIG_PROFILE_DIR` e preserva o login e histórico isolados da pasta sem interferir na conta global selecionada.
- **Recuperação de usage-limit direto na pane do terminal (`#38026`):**
  - Exibe cartão integrado no painel do terminal informando o horário exato de reset da cota e botão "Continue now";
  - Valida o turno falho antes do reenvio, recusa drafts residuais e preserva prompts de plugins.
- **Herança de conta Claude por subagentes da CLI (`#38052`):**
  - Propõe que invocações feitas a partir de um terminal Orca repassem o perfil/`CLAUDE_CONFIG_DIR` do painel chamador
    para o novo agente filho, mantendo workstreams isolados em suas respectivas contas com opção de override via `--account`.
- **Dashboard Global e monitoramento em hosts SSH (`#38134`, `#38116`):**
  - Proposta de dashboard Home global para status da frota e limites de uso, além de keep-awake estendido a agentes remotos.
- **Reinício imediato na troca de conta (`#37943`):** reinicia instantaneamente as sessões e workers do Claude na nova
  conta ao confirmar a troca, abortando turnos bloqueados na conta antiga.
- **Login limpo no Antigravity Chat (`#37998`):** descarta credenciais em cache e força novo fluxo de autorização via navegador.

## O que fazer

Portar o suporte de `claudeConfigProfiles` (`#38149`) e o cartão de recuperação de usage-limit (`#38026`) para o `brza-studio`,
e incorporar a herança de perfil em subagentes CLI (`#38052`) no `brza-workflow`.
