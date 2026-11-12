---
scope:
  - workspace
  - brza-studio
tags:
  - planning
  - infra
refs:
  - PLN-014
---

# R1 do PLN-014 e default dos plugins

## O que foi feito

Anderson respondeu "ambos recomendado" às duas rodadas da auditoria de priorização.

### PLN-014 / R1

1. **A1** — regra de despacho.
2. Issue de chats **fica `open`** com ponteiro a PLN-011 e PLN-010.
3. **Parêntese** nos 7 arquivos que citam número fechado.

Aplicado: bloco de despacho nas quinze issues do terreno de 2026-11-04; parêntese
`(MERGED no upstream; não está no fork)` / `(CLOSED…)` nos sete; Entrevista R1 via `round_log.py`; `phase: design`;
`blocks` da entrevista removido.

### Decisão do worker

[O default dos plugins e o alcance do worker sem sandbox](../decisions/o-default-dos-plugins-e-o-alcance-do-worker-sem-sandbox.md)
passa a `done`: default do fork = `pluginSystemEnabled: false` com `pluginSystemDefaultedOn: true`.

Patch local preparado em `/tmp/brza-studio-pr` (branch `cursor/plugins-default-off-85ba`, commit `4920522af`);
`git push` ao `brza-studio` falhou com 403 para `cursor[bot]`.

## O que não foi feito

- Push/PR do patch no `brza-studio` (403).
- Porte de código das issues do radar.
- Isolamento do token do runtime do worker.
- C1 do PLN-011.
