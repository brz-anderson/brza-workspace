---
scope:
  - workspace
  - brza-workflow
  - brza-studio
refs:
  - MIG-001
  - PLN-008
  - PLN-011
  - REV-006
  - issue:a-sessao-no-brza-studio-nao-recebe-a-identidade-do-workspace
  - issue:o-refs-grava-o-slug-novo-quando-o-commit-renomeia-a-issue
---

# O P8 do PLN-008: o checador, o refs e o termo neutro

Anderson pediu "abra" para a sessão do P8 e "sim" para as sessões do D11. Plano:
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).

## A parte da R14

A sessão `pln008-p8` publicou `brza-workflow@30b3666`, com os três avisos do checador, a norma de `depends_on` de
volta ao D2, o texto do link fora das duas cópias do extrator e um teste de paridade entre elas. Esta sessão rodou o
`brza sync --ref 30b3666`, que gerou `2130026`.

## A colisão que virou o D11

Com o extrator novo, dois worklogs daqui ganhariam o PLN-011 do `studio`, porque citavam em crase o ID de um plano de
outro workspace. As Rodadas 15 a 17 transformaram isso no D11: o nome do workspace de origem sai de todos os
repositórios `brza-*`, com termo neutro, a guarda do `brza init` lendo um arquivo da máquina, o histórico intocado e a
identidade das duas issues renomeadas mantida.

Esta sessão fez a `master` (`bc4f5ba`) e o `brza note sync`, e definiu o mapa de nomes antes de abrir seis sessões. Um
`implementer` fez as 33 notas daqui, que esta sessão revisou e gravou em `835f023`. As sessões gravaram:

- `d11-brza-workflow`: `ebb4e7d`;
- `d11-tools-kit`: `9a40746`, `ffc0cf7` e `e3fd4d2`;
- `d11-studio`: `3297189`;
- `d11-brand`: `2c18797`;
- `d11-playground`: `e271921`;
- `d11-brza-studio`: `a6ef12c`, numa branch.

O `brza sync --ref ebb4e7d` gerou `8098514`.

Na conferência final, nenhum arquivo atual cita o nome, salvo o índice, as identidades da R17.1 e a `master` do
`brza-studio`. O checador deu 0 erros nas cinco árvores, e os três blocos da MIG-001 saíram com 0.

## A Rodada 18

- Anderson escolheu "Corrigir autor e mesclar (Recomendado)" para o `brza-studio`, cuja branch saiu com o e-mail
  noreply.
- Para o defeito do `refs` no rename de issue, escolheu "Issue no workspace (Recomendado)":
  [O refs grava o slug novo quando o commit renomeia a issue](../issues/o-refs-grava-o-slug-novo-quando-o-commit-renomeia-a-issue.md).
- Para o X2, escolheu "Aceitar o X2 (Recomendado)".

## O `brza-studio` e a regressão final

A proteção da sessão `d11-brza-studio` barrou o amend e o force push. Anderson os rodou à mão, e a `master` de lá
ficou em `1ef93b3`, com o Gmail. A causa do noreply era o `.git/config` local do `brza-studio`, e a sessão não tinha os
`GIT_AUTHOR_*`. Na rodada do Fechamento, Anderson escolheu "Issue e config agora (Recomendado)": o `user.email` local
passou ao Gmail, e a causa foi para
[A sessão no brza-studio não recebe a identidade do workspace](../issues/a-sessao-no-brza-studio-nao-recebe-a-identidade-do-workspace.md).

A regressão final em `brza-workflow@ebb4e7d` passou: CLI 483, hooks 291, notes-checker com 99 checagens e
`scripts/brza/tests` com 98. Para as horas, Anderson escolheu "Aferir P5–P8 pela medição".

## O Fechamento

O `collector` aferiu as horas pela medição: 3,2 h de turnos em P6–P8 e US$ 25,23 com os subagentes. P1 a P5 rodaram no
Antigravity e no Codex, fora do hook; o começo do P6 e três sessões do P8 também ficaram sem linha. Na Rodada 19,
Anderson escolheu, para o P6, "2,0 h com nota (Recomendado)"; para a sessão mista, "Só o 1º turno (Recomendado)"; e,
para o que não tem linha, "\"Sem medição\", com o porquê (Recomendado)". A falta de linha nas sessões fora do
workspace foi para a issue da identidade, que tem a mesma causa provável.

O plano fechou com `status: done`, `phase: closed`, `executed_h: 3.2` e `remaining_h: 0`. P1 a P4 fecharam com os
commits deles e a Cobertura da REV-006. As pendências seguem em issues abertas.

## Fora do workspace

- **O quê e onde:** `~/.config/brza/foreign.txt`, criado pela sessão `d11-brza-workflow`, com o nome que a guarda do
  `brza init` recusa. **Risco:** sem ele, um `brza init` nesta máquina deixa de recusar o nome. **Estado:** em uso
  pela guarda. **Como desfazer:** apagar o arquivo.
- **O quê e onde:** os pedidos das sessões, no scratch do chat (`d11-*.md`, `pln008-p8-prompt.md`). **Risco:**
  nenhum. **Estado:** temporários. **Como desfazer:** apagar.
- **O quê e onde:** `user.email` do `.git/config` local de `~/Projects/brza-studio`, de
  `240569289+brz-anderson@users.noreply.github.com` para `brz.anderson.pereira@gmail.com`. **Risco:** nenhum; é a
  identidade que o `CLAUDE.md` exige. **Estado:** em uso. **Como desfazer:** `git -C ~/Projects/brza-studio config
  --local user.email <o e-mail antigo>`.
