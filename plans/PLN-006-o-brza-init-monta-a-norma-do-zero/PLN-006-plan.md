---
status: in_progress
phase: execution
origin: request
ready: sim
estimate_h: 27
executed_h: 2
remaining_h: 10.5
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - tooling
---

# PLN-006: O `brza init` monta a norma num workspace do zero

- **Retomar:** P1, P2, P3, P4 e P7 feitos (`brza-workflow@acf8bef`). Em curso: o P6, em `.worktrees/p6`; depois o P5,
  que chama a camada 1 do sync (X17) e reconcilia o bloco do shell (X18); então P8 e P9. Pontos novos vão na
  recomendada, pela regra de Anderson após a R10.
- **Dividido:** [PLN-006 — Desenho](PLN-006-design.md)

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "nós já temos mecanismos para inicializar a norma inteira, com AGENTS CLAUDE plans/ wiki/ work/ skills/ agents/ num
> repositório do zero?"

Respondido que não, Anderson pediu: "plano".

### Cobertura

| Origem         | Critério de aceite                                                                                                                                                                                  | Passo  | Teste (nível)                                         |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :---------------------------------------------------- |
| `Pedido 1`     | `brza init <dir>` cria, num diretório vazio, um workspace com `AGENTS.md`, `CLAUDE.md`, `README.md`, `plans/`, `wiki/`, `work/`, `.claude/skills/`, `.claude/agents/`, hooks e `settings.json`, e o `notes-checker` roda verde nele | P5     | unidade, num diretório temporário                     |
| `R1.2`         | O workspace inicializado aponta para o repositório de código dele, sem caminho fixo a `brza-workspace` ou `brza-studio` no que foi copiado                                                         | P3, P5 | unidade                                               |
| `R1.4`         | Uma mudança no núcleo genérico chega ao workspace inicializado pelo `brza sync`, sem tocar a parte local dele                                                                                     | P6     | unidade                                               |
| `Pedido 1`     | O `brza-workspace` segue funcionando depois da separação genérico/local: hooks, skills, `brza note` e os testes de hoje                                                                            | P1, P7, P8 | as três suítes (unidade); a Regressão (manual)    |
| `R4.1`, `R7.1` | Do repositório de código, inclusive de um worktree fora do diretório dele, o `brza where`, os hooks e o `claude-brza` acham o workspace pelo `~/.config/brza/workspaces.toml`; sem entrada, nada; o `brza register` recusa ligar um código a dois workspaces | P2 | unidade, com `BRZA_REGISTRY` e um worktree temporário |
| `R4.4`         | O `CLAUDE.md` do workspace inicializado começa com `@AGENTS.md`                                                                                                                                    | P3     | unidade                                               |
| `R5.1`, `R5.3` | `brza note plan-open` numera pelo índice (maior + 1) e grava `created` na `origin/master`; dois `plan-open` em corrida saem com números diferentes                                                 | P4     | unidade, com remote bare local                        |
| `R5.3`, `R7.4` | `brza note commit` de plano, issue ou decisão com frontmatter mudado acrescenta uma linha `changed` na `origin/master` sem tocar o checkout principal; sem mudança, nenhuma linha                  | P4     | unidade                                               |
| `R5.2`         | Duas linhas acrescentadas em paralelo se juntam pelo `merge=union`, e o estado vigente de cada id é o de maior `ts`                                                                                | P4     | unidade                                               |
| `R5.1`         | Depois da migração, o índice traz PLN-001 a PLN-006, as issues e as decisões de todos os workstreams                                                                                              | P8     | `brza note index --rebuild` e a contagem (manual)     |
| `R6.2`         | Com um arquivo do núcleo editado no workspace, o `brza sync` não o escreve, mostra o diff e sai com 1; `--force <caminho>` o escreve e atualiza o lock                                             | P6     | unidade                                               |

### Fora de escopo

- **A norma dentro do próprio repositório de código, sem workspace separado.** Fica de fora pela R1.2; volta como plano
  novo se um projeto pedir.
- **Generalizar o `brza tree` e o `brza test` para outro repositório de código.** Já decidido no
  [PLN-003: O workflow do workspace roda igual no BrzA Studio e no Orca, por plugins e pelo `brza`](../PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md),
  R2.3, no workstream `tools-kit`; este plano não o refaz.
- **O coordenador que lê o índice da `master`.** Pela R5.4, vai a
  [O coordenador se baseia no índice de notas da master](../../work/issues/o-coordenador-le-o-indice-da-master.md); o
  PLN-006 entrega só o índice.

## Entrevista

### Rodada 1 — destino, alvo, mecanismo e atualização (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- Não há mecanismo de inicialização. As peças de hoje — `brza note workstream`, `memory-setup`, `new`, `sync`,
  `brza install`, o `notes-checker` — só operam dentro do `brza-workspace` já montado.
- Os caminhos estão fixos em `scripts/brza/brza_runtime.py:21-23` (`brza-workspace`, `brza-studio`, o `Application
  Support/brza-studio`); a função `claude` do `~/.zshrc` e o `claude-brza` só reconhecem os dois repositórios.
- O `measure.py` e o `compact_guard.py` gravam no `.measurements/` do `BRZA_WORKSPACE`.
- A `master` tem ~14 mil linhas versionadas, metade teste. Umas 250 linhas, em ~40 arquivos, citam o que é local
  (BrzA Studio, `brza-studio`, Anderson, `brz-anderson`, Fixfy, Orca, `~/Projects`); as que mais citam são o
  `CLAUDE.md` (22), o `work/README.md` (16), o `brza-shot` (14), a `plan-runner/SKILL.md` (13), o `AGENTS.md` (12) e o
  molde de plano (12).
- A separação genérico/local custa ~4–6 h em qualquer caminho, e o mecanismo vem em cima.

Respondida em 2026-10-31.

1. **Destino.** Opções:
   - `PLN-006` no `workspace` (recomendada) — custo: abrir o `PLN` (~10 min) e uma linha na `master`; se paga: já,
     porque o trabalho atravessa sessões;
   - `PLN` no `tools-kit` — custo: o mesmo, com a separação da norma virando pedido cruzado; se paga: só se o mecanismo
     pesar mais que a separação;
   - worklog de hoje — custo: nenhum agora; se paga: nunca, porque ~10 h não fecham numa sessão.

   **Decidido — "PLN-006 no workspace (Recomendado)".**

2. **Alvo.** Opções:
   - workspace ao lado do código, como o par `brza-workspace` + `brza-studio` (recomendada) — custo: tirar os caminhos
     fixos e parametrizar o par, ~2–3 h; se paga: no primeiro projeto novo;
   - norma dentro do código, sem workspace separado — custo: refazer o modelo de workstreams, ~4–6 h a mais; se paga: em
     projeto pequeno;
   - os dois formatos — custo: a soma, ~6–9 h, e testes dobrados; se paga: só com os dois em uso.

   **Decidido — "Workspace ao lado do código (Recomendado)".**

3. **Mecanismo.** Opções:
   - `brza init`, script determinístico que copia o núcleo genérico e preenche o local por flags ou prompt (recomendada)
     — custo: ~3–4 h com testes, além da separação; se paga: a partir do segundo repositório;
   - skill com entrevista, rodada por um agente — custo: ~2–3 h, mais tokens a cada uso, com saída que varia; se paga:
     quando a parte local exigir texto livre;
   - repositório template do GitHub — custo: ~1–2 h, com a parte local editada à mão a cada vez; se paga: só se a parte
     local for mínima.

   **Decidido — "brza init, script (Recomendado)".**

4. **Atualização.** Opções:
   - acompanha por sync, com o núcleo genérico numa fonte que o workspace novo puxa (recomendada) — custo: ~3–5 h, e a
     fronteira genérico/local em arquivos separados; se paga: na primeira mudança de norma, que muda quase todo dia;
   - cópia que diverge — custo: zero agora, e cada melhoria portada à mão; se paga: só em repositório curto.

   **Decidido — "Acompanha por sync (Recomendado)".**

### Rodada 2 — a fonte, a fronteira, o núcleo e a raiz (enviada 2026-10-31)

**Apresentado antes**, pelo Terreno do `collector` (inventário em `/private/tmp/pln006/terreno.md`, fora do git),
conferido por amostra na sessão:
- A `master` não versiona as pastas de nota: só o `plans/README.md` e o `work/README.md`. O init precisa criar o
  esqueleto.
- O `AGENTS.md`, o `work/README.md` e o `plans/README.md` são ~90% genéricos; o local está em trechos fechados — "Quem
  commita" (`AGENTS.md:60-65`), as funções do shell, a identidade (`CLAUDE.md:58-67`), a medição datada
  (`CLAUDE.md:134-141`) e as datas do checador (`check_notes.py:41,51`). `brza-app`, `brza-dev`, `brza-test`,
  `brza-tree` e `brza-shot` são só do `brza-studio`.
- Num workspace com outro nome, o `measure.py:589-598` devolve `(None, None)`: a linha sai sem `workstream`, o evento
  `memory` não sai e o `compact_guard` nunca barra. Caminho ou nome fixo também em `brza_runtime.py:19-24`,
  `brza-note:154,160,326`, `claude-brza:40-42`, `brza-install:34,39`, `brza-doctor:37` e no `~/.zshrc:51-82`.
- O `brza note sync` (`brza-note:337-355`) só leva a `origin/master` aos workstreams do mesmo repositório; puxar o
  núcleo de fonte externa é comando novo. O `brza-sessions:144-154` já acha a raiz pelo git common dir do cwd.
- O `resume_guard.py` está versionado, mas fora do `settings.json`.

Respondida em 2026-10-31.

1. **A fonte do núcleo.** Opções:
   - repositório próprio, sem identidade pessoal, que o próprio `brza-workspace` consome pelo sync (recomendada) —
     custo: ~2 h para criar e mover, mais a migração do `brza-workspace` na separação; se paga: na primeira mudança de
     norma depois do segundo workspace;
   - pasta `core/` no `brza-workspace`, com os moldes ao lado da cópia preenchida — custo: ~1 h, e cada mudança de norma
     feita duas vezes; se paga: só sem segundo workspace por meses;
   - plugin do Claude Code, com a norma em Markdown copiada à parte — custo: ~3 h além do sync, e a norma volta a
     divergir; se paga: nunca para a norma.

   **Resposta:** "repo brza-workflow". Leitura da sessão: a primeira opção, com o repositório chamado `brza-workflow`;
   o nome não existe no GitHub do `brz-anderson` (`gh repo view` → não resolve). Vai à R3.1 para confirmar onde mora.

2. **A fronteira genérico/local.** Opções:
   - placeholders e manifesto: o núcleo traz `{{nome}}`, `{{autor}}`, `{{repo-codigo}}`, um `.brza/workspace.toml`
     guarda os valores, o init e o sync renderizam; as seções inteiramente locais viram arquivos locais; no
     `settings.json` o sync é dono de `hooks` e o init escreve `env` e `enabledPlugins` (recomendada) — custo: ~5–6 h,
     quase tudo dentro da separação; se paga: no primeiro sync sem conflito;
   - fragmentos compostos, com `@import` no `CLAUDE.md` e o `AGENTS.md` gerado por concatenação — custo: ~7–8 h e um
     passo de geração por sync; se paga: só com a parte local acima de ~30% do texto;
   - `git merge` puro, com a parte local no mesmo arquivo — custo: ~2 h, e conflito em todo sync que toque linha mista;
     se paga: nunca, porque fere o R1.4.

   **Decidido — "Placeholders + manifesto (Recomendado)".**

3. **O que entra no núcleo.** Opções:
   - a norma, as skills, os agents, o `brza-note`, o `brza_runtime`, o `brza-agents` e os hooks `measure`,
     `compact_guard` e `fact_audit`, lendo a raiz e o repositório de código do manifesto; a camada do cliente
     (`brza-sessions`, `claude-brza`, `install`, `doctor`, `run`) como pacote opcional; `app`, `dev`, `test`, `tree` e
     `shot` locais do `brza-studio`; o `resume_guard` sai (recomendada) — custo: ~2–3 h, a parametrização que a R1.2 já
     previa; se paga: no primeiro workspace novo;
   - só a norma, as skills e os agents — custo: ~1 h, e o workspace novo nasce sem medição, `compact_guard` nem `brza
     note`; se paga: só sem workstreams;
   - tudo, sem parametrizar — custo: 0 h, e quebra em silêncio; se paga: nunca.

   **Decidido — "Hooks e brza note parametrizados (Recomendado)".**

4. **A raiz com mais de um workspace na máquina.** Opções:
   - pelo git common dir do cwd, reconhecendo o workspace pelo `.brza/workspace.toml`, com a `BRZA_WORKSPACE` só como
     override; o `claude-brza` e o `~/.zshrc` deixam de reconhecer os dois por nome (recomendada) — custo: ~2 h, com a
     mudança no `~/.zshrc` ao worklog; se paga: no segundo workspace;
   - uma `BRZA_WORKSPACE` por projeto, por direnv — custo: ~0,5 h por workspace, e o override do app e os links de
     `~/.local/bin` são um só; se paga: nunca, com dois workspaces;
   - uma cópia de `scripts/brza` por workspace — custo: ~3 h, e a cópia diverge; se paga: só sem checkout central.

   **Decidido — "Pelo cwd + workspace.toml (Recomendado)".**

### Rodada 3 — o `brza-workflow`, o CLI, a branch e a identidade (enviada 2026-10-31)

**Apresentado antes:** a leitura da R2.1 — a primeira opção, com o repositório chamado `brza-workflow`, que não existe
no GitHub do `brz-anderson`; o `brza-workspace` e o `brza-studio` são públicos, com a branch padrão `master` (`gh repo
view`). Ficaram fora da rodada, por terem lastro: as datas de `check_notes.py:41,51`, que só isentam nota anterior a
elas e por isso valem inteiras num workspace novo; e o esqueleto de pastas, que o Pedido já nomeia, com o `Último PLN
usado: 000`.

Respondida em 2026-10-31.

1. **Onde mora o `brza-workflow`.** Opções:
   - `brz-anderson/brza-workflow`, público como os outros dois, criado pelo `gh` no passo que move o núcleo
     (recomendada) — custo: ~10 min, e o núcleo sem nada pessoal, que a R2.2 já exige; se paga: já, porque o sync puxa
     sem credencial;
   - o mesmo, privado — custo: ~10 min, e todo sync e init precisam da chave `personal` ou do `gh`; se paga: só com algo
     que não pode ser público no núcleo;
   - só local, em `~/Projects/brza-workflow`, sem remote — custo: 0 agora, e o sync só nesta máquina; se paga: só com o
     primeiro workspace novo nesta máquina, e logo.

   **Decidido — "brz-anderson, público (Recomendado)".** Confirma a leitura da R2.1.

2. **De onde roda o CLI `brza`.** Opções:
   - do checkout do `brza-workflow`, um por máquina, com o `brza install` ligando o `~/.local/bin` a ele; os workspaces
     não recebem `scripts/brza`, e a norma, as skills, os agents e os hooks vão ao workspace pelo sync, porque o Claude
     Code os lê do repositório (recomendada) — custo: ~1 h no `brza install` e na troca dos 13 links de hoje; se paga: no
     segundo workspace;
   - copiado em cada workspace pelo sync — custo: ~0,5 h, e os links apontam para um workspace só; se paga: só com um
     workspace por máquina.

   **Decidido — "Do checkout do brza-workflow (Recomendado)".**

3. **A branch padrão e o remote.** Opções:
   - no manifesto, com `master` e `origin` quando ausentes, lidos do repositório pelo init (recomendada) — custo:
     ~0,5 h; se paga: no primeiro repositório criado pelo GitHub, que nasce com `main`;
   - fixos em `origin/master`, com o init criando sempre `master` — custo: 0 h, e repositório com `main` não serve; se
     paga: só se todo workspace nascer pelo init.

   **Decidido — "No manifesto, padrão master (Recomendado)".**

4. **A identidade git do `env`.** Opções:
   - `--author-name` e `--author-email`, com o padrão do `git config --global user.*`; a chave ssh e o `gh` ficam
     documentados no README do workspace (recomendada) — custo: ~0,5 h; se paga: no primeiro init;
   - pergunta interativa — custo: ~0,5 h, e o init deixa de rodar sem terminal; se paga: só com identidade diferente a
     cada workspace;
   - sem identidade no `env` — custo: 0 h, e perde o que o `env` garante contra o ambiente herdado; se paga: só numa
     máquina com uma identidade.

   **Decidido — "Flags, padrão do git config (Recomendado)".**

### Rodada 4 — o código acha o workspace, os scripts, o contador e o `AGENTS.md` (enviada 2026-10-31)

**Apresentado antes**, pelo rascunho do `designer` (`/private/tmp/pln006/desenho.md`, fora do git, D1–D12 e P1–P8,
~21,5 h), conferido por amostra na sessão:
- Os hooks não importam o CLI: só a stdlib e o `measure` vizinho (`compact_guard.py:28`).
- O `AGENTS.md` carrega junto do `CLAUDE.md` só pela opção de usuário `instructionFiles: claude-md-and-agents-md`
  (`~/.claude/settings.json:234-238`); a doc ignora a chave no settings de projeto, e o `CLAUDE.md:3-4` está impreciso.
- Nenhum Markdown da norma usa `{{`.
- Não conferido: que os hooks sobem no `/usr/bin/python3` 3.9.6, sem `tomllib`; o comando é `${BRZA_PYTHON:-python3}`.

Respondida em 2026-10-31.

1. **Como o repositório de código acha o workspace.** Opções:
   - `git config --local brza.workspace <raiz>` no repositório de código, gravado pelo `brza init --code` e pela
     migração (recomendada) — custo: ~0,5 h no P2 e ~9 ms por hook; se paga: já no P2;
   - registro em `~/.config/brza/workspaces.toml` — custo: ~1 h, e um arquivo de usuário que vai ao worklog a cada
     init; se paga: só com um repositório de código servindo a mais de um workspace;
   - procurar nos diretórios irmãos do checkout de código — custo: ~0,5 h e um stat por irmão a cada hook; se paga: só
     com workspace e código sempre no mesmo diretório pai.

   **Decidido — "Registro em ~/.config/brza".**

2. **Onde ficam os scripts fora do núcleo.** Opções:
   - `app`, `dev`, `test`, `tree` e `shot` em `scripts/brza/` do `brza-workspace`, ligados por `brza install
     --local`; `summarize_measurements` e `fact_outcome` ao workspace pelo sync, em `scripts/`; `brza-print` ao pacote
     do cliente (recomendada) — custo: ~1 h no P6; se paga: no P7, sem caminho novo para quem chama;
   - os cinco ao repositório `brza-studio` — custo: ~2–3 h e um pedido aos workstreams `studio` e `tools-kit`; se paga:
     só com outro workspace no `brza-studio`;
   - a medição como subcomando `brza measure` — custo: ~1,5 h, reescrevendo o `CLAUDE.md` e o `close-task`; se paga:
     nunca no desenho de hoje.

   **Decidido — "Camada local + sync (Recomendado)".**

3. **O contador "Último PLN usado".** Opções:
   - `plans/LAST_PLN`, local, numa linha (recomendada) — custo: ~0,5 h no P3; se paga: no primeiro PLN depois da
     migração;
   - `brza note next-plan`, pelo maior PLN entre as branches — custo: ~1 h; se paga: só se o contador escrito errar;
   - o render preserva a linha — custo: ~1 h e uma exceção por arquivo; se paga: nunca.

   **Resposta:** "jsonl na master do *-workspace com titulo, descrição, status, worktree/workstream e horário em que
   foi criado/alterado, assim o coordenador tem um indice pra se basear". Leitura da sessão: contraproposta — um
   índice dos planos em JSONL na `master` do workspace, que substitui o contador e serve de base a um coordenador. Abre
   exceção à regra de que a `master` guarda só a norma (`AGENTS.md`, "Cada workstream mora numa branch"). Vai à R5.

4. **Como o `AGENTS.md` carrega no Claude Code.** Opções:
   - `@AGENTS.md` na primeira linha do `CLAUDE.md` do núcleo, com o texto local em `.claude/rules/workspace.md` e o do
     pacote do cliente em `.claude/rules/brza-client.md` (recomendada) — custo: ~0,5 h no P3, e corrige o
     `CLAUDE.md:3-4`; se paga: no primeiro init em outra máquina;
   - `pluginConfigs` no settings de projeto — custo: ~0,2 h, e só vale com `--settings`; se paga: só com toda sessão pelo
     lançador;
   - a opção de usuário, documentada — custo: 0 h e um passo manual por máquina; se paga: nunca em máquina nova.

   **Decidido — "@AGENTS.md no CLAUDE.md (Recomendado)".**

### Rodada 5 — o índice da master (enviada 2026-10-31)

**Apresentado antes:** a leitura da R4.3 como contraproposta; o índice na `master` abre exceção à regra de que ela
guarda só a norma; dois acréscimos ao fim do mesmo arquivo conflitam no `git pull --rebase`, e o driver `merge=union`
do git, ligado no `.gitattributes`, junta as linhas.

Respondida em 2026-10-31.

1. **O que o índice registra**, seleção múltipla. Opções:
   - planos: id, título, descrição, status, phase, workstream e worktree, horário; substitui o contador (recomendada) —
     custo: ~2 h no P3, com a gravação; se paga: no primeiro PLN depois da migração;
   - issues — custo: ~1 h a mais e um push na `master` a cada issue que muda de estado; se paga: quando o coordenador
     distribuir issue;
   - decisões — custo: ~1 h a mais; se paga: quando o coordenador precisar ver decisão aberta entre workstreams.

   **Decidido — as três.**

2. **Como cresce.** Opções:
   - só acrescenta, uma linha por evento (criado, alterado), com o estado vigente na última linha de cada id e
     `merge=union` no `.gitattributes` (recomendada) — custo: ~0,5 h; se paga: no primeiro push simultâneo;
   - uma linha por item, reescrita — custo: ~0,5 h, e conflito entre itens vizinhos; se paga: só com uma sessão por vez.

   **Decidido — "Só acrescenta, merge=union (Recomendado)".**

3. **Quem grava e numera.** Opções:
   - o `brza note`: um `plan-open` reserva o número, maior id do índice + 1, com a linha "criado"; o `commit` acrescenta
     "alterado" na `master` quando o frontmatter muda; a linha "Último PLN usado" sai (recomendada) — custo: ~2–3 h no
     P3 e P5; se paga: no primeiro plano;
   - à mão, pela `plan-runner` — custo: ~0,5 h, e a linha esquecida erra sem aviso; se paga: só com consulta ocasional.

   **Decidido — "brza note, automático (Recomendado)".**

4. **O coordenador no PLN-006.** Opções:
   - não, vai a uma issue (recomendada) — custo: ~10 min; se paga: já;
   - sim — custo: uma rodada a mais e horas a estimar depois; se paga: se o coordenador precisar sair junto.

   **Decidido — "Não: vai a uma issue (Recomendado)".** A issue é
   [O coordenador se baseia no índice de notas da master](../../work/issues/o-coordenador-le-o-indice-da-master.md).

### Rodada 6 — o placeholder, a edição local, a versão e a migração (enviada 2026-10-31)

**Apresentado antes:** os quatro pontos restantes do rascunho do `designer`; nenhum Markdown da norma usa `{{`; não
conferido que os hooks rodam no Python 3.9 do sistema, sem `tomllib`.

Respondida em 2026-10-31.

1. **O placeholder e o motor.** Opções:
   - `{{tabela.chave}}`, com as chaves do manifesto em inglês, por regex pura, sem condicional, só em `.md` e no molde
     do settings; chave que falta é erro; o TOML por um parser próprio de um subconjunto, conferido contra o `tomllib`
     nos testes (recomendada) — custo: ~1,5 h no P3; se paga: já;
   - chaves planas em português, `{{nome}}`, `{{autor}}`, `{{repo-codigo}}` — custo: os mesmos ~1,5 h, sem as tabelas
     da R3.3 e da R3.4; se paga: só com meia dúzia de chaves;
   - `string.Template` — custo: ~1 h e escapar cada `$` dos blocos de shell; se paga: nunca;
   - Jinja2 — custo: ~1 h e uma dependência fora da stdlib; se paga: só com seção condicional.

   **Decidido — "{{tabela.chave}}, regex (Recomendado)".**

2. **O arquivo da norma comum editado no workspace.** Opções:
   - o `.brza/core.lock` guarda o sha256; o sync não escreve o divergente, mostra o diff e sai com 1; `--force
     <caminho>` sobrescreve (recomendada) — custo: ~1 h no P5; se paga: no primeiro sync depois de uma edição por engano;
   - merge de 3 vias, pelo `git merge-file` — custo: ~2 h e marcador de conflito na norma; se paga: só se editar a cópia
     virar prática;
   - sobrescreve sempre — custo: ~0,3 h; se paga: nunca.

   **Decidido — "Recusa e mostra o diff (Recomendado)".**

3. **A versão do `brza-workflow`.** Opções:
   - segue a branch `core.ref` (padrão `master`), com o commit no lock e `brza-workflow@<sha7>` na mensagem; `--ref`
     fixa uma vez; o comando é `brza sync`, e o `brza note sync` fica como a segunda camada (recomendada) — custo:
     ~0,5 h; se paga: já;
   - tags semver — custo: ~1,5 h e uma tag por mudança; se paga: com workspace de outro dono que trave versão;
   - sha fixo no manifesto — custo: ~0,3 h e editar o manifesto a cada sync; se paga: nunca.

   **Decidido — "A branch, com o sha no lock (Recomendado)".**

4. **A ordem da migração do `brza-workspace`.** Opções:
   - em estágios: do P1 ao P6 só o `brza-workflow` muda; no P7, o manifesto, as rules e o índice entram antes, o `brza
     sync --dry-run` só pode mostrar uma lista fechada de diferenças, e depois vêm o relink e o sync real (recomendada)
     — custo: ~1 h a mais; se paga: no P7, com as sessões abertas de pé;
   - de uma vez — custo: ~0 h a mais, e quebra a sessão que chamar `brza note` no meio; se paga: só sem sessão aberta.

   **Decidido — "Em estágios (Recomendado)".**

### Rodada 7 — o registro e o índice, no detalhe (enviada 2026-10-31)

**Apresentado antes**, pela revisão do `designer` com a R4–R6: o hook passa no `/usr/bin/python3` 3.9.6, mas as
sessões vivas resolvem `python3` para o 3.14; o parser TOML próprio fica, por um caso mais estreito (máquina só com o
3.9 no PATH, onde o `|| true` calaria a quebra). O `merge=union` deixa as linhas fora de ordem (`man gitattributes`),
então o estado vigente de cada id passa a ser a linha de maior `ts`. O total foi de ~21,5 h para ~27 h, +5 h do índice.

Respondida em 2026-10-31.

1. **O registro.** Opções:
   - o par raiz + código, escrito pelo `brza init` e por `brza register <raiz> [--code <caminho>]`, que recusa código
     já ligado a outro workspace (recomendada) — custo: ~1 h no P2 e uma linha de worklog por máquina; se paga: na
     segunda máquina;
   - só a raiz, com o código do `[code].path` do manifesto — custo: ~0,8 h, e cada busca lê todos os manifestos; se
     paga: só com o código no mesmo caminho em toda máquina;
   - o par, escrito por `brza install --register` — custo: os mesmos ~1 h, e o install liga binários e workspaces; se
     paga: nunca melhor que a primeira.

   **Decidido — "Par raiz+código, brza register (Recomendado)".**

2. **O caminho do índice.** Opções:
   - `.brza/index.jsonl` (recomendada) — custo: 0 h; se paga: já;
   - `work/index.jsonl` — custo: ~0,2 h; se paga: só se quem coordena procurar no `work/`;
   - `INDEX.jsonl` na raiz — custo: 0 h; se paga: só com o índice na página do repositório.

   **Decidido — ".brza/index.jsonl (Recomendado)".**

3. **A descrição de cada linha.** Opções:
   - um campo `description` no frontmatter de plano, issue e decisão, obrigatório na nota nova, com o H1 nas antigas
     (recomendada) — custo: ~1 h no P4; se paga: no primeiro uso do índice pelo coordenador;
   - a primeira frase do corpo — custo: ~0,5 h, e sai `- **Retomar:**` ou `## O pedido`; se paga: só com parágrafo de
     resumo nas notas;
   - só na criação, por flag — custo: ~0,3 h, e a nota criada sem o `brza note` fica sem; se paga: só com tudo criado
     pelo `brza note`.

   **Decidido — "Campo description (Recomendado)".**

4. **Como a linha chega à `master`.** Opções:
   - commit sem checkout na `origin/master`, com 3 tentativas, e o aviso de `brza note index --rebuild` quando falha
     (recomendada) — custo: ~1,5 h no P4 e ~1–2 s por commit, não medido contra o GitHub; se paga: no primeiro commit com
     o checkout principal sujo;
   - no checkout principal — custo: ~0,8 h, e recusa com ele sujo; se paga: só com ele sempre limpo.

   **Decidido — "Commit sem checkout (Recomendado)".**

### Rodada 8 — o id, a Fixfy, a medição datada e a decisão (enviada 2026-10-31)

**Apresentado antes:** o quinto ponto da revisão do `designer` e três escolhas que o rascunho marcou "sem lastro" sem
levar à rodada (`PLN-006-design.md`, D3 e D11).

Respondida em 2026-10-31.

1. **O id de issue e decisão no índice.** Opções:
   - `issue:<slug>` ou `decision:<slug>`, com o slug da criação; o rename só muda o `path` (recomendada) — custo: 0 h;
     se paga: no primeiro `move_note.py` de uma issue;
   - o caminho atual — custo: 0 h, e o rename vira item novo; se paga: nunca.

   **Decidido — "kind:slug da criação (Recomendado)".**

2. **As 7 menções à Fixfy.** Opções:
   - saem do núcleo (recomendada) — custo: ~0,2 h no P3; se paga: já, com o núcleo público;
   - vão à parte local — custo: ~0,3 h; se paga: se a procedência servir a quem lê este workspace;
   - ficam no núcleo — custo: 0 h; se paga: só se a referência for desejada em todo workspace.

   **Decidido — "Saem do núcleo (Recomendado)".**

3. **A medição datada que justifica regras** (`AGENTS.md:92-93`, o cache de 1 h no `CLAUDE.md`). Opções:
   - no núcleo, como o porquê da regra (recomendada) — custo: 0 h; se paga: já;
   - na parte local, com a regra sem o número — custo: ~0,3 h; se paga: quando outro workspace medir o próprio;
   - num guia em `wiki/` — custo: ~0,5 h; se paga: se a medição crescer.

   **Decidido — "No núcleo, como porquê (Recomendado)".**

4. **A exceção à decisão de 2026-10-30.** Opções:
   - nota nova em `work/decisions/`, citando a R5, sem `superseded_by`, nascida como proposta (recomendada) — custo:
     ~0,3 h no P4; se paga: na primeira leitura da de 2026-10-30;
   - reabrir a de 2026-10-30 — custo: ~0,2 h, e a decisão fechada muda; se paga: só com exceção pequena;
   - só no plano e no `AGENTS.md` — custo: 0 h, e a decisão fica contradita; se paga: nunca.

   **Decidido — "Nota nova, sem superseded_by (Recomendado)".**

### Rodada 9 — o corte dos Passos (enviada 2026-10-31, na mensagem)

**Apresentado antes:** o índice dos D, a Cobertura, os Passos P1–P9 (27 h) e a Regressão, na mensagem, por ser a
rodada que aprova o texto do plano.

Respondida em 2026-10-31.

1. **O corte.** Opções:
   - aceitar P1–P9 como estão (recomendada) — custo: 27 h, 5 h delas do índice; se paga: no segundo workspace;
   - dividir, com o índice (P4) num plano próprio — custo: ~15 min e a `plan-runner` mexida duas vezes; se paga: se o
     `brza init` for mais urgente que o índice;
   - juntar P5 e P6 — custo: o mesmo total, num commit maior; se paga: só se init e sync dividirem quase todo o código.

   **Resposta:** "aceito e pode iniciar os passos em paralelo". **Decidido — aceitar P1–P9**, que é o aceite do plano
   em 2026-10-31, e a execução pedida, em paralelo onde a dependência deixa: o P1 antes de todos; P2, P3 e P4 juntos;
   P5, P6 e P7 depois deles; o P8 e o P9 no fim.

### Rodada 10 — as fronteiras que o P1 achou (enviada 2026-10-31)

**Apresentado antes:** a devolução do `implementer` do P1 — as três suítes verdes no `brza-workflow`, dois skips, e
quatro escolhas que o D1 e o D3 não fixaram.

Respondida em 2026-10-31.

1. **O `brza-note` sem o pacote do cliente.** Opções:
   - `session_name()` devolve `None` sem o `brza-sessions` (recomendada) — custo: ~30 min e 1 teste, no P6; se paga: no
     primeiro workspace sem o pacote;
   - a lógica vai ao `brza_runtime` — custo: ~1,5 h; se paga: só com o nome da sessão obrigatório no núcleo;
   - documentar e deixar — custo: 0; se paga: nunca.

   **Decidido — "Devolve None sem o pacote (Recomendado)".**

2. **Como o cliente acha o `brza_runtime`.** Opções:
   - pelo checkout do `brza-workflow`, como a R3.2 (recomendada) — custo: ~0 h; se paga: já;
   - uma cópia do runtime levada pelo sync — custo: ~1 h no P7, contra a R3.2; se paga: só com o cliente fora do
     checkout;
   - o runtime em `core/` — custo: ~2 h e muda o D1; se paga: se o hook precisar dele.

   **Decidido — "Pelo checkout, como a R3.2 (Recomendado)".**

3. **Quem cria o `core/.claude/settings.hooks.json`.** Opções:
   - o P3, com o render e o merge da chave `hooks` (recomendada) — custo: ~20 min; se paga: no P3;
   - o P5 — custo: o teste em skip até lá; se paga: no P5.

   **Decidido — "O P3 (Recomendado)".**

4. **O `.gitignore` da raiz do `brza-workflow`.** Opções:
   - agora, no P1 — custo: 1 min; se paga: já (recomendada);
   - no P9 — custo: 0 e o risco de commit sujo; se paga: nunca melhor.

   **Decidido — "Agora, no P1 (Recomendado)".**

### A regra do resto do plano (2026-10-31)

Depois da R10, Anderson: "o restante dos passos, escolha sempre o recomendado, até o fim desse plano, vamos medir o
resultado". Daqui ao fechamento, cada ponto sem lastro vira rodada gravada aqui, com as opções e o preço, e
**decidida pela regra** na recomendada, sem ir à pergunta. A nota de `work/decisions/` segue nascendo como proposta:
a regra escolhe opção de rodada, e não é a frase explícita que transforma texto em decisão.

### Rodada 11 — os pontos do P2 (decidida pela regra, 2026-10-31)

**Apresentado antes:** a devolução do `implementer` do P2, com cinco escolhas que o D6 e o D7 não fixavam.

1. **O runtime sem workspace achado.** Opções: cair no legado, `BRZA_WORKSPACE` sem manifesto ou
   `~/Projects/brza-workspace` (recomendada) — custo: o nome fixo fica no runtime até o P7/P8; se paga: no P7/P8 ·
   `WORKSPACE = None` e erro no uso — custo: ~1 h a mais, fora do escopo, e quebra o `brza-workspace` antes do P8; se
   paga: depois do P8. **Decidido pela regra — o legado.**
2. **A saída do `brza where` sem workspace.** Opções: nada impresso, saída 0 (recomendada) — custo: nenhum para o
   `-n "$(…)"` do shell; se paga: já · saída 1 — custo: a função com `err_return` falha; se paga: só para `if brza
   where`. **Decidido pela regra — nada, saída 0.**
3. **O papel sob a `BRZA_WORKSPACE`.** Opções: o override escolhe a raiz e o papel vem do cwd, `notes`, `code` ou
   nenhum (recomendada) — custo: o cwd fora dos dois sai sem papel; se paga: já, sem lançar hooks em repositório alheio
   · papel `notes` fixo — custo: hooks em qualquer diretório; se paga: nunca. **Decidido pela regra — do cwd.**
4. **O `brza register` com o mesmo workspace e outro código.** Opções: recusar, com o mesmo par como no-op
   (recomendada) — custo: trocar o código exige editar o arquivo à mão; se paga: já · substituir a entrada — custo: o
   comando reescreve o arquivo do usuário; se paga: só se trocar o código for frequente. **Decidido pela regra —
   recusar.**
5. **A `BRZA_STUDIO` contra o registro.** Opções: a variável vence, até o P7 (recomendada) — custo: duas fontes até lá;
   se paga: no P7 · tirar já — custo: quebra o `claude-brza` e os testes; se paga: só depois do P7. **Decidido pela
   regra — a variável vence até o P7.**

### Rodada 12 — os pontos do P4 (decidida pela regra, 2026-10-31)

**Apresentado antes:** a devolução do `implementer` do P4, com quatro escolhas que o D11 não fixava.

1. **A data de corte do `description` no checador.** Opções: `2026-11-01`, o dia seguinte ao P4 (recomendada) —
   custo: ~0 h, e a nota aberta hoje fica isenta; se paga: já · o dia da migração — custo: ~0,2 h, e nada é cobrado até
   lá; se paga: só se o P8 demorar semanas · só aviso — custo: 0 h; se paga: nunca, contra a R7.3. **Decidido pela
   regra — 2026-11-01.**
2. **A precisão do `ts`.** Opções: segundos, como o exemplo do D11 (recomendada) — custo: 0 h, e empate raro resolvido
   pela ordem do arquivo; se paga: já · milissegundos — custo: ~0,1 h; se paga: se o coordenador mostrar empate.
   **Decidido pela regra — segundos.**
3. **A raiz do índice antes do P2.** Opções: uma função só, `index_repo()` (recomendada) — custo: 0 h; se paga: já ·
   esperar o P2 — custo: o P4 bloqueado; se paga: nunca. **Decidido pela regra — a função**; depois do merge ela lê o
   `runtime.WORKSPACE` que o `discover()` do P2 acha.
4. **A branch que o `--rebuild` lê.** Opções: a da `origin`, com a local de reserva (recomendada) — custo: 0 h; se paga:
   já · a local — custo: 0 h, e indexa nota não publicada; se paga: nunca. **Decidido pela regra — a da `origin`.**

### Rodada 13 — os pontos do P7 (decidida pela regra, 2026-10-31)

**Apresentado antes:** a devolução do `implementer` do P7, com cinco escolhas que o D10 não fixava.

1. **Onde mora o bloco do shell.** Opções: `packages/client/shell/brza.zsh` (recomendada) — custo: ~0; se paga: já,
   o P8 cola de lá · junto da regra em `packages/client/core/` — custo: invade o P3; se paga: nunca · só no README —
   custo: sem teste do zsh; se paga: nunca. **Decidido pela regra — `packages/client/shell/brza.zsh`.**
2. **O `brza install` rodado de um worktree.** Opções: avisar em stderr (recomendada) — custo: ~0; se paga: já · recusar
   — custo: o desenvolvimento em worktree para; se paga: só no uso real · resolver para o checkout principal — custo:
   ~1 h; se paga: nunca. **Decidido pela regra — avisar.**
3. **O `adm-claude` e o `claude-adm`.** Opções: ficam no `~/.zshrc`, fora do bloco (recomendada) — custo: ~0; se paga:
   já · no bloco — custo: o pessoal no pacote público; se paga: nunca. **Decidido pela regra — fora do bloco.**
4. **O `doctor` sem `[author].email` nem `user.email`.** Opções: AVISO (recomendada) — custo: ~0; se paga: já · ERRO —
   custo: trava o `doctor` sem `git config`; se paga: nunca. **Decidido pela regra — AVISO.**
5. **O `app_age` do `doctor` com a `origin/master` do `brza-studio`.** Opções: deixar, porque mede o app instalado
   (recomendada) — custo: ~0; se paga: já · ler `[code].branch` e `remote` — custo: ~20 min e um helper no
   `brza_root`; se paga: no segundo workspace com app diferente. **Decidido pela regra — deixar.**

### Rodada 14 — os pontos do P3 (decidida pela regra, 2026-10-31)

**Apresentado antes:** a devolução do `implementer` do P3, com seis escolhas que o D2–D5 não fixavam.

1. **O `author.login` no manifesto.** Opções: obrigatório, com o P5 pedindo `--author-login` ou o derivando do noreply
   (recomendada) — custo: ~15 min no P5; se paga: no primeiro init · opcional — custo: o render falha sem aviso; se
   paga: nunca. **Decidido pela regra — obrigatório.**
2. **O molde do `settings.json`.** Opções: fiel à `master`, com o Haiku, os TTLs de cache e o
   `disableClaudeAiConnectors`, menos o `GIT_SSH_COMMAND` (recomendada) — custo: uma preferência pessoal vira padrão;
   se paga: já · sem o `disableClaudeAiConnectors` — custo: ~5 min; se paga: se o núcleo público não quiser esse
   padrão. **Decidido pela regra — fiel à `master`.**
3. **A linha do scratch e "o chat do BrzA Studio" no `CLAUDE.md`.** Opções: placeholders `{{workspace.title}}` e
   `{{code.name}}` (recomendada) — custo: 0; se paga: já · mover ao `brza-client.md` — custo: ~20 min e a tabela
   quebrada; se paga: com um segundo app. **Decidido pela regra — placeholders.**
4. **O exemplo do glossário.** Opções: `app` e `ferramental` no lugar de `studio` e `tools-kit` (recomendada) — custo:
   0; se paga: já · deixar — custo: o núcleo cita workstreams alheios; se paga: nunca. **Decidido pela regra —
   generalizar.**
5. **As linhas "Testes:" do `CLAUDE.md` e o gate local do `reviewer.md`.** Opções: apontar ao `brza-workflow` e tirar
   o gate local (recomendada) — custo: 0; se paga: no P8 · deixar — custo: a frase mente em todo cliente; se paga:
   nunca. **Decidido pela regra — apontar ao `brza-workflow`.**
6. **Onde o `check_notes.py` lê as datas do manifesto.** Opções: só no `main()` (recomendada) — custo: 0; se paga: já ·
   também no `check()` — custo: ~1 h; se paga: se alguém importar o `check()` esperando o manifesto. **Decidido pela
   regra — só no `main()`.**

## Desenho

O Desenho, D1–D12, está em [PLN-006 — Desenho](PLN-006-design.md), por passar de 400 linhas.

## Passos

> Do P1 ao P7 só o `brza-workflow` muda, e o `brza-workspace` segue como hoje; o P8 é o único que o toca, em estágios
> (R6.4). Cada passo só executa a pedido explícito de Anderson.

### P1 — O `brza-workflow` nasce com o núcleo, o CLI e os testes verdes

Executa D1, D3 · executor: `implementer`; o `gh repo create brz-anderson/brza-workflow --public` pela sessão

Estimado: 1,5 h · Executado: 0,3 h

- [x] **1. Criar o repositório** e o layout do D1
- [x] **2. Copiar** o núcleo, o CLI e os testes pela fronteira do D3, sem os scripts locais nem o `resume_guard`
- [x] **3. Rodar** as três suítes lá — `scripts/brza/tests`, `.claude/hooks/tests`, `notes-checker` — e ver passar
- [x] **4. Commit e push** no `brza-workflow`

**Evidência:** `brza-workflow@83fce24`, a partir de `brza-workspace@d85c783` · `python3 -m unittest discover -s
tests/hooks` → 159 OK, 1 skip (P3) · `-s tests/cli` → 165 OK, 1 skip (P7) · `tests/notes-checker/run.py` → saída 0;
hooks e checador passam também no `/usr/bin/python3` 3.9.6. Desvios X1–X6.

### P2 — A raiz sai do cwd e do registro, no CLI e nos hooks

Executa D6, D7 · executor: `implementer`

Estimado: 4,5 h · Executado: 0,4 h

- [x] **1. Testes que falham**: o `brza where` de um worktree fora do diretório, sem entrada no registro, e o `brza
  register` recusando um código já ligado
- [x] **2. Implementar** o `brza_root`, o registro, o `brza where` e o `brza register`; os hooks e o `brza_runtime`
  passam a usá-lo, sem `tomllib`
- [x] **3. Rodar e ver passar**, também no `/usr/bin/python3` 3.9
- [x] **4. Commit**

**Evidência:** `brza-workflow@273c47d`, no merge `ca22efe` · na `master` depois do merge: `tests/cli` → 216 OK, 1 skip
(P7) · `tests/hooks` → 193 OK, 1 skip (P3), e no `/usr/bin/python3` 3.9.6 → 193 OK, 4 skips (3 sem `tomllib`, 1 do
P3) · `tests/notes-checker/run.py` → saída 0. O parser confere contra o `tomllib` em 14 documentos válidos, 17
inválidos e 8 fora do subconjunto. Desvios X8–X10; pontos R11.

### P3 — O manifesto, o lock, o motor e a norma em molde

Executa D2, D4, D5 · executor: `implementer`

Estimado: 3,5 h · Executado: 0,4 h

- [x] **1. Teste de ouro que falha**: o render do núcleo com o manifesto do `brza-workspace` sai igual à `master`
  daqui, menos a lista fechada do D12
- [x] **2. Implementar** o parser TOML, o render `{{tabela.chave}}`, o lock; pôr os placeholders nos `.md`, tirar a
  Fixfy (R8.2), o `@AGENTS.md` e as `.claude/rules/`
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@acf8bef`, o merge do P3 sobre o P7 · na `master`: `tests/hooks` → 244 OK, e no
`/usr/bin/python3` 3.9.6 → 244 OK, 5 skips (sem `tomllib`) · `tests/cli` → 264 OK · `tests/notes-checker/run.py` →
saída 0. O teste de ouro reproduz os 16 `.md` da `master` do `brza-workspace@d85c783`, salvo a lista fechada de 37
trocas em `tests/hooks/golden_differences.py`, que o P8 reusa; um `X` plantado em `core/work/README.md` o fez reprovar.
Um teste confere que, com outro manifesto, não sobra nada do `brza-workspace` no núcleo. Desvios X18–X20; pontos R14.

### P4 — O índice da `master`

Executa D11 · executor: `implementer`; o texto da norma e a nota de decisão pela sessão

Estimado: 5 h · Executado: 0,6 h

- [x] **1. Testes que falham**: o `plan-open` em corrida, a linha `changed` do `commit` sem tocar o checkout principal,
  o `merge=union` e o estado vigente pelo maior `ts`
- [x] **2. Implementar** o `brza note plan-open`, a linha do `commit`, o `brza note index --rebuild`, o
  `.gitattributes` e o campo `description` no checador e no molde
- [x] **3. Rodar e ver passar**
- [x] **4. A norma**: o texto do `AGENTS.md` e da `plan-runner` do D11, e a nota de decisão da R8.4, como proposta
- [x] **5. Commit**

**Evidência:** `brza-workflow@8b2a355`, no merge `ca22efe` · no worktree: `tests/cli` → 196 OK, 1 skip; os dois
`plan-open` em processos reais, 6 de 6 sem flake · na `master` depois do merge, as suítes do P2 · a norma em
`core/AGENTS.md`, `core/plans/README.md`, `core/work/README.md` e na `plan-runner` (`SKILL.md`, `open-and-plan.md`,
`close.md`, `plan-template.md`) · a proposta
[O índice de notas mora na `master`, a única exceção à regra da norma](../../work/decisions/o-indice-de-notas-mora-na-master.md),
`open`. Desvios X11–X13; pontos R12.

### P5 — O `brza init`

Executa D8 · executor: `implementer`

Estimado: 3 h · Executado: — h

- [ ] **1. Teste de aceite que falha**: o init num diretório temporário, com o checador verde e sem caminho fixo
- [ ] **2. Implementar**
- [ ] **3. Rodar e ver passar**
- [ ] **4. Commit**

### P6 — O `brza sync`, camada 1

Executa D9 · executor: `implementer`

Estimado: 3 h · Executado: — h

- [ ] **1. Testes que falham**: a mudança do núcleo chega sem tocar a parte local; o arquivo editado é recusado com o
  diff, e o `--force` o escreve
- [ ] **2. Implementar**
- [ ] **3. Rodar e ver passar**
- [ ] **4. Commit**

### P7 — O `install`, o lançador, o `doctor` e os scripts locais

Executa D10 · executor: `implementer`

Estimado: 2 h · Executado: 0,3 h

- [x] **1. Testes que falham** do `--client`, do `--local` e do `--relink`, e do `doctor` com o registro
- [x] **2. Implementar**, com o `claude-brza`, o `brza-sessions` e o bloco do shell sem nome fixo
- [x] **3. Rodar e ver passar**
- [x] **4. Commit**

**Evidência:** `brza-workflow@d60b037` · `tests/cli` → 264 OK, sem skip (o do installer saiu, X4) · `tests/hooks` →
193 OK, 1 skip (P3) · `tests/notes-checker/run.py` → saída 0 · o `brza-install --all --client --relink` rodado com o
`HOME` trocado e o bloco do shell testado no zsh de verdade. O que o P8 precisa — o bloco do shell, a ordem dos
comandos, o cabeçalho dos scripts locais — está no próprio `brza-install` e no `packages/client/shell/brza.zsh`.
Desvios X14–X16; pontos R13. Só o vermelho do `doctor` foi visto antes do código; nos outros, os testes vieram antes,
mas a rodada vermelha não foi capturada.

### P8 — O `brza-workspace` vira cliente do `brza-workflow`

Executa D12, D10 · executor: a sessão do `workspace`

Estimado: 3 h · Executado: — h

- [ ] **1. Estágio 1**: o manifesto, as rules e o índice, povoado pelo `index --rebuild`, entram; os scripts de hoje os
  ignoram
- [ ] **2. Estágio 2**: o `brza sync --dry-run` mostra só a lista fechada do D12
- [ ] **3. Estágio 3**: o `brza register`, o relink do `~/.local/bin` e o bloco do `~/.zshrc`, ao worklog em "Fora do
  workspace"; o sync real
- [ ] **4. Conferir** a Regressão inteira

### P9 — A revisão adversária e o README do `brza-workflow`

Executa todos · executor: `reviewer`; o README pela sessão

Estimado: 1,5 h · Executado: — h

- [ ] **1. A revisão**, com o parecer em `work/reviews/pln-006-o-brza-init.md`
- [ ] **2. Cada achado com destino**

## Regressão

- **O `brza-workspace` segue funcionando a cada estágio do P8.** Como se confere: as três suítes de hoje, o `brza note
  commit` e o `brza note sync` num workstream, e uma linha `turn` com o `workstream` preenchido na medição.
- **O `compact_guard` segue barrando.** Como se confere: `.claude/hooks/tests/test_compact_guard.py` e um `/compact`
  manual com nota sem commit.
- **As sessões do `brza-studio` acham o workspace.** Como se confere: o `brza where` e o `measure.py` de um checkout do
  `brza-studio`, pelo registro.

## Desvios

- **X1 — `tests/` em subpastas** `cli/`, `hooks/` e `notes-checker/`, onde o D1 diz só `tests/`. Separa as três suítes e
  os caminhos relativos de cada uma; afeta P1.
- **X2 — O `brza-note` do núcleo chama o `brza-sessions` do pacote do cliente** para o nome da sessão. A R10.1 decidiu
  que ele devolve `None` sem o pacote; afeta P6.
- **X3 — O pacote do cliente acha o `brza_runtime` pelo `sys.path` do checkout.** A R10.2 confirmou que é o desenho da
  R3.2; o P7 só garante o link.
- **X4 — Dois testes em skip**: o `SettingsTest` do `fact_audit`, até o P3 criar o `core/.claude/settings.hooks.json`
  (R10.3), e o do installer, até o P7.
- **X5 — Um `.gitignore` na raiz do `brza-workflow`**, que o D1 não lista (R10.4).
- **X6 — O CLI segue exigindo Python 3.10 ou mais** (`str | None`), como na origem; só os hooks e o `brza_root`
  rodam no 3.9. Vai ao README no P9.
- **X7 — As levas mudam: P2 e P4; depois P3 e P7; depois P5 e P6.** A R9 previa P2, P3 e P4 juntos, mas o parser
  TOML mora no `brza_root.py` (D2) e serve ao registro do P2 e ao manifesto do P3; o P3 espera o P2. Escolha da sessão,
  pela regra da recomendada.
- **X8 — O P2 não tocou o `bin/brza-note`.** Ele já compara o common dir com `runtime.WORKSPACE` e `runtime.STUDIO`,
  que agora vêm do `brza_root`; os `origin/master` literais dele ficam para o P6 (D9). Afeta P6.
- **X9 — O `brza_root` difere do D6 em três detalhes:** `registry_path()` é função, e não constante, para ler o
  ambiente na hora; o `find` ganhou `branch=False`, porque só o `measure` paga a chamada ao git; o parser aceita
  inteiro e booleano, porque o `schema = 1` do manifesto pede inteiro.
- **X10 — O `brza_runtime.discover()` cai no legado** (`BRZA_WORKSPACE` sem manifesto, ou `~/Projects/brza-workspace`)
  quando não acha workspace, para os scripts de hoje não quebrarem antes do P8; o nome fixo sai no P7 ou no P8.
- **X11 — O `commit` compara com a linha vigente do índice, e não com o commit anterior** como o D11 dizia: o
  `plan-open` já grava `created`, e o índice se conserta no commit seguinte quando um push falha.
- **X12 — O `brza note commit` aceita o caminho antigo de um rename**, com `git rm --cached` para o que sumiu do disco;
  antes o `git add` falhava, e o `changed` com o `path` novo da R8.1 não sairia.
- **X13 — O `plan-open` não cria o arquivo do plano**: reserva o número, grava a linha e imprime o caminho; quem grava é
  a `plan-runner`. O `--no-push` não grava linha, e o `--rebuild` recolhe depois.
- **X14 — O `--local <dir>` aceita a raiz do workspace ou a pasta dos scripts**, e o `--all` liga só o `bin/`; o
  pacote do cliente vai pelo `--client`. O `claude-brza` segue só pelo `--chat-command`.
- **X15 — O bloco do shell divide `<raiz> <papel>` pela última palavra** (`${w% *}`, `${w##* }`), e não pelo `${=w}`
  do D10, que quebrava raiz com espaço no nome.
- **X16 — O `claude-brza` e o `brza where` não têm legado**: sem manifesto e sem registro, a sessão sobe sem hooks. No
  P8, o manifesto e o `brza register` vêm antes de qualquer relink.
- **X17 — O P6 vem antes do P5**, e não junto: o passo 6 do D8 roda a camada 1 do sync no diretório novo. Escolha da
  sessão, pela regra da recomendada.
- **X18 — O bloco do shell tem duas cópias e uma chamada à Fixfy**: o `packages/client/shell/brza.zsh` do P7 cai na
  `fixfy_claude`, contra a R8.2, e o `templates/README.md` do P3 traz outra cópia do bloco. O P5, dono do molde do
  README, os reconcilia.
- **X19 — O `render` ganhou o parâmetro `escape`**, e o `render_settings` escapa o valor para JSON; o
  `templates/.brza/workspace.toml` é a saída exata do `dump_manifest`, para o P5 ter uma fonte só.
- **X20 — Ficaram no núcleo**, só com placeholders, o exemplo `fixfy:architect` do docstring do `measure.py:135` e o
  parágrafo do `CLAUDE.md` sobre o `--agents` do `claude-brza`, que é do cliente. O primeiro sai no P5, com o X18.

## Decisões

- [O índice de notas mora na `master`, a única exceção à regra da norma](../../work/decisions/o-indice-de-notas-mora-na-master.md)
  — R8.4, `open`, como proposta, à espera da confirmação de Anderson.

## Worklogs

- 2026-10-31 — aberto; R1–R8 respondidas, a R2.1 em texto livre e confirmada na R3.1, a R4.3 em texto livre e
  fechada na R5; D1–D12 gravados no `-design`, P1–P9 escritos (27 h). Parou na rodada do corte.
  [PLN-006: a abertura do brza init](../../work/worklogs/2026-10-31-pln-006-a-abertura-do-brza-init.md)
