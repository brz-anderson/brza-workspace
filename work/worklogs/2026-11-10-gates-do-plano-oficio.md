---
scope:
  - workspace
tags:
  - planning
refs:
  - PLN-021
sessions:
  - 01a1c81f-d759-7593-8aca-ce78f6ea32cd
---

# Reunião gates do plano: a participação de Oficio, a voz de quem autoriza

O pedido de Anderson, em 2026-11-10, na sessão da coordenação (`01a1c81f-d759-7593-8aca-ce78f6ea32cd`): "Gates até o plano, corte 00:45 (Recomendado)". Este é o registro de **Oficio** — persona a voz de quem autoriza, no Antigravity sem modelo explícito —, aberto pela coordenação. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

- **Posição:** Gate na tarefa com dono explícito e um clique: lista curta do que é meu e destrava autônoma.

Às 22:33, formulação da tese inicial após conferência do briefing, persona e plano PLN-021.

#### 1. Pendência e dono

- **Posição:** Gate na tarefa com dono explícito da pendência; a fase agrupa a leva e só bloqueia apontando quem destrava.
- **Por quê:** Abro o plano e quero ver em segundos o que é meu e o link do alvo, sem ler tudo. *Lido*: o `phase` do frontmatter é o ciclo macro do plano e não a leva de execução (`.sessions/reuniao-gates/briefing.md:16`). *Lido*: hoje o `ready` é texto livre e não estrutura quem destrava (`PLN-021-plan.md:7`). *Lido*: a fase é uma leva sem dependência interna e pode bloquear ou ser bloqueada (`.sessions/reuniao-gates/briefing.md:22`). *Suposto*: fase travada sem indicar dono da pendência vira gargalo invisível e paralisa tarefas que já rodariam sozinhas.
- **Ideias:** campo `pending_on: @anderson | @agente` na tarefa com link direto do alvo para ação em 1 clique `(ousadia: média)`; metadado de fase `unblocked_by: [T1, T2]` vinculando o desbloqueio a tarefas específicas e seus donos `(ousadia: baixa)`.
- **Risco:** Reduzir demais a estrutura de dependências entre fases para tentar simplificar a lista, mascarando bloqueios técnicos reais.
- **Confiança:** 92/100

#### 2. Unidade de autorização

- **Posição:** A autorização deve ser por tarefa (entrega com valor real), nunca por passo interno ou por checkbox.
- **Por quê:** Autorizar passo a passo causa fadiga de decisão e paralisa o fluxo; autorizar o plano inteiro é cheque em branco. *Lido*: a norma hoje exige pedido explícito a cada passo (`plans/README.md:52`), o que no PLN-021 exige 11 aprovações humanas (`PLN-021-plan.md:370`). *Lido*: checkbox de passo não possui id nem hora (`.sessions/reuniao-gates/briefing.md:21`). *Suposto*: quem autoriza quer validar a entrega da tarefa, deixando o agente rodar seu roteiro interno de passos sem pedir frase nova para commitar.
- **Ideias:** Gate de autorização na Tarefa (`authorized: 22:33 por @anderson`), tornando os passos internos roteiro operacional do agente `(ousadia: baixa)`; bloco de evidência e horas consolidado na Tarefa, dispensando carimbo individual por checkbox `(ousadia: média)`.
- **Risco:** Se uma tarefa for ampla demais e quebrar no meio, o agente precisará de mecanismo para retomar sem reautorizar tudo do início.
- **Confiança:** 94/100

#### 3. Quem executa

- **Posição:** O texto do plano declara apenas o papel e o agente sugerido; sessão, runtime, modelo e esforço ficam no `execucao.json`.
- **Por quê:** Quem autoriza quer saber o papel responsável pela entrega, sem se afogar em parâmetros voláteis de runtime no Markdown. *Lido*: o plano hoje registra apenas `executor: implementer, pela coordenação` (`PLN-021-plan.md:372`). *Lido*: sessão, runtime, modelo e esforço já nascem no `executor.py open` e moram no `execucao.json` (`.sessions/reuniao-gates/briefing.md:20`). *Suposto*: chumbar runtime e modelo no Markdown quebra a estabilidade do plano se houver fallback de cota ou retry em outro modelo.
- **Ideias:** Manter no plano apenas a linha `executor: <papel>` `(ousadia: baixa)`; campo opcional `runtime_profile: balanced|fast|deep` no plano, delegando a resolução do modelo para o orquestrador/manifesto `(ousadia: média)`.
- **Risco:** Dificultar a conferência visual direta caso quem autoriza queira auditar o modelo exato sem abrir o manifesto JSON.
- **Confiança:** 91/100

#### A ideia mais ousada desta rodada

A linha `Retomar` trazer a "Fila de 1 Clique": três links diretos — "Sua pendência agora", "Pode rodar sozinho" e "Bloqueado por terceiros" —, permitindo autorizar uma tarefa inteira com um clique no alvo. Risco: requerer sincronização contínua e rígida do cabeçalho do plano pelo `plan-runner`.

#### Issues candidatas

- **Filtro de pendências no plan-runner** — listar apenas tarefas onde `pending_on: @anderson` para focar a tomada de decisão — prioridade `high`
- **Contrato de autorização por Tarefa no `plan_md.py`** — migrar a granularidade de aprovação de passo para tarefa — prioridade `high`
- **Sincronização de executores no `execucao.json`** — manter o plano limpo delegando metadados de runtime/sessão ao manifesto — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Pendência e dono | Gate na tarefa com dono explícito da pendência; fase só bloqueia apontando quem destrava | 92 |
| 2. Unidade de autorização | Autorização na tarefa (entrega com valor real), nunca por passo interno ou por checkbox | 94 |
| 3. Quem executa | Papel e agente no plano; sessão, runtime, modelo e esforço no execucao.json | 91 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

- **Posição:** Fico com gate e autorização na tarefa; no plano vai a política, execução fica no manifesto.

Às 22:41, registro do debate e votos após síntese da coordenação.

#### As disputas

- **D1** (onde mora o gate): voto `D1a` (tarefa) — mantém — O gate na tarefa dá visibilidade direta de quem destrava; por M1, a ordem da fase engana o grafo e o bloco `corte:` esconde qual tarefa específica paralisa o fluxo. — 95/100
- **D2** (o que Anderson autoriza): voto `D2a` (a tarefa) — mantém — Autorizar por entrega dá 1 clique por valor tangível; o corte em bloco (D2b) é cheque em branco e ignora restrições fora do workspace (M2). — 95/100
- **D3** (o que o plano guarda de quem executa): voto `D3a` (papel e política, fato no manifesto) — ajusta — Concedo que o plano deve registrar a política/perfil da tarefa, mas modelo, runtime e sessão efetivos ficam no manifesto para não mentir em fallback de cota. — 92/100

#### Os ataques

- **Centelha** (D1b/D2b — corte único na fase): Autorizar a fase inteira em bloco é perigoso quando há tarefas de impactos díspares (como edições externas sob a regra M2); quem autoriza quer destravar o que é seguro sem engolir riscos no mesmo pacote. Derrubaria o ataque: se toda fase fosse garantidamente homogênea e sem risco diferencial entre tarefas.
- **Lamina** (D3b — modelo e esforço no plano): Cravar modelo e esforço no Markdown gera desvio assim que a cota estourar e houver fallback (como medido: Claude já em 46); quem autoriza não quer retrabalho de editar texto por variação operacional de runtime. Derrubaria o ataque: se o orquestrador reescrevesse o plano atomicamente a cada fallback sem intervenção humana.

#### A concessão

O dado **M1** (trazido por Calibre): a ordem em prosa não gera dependência no parser (`P10 depends: []`). Concedi que dependências não podem ficar na fala da fase e precisam ser declaradas na tarefa (`depends_on:`), e ajustei D3 para admitir um perfil/política na tarefa, separando intenção do fato executado.

#### "Sim, e…"

Sobre a linha compacta de gate de **Lamina** (`Pendente:` / `Pronto:`): a linha sob o heading da tarefa vira a "Linha de Decisão em 1 Clique" (`Pendente: de @anderson [Link] | Pronto: autônomo por @agente`), servindo de gatilho para o `plan-runner` montar automaticamente o sumário do `Retomar` `(ousadia: média)`.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Pendência e dono | D1a: gate na tarefa com dependência explícita | 92 | 95 | não | M1 (Calibre) |
| 2. Unidade de autorização | D2a: autorização na tarefa, 1 clique por entrega | 94 | 95 | não | M2 (Anderson) contra cheque em branco |
| 3. Quem executa | D3a: papel e política na tarefa, execução no manifesto | 91 | 92 | ajustou | Calibre e Turno (separação política/manifesto) |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

- **Posição:** Apoio P1: gate na tarefa dá 1 clique por entrega sem travar a leva; contra P2 em bloco.
- **Fatos lidos:** M1, M2 e M3 (confirmado que o papel já define modelo default, tornando redundante cravar modelo no plano).

Às 22:44, votação final após conferência da síntese 2 e alinhamento com as regras do workspace.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | Nenhuma; preserva autonomia das tarefas e agilidade de 1 clique por entrega | 96 |
| P2 | contra | Agrupa o gate na fase, tirando granularidade da pendência e travando tarefas independentes | 88 |

#### O que me faria mudar de ideia

- **P1:** Se um teste de carga demonstrasse que a linha de gate em cada tarefa gera mais atrito de leitura do que abrir uma seção inteira de fase.
- **P2:** Se ficasse comprovado que todas as tarefas de uma fase sempre possuem o mesmo dono, o mesmo risco e começam no mesmo instante.

#### A última ideia

Ação Rápida no `Retomar`: o topo do plano compilar automaticamente as tarefas com `Pendente: de @anderson` em links diretos `[Autorizar T1]`, `[Autorizar T2]`. Anderson responde apenas o ID ou clica no alvo, e o `plan-runner` inicia a tarefa sem exigir leitura dos checkboxes operacionais internos `(ousadia: média)`.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Calibre | Revelou M1 (ordem em prosa não é dependência) e o rigor na separação de política e execução | 9.5 |
| Lamina | Trouxe M3 (modelo no papel) e sintetizou a linha compacta de gate `Pendente:` / `Pronto:` | 9.0 |
| Esquadro | Garantiu a defesa de vocabulário fechado e campos checáveis sem quebrar o parser | 8.5 |
| Turno | Destacou que a abertura efetiva pertence ao manifesto por tentativa, aliviando o Markdown | 8.0 |
| Centelha | Pressionou pelo menor número de cliques e autorização por lote, embora alocado na fase | 7.5 |

#### Autoavaliação

Fiel em: lutar contra a fadiga de autorização (1 clique por entrega), repudiar micro-gates em checkbox e manter o plano livre de parâmetros voláteis de runtime.
Saí em: concordar em manter estrutura de política na tarefa além do papel simples, cedendo ao argumento de validação de Calibre e Turno.

<!-- fim-rodada-3 -->

## Custo da tarefa

Não medida — sessão sem turno medido · até 23:37 de 2026-11-10, pelo `brza note commit` · sem o turno do commit
