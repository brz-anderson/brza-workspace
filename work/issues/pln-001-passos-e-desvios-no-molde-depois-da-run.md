---
status: open
scope:
  - workspace
opened: 2026-10-28
tags:
  - tooling
---

# Os Passos e os Desvios do PLN-001 no molde, depois da Run do P44 ao P50

Em 2026-10-28, na sessão `pln-001-norma-fixfy`, Anderson respondeu "Levar tudo ao molde" à pergunta sobre o formato que
o [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md)
herdou do PLN-029 da Fixfy. O Desenho, as seções novas (`## Restrições`, `## Regressão` e `## Casos manuais`), a
Cobertura, o `## Decisões` e o Fechamento já foram levados ao molde nessa sessão. Os Passos e os Desvios ficaram para
depois, porque a sessão `pln-001-p44-p50`, que coordena a Run `run_de875fc52a75`, grava neles a evidência de cada
`worker_done`. Ela respondeu pela orquestração: "depois-da-run", e também a `## Entrevista` e o frontmatter.

Antes, a coordenadora, ao fechar a Run, reescreve o `Retomar` numa linha, leva os IDs da Run ao worklog dela e tira do
`Retomar` o operacional que já está em `## Restrições`.

O que falta, numa sessão nova aberta depois do último commit da Run no plano:

- **Os Passos sem fases**: os `### F1 — …` a `### F7 — …` saem, e cada `#### P<n>` vira `### P<n>`, na forma do
  molde da `plan-runner` (`references/plan-template.md`, `## Passos`).
- **Os Desvios em até duas linhas cada**, do X1 ao último que a Run gravar (eram do X1 ao X12 em 2026-10-28). A
  evidência que estiver no desvio — run, sha256, tamanho do instalador — vai ao passo que ele afeta.
- **Os três testes que a `## Regressão` marca "teste a escrever"**, pedidos à sessão do `brza-studio` (rodada de
  2026-10-28, "Marcar e levar à issue"): o rótulo do upstream para comando sem categoria do BrzA
  (`native-chat-tool-line-label.ts:94-108`), no P44; o recuo de cada logo de marca no mobile
  (`mobile/src/session/native-chat/transcript/brza/`), do P43; e o `isUpdaterEnabled()` com versão de release
  (`1.4.242` e `1.4.242-local.1.abc`), do P26. Cada um vira subpasso do passo dele, e a linha da Regressão perde o
  "teste a escrever" quando o teste entra.
- **O checador** (`python3 .claude/skills/notes-checker/scripts/check_notes.py`) com zero erro, e esta issue em
  `done`, com a linha de como se resolveu.
