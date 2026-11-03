# PLN-004 — Entrevista

Do [PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](PLN-004-plan.md): as rodadas R1–R12, que só crescem. Saíram do `-plan` em 2026-11-03, quando ele passou de 670 linhas.

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
   pedido ao `tools-kit`. **→ reaberta em R10.2**: o código passou ao `brza-workflow`.

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

   **Decidido — "Função e wrapper (Recomendado)".** **→ reaberta em R10.1**: o `.codex/config.toml` e o
   `.agents/rules/` deixam de ser arquivos locais e vão ao pacote `runtimes` do `brza-workflow`.

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

### Rodada 9 — o que a aplicação da R6 a R8 abriu (enviada 2026-10-31, no chat)

**Apresentado antes:** o rascunho do Desenho com a R6 a R8 aplicadas, pelo `designer`, em 551 linhas, e três escolhas
que as rodadas não cobriram. Sem a `BRZA_WORKSPACE`, o `measure.py` e o `claude-brza` já caem em
`~/Projects/brza-workspace` (`.claude/hooks/measure.py:88`, `scripts/brza/claude-brza:18-19`).

Respondida em 2026-10-31, na sessão `workspace`: "todos recomendados".

1. **Para onde o comando dos hooks aponta sem a `BRZA_WORKSPACE`** (D8); o hook do `agy` roda em `<worktree>/.agents`.
   Opções:
   - `${BRZA_WORKSPACE:-$HOME/Projects/brza-workspace}` nos dois hooks (recomendada) — custo: nada além do texto; se
     paga: na primeira sessão aberta sem o wrapper;
   - `..` no `agy` e `.` no Codex, como na Fixfy — custo: sem o wrapper, a medição vai ao worktree e, no brza-studio,
     se perde; se paga: nunca.

   **Decidido — `${BRZA_WORKSPACE:-$HOME/Projects/brza-workspace}`.** **→ reaberta em R10.3**: o `measure.py` e o
   `claude-brza` já não caem nesse caminho.

2. **O `agy-brza` passa `--settings '{"trustedWorkspaces":["<raiz do worktree>"]}'`** (D5). Opções:
   - sim, quando a chamada não traz o próprio `--settings` (recomendada) — custo: ~5 linhas e um teste no `tools-kit`;
     se paga: no primeiro `agy agents` ou numa TUI de worktree novo aberta fora do app;
   - não; o worktree se confia pela TUI ou pelo app — custo: nenhum; se paga: agora, se ninguém listar papéis pelo CLI.

   **Decidido — sim.**

3. **O `brza install --chat-command` põe `agentCmdOverrides.antigravity = agy-brza`** (D5, D12); o override vale só na
   aba de terminal do `agy` no app. Opções:
   - sim (recomendada) — custo: uma chave a mais no `brza install`; se paga: na primeira aba de terminal do `agy` no app;
   - não — custo: nenhum; se paga: só se o `agy` nunca abrir pelo app.

   **Decidido — sim.**

A aprovação do Desenho vai em três mensagens — o que assume, o Terreno e D1–D4; D5–D8; D9–D14 e a ordem —, como
proposto na mesma mensagem e aceito na mesma resposta.

### Rodada 10 — onde cada item mora depois do PLN-006 (enviada 2026-11-02, no chat)

**Apresentado antes:** o levantamento do `collector` contra as mudanças dos três repositórios (agregado no scratch,
`pln-004-revisao-mudancas.md`), com 38 citações conferidas, das quais 19 mudaram de lugar. O PLN-006 levou ao
`brza-workflow` o CLI, os hooks, os papéis e a norma comum (`AGENTS.md`, `CLAUDE.md`, `plans/README.md`,
`work/README.md`); o `brza sync` só escreve `core/` e `packages/<nome>/core/`, e deixa intocado o que não conhece, como
o `.codex/` e o `.agents/`; o `brza-workflow` não tem `plans/` nem `work/` e não cita Codex nem `agy`; o `tools-kit` não
tem item do PLN-004, e o PLN-006 foi executado pela sessão `workspace` nos dois repositórios. Medi o `brza-where`:
mediana de 42 ms em 20 chamadas, e do brza-studio e de subdiretório do worktree ele acha a raiz.

Respondida em 2026-11-02, na sessão `workspace`: "10.1.2 `packages/runtimes` / 10.4.2 `measure_runtimes.py` / restante
`Recomendado`". A rodada saiu com `packages/codex` e `measure_codex.py` como alternativas, sem o `agy`; Anderson
perguntou por quê, a sessão reconheceu a omissão, e as duas opções foram reapresentadas para os dois runtimes.

1. **Onde moram o `.codex/`, o `.agents/` e os papéis gerados** (D1 a D4, D7, D8). Opções:
   - locais do workspace, com as linhas genéricas no `core/AGENTS.md` (recomendada) — custo: uma edição genérica no
     núcleo e um segundo workspace refaz os arquivos locais; se paga: agora;
   - um pacote para os dois runtimes, `packages/runtimes`, ligado no manifesto — custo: sessão e testes no
     `brza-workflow`, o `.toml` entra sem molde, o que o pacote escreve editado local trava o sync, e um workspace que
     usa um runtime só recebe os dois; seria o primeiro pacote além do `client`; se paga: quando um segundo workspace
     usar Codex ou `agy`;
   - um pacote por runtime — custo: o mesmo, mais a disputa pelo `.agents/skills/`, que os dois leem; se paga: nunca,
     enquanto os dois compartilharem esse caminho;
   - tudo local, sem tocar o `AGENTS.md` do núcleo — custo: a norma não cita Codex nem `agy`, e o
     `agent-instructions-writer`, neutro de runtime, fica sem onde registrar; se paga: nunca.

   **Decidido — "10.1.2 `packages/runtimes`"**, não a recomendada. Anderson não deu o porquê; a leitura da sessão é que
   o pacote leva o adaptador, a regra, os hooks e os papéis ao workspace pelo sync, sem editar a norma comum.

2. **Quem executa o código no `brza-workflow`** (`codex-brza`, `agy-brza`, `brza agents --write|--check`,
   `brza sessions --agent`, `brza delegate`, o `measure.py`). Opções:
   - a sessão `workspace`, com `implementer`, como no PLN-006 (recomendada) — custo: sessão grande, e a R1.1 é reaberta;
     se paga: já na fase 1, porque a sessão que conduz o plano tem o contexto e o pedido de 7 itens do D13 deixa de
     existir;
   - o `tools-kit`, por pedido — custo: a fila dele (PLN-003 aberto e 7 issues) e o núcleo editado por outra frente; se
     paga: se a sessão `workspace` não aguentar o tamanho;
   - divisão: núcleo e `measure` pela `workspace`; wrappers, `sessions`, `delegate` e `brza-tree` pelo `tools-kit` —
     custo: dois executores e uma ordem de entrega; se paga: se houver paralelismo.

   **Decidido — a sessão `workspace`, com `implementer`.**

3. **Para onde o comando dos hooks aponta sem a `BRZA_WORKSPACE`** (reabre a R9.1). Opções:
   - a `BRZA_WORKSPACE` que o wrapper põe; sem ela, o `brza-where` (recomendada) — custo: 42 ms só quando a variável
     falta, nos eventos `Stop` e `SubagentStop`, e a dependência do `~/.local/bin` no PATH do hook; se paga: agora, sem
     nome fixo, pelo registro do PLN-006;
   - `${BRZA_WORKSPACE:-$HOME/Projects/brza-workspace}`, como a R9.1 — custo: nome fixo num arquivo local, que o núcleo
     proíbe nos scripts (`test_brza_scripts.py:161`); se paga: nunca;
   - sem fallback — custo: a sessão aberta sem o wrapper nem a função não é medida; se paga: agora, se Anderson aceitar
     o limite.

   **Decidido — a `BRZA_WORKSPACE` do wrapper e, sem ela, o `brza-where`.**

4. **Onde entram os modos `codex` e `agy` do `measure.py`** (D9). Opções:
   - no `core/.claude/hooks/measure.py` do `brza-workflow`, com os testes em `tests/hooks/` (recomendada) — custo: ~260
     linhas de runtime que todo workspace recebe pelo sync sem usar; se paga: agora, com um `measure.py` só;
   - um arquivo para os dois runtimes, `measure_runtimes.py`, num pacote — custo: importar o `memory()` e o
     `workstream_of` do `measure.py` do núcleo, e depende de a 10.1 escolher o pacote; se paga: com o segundo
     workspace;
   - um arquivo por runtime, `measure_codex.py` e `measure_agy.py` — custo: o mesmo, com dois arquivos; se paga: se os
     dois divergirem a ponto de não dividir o import.

   **Decidido — `measure_runtimes.py`**, não a recomendada, coerente com o pacote da 10.1.

**O que a R10 deixa aberto**, e vai à R11: como o `.agents/skills/` chega ao workspace, porque o `brza-sync` só conhece
os modos `100644` e `100755` e gravaria um symlink do pacote como arquivo de texto (`bin/brza-sync:115`, `:323-331`);
onde moram os papéis gerados; onde entram o `codex()` e o `agy()` no shell; e o que fazer com a auditoria de fatos, que
só roda para o Claude.

### Rodada 11 — o que o pacote `runtimes` abriu (enviada 2026-11-02, no chat)

**Apresentado antes:** o `brza-sync` só conhece os modos `100644` e `100755` e gravaria um symlink do pacote como arquivo
de texto (`brza-workflow/bin/brza-sync:115`, `:323-331`, lido, não rodado); o `~/.zshrc` faz `source` do `brza.zsh`, tem
a `brza_claude_fallback`, e o `codex()` e o `agy()` dele são da Fixfy; o `fact_audit.py` lê o transcript no formato do
Claude (`blocks_of`, `sources_of`, `runs_of`), só para `designer` e `collector`, e solta o `claude -p --model haiku`, cuja
metade `run` não depende do runtime.

Respondida em 2026-11-02, na sessão `workspace`: "11.3 meça a opção 2, restante `Recomendado`".

1. **Como os papéis gerados e os links de `.agents/skills/` chegam ao workspace** (D4, D7). Opções:
   - tudo pelo sync: o pacote entrega os papéis gerados, e o `brza-sync` aprende o modo `120000` (recomendada) — custo:
     mexer no `brza-sync` e no lock, com testes em `tests/cli/`, e regerar o pacote no commit que muda um papel do
     núcleo; se paga: agora, porque o PLN-006 prometeu que a mudança do núcleo chega pelo sync;
   - tudo local, pelo `brza agents --write` depois de cada sync — custo: um passo manual por sync e por skill nova, e a
     defasagem só aparece no `--check`; se paga: agora, sem mexer no sync;
   - papéis pelo sync e links locais — custo: dois mecanismos; se paga: se mexer no sync não valer.

   **Decidido — "Tudo pelo sync (Recomendado)".**

2. **Onde entram o `codex()` e o `agy()` no shell** (D6). Opções:
   - um arquivo do pacote `runtimes` (`shell/runtimes.zsh`), com o `~/.zshrc` renomeando os da Fixfy para
     `brza_codex_fallback` e `brza_agy_fallback` (recomendada) — custo: Anderson edita o `~/.zshrc` (~6 linhas), e vai ao
     worklog em "Fora do workspace"; se paga: agora;
   - dentro do `packages/client/shell/brza.zsh` — custo: o `client` passa a conhecer o `codex-brza`, de outro pacote;
     se paga: nunca;
   - direto no `~/.zshrc` — custo: uma segunda fonte fora do repositório; se paga: nunca.

   **Decidido — "Um arquivo do pacote `runtimes` (Recomendado)".**

3. **O que fazer com a auditoria de fatos nos papéis do Codex e do `agy`.** Opções, na ordem em que voltaram com as
   medições:
   - auditar o que o `brza delegate` devolve, com uma entrada nova do `fact_audit.py` e o mesmo `run` do Haiku, sem hook
     (recomendada) — custo: ~40 linhas e testes, ~US$ 0,10 por devolução; se paga: na primeira delegação de
     levantamento; cobre o caminho da R3.4, não a sessão interativa;
   - hooks nos dois runtimes — `SubagentStop` no Codex e `Stop` no `agy`, filtrando pela marca, só `lido` e `doc` —:
     custo: ~140 linhas, ~8 testes, 1 a 2 hooks a mais por runtime para confiar em `/hooks` em cada worktree, e US$
     0,0043 por fato; se paga: quando sessões interativas de Codex ou `agy` fizerem desenho e levantamento em volume;
   - aceitar o limite, com uma linha no bloco do papel gerado — custo: nenhum código; se paga: agora.

   **Resposta:** primeiro "meça a opção 2"; depois da medição, "11.3.2". **Decidido — hooks nos dois runtimes**, não a
   recomendada: `SubagentStop` no Codex e `Stop` no `agy`, só `lido` e `doc`. Anderson não deu o porquê. A opção de
   auditar o `brza delegate` nasceu da medição e ficou de fora. O que a medição achou:
   - **O custo da auditoria:** US$ 1,03 em 8 auditorias para 238 fatos, ou **US$ 0,0043 por fato**, com mediana de 134 s
     em segundo plano (`.measurements/measurements.jsonl`, eventos `fact_audit`); com ~24 fatos auditáveis por devolução
     (240 em 10 capturas), **~US$ 0,10 por devolução**. O auditor é o Haiku do `claude -p`: não muda com o runtime.
   - **O Codex dá o que o `stop` precisa:** o `SubagentStop` traz `agent_type` e `agent_transcript_path`; na Fixfy há 11
     linhas `subagent` de `reviewer` do Codex (`~/Projects/fixfy/.measurements/measurements.jsonl`;
     `FX/.claude/hooks/measure.py:326-329,558`). Aqui o hook só roda depois do `/hooks`, por worktree.
   - **O `agy` não dá:** o `Stop` traz `conversationId`, `transcriptPath` e `lastUserInput`, sem nome de agente, e não há
     `SubagentStop` (`pln-004-sondas-r6.md`, eventos do espião); só dá para filtrar pela marca na última resposta.
   - **O `rodado` pesa menos do que parece:** dos 240 fatos auditáveis, 82 são `rodado` (34%), e mesmo no Claude 49 de 80
     saíram `unknown` (61%); o `lido` segurou 105 de 150 (70%).
   - **Estimativa, não medida:** ~140 linhas e ~8 testes para os dois adaptadores de captura (o `stop` tem 40 linhas; o
     `codex()` e o `agy()` do `measure.py` da Fixfy, 48 e 33).

### Rodada 12 — o foco da revisão (enviada 2026-11-02, no chat)

**Apresentado antes:** a Fixfy parte o diff de uma entrega em três revisores isolados, com o mesmo escopo e a mesma
régua, cada um só relatando o que cai no foco dele — simplicidade, defeito ou convenção
(`~/Projects/fixfy/fixfy-plugin/skills/review-writer/references/review-orders.md:13-30`) —, e Anderson mandou os três para
a frente 4, "um por runtime". O custo de uma revisão, medido: **Codex** US$ 1,98 de mediana (`gpt-6-astra` em `xhigh`,
122 s, 11 revisões da Fixfy); **Claude** US$ 4,22 (`opus-5-5`, 1.079 s, 4 revisões daqui); **`agy`** estimado em US$ 0,1
a 0,4 pelos tokens das sondas, no preço da tabela da Fixfy. As tarefas diferem: é a forma do custo, não a qualidade. A
Fixfy não gravou o veredito da delegação, que fechava em 2026-10-30.

Respondida em 2026-11-02, na sessão `workspace`: "11.3.2 / 12.1.1 / 12.2.2".

1. **Onde entra o foco da revisão** (D11). Opções:
   - no pedido de cada `brza delegate --type review`, com `--focus simplicidade|defeito|convenção`, e o corpo do
     `reviewer` igual nos três (recomendada) — custo: ~20 linhas no `brza delegate` e o texto dos três focos num
     arquivo do núcleo; se paga: agora, e o mapa da 12.2 muda sem regerar papel;
   - um bloco por runtime que o gerador injeta no `reviewer` gerado — custo: o gerador deixa de só copiar o corpo, e
     mudar o mapa regera o pacote; se paga: se o foco virar fixo por runtime;
   - no `reviewer.md` do núcleo — custo: vira regra de todo workspace, inclusive o Claude; se paga: nunca, enquanto só
     este workspace delegar.

   **Decidido — `--focus` no pedido de cada `brza delegate --type review`.**

2. **Qual foco vai a qual runtime.** Opções:
   - Claude = defeito, Codex = simplicidade, `agy` = convenção (recomendada) — inferência, sem medição de qualidade —:
     custo: ~US$ 6,3 a 6,6 por revisão completa dos três; se paga: agora, revista pela medição;
   - medir antes, com o mesmo diff de referência nos três focos e nos três runtimes, 9 revisões — custo: ~US$ 19 a 20 e
     ~1 h da sessão; se paga: se o mapa valer por meses, ou se os achados dos três divergirem;
   - sem mapa fixo, com o `--focus` obrigatório e quem pede escolhe — custo: nenhum agora, e o hábito pode virar sempre
     o mesmo foco; se paga: agora, até a medição mostrar qual runtime acerta qual foco.

   **Decidido — medir antes**, não a recomendada. Anderson não deu o porquê. O diff de referência e o critério de acerto
   saíram da sessão e voltaram a Anderson antes de gastar: o diff é a entrega do PLN-005 na `master`
   (`2e8ea67..13a291a`, 2.519 linhas em 22 arquivos), com o parecer do `reviewer` como resposta conhecida, 10 achados
   reais e 5 hipóteses falsas, e o recall contado sobre os 7 achados que o diff permite (A5, A9 e A10 dependem do plano
   e do log). Anderson o confirmou em 2026-11-02, "confirmo o experimento", e as 9 revisões rodaram. **As 3 do Codex
   usaram exatamente os 100% do limite de 5 h**, na palavra de Anderson; os rollouts mostram a janela de 0% a 99% no
   último evento, de 28 a 35 pontos por revisão.

   **O resultado das 9 revisões, em uma execução por braço:**

   | Runtime | Achados | Recall (÷7) | Precisão | Custo dos 3 focos | Tempo |
   | :-- | --: | --: | --: | --: | --: |
   | Claude | 17 | 0,43 | 17/17 | US$ 3,44 | 10,6 min |
   | Codex | 14 | 0,21 | 13/14 | US$ 9,91 e a janela de 5 h | 20,9 min |
   | `agy` | 21 | 0,50 | 20/21 | US$ 10,54 (tabela) | 37,9 min |

   Por foco: defeito, Claude 0,20, Codex 0,10, `agy` 0,40; convenção, 1,00, 0,50 e 0,75. A2, A7 e A8: 0 dos 9 braços. O
   detalhe está no worklog de 2026-11-02. O `qwen2.5:14b` local, medido à parte, ficou em recall 0 de 7 e fora das
   revisões.

   **A rodada que veio da pontuação** (a 12.2 de novo): 1, Claude nos 3 focos e o `agy` como segundo revisor do defeito,
   recomendada; 2, cada foco no runtime de maior recall; 3, repetir os braços do Claude e do `agy` antes de decidir.
   **Respondida "3"**, em 2026-11-02, na sessão `workspace`: repetir os 6 braços (Claude e `agy`, sem o Codex), para ver
   se a diferença de 1 item no defeito sobrevive à variação entre execuções. Custo declarado: ~US$ 14 de tabela e
   ~48 min. O mapa fica decidido depois da repetição.

   **A repetição rodou** (Claude e `agy`, 6 braços, o `agy` em paralelo; custo real US$ 11,38 de tabela e ~15 min de
   parede, abaixo do declarado). O recall do Claude foi de 0,43 a 0,50 e o do `agy` de 0,50 a 0,29; no defeito natural,
   o `agy` foi de 0,40 a 0,20 e o Claude de 0,20 a 0,30, ou seja, **a vantagem do `agy` não se repetiu**; na convenção,
   o Claude ficou em 1,00 duas vezes e o `agy` foi de 0,75 a 0,50. Só metade dos achados verdadeiros reaparece entre
   as duas execuções (interseção ÷ união de 0,50 no Claude e 0,45 no `agy`). O detalhe está no worklog de 2026-11-02.
   A R12.2 voltou a Anderson, com a evidência da repetição, em três opções: 1, o Claude como padrão nos três focos, com o
   `agy` e o Codex como segundo passe opcional, sem mapa foco → runtime (recomendada), com custo de US$ 1 a 1,3 e 2,5 a
   5 min por revisão Claude e de US$ 2,1 a 3,3 e 12 a 15 min por foco no segundo passe do `agy`, que se paga numa
   entrega grande; 2, sem padrão, com `--focus` e `--runtime` obrigatórios; 3, o mapa fixo, defeito no `agy` e os
   outros dois no Claude, que não se paga com a evidência atual.

   **Decidido — a 1, a recomendada**, respondida "recomendado" em 2026-11-03, na sessão `workspace`: o Claude é o
   runtime padrão de revisão nos três focos; o `agy` e o Codex entram como segundo passe, pedido por quem pede, com
   `--runtime` além do `--focus`, e não há mapa foco → runtime. O D11 do Desenho segue o `--focus` da 12.1 e ganha o
   `--runtime`, sem padrão por foco.

### Rodada 13 — a norma, o nome do workspace e o `tomllib` (enviada 2026-11-03, no chat)

**Apresentado antes:** o `designer` reescreveu o Desenho para o `brza-workflow` (`pln-004-design-v2.md`, no scratch,
com os D1 a D14 mantidos, o D13 fora e o D15 e o D16 novos) e devolveu 11 pontos sem lastro, que viraram as rodadas 13 a
16. Conferi os fatos desta: o sync só renderiza `.md` (`bin/brza-sync:188`), o `brza_root` recusa string de várias linhas
(`core/.claude/hooks/brza_root.py:189-190`), o README do `brza-workflow` pede Python 3.10 (`README.md:26`) e o `python3`
do PATH é o 3.15, o do sistema o 3.9; o `core/AGENTS.md:35` lista o que mora na `master` sem `.codex/` nem `.agents/`.

Respondida em 2026-11-03, na sessão `workspace`: "todos recomendado".

1. **A norma do pacote `runtimes` toca o núcleo?** (D1) Opções:
   - nada no núcleo; a regra `brza-runtimes.md` do pacote completa a lista (recomendada) — custo: a lista do `AGENTS.md`
     fica incompleta para quem lê só ela; se paga: agora, sem diferença no teste de ouro;
   - uma linha genérica no `core/AGENTS.md:35` e outra na tabela da `agent-instructions-writer` — custo: 2 linhas no
     núcleo e 2 entradas no `golden_differences.py`, que todo workspace recebe; se paga: quando um segundo pacote
     trouxer arquivos fora do `.claude/`.

   **Decidido — nada no núcleo**, a regra do pacote. O precedente é o pacote `client`.

2. **Como o nome do workspace chega ao papel do Codex** (D7, D15, D2). Opções:
   - o sync renderiza também o `.toml` (recomendada) — custo: ~3 linhas no `render_file` e 2 testes, junto do D15; se
     paga: agora, no primeiro sync do pacote, e o adaptador do D2 também usa o molde;
   - o gerador troca cada `{{…}}` por um texto neutro — custo: o papel do Codex diverge do do Claude no texto, e o
     `--check` compara contra o texto trocado; se paga: só se o sync não puder tocar o `.toml`;
   - o papel do Codex só manda ler o `.claude/agents/<papel>.md` — custo: o contorno por texto que a R2.2 e a R3.2
     recusaram; se paga: nunca.

   **Decidido — o sync renderiza também o `.toml`.** O gerado usa a string literal `'''`, e o gerador recusa o corpo
   que tenha `'''`.

3. **O `codex-brza` lê o `developer_instructions` multilinha do `.codex/config.toml`** (D5), só no repositório de
   código. Opções:
   - `tomllib`; sem ele, o wrapper segue sem o adaptador e avisa no stderr (recomendada) — custo: ~6 linhas e um teste;
     numa máquina com 3.10 o Codex no código sobe sem a norma; se paga: agora, com a premissa de que o app e o
     `subprocess` da delegação usam o `python3` do PATH;
   - o `parse_toml` do `brza_root` aprende a string `"""` — custo: ~25 linhas e testes num módulo que roda no 3.9 dos
     hooks; se paga: se aparecer uma máquina em 3.10.

   **Decidido — `tomllib`, e o aviso no stderr sem ele.**

### Rodada 14 — os modelos (enviada 2026-11-03, no chat)

**Apresentado antes:** no papel, o `agy agents` só aceita `pro`, `flash`, `inherit` ou nada, e descarta calado o nome
completo (sonda do `designer`, sem turno de modelo, em `agy` 1.4.12); na chamada, o `--model` usa os nomes do
`agy models`. O que o `pro` resolve é desconhecido. O experimento da 12.2 usou `gemini-4-argon-high` no `agy` e
`gpt-6-astra` em `xhigh` no Codex; o padrão do `~/.codex/config.toml` de Anderson é `gpt-6.1-sol` em `medium`; cada
revisão do Codex gastou de 28 a 35 pontos da janela de 5 h.

Respondida em 2026-11-03, na sessão `workspace`: "14.1.1 / 14.2 opção 1, mas `gpt-6-astra` em `high`" e "sem mais
rodadas, por ora".

1. **O mapa de modelos do `agy` por camada** (D3, D7, D11). Opções:
   - no papel, `opus` e `sonnet` viram `pro` e `haiku` vira `flash`; na chamada, a revisão usa `gemini-4-argon-high` e a
     leitura `gemini-4-argon-medium`; antes de gerar, um turno de `agy --agent` com `model: pro` lê o `modelName` do
     `Stop` (recomendada) — custo: um turno, ~US$ 0,01 a 0,05; se paga: no D7, com o nível do `pro` como fato;
   - `model: inherit` em todo papel gerado, e o modelo sempre pelo `--model` da sessão ou da chamada — custo: o
     subagente do `agy` perde a camada e roda no modelo do pai; se paga: se o `pro` resolver a um nível que não serve
     ao `designer`.

   **Decidido — a recomendada.** O turno que lê o `modelName` do `pro` roda no D7, antes de gerar os papéis.

2. **O modelo e o esforço do Codex no `brza delegate`** (D11). Opções:
   - pela camada do papel: revisão em `gpt-6-astra` com `xhigh`, o que a R12.2 mediu; leitura em `gpt-6.1-sol` com
     `medium`, o padrão do usuário (recomendada) — custo: cada revisão gasta de 28 a 35 pontos da janela de 5 h; se paga:
     no segundo passe ocasional que a R12.2 prevê;
   - o mesmo, com `--effort` repassado ao filho e `xhigh` como padrão — custo: ~5 linhas e um teste; o recall com
     menos esforço não foi medido; se paga: quando a janela de 5 h apertar.

   **Decidido — a opção 1, mas a revisão em `gpt-6-astra` com `high`, e não `xhigh`**, nas palavras de Anderson, sem o
   porquê. É a variante que a sessão deixou de fora por não ter o custo medido: o recall e os pontos da janela de 5 h
   com `high` não foram medidos, e o experimento da 12.2 só tem `xhigh`. A leitura segue em `gpt-6.1-sol` com `medium`.

**Parada de Anderson ("sem mais rodadas, por ora"):** as R15 (a delegação: o papel no `brza delegate`, onde o
`--runtime` pega o padrão e o texto dos três focos) e R16 (a medição e a máquina: onde fica a captura de fatos, a
tabela por runtime, o `~/.zshrc` e a conferência do override) ficam abertas, com as opções que o `designer` deixou no
fim do `pln-004-design-v2.md` (P5 a P11). A aprovação do Desenho só vem depois delas.
