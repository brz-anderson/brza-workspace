---
status: in_progress
phase: execution
origin: request
description: O brza sessions e a meeting-runner funcionam na cloud pela porta AgentRuntime, com reunião real e ata.
ready: "P1–P8 têm evidência e nenhuma caixa fecha antes do merge. P7 e P8 estão implementados, aguardando merge, no d45b7d8. P9 e P10 ficam de fora"
estimate_h: 28
executed_h: 1.7
remaining_h: 26.3
priority: high
scope:
  - brza-workflow
  - workspace
opened: 2026-11-14
owner: Anderson
deadline: 2026-11-14
tags:
  - tooling
---

# PLN-026: brza sessions e meeting-runner funcionam na cloud

- **Retomar:** Nenhum passo está concluído antes do merge. P7 e P8 estão implementados e aguardam o merge. A passagem do `92575d1` está na ata [A reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-coordenacao.md). A prova do `e07fd479fef2b5cc7e3656ca0e2cb6a05ec9274b` está na ata [A segunda reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-2-coordenacao.md). O runtime único é `packages/client/bin/cloud_runtime.py` em `d45b7d82e1db33b07004e3bf36addec5871c7c15`, [PR 2](https://github.com/brz-anderson/brza-workflow/pull/2), rebaseado em `2a0580d6cb07d2a4d50ff086016b96ec775dbf8b` (`builder/pln-026-pr-a`). O primeiro `agent -p` não leva `--resume`; o id é o `session_id` do JSON. O transporte lê `BRZA_WORKFLOW_DIR` e não fixa branch. P9 e P10 ficam de fora. `executed_h` 1,7 pelo relógio entre `52184ee` (16:11:00Z) e `e07fd47` (17:54:25Z).

## Pedido

- **Origem:** pedido da sala BrzA Cloud Builders em 2026-11-14, com aprovação do Anderson, nesta sessão cloud. Inverte a R1.4 do [PLN-024: Norma aceita o prefixo builder/ (workstream pessoal de Builder)](../PLN-024-prefixo-builder/PLN-024-plan.md). O desenho vigente é a ADR-003, autor Linus, status Proposta, que incorpora a ADR-002 e não tem arquivo neste repositório. A medição de execução encosta no [PLN-025: Cada execução de Builder deixa métrica, nota e persona calibrável](../PLN-025-esboco-dos-builders/PLN-025-plan.md). A reunião de hoje usa a skill do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md), que vive em `origin/workstream/playground`.

"R1, aceite: (1) `brza sessions list --json` sai 0 sem o socket do Studio e traz a run atual com id `bc-`; (2) `brza sessions diag-cloud --agent cursor --dry-run` sai 0, imprime `abriria` e não chama worker-start; (3) `brza doctor --env` passa; (4) a execução aparece no `--by-execution` (PLN-025 P3) com custo e tokens marcados como ausentes, nunca zero, quando não há chave."

"o fluxo funcionando numa REUNIÃO usando o `meeting-runner` na cloud, com PR(s) para a master."

"Os passos do PLN-026 devem seguir essa ADR e os critérios de aceite que estão no fim dela." O caminho do `open` pedido na mensagem seguinte: `agent -p --output-format json --model <id> --workspace <dir> --trust` com `--resume <chatId>` por persona, sem `--force`.

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| R1.1 ponto 1 | `brza sessions list --json` sai 0 sem o socket e traz a run `bc-` com `source: cloud` | P1 | `tests/cli/test_brza_sessions.py` (unidade) |
| R1.1 ponto 2 | `diag-cloud --agent cursor --dry-run` sai 0, imprime `abriria` e não chama `worker-start` | P2 | o mesmo arquivo, espiando a chamada (unidade) |
| R1.1 ponto 3 | `brza doctor --env` sai 0 | P5 | o comando no pod, depois da R2.1 (manual) |
| R1.1 ponto 4 | `--by-execution` marca custo e tokens como `ausente`, nunca zero, sem chave | P6 | `tests/hooks/test_summarize_measurements.py` (unidade) |
| Entrega | Uma reunião real pelo `meeting-runner` na cloud, com ata no worklog | P8 | a ata gravada (manual) |
| ADR, aceite 2 | Capacidade ausente sai diferente de 0 e nomeia runtime e capacidade | P3 | teste de contrato (unidade) |
| ADR, aceite 3 | A suíte de contrato passa nos dois adaptadores | P4 | a suíte (unidade) |
| ADR, aceite 4 | No Mac, o `StudioRuntime` repete o comportamento atual, regressão do PLN-013 verde | P4 | `tests/cli/test_brza_sessions.py` (unidade) |
| ADR, aceite 5 | Nenhum `ORCA_*` nasce do `bc-`; nenhum registro `cloud` entra no JSON de abas | P1 | teste que o ambiente e o JSON de abas ficam intocados (unidade) |
| R1.5 | `open` só entra nas capacidades depois da prova do `agent -p` sem `--force` | P7 | a prova com a chave, saída 0 (manual), e o contrato atualizado (unidade) |

### Fora de escopo

- **Executar os passos nesta sessão.** O plano abre; cada passo espera pedido explícito de Anderson.
- **Pull request nesta sessão.** Os PRs previstos ficam na lista abaixo e nascem na sessão que executar o código.
- **Editar o `brza-studio`.** O `StudioRuntime` encapsula o cliente que já existe. Mudança no app só se a regressão do P4 não couber no `brza-workflow`.
- **Arquivo da ADR-003 neste repositório.** Artefato de arquiteto não entra em PR nem no repo. A citação pelo número e o resumo das regras ficam no Desenho. A ADR-002 também não ganha arquivo.
- **Degrau 2 como entrega de hoje.** O P10 está no plano e é o primeiro corte da janela.
- **Reserva manual do índice.** Ninguém edita `.brza/index.jsonl` à mão. A R2.3 trata do número.

## Janela

- **Janela e meta:** 2026-11-14, até 19:00 America/Sao_Paulo. No fim, uma reunião pelo `meeting-runner` na cloud tem ata, e os quatro pontos da R1.1 estão verdes ou o corte abaixo diz o que ficou.
- **Cortes previstos:** a ordem recomendada está na R2.4, ainda sem resposta. Enquanto a sala não escolher, o texto de trabalho corta primeiro o P10 e depois o P9, mantém o P4 no PR e faz a reunião com 2 personas e uma rodada.

## Restrições

- **A master deste repositório não recebe a nota.** O plano e a ata ficam em `builder/bob-the-builder`. O índice só mudaria pelo `brza note`, que nesta branch recusou.
- **Consumidor fala com a porta.** `brza sessions` e a `meeting-runner` não leem socket, `ORCA_*` nem a API do Cursor por conta própria.
- **Capacidade fora do conjunto falha com rc diferente de 0** e a mensagem nomeia o runtime e a capacidade.
- **Métrica que não existe sai `ausente`.** Zero ficaria parecendo medida.
- **O default de `user_data()` no macOS permanece** `~/Library/Application Support/brza-studio`.
- **Commit em `builder/*` usa `Bob The Builder <bob@brza.dev>`.** Decisão do Anderson em 2026-11-14 (R3.3). O `52184ee` permanece com Anderson Pereira. Não se reescreve.

## Pré-requisitos

- **`CURSOR_CONVERSATION_ID` definida, com prefixo `bc-`.** Conferido neste pod em 2026-11-14 (comprimento 39). Sem ela, o degrau 1 não tem run para listar e o P1 para.
- **`BRZA_CURSOR_API_KEY` presente no pod da prova do P7** (comprimento 102; o valor não foi gravado). O P1, o P2 e o P5 não precisam dela. Sem a chave ou sem o binário `agent`, o `open` não é declarado. A chave entra como segredo com esse nome (R3.2). O wrapper copia para `CURSOR_API_KEY` só no processo filho. Não vai em `--api-key`, no `env.sh` nem no repo.
- **O binário `agent` 2026.11.13-eacade1 está neste pod**, em `~/.local/bin/agent` (o `cursor-agent` é o mesmo arquivo). `agent --help` sai 0 e lista `-p`, `--output-format`, `--model`, `--workspace`, `--trust`, `--resume` e `--force`. `agent status` sai 0 com "Not logged in". `agent models` sai 1 pedindo autenticação. Um pod novo não herda o binário: a instalação é `curl https://cursor.com/install -fsS | bash`.
- **A skill `meeting-runner` está nesta branch desde o P8 (X6).** A origem é `origin/workstream/playground` no SHA `03c9579d56fb2304a48821e2c6978e0514cd7df3`. O D4 pedia um worktree só de leitura; a ordem do P8 trouxe a skill, e o `skillkit` de que ela importa (X7). O transporte studio continua o padrão. Não houve merge na master.

## Entrevista

### Rodada 1 — o que a sala já fechou (enviada 2026-11-14)

**Apresentado antes:** o diagnóstico bc-1ac1c85f mostrou o `brza sessions` preso ao socket do Studio. Nesta sessão, o inventário achou a skill só em `workstream/playground`, o `brza doctor` sem `--env` (rc 2) e o `plan-open` recusando `builder/*`. O `agent` instalou e as flags do `open` existem; a conta não está autenticada.

Respondida em 2026-11-14, na sala BrzA Cloud Builders, com aprovação do Anderson. A mensagem seguinte da mesma sessão fixou a ADR e o comando do `open`.

1. **Aceite do `brza sessions` na cloud e a reunião como entrega.** Opções apresentadas pela sala, já com a escolha feita:
   - os quatro pontos da R1.1 mais uma reunião real com ata (a escolhida) — custo: a porta e uma prova com personas; se paga: na reunião de hoje, se a chave existir;
   - só o degrau 1, sem reunião — custo: o prazo das 19h entrega lista e não ata; se paga: se a chave não entrar.

   **Decidido — os quatro pontos e a reunião com ata.**

2. **A porta.** A mensagem da sala falava em `SessionSource`, com `StudioSource` e `CloudSource`. No mesmo dia a ADR-003 troca o nome e junta a ADR-002. Opções:
   - a porta `AgentRuntime` da ADR-003, com `StudioRuntime` e `CloudRuntime` (a escolhida, pela mensagem que manda os passos seguirem a ADR) — custo: um contrato e dois arquivos novos no `brza-workflow`; se paga: quando o segundo consumidor (`meeting-runner`) usar o mesmo `open`;
   - manter o nome `SessionSource` da primeira mensagem — custo: divergir da ADR já escrita; se paga: nunca, com a ADR no mesmo dia;
   - condicionais dentro do `brza sessions` — custo: o `if cloud` se repete na `meeting-runner`; se paga: nunca, para dois consumidores.

   **Decidido — `AgentRuntime`, como a ADR-003.** O nome `SessionSource` fica substituído antes de o plano ser gravado. A ADR permanece Proposta até a frase do Anderson.

3. **Abrir este plano, invertendo a R1.4 do PLN-024.** O texto de lá: "este plano não cria a frente do Bob nem mexe em `brza sessions`" (`plans/PLN-024-prefixo-builder/PLN-024-plan.md:97`, na `origin/workstream/workspace` `28608025`). Opções:
   - abrir o PLN-026 e criar a frente (a escolhida) — custo: uma branch `builder/` com notas, e o código no `brza-workflow`; se paga: nesta abertura;
   - esperar o PLN-024 executar o verbo `brza note builder` — custo: a reunião de hoje não tem branch; se paga: se a norma do prefixo tiver de existir antes de qualquer nota.

   **Decidido — abrir o PLN-026 e publicar `builder/bob-the-builder`.** A R1.4 do PLN-024 fica invertida por esta sala. O PLN-024 em si não é editado daqui.

4. **A branch.** Opções:
   - `builder/bob-the-builder` a partir de `origin/master`, com worktree em `.worktrees/bob-the-builder` (a escolhida) — custo: o `brza note` de hoje recusa a branch, e o commit sai pelo git; se paga: agora, porque a R4 da sala já nomeou a branch;
   - `workstream/bob-the-builder` — custo: contradiz a R4 e o PLN-024; se paga: nunca para esta frente.

   **Decidido — `builder/bob-the-builder`.** Ponto de partida `5491da433fae67d1dd6217ba99862652c927e3f1`.

5. **O comando do `open`.** Opções, na mensagem seguinte:
   - `agent -p --output-format json --model <id> --workspace <dir> --trust`, com `--resume <chatId>` por persona, sem `--force`, e a capacidade só entra quando a prova passar (a escolhida; a ADR já dizia "só é declarada quando provada") — custo: uma chave e um processo por persona; se paga: na primeira ata;
   - `cursor-agent -p` como candidato solto, à espera da pesquisa da Shelly, que é o texto original da ADR — custo: adiar o comando que o `--help` já confirma; se paga: se o binário não fosse o `agent`;
   - `--force` junto — custo: a persona executa comando sem a trava que a sala tirou; se paga: nunca nesta prova.

   **Decidido — o comando com `--trust` e sem `--force`.** `--force` existe no `--help` e não entra no argv.

### Rodada 2 — em aberto, para a sala (não respondida)

**Apresentado antes:** `brza doctor --env` hoje sai 2 (`unrecognized arguments`). Sem a flag, o doctor sai 1 porque `GIT_AUTHOR_IDENT` é `Cursor Agent <cursoragent@cursor.com>`, e não o e-mail do `brz-anderson` (`packages/client/bin/brza-doctor:87-100`). `agent models` sai 1: "Authentication required". Não há lista de modelos para escolher.

1. **O que `brza doctor --env` confere para sair 0.**
   - `CURSOR_CONVERSATION_ID` definida basta; socket, app e identidade git não são erro; chave ausente é aviso (recomendada) — custo: uma flag no `brza-doctor`; se paga: no comando de aceite, neste pod;
   - exigir a identidade do `brz-anderson` — custo: o comando não passa neste pod sem exportar `GIT_AUTHOR_*`; se paga: se a cloud tiver de commitar pelo ambiente, e não por `git -c`;
   - exigir `CURSOR_API_KEY` — custo: o aceite do degrau 1 fica preso à chave; se paga: nunca para o degrau 1.

2. **Modelo e tamanho da reunião de prova.**
   - 2 personas, uma rodada, `--model` escolhido quando `agent models` listar a conta (recomendada) — custo: duas sessões headless depois da chave; se paga: na ata de hoje, se a chave entrar antes das 19h;
   - 3 personas — custo: uma sessão a mais de API; se paga: se a sala exigir quórum de três;
   - adiar a reunião até a chave e o modelo estarem nomeados — custo: a meta das 19h cai se a chave não chegar; se paga: se a chave não entrar hoje.

3. **Como o número PLN-026 entra no índice.**
   - o plano fica com esse número nesta branch, sem linha na master, até existir `brza note builder` (PLN-024/R1.1, ainda sem passo) (recomendada) — custo: outro `plan-open` pode emitir 026 nesse intervalo; se paga: quando o verbo existir e a reserva for refeita, sem editar o índice à mão;
   - criar `workstream/bob-the-builder` só para o `plan-open` — custo: segunda branch e um commit na master, contra o pedido desta sessão; se paga: agora, se a colisão for inaceitável;
   - editar `.brza/index.jsonl` à mão — custo: quebra a regra de que só o `brza note` acrescenta; se paga: nunca.

4. **O que cai se a janela apertar.**
   - caem, nesta ordem, o P10 e o P9; a reunião fica em 2 personas e uma rodada; o P4 permanece no PR (recomendada) — custo: usage pela API e `GROK_HOME` ficam para depois; se paga: na janela de hoje;
   - cortar também o P4 — custo: a ADR não dá o adaptador por aceito sem a suíte; se paga: nunca, num PR para a master;
   - não cortar nada — custo: a meta das 19h afirma o que não coube; se paga: nunca.

### Rodada 3 — a ADR fora do repo, a chave e o autor (enviada 2026-11-14)

**Apresentado antes:** o `52184ee` gravou `arquitetura/adr/ADR-003-porta-agent-runtime.md` e saiu com autor Anderson Pereira. Nomes `CURSOR_*` podem ser recusados em agentes da cloud. O `env.sh` só aceita `GIT_*`.

Respondida em 2026-11-14, pedido do Anderson nesta sessão.

1. **Onde mora a ADR-003.** Opções:
   - citação pelo número no plano, sem arquivo no repo (a escolhida) — custo: o texto integral fica fora do git; se paga: agora, porque artefato de arquiteto não entra em PR nem no repo;
   - manter o arquivo em `arquitetura/adr/` — custo: o PR e o repo passam a carregar o artefato; se paga: nunca, com a regra desta mensagem.

   **Decidido — sem arquivo.** Citação: ADR-003, autor Linus, status Proposta. O resumo das regras está no Desenho.

2. **Como a chave chega ao participante.** Opções:
   - segredo `BRZA_CURSOR_API_KEY`, e o wrapper faz `CURSOR_API_KEY="$BRZA_CURSOR_API_KEY"` só no ambiente do processo filho (a escolhida) — custo: uma variável a mais no wrapper; se paga: no P7, quando o agente da cloud aceitar o segredo;
   - `CURSOR_API_KEY` direto no ambiente do agente — custo: o nome `CURSOR_*` pode ser recusado; se paga: nunca, se a cloud recusar o prefixo;
   - `--api-key` na linha de comando ou linha no `env.sh` — custo: a chave aparece no argv ou num arquivo que só deve ter `GIT_*`; se paga: nunca.

   **Decidido — `BRZA_CURSOR_API_KEY` no wrapper, só no filho.** A chave não vai em `--api-key`, no `env.sh` nem no repo.

3. **Autor dos commits em `builder/*`.** Opções:
   - `Bob The Builder <bob@brza.dev>` daqui para a frente, sem reescrever o `52184ee` (a escolhida) — custo: o primeiro commit fica com outro autor; se paga: neste commit;
   - reescrever o `52184ee` — custo: reescreve história já publicada; se paga: nunca, com o pedido desta mensagem.

   **Decidido — Bob daqui para a frente.** O `52184ee` permanece com Anderson Pereira.

## Desenho

A ADR-003 (autor Linus, status Proposta) não tem arquivo neste repositório. Ela incorpora a ADR-002. Os passos executam este resumo:

- A porta é `AgentRuntime`, com `capabilities`, `list` e `read` obrigatórias, e `usage`, `open` e `send` opcionais.
- Capacidade não declarada falha com rc diferente de 0 e a mensagem nomeia o runtime e a capacidade.
- Os adaptadores são `StudioRuntime` e `CloudRuntime`.
- `CloudRuntime.open` é um `agent -p` por persona, com `--resume <chatId>`, sem `--force`. Revisor roda com `--mode ask`.

### O que este desenho assume

- **R1.1:** os quatro pontos de aceite e a ata da reunião.
- **R1.2:** a porta é `AgentRuntime`. Socket presente escolhe `StudioRuntime`; sem socket e com `CURSOR_CONVERSATION_ID`, escolhe `CloudRuntime`. `--runtime studio|cloud` força. Os dois presentes: o socket ganha, na ordem da frase da ADR.
- **R1.5:** o argv do `open` é o do `agent`, sem `--force`. A capacidade `open` entra no conjunto só depois da prova sair 0.
- **A reunião de prova tem uma rodada, entregue no prompt de abertura.** O `send` e o `close` ficam fora do conjunto até uma rodada seguinte precisar. O fim da rodada é o marcador do worklog (`wait_round.py --source marker`), porque `worker_done` é do Studio. Isso usa o que a skill já faz na abertura (`launch_persona.py:63-64`) e no modo de arquivo (`wait_round.py:14`).
- **A skill continua chamando `brza sessions`.** Não ganha caminho próprio de socket nem de `agent`.

### Terreno

#### O `brza sessions` hoje

- **A abertura exige o Studio.** `packages/client/bin/brza-sessions:4-7` e `:374-376`: `worker-start` e `ORCA_AGENT_SESSION_ID` ou `ORCA_TERMINAL_HANDLE`. A chamada está em `:980`.
- **O socket é o de macOS por default.** `bin/brza_runtime.py:26` e `:69-74`: `user_data()` cai em `~/Library/Application Support/brza-studio/orca-runtime.json`.
- **`--agent cursor` é recusado antes de efeito.** `tests/cli/test_brza_sessions.py:535-553`.
- **`GROK_HOME` não aparece** em `brza-sessions` nem em `brza_runtime.py`. A regra que a porta deve repetir está em `brza-studio/src/shared/grok-session-paths.ts:41-46`: `resolveGrokHomeDir` usa `GROK_HOME` absoluto ou `~/.grok`.

#### A meeting-runner

- **Mora em `origin/workstream/playground`**, SHA `03c9579d`, caminho `.claude/skills/meeting-runner/SKILL.md`. Não está na master nem nesta branch. Não está no `brza-workflow` nem no `brza-studio`.
- **Quem abre é o `brza sessions`.** `SKILL.md:55-56` e `:95-96`; `scripts/launch_persona.py:13-21`. O argv sai de `.claude/scripts/skillkit/sessions_cli.py:45-46`: `<nome> --agent --checkout --prompt-file --title --wait`.
- **A mensagem da rodada seguinte é `brza sessions send`.** `SKILL.md:114` e `:262`. A espera padrão é `brza sessions wait` (`wait_round.py:10-12`). O marcador `<!-- fim-rodada-N -->` é o registro que o `tally.py` lê (`SKILL.md:120`).
- **A ata da coordenação é** `work/worklogs/AAAA-MM-DD-<reuniao>-coordenacao.md` (`references/closing.md:33`). O commit previsto pela skill é `brza note commit` na branch do workstream (`closing.md:76`), que nesta branch recusa.

#### O que este pod roda

- **`CURSOR_API_KEY` ausente. `CURSOR_CONVERSATION_ID` presente** (prefixo `bc-`). `grok`, `claude` e `codex` ausentes antes e depois da instalação.
- **`agent` e `cursor-agent` apontam para o mesmo binário** 2026.11.13-eacade1. `--help` sai 0. `status` sai 0, "Not logged in". `models` sai 1. `create-chat` não voltou em 10 minutos e o processo foi encerrado.
- **`brza doctor --env` sai 2.** `brza doctor` sai 1 pela identidade.
- **`brza note plan-open` sai 1** nas duas formas: sem `--workstream` e com `--workstream bob-the-builder`. A master não recebeu commit.

### D1 — A porta `AgentRuntime` — `brza-workflow` (P1, P3, P4, P7, P9, P10)

- **Origem:** R1.2, R1.5, R3.1
- **Contexto:** dois consumidores com o mesmo buraco. O resumo da ADR-003 fixa o contrato; o degrau 1 não precisa de segredo.

#### Como fica

Dois arquivos novos. O agregador escolhe o adaptador e repassa. `StudioRuntime` chama o código que hoje está em `brza-sessions` e em `brza_runtime.rpc`, sem mudar o default de `user_data()`.

`CloudRuntime` no degrau 1 declara `capabilities`, `list` e `read`. `list` devolve um `SessionRecord` com `id` igual a `CURSOR_CONVERSATION_ID`, `source: cloud`, `agent: cursor`, `status: running`. `read` devolve ausente, com a marca `ausente`, porque o transcript ainda não está na máquina. `usage`, `open` e `send` ficam de fora do conjunto até serem provados: a chamada sai com rc diferente de 0 e a mensagem contém `cloud` e o nome da capacidade. Nada é escrito no JSON de abas. Nenhuma variável `ORCA_*` é criada.

`usage`, quando passar a existir, preenche cada métrica com a origem (`hook`, `note`, `api` ou `ausente`). O valor ausente é a string `ausente`, nunca `0`.

O `open`, depois da prova, é um processo por persona:

```text
agent -p --output-format json --model <id> --workspace <dir> --trust
```

O primeiro turno não leva `--resume` nem chama `create-chat`. O id é o `session_id` do JSON desse turno. Os seguintes acrescentam `--resume <session_id>`. Revisor acrescenta `--mode ask`. Sem `--force` e sem `--api-key`. O `--workspace` é o checkout absoluto da reunião. O wrapper do filho exporta `CURSOR_API_KEY` a partir de `BRZA_CURSOR_API_KEY`, tira `BRZA_CURSOR_API_KEY` do filho e não põe `CURSOR_API_KEY` no processo pai (R3.2). A prova que declara a capacidade é esse comando saindo 0.

O degrau 2, com a mesma chave no filho, acrescenta `list` de outras runs, `read` do transcript e `usage` com origem `api`. É o P10.

`GROK_HOME`, quando o runtime escolhido for `grok`, resolve como `resolveGrokHomeDir`: diretório absoluto da variável, ou `~/.grok`. É o P9. O caminho `agent` não lê essa variável.

#### Em aberto

- **R2.2** escolhe o `<id>` do modelo e se a prova tem 2 ou 3 personas. O argv acima já deixa o `<id>` como argumento.

### D2 — O dry-run e o doctor — `packages/client/bin/brza-sessions`, `brza-doctor` (P2, P5)

- **Origem:** R1.1 pontos 2 e 3

#### Como fica

`brza sessions diag-cloud --agent cursor --dry-run --model <id> --workspace <dir>` sai 0, imprime uma linha com `abriria` e o argv do D1, e não chama `orchestration worker-start`. `--agent` diferente de `cursor` nesse verbo sai diferente de 0.

#### Em aberto

- **R2.1** fecha o que `--env` trata como erro. A recomendação: sai 0 com `CURSOR_CONVERSATION_ID` definida; socket ausente e identidade git diferente do `brz-anderson` não são erro; chave ausente é aviso.

### D3 — O marcador no `--by-execution` — `core/scripts/summarize_measurements.py` (P6)

- **Origem:** R1.1 ponto 4, alinhado ao P3 do PLN-025

#### Como fica

`python3 scripts/summarize_measurements.py --by-execution` imprime custo e tokens como `ausente` quando o log não traz o número. O teste grava o esperado `ausente` no próprio teste. O PLN-025 falava em campo vazio; esta sala pediu a marca `ausente`, para o vazio não ser lido como zero. O código mora no `brza-workflow`. O arquivo do PLN-025 não é editado desta branch.

### D4 — A reunião de prova — skill em `origin/workstream/playground`, ata nesta branch (P8)

- **Origem:** a entrega pedida, R2.2 quando fechar

#### Como fica

A sessão que Anderson pedir abre um worktree só de leitura de `origin/workstream/playground` em `03c9579d` e roda `launch_persona.py` de lá. O manifesto da reunião nasce nesta branch, com 2 personas (ou 3, se a R2.2 mudar), uma rodada, `--agent cursor` e o checkout deste worktree. A ata sai em `work/worklogs/AAAA-MM-DD-<reuniao>-coordenacao.md`, no molde de `references/closing.md`. O commit da ata é nesta branch, sem PR.

## Passos

### P1 — Listar a run da cloud sem o socket — em PR

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 3 h · Executado: — h

Repo: `brza-workflow`, PR para a `master`. Risco ao Studio: nenhum, se o caminho com socket continuar no `StudioRuntime` e o default de `user_data()` não mudar. Desfazer: reverter o commit do PR.

- [ ] **1.** Teste que falha: sem `orca-runtime.json` e com `CURSOR_CONVERSATION_ID=bc-teste`, `list --json` sai 0 e o JSON tem `source: cloud` e esse id.
- [ ] **2.** Implementar `CloudRuntime.list` no degrau 1 e a seleção da porta.
- [ ] **3.** O mesmo teste mostra que o JSON de abas não foi escrito e que o ambiente não ganhou `ORCA_*`.
- [ ] **4.** Commit no `brza-workflow`.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `2dc77ac`. O teste `CloudPortTest.test_list_json_without_the_socket_returns_the_cloud_run_and_writes_nothing` passa. As caixas seguem abertas até o merge.

### P2 — O dry-run que imprime `abriria` — em PR

Executa D2 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

Repo: `brza-workflow`, no mesmo PR do P1. Risco ao Studio: a recusa de `--agent cursor` no runtime studio permanece (`test_brza_sessions.py:535`). Desfazer: reverter o commit.

- [ ] **1.** Teste que falha: `diag-cloud --agent cursor --dry-run` sai 0, a saída contém `abriria`, e o espião de `worker-start` conta 0.
- [ ] **2.** Implementar o verbo em cima do argv do D1, sem executar.
- [ ] **3.** Rodar o teste.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `2dc77ac`. O teste `CloudPortTest.test_diag_cloud_dry_run_prints_abriria_and_does_not_start_a_worker` passa. As caixas seguem abertas até o merge.

### P3 — Capacidade ausente falha nomeando runtime e capacidade — em PR

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

Repo: `brza-workflow`, no mesmo PR. Risco ao Studio: nenhum no caminho studio. Desfazer: reverter o commit.

- [ ] **1.** Teste que falha: `--runtime cloud` em `read` sai 0 e o campo de transcript é `ausente`.
- [ ] **2.** `usage`, `open` e `send`, enquanto não forem declarados, saem diferentes de 0 e a mensagem contém `cloud` e o nome da capacidade.
- [ ] **3.** Rodar o teste.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `2dc77ac`. `read` sai 0 com `transcript: ausente`. `usage`, `open` e `send` saem 1 e a mensagem nomeia `cloud` e a capacidade. As caixas seguem abertas até o merge.

### P4 — `StudioRuntime` e a suíte de contrato — em PR

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 4 h · Executado: — h

Repo: `brza-workflow`, no mesmo PR. Risco ao Studio: o comportamento no Mac pode divergir se a extração mudar argv ou rc. Desfazer: reverter o commit; a regressão se confere antes do merge.

- [ ] **1.** Mover o comportamento atual para `StudioRuntime` sem alterar saída dos testes já verdes.
- [ ] **2.** A suíte de contrato roda contra os dois adaptadores.
- [ ] **3.** `tests/cli/test_brza_sessions.py` passa, inclusive a recusa de `--agent cursor` quando o runtime é o studio.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `2dc77ac`. A suíte de contrato passa nos dois adaptadores. A expectativa de `test_unknown_agent_is_refused_before_any_side_effect` não foi editada. As caixas seguem abertas até o merge.

### P5 — `brza doctor --env` sai 0 — em PR

Executa D2 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

Repo: `brza-workflow`, no mesmo PR. Risco ao Studio: `brza doctor` sem a flag permanece como está. Desfazer: reverter o commit.

- [ ] **1.** A R2.1 respondida vira o critério do teste.
- [ ] **2.** Implementar `--env` sem mudar o rc do doctor sem flag.
- [ ] **3.** Neste pod, `brza doctor --env` sai 0.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `903bf7d`. No pod, `brza doctor --env` saiu 0. Socket ausente só deixa de ser erro com `CURSOR_CONVERSATION_ID`. Sem a variável, o teste `DoctorTest.test_env_without_cloud_and_without_socket_is_an_error` exige `ERRO`. As caixas seguem abertas até o merge.

### P6 — Custo e tokens ausentes no `--by-execution` — em PR

Executa D3 · executor: sessão no `brza-workflow`

Estimado: 3 h · Executado: — h

Repo: `brza-workflow`, no mesmo PR ou num PR empilhado se o P3 do PLN-025 já estiver mexendo no arquivo. Risco ao Studio: nenhum. Desfazer: reverter o commit. Não editar o arquivo do PLN-025 a partir desta branch.

- [ ] **1.** Teste que falha com o literal `ausente` para uma execução sem custo e sem tokens, e com um número para a execução que tem os dois.
- [ ] **2.** Implementar no agregador que o PLN-025/D1 já descreve.
- [ ] **3.** O teste passa e a saída da execução sem chave não contém `0` nesses dois campos.

**Evidência:** em PR, [brza-workflow#3](https://github.com/brz-anderson/brza-workflow/pull/3), commit `e1dd29f`. `ByExecutionTest` passa. No pod, a linha da run é `custo=ausente (ausente)  tokens=ausente (ausente)`. As caixas seguem abertas até o merge.

### P7 — Provar o `open` e só então declará-lo

Executa D1 · executor: sessão no `brza-workflow`, no pod com o segredo

Estimado: 3 h · Executado: — h

Repo: `brza-workflow`, PR separado, depois da prova. Risco ao Studio: nenhum enquanto a capacidade só existe no `CloudRuntime`. Desfazer: tirar `open` do conjunto e reverter o commit. Sem `BRZA_CURSOR_API_KEY`, o passo para e a capacidade continua de fora.

**Decisão da sala (R3.2, 2026-11-14).** A chave entra como segredo `BRZA_CURSOR_API_KEY`. Nomes `CURSOR_*` podem ser recusados em agentes da cloud. O wrapper do participante faz `CURSOR_API_KEY="$BRZA_CURSOR_API_KEY"` só no ambiente do processo filho. A chave nunca vai em `--api-key`, no `env.sh` (que só aceita `GIT_*`) nem no repo.

- implementado, aguardando merge. **1.** Com `BRZA_CURSOR_API_KEY` no segredo, o filho recebe `CURSOR_API_KEY` e o primeiro turno devolve um id. O processo pai não fica com `CURSOR_API_KEY`. O argv não contém `--api-key`. O id é o `session_id` do JSON do `agent -p`.
- implementado, aguardando merge. **2.** O comando do D1, com esse id no `--resume`, sai 0 e imprime JSON. Sem `--force`. Revisor leva `--mode ask`. O `send` de outro processo relê workspace, modelo e modo do `persona.json`.
- implementado, aguardando merge. **3.** `open` e `send` entram em `capabilities()` só com chave e binário `agent`. O `ContractTest` do PR A roda contra `StudioRuntime` e `CloudRuntime`. `test_open_argv_is_agent_p_without_force` segue passando.

**Evidência:** em PR, sem caixa marcada. A ponta é `d45b7d82e1db33b07004e3bf36addec5871c7c15` em `builder/pln-026-pr-b`, [PR 2](https://github.com/brz-anderson/brza-workflow/pull/2), sobre `2a0580d6cb07d2a4d50ff086016b96ec775dbf8b`. A prova daquele corte, `e07fd479fef2b5cc7e3656ca0e2cb6a05ec9274b` sobre `bc89dda14be5d4df39c0d01e3627f5054ec3c2b5`, no pod, modelo `grok-4.7-low`, modo `ask`, send de outro processo: open rc 0, `session_id` `2cc17cfa-ac1c-4e3b-b710-de38049cd9f2`, result `P7-OK`, 2064 ms, tokens 17613/34/1152/0/30; send rc 0, o mesmo id, result `P7-OK`, 3931 ms, tokens 233/180/18688/0/176. Custo `ausente`. `leak_count` 0. O `session_id` foi aceito pelo `--resume` e o contexto ficou. Detalhe no [O P7 do PLN-026 abre e retoma o turno na cloud](../../work/worklogs/2026-11-14-pln026-pr-b.md). Executado: 1,7 h no plano, critério no Retomar.

### P8 — A reunião e a ata

Executa D4 · executor: sessão nesta branch, com a skill do playground

Estimado: 3 h · Executado: — h

Repo da ata: `brza-workspace`, branch `builder/bob-the-builder`, sem PR. Risco ao Studio: nenhum; o runtime forçado é `cloud` e o socket não existe neste pod. Desfazer: apagar o worklog da reunião num commit nesta branch e não declarar a reunião feita. Depende do P7 e da R2.2.

- implementado, aguardando merge. **1.** A skill veio de `origin/workstream/playground` `03c9579d56fb2304a48821e2c6978e0514cd7df3` para esta branch (`61658f02461b7cc2d2c8362ec1b91015e30e5020`), com o `skillkit` (`fd476c8fd52cc53ecb21f5374d0821bb141534bb`). X6 e X7.
- implementado, aguardando merge. **2.** `--transport cloud` abre com `CloudRuntime.open(spec)` e manda a rodada com `send(session_id, prompt)`. O checkout vem de `BRZA_WORKFLOW_DIR` e o módulo é `packages/client/bin/cloud_runtime.py`. Sem a variável, a mensagem pede para defini-la. Sem a flag, o `brza sessions` segue igual.
- implementado, aguardando merge. **3.** As atas smoke estão em `work/worklogs/`, com `<!-- fim-rodada-1 -->` e a marca SMOKE. Não contam para a promoção. O commit é nesta branch, sem PR.

**Evidência:** em PR, sem caixa marcada. A ata da passagem do `92575d1` está em `9c20c76680d0ba589b4e2b2d422fff8c9595e60d`, [A reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-coordenacao.md). O transporte desta nota aponta para `e07fd479fef2b5cc7e3656ca0e2cb6a05ec9274b`. A prova desse SHA, com as duas personas, está em [A segunda reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-2-coordenacao.md). X8: a rodada contra `a066d39` foi descartada e não é a ata gravada. O probe `e80ab013` saiu da evidência: o JSONL não está no worklog. Custo `ausente`. `leak_count` 0. Marcador `<!-- fim-rodada-1 -->`. O detalhe está no [O P8 do PLN-026 roda a reunião smoke na cloud](../../work/worklogs/2026-11-14-pln026-p8.md). Executado: — h (X5).

### P9 — `GROK_HOME` pela regra do Studio

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

Repo: `brza-workflow`. Risco ao Studio: nenhum; a função do app não muda. Desfazer: reverter o commit. Primeiro candidato a corte depois do P10.

- [ ] **1.** Teste: `GROK_HOME` absoluto vence; sem a variável, o diretório é `~/.grok`.
- [ ] **2.** O runtime `cursor` não lê a variável.

**Evidência:** —

### P10 — Degrau 2, a API com a chave

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 4 h · Executado: — h

Repo: `brza-workflow`, PR próprio. Risco ao Studio: nenhum. Desfazer: reverter o commit. Primeiro corte da janela. Sem `BRZA_CURSOR_API_KEY`, não começa. O filho usa o mesmo wrapper do P7.

- [ ] **1.** `list` de outra run, `read` do transcript e `usage` com origem `api`, cada um com teste que falha antes.
- [ ] **2.** Campo sem dado na resposta continua `ausente`.

**Evidência:** —

## Regressão

- **No Mac, com o socket, `list`, `read`, `usage`, abertura, `send` e `close` seguem iguais.** Conferência: `tests/cli/test_brza_sessions.py` no CI do `brza-workflow`.
- **`--agent cursor` no runtime studio continua recusado** com a frase do teste em `test_brza_sessions.py:547-549`.
- **`user_data()` sem `ORCA_USER_DATA_PATH` continua** `~/Library/Application Support/brza-studio` (`brza_runtime.py:26`).

## PRs previstos

- **PR A, `brza-workflow` → `master`:** P1 a P6. É o degrau 1, o dry-run, a falha explícita, o `StudioRuntime`, o `--env` e o marcador `ausente`.
- **PR B, `brza-workflow` → `master`, depois da prova:** P7 e, se a janela deixar, P9. O P10 fica num PR C se não for cortado.
- **Nenhum PR no `brza-studio`**, salvo o P4 mostrar regressão que não caiba no cliente.
- **A ata não vai por PR.** O commit é direto em `builder/bob-the-builder`, como a norma deste repositório.

## Worklogs

- 2026-11-14 — abertura: branch, inventário, probe do `agent` e este plano. A Rodada 2 ficou sem resposta. R3.1 tirou a ADR-003 do repo. R3.2 fixou `BRZA_CURSOR_API_KEY`. Nenhum passo executado.
  [A abertura do PLN-026 ficou na branch do Bob](../../work/worklogs/2026-11-14-pln026-abertura.md)
- 2026-11-14 — PLN-026 P7: `open` e `send` no `CloudRuntime`, prova no pod e PR 2. O PR A não estava no origin. P8, P9 e P10 não foram tocados.
  [O P7 do PLN-026 abre e retoma o turno na cloud](../../work/worklogs/2026-11-14-pln026-pr-b.md)
- 2026-11-14 — PLN-026 P8: transporte `cloud` na meeting-runner e a reunião smoke, com ata. Não conta para a promoção. P9 e P10 não foram tocados.
  [O P8 do PLN-026 roda a reunião smoke na cloud](../../work/worklogs/2026-11-14-pln026-p8.md)
- 2026-11-14 — ata da reunião smoke do P8, marcada SMOKE.
  [A reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-coordenacao.md)
- 2026-11-14 — P1 a P6 em PR, sem merge. As caixas seguem abertas.
  [O PR A do PLN-026 levou o degrau 1](../../work/worklogs/2026-11-14-pln026-pr-a.md)
- 2026-11-14 — segunda ata smoke do P8, depois da revisão xhigh, marcada SMOKE.
  [A segunda reunião smoke do PLN-026 não conta para a promoção](../../work/worklogs/2026-11-14-pln026-reuniao-smoke-2-coordenacao.md)

## Revisões

- [REV-028: a revisão xhigh R2 do P8 do PLN-026](../../work/reviews/REV-028-pln026-p8-r2.md) — 2026-11-14, 7 achados, triagem corrigir.
- [REV-pln026-pr-b R2: a revisão xhigh R2 do PR 2 do PLN-026](../../work/reviews/2026-11-14-REV-pln026-pr-b-r2.md) — 2026-11-14, achados 1 a 4 e os gates 2 e 3, triagem corrigir.

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um. Trabalho só em notas de `work/` e `plans/` não tem resumo.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão em `work/decisions/`, a norma do `brza-studio`, o guia.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
