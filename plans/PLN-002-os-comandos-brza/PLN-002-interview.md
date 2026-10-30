# PLN-002 — Entrevista

### Rodada 1 — o `brza tree` (enviada 2026-10-28)

**Apresentado antes:**
- **O P0:** o despacho `brza X` → `brza-X` é feito pela `brza-cli-subcomandos`, fora desta sessão. O checkout principal
  do `brza-studio` está sujo e com a `master` local atrás da `origin/master` (`7e9e0d18948` contra `d7f4e5b5618`).
- **Os worktrees de hoje:** ficam todos em `.worktrees/`. As branches nasceram de `origin/master`, pelo reflog de
  `feat/pln-001-p48` e `feat/pln-001-p44-p47`.
- **O `brza-sessions --checkout`:** só abre o chat (`scripts/brza/brza-sessions:115,135`).
- **O conserto do node_modules:** foi `pnpm install --offline --frozen-lockfile` no próprio worktree, em menos de 1 s
  ([o worklog do ▶ e do ⤢](../../work/worklogs/2026-10-27-o-executar-e-o-expandir-do-orca-fixfy-no-chat.md), linhas
  48-52).
- **Os órfãos:**
  - o `conferencia-p52-p53` é worktree registrado, em detached HEAD;
  - o `chat-markdown-largura-e-links` é só um diretório com `.cache/`, sem registro.
- **A regra "na `origin/master`":** deixaria o `--rm` apagar as branches sem commit próprio, como `feat/pln-001-p44-p47`
  e `feat/pln-001-p48`.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O `tree` abre também o chat?** Opções:
   - só cria o worktree, instala e imprime o caminho (recomendada). Custo: um segundo comando por quem abre a sessão. Se
     paga: agora, porque o `tree` não depende do app aberto nem da interface do `sessions`;
   - `--chat <nome>` opcional, que chama o `brza-sessions --checkout` no fim. Custo: o `tree` passa a depender do app e da
     interface do `sessions`, a combinar com a 2d. Se paga: depois que o `list/send/close` fechar;
   - sempre abre o chat. Custo: quem quer o worktree só para `dev`, `test` ou worker abre sessão à toa. Se paga: nunca, no
     uso levantado.

   **Decidido — `--chat <nome>` opcional.** O `tree` chama o `--checkout` que já existe, sem esperar o `list/send/close`.

2. **De que base sai a branch?** Opções:
   - `git fetch origin` e a branch de `origin/master`, com `--base <ref>` opcional (recomendada). Custo: um fetch pela
     chave `personal` por chamada. Se paga: agora, porque a `master` local está atrás;
   - `origin/master` sem fetch. Custo: pode sair de base velha sem avisar. Se paga: só offline;
   - o `HEAD` do checkout principal. Custo: herda o checkout sujo e atrasado. Se paga: nunca, para trabalho de plano.

   **Decidido — fetch e `origin/master`, com `--base <ref>`.**

3. **Como instala sem o node_modules por symlink?** Opções:
   - `pnpm install --offline --frozen-lockfile` dentro do worktree, com falha clara que diz o comando online
     (recomendada). Custo: menos de 1 s; falha quando há dependência nova. Se paga: agora;
   - offline e depois online, sozinho. Custo: rede e minutos no pior caso, sem aviso. Se paga: quando o offline falhar na
     prática, o que não se mediu;
   - não instalar. Custo: o `verifyDepsBeforeRun` já derrubou o checkout principal uma vez. Se paga: nunca.

   **Decidido — offline, com falha clara.**

4. **Qual a regra do `--rm`?** Opções:
   - remove se o `HEAD` é ancestral da `origin/master` e o worktree está limpo; pede `--force` à branch sem commit
     próprio; trata o diretório órfão sem registro (recomendada). Custo: umas 30 linhas a mais. Se paga: no primeiro
     `--rm`;
   - só a regra da issue. Custo: o diretório órfão fica sem proteção, e a branch vazia passa por mergeada. Se paga: nunca,
     porque a perda é irreversível;
   - o `brza worktree rm` do app. Custo: não se conferiu se ele remove do disco e do git. Se paga: se o app guardar estado
     fora do `git worktree list`, o que não se mediu.

   **Decidido — merge, limpo e órfãos.**

### Rodada 2 — o `brza dev` e o baseline do `brza test` (enviada 2026-10-28)

**Apresentado antes:**
- **O seed:** o `pnpm dev:seed-profile` falha quando o perfil já tem estado (`config/scripts/dev-profile-seed.mjs:126-128`).
- **Um build por worktree:** cada worktree tem perfil e portas próprios (`config/scripts/dev-instance-isolation.mjs:90-111`).
  O lock de instância única é por `userData`, então dois builds no mesmo worktree colidem.
- **O pid:** o runner grava o `runnerPid` em `out/dev-instance.json`, não o apaga ao sair, e escala de SIGTERM para
  SIGKILL em 5 s (`config/scripts/run-electron-vite-dev.mjs:593-645`). Os dois pids em disco são de processos mortos.
- **O baseline:** nenhuma nota registra como foi refeito.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O `dev` semeia o perfil por padrão?** Opções:
   - só se o perfil do worktree está vazio, com `--no-seed` e `--reset` opcionais (recomendada). Custo: lê o perfil do
     `brza-dev` ou do app instalado na primeira subida. Se paga: agora, porque sem seed o build abre vazio e com a
     Interface de Chat desligada;
   - nunca semeia. Custo: toda conferência começa configurando o app à mão. Se paga: nunca;
   - sempre com `--reset`. Custo: perde o estado da conferência anterior. Se paga: nunca.

   **Decidido — só se o perfil está vazio.**

2. **Quantos builds por worktree, e de onde o `--stop` tira o pid?** Opções:
   - um por worktree, com o `runnerPid` de `out/dev-instance.json`, conferido vivo e como runner antes do SIGTERM
     (recomendada). Custo: umas 40 linhas. Se paga: agora;
   - vários por worktree. Custo: mexer no `dev-instance-isolation.mjs` do `brza-studio`. Se paga: nenhum caso levantado
     precisa;
   - pid próprio em `~/.local/state`. Custo: duplica o registro do runner. Se paga: nunca.

   **Decidido — um, pelo `dev-instance.json`.**

3. **A janela sobe visível ou em background?** Opções:
   - visível, com `--background` opcional, que põe `ORCA_BACKGROUND_LAUNCH=1` (recomendada). Custo: o agente que esquecer
     o flag rouba o foco. Se paga: agora, porque as conferências são com Anderson olhando;
   - background, com `--visible` opcional. Custo: na conferência, a janela não aparece sem o flag. Se paga: se a maioria
     das chamadas for de agente, o que não se mediu.

   **Decidido — visível, com `--background` opcional.**

4. **De onde o `test` tira o baseline da master?** Opções:
   - worktree temporário da `origin/master`, pelo código do `tree`, rodando só os arquivos que falharam, removido no fim
     (recomendada). Custo: segundos de criação e install, mais a corrida. Se paga: agora, porque não toca o checkout
     principal;
   - checkout principal com stash. Custo: mexe no que outras sessões usam. Se paga: nunca;
   - sem baseline. Custo: o julgamento volta à mão. Se paga: só se o baseline ficar caro, o que não se mediu.

   **Decidido — worktree temporário.**

### Rodada 3 — o `brza test`, o `brza app install` e o `brza_runtime.py` (enviada 2026-10-28)

**Apresentado antes:**
- **O `check:changed`:** sem `--base`, ele cai em `origin/main`, que não existe no `brza-studio`
  (`config/scripts/check-changed.mjs:48,64`).
- **O build:** o `build:mac` grava na versão o `HEAD` de onde roda (`config/scripts/build-mac-local.mjs:22-30`). O alvo
  padrão é `dir`.
- **O app aberto:** o chat roda dentro do `/Applications/BrzA Studio.app`, e o `claude-brza` e os `brza-*` chamam o CLI
  dele. Ninguém mediu o que o `ditto` faz com o app aberto.
- **O que o P0 deixa para o `app install`:**
  - a reinstalação, com a conferência do `brza sessions --help` no chat e no terminal;
  - a troca de `brza-install`/`brza-run` por `brza install`/`brza run` na ajuda dos scripts e no `CLAUDE.md`.
- **A duplicação:** o `canonicalize` e o `send_to_chat` estão iguais em `brza-run:109-133` e `brza-sessions:82-100`.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **O que o `test` roda?** Opções:
   - os testes dos caminhos alterados contra `origin/master` e o `check:changed --base=origin/master`, sempre com a base
     injetada (recomendada). Custo: o tempo do `check:changed`, que não se mediu. Se paga: agora, porque o `--base`
     esquecido já quebrou a corrida;
   - só o vitest por caminho. Custo: lint, tipos e ratchets voltam à mão. Se paga: só se o `check:changed` for lento demais.

   **Decidido — vitest e `check:changed`.**

2. **O `app install` pede confirmação antes de sobrescrever?** Opções:
   - pergunta antes do `ditto`, recusa com o app aberto (saída 2) sem `--yes` e só apaga `dist` com `--clean`
     (recomendada). Custo: um `--yes` a mais. Se paga: na primeira vez com sessões abertas;
   - sem confirmação. Custo: a sessão que roda o comando pode derrubar a si mesma e às outras. Se paga: nunca;
   - instala ao lado e troca no fim. Custo: mais 1,8 GB temporário. Se paga: se a falha no meio do `ditto` virar problema.

   **Decidido — confirma e recusa com o app aberto.**

3. **De que checkout o `app install` constrói?** Opções:
   - um worktree da `origin/master` pelo código do `tree`, com `--from <caminho>` e `--dmg` opcionais (recomendada).
     Custo: um worktree e um install a mais por build. Se paga: agora, porque o checkout principal está sujo;
   - sempre do checkout principal. Custo: constrói o que estiver lá. Se paga: nunca;
   - do diretório atual. Custo: o resultado depende de onde a sessão está. Se paga: para testar um worktree antes do
     merge, que o `--from` também cobre.

   **Decidido — worktree da `origin/master`.**

4. **O `canonicalize` e o `send_to_chat` vão para o `brza_runtime.py`?** Opções:
   - sim, e o runtime ganha a constante `STUDIO`, do checkout do `brza-studio`; o contrato só cresce (recomendada). Custo:
     ajustar os patches de `test_brza_sessions.py:62-76` e `test_brza_scripts.py:110-113`. Se paga: no primeiro
     `sessions send`;
   - não. Custo: três cópias do envio. Se paga: nunca;
   - módulo novo `brza_chat.py`. Custo: mais um arquivo. Se paga: se o runtime passar de ~200 linhas (tem 77).

   **Decidido — sim, com o `STUDIO`.**

### Rodada 4 — o `brza-install`, o `brza doctor`, o `brza note` e a ordem (enviada 2026-10-28)

**Apresentado antes:**
- **O `brza-install`:** liga uma lista fixa de três scripts, com uma flag por script
  (`scripts/brza/brza-install:24-26,82-84`). A `brza-cli-subcomandos` deixou duas coisas para o PLN-002: o
  `~/.local/bin/brza-install` não está no PATH, e ele deve ligar a si mesmo.
- **O PATH:** o do chat é diferente do do terminal. O `brza-dev-wt` ainda não existe, e isso é normal.
- **As notas:** não há molde de worklog nem de issue (`work/README.md:84`). O frontmatter de cada pasta está em
  `work/README.md:140-149`, e o `## Fora do workspace`, em `:297-303`.
- **O encadeamento:** o `dev`, o `test` e o `app install` usam o worktree do `tree`. O `doctor` confere o que os outros
  instalam.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **Como o `brza-install` liga os scripts novos?** Opções:
   - glob `brza-*` executável em `scripts/brza/`, inclusive ele mesmo, com as flags de hoje como atalho (recomendada).
     Custo: ajustar o `InstallTest.setUp` (`test_brza_scripts.py:168-180`). Se paga: no segundo script novo;
   - uma flag por script. Custo: sete flags novas. Se paga: nunca.

   **Decidido — glob `brza-*`, inclusive ele.**

2. **O que o `doctor` trata como erro?** Opções:
   - sai com 1 se falta identidade, hook de medição, link em `~/.local/bin` ou override `claude-brza`; só avisa o que
     depende de onde roda, como o pnpm no PATH e o perfil `brza-dev` (recomendada). Custo: umas 100 linhas. Se paga:
     agora, como portão no arranque;
   - tudo é aviso. Custo: não serve de portão. Se paga: nunca.

   **Decidido — erro no essencial.**

3. **O que o `note` faz?** Opções:
   - `note new <issue|worklog> <assunto>` gera o esqueleto; `note commit <caminho…> -m` roda o `check_notes.py`, `git add`
     por caminho, commit e `pull --rebase` (recomendada). Custo: o texto do esqueleto é escolha nova, que vai ao Desenho.
     Se paga: agora;
   - só `commit`. Custo: o esqueleto segue à mão. Se paga: se o esqueleto variar demais, o que não se viu.

   **Decidido — `new` e `commit`.**

4. **Em que ordem os passos rodam?** Opções:
   - primeiro o runtime e o `brza-install` por glob; depois o `tree`; depois `dev`, `test`, `app install` e `note` em
     paralelo; o `sessions` quando a combinação com a 2d fechar; o `doctor` por último (recomendada). Custo: dois passos em
     série antes do resto. Se paga: agora, porque evita conflito no `brza_runtime.py` e no `brza-install`;
   - todos em série. Custo: o tempo total soma os sete. Se paga: se só uma sessão executar;
   - todos em paralelo. Custo: conflito nos dois arquivos comuns. Se paga: nunca.

   **Decidido — base, `tree`, paralelo, `doctor`.**

### Rodada 5 — o nome do `tree`, o `sessions` e o executor (enviada 2026-10-28)

**Apresentado antes:**
- **O nome:** a norma pede a branch `<tipo>/pln-NNN-<slug>` e o worktree em `.worktrees/` (`plans/README.md:23`). Hoje o
  diretório é `pln-001-p48` e a branch é `feat/pln-001-p48`; o padrão `feat` não tem fonte.
- **O `sessions`:** a escolha de 2026-10-28 foi "Reabrir a 2d e combinar", e a `brza-workspace-2d` não está aberta. Os
  RPCs do app são `session.tabs.listAll` (`src/main/runtime/rpc/methods/session-tabs.ts:44-51`), `agentSession.send`,
  `agentSession.close` (`structured-agent-session.ts:147-170`) e `session.tabs.close`
  (`session-tab-close-methods.ts:13-60`, com `reason`). Não se conferiu se o título da aba é o nome do `/rename`, nem se
  o `reason: 'user'` passa vindo de script.
- **O executor:** os scripts moram no `brza-workspace`, sem a convenção de worktree, com commit direto na `master`. O
  PLN-001 usou workers do Orca no trecho paralelo.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **Como o `tree` nomeia diretório e branch?** Opções:
   - `brza tree <nome> [--type feat|fix|docs|chore]`: diretório `.worktrees/<nome>`, branch `<tipo>/<nome>`, tipo padrão
     `feat`, e o `<nome>` traz o `pln-NNN-` quando é de plano (recomendada). Custo: um flag a mais. Se paga: agora;
   - tipo obrigatório. Custo: digitá-lo sempre. Se paga: se o `feat` padrão errar com frequência, o que não se viu;
   - `--plan PLN-NNN` monta o nome. Custo: mais um flag e mais lógica. Se paga: se quase todo worktree for de plano.

   **Decidido — `<nome>` e `<tipo>/<nome>`, com `feat` padrão.**

2. **Como o passo do `sessions` entra no plano?** Opções:
   - o Desenho leva a proposta, e o passo começa pela combinação com a 2d, que Anderson reabre, conferindo os dois pontos
     não medidos e ajustando o `D` antes do código (recomendada). Custo: uma sessão a mais para abrir. Se paga: no primeiro
     `close` que não deixa aba órfã;
   - passo bloqueado até a 2d devolver a interface. Custo: um `D` vazio e um passo sem estimativa. Se paga: se a 2d tiver
     ideia muito diferente;
   - sem a 2d, o executor decide. Custo: reverte a escolha "Reabrir a 2d e combinar". Se paga: se a 2d não for reaberta.

   **Decidido — proposta, com a combinação como primeiro subpasso.** → reaberta em
   [PLN-003/R6.1](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md), em 2026-10-29: "Sessão nova pln-002-p7, eu
   abro (Recomendado)". A combinação sai da 2d e vai à sessão `pln-002-p7`, que a faz sem ela.

3. **Quem executa os passos de script?** Opções:
   - uma sessão por passo, `claude --name pln-002-pN` no `brza-workspace`, aberta por Anderson, com commit direto na
     `master` e `git add` por caminho (recomendada). Custo: abrir e conduzir uma sessão por passo. Se paga: agora, pela
     norma "uma tarefa, uma sessão";
   - workers do Orca, como no PLN-001. Custo: especificações e uma Run, com os workers no mesmo checkout. Se paga: no
     trecho de quatro passos em paralelo;
   - uma sessão para tudo. Custo: contexto grande e regravação de cache. Se paga: nunca.

   **Decidido — uma sessão por passo.**

### Rodada 6 — onde mora o código do worktree (enviada 2026-10-28)

**Apresentado antes:** o `tree`, o baseline do `test` (R2.4) e o `app install` (R3.3) criam worktree "pelo código do
`tree`", e o lugar desse código não estava decidido.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **Onde mora o código que cria o worktree e instala offline?** Opções:
   - no `brza_runtime.py`, como `worktree_add(path, base, branch=None)` e `install_offline(path)` (recomendada). Custo: o
     runtime cresce umas 50 linhas e passa a ter git. Se paga: agora, porque os três passos paralelos partem da mesma
     função, testada uma vez;
   - o `test` e o `app install` chamam o `brza-tree` como processo. Custo: `--detach` no `tree`, as regras do `--rm` no
     worktree temporário, e o P3 ao P5 esperando o P2. Se paga: se o `tree` ganhar regra que os outros devam seguir;
   - módulo novo `brza_worktree.py`. Custo: mais um arquivo, fora do contrato. Se paga: se o runtime passar de ~200 linhas.

   **Decidido — no `brza_runtime.py`.**

### Rodada 7 — os pontos sem lastro do desenho e o corte (enviada 2026-10-28)

**Apresentado antes:** o D1 ao D8 e o P1 ao P8, gravados em `a518b8b`, e os pontos que entraram no rascunho sem fonte:
`tree --list`, `dev --status`, o `install --all` como flag, o aviso de app velho no `doctor`, o push do `note commit`
só com `--push` (o `AGENTS.md` manda o push direto na `master`) e a escolha dos testes do `brza test`.

Respondida em 2026-10-28, na sessão `pln-002-comandos-brza`.

1. **Quais extras ficam?** Seleção múltipla:
   - `tree --list` e `dev --status` (recomendada). Custo: ~30 linhas cada, no P2 e no P3. Se paga: na primeira limpeza de
     worktrees e na primeira conferência;
   - o aviso de app velho no `doctor` (recomendada). Custo: ~15 linhas no P8. Se paga: no primeiro esquecimento de
     reinstalar;
   - `install --all` virar o padrão. Custo: muda o `brza install` sem flag, que hoje mostra o estado. Se paga: nunca, se
     mostrar continuar útil.

   **Decidido — `tree --list`, `dev --status` e o aviso de app velho.** O `--all` fica flag.

2. **O `note commit` faz o push?** Opções:
   - sempre, com `--no-push` (recomendada). Custo: rede pela chave `personal` em todo commit. Se paga: agora;
   - só com `--push`. Custo: a nota pode ficar só no local. Se paga: se houver muito commit em série, o que não se viu.

   **Decidido — sempre, com `--no-push`.**

3. **Quais testes o `test` escolhe sem caminho dado?** Opções:
   - o `*.test.ts` alterado e o vizinho de cada fonte alterada, com "sem teste" para a fonte sem vizinho (recomendada).
     Custo: ~20 linhas; teste que mora longe fica de fora. Se paga: agora;
   - o `vitest --changed`. Custo: não se conferiu se o `run-vitest.mjs` repassa o flag. Se paga: se o P4 mostrar que
     funciona;
   - sempre a suíte inteira. Custo: o tempo da suíte, não medido. Se paga: antes de push, se a suíte for rápida.

   **Decidido — alterados e vizinhos.**

4. **O corte — P1 a P8, um por comando, 18 h — está aceito?** Opções:
   - aceitar como está (recomendada). Custo: 8 sessões. Se paga: agora;
   - juntar o P1 ao P2. Custo: um passo de 4 h, e o P3 ao P6 esperam mais. Se paga: uma sessão a menos;
   - dividir o P5. Custo: uma sessão a mais. Se paga: se o C2 precisar de outro dia.

   **Decidido — aceitar como está.** É o aceite do plano, em 2026-10-28.

### Rodada 8 — o `--dmg` e a substituição do app, no P5 (enviada 2026-10-28)

**Apresentado antes:**
- **O `--dmg` e o worktree temporário:** o D5 constrói num worktree que sai no fim (R3.3), e o `.dmg` iria junto. O
  fluxo manual era `build:mac --dmg`, `ditto` e `rm -rf dist`
  (`work/issues/os-comandos-brza-que-viram-o-pln-002.md:41`): o dmg nascia e se jogava fora.
- **O `ditto` sobre um `.app` que existe mescla:** o arquivo que saiu da versão nova fica no pacote e quebra o selo da
  assinatura ad hoc. A primeira instalação foi num destino vazio
  (`work/worklogs/2026-10-27-brza-studio-convive-com-o-orca.md:97-99`).

Respondida em 2026-10-28, na sessão `pln-002-p5`.

1. **Com o build no worktree temporário, para onde vai o `.dmg` do `--dmg`?** Opções:
   - `~/Downloads`, com o caminho impresso (recomendada). Custo: ~470 MB por build com `--dmg`. Se paga: na primeira vez
     que o build for entregue a alguém;
   - só com `--from`, e o `--dmg` sem ele é uso errado. Custo: o dmg da `origin/master` pede um checkout limpo à mão. Se
     paga: agora, se o dmg quase nunca for usado;
   - no diretório atual. Custo: cai onde a sessão estiver. Se paga: nunca, comparado a `~/Downloads`.

   **Decidido — `~/Downloads`.**

2. **Como o app novo substitui o que está em `/Applications`?** Opções:
   - apaga o antigo e copia com `ditto`; o `ditto` que falha deixa o worktree e imprime o comando a repetir
     (recomendada). Custo: segundos sem app instalado. Se paga: no primeiro build que tirar um arquivo do pacote;
   - `ditto` por cima, mesclando. Custo: o arquivo que saiu fica e quebra a assinatura. Se paga: nunca.

   **Decidido — apaga e copia.**

### Rodada 9 — a combinação do D7, sem a 2d (enviada 2026-10-29)

**Apresentado antes**, medido nesta sessão contra o app aberto:
- **O título da aba não é o nome.** O `session.tabs.listAll` deu `"PLN-002 P7: renomear chat"` para o chat
  `claude_d839fe67_…`, renomeado `pln-002-p7`. O título é o nome do chat no app, trocado pelo `agentSession.rename`
  (`brza-studio/src/main/runtime/rpc/methods/structured-agent-session-rename.ts:1-2`); o `/rename` não chega a ele.
- **O app liga o chat à sessão do Claude.** O `agentSession.history` devolve `providerSession: {"key": "session_id",
  "id": "56c85a7b-…"}`, o mesmo `--session-id` do processo, também para o chat parado, sem processo vivo.
- **O nome do `/rename` fica no transcript**, `{"type": "custom-title", "customTitle": "pln-002-p7"}`, em
  `~/.claude/projects/<cwd>/<id>.jsonl`. O `~/.claude/sessions/<pid>.json` também o traz, mas só do processo vivo: 4
  arquivos para 7 chats.
- **A trava roda no chat**, que sobe com o `--settings` do workspace; o `send` comum a uma sessão grande parada seria
  barrado lá dentro sem o script saber (`.claude/hooks/resume_guard.py:141-170`), o conflito K5 do PLN-003.

Respondida em 2026-10-29, na sessão `pln-002-p7`.

1. **De onde o `brza sessions` tira o nome do chat?** Opções:
   - o transcript: `listAll` → `history.providerSession.id` → o último `custom-title` (recomendada). Custo: ler o
     transcript de cada chat a cada `list`; ~30 linhas. Se paga: agora, porque cobre os chats abertos à mão;
   - o registro dos processos vivos. Custo: o chat sem processo fica sem nome. Se paga: se o transcript ficar lento;
   - o título da aba, com o `open` chamando o `agentSession.rename`. Custo: o chat renomeado só pelo `/rename` não é
     achado. Se paga: nunca sozinho.

   **Decidido — o transcript.** → reaberta em R12.3.

2. **O `open` também troca o título da aba pelo nome?** Opções:
   - não agora; o `list` mostra o nome e o título lado a lado (recomendada). Custo: a aba segue com o título
     automático. Se paga: agora, sem mudar o escopo;
   - sim, no `open`. Custo: ~0,3 h e o fim do título automático. Se paga: quando o nome for procurado na tela.

   **Decidido — não agora.** → reaberta em R11.4.

3. **O que o `send` faz quando a trava barraria o destino?** Opções:
   - recusa com saída 3 e a conta da trava, também no `--json`; o `--wake` grava a passagem no `guard.json`, como o
     reenvio, e manda uma vez (recomendada). Custo: ~0,5 h e o acoplamento ao `resume_guard.py`. Se paga: no primeiro
     envio do roteador do PLN-003 a uma sessão grande parada;
   - só recusa. Custo: acordar de propósito pede o reenvio à mão. Se paga: se a regra virar "nunca acordar por script";
   - avisa e manda. Custo: a mensagem é barrada lá dentro e o script sai 0. Se paga: nunca.

   **Decidido — recusa, e o `--wake` passa.** → reaberta em R10.1.

4. **O `close` num chat no meio de um turno?** Opções:
   - recusa com saída 1 sem `--force` (recomendada). Custo: uma flag e um teste. Se paga: no primeiro `close` por
     engano;
   - fecha sempre. Custo: o turno em curso se perde. Se paga: só com um `list` conferido antes de todo `close`.

   **Decidido — recusa sem `--force`.**

### Rodada 10 — o `send` sem a trava de retomada (enviada 2026-10-29)

**Apresentado antes:** a sessão `brza-workspace-b7` mandou, por correio, a rodada que Anderson respondeu lá em
2026-10-29: "O que fazer com a trava de retomada (resume_guard no UserPromptSubmit)?" → "Desligar (Recomendado)", cuja
opção dizia que o `brza sessions send` deixa de consultá-la. A mudança estava na árvore, sem commit nem "decidido", e o
P7 já tinha a trava no `send` em `brza-workspace@9daa020` (R9.3).

Respondida em 2026-10-29, na sessão `pln-002-p7`.

1. **Com a trava desligada, como fica o `send`?** Opções:
   - tirar a trava do `send`: saem a saída 3, o `--wake`, o `guard` do `--json` e a linha do `list`, e o
     `resume_guard.py` volta ao que era (recomendada). Custo: ~0,3 h; o roteador do PLN-003 pode acordar uma sessão
     grande parada sem aviso. Se paga: agora, sem campo morto no contrato do `--json`;
   - aviso sem recusa, com o `guard` no `--json`. Custo: ~0,3 h e o `resume_guard.py` vivo só como calculadora. Se paga:
     quando o roteador precisar pesar o custo antes de acordar;
   - manter até o "decidido" da b7. Custo: o `send` recusa o que o hook já não barra. Se paga: só se a b7 voltar atrás.

   **Decidido — tirar a trava do `send`.**

### Rodada 11 — o pedido 8: o destino, a revisão, a flag e o título (enviada 2026-10-29)

**Apresentado antes**, lido nesta sessão:
- **Hoje o nome é o `/rename`.** O `open` manda `/rename <nome>` como primeiro prompt (`scripts/brza/brza-sessions:249-250`);
  o `list`, o `send` e o `close` acham o chat pelo `custom-title` do transcript (`:113-131`); o `running()`, que pula o
  nome que já roda, e o `--wait` leem o mesmo nome.
- **Sem o `/rename`, esse caminho some** para a sessão nova, e o mapa vira a fonte do par nome e chat, o que reabre a
  R9.1, que descartou "o registro nome e id gravado pelo `open`".
- **O título da aba sai do `agentSession.rename`**, o nome único do chat no app
  (`brza-studio/src/main/runtime/rpc/methods/structured-agent-session-rename.ts:1-2`).
- **O correio endereça pelo nome da sessão do Claude** (`CLAUDE.md`, a tabela do vocabulário), que só o `/rename` dá.

Respondida em 2026-10-29, na sessão `pln-002-sessions-rename`.

1. **Onde entra o pedido do `/rename` opcional e do mapa de sessões?** Opções:
   - pedido 8 do PLN-002: o D7 reescrito no lugar e o P9; o plano volta à execução (recomendada). Custo: ~0,3 h de
     registro e o plano reaberto. Se paga: agora, porque o D7 e o `--json` do `list` são contrato deste plano e do
     roteador do PLN-003;
   - um PLN-004 próprio. Custo: ~0,5 h de arranque, um Terreno que repete o do D7 e dois planos no mesmo script. Se
     paga: só se o mapa crescer além do `brza sessions`;
   - uma issue para depois. Custo: os pedidos 31 e 32 do PLN-001 seguem com o `/rename` e o `--wait` de hoje. Se paga:
     se não houver pressa.

   **Decidido — pedido 8 do PLN-002.**

2. **A revisão da entrega (P0 ao P8) vem quando?** Opções:
   - uma só, depois do P9 (recomendada). Custo: a revisão espera o P9, de 2 a 3 h. Se paga: no fim do P9, com uma
     corrida de revisor em vez de duas, sem revisar um D7 que vai mudar;
   - agora, em paralelo ao P9. Custo: duas revisões, e a primeira lê um D7 a reescrever. Se paga: se o P9 for demorar
     dias.

   **Decidido — uma só, depois do P9.**

3. **Qual o nome da flag que liga o `/rename`, desligado por padrão?** Opções:
   - `--rename` (recomendada). Custo: nenhum além do nome. Se paga: agora;
   - `--claude-name`. Custo: mais longo, e confunde com o `--name` do `claude`, que o chat não tem. Se paga: só se surgir
     outro jeito de dar o nome.

   **Decidido — `--rename`.**

4. **De onde sai o título da aba?** Opções:
   - `--title` opcional; sem ele, o `<nome>`. O `<nome>` curto segue como chave do `send` e do `close`, e o título vai ao
     `agentSession.rename` (recomendada). Custo: ~0,3 h e uma flag a mais na abertura com título. Se paga: agora, sem
     aspas nem espaço no `send` e no `close`;
   - `--title` obrigatório. Custo: quebra as chamadas de hoje. Se paga: nunca, a não ser que a aba sem título vire
     problema;
   - o `<nome>` já é o título, e o mapa usa o título como chave. Custo: aspas em todo `send` e `close`, e chave com espaço
     e dois-pontos. Se paga: se só humanos chamarem o comando.

   **Decidido — `--title` opcional; sem ele, o `<nome>`.**

### Rodada 12 — o mapa, a leitura, a busca e o D50 do PLN-001 (enviada 2026-10-29)

**Apresentado antes:**
- **O `--wait` dos pedidos 31 e 32 do PLN-001** espera o `/rename` em `<config>/sessions/<pid>.json`
  (`brza-sessions:95-101`); sem o `--rename`, não tem o que esperar.
- **O `brza-studio` é o app genérico do PLN-001**; o mapa é arquivo de script do workspace, e o renderer do P64 não chama
  a CLI.
- **O remetente do D48 é o `from=` do correio**, o nome da sessão do Claude (`PLN-001-design.md:515-529`). O `from=` de
  uma sessão sem `/rename` não foi medido; fica para a combinação do P9.

Respondida em 2026-10-29, na sessão `pln-002-sessions-rename`.

1. **Onde mora o mapa, e em que formato?** Opções:
   - JSON em `.sessions/sessions.json` do workspace, um objeto por nome (recomendada). Custo: ~0,5 h; a entrada da aba
     fechada à mão fica velha. Se paga: no primeiro `send` a uma sessão aberta sem `--rename`;
   - JSONL só de acréscimo, uma linha por evento (`open`, `title`, `close`). Custo: quem lê reconstrói o estado a cada
     leitura; ~0,2 h a mais. Se paga: quando se quiser o histórico das sessões;
   - no `userData` do app. Custo: o dev build tem outro `userData` e outro mapa. Se paga: só se o app for ler o mapa.

   **Decidido — JSONL só de acréscimo.** O lugar foi à R13.1.

2. **Como o orquestrador ou o coordenador lê o mapa?** Opções:
   - pelo `brza sessions list --json`, que junta o mapa ao estado do app; o arquivo é detalhe interno, e o contrato só
     cresce com `opened` e `source` (recomendada). Custo: ~0,2 h. Se paga: agora, com um contrato só para o roteador do
     PLN-003;
   - o arquivo direto. Custo: dois contratos, e o arquivo não sabe se a aba segue aberta. Se paga: só se o leitor não
     puder chamar a CLI.

   **Decidido — pelo `list --json`.**

3. **Como o `list`, o `send`, o `close` e o `open` acham o nome?** Opções:
   - o mapa primeiro e o `custom-title` do transcript depois; o `open` pula o nome que o mapa tem com o chat ainda no
     `listAll` (recomendada). Custo: ~0,5 h, e reabre a R9.1. Se paga: agora, com o chat renomeado à mão ainda achado;
   - só o mapa. Custo: o chat aberto à mão com `/rename` deixa de ser achado. Se paga: nunca, enquanto houver chat aberto
     fora do `brza sessions`.

   **Decidido — o mapa primeiro, o `/rename` depois.**

4. **O mapa serve também ao P64 do PLN-001 (D50)?** Opções:
   - não; o P64 usa o que o app guarda, e o PLN-002 grava uma linha no `Retomar` do PLN-001 sobre o `--rename`
     desligado (recomendada). Custo: o P64 resolve o nome sozinho, no app. Se paga: agora, sem o app genérico depender
     de um arquivo do workspace;
   - sim, o app lê o mapa. Custo: o mapa vai ao `userData` do app e só cobre as sessões abertas pelo script; ~1 h a mais
     no P64. Se paga: se toda sessão for aberta pelo `brza sessions`.

   **Decidido — não; o P64 usa o que o app guarda.**

### Rodada 13 — o lugar do mapa, o `--wait`, o verbo `title` e o correio (enviada 2026-10-29)

**Apresentado antes:** a opção do JSONL, na R12.1, não dizia o lugar. Pelo `CLAUDE.md`, o correio endereça a sessão pelo
nome dela, que hoje só o `/rename` dá.

Respondida em 2026-10-29, na sessão `pln-002-sessions-rename`.

1. **Onde mora o JSONL?** Opções:
   - `.sessions/sessions.jsonl` na raiz do `brza-workspace`, fora do git como o `.measurements/`; as sessões do
     `brza-studio` gravam ali pela `WORKSPACE` do runtime (recomendada). Custo: uma linha no `.gitignore`. Se paga: agora;
   - `~/.local/state/brza/sessions.jsonl`. Custo: entra no `## Fora do workspace`, e o backup do workspace não o leva. Se
     paga: só se os scripts forem usados fora do workspace.

   **Decidido — `.sessions/sessions.jsonl` do workspace.**

2. **O que o `--wait` espera com o `/rename` desligado?** Opções:
   - o `claude_session` do chat: sem `--rename`, espera o `agentSession.history` dar o `providerSession.id` e o grava no
     mapa; com `--rename`, espera também o nome (recomendada). Custo: ~0,3 h; o id talvez só apareça depois do primeiro
     turno, a conferir no P9. Se paga: no primeiro `send` do coordenador logo depois do `open`;
   - o `--wait` exige `--rename`. Custo: os pedidos 31 e 32 e a memória passam a `--rename --wait`. Se paga: se só o
     nome do Claude importar;
   - o `--wait` sai. Custo: quebra as chamadas de hoje. Se paga: nunca, enquanto houver chamada com `--wait`.

   **Decidido — o `claude_session` do chat.**

3. **Entra um verbo para trocar o título da aba depois de aberta?** Opções:
   - não agora (recomendada). Custo: retitular pede o app. Se paga: agora, sem crescer o escopo;
   - sim, `brza sessions title <nome> "<título>"`, com o `agentSession.rename` e uma linha `title` no mapa. Custo: ~0,3 h
     e um teste. Se paga: quando o coordenador mudar a fase de uma sessão.

   **Decidido — sim, `brza sessions title`.**

4. **Quem abre sessão que conversa por correio passa `--rename`?** Opções:
   - sim, e a regra vai à ajuda do `brza sessions` e à memória de abrir sessão; o resto usa o `brza sessions send`
     (recomendada). Custo: ~0,1 h de texto. Se paga: no primeiro `SendMessage` para uma sessão aberta pelo script;
   - não; entre sessões abertas pelo script, o canal passa a ser o `send`. Custo: o `SendMessage` para essas sessões não
     acha o destino, e o remetente do D48 fica sem nome. Se paga: se o correio do runtime cair em desuso.

   **Decidido — sim, e a regra vai à ajuda e à memória.**
