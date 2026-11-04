---
scope:
  - workspace
tags:
  - tooling
refs:
  - MIG-001
  - PLN-001
  - PLN-002
  - PLN-008
---

# O termo neutro nas notas do `studio`, no lugar do workspace de origem

O D11 do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../../workspace/plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md),
no P8, aplicado ao workstream `studio`. O pedido veio da sessão `workspace-a6`, com a autorização de Anderson de
2026-11-03 ("sim", à pergunta "Posso abrir as sessões?" do D11). Rodou na sessão `d11-studio`.

## O que Anderson decidiu (R15 a R17 do PLN-008, na `workspace-a6`)

- R15.1, em texto livre, e R15.2 "Tudo, inclusive código": a citação ao outro workspace sai de todos os repositórios.
- R16.3 "Termo neutro (Recomendado)": "outro workspace" ou "o workspace de origem", sem nome nem ID da nota de lá,
  inclusive em planos e worklogs fechados. R16.4 "Ficam como estão (Recomendado)": o histórico do git, o e-mail dos
  commits antigos e o `.brza/index.jsonl` não mudam.
- R17.1 "Exceção: ID de issue fica (Recomendado)": a identidade das duas issues do `tools-kit` fica no `refs` e no
  `depends_on`. Aqui nenhuma das duas aparece no `refs`.

## O que mudou

Commit `3297189`, com push na `workstream/studio`: 17 arquivos, com 121 citações em 17 notas antes da troca.

- **O termo de cada citação.** O workspace vira "workspace de origem", o fork de lá vira "fork de origem", e o plano
  que se dividiu e virou o PLN-001 vira "plano de origem". O plano que veio para cá vira "o plano de lá", e o plano do
  fork, "o plano do fork de origem". Os IDs desses três planos de lá saíram também nas citações sem o nome, como a
  conferência no Orca de cada passo do PLN-001. O número da rodada ou do passo de lá fica, com "de lá" ou "do plano de
  origem": não é ID de nota.
- **Sessões, contas e caminhos.** As sessões de lá ficam pelo número ("sessão 35 do workspace de origem"), e a sessão
  daqui que tinha o nome de lá fica pelo que fez ("a sessão que levou o PLN-001 ao molde"). Os e-mails viram "a conta
  `anderson@`" e "a conta `admin@`", e o certificado de assinatura fica `Apple Development: anderson@… (V72RV8BZY4)`.
  O worktree, a branch e o site Atlassian de lá ficam pelo assunto. Os caminhos de notas e de worklogs de lá saíram,
  e o `## Decisões` do PLN-001 cita as duas decisões de lá pelo assunto e pela rodada.
- **Dois worklogs renomeados** pelo `move_note.py`, pelo mapa do D11:
  - [O PLN-001 conferido contra a norma de planos do workspace de origem e levado ao molde](2026-10-28-pln-001-no-molde-do-workspace-de-origem.md),
    com H1 novo;
  - [O ▶ que executa o bloco de shell, o ⤢ que expande o bloco e o copiar sem o `\n` final no chat](2026-10-27-o-executar-e-o-expandir-do-orca-de-origem-no-chat.md),
    com o H1 de antes, que já era neutro.
- **O link para o `tools-kit`.** A issue dos scripts de orquestração já tinha o nome novo lá (`9a40746`), e o link da
  issue do Codex como subagente foi junto, com o H1 novo de lá.
- **O worklog da MIG-001** recomitado: com o extrator do `brza-workflow@30b3666` (R14.3), o `refs` dele perdeu os
  dois pareceres que vinham só do rótulo do link para a MIG-001.
- **As linhas que passaram de 120 colunas** foram rebatidas, só nos parágrafos que mudaram.

## Conferência

- `python3 .claude/skills/notes-checker/scripts/check_notes.py`: 75 arquivos, 0 links não resolvidos, **0 erros** e
  8 avisos (6 `backlink-missing` e 2 `tag-out-of-vocabulary`).
- O `git grep -il` do nome de lá, fora do `.brza/index.jsonl`, sai vazio. Nada de norma da `master` apareceu.

## O que ficou aberto

- O `plans/PLN-002-os-comandos-brza/PLN-002-interview.md`, do `tools-kit`, aponta o worklog do ▶ e do ⤢ pelo nome
  antigo. O link quebra até a segunda passagem do `tools-kit`.
- O `work/worklogs/2026-11-03-pln-011-execucao.md` estava sujo por outra sessão e não foi tocado; ele não cita o
  workspace de origem.
