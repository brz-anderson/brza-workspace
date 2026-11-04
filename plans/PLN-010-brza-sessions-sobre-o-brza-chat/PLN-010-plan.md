---
status: open
phase: interview
origin: issue
origin_ref: brza-sessions-sobre-o-brza-chat
description: O brza sessions passa a ser alias do brza chat do Studio, com leitura por cursor, recibo fiel do envio, retry seguro e a origem do coordenador preservada
ready: "não — faltam a Rodada 2 e o contrato do brza chat do PLN-011, no studio; isso trava o Desenho"
scope:
  - brza-workflow
opened: 2026-11-03
owner: Anderson
priority: high
tags:
  - chat
  - tooling
---

# PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel

- **Retomar:** R1 respondida em 2026-11-03: quatro fases, os três chamadores do `send_to_chat`, o cursor com quem
  chama e a falha sem o `brza chat`. Próximo: a Rodada 2 — o código de saída do recibo, o retry e o cursor inválido. Falta o
  `depends_on: [PLN-011]`, que o checador recusa até o `studio` commitar o plano reservado.

## Pedido

- **Origem:** [O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../work/issues/brza-sessions-sobre-o-brza-chat.md),
  frente do `brza-workflow` da issue
  [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md),
  do workstream `playground`, pelo pedido da sessão "Plano: chat via CLI e plugins" de 2026-11-03.

"os aliases de `brza sessions` sobre o `brza chat` do Studio, a leitura por cursor, o recibo fiel do envio (hoje o
`sent: true` de `brza-sessions:283-287` e o resultado descartado em `brza_runtime.py:141-145`), o retry seguro sem
prometer resolver `unknown`, e a origem do coordenador preservada (`orchestrationCompatibilityEvidence`)." — o pedido de
abertura, de 2026-11-03.

1. Os aliases de `brza sessions` sobre o `brza chat` do Studio.
2. A leitura incremental por cursor, com tratamento de cursor inválido.
3. O recibo fiel do envio, preservando o `queue-if-active` e expondo a fila, também quando uma pergunta pendente a
   retém.
4. O retry seguro, sem prometer resolver o `unknown`.
5. A origem do coordenador preservada (`orchestrationCompatibilityEvidence`).

### Fases

Por prioridade, pela R0.5 e pela R1.1; cada fase depois da coordenação tem issue própria e espera a frente
correspondente do `PLN-011`.

| Fase | Prioridade | O que entrega                                                  | Issue |
| :--- | :--------- | :------------------------------------------------------------- | :---- |
| 1    | `high`     | A coordenação: `list/read/send`, o recibo, o retry e a origem  | [O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../work/issues/brza-sessions-sobre-o-brza-chat.md) |
| 2    | `medium`   | `brza sessions focus <nome>` sobre o `brza chat focus`         | [O `brza sessions focus` traz à frente o chat pelo nome](../../work/issues/brza-sessions-focus-sobre-o-brza-chat-focus.md) |
| 3    | `low`      | Os plugins do workflow veem o Native Chat no `agents.list`     | [Os plugins do workflow veem o Native Chat no `agents.list`](../../work/issues/os-plugins-do-workflow-veem-o-native-chat.md) |
| 4    | `low`      | O `brza quota` lê o `account usage` do app                     | [O `brza quota` lê o uso por conta pelo `account usage` do app](../../work/issues/o-brza-quota-le-o-account-usage-do-app.md) |

### Cobertura

Rascunho da abertura; o critério de aceite de cada linha é proposta até a rodada que o confirma.

| Origem     | Critério de aceite                                                                                                     | Passo | Teste (nível)                         |
| :--------- | :--------------------------------------------------------------------------------------------------------------------- | :---- | :------------------------------------ |
| `Pedido 1` | `brza sessions list/read/send <nome>` resolve o nome pelo mapa e chama o `brza chat` do Studio com o id do chat         | —     | `test_brza_sessions` (unidade)        |
| `Pedido 2` | `read` devolve só o que veio depois do cursor e o cursor seguinte; cursor inválido sai com erro próprio, sem reler tudo | —     | `test_brza_sessions` (unidade)        |
| `Pedido 3` | `send` imprime o recibo que o Studio devolveu — enfileirada ou submetida, com `accepted`, `rejected`, `pending` ou `unknown` —, nunca `sent: true` por conta própria | — | `test_brza_sessions` (unidade); envio a chat ocupado (manual) |
| `Pedido 4` | repetir o envio com a mesma operação não dispara de novo, e o `unknown` sai como `unknown`                            | —     | `test_brza_sessions` (unidade)        |
| `Pedido 5` | o envio feito de dentro de um chat chega ao destino como tarefa do coordenador, não como a mensagem da pessoa          | —     | `test_brza_sessions` (unidade); conferência no app (manual) |
| `R1.2`     | o `open` com `--rename` e `--prompt` e o `brza-run` mostram o recibo do envio, pelo mesmo transporte do `send`          | —     | `test_brza_sessions`, `test_brza_run` (unidade) |
| `R1.3`     | `read <nome> --since <cursor>` devolve o cursor seguinte; sem `--since`, as últimas N; nada de cursor guardado no mapa | —     | `test_brza_sessions` (unidade)        |
| `R1.4`     | sem o `brza chat` no app alvo, os comandos saem com erro que pede o build com ele, sem cair no `rpc` antigo            | —     | `test_brza_sessions` (unidade)        |
| `R1.1`     | `brza sessions focus <nome>` traz o chat à frente pelo `brza chat focus`                                               | —     | `test_brza_sessions` (unidade); conferência no app (manual) |
| `R1.1`     | os plugins do workflow enxergam o Native Chat no `agents.list`                                                         | —     | a definir no Desenho da fase 3        |
| `R1.1`     | o `brza quota` lê o uso por conta pelo `account usage` do app                                                          | —     | a definir no Desenho da fase 4        |

### Fora de escopo

- **O `brza chat list/read/send` no `brza-studio`**, o contrato dele e o porte do `#37774`. Do `PLN-011`, no workstream
  `studio`.
- **A navegação (`focus`, barra lateral, Jump Palette), o journal do `#37802`, os plugins e o `account usage`
  (`#37467`)** no `brza-studio`. Do mesmo `PLN-011`, por prioridade; o lado do `brza-workflow` de três delas são as
  fases 2 a 4, pela R1.1.
- **A barra lateral, a Jump Palette e o journal do `#37802`.** Não têm lado no `brza-workflow`; ficam só no `PLN-011`.

## Pré-requisitos

- **O `brza chat` do Studio, com a forma que o `PLN-011` decidir.** Assinatura a conferir no build:
  `brza chat list --json`, `brza chat read <chat> --since <cursor> --json` com o cursor seguinte na saída, e
  `brza chat send <chat> <texto> --json` com o recibo do `AgentSessionSendResult` e a operação que se repete. Falta:
  o Desenho daqui para nos itens que dependem dele, e o `ready` fica `não`.
- **O envio leva a origem do coordenador.** O `brza chat send` aceita o chat de origem (o `ORCA_AGENT_SESSION_ID`), ou o
  item do Pedido 5 fica no `rpc` do `brza_runtime`. É ponto a pedir ao `PLN-011`, não decisão daqui.

## Entrevista

### Rodada 0 — o que o `playground` já decidiu (respondida em 2026-11-03)

Respondida na sessão "Plano: chat via CLI e plugins" do `playground`, e transcrita do pedido de abertura e da
[issue de origem](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md), sem
perguntar de novo. As opções que perderam estão lá.

1. **Foco.** **Decidido:** "Coordenação entre sessões (Recomendado)".
2. **Acompanhamento.** **Decidido:** leitura incremental por cursor, com tratamento de cursor inválido.
3. **Envio durante atividade.** **Decidido:** preservar `queue-if-active` e expor que a mensagem está enfileirada,
   inclusive quando uma pergunta pendente retém a fila.
4. **Workstreams.** **Decidido:** "studio + tools-kit (Recomendado)" — um `PLN` no `studio`, o `brza chat` no
   `brza-studio`, e este no `tools-kit`, com `depends_on` no do `studio`, o `PLN-011`.
5. **Fases.** **Decidido:** "Todas as frentes, por prioridade (Recomendado)".
6. **Prioridades.** **Decidido:** "Proposta abaixo (Recomendado)" — a coordenação (`list/read/send`) é `high`.
7. **Issues.** **Decidido:** "No workstream da frente (Recomendado)" — a sessão que abre o plano cria as issues dele.

### Rodada 1 — as fases, os chamadores, o cursor e o app sem `brza chat` (enviada 2026-11-03)

> **Apresentado antes:** o `send_to_chat` tem três chamadores — o `brza sessions send` (`brza-sessions:285`), o prompt
> depois do `--rename` no `open` (`:408`) e o `brza-run` (`packages/client/bin/brza-run:114`) —, e os três descartam o
> resultado. O `brza sessions` mira o Studio por padrão (`bin/brza_runtime.py:26`); o Orca só tem o `brza chat` se o
> upstream integrar o `#33115`. O cursor, a forma do recibo e a operação reusável são do contrato do `PLN-011`, fora
> da rodada. Tudo no `brza-workflow@7a18392`.

Respondida em 2026-11-03, nesta sessão, pela pergunta com opções.

1. **Fases além da coordenação**, seleção múltipla:
   - alias `focus` (recomendada) — fase `medium`, `brza sessions focus <nome>` sobre o `brza chat focus`; custo: ~1 h
     e um teste, depois do focus do Studio; se paga: na primeira vez que o coordenador trouxer à frente um chat pelo
     nome;
   - Native Chat nos plugins — fase `low`, os plugins do `PLN-003` leem os chats no `agents.list`; custo: ~2–4 h,
     depois da frente de plugins do `PLN-011`; se paga: quando um plugin precisar ver os chats;
   - account usage no MCP — fase `low`, o MCP do `PLN-009` lê o `#37467`; custo: ~2 h, depois da integração no
     upstream; se paga: quando o MCP trocar a fonte da cota;
   - só a coordenação — custo: nenhum agora; se paga: agora, com o plano fechando mais cedo.

   **Decidido — as três**: alias `focus`, Native Chat nos plugins e account usage no MCP, em fases 2 a 4, cada uma com
   issue própria (R0.7).

2. **Chamadores do recibo:**
   - os três (recomendada) — custo: ~1–2 h a mais nos testes do `open` e do `brza-run`; se paga: agora, com um
     transporte só e o `brza-run` deixando de anunciar o que não conferiu;
   - só o `send` — custo: dois transportes, e o `open` e o `brza-run` sem recibo; se paga: nunca para os outros dois.

   **Decidido — os três (Recomendado).**

3. **Onde fica o cursor:**
   - com quem chama (recomendada) — `read <nome> --since <cursor>` devolve o seguinte; sem `--since`, as últimas N;
     custo: o coordenador guarda o cursor e recomeça pelas últimas N depois de uma compactação; se paga: agora, sem
     estado compartilhado entre coordenadores;
   - no mapa de sessões — custo: ~2–3 h, chave por leitor e limpeza; se paga: quando a compactação fizer perder o
     cursor com frequência;
   - os dois — custo: ~3 h e dois jeitos de ler; se paga: só se as duas situações acontecerem.

   **Decidido — com quem chama (Recomendado).**

4. **O app sem o `brza chat`:**
   - falha com aviso (recomendada) — erro que pede o build com o `brza chat`, sem reserva; custo: o `send` para num
     Studio antigo até a atualização; se paga: agora, porque o Studio é compilado aqui e é o padrão;
   - reserva pelo `rpc` de hoje — custo: ~3 h, dois transportes e testes em dobro; se paga: se o Orca precisar do
     `brza sessions` antes do `#33115`.

   **Decidido — falha com aviso (Recomendado).**

## Pendências conhecidas

As fases 2 a 4, abertas na R1.1, cada uma esperando a frente correspondente do `PLN-011`:

- [O `brza sessions focus` traz à frente o chat pelo nome](../../work/issues/brza-sessions-focus-sobre-o-brza-chat-focus.md) — fase 2, `medium`.
- [Os plugins do workflow veem o Native Chat no `agents.list`](../../work/issues/os-plugins-do-workflow-veem-o-native-chat.md) — fase 3, `low`.
- [O `brza quota` lê o uso por conta pelo `account usage` do app](../../work/issues/o-brza-quota-le-o-account-usage-do-app.md) — fase 4, `low`.

## Worklogs

- 2026-11-03 — abertura: a issue da frente, o `PLN-010` e a R0 transcrita; R1 respondida, com as issues das fases 2
  a 4. Parou na Rodada 2.
  [O PLN-010: a abertura do `brza sessions` sobre o `brza chat`](../../work/worklogs/2026-11-03-pln-010-abertura-do-brza-sessions-sobre-o-brza-chat.md)
