---
name: suite-completa-uma-vez-no-merge
description: "Ao abrir várias sessões do brza-studio em paralelo, a suíte de teste completa roda uma só vez, no merge na master, pela sessão de coordenação; as sessões rodam só o alvo."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1cc6cebf-df5c-4f57-a8ad-cdddea824cf4
  modified: 2026-11-02T23:20:35.967Z
---

Quando eu abrir várias sessões em paralelo no `brza-studio`, a suíte de teste completa roda **uma única vez, no merge na
`master`**, e não em cada sessão.

**Why:** Anderson pediu em 2026-11-02, depois de eu abrir seis sessões de uma vez (pedidos 37 a 39): a suíte inteira leva
~16 min e satura a máquina (15 núcleos, dezenas de processos de vitest juntos), e rodá-la em cada sessão multiplica o
gasto sem achar mais nada. Ver [[upstream-sync-procedure]] sobre uma suíte por vez.

**How to apply:**
- No prompt de cada sessão paralela, desde o início: rode só os testes dos arquivos tocados e dos vizinhos, por caminho,
  com `--maxWorkers=2`, o typecheck do projeto que mexeu e `pnpm check:changed --base=origin/master --maxWorkers=2`
  (que seleciona só o que os caminhos pedem). Nada de `pnpm test`, vitest sem filtro ou lint da árvore inteira. A
  Evidência diz o que rodou e "suíte inteira: roda no merge, pela coordenação".
- Eu, a sessão de coordenação, rodo a suíte completa uma vez, quando todos os pushes estiverem na `master`, num
  worktree limpo de `origin/master` (nunca no checkout raiz nem com outra suíte em curso), e registro o resultado no
  worklog, comparando com a linha de base conhecida (25 arquivos vermelhos da v1.4.246 pura).
- Sessão já aberta sem a regra recebe o aviso por `brza sessions send <nome> "<texto>"`.
