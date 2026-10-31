---
name: padroes-de-erro-nas-entregas
description: Onde os defeitos das entregas de plano do workspace costumam se esconder (hooks de medição, auditoria por LLM, evidência de passo [x], desvios), e as hipóteses que costumam cair
metadata:
  type: project
---

Padrões vistos na revisão do PLN-005 (2026-10-31), a primeira deste papel no workstream `workspace`.

**Os que se repetem e onde se escondem:**
- **O corte que alimenta outro consumidor.** Uma constante de limite (`TEXT_LIMIT`, `[:300]`) pensada para o log vai
  também ao que decide (o arquivo do auditor). Conferir no dado real quantos itens batem no limite exato; o teste
  costuma fixar o corte como comportamento. Confiança dada: 95, verificado no transcript real.
- **Veredito de LLM sem prova.** Auditor `claude -p` diz `holds` com linha e arquivo no `why` sem ter aberto o arquivo.
  Conferir cruzando o transcript da sessão do auditor (`~/.claude/projects/<cwd>/<session>.jsonl`, `tool_use`) com o
  que cada fato cita. Confiança dada: 90.
- **Evidência de `[x]` que afirma uma medida** ("nenhuma linha passa de 120 colunas", "N linhas"): refazer com `len()`
  do Python, não com `awk length` (conta bytes no macOS e acusa falso positivo em linha com acento).
- **Desvio que mudou um `D` sem rodada**, com o `D` deixado no texto antigo: comparar o plano aceito
  (`git show <commit do aceite>:plans/...`) com o atual. A regra é a do `conduct.md` ("Desvio que muda um D vira
  rodada"). Confiança dada: 92.
- **Norma que não acompanhou a última mudança do código**: o passo que muda o código depois do passo da norma (aqui, o
  P10 depois do P7) deixa o `CLAUDE.md` com o valor antigo. `git diff <commit da norma> <último> --stat`.
- **Script que acha a raiz por `scripts/..` ou pela `BRZA_WORKSPACE`**: o `~/.zshrc` não exporta a variável, e no
  worktree a raiz vira o worktree, que pode ter um `.measurements/` velho; o log ausente vira "vazio" sem aviso. Testar
  com `env -u BRZA_WORKSPACE` no worktree e rodar da raiz da `master` (onde o workstream é `master`, não vazio).
- **Teste de timeout que não distingue `killpg` de `kill`**: mutação numa cópia em `/private/tmp` mostra.

**Hipóteses que costumam cair** (deixar como `→ falso` no parecer):
- a trava compartilhada do `measure.State` segurando o hook — conferir pelos timestamps `subagent` → `fact_capture`;
- a sessão no worktree do `brza-studio` sem o modelo ou a permissão — o `env` do `settings.json` chega aos filhos, e o
  `defaultMode: auto` é de usuário;
- vazamento para o log — `.measurements/` está no `.gitignore`.

**Cuidado de leitura:** dois `sed -n` concatenados num só comando colam trechos de testes diferentes e fazem parecer
código morto; ler o teste pelos limites do `def`.

Relacionado: [[o-log-de-medicao-como-dado]].
