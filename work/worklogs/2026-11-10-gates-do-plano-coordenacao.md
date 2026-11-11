---
scope:
  - workspace
tags:
  - planning
refs:
  - PLN-014
  - PLN-017
  - PLN-019
  - PLN-020
  - PLN-021
  - PLN-023
sessions:
  - 01a1c81f-d759-7593-8aca-ce78f6ea32cd
---

# Reunião gates do plano: a coordenação

Pedido de Anderson em 2026-11-10, na sessão `01a1c81f-d759-7593-8aca-ce78f6ea32cd`: discutir o gate do plano e, se a decisão fechasse a tempo, gravar o plano. A palavra final foi "gravar".

## Rodadas

| Rodada | Aberta | Fechada | O que produziu |
| :----- | :----- | :------ | :------------- |
| 1, opinião | 22:30 | 22:37 | Cinco personas no gate na tarefa; a Centelha num corte da fase |
| 2, debate | 22:40 | 22:42 | Lamina e Centelha saem de cravar runtime no plano; o corte segue só na Centelha |
| 3, voto | 22:43 | 22:45 | P1 com cinco apoios e um contra; P2 com um apoio |

## Modelos

Nenhum fallback foi usado.

| Persona | Runtime | Modelo | Esforço | Fallback |
| :------ | :------ | :----- | :------ | :------- |
| Calibre | codex | `gpt-6-astra` | `xhigh` | nenhum |
| Esquadro | claude | `claude-sonnet-5-5` | `medium` | nenhum |
| Turno | codex | `gpt-6.1-terra` | `medium` | nenhum |
| Lamina | claude | `claude-opus-5-5` | `high` | nenhum |
| Centelha | grok | `grok-4.7-build-fast` | `low` | nenhum |
| Oficio | antigravity | — | — | nenhum |

## Medição

Fonte: `tally.py` de cada rodada. Grok e Antigravity sem custo de API. Codex em tokens, quando o tally trouxe.

| Persona | Confiança R1 → R3 | Custo visto no painel |
| :------ | :---------------- | :-------------------- |
| Calibre | 85 → 84 | 0,68 M na R1; 0,53 M na R2 |
| Esquadro | 68,7 → 77 | US$ 0,24 na R1; US$ 0,12 na R2; US$ 0,11 na R3 |
| Turno | 73,3 → 80 | 0,24 M na R2; 0,27 M na R3 |
| Lamina | 72,3 → 81 | US$ 0,69 na R1; US$ 0,38 na R2; US$ 0,18 na R3 |
| Centelha | 74,7 → 73 | sem medição |
| Oficio | 92,3 → 92 | sem medição; fora da média |

Sala na R3: média 79 (5/6), mediana 80, faixa 73–84. Revisor da v3: 88. Diferença sala − revisor: −9. Sem contraprova.

## O que se fez

A sala votou o gate na tarefa. O revisor levou a v1 de 64 para a v3 em 88, depois de corrigir vocabulário, o `open` padrão e as linhas citadas. Anderson disse "gravar". Nasceu o [PLN-023: O plano novo do playground mostra a pendência, o dono e quem pode executar](../../plans/PLN-023-gates-do-plano/PLN-023-plan.md) e a decisão [O plano novo do playground mostra a pendência na tarefa](../decisions/o-plano-novo-do-playground-mostra-a-pendencia-na-tarefa.md).

Os registros das personas:

- [Reunião gates do plano: a participação de Calibre, o cético que mede](2026-11-10-gates-do-plano-calibre.md)
- [Reunião gates do plano: a participação de Esquadro, regra e consistência](2026-11-10-gates-do-plano-esquadro.md)
- [Reunião gates do plano: a participação de Turno, especialista em runtimes](2026-11-10-gates-do-plano-turno.md)
- [Reunião gates do plano: a participação de Lamina, narrativa do plano](2026-11-10-gates-do-plano-lamina.md)
- [Reunião gates do plano: a participação de Centelha, a provocadora](2026-11-10-gates-do-plano-centelha.md)
- [Reunião gates do plano: a participação de Oficio, a voz de quem autoriza](2026-11-10-gates-do-plano-oficio.md)

## A proposta final (v3, copiada de `.sessions/reuniao-gates/proposta-v3.md`)

Anderson disse "gravar" em 2026-11-10, com este texto inteiro na mensagem. A cópia abaixo é o arquivo da rodada, inclusive o cabeçalho que ainda dizia "não aprovada".

> Rascunho da coordenação, v3, depois do parecer em `revisor-v2.md` (confiança 73). **Nada aqui está decidido**; as decisões são de Anderson. Marcas: **[medido]** rodou hoje, com a saída; **[lido]** código ou norma; **[inferido]** ninguém testou. Origem: **R3**, **revisor**, ou a coordenação.

### O requisito

Entregar, neste workstream, o desenho do gate do plano: o que está pendente e de quem, e o que pode executar e por quem (sessão, runtime, agente, modelo, esforço).

Não entrega: código do `plan_md.py`, do checador ou do `move_note.py`; reescrita de plano já aberto; edição do `plans/README.md`, que o `.brza/core.lock` segue; qualquer arquivo fora do workstream `playground`.

### O que se mediu

| # | Fato | Marca |
| :- | :--- | :---- |
| M1 | `plan_md.load` de `plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md` devolve `P10 depends []`, `P9 depends ['P6', 'P7', 'P8', 'P11']`, `P7 depends ['P1']`. A prosa em `PLN-021-plan.md:392-393` diz `P9 → P10`, no introito de `## Passos`, fora do corpo de qualquer passo. O parser só lê `depende de` no corpo do passo (`plan_md.py:392-394`). O P10 não tem essa frase. | [medido] o revisor rodou de novo e a saída bateu; [lido] as linhas |
| M2 | Anderson, nesta sessão: "o plano fica contido nesse workstream, qualquer alteração em outro workstream/repositório só sai com pedido meu". | [lido] `.sessions/reuniao-gates/briefing.md:14` |
| M3 | `implementer.md:4` e `collector.md:5` têm `model: sonnet`. `reviewer.md:5` e `designer.md:5` têm `model: opus`. `designer.md:4` é a linha `tools:`. | [lido] frontmatter |
| M4 | `plans/README.md` está no `.brza/core.lock:34`. O que o lock segue se edita no `core/` do `brza-workflow` (`AGENTS.md:67-68`). | [lido] |
| M5 | O passo que o parser aceita casa `^(P\d+[a-z]?)\s*[—–-]\s*(.*)$` (`plan_md.py:30`): `P`, dígitos, uma letra minúscula opcional, travessão obrigatório. `steps()` olha headings de nível 2 a 4 (`plan_md.py:476-478`). `P4a` é passo (`plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md:341`). | [lido] revisor |
| M6 | O manifesto é `.sessions/pln-nnn/execucao.json` (`executor.py:14-15`). O `open` sem `--agent` e sem `--model` grava `agent` `claude` e `model` `claude-sonnet-5-5` (`executor.py:62`, `executor.py:337-339`, `executor.py:412-414`). A célula do painel só imprime `padrão do runtime` quando `model` é falso (`executor.py:420`). Isso ocorre com `--agent grok` ou `antigravity` sem `--model`, e com `codex` sem `--model` e sem `--effort` (`executor.py:293-300`). Não ocorre no `open` padrão. | [lido] revisor, v2 |
| M7 | Um pedido que nomeia dois passos independentes já pode esperar os dois juntos (`conduct.md:95-97`). "Execute o P3" não autoriza o P4 (`conduct.md:30-31`). | [lido] |

### O desenho

`## Passos` continua. A fase não é heading: um heading `## F1` encerraria `## Passos` (`plan_md.py:114`, heading de nível menor ou igual encerra a seção). Origem: revisor, achado 3.

```markdown
## Passos

**F1 — O executor.** Espera: F0 · de: Anderson

### P3 — O executor em uma transação
Executa D1 · executor: implementer
```

`### P3 —` continua passo: letra `P`, dígitos, travessão. `P4a —` também. Origem: revisor, achado 4; M5.

`Espera:` só existe nessa linha da fase. Cita o id da fase que bloqueia e quem destrava. Quem destrava é uma pessoa, não a fase de novo. No exemplo, quem destrava é Anderson.

`Pendente:` só existe na tarefa. Não é a mesma linha com outra capitalização.

Dois exemplos que não cabem na mesma cadeia.

Tarefa autorizada e ainda bloqueada. Não tem `Pronto:`.

```markdown
### P3 — O executor em uma transação
Executa D1 · executor: implementer

Autorizado: pedido de Anderson 2026-11-10 22:40, P3 P5, plano @abc1234
Pendente: F0 aberta · de: Anderson
```

Tarefa que já pode executar. Não tem `Pendente:`.

```markdown
### P5 — O painel no chat
Executa D2 · executor: implementer

Pronto: pedido de Anderson 2026-11-10 22:40, P3 P5, plano @abc1234
```

`Autorizado:` grava o pedido. Pode conviver com `Pendente:`. `Pronto:` só entra quando não há `Pendente:`: o pedido cita esta tarefa e o commit do plano, e cada bloqueio citado já fechou. Autorizar não apaga pendência. A versão é a lista de ids mais o commit do plano. Os dois exemplos citam `P3 P5`. Origem: R3, Calibre e Lamina; revisor, achado 1.

`executor:` no plano só tem o papel: `executor: implementer`. Não tem camada. A camada é o `model:` do arquivo do papel (M3), não uma palavra nessa linha. Origem: revisor, achado 2.

Nesta versão, o corpo da tarefa não recebe sessão, runtime, modelo nem esforço, nem como restrição. Não há token `só claude`. A lista do que entra no corpo, além do papel, está fechada: nada. Restrição de runtime fica para o pedido que migrar a norma.

O manifesto é o arquivo `.sessions/pln-nnn/execucao.json`. Ele guarda `session`, `agent`, `model` e `effort` do `open` (`executor.py:412-414`), não o que o provedor serviu depois. No `open` padrão, sem `--agent` e sem `--model`, isso é sessão com o nome gerado, runtime `claude`, modelo `claude-sonnet-5-5`. A frase `padrão do runtime` só aparece na tabela quando `model` ficou falso, nos casos de M6, não no padrão.

Onde Anderson vê quem executa, fora do corpo da tarefa: a tabela que o `open` imprime, colunas Executor (a sessão), Runtime (o `agent`), Modelo e Esforço (`executor.py:418-420`). O corpo da tarefa só tem o papel. Origem: revisor, achado 2 da v2; M6.

Um pedido pode nomear `P3` e `P5` juntos quando os dois são independentes. Cada tarefa grava a lista. Nomear o P3 não cobre o P4. Tarefa criada depois desse commit, ou trabalho fora do `playground`, não fica coberta. Origem: M7; M2.

O checkbox numerado continua sem hora, sem pedido e sem linha de gate.

O parser de hoje não lê `Espera:`, `Autorizado:`, `Pendente:` nem `Pronto:`. Até um pedido seu de migrar a norma, o plano novo deste workstream nasce com essas linhas, e o `plan_md.py` segue sem vê-las.

### As alternativas

| Alternativa | Atende o requisito? | Custo | Risco | Se paga |
| :---------- | :------------------ | :---- | :---- | :------ |
| P1, acima | Parcial. A pendência e o dono ficam na tarefa. O papel fica na tarefa. Sessão, runtime, modelo e esforço ficam na tabela do `open` e no manifesto, não no corpo. O parser não lê as linhas novas. | A norma comum e o código ficam para um pedido seu. Planos abertos não são reescritos. | Até lá, o gate é prosa. A seta de ordem já é prosa cega (M1). | Quando você autorizar a migração. O plano novo daqui já nasce neste formato. |
| P2, o corte na fase | Parcial. Um pedido lista os ids, e o dono sai da tarefa. | Menos linha por tarefa. | A pendência não fica na tarefa. Uma persona apoiou; cinco votaram contra. | Não, se o requisito é ver a pendência e o dono na tarefa. |

### Fora deste arquivo

- Não se edita `plans/README.md` daqui. M4.
- Não se edita `brza-studio`, `brza-workflow`, outro workstream, nem a `master`, sem pedido explícito.
- Não se reescreve PLN-014, PLN-019, PLN-020 nem PLN-021.

### A confiança do plano

| Quem | Número | Base |
| :--- | -----: | :--- |
| **Revisor independente** | 88 | a confiança do plano. Parecer em `revisor-v3.md`: os quatro defeitos da v2 sumiram e nada novo impede. |
| Sala (média, mediana, n, faixa) | 79, 80, 5/6, 73–84 | `tally.py 3`, janela 22:43:57–22:45:29. Antigravity fora da conta. |
| Antigravity (à parte) | 92 | Oficio. Não entra na média. |
| Diferença sala − revisor | −9 | o revisor ficou 9 acima da média da sala. Abaixo do corte de 10 para contraprova. |

O revisor da v1 deu 64. O da v2 deu 73. Não houve contraprova: a diferença é 9, e gravar o plano neste workstream se desfaz apagando o arquivo.

## Fora do workspace

- **O quê e onde:** seis sessões da reunião ainda abertas no Run `run_b6a7a1404549` — `gates-calibre`, `gates-esquadro`, `gates-turno`, `gates-lamina`, `gates-centelha`, `gates-oficio`.
- **O risco:** seguem contando cota até o host liberar.
- **Estado:** ativas no fim desta gravação. O pedido "gravar" não as fecha.
- **Como desfazer:** `python3 -I .claude/skills/meeting-runner/scripts/launch_persona.py .sessions/reuniao-gates/reuniao.json --close`, e depois `--status --wait-settled 180`.
- **Memória de runtime** (`runtime_memory_check.py 2026-11-10T22:19:00-03:00`): desta sessão, `~/.grok/memory-v2/workspaces/brza-workspace-34595849/topics/plan-notes-and-phases.md` e `topics/reuniao-gates.md`, ambos às 22:50. O mesmo comando listou sonhos de arquivo, sqlite e notas de outras sessões Grok (`topics/pln-021.md`, inbox de `01a1c7c8` e `01a1c83a`). Codex, Claude e Antigravity não apareceram.

## Custo da tarefa

Não medida — sessão sem turno medido · até 23:37 de 2026-11-10, pelo `brza note commit` · sem o turno do commit
