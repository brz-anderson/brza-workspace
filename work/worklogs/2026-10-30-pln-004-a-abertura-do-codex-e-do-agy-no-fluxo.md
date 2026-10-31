---
scope:
  - workspace
---

# O PLN-004: a abertura do Codex e do agy no fluxo

O pedido de Anderson, em 2026-10-30, no chat do BrzA Studio, na sessão `brza-workspace-80`: "vamos integrar o `codex` e
o `agy` ao nosso fluxo de trabalho". Lá fechou a rodada 1 — destino, escopo, partida e identidade — e o número foi
reservado na `master` (`233ea9a`). O plano é o
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md).

## O que se fez

- **O `git merge master`** neste worktree, para trazer a reserva do número.
- **A abertura do plano**, na sessão `workspace`: o frontmatter em `phase: interview`, o `Retomar`, o Pedido com as
  quatro frentes da R1.2, a Cobertura em rascunho, o Fora de escopo e a R1, gravada como foi respondida na sessão de
  origem, sem perguntar de novo.
- **O levantamento do PLN-011 da Fixfy**, pelo `collector`, por peça, com o agregado no scratch da sessão; deu oito
  pontos sem lastro.
- **A rodada 2**, da base e da identidade: função e wrapper; as skills espelhadas em `.agents/skills/`; a sonda da
  identidade antes do desenho; o `.codex/hooks.json` versionado, com revisão por worktree.
- **A rodada 3**, dos papéis, da memória, da medição e da delegação: o bloco de memória no prompt do papel, com o
  runtime registrado (contraproposta de Anderson); o `tools` traduzido no `agy`; a medição portada com US$; a delegação
  reduzida.
- **A rodada 4**: o runtime em `metadata.runtime` no arquivo e no evento `memory`; as três sondas antes do Desenho.
- **As sondas**, pelo `collector`, num repositório descartável do scratch: o Codex comita no worktree com
  `writable_roots` e sem rede; o `agy` não comita; o `tools:` do `agy` aceita as duas famílias de nomes; o
  `guardian_review` não entra no pai. Uma primeira chamada, que permitia `--dangerously-bypass-hook-trust` no
  repositório descartável, foi barrada pelo classificador e saiu sem a flag.
- **A rodada 5**: o `agy` não comita; o `guardian_review` com linha própria ligada ao pai; o wrapper do Codex libera o
  `.git` do worktree, e o push pede aprovação.
- **Um defeito do `~/.zshrc`**, achado nas sondas: o `fixfy_where` responde `root` em qualquer cwd quando a
  `FIXFY_WORKSPACE` está vazia (`~/.zshrc:17`). Entra no desenho das funções novas.
- **O rascunho do Desenho**, pelo `designer`, no scratch: D1 a D14 e a ordem de execução, com 8 pontos para rodada.
- **A rodada 6**, no chat, a pedido de Anderson: as sondas que sobraram agora; as skills por symlink; o `brza tree`
  liga `.codex/` e `.agents/` no brza-studio; o gerador dos papéis no `brza agents --write|--check`.

## O que ficou

- **O custo e o "se paga" das opções da R1** ficaram na sessão `brza-workspace-80`; o plano grava as opções e as
  respostas.
- **O próximo:** as sondas da R6.1, com um `/hooks` de Anderson, e a rodada 7; depois, o Desenho gravado em
  `PLN-004-design.md`.

## Fora do workspace

- **O `agy` se atualizou sozinho de 1.4.8 para 1.4.12** durante o levantamento, pelo auto-updater disparado nas chamadas
  de ajuda e listagem do `collector` (`~/.gemini/antigravity-cli/updater/update_status.json`: "Update successful").
  - Risco: o formato do transcript e os nomes das ferramentas podem mudar entre o que o levantamento leu e o que o
    desenho usa.
  - Estado: ativo; `agy --version` → `1.4.12`.
  - Como desfazer: reinstalar o `agy` 1.4.8; o updater volta a subir a versão se não for desligado.
- **A confiança do repositório descartável das sondas, no `~/.codex/config.toml:266-267`**: o `codex exec` gravou
  `[projects."…/chat-scratch/f9a99dc712d9b2b01373911a721bf604/sondas/repo"] trust_level = "trusted"`.
  - Risco: nenhum além de uma entrada morta quando o scratch sumir.
  - Estado: ativo.
  - Como desfazer: apagar as duas linhas.
- **Os rollouts das sondas**, em `~/.codex/sessions/2026/10/30/` — `rollout-2026-10-30T22-21-12-01a18f8b-…`,
  `…22-22-12-01a18f8c-…`, `…22-23-10-01a18f8d-…`, `…22-33-58-01a18f97-9257-…` (pai) e `…22-33-58-01a18f97-93eb-…`
  (guardian) —, com os `state_5.sqlite`, `thread_history_1.sqlite`, `logs_2.sqlite`, `session_index.jsonl` e
  `queue_1.sqlite` atualizados.
  - Risco: aparecem no histórico do Codex e numa medição que varra os rollouts.
  - Estado: ativo.
  - Como desfazer: `codex delete <id>` em cada um.
- **Um `codex plugin marketplace upgrade`**, rodado pela função `codex` da Fixfy na primeira chamada das sondas, por
  causa do `fixfy_where` com a `FIXFY_WORKSPACE` vazia.
  - Risco: o marketplace da Fixfy no `~/.codex/plugins` atualizado fora de hora; o efeito não foi conferido.
  - Estado: ativo.
  - Como desfazer: nada a desfazer, salvo se a Fixfy precisar da versão anterior.
- **Os transcripts das sondas do `agy`**, em `~/.gemini/antigravity-cli/brain/` — `00feb094-…`, `9eacb174-…`,
  `93f949d7-…`, `cc301532-…`, `b821b81b-…`, `b1db9c6b-…`, `de28153a-…` e `d20b8a24-…` —, mais o `conversations/`, o
  `conversation_summaries.db` e os logs.
  - Risco: aparecem no histórico do `agy` e numa medição que varra o `brain/`.
  - Estado: ativo.
  - Como desfazer: apagar as oito pastas.
