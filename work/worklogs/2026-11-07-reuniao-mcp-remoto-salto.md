---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
---

# Reunião MCP remoto: a participação de Salto, o Provocador

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Salto** — persona o Provocador, no
Grok grok-4.7-build-fast low —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

A pergunta está pequena. O Mac no centro e o correio síncrono são premissa, não requisito. O requisito é a sessão Cloud falar com a sessão do Mac. Isso cabe numa fila que o Mac *puxa*.

#### 1. Arquitetura

- **Posição:** F, o git como barramento — combinação de C com uma alternativa que a pauta não listou; A e E ficam de fora.
- **Por quê:** O correio hoje só anda por socket unix na mesma máquina (*lido*, levantamento A, `brza_runtime.py`). A Cloud já entra por git e, no Claude, por `claude -p --cloud <id>` (*lido*, levantamento B). Túnel (A) e `brza serve` (E) mantêm o Mac como servidor; o requisito não pede isso. O `brza-quota` lê estado do Mac (*lido*, `accounts.py` / Application Support): ao vivo ele não mora na nuvem. *Suposto:* duas sessões quase nunca estão as duas acordadas no mesmo segundo, então síncrono é teatro.
- **Ideias:** um ref `refs/brza/mail` (ou `.sessions/correio/`), append-only, que o Mac drena para `agentSession.send` `(ousadia: alta)`; o quota vira um JSON de números commitado pelo launchd, sem servidor `(ousadia: média)`.
- **Risco:** latência de push/pull; conflito de ref; alguém commita segredo no barramento.
- **Confiança:** 62/100

#### 2. Segurança

- **Posição:** zero porta de entrada no Mac; a autenticação é a do git (ou de um repo privado só de correio).
- **Por quê:** Túnel e pareamento anunciado (`--pairing-address`, *lido*, help do `brza serve`) abrem superfície. O fallback `token-insecure-origin` guarda código no `localStorage` (*lido*, `web-device-key.ts`). Bearer do quota e `authToken` do runtime ficam no disco do Mac (*lido*, levantamento A) — não atravessam o git. *Suposto:* um repo privado com a mesma conta que já clona o workspace chega para a sala.
- **Ideias:** payload do correio é texto de sessão, tamanho teto, sem anexo e sem path de `orca-runtime.json` `(ousadia: baixa)`; quota publicado só com números de cota, sem token `(ousadia: baixa)`.
- **Risco:** histórico do git é para sempre; mensagem sensível não some com delete. Mitigação declarada: ref separado, não o branch de código, e GC explícito.
- **Confiança:** 70/100

#### 3. Runtimes Cloud

- **Posição:** F funciona hoje onde a sessão já tem o git. MCP HTTP ao vivo não é o caminho comum.
- **Por quê:** Claude Cloud: rede Trusted não alcança host arbitrário; conectores MCP passam pelos servidores da Anthropic; `claude -p --cloud` já enfileira (*lido*, levantamento B). Cursor: MCP HTTP/stdio no dashboard e Tailscale (*lido*) — isso é A, e eu recuso. Codex: internet do agente desligada por padrão e MCP no Cloud não confirmado (*lido*). *Suposto:* os três conseguem ler e escrever um arquivo no repo da sessão; o Codex sem internet ainda lê o que o setup já clonou, e o retorno espera o próximo push do Mac.
- **Onde funciona hoje:** Claude Code Cloud, sim (git + `--cloud`). Cursor Cloud Agents, sim se o agente commita no repo (*suposto* o commit; *lido* que MCP lá é configuração de time). Codex Cloud, só o lado leitura do que já está no clone enquanto a internet do agente estiver off; escrita no barramento fica para o setup script ou para quando a rede irrestrita estiver ligada (*lido* o default off; *suposto* o setup poder dar push).
- **Ideias:** não esperar paridade de MCP; o correio é arquivo `(ousadia: média)`; `context7` continua plugin do fornecedor, fora desta briga `(ousadia: baixa)`.
- **Risco:** Cursor e Codex tratarem o worktree como somente leitura na prática. Aí F vira mão única até alguém medir um commit.
- **Confiança:** 55/100

#### 4. Ergonomia e rollout

- **Posição:** o primeiro passo é um dreno local, sem túnel e sem servidor novo. A pessoa manda como sempre; o transporte é detalhe.
- **Por quê:** Falha silenciosa é o modo padrão de fila: a Cloud acha que enviou e o Mac estava dormindo. *Suposto:* um recibo no mesmo ref (`ack/<id>`) cabe em um arquivo. O comando que a pessoa já tem é `brza sessions send` (*lido*, briefing).
- **Ideias:** `brza sessions send` ganha `--via git` que só anexa um markdown e não abre socket quando o alvo é remoto `(ousadia: média)`; um launchd no Mac faz `git fetch` + `agentSession.send` + `ack` `(ousadia: média)`.
- **Primeiro passo barato:** um script de leitura no Mac, cron ou launchd de 1 min, que pega arquivos novos em `.sessions/correio/inbox/` e chama o send local. Sem mudar o Studio.
- **Métrica de sucesso:** uma sessão Claude Cloud entrega uma frase numa sessão local do Mac, com `ack` no ref, em até 2 minutos, e `lsof` no Mac não mostra porta nova fora de `127.0.0.1`.
- **Risco:** o dreno para se o git pedir credencial interativa. Declarado: remote com credencial já usada pelo workspace, senão o passo não conta.
- **Confiança:** 68/100

#### A ideia mais ousada desta rodada

O correio deixa de ser RPC. Vira um ref git `refs/brza/mail`. A Cloud é par, o Mac é assinante e só faz conexão de saída. O `brza-quota` ao vivo morre para a Cloud: o que ela lê é um snapshot de números. O `brza serve` e o túnel continuam existindo para quem quer desktop remoto — outro produto, outra issue.

Risco: a sala mede e descobre que Cursor ou Codex não dá push. Aí F fica Claude-only na escrita até o segundo runtime ser medido. Segurança relaxada (mensagem eterna no histórico) é o preço declarado; ref separado e sem segredo no payload são o freio.

#### Issues candidatas

- **Correio por ref git, Mac só puxa** — tira o socket unix do caminho da Cloud sem abrir porta — prioridade `high`
- **Snapshot de cota sem servidor** — o `brza-quota` depende do disco do Mac; publicar números num JSON versionado — prioridade `medium`
- **Recibo `ack` no mesmo barramento** — fila sem ack é falha silenciosa — prioridade `medium`
- **Medir push a partir de Cursor Cloud e Codex Cloud** — a posição F está *suposta* nesses dois — prioridade `high`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | F: git é o barramento, Mac assina, A e E ficam de fora | 62 |
| 2. Segurança | Sem porta de entrada; auth é a do git; segredo não entra no ref | 70 |
| 3. Runtimes Cloud | Escrita hoje no Claude; Cursor e Codex ainda por medir | 55 |
| 4. Ergonomia e rollout | Dreno launchd de 1 min; sucesso é ack em 2 min sem porta nova | 68 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

F sai da base. M2 entregou correio de verdade (Codex CLI → túnel → `brza sessions send`). Git eterno perdeu para 200 ms medidos. A premissa que sobra é outra: a VM não é o único "remoto".

#### As disputas

- **D1:** e: G quando a ferramenta pode rodar no Mac (M5, saída só); A+D estreito só para a VM que não pode. F deixa de ser a base. M2 mediu o CLI, não a VM (M4). — 72/100
- **D2:** b: a volta é caixa no mesmo MCP, com poll. O `claude -p --cloud` (a) fica atalho grátis só do Claude (M6), não o desenho. — 64/100
- **D3:** a: dado rotulado, em quarentena, lido quando a sessão do Mac pede. M3 mostrou o modelo inventar em cima de corte. Allowlist (c) não cura isso. — 78/100
- **D4:** a, se houver túnel: nomeado + Access. O quick tunnel (c) morre no reinício (M1). G não tem túnel (d). Tailscale não é o que foi medido. — 70/100
- **D5:** a: fechar o caminho que M2 já abriu — recibo e contagem conferível (M3) — num runtime. O dreno git (d) agora é desvio. — 74/100

#### Os ataques

- **Cartógrafo, arquitetura, confiança 85 em D+A para a Cloud.** M4 não sondou a VM; M1 é quick tunnel efêmero; M3 fez o Codex afirmar "0 sessões" com 7 na lista. Derruba o ataque: uma sessão Cloud Trusted chamar túnel nomeado e devolver a contagem certa.
- **Plantão, runtimes: "C funciona hoje só no Cursor".** O que funcionou hoje foi A, no Codex CLI (M2), não C e não o Cursor Cloud. Derruba o ataque: um log de Cursor Cloud Agents consumindo relay só de saída, com recibo.

#### A concessão

M2 me moveu. F era a aposta porque ninguém tinha atravessado o correio. Atravessou, sem git. M3 me moveu junto: ferramenta remota que corta em silêncio mente. Recibo de consumo (Régua, Plantão) entra no contrato.

#### "Sim, e…"

Em cima do Muralha (mensagem da Cloud é dado, não tarefa) e da ferramenta que o M2 já chamou: `mail_send` devolve `{id, hash, total}` e o corpo só aparece quando a sessão do Mac chama `mail_read(id)`. O modelo remoto não injeta prompt; o corte fica visível no `total`. `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Arquitetura | G no Mac; A+D estreito só para VM; F fora da base | 62 | 72 | virou | M2 e M5 |
| 2. Segurança | Quarentena + túnel nomeado se houver; sem porta no G | 70 | 76 | ajustou | M1, M3, Muralha |
| 3. Runtimes Cloud | Medido: Codex CLI. VM Cloud ainda aberta. G é o atalho | 55 | 68 | ajustou | M2, M4, M5 |
| 4. Ergonomia e rollout | Semana 1 fecha recibo e contagem no caminho do M2 | 68 | 74 | ajustou | M3, Régua, Plantão |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

O plano acerta o mapa e erra a ordem. Gasta a semana no endpoint público que o M7 já recusou na rede padrão, e deixa para o fim as 2–4 h do modo que não abre porta.

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 46 | Só `--help` (M5); o poder de uma sessão local está no risco e ninguém rodou o worker |
| Modo 2 (A + D estreito) | 57 | M1, M2 e M2b mediram o formato; M7 mediu que a Cloud padrão não chega; Custom e token vinculado não rodaram |
| Modo 3 (a volta) | 74 | M8 mediu o Claude sem túnel; `mail_inbox` nos outros é inferência |
| As fases e os critérios de pronto | 48 | A fase 1 fecha com 20/20 IDs e não exige a prova de que a entrega perdeu a autoridade de coordenador |
| **O plano inteiro** | 55 | Serve à VM se Anderson pagar rede Custom; hoje o único caminho medido até a Cloud é a volta do M8 |

- **O erro que você vê:** o requisito pede conversa normal, e o M2 entregou pelo `brza sessions send`, o mesmo caminho que carrega autoridade de coordenador (`brza_runtime.py:95-97`, citado na proposta). O "pronto" da fase 1 (20/20, zero duplicata) não inclui um teste negativo disso. A sala pode carimbar um canal que injeta tarefa.
- **A mudança que mais subiria a sua confiança:** fase 3 antes da fase 1, e o pronto da fase 0 exige a mensagem vista no Mac sem autoridade de coordenador. O plano inteiro iria a **72**.
- **A decisão que é de Anderson:** a sessão que importa nesta semana roda fora do Mac, ou basta abrir do celular/web com a ferramenta no Mac? Recomendo medir o G antes de comprar domínio e Access; o túnel só se a VM for o requisito.
- **Nota aos colegas:** Muralha 9 (autoridade e injeção). Régua 9 (recibo, cabeçalho forjado, 20/20). Plantão 7 (Mac dormindo e aviso visível). Atalho 6 (caminho curto, pouca briga com o M7). Cartógrafo 5 (o denominador HTTP ajudou; a confiança 85 em D+A não sobreviveu ao M7).

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

O M10 fecha o que a R3 só temia: "sent" em 200 ms, a frase no chat 14 min depois, como a pessoa. A caixa sem byte remoto é o desenho certo. O aviso fixo continua sendo turno.

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 46 | 63 | A ordem e o usuário macOS separado entraram; o worker continua [lido], e a conta ainda é credencial do Mac |
| Modo 2 (A + D estreito) | 57 | 60 | A caixa evita o texto remoto no chat; o M10 mostra que o aviso ainda entra como a pessoa, e a VM Custom segue sem medida |
| Modo 3 (a volta) | 74 | 70 | O M8 continua de pé; o verbo `send remote:` é novo, e o login do `claude -p` vence entre 9 e 12 de novembro |
| As fases e os critérios de pronto | 48 | 66 | G virou a fase 1; o teste negativo da fase 0 está escrito e o código de hoje não tem remetente `remote` para cumpri-lo |
| **O plano inteiro** | 55 | 64 | Parcial de propósito, na ordem certa; o marco ainda pode ser carimbado com o aviso virando turno da pessoa |

- **A sua mudança da R3 entrou?** Em parte. G antes do túnel entrou e resolve a ordem. O teste negativo entrou na fase 0, e não resolve: o M10 e `agent-session-message-source.ts` dizem que, sem o remetente `remote`, o aviso é a pessoa. Esse remetente ficou fora das fases, como D1.
- **O que ainda está errado:** o "pronto" da fase 0 aceita um aviso que o app de hoje só sabe renderizar como pessoa ou coordenador.
- **Autoavaliação:** o vício apareceu no F, barramento sem caminho, e de novo ao empurrar o G sem pesar que a conta da Cloud vira credencial do Mac — isso só ficou sério com o revisor.

<!-- fim-rodada-4 -->

### Rodada 5: o foco no MCP do `brza-workflow`

- **Como expor o `brza-orchestrator`:** não se constrói outro servidor. Ele já é MCP Streamable HTTP em `127.0.0.1:4242` (*lido*, `server.py:1-18`). Para a VM, o túnel nomeado aponta para essa porta; o G usa o loopback e não abre porta. O que muda em relação ao correio: não há mensagem. O `dispatch` enfileira e o ciclo abre um worker no Mac (*lido*, `cycle.py:1-8`). O `/health` hoje não responde (*lido*, coordenação). Não chamei o `dispatch`.
- **O que a sessão remota pode chamar:** `status`, sim, com o Bearer do `~/.brza/runtime`, e o servidor é quem grava o chamador — o `X-Brza-Session` e o argumento `caller` se ignoram (*lido*, `tools.py:196-199`, `server.py:111`; o E2 forjou o cabeçalho). `dispatch` só no papel `consultor`, que entra na fila; outro papel devolve `gate` e a aprovação fica no Mac (*lido*, `tools.py:261-290`, `356-366`). `config` grava política (*lido*, `tools.py:505-530`): a Cloud não chama.
- **Como "conversa":** o worker abre com `ORCA_AGENT_SESSION_ID` igual ao chamador (*lido*, `cycle.py:4-7`). A volta no MCP é o `status`: `finished` só daquele chamador, e o `brief` traz estado e `error`, não o texto do worker (*lido*, `queue.py:228-231`, `tools.py:472-500`). *Suposto:* a prosa fica na sessão do worker no Studio; o remoto só vê a fila. Sem um chamador preso ao token, o worker nasce pendurado na sessão errada.
- **O risco mais grave:** um `dispatch` remoto gasta conta e abre worker como se fosse a pessoa, e o mesmo chamador forjado aprova o próprio gate. Mitigação: chamador gravado no token, `config` fora, `approved` recusado se o chamador não for local.
- **Confiança:** 68/100

<!-- fim-rodada-5 -->

### Rodada 6: a confiança na v3

O M13 mediu o que a R5 leu: pelo túnel, o cabeçalho forjado virou `caller`. O proxy na frente da 4242 é o corte certo. A volta do texto continua sendo outro produto.

| Parte | Confiança (0–100) | Uma linha de porquê |
| :---- | :---------------- | :------------------ |
| O proxy remoto (fase 0) | 76 | Os testes negativos batem com o M13 e o L1; o proxy não existe, e a 4242 crua continua forjável até ele entrar |
| O G (fase 1) | 55 | Usuário separado e token remoto estão certos; o worker segue [lido], e um `dispatch` de consultor ainda gasta conta |
| A Cloud pelo túnel (fase 2) | 62 | M11 e M12 mediram `health` e `status` no servidor real; o `dispatch` da VM e a rede Custom não rodaram (M7) |
| A volta e a sessão-caixa (fase 3) | 44 | O L3 diz que o `status` não traz o texto; a volta repousa no `--cloud` e num remetente `remote` que o app não tem |
| **O plano inteiro** | 60 | A ida fica estreita e testável; o requisito de "conversar" só fecha na fase 3, que ainda não tem canal |

- **O que ainda está errado:** a fase 3 promete o texto do worker de volta, e o orquestrador não carrega esse texto (L3); o critério de "nenhum byte como turno" depende do remetente `remote`, que continua de fora.

<!-- fim-rodada-6 -->
