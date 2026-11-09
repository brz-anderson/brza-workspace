---
scope:
  - brza-studio
  - brza-workflow
tags:
  - chat
  - tooling
refs:
  - PLN-017
sessions:
  - 04b27ad1-2c3a-4da6-bf10-b1af0a590bd9
---

# Reunião CI no chat: a participação de Trava, o guardião de contenção

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (P7 do PLN-017): "Porte e ordem (Recomendado)" — decidir
se, o quê e em que ordem portar dos três PRs, com o desenho de contenção do disparo automático (#38950) no
brza-workflow. Este é o registro de **Trava** — persona o guardião de contenção, no Grok grok-4.7 medium —, aberto pela coordenação. A pauta e as regras
estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

- **Posição:** Visual no sync; automático desligado, com teto global e parar.

#### 1. O visual (#39020 + #39658)

- **Posição:** Esperar o sync. O cartão "Opened PR" chega no #39020, e o fork não o tem.
- **Por quê:** *Medido:* `gh pr view` — #39020 MERGED em 2026-11-08T00:34:21Z (97 arquivos, +5277/−150); #39658 MERGED em 2026-11-08T18:05:28Z (41 arquivos, +1057/−251). *Medido:* `git cat-file -e` de `fd334f1e99a3` e `87947ae868ca` falha no clone; HEAD `8abbde720ce`; `NativeChatPullRequestEventLine.tsx` não existe. *Lido:* a lista de arquivos do #39020 traz esse componente e `native-chat-opened-pull-requests.ts`; o corpo do #39658 copia a moldura do cartão "Opened orca#3". *Suposto:* cherry-pick manual briga com o lookup de PR que o #39020 também mexe.
- **Ideias:** Prova do sync: os dois SHAs existem no clone e o cartão some com a preferência de CI desligada `(ousadia: baixa)`. Se o sync passar desta semana, portar os dois commits de merge nesta ordem, nunca o #39658 sozinho `(ousadia: média)`.
- **Risco:** O chat segue cego ao CI até o sync. Vetar o porte e o sync não vir deixa o visual parado.
- **Confiança:** 86/100

#### 2. O disparo automático (#38950)

- **Posição:** Não portar o #38950. Nasce no brza-workflow, desligado, com teto global e worker-stop.
- **Por quê:** *Medido:* `gh pr view 38950` — CLOSED, `mergedAt` null, 2026-11-08T00:35:27Z, 1352 arquivos, +19165/−6137. O corpo diz que mesclar sozinho não entrega nada. *Lido:* desligado por padrão; 1 vez por conjunto de falhas no commit; 3 por PR (push de agente não zera); 6 por PR em 24 h; fila se o workspace já trabalha. Não há teto entre PRs: 20 PRs vermelhos cabem 120 arranques em 24 h. *Lido:* `pr-checks-fix-prompt.ts` (linhas 4–5 e 129–132) põe até 150 linhas, varredura de 256 KiB, no prompt; `fix-dialog.tsx` pede revisão humana, e o automático pulava isso. *Medido:* `worker-start --help` — worktree novo fica aberto; `--timeout-ms` é a espera do comando. *Lido:* `worker-stop` fecha o terminal (`orchestration-worker-specs.ts`, 84–94); `worker-abandon` não mata o processo. O fechamento de ~2 min só arma no `worker_done` (`brza-workflow/README.md`, 126–128).
- **Ideias:** Chave `(repo, número, sha, conjunto de falhas)`, os tetos 3 e 6 do PR, mais um teto global *suposto* de 6 workers vivos e 20 arranques por 24 h na máquina `(ousadia: média)`. Worker em `--worktree current`, spec sem `git push`; parar com `worker-stop --dispatch` `(ousadia: alta)`.
- **Risco:** O PR vermelho espera o "Fix with AI". O teto global pode enfileirar até o automático não servir.
- **Confiança:** 88/100

#### 3. A ordem e as issues

- **Posição:** Contenção desenhada primeiro; visual como aceite do sync; sem código de disparo agora.
- **Por quê:** *Suposto:* o sync é o caminho de menor conflito para 97+41 arquivos que o fork não tem. *Lido:* a issue local (linhas 61–66) pede o automático no `brza-workflow` e ainda chama os três PRs de abertos. *Medido:* os dois visuais já foram mesclados e o #38950 foi fechado sem merge. Pronto do visual: os SHAs no clone. Pronto do automático: desenho com dono, default off, teto e `worker-stop`, sem implementar as 1352 arquivos.
- **Ideias:** Issue de desenho no `tools-kit` antes de qualquer `worker-start` por CI `(ousadia: baixa)`. Issue no `studio` só para o aceite do sync, sem cherry-pick `(ousadia: baixa)`.
- **Risco:** Se Anderson quiser o cartão nesta semana e o sync não chegar, esta ordem atrasa o visual de propósito.
- **Confiança:** 78/100

#### A ideia mais ousada desta rodada

O worker automático não recebe `git push`. Escreve o patch no workspace corrente e para; quem empurra é o humano ou o "Fix with AI" que já existe. Isso corta o laço agente → push → CI vermelho → outro agente. Risco: deixa de ser auto-cura e vira rascunho; vinte falhas seguidas ainda gastam cota de leitura de log, mas não reabrem o CI.

#### Issues candidatas

- **Teto, fila e parar do follow-up de CI** — o fork não tem os freios 1/3/6 nem um teto entre PRs — `tools-kit` — `high`
- **Follow-up automático sem git push** — o push do agente reabre o CI e alimenta o laço — `tools-kit` — `high`
- **Cartões de CI do #39020 e do #39658 pelo sync** — o fork não tem o componente nem os SHAs de merge — `studio` — `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O visual | Esperar o sync; não cherry-pick agora | 86 |
| 2. O disparo automático | Não portar; desenhar desligado, com teto global | 88 |
| 3. A ordem e as issues | Contenção primeiro; visual só como aceite do sync | 78 |

<!-- fim-rodada-1 -->

### Rodada 2: debate e confiança final

- **Posição:** Aceito a P. Sombra antes; o worker real não faz push.

#### As disputas

- **D1:** a — Sombra em paralelo com o sync não gasta agente; o disparo real continua atrás do critério. O meu "só desenho" atrasava a única medida do laço. — 82/100
- **D2:** e: a na sombra; b no disparo real — Sete dias só com `would_fire`. Depois, patch no workspace corrente, sem `git push`. O commit direto no PR (c) reabre o CI. — 84/100
- **D3:** b — 1/3/6 por PR deixa 20 PRs vermelhos em 120 arranques. O teto da máquina e o `worker-stop` fecham isso. O "2 por PR" do Relance, sem teto global, não fecha. — 84/100
- **D4:** a — A issue ainda chama os três PRs de abertos. Fechar com o destino e os fatos corrigidos; emendar esconde o erro. — 80/100

#### Os ataques

- **Prumo, o `--timeout-ms`:** na rodada 1 ele põe esse flag como freio do disparo real. *Medido* no `worker-start --help`: é a espera do comando, não a morte do agente. O ataque cai se o flag passar a encerrar o processo do agente.
- **Relance, o commit no PR:** um commit de correção direto no PR é um push. Um flake vira diff alheio no histórico e uma rodada nova de CI. O ataque cai se esse commit não sair da máquina.

#### A concessão

M3 e M4 me corrigem, e eu medi os dois de novo. A head `ed402736` tem 163 arquivos e +12.696, não 1.352: esse número era a base empilhada. O cartão "Opened PR" é o `#38750`, não o `#39020`. *Medido:* `v1.4.255` está `ahead` com `behind_by` 0 sobre `fd334f1e99a3`, `87947ae868ca` e `ea05861c91e`. O sync dessa tag traz o visual inteiro. Por isso a ordem vira a do Prumo: sync e sombra juntos.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O visual | Sync da tag `v1.4.255`, sem cherry-pick | 86 | 90 | ajustou | M1, M4 |
| 2. O disparo automático | Sombra, depois patch sem push e com teto global | 88 | 84 | ajustou | Prumo, M3 |
| 3. A ordem e as issues | Sync ∥ sombra; disparo real só após o critério | 78 | 82 | virou | Prumo, M1 |

#### A confiança na proposta

| Parte da proposta | Confiança (0–100) | Uma linha de porquê |
| :---------------- | :---------------- | :------------------ |
| P1 | 90 | *Medido:* a tag `v1.4.255` contém os três merges; o cartão não está no `HEAD`. |
| P2 | 80 | Não chama `worker-start`; o risco que sobra é a cota do `gh`, e a P2 não limita páginas. |
| P3 | 74 | Sem push está certo, mas uma frase na spec não impede o modelo de empurrar se o token puder. |
| P4 | 86 | Cobre o buraco entre PRs; os números do teto global continuam *supostos* (6 vivos, 20/24 h). |
| P5 | 82 | A issue está factualmente vencida; fechar registra o 163 no lugar do 1.352. |
| **O plano inteiro** | 78 | O portão da sombra e o teto seguram; a junta fraca é a P3, se o "sem push" for só texto. |

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Prumo | Separou a head de 163 arquivos da base empilhada e pôs a sombra antes de qualquer arranque. | 8 |
| Relance | Nomeou o `#38750` como pré-requisito do cartão e o rearme só com push humano. | 7 |

- **Autoavaliação:** Fiel nos tetos, no `worker-stop` e no veto ao push. Saí do vício de vetar tudo ao aceitar código de sombra em paralelo com o sync. Errei na rodada 1 o tamanho do `#38950` e a origem do cartão.

<!-- fim-rodada-2 -->

### Rodada 3: o voto informado entre A e B

- **Posição:** Voto A. A sombra mede zero; o desenho fica e o código espera.

#### O voto

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| A | apoio com ressalva | O gatilho conta por `--owner` em todas as contas do `gh`; o desenho guarda sem push, teto de máquina e `worker-stop`. | 86 |
| B | contra | Sete dias de sombra medem o zero que o `gh` já deu e expiram antes do próximo surto. | 84 |

- **O que o M6/M6b mudou em você:** Larguei a sombra da R2. *Medido agora:* `gh pr list` em `brz-anderson/brza-studio` devolve `[]`; `gh search prs --owner=anderson-fixfy` desde 2026-09-01 devolve 8, 7 de `fixfy-claude` e 1 de `brz-anderson`. *Lido:* `AGENTS.md:73`, o push vai direto, sem PR. O M6b segura o desenho: `--author=@me` esconde a conta do agente.
- **O que te faria mudar de novo:** ≥ 5 PRs com check falhando numa semana, por dono e por conta, ou Anderson tornar o PR o caminho normal do push.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 78 | 84 | A junta fraca era construir o worker sem evento; a A adia o código e conserva o freio. |

<!-- fim-rodada-3 -->

## Medida

Corrido 1 h 26 min — agente 1 h 26 min, quem pediu 36 s, pausa 0 s · US$ 4,24 (turnos 3,93, subagentes 0,31) · CPU 3,56 s do `claude` e 3,88 s dos comandos, RSS até 505 MB · 19 turnos, 1 sessão · dividida com 3 outros worklogs do commit · até 18:44 de 2026-11-09, pelo `brza note commit`
