---
scope:
  - workspace
---

# O /compact, o nome em inglês e o arquivo gravado à vista

Numa sessão própria do `workspace` (`workspace-75`), aberta sem plano, Anderson perguntou: "oq o comando /compact do
claude code faz exatamente?" e, em seguida, "conseguimos fazer o compact chamar um script que grava o `Retomar` e `worklog`?".
A conversa deu na trava de fechamento, encomendada a outra sessão, e em três regras de norma.

## O que se levantou

Pela documentação atual dos hooks (`code.claude.com/docs/en/hooks`, via `context7`):
- o `PreCompact` aceita só hook `command`, bloqueia com exit 2 ou `{"decision": "block"}` e, no `manual`, mostra o
  stderr a quem digitou;
- bloquear o `auto` pode fazer o pedido falhar, quando a compactação veio para recuperar um erro de limite;
- o `PostCompact` recebe o `compact_summary`, sem controle de decisão;
- o modelo não roda o `/compact`.

Um `claude -p` no hook, que escrevesse o worklog sozinho, leria 200 mil tokens sem cache: ~US$ 0,80 no Opus 5.5 por
compactação, pela tabela do `.claude/hooks/measure.py`, contra ~US$ 0,04 do resumo com cache quente.

## A rodada da trava

Quatro opções: a skill de fechamento com trava no `PreCompact` `manual`; a mesma, mais um aviso no `SessionStart` depois
da compactação automática; o `claude -p` no hook; só o aviso. Anderson respondeu "siga com a 2". A implementação foi
para a sessão `compact-guard`, aberta pelo `brza sessions` com a resposta literal no prompt, e está em
[A trava de fechamento antes do /compact](2026-10-30-a-trava-de-fechamento-antes-do-compact.md).

O `brza sessions --checkout .worktrees/workspace`, como o `CLAUDE.md` exemplifica, falhou rodado de dentro do worktree:
o caminho relativo virou `.worktrees/workspace/.worktrees/workspace`. Com o caminho absoluto, abriu.

## As três regras que subiram à norma

Vieram como correções de Anderson ao longo da conversa:
- "os termos utilizados pra nomear agents e skills deve ser em inglês" — o `/fechar` de trabalho virou `close-task` na
  outra sessão;
- "sempre que gravar - adicionar|editar - um arquivo de `norma` | `plans/` | `wiki` | `work/`, mostre no
  chat/terminal, igual fez com a memória";
- "markdown renderizado como modo de visualização ao expandir" e "adicione um separador --- entre os arquivos".

Dois arquivos de exemplo, no scratch do chat, mostraram o formato; Anderson: "está bom assim". O rascunho das três
regras foi à rodada de aprovação na mensagem, e Anderson respondeu "1" (aprovar como estão). Entraram no `AGENTS.md`,
na `master`, em `2d3f0f6`, e chegaram aos três workstreams pelo `brza note sync`. As duas memórias que as guardavam
saíram de `memory/`.

## A memória neste commit

Vão juntas as memórias que a sessão do PLN-004 (`workspace`) deixou sem commit e que a trava barrava: `memory/rodada-do-desenho-vai-no-chat.md`
e, no `designer`, `feedback_mecanismo-nativo-do-runtime.md` e `feedback_medir-antes-de-desenhar.md`, com os índices.
