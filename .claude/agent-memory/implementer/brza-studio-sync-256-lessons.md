---
name: brza-studio-sync-256-lessons
description: Resolver blocos diff3 do sync v1.4.256 - classificar bloco como rebrand-puro, upstream apagou testes, extração de runner do fork, max-lines por import
metadata:
  type: project
---

- Bloco diff3 em que `ours` == `base` a menos de rebrand/espaço: pegue `theirs` e reaplique o rebrand (regex `\bOrca\b` -> BrzA Studio, "An Orca" -> "A BrzA Studio"); script por bloco evita ler 100 KB de conflito.
- Upstream da 256 apagou 279 testes de baixo valor (#39527): em teste com `ours` = fork, pegue `theirs`, mas preserve só a asserção que é identidade do fork (repos de release `brz-anderson/*`, linha `brza ...`), e confira o import que o upstream encolheu.
- Valores de locale que o merge_locales deixou "do upstream sem rebrand": editar por caminho JSON (walk por prefixo com ponto) e `json.dumps(indent=2, ensure_ascii=False)` mantém o diff só nas linhas certas. Coreano: `Orca` colado em partícula, use `replace('Orca','BrzA Studio')`.
- `max-lines` 300 conta só código: import multilinha do fork pode virar dois imports de uma linha (`import` + `import type`) quando o arquivo do upstream já está no teto.
- Fork extraiu `runDaemonEntry` para `config/build-plugins/plain-node-daemon-smoke-runner.ts`; ao ressolver o `plain-node-entry-guard.ts`, mantenha esse import e o `cli-main-entry-names.ts` do upstream (entrada do fork vai nele).
