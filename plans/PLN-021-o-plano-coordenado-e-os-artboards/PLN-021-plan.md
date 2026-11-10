---
status: open
phase: interview
origin: request
description: Protótipo no playground de um plan-runner com sessão coordenadora (executores dos passos, consultores em sessões, painel de andamento), scripts e references como os da meeting-runner, e uma skill própria de artboards para protótipos de tela web, mobile e desktop.
ready: "não — falta o Desenho de D1 a D7"
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

- **Retomar:** R1 a R3 respondidas em 2026-11-09, com o Terreno em `/private/tmp/pln021/terreno.md` (scratch da sessão). Próximo: o Desenho de D1 (`.claude/scripts/`) a D7 (`screen-artboards`), com o rascunho do `designer` em `/private/tmp/pln021/design-draft.md` levado a rodada; as skills se escrevem pela `skill-creator`.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `playground` de 2026-11-09.

"adaptar a skill `plan-runner` para ficar mais parecido com a `meeting-runner`, com uma sessão coordenadora, com mais
scripts de apoio e referencias;

adicionar também a `plan-runner` - pode sugerir outra skill, se necessário - uma rotina para criação de artboards, para
protótipos de tela, tanto web quanto mobile e desktop;"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 1` (sessão coordenadora) · R1.3 | A coordenação abre a sessão executora de um passo pelo `brza sessions`, envia o pedido do passo, espera o status e traz a evidência ao plano, sem comando digitado por Anderson | a planejar | os `unittest` dos scripts (unidade); um passo real de um plano aberto (manual) |
| `Pedido 1` · R1.3 · R2.3 | Na bifurcação com 3 ou mais alternativas e escolha cara de reverter, ou a pedido, os consultores do Desenho abrem como sessões em modelos e runtimes diferentes, e as alternativas voltam lado a lado; no resto, o `Agent` | a planejar | a planejar |
| `Pedido 1` · R1.3 | O painel de andamento do plano (passos, fase, horas, executores) sai de script, como `::orca-visual`, a cada mudança de estado | a planejar | os `unittest` do painel (unidade); o PNG conferido (manual) |
| `Pedido 2` (scripts de apoio e references) | As operações mecânicas do plano saem de script, e cada operação tem a reference dela, como na `meeting-runner` | a planejar | a planejar |
| `Pedido 3` (artboards) · R1.4 · R2.4 | A `screen-artboards` gera o artboard de tela em web, mobile e desktop, com o pacote de tokens do projeto e a moldura do aparelho, confere pelo PNG em cada largura, e o Desenho do plano a aciona | a planejar | os `unittest` do script (unidade); a rodada de um Desenho real com artboards (manual) |
| R2.4 (tokens) | O pacote do `brza-studio` sai por script do `main.css` e do `mobile-theme.ts`, e o script avisa a deriva; o pacote neutro cobre o projeto sem tokens | a planejar | os `unittest` da extração (unidade) |
| R3.1 (protótipo com o nome) | O `plan-runner` novo vive só na branch do playground, com o mesmo nome; a master segue com o do core | a planejar | `git diff master workstream/playground --stat -- .claude/skills/plan-runner` só no playground; `git status` limpo na master depois do `brza sync` (manual) |
| R2.2 (os scripts) | `plan_state.py`, `step_request.py`, `round_log.py` e `close_check.py` existem, com testes, e a skill manda usá-los no lugar da conferência à mão | a planejar | os `unittest` de cada script (unidade) |
| R3.2 · R3.3 (código comum) | `.claude/scripts/` guarda o mapa de sessões, os verbos do `brza sessions`, a medição por janela e o salvar visual com PNG pelo `brza shot`; a `meeting-runner` importa de lá | a planejar | os 323 testes da `meeting-runner` e os de `.claude/scripts/` (unidade) |

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

## Worklogs

- 2026-11-09 — aberto; R1 respondida (destino, protótipo no playground, as três frentes de coordenação, skill própria
  de artboards); Terreno do `collector`; R2 (os quatro scripts, consultores só em decisão cara, pacote de tokens por
  projeto) e R3 (o nome `plan-runner` na branch, `.claude/scripts/`, a `meeting-runner` migra).
  [A entrevista do PLN-021: o plan-runner com sessão coordenadora e a skill de artboards](../../work/worklogs/2026-11-09-a-entrevista-do-pln-021.md)
