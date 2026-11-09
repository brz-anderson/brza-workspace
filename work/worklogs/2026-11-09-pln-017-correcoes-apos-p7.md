---
scope:
  - workspace
tags:
  - tooling
refs:
  - PLN-017
  - REV-023
  - issue:custo-e-tokens-do-grok-nas-medicoes-da-reuniao
  - issue:estado-do-worker-e-eventos-no-brza-sessions
  - issue:promocao-da-meeting-runner-apos-duas-reunioes-sem-desvio
---

# PLN-017: correções após P7 e rodada de voto informado

Anderson pediu "siga o plano", após confirmar P7 executado com 19 desvios. A execução das correções da skill e integração com CLI v2 segue no Dispatch `ctx_5877fe248b98`, por Claude com `skill-creator@claude-plugins-official` carregada. A coordenação conserva o registro no [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md); P8 concluído após a entrega e a reverificação independente.

## R8 — X10

Anderson escolheu literalmente: "Executar rodada extra automaticamente. Custo: cerca de 3–5 min quando o gatilho ocorrer, com a coordenação prolongando a reunião sem perguntar. Se paga: quando eu estiver indisponível e o voto precisar considerar o fato novo."

A pergunta e as três opções estão no plano. Gatilho: fato novo da própria rodada de voto que contradiz a premissa de algum voto. A coordenação compartilha a síntese antes do voto informado extra; sem gatilho, nenhuma rodada adicional. A escolha não transfere a decisão final de Anderson. Duração estimada em 3–5 min; custo financeiro não medido. Resposta enviada à execução em `msg_23b96f508744`; a executora informou aplicação em SKILL.md, tipo 5 e closing, com avaliação de gatilho e ausência. Isso ainda não é aceite da implementação: faltam testes e revisão independente.

## R9 — participantes da rodada extra

Anderson respondeu literalmente em 2026-11-09, sessão `Retomar PLN-017`: "A coordenação escolhe e registra o motivo. Custo: um julgamento sobre participantes em cada gatilho, além da rodada. Se paga: quando o alcance do fato varia entre reuniões."

R9 registra as três opções e a resposta; D1 atualizado. A coordenação seleciona participantes caso a caso e registra o motivo antes do disparo, sem exigir subconjunto nem sala inteira. R8 conserva a extensão automática pelo gatilho; a decisão final continua com Anderson. Resposta transmitida em `msg_067ef1a3938d`, com pedido de atualização da skill, tipo 5 e avaliação de seleção justificada. Testes e revisão da implementação continuam pendentes.

## Correção factual da medição do Grok

A executora informou a fonte de custo/tokens do Grok. A coordenação leu o `usage.json` da sessão `01a1c119-2faf-71f0-9d21-dfd87c062873` e conferiu campos e soma dos quatro turnos: 2.632.760 tokens de entrada, 24.264 de saída e 18.738.880.000 `costUsdTicks`. F19/F20 do Desenho e F29 de D2 corrigidos; o contrato implementado continua `unmeasured`. A [O custo e os tokens do Grok entram nas medições da reunião](../issues/custo-e-tokens-do-grok-nas-medicoes-da-reuniao.md) guarda a integração, com escala e agregação de subagentes a validar. Antigravity não foi reconferido. A execução foi orientada em `msg_a65fac353818` a manter o escopo atual.

## Fora do workspace

- **O quê e onde:** especificação no scratch desta coordenação, `pln-017-correcoes-skill-spec.md`, e Dispatch no estado do Studio. **Risco:** ocupação de disco e custo da execução. **Estado:** execução em andamento; especificação preservada como evidência. **Como desfazer:** encerrar a sessão pelo protocolo do orquestrador quando terminar e remover o arquivo após preservar a entrega.

## Entrega, revisão e P8

Publicados `d12ed91` e `db619ac`: 300 testes, regressões vermelhas antes e revisão final independente em duas passadas. A [REV-023: A revisão final da meeting-runner v2 e os limites antes da promoção](../reviews/REV-023-pln-017-meeting-runner-v2-final.md) guarda os achados A1-A4, correções/documentação e resíduos. O worklog executor registra 26 min de agente (~0,433 h) e US$ 37,41, dos quais US$ 21,61 de subagentes; avaliações têm vazamento da linha de base e não provam ganho causal.

P8 fecha a issue de origem e registra a pendência [A meeting-runner chega ao core depois de duas reuniões sem desvio](../issues/promocao-da-meeting-runner-apos-duas-reunioes-sem-desvio.md). Estado do worker e datas dos eventos no CLI têm destino em [O brza sessions distingue o estado do worker do estado do Dispatch](../issues/estado-do-worker-e-eventos-no-brza-sessions.md). O defeito foi reproduzido pela principal com a função real e a fixture do runtime: `dispatch.status=completed`, `worker.state=succeeded`, retorno `completed`. Nenhuma correção no CLI foi alegada.

O protótipo permanece no playground; zero reuniões sem desvio e nenhuma reunião completa pelos verbos v2. P7 permanece concluído como verificação com 19 desvios. Registro final de P8 estimado em ~0,1 h, sem medição; subtotal aproximado do plano 9,516 h, restante zero. O fechamento não autoriza promoção nem inventa aceite dos resíduos.

Especificação e relatórios da conferência final permanecem nos scratches identificados nas chamadas de coordenação; só leitura e artefatos temporários de teste, sem nova alteração de configuração externa.
