---
name: reference-fixfy-skills-triagem-atalhos
description: Mapa para triar/comparar as skills da Fixfy (fixfy-plugin/skills) com as do brza-workspace; atalhos de grep/diff e armadilhas de citar linha
metadata:
  type: reference
---

Confirmado em 2026-10-31 (confira que os caminhos ainda existem).

**Onde mora**
- Origem: `~/Projects/fixfy/fixfy-plugin/skills/<skill>/{SKILL.md,references/,scripts/}`; papéis em `~/Projects/fixfy/fixfy-plugin/agents/` (8: architect, atlassian-collector, developer, product-owner, qa-engineer, reviewer, ui-designer, ux-designer). Só um script em skill: `git-runner/scripts/clean_merged.py`.
- Destino: `.claude/skills/{plan-runner,close-task,notes-checker}` e `.claude/agents/{collector,designer,implementer,reviewer}` no worktree. `plan-runner` daqui é porte limpo da Fixfy (grep `fixfy|jira|FIX-|architect|product-owner` vazio).
- A norma de pastas de nota (e a lista das que NÃO existem: archive, templates, sessions…) está em `work/README.md:77-88`; `wiki/` está vazia, `work/{issues,notes,reviews}` vazias, `plans/` só tem PLN-004.

**Atalhos**
- Os 8 skills de "documento" (adr, constitution, manual, migration, readme, spec, review, agent-instructions) dependem todos de `fixfy-context/references/{doc-governance,decision-protocol,fixfy-engineering-policy}.md` e dos papéis `architect`/`reviewer`: um grep por `fixfy-context|architect|docs/(adr|migration|architecture)` em cada um já dá a dependência; não precisa ler as ~5 refs de cada.
- Comparar o plan-runner: `diff <(grep '^#' F/x.md) <(grep '^#' W/x.md)` por arquivo mostra só a estrutura; o `diff` completo de SKILL.md passa de 200 linhas.
- Tamanho de refs por skill: `find <d> -type f ! -name SKILL.md -exec cat {} + | wc -l`.
- `~/Projects/brza-studio` é fork do Orca (AGENTS.md de 69 linhas, `docs/agents-md-refs/`, `skill-guides/` do Orca); não tem docs/adr, manuais nem constituição — não procure lá o gênero das skills de doc.

**Armadilhas**
- Número de linha citado de cabeça ou de saída de `diff` erra: reconfira com `grep -n` antes de gravar (errei ~15 em um levantamento).
- O `decision-protocol.md` da Fixfy (85 linhas) já está parcialmente absorvido no `AGENTS.md` daqui (rodadas, ataque à recomendação); "O que já existe precisa ser revisado?" não foi conferido lá.
- `work/README.md:336` promete releitura de `work/notes/` "no encerramento do dia", mas o `close-task` não a faz (lacuna).
