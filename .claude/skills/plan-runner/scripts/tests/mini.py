"""Planos pequenos, feitos à mão, para os testes de cada código de problema."""

FM = """---
status: in_progress
phase: execution
origin: request
description: um plano de teste
ready: sim
estimate_h: {est}
executed_h: {exe}
remaining_h: {rest}
opened: 2026-11-09
owner: Anderson
---
"""


def plan(steps="", interview="", deviations="", extra="", estimate="5", exe="0", rest="5", fm=None):
    header = fm if fm is not None else FM.format(est=estimate, exe=exe, rest=rest)
    return header + """
# PLN-900: Um plano de teste

- **Retomar:** nada.

## Pedido

- **Origem:** pedido livre.

## Entrevista

""" + interview + """
## Passos

""" + steps + """
""" + deviations + extra


ROUND1 = """### Rodada 1 — o começo (enviada 2026-11-09)

> **Apresentado antes:** o texto.

Respondida em 2026-11-09, na sessão do workstream `playground`.

1. **Destino.** Opções:
   - PLN novo (recomendada) — custo: 15 min; se paga: já;
   - worklog — custo: zero; se paga: nunca.

   **Decidido — PLN novo.**

2. **O nome.** Opções:
   - `plan-runner` (recomendada) — custo: nada; se paga: agora;
   - outro — custo: sync; se paga: nunca.

   **Resposta:** "mantém o nome" — lida como a primeira opção.
"""

DESIGN = """# PLN-900 — Desenho

## O que este desenho assume

- **R1.1:** o de sempre.

### D1 — O primeiro item — `a/b.py` (P1)

- **Origem:** R1.1, R1.2
- **Contexto:** porque sim.

#### As alternativas

##### A1 — Uma

- **Custo:** x.

##### A2 — Outra

- **Custo:** y.

#### Como fica

```
## isto não é heading
# nem isto
```

### D2 — O segundo item — `c/d.py` (P2)

- **Origem:** R1.1
- **Contexto:** outro.
"""


def step(pid="P1", title="Um passo", executes="Executa D1", estimate="5", exe="— h", checks="- [ ] **1. A**",
          evidence=None, extra=""):
    t = "### %s — %s\n\n%s · executor: `implementer`\n\nEstimado: %s h · Executado: %s\n\n%s\n" % (
        pid, title, executes, estimate, exe, checks)
    if evidence is not None:
        t += "\n**Evidência:** %s\n" % evidence
    return t + extra + "\n"
