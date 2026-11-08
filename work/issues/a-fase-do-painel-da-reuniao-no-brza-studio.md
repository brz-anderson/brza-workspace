---
status: open
description: Depois do painel da rodada como `::orca-visual`, a fase seguinte no BrzA Studio: a argumentação integral por persona, abrir o chat da persona, o gate de decisão e a atualização ao vivo, lendo o `estado-rN.json`; o `orchestration-crew` não se religa.
scope:
  - brza-studio
opened: 2026-11-08
priority: low
tags:
  - chat
  - tooling
---

# A fase do painel da reunião no BrzA Studio: argumentação por persona, abrir o chat, gate de decisão e atualização ao vivo

Levantado no [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md), passo P3, para o workstream `studio`. A v1 do painel da rodada é um `::orca-visual` gerado pela coordenação, sem código no app ([PLN-017 — Desenho: o painel da rodada (D3)](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-design-painel.md)); esta issue guarda o que a v1 não dá e onde isso encaixa no app, para quando houver três ou mais reuniões e o artboard incomodar. Não é pedido de execução.

## O que a v1 não dá, e a fase do painel daria

| Falta na v1 | Por quê | Na fase do painel |
| :---------- | :------ | :---------------- |
| A argumentação integral por persona | Anderson a tirou do chat da coordenação (PLN-017 R1.4: "argumentação integral fica pra fase do painel"); o frame do visual tem teto de 2000 px (`src/shared/native-chat/native-chat-visual-shell.ts:55-56,304-308`) | seção recolhida por persona, lida do worklog |
| Abrir o chat da persona com um clique | o link do visual só sai para `http`/`https` (`native-chat-visual-shell.ts:145-158`) | `revealDashboardAgent` ou `chat focus` a partir da linha |
| Botão de decisão | `submit` cancelado e sem mensagem de ação no visual (`:158`) | gate (`gate-create`/`gate-resolve`, hoje só na CLI: `src/cli/specs/orchestration-gate-specs.ts:5-27`) com cartão na UI, ou cartão de pergunta |
| Atualização ao vivo | o frame não observa o arquivo; só a mensagem nova o relê (`use-native-chat-visual-document.ts:74-131`) | painel que ouve `agent.status.changed` e lê o estado da reunião |
| Link para a seção do worklog | os worklogs só chegam ao GitHub no commit do fim | abrir o arquivo local no editor do app |

## O contrato que a fase lê

O `estado-rN.json` do gerador da skill `meeting-runner` (PLN-017/D3, "O modelo de dados"): por rodada, as personas com sessão, runtime, modelo, esforço, estado (`respondeu`, `falta`, `atrasado`, `erro`), hora e latência, confiança e delta contra a R1, posição em uma linha, voto, virada, custo ou tokens, e o `arquivo:linha` da seção; mais as medições da coordenação, a síntese e as decisões pendentes. A fase do painel lê o JSON, não o HTML.

## As superfícies candidatas, pelo levantamento de 2026-11-08

- **Plugin de painel na barra direita** (`contributes.panels` com `ui: components`, `statusBarItems`, `agents.list`, `agent.status.changed`; `docs/reference/plugin-manifest.md:33,47,53,201-212`, `plugin-host-api.md:172-178`): um `trusted-worker` lê o `estado-rN.json` e cruza com o estado ao vivo. 12 a 20 h, com a base das estimativas do PLN-011. Liga persona a chat só por título até o P14 do PLN-011 (`sessionId`), que espera o C1 de Anderson.
- **Gate com cartão na UI:** 10 a 20 h; se paga se a reunião rodar sem a coordenação presente.
- **Aba nativa "sala de reunião":** 40 a 70 h; só depois de o plugin provar o uso.

## O `orchestration-crew` não se religa (PLN-017 R3.4, 2026-11-08: "Não religar; reavaliar na fase do painel")

O painel de equipe do Orca (`src/renderer/src/components/orchestration-crew/`, `src/shared/orchestration-crew.ts:6-32`) mostrava, dentro do chat, uma linha por agente com papel, estado, tarefa, última mensagem, pergunta pendente e destino para abrir. Está desligado: `use-orchestration-panel-enabled.ts:1-4` devolve `false` ("Suspended after repeated performance regressions"). O upstream o desligou duas vezes em dois dias (`7872cb5aa17` e `40b660357c4` em 2026-11-02, `20ff1375047` em 2026-11-03, #38045), por amplificação de CPU no `main` (`src/main/runtime/orchestration/crew/`, 3 456 linhas sem testes). A fonte dele é o banco de orquestração (dispatches, runs e mailbox: `crew-parent-inputs.ts:36-60`, `crew-party-snapshot.ts:198-251`): um chat aberto por `brza agent launch --surface chat` sem run não aparece em nenhuma seção. Religar e adaptar custaria de 25 a 60 h, numa pasta que recebeu 20 commits do upstream em quatro dias. Reavaliar só se a reunião virar rotina diária e o plugin demorar mais de dois meses.

## O que trava

- O PLN-011 (`studio`) espera o caso manual C1 de Anderson; sem o P14 dele, o plugin liga persona a chat só por título.
- O PLN-014 (`playground`) trava a emenda e o porte das issues de 2026-11-03 deste workstream (entre elas "painel de atividades de subagentes" e "native chat aos plugins"); esta issue só as cita.
