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
`brza-workflow` depois de duas reuniões sem desvio de fluxo (PLN-017/R2.1).

## Quem é quem

- **A coordenação** é a sessão principal: pergunta a Anderson, abre as sessões, sintetiza, confere números, grava.
- **As personas** são chats do Studio que escrevem só no worklog delas; nunca perguntam, nunca commitam.
- **Anderson decide.** A coordenação não decide: a rodada de decisões leva as opções, e decisão só vale com a frase
  explícita ("decidido", "fechado", "pode aplicar"). A norma de rodadas é a do `AGENTS.md`; esta skill não a repete.

## Os arquivos e quando ler

| Preciso de… | Leia / rode |
| :--- | :--- |
| o briefing da reunião | `references/briefing.md` |
| uma persona (arquétipo, papel → modelo, régua da confiança) | `references/persona.md` |
| o esqueleto do worklog de uma persona | `references/persona-worklog.md` |
| o pedido de uma rodada (os quatro tipos, a linha `**Posição:**`) | `references/round-request.md` |
| a síntese, o `sintese-N.json` do painel | `references/synthesis.md` |
| a proposta, a confiança do plano, o revisor, a contraprova | `references/proposal.md` |
| a rodada de decisão, o worklog da coordenação, o encerramento | `references/closing.md` |
| o que dizer no chat e o ciclo do painel | `references/narration.md` |
| abrir, enviar, liberar ou parar as sessões | `$S/launch_persona.py $R [--via …] [--send …] [--release …] [--stop …]` |
| esperar o fim da rodada | `$S/wait_round.py N --reuniao $R` |
| a tabela por persona, sem conta à mão | `$S/tally.py N --reuniao $R --opened HH:MM:SS --closed HH:MM:SS` (sem a janela, o custo é o da sessão inteira) |
| o painel da rodada | `$S/panel.py collect N --reuniao $R --opened … [--closed …]` e `$S/panel.py render …` |
| a memória de runtime fora do repositório | `$S/runtime_memory_check.py <início>` |

**Convenção dos comandos:** rodam da raiz do worktree, com `python3 -I .claude/skills/meeting-runner/scripts/<script>.py` (abaixo, `$S`); a raiz padrão dos
scripts é a do git, e o manifesto é `.sessions/<reuniao>/reuniao.json` (`$R`). Os caminhos relativos do manifesto resolvem contra essa raiz.

O **manifesto** `reuniao.json` (nome, slug, papel, runtime, modelo, esforço, sessão, fallback de cada persona, mais o
tema, a pasta da reunião e o molde do caminho dos worklogs) é a fonte única do lançamento, das tabelas e do painel; o
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

- **As personas abrem com o ciclo de vida dos workers do Orca** (R5 de Anderson): depois que a coordenação manda o
  encerramento, a sessão fecha sozinha ~2 min depois, e o chat mostra o botão "manter aberta" para Anderson guardar a que
  quiser consultar. O `launch_persona.py reuniao.json` abre pela via que a sonda P4a.0 do PLN-017 decidir: `--via
  worker-start` (padrão: `brza orchestration worker-start --spec-file … --agent … --model … --effort …`), `--via hybrid`
  (chat por `agent launch --surface chat` e depois `worker-start --terminal`) ou `--via agent-launch` (abre como antes,
  **sem** ciclo de vida: só para testar o resto da skill). Ele grava `dispatch_id` e `orca_session_id` no mapa. v2:
  `brza sessions open --model --effort` pela mesma via.
- **A sonda P4a.0 ainda não rodou**: nenhuma das duas vias com ciclo de vida foi verificada contra o Studio, e o formato
  do recibo do `worker-start` não foi visto. Antes da primeira reunião real, abra uma persona de teste e confira o que o
  script gravou no mapa e se o `autoReleaseAt` aparece (`brza orchestration worker-show`).
- O prompt de abertura é de uma linha por persona e é guardado em `prompt-<slug>.txt`. Ele começa com "Você é uma
  persona numa reunião multiagente": é o que impede a persona de acionar esta skill. Chega depois do preâmbulo do Orca,
  como turno do coordenador, e diz à persona que o `worker_done` que o preâmbulo pede é o do **encerramento**.
- Codex `exec` roda com `< /dev/null` (esperou o stdin e custou 3 minutos). Narre a abertura (`narration.md`).

## Passo 3 — conduzir uma rodada

- O pedido sai do molde (`references/round-request.md`), com **duração** ("~5 min"), não hora: os prazos das duas
  reuniões não eram monotônicos e ninguém os cobrou.
- **O sinal de fim** é uma mensagem: ao fechar a rodada, a persona roda `brza orchestration send --subject
  "fim-rodada-N"` para a coordenação (R6.2). O **marcador** continua, como registro escrito que o `tally.py` lê: "acrescente
  a sua seção no fim do worklog; a última linha do arquivo é `<!-- fim-rodada-N -->`", regra única. O `worker_done` NÃO vai
  por rodada: arma os 2 min de fechamento e a persona sumiria no meio da síntese.
- Envio: uma linha que aponta o arquivo da rodada, só para persona com `state` fora de `working` — a fila entrega na
  virada do turno (~12 min medidos), e o "sent" do `brza sessions` não diz quando chega. Persona aberta como worker (a
  via padrão) não está no mapa do `brza sessions` até a sonda P4a.0: envie por `python3 -I $S/launch_persona.py $R
  --send <persona|todas> --message "Faça a rodada N: .sessions/<reuniao>/rodada-N.md"` (`brza orchestration send --to
  dispatch:<id>`). Com `--via agent-launch`, `brza sessions send <sessão> "…"` como antes.
- Espera: `python3 -I $S/wait_round.py N --reuniao $R` (embrulha `brza orchestration check --wait`; v2:
  `brza sessions wait`). Ele cruza a mensagem com o marcador e avisa a persona que mandou o fim sem fechar o worklog.
  Para chat aberto com `--via agent-launch` (sem Dispatch), `--source marker` espera só pelo marcador. Narre cada chegada.
- Rodadas-tipo: R1 independente; R2 debate (disputas D#, ataques, concessão, placar com "Mudou?"); R3 voto e notas; a
  última, confiança final e autoavaliação. Toda seção traz a linha `**Posição:**` (alimenta o painel).
- **Isolamento da R1:** o pedido proíbe ler os worklogs dos colegas, e a coordenação confere por `grep` do nome das
  outras personas na seção R1 de cada uma. Só há instrução, não mecanismo.

## Passo 4 — o atrasado e a queda de runtime

- Timeout da rodada: 2× a mediana das que entregaram, no mínimo 3 min. A síntese fecha sem quem falta e **o diz**.
- O atrasado entra pela rodada anterior, rotulado, e pode juntar duas rodadas numa seção.
- Duas rodadas perdidas, ou erro de cota: a persona reabre no `fallback` do manifesto, com o worklog dela como contexto.
- A contraprova e a rodada a mais, se as decisões pedirem, acontecem **antes** do encerramento: depois do `worker_done` a
  sessão fecha sozinha em ~2 min (reabrir custa uma sessão nova pelo `fallback`).

## Passo 5 — sintetizar

1. Rode `python3 -I $S/tally.py N --reuniao $R --opened <hora do envio> --closed <hora do último fim>` **antes** de escrever: o `estado-rN.json` traz status,
   posição, confiança, voto, nota e medição por persona. A média da conta à mão errou nas duas reuniões.
2. A síntese segue o molde (`references/synthesis.md`): convergências C#, fatos medidos M#, disputas D#, propostas P#.
3. A coordenação **confere por comando** os números das personas e mede o que a sala não mediu.
4. Disputa técnica ou visual: prova de conceito ou evidência renderizada antes do voto. Nada exposto sem autenticação;
   derrube o que subir. O erro de shell da própria coordenação não vai ao chat.
5. Escreva o `sintese-N.json` (medições, síntese em até 5 linhas, decisões) e **publique o painel**
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
- Memória de runtime: `python3 -I $S/runtime_memory_check.py <hora de abertura>`; o que listar entra em `## Fora do
  workspace` (as personas Grok gravaram memória em `~/.grok/memory-v2/` contra a ordem do briefing).
- **Encerramento (R6):** mande a cada persona "a reunião acabou; envie `worker_done`". O host arma os 2 min e o botão
  "manter aberta" aparece no chat; Anderson guarda a que quiser. Quem não responder, libere com
  `python3 -I $S/launch_persona.py $R --stop <persona>` (`worker-stop`: o `worker-release` só vale para worker que já
  enviou `worker_done`); `--keep-open <persona>` mantém por comando. O `brza sessions close` de cada persona saiu do passo. Persona aberta por `--via agent-launch` não
  tem esse ciclo e continua a fechar por `brza sessions close`.
- `brza note commit` dos worklogs e issues.

## A narração e o painel

A tabela de regras está em `references/narration.md`; leia-a antes da abertura. Em resumo, o que Anderson precisa ver no
chat da coordenação, e **o porquê**: ele acompanhou a Carvão pelo chat e a MCP pelos chats das filhas, e a diferença não
foi silêncio, foi conteúdo (personas nomeadas em 11 de 57 blocos contra 4 de 47).

- **Abertura:** a tabela Persona · papel · runtime · modelo · esforço.
- **Cada chegada (mensagem de fim de rodada):** uma linha "R2 · 4/6 — entregaram … ; faltam …", e a mesma linha a cada 3 min sem chegada.
- **Fechamento de rodada:** a tabela do `tally.py` (posição, confiança, mudou?, voto), a sala e o revisor, os números
  conferidos ("confere/diverge: … — fonte → resultado") e o painel `::orca-visual`.
- **Não vai ao chat:** a argumentação integral das personas (R1.4); ela fica no worklog e na fase do painel.
- **O painel:** um arquivo por rodada (`<reuniao>-rN-<hash>.html`), republicado na abertura, a cada resposta nova e no
  fechamento; a rodada seguinte ganha nome novo. Conferido por PNG antes de aparecer (`narration.md`).

## v1 × v2 (o CLI que vem)

| Passo | v1 (hoje) | v2 (verbos do D2) |
| :-- | :-- | :-- |
| Abrir com modelo e ciclo de vida | `launch_persona.py` | `brza sessions open` pela via de worker |
| Enviar a N | laço de `brza sessions send`, depois do `wait` | `send` a N com recibo |
| Esperar | `wait_round.py` (`check --wait`) | `brza sessions wait` |
| Ler | o worklog; o chat, só abrindo a aba | `brza sessions read --last` |
| Trocar modelo | fechar e reabrir no `fallback` | `brza sessions model` |
| Medir | `tally.py` (Claude + Codex) | `tally.py` sobre `brza sessions usage` |
| Fechar | `worker_done` das personas + `--stop` | `close` por `worker-release` |

Quando o CLI chegar, `launch_persona.py` e `wait_round.py` saem e esta tabela troca "v1" por "v2". O `tally.py` e o
`panel.py` ficam.

## Invariantes

- A persona nunca pergunta, nunca commita, só escreve no worklog dela.
- Nenhum número entra no chat sem a fonte (`tally.py`, comando ou worklog).
- Sem a frase explícita de Anderson, nada vira decisão: o registro nasce como proposta.
- A conta de médias, mediana, soma de custo e a lista "sem medição" saem dos scripts, nunca da coordenação.
