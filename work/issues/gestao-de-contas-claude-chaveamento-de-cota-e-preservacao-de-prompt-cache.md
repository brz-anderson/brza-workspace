---
status: open
description: O PR #38227, o PR #38149 e o PR #38026 trazem seleção CLI de contas Claude, perfis de pasta isolados e recuperação de limites de uso em terminais.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38227`](https://github.com/stablyai/orca/pull/38227),
[`stablyai/orca#38149`](https://github.com/stablyai/orca/pull/38149),
[`stablyai/orca#38026`](https://github.com/stablyai/orca/pull/38026),
[`stablyai/orca#38201`](https://github.com/stablyai/orca/pull/38201) (Issue [`#38195`](https://github.com/stablyai/orca/issues/38195)),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569), além das issues
[`stablyai/orca#38224`](https://github.com/stablyai/orca/issues/38224),
[`stablyai/orca#38134`](https://github.com/stablyai/orca/issues/38134),
[`stablyai/orca#38116`](https://github.com/stablyai/orca/issues/38116),
[`stablyai/orca#38052`](https://github.com/stablyai/orca/issues/38052),
[`stablyai/orca#38024`](https://github.com/stablyai/orca/issues/38024),
[`stablyai/orca#38085`](https://github.com/stablyai/orca/issues/38085) e
[`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833).

## O problema

1. **Inexistência de seleção CLI para contas Claude (`#38227`):** o comando `orca account select` aceitava apenas OpenCode
   e Devin. Não era possível alternar ou automatizar via scripts e agentes qual conta Claude ativa deve ser usada para novos
   disparos, nem rotear a seleção para hosts remotos (`--environment`).
2. **Consumo desproporcional de cota em abas de chat vs. terminal (`#38224`):** usuários observaram que conversas conduzidas
   em abas de Chat UI consomem cerca de 1,5× mais da janela de 5 horas do Claude do que as mesmas tarefas em abas de
   terminal cru, devido a diferenças na injeção de preâmbulos e repasse de histórico não compactado.
3. **Subcontagem de tokens em transcripts bifurcados (`#38201`, `#38195`):** ao chavear sessões ou forkar transcrições, a
   contabilidade de tokens de saída descartava valores maiores computados por outros arquivos de transcrição compartilhados.
4. **Perfis customizados de Claude atrelados a diretórios do usuário (`#38149`):** desenvolvedores que mantêm múltiplas
   instalações/contas locais de Claude (ex.: `~/.claude-trabalho`, `~/.claude-pessoal`) não tinham como cadastrá-las no app
   como opções persistentes no menu de agentes da barra de abas sem sobrescrever o diretório padrão `~/.claude`.
5. **Parada sem feedback em usage limits de terminais (`#38026`):** agentes Claude e Codex rodando em terminais paravam
   abruptamente ao bater no teto de uso da conta sem exibir quando a cota seria resetada nem oferecer um meio interativo de
   retomada sem ter que digitar novamente no terminal ou reiniciar o processo.
6. **Subagentes disparados via CLI não herdam a conta do chamador (`#38052`):** quando um agente coordenador dispara um
   subagente ou revisor via CLI, o novo agente inicia na conta globalmente selecionada no app, arriscando debitar cotas
   pessoais em tarefas de trabalho.
7. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
   janela de cache de prompt (1 hora em contextos ≥ 200k tokens), multiplicando custos e tempo de resposta.

## O que o upstream propõe e implementa

- **Seleção CLI de contas Claude (`#38227`):**
  - Estende `orca account select --agent claude --account <id|system>`;
  - Permite direcionar a seleção para instâncias remotas usando `--environment <selector>`;
  - Reutiliza a RPC interna `accounts.selectClaude` já validada no app desktop.
- **Preservação de contagem cheia de tokens (`#38201`):** retém o maior valor de tokens de saída medido entre transcrições
  irmãs concorrentes.
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

## O que fazer

Portar o comando `orca account select --agent claude` (`#38227`) para a CLI do `brza`, adotar o suporte a
`claudeConfigProfiles` (`#38149`) no `brza-studio` e ajustar a parametrização de preâmbulos para mitigar o consumo de
tokens no Native Chat (`#38224`).
