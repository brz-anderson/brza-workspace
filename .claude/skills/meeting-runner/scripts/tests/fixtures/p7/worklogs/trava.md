# Reunião CI no chat: Trava

## O que foi dito

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
