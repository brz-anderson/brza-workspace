---
status: in_progress
phase: execution
origin: request
description: O esboço dos Builders mede cada execução, guarda a nota de feedback e deixa a persona com modelo Grok e alternativa quando houver crédito.
ready: sim
estimate_h: 12.5
executed_h: 0
remaining_h: 12.5
priority: medium
depends_on:
  - PLN-024
scope:
  - workspace
  - brza-workflow
opened: 2026-11-14
owner: Anderson
tags:
  - planning
  - tooling
---

# PLN-025: Cada execução de Builder deixa métrica, nota e persona calibrável

- **Retomar:** P1 feito em 2026-11-14. O P2 está em PR aprovado na revisão e aguarda o merge de Anderson: [PR 1](https://github.com/brz-anderson/brza-workflow/pull/1), branch `cursor/pln-025-feedbacks-f7d0`, HEAD `2245460`. O passo continua desmarcado. A prova está em [A execução do P2 do PLN-025 ficou no PR do gênero feedbacks](../../work/worklogs/2026-11-14-pln025-p2-feedbacks.md). Depois do merge, o próximo ato é marcar o P2. P3 não começou.

## Pedido

- **Origem:** pedido de Anderson, nesta sessão do Bob, em 2026-11-14. A norma vigente ainda manda o autor `brz-anderson` em `workstream/*`. O [PLN-024: Norma aceita o prefixo builder/ (workstream pessoal de Builder)](../PLN-024-prefixo-builder/PLN-024-plan.md) já decidiu o manifesto e o rótulo `builder/<nome>`, e nenhum passo dele rodou.

"abrir um PLANO (só o plano, sem executar nenhum passo) para um primeiro esboço do BrzA Builders". As quatro frentes, nas palavras do pedido: "Scripts para medir a eficiência dos agentes", com tarefa, tipo, modelo, esforço, duração, custo e tokens se houver, rodadas, chamadas de ferramenta, retrabalho, correções do humano e resultado, reaproveitando o que já existe; "Notas de feedback de cada execução", com o que foi pedido, o modelo e o esforço e o porquê, onde o modelo errou, se o esforço ficou desregulado e uma recomendação; "Personas", com modelo e esforço padrão, o porquê e os limites, ligadas ao manifesto `.brza/builders/<nome>.toml` e aos passos E1 a E8 do ambiente replicável, com modelo Grok padrão e alternativa quando houver crédito; "Ciclo de calibração", com relatório, limiares e quem decide. "Todos os passos ficam desmarcados."

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| Pedido 1 | Uma execução reúne os campos pedidos a partir do log que já existe; custo e tokens ausentes ficam vazios | P3 | `tests/hooks/test_summarize_measurements.py` (unidade) |
| Pedido 2 | A nota de feedback tem o molde, e o checador recusa nota sem as seções | P2 | `tests/notes-checker/run.py` (unidade) |
| Pedido 3 | O catálogo tem persona, Grok padrão, alternativa com crédito, porquê e limites, e aponta o manifesto | P4 | leitura do toml contra `runtimes.efforts` (unidade) |
| Pedido 4 | O relatório sugere ajuste e não grava o catálogo | P5 | o comando não altera `.brza/personas.toml` (unidade) |
| Pedido, o exemplo | A execução desta sessão fica preenchida no molde | P6 | leitura da nota (manual) |

### Fora de escopo

- **Executar E1 a E9 do estudo do ambiente.** O canvas de 2026-11-14 fica como terreno. Nenhum `mise.toml`, `brza builder up` nem Dockerfile nasce aqui.
- **Executar o PLN-024.** O manifesto do Bob e o prefixo `builder/` continuam naquele plano.
- **A branch `builder/bob-the-builder`.** Não se cria, não se apaga, não recebe nota.
- **Editar o `brza-workflow` nesta abertura.** O código entra nos passos, numa sessão daquele repositório, quando Anderson pedir o passo.
- **Tabela de preço do Grok e hook novo do Cursor cloud.** Sem fonte no disco, o campo fica vazio.

## Restrições

- **Passo deste plano só executa com pedido explícito de Anderson, um por vez.**
- **Custo e tokens que o log não traz ficam ausentes.** O agregador não estima preço de modelo fora da tabela.
- **O catálogo não muda sozinho.** O relatório sugere; a frase de Anderson grava.
- **Commit em `workstream/*` segue com brz-anderson** até o P5 do PLN-024 existir na norma.

## Pré-requisitos

- **O log `.measurements/measurements.jsonl` e o `summarize_measurements.py` existem** no `brza-workflow`. Sem o log, o P3 para e o campo da execução fica só na nota.
- **A R1 respondida em 2026-11-14**, nas quatro recomendações. P2–P6 podem começar quando Anderson pedir o passo.

## Entrevista

### Rodada 1 — nota, catálogo, quem decide e a fonte no cloud (enviada 2026-11-14)

**Apresentado antes:** o hook de medição já grava, num turno Claude, modelo, esforço, duração, tokens, custo estimado, chamadas de ferramenta e rodadas (`core/.claude/hooks/measure.py:487-507`). A tabela de preço só tem modelos Claude (`measure.py:56-67`); Grok sai com custo vazio. A telemetria `route` grava a decisão de modelo e esforço (`packages/mcp/brza_mcp/telemetry.py:80-91`). O `brza quota` lê janelas de uso (`accounts.py:327`). A policy já tem três papéis por runtime, e no Grok o architect é `grok-4.7` com `xhigh`, o executor com `high` e o consultant com `low` (`policy.py:36-38`). A escada do `grok-4.7` é `low`, `medium`, `high`, `xhigh` (`runtimes.py:32`). Não há diretório de eval nas skills do `brza-workflow` nem deste workspace; a prova delas hoje é o teste de ouro e o `tests/notes-checker/run.py`. O [PLN-023: O plano novo do playground mostra a pendência, o dono e quem pode executar](../PLN-023-gates-do-plano/PLN-023-plan.md) fecha o gate na tarefa (`Autorizado`, `Pendente`, `Pronto`), e o código desse gate não foi escrito. O canvas "Ambiente replicável e isolado dos Builders" (2026-11-14) lista nove passos sem a letra E. Este plano chama de E1 a E8 os oito primeiros, como no pedido, e de E9 a comparação do `doctor` entre o Mac e a cloud. As personas encostam no E3, o schema do manifesto. Esta sessão foi lançada em `grok-4.7` com esforço `high` depois de `claude-opus-5-5` com esforço `high` recusado com "Buy credits or switch to a Grok model".

Respondida em 2026-11-14, nesta sessão. Anderson aceitou as quatro recomendações.

1. **Onde a nota de feedback vive.** Opções:
   - gênero novo `work/feedbacks/`, uma nota por execução, sem `status`, nome `AAAA-MM-DD-<assunto>.md` (recomendada) — custo: uma seção no `work/README.md` e uma regra no `check_notes.py`, no mesmo commit do `brza-workflow`; se paga: no primeiro relatório, que filtra nota sem ler o worklog inteiro;
   - seção `## Feedback do modelo` dentro do worklog da tarefa — custo: zero gênero novo, e o checador passa a exigir as cinco seções nesse worklog; se paga: agora, se a execução e o diário forem sempre o mesmo arquivo;
   - memória `type: feedback`, que o `--by-workstream` já conta — custo: fica fora do git como nota e o checador não vê o molde; se paga: nunca, se a pergunta for a nota existir e o checker validar.

   **Decidido em 2026-11-14 — a recomendada.** "A nota de feedback fica num gênero novo, `work/feedbacks/`, com uma nota por execução." O P2 grava o gênero. A seção no worklog e a memória `feedback` ficam de fora.

2. **Onde o catálogo de personas vive.** Opções:
   - arquivo versionado `.brza/personas.toml` no brza-workspace, schema na norma, e o `.brza/builders/<nome>.toml` só aponta e sobrescreve (recomendada) — custo: um arquivo e o schema, ao lado do E3; se paga: quando o segundo Builder nascer, sem copiar as seis personas;
   - seção `[personas]` dentro de cada manifesto — custo: uma cópia por Builder, cobrada em toda mudança de padrão; se paga: se cada Builder tiver catálogo próprio de verdade;
   - estender `policy.roles` no `brza.toml` — custo: mistura cota e roteamento com o tipo de tarefa; se paga: se as seis personas couberem nas três camadas que já existem.

   **Decidido em 2026-11-14 — a recomendada.** "O catálogo de personas fica em `.brza/personas.toml` no brza-workspace, com o schema na norma. O manifesto só aponta para o catálogo e sobrescreve o que precisar."

3. **Quem aplica o ajuste de modelo e esforço.** Opções:
   - o relatório sugere e Anderson decide em rodada; o toml só muda com a frase dele (recomendada) — custo: uma rodada por ciclo; se paga: na primeira vez que um limiar dispararia sozinho e estaria errado;
   - o script grava a troca e Anderson revê depois — custo: o catálogo muda sem frase, cobrado na sessão seguinte que ler o padrão velho; se paga: se o ciclo for frequente e a rodada atrasar a correção;
   - ninguém muda até haver um número mínimo de notas, e esse número fica para a R2 — custo: o padrão espera a amostra; se paga: enquanto a única execução for esta sessão.

   **Decidido em 2026-11-14 — a recomendada.** "O relatório sugere o ajuste e o Anderson decide em rodada." O toml não muda sem essa frase. Os números 3, 2 e 5 continuam hipótese, para a R2.

4. **De onde a execução no Cursor cloud tira custo e tokens.** Opções:
   - a nota é a fonte quando não há hook; o script lê o log Claude quando ele existe e deixa custo e tokens vazios no Grok e no cloud (recomendada) — custo: a nota carrega modelo, esforço, recusa e resultado; se paga: nesta sessão, que não passa pelo `measure.py`;
   - esperar um hook do Cursor para medir cloud — custo: o esboço não mede estas sessões até o hook existir; se paga: se esse hook entrar no E6;
   - um jsonl novo, escrito pelo agente — custo: um segundo log ao lado de `.measurements/`; se paga: nunca, porque o resumo já lê um log só.

   **Decidido em 2026-11-14 — a recomendada.** "A nota é a fonte quando não há hook. O script lê o log do Claude quando ele existir e deixa custo e tokens vazios nas sessões Grok e cloud." O script é a flag do D1. A2 fica descartada.

## Desenho

### O que este desenho assume

- **R1.1:** a nota é o gênero `work/feedbacks/`, uma por execução.
- **R1.2:** o catálogo é `.brza/personas.toml` no brza-workspace, com o schema na norma. O manifesto aponta e sobrescreve.
- **R1.3:** o relatório sugere. Anderson decide em rodada. O toml só muda com a frase dele.
- **R1.4:** sem hook, a nota é a fonte. Com log Claude, o script lê esse log. Custo e tokens ficam vazios em Grok e no cloud.
- **R1.6 do PLN-024, ainda não executada:** quando a branch for `builder/<nome>`, a medição gravará `builder/<nome>`. Este plano não muda o hook; o relatório lê o rótulo que o hook gravar.
- **O E3 não foi executado.** O catálogo aponta o manifesto; não cria o toml do Bob.

### Terreno

#### Medição que já existe

- **O retorno de um turno.** `brza-workflow/core/.claude/hooks/measure.py:487-507` — `model`, `effort`, `duration_s`, `api_calls`, `tool_calls`, `tokens`, `estimated_cost_usd`, `denials`, e ao lado `rounds` e `prompt_head`.
- **Preço só de Claude.** `measure.py:56-67`. Modelo fora da tabela fica com custo `None` (`measure.py:53-54`).
- **O prefixo.** `measure.py:781-785` só corta `workstream/`. O mesmo corte está em `telemetry.py:26` e `:75`. O P4 do PLN-024 é que passa a gravar `builder/<nome>`.
- **A rota.** `telemetry.py:80-91` — evento `route`, com `model`, `effort`, `decision`, `reason`.
- **A cota.** `accounts.py:327-355` — por conta e runtime, `used`, `resets_at` e a projeção. O teto padrão é `quota.hard_cap_percent` 90 (`policy.py:43`).
- **O resumo.** `core/scripts/summarize_measurements.py` — `--by-workstream` e `--by-task`. A memória `feedback` entra na conta de correções (`summarize_measurements.py:352`).
- **Os planos vizinhos.** PLN-012 mede tempo, custo e máquina por tarefa. PLN-018 põe Grok e Codex nessa medição. Os dois estão no workstream `tools-kit`.

#### Nota, checador e gate

- **Gêneros.** `check_notes.py:80-87` conhece `work/notes`, `work/issues`, `work/worklogs`, `work/reviews`, `work/decisions` e `wiki/guides`. Pasta nova sem entrada aqui não vira gênero.
- **Worklog.** `work/README.md:307-331` — um assunto por arquivo, sem `status`, e a `## Custo da tarefa` é do `brza note commit`, não à mão.
- **O gate do PLN-023.** A pendência fica na tarefa, com `Pendente: … · de: Anderson`. Serve de forma para "quem destrava", e não de métrica de eficiência.

#### Ambiente e manifesto

- **E1.** `mise.toml` e `mise.lock` no `brza-workflow`, sem mudar o `install.sh` ainda.
- **E2.** Tirar hardcodes: `GROK_HOME`, a porta do MCP por `BRZA_HOME`, e o autor git do `settings.json`.
- **E3.** O schema do manifesto na norma e o primeiro arquivo, o do Bob.
- **E4.** `brza builder up` e `down`, o HOME isolado.
- **E5.** Segredos por referência.
- **E6.** `brza bootstrap`, e o painel do BrzA Cloud Builders fica com duas linhas.
- **E7.** `brza doctor --env`.
- **E8.** Dockerfile ou devcontainer gerado do mesmo lock.
- **E9.** Comparar a saída do `doctor` no Mac e na cloud. O canvas não separa este nono do resto; o pedido falou em E1 a E8, e a comparação fica nomeada para não sumir.
- **O manifesto decidido.** PLN-024/D5 — `.brza/builders/<nome>.toml`, schema na norma. O toml do Bob não nasce naquele plano.

### D1 — Uma execução no resumo que já existe — `core/scripts/summarize_measurements.py` (P3)

- **Origem:** R1.4
- **Contexto:** o pedido lista campos que o hook já tem e campos que ninguém grava (tipo da tarefa, retrabalho, correção pedida, resultado). Um segundo log dividiria o resumo.

#### As alternativas

##### A1 — Flag no resumo

- **Custo:** um modo a mais no arquivo que já agrega o jsonl. · **Se paga:** no primeiro `--by-execution`, que reusa o parser. · **Reabre:** se a nota e o log precisarem de um programa só deles.

##### A2 — Script novo que relê o jsonl

**Descartada.** Anderson aceitou a recomendação em 2026-11-14: o script lê o log que já existe. Um segundo leitor cobraria a mesma mudança duas vezes.

#### Como fica

`python3 scripts/summarize_measurements.py --by-execution` imprime uma linha por execução. A execução Claude é o grupo de eventos `turn`, `subagent`, `route` e `failure` já gravados, unidos pela sessão. A nota de feedback, quando existe, entra pela sessão e preenche tipo, retrabalho, correção e resultado. O comando não escreve arquivo.

| Campo | Fonte |
| :---- | :---- |
| Tarefa | `prompt_head` do turno; o pedido da nota quando houver |
| Tipo | a nota |
| Modelo e esforço | o turno, ou a linha `route`, ou a nota |
| Duração | `duration_s` |
| Custo e tokens | o turno, só se o modelo estiver em `PRICES`; senão vazio |
| Rodadas e ferramentas | `rounds` e `tool_calls` |
| Retrabalho, correção, resultado | a nota |
| Rótulo | o `workstream` que o hook gravou, inclusive `builder/<nome>` quando o P4 do PLN-024 tiver rodado |

Execução sem hook, como esta sessão no Cursor cloud, aparece se houver nota. Custo e tokens ficam vazios.

### D2 — A nota de feedback — `work/feedbacks/` (P2, P6)

- **Origem:** R1.1
- **Contexto:** o worklog é o diário da tarefa. A memória `feedback` já conta correção e não tem molde. O checador só valida gênero que está na tabela.

#### Como fica

Pasta `work/feedbacks/`, gênero `feedback`, sem `status`, no mesmo grupo de `worklog` e `note`. Nome `AAAA-MM-DD-<assunto>.md`. Frontmatter com `scope`, `builder`, `task_type`, `model`, `effort`, `result` (`done`, `refused` ou `partial`) e `session` quando houver id. Cinco seções, nesta ordem: `## Pedido`, `## Escolha`, `## Erro`, `## Esforço`, `## Próxima vez`.

O `check_notes.py` ganha o gênero na tabela e recusa nota sem uma dessas seções, com `result` fora dos três valores, ou com `model` e `effort` vazios. A norma e o script mudam no mesmo commit, no P2. O exemplo continua neste plano até o P6: a pasta ainda não é gênero no checador.

#### Exemplo desta sessão

```markdown
---
scope:
  - workspace
builder: bob
task_type: design
model: grok-4.7
effort: high
result: done
session: cursor-cloud-2026-11-14
---

# Feedback 2026-11-14 esboço dos Builders

## Pedido

Abrir só o plano do esboço dos Builders, nas quatro frentes, com os passos desmarcados, pelo `brza note plan-open` no workstream `workspace` e o `brza note commit`. Sem editar o `brza-workflow` e sem mexer na branch `builder/bob-the-builder`.

## Escolha

`grok-4.7`, esforço `high`. A tarefa é desenho, com a norma de plano, o worklog, o PLN-024, o hook e o estudo do ambiente no mesmo texto. A primeira escolha foi `claude-opus-5-5` com esforço `high`, a camada alta do AGENTS.md para desenho. O launch foi recusado com "Buy credits or switch to a Grok model".

## Erro

O canvas do ambiente não numera E1 a E8: são nove itens sem letra. O plano nomeia os oito primeiros como no pedido e guarda o nono como E9. Não há pasta de eval nas skills; o plano cita o teste de ouro e o checador, e não um caminho inventado. Fora isso, nesta abertura, o molde do plano fechou com a R1 aberta e os passos desmarcados.

## Esforço

Regulado. Evidência: a policy põe o architect Grok em `xhigh`, e esta sessão usou `high`, o mesmo esforço da escolha que o crédito recusou, trocando só o modelo. O plano coube no molde sem uma segunda rodada de correção do checador. Subir a `xhigh` ficaria demais enquanto `high` fecha a abertura. Descer a `medium` ficaria pouco: o texto cruza PLN-024, PLN-023, o hook e o canvas.

## Próxima vez

Desenho de plano no Cursor cloud, sem crédito extra, começa em `grok-4.7` com esforço `high`. `claude-opus-5-5` com esforço `high` volta quando o launch for aceito. `xhigh` entra se uma sessão `high` perder uma dependência da norma que outra pessoa apontar.
```

### D3 — O catálogo de personas — `.brza/personas.toml` (P4)

- **Origem:** R1.2
- **Contexto:** seis tipos de tarefa não cabem nos três papéis da policy sem perder o revisor, o medidor e o operador. O modelo padrão tem de ser Grok, porque o cloud sem crédito recusou o Opus. A alternativa fica no catálogo para o dia em que o launch passar.

#### Como fica

`.brza/personas.toml` na raiz do brza-workspace. O schema mora na norma, no `core/` do `brza-workflow`, no mesmo texto que o PLN-024/P6 reserva para o schema do manifesto. O manifesto ganha, quando o E3 ou o P5 do PLN-024 escrever o arquivo, a chave `personas` apontando para este toml e uma tabela curta de sobrescrita. Sem o toml do Bob, o catálogo já vale como padrão.

Identificador em inglês. O esforço padrão está na escada do `grok-4.7`. A coluna "com crédito" é a alternativa; sem crédito, ela não é tentada.

| Persona | Tipo | Padrão | Porquê | Com crédito | Limites |
| :------ | :--- | :----- | :----- | :---------- | :------ |
| `planner` | design | `grok-4.7` `high` | esta sessão; `xhigh` é o degrau da policy para architect | `claude-opus-5-5` `high` | não executa passo; não escolhe entre alternativas |
| `implementer` | code | `grok-4.7` `high` | `policy.roles.executor.grok` | `claude-sonnet-5-5` `high` | não edita a norma comum |
| `reviewer` | review | `grok-4.7` `high` | a revisão é camada alta no AGENTS.md | `claude-opus-5-5` `high` | não corrige o que revisa |
| `measurer` | measurement | `grok-4.7` `low` | `policy.roles.consultant.grok`; tarefa mecânica | `claude-haiku-5-5` `low` | não recomenda troca de modelo |
| `researcher` | research | `grok-4.7` `low` | o mesmo papel consultant | `claude-sonnet-5-5` `low` | não decide |
| `operator` | ops | `grok-4.7` `medium` | entre consultant e executor | `grok-4.7` `high` | não edita `brza-workflow` sem passo de plano |

O `operator` com crédito continua em Grok e só sobe o esforço: a tarefa é procedimento, e a família não muda.

### D4 — O ciclo que sugere e não grava — o mesmo resumo (P5)

- **Origem:** R1.3
- **Contexto:** um limiar com número, nesta amostra de uma sessão, seria chute. A forma do ciclo cabe agora; o número que dispara sozinho fica para quando houver notas.

#### Como fica

O `--by-execution` ganha um bloco "sugestão", lido e não escrito. Para cada persona, conta nas notas o `Esforço` (`regulado`, `pouco`, `demais`) e o resultado. A sugestão desce um degrau da escada quando as notas recentes dizem `demais` com resultado `done`. Sobe um degrau quando dizem `pouco`, ou quando o retrabalho da nota aponta contexto faltando. Duas recusas de crédito seguidas mantêm o padrão Grok e deixam a coluna "com crédito" de lado até um launch daquele modelo passar.

O número de notas que arma a sugestão não entra no toml neste plano. O P5 deixa o limite num constante comentado, com o valor inicial 3 para descer e 2 para subir, marcado como hipótese. A R2 troca o número quando houver amostra. O comando não escreve `.brza/personas.toml`. Quem grava é Anderson, na frase da rodada, no mesmo espírito do `Pendente: … · de: Anderson` do PLN-023: a sugestão fica pendente dele.

O relatório roda quando Anderson pedir, e de novo a cada cinco notas novas de feedback. O cinco é a mesma classe de hipótese. A R2 confirma ou troca.

#### Em aberto

- **R2**, os números 3, 2 e 5, depois das primeiras notas. Quem decide já é a R1.3.

## Passos

### P1 — A R1

Executa a entrevista · executor: Anderson

- [x] Responder as quatro perguntas. Resposta em texto livre volta como opção na rodada seguinte. O `D` da pergunta respondida é reescrito no lugar antes de qualquer passo de código.

**Evidência:** Anderson, em 2026-11-14, nesta sessão: "aceitando todas as recomendações", com as quatro frases em R1.1 a R1.4.

### P2 — O gênero da nota e o checador

Executa D2 · executor: sessão no `brza-workflow`

Estimado: 3 h · Executado: — h

- [ ] `work/feedbacks/` em `core/work/README.md` e em `GENRES` / `STATELESS_GENRES` de `core/.claude/skills/notes-checker/scripts/check_notes.py`, com as cinco seções, `model`, `effort` e `result`.
- [ ] Norma e script no mesmo commit do `brza-workflow`, numa branch nova e por PR, como o PLN-024 já manda para código de lá. O trabalho está no [PR 1](https://github.com/brz-anderson/brza-workflow/pull/1) e a prova está em [A execução do P2 do PLN-025 ficou no PR do gênero feedbacks](../../work/worklogs/2026-11-14-pln025-p2-feedbacks.md). O passo segue aberto até o merge. Um caso em `tests/notes-checker/run.py` que falha se a seção some.
- [ ] Desfazer: reverter esse commit. A nota sem seção volta a passar, e o gênero some da tabela. Quem faz é a sessão no `brza-workflow`.

### P3 — O agregador da execução

Executa D1 · executor: sessão no `brza-workflow`

Estimado: 4 h · Executado: — h

- [ ] `--by-execution` em `summarize_measurements.py`, na forma da A1, lendo o jsonl e a nota do gênero que o P2 criou. Campos vazios continuam vazios.
- [ ] Teste em `tests/hooks/test_summarize_measurements.py`: uma linha fixture de turno Claude com custo, e uma nota Grok sem tokens. O esperado está escrito no teste, não calculado pela função.
- [ ] Desfazer: reverter o commit. O resumo volta a não ter o flag.

### P4 — O catálogo e o schema

Executa D3 · executor: sessão no `brza-workflow` para o schema, e sessão neste workspace para o toml

Estimado: 3 h · Executado: — h

- [ ] O schema na norma, no commit do `core/`. O `.brza/personas.toml` neste workspace, com a tabela do D3.
- [ ] Um teste lê o esforço de cada persona e confere com `runtimes.efforts('grok', model)`. Fora da escada, o teste falha.
- [ ] A chave `personas` no manifesto fica citada no schema e só é gravada no toml de um Builder quando o PLN-024 ou o E3 criar esse arquivo.
- [ ] Desfazer: reverter os dois commits. O schema deixa de citar personas.

### P5 — A sugestão de calibração

Executa D4 · executor: sessão no `brza-workflow`

Estimado: 2 h · Executado: — h

- [ ] O bloco "sugestão" no mesmo flag, com as hipóteses 3, 2 e 5 em constante comentada. O comando não abre o toml para escrita.
- [ ] Teste: rodar o flag num workspace fixture deixa `.brza/personas.toml` com o mesmo hash.
- [ ] Desfazer: reverter o commit. O flag volta a só listar execuções.

### P6 — A primeira nota, a desta sessão

Executa D2 · executor: sessão neste workspace

Estimado: 0.5 h · Executado: — h

- [ ] Copiar o exemplo do D2 para `work/feedbacks/2026-11-14-esboco-dos-builders.md`, com o H1 da nota, e passar no checador.
- [ ] Desfazer: apagar a nota no commit seguinte. O exemplo continua neste plano.

## Regressão

- **`--by-workstream` e `--by-task` continuam com a mesma saída** para um log que já passa nos testes de `test_summarize_measurements.py`.
- **Nota antiga continua válida.** A regra nova só olha `work/feedbacks/`. O `tests/notes-checker/run.py` dos casos que já existem permanece verde.

## Worklogs

- 2026-11-14 — R1 enviada, D1–D4 como recomendação, P1–P6 escritos e nenhum executado. Parou na resposta da R1.
  [O PLN-025 do esboço dos Builders foi aberto](../../work/worklogs/2026-11-14-esboco-dos-builders.md)
- 2026-11-14 — R1.1 a R1.4 decididas nas recomendações. D1–D4 fechados. P1 feito. `ready: sim`, `phase: execution`. P2 não começou.
  [O PLN-025 do esboço dos Builders foi aberto](../../work/worklogs/2026-11-14-esboco-dos-builders.md)
- 2026-11-14 — P2 executado no PR 1 do `brza-workflow`, revisado e corrigido. O passo segue desmarcado até o merge.
  [A execução do P2 do PLN-025 ficou no PR do gênero feedbacks](../../work/worklogs/2026-11-14-pln025-p2-feedbacks.md)

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um. Trabalho só em notas de `work/` e `plans/` não tem resumo.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão em `work/decisions/`, a norma do `brza-studio`, o guia.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
