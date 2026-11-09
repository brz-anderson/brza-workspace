# PLN-017 — Desenho

## Desenho

### O que este desenho assume

- **R1.1:** o desenho mora aqui; a execução sai por issue para o workstream dono (`workspace`, `tools-kit`, `studio`).
- **R1.2:** as primitivas nascem no `brza sessions`; o MCP embrulha depois.
- **R1.3 e R3.4:** o painel da rodada é um `::orca-visual` gerado pela coordenação; o `orchestration-crew` não se religa (Terreno, F81 a F83).
- **R1.4:** a coordenação narra quem respondeu e quem falta, a posição e a confiança por persona e rodada, e as medições na hora; a argumentação integral fica para a fase do painel.
- **R2:** a skill nasce na branch do `playground`, com oito references e quatro scripts; o revisor é o número da confiança; a contraprova é por gatilho; a rodada final leva o voto e o argumento mais forte a favor e contra por persona.
- **R3:** recibo, `--operation` e `read --last` pelo `rpc` como transição; `wait` por estado, fila e `updatedAt`; latência no mapa e `usage` do Codex; um painel por rodada, republicado durante ela.
- **R5 e R6:** as sessões que a coordenação abre têm o ciclo de vida dos workers do Orca (fechamento ~2 min depois do `worker_done`, botão "manter aberta"); a sonda da híbrida decide entre ela e o `worker-start` puro; o fim de rodada é uma mensagem de mailbox da persona e o `worker_done` vai só no encerramento, então o `wait` vira `check --wait`; os quatro agentes estão em Chat.

### Os itens D

Cada frente num arquivo, pelo teto de linhas do molde; as alternativas e o "Em aberto" de cada um vão às rodadas 2 e 3.

| Item | O quê | Arquivo | Estimado |
| :--- | :---- | :------ | :------- |
| D1 | a skill `meeting-runner`: protocolo, moldes, scripts e as regras de narração | [PLN-017 — Desenho: a skill (D1)](PLN-017-design-skill.md) | ~10,5 h |
| D2 | os verbos do `brza sessions` (`open --model`, `send` a N com recibo, `wait`, `model`, `usage`, `close --prefix`), a medição por runtime e o `brza shot` | [PLN-017 — Desenho: as primitivas do `brza sessions` (D2)](PLN-017-design-cli.md) | 14,5 h, com a sonda e a via A (P4a 10 h, P4b 3,5 h, `brza shot` 1 h) |
| D3 | o painel da rodada como `::orca-visual`, o `estado-rN.json` e o gerador | [PLN-017 — Desenho: o painel da rodada (D3)](PLN-017-design-painel.md) | 6 a 6,5 h |

### Terreno

Consolidado em 2026-11-08 a partir de cinco levantamentos de `collector` (ferramental, Studio, protocolo e medições, narração dos dois chats, planos vizinhos) e da investigação do painel `orchestration-crew`; os agregados ficaram no scratch da sessão, fora do git. Cada fato leva a marca de evidência e confiança do papel; os de confiança 80 a 89 vêm transcritos dos levantamentos sem reabrir a fonte primária. Siglas de caminho: `B/` = `.sessions/reuniao-brasa/`, `M/` = `.sessions/reuniao-mcp-remoto/`, `coordB` = `work/worklogs/2026-11-07-reuniao-carvao-em-brasa-coordenacao.md`, `coordM` = `work/worklogs/2026-11-07-reuniao-mcp-remoto-coordenacao.md`, `issue` = `work/issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md`.


#### As duas reuniões: protocolo e o que a segunda corrigiu e perdeu
- **A reunião M copiou o fluxo da B com 17 passos comuns.** `B/briefing.md:13-14`, `M/briefing.md:6-11` — briefing, personas, 6 sessões em paralelo, rodadas com marcador, síntese, proposta, revisor, rodada de decisões, issues. [F1 · lido · 90]
- **Só a M guardou o pedido à própria coordenação.** `M/prompt-coordenacao.md:1-22` — manda delegar o levantamento ao `collector`, ter revisor independente e fazer prova de conceito. A B não tem esse arquivo. [F2 · lido · 90]
- **O marcador de fim tem regra única na M.** `M/briefing.md:64-65` — acrescenta no fim do arquivo, e a última linha é `<!-- fim-rodada-N -->`. Na B o briefing dizia "dentro de `## O que se fez`" (`B/briefing.md:90-91`) e o pedido da R1 dizia "antes de `## O que ficou`" (`B/rodada-1.md:8-9`). [F3 · lido · 95]
- **Três personas da B puseram o marcador nos dois lugares.** `issue:23-24,57-58`; `coordB:134-135` — hoje os arquivos finais da B não mostram mais a duplicidade (conferido por `tail -1` e `grep`). [F4 · rodado · 90]
- **A M gravou modelo e esforço por papel desde a abertura.** `M/launch.py:1-21`; `M/prompt-coordenacao.md:10` — na B isso veio só depois, por pedido de Anderson às 20:43 (`coordB:139-144`). [F5 · lido · 95]
- **A M exigiu evidência medido, lido ou suposto.** `M/briefing.md:62-63` — a B pedia só "mediu ou leu" (`B/rodada-1.md:16`). [F6 · lido · 95]
- **A M perdeu três passos da B.** Contraprova às cegas em outros modelos (`B/contraprova-1.md:3`; `coordB:137-184`), rodada "mão na massa" (`B/rodada-4.md:21-41`) e voto apoio, ressalva ou contra (`B/rodada-3.md:12-18`; a M trocou por confiança por parte do plano em `M/rodada-3.md:11-17`). [F7 · lido · 95]
- **A pergunta-alvo da M ficou ambígua e custou quatro rodadas.** `M/rodada-5.md:3-9`; `coordM:30-37` — o briefing falava "MCP" e listava `context7`, `brza-quota` e Studio. Às 21:35:56 Anderson corrigiu para o MCP do `brza-workflow` e as rodadas 1 a 4 foram descartadas. [F8 · lido · 95]
- **O `sessions.jsonl` não registra envio nem fim de turno.** `.sessions/sessions.jsonl` na raiz do repositório — eventos: open 91, session 80, close 4, title 1. A latência por rodada só sai de marcador, de `turn.duration_s` (Claude) e dos rollouts do Codex. [F9 · rodado · 95]
- **O revisor independente ficou abaixo da sala nas duas.** B: 74 contra 85,8 na v3 (`coordB:128-130`). M: 45 contra 61,8 na v1 e 68 contra 64,75 na v3 (`coordM:296-303`). [F10 · lido · 95]
- **O Antigravity foi o mais confiante e o de evidência mais fraca nas duas.** `issue:29-30,43-46,62-63` — na contraprova, Fogareiro foi de 89 para 67 ao sair do Gemini 3.8 Flash (High) para o Haiku `low` (`coordB:172-175`). [F11 · lido · 95]
- **O Grok atrasou a B.** `issue:25-26`; `B/sintese-2.md:3` — 7 min por rodada (`xhigh`), uma rodada atrás; a síntese 2 "entrou pela R1". [F12 · lido · 95]
- **A cota do Codex acabou no meio da M.** `coordM:117,167-169` registra 21h41. O rollout em `~/.codex/sessions/2026/11/07/rollout-2026-11-07T21-19-25-*.jsonl` mostra o primeiro erro de limite às 21:37:11 (Régua) e 21:37:15 (Atalho), e 21:41:45 no `codex exec`. As duas personas perderam as rodadas 5 e 6. [F13 · rodado · 90]
- **As personas Grok gravaram memória fora do repositório.** `~/.grok/memory-v2/workspaces/brza-workspace-34595849/topics/` — `reuniao-carvao-faisca.md`, `carvao-em-brasa-rodada-1.md`, `carvao-contraprova-faisca.md`, `reuniao-mcp-remoto-salto.md`, embora o briefing mande escrever só no próprio worklog (`B/briefing.md:84-87`). [F14 · rodado · 90]
- **A média "nota dos colegas" da B só bate sem a nota da Faísca.** `coordB:97-102` — Tição 8,9 contra 8,5 com ela, Fogareiro 6,25 contra 6,6, Fole 8,25 contra 8,4. A ordem não muda. Premissa: a R3 da Faísca chegou depois da conta. [F15 · rodado · 85]

#### O que custou e o que se mediu
Custo em US$ pelo `estimated_cost_usd` do hook, `workstream: playground`, 2026-11-07, sessão de coordenação e subagentes (`/private/tmp/wf-improv/processo/agrega.py`, saída em `agrega-saida.txt`). Só Claude. [F16 · rodado · 90]

| Item | Reunião B (Carvão) | Reunião M (MCP remoto) |
| :-- | --: | --: |
| Coordenação (Opus 5.5; B xhigh, M high) | 22,67 | 6,03 |
| Revisor (subagente `reviewer`, Opus 5.5) | 3,84 | 2,39 |
| `collector` | 0 (material do PLN-007) | 0,36 (Sonnet 5.5) |
| Personas Claude na reunião | 6,74 (Tição 3,61, Fole 3,13) | 1,86 (Muralha 1,70, Plantão 0,16) |
| Contraprova Claude | 3,51 (Fable 3,07, Sonnet 0,41, Haiku 0,03) | não houve |
| Total medido | 36,76 | 10,64 |

- **A coordenação pesa mais que todas as personas juntas.** B: 22,67 de 36,76 (62%) em uma sessão. M: 6,03 de 10,64 (57%). [F17 · rodado · 85]
- **A mesma sessão de coordenação continuou em 2026-11-08.** M: +US$ 6,22 (turno de 68 570 s esperando Anderson, 6,04). B: +3,79 em cinco turnos. Fora da tabela. [F18 · rodado · 90]
- **A tabela acima não inclui US$ de Codex, Grok e Antigravity.** Isso é limite da coleta, não prova de ausência de custo em disco. Tokens de entrada do Codex: B 4,63 M, 5,74 M, 0,65 M, 0,44 M; M 2,60 M e 1,37 M, lidos do último `token_count.total_token_usage` do rollout. O Grok tem `costUsdTicks` em `usage.json` (F20); as reuniões B/M não foram recalculadas nesta correção. [F19 · corrigido em 2026-11-09 · rodado · 90]
- **Grok grava tokens e custo por sessão e turno.** Conferido em `~/.grok/sessions/%2FUsers%2Fandepb%2FProjects%2Fbrza-workspace%2F.worktrees%2Fplayground/01a1c119-2faf-71f0-9d21-dfd87c062873/usage.json`: `session.inputTokens=2632760`, `outputTokens=24264`, `costUsdTicks=18738880000`; os quatro itens de `turns[]` somam os mesmos totais. A escala informada pelo levantamento é 10^10 ticks/US$ (US$ 1,873888 neste exemplo), ainda a conferir no produtor. A afirmação anterior de ausência de tokens do Grok era falsa. Antigravity não foi reconferido. A integração da leitura e a agregação de subagentes ficam na [O custo e os tokens do Grok entram nas medições da reunião](../../work/issues/custo-e-tokens-do-grok-nas-medicoes-da-reuniao.md). [F20 · corrigido em 2026-11-09 · rodado · 95 para os campos e somas]
- **O revisor ao custo de US$ 2,4 a 3,8 muda o número.** Haiku `low` na contraprova custou US$ 0,03 e achou um erro real; Fable `high` custou US$ 3,07, três vezes o Opus `high` na R1 (2,18 contra 0,74). [F21 · rodado · 90]
- **Sem medição:** latência de envio, latência de Grok e Antigravity, custo de Codex em US$, modelo das seis personas da B no mapa (`sessions.jsonl` de 20:00:53 não grava `model` nem `effort`). [F22 · rodado · 90]

#### A narração em chat das duas coordenações
Fonte: transcripts `4cbdb093-…jsonl` (B) e `21c30e73-…jsonl` (M), por `/private/tmp/wf-improv/chat/comparacao.md`. A classificação por tipo é manual, sem dupla leitura. [F23 · rodado · 80]

| Contagem | Carvão | MCP |
| :-- | --: | --: |
| Blocos de texto ao chat | 57 | 47 |
| Caracteres | 33.587 | 13.398 |
| Mediana de caracteres | 119 | 113 |
| Blocos com menos de 200 | 50 | 41 |
| Blocos que nomeiam persona | 11 | 4 |
| Blocos de síntese (caracteres) | 3 (22.355) | 4 (5.945) |
| Blocos de medição da coordenação | 2 | 13 |
| Maior intervalo sem texto | 7m43 | 3m34 |

- **O silêncio não distingue as duas.** `comparacao.md` §1 — nenhuma teve 20 min só de ferramenta; a Carvão teve esperas mais longas (20:12:20 a 20:20:03). [F24 · rodado · 90]
- **Salto e Plantão não aparecem em nenhuma fala da M.** Das seis personas, duas nunca são nomeadas ao chat (`comparacao.md` §2). [F25 · rodado · 90]
- **P1, a persona é o sujeito.** A B abre com quem é quem e o runtime (20:01:02) e lista quem respondeu e quem falta (20:03:03). [F26 · lido · 90]
- **P2, a síntese compara posições.** A B, às 20:43:23, deu 76,7 para 85,8, o revisor em 74 e o comportamento por tipo de persona. A M deu um número agregado (61,8 para 70,0, às 21:35:55) e uma frase. [F27 · lido · 90]
- **P3, o registro vai à resposta.** A B mostrou o worklog em `<details>` com a tabela Rodada, Aberta, Fechada, O que produziu, e a tabela de modelos por persona (20:56:46). A M listou 12 arquivos e escreveu que o worklog "tem ~310 linhas e está no commit". [F28 · lido · 85]
- **P4, o painel visual.** A B escreveu `painel.py` (8.881 caracteres, 20:27:48 a 20:41:21) e entregou um `::orca-visual` com votos 15 propostas por personas, conferido por PNG. A M não gerou visual. [F29 · lido · 90]
- **P5, a pergunta final desenhada.** A B perguntou em texto, com artboards por alternativa e `Custo: … Se paga: …`. A M usou `AskUserQuestion`, quatro perguntas, sem alternativas desenhadas. [F30 · lido · 80]
- **Anderson não escreveu durante as rodadas da B (20:00 a 20:43).** Mensagens dele: 19:55:54 (pedido), 20:43:24 (modelo e esforço por papel). Na M: 21:16:30 (pedido) e 21:35:56 (correção do tema). [F31 · rodado · 90]

#### O `brza sessions` e o `brza agent launch` hoje
- **O `brza sessions` tem 5 verbos.** `brza-workflow/packages/client/bin/brza-sessions:71` — `open` (implícito), `list`, `send`, `title`, `close`. Não há `read`, `wait`, `model` nem `status`. [F32 · lido · 95]
- **O `open` não aceita `--model` nem `--effort`.** `brza-workflow/packages/client/bin/brza-sessions:406-421` e `:456-457` — chama `brza agent launch --agent --surface chat --worktree path:<checkout> [--prompt]`. O `grep -i 'model\|effort'` no arquivo voltou vazio. [F33 · rodado · 95]
- **O `brza agent launch` aceita `--model` e `--effort`.** `brza-studio/src/cli/specs/agent-launch.ts:9,25` — `--effort` exige `--model`; vale em chat e terminal. [F34 · lido · 97]
- **O `launch.py` da M contorna.** `.sessions/reuniao-mcp-remoto/launch.py:9-21` — importa o `brza-sessions`, anexa `--model` e `--effort` e grava ambos no `open`. O `session_map()` os descarta (`brza-sessions:86-111`). [F35 · lido · 95]
- **O `--wait` espera só a abertura.** `brza-sessions:212-250,483-493` — até 60 s pelo `providerSession.id`; não espera fim de turno. [F36 · lido · 96]
- **O `send` é posicional, sem recibo e sem dedup.** `brza-sessions:341-346,379-382`; `brza-workflow/bin/brza_runtime.py:130-145` — responde `{"sent": true}` sempre, `delivery: 'queue-if-active'`, `clientOperationId` novo a cada chamada. A mensagem chegou ~12 min depois na virada de turno (`M/proposta-v2.1.md:23,115`). [F37 · lido · 95]
- **A mensagem chega como da pessoa sem `ORCA_AGENT_SESSION_ID`.** `brza_runtime.py:87-97` — a evidência de origem só anexa se a variável existir no chamador. [F38 · lido · 94]
- **O `list` não traz agente, modelo, custo nem último texto.** `brza-sessions:50-51,293-310` — o único sinal de fim de turno é `state` (`:307`, `:360`). [F39 · lido · 95]
- **O `brza chat read` não existe no `brza` instalado.** `brza chat --help` → "Unknown command: chat". Existe `brza orchestration worker-read`, só para workers de `worker-start`. [F40 · rodado · 93]
- **O app tem RPC `agentSession.setOption`, fora do CLI.** `brza-studio/src/shared/rpc-contract/structured-agent-session-params.ts:205-209` — que a chave seja `model` ou `effort` é inferência (`agent-session-options-result.ts:13`). [F41 · lido · 82]
- **O `brza shot` não roda contra o Studio atual.** `brza-studio/src/shared/native-chat/native-chat-visual-shell.ts:106` agora é `const BASE_CSS = visualBaseCss(true)`; o `string_concat` de `scripts/brza/brza-shot:162-166` só entende literais. Não rodei o `brza shot`. [F42 · lido · 85]

#### O orquestrador MCP
- **Três ferramentas.** `brza-workflow/packages/mcp/brza_mcp/tools.py:540-545` — `dispatch`, `status`, `config`. [F43 · lido · 98]
- **O `dispatch` abre um worker por chamada, sem nome, título, checkout nem `keep_open`.** `tools.py:30-35,230-290` — `task` e `role` obrigatórios; `target` é gravado (`queue.py:23,29`) mas `cycle.py` não o usa. [F44 · lido · 95]
- **O worker dura uma tarefa e não recebe segunda rodada.** `brza-workflow/packages/mcp/brza_mcp/cycle.py:44-49,111-117,136-167,188-199` — `run-create`, `task-create`, `worker-start`; fim por consulta a cada 15 s; não passa `--worktree`, `--keep-open`, `--name`, `--surface`. [F45 · lido · 88]
- **Só o papel `consultant` entra sem gate.** `tools.py:343-346,356-435` — `executor` e `architect` devolvem gate e esperam `approved`. Seis personas de outro papel são seis aprovações. [F46 · lido · 95]
- **A política vence o modelo pedido.** `brza-workflow/packages/mcp/brza_mcp/policy.py:22-23,30-41,231-274` — com `policy.enforce` (padrão true), a linha do papel manda; as linhas `policy.roles.*` só mudam por `brza.toml` (`:53-68,94-122`). [F47 · lido · 93]
- **O `status` não traz texto, tokens nem latência do worker.** `tools.py:456-501`. A telemetria `route` guarda decisão, modelo, esforço e conta, sem tokens (`telemetry.py:78-106,120-159`). [F48 · lido · 96]
- **Não há reencaminhamento entre runtimes.** `tools.py:294-341`; `accounts.py:115-124` — a troca de conta é global, gated e só do Codex. [F49 · lido · 90]
- **Um client fora do Studio precisa falar MCP HTTP com Bearer.** `tools.py:195-199,242-247`; `cli.py:132-134`; `cycle.py:105-109` — o ciclo só sabe falar com BrzA Studio ou Orca. [F50 · lido · 92]
- **O `brza orchestration worker-start` aceita `--model` e `--effort`.** `worker-start --help` — o modo (chat ou terminal) "follows the user's own setting; there is no flag". [F51 · rodado · 95]

#### A medição por runtime
- **O `measure.py` só lê transcript do Claude Code.** `brza-workflow/core/.claude/hooks/measure.py:1-23,437-439,507` — `grep -ci "codex|grok|antigravity"` dá 0. [F52 · rodado · 95]
- **Ninguém no `brza-workflow` lê o rollout do Codex.** `grep -rn "token_count|codex/sessions" --include='*.py'` fora de worktrees e testes: vazio; o custo do Codex foi extraído à mão. [F53 · rodado · 90]
- **A latência do pedido ao MCP sai por diferença de timestamps da telemetria `route`.** `admitted` e `done` ou `failed`; o `summarize_measurements.py:136,175-180` conta decisões e não calcula a latência. [F54 · lido · 88]
- **O PLN-012 deixou Codex e Antigravity fora da medida por tarefa.** `workstream/tools-kit:plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md:57-58,118-121` — opção recusada por custo de 6 h ou mais; Grok em issue própria. [F55 · lido · 90]

#### O chat e os painéis do Studio
- **A origem da mensagem é um contrato fechado.** `brza-studio/src/shared/agent-session/agent-session-message-source.ts:12-19,56-62,126` — `relation: 'worker' | 'coordinator' | 'none'`; não há campo de rodada, confiança nem persona. [F56 · lido · 95]
- **O cabeçalho do cartão deriva da origem.** `brza-studio/src/shared/agent-session/agent-message-presentation.ts:12-19,39-61` e `brza-studio/src/renderer/src/components/native-chat/NativeChatAgentMessageCard.tsx:30-58` — "Task from coordinator", "Update from worker", "Hand-back from". [F57 · lido · 95]
- **Há um ponto de extensão para origem estranha ao Orca.** `brza-studio/src/shared/native-chat/brza/brza-claude-peer-sender.ts:9-12` — endereço `claude-peer:` ou `claude-hand-back:`. [F58 · lido · 90]
- **O `::orca-visual` é documento estático.** `brza-studio/resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md:20,42-46`; `src/shared/native-chat/native-chat-visual-directive.ts:13,16` — até 8 por resposta, 512 KB; iframe `sandbox="allow-scripts"` (`NativeChatVisualFrame.tsx:174`), CSP `connect-src 'none'` (`native-chat-visual-shell.ts:27`); `submit` é cancelado (`:158`). [F59 · lido · 90]
- **O Agent Dashboard é um kanban com 4 colunas.** `brza-studio/src/shared/dashboard-snapshot.ts:10-18,84-146` — `attention | working | done | idle`; cartão com `dotState`, `verdict`, `lastAgentMessage`, `parentPaneKey`. Abre em gaveta ou janela (`agent-dashboard-open-mode.ts:10-16`). [F60 · lido · 95]
- **A hierarquia pai e filho existe.** `brza-studio/src/renderer/src/components/dashboard/agent-row-lineage-model.ts:1-60`. As sessões do `brza sessions` são `agent launch` soltos, não workers do Orca (inferência, 70). [F61 · lido · 90]
- **O painel `orchestration-crew` está desligado.** `brza-studio/src/renderer/src/components/orchestration-crew/use-orchestration-panel-enabled.ts:1-4` devolve `false` ("Suspended after repeated performance regressions"), commit `20ff1375047`. O modelo `CrewRow` está em `src/shared/orchestration-crew.ts:5-33`. [F62 · lido · 95]
- **O painel `orchestration-crew` lia o banco de orquestração, não os chats.** `brza-studio/src/main/runtime/orchestration/crew/crew-parent-inputs.ts:36-60`, `crew-party-snapshot.ts:198-251` — `managing` e `managedBy` vêm de `dispatches` e `runs`; `talkingWith`, da mailbox da orquestração. Um chat aberto por `brza agent launch --surface chat` sem run não aparece em nenhuma seção (inferência do código, 78). A linha `CrewRow` tem papel, estado, tarefa, última mensagem, pergunta pendente e destino para abrir (`src/shared/orchestration-crew.ts:6-32`); não tem grupo, rodada, posição nem confiança. [F81 · lido · 90]
- **O upstream o desligou duas vezes em dois dias.** `7872cb5aa17` (2026-11-02, "Disable the lagging experimental orchestration panel", "after reported app lag"), `40b660357c4` (mesmo dia, "remove orchestration panel CPU amplification", ~17 arquivos do `main`), `7863aefbc22` (restaura o opt-in) e `20ff1375047` (2026-11-03, #38045, suspende de novo e remove o setting; 22 arquivos, −500 linhas). A causa é do lado do `main` (invalidação e reconstrução do read model), inferida dos títulos; não há issue, PR descritivo nem CHANGELOG. [F82 · rodado · 90]
- **O tamanho do caminho:** renderer 19 arquivos e 2 559 linhas com testes; `main/runtime/orchestration/crew/` 3 456 linhas sem testes. A pasta recebeu 20 commits do upstream em quatro dias de novembro, muitos de reorganização. [F83 · rodado · 90]
- **Os gates de decisão só existem na CLI.** `brza-studio/src/cli/specs/orchestration-gate-specs.ts:5-27` — `gate-create`, `gate-resolve`, `gate-list`; o `grep` em `src/renderer/src` não achou componente de gate. [F63 · rodado · 80]
- **Plugin: painéis na barra direita, sem contribuição para o chat.** `brza-studio/docs/reference/plugin-manifest.md:33,47,53,201-212` — `ui: components`, status bar, eventos, hooks; `sidebarCards` reservado e vazio. [F64 · lido · 95]
- **O plugin vê agentes do workspace focado.** `docs/reference/plugin-host-api.md:172-178` — `agents.list` devolve `{terminalId|null, title|null, agent|null, state, stateStartedAt}`; sem API de transcrição nem de envio ao chat. [F65 · lido · 95]
- **Não há "FleetView" no app.** `grep -rli fleet src docs resources` não acha o termo como recurso. [F66 · rodado · 90]
- **A CLI de chats só existe na branch do PLN-011.** `brza-studio/.worktrees/pln-011-chat-cli/src/cli/specs/chat.ts:5-40` — `chat list`, `chat read --cursor`, `chat send`; `ls src/cli/handlers | grep -i chat` vazio na `master` (`8abbde720ce`). [F67 · rodado · 90]
- **O Jump Palette já inclui chats na `master`.** `brza-studio/src/renderer/src/lib/workspace-tab-palette-content-type.ts:8-10` — o design do PLN-011 dizia o contrário. [F68 · lido · 95]

#### Os planos vizinhos
- **PLN-011 (`workstream/studio`) está bloqueado no C1.** `workstream/studio:plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md:2-33` — `status: open`, `phase: blocked`, 1,8 h de 31 h; P1 a P5 fechados; P6/C1 espera Anderson no app de dev (`blocks` preenchido). Fora de escopo: `brza sessions` sobre a CLI nova (vai ao PLN-010). [F69 · lido · 95]
- **PLN-010 (`workstream/tools-kit`), `brza sessions` sobre o `brza chat`.** `workstream/tools-kit:plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md:6-7,22-24,36-43,62-73,93-103` — `open`, `interview`, `depends_on: PLN-011`; pede `list`, `read --since`, recibo fiel (`accepted|rejected|pending|unknown`), `--operation`, origem do coordenador. Sem passo. [F70 · lido · 95]
- **PLN-013 (`workstream/tools-kit`), `done` em 2026-11-04.** `workstream/tools-kit:plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md:1-14` — abre Grok, Codex e Antigravity no `brza sessions` e no MCP; `--model` e `--effort` entraram só no MCP (`cycle.py:152-156`); `--rename` não chega ao Grok nem ao Antigravity (duas issues abertas). [F71 · lido · 95]
- **PLN-009 (`workstream/tools-kit`), `done` em 2026-11-06.** `workstream/tools-kit:plans/PLN-009-o-mcp-orquestrador-do-fluxo/PLN-009-plan.md` — MCP em `brza-workflow@23d812d`; sem `cancel` (issue `o-mcp-nao-cancela-pedido-na-fila`); `o-dispatch-aceita-chamador-fora-do-studio` aberta. [F72 · lido · 95]
- **PLN-012 (`workstream/tools-kit`), em execução.** `workstream/tools-kit:plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md:1-14` — 3,5 h de 16 h; P3 e P6 abertos; `feat/pln-012-medida-por-tarefa` está 22 commits à frente e 2 atrás da `master` do `brza-workflow` (`0a6f181`, 13 arquivos, +1861/-51). [F73 · rodado · 95]
- **PLN-015 (`workstream/tools-kit`), `open` em `design`.** `workstream/tools-kit:plans/PLN-015-advisor-no-executor/PLN-015-plan.md` — advisor no executor; toca o `measure.py`; exclui Codex, Grok e Antigravity. [F74 · lido · 95]
- **PLN-004 (`workstream/workspace`), `open` em `interview`.** `workstream/workspace:plans/PLN-004-os-runtimes-codex-agy-e-grok-no-fluxo/PLN-004-plan.md:19-45` — R12.2 Claude como revisor padrão; `brza delegate` só decidido; P18 (`agy` em `--surface terminal`) por perguntar; fora de escopo o chat Antigravity do Studio. [F75 · lido · 90]

| Necessidade da reunião | Plano | Estado |
| :-- | :-- | :-- |
| Abrir sessão com modelo e esforço | PLN-013 (MCP) | MCP entregue; `brza sessions`: nenhum plano |
| Abrir nos quatro runtimes | PLN-013 | entregue; Antigravity só pelo chat do app |
| Enviar com recibo e retry | PLN-010 | `open`, depende do PLN-011 |
| Esperar fim de rodada | nenhum | `--wait` só da abertura; `worker_done` só de workers |
| Ler o chat da persona | PLN-010, PLN-011 | sem `read` no `brza`; `chat read` só na branch |
| Medir Claude | PLN-012 | em branch, P3 e P6 abertos |
| Medir Codex, Grok, Antigravity | issues `low` do PLN-012 | sem passo |
| Cota por runtime | PLN-013 | entregue; troca de conta só do Codex |
| Revisor independente | PLN-004 (`brza delegate`) | decidido, sem código |
| Persona livre (modelo próprio) | nenhum | MCP tem 3 papéis fixos |

[F76 · lido · 85]

#### As colisões
- **O PLN-014 trava emenda e porte.** `plans/PLN-014-refinamento-do-radar-do-playground/PLN-014-plan.md:13,20,43-44` — `blocks: A emenda das issues e qualquer porte esperam a entrevista deste plano.`; `status: open`, `phase: interview`. Cobre as quinze issues do `playground`, a de 2026-11-03 sobre chats inclusive. [F77 · lido · 95]
- **O PLN-010 tem a R1.4 que proibia voltar ao `rpc`.** `workstream/tools-kit:plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md`, R1.4 — citada pelo levantamento do `brza-workflow` (seção 3, ponto 2). Os `read`, recibo e `send` do `brza sessions` de hoje saem pelo `rpc()` de `brza_runtime.py:87-145`. [F78 · lido · 80]
- **O `measure.py` tem três donos.** PLN-012 (branch, P3 e P5.4 abertos), PLN-015 (entra antes, R1.1) e a medição por runtime (PLN-004, R17, só entrevista). `workstream/tools-kit:plans/PLN-012-…/PLN-012-plan.md` dá o PLN-015 como anterior. [F79 · lido · 90]
- **O PLN-011 espera Anderson no C1.** `workstream/studio:plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md:2-33` — o PLN-010 depende dele (`depends_on`), logo `read`, recibo e `chat focus` ficam sem prazo. [F80 · lido · 95]
