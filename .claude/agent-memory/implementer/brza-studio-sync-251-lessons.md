---
name: brza-studio-sync-251-lessons
description: Armadilhas do sync v1.4.251 do brza-studio que valem para o próximo sync (base ruidosa, fork ja extraido, import movido, checar linhas do fork)
metadata:
  type: project
---

- **A base do merge (54ef0dea) é ruidosa**: `git diff base HEAD` mostra mudança do upstream como se fosse do fork. Para saber o que o fork fez, use `git log 54ef..HEAD -- <arq>` e os commits do fork (`git show <c>`), e confira com um script que cada linha `+` do commit do fork ainda existe no arquivo resolvido.
- **Resolvedor de hunks diff3**: um script Python com regex sobre `<<<<<<< ours ... ||||||| base ... ======= ... >>>>>>> theirs` e escolha por hunk (ours/theirs/texto) é bem mais rápido que editar à mão. No zsh, não faça `echo "===="` (vira expansão).
- **Auto-merge deixa resíduo**: import sem uso (`vi`, `AgentSessionOptionRejectedError`, `stopVisualsSweep` no `catch`) e caminho de import velho em arquivo do fork sem conflito. Rode `tsc` com `tsconfig` temporário (extends `config/tsconfig.node.json`, `composite:false`, `include` só dos seus arquivos mais os helpers do fork) e filtre `TS1185`.
- **Duas features iguais**: o upstream passou a ter retomada automática no limite de uso própria; a do fork (P79, `state-schedules`) convive. Ponto de rodada, não decisão do implementer.
- **Outro grupo mexe no índice**: `git status` deixa de mostrar `UU`; guie-se por `grep '^<<<<<<< '` e `git ls-files -u`.
- **Teste de mobile não roda** aqui; o upstream apaga testes de baixo valor: aceite a remoção quando o fork só trocou o mock.
