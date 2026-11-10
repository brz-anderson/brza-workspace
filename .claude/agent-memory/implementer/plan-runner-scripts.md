---
name: plan-runner-scripts
description: scripts da skill plan-runner (PLN-021 P2) — formas reais dos planos que o plan_md.py precisa tolerar, armadilhas do parser e comando que valida
metadata:
  type: project
---

**Valida:** `cd <worktree> && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover -s ".claude/skills/plan-runner/scripts/tests"`
(84 OK em 2026-11-09). Rodar script com `python3 -I` sem a variável deixa `__pycache__` na pasta: apague antes de devolver.
`PR_SCRIPTS=<pasta>` aponta a suíte para outro snapshot (como o `MR_SCRIPTS` da meeting-runner).

**Formas reais do plano (o que o `plan_md.py` tolera, e por quê)**
- Rodada: `### Rodada N` no plano (PLN-017/020/021), `## Rodada N` no `-interview.md` (PLN-019, com `**R2.1.` explícito e
  opções `1. **…**` também em negrito: se há `**R<n>.<k>.` na rodada, só eles contam). Pergunta é `^\d+\. \*\*` na coluna 0;
  o "Apresentado antes" do PLN-020 R1 tem lista numerada SEM negrito, e a R8 do PLN-017 usa `1.` sem negrito para opções
  mais `**Pergunta:**` (uma pergunta só).
- A opção quebra em várias linhas: `(recomendada)` e `— custo:` podem estar na 2ª linha; `opcoes()` junta a continuação.
- `Decidido` aparece como `**Decidido — …**`, `**Escolhida …**`; a resposta literal como `**Resposta:**` ou
  `**Resposta literal de Anderson**`. Pergunta só com `Resposta` (vai à rodada seguinte) NÃO é decidida.
- `### D<n>` está em nível 3 no PLN-021 e nível 2 no PLN-020; no `PLN-017-design-cli.md` há `##### D1/D2/D3` de NÍVEL 5 que
  são alternativas, não itens: só níveis 2–4 valem. `A1` repete em cada D: o ID é escopado (`D1/A1`).
- Heading e checkbox dentro de cerca ``` não contam (o D3 do PLN-021 traz um molde com `## O passo`).
- `Executado:` vem como `~4 h (estimativa…)`, `0,174 h`, `— h` e `incluído nas 1,109 h agregadas…` (texto: vale como
  preenchido, não soma). `Estimado: 10,5 h` com vírgula.
- Regex de commit: `(?<!\w)` e exigir dígito; sem isso `run_fe70b351bc36` (id de Run) passa por commit.

**O que os scripts disseram dos reais (2026-11-09):** PLN-017 tem 2 erros verdadeiros (P7 sem commit/`→`/arquivo:linha;
`executed_h` 9.516 no frontmatter contra 7.974 somado) e 13 avisos `deviation-not-cited` (X só na tabela do design).
PLN-021 e PLN-020 limpos. Desvios do D6 que ficaram como `X` proposto: `nivel` (erro/aviso) e `linha` extras no problema;
`deviation-not-cited` e `hours-unreadable` são aviso.

**Fixtures:** `tests/fixtures/raiz/plans/` guarda cópias congeladas de PLN-017 (plan + 4 design) e PLN-021 (plan + design);
não atualize quando o plano real mudar. `tests/mini.py` tem os planos pequenos; `_paths.plano_tmp(plan, interview, design,
extra)` monta um `plans/PLN-900-teste/` num tmp e `copia_raiz()` copia as fixtures reais para escrever sem sujar o repo.
O `plan_md.carrega` deduz a raiz de `plans/` pelo caminho do arquivo (sem git); o git só entra para `PLN-NNN` sem `raiz`
e no `close_check.le_nota`, que lê nota de outro workstream por `git show workstream/x:caminho`.
