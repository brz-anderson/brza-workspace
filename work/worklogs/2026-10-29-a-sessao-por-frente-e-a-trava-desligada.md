---
scope:
  - workspace
---

# A sessão por frente e a trava de retomada desligada

O pedido de Anderson, em 2026-10-29: "precisamos reavaliar o cache e a trava das sessões, assim como o fluxo - cada
tarefa, uma sessão -, está mais atrapalhando que economizando tokens". A sessão mediu, levou à rodada e aplicou a
decisão: [Uma sessão por frente de trabalho, sem trava de retomada e com o cache de 1 h](../decisions/uma-sessao-por-frente-e-sem-trava-de-retomada.md).

## O que se fez

- **A medição:** `.measurements/measurements.jsonl`, de 2026-10-27 a 2026-10-29. Metade do gasto da sessão principal
  foi o primeiro turno das 33 sessões; a trava barrou uma vez; o cache de 1 h se pagou. Os números estão na decisão.
- **A rodada:** desligar a trava, uma sessão por frente e manter o cache de 1 h, todas nas recomendadas; depois,
  "Decidido, pode aplicar" e a nota no `Retomar` do PLN-003.
- **A configuração:** o hook `UserPromptSubmit` do `resume_guard.py` saiu do `.claude/settings.json`.
- **A norma:** a seção do `AGENTS.md` virou "Uma frente, uma sessão; uma tarefa, um worklog", com a _compactação_ no
  glossário; o `CLAUDE.md` perdeu a seção da trava e a linha `guard` da medição, e ganhou o `/compact` e os números do
  cache; o `README.md` perdeu as menções à trava.
- **O `brza sessions send`:** a sessão `pln-002-p7` recebeu as respostas literais por correio e tirou a trava do `send`
  em `88d8a3a`.
- **O PLN-003:** uma linha no `Retomar`, porque o Desenho ainda conta com a trava no roteador (M2) e na tabela de
  conflitos.

## O que ficou

- **O `resume_guard.py`** segue no repositório, fora de qualquer hook; o destino dele fica com o P7 do PLN-002.
- **O comentário do `~/.zshrc`** ainda cita a trava de retomada; ninguém mexeu nele, por estar fora do workspace.
- **A revisão da política** sai da medição dos próximos dias: o custo do primeiro turno por sessão e o contexto máximo.
