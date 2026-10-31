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

- **Retomar:** R1–R3 fechadas, e a estrutura está decidida. Próximo: os itens `D` pelo `designer` — o
  `brza-workflow`, o manifesto, a fronteira arquivo a arquivo, o init, o sync de duas camadas e a raiz pelo cwd.

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

## Worklogs

- 2026-10-31 — aberto; R1–R3 respondidas, a R2.1 em texto livre e confirmada na R3.1. Parou antes do Desenho.
  [PLN-006: a abertura do brza init](../../work/worklogs/2026-10-31-pln-006-a-abertura-do-brza-init.md)
