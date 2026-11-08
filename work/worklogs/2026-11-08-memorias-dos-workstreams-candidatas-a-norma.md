---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
refs:
  - PLN-017
  - issue:memorias-dos-workstreams-sobem-a-norma
---

# As memórias dos quatro workstreams, lidas contra a norma: o que sobe, o que sai

Pedido de Anderson em 2026-11-08, na sessão `workflow-improvements` (`playground`), depois de o PLN-017 fechar a rodada 4: "levante também memórias dos outros workstreams, que não foram a `master`, mas que podem ser úteis, e que são candidatas há subir".

## O que se fez

Dois `collector` em paralelo leram as 76 memórias de `memory/` e `.claude/agent-memory/` das branches `workstream/workspace` (21), `tools-kit` (14), `studio` (29) e `brand` (12), sem checkout, e conferiram cada uma contra os onze arquivos da norma da `master` e contra o disco (`brza-workflow`, `brza-studio`, versões dos runtimes, status dos planos). Os agregados ficaram no scratch da sessão.

- **Nenhuma memória está inteira na norma.** Cinco estão parciais (a norma diz "a tarefa fecha na hora"; a memória diz "sem perguntar").
- **A lição mais repetida** são as armadilhas do zsh e do macOS (`$rev:arq` como modificador, glob sem aspas, `echo ===`, `sed -i ''`, `rm -rf` com glob barrado): doze memórias de três papéis nos quatro workstreams.
- **A mesma correção de Anderson apareceu duas vezes**, em `studio` (2026-11-02) e `brand` (2026-11-03): o push ou o aceite fecha a tarefa; o `close-task` roda sem oferecer.
- **Quatro memórias contradizem a norma de hoje:** a edição renderizada em callout (pedido de 2026-10-31) contra a cerca `diff`; "commit ao fechar todo passo" (ordem de 2026-11-03) contra "commite só com confirmação"; a rodada delegada a outro agente sem a recomendação (pedido de 2026-11-03) contra "a recomendação é a primeira opção"; "a suíte uma vez, no merge" contra "rode a suíte inteira do que tocou".
- **Nove memórias citam caminhos que o Studio já moveu** (`run-vitest.mjs`, `ci-unit-files.mjs`, `MarkdownPreviewBody.tsx`, `orca-dev.mjs`, `agent-trust-presets.ts`), e nove envelheceram com a tarefa (as lições do sync 251, `hooks-do-claude-testes`, `cada-passo-revisado-pelo-agy`).
- **O `AGENTS.md` do `brza-studio` é o texto do upstream**, com só autores do upstream no `git log`: as três regras de código do fork não têm casa.

## A rodada

Quatro perguntas, respondidas por Anderson em 2026-11-08, na sessão `workflow-improvements`:

1. **O que sobe:** "As regras de conduta no AGENTS.md, As armadilhas e os testes nas rules, As lições dos papéis" (as três, em seleção múltipla).
2. **As contradições que se resolvem a favor da memória:** "Edição em callout, não em cerca diff, Suíte inteira uma vez, no merge, Rodada delegada sem recomendação, Commit ao fechar todo passo, para todos" (as quatro).
3. **A norma de código do `brza-studio`:** "Bloco 'BrzA fork' no fim do AGENTS.md do studio".
4. **Quem executa:** "Issue ao workspace, com os textos prontos".

O texto das opções, com custo e quando se paga, está nesta sessão; a issue traz as decisões citadas.

## O que ficou

- **A issue** [As memórias dos workstreams que valem para todos sobem à norma, com o texto pronto por arquivo](../issues/memorias-dos-workstreams-sobem-a-norma.md), ao `workspace` (e ao `studio`, pelo bloco do fork), com 21 textos por arquivo de destino, a lista do que sai em cada workstream e os caminhos a corrigir. A execução é pela `agent-instructions-writer`, no `core/` do `brza-workflow` e na `master`, com `brza sync` e `brza note sync`; cada workstream apaga as suas no `close-task` seguinte.
- **Nada da norma foi editado nesta sessão**, que é do `playground`; as memórias deste workstream não entraram no levantamento (são de hoje e já estão nas Restrições e no D1 do PLN-017).
