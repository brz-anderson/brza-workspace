---
scope:
  - workspace
---

# A trava de fechamento antes do /compact

O pedido veio da sessão do PLN-004, depois da rodada que Anderson respondeu em 2026-10-30 com "siga com a 2" (o registro
está no [O /compact, o nome em inglês e o arquivo gravado à vista](2026-10-30-o-compact-o-nome-em-ingles-e-o-arquivo-gravado-a-vista.md)).
A opção 2 era a skill de fechamento com uma trava no `PreCompact`, só no `manual`, mais um aviso depois da compactação
automática. A norma foi para a `master` em `ec2b1f0` e chegou aos três workstreams pelo `brza note sync`.

## O que a rodada desta sessão fechou

Rodada de 2026-10-30, com as respostas de Anderson:

| Ponto | Resposta |
| :---- | :------- |
| Forma da skill | A sessão também aciona (sem `disable-model-invocation`) |
| Caminhos que travam | Os cinco das notas: `work/`, `plans/`, `wiki/`, `memory/` e `.claude/agent-memory/` |
| Escape quando não há o que registrar | Palavra nas instruções: `/compact sem-fechar` |
| Fora de worktree de workstream | Na `master`, passa; no `brza-studio`, confere o workstream do plano, e a mensagem dá os passos, porque a skill não sobe lá |
| Nome | `/close-task`, refeito em rodada própria depois da correção "os termos utilizados pra nomear agents e skills deve ser em inglês"; o `/fechar` era só nome de trabalho |

O worklog de hoje sai do prefixo de data do nome em `work/worklogs/`, porque o frontmatter do worklog não tem data
(`work/README.md`, seção `work/worklogs/`).

## O que se fez

- **`.claude/hooks/compact_guard.py`:** o modo `pre` roda no `PreCompact` `manual` e barra com `decision: block`, com a
  lista dos arquivos sujos e a falta do worklog. O modo `post` roda no `SessionStart` `compact` e, com nota suja, injeta
  a ordem de atualizar o worklog a partir do resumo. O workstream e o worktree saem do `measure.resolve_workstream`. O
  `sem-fechar` fica num estado em `.measurements/compact_guard.json` por 30 min, para o `post` da mesma sessão não
  insistir.
- **`.claude/skills/close-task/SKILL.md`:** seis passos — situar, o worklog de hoje, o pendente, a memória, o
  `brza note commit`, conferir e devolver.
- **`.claude/settings.json`:** os dois hooks, no padrão `${BRZA_PYTHON:-python3}` e `${BRZA_WORKSPACE:-$CLAUDE_PROJECT_DIR}`
  com `|| true`. Por causa do `|| true`, o bloqueio vai em JSON com saída 0, e não por exit 2.
- **`scripts/summarize_measurements.py`:** a linha `guard` com `kind: compact` sai da tabela da trava de retomada e
  ganha a tabela própria, por workstream e decisão, e a chave `compact_guard` no `--json`.
- **`CLAUDE.md`:** a seção "A trava de fechamento antes do `/compact`" e o `/close-task` na linha da compactação do
  vocabulário.

## O que rodou

- `python3 -m unittest discover -s .claude/hooks/tests`: 73 testes, todos passando, 16 deles da trava nova.
- O `pre` contra o worktree real do `workspace` barrou: 6 arquivos não rastreados em `memory/` e
  `.claude/agent-memory/designer/`, gravados pela sessão do PLN-004. Na `master`, passou.

## O que ficou aberto

- O `/compact` real ainda não foi exercido numa sessão: a primeira compactação manual depois desta confirma que a
  mensagem do `reason` aparece para quem digitou.
- A memória `nome-de-agente-e-skill-em-ingles` diz que a regra é candidata a subir ao `AGENTS.md`. Fica com a sessão
  do PLN-004, dona dela.
