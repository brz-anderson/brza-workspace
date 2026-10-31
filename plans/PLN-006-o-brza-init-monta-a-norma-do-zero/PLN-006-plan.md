---
status: open
phase: design
origin: request
ready: não — faltam o Desenho e os Passos
scope:
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - tooling
---

# PLN-006: O `brza init` monta a norma num workspace do zero

- **Retomar:** R1–R6 fechadas. O rascunho D1–D12 do `designer` está em `/private/tmp/pln006/desenho.md`, fora do git,
  e precisa refletir a R4.1 (registro em `~/.config/brza`) e a R5 (o índice da `master`). Próximo: o `designer` revisa,
  e o Desenho vai ao `PLN-006-design.md`, com os Passos e a rodada do corte.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31.

> "nós já temos mecanismos para inicializar a norma inteira, com AGENTS CLAUDE plans/ wiki/ work/ skills/ agents/ num
> repositório do zero?"

Respondido que não, Anderson pediu: "plano".

### Cobertura

> Rascunho da abertura: os critérios são propostas e se fecham no Planejar, com o passo e o teste.

| Origem     | Critério de aceite                                                                                                                                                                                  | Passo | Teste (nível)                    |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---- | :------------------------------- |
| `Pedido 1` | `brza init <dir>` cria, num diretório vazio, um workspace com `AGENTS.md`, `CLAUDE.md`, `README.md`, `plans/`, `wiki/`, `work/`, `.claude/skills/`, `.claude/agents/`, hooks e `settings.json`, e o `notes-checker` roda verde nele | —     | unidade, num diretório temporário |
| `R1.2`     | O workspace inicializado aponta para o repositório de código dele, sem caminho fixo a `brza-workspace` ou `brza-studio` no que foi copiado                                                         | —     | unidade                          |
| `R1.4`     | Uma mudança no núcleo genérico daqui chega ao workspace inicializado por um comando de sync, sem tocar a parte local dele                                                                           | —     | unidade                          |
| `Pedido 1` | O `brza-workspace` segue funcionando depois da separação genérico/local: hooks, skills, `brza note` e os testes de hoje                                                                            | —     | os testes de hoje (unidade)      |

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

## Worklogs

- 2026-10-31 — aberto; R1–R6 respondidas, a R2.1 em texto livre e confirmada na R3.1, a R4.3 em texto livre e
  fechada na R5; rascunho D1–D12 e P1–P8 do `designer`. Parou antes de gravar o Desenho.
  [PLN-006: a abertura do brza init](../../work/worklogs/2026-10-31-pln-006-a-abertura-do-brza-init.md)
