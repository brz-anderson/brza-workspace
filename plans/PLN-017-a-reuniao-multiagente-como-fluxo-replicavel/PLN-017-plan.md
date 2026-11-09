---
status: in_progress
phase: execution
origin: issue
origin_ref: reuniao-multiagente-com-personas-pelo-brza-sessions
description: Levantamento e desenho, em três frentes, do que falta para a reunião multiagente com personas rodar sem improviso em qualquer client: a skill, as primitivas do brza sessions e o painel da rodada no chat do Studio.
ready: "P1 a P7 concluídos; próximo P8 e as correções da skill (X19, X1, X10) antes da próxima reunião"
estimate_h: 34.75
executed_h: 8.983
remaining_h: 11.5
priority: high
scope:
  - workspace
  - brza-workflow
  - brza-studio
opened: 2026-11-08
owner: Anderson
tags:
  - tooling
  - planning
---

# PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat

- **Retomar:** P1 a P7 concluídos. P7 rodou a reunião de verificação "CI no chat" pela skill (Prumo Claude Opus xhigh, Trava Grok 4.7 medium, Relance Antigravity), via `worker-start` num Run único, com R1, R2 e uma R3 extra escolhida por Anderson; decisões aplicadas em três issues; 19 desvios, que **não** contam como reunião sem desvio. A reunião usou os scripts v1 da skill (`launch_persona.py`, `wait_round.py`), não os verbos v2 do `brza sessions` publicados em P4a/P4b. Próximo: as correções da skill que os desvios pedem, em [D1, os desvios do P7](PLN-017-design-skill.md) — primeiro o `worker_done` sem `--task-id` (X19), a sessão do provedor no recibo (X1) e o fato que chega tarde (X10) —, a troca para os verbos v2, e P8. Pendências menores da skill seguem no worklog de P1/P2.
- **Dividido:** [PLN-017 — Desenho](PLN-017-design.md) · [D1, a skill](PLN-017-design-skill.md) · [D2, o `brza sessions`](PLN-017-design-cli.md) · [D3, o painel](PLN-017-design-painel.md)

## Pedido

- **Origem:** [A reunião multiagente com personas pelo `brza sessions`](../../work/issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md); o pedido de Anderson na sessão `workflow-improvements` de 2026-11-08, no workstream `playground`.

"a sessão `Rebranding BrzA: Carvão em Brasa` coordenou uma reunião ontem, com vários runtimes, diferentes personas e modelo/esforço escolhidos por frente/abordagem, também tivemos a sessão `Reunião: MCP remoto e sessões Cloud` que coordenou outra reunião, nos mesmos moldes da primeira, replicando o formato - essa também fez medições úteis quanto ao nosso `brza-orchestrator` -, com isso vamos extrair os dados e medições feitos, no intuito de melhorar nosso fluxo como um todo.

os pontos que devem ser considerados são:

- a sessão `Rebranding BrzA: Carvão em Brasa` coordenou muito bem a reunião, e principalmente, informou muito bem o desenrolar da reunião no chat, o que facilitou a minha revisão dos fatos;
- a sessão `Reunião: MCP remoto e sessões Cloud` também coordenou bem a discussão entre as sessões/personas, mas deixou a desejar no acompanhamento dos fatos, as sessões "filhas" registraram de forma mais clara e organizada, o que me obrigou a acompanhar as rodadas pelo chat das filhas;
- centralizar as informações visíveis ao usuário - no caso eu, que sou o decisor e mantenedor - facilita o acompanhamento e a tomada de decisões;
- diferentes personas destrincharam os fatos muito mais efetivamente e levaram a achados que apenas alterar modelo/esforço não levariam;
- a reunião fez com que as decisões que dependem de mim chegassem muito mais maduras, tendo em vista que meu tempo disponível é curto, prevejo ganho de performance nessa abordagem;

dito isso, nossa missão agora é:

- levantar possíveis skills que possam ser criadas;
- levantar melhorias que possam ser feitas tanto no `BrzA CLI` quanto no `brza-orchestrator`, para que o fluxo possa ser replicado independente do `client` utilizado;
- levantar melhorias que possam entrar no `BrzA Studio`, de interface, para tornar o fluxo visualmente simples e intuitivo, incluindo a UI do chat e plugins;"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 0` ("extrair os dados e medições") | As medições das duas reuniões (latência, custo, confiança, utilidade por persona e modelo, narração em chat) estão no Terreno, cada número com a fonte | Terreno (feito) | as tabelas do Terreno, conferidas contra os worklogs de coordenação (duas divergências registradas: a nota dos colegas e a hora da cota) |
| `Pedido 1` (skills) | A skill `meeting-runner` existe em `.claude/skills/` da branch, criada e revisada pela `skill-creator`, com os três casos de teste passando e uma reunião curta rodada por ela | P1, P7 | `evals/evals.json` com as asserções (unidade); a reunião de verificação (manual) |
| `Pedido 2` (CLI e orquestrador) | O `brza sessions` abre com modelo, envia com recibo, espera o fim da rodada, lê a última resposta, troca o modelo, mede por runtime e fecha por prefixo; o `brza shot` roda; o embrulho MCP está anotado para depois | P3, P4a, P4b, P5, P6 | `tests/cli/test_brza_sessions.py` e `test_brza_shot.py` (unidade); a reunião de verificação sem o `launch.py` (manual) |
| `Pedido 3` (UI do Studio) | O painel da rodada sai do gerador da skill como `::orca-visual`, republicado durante a rodada e conferido por PNG; a fase seguinte e o `orchestration-crew` estão na issue ao `studio` | P2, P3 | os testes do `panel.py` com a R3 da reunião MCP (unidade); o painel na reunião de verificação (manual) |
| Considerações ("centralizar as informações visíveis ao decisor") | As práticas de narração que distinguem a coordenação do Carvão da do MCP viram regra da skill, com a evidência dos transcripts, e dado do painel | D1, D3 | a comparação dos transcripts no Terreno |

### Fora de escopo

- **A execução em cada repositório.** A skill no `core/` do `brza-workflow`, os verbos do `brza sessions` e qualquer código do `brza-studio` são do workstream dono (`workspace`, `tools-kit`, `studio`) e saem deste plano por issue ou linha de `Retomar`, com o `D` e o que as rodadas decidiram (R1.1).
- **O embrulho MCP das primitivas.** Vem depois de o CLI rodar duas reuniões (R1.2); D2 só anota o que ele reaproveita.
- **A argumentação integral de cada persona no painel.** Fica para a fase do painel (plugin ou painel nativo), por Anderson em R1.4; a v1 mostra posição, confiança, estado, medições e, no máximo, o caminho da seção do worklog.
- **As issues de 2026-11-03 do `playground`** que tocam o tema (chats pela CLI, painel de atividades de subagentes, native chat aos plugins). O PLN-014 trava a emenda e o porte delas; este plano só as cita.
- **O relay/fila de saída e o proxy remoto do `brza-mcp`.** São da reunião MCP remoto e das issues dela, não deste fluxo.

## Restrições

- **Toda skill deste plano se cria e se revisa pela skill `skill-creator`.** Pedido de Anderson em 2026-11-08: "utilize a skill skill-creator para criar e revisar as skills desse plano e as que serão criadas futuramente nesse workstream". O plugin `skill-creator@claude-plugins-official` está habilitado no `.claude/settings.json` da branch `workstream/playground` (`brza-workspace@b18f520`), e o registro do escopo está em `.claude/rules/workspace.md`, na `master`. O passo que escreve o `SKILL.md` de D1 roda numa sessão aberta com o plugin carregado e aciona `/skill-creator` antes de gravar; a revisão da skill também passa por ele.
- **As issues de 2026-11-03 do `playground` não se emendam nem se portam** antes da entrevista do PLN-014, que as trava.
- **A skill `meeting-runner` mora na branch `workstream/playground`, em `.claude/skills/`, fora da `master`** (R2.1): é um desvio declarado da norma "o `.claude/` mora na `master`", válido até a promoção ao `core/` do `brza-workflow`, depois de duas reuniões sem desvio de fluxo. O `brza sync` não apaga a pasta, porque ela não está no `core.lock`.

## Entrevista

### Rodada 1 — destino, primitiva, UI e narração (enviada 2026-11-08)

**Apresentado antes:** o resumo dos cinco levantamentos (ferramental, Studio, protocolo e medições, narração dos dois chats, planos vizinhos): a coordenação pesa 57% a 62% do custo medido das reuniões (US$ 22,67 e 6,03 das duas sessões de coordenação, contra US$ 36,76 e 10,64 de total Claude); a diferença de narração entre as coordenações não é de silêncio, mas de conteúdo (personas nomeadas em 11 de 57 blocos contra 4 de 47; síntese com posição, viradas e números contra o agregado; worklog em `<details>` e painel `::orca-visual` contra a lista de arquivos); o protocolo tem 17 passos e 10 ficaram implícitos; o `brza sessions` não tem `read`, `wait` nem troca de modelo e não repassa `--model`/`--effort`; o worker do orquestrador dura uma tarefa; o Orca tem um painel de equipe no chat desligado por regressão de desempenho e gates só na CLI; o PLN-014 trava emenda e porte das issues de 2026-11-03.

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **Destino.** Onde mora este plano, que guarda o levantamento e o desenho das três frentes, com a execução em outro workstream por issue:
   - um PLN no `playground`, origem a issue da reunião, as três frentes como itens D e a saída por issue (recomendada) — custo: esta sessão, hoje, depois uma sessão por workstream dono; se paga: agora, a decisão amadurece num lugar só antes de tocar três repositórios;
   - três PLNs, um por workstream, abertos agora — custo: três sessões hoje e o levantamento repartido; se paga: só se as três frentes executarem já, em paralelo;
   - só worklog e emenda da issue — custo: 1 h; se paga: nunca para o desenho; as 35 perguntas dos levantamentos ficam sem rodada.

   **Decidido — um PLN no `playground`**: este, PLN-017.

2. **Primitiva.** Onde nasce a primitiva (abrir com modelo/esforço, enviar a N com recibo, esperar fim de turno, ler, trocar modelo, fechar):
   - `brza sessions` primeiro; o MCP só embrulha os verbos depois, para quem chama sem shell (recomendada) — custo: 2 a 4 dias no `tools-kit`, sem tocar o ciclo do orquestrador; se paga: na próxima reunião, sem o `launch.py` improvisado;
   - orquestrador primeiro (`dispatch` com `keep_open`, `worktree`, `send`/`read`/`wait` para worker aberto; a política deixa a persona escolher o modelo) — custo: 4 a 8 dias em `cycle.py`, `policy.py`, `tools.py` e `tests/mcp/`; se paga: só quando a coordenação rodar fora do Mac;
   - os dois juntos — custo: 6 a 12 dias; se paga: nunca antes de o fluxo rodar duas vezes pelo CLI.

   **Decidido — `brza sessions` primeiro.**

3. **UI.** Por onde começa a frente do BrzA Studio:
   - painel da rodada como `::orca-visual` gerado pela coordenação, sem código no app, conferido por PNG, pela skill (recomendada) — custo: 4 a 8 h no `brza-workflow`; se paga: na próxima reunião, e mede o que o plugin precisa mostrar;
   - plugin de painel na barra direita — custo: 12 a 20 h no `studio`, ligando persona a chat só por título até o P14 do PLN-011; se paga: da terceira reunião em diante;
   - religar o painel de equipe do Orca (`orchestration-crew`) — custo: 16 a 30 h, com a causa da regressão desconhecida e merge futuro do upstream; se paga: só com reunião semanal;
   - só issues no `studio`, nada agora — custo: 0 h; se paga: nunca para a próxima reunião.

   **Resposta:** "opção 1, mas faça uma investigação breve para medirmos o custo X beneficio da opção 3". **Decidido — o painel gerado no chat (D3)**, e a investigação do custo de religar o `orchestration-crew` entra no Terreno e no "Em aberto" de D3.

4. **O que faltou.** O que Anderson viu nos chats das personas da reunião MCP e faltou no da coordenação (seleção múltipla):
   - posição e confiança de cada persona por rodada — custo: 1 bloco por rodada, ~2 mil caracteres; se paga: agora, regra da skill;
   - quem já respondeu e quem falta, em tempo real — custo: 1 linha por conferência; se paga: agora, regra da skill, e o painel mostra o mesmo;
   - a argumentação integral, não a síntese — custo: ~1,5 mil palavras por persona por rodada; se paga: só com o painel, que recolhe o texto;
   - os números e medições conferidos — custo: 1 bloco por medição; se paga: agora, regra da skill.

   **Resposta:** "Posição e confiança de cada persona por rodada, Quem já respondeu e quem falta, em tempo real, Os números e medições conferidos, argumentação integral fica pra fase do painel". **Decidido — os três primeiros viram regra de narração da skill (D1) e dados do painel (D3); a argumentação integral fica para a fase do painel**, fora deste plano.

### Rodada 2 — a skill (enviada 2026-11-08)

**Apresentado antes:** o desenho D1 ([PLN-017 — Desenho: a skill (D1)](PLN-017-design-skill.md)): o `.sessions/` está no `.gitignore`, e a proposta final passa a ser copiada ao worklog da coordenação; a contraprova do Carvão custou perto de US$ 9,8 e não 3,5, porque o turno de 802 s da coordenação a cobre; o "desconto do revisor" não vira regra, porque na v3.2 do MCP ele ficou acima da sala; a skill fixa 17 passos e as regras de narração da R1.4, na forma da `skill-creator`, com três casos de teste determinísticos em vez de reuniões inteiras.

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **Onde a skill nasce.** Hoje a norma diz que o `.claude/` mora na `master`; o `brza sync` não apaga pasta nova em `.claude/skills/`:
   - protótipo em `.claude/skills/meeting-runner/` só na branch do `playground`, promovido ao `core/` do `brza-workflow` depois de duas reuniões sem desvio de fluxo (recomendada) — custo: um desvio de norma declarado no plano e uma rodada de sync na promoção; se paga: agora, cada correção depois de uma reunião é um commit de nota;
   - na `master` do `brza-workspace`, fora do `core.lock` — custo: cada ajuste vira issue ao `workspace` e `brza note sync`; se paga: quando outra frente pedir reunião antes da promoção;
   - direto no `core/` do `brza-workflow`, por sessão do `workspace` — custo: cada correção da v1 é commit lá, `brza sync` e `brza note sync`; se paga: só depois de estabilizar;
   - guia em `wiki/guides/`, sem skill — custo: ~3 h, sem gatilho nem scripts; se paga: nunca para a agregação.

   **Decidido — protótipo na branch do `playground`**, promovido ao `core/` depois de duas reuniões sem desvio; o desvio da norma está nas Restrições.

2. **O escopo da v1.** O painel (D3) fica à parte em qualquer opção:
   - `SKILL.md`, oito references e quatro scripts (`launch_persona.py`, `wait_round.py`, `tally.py`, `runtime_memory_check.py`), criada pela `skill-creator` com três casos de teste determinísticos (recomendada) — custo: ~10,5 h, das quais ~1,25 h morrem quando o CLI ganhar `--model` e `wait`; se paga: na primeira reunião, pela tabela por persona a cada rodada sem conta à mão;
   - `SKILL.md` e references, sem scripts — custo: ~6 h, lançador reescrito a cada reunião e tabela manual; se paga: só se o CLI do D2 chegar antes da próxima reunião;
   - `SKILL.md` mínimo — custo: ~2 h; se paga: nunca, repete a forma que deixou 15 itens implícitos.

   **Decidido — `SKILL.md`, oito references e quatro scripts.**

3. **A confiança do plano e a contraprova.** O revisor ficou 12 e 17 pontos abaixo da sala em duas medições e 3 acima na terceira:
   - o número do revisor independente é a confiança; a sala ao lado (média, mediana, n, faixa), o Antigravity fora da conta, a diferença sala × revisor registrada; contraprova só quando a proposta vai a aprovação e é cara de reverter, ou sala e revisor divergem mais de 10 pontos, em modelos baratos, sem Fable (recomendada) — custo: US$ 2,4 a 3,8 de revisor por reunião, ~US$ 7 e 13 min quando a contraprova dispara; se paga: na primeira reunião, pelo erro que o revisor acha;
   - revisor como número, contraprova sempre — custo: ~US$ 10 e ~13 min a mais por reunião; se paga: só em decisão cara de reverter;
   - média da sala, sem contraprova — custo: US$ 0, superestima em duas de três medições; se paga: nunca para decisão.

   **Decidido — o revisor como número; a contraprova por gatilho.**

4. **A rodada final de decisão.** A memória `consultant-debate-shown-in-full` (2026-11-03) pede a argumentação completa dos consultores; a R1.4 tirou a argumentação integral do chat:
   - por opção, o voto de cada persona e, em uma linha cada, o argumento mais forte a favor e o mais forte contra, com o link do worklog; a memória passa a valer só para consultores por `Agent` (recomendada) — custo: a rodada cabe numa tela, uma emenda na memória; se paga: agora;
   - a argumentação completa, como a memória manda — custo: 6 personas × 4 decisões, várias telas; se paga: quando a decisão é uma só e disputada;
   - só o placar dos votos — custo: Anderson volta aos chats das filhas; se paga: nunca.

   **Decidido — o voto e o argumento mais forte a favor e contra**; a memória `consultant-debate-shown-in-full` foi emendada no mesmo dia.

### Rodada 3 — as primitivas do `brza sessions` e o painel (enviada 2026-11-08)

**Apresentado antes:** os desenhos D2 ([PLN-017 — Desenho: as primitivas do `brza sessions` (D2)](PLN-017-design-cli.md)) e D3 ([PLN-017 — Desenho: o painel da rodada (D3)](PLN-017-design-painel.md)), com o artboard do painel nas duas situações (durante a rodada, com uma persona faltando, e fechada): o recibo de hoje esconde a recusa, porque o `rpc()` só erra quando o transporte falha; o contrato do `brza chat send` da branch do PLN-011 serve de forma; o `wait` fecha a rodada por estado, `updatedAt` e fila; 11,5 h no total, sem colisão com o PLN-012; o painel de equipe do Orca lê o banco de orquestração e foi desligado duas vezes pelo upstream.

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **O recibo e o `read`.** A R1.4 do PLN-010 decidiu "falha com aviso, sem cair no `rpc` antigo"; isto é uma exceção de transição, a escrever no PLN-010:
   - recibo (`queued|accepted|rejected|unknown`) e `--operation` pelo `rpc`, na forma do `brza chat send`, sem `read` (recomendada) — custo: 2 h agora e ~0,5 h no PLN-010 para trocar o transporte; a pergunta de uma persona `blocked` só se vê abrindo a aba; se paga: na próxima reunião, porque o `wait` precisa do id da fila;
   - recibo, `--operation` e `read --last` pelo `rpc` — custo: ~3 h e exceção maior à R1.4, que passa a cobrir a leitura; se paga: na primeira persona `blocked` ou que terminou o turno sem marcador;
   - sem exceção: só o envio a vários nomes e `--file` — custo: 0,5 h; o `wait` perde a checagem da fila; se paga: quando o Studio fundir a branch do PLN-011.

   **Decidido — recibo, `--operation` e `read --last` pelo `rpc`**: o D2 ganha o verbo `read --last` (1 h), e a exceção à R1.4 do PLN-010 cobre o envio e a última resposta.

2. **O fim de rodada e a medição.**
   - `wait` por estado, fila e `updatedAt`, com o marcador como confirmação e `--any`; a latência no mapa; `usage` com o Claude pelo hook e os tokens do Codex pelo rollout; Grok e Antigravity `unmeasured` (recomendada) — custo: 4,5 h, sem tocar o `measure.py`; se paga: na próxima reunião com Codex;
   - o mesmo `wait`, só latência — custo: 3 h; se paga: agora, com o custo do Codex à mão;
   - só marcador, sem medição — custo: 1 h; a persona que caiu de cota só aparece no timeout; se paga: agora, com personas disciplinadas.

   **Decidido — `wait` completo, latência e `usage` do Codex.**

3. **O ciclo do painel.** O app relê o visual só quando uma mensagem nova o monta:
   - um arquivo por rodada, republicado na abertura, a cada resposta nova e no fechamento; a rodada seguinte com nome novo (recomendada) — custo: 3 a 5 mensagens curtas por rodada, 0 h a mais no gerador; se paga: na primeira reunião, a única que dá "quem falta, em tempo real" sem código no app;
   - um visual por rodada, só no fechamento — custo: 1 mensagem por rodada; se paga: agora, sem o tempo real da R1.4;
   - um placar único da reunião, sempre o mesmo arquivo — custo: mais ~1 h no render; se paga: na primeira reunião, perdendo o histórico de cada rodada.

   **Decidido — um arquivo por rodada, republicado durante ela.**

4. **O painel de equipe do Orca (`orchestration-crew`).** Lê o banco de orquestração, onde os chats do `brza sessions` não estão; o upstream o desligou duas vezes em dois dias:
   - não religar; seguir com o `::orca-visual` e reavaliar na fase do painel por plugin, com três ou mais reuniões (recomendada) — custo: 0 h; se paga: agora;
   - religar atrás de flag, só para medir — custo: 1 a 3 h, e sai vazio para os chats do `brza sessions`; se paga: nunca para a reunião;
   - religar e adaptar à reunião — custo: 25 a 60 h, no caminho da regressão e numa pasta que o upstream refatora; se paga: só com reunião diária e o plugin a mais de dois meses.

   **Decidido — não religar**; a fase do painel fica registrada na issue ao `studio`.

### Rodada 4 — o corte em passos (enviada 2026-11-08)

**Apresentado antes:** a tabela dos oito passos derivados de D1 a D3, com executor e estimativa: P1 skill 10,5 h; P2 painel 6,5 h; P3 duas issues 1 h; P4 verbos do `brza sessions` 11,5 h; P5 `brza shot` 1 h; P6 emenda ao PLN-010 0,5 h; P7 reunião de verificação 1,25 h; P8 fechamento 0,5 h; 32,75 h no total, 20,75 aqui e 12 nos outros workstreams.

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **O corte.** A opção que aceita é o aceite do plano:
   - aceitar os oito passos (recomendada) — custo: 32,75 h; se paga: a primeira reunião pela skill roda com P1 e P2, sem esperar o CLI;
   - juntar P1+P2 e P3+P8, P4 e P6 numa issue — custo: as mesmas horas, revisão em blocos maiores; se paga: se uma sessão só fizer P1 e P2 de uma vez;
   - dividir P4 em envio/espera (P4a: `open`, `send`, `wait`, `read --last`, `close`, 8 h) e medição (P4b: `list`, `model`, `usage`, 3,5 h) — custo: duas revisões no `tools-kit`; se paga: se a próxima reunião vier antes de P4 fechar e precisar só do `wait`;
   - só as issues agora, skill e painel depois — custo: 1 h; se paga: nunca para a próxima reunião.

   **Decidido — dividir P4 em P4a e P4b**; o plano está aceito com nove passos e as mesmas 32,75 h.

2. **O que executar agora.**
   - P3 agora e abrir a sessão de P1+P2 pelo `brza sessions` (recomendada) — custo: ~1 h aqui e ~17 h e US$ 15 a 30 na sessão nova; se paga: a próxima reunião já roda pela skill;
   - só P3 agora — custo: ~1 h; se paga: agora;
   - nenhum agora, fechar e compactar — custo: 0 h; se paga: se Anderson quiser rever o desenho antes.

   **Decidido — P3 agora e abrir a sessão de P1+P2.**

### Rodada 5 — o ciclo de vida das sessões abertas pela coordenação (enviada 2026-11-08)

**Apresentado antes:** nada; o requisito veio de Anderson, na sessão `workflow-improvements`, depois de o plano ter sido aceito em R4 e com P1 e P2 em execução na sessão `pln-017-skill`.

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **O ciclo de vida das personas.** **Resposta:** "as sessões abertas pelo coordenador devem abrir como o `orca-orchestrator` faz, fechando sozinho 2min após não ser mais necessário, com o botão de `manter aberta` acima do input de conversa do chat". **Decidido — requisito do fluxo**: toda sessão que a coordenação abre tem o ciclo de vida dos workers do orquestrador do Orca (fechamento automático cerca de 2 min depois de deixar de ser necessária, com o botão "manter aberta" no chat). O "como" é desenho: o D2 (a abertura pelo `brza sessions`) e o D1 (a abertura e o encerramento na skill) são reescritos a partir do mecanismo do Studio (`worker-start --keep-open`, `autoReleaseAt`, `orchestration.worker-auto-release.v1`), e a via escolhida vai a rodada se houver mais de um caminho defensável.

### Rodada 6 — o ciclo de vida das personas: a via, o fim e a superfície (enviada 2026-11-08)

**Apresentado antes:** o mapa do mecanismo no `brza-studio`, lido por um `collector`: o prazo de 2 min é a constante `WORKER_TERMINAL_AUTO_RELEASE_GRACE_MS` (`src/main/runtime/orchestration/db/worker-terminal/worker-terminal-auto-release.ts:10`), armada só por um `worker_done` aceito (`worker-report-settlement.ts:280-281`); o fim de turno de um chat sem `worker_done` não arma nada, o host só avisa "Worker stopped without reporting" (`worker-turn-stop-report.ts:74-130`); o worker em trabalho suspende a contagem, que recomeça com mais 2 min ao repousar (`worker-auto-release-activity.ts:32-55`); a faixa com o botão "Keep open" (`NativeChatStructuredWorkerLifetimeStrip.tsx`) só aparece em aba com Dispatch de orquestração (`renderer/src/lib/worker-auto-close.ts:85-125`); um chat aberto por `agent launch` não recebe nada disso sem 20 a 40 h de código no fork, com conflito de merge alto; o `worker-start --spec` não precisa de `run-create`, exige identidade do chamador (`ORCA_AGENT_SESSION_ID` ou terminal ativo), segue o ajuste Chat|CLI por agente (sem `--surface`; o padrão de fábrica é terminal), entrega o `--spec` com o preâmbulo do Orca como turno do coordenador, não nomeia o chat em worktree existente, e o worker precisa enviar `worker_done`; a variante híbrida (chat por `agent launch --surface chat` tornado worker por `worker-start --terminal orca_session_id:<chat>`) não foi testada e, pelo código, provavelmente não fecha sozinha (terminal reusado não é fechado). O MCP do `brza-workflow` já abre workers por esse caminho (`cycle.py:136-167`).

Respondida em 2026-11-08, na sessão `workflow-improvements`.

1. **A via.**
   - testar a híbrida em 1 a 2 h e, se o fechamento automático não valer, a via A pura: o `brza sessions open` passa a chamar `worker-start --spec --agent --model --effort --worktree path:` (recomendada) — custo: 1 a 2 h de sonda e 6 a 12 h no `brza-workflow`; se paga: na próxima reunião, com botão nativo e zero código no Studio;
   - `worker-start` puro, sem a sonda — custo: 6 a 12 h; a superfície segue o ajuste por agente e o nome visível se perde; se paga: na próxima reunião;
   - o ciclo de vida no `agent launch`, no Studio — custo: 20 a 40 h no fork, com conflito de merge alto; se paga: só se a via A falhar em "chat garantido" e "nome visível";
   - o `brza sessions` fechando por CLI, sem botão — custo: 3 a 6 h; não cumpre o requisito; se paga: nunca como substituto.

   **Decidido — testar a híbrida; se falhar, `worker-start` puro.**

2. **O fim de cada rodada e o "não ser mais necessário".** O `worker_done` arma os 2 min; entre rodadas a coordenação leva de 2 a 7 min para sintetizar:
   - o marcador no worklog segue por rodada e o `worker_done` vai só no encerramento, quando a coordenação manda a mensagem final (recomendada) — custo: uma linha no pedido de encerramento; se paga: já, a persona não fecha no meio da síntese;
   - `worker_done` a cada rodada, com `worker-keep-open` da coordenação depois de cada um e `worker-release` no fim — custo: dois comandos por persona por rodada, e a persona fecha se a coordenação atrasar 2 min; se paga: só se o `worker_done` virar o recibo da rodada;
   - mensagem de mailbox por rodada (`brza orchestration send`) e `worker_done` no encerramento; o `check --wait` substitui o `grep` do marcador — custo: um comando por persona por rodada, e o `wait` do D2 muda para `check --wait`; se paga: quando a espera virar nativa, sem polling de arquivo.

   **Resposta:** "Mensagem de mailbox por rodada; worker_done no fim". **Decidido — a persona envia `brza orchestration send` à coordenação ao fechar cada rodada e o `worker_done` só no encerramento**; o `wait` do D2 vira `check --wait`; o marcador no worklog fica como registro escrito, não como sinal.

3. **A superfície dos agentes no app.** O `worker-start` abre como chat só se o ajuste Chat|CLI do agente for Chat:
   - Claude, Codex, Grok e Antigravity em Chat — custo: 0; se paga: já;
   - não sei; a sonda confere — custo: incluído no teste;
   - algum em CLI — custo: a troca do ajuste no app, uma vez.

   **Decidido — os quatro em Chat**: a via A abre chats sem mexer no ajuste.

### Rodada 7 — `close` com Dispatch ativo (2026-11-09)

**Apresentado antes:** D2:447 previa `worker-release` para quem não respondeu; o `worker-release --help` instalado só libera workers settled. A sonda de P4 confirmou essa restrição. O guia `recovery-and-cleanup.md` exige parada confirmada e preservação de identidade, custódia e Keep open.

1. **Como `close` trata um worker ainda ativo?**
   - Pedir encerramento; `--force` usa parada guardada (Recomendado). Custo: implementar e testar pedido por mailbox, estado `closing` e protocolo de parada com confirmação; `--force` pode interromper trabalho ativo. Se paga: ao encerrar uma persona travada, preservando a função do `--force`.
   - Recusar worker ativo, mesmo com `--force`. Custo: uma etapa manual para encerrar personas travadas; implementação menor agora. Se paga: nesta entrega, mantendo apenas a liberação de workers já encerrados.

**Resposta literal de Anderson**, em 2026-11-09, sessão `Retomar PLN-017`: "Pedir encerramento; --force usa parada guardada (Recomendado). Custo: implementar e testar pedido por mailbox, estado closing e protocolo de parada com confirmação; --force pode interromper trabalho ativo. Se paga: ao encerrar uma persona travada, preservando a função do --force."

**Escolhida a primeira opção:** D2 atualizado; instrução enviada ao Dispatch `ctx_f0b0d3dbd714`. Parada incerta não conta como fechamento e não autoriza repetição cega ou abandono.

## Passos

### P1 — A skill `meeting-runner` v1

Executa D1 · executor: sessão nova deste worktree (`pln-017-skill`), com o plugin `skill-creator` carregado

Estimado: 10,5 h · Executado: ~4 h (estimativa de relógio ativo; sem medição)

- [x] **1. `/skill-creator`**: capturar a intenção a partir do D1 e escrever `.claude/skills/meeting-runner/SKILL.md` (abaixo de 500 linhas, descrição com o gatilho negativo "não use se você é uma persona"), as oito `references/` e os quatro `scripts/` (`launch_persona.py`, `wait_round.py`, `tally.py`, `runtime_memory_check.py`)
- [x] **2. Os casos de teste** em `evals/evals.json`: o briefing a partir do gate do tema; a síntese da rodada 3 da reunião MCP a partir dos seis worklogs de 2026-11-07; o `tally.py` refazendo as tabelas por persona do levantamento; as rodadas com e sem a skill, a nota e o visor, no scratch da sessão
- [x] **3. A revisão** pelo laço da `skill-creator` e pelo `reviewer`; o teste de aceite do `tally.py` contra as tabelas das coordenações (com as duas divergências conhecidas)
- [x] **4. `brza note commit`** da skill e do worklog da sessão

**Evidência:** `brza-workspace@bf06d0a` (a branch `workstream/playground`); `.claude/skills/meeting-runner/` (`SKILL.md` com 199 linhas, 8 `references/`, 5 scripts, `evals/evals.json` com 3 casos); `cd .claude/skills/meeting-runner && python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'` → 149 testes, OK; aceite do `tally.py` contra `levantamento-processo.md` 3.1 e 3.2 (confiança R1, voto R3, nota dos colegas com as duas variantes, sala 61,8/56,5/57,2, latência e custo de Muralha, Régua e da R7 da Carvão), sem divergência numérica; avaliação com e sem a skill: iteração 1, 100% × 88,9%; iteração 2, 100% × 81,8% (+22 s e +16 mil tokens por tarefa); revisão do `reviewer`: 2 bloqueiam, 15 a corrigir e 8 de melhoria, todos corrigidos salvo M5 e M7, **sem nova revisão das correções**. Fica de fora: a abertura e o encerramento pelo ciclo de vida dos workers e o `wait_round --source mailbox`, nunca rodados contra o Studio ([worklog](../../work/worklogs/2026-11-09-pln-017-p1-p2-a-skill-meeting-runner.md)).

### P2 — O gerador do painel da rodada

Executa D3 · executor: a sessão de P1

Estimado: 6,5 h · Executado: ~2 h (estimativa de relógio ativo; sem medição)

- [x] **1. `scripts/panel.py`** com `collect` (mapa, `brza sessions list --json`, marcadores, blocos do molde, `measurements.jsonl`, rollouts do Codex, `sintese-N.json` → `estado-rN.json`) e `render` (JSON → HTML na forma da `orca-chat-visuals`), a partir do protótipo do scratch
- [x] **2. Os moldes**: a linha `**Posição:**` no pedido de rodada, o `sintese-N.json`, o ciclo de publicação (abertura, cada resposta, fechamento; nome novo por rodada) e a conferência por PNG na skill
- [x] **3. Testes `unittest`** com o estado da rodada 3 (fechada e às 21h29) e uma persona sem medição
- [x] **4. Commit** junto de P1

**Evidência:** `brza-workspace@bf06d0a`; `scripts/panel.py` (`collect`, `render --publish-dir`, `--png`) e os testes de `panel`, com a R3 da reunião MCP fechada e às 21:29:30, persona sem medição, `sem cota`, `erro`, voto e a integração com o `tally.py` sobre os worklogs reais; o PNG a 736 px conferido nas duas situações depois das correções da revisão, com os defeitos cosméticos registrados no worklog (cartão de custo ignora o `--at`; denominador da sala). A média da sala exclui o Antigravity (57,2 em 5 de 6, "Antigravity à parte: 85"), pela E-1 do D1.

### P3 — As duas issues

Executa D2, D3 · executor: a sessão que conduz

Estimado: 1 h · Executado: 1 h

- [x] **1. Ao `tools-kit`**: [O `brza sessions` ganha os verbos da reunião multiagente: modelo na abertura, recibo, `wait`, `read --last`, `model`, `usage` e `close --prefix`](../../work/issues/o-brza-sessions-para-a-reuniao-multiagente.md), com P4a, P4b, P5, P6 e a exceção à R1.4 do PLN-010
- [x] **2. Ao `studio`**: [A fase do painel da reunião no BrzA Studio: argumentação por persona, abrir o chat, gate de decisão e atualização ao vivo](../../work/issues/a-fase-do-painel-da-reuniao-no-brza-studio.md), com o `orchestration-crew` fora

**Evidência:** `brza-workspace@cea9595`, os dois arquivos em `work/issues/`; `python3 .claude/skills/notes-checker/scripts/check_notes.py` → erros: 0, avisos: 0

### P4a — A abertura com ciclo de vida, o envio e a espera do `brza sessions`

Executa D2 (revisto pela R5 e R6) · executor: sessão do `tools-kit`, no `brza-workflow`, a partir da issue de P3

Estimado: 10 h · Executado: incluído nas 1,109 h agregadas de P4a/P4b/P6, sem rateio por passo

- [x] **0. A sonda da híbrida (1 a 2 h):** abrir um chat por `agent launch --surface chat --model --effort` e torná-lo worker por `worker-start --terminal orca_session_id:<chat> --spec …`; conferir se o `autoReleaseAt` vale depois do `worker_done`, se a faixa "Keep open" aparece e se o `brza orchestration send` da persona chega à coordenação; anotar a superfície que cada um dos quatro agentes abre pelo `worker-start --spec`. O resultado decide entre a híbrida e a via A pura
- [x] **1. A sonda do resto** com chats reais: `setOption`, reenvio com a mesma `operation`, `updatedAt` ao entrar em `working`, identidade do chamador fora do chat do Studio
- [x] **2. Testes que falham antes**, em `tests/cli/test_brza_sessions.py`, um por verbo: `open` pela via decidida (grava `dispatch` e `model`/`effort` no mapa), `send` com recibo e `--operation`, `wait` sobre `check --wait` (mensagem de fim de rodada por persona, `worker_done`, timeout, `blocked`/`failed` pelo estado), `read --last`, `close` por `worker-release` e `worker-keep-open`
- [x] **3. Implementar** pela menor mudança do D2; o `launch.py` sai; o `wait` por estado e fila fica como fallback para chat sem Dispatch
- [x] **4. `python3 -m unittest discover -s tests/cli -p test_brza_sessions.py`** com `env -u BRZA_WORKSPACE`, revisão e merge na `master` do `brza-workflow`

**Evidência:** `brza-workflow@3d3d2bb`, publicado na `master`; snapshot de 90 testes verdes, sondas reais dos quatro runtimes e revisão independente REV-022. Híbrida sem auto-release selecionou a via pura de R6; encerramento conforme R7.1.

### P4b — Os verbos de medição do `brza sessions`

Executa D2 · executor: sessão do `tools-kit`, no `brza-workflow`

Estimado: 3,5 h · Executado: incluído nas 1,109 h agregadas de P4a/P4b/P6, sem rateio por passo

- [x] **1. Testes que falham antes**: `list` com modelo, esforço e último turno; `model` com `model` e depois `effort`; `usage` com o Claude pelo hook, o Codex pelo rollout (fixture com `info: null`) e Grok/Antigravity `unmeasured`
- [x] **2. Implementar**, sem tocar o `measure.py`
- [x] **3. Rodar, revisar e mesclar**

**Evidência:** `brza-workflow@db6bd28`, publicado na `master`; 100 testes específicos verdes (dez sobre o snapshot de P4a), 580 na CLI ampla antes do último teste somente de regressão, sem mudança posterior de produção; REV-022 sem bloqueios.

### P5 — O `brza shot` lê o CSS atual do Studio

Executa D2 · executor: sessão da `master` do `brza-workspace`

Estimado: 1 h · Executado: 0,174 h (janela da sessão executora, incluindo fechamento)

- [x] **1. Teste que falha antes** em `scripts/brza/tests/test_brza_shot.py`, com a fixture na forma `visualBaseCss(true)`
- [x] **2. `base_css_call`** ao lado do `string_concat` em `scripts/brza/brza-shot:162-166`
- [x] **3. `python3 -m unittest discover -s scripts/brza/tests`** e commit na `master`

**Evidência:** `brza-workspace@b24de7c1f1324b2ea85df061b57765ea500ff0bc`, publicado na `master`; vermelho com 2 `ShotError BASE_CSS`, verde com 99 testes. Reviewer independente Claude `opus`, Dispatch `ctx_7153fa486731`: cli 492, hooks 291 e notes-checker 26/26; captura real 1472×108; A1 de cobertura corrigido e verificado por mutação. [PLN-017/P5: o brza shot lê visualBaseCss e mantém o literal antigo](../../../workspace/work/worklogs/2026-11-09-pln-017-p5-brza-shot.md), publicado no `workstream/workspace` em `8f6846f`.

### P6 — A emenda ao PLN-010

Executa D2 · executor: sessão do `tools-kit`

Estimado: 0,5 h · Executado: incluído nas 1,109 h agregadas de P4a/P4b/P6, sem rateio por passo

- [x] **1. Registrar no PLN-010** a exceção à R1.4, citando PLN-017/R3.1 ("Recibo, --operation e read --last pelo rpc", 2026-11-08, sessão `workflow-improvements`), e o que a troca de transporte custa quando o `brza chat` chegar

**Evidência:** `brza-workspace@ff8def8` e `0cbeb26`, publicados em `workstream/tools-kit`; exceção à R1.4 registrada no PLN-010 com resposta literal, data, sessão e estimativa de 0,5 h para a troca futura do transporte; REV-022 sem bloqueios.

### P7 — A reunião de verificação

Executa D1, D3 · executor: a sessão de coordenação da reunião, neste worktree

Estimado: 1,25 h · Executado: ~0,7 h (estimativa de relógio ativo, 13:13–13:36 e 18:36–18:50; a sessão mediu US$ 13,64 com a pausa de ~5 h)

- [x] **1. Três personas, duas rodadas**, pela skill e com o painel republicado por rodada, sobre um tema pequeno do `playground` — três personas (Claude, Grok, Antigravity), R1 e R2 e uma R3 extra para duas personas, por escolha de Anderson (alternativa C)
- [x] **2. O que desviar** do fluxo volta a D1 como desvio `X`; a primeira das duas reuniões sem desvio que o critério de promoção pede — 19 desvios em D1; esta reunião **não conta** como sem desvio

**Evidência:** [Reunião CI no chat: a coordenação da reunião de verificação do PLN-017](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-coordenacao.md), com a proposta v2 copiada, as tabelas por persona do `tally.py`, os custos e os 19 desvios; os worklogs das personas [Prumo](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-prumo.md), [Trava](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-trava.md) e [Relance](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-relance.md). Verificado contra o Studio: `worker-start` em três agentes no Run `run_fe70b351bc36`; o `fim-rodada-N` por mailbox de todas; o ciclo da R5 (5 h parada sem fechar, `autoReleaseAt` ~2 min depois do `worker_done` aceito); o painel por rodada conferido por PNG; o revisor independente (78). Não verificado: os verbos v2 do `brza sessions` (a reunião usou os scripts v1). As decisões de Anderson ("2, 3 e 4 decididos"; "1A decidido") estão na issue de origem emendada e em [O follow-up automático de CI espera o gatilho de uso, com a contenção já desenhada](../../work/issues/o-follow-up-automatico-de-ci-espera-o-gatilho-de-uso.md) e [O CI agendado do `brza-studio` falha sem ninguém ver](../../work/issues/o-ci-agendado-do-brza-studio-falha-sem-ninguem-ver.md).

### P8 — O fechamento

Executor: a sessão que conduz

Estimado: 0,5 h · Executado: — h

- [ ] **1. A issue de origem** ganha o destino (este plano) e fecha quando P1, P2 e P7 fecharem
- [ ] **2. O critério de promoção ao `core/`** (duas reuniões sem desvio) registrado numa issue ao `workspace` quando a primeira reunião fechar
- [ ] **3. O worklog** e o `Retomar`

**Evidência:** —

## Worklogs

- 2026-11-09 — P7: a reunião de verificação "CI no chat" pela skill, três personas em três runtimes via `worker-start`, R1, R2 e R3 extra; Anderson decidiu os quatro pontos; três issues; 19 desvios a D1, a reunião não conta como sem desvio.
  [Reunião CI no chat: a coordenação da reunião de verificação do PLN-017](../../work/worklogs/2026-11-09-reuniao-ci-no-chat-coordenacao.md)

- 2026-11-09 — P4a/P4b/P6 concluídos e publicados; sondas reais, 100 testes específicos, 580 CLI ampla e REV-022; 1,109 h medidas da executora, sem intervalo suspenso nem rateio inventado.
  [O `brza sessions` recebe as primitivas da reunião e o PLN-010 registra a transição pelo `rpc`](../../../tools-kit/work/worklogs/2026-11-09-pln-017-sessions-e-excecao-ao-pln-010.md)

- 2026-11-09 — coordenação de P4/P5/P6; R7 escolhe o encerramento e a parada guardada; P4/P5/P6 concluídos, revisados e publicados; P7 fica para a próxima execução.
  [PLN-017: coordenação de P4, P5 e P6 e encerramento de workers](../../work/worklogs/2026-11-09-pln-017-coordenacao-p4-p5-p6.md)
- 2026-11-09 — P5 executado na `master`, 99 testes e revisão independente; commit `b24de7c` publicado.
  [PLN-017/P5: o brza shot lê visualBaseCss e mantém o literal antigo](../../../workspace/work/worklogs/2026-11-09-pln-017-p5-brza-shot.md)

- 2026-11-09 — P1 e P2: a skill `meeting-runner` v1, o `panel.py`, 149 testes, a avaliação com e sem a skill (100% × 81,8%), a revisão (25 achados, corrigidos salvo 2) e a R5/R6 aplicada nos scripts, só em `--dry-run`. Nada testado contra o Studio.
  [PLN-017 P1 e P2: a skill `meeting-runner` e o gerador do painel](../../work/worklogs/2026-11-09-pln-017-p1-p2-a-skill-meeting-runner.md)

- 2026-11-09 — retomada: protótipo de P1/P2 sem commit; 102 testes, 7 falhas e 1 erro; checador de notas sem erros nem avisos. Nenhum passo fechado.
  [PLN-017: retomada e conferência do protótipo da skill](../../work/worklogs/2026-11-09-pln-017-retomada.md)

- 2026-11-08 — R1 a R4: destino, primitiva, UI, narração, a skill, o CLI, o painel e o corte; D1 a D3 gravados; P3 feito (`cea9595`). Parou ao abrir a sessão `pln-017-skill` para P1 e P2.
  [O fluxo de reunião multiagente vai a plano: as duas reuniões medidas e a rodada 1](../../work/worklogs/2026-11-08-o-fluxo-de-reuniao-multiagente-vai-a-plano.md)

## Revisões

- [REV-022: As primitivas do brza sessions e a exceção transitória do PLN-010](../../../tools-kit/work/reviews/REV-022-pln-017-sessions-e-transicao-rpc.md) — concluída, achados corrigidos e hipóteses falsas documentadas; P4a/P4b/P6 sem bloqueios.

## Pendências conhecidas

- [O `brza sessions` ganha os verbos da reunião multiagente: modelo na abertura, recibo, `wait`, `read --last`, `model`, `usage` e `close --prefix`](../../work/issues/o-brza-sessions-para-a-reuniao-multiagente.md) — de P3; P4a/P4b/P5/P6 concluídos, com evidências nos passos; a integração na reunião fica para P7.
- [A fase do painel da reunião no BrzA Studio: argumentação por persona, abrir o chat, gate de decisão e atualização ao vivo](../../work/issues/a-fase-do-painel-da-reuniao-no-brza-studio.md) — de P3; registro para o `studio`, sem pedido de execução.
- [Resultados de CI no chat e disparo automático de agentes em falhas de PR](../../work/issues/resultados-de-ci-no-chat-e-disparo-automatico-de-agentes-em-falhas-de-pr.md) — o tema da reunião de P7; emendada com o destino de cada PR e aberta até o merge de tag trazer o visual.
- [O follow-up automático de CI espera o gatilho de uso, com a contenção já desenhada](../../work/issues/o-follow-up-automatico-de-ci-espera-o-gatilho-de-uso.md) — de P7, ao `tools-kit`, `low`; decisão 1A de Anderson.
- [O CI agendado do `brza-studio` falha sem ninguém ver](../../work/issues/o-ci-agendado-do-brza-studio-falha-sem-ninguem-ver.md) — de P7, ao `studio`, `low`; decisão 4 de Anderson.
