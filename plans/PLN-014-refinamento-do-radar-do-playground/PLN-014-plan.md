---
status: open
phase: interview
origin: request
description: A entrevista escolhe o destino do refinamento das quinze issues do playground, com terreno e opções já medidos.
ready: "não — aguarda a entrevista de Anderson sobre o destino do refinamento"
scope:
  - workspace
  - brza-studio
  - brza-workflow
opened: 2026-11-04
owner: Anderson
blocks: A emenda das issues e qualquer porte esperam a entrevista deste plano.
tags:
  - planning
---

# PLN-014: O refinamento do radar do playground chega à entrevista com as opções medidas

- **Retomar:** Terreno e opções estão no Desenho. A R1 foi reapresentada em 2026-11-12 na auditoria
  [Priorização: issues high × planos abertos × Context7](../../work/worklogs/2026-11-12-priorizacao-issues-high-planos-e-context7.md),
  com o cruzamento dos 13 planos abertos e provas Context7 (MCP OAuth/PKCE, Electron `kNoSandbox`, contraste WCAG).
  Em 2026-11-12 o playground tem 47 issues `high` abertas (não mais só as nove do terreno de 2026-11-04); a regra
  `blocks` deste plano continua: nada se emenda e nada se porta antes da resposta da R1. Cadeia paralela que não
  espera este plano: C1 do PLN-011 → Desenho do PLN-010; PLN-003/P4 no `tools-kit` (com desvio de distribuição).

## Pedido

- **Origem:** pedido de Anderson nesta sessão, em 2026-11-04, no workstream `playground`. Nenhuma das quinze issues é a origem sozinha. A de chats já teve rodada em 2026-11-03 e o trabalho segue no [PLN-011: Os chats do BrzA Studio se coordenam pela CLI, aparecem na navegação e chegam aos plugins](../../../studio/plans/PLN-011-chats-pela-cli-e-plugins/PLN-011-plan.md) e no [PLN-010: O `brza sessions` lê e envia pelo `brza chat` do Studio, com recibo fiel](../../../tools-kit/plans/PLN-010-brza-sessions-sobre-o-brza-chat/PLN-010-plan.md).

"coordene um fluxo de refinamento das issues desse workstream, abra subagents para coletar mais informações, faça auditorias para validar os dados e medições, faça rodadas de brainstorm para levantar mais hipóteses, quando tiver confiança suficiente nos levantamentos, abra o plano, inicie o terreno, faça mais medições, desenhe as opções, e só então solicite a minha intervenção, para a rodada de entrevista"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 1` | As quinze issues foram lidas e os números citados no upstream foram conferidos | R1 | coleta no scratch; a auditoria refez os doze `closed` |
| `Pedido 2` | A classe de sobreposição e a medição foram atacadas | R1 | pareceres no scratch, com o que caiu |
| `Pedido 3` | Há hipóteses de três focos, cada uma com o que caiu | R1 | rascunhos no scratch |
| `Pedido 4` | O plano está aberto neste workstream | R1 | este arquivo |
| `Pedido 5` | O terreno do destino tem `arquivo:linha` | R1 | a seção Terreno |
| `Pedido 6` | O custo que entra na entrevista foi contado, ou ficou de fora | R1 | contagem das 7 notas; `git grep` do símbolo; prompt da automação relido |
| `Pedido 7` | Três opções lado a lado, com custo e quando se paga | R1 | D1, em aberto |
| `Pedido 8` | Anderson escolhe, e nada executa antes da resposta | R1 | a mensagem da sessão; nenhuma issue mudou de `status` |

### Fora de escopo

- **Porte de código das quinze issues.** A casa do código é o `studio` ou o `tools-kit`, e passo de código espera pedido explícito depois desta entrevista.
- **Emendar nota antes da resposta.** O parêntese nos números fechados e o `done` da issue de chats estão em D1.
- **Corrigir worklog já commitado.** A linha da próxima execução no radar de 2026-11-03 e os campos `opened`/`completed` do P8 e do radar de 2026-11-04 ficam como foram escritos.
- **Classificar** [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../../work/issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md). Diff, cache e ranking do menu `/` ficaram abaixo de 80.
- **Eleger a ordem das nove `high`.**

## Restrições

- **Uma pergunta por plano.** Este arquivo guarda o refinamento. Não porta as quinze.
- **Merge no upstream não é patch no `brza-studio`.** O merge `14819eb8c043` do `#37774` não é ancestral do HEAD `8f41dd56a336`.
- **US$ 3,77 não é esta sessão.** É o recorte `playground` de 2026-11-03 no jsonl. Esta sessão é Grok e não está nesse arquivo.
- **Hora não medida não entra no custo.** O que sustenta a opção é a contagem que o comando fez.

## Desenho

### O que este desenho assume

- **Nada ainda.** A entrevista não foi respondida. D1 é ponto sem lastro.

### Terreno

#### O inbox

- **Quinze issues, todas `open`:** 9 `high`, 4 `medium`, 2 `low`. Nenhuma tem critério de aceite nem `blocks`. `plans/` deste workstream, antes deste arquivo, só tinha o `README.md`.
- **Nenhuma está coberta no `brza-studio` `master`.** A auditoria corrigiu a classe para 0 cobertas, 4 parciais (titulação, chats, `ORCA_WORKTREE_ID`, SSH), 10 ausentes e 1 não verificada (a de Native Chat, fora de escopo).
- **Oito PRs citados estão `MERGED` no upstream e não estão neste HEAD:** `#37659`, `#37703`, `#37716`, `#37730`, `#37774`, `#37883`, `#37891`, `#37974`. Dois PRs estão `CLOSED` sem merge: `#37507`, `#37861`. Duas issues estão `CLOSED`: `#37505`, `#37859`. Sete notas citam pelo menos um desses doze números.

#### O que já tem dono

- **A issue de chats** [Ler e enviar mensagens a chats pela CLI e expor Native Chat aos plugins](../../work/issues/ler-e-enviar-mensagens-a-chats-pela-cli-e-expor-native-chat-aos-plugins.md) está `open`, sem `owner`. Nas linhas 126–127 ela diz que passa a `done`, com os links, quando as issues novas existirem. Ela não cita `PLN-011` nem `PLN-010`.
- **As filhas existem e estão `open`.** O PLN-011 está `phase: blocked`, `owner: Anderson`, à espera do caso manual C1. O PLN-010 está `phase: interview` e `depends_on: PLN-011`.

#### O setup, hoje

- **O padrão é `setupRunPolicy: 'run-by-default'`.** `brza-studio/src/shared/constants.ts:127`.
- **Com decisão `inherit`, o create roda o setup quando a política efetiva é essa.** `shouldRunSetupForCreate` em `src/main/effective-hook-config.ts:64-77`. `ask` lança erro. `skip` não roda.
- **A UI parte de `inherit`.** A confirmação lê o `orca.yaml` de `repo.path`, não o do worktree novo. `src/renderer/src/lib/ensure-hooks-confirmed.ts` e `src/main/runtime/runtime-local-worktree-setup.ts:36-77`.
- **Automação headless repassa `setupDecision` gravado, ou `skip`.** `src/main/automations/headless-workspace-create.ts:40`.
- **`runApprovedSetup` não tem linha** no `brza-studio`, no `brza-workflow` nem no worktree `studio`. `git grep -F` saiu 1 nos três.
- **`.orca/issue-command` é lido**, e conteúdo local não vazio vence o yaml. `src/main/issue-command-file.ts:15-56`. Isso não é o hash.

#### O radar que escreve as notas

- **A automação `f75b8281-8ae3-4558-afe4-7ab5bbc35601` está ligada**, cron `0 */6 * * *`, fuso `America/Sao_Paulo`, no worktree `playground`. O prompt manda criar ou atualizar `work/issues/` e commitar. Não manda preservar emenda manual. Se a emenda sobrevive ao próximo ciclo não foi observado.

### D1 — O destino deste plano — ponto sem lastro

- **Origem:** ponto sem lastro. A R1 ainda não foi respondida.
- **Contexto:** o pedido abre este plano e pede a entrevista por último. As três hipóteses não concordam no que o plano passa a responder.

#### As alternativas

##### A1 — A pergunta deste plano é a regra de despacho

Cada nota passa a dizer a classe (coberta, parcial, ausente, não verificada), a casa (`studio`, `tools-kit` ou as duas) e o plano que já existe, se houver. Merge no upstream não muda `status`. Plano de comportamento só nasce na casa do código, quando Anderson pedir aquele comportamento.

- **Custo:** depois da resposta, uma sessão de notas. A contagem medida é 15 linhas de casa e classe, e parêntese em 7 notas que citam número fechado. A hora não foi medida e não entra. Não há porte.
- **Se paga:** na leitura do próximo ciclo de 6h, se o ciclo não apagar a frase. A sobrevivência da emenda não foi observada.
- **Reabre:** a frase de 2026-11-03 de que a issue de chats passa a `done` quando as filhas existirem.

##### A2 — A pergunta deste plano passa a ser o gate de setup

A origem passa a ser a [Segurança de hooks em worktrees e integridade de setup em automações](../../work/issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md). As outras quatorze ficam de fora. O gate (`ask`, hash, ou só emenda da nota) é outra rodada, com o diff dos PRs ainda aberto. Nenhum passo de código nesta passagem.

- **Custo:** trocar a origem e fazer a rodada do gate depois. `runApprovedSetup` está ausente (exit 1) e o padrão do create na UI é rodar. A automação headless já cai em `skip` quando não há decisão gravada. A hora de implementar não foi medida e não entra. O "O que fazer" da nota são 3 linhas e nomeia quatro PRs (`#37977`, `#37978`, `#37979`, `#37931`).
- **Se paga:** quando Anderson pedir a execução, no create da UI que herda `run-by-default`. Não se paga no create headless que já usa `skip`, nem no destino das outras quatorze.
- **Reabre:** a eleição entre as nove `high`, e o `#37931` se a nota entrar inteira.

##### A3 — Encerrar este plano e ficar na emenda

`phase: dropped`, com a linha do porquê. O número não se reusa. A emenda (parêntese nas 7, e o que a R1 disser da issue de chats) espera pedido de execução. Não responde à regra de despacho nem ao gate.

- **Custo:** um plano aberto e fechado na mesma sessão, mais a emenda se ela for pedida. A hora não foi medida e não entra.
- **Se paga:** na próxima leitura das 7 notas, para o número fechado não continuar como proposta aberta. Não se paga como pergunta que as notas sozinhas não respondem.
- **Reabre:** o pedido desta sessão, que mandou abrir o plano.

#### Em aberto

1. **Destino do PLN-014.** A1, a regra de despacho, é a recomendada: o pedido é o refinamento das issues, o gate de setup não é "sempre roda", e porte não foi pedido.
   - A1 — custo: 15 linhas e parêntese em 7 notas, hora fora; se paga: na leitura do próximo ciclo, se a frase sobreviver.
   - A2 — custo: outra rodada para o gate, hora de código fora; se paga: na execução pedida, no create da UI; nunca nas outras quatorze.
   - A3 — custo: dropar o número recém-aberto; se paga: na leitura das 7 notas; nunca como a pergunta do pedido.

2. **A issue de chats.** Fica `open`, com ponteiro para o PLN-011 e o PLN-010, é a recomendada. As filhas existem e estão `open`, e o PLN-011 espera o C1.
   - Fica `open` — custo: nenhuma troca de `status`; se paga: agora, para a próxima leitura não tratar o C1 como entrega.
   - Passa a `done`, com a linha de handoff — custo: uma troca de `status`, sem código; se paga: agora, se "quando elas existirem" basta.

3. **Parêntese nos 7 arquivos que citam número fechado.** Entra nesta passagem, no número, sem reescrever o adjetivo da lista mista, é a recomendada. `MERGED` não vira "já está no fork".
   - Entra — custo: 7 notas; se paga: na próxima leitura.
   - Fica para outra passagem — custo: nenhum; se paga: nunca para o "aberto" que já não é.

## Worklogs

- 2026-11-04 — abertura, terreno e D1 em aberto. Parou na R1.
  [Refinamento do radar do playground até a entrevista](../../work/worklogs/2026-11-04-refinamento-do-radar-do-playground.md)
- 2026-11-12 — auditoria high × planos × Context7; R1 reapresentada; sem emenda nem porte.
  [Priorização: issues high × planos abertos × Context7](../../work/worklogs/2026-11-12-priorizacao-issues-high-planos-e-context7.md)

## Documentação

- MCP Authorization (spec 2025-11-25): OAuth 2.1 + PKCE no HTTP; STDIO lê credenciais do ambiente —
  `https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization` (Context7
  `/websites/modelcontextprotocol_io_specification_2025-11-25`).
- Electron sandbox / `utilityProcess` sem sandbox Chromium (`kNoSandbox`) — docs Electron via Context7
  `/electron/electron`.
- Contraste WCAG 2.1 / `forced-colors` — WAI-ARIA APG via Context7 `/w3c/aria-practices`.

## Pendências conhecidas

- [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../../work/issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md)
  — `high`; porte só depois da R1 (e alinhamento OAuth/PKCE da spec).
- [O default dos plugins e o alcance do worker sem sandbox](../../work/decisions/o-default-dos-plugins-e-o-alcance-do-worker-sem-sandbox.md)
  — proposta `open`; Context7 confirma worker Electron unsandboxed.

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano. Trabalho só em notas não tem resumo.
- [ ] O durável saiu para a casa dona.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
