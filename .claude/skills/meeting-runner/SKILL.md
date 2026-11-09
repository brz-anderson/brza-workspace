---
name: meeting-runner
description: >-
  Conduz uma reunião multiagente com personas: a sessão de coordenação abre N chats do BrzA Studio em runtimes, modelos
  e esforços diferentes, roda rodadas (opinião, debate, voto e notas, confiança final), sintetiza, confere os números,
  chama o revisor independente e leva as decisões a Anderson, narrando no chat quem respondeu, a posição, a confiança e o
  painel de cada rodada. Use sempre que o pedido for "monte uma reunião sobre X", "reunião com personas", "replique a
  reunião do Carvão em Brasa / do MCP remoto", "abra seis personas para debater", "rodada de debate entre sessões",
  mesmo que a palavra "skill" não apareça. Não use se você é uma persona da reunião (o seu prompt diz "você é uma
  persona"): a persona só segue o briefing e escreve no worklog dela. Não use para consultores em paralelo por `Agent`
  (isso é o laço consultor do `plan-runner`) nem para uma conversa de uma sessão só.
---

# Reunião multiagente — preparar, conduzir, sintetizar e fechar

Duas reuniões de 2026-11-07 (Carvão em Brasa, MCP remoto) provaram que personas diversas destrincham os fatos e levam
decisões mais maduras a Anderson, mas deixaram 15 de 32 itens do protocolo implícitos e custaram quatro rodadas no tema
errado, duas personas na cota do Codex e a conta de médias errada. Esta skill fixa o fluxo e os números, para a próxima
reunião rodar sem improviso. Estado: **v1, protótipo** — vive na branch `workstream/playground` e vai ao `core/` do
`brza-workflow` depois de duas reuniões sem desvio de fluxo (PLN-017/R2.1). A primeira reunião pela skill (P7,
2026-11-09) teve 19 desvios e não conta; as correções deles estão nos passos abaixo, marcadas `(X…)`.

## Quem é quem

- **A coordenação** é a sessão principal: pergunta a Anderson, abre as sessões, sintetiza, confere números, grava.
- **As personas** são workers do Orca em chat, que escrevem só no worklog delas; nunca perguntam, nunca commitam.
- **Anderson decide.** A coordenação não decide: a rodada de decisões leva as opções, e decisão só vale com a frase
  explícita ("decidido", "fechado", "pode aplicar"). A norma de rodadas é a do `AGENTS.md`; esta skill não a repete.

## Os arquivos e quando ler

| Preciso de… | Leia / rode |
| :--- | :--- |
| o briefing da reunião, e conferir os números dele | `references/briefing.md`; `$S/check_briefing.py <dir>/briefing.md` |
| uma persona (arquétipo, papel → modelo, régua da confiança) | `references/persona.md` |
| o esqueleto do worklog de uma persona | `references/persona-worklog.md` |
| o pedido de uma rodada (os cinco tipos, a linha `**Posição:**`) | `references/round-request.md` |
| a síntese, o `sintese-N.json` do painel | `references/synthesis.md` |
| a proposta, a confiança do plano, o revisor, a contraprova | `references/proposal.md` |
| a rodada de decisão, o worklog da coordenação, o encerramento | `references/closing.md` |
| o que dizer no chat, o ruído do host e o ciclo do painel | `references/narration.md` |
| abrir as personas | `$S/launch_persona.py $R` |
| enviar a rodada N | `$S/launch_persona.py $R --send todas --round N` |
| esperar o fim da rodada | `$S/wait_round.py N --reuniao $R [--personas …]` |
| pedir o encerramento, conferir o aceite, forçar | `$S/launch_persona.py $R --close`, `--status --wait-settled 180`, `--stop <persona>` |
| a tabela por persona, sem conta à mão | `$S/tally.py N --reuniao $R --opened HH:MM:SS --closed HH:MM:SS --settle 60` |
| o painel da rodada | `$S/panel.py collect N --reuniao $R --opened … [--closed …]` e `$S/panel.py render …` |
| a memória de runtime fora do repositório | `$S/runtime_memory_check.py <início>` |

**Convenção dos comandos:** rodam da raiz do worktree, com `python3 -I .claude/skills/meeting-runner/scripts/<script>.py`
(abaixo, `$S`); a raiz padrão dos scripts é a do git, e o manifesto é `.sessions/<reuniao>/reuniao.json` (`$R`). Os
caminhos relativos do manifesto resolvem contra essa raiz.

**O transporte é o `brza sessions` v2** (PLN-017 P4a/P4b, `brza-workflow@db6bd28`): o `launch_persona.py` e o
`wait_round.py` só traduzem o manifesto para os verbos dele (`open`, `send`, `wait`, `close`) e narram a saída. Quem abre o
worker, anexa o protocolo da rodada, lê a mailbox do Run sem consumi-la e decide o que é fechado é o CLI. O mapa
`.sessions/sessions.jsonl` da raiz comum do git guarda, por nome, o Dispatch, o Run, o remetente, a coordenação, o modelo
e o id do provedor; a medição e a espera leem dele, também depois do fechamento automático.

O **manifesto** `reuniao.json` (nome, slug, papel, runtime, modelo, esforço, sessão, fallback de cada persona, mais o
tema, a pasta da reunião e o molde do caminho dos worklogs) é a fonte única da abertura, das tabelas e do painel; o
schema está no docstring de `scripts/tally.py`. Crie-o no Passo 1, na pasta da reunião (`.sessions/<reuniao>/`).

## Passo 0 — o gate do tema, antes de qualquer arquivo

A reunião MCP perdeu quatro rodadas porque o briefing dizia "MCP" e a pergunta era sobre o MCP do `brza-workflow`.
Por isso nenhuma sessão abre antes da confirmação:

- Rodada curta com Anderson (pergunta com opções): o objeto em uma frase, o que está **fora**, a saída esperada e a hora
  de fim. A leitura da coordenação vai como primeira opção, com a fonte.
- A resposta literal vai ao topo do briefing. Sem resposta, nenhuma sessão abre.
- Correção de tema no meio: a rodada em curso fecha, e o material fora do tema é descartado por escrito na síntese.

## Passo 1 — preparar

- Levantamento longo vai ao `collector`, em paralelo; a R1 não espera por ele.
- Briefing pelo molde (`references/briefing.md`). A restrição do tema (segurança da sala, por exemplo) é um slot do
  molde, não improviso.
- **Os números do briefing se conferem antes de abrir (X8).** Na P7, o "O que existe hoje" levou 1.352 arquivos em vez de
  163, e duas personas herdaram o erro. Cada item com número leva `conferido às HH:MM: \`comando\` → resultado`, rodado
  pela coordenação agora, e `$S/check_briefing.py <dir>/briefing.md` sai 0 antes do Passo 2.
- Personas pelo molde (`references/persona.md`). **Modelo e esforço pelo papel, e nunca dois papéis no mesmo modelo e
  esforço** (memória `meeting-model-per-role`): é o que fez a posição ser da persona e a confiança ser do modelo.
- Cota: `brza quota --json` antes de abrir. Runtime acima de 55% na janela de sessão não hospeda papel crítico. O
  medidor/cético e o de segurança ficam em runtimes diferentes, e toda persona tem `fallback` no manifesto.
- O worklog de cada persona nasce pelo molde (`references/persona-worklog.md`), criado pela coordenação antes de abrir
  a sessão.
- **Antigravity: no máximo uma cadeira**, em papel de ideação ou de usuário, sem modelo explícito (o chat recusa), e a
  confiança dele sai da média e do número do plano, relatada à parte. Foi o mais confiante e o de pior nota nas duas
  reuniões; o número que ele trouxer passa pela conferência antes da síntese.

## Passo 2 — abrir as sessões

- **`$S/launch_persona.py $R`** abre cada persona por `brza sessions <sessao> --agent … --model … --effort …
  --prompt-file … --wait`, **uma de cada vez**: a primeira abertura cria o Run e as outras entram nele. No fim ele imprime
  a tabela da narração (persona, papel, runtime, modelo, esforço, Dispatch, Run, id do provedor) e sai 1 se as personas
  ficaram em mais de um Run. Não relance persona que "abriu sem o id do provedor": o `wait` grava o id depois (X1). Não
  relance a que "não abriu" antes de ler o `pending-*.json` que o CLI cita.
- **O ciclo de vida é o dos workers do Orca** (R5 de Anderson): depois do `worker_done` aceito, a sessão fecha sozinha ~2
  min depois, e o chat mostra "manter aberta" para Anderson guardar a que quiser consultar. Uma pausa longa entre rodadas
  não fecha ninguém: o prazo só arma no `worker_done` (P7: 5 h de pausa, X15).
- **O prompt de abertura** é de uma linha por persona, guardado em `prompt-<slug>.txt`, e é a rodada 1. Começa com "Você
  é uma persona numa reunião multiagente": é o que impede a persona de acionar esta skill. Não traz comando
  `brza orchestration` próprio: o CLI anexa a cada pedido o protocolo do status da rodada, com o `round_id` e o Dispatch
  reais. O `worker_done` é só do encerramento e sai **do preâmbulo do Orca, com o `--task-id` e o `--dispatch-id` dele**
  (X19: o comando que a skill dava sem os ids foi recusado, "worker_done requires taskId").
- Narre a abertura (`narration.md`).

## Passo 3 — conduzir uma rodada

- O pedido sai do molde (`references/round-request.md`), com **duração** ("~5 min"), não hora: os prazos das duas
  reuniões não eram monotônicos e ninguém os cobrou.
- **Enviar:** `$S/launch_persona.py $R --send todas --round N` chama `brza sessions send … --text "Faça a rodada N:
  <dir>/rodada-N.md"` e mostra o recibo por persona. O CLI anexa o protocolo da rodada; a mensagem chega como turno do
  coordenador, e não como mensagem de mailbox, por isso não há "Re: rodada" (X9). **`pending` ou `unknown` (saída 75)
  não é falha nem sucesso** (R2.1): vá ao `wait`, ou repita só aquela persona com `--operation <a mesma>` e o mesmo
  texto. Nunca um envio novo às cegas.
- **O sinal de fim** é o status da persona, com o `round_id` e o Dispatch daquele envio, do remetente certo; o
  **marcador** `<!-- fim-rodada-N -->` na última linha do worklog continua como o registro que o `tally.py` lê.
- **Esperar:** `$S/wait_round.py N --reuniao $R` chama `brza sessions wait --any` e imprime uma linha por chegada. Ele
  cruza a chegada com o marcador, avisa `blocked`, `failed` e pergunta real, e conta à parte o ruído previsto (X3): o host
  escala "Worker stopped without reporting" a cada fim de turno sem `worker_done`, que é o normal entre rodadas — não se
  responde nem se narra como falha. Falha real é o desfecho `failed`/`blocked` do `wait` ou o worker `failed`/`stopped`.
- **A rodada com participantes escolhidos** (a rodada extra da R8, com a lista que a coordenação escolheu pela R9: parte
  da sala ou a sala inteira): os nomes no `--send` (`--send Trava Relance --round 3`), `--personas` no `wait_round.py` e `--participantes` no `tally.py` e no `panel.py collect`;
  os outros ficam "fora da rodada" e não seguram o fechamento nem a síntese do painel (X18).
- Rodadas-tipo: R1 independente; R2 debate (disputas D#, ataques, concessão, placar com "Mudou?"); R3 voto e notas; a
  última, confiança final e autoavaliação; e a rodada extra de voto informado, com o molde do tipo 5 (X17: a improvisada
  da P7 não foi lida pelo `tally.py`). Toda seção traz a linha `**Posição:**` (alimenta o painel).
- **O voto final só depois da síntese que traz os fatos da rodada anterior (X10).** O pedido de rodada com voto aponta a
  `sintese-(N-1).md`, lista os M# novos, e a persona declara `**Fatos lidos:**` antes de votar; o `tally.py` avisa quem
  votou sem a linha. Na P7, o fato decisivo (0 PRs) nasceu na mesma rodada do voto, e duas personas votaram sem ele.
- **A rodada extra de voto informado é automática quando o gatilho vale (R8 de Anderson, 2026-11-09:** "Executar rodada
  extra automaticamente. Custo: cerca de 3–5 min quando o gatilho ocorrer, com a coordenação prolongando a reunião sem
  perguntar. Se paga: quando eu estiver indisponível e o voto precisar considerar o fato novo."**).**
  - **O gatilho:** um fato novo (M#), nascido na própria rodada de voto, contradiz a premissa de algum voto dela. A
    coordenação confere o fato por comando antes de usá-lo.
  - **O que a coordenação faz, sem pedir licença para a extensão:** sintetiza o fato, publica a síntese com o M# marcado
    como novo, escolhe os participantes e envia a rodada do tipo 5. Narra uma linha: "Rodada extra automática (R8): M6
    contradiz a premissa do voto B de Trava e Relance; vai a Trava e Relance, porque o voto A do Prumo não depende de M6
    (R9)".
  - **A quem vai: a coordenação escolhe e registra o motivo (R9 de Anderson, 2026-11-09:** "A coordenação escolhe e
    registra o motivo. Custo: um julgamento sobre participantes em cada gatilho, além da rodada. Se paga: quando o alcance
    do fato varia entre reuniões."**).** Antes do disparo, o motivo vai ao `sintese-N.json` (`rodada_extra`) e à linha da
    narração: parte da sala (por exemplo, só quem votou com a premissa contradita) ou a sala inteira (o fato mexe em
    votos que não contradiz de frente). Não há composição fixa. A lista escolhida é a mesma no `--send`, no
    `--personas` e no `--participantes`.
  - **Sem gatilho, não há rodada extra**: ela não é praxe nem obrigatória. Fato novo que não toca premissa de voto vai à
    síntese e à proposta, sem rodada.
  - **O limite:** a extensão é a única coisa automática. A decisão final continua de Anderson, na rodada de decisões, e
    nem as personas nem a coordenação decidem por ele. A duração é ~3–5 min, estimativa, sujeita à persona mais lenta
    (as personas rodam em paralelo); o custo em US$ da rodada extra não foi medido na P7.
- **Isolamento da R1:** o pedido proíbe ler os worklogs dos colegas, e a coordenação confere por `grep` do nome das
  outras personas na seção R1 de cada uma. Só há instrução, não mecanismo.

## Passo 4 — o atrasado e a queda de runtime

- **O prazo da espera respeita a duração anunciada (X6):** o `wait_round.py` só encerra depois da duração do
  `rodada-N.md` mais 2 min, contados do envio (o mapa guarda a hora). Sem duração anunciada, 2× a mediana das chegadas, no
  mínimo 3 min. A síntese fecha sem quem falta e **o diz**.
- O atrasado entra pela rodada anterior, rotulado, e pode juntar duas rodadas numa seção.
- Duas rodadas perdidas, ou erro de cota: a persona reabre no `fallback` do manifesto, com o worklog dela como contexto.
- A contraprova e a rodada a mais, se as decisões pedirem, acontecem **antes** do encerramento: depois do `worker_done` a
  sessão fecha sozinha em ~2 min (reabrir custa uma sessão nova pelo `fallback`).

## Passo 5 — sintetizar

1. Rode `$S/tally.py N --reuniao $R --opened <hora do envio> --closed <hora do último fim> --settle 60` **antes** de
   escrever: o `estado-rN.json` traz status, posição, confiança, voto, nota e medição por persona. A média da conta à mão
   errou nas duas reuniões. A medição do Claude só chega no `Stop` do turno, segundos depois do status (X4): o
   `--settle` espera por ela, e a persona ainda sem linha sai "medição pendente", nunca zero nem "sem medição". Sem
   `--opened`/`--closed`, o custo é o total da sessão, e a tabela e o painel o dizem no rótulo (X7).
2. A síntese segue o molde (`references/synthesis.md`): convergências C#, fatos medidos M#, disputas D#, propostas P#.
3. A coordenação **confere por comando** os números das personas e mede o que a sala não mediu.
4. Disputa técnica ou visual: prova de conceito ou evidência renderizada antes do voto. Nada exposto sem autenticação;
   derrube o que subir. O erro de shell da própria coordenação não vai ao chat.
5. Escreva o `sintese-N.json` (medições, síntese em até 5 linhas, decisões com quem as levantou) e **publique o painel**
   (`narration.md`, "O painel").

## Passo 6 — a proposta, o revisor e a contraprova

- Proposta pelo molde (`references/proposal.md`): origem (R#, revisor, contraprova) e evidência (`[medido]`, `[lido]`,
  `[inferido]`) em cada linha; "não aprovada".
- Revisor independente (`reviewer`) em toda versão que vai a Anderson, com as cinco conferências da memória do revisor.
- **Confiança do plano = o número do revisor independente** (R2.3). A sala vai ao lado, com média, mediana, n e faixa; o
  Antigravity à parte; a diferença sala × revisor é registrada em toda reunião. Nenhum desconto fixo vira regra: o
  revisor ficou 12 e 17 pontos abaixo em duas medições e 3 acima na terceira.
- **Contraprova** só quando a proposta vai a aprovação **e** (a decisão é cara de reverter **ou** sala e revisor
  divergem mais de 10 pontos): R1 às cegas mais a confiança na proposta, em modelos baratos, sem Fable. Custa ~US$ 1 nas
  personas e ~US$ 6 e ~13 min da coordenação que a conduz.

## Passo 7 — fechar

- Rodada de decisões para Anderson pelo molde (`references/closing.md`): **em texto**, com a proposta inteira à vista.
  Por opção, o voto de cada persona e o argumento mais forte a favor e contra, uma linha cada, com o link do worklog
  (R2.4). A regra da memória `consultant-debate-shown-in-full` (argumentação integral) vale para consultores por `Agent`,
  não aqui: o integral fica no worklog e, depois, no painel.
- Issues para o que sobra. O worklog da coordenação leva a **proposta final copiada**, porque `.sessions/` não vai ao
  git.
- Memória de runtime: `$S/runtime_memory_check.py <hora de abertura>`; o que listar entra em `## Fora do workspace`
  (as personas Grok gravaram memória em `~/.grok/memory-v2/` contra a ordem do briefing, também na P7).
- **Encerramento (R7 de Anderson):**
  1. `$S/launch_persona.py $R --close` pede a cada persona o `worker_done` do preâmbulo, e o CLI devolve `closing`.
     **`closing` não é fechado.**
  2. `$S/launch_persona.py $R --status --wait-settled 180` confere, no `worker-show`, que o host aceitou o `worker_done`
     (`succeeded`/`settled`, com o `taskId` e o `autoReleaseAt`). Só então a narração diz "encerrada". Quem não
     respondeu aparece com o comando que o preâmbulo dela deveria ter usado, com os ids reais, para a coordenação decidir.
     O `--status` **sem** `--wait-settled` é consulta informativa: imprime o veredito de cada persona e sai 0 sempre que
     leu todas (1 só quando falta Dispatch ou o `worker-show` falha), também com `falhou` ou `liberada (falhou)` na linha.
     Quem decide pelo código de saída usa o `--wait-settled`, que sai 0 só com todas aceitas ou liberadas, 1 com falha e
     75 no prazo; a falha nunca se lê pelo rc 0 da consulta.
  3. Persona travada: `$S/launch_persona.py $R --stop <persona>` (parada guardada: confirma `stopped` e o settlement
     antes de liberar). `stop_unknown` e `retained` **não** são fechados e **não** autorizam repetir o comando: confira
     com `--status` e relate a incerteza.
  4. `--keep-open <persona>` mantém por comando; o botão "manter aberta" do chat faz o mesmo.
  5. **Depois de "encerrada e aceita", não chame `--close` de novo:** o fechamento automático libera em ~2 min. O `close`
     do v2 hoje lê o `dispatch.status` (`completed`) antes do `worker.state` (`succeeded`), não reconhece o worker
     encerrado e mandaria outro pedido de encerramento em vez de liberar (`brza-sessions:564`; a correção é do
     `brza-workflow`). **"Encerrada, retida"** é diferente: o terminal ficou com outro dono ou sem identidade provada e não
     fecha sozinho; diga-o no chat e no worklog, e Anderson decide se fecha a aba.
     O mesmo defeito do `worker_state` faz o `wait` do v2 não concluir rodada por `worker_done`; a rodada conclui pelo
     status, como deve.
- `brza note commit` dos worklogs e issues.

## A narração e o painel

A tabela de regras está em `references/narration.md`; leia-a antes da abertura. Em resumo, o que Anderson precisa ver no
chat da coordenação, e **o porquê**: ele acompanhou a Carvão pelo chat e a MCP pelos chats das filhas, e a diferença não
foi silêncio, foi conteúdo (personas nomeadas em 11 de 57 blocos contra 4 de 47).

- **Abertura:** a tabela Persona · papel · runtime · modelo · esforço, que o `launch_persona.py` imprime.
- **Cada chegada:** uma linha "R2 · 4/6 — entregaram … ; faltam …", e a mesma linha a cada 3 min sem chegada.
- **Fechamento de rodada:** a tabela do `tally.py` (posição, confiança, mudou?, voto), a sala e o revisor, os números
  conferidos ("confere/diverge: … — fonte → resultado") e o painel `::orca-visual`.
- **Não vai ao chat:** a argumentação integral das personas (R1.4) e o ruído previsto do host (X3), contado numa linha.
- **O painel:** um arquivo por rodada (`<reuniao>-rN-<hash>.html`), republicado na abertura, a cada resposta nova e no
  fechamento; a rodada seguinte ganha nome novo. Conferido por PNG antes de aparecer (`narration.md`).
- **A hora** de toda linha da narração e do worklog sai de `date '+%H:%M:%S'`, rodado na hora, nunca de cabeça (X11).

## Os verbos por passo

| Passo | Comando da skill | O verbo do `brza sessions` por baixo |
| :-- | :-- | :-- |
| Abrir com modelo e ciclo de vida | `launch_persona.py $R` | `brza sessions <nome> --agent --model --effort --prompt-file --wait` |
| Enviar a N | `launch_persona.py $R --send … --round N` | `send <nomes…> --text`, com recibo e `--operation` |
| Esperar | `wait_round.py N` | `wait <nomes…> --any --timeout` |
| Ler a persona travada | — | `read <nome> --last` |
| Trocar modelo | — | `model <nome> <modelo> --effort` |
| Medir | `tally.py --opened … --closed …` (a janela vem dos horários que a coordenação passa) | — (o `usage` dá o total da sessão; a skill não o chama) |
| Fechar | `launch_persona.py $R --close`, `--status`, `--stop`, `--keep-open` | `close`, `close --force`, `close --keep-open`; `worker-show` só leitura |

O `tally.py`, o `panel.py`, o `check_briefing.py` e o `runtime_memory_check.py` não têm verbo correspondente e ficam.

## Invariantes

- A persona nunca pergunta, nunca commita, só escreve no worklog dela.
- Nenhum número entra no chat sem a fonte (`tally.py`, comando ou worklog).
- Sem a frase explícita de Anderson, nada vira decisão: o registro nasce como proposta.
- A conta de médias, mediana, soma de custo e a lista "sem medição" saem dos scripts, nunca da coordenação.
- Nada se reenvia, se fecha de novo ou se relança às cegas: `pending`, `unknown`, `closing`, `stop_unknown` e `retained`
  se conferem antes da próxima ação.
