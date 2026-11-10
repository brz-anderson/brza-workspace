---
status: done
description: Revisão adversária da entrega de P1 a P7 do PLN-021: 12 achados importantes, 6 sugestões e 5 hipóteses que caíram.
scope:
  - workspace
opened: 2026-11-10
completed: 2026-11-10
tags:
  - tooling
  - planning
refs:
  - PLN-021
---

# REV-026: PLN-021 P1 a P7, a entrega do plan-runner coordenado e da screen-artboards

Revisor: `reviewer` (subagente), 2026-11-10, ~00:45 BRT. Alvo: o worktree `playground` em HEAD `21dd29e` mais o diff sem
commit do ajuste R4.6.2 (artboard.py às 00:36, plano às 00:32). Isolado, sem corrigir nada.

Contagem: **12 importantes, 6 sugestões, 5 falsos.**

## Achados

### A1 — O roster padrão da R4.3 não abre o Codex: `--effort xhigh` sem `--model`, e o `brza` recusa

> bug · importante · confiança 95 · → corrigido aqui (P11)

**Evidência:** `consult.py:50` põe o Codex com `"model": None, "effort": "xhigh"`, e `sessions_cli.open_argv`
(`sessions_cli.py:46-50`) acrescenta `--effort` sem `--model`. `consult.py open PLN-021 D4 --brief … --dry-run` imprime
`brza sessions pln021-d4-mudanca-minima --agent codex … --wait --effort xhigh --rename`. O mesmo argv no `brza` real:
`brza sessions zz-review-probe --agent codex --effort xhigh --prompt x --dry-run` → `CHECK: --effort exige --model; nada
foi aberto`, rc 1. Com `--model`, o mesmo comando "abriria". O cenário: o `open` abre o Claude, cai no Codex com
`falha`, diz "paro aqui" e devolve 1; o Grok nunca abre. Os 16 testes passam porque o `brza` é falso. O mesmo vale para
`executor.py open --agent codex --effort …` sem `--model`. A X4 já dizia que o `xhigh` "não foi conferido no `brza
sessions` real".

### A2 — O corte por cota nunca acontece: o `cotas()` lê um JSON que o `brza quota` não produz

> bug · importante · confiança 95 · → corrigido aqui (P11)

**Evidência:** `consult.py:86-98` espera `{runtime: {session_pct: N}}`. O `brza quota --json` real devolve
`{"accounts": [{"runtime": "claude", "windows": [{"name": "session", "used": 18}, …]}, …]}`, sem `session_pct`. O
`python3 -I -c '…consult.cotas()'` → `{}`, e o `open --dry-run` imprime `⚠ não li o brza quota --json: nenhum runtime
foi cortado por cota`. A fixture `test_consult.py:20` inventa a forma que o parser lê: é o molde × parser. A regra "acima
de 55% não entra" (`consultants.md:52-53`, a R4.3) fica sem efeito. Há ainda conta duplicada por runtime (dois `claude`)
e o Grok só tem janela `weekly`.

### A3 — O `wait` gira sem pausa quando o `brza sessions wait` sai com rc 1 e erro, e imprime uma linha por volta

> bug · importante · confiança 92 · → corrigido aqui (P11)

**Evidência:** `executor.py:406` só aborta com erro quando `rc not in (0, 1, 75)`. Com rc 1, o laço segue, e as linhas
`:441-444` só dormem com `sem_fim` ou `timed_out`/rc 75. O `brza` real, para uma sessão que não existe mais, faz
`brza sessions wait zz-inexistente-revisor --any --timeout 2 --json` → `{"error": "0 chats abertos se chamam …"}`, rc 1,
em 0,28 s. A sonda com o `wait` falso devolvendo `(1, {"error": …})` e `--timeout 600` fez 100 chamadas e 100 linhas
"em curso". No relógio real são ~6.400 processos `brza` e as mesmas linhas em 1.800 s. O cenário: a sessão foi fechada ou
o chat foi fechado à mão. A `consult.py:291,314-315` repete o padrão, na leitura.

### A4 — Reabrir um passo `parado` devolve na hora o marcador velho; reabrir um `feito` apaga a evidência do manifesto

> bug · importante · confiança 95 · → corrigido aqui (P11)

**Evidência:** `executor.py:230` só recusa `VIVOS` (`aberto`, `em-curso`, `bloqueado`, `:60`). A mensagem e o docstring
dizem "só reabre fechado, parado ou falhado", mas o código também reabre `feito` e `evidencia-gravada`. O
`cria_worklog` (`:194-196`) não toca o worklog que já existe, e o `wait` lê o marcador antes de chamar o `brza`
(`:387-393`). Nas sondas com o harness `_exec.py`:

- **`parado` → `open` → `wait`:** rc 0, `P1 · parado em 0 min`, 0 chamadas ao `brza sessions wait`. A espera não
  esperou o executor novo.
- **`evidencia-gravada` → `open`:** rc 0, o manifesto volta a `estado: aberto` com `evidencia: None`.

O caminho documentado (parado → rodada → reabrir) quebra.

### A5 — O pedido do passo proíbe commit no `brza-workspace` e, no checkout padrão, autoriza o commit na branch dele

> bug · importante · confiança 95 · → corrigido aqui (P11)

**Evidência:** sem `--tree` e sem `--checkout`, o `executor.py:257-258` usa `checkout = pl.raiz` e a branch atual do
workspace. O pedido gerado (sonda com `git init -b workstream/x`) traz duas regras que se contradizem:

- "Não grave o plano, não commite nada no brza-workspace" (`step_request.py:166`);
- "O pedido autoriza o commit na branch `workstream/x` do checkout" (`:169-170`).

Com `--checkout` sem `--branch`, a branch autorizada é a atual do checkout (`:256`), por exemplo a `master` do
`brza-studio`, e não "a branch do passo" da R4.1. O `step_request.py` à mão tem outro padrão (o `brza-studio/.worktrees`,
`:126-129`), e por isso o pedido lido antes de abrir não é o que o `open` envia. A X4 registrou o conflito e disse que ia
à R4; não foi (ver A9).

### A6 — O Desenho não foi reescrito com a R5, e o pedido do executor copia "Em aberto" que já fechou

> desvio · importante · confiança 95 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:** a `Origem` de D3 é `R1.3(a)` (`design.md:276`), a de D4 é `R1.3(b), R2.3` (`:409`) e a de D7 é
`R1.4, R2.4` (`:568`). Nenhum `D` cita a R4 nem a R5. Seguem como estavam:

- D3 "Em aberto: o commit do executor: ponto 1 da rodada" (`:401-403`) e o molde "`<o commit: pela resposta ao ponto 1>`"
  (`:370`);
- D4 "ponto 3/ponto 4 da rodada" (`:435-440`);
- D2 "ver o ponto 7" (`:270`);
- "Escolhas menores sem lastro" (`:706-713`).

`step_request.py PLN-021 P3 --out …` gera um pedido com "#### Em aberto — O commit do executor: ponto 1 da rodada" e
"`<o commit: pela resposta ao ponto 1 da rodada>`" junto da regra que autoriza o commit. O pedido do P7 não traz a
R4.6.2 em "O que as rodadas decidiram". Isso viola a regra da própria skill: "o `D` passa a declarar a origem nova"
(`SKILL.md:161`). O `close_check.py PLN-021` item 3 lista sete R5.x "decididos sem D".

### A7 — O P3 está `[x]` sem a sonda de permissão que o título e o D3 prometem, e sem desvio nem destino

> lacuna · importante · confiança 92 · → corrigido aqui (X7 no P3; a sonda roda no P9)

**Evidência:** o título do P3 diz "e a sonda de permissão" (`plan.md:355`). O D3 diz "A sonda é o primeiro subpasso do
P3" e a chama de "o ataque à A1 que ficou de pé": o executor do `brza-studio` grava o worklog fora do checkout e pode
travar em `blocked` (`design.md:396-399`). O P3 tem um subpasso só, `executor.py` (`plan.md:361`), e a Evidência admite
"a sonda de permissão de gravar fora do checkout não rodou" (`:367`). Nenhum `X` a cita, e o P9 não a nomeia.

### A8 — A Evidência do P7 é anterior ao ajuste R4.6.2 de hoje, que está sem commit e sem registro

> desvio · importante · confiança 95 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:** o P7 diz "→ 48 OK · 14 PNGs … `/v2/png/`" (`plan.md:417-420`), e 48 é a conta de HEAD (31 + 17
`def test`). No disco são 55 (`unittest discover` → 55 OK). O `artboard.py` mudou às 00:36, depois do plano (00:32). Os
PNGs do desktop vivo estão em `v3/png/` (00:36). O diff de `artboard.py`, `test_artboard.py`, `SKILL.md`, `frames.md` e
`chat-rules.md` está sem commit, e nenhuma linha do P7, do X1 ou do X5 cita a R4.6.2. O `evals.json` caso 1 ainda espera
"os tokens do brza-studio escopados no mockup", e os evals (+0,08) são de antes do caminho vivo.

### A9 — Os desvios X3 e X4 mandaram pontos à R4 que nenhuma rodada levou; X2 a X5 mudam um `D` sem rodada nem reescrita

> desvio · importante · confiança 90 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:**

- **X3** diz "a classificação aviso × erro vai à R4", e **X4** diz "os fallbacks e o checkout padrão vão à R4"
  (`plan.md:459-467`). A R4 (`:212-256`) e a R5 (`:264-321`) não têm nenhum desses pontos.
- **X4** contradiz o D3 sem reescrevê-lo. O D3 diz "marca `[x]` nos subpassos que a evidência cobre"
  (`design.md:334-335`); o `executor.py:605-608` marca todos, e a `conduct.md:78-79` documenta isso.
- **A regra violada:** "Desvio que muda um `D` vira rodada antes de seguir" (`conduct.md:43`).

### A10 — O `close_check` e o painel só contam "Decidido"; a pergunta respondida por `Resposta:` some, e a R5.6 mudou código

> bug · importante · confiança 90 · → corrigido aqui (P11)

**Evidência:** `plan_md.py:260-261` (`decidida` = tem linha `**Decidido**`), `close_check.py:166` e `plan_panel.py:156`
usam só isso. O `close_check.py PLN-021` lista R5.1–R5.5, R5.7 e R5.8, e não a R5.6 nem a R5.9. O painel renderizado
mostra "R5 — 9 perguntas, 7 decididas". O `round_log.py` grava `**Resposta:** "…" Lida como: …` sempre que há `literal`
(`round_log.py:161-166`), e por isso toda resposta em texto livre fica fora do item 3. Premissa: a resposta com "Lida
como" é decisão. A norma trata o texto livre como contraproposta, mas aqui a leitura nomeia a opção escolhida.

### A11 — O `evidence` roda o comando escrito pelo executor, com shell, já na proposta, antes de a coordenação ler

> bug · importante · confiança 88 · → corrigido aqui (P11)

**Evidência:** `confere()` roda todo `comando:` com `(≤ 2 min)` por `run_shell(cmd, checkout)` com `shell=True`
(`executor.py:84-92, 516-520`), e é chamado em `cmd_evidence:651`, antes do teste de `--apply` (`:668`). A sonda, com o
worklog dizendo ``comando: `git push --force` → ok (≤ 2 min)``, rodou `['git push --force']` sem `--apply`. O D3 fala em
"comando de teste" (`design.md:331`), e a `conduct.md:74` manda "leia a proposta antes de aplicar", mas a proposta só sai
depois de o comando rodar. Premissa: o worklog é entrada de outra sessão, possivelmente de outro runtime, e não é
confiável.

### A12 — Os evals saíram com 3 e 2 casos, contra 5 e 3 do Desenho, sem desvio

> desvio · importante · confiança 92 · → descartado: o delta de +0,44 já discrimina e a memória skill-evals-need-rules-the-repo-lacks diz que expectativa sem regra nova só empata (R6.3)

**Evidência:** `design.md:684-690` lista cinco casos do `plan-runner`; o `evals.json` tem três (retomar, executar,
consultores). Faltam o 4 ("3 alternativas baratas → `Agent`, não abre sessão"), o caso negativo do gatilho R2.3 que
segura a cota, e o 5 (`round_log` com `reabre`). `design.md:695-701` lista três casos da `screen-artboards`; há dois,
sem o 3 (deriva com fixture). O `benchmark.json` tem 1 execução por configuração, e o cabeçalho do `benchmark.md` diz
"3 runs each". Nenhum `X` registra o corte.

### A13 — O `open --tree` cria o worktree antes de conferir o pedido, e a recusa deixa um worktree órfão

> bug · sugestão · confiança 95 · → corrigido aqui (P11)

**Evidência:** `executor.py:240-253` roda `brza tree` antes de `step_request.monta` (`:263-267`). A sonda com o passo
`Executa D9` (que o Desenho não tem) e o `brza tree` falso devolvendo um caminho que existe deu `rc 1`, `recusado: o passo
P1 executa D9…`, com a chamada `('brza', ['tree', 'pln-900-p1', '--type', 'feat'])` já feita. Premissa para o efeito
seguinte: o `open --tree` com o mesmo nome, depois de corrigir o plano, esbarra no worktree que já existe.

### A14 — No PNG do desktop vivo, o `:root` de reserva do pacote vence o token que o `brza shot` já injeta

> bug · sugestão · confiança 85 · → corrigido aqui (P11)

**Evidência:** o `brza shot` injeta os tokens do chat. Um HTML com `var(--background, red)` sai branco no claro e
`(22,22,22)` no escuro. Com `<style>:root{--background:#ff00ff}</style>` no `<head>`, o mesmo shot escuro sai
`(255,0,255)`: o estilo do artboard vence. O `artboard.py:302-352` (`_variante`, `_fallback`, `cmd_shot`) põe esse
`:root` com o `.dark` do pacote (`background #0a0a0a`), e por isso o PNG conferido mostra o pacote, e não o tema que o
`brza shot` emula. A `chat-rules.md:28` dá o fallback como necessário, o que não confere. Premissa: o render do `brza
shot` é a referência do chat.

### A15 — Com o turno encerrado sem o marcador, o `wait` imprime "em curso" a cada ~5 s, e não a cada ~3 min

> bug · sugestão · confiança 85 · → corrigido aqui (P11)

**Evidência:** `executor.py:441-448` dorme 5 s com `sem_fim` e imprime a linha de batida em toda volta; a
`consult.py:312-317` faz o mesmo. A sonda com o `done` sempre `ended_without_marker` deu 54 linhas "em curso" em 600 s
de relógio falso, que avança 1 s por leitura. A `narration.md:16` promete "a cada ~3 min sem evento". Premissa: o `brza
sessions wait` volta na hora com a sessão ociosa, o que o comentário do código afirma (`:442`).

### A16 — A R5 respondida não chegou ao estado do plano nem às skills, que seguem "a confirmar"

> desvio · sugestão · confiança 95 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:**

- **No plano:**
  - `ready: "não — a R4 está sem resposta…"` (`plan.md:6`), que o `plan_state.py` e o painel repetem;
  - o `Retomar` "Anderson responde a R4" (`:22`);
  - "(R4.8 a confirmar)" e "com as recomendadas da R4" (`:325-326`);
  - a R4 sem linha que aponte para a R5 (`:208-210`).
- **Nas skills, "recomendada, a confirmar":**
  - `step-request.md:61`;
  - `consultants.md:51`;
  - `consult.py:17`;
  - `screen-artboards/SKILL.md:71`;
  - `references/tokens.md:23`;
  - `narration.md:20` ("R4.4 recomendada").

### A17 — `review.md` repete o parágrafo de abertura

> convenção · sugestão · confiança 98 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:** `references/review.md:3-4` e `:7` dizem o mesmo ("Com todo passo `[x]` ou `[-]`…: `phase: review`,
`status: in_review`"), com duas linhas em branco entre eles.

### A18 — A R5 saiu com o "(seleção múltipla)" duplicado e a sessão como UUID solto

> convenção · sugestão · confiança 95 · → corrigido aqui (pela coordenação, R6.2)

**Evidência:** `plan.md:313` "**R4.9 — As escolhas menores (seleção múltipla)** (seleção múltipla)": o `tema` já trazia
o sufixo, e o `round_log.py:142` o acrescenta de novo. Em `:262` está "Respondida em 2026-11-10,
273fc24b-adde-…", sem "na sessão…", porque o `_sessao` (`:118-122`) só reescreve o texto que começa por "sessão". As
linhas da R5 também saíram sem quebra, com mais de 300 caracteres.

### A19 — As contagens de teste da Evidência de P3 a P5 não batem

> lacuna · importante · confiança 95 · → falso

**Por que é falso:** as contagens refeitas por arquivo batem com o que o plano diz.

**Evidência:** `-p test_executor.py` → 39 OK; `-p test_plan_panel.py` → 12 OK; `-p test_consult.py` → 16 OK; a suíte
do `plan-runner` → 151 OK; `plan_state.py PLN-017` → rc 1, com os 2 erros citados (P7 sem evidência que se refaça;
`executed_h` 9.516 × 7.974).

### A20 — Os testes novos do R4.6.2 passariam sem o código novo

> lacuna · importante · confiança 95 · → falso

**Por que é falso:** com o `artboard.py` de HEAD, cinco dos testes novos falham.

**Evidência:** numa cópia em scratch com o `artboard.py` de `21dd29e`, a mesma suíte deu `FAILED (failures=2,
errors=3)`, em `test_desktop_do_brza_studio_usa_os_tokens_vivos_sem_escopo_de_pacote`,
`test_scheme_explicito_no_desktop_do_brza_studio_sai_2`, `test_shot_desktop_do_brza_studio_*` e
`test_promote_desktop_do_brza_studio_com_tema`.

### A21 — O caminho vivo põe tokens no `:root` do artboard publicado

> bug · importante · confiança 95 · → falso

**Por que é falso:** o `:root` de reserva só entra no HTML temporário do PNG.

**Evidência:** `grep -c ':root'` dá 0 em `v3/d-macos-macos-092c.html` e `d-windows-windows-06b0.html`, e 1 só em
`v3/png/_variantes/*.html`.

### A22 — A master já recebeu o `plan-runner` novo (R3.1 quebrada)

> desvio · importante · confiança 95 · → falso

**Por que é falso:** a master segue com a v1.

**Evidência:** `git show master:.claude/skills/plan-runner/SKILL.md | grep -c executor.py` → 0; `git diff master
workstream/playground --stat -- .claude/skills/plan-runner` → 38 arquivos, só no playground.

### A23 — Os commits citados não existem

> lacuna · importante · confiança 98 · → falso

**Por que é falso:** os dois commits existem.

**Evidência:** `git cat-file -e 21dd29e` e `git cat-file -e 1a23a6c` → ok.

## Pontos para rodada

Respondidos na Rodada 6 do plano, todos na primeira opção: o ajuste R4.6.2 entra no X1 e na Evidência do P7; o navegador
com `--pack brza-studio` segue o pacote; o `Executado` de P6 e P7 se mede pelo `--by-task` no P10.

## O que rodou e o que deu

- `python3 -I -m unittest discover -s .claude/scripts/tests` → 55 OK; `-s .claude/skills/plan-runner/scripts/tests` →
  151 OK; `-s .claude/skills/screen-artboards/scripts/tests` → 55 OK; `-s .claude/skills/meeting-runner/scripts/tests`
  → 323 OK.
- `plan_state.py PLN-021` → rc 0, "problemas: nenhum", com o `ready` velho; `plan_state.py PLN-017` → rc 1, os 2 erros.
- `check_notes.py` → 0 erros, 2 avisos `unknown-ref-mention`, rc 0.
- `close_check.py PLN-021` → rc 1: P8 a P10 pendentes, e o item 3 sem a R5.6 nem a R5.9.
- `step_request.py PLN-021 P3|P7 --out <scratch>` → rc 0; o "Em aberto" velho e a R4.6.2 ausente.
- `plan_panel.py render PLN-021 --out <scratch>` → "R5 — 9 perguntas, 7 decididas".
- `consult.py open PLN-021 D4 --dry-run` → o argv do Codex sem `--model`, e o aviso de cota.
- No `brza` real, só leitura e `--dry-run`:
  - `brza sessions … --effort xhigh --dry-run` → rc 1, "--effort exige --model";
  - `brza sessions wait <nome inexistente>` → rc 1 com `error`;
  - `brza quota --json` → a forma `accounts[].windows[]`;
  - `brza shot`, nos três HTML de sonda do scratch.
- Sondas com o harness `_exec.py`, num scratch fora do repositório: o `parado`/`feito` reaberto, o rc 1 do `wait`, o
  `--tree` antes da recusa, o comando rodado na proposta, o checkout padrão e a batida.
- `git cat-file -e` de `21dd29e` e `1a23a6c` → ok.
- Nada foi gravado no repositório; o `consult.py --dry-run` não criou `.sessions/pln-021`.
