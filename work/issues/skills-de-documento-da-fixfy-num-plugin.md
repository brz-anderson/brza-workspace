---
status: open
scope:
  - workspace
  - brza-studio
opened: 2026-10-31
trigger: Anderson abre o plugin, ou o brza-studio passa a registrar decisão de estrutura, manual ou spec próprios.
tags:
  - tooling
---

# As skills de documento da Fixfy num possível plugin do BrzA

Em 2026-10-31, a sessão `workspace` triou as 16 skills do `~/Projects/fixfy/fixfy-plugin/skills/` para o porte ao
brza-workspace. As seis de documento ficaram fora do workspace, e Anderson as mandou para cá: "essas vão ao `tools-kit`
para um possível plugin".

| Skill, na Fixfy | O que faz lá | Por que não entrou no workspace | Tamanho (`SKILL.md` + refs) |
| :-------------- | :----------- | :------------------------------ | :-------------------------- |
| `adr-writer` | ADR em `docs/adr`, com proposta, congelamento e migração | A decisão daqui já é `work/decisions/`; o molde `proposed-template.md` é o que mais se aproveita | 251 + 806 linhas |
| `constitution-writer` | A constituição de um repositório | A norma de topo daqui é o `AGENTS.md` | 175 + 290 |
| `manual-writer` | Manual em `docs/architecture` e `docs/conventions` | Os dois não existem; `wiki/guides/` é outro gênero | 230 + 363 |
| `migration-writer` | Dívida de migração `MIG-NNN`, que pressupõe ADR e constituição | A dívida daqui é `work/issues/` | 196 + 513 |
| `spec-writer` | `SPEC.md` por feature, no SDD da Fixfy, com persona e card `FIX-NN` | Não há SDD, persona nem card aqui | 162 + 979 |
| `readme-writer` | README de pacote e feature em Dart, com emoji e badges | O repositório tem um README só | 134 + 478 |

O que as seis têm em comum é o `docs/` de um repositório de código, que o `brza-studio` não tem: sem `docs/adr`, manual
nem constituição (`ls ~/Projects/brza-studio/docs`, no levantamento). O plugin faria sentido quando ele passar a ter.

**O porte não é cópia.** Cada uma cita o `fixfy-context`, o `doc-governance` e os papéis do time da Fixfy
(`architect`, `product-owner`), que aqui viram os subagentes por papel do `AGENTS.md`. A triagem inteira está em
[O porte das skills da Fixfy para o workspace](../worklogs/2026-10-31-o-porte-das-skills-da-fixfy.md), no workstream
`workspace`.
