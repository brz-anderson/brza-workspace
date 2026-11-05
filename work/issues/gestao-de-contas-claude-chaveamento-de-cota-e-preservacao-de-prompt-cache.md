---
status: open
description: Os PRs #38509, #38298, #38227, #38149 e #38026 e as issues #38547 e #38254 trazem métricas /stats no Usage Tracking, chaveamento de cota, perfis isolados e reinício sob crons.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#38509`](https://github.com/stablyai/orca/pull/38509),
[`stablyai/orca#38298`](https://github.com/stablyai/orca/pull/38298),
[`stablyai/orca#38227`](https://github.com/stablyai/orca/pull/38227),
[`stablyai/orca#38149`](https://github.com/stablyai/orca/pull/38149),
[`stablyai/orca#38026`](https://github.com/stablyai/orca/pull/38026),
[`stablyai/orca#38201`](https://github.com/stablyai/orca/pull/38201) (Issue [`#38195`](https://github.com/stablyai/orca/issues/38195)),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#38010`](https://github.com/stablyai/orca/pull/38010),
[`stablyai/orca#37567`](https://github.com/stablyai/orca/pull/37567),
[`stablyai/orca#37568`](https://github.com/stablyai/orca/pull/37568) e
[`stablyai/orca#37569`](https://github.com/stablyai/orca/pull/37569), além das issues
[`stablyai/orca#38547`](https://github.com/stablyai/orca/issues/38547),
[`stablyai/orca#38528`](https://github.com/stablyai/orca/issues/38528),
[`stablyai/orca#38254`](https://github.com/stablyai/orca/issues/38254),
[`stablyai/orca#38224`](https://github.com/stablyai/orca/issues/38224),
[`stablyai/orca#38134`](https://github.com/stablyai/orca/issues/38134),
[`stablyai/orca#38116`](https://github.com/stablyai/orca/issues/38116),
[`stablyai/orca#38052`](https://github.com/stablyai/orca/issues/38052),
[`stablyai/orca#38024`](https://github.com/stablyai/orca/issues/38024),
[`stablyai/orca#38085`](https://github.com/stablyai/orca/issues/38085) e
[`stablyai/orca#37833`](https://github.com/stablyai/orca/issues/37833).

## O problema

1. **Divergência entre contagem de tokens do app e `/stats` do Claude Code (`#38509`):**
   O painel Claude Usage Tracking computa totais apenas a partir dos transcripts do próprio app. O total de vida útil
   reportado nativamente pelo Claude Code via `/stats` (armazenado em `~/.claude/stats-cache.json`) não era visível, gerando
   confusão sobre o consumo histórico global da conta em múltiplos ambientes (WSL, servidores remotos).
2. **Panes limitadas por cota com crons ativos não reiniciam na troca de conta (`#38547`):**
   Ao configurar reinício automático na troca de conta ("Always restart"), uma pane do Claude que bateu no limite de 5h
   e possui agendamentos/crons de sessão fica travada aguardando indefinidamente um estado `done` que nunca chega,
   impossibilitando o chaveamento automático até que o usuário mate manualmente o processo com `/exit`.
3. **Falta de fallback automático entre contas para helpers pontuais de IA (`#38528`):**
   Quando geradores automáticos de texto (nomes de chat, mensagens de commit, descrições) batem em limite de assinatura de
   uma conta, a operação falha em vez de tentar contas alternativas salvas.
4. **Inexistência de seleção CLI para contas Claude (`#38227`):** o comando `orca account select` aceitava apenas OpenCode
   e Devin. Não era possível alternar ou automatizar via scripts e agentes qual conta Claude ativa deve ser usada para novos
   disparos, nem rotear a seleção para hosts remotos (`--environment`).
5. **Panes de longa duração mantêm `CLAUDE_CONFIG_DIR` antigo após troca de conta (`#38254`):**
   Ao alternar a conta Claude ativa pelo app ou CLI, apenas a aba em foco ou processos recém-criados recebiam o novo ambiente;
   panes em execução contínua ou terminais abertos em segundo plano continuavam apontando para o diretório de perfil antigo,
   causando consumo fantasma na conta anterior.
6. **Parada sem ação ao atingir limite de cota no cliente mobile (`#38298`):**
   Ao receber notificações de limite de uso no app mobile, o usuário não dispunha de atalhos rápidos para alternar para uma
   conta secundária ou programar retomada automática ("Automatic continue") assim que a janela de cota resetar.
7. **Consumo desproporcional de cota em abas de chat vs. terminal (`#38224`):** usuários observaram que conversas conduzidas
   em abas de Chat UI consomem cerca de 1,5× mais da janela de 5 horas do Claude do que as mesmas tarefas em abas de
   terminal cru, devido a diferenças na injeção de preâmbulos e repasse de histórico não compactado.
8. **Subcontagem de tokens em transcripts bifurcados (`#38201`, `#38195`):** ao chavear sessões ou forkar transcrições, a
   contabilidade de tokens de saída descartava valores maiores computados por outros arquivos de transcrição compartilhados.
9. **Perfis customizados de Claude atrelados a diretórios do usuário (`#38149`):** desenvolvedores que mantêm múltiplas
   instalações/contas locais de Claude (ex.: `~/.claude-trabalho`, `~/.claude-pessoal`) não tinham como cadastrá-las no app
   como opções persistentes no menu de agentes da barra de abas sem sobrescrever o diretório padrão `~/.claude`.
10. **Parada sem feedback em usage limits de terminais (`#38026`):** agentes Claude e Codex rodando em terminais paravam
    abruptamente ao bater no teto de uso da conta sem exibir quando a cota seria resetada nem oferecer um meio interativo de
    retomada sem ter que digitar novamente no terminal ou reiniciar o processo.
11. **Subagentes disparados via CLI não herdam a conta do chamador (`#38052`):** quando um agente coordenador dispara um
    subagente ou revisor via CLI, o novo agente inicia na conta globalmente selecionada no app, arriscando debitar cotas
    pessoais em tarefas de trabalho.
12. **Perda de prompt cache em chats ociosos (`#37833`):** uma aba de Native Chat com Claude deixada ociosa perde a
    janela de cache de prompt (1 hora em contextos ≥ 200k tokens), multiplicando custos e tempo de resposta.

## O que o upstream propõe e implementa

- **Exibição de tokens vitalícios do `/stats` do Claude Code (`#38509`):**
  - Lê `<config home>/stats-cache.json` e renderiza ao lado do título do painel a contagem vitalícia (ex.: `58.6B lifetime tokens`),
    discriminando por histórico de conta/host sem misturar filtros locais de transcript.
- **Detecção e destravamento de panes em limite com crons ativos (`#38547`):**
  - Proposta para forçar a transição de saída e reiniciar o processo PTY quando um chaveamento de conta for solicitado em
    sessões sob limite de cota com agendamentos de cron ativos.
- **Seleção CLI de contas Claude (`#38227`):**
  - Estende `orca account select --agent claude --account <id|system>`;
  - Permite direcionar a seleção para instâncias remotas usando `--environment <selector>`;
  - Reutiliza a RPC interna `accounts.selectClaude` já validada no app desktop.
- **Propagação consistente de conta entre todas as panes (`#38254`):**
  - Proposta para sinalizar e reiniciar uniformemente todas as panes atreladas ao runtime de Claude quando houver troca de
    conta, atualizando `CLAUDE_CONFIG_DIR` em tempo real.
- **Ações de retomada e troca de conta em avisos de limite (`#38298`):**
  - Oferece suporte a "Automatic continue" e "Switch Account" diretamente nos avisos de usage limit no cliente mobile e
    notificações push.
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

- Integrar a leitura de `stats-cache.json` (`#38509`) no `brza-studio` para exibir contagem vitalícia de tokens Claude.
- Resolver o travamento de reinício de panes com crons sob limite de cota (`#38547`).
- Portar o comando `orca account select --agent claude` (`#38227`) para a CLI do `brza`.
- Adotar o suporte a `claudeConfigProfiles` (`#38149`) no `brza-studio` e garantir reinício/atualização de `CLAUDE_CONFIG_DIR`
  em todas as panes (`#38254`).
- Incorporar o fluxo de "Automatic continue / Switch Account" (`#38298`, `#38026`) nas notificações e terminais.
- Ajustar a parametrização de preâmbulos para mitigar o consumo de tokens no Native Chat (`#38224`).
