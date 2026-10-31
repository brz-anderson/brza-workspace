---
status: open
phase: interview
origin: request
ready: "não — faltam o Desenho e os Passos"
scope:
  - workspace
  - brza-studio
opened: 2026-10-30
owner: Anderson
tags:
  - tooling
---

# PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude

- **Retomar:** o Desenho está em rascunho no scratch da sessão `workspace` (`pln-004-design-rascunho.md`, D1 a D14), com
  as rodadas 6 a 8 fechadas e as sondas da R6.1 feitas (`pln-004-sondas-r6.md`). O próximo é o `designer` aplicar a R6
  a R8 ao rascunho e a aprovação do texto, na mensagem, antes de gravá-lo em `PLN-004-design.md`.

## Pedido

- **Origem:** pedido livre, no chat do BrzA Studio, na sessão `brza-workspace-80` ("Integrar codex e agy ao fluxo"),
  aberta na `master`, de 2026-10-30. A partida é o PLN-011 da Fixfy (R1.3),
  `~/Projects/fixfy/plans/PLN-011-claude-codex-e-antigravity-no-mesmo-ecossistema/`. Toca o
  [PLN-001](../PLN-001-o-brza-studio-generico/PLN-001-plan.md), que já marca os passos que outro runtime pode executar,
  e a issue
  [O Codex chamado pela sessão Claude aparece como subagente no chat do BrzA Studio](../../work/issues/codex-como-subagente-no-chat-do-claude.md),
  do `studio`, que se liga a este plano (R1.2).

"vamos integrar o `codex` e o `agy` ao nosso fluxo de trabalho" — Anderson, em 2026-10-30.

As frentes do pedido, pela R1.2, numeradas para a Cobertura:

1. **Base:** o adaptador no `.codex/config.toml` e em `.agents/rules/`, e as funções `codex` e `agy` para o
   brza-workspace e o brza-studio, com a identidade do `brz-anderson` (R1.4) e a `BRZA_WORKSPACE`;
2. **Papéis e memória:** o `collector`, o `implementer`, o `reviewer` e o `designer` em `.codex/agents/*.toml` e
   `.agents/agents/*.md`, gravando na memória do workstream, gerados para não divergir do `.claude/agents/`;
3. **Medição:** o `measure.py` lendo o rollout do Codex e o transcript do `agy`, com o runtime em cada linha;
4. **Delegação e sessões:** a sessão Claude manda revisão e levantamento ao Codex e ao `agy`, só leitura, e o
   `brza sessions` abre sessão Codex ou `agy` no worktree.

### Cobertura

> Rascunho: os critérios são propostas até a rodada que os confirma; o passo e o teste saem do Desenho.

| Origem   | Critério de aceite                                                                                                                  | Passo | Teste (nível) |
| :------- | :---------------------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `R1.2` 1 | o `codex` e o `agy` abertos no brza-workspace, no brza-studio e nos worktrees deles leem a norma do `AGENTS.md` pelo adaptador próprio | —     | —             |
| `R1.2` 1 | o commit feito numa sessão Codex, no worktree, sai com o noreply do `brz-anderson`, e o push vai pela chave `personal` com a aprovação de Anderson (R1.4, R5.3); o `agy` não comita (R5.1) | —     | —             |
| `R3.3`   | a medição do Codex grava o `guardian_review` numa linha própria, ligada ao pai e fora da soma dele (R5.2)                           | —     | —             |
| `R3.1`   | a memória gravada fora do Claude leva `metadata.runtime`, e o evento `memory` o carrega (R4.1)                                      | —     | —             |
| `R1.2` 2 | os quatro papéis existem nos três runtimes, gerados de uma fonte só, e a geração acusa a divergência                                 | —     | —             |
| `R1.2` 2 | o papel rodado no Codex ou no `agy` grava na memória do workstream da sessão                                                         | —     | —             |
| `R1.2` 3 | a sessão Codex e a `agy` geram linhas em `.measurements/measurements.jsonl`, com o `runtime` e o `workstream`                        | —     | —             |
| `R1.2` 4 | a sessão Claude pede revisão e levantamento ao Codex e ao `agy` sem que eles gravem no repositório                                   | —     | —             |
| `R1.2` 4 | o `brza sessions` abre uma sessão Codex ou `agy` no worktree do workstream                                                           | —     | —             |

### Fora de escopo

- **O que é só da Fixfy** — as contas `fixfy-*`, o `fixfy-plugin`, a guarda —, pela R1.3. Fica no PLN-011 de lá.
- **O código do `brza`** — o `brza sessions`, o `claude-brza` —, pela R1.1. Vai como pedido ao `tools-kit`, que o
  executa numa sessão dele.
- **O chat Antigravity do BrzA Studio.** É um servidor ACP gerenciado pelo app, que não é o `agy` e ignora o
  `agentCmdOverrides` (`brza-studio/src/main/acp/acp-launch-specs.ts:261-265`); o `agy` deste plano é o do terminal e o
  do `brza sessions`.
- **O Codex como cartão de subagente no chat do BrzA Studio.** Fica na issue do `studio`, ligada a este plano pela R1.2.

## Entrevista

### Rodada 1 — destino, escopo, partida e identidade (enviada 2026-10-30)

**Apresentado antes**, na sessão `brza-workspace-80`:
- **Os binários:** `codex-cli 0.164.0` e `agy 1.4.8` instalados. As funções `codex` e `agy` do `~/.zshrc` só tratam a
  Fixfy (`fixfy_where`); fora dela, chamam o binário puro, sem a identidade e sem a medição.
- **A norma:** neutra — o `AGENTS.md` mais um adaptador por runtime —, mas só existe o adaptador do Claude, o
  `CLAUDE.md`.
- **O que já toca o assunto:** o PLN-001 marca os passos para outro runtime
  (`workstream/studio:plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md:933`), e a issue
  `workstream/studio:work/issues/codex-como-subagente-no-chat-do-claude.md` trata o Codex chamado pela sessão Claude.
- **O precedente:** o PLN-011 da Fixfy, com as peças em `~/Projects/fixfy/.codex/` (`config.toml` com
  `developer_instructions`, `agents/*.toml`, `hooks.json`) e em `~/Projects/fixfy/.agents/` (`rules/runtime.md`,
  `agents/*.md`, `hooks.json`, `mcp_config.json`, `plugins.json`). Lá, o P4, o P5, o P8.5 e o P9 foram reabertos (R27),
  e o P13, o guia de custo por peça, não foi feito.

Respondida em 2026-10-30, na sessão `brza-workspace-80`, e trazida a este plano sem perguntar de novo. O custo e o
"se paga" de cada opção ficaram naquela sessão; chegaram aqui as opções e as respostas.

1. **Destino.** Opções:
   - PLN-004 no workspace (recomendada);
   - PLN-004 no tools-kit;
   - emenda ao PLN-003.

   **Decidido — "PLN-004 no workspace (Recomendado)".** O que é código do `brza` (`sessions`, `claude-brza`) vai como
   pedido ao `tools-kit`.

2. **Escopo**, seleção múltipla. Opções:
   - Base: adaptador e shell;
   - Papéis e memória;
   - Medição;
   - Delegação e sessões.

   **Decidido — as quatro**, como estão no Pedido. A delegação inclui um pedido ao `tools-kit` e a issue do `studio`
   ligada ao plano.

3. **Partida.** Opções:
   - portar o PLN-011 (recomendada);
   - desenhar do zero.

   **Decidido — "Portar o PLN-011 (Recomendado)".** Um `collector` levanta as peças da Fixfy, os desvios X1–X8 e os
   passos reabertos; o desenho tira o que é só de lá (as contas `fixfy-*`, o `fixfy-plugin`, a guarda).

4. **Identidade.** Opções:
   - brz-anderson, igual ao Claude (recomendada);
   - uma conta por runtime.

   **Decidido — "brz-anderson, igual ao Claude (Recomendado)".** As funções do shell exportam o mesmo
   `GIT_AUTHOR_*`/`GIT_COMMITTER_*` e o `GIT_SSH_COMMAND` do `env` do `.claude/settings.json`.

### Rodada 2 — a base e a identidade (enviada 2026-10-30)

**Apresentado antes:** o levantamento do PLN-011 da Fixfy, pelo `collector`, com o agregado no scratch da sessão
(`pln-004-levantamento-pln-011.md`). As fontes abaixo são de lá; `FX` é `~/Projects/fixfy`.
- **O Codex 0.164 lê o `AGENTS.md` do worktree e não o `CLAUDE.md` nem as `.claude/skills`** — `codex debug
  prompt-input`, com `CODEX_HOME` vazio.
- **Na Fixfy, o adaptador do Codex** é o `developer_instructions` do `FX/.codex/config.toml:9-19`, e o do `agy`, o
  `FX/.agents/rules/runtime.md:1-18`, com `trigger: always_on`. As funções `codex` e `agy` do `~/.zshrc:79-98` só tratam
  a Fixfy.
- **As sessões Codex que o app abriu em worktree do brza-studio** (3 rollouts de 2026-10-28, `originator:
  orca_desktop`) rodaram sem a norma do workspace, sem a identidade e sem a medição.
- **Os hooks do Codex só rodam depois de confiados**, por hash e por caminho (`~/.codex/config.toml:161-210`): cada
  worktree novo pede revisão (X3 da Fixfy, `PLN-011-plan.md:783`).
- **A doc do Codex não diz qual `shell_environment_policy` vale por padrão**, nem se o `.git` do worktree é gravável em
  `workspace-write`; a página `config-reference` deu 404.

Respondida em 2026-10-30, na sessão `workspace`.

1. **Por qual canal o adaptador chega ao brza-workspace e ao brza-studio.** Opções:
   - função e wrapper (recomendada): as funções `codex()`/`agy()` e um wrapper no estilo do `claude-brza` passam o
     adaptador (`-c developer_instructions`, `--add-dir`), mais `.codex/config.toml` e `.agents/rules/` no workspace —
     custo: o código do wrapper, como pedido ao `tools-kit`, e a cópia do bloco ao `~/.zshrc`; se paga: na primeira
     sessão Codex no brza-studio, onde hoje a norma não chega;
   - só os arquivos no workspace, como a Fixfy — custo: poucos arquivos; se paga: nunca no brza-studio, que fica sem a
     norma.

   **Decidido — "Função e wrapper (Recomendado)".**

2. **Como o "acionar uma skill" funciona no Codex e no `agy`.** Opções:
   - uma linha no adaptador manda ler `.claude/skills/<nome>/SKILL.md`, como a Fixfy no Codex
     (`FX/.codex/config.toml:16`) (recomendada) — custo: nenhum arquivo novo; se paga: agora, nas duas skills;
   - espelhar em `.agents/skills/` — custo: a duplicação, que a Fixfy deixou em issue aberta (`PLN-011-plan.md:363-365`);
     se paga: só com muitas skills.

   **Decidido — "Espelhar em `.agents/skills/`".** Como o espelho evita divergir do `.claude/skills/` vai ao Desenho.

3. **Medir antes se `GIT_AUTHOR_*` e `GIT_SSH_COMMAND` chegam ao `git commit` no Codex e no `agy`.** Opções:
   - sondar antes (recomendada): um commit num repositório descartável do scratch, um turno por runtime — custo: dois
     turnos curtos, ~US$ 0,20 cada no Codex (`PLN-011-plan.md:696`); se paga: antes de a R1.4 virar função do shell;
   - confiar no `env` exportado — custo: nada agora; se paga: talvez nunca, e o commit com outra identidade só se
     descobre depois.

   **Decidido — "Sondar antes (Recomendado)".**

4. **Onde moram os hooks de medição do Codex.** Opções:
   - `.codex/hooks.json` versionado no workspace, aprovado uma vez por worktree (recomendada) — custo: uma aprovação em
     `/hooks` por worktree novo; se paga: na primeira medição fechada de um workstream;
   - `~/.codex/hooks.json` global, com uma aprovação só, e o `measure.py` filtrando pelo `cwd` — custo: dispara em toda
     sessão da máquina, junto dos hooks do Orca; se paga: se a revisão por worktree incomodar;
   - `--dangerously-bypass-hook-trust` na função — custo: nenhuma revisão de hook em sessão nenhuma; se paga: nunca,
     salvo risco aceito.

   **Decidido — "Versionado, revisão por worktree (Recomendado)".**

### Rodada 3 — os papéis, a memória, a medição e a delegação (enviada 2026-10-30)

**Apresentado antes:** do mesmo levantamento.
- **Os geradores da Fixfy** — `generate_codex_agents.py` e `generate_agy_agents.py`, sobre `agent_frontmatter.py` —
  têm `--check`, que acusa divergência (`FX/fixfy-plugin/scripts/generate_codex_agents.py:93-108`). O Codex não traduz
  `tools` nem `memory` (`:13-15`).
- **Nem o Codex nem o `agy` têm campo de memória por agente**; aqui, os papéis usam `memory: project`
  (`.claude/agents/collector.md:6`).
- **O `agy` trocou os nomes das ferramentas** em 2026-10-20 (`view_file` → `read_file`, `write_to_file` →
  `write_file`, `replace_file_content` → `edit_file`); a tabela da Fixfy (`generate_agy_agents.py:34-43`) e os matchers
  do `FX/.agents/hooks.json:14-40` têm os nomes antigos.
- **O `measure.py` daqui** não tem `runtime` nem os modos `codex` e `agy`; o da Fixfy tem os dois
  (`FX/.claude/hooks/measure.py:468-701`). O Codex 0.164 grava também rollouts `guardian_review`.
- **A delegação da Fixfy** é o `FX/scripts/delegate.py`, do PLN-022, com o destino pelo `quota.py` e a conta `adm`; a
  medição dela fecha hoje, sem veredito gravado.

Respondida em 2026-10-30, na sessão `workspace`.

1. **Como o papel grava na memória do workstream no Codex e no `agy`.** Opções:
   - o gerador injeta no papel "leia e grave em `.claude/agent-memory/<papel>/`", com o caminho do worktree
     (recomendada) — custo: o gerador conhece o worktree, e os geradores e os testes crescem; se paga: no primeiro papel
     rodado fora do Claude;
   - a memória dos papéis vai a uma pasta neutra — custo: muda o `memory_dirs()` (`measure.py:627-638`), o
     `memory: project` e o `AGENTS.md`; se paga: só se o `.claude/` atrapalhar o Codex.

   **Resposta:** "opção 1 + a memória registra se foi gravada por um runtime diferente de claude". Leitura: vale o
   bloco no prompt, e a memória gravada fora do Claude carrega o runtime que a gravou. Onde o runtime fica — no arquivo
   da memória, no evento `memory` da medição, ou nos dois — vai à rodada 4.

2. **Como `reviewer`, `collector` e `designer` ficam só em leitura fora do Claude.** Opções:
   - pela chamada (`codex exec -s read-only`, `agy --mode plan`) e pelo texto, sem `tools` no `agy` (recomendada) —
     custo: a restrição só vale quando o papel vem pela delegação; se paga: agora, sem portar a tabela de nomes ainda
     não provados;
   - traduzir `tools` no `agy`, depois de uma sonda de um turno (`agy -p`) que lê os nomes atuais — custo: um turno
     medido (~US$ 0,35 em seis turnos no P11 da Fixfy, `PLN-011-plan.md:696`), a tabela e os testes; se paga: se um
     papel do `agy` rodar como sessão interativa.

   **Decidido — "Traduzir tools no agy"**, com a sonda dos nomes antes.

3. **Como a medição do Codex e do `agy` entra no `measure.py` daqui.** Opções:
   - portar o `codex()`/`agy()` da Fixfy, com `runtime`, `workstream` e `memory()` em todo modo, o `API_PRICES`
     conferido com os modelos de hoje e a tabela "Por runtime" no resumo, depois de uma sonda que vê se o
     `guardian_review` dispara `SubagentStop` (recomendada) — custo: ~260 linhas e testes com três fixtures; se paga: no
     primeiro resumo com linha real de cada runtime, o que o P9 da Fixfy reabriu;
   - só tokens e cota, sem US$ — custo: menor, sem comparar com o Claude; se paga: nunca, se o custo por turno for
     métrica.

   **Decidido — "Portar com US$ (Recomendado)".**

4. **Se a delegação porta o `delegate.py` da Fixfy.** Opções:
   - versão reduzida: `--type review|reading`, `--to codex|agy` explícito, sem `quota.py` nem a conta `adm`, só leitura,
     com a linha `delegation` na medição (recomendada) — custo: ~150 linhas a menos que o original e um pedido ao
     `tools-kit`; se paga: na primeira revisão feita pelo Codex ou pelo `agy`;
   - esperar o veredito da Fixfy — custo: o PLN-004 para na frente 4; se paga: se o veredito for encerrar a delegação.

   **Decidido — "Versão reduzida (Recomendado)".**

### Rodada 4 — o runtime na memória e as sondas (enviada 2026-10-30)

**Apresentado antes:** a leitura da resposta da R3.1, e as três sondas que as rodadas pediram — a identidade no commit
(R2.3), os nomes das ferramentas do `agy` (R3.2) e o `guardian_review` com o `SubagentStop` (R3.3). O `memory()` do
`measure.py` já lê o bloco `metadata:` do frontmatter (`.claude/hooks/measure.py:606-623`).

Respondida em 2026-10-30, na sessão `workspace`.

1. **Onde fica o runtime da memória gravada fora do Claude** (R3.1). Opções:
   - no arquivo e no evento (recomendada): o bloco do papel manda gravar `metadata.runtime: codex|agy` no frontmatter —
     sem o campo, foi o Claude —, e o evento `memory` lê o campo — custo: uma linha no bloco gerado e a leitura no
     `memory()`, com teste; se paga: na primeira memória gravada fora do Claude, à vista no git e no `--by-workstream`;
   - só no arquivo — custo: só a linha no bloco; se paga: agora no git, sem o resumo separar por runtime;
   - só no evento, pelo runtime da sessão — custo: a leitura no `memory()`, com o `session_id` aproximado do retrato;
     se paga: só se o runtime da sessão for confiável no retrato, e hoje não é.

   **Decidido — "No arquivo e no evento (Recomendado)".**

2. **Quando rodam as três sondas.** Opções:
   - agora, antes do Desenho, por um subagente, num repositório descartável do scratch (recomendada) — custo: ~2 turnos
     de Codex (~US$ 0,40), ~2 de `agy` (~US$ 0,12) e o subagente; se paga: no Desenho, com fato no lugar de hipótese;
   - como P0 do plano — custo: o mesmo, mais reescrever o `D` que a sonda desmentir; se paga: só se as três
     confirmarem o que o Desenho supôs.

   **Decidido — "Agora, antes do Desenho (Recomendado)".**

### Rodada 5 — o que as sondas abriram (enviada 2026-10-30)

**Apresentado antes:** as três sondas da R4.2, pelo `collector`, num repositório descartável do scratch com um worktree;
o detalhe está em `pln-004-sondas.md`, no scratch da sessão `workspace`.
- **Codex, a identidade:** o `env` chega aos comandos; o commit sai com o noreply do `brz-anderson` como autor e
  committer (`a1490f5`, conferido de fora com `git log`).
- **Codex, o commit no worktree:** falha em `workspace-write` (`Unable to create '<repo>/.git/worktrees/wt/index.lock':
  Operation not permitted`) — o sandbox protege todo diretório `.git`, e o `--add-dir` não resolve. Passa com
  `-c 'sandbox_workspace_write.writable_roots=["<common>/worktrees/<wt>","<common>/objects","<common>/refs","<common>/logs"]'`.
  O `workspace-write` não tem rede: o `git push` não passa dentro dele.
- **Codex, o `guardian_review`:** dispara com `approval_policy=on-request` e `approvals_reviewer=auto_review`; liberou o
  commit fora do sandbox (`682e434`). O rollout filho tem `thread_source: guardian_review` e o `parent_thread_id` do
  pai; **os tokens do filho não entram no pai** — nos dois casos de 2026-10-28 e na reprodução, a soma do pai bate com
  o total dele, e o filho fica à parte (~3% da entrada em 2026-10-28). Na Fixfy, 0 de 14 filhos têm linha na medição.
  O evento de hook não foi observado: hook sem confiança é pulado em silêncio.
- **`agy`, a identidade:** o `env` chega; o commit não passa — sem `--add-dir`, `not a git repository`; com ele,
  `index.lock: Operation not permitted`. A candidata, `--settings '{"enableTerminalSandbox":false}'`, ficou sem teste.
- **`agy`, as ferramentas:** o agente principal usa `read_file`, `write_file`, `edit_file` e `run_command`; o `tools:`
  aceita a família antiga e a nova, e o subagente recebe a que o frontmatter nomeia; o `agy agents` não valida nomes.
- **O `fixfy_where`** responde `root` em qualquer cwd quando a `FIXFY_WORKSPACE` está vazia (`~/.zshrc:17`, o
  `cd ""` não falha): a função da Fixfy pega o `codex` fora dela.

Respondida em 2026-10-30, na sessão `workspace`.

1. **Como fica o commit do `agy`.** Opções:
   - o `agy` não comita: lê e grava arquivos, e o commit fica com a sessão Claude ou com o Codex (recomendada) — custo:
     o `agy` sem fluxo de commit; se paga: agora, na delegação só de leitura (R3.4);
   - testar `--settings '{"enableTerminalSandbox":false}'` no scratch — custo: ~US$ 0,01, e o uso depois tira o
     sandbox de terminal da sessão; se paga: só com o `agy` comitando no worktree;
   - deixar a medir no Desenho — custo: um `D` aberto; se paga: quando o primeiro papel `agy` precisar gravar.

   **Decidido — "agy não comita (Recomendado)".**

2. **O que a medição faz com o `guardian_review`.** Opções:
   - linha própria ligada ao pai: o `measure.py` acha os rollouts com o `parent_thread_id` do pai e grava
     `event: subagent`, `agent_type: guardian`, sem somar ao pai (recomendada) — custo: ~30 linhas, uma fixture e o
     preço do `codex-auto-review` no `API_PRICES`; se paga: no primeiro resumo com guardian real;
   - ignorar e documentar a subcontagem de ~3% — custo: nenhum código; se paga: nunca, se o custo por turno for
     métrica.

   **Decidido — "Linha própria ligada ao pai (Recomendado)".**

3. **Como a sessão Codex grava e envia.** Opções:
   - o wrapper calcula e passa os `writable_roots` do worktree, e o push do `brza note commit` pede escalonamento
     (`approval_policy=on-request`), aprovado por Anderson na sessão interativa (recomendada) — custo: uma aprovação por
     push e o cálculo no wrapper, no pedido ao `tools-kit`; se paga: no primeiro commit de nota numa sessão Codex;
   - push automático pelo `auto_review` — custo: um guardian por push (~7,5 mil tokens de entrada na sonda), e depende
     de o modelo pedir o escalonamento; se paga: com muitos pushes por sessão;
   - o Codex comita sem push (`--no-push`), e o push fica com a sessão Claude ou com Anderson — custo: um passo manual
     por sessão; se paga: só se o push pelo Codex der problema.

   **Decidido — "Wrapper libera o .git; push com aprovação (Recomendado)".**

### Rodada 6 — a estrutura do Desenho (enviada 2026-10-30, no chat)

**Apresentado antes:** o rascunho do Desenho, pelo `designer`, no scratch da sessão `workspace`
(`pln-004-design-rascunho.md`, 730 linhas): D1 a D14, a ordem de execução, 8 pontos para rodada e 12 fatos "a
conferir". A rodada foi no chat, sem a ferramenta, a pedido de Anderson: "faça a rodada no chat, igual a de decisão, sem
a ferramenta de pergunta".

Respondida em 2026-10-30, na sessão `workspace`: "6.1.1 / 6.2.1 / 6.3.1 / 6.4.1".

1. **Quando rodam as sondas que sobraram** — o `agy` segue symlink; o `trustedWorkspaces` e o `--sandbox` pelo
   `--settings` do `agy`; o hook do `agy` num worktree não confiado, e o cwd dele; o `hooks.json` do Codex por symlink;
   o app com `agentCmdOverrides.codex` e `.antigravity`; os nomes novos de busca e web no `agy`. Opções:
   - agora, antes de fechar o Desenho, pelo `collector`, com um `/hooks` de Anderson (recomendada) — custo: ~US$ 0,15
     e ~5 min de Anderson; se paga: no Desenho, porque três respostas decidem a R6.2 e a R6.3;
   - como P0 do plano — custo: o mesmo, mais reescrever o `D` desmentido; se paga: só se todas confirmarem.

   **Decidido — agora, antes de fechar o Desenho.**

2. **Como o espelho em `.agents/skills/` não diverge** (D4). Opções:
   - um symlink por skill, e o `brza agents --check` acusa o link que falta ou está quebrado (recomendada) — custo: 2
     links e uma sonda de ~US$ 0,01 no `agy`; o Codex já segue o link; se paga: agora;
   - cópia gerada, com `--check` — custo: ~60 linhas, 136 KB duplicados e a troca de `${CLAUDE_SKILL_DIR}`; se paga: só
     se o texto mudar por runtime;
   - esqueleto gerado, com a linha "leia `.claude/skills/<nome>/SKILL.md`" — custo: ~30 linhas e uma leitura a mais por
     acionamento; se paga: se o `agy` não seguir o link.

   **Decidido — um symlink por skill**, a confirmar no `agy` pela sonda da R6.1.

3. **Como os hooks, a regra do `agy` e os papéis chegam ao brza-studio** (D8). Opções:
   - o `brza tree` liga por symlink, como já liga o `.claude/agent-memory` (recomendada) — custo: código no
     `tools-kit`, `/.codex/` e `/.agents/` no `.gitignore` do brza-studio e um `/hooks` por worktree; os worktrees que o
     app cria em `~/orca/workspaces/…` ficam de fora; se paga: na primeira sessão Codex ou `agy` num worktree do
     brza-studio;
   - pelo wrapper, `-c hooks.…` no Codex e hooks globais do `agy` — custo: uma sonda interativa, e no `agy` o hook em
     toda sessão da máquina, o que reabre a R2.4; se paga: se a primeira deixar muitos worktrees de fora;
   - sem hooks no brza-studio por ora — custo: nenhum agora; se paga: nunca, se a medição vale lá.

   **Decidido — o `brza tree` liga por symlink.**

4. **Onde mora o gerador dos papéis** (D7). Opções:
   - no `brza agents --write|--check`, sobre o `parse_frontmatter` que já existe (recomendada) — custo: ~150 linhas e
     ~10 testes pelo `tools-kit`, e a frente 2 na fila dele; se paga: agora, com um parser só;
   - um script novo na `master`, pela sessão que conduz — custo: as mesmas linhas, mais um `import` cruzado ou um
     parser repetido, e pode reabrir a R1.1; se paga: se o `tools-kit` não tiver sessão livre antes do D9;
   - portar os geradores da Fixfy — custo: 282 linhas e um parser que já divergiu (G13); se paga: nunca.

   **Decidido — no `brza agents --write|--check`.**

### Rodada 7 — o Codex no app, a memória, o shell e a issue (enviada 2026-10-31, no chat)

**Apresentado antes:** as sondas da R6.1, no scratch da sessão `workspace` (`pln-004-sondas-r6.md`): o `agy` segue o
symlink da skill, da regra, do agente e do hook, e o hook roda com o cwd em `<worktree>/.agents`; os nomes de busca e
web do `agy` são os velhos, só no `tools:` do subagente; o chat do Codex no app roda `<override> … app-server`
(`brza-studio/src/main/codex/codex-structured-launch-resolution.ts:85`), e o chat Antigravity não é o `agy`
(`brza-studio/src/main/acp/acp-launch-specs.ts:261-265`).

Respondida em 2026-10-31, na sessão `workspace`: "7.1.1 / 7.2.1 / 7.3.1 / 7.4.1".

1. **O app abre o Codex com `--approve-for-me`** (`agentDefaultArgs.codex`), que manda a aprovação ao revisor
   automático e não a Anderson, contra a R5.3. Opções:
   - o `codex-brza` tira a flag nos checkouts brza (recomendada) — custo: ~5 linhas e um teste, no pedido ao
     `tools-kit`; se paga: no primeiro push numa sessão Codex do app;
   - Anderson esvazia o `agentDefaultArgs.codex` no app — custo: vale também para a Fixfy; se paga: agora;
   - aceitar o revisor automático no app — custo: reabre a R5.3; se paga: só com muitos pushes por sessão.

   **Decidido — o `codex-brza` tira a flag nos checkouts brza.**

2. **Como o bloco gerado do papel aponta a memória** (D7). Opções:
   - caminho relativo à raiz do worktree (`git rev-parse --show-toplevel`), com os gerados versionados (recomendada) —
     custo: nada além do bloco; se paga: agora, em todo worktree;
   - caminho absoluto, gerado por worktree e fora do git, a leitura literal da R3.1 — custo: gerar a cada worktree e
     perder o `--check` versionado; se paga: nunca, enquanto o relativo resolver.

   **Decidido — caminho relativo à raiz do worktree.**

3. **Como a função nova `codex`/`agy` convive com a da Fixfy no `~/.zshrc`** (D6). Opções:
   - o bloco BrzA copia a função da Fixfy para `fixfy_codex`/`fixfy_agy` com `functions -c` e a redefine (recomendada)
     — custo: 2 linhas, e o bloco vem depois do da Fixfy; se paga: agora, sem mexer na Fixfy;
   - renomear as funções no README da Fixfy — custo: mexe em outro workspace, contra a R1.3; se paga: só se a Fixfy já
     for mexer nesse bloco.

   **Decidido — `functions -c` no bloco BrzA.**

4. **Como a issue do `studio` se liga ao plano** (D14). Opções:
   - um pedido à sessão do `studio`, que acrescenta a linha "Plano:" na issue, com o `brza delegate` do D11 no lugar do
     `delegate.py` (recomendada) — custo: um pedido curto; se paga: quando o `brza delegate` existir;
   - só o link que já está no Pedido do plano — custo: nenhum; se paga: agora, com a issue citando o `delegate.py`.

   **Decidido — um pedido à sessão do `studio`.**

### Rodada 8 — o hook do Codex e o scratch (enviada 2026-10-31, no chat)

**Apresentado antes:** o `/hooks` de Anderson, numa sessão Codex no worktree da sonda: o `papel` carregou pelo
`.codex/agents` em symlink, mas o espião do hook não gravou nada, e o `~/.codex/config.toml` não ganhou `hooks.state`
para o `sondas2`. A captura de Anderson mostrou a tela "PreToolUse hooks" só com o hook do Orca (`Source: User config -
~/.codex/hooks.json`), que não decide, porque o hook da sonda é só `Stop` e `SubagentStop`. A única confiança de
`hooks.json` por link na máquina, a da Fixfy, foi gravada pelo caminho resolvido (`~/.codex/config.toml:209`).

Respondida em 2026-10-31, na sessão `workspace`: "8.1.1 / 8.2.1".

1. **Como o `.codex/hooks.json` chega ao worktree do brza-studio** (D8, R6.3). Opções:
   - o `brza tree` o copia, e o `.codex/agents` e o `.agents/` seguem por symlink (recomendada) — custo: ~5 linhas no
     `brza tree`, no pedido ao `tools-kit`; a cópia envelhece quando o hook muda, e cada mudança pede um `/hooks`; se
     paga: agora, sem mais sonda;
   - Anderson olha a tela do `Stop` e do `SubagentStop` no `/hooks`, e o link fica se o hook aparecer — custo: ~2 min
     de Anderson; se paga: só se o link funcionar.

   **Decidido — o `brza tree` copia o `.codex/hooks.json`.** A conferência final em cada runtime prova que o hook roda.

2. **Onde o Codex guarda o scratch** (D2). Opções:
   - em `$TMPDIR/codex-scratch/<id da sessão>`, escrito no adaptador (recomendada) — custo: uma linha no
     `developer_instructions`; se paga: no primeiro levantamento de um papel no Codex;
   - sem scratch, com o agregado na devolução — custo: nenhum agora; se paga: nunca, quando o levantamento passa de uma
     tela.

   **Decidido — `$TMPDIR/codex-scratch/<id da sessão>`.**

## Worklogs

- 2026-10-30 — aberto; R1 trazida da sessão `brza-workspace-80`; o levantamento do PLN-011; R2 a R4; as sondas; R5; o rascunho
  do Desenho, pelo `designer`; R6. Parou nas sondas da R6.1.
  [O PLN-004: a abertura do Codex e do agy no fluxo](../../work/worklogs/2026-10-30-pln-004-a-abertura-do-codex-e-do-agy-no-fluxo.md)
- 2026-10-31 — as sondas da R6.1; o `/hooks` de Anderson, sem o hook rodar; R7 e R8. Parou na
  aprovação do Desenho.
  [O PLN-004: as sondas da R6 e o Desenho do Codex e do agy](../../work/worklogs/2026-10-31-pln-004-as-sondas-e-o-desenho.md)
