---
status: in_progress
phase: execution
origin: request
description: Protótipo no playground de um plan-runner com sessão coordenadora (executores dos passos, consultores em sessões, painel de andamento), scripts e references como os da meeting-runner, e uma skill própria de artboards para protótipos de tela web, mobile e desktop.
ready: "sim — o P13 (X11, X12 e os cartões) espera o pedido de Anderson"
estimate_h: 49.75
executed_h: 1.451
remaining_h: 2.5
priority: medium
scope:
  - workspace
opened: 2026-11-09
owner: Anderson
tags:
  - tooling
  - planning
---

# PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela

- **Retomar:** a R10 (2026-11-12) deu "passa" ao C1–C4, escolheu os cartões (B) e mandou o X11 e o X12 ao P13; o P12 entrou na master do `brza-studio` (`c470dda`), e o P14 provou o X7 pelo `Write`. O P9 fechou. Próximo: o P13, a pedido de Anderson; depois o P10.
- **Dividido:** [PLN-021 — Desenho](PLN-021-design.md)

## Pedido

- **Origem:** pedido livre, na sessão do workstream `playground` de 2026-11-09.

"adaptar a skill `plan-runner` para ficar mais parecido com a `meeting-runner`, com uma sessão coordenadora, com mais
scripts de apoio e referencias;

adicionar também a `plan-runner` - pode sugerir outra skill, se necessário - uma rotina para criação de artboards, para
protótipos de tela, tanto web quanto mobile e desktop;"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 1` (sessão coordenadora) · R1.3 | A coordenação abre a sessão executora de um passo pelo `brza sessions`, envia o pedido do passo, espera o status e traz a evidência ao plano, sem comando digitado por Anderson | P3 | os `unittest` de `executor.py` (unidade); C1 (manual) |
| `Pedido 1` · R1.3 · R2.3 | Na bifurcação com 3 ou mais alternativas e escolha cara de reverter, ou a pedido, os consultores do Desenho abrem como sessões em modelos e runtimes diferentes, e as alternativas voltam lado a lado; no resto, o `Agent` | P5 | os `unittest` de `consult.py`, inclusive a tabela lado a lado (unidade) |
| `Pedido 1` · R1.3 | O painel de andamento do plano (passos, fase, horas, executores) sai de script, como `::orca-visual`, a cada mudança de estado | P4 | os `unittest` do painel (unidade); C2 (manual) |
| `Pedido 2` (scripts de apoio e references) | As operações mecânicas do plano saem de script, e cada operação tem a reference dela, como na `meeting-runner` | P2, P6 | os `unittest` de `plan_state.py`, `step_request.py`, `round_log.py`, `close_check.py` e `plan_md.py` (unidade); a `SKILL.md` e as references conferidas no P6 |
| `Pedido 3` (artboards) · R1.4 · R2.4 | A `screen-artboards` gera o artboard de tela em web, mobile e desktop, com o pacote de tokens do projeto e a moldura do aparelho, confere pelo PNG em cada largura, e o Desenho do plano a aciona | P7 | os `unittest` da `screen-artboards` (unidade); C3 (manual) |
| R2.4 (tokens) | O pacote do `brza-studio` sai por script do `main.css` e do `mobile-theme.ts`, e o script avisa a deriva; o pacote neutro cobre o projeto sem tokens | P7 | os `unittest` da extração (unidade) |
| R3.1 (protótipo com o nome) | O `plan-runner` novo vive só na branch do playground, com o mesmo nome; a master segue com o do core | P6 | C4 (manual): `git diff master workstream/playground --stat -- .claude/skills/plan-runner` só no playground, e `git status` limpo na master depois do `brza sync` |
| R2.2 (os scripts) | `plan_state.py`, `step_request.py`, `round_log.py` e `close_check.py` existem, com testes, e a skill manda usá-los no lugar da conferência à mão | P2 | os `unittest` de cada script (unidade) |
| R3.2 · R3.3 (código comum) | `.claude/scripts/` guarda o mapa de sessões, os verbos do `brza sessions`, a medição por janela e o salvar visual com PNG pelo `brza shot`; a `meeting-runner` importa de lá | P1 | os 323 testes da `meeting-runner` e os de `.claude/scripts/` (unidade) |

### Fora de escopo

- **A promoção ao `core/` do `brza-workflow`.** Vem depois de o protótipo conduzir planos reais sem desvio de fluxo, como
  na `meeting-runner` (PLN-017/R2.1); o critério de promoção é da rodada que o fixar.

## Restrições

- **O `plan-runner` muda só na branch `workstream/playground`** (R3.1). A master e os outros workstreams seguem com o do
  core até a promoção; o conflito do `brza note sync`, quando o core mudar a skill, se resolve à mão, guardando a versão
  do playground.
- **O código comum mora em `.claude/scripts/`, também só nesta branch** (R3.2), fora do `.brza/core.lock`.
- **Toda skill deste plano se cria e se revisa pela `skill-creator`**, pela memória do workstream de 2026-11-08.

## Entrevista

### Rodada 1 — destino, onde mora, o que coordena, onde moram os artboards (enviada 2026-11-09)

> **Apresentado antes:** o `plan-runner` está no `.brza/core.lock:24-28`, e editá-lo aqui trava o `brza sync`; a
> `meeting-runner` nasceu como protótipo no playground pelo mesmo motivo (PLN-017/R2.1). O pedido tem lacuna de desenho
> e não fecha numa sessão (Passo 1 do `plan-runner`). Hoje o passo de código "roda numa sessão nova aberta no
> `brza-studio`", com o pedido em arquivo, sem quem a abra, a acompanhe ou leia a evidência de volta
> (`references/conduct.md`, "Executar um passo"). O artboard é uma linha do Desenho (`references/open-and-plan.md`,
> passo 3), com o `brza shot --width` (padrão 736) e sem molde de tela nem moldura de aparelho.

Respondida em 2026-11-09, na sessão do workstream `playground`.

1. **Destino.** Opções:
   - PLN novo no playground (recomendada) — custo: ~15 min de abertura agora, e cada rodada vira texto no plano; se paga:
     já na 2ª sessão, porque o trabalho tem pelo menos três frentes e não fecha hoje;
   - worklog de hoje — custo: zero agora, e a promoção a PLN (~20 min) quando atravessar a sessão; se paga: só se tudo
     fechar hoje.

   **Decidido — PLN novo no playground.**

2. **Onde o novo `plan-runner` é escrito.** Opções:
   - protótipo no playground (recomendada), skill nova com nome de trabalho `plan-coordinator`, fora do `core.lock`, com
     o `plan-runner` do core intacto até a promoção — custo: dois fluxos de plano convivendo, e o novo só por
     `/plan-coordinator` durante o protótipo; se paga: na promoção, que leva ao core uma versão testada em planos reais;
   - direto no core do `brza-workflow`, por uma sessão do `tools-kit` — custo: cada iteração é commit no
     `brza-workflow` mais sync, e o erro chega a todos os workspaces; se paga: logo, se o desenho sair estável, o que é
     improvável no primeiro corte;
   - editar aqui mesmo — custo: trava o próximo `brza sync` e cria divergência a resolver à mão; se paga: nunca, salvo
     como rascunho descartável.

   **Decidido — protótipo no playground.** **→ reaberta em R3.1:** o nome continua `plan-runner` (R2.1).

3. **O que a sessão coordenadora abre e acompanha** (seleção múltipla). Opções:
   - sessões executoras dos passos (recomendada) — custo: dois scripts (abrir e enviar; esperar) mais o molde do pedido,
     ~1 sessão de trabalho; se paga: no primeiro plano com 2 ou mais passos de código;
   - consultores do Desenho em sessões, em modelos e runtimes diferentes, no lugar do `Agent` — custo: tempo de abertura
     e cota de outros runtimes a cada bifurcação; se paga: só quando a diversidade de modelo muda a recomendação;
   - painel de andamento do plano, `::orca-visual` gerado por script a cada mudança de estado — custo: um script de
     painel mais testes, ~meia sessão; se paga: com 2 ou mais executores em paralelo.

   **Decidido — as três.**

4. **Onde mora a rotina de artboards.** Opções:
   - skill própria (recomendada), nome de trabalho `screen-artboards`, com moldes por plataforma, moldura de aparelho,
     pontos de quebra e um script que gera o esqueleto e tira o PNG por largura; o Desenho do plano a aciona — custo: uma
     skill a mais para manter e avaliar; se paga: no primeiro uso fora de plano (issue, decisão, reunião);
   - dentro do `plan-runner`, numa reference e num script — custo: a skill de plano cresce, e quem quer só um protótipo
     de tela aciona o fluxo de plano; se paga: só se todo protótipo nascer dentro de plano.

   **Decidido — skill própria.**

### Rodada 2 — o código comum, os scripts, os consultores, os tokens (enviada 2026-11-09)

> **Apresentado antes:** o Terreno do `collector`. O `sessions_map.py` da `meeting-runner` é genérico; abrir, enviar e
> esperar (`launch_persona.py:140-185`, `wait_round.py:179-196`), a medição por janela (`tally.py:459-531`) e o
> `salva_visual` (`panel.py:519`) também, mas misturados ao manifesto de reunião; os 323 testes dela passam em 10 s. O PNG
> dela sai do Chrome (`panel.py:496`); o `brza shot` voltou a funcionar. O `check_notes.py` não confere soma de horas,
> IDs, `[x]` com evidência nem a origem do `D` (`check_notes.py:56`, `:495`). Não há molde de tela nem moldura; os
> tokens do `brza-studio` estão em `src/renderer/src/assets/main.css:194` e `mobile/src/theme/mobile-theme.ts:5-202`.
> Os evals seguem o P1 do PLN-017 (`PLN-017-plan.md:306-315`) e a memória `skill-evals-need-rules-the-repo-lacks`.

Respondida em 2026-11-09, na sessão do workstream `playground`.

1. **Onde mora o código comum.** Opções:
   - pasta `.claude/skills/_shared/`, a `meeting-runner` importando dela, e o PNG pelo `brza shot` (recomendada) —
     custo: ~2–3 h, mais os 323 testes de novo; se paga: no primeiro script do `plan-coordinator` e na
     `screen-artboards`;
   - copiar para a skill nova — custo: ~0,5 h, e duas cópias que envelhecem; se paga: só com protótipo descartável;
   - importar da `meeting-runner` — custo: ~0,3 h, e o acoplamento; se paga: nunca como estado final.

   **Resposta:** "pasta script/ em .claude/; e não é pra mudar o nome da skill, continua sendo `plan-runner`". Lida
   como contraproposta em dois pontos: a pasta vai a `.claude/` e o nome reabre a R1.2. Foi à rodada 3.

2. **Os scripts de apoio** (seleção múltipla). Opções:
   - `plan_state.py`, estado e conferência: próximo passo, `[x]` sem evidência, horas contra o frontmatter (`--fix`
     reescreve), IDs e origens (recomendada) — custo: ~4–6 h; se paga: no primeiro Retomar;
   - `step_request.py`, o pedido do passo a partir do `P`, dos `D` e das rodadas citadas — custo: ~2 h; se paga: no
     primeiro passo de código;
   - `round_log.py`, a rodada em JSON acrescentada à Entrevista com o próximo `R` — custo: ~2–3 h; se paga: a partir da
     3ª rodada de um plano;
   - `close_check.py`, os seis itens do `close.md` — custo: ~2 h; se paga: no primeiro fechamento.

   **Decidido — os quatro.**

3. **Quando os consultores abrem como sessões.** Opções:
   - só em decisão cara (recomendada): 3 ou mais alternativas e escolha cara de reverter (contrato, formato de dado,
     norma), ou a pedido; no resto, o `Agent` — custo: abertura e cota de outro runtime só nesses casos; se paga: quando
     a diversidade de modelo muda a recomendação numa decisão que custaria refazer;
   - toda bifurcação com 3 ou mais — custo: cota e espera também nas baratas; se paga: não medido;
   - só a pedido — custo: zero de cota; se paga: agora, mas o recurso pode ficar sem uso.

   **Decidido — só em decisão cara.**

4. **Os tokens e as molduras dos artboards.** Opções:
   - pacote por projeto (recomendada): o do `brza-studio` (desktop do `main.css`, mobile do `mobile-theme.ts`),
     extraído por script que avisa a deriva, mais um neutro; molduras CSS de janela macOS e Windows, iPhone e Android, e
     navegador em 375, 768 e 1280 — custo: ~5–7 h; se paga: no primeiro protótipo do `brza-studio`, e a cada projeto
     novo, que só acrescenta um pacote;
   - só o `brza-studio`, fixo — custo: ~4 h; se paga: só com protótipos do `brza-studio`;
   - neutro — custo: ~3 h; se paga: só para wireframe.

   **Decidido — pacote por projeto.**

### Rodada 3 — o nome, a pasta comum, a `meeting-runner` (enviada 2026-11-09)

> **Apresentado antes:** o `brza sync` lê o disco da raiz, a master (`brza-workflow/bin/brza-sync:8-13`); editar o
> `plan-runner` só na branch do playground não o trava, mas o `brza note sync` pode dar conflito de merge quando o core
> mudar a skill — o core a mudou três vezes, em 2 e 3/11, e nenhuma desde então. Não há `.claude/scripts/` nem
> `.claude/script/`.

Respondida em 2026-11-09, na sessão do workstream `playground`.

1. **Mantido o nome `plan-runner`, onde ele é editado** (reabre a R1.2). Opções:
   - na branch do playground (recomendada) — custo: conflito de merge no `brza note sync` quando o core mudar a skill, e
     toda sessão do playground já na versão nova durante o protótipo; se paga: no primeiro plano do playground, e a
     promoção copia a pasta ao `core/`;
   - direto no core do `brza-workflow` — custo: commit e sync a cada iteração, e o erro chega a todos; se paga: só com
     o desenho estável.

   **Decidido — na branch do playground, com o nome `plan-runner`.**

2. **A pasta dos scripts comuns.** Opções:
   - `.claude/scripts/` no playground (recomendada), fora do `core.lock` — custo: nada agora; vai junto na promoção; se
     paga: agora;
   - `.claude/script/`, no singular — custo: destoa do `scripts/` das skills; se paga: só se o singular for proposital;
   - `.claude/scripts/` na master — custo: código só do playground indo a todo worktree; se paga: quando outra skill
     fora do playground o importar.

   **Decidido — `.claude/scripts/` no playground.**

3. **A `meeting-runner` importa de `.claude/scripts/` neste plano.** Opções:
   - sim, neste plano (recomendada): o mapa de sessões, os verbos, a medição e o salvar visual com PNG pelo `brza shot`,
     com os 323 testes de novo — custo: ~2–3 h; se paga: na primeira mudança do `brza sessions` v2, corrigida num lugar
     só;
   - só as skills novas — custo: ~0,5 h, e duas cópias até uma issue fechar; se paga: só com reunião em curso que não
     pode ser mexida.

   **Decidido — sim, neste plano.**

### Rodada 4 — o executor, os consultores, os artboards, o corte (enviada 2026-11-09)

> **Apresentado antes:** o rascunho do Desenho do `designer`, em [PLN-021 — Desenho](PLN-021-design.md), com os itens
> D1 a D7, os evals e a proposta de passos (41 h). Os oito pontos abaixo são os dele, com as recomendações e os custos;
> as seis escolhas menores estão no fim do Desenho.

Sem resposta. Anderson, em 2026-11-09: "registres as opções em Desenho e as rodadas em Entrevista, retomaremos o plano
amanhã, siga direto para escrever as skills", e depois "em seguida, já roda os evals". Lida como ordem de executar com
as recomendadas, que ficam a confirmar nesta rodada; nenhuma delas é decisão.

1. **O commit do executor** (hoje, só com confirmação: `conduct.md:47-48`). Opções:
   - o pedido do passo autoriza o commit na branch do passo, com os testes verdes; merge e push pedem confirmação
     (recomendada) — custo: muda a regra de hoje, e pode sair commit que Anderson não viu, desfeito por `git reset` na
     branch; se paga: em todo passo de código, sem a sessão parada esperando;
   - o executor para antes do commit, com `commit: aguarda confirmação`, e a coordenação leva a rodada — custo: uma
     rodada de 1–2 min por passo, com a sessão parada; se paga: agora, se a regra de hoje vale sem exceção;
   - o executor pergunta no próprio chat — custo: a pergunta fica fora do chat da coordenação; se paga: nunca.
2. **Onde o executor devolve a evidência.** Opções:
   - na seção `## Evidência` do worklog do executor, com o marcador `<!-- fim-Pn: feito|parado -->` que o `wait
     --marker` lê (recomendada) — custo: a coordenação cria o worklog antes de abrir e o commita com o plano; se paga: no
     primeiro passo;
   - em `.sessions/pln-nnn/Pn/evidencia.md`, fora do git — custo: um arquivo que some com o `.sessions/`; se paga: só sem
     o worklog do executor.
3. **Os runtimes padrão dos três consultores.** Opções:
   - Claude Opus `high`, Codex no maior esforço e Grok, um foco cada (recomendada) — custo: ~US$ 2,8–4,4 no Claude, e
     cota sem valor em US$ no Codex e no Grok; se paga: quando a diversidade muda a recomendação numa decisão cara;
   - Claude e Codex em sessão, mais um `designer` por `Agent` — custo: ~US$ 2,8 a mais no `Agent`, e um runtime a menos;
     se paga: com o Grok sem cota.
4. **O que vai ao chat na rodada dos consultores em sessão.** Opções:
   - a tabela lado a lado e a argumentação integral de cada um (recomendada) — custo: ~três telas por rodada, rara pelo
     gatilho da R2.3; se paga: na primeira, pela memória `consultant-debate-shown-in-full`;
   - a tabela e uma linha a favor e contra por consultor, com o caminho do integral — custo: o integral fica fora do
     chat; se paga: só se três consultores pesarem como uma reunião.
5. **As larguras do navegador no chat.** Opções:
   - um artboard por alternativa, larguras empilhadas com `zoom`, e um PNG por largura no scratch (recomendada) — custo:
     um artboard de ~três telas por alternativa; se paga: a partir de 3 alternativas (3 × 3 passa de 8 visuais);
   - um artboard por largura — custo: só 2 alternativas por resposta; se paga: só com 2.
6. **O tema do mockup.** Opções:
   - o tema vem do pacote, escopado no mockup (`--scheme light|dark|both`, `both` no `brza-studio`) (recomendada) —
     custo: não segue o tema do chat, e o `both` dobra a altura; se paga: na primeira tela do `brza-studio`;
   - o desktop do `brza-studio` usa os tokens vivos do Orca; só o mobile e os outros projetos usam o pacote — custo: dois
     caminhos de CSS, ~1 h a mais; se paga: se Anderson quer a tela no tema em que está.
7. **Quando o `plan-runner` novo passa a conduzir o PLN-021.** Opções:
   - ao fechar o P6, e o P7 ao P10 rodam por ele, com o P9 como aceite (recomendada) — custo: o plano troca de fluxo no
     meio; se paga: no P9, sem precisar de outro plano;
   - escrever em `plan-runner-next/` e trocar no fechamento — custo: o nome muda durante o plano, contra a R3.1; se
     paga: só se alguém precisar do fluxo velho estável.
8. **A base das horas** (o PLN-017 executou ~35% do estimado nos passos de skill). Opções:
   - as faixas das rodadas (41 h), com a nota da calibração e o executado medido (recomendada) — custo: o `remaining_h`
     alto no painel até os primeiros passos; se paga: no fechamento;
   - calibrado a ~40%, ~16 h — custo: troca o preço das rodadas por duas medições; se paga: se o PLN-021 executar perto
     do PLN-017.
9. **As escolhas menores** (seleção múltipla, para confirmar): o nome `skillkit`; o `gera_png` com `--scale 1`; o
   `executor.py open` com Claude Sonnet por padrão; um painel por plano e dia; os prefixos `--sa-` e `--sa-m-`; rodar de
   novo só o teste marcado `(≤ 2 min)`.

### Rodada 5 — as respostas da R4 (4a, 4b e 4c) (enviada 2026-11-10)

> **Apresentado antes:** Os oito pontos e as seis escolhas menores da Rodada 4, reapresentados em duas rodadas (4a: R4.1–R4.4; 4b: R4.5–R4.8) e a 4c (escolhas menores). Respostas de Anderson em 2026-11-10: 4a "todos recomendado"; 4b "4.6.2 / restante recomendado"; 4c coberta pelo "restante recomendado". A Rodada 4 acima segue sem a linha de resposta; vale esta.

Respondida em 2026-11-10, 273fc24b-adde-4de7-a0f1-a5849fcac429.

1. **R4.1 — O commit do executor.** Opções:
   - O pedido do passo autoriza o commit na branch do passo, com testes verdes; merge e push pedem confirmação (recomendada) — custo: muda a regra de hoje; pode sair commit não visto, desfeito por git reset na branch; se paga: em todo passo de código;
   - O executor para antes do commit e a coordenação leva a rodada — custo: rodada de 1–2 min por passo, sessão parada; se paga: agora, se a regra de hoje vale sem exceção;
   - O executor pergunta no próprio chat — custo: a pergunta fica fora do chat da coordenação; se paga: nunca.

   **Decidido — O pedido do passo autoriza o commit na branch do passo, com testes verdes; merge e push pedem confirmação.**

2. **R4.2 — Onde o executor devolve a evidência.** Opções:
   - `## Evidência` do worklog do executor, com o marcador `<!-- fim-Pn: feito|parado -->` (recomendada) — custo: a coordenação cria o worklog antes de abrir e o commita com o plano; se paga: no primeiro passo;
   - `.sessions/pln-nnn/Pn/evidencia.md`, fora do git — custo: arquivo que some com o `.sessions/`; se paga: só sem o worklog do executor.

   **Decidido — `## Evidência` do worklog do executor, com o marcador `<!-- fim-Pn: feito|parado -->`.**

3. **R4.3 — Os runtimes padrão dos consultores.** Opções:
   - Claude Opus high, Codex no maior esforço e Grok, um foco cada (recomendada) — custo: ~US$ 2,8–4,4 no Claude; cota sem valor em US$ no Codex e no Grok; se paga: quando a diversidade muda a recomendação numa decisão cara;
   - Claude e Codex em sessão, mais um designer por Agent — custo: ~US$ 2,8 a mais no Agent e um runtime a menos; se paga: com o Grok sem cota.

   **Decidido — Claude Opus high, Codex no maior esforço e Grok, um foco cada.**

4. **R4.4 — O que vai ao chat na rodada dos consultores.** Opções:
   - A tabela lado a lado e a argumentação integral de cada um (recomendada) — custo: ~três telas por rodada, rara pelo gatilho da R2.3; se paga: na primeira, pela memória consultant-debate-shown-in-full;
   - A tabela e uma linha a favor e contra por consultor, com o caminho do integral — custo: o integral fica fora do chat; se paga: só se três consultores pesarem como uma reunião.

   **Decidido — A tabela lado a lado e a argumentação integral de cada um.**

5. **R4.5 — As larguras do navegador no chat.** Opções:
   - Um artboard por alternativa, larguras empilhadas com zoom, e um PNG por largura no scratch (recomendada) — custo: artboard de ~três telas por alternativa; se paga: a partir de 3 alternativas (3 × 3 passa de 8 visuais);
   - Um artboard por largura — custo: só 2 alternativas por resposta; se paga: só com 2.

   **Decidido — Um artboard por alternativa, larguras empilhadas com zoom, e um PNG por largura no scratch.**

6. **R4.6 — O tema do mockup.** Opções:
   - O tema vem do pacote, escopado no mockup (`--scheme light|dark|both`) (recomendada) — custo: não segue o tema do chat; o both dobra a altura; se paga: na primeira tela do brza-studio;
   - O desktop do brza-studio usa os tokens vivos do Orca; só o mobile e os outros projetos usam o pacote — custo: dois caminhos de CSS, ~1 h a mais; se paga: se Anderson quer a tela no tema em que está.

   **Resposta:** "4.6.2" Lida como: O desktop do brza-studio usa os tokens vivos do Orca; só o mobile e os outros projetos usam o pacote.

7. **R4.7 — Quando o plan-runner novo passa a conduzir o PLN-021.** Opções:
   - Ao fechar o P6; o P7 ao P10 rodam por ele, com o P9 como aceite (recomendada) — custo: o plano troca de fluxo no meio; se paga: no P9, sem outro plano;
   - Escrever em plan-runner-next/ e trocar no fechamento — custo: o nome muda durante o plano, contra a R3.1; se paga: só se alguém precisar do fluxo velho estável.

   **Decidido — Ao fechar o P6; o P7 ao P10 rodam por ele, com o P9 como aceite.**

8. **R4.8 — A base das horas.** Opções:
   - As faixas das rodadas (41 h), com a nota da calibração e o executado medido (recomendada) — custo: remaining_h alto no painel até os primeiros passos; se paga: no fechamento;
   - Calibrado a ~40%, ~16 h — custo: troca o preço das rodadas por duas medições; se paga: se o PLN-021 executar perto do PLN-017.

   **Decidido — As faixas das rodadas (41 h), com a nota da calibração e o executado medido.**

9. **R4.9 — As escolhas menores (seleção múltipla)** (seleção múltipla). Opções:
   - o nome `skillkit` (recomendada) — custo: —; se paga: —;
   - o `gera_png` com `--scale 1` (recomendada) — custo: —; se paga: —;
   - o `executor.py open` com Claude Sonnet por padrão (recomendada) — custo: —; se paga: —;
   - um painel por plano e dia (recomendada) — custo: —; se paga: —;
   - os prefixos `--sa-` e `--sa-m-` (recomendada) — custo: —; se paga: —;
   - rodar de novo só o teste marcado `(≤ 2 min)` (recomendada) — custo: —; se paga: —.

   **Resposta:** "restante recomendado" Lida como: o nome `skillkit`; o `gera_png` com `--scale 1`; o `executor.py open` com Claude Sonnet por padrão; um painel por plano e dia; os prefixos `--sa-` e `--sa-m-`; rodar de novo só o teste marcado `(≤ 2 min)`.

### Rodada 6 — o destino dos achados do P8 e a língua do código (enviada 2026-11-10)

> **Apresentado antes:** O parecer do reviewer sobre P1–P7 (12 achados importantes, 6 sugestões, 5 hipóteses que caíram), em `work/reviews/` (REV do P8), com a conferência dos achados A1, A2, A3 e A10 refeita pela coordenação.

Respondida em 2026-11-10, 273fc24b-adde-4de7-a0f1-a5849fcac429.

1. **R6.1.** Opções:
   - Corrigido aqui, com o P11 novo: os defeitos do P8 (A1–A5, A10, A11, A13–A15) (recomendada) — custo: ~3–4 h, pelo implementer, com teste que falha antes; se paga: antes do P9;
   - Corrigir só A1–A5 e mandar o resto a uma issue — custo: ~2 h; a issue fica para depois; se paga: se o P9 precisa começar logo;
   - Tudo para uma issue — custo: nenhum agora; se paga: nunca para A1–A3.

   **Decidido — Corrigido aqui, com o P11 novo: os defeitos do P8 (A1–A5, A10, A11, A13–A15).**

2. **R6.2.** Opções:
   - Corrigido aqui, pela coordenação, antes do P9 (A6–A9, A12, A16–A18) (recomendada) — custo: ~1 h; se paga: agora, porque o P9 lê esses textos;
   - Corrigir A6, A8, A16–A18 e registrar A7, A9, A12 como desvios sem refazer — custo: ~0,5 h; se paga: se evals e sonda do P3 não valem refazer.

   **Decidido — Corrigido aqui, pela coordenação, antes do P9 (A6–A9, A12, A16–A18).**

3. **R6.3.** Opções:
   - A12 descartado, com o porquê no parecer (recomendada) — custo: nenhum; se paga: agora;
   - Refazer com os 5 e 3 casos do Desenho e 3 execuções — custo: ~1,5 h; se paga: só se o +0,08 do screen-artboards virar argumento.

   **Decidido — A12 descartado, com o porquê no parecer.**

4. **R6.4.** Opções:
   - Registrar o ajuste no X1 e na Evidência do P7, manter o navegador com o pacote e medir o Executado pelo --by-task no P10 (recomendada) — custo: ~0,5 h agora e 15 min no P10; se paga: agora e no P10;
   - Refazer o ajuste pelo executor.py, como primeira prova real dele — custo: ~45 min e uma sessão; se paga: no P9.

   **Decidido — Registrar o ajuste no X1 e na Evidência do P7, manter o navegador com o pacote e medir o Executado pelo --by-task no P10.**

5. **R6.5 — A língua do código (ajuste de Anderson à resposta).** Opções:
   - Todo o código em inglês — arquivos, métodos, classes, variáveis —; pt-BR só em docstrings e no texto que volta ao usuário (recomendada) — custo: reescrever o código do PLN-021 que hoje tem nomes em português; se paga: no P11, junto dos defeitos.

   **Resposta:** "todos na primeira opção + um ajuste: todo o código deve ser em inglês, incluindo nomes de arquivos, métodos, classes e variáveis, em pt-BR somente docstrings e conteúdo que retorne ao usuário, como um retorno de texto, por exemplo" Lida como: todo o código em inglês, com o pt-BR só em docstring e no texto que volta ao usuário; a regra subiu à norma do ecossistema.

### Rodada 7 — o aviso, o fallback, o cobre e os pareceres do P11 (enviada 2026-11-10)

> **Apresentado antes:** A revisão do plano no 20dff79 sustentou os quatro pontos. O X3 atribui a classificação aviso × erro à Rodada 5, e a Rodada 5 não tem esse ponto. O roster troca de runtime acima de 55% sem a narração dizer o modelo. Sem cobre:, o --apply marca todos os subpassos pendentes. A evidência das revisões em laço do P11 está em /tmp.

Respondida em 2026-11-10, na sessão 01a1c7c8-3571-7120-bb0f-1125dc3e36ea.

1. **A classificação aviso × erro do plan_state.** Opções:
   - Fica aviso, e o X3 passa a citar esta rodada (recomendada) — custo: reescrever a última frase do X3, cerca de 5 minutos; se paga: agora, porque o --strict e o close_check usam essa fronteira;
   - deviation-not-cited e hours-unreadable passam a erro — custo: cerca de 0,3 h de código e testes, e o PLN-017 trava em mais um ponto; se paga: no primeiro plano que fecharia com desvio sem citação.

   **Resposta:** "todos pelo recomendado" Lida como: fica aviso, e o X3 passa a citar esta rodada.

2. **O fallback do roster e o corte de 55%.** Opções:
   - Manter o fallback e os 55%, e a tabela e a narração dizerem qual consultor trocou e para qual modelo (recomendada) — custo: cerca de 0,5 h de código e teste; se paga: na primeira rodada em que um runtime passar de 55%;
   - Sem fallback: o runtime acima da cota fica de fora — custo: cerca de 0,3 h; se paga: se a diversidade de modelo vale mais do que três pareceres;
   - Manter a troca silenciosa — custo: nenhum agora; se paga: nunca, porque a troca apaga a razão da R5.3.

   **Resposta:** "todos pelo recomendado" Lida como: manter o fallback e os 55%, e a tabela e a narração dizerem qual consultor trocou e para qual modelo.

3. **O --apply sem a linha cobre:.** Opções:
   - Recusar o --apply sem cobre: e mandar o executor completar pelo send (recomendada) — custo: cerca de 0,3 h e um teste; quem esquece a linha dá uma ida e volta; se paga: no primeiro passo parcial em que a linha faltar;
   - Manter marca todos e avisa, e reescrever o subpasso 3 do P11 para dizer isso — custo: nenhum de código, uma linha no plano; se paga: só se o passo sem cobre: deve fechar inteiro.

   **Resposta:** "todos pelo recomendado" Lida como: recusar o --apply sem cobre: e mandar o executor completar pelo send.

4. **Onde ficam os pareceres das revisões em laço do P11.** Opções:
   - Juntar os pareceres do P11.1 e do P11.2 num REV só, com as rodadas em seções, e apontá-lo em Revisões (recomendada) — custo: cerca de 0,3 h agora; se paga: no P10, cujo item 2 confere destino de achado;
   - Deixar em /tmp e registrar um X dizendo isso — custo: cerca de 5 minutos; se paga: só enquanto esses arquivos existirem.

   **Resposta:** "todos pelo recomendado" Lida como: juntar os pareceres do P11.1 e do P11.2 num REV só e apontá-lo em Revisões.

### Rodada 8 — os oito achados de texto que a revisão do plano sustentou (enviada 2026-11-10)

> **Apresentado antes:** O parecer do plano inteiro deixou oito achados com destino corrigido aqui. Os cinco falsos continuam falsos. A Cobertura segue com Passo a planejar e sem casos C. O Desenho ainda diz Em aberto e sem lastro em escolhas que a R5 fechou, e o pedido gerado copia isso. O P9 e o P10 não carregam a sonda do X7, a prova do CODEX_MODEL nem o --by-task. O P11.1 fechou sem worklog. A linha Executa do P11 diz que o executor.py abriu a sessão. O D1 e o D3 descrevem contratos que o código já mudou. Sobram RE_DATA, strip_measurement(texto) e AQUI no trecho do kit. A ordem dos passos não tem o P11.

Respondida em 2026-11-10, 01a1c7c8-3571-7120-bb0f-1125dc3e36ea.

1. **Aplico os oito juntos, como texto no plano e no Desenho, com o rename pontual do A9.** Opções:
   - Aplicar os oito agora, antes do P9 (recomendada) — custo: cerca de 3,5 h de escrita na coordenação, mais o rename de RE_DATA, do README do kit e do AQUI desse trecho; se paga: antes do P9, porque o pedido do passo copia o Desenho e o P9 hoje executa uma lista C vazia;
   - Aplicar só A1, A2, A5 e A6 — custo: cerca de 2,5 h; se paga: no P9, para a Cobertura e os três compromissos; A7 a A10 ficam para a próxima revisão;
   - Deixar os oito como estão e esperar o pedido do P9 — custo: nenhum agora; se paga: nunca para o A1, porque o aceite manual executa os C e a lista está vazia.

   **Resposta:** "aplicar agora" Lida como: aplicar os oito achados de texto agora, antes do P9.

### Rodada 9 — o que roda do P9 e o passo-sonda do C1 e do X7 (enviada 2026-11-12)

> **Apresentado antes:** O PLN-021 tem 9 de 11 passos feitos; o próximo é o P9, com os C1–C4, a sonda do X7 e a prova do CODEX_MODEL do X9. Nenhum plano aberto tem passo de execução pronto: o PLN-014 está no Desenho, e o PLN-019 e o PLN-020 esperam rodadas. Por isso o C1 e o X7 precisam de um passo para servir de sonda.

Respondida em 2026-11-12, 464ae592-7fb4-4ed1-9f6d-8dd26bd7d065.

1. **Quais itens do P9 rodam agora** (seleção múltipla). Opções:
   - C2 + C4 (recomendada) — custo: cerca de 10 min, nenhuma sessão aberta; se paga: agora, fecha 2 dos 6 itens sem cota;
   - X9: CODEX_MODEL — custo: 5 a 10 min e um turno da cota Codex; se paga: na primeira bifurcação cara com consultor Codex pelo consult.py;
   - C1 + X7 juntos — custo: 30 a 45 min e uma sessão Sonnet, num worktree do brza-studio por --tree; se paga: no primeiro passo de código de um plano real;
   - C3: artboards — custo: 20 a 30 min, e uma tela para desenhar; se paga: no primeiro Desenho que muda o que se vê.

   **Decidido — C2 + C4; X9: CODEX_MODEL; C1 + X7 juntos; C3: artboards.**

2. **Que passo serve de sonda para o C1 e o X7.** Opções:
   - P12 sonda no PLN-021 (recomendada) — custo: cerca de 5 min de plano e um passo a mais; o executor muda uma linha no brza-studio num worktree --tree, sem merge; se paga: agora, o P9 fecha sem esperar outro plano;
   - Esperar um plano real — custo: o PLN-021 aberto por dias ou semanas; se paga: quando o passo chegar, com prova mais fiel;
   - C1 no workspace, X7 depois — custo: cerca de 20 min; se paga: agora para o C1; nunca para o X7, se ficar só no achado.

   **Decidido — P12 sonda no PLN-021.**

### Rodada 10 — os vereditos do P9, o layout do painel, o destino do X11 e do X12, a branch do P12 (enviada 2026-11-12)

> **Apresentado antes:** O P9 rodou: o C1 pelo P12 (brza-studio@c470dda, sem comando digitado), o C2 pelo PNG do painel (X11: a linha Executa cortada), o C3 com os artboards A (tabela) e B (cartões abaixo de 700 px) em 375, 768 e 1280, o C4 pelo diff e pelo brza sync --dry-run (o sync real barrado pelo classificador). O X9 provado pelo rollout do Codex. O X7 provado em parte: o executor gravou o worklog fora do checkout pelo Bash, não pelo Write. O X12: a janela do Executado começa depois do --wait do open.

Respondida em 2026-11-12, 464ae592-7fb4-4ed1-9f6d-8dd26bd7d065.

1. **Os vereditos do C1 ao C4, e o X7** (seleção múltipla). Opções:
   - Os quatro passam, com o X11 e o X12 como desvios, e o X7 fecha pela sonda no Bash (recomendada) — custo: nenhum agora; se paga: agora, o P9 fecha;
   - Uma segunda sonda do X7 que obrigue o executor a gravar pelo Write — custo: cerca de 5 min e mais uma sessão Sonnet; se paga: no primeiro executor que gravar pelo Write e travar;
   - O C4 roda de novo com o brza sync real — custo: cerca de 2 min e o git merge da master em todos os worktrees; se paga: agora, prova literal do C4;
   - Algum caso falha — custo: —; se paga: —.

   **Resposta:** "1 e 2" C1 a C4 passam, com o X11 e o X12 como desvios; o X7 não fecha pela sonda no Bash: roda a segunda sonda, pelo Write

2. **O C3: que layout o painel usa.** Opções:
   - A, a tabela de hoje (recomendada) — custo: nenhum; se paga: agora; o chat tem 736 px;
   - B, cartões abaixo de 700 px — custo: cerca de 1 h no plan_panel.py e os testes do painel; reabre a D5; se paga: quando o painel for aberto no celular.

   **Resposta:** "B" Lida como: B, cartões abaixo de 700 px.

3. **O destino do X11 e do X12.** Opções:
   - Um P13 no PLN-021, pelo implementer com revisão (recomendada) — custo: cerca de 1 h; se paga: no próximo plano com executor;
   - Uma issue no playground, e o PLN-021 fecha sem eles — custo: cerca de 10 min; se paga: na promoção ao core;
   - Só os desvios registrados — custo: nenhum; se paga: nunca.

   **Resposta:** "P13" Lida como: Um P13 no PLN-021, pelo implementer com revisão.

4. **A branch docs/pln-021-p12 do brza-studio.** Opções:
   - Merge na master do brza-studio e push (recomendada) — custo: cerca de 2 min; o push vai ao GitHub; se paga: agora;
   - Manter a branch e remover o worktree — custo: nenhum; se paga: nunca, se ninguém voltar;
   - Descartar a branch e o worktree — custo: perde a linha; se paga: nunca.

   **Resposta:** "merge" Lida como: Merge na master do brza-studio e push.

## Passos

Do Desenho, com as horas do `designer` (R4.8 confirmada na Rodada 5). A ordem: P1 ∥ P2 → P3 → P4, P5 → P6; o P7 depois do P1; P8 →
P11 → P12 → P14 → P9 → P10, e o P13 depois do P12. Executam a pedido de Anderson de 2026-11-09, com as recomendadas da R4, confirmadas na Rodada 5 (menos a R4.6.2).

### P1 — O `skillkit` e a migração da `meeting-runner`

Executa D1 · executor: `implementer`, pela coordenação

Estimado: 3 h · Executado: 0.08 h

- [x] **1. `.claude/scripts/skillkit/`** (`paths`, `sessions_map`, `sessions_cli`, `measure`, `visual`) e os testes
- [x] **2. A `meeting-runner` importa do kit** pelo `_kit.py`, sem mudar teste

**Evidência:** `python3 -I -m unittest discover -s .claude/scripts/tests` → 55 OK ·
`python3 -I -m unittest discover -s .claude/skills/meeting-runner/scripts/tests` → 323 OK · o `panel.py render` da
fixture `estado-r3.json` saiu pelo `brza shot` (736×1659, lido inteiro) · `Executado` pela duração do subagente (272 s) ·
desvios em X2

### P2 — Os quatro scripts de R2.2 e o `plan_md.py`

Executa D6 · executor: `implementer`, pela coordenação; em paralelo com o P1

Estimado: 11.5 h · Executado: 0.18 h

- [x] **1. `plan_md.py`**, o leitor do plano dividido
- [x] **2. `plan_state.py`, `step_request.py`, `round_log.py`, `close_check.py`**, com testes por código de problema

**Evidência:** `python3 -I -m unittest discover -s .claude/skills/plan-runner/scripts/tests` → 84 OK · `plan_state.py
PLN-021` → limpo, 41 h conferem · `plan_state.py PLN-017` → 2 erros reais (P7 sem evidência que se refaça;
`executed_h` 9.516 × 7.974 somado) · `Executado` pela duração do subagente (660 s) · desvios em X3

### P3 — O executor: `executor.py`, o molde do pedido e a sonda de permissão

Executa D3 · executor: `implementer`, pela coordenação · depende de P1 e P2

Estimado: 4 h · Executado: 0.06 h

- [x] **1. `executor.py`** (`open|send|wait|evidence|close|status`), o manifesto e o worklog do executor

**Evidência:** `python3 -I -m unittest discover -s .claude/skills/plan-runner/scripts/tests` → 151 OK (39 do executor) ·
a prova com o `brza` falso no PLN-901: `open` (tabela e `brza tree` + `brza sessions … --prompt-file`), `wait` → rc 75
e, com o marcador, `P3 · feito`; `evidence` conferiu o commit e o comando, e o `--apply` gravou o `### P3` ·
`Executado`: o P3–P5 foi um subagente só, 357 s medidos na retomada (a parte anterior ao limite de uso não foi medida),
dividido pelo peso · a sonda de permissão de gravar fora do checkout não rodou, porque o `brza` era falso · desvios em X4

### P4 — O painel do plano

Executa D5 · executor: `implementer`, pela coordenação · depende de P1 a P3

Estimado: 2.5 h · Executado: 0.02 h

- [x] **1. `plan_panel.py`** (`publish|render`), chamado pelo `executor.py`, `round_log.py` e `plan_state.py --fix`

**Evidência:** `python3 -I -m unittest discover -s .claude/skills/plan-runner/scripts/tests -p test_plan_panel.py` → 12 OK · `/private/tmp/pln021/p3-panel/painel.png` a 736 lido, sem corte,
com as horas, os passos e os consultores · `Executado` no P3

### P5 — Os consultores em sessão

Executa D4 · executor: `implementer`, pela coordenação · depende de P3

Estimado: 3 h · Executado: 0.02 h

- [x] **1. `consult.py`** (`open|wait|table|close`), o roster com o corte de cota e a tabela lado a lado

**Evidência:** `python3 -I -m unittest discover -s .claude/skills/plan-runner/scripts/tests -p test_consult.py` → 16 OK · a prova no PLN-901 abriu Claude, Codex e Grok pelo `brza`
falso, com os prompts "Você é consultor do Desenho de D3 do PLN-901", e o `table` montou a tabela com quem não entregou ·
`Executado` no P3

### P6 — A SKILL.md e as references do `plan-runner`, pela `skill-creator`, com os evals

Executa D2 · executor: a sessão que conduz · depende de P2 a P5

Estimado: 6 h · Executado: 0.3 h

- [x] **1. A `SKILL.md` e as references**, pela `skill-creator`: `design.md`, `consultants.md`, `step-request.md`,
      `review.md`, `narration.md` novas; `open-and-plan.md`, `conduct.md`, `close.md` e o molde reescritos
- [x] **2. Os evals, iteração 1**, contra a versão antiga, em cópias isoladas com o `brza` falso

**Evidência:** `/private/tmp/pln021/plan-runner-workspace/iteration-1/benchmark.md` → versão nova 17/17, antiga 9/17
(+0,44); o caso que separa é o do executor (7/7 × 2/7) e o dos consultores em sessão (5/5 × 3/5); o de retomar empata no
diagnóstico e só difere no script (5/5 × 4/5) · `python3 -I -m unittest discover -s .claude/skills/plan-runner/scripts/tests`
→ 151 OK · `Executado`: a escrita e a correção pela coordenação, estimadas pelas horas do turno, sem medição por passo

### P7 — A `screen-artboards`, pela `skill-creator`, com os evals

Executa D7 · executor: `implementer` para os scripts, e a sessão que conduz para a SKILL.md e os evals · depende de P1

Estimado: 7 h · Executado: 0.13 h

- [x] **1. A `SKILL.md` e as quatro references**, pela coordenação, com a `skill-creator`
- [x] **2. `artboard.py`, `tokens.py`, as cinco molduras e os pacotes `brza-studio` e `neutral`**
- [x] **3. Os evals, iteração 1**, com e sem a skill, em cópias isoladas

**Evidência:** `python3 -I -m unittest discover -s .claude/skills/screen-artboards/scripts/tests` → 55 OK (48 mais 7 do ajuste R4.6.2, X6) · 14 PNGs das
cinco molduras lidos (`/private/tmp/pln021/artboards-p7/v2/png/`) e o desktop do `brza-studio` com tokens vivos em `/private/tmp/pln021/artboards-p7/v3/png/` · evals: com a skill 13/13, sem 12/13, delta +0,08; o
caso de desktop empata em 7/7, e o que discrimina é a página web num artboard só (R4.5) · `Executado`: os scripts, 464
s do subagente; a SKILL.md e os evals pela coordenação, sem medição · desvios em X5 e X6

### P8 — A revisão da entrega

Executa a revisão · executor: `reviewer` · depende de P1 a P7

Estimado: 2 h · Executado: 0.2 h

- [x] **1. A revisão adversária de P1 a P7**, pelo `reviewer` (Opus), e a conferência dos achados A1, A2, A3 e A10 pela coordenação
- [x] **2. O destino de cada achado**, pela Rodada 6

**Evidência:** [REV-026](../../work/reviews/REV-026-pln-021-p1-a-p7.md) · `python3 -I -m unittest discover` nos quatro conjuntos → 55 (kit), 151 (plan-runner), 55 (screen-artboards), 323 (meeting-runner) OK · `brza sessions … --effort xhigh --dry-run` → "--effort exige --model" (A1) · `brza quota --json` → `accounts[].windows[]` (A2) · `Executado` pela duração do subagente (~700 s) e a conferência

### P11 — Os defeitos do P8 e o código em inglês

Executa D2, D3, D4, D5, D6 e D7, a partir de [REV-026](../../work/reviews/REV-026-pln-021-p1-a-p7.md) e da R6 · executor: `implementer`, pela coordenação, na sessão que a coordenação abriu (o `executor.py` não abriu o P11; X1 e X9) · depende de P8

Estimado: 6 h · Executado: sem medição desta sessão

- [x] **1. Os defeitos de código do REV-026** (A1–A5, A10, A11, A13–A15), cada um com o teste que falha antes e, onde der, a prova pelo `brza` real em `--dry-run`
- [x] **2. O código em inglês** (R6.5): nomes de arquivo, função, classe e variável de `.claude/scripts/skillkit/`, `plan-runner/scripts/` e `screen-artboards/scripts/` em inglês, com a `meeting-runner` importando do kit sem mudar um teste; pt-BR só em docstring e no texto que volta ao usuário
- [x] **3. O `--apply` do `executor.py` marca só os subpassos que a evidência cobre** (D3), e não todos os pendentes (X4; REV-026 A9)
- [x] **4. As skills e o Desenho acompanham** os nomes novos (SKILL.md, references, D1–D7)

Faz-se antes do P9: o aceite manual roda sobre o roster e o `wait` corrigidos.

**Evidência:** `brza-workspace@0797029` · `python3 -I -m unittest discover` nos quatro conjuntos → 56 (kit), 193 (plan-runner), 56 (screen-artboards), 323 (meeting-runner) OK · a `meeting-runner` só mudou em `common.py`, `launch_persona.py`, `panel.py` e `tally.py`, e o `_legacy_measure` traduz as chaves inglesas da medida · subpassos 1 e 3 no `4350325`, com o registro em [O PLN-021: os defeitos do P11.1](../../work/worklogs/2026-11-10-pln-021-p11-1-os-defeitos.md), sem uma 4ª rodada (o limite de três foi o pedido) · seis rodadas de revisão do P11 no [REV-027](../../work/reviews/REV-027-pln-021-p11.md) · `Executado`: sem medição desta sessão · desvios em X9 e proposta em X10

### P12 — A sonda do executor: uma linha no `brza-studio`

Executa D3 pelo `executor.py`, como sonda do C1 e do X7 (R9.2) · executor: uma sessão executora Claude Sonnet, aberta pelo `executor.py open --tree pln-021-p12 --type docs` · depende de P11

Estimado: 0.5 h · Executado: 0.005 h (da abertura da sessão, 19:14:15, ao worklog, 19:14:34; a janela do `executor.py` deu 0.003 h, X12)

- [x] **1. A linha** — no `docs/development.md` do `brza-studio`, ao fim de `## Troubleshooting`, um item em inglês: a máquina que trava nos testes roda só os arquivos tocados, por caminho, com `--maxWorkers=2` (`pnpm test <file> --maxWorkers=2`), e a suíte completa roda no GitHub pelo `node-next-compat.yml` (`gh workflow run node-next-compat.yml --ref <branch>`). Commit na branch `docs/pln-021-p12`, sem merge nem push.
- [x] **2. O worklog fora do checkout** — o executor grava a evidência no worklog do workstream, fora do worktree do `brza-studio`; se o Claude pedir permissão para isso, o `wait` devolve `bloqueado`, e esse é o resultado da sonda do X7.

**Evidência:** brza-studio@c470dda · `git -C /Users/andepb/Projects/brza-studio/.worktrees/pln-021-p12 show --stat HEAD` → 1 arquivo, `docs/development.md`, +1 linha · arquivos: docs/development.md · o commit é das 19:14:26, com o autor `brz-anderson`, na `docs/pln-021-p12`, sem merge · o worklog gravado fora do checkout sem pedido de permissão e o `wait` sem `bloqueado` (X7), mas por script no Bash, e não pela ferramenta `Write` (o `worker_done` do executor): a gravação pelo `Write` fora do checkout segue sem prova · o worktree nasceu pelo `brza tree` em ~3 min, fora da janela · desvios em X12

### P14 — A segunda sonda do X7: o worklog pelo `Write`

Executa D3 pelo `executor.py`, como a segunda sonda do X7 (R10.1) · executor: uma sessão executora Claude Sonnet, aberta pelo `executor.py open --tree pln-021-p14 --type chore` · depende de P12

Estimado: 0.25 h · Executado: 0.006 h (da abertura da sessão, 19:33:53, ao worklog, 19:34:15; a janela do `executor.py` deu 0.002 h, X12)

- [x] **1. A leitura** — no `docs/development.md` do `brza-studio`, ache a linha que o P12 acrescentou (a do `--maxWorkers=2`) e anote no worklog o número dela. Sem mudar arquivo do `brza-studio` e sem commit.
- [x] **2. O worklog pelo `Write`** — grave o worklog, fora do checkout, só pelas ferramentas `Write` ou `Edit`, nunca por comando de shell. Se o Claude pedir permissão, o `wait` devolve `bloqueado`, e esse é o resultado da sonda.

**Evidência:** sem commit, como o passo pede · `cd /Users/andepb/Projects/brza-studio/.worktrees/pln-021-p14 && grep -n -e --maxWorkers=2 docs/development.md` → uma linha, a 59 · arquivos: /Users/andepb/Projects/brza-workspace/.worktrees/playground/work/worklogs/2026-11-12-pln-021-p14-a-segunda-sonda-do-x7-o-worklog-pelo-write.md · o transcript do executor tem um `Write` no worklog às 19:34:13 e nenhum resultado de permissão negada; nenhum `Bash` gravou nele · a sonda vale para o modo de permissão que o `open` dá à sessão · o worktree removido sem mudança

### P13 — Os desvios X11 e X12 e o painel em cartões

Executa D3 e D5, a partir do X11, do X12 e da R10.2 · executor: `implementer`, pela coordenação, com o `reviewer` · depende de P12

Estimado: 2 h · Executado: — h

- [ ] **1. O X11** — o leitor do passo junta a linha `Executa … · executor: …` que continua nas linhas seguintes, até a linha em branco, e o painel mostra o executor inteiro. Teste com o `### P9` quebrado em duas linhas.
- [ ] **2. O X12** — o `executor.py open` grava o evento `aberto` com o `at` do evento `open` da sessão no `.sessions/sessions.jsonl`, e não com a hora em que o `--wait` volta; sem o evento, com a hora de antes da chamada ao `brza sessions`. Teste: a janela do P12 (19:14:15 → 19:14:34) dá 0.005 h.
- [ ] **3. O painel em cartões** (D5, R10.2) — abaixo de 700 px, por `@container`, um cartão por passo, como no [protótipo](PLN-021-painel-cartoes.png); de 700 px para cima, a tabela de hoje, com as colunas que ela tem. Testes do painel, e o PNG conferido em 375 e 736 px.

### P9 — O aceite manual

Executa os C1–C4, a sonda de permissão do X7 e a prova do `CODEX_MODEL` do X9 · executor: a sessão que conduz e Anderson · depende de P6 a P8, P11, P12 e P14

Estimado: 1.5 h · Executado: 0.45 h (relógio da coordenação, 19:09 → 19:36, sem a espera da R10)

- [x] **1. C1** — um passo real de um plano aberto pelo `executor.py`, sem comando digitado por Anderson: o P12 (R9.2)
- [x] **2. C2** — o PNG do painel conferido no chat
- [x] **3. C3** — um Desenho com artboards no chat, conferido pelo PNG em cada largura
- [x] **4. C4** — o `plan-runner` novo só na branch do playground, e a master limpa depois do `brza sync`
- [x] **5. A sonda de permissão do X7**, com o `brza` real, no executor do `brza-studio`: o P12 (R9.2) pelo Bash, e o P14 pelo `Write` (R10.1)
- [x] **6. A prova do `CODEX_MODEL`** `gpt-6.1-sol`, com uma sessão real — em 2026-11-12, `brza sessions pln021-x9-codex --agent codex --model gpt-6.1-sol --effort xhigh` abriu e respondeu sem recusa; o modelo não sabe o próprio nome, e a prova é o rollout `~/.codex/sessions/2026/11/12/rollout-2026-11-12T19-18-21-01a1d1d7-….jsonl` → `"model":"gpt-6.1-sol"` (7×) e `"effort":"xhigh"`; o `executor.CODEX_MODEL` é o mesmo

**Evidência:** parcial, 2026-11-12 — o 6: `grep -o '"model":"[^"]*"' ~/.codex/sessions/2026/11/12/rollout-2026-11-12T19-18-21-01a1d1d7-25e1-74e2-bc75-c7aab19f4231.jsonl` → `"model":"gpt-6.1-sol"`; C1 a C4 com o Observado na tabela de `## Casos manuais` e o Veredito de Anderson, "passa" (R10.1); o 5 pelo P12 (Bash) e pelo P14 (`Write`), os dois sem `bloqueado` nem pedido de permissão

### P10 — O fechamento

Executa o fechamento, pelo `close_check.py`, e a medida do `Executado` pelo `--by-task` (R6.4) · executor: a sessão que conduz

Estimado: 0.5 h · Executado: — h

- [ ] **1. O `close_check.py PLN-021`**, com o destino de cada achado e o que o item 3 ainda lista
- [ ] **2. Medir o `Executado` pelo `--by-task`** (R6.4)

## Regressão

- **A `meeting-runner` faz o mesmo com o `skillkit`.** Como se confere: os 323 testes dela e um `panel.py publish` sobre a
  fixture `estado-r3.json`, com o PNG conferido.
- **O `plan-runner` novo segue o molde e o `check_notes.py`.** Como se confere: o `check_notes.py` limpo nos planos do
  playground depois do P6, e os planos fechados intocados.

## Desvios

- **X1 — Os passos rodam por `implementer`, e não por sessão nova aberta pelo `brza sessions`.** O `executor.py` ainda não
  existe, e Anderson pediu para seguir direto; afeta P1 a P5 e P7.
- **X2 — O `skillkit` saiu com oito ajustes de assinatura** para a `meeting-runner` não mudar de comportamento:
  `wait_brza` devolve `(rc, dict)`; `list_states` ganha `cmd` e `ids`; `send_argv` recusa corpo vazio ou duplo; `--rename`
  só com `rename=True`; `salva_visual(doc, prefixo, …)`; o `gera_png` cai no Chrome também quando o `brza shot` não grava;
  os pontos de troca em teste são `visual._run` e `visual._chrome`; `measure` leva `find_rollout` e `codex_turns`. Afeta
  P1 e D1.
- **X3 — Os scripts do D6 classificam e localizam**: cada problema tem `level` (`erro`/`aviso`) e `line`;
  `deviation-not-cited` e `hours-unreadable` são aviso; o desvio que nomeia o passo conta como citado; `step-without-design`
  isenta rodada, revisão, aceite e fechamento; `round_log --next` imprime só o número. Afeta P2 e D6; a classificação
  aviso × erro: fica aviso, decidido na Rodada 7 (a Rodada 5 não tinha esse ponto).
- **X4 — O executor e os consultores saíram com escolhas que o D3 e o D4 não fixavam**: o `--marker` só vai ao `brza
  sessions wait` com um passo (com vários, o script confere o marcador sozinho); o rc com eventos juntos prioriza falha,
  depois bloqueado; o `verdict` ficou no `executor.py`, fora do `skillkit`; o marcador só vale como última linha;
  o `--apply` marca todos os subpassos pendentes (contra o D3, que diz os cobertos: subpasso 3 do P11); os fallbacks do roster (Opus → Grok; Codex e Grok → Sonnet `high`) são
  do executor, e o `--effort xhigh` do Codex não foi conferido no `brza sessions` real (o REV-026 A1 mostrou que falha sem `--model`); sem `--checkout` nem `--tree`, o
  executor abre no worktree do workspace, o que conflita com a regra "não commite no brza-workspace" do pedido. Afeta P3
  a P5, D3 e D4; os fallbacks e o checkout padrão: o checkout padrão é o defeito A5 do REV-026, corrigido no P11.
- **X5 — A `screen-artboards` corrigiu as references em seis pontos**: o `xmlns` do SVG passa no filtro de rede; a deriva
  só sai 4 quando um token muda; todos os tokens do mobile entram com `--sa-m-` e sobrescrevem os do desktop nas molduras
  de celular; o PNG de issue é `<nome>-<assunto>.png`; o fragmento responsivo usa `@container`, e não `@media` (achado do
  eval); telas que não são alternativas saem sem letra. Afeta P7 e D7.
- **X6 — O ajuste R4.6.2 do P7 saiu por subagente, depois do P6**: o desktop do `brza-studio` (`macos`/`windows` com
  `--pack brza-studio`) usa os tokens vivos do chat (`.sa-art[data-live]`, 27 tokens, com `ALIAS_VIVO` para os que o chat
  não injeta); `--scheme` ali é erro (código 2); o `shot` injeta o esquema do pacote só no HTML temporário; o navegador com
  `--pack brza-studio` segue o pacote (R6.4). Os 55 testes passam e os PNGs estão em `v3`. Afeta P7 e D7.
- **X7 — A sonda de permissão do P3 não rodou**: o `brza` dos testes era falso, e o executor do `brza-studio` grava o
  worklog fora do checkout. Roda no P9, com o `brza` real. Afeta P3 e D3. **Rodou em 2026-11-12**: o P12 gravou o worklog pelo Bash e o P14 pelo `Write`, fora do checkout, sem pedido de permissão (R10.1).
- **X8 — Os evals saíram com 3 e 2 casos, contra os 5 e 3 do Desenho**: faltam o caso negativo do gatilho R2.3, o do
  `round_log` com `reabre` e o da deriva de tokens, e cada configuração rodou uma vez. Descartado como achado (R6.3): o
  delta de +0,44 já discrimina. Afeta P6, P7 e D2.

- **X9 — O P11.1 saiu por `implementer` e revisor em laço, e não pelo `executor.py`**, porque os defeitos A3, A4, A5 e A11
  estão no próprio `executor.py`. Os X propostos pelo `implementer` entram aqui: o `CODEX_MODEL` `gpt-6.1-sol` (do
  `~/.codex/config.toml`, sem prova com sessão real: roda no P9); a cota pela conta ativa e a janela `session` (ou
  `weekly` no Grok); `**Resposta:**` com "lida como" conta como decidida, exceto contraproposta e esclarecimento; `open`
  sem `--checkout` nem `--tree` recusa (rc 2); `running:` recusa, também na primeira abertura; o `--apply` marca só os
  subpassos que a linha `cobre:` declara (`todos` vence; sem ela, o P11.1 marcava todos e avisava). A Rodada 7 recusou isso: o `--apply` sem `cobre:` não grava e manda completar pelo `send`. O passo coberto em parte volta
  pelo `send` ou pelo `open`. Afeta P3 a P5, D3 e D4.
- **X10 — Duas chaves ficaram em português. Proposta, sem decisão de Anderson.** `last_send["origem"]` em `sessions_map.py` ficou porque o teste da `meeting-runner` afirma a chave. `answered.data` em `round_log.py` e no Desenho D6 ficou porque a spec fechada do subpasso 2 manda `literal` e `data`; a rodada 2 marcou o pedido de renome como falso. Afeta P11 e D6. Se houver rodada:
  1. Manter as duas (recomendada) — custo: nenhuma troca agora; se paga: já, o adaptador e a spec não quebram.
  2. Renomear `origem` → `origin` e `data` → `date` nos leitores e escritores, com o teste da `meeting-runner` — custo: uma rodada de código e os 323 testes; se paga: quando a spec for reaberta.

- **X11 — O painel corta a linha `Executa` que quebra no Markdown**: no PNG do C2, o executor do P9 saiu "a sessão que", porque o resto ("conduz e Anderson") estava na linha seguinte do `### P9`, e o leitor do passo lê só a primeira. A linha do P9 foi juntada; o leitor segue sem a correção. Afeta P4 e D5.

- **X12 — A janela do `Executado` começa depois do trabalho**: o `executor.py open` grava o `aberto` quando o `brza sessions --wait` volta, e o executor do P12 fez o passo inteiro dentro desse `--wait` (sessão às 19:14:15, commit às 19:14:26, worklog às 19:14:34, `aberto` às 19:14:43). A janela deu 0.003 h contra 0.005 h, e o turno do executor não aparece no `measurements.jsonl`. A janela devia começar no `open` do `sessions.jsonl`. Afeta P3 e D3.

## Revisões

- 2026-11-10 — [REV-026: PLN-021 P1 a P7, a entrega do plan-runner coordenado e da screen-artboards](../../work/reviews/REV-026-pln-021-p1-a-p7.md): 12 achados importantes, 6 sugestões e 5 falsos; o código vai ao P11, o plano e as skills foram corrigidos na coordenação, o A12 foi descartado.
- 2026-11-10 — [REV-027: PLN-021 P11, as revisões em laço](../../work/reviews/REV-027-pln-021-p11.md): as seis rodadas do P11.1 e do P11.2, 71 achados com a evidência na nota. O P11.1 declara 4, 0 e 1 importantes nas três rodadas; no P11.2 a rodada 1 tem 2 importantes e as outras duas só sugestão ou falso.

## Worklogs

- 2026-11-09 — aberto; R1 respondida (destino, protótipo no playground, as três frentes de coordenação, skill própria
  de artboards); Terreno do `collector`; R2 (os quatro scripts, consultores só em decisão cara, pacote de tokens por
  projeto) e R3 (o nome `plan-runner` na branch, `.claude/scripts/`, a `meeting-runner` migra).
  [A entrevista do PLN-021: o plan-runner com sessão coordenadora e a skill de artboards](../../work/worklogs/2026-11-09-a-entrevista-do-pln-021.md)
- 2026-11-10 — Desenho D1–D7 registrado e R4 enviada sem resposta; P1 a P7 executados com as recomendadas, a pedido;
  evals da iteração 1 das duas skills. Travou na R4. [As skills do PLN-021 escritas e os evals da iteração 1](../../work/worklogs/2026-11-10-as-skills-do-pln-021-e-os-evals.md)
- 2026-11-10 — R4 respondida (Rodada 5, com a R4.6.2 em outra opção), P7 reaberto (X6), P8 feito ([REV-026](../../work/reviews/REV-026-pln-021-p1-a-p7.md)), Rodada 6 e o P11 aberto; o código em inglês subiu à norma. Próximo: o pedido do P11. [O PLN-021: a R4 respondida, o P7 reaberto e a revisão do P8](../../work/worklogs/2026-11-10-pln-021-r4-respondida-e-a-revisao-do-p8.md)
- 2026-11-10 — P11.1, subpassos 1 e 3, no `4350325` e no `ac36476`, com três rodadas; o worklog saiu na Rodada 8. [O PLN-021: os defeitos do P11.1](../../work/worklogs/2026-11-10-pln-021-p11-1-os-defeitos.md)
- 2026-11-10 — P11 fechado: subpassos 2 e 4 no `0797029`, três rodadas de revisão. Próximo: o P9, a pedido. [O PLN-021: o código em inglês do P11](../../work/worklogs/2026-11-10-pln-021-codigo-em-ingles.md)
- 2026-11-11 — Rodada 8, "aplicar agora": os oito achados de texto no plano e no Desenho, antes do P9. [O PLN-021: os oito achados de texto](../../work/worklogs/2026-11-11-pln-021-os-oito-achados-de-texto.md)
- 2026-11-12 — Parecer da rodada 2 do texto: quatro resíduos aplicados, a CLI do D3, o `verdict`, `level`/`line` e a R6.5 em D4–D6. [O PLN-021: os quatro resíduos do texto](../../work/worklogs/2026-11-12-pln-021-os-quatro-residuos-do-texto.md)
- 2026-11-12 — R9 e R10 respondidas; P12 e P14, as sondas do executor (`brza-studio@c470dda` na master); C1–C4 passam; X9 e X7 provados; o P9 fechou e o P13 nasceu com X11, X12 e os cartões da D5. Próximo: o P13, a pedido. [O PLN-021: o aceite manual e as sondas do executor](../../work/worklogs/2026-11-12-pln-021-o-aceite-manual-e-as-sondas.md)

## Casos manuais

O Observado e o Veredito ficam "—" até Anderson rodar o P9.

| ID | Critério | Passos | Esperado | Observado | Veredito |
| :-- | :-- | :-- | :-- | :-- | :-- |
| C1 | A coordenação abre um passo real de um plano aberto pelo `executor.py`, sem comando digitado por Anderson | Abrir o passo pelo `executor.py open`, esperar o status e trazer a evidência | A sessão abre, o pedido segue, o `wait` devolve o status e a evidência volta ao plano | P12, em 2026-11-12: o `executor.py open --tree` abriu a `pln021-p12` (Sonnet), o executor commitou `brza-studio@c470dda` e marcou o worklog, o `wait` devolveu `feito`, o `evidence --apply` gravou o `### P12`; nenhum comando digitado por Anderson. A janela mediu mal (X12) | passa, Anderson, 2026-11-12, R10.1 (com o X12) |
| C2 | O PNG do painel conferido no chat | Publicar o painel e abrir o PNG no chat | O PNG mostra os passos, a fase, as horas e os executores, sem corte | 2026-11-12, `brza shot --width 736` → 1472×2654, tema light: os 11 passos, a fase, as horas e o estado, sem corte nem sobreposição; o executor do P9 saiu "a sessão que" (X11) | passa, Anderson, 2026-11-12, R10.1 (com o X11) |
| C3 | Um Desenho com artboards no chat, conferido pelo PNG em cada largura | Rodar uma rodada de Desenho com artboards | Um artboard por alternativa, conferido pelo PNG em cada largura | 2026-11-12: o layout do painel na largura estreita, A (a tabela de hoje) e B (cartões abaixo de 700 px), pelo `artboard.py new --frame browser --pack brza-studio`; o `shot` deu 375, 768 e 1280 em claro e escuro; o PNG pegou o B v1 com o estado na coluna do Executor, corrigido no B v2; o `new` avisou a deriva de 2 tokens do mobile, fora do `browser` | passa, Anderson, 2026-11-12, R10.1 — escolhida a B (R10.2) |
| C4 | O `plan-runner` novo só na branch do playground, e a master no do core | No playground, `git diff master workstream/playground --stat -- .claude/skills/plan-runner`; depois do `brza sync`, `git status` na master | O diff do `plan-runner` aparece só na branch do playground, e a master fica limpa | 2026-11-12: `git diff master workstream/playground --stat -- .claude/skills/plan-runner` → 39 arquivos, +10016 −259; a master com `git status` limpo, o `plan-runner` dela igual ao `core@45e6013` a menos dos `{{…}}` do molde; `brza sync --dry-run` → nada a escrever. O `brza sync` real não rodou (o classificador barrou, por mexer em recurso compartilhado) | passa, Anderson, 2026-11-12, R10.1 sem o `brza sync` real |
