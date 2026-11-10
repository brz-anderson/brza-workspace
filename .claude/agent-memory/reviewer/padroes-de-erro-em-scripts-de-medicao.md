---
name: padroes-de-erro-em-scripts-de-medicao
description: Onde o defeito se esconde nos scripts de agregação e medição (summarize_measurements.py e hooks) — assimetria na resolução de metadados entre sessão corrente e pares, omissão de símbolo monetário, inversão de precedência em fallbacks e testes parciais
metadata:
  type: project
---

Padrões observados na revisão do PLN-012/P2 (2026-11-06, `--by-task` e `--pending`):

- **Inversão de precedência por concatenação não cronológica de listas em fallback de metadados.** Ao tentar herdar
  o `workstream` de eventos pontuais (`task`) quando as linhas contínuas (`turn`) não o possuem, concatenar
  `workstreams = rows_ws + tasks_ws` e pegar `workstreams[-1]` faz com que qualquer commit de tarefa anterior apareça
  após todas as linhas no array, sobrescrevendo turnos mais recentes caso a sessão tenha operado em mais de um workstream.
  *Cheque:* fallback deve ser condicional (`if rows_ws: return rows_ws[-1]`), e não concatenação cega com índice `[-1]`.
- **Helper extraído aplicado apenas no ponto que motivou a correção, esquecendo outras tabelas da mesma entidade.**
  A função helper `session_workstream` foi introduzida para corrigir a resolução de pares no `--pending`, mas a Tabela 3
  de sessões (`aggregate_by_task`) continuou extraindo `workstream` apenas diretamente das rows da sessão, deixando sessões
  com commits no workstream como `(sem workstream)` e descartando-as silenciosamente sob `--workstream <nome>`.
  *Cheque:* após extrair helper de resolução de metadados, fazer busca em todo o arquivo por expressões equivalentes.
- **Assimetria na resolução de metadados entre a entidade corrente e seus pares.** Ao filtrar ou agregar entidades
  relacionadas (como as "outras sessões" em `--pending`), o script resolveu `workstream` para a sessão atual buscando
  em todos os segmentos e eventos `task`, mas para as outras sessões buscou apenas nas linhas do segmento aberto
  (`theirs[-1]["rows"]`). Se o segmento aberto de outra sessão não tiver o campo `workstream` explícito nas linhas,
  a sessão é descartada silenciosamente mesmo tendo histórico rico de tarefas no mesmo workstream.
  *Cheque:* verificar se funções que filtram pares usam o mesmo critério de resolução de contexto usado para a entidade sob foco.
- **Omissão de símbolo monetário em interpolações secundárias.** Ao formatar múltiplos custos na mesma frase
  ("US$ X dos turnos e Y de N subagentes"), o prefixo de moeda foi omitido no segundo valor.
  *Cheque:* validar todas as strings interpoladas voltadas ao usuário com valores compostos.
- **Teste de regressão que esquece uma das visões do comando.** O plano prometia que o relatório padrão, o
  `--by-workstream` e o `--facts` ignoravam eventos novos (`task` e `run`). O teste cobriu os dois primeiros, mas
  esqueceu a asserção sobre o terceiro (`aggregate_facts`).
  *Cheque:* mapear cada visão mencionada na seção de Regressão do plano contra as asserções do teste de regressão.
- **Delta diferencial com base arredondada gerando pico falso de métrica cumulativa.** Ao subtrair uma base salva arredondada
  (`round(base, 4)`) de um float contínuo (`r[key]`), se o processo não gastou CPU no turno, `d = r - base` pode resultar
  em epsilon negativo (`-0.00001`). Uma checagem de fallback ingênua `d if d >= 0 else r[key]` cai no `else` e atribui
  todo o tempo acumulado do processo (`r[key]`) a um único turno.
  *Cheque:* em métricas de delta com chave de processo idêntica (`start`), `d < 0` deve ser limitado a zero (`max(0.0, round(d, 2))`), e nunca retornar o acumulado global.
- **`re.match` em tags XML com ordem variável no transcript.** Em comandos customizados ou skills invocadas via slash
  command (`/plan-runner`, `/close-task`), o Claude Code grava `<command-message>` antes de `<command-name>`.
  Usar `re.match` em vez de `re.search` falha silenciosamente e trata o comando como prompt do usuário, poluindo o `prompt_head`.
  *Cheque:* usar `re.search` ou validar se as tags XML da mensagem podem ser precedidas por outras marcas.
- **Mensagens de sistema no transcript como `type: "user"`.** Mensagens como `<system-reminder>` chegam sem `origin`
  e sem `isMeta`, precisando de filtragem explícita na tupla de mensagens ignoradas (`NOT_A_REQUEST`) para não incrementarem
  contadores de pedidos ou gerarem falsas esperas (`waits_s`).
  *Cheque:* buscar em transcripts reais todas as variações de conteúdo que chegam como `type: "user"` sem ação do usuário.
- **Validação permissiva em regex casada com construtor rígido causando exceção na leitura.** Em parsers de carimbos
  parciais (ex.: `HH:MM` em `until`), regexes que aceitam valores fora de faixa (`\d{1,2}:\d{2}` casando `"25:00"`)
  passam strings que quebram construtores estritos (`stamp.replace(hour=25)` lançando `ValueError`). Mesmo que a camada
  de gravação valide antes de salvar, linhas corrompidas ou antigas no log derrubam a agregação inteira.
  *Cheque:* em leitores de logs tolerantes a falha, operações de substituição/conversão devem conter tratamento de
  `ValueError` com fallback transparente ao carimbo original da linha.

Padrões da revisão final do PLN-012/P4 (2026-11-06, `brza-run` grava a linha `run`):

- **Isolamento parcial do passo da medida.** O contrato "a medida nunca muda o resultado do comando" foi cumprido peça
  a peça (`except Exception` no `find` e no `workstream_of`, `except OSError` na escrita), mas os *argumentos* da
  chamada — `record_run(..., Path.cwd(), provider_session(chat))` — são avaliados fora de qualquer `try`: o `Path.cwd()`
  depois de um comando que apagou o cwd levanta `FileNotFoundError`, e o `provider_session` só pega `BrzaError`
  enquanto o `send_to_chat` irmão, sobre o mesmo `rpc`, pega `(OSError, ValueError, KeyError, BrzaError)`.
  *Onde se esconde:* na linha que chama a função protegida, e no `except` estreito da cópia de helper.
  *Cheque:* listar cada expressão avaliada entre o fim do comando e o `return`, e para cada uma o que levanta; comparar
  o `except` com o da chamada irmã ao mesmo RPC. Sondar com script em `/private/tmp` (runtime file sem `authToken`,
  comando que faz `rmdir` do cwd). Dei 90.
- **Cópia de helper que diverge no mesmo PR.** A correção do `result` nulo (`(found or {})`) entrou só na cópia do
  `brza-run`; o original no `brza-sessions` segue com `found.get`. Ao ver "cópia em vez de import", conferir as duas
  versões linha a linha no commit final.
- **Desvio deliberado sem teste que o prenda.** A CPU como diferença antes/depois do `getrusage` sobreviveu à mutação
  "só o depois" (38 OK): o teste só tem piso (`>= 0.25`), sem teto. Para desvio declarado pelo executor, mutar o
  desvio de volta ao Desenho e ver se algum teste cai.

- **Na conferência da correção, o `except` ampliado cobre só a chamada, e não o pós-processamento.** No `aa752e6`, o
  `AttributeError` entrou no `except` do `rpc`, mas o `.get` do `providerSession` ficou depois do `try`. Não entrou como
  achado, porque o app sempre dá um objeto (`acp-conversation-copy.ts:72`). Na conferência, olhar a linha depois do `try`.

Padrões da rodada final do PLN-012/P2 (2026-11-06, Opus depois de três rodadas do Gemini Flash, que não os viu):

- **Teste com o nome da regra cuja fixture dá o mesmo resultado pelos dois ramos.** O teste "o subagente vai ao turno que
  contém o começo dele, ou ao segmento pelos marcos" pôs todo subagente num turno que fica do mesmo lado do marco: o
  mutante sem a busca do turno (`inside = None`) passou nos 71 testes. *Cheque:* mutar o ramo (script em
  `/tmp/pln012-p2/opus/mutate.py`) e exigir um caso em que os dois ramos divergem (turno que contém o commit e
  subagente que começa depois do marco). Confiança que dei: 95, verificada por mutação.
- **Fronteira de intervalo sem teste no ponto exato.** `bisect_left` × `bisect_right` (o turno que começa no marco)
  passou nos dois sentidos; e o Desenho mudou a fronteira de `(k−1, k]` para `[k−1, k)` durante a execução paralela
  (X2), deixando o código fora do contrato sem nenhum teste acusar. *Cheque:* em toda janela por marco, um caso com o
  valor igual ao marco; e reler o Desenho no `git log` do workstream antes de devolver.
- **Saída com resolução menor que a entrada que o passo seguinte pede.** O `--pending` mostra `HH:MM`, e a skill manda
  usar a hora ISO com segundos quando dois turnos começam no mesmo minuto: o agente não tem de onde tirar o segundo.
  *Cheque:* seguir cada número impresso até o comando que o consome.
- **Contexto resolvido só pelo histórico do log, sem o caso "primeira vez".** A sessão cujo único turno está em curso
  não tem linha no log, e o `--pending` perde o workstream e a linha das outras sessões (45 de 133 sessões reais têm um
  turno só). *Cheque:* rodar a função com a entidade ausente do log.
- **"Sai 0 sempre" quebrado pela validação do argparse** com a variável de ambiente vazia (`--session ""` → saída 2).

- **Conserto de data que compara os itens entre si, e não com o "hoje" de quem consome.** O `dd/mm` do `--pending`
  só aparece quando a lista tem mais de um dia; a lista toda de ontem sai em `HH:MM`, que o `--until` lê como hoje.
  *Cheque:* no conserto de formato de hora, testar a lista inteira de um dia que não é o de `now`.

Padrão da revisão do PLN-012/P7 (2026-11-09, suíte que grava no log real):

- **O teste vaza para o log real quando o stub não pega.** Achar a origem do vazamento pelo próprio log: agrupar as
  linhas suspeitas por `cwd`, `chat_id` e `worklogs` e procurar o nome do worklog ou o id (`claude_x`) em `tests/` —
  levou direto ao `test_migrate_pln008` (o `ng['commit']` chamado fora do `chdir`, daí o `cwd` no repositório) e ao
  teste do `main` do `brza run`. A limpeza do X9 tirou só `task`; as linhas `run` falsas ficaram.
  *Cheque:* rodar a suíte numa cópia sem `.git` com `BRZA_WORKSPACE` apontando um workspace de mentira, e provar o
  detector com o mutante sem a limpeza (que gravou 6 `task` lá). Nunca rodar com o ambiente da sessão no log real.
- **Parser de cerca escrito à mão com as regras de fechamento sondadas só à mão.** O `without_cost_section` fecha a
  cerca pelo caractere, pelo comprimento e sem info string, mas o teste só tem a cerca simples: o mutante "toda cerca
  alterna" (o modelo do `check_notes.py`) passou nos 108 e corta o worklog dentro de ```` ```python ```` aninhado.
  Também: cerca que não fecha, ou ```` ```x``` ```` na linha, esconde a seção e ela duplica a cada commit.
  *Cheque:* sonda com lista, citação, indentação de 4, aninhada, til em crase e cerca aberta; depois o mutante toggle.
  Dei 90 ao teste fraco.

**Why:** são defeitos reais que passam em testes unitários quando as fixtures fornecem sempre os dados no cenário ideal.
**How to apply:** em revisões de scripts de sumarização, rodar testes adversários com linhas parciais (sem workstream nas rows) e inspecionar a saída formatada de cada flag.
Relacionado: [[achados-que-costumam-cair]].

Padrões da revisão da entrega do PLN-012 (2026-11-09, o plano inteiro):

- **Campo do evento com o processo errado.** O `task` grava `'pid': os.getpid()`, o do `brza-note`, enquanto o
  exemplo do D1 traz o pid do `claude` (o mesmo da `CLAUDE_PID` no Terreno). Nenhum leitor usa o campo, e por isso
  nenhum teste caiu. *Cheque:* para cada campo de identidade num evento (`pid`, `session_id`, `cwd`), comparar o valor
  gravado no log real com o da linha `turn` da mesma sessão. Dei 88.
- **Duas regras de formato na mesma linha.** A `## Custo da tarefa` formata a CPU do `brza run` pelo `human_duration`
  ("CPU 2 min") e a do `claude` com `f'{x:.2f} s'` ("1089,43 s"); o D3 manda segundos só abaixo de 1 min. O teste fixa
  o formato errado (`'CPU 0,80 s'`). *Cheque:* ler a linha gerada no worklog real, com números grandes. Dei 82.
- **Título renomeado sem a skill citar o antigo.** O comando corta nos dois títulos, mas o `close-task` só manda
  acrescentar "acima da `## Custo da tarefa`"; nos worklogs do dia com `## Medida`, o acréscimo no fim se perde no
  próximo commit. *Cheque:* `git grep` do título antigo nas branches `workstream/*` com a data de hoje. Dei 85.
