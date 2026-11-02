---
name: padroes-de-erro-nas-entregas
description: Onde os defeitos das entregas de plano do workspace costumam se esconder (hooks, auditoria por LLM, evidência de passo [x], desvios, cópia congelada, sync, override da BRZA_WORKSPACE, arquivo local velho), as hipóteses que costumam cair e a higiene do experimento em clone
metadata:
  type: project
---

Padrões vistos nas revisões do PLN-005 (2026-10-31) e do PLN-006 (P1–P7 e P8, 2026-11-02), no workstream `workspace`.

**Os que se repetem e onde se escondem:**
- **O corte que alimenta outro consumidor.** Uma constante de limite (`TEXT_LIMIT`, `[:300]`) pensada para o log vai
  também ao que decide (o arquivo do auditor). Conferir no dado real quantos itens batem no limite exato; o teste
  costuma fixar o corte como comportamento. Confiança dada: 95, verificado no transcript real.
- **Veredito de LLM sem prova.** Auditor `claude -p` diz `holds` com linha e arquivo no `why` sem ter aberto o arquivo.
  Conferir cruzando o transcript da sessão do auditor (`~/.claude/projects/<cwd>/<session>.jsonl`, `tool_use`) com o
  que cada fato cita. Confiança dada: 90.
- **Evidência de `[x]` que afirma uma medida** ("nenhuma linha passa de 120 colunas", "N linhas"): refazer com `len()`
  do Python, não com `awk length` (conta bytes no macOS e acusa falso positivo em linha com acento).
- **Desvio que mudou um `D` sem rodada**, com o `D` deixado no texto antigo: comparar o plano aceito
  (`git show <commit do aceite>:plans/...`) com o atual. A regra é a do `conduct.md` ("Desvio que muda um D vira
  rodada"). Confiança dada: 92.
- **Norma que não acompanhou a última mudança do código**: o passo que muda o código depois do passo da norma (aqui, o
  P10 depois do P7) deixa o `CLAUDE.md` com o valor antigo. `git diff <commit da norma> <último> --stat`.
- **Script que acha a raiz por `scripts/..` ou pela `BRZA_WORKSPACE`**: o `~/.zshrc` não exporta a variável, e no
  worktree a raiz vira o worktree, que pode ter um `.measurements/` velho; o log ausente vira "vazio" sem aviso. Testar
  com `env -u BRZA_WORKSPACE` no worktree e rodar da raiz da `master` (onde o workstream é `master`, não vazio).
  Depois do PLN-006 o `brza_root` sobe pelo common dir, e esse caso caiu (ver os falsos).
- **O override da `BRZA_WORKSPACE` vence o cwd no que escreve** (PLN-006/P8): o `brza_root.find` devolve a raiz do
  override com `role=None` quando o cwd é de outro workspace; o `brza-where` recusa, mas o `brza sync` e o `brza note`
  seguem e commitam no workspace da variável. Toda sessão lançada pelo `brza.zsh`/`claude-brza` tem a variável.
  Procurar todo `find(...)` cujo chamador não confere o `role`. Confiança dada: 97, reproduzido em dois clones.
- **Arquivo local que o sync não toca fica com a cópia velha** (o `README.md` com o bloco antigo do shell, que a
  `rules/brza-client.md` do núcleo manda ler): o molde do `brza-workflow` muda, o arquivo local do workspace migrado
  não. Cruzar cada ponteiro do núcleo ("está no `README.md`, em …") com o arquivo local. Confiança dada: 96.
- **A norma que passou a ser do núcleo ainda manda editar no lugar antigo** (o `AGENTS.md` e a
  `agent-instructions-writer` mandam editar na `master`, e o sync recusa o editado para sempre). Depois de mover dono
  de arquivo, `git grep` pelo verbo "edite"/"grava" nos arquivos do lock. Confiança dada: 93.
- **O `--dry-run` que diz "nada" e o real que commita** (o lock que só troca o sha): rodar o real num clone logo
  depois do dry-run e comparar. Confiança dada: 97.
- **Desvio que promete "sai no P_x"** (o legado do X10): conferir no código do último passo se saiu, e se outro desvio
  registra que ficou.
- **Teste de timeout que não distingue `killpg` de `kill`**: mutação numa cópia em `/private/tmp` mostra.
- **Cópia que congelou num sha enquanto a origem andou** (PLN-006: o `brza-workflow` nasceu de `d85c783`, e a `master`
  ganhou o P11 do PLN-005 depois). O sync "sem entrada no lock → sobrescreve" desfaz a mudança alheia com saída 0.
  Conferir com `git log <sha da cópia>..origin/master` e com o `shasum` de cada arquivo nos três lados. Depois, ensaiar
  o `--dry-run` num clone em `/private/tmp`, com o `BRZA_WORKFLOW` apontando para um clone, porque o `fetch` do sync
  escreve no `.git` do repositório real. Confiança dada: 97.
- **Valor padrão que difere do valor real do workspace**: o dict de teste "que o P8 grava" omite uma chave, e o
  `with_defaults` preenche outra data. Rodar o checador do núcleo nas notas reais dos worktrees
  (`git worktree add <tmp> origin/workstream/<x>`) com os dois valores. Confiança dada: 90, com premissa.
- **Promessa de reparo que só cobre metade**: o aviso manda rodar um `--rebuild` que só acrescenta o que falta e não
  corrige o que ficou velho. O teste fixa o lado que falha ("sem push, sem linha") e não o reparo. Reproduzir a
  sequência inteira (mudar, perder, reparar). Confiança dada: 95.
- **Flag nova que contradiz um "deixar até…" de outra rodada**: a R15.4 deixou o `origin`/`master` fixos "até haver um
  workspace assim", e o P5 ganhou `--branch`, que cria um. Cruzar as condições "se paga: se o P_x criar…" com as flags
  dos passos seguintes.
- **Esqueleto do CLI que o checador do mesmo núcleo reprova**: a regra nova do checador (o `description`) não chegou
  ao molde do `brza note new`. O aceite roda o checador num workspace vazio, e por isso passa. Testar criando a nota
  pelo comando.

**Hipóteses que costumam cair** (deixar como `→ falso` no parecer):
- a trava compartilhada do `measure.State` segurando o hook — conferir pelos timestamps `subagent` → `fact_capture`;
- a sessão no worktree do `brza-studio` sem o modelo ou a permissão — o `env` do `settings.json` chega aos filhos, e o
  `defaultMode: auto` é de usuário;
- vazamento para o log — `.measurements/` está no `.gitignore`.
- caminho `../` no lock apagando fora da raiz — o `git status -- <caminhos>` do guard recusa o caminho fora do
  repositório antes de escrever;
- `--relink` apagando arquivo que não é link — a recusa vem antes de qualquer `unlink`;
- "o repositório público ganhou e-mail ou caminho pessoal" — conferir com `git grep` na `origin/master` do
  `brza-workspace`, que é público e já os tinha;
- o `claude-brza` quebrando no 3.9 — o `import` falho cai num `except` e só perde o `--agents`, como antes (X6).
- o worktree do workspace achando o próprio worktree como raiz — o `brza_root` e o `measure.script_root` sobem pelo
  common dir desde o PLN-006;
- os `hook_error` `KeyError(None)` na medição — são sonda do `compact_guard.py` sem modo, não a trava em uso;
- script ou teste "perdido" na migração — conferir pelos links do `~/.local/bin` e pelo `ls tests/*` do
  `brza-workflow` antes de acusar.

**Ambiente de experimento:** o `rm -rf` com glob relativo é barrado pela trava do runtime. Crie um diretório novo por
experimento (`/private/tmp/<plano>/expN`), com `HOME`, `GIT_CONFIG_GLOBAL`, `BRZA_REGISTRY` e `XDG_CONFIG_HOME`
temporários, num `env.sh` que cada comando carrega. **O `env.sh` começa com `unset BRZA_WORKSPACE BRZA_STUDIO
BRZA_WORKFLOW`, e nenhum comando que escreve roda sem ele**: a sessão do revisor herda a `BRZA_WORKSPACE` do lançador,
e em 2026-11-02 um `brza-sync --no-push` rodado no clone commitou na `master` real; o `git reset` para desfazer é
barrado pela trava do runtime e volta à sessão principal. Antes de cada ensaio que escreve, `--dry-run` primeiro e
`git -C <real> log -1` depois.

**Cuidado de leitura:** dois `sed -n` concatenados num só comando colam trechos de testes diferentes e fazem parecer
código morto; ler o teste pelos limites do `def`.

Relacionado: [[o-log-de-medicao-como-dado]].
