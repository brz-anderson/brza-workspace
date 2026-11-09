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

# Reunião CI no chat: a participação de Prumo, o cético medidor

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (P7 do PLN-017): "Porte e ordem (Recomendado)" — decidir
se, o quê e em que ordem portar dos três PRs, com o desenho de contenção do disparo automático (#38950) no
brza-workflow. Este é o registro de **Prumo** — persona o cético medidor, no Claude claude-opus-5-5 xhigh —, aberto pela coordenação. A pauta e as regras
estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

- **Posição:** visual pelo sync, não por cherry-pick; automático só em modo sombra no `brza-workflow`.

Os números abaixo saíram nesta rodada, das 13h25 às 13h35. A fonte de cada um é o comando citado. O clone do
`brza-studio` está em `8abbde720ce`, de 2026-11-06, e nada foi baixado.

#### 1. O visual (#39020 + #39658)

- **Posição:** A, esperar o sync: o cherry-pick não é de 2 PRs, é de uma cadeia de 4 PRs mais arquivos órfãos.
- **Por quê:**
  - *Medido*, `gh pr view --json files` cruzado com `git cat-file -e HEAD:<path>`: o `#39020` tem 97 arquivos (+5.277/−150), e 47 não existem no fork. O `#39658` tem 41 (+1.057/−251) e 16 ausentes: 3 nascem no `#39020`, e 13 vêm de outros commits do upstream, entre eles dois arquivos que o PR edita e o fork não tem.
  - *Medido*, `git grep NativeChatOpenedPullRequestCard`: o cartão "Opened PR" **não existe** no fork. Ele vem do `#38750` (28 arquivos, +1.856, mesclado em 2026-11-06T10:26Z) e do `#38999` (5 arquivos). Já está no `upstream/main` local, `c5383afb6cb`.
  - *Medido*, `gh api compare`: o merge-base do fork é `7634d08f743`, de 2026-11-05. O upstream está 523 commits à frente até o `#39020` e 714 até o `#39658`.
  - *Medido*, `git diff --name-only <merge-base> HEAD`: dos 133 caminhos dos dois PRs, o fork só mexeu em 5, como os `en.json` e `NativeChatMessageList.tsx`. Por isso o sync tem pouca superfície de conflito nesse trecho.
- **Ideias:**
  - Antes do sync, rodar `git merge-tree --write-tree HEAD 87947ae868ca` para contar os conflitos sem tocar no worktree. Depende de um `fetch` que esta reunião não pode fazer (ousadia: baixa).
  - Pronto do sync = `git grep -l NativeChatPullRequestEventLine src mobile` não vazio, mais o vitest dos 5 arquivos que o fork mexeu (ousadia: baixa).
  - Se o `merge-tree` der mais de 10 conflitos, recuar para a cadeia `#38750 → #38999 → #39020 → #39658` num worktree descartável e medir de novo (ousadia: média).
- **Risco:** o visual fica refém de um sync de 714+ commits. O fork, com 122 commits à frente, pode conflitar fora deste trecho e atrasar tudo.
- **Confiança:** 82/100

#### 2. O disparo automático (#38950)

- **Posição:** adotar a ideia, não o código. Desenhar no `brza-workflow`, primeiro em modo sombra, sem disparar nada.
- **Por quê:**
  - *Medido*, `gh pr view 38950`: a base era `brennanb2025/chat-pr-card-ci-lines`, a branch do `#39020`, que hoje dá 404. O PR fechou às 00:35:27Z, 66 s depois do merge do `#39020` (00:34:21Z), com um único comentário, do coderabbit. *Suposto (70):* foi um fechamento mecânico de PR empilhado, não uma rejeição.
  - *Medido*, `gh api compare main...brennanb2025/pr-followups-ci`: a head ainda vive em `ed402736`. O diff real é de 163 arquivos (+12.696/−134), com 37 commits à frente e 830 atrás. Os "1.352 arquivos" do briefing são artefato da base velha. Há 32 arquivos em `src/main/pr-follow-ups` e 45 em `src/main/github`.
  - *Lido*: `packages/mcp/brza_mcp/limits.py:22` já tem os tetos `CEILINGS` de workspace, sessões, cota da conta e máquina, e `cycle.py:4` já chama o `worker-start`. *Medido*, `git grep statusCheckRollup|gh pr checks`: nenhum leitor de CI no `brza-workflow`.
- **Ideias:**
  - Modo sombra: um laço com `gh pr checks` grava uma linha `would_fire` em `.measurements/` por falha nova, com a chave `(pr, sha, nomes dos checks falhos)`. Dura 7 dias, sem `worker-start` (ousadia: média).
  - Acrescentar aos `CEILINGS` do `limits.py` os tetos `pr_followups`: 3 seguidos por PR, 6 em 24 h, um por chave (ousadia: baixa).
  - Ler `src/main/pr-follow-ups/` da head `ed402736` como especificação das regras de dedupe, e não como código a portar (ousadia: baixa).
- **Risco:** o modo sombra nunca se forma e vira paralisia por medição, o vício desta persona. O polling do `gh` gasta cota da API; o upstream limitou a paginação a 10 páginas (*lido*, issue, linha 39).
- **Confiança:** 72/100

#### 3. A ordem e as issues

- **Posição:** primeiro o sync (visual), em paralelo o modo sombra, e o disparo real só com o modo sombra medido.
- **Por quê:**
  - *Medido*: o visual não depende do automático. O `#39658` não toca em `pr-follow-ups/`, e o `#38950` era quem dependia do `#39020`, não o contrário.
  - *Lido*: a issue atual (linhas 16 e 62–66) chama os três PRs de "abertos" e pede "portar". Os dois fatos estão vencidos, e é melhor fechá-la e partir em duas do que editá-la.
  - *Suposto (60)*: o "Fix with AI" não tem uso medido no fork. Sem esse número, a prioridade do disparo real não passa de `low`.
- **Ideias:**
  - Critério do disparo real: o modo sombra mostra pelo menos 5 `would_fire` em 7 dias e nenhum duplicado pela chave (ousadia: média).
  - O disparo real nasce sem `--keep-open` e com `--timeout-ms` (ajuda do `worker-start`, linha 46), atrás de uma chave do `brza.toml` com valor padrão `off` (ousadia: baixa).
- **Risco:** com o sync atrasado, o modo sombra mede falhas que ninguém vê no chat, e o ganho visível some.
- **Confiança:** 75/100

#### A ideia mais ousada desta rodada

Nenhuma linha de código de disparo no Studio. O follow-up automático é o `cycle.py` do `brza-workflow` chamando
`brza orchestration worker-start --spec "<prompt do Fix with AI>" --agent claude`, com os tetos do `limits.py` mais
`pr_followups`. O Studio só mostra a linha de CI, que chega pelo sync, e o trabalho de porte cai de 163 arquivos para
um leitor de `gh` mais uma regra de dedupe. **Risco:** um laço que gasta a cota de Anderson sem ninguém olhar. O
`account_quota` do `limits.py` segura o gasto, mas não segura um agente que piora o PR.

#### Issues candidatas

- **Sync do upstream até `87947ae868ca` (#39658), com o cartão de CI no chat**: traz o visual e os pré-requisitos (#38750, #38999) sem cadeia de cherry-pick. Workstream `studio`, prioridade `medium`.
- **Follow-up de CI em modo sombra no `brza-workflow`**: leitor `gh pr checks`, chave de dedupe e linha `would_fire` na medição, por 7 dias. Workstream `tools-kit`, prioridade `medium`.
- **Tetos `pr_followups` no `limits.py` e disparo real por `worker-start`, atrás de chave `off`**: só depois do critério do modo sombra. Workstream `tools-kit`, prioridade `low`.
- **Fechar a issue "Resultados de CI no chat…" e reabrir em duas**: os PRs não estão abertos e o `#38950` não se porta. Workstream `playground`, prioridade `low`.

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O visual | A: sync até #39658; cherry-pick exige #38750 + #38999 + 13 arquivos órfãos | 82 |
| 2. O disparo automático | ideia sim, código não: modo sombra no `brza-workflow` sobre o `limits.py` | 72 |
| 3. A ordem e as issues | sync e modo sombra em paralelo; disparo real só com 5 `would_fire` em 7 dias | 75 |

<!-- fim-rodada-1 -->

### Rodada 2: debate e confiança final

- **Posição:** visual pelo sync; o automático tem taxa de base zero, e não se constrói nem a sombra.

O fato novo desta rodada, *medido* às 13h40:
- `gh pr list --state all` dá **0 PRs** em `brz-anderson/brza-studio`, `brza-workflow` e `brza-workspace`.
- `gh search prs --author=@me --created=">=2026-09-01"` dá **1 PR** em 70 dias, no `anderson-fixfy/orca-fixfy`.
- `gh run list -R brz-anderson/brza-studio --limit 100` dá 96 runs `schedule` e 4 `workflow_run`. Nenhum run é de `push` ou `pull_request`, embora 34 workflows declarem esses gatilhos.
- O `AGENTS.md` confirma o fluxo: "O push vai direto, sem PR".

O `#38950` dispara em "PR's checks fail", e o `#39020` mostra a linha "in the chat that opened or pushed to a pull
request" (os títulos, *lidos* no `gh pr view`). No fluxo de hoje, os dois teriam zero eventos.

#### As disputas

- **D1:** e: o sync só. O automático vira uma issue de desenho `low` com uma trava de uso, `gh search prs --author=@me` com 5 ou mais PRs por semana. A taxa de hoje é 1 PR em 70 dias. — 82/100
- **D2:** e: nada, até a trava de uso abrir. Depois, (b) da Trava, sem `git push`. Retiro a minha (a): 7 dias de sombra mediriam 0, e dois comandos já mediram. — 80/100
- **D3:** a, no desenho e não no código. O `limits.py:22` já tem `machine` e `account_sessions` (M5), que fazem o "6 vivos" da Trava. Falta só o contador de 20 arranques em 24 h. — 68/100
- **D4:** a: fechar a issue com o destino e os fatos corrigidos. Os 0 PRs entram como o motivo do adiamento. — 90/100

#### Os ataques

- **Relance, sobre D1 e D2.** "O auto-fix primeiro porque poupa cliques à noite": com 0 PRs nos três repositórios e nenhum run de `push` ou `pull_request` no fork, os cliques poupados são zero. O commit direto no PR (D2 c) é o laço que a Trava corta. **O que derrubaria este ataque:** um fluxo de PR que esta conta do `gh` não vê, com pelo menos 5 PRs por semana com checks falhando.
- **Trava, sobre a prioridade.** Pôr `high` nos tetos e no "sem push" é contenção cara para um disparo que hoje não acontece nenhuma vez. O desenho dela é o certo, mas fica para quando abrir a trava de uso. **O que derrubaria este ataque:** uma decisão de Anderson de passar o `brza-studio` para fluxo de PR, ou PRs abertos por workers que esta medição não pegou.

#### A concessão

- **A minha própria medição me derrubou.** O modo sombra de 7 dias da R1 era o meu vício, paralisia por medição: dois comandos de `gh` medem hoje o mesmo que ele mediria, e dão zero. Larguei a P2.
- **M1 e M2 subiram o visual.** A tag `v1.4.255` traz o `#38750`, o `#39020` e o `#39658` juntos, e o fork mescla tag a cada 2 a 7 dias. Com isso, as minhas ideias de `merge-tree` e de cadeia de cherry-pick ficam sem uso.
- **Da Trava, adoto o "sem `git push`"** para quando o disparo existir.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O visual | merge da `v1.4.255` no sync de rotina; o ganho é pequeno sem PR, mas o custo é quase zero | 82 | 88 | ajustou | M1, M2 |
| 2. O disparo automático | não construir, nem a sombra; desenho `low` com trava de uso; depois sem push | 72 | 80 | virou | a medição de 0 PRs; a Trava |
| 3. A ordem e as issues | sync (`studio`), uma issue de desenho (`tools-kit`, `low`) e fechar a origem | 75 | 80 | ajustou | a medição de 0 PRs |

#### A confiança na proposta

| Parte da proposta | Confiança (0–100) | Uma linha de porquê |
| :---------------- | :---------------- | :------------------ |
| P1 | 85 | Certo e barato, por M1 e M2; prioridade `low`, porque sem PR a linha de CI não aparece |
| P2 | 25 | A sombra mediria 0 por 7 dias: `gh search prs` já mede a taxa de base em segundos |
| P3 | 35 | O conteúdo (sem push, `--worktree current`) está certo; o critério de 5 `would_fire` nunca passa com 0 PRs |
| P4 | 50 | Tetos certos, hora errada; metade já existe nos `CEILINGS` (M5) |
| P5 | 90 | Certo; acrescentar "0 PRs nos repositórios de Anderson" ao motivo |
| **O plano inteiro** | 55 | O visual e o fechamento estão de pé; o automático gasta duas issues num evento que não acontece |

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Trava | O worker sem `git push` corta o laço agente → CI → agente; e o `worker-abandon` não mata o processo | 8 |
| Relance | Achou sozinho o `#38750` como ancestral que falta; perdeu ponto no 1.352 e no nome errado do observador (M6) | 6 |

- **Autoavaliação:** fui fiel à persona ao medir a taxa de base antes de discutir os tetos. Saí dela na R1, quando propus 7 dias de sombra para medir o que dois comandos mediam.

<!-- fim-rodada-2 -->

## Medida

Corrido 1 h 26 min — agente 1 h 26 min, quem pediu 36 s, pausa 0 s · US$ 4,24 (turnos 3,93, subagentes 0,31) · CPU 3,56 s do `claude` e 3,88 s dos comandos, RSS até 505 MB · 19 turnos, 1 sessão · dividida com 3 outros worklogs do commit · até 18:44 de 2026-11-09, pelo `brza note commit`
