# Adaptador do Claude Code

A norma do workspace está no `AGENTS.md`. O Claude Code lê esse arquivo junto com este quando a opção
`claude-md-and-agents-md` está ativa. Este arquivo traz só o adaptador: traduz o vocabulário da norma e acrescenta a
mecânica própria do Claude.

## O vocabulário do `AGENTS.md` no Claude Code

| Termo do `AGENTS.md`       | No Claude Code                                                                                   |
| :------------------------- | :----------------------------------------------------------------------------------------------- |
| pergunta com opções        | `AskUserQuestion`                                                                                |
| correio                    | `SendMessage`, para o nome da sessão; `ListAgents` lista as abertas                              |
| acionar uma skill          | `Skill`, ou `/nome` digitado                                                                     |
| subagente                  | `Agent`, com o `model` pela camada                                                               |
| retomar o subagente        | `SendMessage` com o nome ou o ID do agente, que volta com o contexto dele; não abre `Agent` novo |
| estágio de workflow        | cada `agent()` de um workflow                                                                    |
| camada alta, média, rápida | Opus, Sonnet, Haiku — o `haiku` é o Haiku 5.5, pelo `env` do `settings.json`                     |
| scratch                    | o scratchpad da sessão, anunciado no arranque, em `/private/tmp/claude-501/…`                    |
| sessão nova                | `/exit` e `claude --name <nome>` no mesmo terminal, sem `--resume`, `--continue` nem `--rc`       |

O comando que a sessão passa a Anderson para abrir uma sessão nova com prompt é `claude --name <nome> "<prompt>"`.
**Não use `--rc`**: com ele, o prompt entre aspas não funciona. Não use `/clear` no lugar da sessão nova, porque ele
troca o `session_id` mas mantém a conversa anterior ligada à sessão.

## A configuração chega pela função do shell

O `.claude/settings.json` daqui **não é herdado** pelo `brza-studio`, que fica ao lado e não dentro deste repositório. Por
isso a função `claude` do `~/.zshrc` passa `--settings ~/Projects/brza-workspace/.claude/settings.json` e
`BRZA_WORKSPACE` sempre que o cwd está no `brza-workspace` ou no `brza-studio`, inclusive nos worktrees. Fora deles, ela
segue para a função da Fixfy. O bloco está no `README.md`, em "Funções do shell".

A sessão aberta sem a função — numa IDE ou no chat do app, se ele não passar o `--settings` — sobe sem os hooks, sem a
trava e sem a identidade abaixo.

## A identidade é a do brz-anderson, pelo `env`

O `env` do `.claude/settings.json` define:
- `GIT_AUTHOR_*` e `GIT_COMMITTER_*`: `Anderson Pereira Brzezinski <240569289+brz-anderson@users.noreply.github.com>`;
- `GIT_SSH_COMMAND`: o `~/.ssh/config` padrão, onde mora o alias `personal`.

Isso vale para os commits deste repositório e do `brza-studio`, e vence o ambiente da `fixfy-claude` que uma sessão
herde. O `git var GIT_AUTHOR_IDENT` confere: deve sair o noreply do `brz-anderson`.

O `gh` usa o perfil padrão, com a conta `brz-anderson` ativa (`gh auth switch`).

## Os plugins são habilitados só aqui

O `.claude/settings.json` habilita só o `context7`. Não há `.mcp.json`. Nenhum plugin daqui vai para a configuração de
usuário.

## O hook de medição

O `.claude/hooks/measure.py`, ligado no `settings.json`, grava uma linha JSON por evento em
`.measurements/measurements.jsonl`:

| Evento     | Quando                                            | O que grava                                                                                                                                         |
| :--------- | :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subagent` | `SubagentStop`, inclusive o `agent()` de workflow | duração, chamadas à API e de ferramenta, tokens por tipo, o maior contexto de uma chamada, custo estimado em US$, conta, modelo, modelo pedido, esforço, versão do plugin, workflow e fase |
| `turn`     | `Stop`, o fim de cada turno da sessão principal   | o mesmo, e as skills e os agentes que rodaram no turno                                                                                             |
| `skill`    | a ferramenta `Skill`                              | o nome, os argumentos e a versão do plugin                                                                                                         |
| `command`  | `/nome` digitado, que não passa pela `Skill`      | o nome, os argumentos e a origem                                                                                                                   |
| `failure`  | `StopFailure`                                     | o erro de API que encerrou o turno, como o limite de uso                                                                                           |
| `mcp`      | toda chamada `mcp__*`                             | o servidor, a ferramenta, a duração e a falha                                                                                                      |
| `guard`    | `UserPromptSubmit`, pela trava de retomada        | a decisão (`blocked`, `released`, `skipped`), os minutos parada, o TTL, o contexto e o custo estimado da regravação                                 |

- **Só o trecho novo do transcript:** retomada e turno medem só o que veio depois da última leitura.
- **Onde grava:** sempre no `.measurements/` daqui, também nas sessões do `brza-studio`. O comando acha o script pela
  `BRZA_WORKSPACE` antes da `CLAUDE_PROJECT_DIR`, que no `brza-studio` apontaria para lá.
- **Sem bloquear:** o `|| true` impede que um script ausente barre a sessão.
- **Python:** o da `BRZA_PYTHON`, ou `python3` sem ela.
- **Precisão:** a saída de tokens fica subcontada, porque o transcript guarda a contagem do início de cada mensagem.
  Entrada e cache valem, e são eles que pesam no custo.
- **Resumo:** `python3 scripts/summarize_measurements.py`.
- **Testes:** em `.claude/hooks/tests/`.

## A trava de retomada de cache

O `.claude/hooks/resume_guard.py`, ligado no `UserPromptSubmit`, barra o prompt que acorda uma sessão parada além do TTL
do cache e com 150 mil tokens ou mais de contexto no último turno. Esse pedido regravaria o contexto inteiro.
- **A mensagem** diz o tempo parado, o TTL, o contexto e o custo estimado da regravação, e manda abrir sessão nova e
  retomar pelo `Retomar` do plano ou pela issue.
- **Reenviar o mesmo prompt em até 2 min passa**, e o correio entre sessões nunca é barrado.

O mesmo `settings.json` põe o cache da sessão principal em 1 h (`promptCacheTtl`) e o do resto — subagentes, workflows,
pedidos auxiliares — em 5 min (`subagentPromptCacheTtl`).
