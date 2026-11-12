---
name: brza-studio-sync-256-ud-lessons
description: UD do sync v1.4.256 — rastrear destino por git log --name-status, rename não detectado, merge-file por arquivo, fork-only com import velho
metadata:
  type: feedback
---

- **Rastreio do destino em um passo só:** `git log --reverse --format='C %h' --name-status --diff-filter=RD -M -l5000 base..tag > log` e um script que segue cada caminho (R troca, D encerra). Leva 0,5 s. Quando o rename passa de ~50% de mudança o git emite D+A: confira `git ls-tree -r --name-only tag | grep "/<basename>$"` para os "deletados" antes de aceitar a remoção.
- **Porte por arquivo:** `git merge-file -p --diff3 ours base theirs` com `base:old`, `HEAD:old`, `tag:novo`; resolva conflito com `--theirs` e leia o `diff` contra theirs: é o que o fork de fato acrescenta. Conflito com theirs vazio = o upstream apagou o teste ("remove low-value tests"), aceite.
- **Barril apagado pelo upstream:** o importador fork-only já movido por outro grupo continua apontando para o barril; ache com `git grep` e importe do contrato em `shared/`.
- **Teste de fork num arquivo apagado:** vizinho `*.brza.test.ts` com o harness do tag; o harness mudou (`RESUMES` virou const local, `CALLER` tem várias cópias).
- **Teste novo não roda enquanto outro grupo não ajusta fork-only com import velho** (`./journal-account-switch`, `./structured-agent-session-mutation-admission`): reporte e siga.
