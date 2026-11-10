# O fluxo principal — abrir, entrevistar, planejar

Abrir, entrevistar, desenhar e planejar, nesta ordem, e no `PLN` cada uma pode ser o ponto em que o plano para por uma sessão. O que decide a
ordem é que cada etapa depende da anterior: não há passo sem desenho quando o gatilho do Desenho vale, e não há desenho
sem saber o que foi pedido. Antes delas, os Passos 1 e 2 da `SKILL.md` já disseram que é plano e onde ele mora.

**No destino worklog, nada vai a `work/` antes do aceite.** Plano recusado ou reescrito antes do aceite não entra no
worklog: o rascunho e as rodadas ficam na sessão — no scratchpad, para sobreviver a uma compactação da conversa — e
entram junto com o plano aceito, na seção datada que o abre. No `PLN`, cada etapa vai ao plano quando fecha.

## Abrir

1. **Confirme que é plano e onde ele mora**, pelos Passos 1 e 2 da `SKILL.md`.
2. **Resolva o nome.** No `PLN`, `brza note plan-open <assunto-em-kebab> --title "<H1 sem o PLN-NNN>" --description
   "<uma frase>"` reserva o número no índice da `master`, mesmo com outra sessão abrindo plano junto, e imprime o
   `PLN-NNN` e o caminho; o plano se grava no worktree do workstream da sessão. No worklog,
   `AAAA-MM-DD-assunto-em-kebab.md`.
3. **Escreva o frontmatter, o `Retomar`, o `## Pedido` e o `## Worklogs`** pelo molde, com o pedido nas palavras de quem
   pediu e a linha da sessão que abre. `phase: interview` quando há rodada a fazer; `phase: design` quando a origem já
   traz o requisito fechado e falta o como; nas duas, `status: open`, o `origin` da origem e o `origin_ref`, salvo com
   `origin: request`, que não o leva. No worklog, o plano aceito não leva frontmatter nem `Retomar`.
4. **Rascunhe a Cobertura e o Fora de escopo** com os itens do pedido: uma linha por item, com o critério de aceite, o
   passo e o teste.
5. **Grave**, pela seção "Quem grava" da `SKILL.md`. No `PLN`, a abertura vai já: é ela que reserva o número.

## Entrevistar

A entrevista fecha as lacunas antes de alguém escrever. **Até cinco rodadas por lacuna**; marcador no texto é o último
recurso, não o primeiro. As rodadas seguem "Como perguntar", na `SKILL.md`.

- **Levante antes de perguntar.** O que o repositório e as notas já respondem não se pergunta: leia o código do
  `brza-studio`, as decisões de `work/decisions/` e os planos vizinhos, e leve a inferência ao texto, com a fonte, como
  primeira opção a confirmar. Levantamento pesado vai a um subagente (o laço da `SKILL.md`).
- **O que costuma faltar** num pedido de app: o comportamento nos dois sistemas (macOS e Windows) quando importa, o que
  acontece sem rede ou com o agente parado, a referência visual, o padrão ligado ou desligado, e o que fica de fora.
- **Critério de aceite que falta é derivado aqui como proposta**: o critério é uma frase que se confere — o que se vê ou
  o que o teste afirma —, e Anderson confirma antes de ele entrar na Cobertura.
- **Cada rodada vai ao plano ao fechar**, com o "Apresentado antes", cada opção com o custo e quando se paga, e a
  resposta. Resposta em texto livre vai entre aspas, com a leitura que você fez dela e o que acontece em seguida.
- **Grave pelo `round_log.py`**, não à mão: escreva a rodada em JSON (a forma está no docstring do script e em
  `PLN-NNN-design.md` do PLN-021, D6) e rode `$S/round_log.py PLN-NNN --from rodada.json --dry-run`, leia, e rode sem o
  `--dry-run`. Ele numera a rodada pelo maior `### Rodada` + 1, escreve as opções no formato do molde, põe
  **Decidido — …** só quando há opção escolhida sem texto livre, e marca "→ reaberta em RN.k" na pergunta que `reabre`
  cita. A resposta em texto livre vai em `literal`, sem `escolhidas`: ela não é decisão até a rodada seguinte fechar.

Ao terminar, devolva em uma lista o que continua aberto, separado em **estrutura** (bloqueia o desenho) e **texto**
(vira marcador no plano).

## Desenhar

Quando o gatilho do Desenho vale, a etapa está em `references/design.md`: o Terreno, os itens `D`, os consultores e a
rodada das alternativas, com os artboards de tela pela `screen-artboards`.

## Planejar

1. **Derive os passos dos itens `D`**, cada um citando o que executa. Sem Desenho, siga a ordem do pedido.
2. **Escolha a forma de cada passo**: detalhada quando toca código — os arquivos, o porquê que o `D` não diz, os
   subpassos com o teste que falha antes, o comando e o commit, a linha de evidência —; curta quando é uma rodada ou um
   registro. **Código no passo é instrução, não fonte**: o trecho que o passo pede — a assinatura, o teste que falha
   antes, o corpo quando o `D` o fixou — vale até o commit que o fecha, e dali em diante o disco é a verdade.
3. **Nomeie o executor**: a coordenação, para o que é nota e rodada; **uma sessão executora**, aberta pelo
   `executor.py open`, para o passo de código — no `brza-studio`, num worktree em `.worktrees/` que o `--tree` cria, na
   branch `<tipo>/pln-NNN-pN`, uma sessão por passo (`plans/README.md`, "Branch") —, para o protótipo e para o passo
   longo do próprio workspace; um subagente (`Agent`), para leitura, rascunho e o passo curto que cabe numa devolução;
   **Anderson**, para o que só se prova no aparelho dele. A linha `Executa` diz qual: `executor: sessão (executor.py)`,
   `executor: implementer`, `executor: a coordenação`, `executor: Anderson`.
4. **Feche a Cobertura**: toda linha com passo e teste, no nível que prova o critério — unidade, ou conferência manual no
   app. Linha da Origem leva o item do pedido (`Pedido 5`) ou a rodada (`R3.2`).
5. **Escreva o que tem gatilho, quando ele vale**: os Pré-requisitos como assinatura, as Restrições particulares deste
   trabalho, a Janela quando há prazo — meta, prazo e os cortes previstos —, e a Regressão quando o trabalho altera
   comportamento que já existe — as duas seções estão no molde. **A estimativa em horas não tem gatilho: todo passo que
   executa algo** — código, documento, protótipo, revisão — **leva a linha `Estimado`**, e as três horas do frontmatter
   são somadas dela. Passo de rodada ou "a pedido" não leva.
6. **Leve o corte a uma rodada** — aceitar, juntar, dividir — e só então grave. **A opção que aceita é o aceite do
   plano**, com a data da rodada; frase de aprovação na conversa conta igual, citada. O commit fecha a cada passo verde,
   então o corte em passos é também o corte em commits.

Antes do aceite, rode `$S/plan_state.py PLN-NNN`: passo sem `Executa D…`, `D` sem origem e horas que não somam
aparecem ali, e o aceite não vai com problema aberto. `$S/plan_state.py PLN-NNN --fix` escreve as três horas.

`ready: sim` quando todo pré-requisito existe em disco. No `PLN`: `phase: execution`, `status: in_progress`. No destino
worklog, o aceite abre o worklog com o plano dentro, sem frontmatter.
