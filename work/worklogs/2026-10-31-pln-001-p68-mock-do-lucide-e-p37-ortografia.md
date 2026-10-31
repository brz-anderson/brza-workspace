---
scope:
  - brza-studio
date: 2026-10-31
tags:
  - chat
  - mobile
---

# O P68 e o P37 do PLN-001, o mock compartilhado do lucide e a ortografia conferida

Depois do P67, Anderson pediu o "próximo passo" duas vezes, na sessão do workstream `studio` do `brza-workspace`. A
primeira levou ao X47 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
que virou o P68. A segunda, enquanto o P68 rodava, levou à conferência do P37, aberto desde a Fixfy. A evidência
detalhada está nos passos, no plano.

## O P68 — os testes do transcript do mobile voltam a carregar

Commit `brza-studio@7be19418c8f`, pelo `implementer` (Sonnet) no worktree `.worktrees/pln-001-p68` do `brza-studio`, com
o commit e o push direto na `master` pela sessão.

- **A causa.** Desde o P43, o `brza-mobile-tool-glyphs.ts` importa 12 ícones do `lucide-react-native` que os mocks à
  mão dos sete testes do X47 não tinham, e os arquivos nem carregavam.
- **O helper.** O `lucideMock`, em `mobile/src/test-support/lucide-react-native-mock.ts`, responde a qualquer ícone em
  PascalCase com o próprio nome e aceita sobrescritas. Os sete arquivos e o do raciocínio o usam, com 194 linhas a
  menos.
- **Os dois testes expostos.** Com os arquivos carregando, dois testes antigos falharam pelo comportamento do P43: o
  `npm test` ganhava o frasco, e o `pnpm vitest run` virava "vitest — passou". Trocaram para `ls -la` e um `find` longo,
  fora das categorias do BrzA.
- **Os testes.** Antes, 7 arquivos da `transcript/` falhavam no carregamento. Depois, a `transcript/` e o teste do
  helper deram 28 arquivos e 224 passed; o `typecheck` e o `typecheck:tests` do `mobile/` deram exit 0; o
  `check:changed` ficou só com o vermelho de antes. O `rpc-recording/family-recordings.test.ts` falha em 2 casos também
  na `origin/master`, fora desta mudança.

## O P37 — as sugestões de ortografia aparecem

Fechou sem código. A primeira conferência pareceu defeito: a palavra sublinhava, e o menu do sistema trazia o "Add to
dictionary" sem sugestões. Uma sonda com o Electron 43.8.1 do `brza-studio`, fora do app, mostrou que o corretor do macOS
dá sugestões para `ortogrfia` num `textarea` e num `contenteditable`, com qualquer `lang`, mas marca `excessão` sem
sugestão. A palavra que sugeri no primeiro teste era a ruim. No reteste com `ortogrfia`, o menu trouxe "ortografia" no
topo.

## As rodadas

- **R57.1** — o próximo passo. Anderson escolheu "X47: os testes do mobile (Recomendado)".
- **R57.2** — a correção dos mocks. Anderson escolheu "Mock compartilhado (Recomendado)", contra acrescentar os nomes
  como no X46.
- **R58.1** — o que roda em paralelo ao P68. Anderson escolheu "P37.1: ortografia (Recomendado)".
- **R58.2 a R58.4** — a primeira conferência do P37: "Sublinha, mas sem sugestões", "Menu do sistema, em inglês" e "Sim,
  mas sem sugestões acima".
- **R59.1** — os dois testes expostos. Anderson escolheu "Trocar por comandos neutros (Recomendado)".
- **R59.2** — os outros ~40 mocks à mão do `mobile/`. Anderson escolheu "Sob demanda (Recomendado)".
- **R59.3** — o helper só para ícones. Anderson escolheu "Só ícones (Recomendado)".
- **R59.4** — o reteste do P37. A primeira resposta, "Sim, \"ortografia\" no topo", foi corrigida em texto livre:
  "digitei errado" e "ortografia não acusa como erro". A palavra digitada tinha sido a certa. O fechamento gravado no
  plano foi desfeito, e o reteste voltou à rodada com a palavra soletrada. Resposta: "\"ortografia\" no topo".

## A memória

O `implementer` acrescentou à `.claude/agent-memory/implementer/brza-studio-native-chat-tools.md` a pasta
`mobile/src/test-support/`, o ícone simulado como string, o baseline vazio do `typecheck:tests`, o `Reflect.get` barrado
pelo oxlint e a falta do `mobile/node_modules` no worktree novo.

## Para o tools-kit

O `brza tree` disse "install: ok (offline)", mas o worktree saiu sem o `mobile/node_modules`, e o `implementer` rodou
`pnpm install --offline --frozen-lockfile` no `mobile/`. Pertence ao workstream `tools-kit`, e não entrou aqui.
