---
name: skills-via-skill-creator
description: No workstream playground, toda skill se cria e se revisa pela skill skill-creator, do plugin habilitado no .claude/settings.json da branch
metadata:
  type: feedback
---

Toda skill deste workstream (a `meeting-runner` do PLN-017 e as que vierem) se cria e se revisa pela skill `skill-creator`, do plugin `skill-creator@claude-plugins-official`, habilitado no `.claude/settings.json` versionado da branch `workstream/playground` (não no `settings.local.json`, como a norma manda para os outros workstreams).

**Why:** pedido de Anderson em 2026-11-08, na sessão `workflow-improvements`: "instale o plugin skill-creator no escopo desse workstream, no settings.json versionado, e utilize a skill skill-creator para criar e revisar as skills desse plano e as que serão criadas futuramente nesse workstream". O registro do escopo está em `.claude/rules/workspace.md`, na `master`.

**How to apply:** o passo que escreve ou revisa uma skill aciona `/skill-creator` antes de gravar o `SKILL.md`, e roda numa sessão aberta depois de o plugin entrar no `settings.json` (a sessão carrega plugins no arranque). Enquanto a sessão não o vê na lista, lê-se o `SKILL.md` do plugin no cache (`~/.claude/plugins/cache/claude-plugins-official/skill-creator/<versão>/skills/skill-creator/SKILL.md`) e segue-se o processo dele. Ver [[coordination-narration-in-chat]].
