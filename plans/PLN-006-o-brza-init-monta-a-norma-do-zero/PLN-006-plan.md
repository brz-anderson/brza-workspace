---
status: open
phase: interview
origin: request
ready: não — faltam a R2 (a fronteira genérico/local e a fonte do núcleo), o Desenho e os Passos
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - tooling
---

# PLN-006: O `brza init` monta a norma num workspace do zero

- **Retomar:** R1 fechada, toda na recomendada. Próximo: o Terreno pelo `collector` (o que é genérico e o que é local
  em cada arquivo da norma) e a R2, sobre a fronteira e a fonte do núcleo.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "nós já temos mecanismos para inicializar a norma inteira, com AGENTS CLAUDE plans/ wiki/ work/ skills/ agents/ num
> repositório do zero?"

Respondido que não, Anderson pediu: "plano".

### Cobertura

> Rascunho da abertura: os critérios são propostas e se fecham no Planejar, com o passo e o teste.

| Origem     | Critério de aceite                                                                                                                                                                                  | Passo | Teste (nível)                    |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---- | :------------------------------- |
| `Pedido 1` | `brza init <dir>` cria, num diretório vazio, um workspace com `AGENTS.md`, `CLAUDE.md`, `README.md`, `plans/`, `wiki/`, `work/`, `.claude/skills/`, `.claude/agents/`, hooks e `settings.json`, e o `notes-checker` roda verde nele | —     | unidade, num diretório temporário |
| `R1.2`     | O workspace inicializado aponta para o repositório de código dele, sem caminho fixo a `brza-workspace` ou `brza-studio` no que foi copiado                                                         | —     | unidade                          |
| `R1.4`     | Uma mudança no núcleo genérico daqui chega ao workspace inicializado por um comando de sync, sem tocar a parte local dele                                                                           | —     | unidade                          |
| `Pedido 1` | O `brza-workspace` segue funcionando depois da separação genérico/local: hooks, skills, `brza note` e os testes de hoje                                                                            | —     | os testes de hoje (unidade)      |

### Fora de escopo

- **A norma dentro do próprio repositório de código, sem workspace separado.** Fica de fora pela R1.2; volta como plano
  novo se um projeto pedir.
- **Generalizar o `brza tree` e o `brza test` para outro repositório de código.** Já decidido no
  [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
  R2.3, no workstream `tools-kit`; este plano não o refaz.

## Entrevista

### Rodada 1 — destino, alvo, mecanismo e atualização (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- Não há mecanismo de inicialização. As peças de hoje — `brza note workstream`, `memory-setup`, `new`, `sync`,
  `brza install`, o `notes-checker` — só operam dentro do `brza-workspace` já montado.
- Os caminhos estão fixos em `scripts/brza/brza_runtime.py:21-23` (`brza-workspace`, `brza-studio`, o `Application
  Support/brza-studio`); a função `claude` do `~/.zshrc` e o `claude-brza` só reconhecem os dois repositórios.
- O `measure.py` e o `compact_guard.py` gravam no `.measurements/` do `BRZA_WORKSPACE`.
- A `master` tem ~14 mil linhas versionadas, metade teste. Umas 250 linhas, em ~40 arquivos, citam o que é local
  (BrzA Studio, `brza-studio`, Anderson, `brz-anderson`, Fixfy, Orca, `~/Projects`); as que mais citam são o
  `CLAUDE.md` (22), o `work/README.md` (16), o `brza-shot` (14), a `plan-runner/SKILL.md` (13), o `AGENTS.md` (12) e o
  molde de plano (12).
- A separação genérico/local custa ~4–6 h em qualquer caminho, e o mecanismo vem em cima.

Respondida em 2026-10-31.

1. **Destino.** Opções:
   - `PLN-006` no `workspace` (recomendada) — custo: abrir o `PLN` (~10 min) e uma linha na `master`; se paga: já,
     porque o trabalho atravessa sessões;
   - `PLN` no `tools-kit` — custo: o mesmo, com a separação da norma virando pedido cruzado; se paga: só se o mecanismo
     pesar mais que a separação;
   - worklog de hoje — custo: nenhum agora; se paga: nunca, porque ~10 h não fecham numa sessão.

   **Decidido — "PLN-006 no workspace (Recomendado)".**

2. **Alvo.** Opções:
   - workspace ao lado do código, como o par `brza-workspace` + `brza-studio` (recomendada) — custo: tirar os caminhos
     fixos e parametrizar o par, ~2–3 h; se paga: no primeiro projeto novo;
   - norma dentro do código, sem workspace separado — custo: refazer o modelo de workstreams, ~4–6 h a mais; se paga: em
     projeto pequeno;
   - os dois formatos — custo: a soma, ~6–9 h, e testes dobrados; se paga: só com os dois em uso.

   **Decidido — "Workspace ao lado do código (Recomendado)".**

3. **Mecanismo.** Opções:
   - `brza init`, script determinístico que copia o núcleo genérico e preenche o local por flags ou prompt (recomendada)
     — custo: ~3–4 h com testes, além da separação; se paga: a partir do segundo repositório;
   - skill com entrevista, rodada por um agente — custo: ~2–3 h, mais tokens a cada uso, com saída que varia; se paga:
     quando a parte local exigir texto livre;
   - repositório template do GitHub — custo: ~1–2 h, com a parte local editada à mão a cada vez; se paga: só se a parte
     local for mínima.

   **Decidido — "brza init, script (Recomendado)".**

4. **Atualização.** Opções:
   - acompanha por sync, com o núcleo genérico numa fonte que o workspace novo puxa (recomendada) — custo: ~3–5 h, e a
     fronteira genérico/local em arquivos separados; se paga: na primeira mudança de norma, que muda quase todo dia;
   - cópia que diverge — custo: zero agora, e cada melhoria portada à mão; se paga: só em repositório curto.

   **Decidido — "Acompanha por sync (Recomendado)".**

## Worklogs

- 2026-10-31 — aberto; R1 respondida, toda na recomendada. Parou antes do Terreno e da R2.
  [PLN-006: a abertura do brza init](../../work/worklogs/2026-10-31-pln-006-a-abertura-do-brza-init.md)
