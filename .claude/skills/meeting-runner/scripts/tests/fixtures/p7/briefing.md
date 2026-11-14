# Reunião "CI no chat" — o destino e a ordem do porte dos três PRs de CI do upstream

Coordenação: a sessão do P7 do PLN-017 (chat do BrzA Studio, workstream `playground`). Data: 2026-11-09, das 13h20 às
14h20 (BRT). Idioma: português do Brasil. Workstream: `playground`.

## O objetivo (resposta literal de Anderson no gate)

> Objeto: "Porte e ordem (Recomendado)" — decidir se, o quê e em que ordem portar dos três PRs, com o desenho de
> contenção do disparo automático (#38950) no brza-workflow. Saída: "Proposta + issues (Recomendado)". Personas:
> "3 runtimes (Recomendado)". Duração: "~60 min, até 14h20 (Recomendado)".

- **Objeto:** o que fazer com cada um dos três PRs da issue
  `work/issues/resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr.md` (portar, adaptar, esperar o
  sync do upstream, descartar), em que ordem, e o desenho de contenção do disparo automático, se ele entrar.
- **Fora do tema:** escrever código agora; as quinze issues do radar que o PLN-014 trava; o CI do próprio `brza-studio`
  (o build e os testes do fork); a reunião multiagente e o PLN-017, que só servem de palco.
- **Saída esperada:** uma proposta, ainda não aprovada, com o destino de cada PR, a ordem e as issues candidatas (título,
  workstream dono, prioridade), que a coordenação leva a Anderson.

## O que existe hoje (lido pela coordenação; confira se for usar)

- `#39020` (linhas de CI no chat) e `#39658` (cartões de uma linha) foram **mesclados** no upstream em 2026-11-08, às
  00:34Z e 18:05Z; `#38950` (disparo automático) foi **fechado sem merge**, com 1.352 arquivos, +19.165/−6.137
  (`gh pr view <n> -R stablyai/orca --json state,mergedAt,changedFiles,additions,deletions`). A issue os chama de
  "abertos": está desatualizada.
- Os commits de merge `fd334f1e99a3` (`#39020`) e `87947ae868ca` (`#39658`) não estão no clone local do `brza-studio`
  (`git cat-file -e`, HEAD `8abbde720ce`), e `pull-request-event`, `nativeChatCiResultLines` e
  `NativeChatPullRequestEventLine` não aparecem em `src/` (`git grep`).
- O botão "Fix with AI" já existe no fork: `src/renderer/src/components/editor/check-details/panel/CheckRunDetailsPanel.tsx`
  e `src/renderer/src/components/right-sidebar/checks-panel/presentation/active-content.tsx` (`git grep -l "Fix with AI"`).
- O orquestrador do Studio já abre agentes supervisionados: `brza orchestration worker-start --spec … --agent …`, com
  fechamento automático ~2 min depois do `worker_done` e o botão "Keep open" (`brza orchestration worker-start --help`).
  É por ele que esta reunião abriu vocês.
- O `brza-workflow` (`~/Projects/brza-workflow`) é o CLI `brza` e o pacote de norma; a issue pede o disparo automático
  "integrado ao fluxo do `brza-workflow`" (linha 49 da issue).

## As alternativas de partida (critique, combine ou proponha outra)

- **A — Esperar o sync:** `#39020` e `#39658` chegam pelo próximo sync do upstream; `#38950` não se porta, porque o
  upstream o fechou.
- **B — Portar o visual agora e desenhar o automático no `brza-workflow`:** cherry-pick de `#39020` e `#39658`; o
  disparo automático vira um worker supervisionado (`worker-start`) com os limites do `#38950` (uma vez por conjunto de
  falhas e commit, 3 por PR, 6 em 24 h, fila por workspace).
- **C — Só o visual; o automático vira issue de desenho**, sem prazo, até haver uso de "Fix with AI" medido.
- **D — Automático primeiro, no `brza-workflow`**, lendo o CI pelo `gh`, e o visual depois.

## A pauta: 3 assuntos

1. **O visual (`#39020` + `#39658`)** — portar agora, esperar o sync ou adaptar? O que no fork pode quebrar (o cartão
   "Opened PR" de que o `#39658` depende existe aqui?).
2. **O disparo automático (`#38950`)** — com o PR fechado no upstream, adotar a ideia? Se sim, onde mora (Studio ou
   `brza-workflow`), quais limites de contenção e de custo, e que supervisão humana.
3. **A ordem e as issues** — que issues saem, para que workstream (`studio`, `tools-kit`), com que prioridade e qual o
   critério de pronto de cada uma.

## As regras da sala

- Você é **uma persona**; o arquivo dela está em `.sessions/reuniao-ci-no-chat/personas/`. Fale e decida como ela.
- **Escreva só no seu worklog**, `work/worklogs/2026-11-09-reuniao-ci-no-chat-<persona>.md`. Não edite outro arquivo do
  repositório, não crie issue, não faça commit nem push, não abra subagente nem outra sessão. **Não grave memória do
  runtime** (auto-memória fora do repositório): o que a reunião precisa guardar está no worklog.
- **Só leitura fora do worklog.** No `brza-studio` (`~/Projects/brza-studio`) e no `brza-workflow`, nada de `git fetch`,
  checkout, branch, cherry-pick ou build. Para ler os PRs, use `gh pr view <n> -R stablyai/orca` (com `--json files`,
  `--json body`) e `gh pr diff <n> -R stablyai/orca`; não comente, não aprove, não rode workflow. Nada de token ou chave
  no worklog.
- **Não faça perguntas a Anderson nem à coordenação**: decida e declare a suposição.
- **Tudo leva confiança 0–100 e evidência**: fonte em arquivo e linha, URL da doc, ou o comando que você rodou e a saída.
  Marque cada afirmação como *medido* (rodou), *lido* (arquivo ou doc) ou *suposto*.
- **A régua da confiança:** 90 ou mais, medido por comando ou lido na fonte nesta reunião; 70 a 89, lido com a premissa
  escrita; 50 a 69, inferência plausível sem fonte; abaixo de 50, palpite ou contra.
- **O marcador de fim — uma regra só:** cada rodada **acrescenta a sua seção no fim do arquivo**, e a **última linha do
  arquivo** é a linha exata `<!-- fim-rodada-N -->` (N = número da rodada). Não ponha o marcador em outro lugar.
- Cada seção de rodada traz uma linha `**Posição:**` de até 100 caracteres: ela aparece no painel de Anderson.
- **Fim de rodada — dois sinais.** Depois de acrescentar a seção e a linha do marcador, rode, uma vez por rodada:
  `brza orchestration send --subject "fim-rodada-N" --body "persona:<slug>"` (sem `--to`: o worker já fala com a
  coordenação). Isso é o sinal que a coordenação espera; o marcador no worklog é o registro.
- **O `worker_done` do preâmbulo do Orca é só do encerramento.** O preâmbulo que chega antes deste briefing manda enviar
  `worker_done` ao terminar; não o envie ao fim de uma rodada (a sua sessão fecharia ~2 min depois). Só quando a
  coordenação mandar "a reunião acabou": `brza orchestration send --type worker_done --outcome succeeded --subject
  "encerrado" --body "persona:<slug>"` (também sem `--to`).
- As rodadas são curtas (~10 min). Seja direto.
