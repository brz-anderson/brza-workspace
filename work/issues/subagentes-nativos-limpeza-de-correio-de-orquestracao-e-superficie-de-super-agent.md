---
status: open
description: Os PRs #37574, #33403, #37918 e #37966 e as issues #37407, #37637 e #38000 do upstream refinam o roteamento para subagentes, entrega de correio em turnos ativos e supervisão na UI.
scope:
  - brza-studio
  - brza-workflow
priority: medium
opened: 2026-11-03
tags:
  - chat
  - tooling
---

# Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent

Rastreado dos PRs abertos no upstream [`stablyai/orca#37918`](https://github.com/stablyai/orca/pull/37918),
[`stablyai/orca#37966`](https://github.com/stablyai/orca/pull/37966),
[`stablyai/orca#37974`](https://github.com/stablyai/orca/pull/37974),
[`stablyai/orca#37574`](https://github.com/stablyai/orca/pull/37574),
[`stablyai/orca#33403`](https://github.com/stablyai/orca/pull/33403),
[`stablyai/orca#21333`](https://github.com/stablyai/orca/pull/21333),
[`stablyai/orca#37703`](https://github.com/stablyai/orca/pull/37703),
[`stablyai/orca#37868`](https://github.com/stablyai/orca/pull/37868),
[`stablyai/orca#37866`](https://github.com/stablyai/orca/pull/37866),
[`stablyai/orca#37891`](https://github.com/stablyai/orca/pull/37891),
[`stablyai/orca#37850`](https://github.com/stablyai/orca/pull/37850) e
[`stablyai/orca#11279`](https://github.com/stablyai/orca/pull/11279), além das issues
[`stablyai/orca#38000`](https://github.com/stablyai/orca/issues/38000),
[`stablyai/orca#37741`](https://github.com/stablyai/orca/issues/37741),
[`stablyai/orca#37702`](https://github.com/stablyai/orca/issues/37702),
[`stablyai/orca#37693`](https://github.com/stablyai/orca/issues/37693),
[`stablyai/orca#37731`](https://github.com/stablyai/orca/issues/37731),
[`stablyai/orca#37867`](https://github.com/stablyai/orca/issues/37867),
[`stablyai/orca#37865`](https://github.com/stablyai/orca/issues/37865),
[`stablyai/orca#37849`](https://github.com/stablyai/orca/issues/37849),
[`stablyai/orca#37907`](https://github.com/stablyai/orca/issues/37907),
[`stablyai/orca#37683`](https://github.com/stablyai/orca/issues/37683),
[`stablyai/orca#37684`](https://github.com/stablyai/orca/issues/37684),
[`stablyai/orca#37407`](https://github.com/stablyai/orca/issues/37407),
[`stablyai/orca#37637`](https://github.com/stablyai/orca/issues/37637) e
[`stablyai/orca#19388`](https://github.com/stablyai/orca/issues/19388).

## Os pontos do upstream

1. **Entrega de correio durante turnos ativos via steering (`#37918`):**
   - O PR `#37918` entrega mensagens da caixa postal de orquestração diretamente durante turnos de execução ativos
     (via steering de agente), sem forçar o remetente a esperar que o turno termine ou fique ocioso. Isso resolve gargalos
     em que coordenadores demoravam dezenas de segundos para receber atualizações críticas de workers.
2. **Origem limpa de mensagens de conclusão em background (`#37966`):**
   - O PR `#37966` renderiza avisos de conclusão de tarefas em segundo plano exibindo o comando original disparado como fonte,
     em vez de fabricar um avatar ou bolha artificial de agente que confundia a autoria das ações.
3. **Diferenciação visual entre Coordenador e workers na UI (`#38000`):**
   - A issue `#38000` propõe hierarquia visual explícita na barra lateral / árvore de sessões entre o Coordenador e os
     workers operários, impedindo que o operador humano envie prompts manuais por engano diretamente a workers especializados.
4. **Limpeza de alertas de desktop já visualizados (`#37974`):**
   - O PR `#37974` limpa notificações de conclusão de tarefa da central do sistema operacional assim que o usuário foca ou
     reconhece a aba no aplicativo.
5. **Espera agendada e eliminação de falsos alertas de parada (`#37868`, `#37867`):**
   - `#37868` introduz `orchestration send --type status --wait-until <duration|ISO time>`, permitindo que workers
     de longa duração declarem espera explícita. Enquanto a espera for válida, a parada ociosa não dispara alerta HIGH
     de escalação ("Worker stopped without reporting") para o coordenador, resolvendo a issue `#37867`.
6. **Preservação de logs de falha no arranque e limpeza de mensagens (`#37866`, `#37865`, `#37891`, `#37850`, `#37849`):**
   - `#37866`: retém o tail de saída do terminal quando um worker morre durante o startup/readiness (ex.: travamento de
     importação Python em workers Hermes), anexando-o ao recibo de despacho em vez de descartar a tela;
   - `#37891`: exibe apenas o assunto e corpo limpo da mensagem de orquestração na UI e no botão copiar, removendo o
     envelope com IDs de sessão, separadores e comandos de resposta repetitivos;
   - `#37850`: limpa redundâncias na descrição da skill `orchestration`, encurtando o stub para economizar contexto.
7. **Ligação direta entre chats locais de agentes com controle do usuário (`#37741`):** propõe ação "Work together…" no
   cabeçalho do chat para emparelhar dois chats locais em worktrees diferentes, com introdução mútua, acordar parceiro
   quando ocioso, journal cronológico persistente e entrega sem conceder autoridade irrevogável ao agente.
8. **Ciclo de vida, retenção de permissões e recuperação de workers (`#37702`, `#37693`, `#37731`, `#37703`, `#37907`):**
   - `#37702`: permite ao coordenador fechar abas `--keep-open` após `ownership_transferred`, evitando acúmulo de abas;
   - `#37693`: corrige perda do modo de permissão configurado (Full access) ao reabrir worker via `orchestration send`;
   - `#37731`: corrige entrega de correio a workers Hermes que ficavam eternamente pendentes após restart do runtime;
   - `#37703`: retém a identidade do agente mesmo após encerramento do daemon pai.
9. **Filtros e leituras diretas de orquestração no host para plugins (`#37683`, `#37684`):**
   - `#37683`: adiciona `run-list --coordinator` para evitar paginação massiva em busca do Run de um terminal;
   - `#37684`: expõe chamadas de leitura direta em `agents.list` e no host sobre Runs e agentes filhos sem subprocessos.
10. **Preferência por subagentes nativos nomeados (`#37574`):** remove da skill `orchestration` (`skills/orchestration/SKILL.md`
    e `skill-guides/orchestration.md`) a regra que transformava toda requisição de revisão em um worker externo do app,
    preferindo os subagentes nativos nomeados do runtime quando disponíveis.
11. **Correio de orquestração recolhido e sem atropelar digitação (`#33403`, `#37637`, `#11279`):**
    - `#33403` recolhe envelopes internos de correio de orquestração e mantém a trilha do chat voltada para a conversa
      humana;
    - `#37637` pede que o assunto e o corpo enviados por um worker apareçam diretamente no Native Chat do coordenador;
    - `#11279` adia a injeção `push-on-idle` enquanto o usuário está digitando no composer (evitando o bug da `#14832`).
12. **Nome do worktree no preâmbulo de despacho (`#21333`) e GC de workers encerrados (`#19388`):** identifica o worktree
    do worker no preâmbulo e aponta a falta de coleta automática para workers em `terminalState=reclaimable`.
13. **Superfície estável para super-agent (`#37407`):** propõe contratos estáveis para que um supervisor externo observe,
    direcione e feche o ciclo de execução de agentes sem depender de scraping de terminal.

## O que fazer

- Adotar o steering de entrega de correio em turnos ativos (`#37918`) no runtime do `brza-studio` para destravar diálogos
  entre coordenador e workers sem latência ociosa.
- Implementar no `brza-studio` a distinção visual entre Coordenadores e workers (`#38000`) e incorporar `--wait-until`
  no `brza-workflow`.
