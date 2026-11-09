---
name: achados-que-costumam-cair
description: Hipóteses de revisão que pareciam achado e caíram ao verificar — limiar "sem lastro" que está no texto da opção, terreno que existe, despacho brza que funciona
metadata:
  type: feedback
---

Hipóteses que caíram na revisão do PLN-009 (2026-11-03), com a confiança que eu teria dado sem verificar:

- **"Limiar sem lastro" que está no texto da opção recomendada** (~90 antes de ler): o 55%/90% vinha da opção da R7.1
  ("55% e 90%, como no `quota.py`"), e a linha "Decidido" não repete o número. Ler a opção inteira, não só o "Decidido".
- **"Endpoint ou comando não existe"** (~70): `/v1/systemone` respondeu 400 "model is required" sem carregar modelo;
  `orca account list --json` traz `usedPercent`/`resetsAt`. Sondar com chamada barata antes de afirmar.
- **"`brza <sub>` não chega ao `brza-<sub>`"** (~75): o `brza` do PATH é o shim do BrzA Studio, que despacha; o
  "Unknown command" só aparece quando o `brza-<sub>` não existe. Teste com um `brza-*` que existe (`brza where --help`).
- **"`KeepAlive: {'SuccessfulExit': False}` faz o launchd reiniciar serviço após `bootout`"** (~80): o `bootout`
  descarrega o job da tabela do launchd; o KeepAlive só opera enquanto o job estiver carregado.
- **"Apagar o plist antes de descarregar quebra o `launchctl bootout`"** (~85): o `bootout` recebe o identificador lógico
  do serviço (`target()`, `gui/<uid>/<label>`), e não o caminho físico do arquivo plist.


- **"O teste passa sem a espera"** (~70, P8 do PLN-009): o `assertGreaterEqual(prints, 4)` parecia frouxo, mas o
  `assertFalse(is_loaded())` logo depois barra; a mutação sem o laço falhou em 3 testes. Mutar antes de afirmar.
- **"Teste novo de regressão deve falhar contra o código antigo"** (~80 antes de verificar, R2 do P8): quando o teste cobre
  guarda contra mutação em funcionalidade nova (ex.: não mencionar plist no CLI sem plist órfão) ou comportamento que o
  código anterior já fazia por outro motivo (reter plist em erro genérico de bootout), ele passa no código antigo e só falha
  contra o mutante do código novo. Provar a guarda por mutação na implementação nova, e não esperar falha no código antigo.

Hipóteses que caíram na revisão do PLN-012/P1 (2026-11-06, esperas, prompt_head e máquina no hook):

- **"Offsets ou padding errados no struct ctypes de rusage_info_v4"** (~85 antes de checar): `ri_uuid[16]` ocupa 16 bytes e
  os 12 uint64 seguintes coincidem exatamente com múltiplos de 8 bytes no LP64; o buffer `_rest` (624 bytes) acomoda com
  folga os 296 bytes escritos pelo kernel no flavor 4.
- **"Escala errada no mach_timebase_info em Apple Silicon"** (~80): em Apple Silicon o timebase é 125/3 ns (24 MHz); a divisão
  `numer / denom / 1e9` converte os ticks diretamente para segundos, batendo com `time.process_time()` na razão 0.99.
- **"Leitura de máquina dentro do state.json segura a trava excessivamente"** (~75): `claude_pid()` sobe os PPIDs fora da trava;
  dentro do `State` roda apenas a chamada C direta do `proc_pid_rusage`, em microsegundos.
- **"Pergunta recusada perde a espera"** (~80): o `is_error` só é checado na contagem de rounds; a espera é coletada pelo
  `tool_use_id in asked_at` independente do status de erro.
- **"Mensagens user vazias inflam contagem de requests"** (~75): em 200 transcripts reais do Claude Code há 0 ocorrências de
  mensagens `user` com `content` vazio ou sem texto/tool_result.
- **"O teste novo não é TDD / já passava antes da implementação"** (~80 antes de verificar, P5 do PLN-012): o checador não restringe
  chaves de frontmatter (F26) e o worklog já passava no checador, mas as asserções de conteúdo (`read_core()`) no mesmo teste barravam
  antes da norma, da skill e do adaptador. Avaliar a suíte do teste por inteiro e suas asserções de conteúdo, não apenas o comportamento
  da ferramenta sob teste.
- **"Texto de skill diverge do Desenho por conter regras omitidas no D específico"** (~85 antes de verificar, D6 do PLN-012): as adições
  ("Sem CLAUDE_CODE_SESSION_ID no ambiente, o passo não se aplica", "A ## Medida não se escreve à mão") decorriam diretamente de outros
  Ds do mesmo plano (D1 e D3) para evitar que agentes emitissem comandos inválidos ou inventassem seções. Checar os contratos globais do
  plano antes de acusar divergência.
- **"Rollover de `--until HH:MM` para commit após meia-noite joga o marco para o futuro"** (~85 antes de verificar, P2 do PLN-012):
  o Desenho D1 restringe o formato `HH:MM` expressamente ao "dia de hoje, no fuso local" e determina que o commit seja recusado antes
  se a hora cair fora da janela (entre marco anterior e agora); para horas do dia anterior a regra exige hora ISO completa, que o parser
  já trata. Conferir as regras de validação do comando que grava a flag antes de supor entrada arbitrária no leitor.
- **"`until` com hora inválida (ex.: `99:99`) causando `ValueError` em `stamp.replace` no `task_mark`"** (~85 antes de conferir):
  o comando `brza note commit` valida expressamente a hora informada contra a janela e a sintaxe de hora válida antes de registrar
  o evento `task` no log; valores fora do padrão ou inválidos são recusados antes do commit tocar o repositório.
- **"Generalização de encadeamento com `--until` para 3+ tarefas diverge do Desenho"** (~85 antes de conferir, P5 do PLN-012):
  o D6 formulava a regra com "mais de uma tarefa" e usou 2 apenas no exemplo concreto; a repetição da mais antiga para a mais nova
  preserva a semântica de janelas `(marco k-1, marco k]` do D1.
- **"Divergência de caminho entre `core/CLAUDE.md` e fixture golden (`tests/hooks/` vs `.claude/hooks/tests/`)"** (~85 antes de checar):
  diferença intencional entre o repositório fonte (`brza-workflow`) e o consumidor (`brza-workspace`), mapeada explicitamente nas
  exceções de `golden_differences.py`.
- **"`<system-reminder>` atualiza `last_talk` e encurta a espera de Anderson se injetado em período ocioso"** (~80 antes de verificar, R2 do P1):
  em transcripts reais, o reminder só chega com `isMeta: true` ou colado no mesmo timestamp do comando; atualizar `last_talk` em
  `kind in ('user', 'assistant')` é requisito indispensável para que `[Request interrupted by user]` fixe o momento exato da interrupção.
- **"Discrepância de separador decimal entre números na mesma ferramenta (ponto vs vírgula)"** (~80 antes de verificar, R3 do PLN-012/P2):
  o D3 e o D6 estipulam vírgula decimal expressamente para a prosa voltada ao usuário no terminal e no worklog (`brl()`), enquanto tabelas
  do CLI e agregações mantêm o padrão numérico pré-existente do script (`usd()` com ponto). Checar se a convenção de localização do projeto
  distingue tabelas de prosa antes de apontar inconsistência.
- **"Eventos secundários (`subagent`, `run`) sem sessão casada ou órfãos corrompem a agregação de sessões"** (~85 antes de verificar, R3 do PLN-012/P2):
  o `task_segments` isola eventos desprovidos de sessão no segmento aberto de `sid = None`, que não possui `turns` e é formatado como
  `(sem sessão)` sem corromper a ociosa ou os turnos pendentes de sessões ativas.

Hipóteses que caíram na revisão final do PLN-012/P4 (2026-11-06, `brza-run` mede):

- **"O `X | None` novo quebra o `brza-run` no Python 3.9 do macOS"** (~80): o `brza_runtime.py:31` já tinha
  `Path | None` no import; o CLI exige 3.10 pelo README:27. Conferir o que o arquivo já importava antes do diff.
- **"O `zsh -ic` infla a CPU e a duração do comando"** (~75): o `run_here('true')` com o `.zshrc` real dá 0,04 s de CPU
  e 5 MB. Medir antes de afirmar overhead.
- **"O ▶ acha o workspace errado pelo `Path.cwd()`"** (~70): o app abre a aba com `startupCwd: context.worktreePath`
  (`brza-studio/src/renderer/src/components/native-chat/brza/BrzaRunCodeButton.tsx:32`); o defeito real era o *momento*
  da leitura (depois do comando), e não a escolha.
- **"A diferença do `RUSAGE_CHILDREN` é desnecessária"** (~70): no processo real, o import do `brza_runtime` já colheu
  filhos `git` (0,012 s, 4,7 MB) antes do `pty.spawn`; a diferença é a forma certa, só sem teste.

Hipóteses que caíram na rodada final do PLN-012/P2 (2026-11-06, Opus):

- **"A tarefa chaveada só pelo caminho do worklog funde worklogs de workstreams diferentes"** (~80): 0 nomes repetidos
  entre os 165 worklogs de todas as `workstream/*`; a data e o slug no nome bastam hoje.
- **"O relatório padrão, o `--by-workstream` ou o `--facts` mudam com `task` e `run` no log"** (~75): a saída do CLI,
  menos o cabeçalho, sai igual nas três visões.

Hipóteses que caíram na revisão do `fix/brza-run-argv` (2026-11-09):

- **"O `argparse` com `nargs=REMAINDER` come o `--` de dentro do comando"** (~70): no 3.9 e no 3.15, só o primeiro
  `--` fica no começo da lista, e o `git log -- f` chega inteiro. Sondar o parser com a lista antes de afirmar.
- **"Algum chamador conta com o contrato antigo de juntar com espaço"** (~70): o ▶ digita o bloco no zsh da aba e o
  despacho do `brza` passa o argv intacto; as linhas `run` da medição e os transcripts só mostram um argumento citado.

**Why:** cada um teria entrado como achado importante e sido refutado pela sessão principal em um comando.
**How to apply:** nesses três formatos, rodar o cheque antes de pôr confiança; o que cair vai como `→ falso`.
Relacionado: [[padroes-de-erro-em-planos-extraidos]].
