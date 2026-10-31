---
scope:
  - workspace
---

# O porte das skills da Fixfy para o workspace

Anderson pediu, na sessão `workspace`: "vamos avaliar o porte das skills da `Fixfy` usando a
/skill-creator:skill-creator". A `skill-creator` tinha acabado de entrar no escopo local do worktree, como registra o
[O PLN-004: as sondas da R6 e o Desenho do Codex e do agy](2026-10-31-pln-004-as-sondas-e-o-desenho.md).

## A triagem

O `collector` leu as 16 skills de `~/Projects/fixfy/fixfy-plugin/skills/` contra a norma e as skills daqui. Tamanho é o
`SKILL.md` mais as referências, em linhas.

| Skill | Classe | Argumento | Tamanho |
| :---- | :----- | :-------- | :------ |
| `plan-runner` | já portada | O `diff` não acha resíduo da Fixfy; mudaram as pastas, o `brza note commit`, o critério de plano e a delegação por papel | 229 + 461 |
| `agent-instructions-writer` | adaptar | Este workstream edita a norma o tempo todo, e nenhuma skill guia isso; as invariantes servem, o roteamento por constituição e `docs/` não | 91 + 146 |
| `review-writer` | adaptar em parte | A forma do achado já está no `plan-runner` (`references/conduct.md`); sobram a confiança, o achado falso e a ordem de revisão | 159 + 471 |
| `end-day-runner` | não serve | O `close-task` cobre o principal; sobram dois furos | 166 |
| `git-runner` | não serve | PR, Jira e submódulo; aqui o push é direto e o `brza note commit` faz a mecânica | 161 + 318 |
| `adr-writer`, `constitution-writer`, `manual-writer`, `migration-writer`, `spec-writer`, `readme-writer` | não serve aqui | Pressupõem o `docs/` de um repositório de código; a decisão daqui é `work/decisions/` e a norma de topo, o `AGENTS.md` | ~6.000 no total |
| `fixfy-context`, `atlassian-runner`, `sprint-runner`, `prototype-creator`, `token-drift-checker` | não serve | Presas ao Jira, ao Figma, ao design system ou ao mapa de repositórios da Fixfy | — |

A norma não diz o formato da mensagem de commit, embora a prática seja `docs:`, `fix(brza):` e afins; ficou fora da
rodada.

## As rodadas

- **O que se adapta:** "Instruções + 3 itens" — o `agent-instructions-writer` como skill, e do `review-writer` só os
  itens que vão ao `reviewer.md` e ao `conduct.md`, sem skill nova. O rótulo da opção dizia três itens e a descrição,
  dois; na rodada seguinte, sobre quais, Anderson respondeu: "rode 3 subagents em paralelo, cada um defendendo o porte
  de cada um dos três".
- **Como medir:** "3 tarefas, com e sem" — a mesma tarefa com a skill adaptada e sem ela, pela `skill-creator`; e as
  três tarefas propostas, "Servem".
- **As skills de documento:** "essas vão ao `tools-kit` para um possível plugin", registrado como "Issue no tools-kit"
  em [As skills de documento da Fixfy num possível plugin do BrzA](../issues/skills-de-documento-da-fixfy-num-plugin.md).
- **Os furos do `end-day-runner`:** "Issue", em
  [O close-task não varre o work/notes/ do dia nem relata os worktrees sujos](../issues/close-task-sem-varredura-de-notes-nem-worktrees-sujos.md).

## Os três itens do review-writer

Três `designer` defenderam, em paralelo, um item cada. Nenhum achou caso em que a falta custou algo, salvo a ordem de
revisão: a lente da falha silenciosa teria pegado o `brza tree` que dizia `ok` sem instalar o `mobile/` (`f87357d`). O
papel `reviewer` nunca rodou, e houve um parecer só, o do PLN-002, sem achado falso.

- **Confiança:** "Número, só texto" — de 0 a 100, com corte em 80, sem aviso no checador. O melhor argumento contra,
  do próprio defensor, era o número dito pelo mesmo modelo que escreve o achado.
- **Achado falso:** "Só no texto" — destino `→ falso`, separado de `descartado`, e a sessão refaz a evidência antes da
  rodada.
- **Ordem de revisão:** "No reviewer.md", sem o "estado presente" da Fixfy, porque a norma daqui guarda medição datada
  de propósito.
- **Três revisores com foco:** "Com a frente 4", numa linha no `Retomar` do
  [PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md).
- **Os detalhes:** a `dúvida` "Sai" dos tipos de achado; a confiança vai "Antes da seta"; a lista "Não é achado" "Fica
  de fora".

O texto foi aprovado na mensagem ("1", pode aplicar) e gravado na `master` em `038c82d`: o `reviewer.md`, o
`conduct.md` e o `close.md` do `plan-runner` e o `work/README.md`. O gate do `brza-studio` virou ponteiro ao `AGENTS.md`
de lá, porque o rascunho citava um comando que não é o dele.

## A medição da agent-instructions-writer

A skill adaptada tem ~100 linhas, a partir das 237 da de lá. Três tarefas, cada uma num clone descartável, com a skill e sem ela, em Sonnet:

| Tarefa | Com | Sem | O que separou |
| :----- | :-- | :-- | :------------ |
| Registrar o plugin local na norma | 6/6 | 6/6 | Nada; diffs quase iguais |
| Revisar o `CLAUDE.md` | 5/6 | 2/6 | Sem a skill, acusou o `ListAgents` como inexistente e não estimou os tokens |
| Subir uma memória à norma | 4/5 | 4/5 | Sem a skill, o `AGENTS.md` citou `Edit` e `Bash`; com ela, a escolha anterior de Anderson não voltou à rodada |

Ao todo, 88% contra 71%, com ~+4,8 mil tokens e ~+7 s por execução. Uma execução por tarefa: o ± é entre tarefas.
O `collector` e uma execução copiaram o caminho do scratch sem o `0` final do hash; a execução parou e foi relançada
por um link curto, `/private/tmp/aiw`.

**O retorno de Anderson no visualizador**: no plugin, "a skill melhorou o resultado"; na revisão, "aqui sem a skill
ficou melhor"; na memória, "os blocos expansiveis ficaram levemente melhores com a skill". A revisão sem a skill tinha
56 linhas contra 112, e achou a configuração de usuário que carrega o `AGENTS.md` e uma frase quebrada; a com a skill
seguiu a régua como roteiro e parou em "não conferi".

**A versão 2** mandou ler o arquivo inteiro como quem vai segui-lo, com a régua como mínimo; seguir o ponteiro para fora
do repositório, só lendo; dizer o que quebra; responder às perguntas do pedido em lista; e citar a escolha anterior
que o pedido contraria. A iteração 2 deu 100% contra 87%, com ~+12 mil tokens e ~+16 s por execução. Na revisão, 8/8
contra 5/8: só a versão com a skill achou o `~/.zshrc` sem o `--agents` e o `gh` na conta `anderson-fixfy`, os dois
conferidos; a sem a skill afirmou que o `~/.zshrc` batia com o `README.md`. As outras duas tarefas empataram.

Anderson: "tudo aprovado, segue". A skill entrou na `master` em `3f55576`, em `.claude/skills/agent-instructions-writer/`.
A otimização da `description` pela `skill-creator` não rodou.

**O link curto para o scratch subiu à norma**, a pedido de Anderson ("suba o candidato a norma"), pela
`agent-instructions-writer`: no `CLAUDE.md`, um parágrafo depois da tabela de vocabulário, e a linha do scratch passou
a dizer onde ele fica no chat do BrzA Studio, que o `/private/tmp/claude-501/…` não cobria (`81a3d1b`). A memória que o
guardava saiu.

## A sessão paralela na Fixfy

Anderson pediu: "em pararelo, abra uma sessão no `fixfy-workspace`, em workstream, para fazer as medições e planejar
possíveis melhorias", e depois "abra no `BrzA Studio`". A sessão `fixfy-skills` abriu pelo `brza sessions`, em
`~/Projects/fixfy`, com o título "Fixfy: medir e melhorar as skills". A Fixfy não tem workstream; ela abriu na raiz, onde
a norma de lá grava as notas, com a ordem de abrir worktree para mudar skill e de trazer a rodada do que medir antes de
rodar. No chat do app, o `claude-brza` roda ali o `claude` puro, sem a função `fixfy_claude`: a conta é a padrão.

## Fora do workspace

- **A conta ativa do `gh` no perfil padrão**, trocada de `anderson-fixfy` para `brz-anderson` com
  `gh auth switch --hostname github.com --user brz-anderson`, como o `CLAUDE.md` promete ("O `gh` usa o perfil padrão,
  com a conta `brz-anderson` ativa"). Quem achou foi a revisão da `agent-instructions-writer`, na iteração 2 da medição;
  Anderson: "conserte".
  - Risco: a sessão aberta sem a `fixfy_claude`, como a `fixfy-skills` no BrzA Studio, usa o perfil padrão e passa a
    falar com o GitHub como `brz-anderson`; a `fixfy_claude` usa o próprio `GH_CONFIG_DIR` e não muda.
  - Estado: ativo.
  - Como desfazer: `gh auth switch --hostname github.com --user anderson-fixfy`.
- **O bloco do BrzA no `~/.zshrc` está atrás do `README.md`**: a `brza_claude` de lá não passa o `--agents`, e a
  sessão aberta pelo terminal no `brza-studio` sobe sem os subagentes por papel. A cópia foi barrada pelo classificador
  de permissões da sessão e ficou com Anderson.
  - Risco: até a cópia, o `Agent` com `reviewer`, `collector`, `implementer` ou `designer` não acha o papel no terminal
    do `brza-studio`; o chat do app não sofre, porque o `claude-brza` passa o `--agents`.
  - Estado: pendente.
  - Como desfazer: depois da cópia, o `~/.zshrc.bak-2026-10-31-brza` que o comando grava.

- **A sessão `fixfy-skills` no BrzA Studio**, em `~/Projects/fixfy`, que vai instalar a `skill-creator` no escopo local
  do checkout da Fixfy.
  - Risco: a sessão grava notas e worktrees na Fixfy, pela norma de lá.
  - Estado: ativa.
  - Como desfazer: `brza sessions close fixfy-skills`; o que ela gravar se desfaz pela norma da Fixfy.
