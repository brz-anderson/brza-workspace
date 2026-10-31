---
name: project-pln-006-rodadas-e-sondas
description: PLN-006 (brza init): o que Anderson aceitou e recusou nas R1–R6, o critério provável, e a premissa de custo que errei (o hook no Python 3.9)
metadata:
  type: project
---

Nas R1–R3 do PLN-006 (2026-10-31) Anderson escolheu a recomendada nas 11 perguntas. Na R4, recusou duas:
- **R4.1:** o `git config --local brza.workspace` (recomendado, ~0,5 h, "se paga já") perdeu para "Registro em
  ~/.config/brza", que eu tinha escrito como "se paga só com código servindo a mais de um workspace". Ele não disse o
  porquê; a leitura provável é o arquivo de configuração visível e próprio da ferramenta, que vai ao worklog, contra o
  dado escondido no `.git/config` de outro repositório.
- **R4.3:** o `plans/LAST_PLN` virou, em texto livre, um índice JSONL na `master` "para o coordenador ter um índice";
  ele aceitou abrir exceção à regra "a master guarda só a norma" para ter visão entre os workstreams.
As R5 e R6 saíram todas na recomendada.

**Why:** com custo e "se paga" escritos, ele não reabre; quando troca, troca por visibilidade (arquivo explícito,
índice comum), não por custo menor.

**How to apply:** ao recomendar, pese "o estado fica visível e com procedência" acima de economia de meia hora; quando
a solução esconde estado num lugar implícito, ofereça a alternativa explícita com custo honesto. Ver
[[feedback-mecanismo-nativo-do-runtime]].

**Custo que errei:** justifiquei o parser TOML próprio com "o hook roda no 3.9 sem tomllib". A sonda mostrou que o hook
*sobe* no 3.9 (176 testes OK no `/usr/bin/python3`), mas as sessões vivas rodam no 3.14 do PATH (`ps eww` dos pids do
`claude`). Antes de usar "roda no Python X" como argumento, confira o PATH das sessões vivas, e não só o
`/usr/bin/python3`. Armadilha correlata: o `CLAUDE.md` lê o `AGENTS.md` junto só pela opção no
`~/.claude/settings.json` de usuário. Outra: `merge=union` deixa as linhas fora de ordem; "a última linha" de um log só
acrescentado vira "a de maior ts". Ver também [[feedback-medir-antes-de-desenhar]].
