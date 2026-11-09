---
scope:
  - workspace
  - brza-workflow
tags:
  - tooling
refs:
  - PLN-012
  - PLN-017
---

# PLN-017: coordenação de P4, P5 e P6 e encerramento de workers

Anderson pediu: "coordene a execução do P4, P5 e P6". Duas sessões supervisionadas pelo Run `run_2287f933d683`: P4a/P4b/P6 no `tools-kit`, Dispatch `ctx_f0b0d3dbd714`; P5 na `master` do workspace, Dispatch `ctx_3a1b0058cb10`. O [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md) guarda a rodada R7 e o estado dos passos.

## Execução

P5 concluído: código `brza-workspace@b24de7c`, publicado; 99 testes verdes após vermelho reproduzido, revisão independente e A1 corrigido. O [PLN-017/P5: o brza shot lê visualBaseCss e mantém o literal antigo](../../../workspace/work/worklogs/2026-11-09-pln-017-p5-brza-shot.md) traz evidências e limites; notas publicadas em `8f6846f`. Janela total informada: 0,174 h.

P4 reportou a híbrida sem fechamento automático (`autoReleaseAt:null`, `external_terminal`): aplica-se a via pura já aprovada em R6. O host aceita `status`, não `message`; conferido por `send --help`. D2 adaptado ao tipo instalado e à leitura de mailbox sem consumo. P4/P6 foram entregues e revisados; fechamento registrado abaixo.

R7 perguntou como encerrar worker ativo, pois `worker-release --help` só aceita settled. Anderson escolheu pedir encerramento por mailbox, retornar `closing` e usar parada guardada com confirmação no `--force`. Resposta literal e alternativas registradas no plano e enviadas à execução em `msg_bf677cde67b7`. Nenhum fechamento incerto conta como concluído.

## Fechamento de P4a/P4b/P6

Publicados `brza-workflow@3d3d2bb` (P4a) e `db6bd28` (P4b); notas e P6 em `brza-workspace@ff8def8`/`0cbeb26`, branch `workstream/tools-kit`. Ancestralidade conferida nas referências locais de origin. A [REV-022: As primitivas do brza sessions e a exceção transitória do PLN-010](../../../tools-kit/work/reviews/REV-022-pln-017-sessions-e-transicao-rpc.md) encerrou a revisão sem bloqueios, com destinos por achado.

Validação da executora: 100 testes específicos, snapshot P4a com 90; 580 da CLI ampla antes do último teste somente de regressão, sem mudança posterior de produção; hooks 348, MCP 390 e scripts 113 verdes. Sondas reais confirmaram os quatro runtimes em Chat e liberados, replay sem duplicação, modelo, espera por rodada e medição após auto-release. O registro [O `brza sessions` recebe as primitivas da reunião e o PLN-010 registra a transição pelo `rpc`](../../../tools-kit/work/worklogs/2026-11-09-pln-017-sessions-e-excecao-ao-pln-010.md) traz evidências e limites; relatório final no scratch da executora, `pln-017-sonda/entrega-final.md`.

Tempo final informado: 1,109 h medidas de P4a/P4b/P6, excluído o intervalo suspenso por limite de uso; sem rateio inventado entre passos. O marco de 1,007 h do worklog executor antecede fechamento e entrega. Somado ao P5, esta execução soma 1,283 h; o plano soma 8,283 h executadas e 12,75 h restantes de estimativa.

P7/P8 ficam fora da execução pedida. Antes da reunião, conferir integração da skill com Run único, mapa, mailbox sem consumo e payload da rodada. `pending`/saída 75 exige `wait` ou replay da mesma operação e texto, nunca envio novo cego. `measure.py`, PLN-012 e arquivos alheios foram preservados.

## Fora do workspace

- **O quê e onde:** especificações temporárias `/private/tmp/pln-017-p4-p6-spec.md` e `/private/tmp/pln-017-p5-spec.md`. **Risco:** ocupação de disco. **Estado:** permanecem como registro dos pedidos. **Como desfazer:** apagar após encerrar as tarefas.
- **O quê e onde:** Run, Dispatches e mensagens no estado do BrzA Studio. **Risco:** custo das sessões executoras e testes com chats. **Estado:** P4/P5/P6 concluídos, com `worker_done`; os registros permanecem. **Como desfazer:** encerrar workers pelo ciclo de vida do orquestrador após conclusão, preservando o histórico.
