---
scope:
  - brza-studio
  - workspace
---

# PLN-007: os tokens da marca e o aviso de pergunta azul

O pedido de Anderson, em 2026-11-02, na sessão `pln-007-brand-tokens`: "Execute o P3 do PLN-007: os tokens da paleta da
marca BrzA e o aviso de pergunta em azul", de uma sessão de código do `brza-studio`, parando antes do merge. Depois, na
mesma sessão: "merge na `master` e corrigir o `path-literal-ratchet`", e "registre o plano e faça o push".

O P3 do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md).

## O que se fez

A conferência antes deu 2 usos de `agent-question: var(--color-orange` e 0 de `--brand-gradient`. O D4 entrou em
`main.css`: os `--brand-*` constantes no `:root`, o `--brand-text` e o `--brand-sheen` por tema, os `--color-brand-*` no
`@theme inline`, e o `--agent-question` no `blue-700`/`blue-800` no claro e no `blue-400`/`blue-300` no escuro. O papel
`brand-*` foi à tabela de `docs/styleguide/color.md`, e a exceção ao `docs/STYLEGUIDE.md:5`. Os `--chat-composer-focus-*`
que o D4 mostra como linha de contexto não existiam no arquivo e ficaram para o D5, no P5.

O `fixtures:shot native-chat/NativeChatQuestionCard` do plano não mostra o azul: o cartão de pergunta do chat não usa o
`--agent-question`. O azul foi conferido no `AgentStateDot:allStates` a 2x, nos dois temas, no ícone de "Requer
atenção" e no de "Aguardando entrada".

O `check:changed` não achou `origin/main` e rodou com `--base=master`. Falhou o `path-literal-ratchet`, e a falha já
estava na `master`: o `computer-e2e.yml` e o `pr.yml`, do sync do v1.4.246, apontavam para
`src/main/providers/local-pty/`, uma subpasta que a árvore não tem. Anderson pediu o conserto, e os dois caminhos
passaram ao layout plano. No `pr.yml` o caminho velho também deixava o vitest do passo de shell real sem arquivo de
teste. Com isso, os 21 checks passaram.

O merge na `master` foi fast-forward, e o push foi direto, como a norma manda no `brza-studio`.

Depois do registro, Anderson pediu seguir com o que ficou aberto. O app dev subiu fora da tela, com perfil temporário e
CDP, e os tokens foram lidos no app vivo: nos dois temas o `--agent-question` e o `--agent-question-text` resolvem para o
azul do D4, e a classe `text-agent-question` pinta essas cores. O app e o perfil foram encerrados e removidos. O worktree
`.worktrees/pln-007-brand-tokens` e a branch `feat/pln-007-brand-tokens` foram removidos, a branch já contida na
`master`.

## O que ficou

- A conferência com uma pergunta de agente de verdade no app, que a Regressão do plano pede para o aviso azul: não foi
  feita. O perfil novo não tem projeto nem terminal e a store não está exposta; dá-la pede um workspace e um agente
  rodando, que gasta a conta de Anderson, ou um evento de hook sintético num painel existente.
- O texto do passo 3 do P3 manda o `NativeChatQuestionCard`, que não exercita o token; o P5 e a Regressão que citam "o
  `fixtures:shot` do P3" devem usar o `AgentStateDot:allStates`.

## Fora do workspace

No `brza-studio`, na `master`, em `a3a89e3aaf5` (push em `origin/master`):

- `41bfe6d1d4e` — `feat(brand): BrzA brand tokens and a blue agent-question (PLN-007 P3)`.
- `a3a89e3aaf5` — `ci: point the local-pty workflow paths at the flat providers layout`.
