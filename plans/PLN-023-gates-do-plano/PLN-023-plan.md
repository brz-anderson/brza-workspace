---
status: done
phase: closed
origin: decision
origin_ref: o-plano-novo-do-playground-mostra-a-pendencia-na-tarefa
description: O plano novo deste workstream nasce com a pendência e o dono na tarefa, e com sessão, runtime, modelo e esforço na tabela do open.
ready: sim
estimate_h: 1
executed_h: 1
remaining_h: 0
priority: medium
scope:
  - workspace
opened: 2026-11-10
completed: 2026-11-10
owner: Anderson
tags:
  - planning
---

# PLN-023: O plano novo do playground mostra a pendência, o dono e quem pode executar

- **Retomar:** Fechado em 2026-11-10. O desenho está em D1 e D2. Nada a executar daqui.

## Pedido

- **Origem:** pedido de Anderson na sessão Grok `01a1c81f-d759-7593-8aca-ce78f6ea32cd`, em 2026-11-10, e a palavra "gravar" na rodada em que a proposta v3 estava inteira na mensagem. A decisão está em [O plano novo do playground mostra a pendência na tarefa][decisao].

"gravar" — a opção 1: gravar o plano neste workstream, sem código e sem outro repositório.

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Pedido 1 | O arquivo deste plano traz a fase, a pendência, o dono e o papel no texto, e aponta sessão, runtime, modelo e esforço para a tabela do `open` | P1 | Leitura do arquivo (manual) |

### Fora de escopo

- **O código do `plan_md.py`, do checador e do `move_note.py`.** Fica para um pedido explícito. O parser de hoje não lê `Espera:`, `Autorizado:`, `Pendente:` nem `Pronto:`.
- **A norma comum em `plans/README.md`.** O arquivo está no `.brza/core.lock` e se edita no `core/` do `brza-workflow`.
- **Reescrita de plano já aberto,** inclusive o PLN-021.
- **O corte na fase como gate.** Recusado na mesma decisão. A pendência fica na tarefa.

## Restrições

- **Este workstream.** Alteração em outro workstream, no `brza-studio`, no `brza-workflow` ou na `master` não é passo deste plano.

## Entrevista

### Rodada 1 — link, fase e unidade (enviada 2026-11-10)

Respondida em 2026-11-10.

1. **Como o id vira link.** Opções:
   - definição por arquivo, rótulo igual ao H1 (recomendada) — custo: o checador passa a ler a definição; se paga: na nota que repete o mesmo id;
   - o id é o texto visível — custo: a regra do H1 muda; se paga: se o clique for pelo id;
   - só link inline — custo: o caminho se repete; se paga: agora, se a meta for só não deixar o id solto.

   **Decidido — definição por arquivo, rótulo igual ao H1.** Link externo continua inline.

2. **O que a fase obriga.** Opções:
   - leva, sem dependência interna (recomendada) — custo: o parser confere; se paga: no plano com tarefas paralelas;
   - barreira, a leva seguinte espera — custo: a tarefa que só depende de uma anterior espera o resto; se paga: se o lote fechado valer a espera;
   - só título — custo: zero no parser; se paga: nunca como estrutura.

   **Resposta:** "opção 1 + uma fase pode ser bloqueante ou bloqueada por".

3. **Quem Anderson autoriza.** As três opções foram para a sala, no sentido do gate. A resposta não escolheu uma letra.

### Rodada 2 — o gate da reunião (enviada 2026-11-10)

Respondida em 2026-11-10.

1. **Confirma o objeto, o fora, a saída e o corte às 00:45.** Opções:
   - gates até o plano, corte 00:45 (recomendada) — custo: a sala não reabre link nem leva; se paga: nas rodadas desta janela;
   - só a proposta nesta janela — custo: o arquivo não nasce hoje; se paga: se a proposta íntegra valer mais;
   - a sala pode reabrir link e fase — custo: uma rodada a mais; se paga: só se o que já foi escolhido voltar à mesa.

   **Decidido — a recomendada.**

### Rodada 3 — gravar a v3 (enviada 2026-11-10)

**Apresentado antes:** a proposta v3 inteira, com confiança do revisor 88, média da sala 79 (5/6) e o Oficio à parte em 92.

Respondida em 2026-11-10.

1. **Fecho a v3 e gravo o plano neste workstream?** Opções:
   - gravar o plano aqui (recomendada) — custo: um plano e o worklog, sem código e sem outro repositório; se paga: quando o próximo plano daqui nascer neste formato;
   - guardar a v3 e não gravar o plano hoje — custo: o texto fica fora do git até o worklog; se paga: se uma linha for mudar antes do arquivo;
   - não fechar — custo: outra rodada; se paga: só se uma linha da v3 estiver errada.

   **Decidido — gravar.** A palavra foi "gravar".

## Desenho

### O que este desenho assume

- **R1.1:** o link interno é definição no arquivo, com o H1 no rótulo.
- **R1.2:** a fase agrupa tarefas sem dependência entre si e pode bloquear ou ser bloqueada, nomeando quem destrava.
- **R3.1:** o gate fica na tarefa, não num corte da fase. Autorizar não apaga a pendência.

### D1 — As linhas do gate — `plans/PLN-023-gates-do-plano/PLN-023-plan.md` (P1)

- **Origem:** R3.1
- **Contexto:** o parser não lê a seta de ordem. No PLN-021, `PLN-021-plan.md:392-393` diz `P9 → P10` e o `plan_md.load` devolve `P10 depends []`.

#### Como fica

`## Passos` continua. A fase é uma linha em negrito, não um heading. A tarefa continua `### Pn —`, com travessão.

```markdown
## Passos

**F1 — O executor.** Espera: F0 · de: Anderson

### P3 — O executor em uma transação
Executa D1 · executor: implementer

Autorizado: pedido de Anderson 2026-11-10 22:40, P3 P5, plano @abc1234
Pendente: F0 aberta · de: Anderson
```

`Pronto:` substitui o par quando não há pendência. A versão é a lista de ids mais o commit do plano. `executor:` só tem o papel. Sessão, runtime, modelo e esforço aparecem na tabela do `open` (`executor.py:418-420`) e em `.sessions/pln-nnn/execucao.json`. No `open` padrão, runtime `claude` e modelo `claude-sonnet-5-5`.

### D2 — O link por referência — notas e planos deste workstream (P1)

- **Origem:** R1.1
- **Contexto:** o checador e o `move_note.py` só reescrevem o link inline. A definição fica no fim do arquivo que cita.

#### Como fica

```markdown
Veja [O plano novo do playground mostra a pendência na tarefa][decisao].

[decisao]: ../../work/decisions/o-plano-novo-do-playground-mostra-a-pendencia-na-tarefa.md
```

O rótulo visível no corpo pode ser o H1. A chave é o id, ou um nome curto que aponta para a definição. Link de fora do repositório continua inline.

## Passos

**F0 — O registro.** Sem espera.

### P1 — O desenho gravado neste arquivo

Executa D1, D2 · executor: coordenação

Estimado: 1 h · Executado: 1 h

- [x] **1. Gravar a decisão e este plano no workstream playground**
- [x] **2. Não editar norma comum, código nem outro repositório**

**Evidência:** este arquivo e [O plano novo do playground mostra a pendência na tarefa][decisao]. O `check_notes.py` corre no fechamento da gravação.

Pronto: pedido de Anderson 2026-11-10, a palavra gravar, P1

## Worklogs

- 2026-11-10 — R1 a R3 fechadas; D1 e D2 gravados; P1 feito. Nada travou neste arquivo.
  [Reunião gates do plano: a coordenação](../../work/worklogs/2026-11-10-gates-do-plano-coordenacao.md)

## Decisões

- [O plano novo do playground mostra a pendência na tarefa][decisao] — R3.1, `done`.

[decisao]: ../../work/decisions/o-plano-novo-do-playground-mostra-a-pendencia-na-tarefa.md
