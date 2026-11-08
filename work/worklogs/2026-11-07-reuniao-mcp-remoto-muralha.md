---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
---

# Reunião MCP remoto: a participação de Muralha, a Arquiteta de Rede e Segurança

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Muralha** — persona a Arquiteta de Rede e Segurança, no
Claude Opus 5.5 high —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

Modelo de ameaça de partida (*suposto*, mas é o que guia tudo): a sessão Cloud lê conteúdo da internet e de repositório
de terceiros, então **toda sessão Cloud é presumida sob injeção de prompt**. A pergunta não é "quem tem o token", é "o
que o modelo injetado faz com o que a sessão alcança". O pior caso plausível: a Cloud injetada manda ao Mac uma tarefa
que roda shell como o usuário Anderson, com as chaves do `brz-anderson` e as contas do `brza-quota`.

#### 1. Arquitetura

- **Posição:** C + D estreito — um relay só de saída (Mac → relay ← Cloud) carregando um **MCP do correio** com meia
  dúzia de verbos; o E (`brza serve` + pareamento) e o A amplo ficam **fora** da Cloud.
- **Por quê:**
  - O RPC do runtime tem permissão por método, e `agentSession.send` exige `workspace`, que o próprio código define como
    "equals running commands as this host's user" (*lido*, `brza-studio/src/main/runtime/rpc/rpc-method-permission.ts:4-5`;
    `methods/structured-agent-session.ts:141-142`).
  - Logo o E entrega à Cloud uma casca do Mac. Até a allowlist do celular inclui `agentSession.respondToApproval` e
    `agentSession.create` (*lido*, `server/runtime-rpc-mobile-agent-session-methods.ts:2-19`): aprovar ferramenta é executar.
  - Hoje tudo escuta só no loopback: `127.0.0.1:6868` e o `brza-quota` em `127.0.0.1` (*medido*, `lsof -iTCP -sTCP:LISTEN`;
    *lido*, `brza_mcp/server.py:18`). Isso é bom e o relay preserva: nada novo escuta no Mac.
- **Ideias:**
  - Um `brza-mail-mcp` no Mac que **puxa** do relay (long-poll de saída) e só traduz para `rpc('agentSession.send')` local,
    com destinatários numa allowlist de nomes de sessão e prefixo fixo "[remoto, não confiável: <origem>]" (ousadia: média).
  - O relay mais barato é um repositório git privado só de caixas (`inbox/<sessão>/*.json`), com deploy key de escrita só
    nele; o Codex Cloud, que não tem rede no agente, lê no setup (ousadia: baixa).
  - Do `brza-quota`, expor só `status`; `dispatch` (gasta conta) e `config` nunca saem do Mac (*lido*, `brza_mcp/tools.py:540-544`) (ousadia: baixa).
- **Risco:** o relay vira um correio assíncrono, com latência de segundos a minutos; quem quer "conversa normal" vai
  pedir o E e o atalho volta.
- **Confiança:** 75/100

#### 2. Segurança

- **Posição:** a Cloud nunca recebe credencial com escopo `workspace`; recebe um token por sessão, curto e revogável, que
  só deixa **depositar mensagem** numa caixa — e a mensagem chega ao Mac rotulada como dado, nunca como tarefa do coordenador.
- **Por quê:**
  - O `authToken` do `orca-runtime.json` é um só para todo método do socket (*lido*, `brza_runtime.py:94-95`); vazado,
    é shell no Mac. Ele não pode sair da máquina, nem via túnel.
  - O `brza sessions send` marca a mensagem com `orchestrationCompatibilityEvidence` para chegar "como tarefa do
    coordenador" (*lido*, `brza_runtime.py:88-90,96-98`). A ponte remota **não** pode herdar isso.
  - Claude Code Cloud tem "network secrets": o proxy da Anthropic anexa o header ao host listado e o segredo não entra
    na VM (*lido*, levantamento → code.claude.com/docs/en/cloud-environments). É o melhor lugar para o token do relay.
- **Ideias:**
  - Token por sessão emitido pelo Mac (`brza remote grant <sessão> --ttl 8h --to <destinos>`), HMAC com escopo
    `{origem, destinos, expira}`; revogar = apagar a chave no Mac (ousadia: média).
  - Quarentena: mensagem remota cai como **pergunta para Anderson aprovar** no chat de destino nas primeiras semanas,
    não como prompt executável (ousadia: baixa).
  - Se algum dia houver túnel (A), Tailscale com ACL por tag e porta, sem Funnel; nunca `--pairing-address` público (ousadia: baixa).
- **Risco:** a quarentena mata a autonomia que motivou o pedido; o rótulo "não confiável" não impede um modelo
  ingênuo no Mac de obedecer.
- **Confiança:** 80/100

#### 3. Runtimes Cloud

- **Posição:** o relay HTTP de saída funciona hoje no Claude Code Cloud e no Cursor Cloud Agents; o Codex Cloud só pelo
  git no setup, sem conversa ao vivo.
- **Por quê:**
  - Claude Code Cloud: MCP HTTP com header; network secret por host; e o caminho **de volta** Mac → Cloud já existe sem
    abrir nada: `claude -p "msg" --cloud <session-id>` (*lido*, levantamento → claude-code-on-the-web). Confiança no `.mcp.json`
    do repo ser carregado na Cloud: baixa (*lido*, levantamento marca 40).
  - Cursor Cloud: MCP HTTP + OAuth e segredos de time injetados no start (*lido*, cursor.com/docs/cloud-agent); o segredo
    fica legível na VM, então o token tem de ser curto.
  - Codex Cloud: agente sem internet por padrão, segredo só no setup (*lido*, learn.chatgpt.com/…/cloud-environment).
- **Ideias:**
  - Para o Claude Cloud, MCP do relay com `url` + header vindo de network secret, nunca de env var do ambiente (ousadia: baixa).
  - Para o Codex, o setup script clona o repositório-caixa e o agente escreve a resposta num arquivo que um hook de fim
    commita (ousadia: média).
- **Risco:** a doc dos três muda rápido; o Codex Cloud pode não carregar MCP algum (*lido*, levantamento 75).
- **Confiança:** 65/100

#### 4. Ergonomia e rollout

- **Posição:** começar com **um** sentido e **um** runtime: Cloud do Claude Code → caixa → Mac, só leitura no Mac
  (aparece, Anderson decide), medido por uma semana.
- **Por quê:** a ida Mac → Cloud já é `claude -p --cloud` (*lido*); falta só a volta. Falha silenciosa é o risco
  ergonômico maior: relay fora do ar parece "ninguém respondeu" (*suposto*).
- **Ideias:**
  - Primeiro passo barato: o repositório-caixa privado + `brza sessions inbox --remote` que lista e entrega com o
    rótulo; zero porta, zero serviço novo (ousadia: baixa).
  - Batimento: o puxador grava `last_pull` e o `brza doctor` acusa > 5 min sem puxar (ousadia: baixa).
- **Métrica:** mensagens remotas entregues/semana, latência p50 Cloud→chat do Mac < 60 s, e **zero** credencial com
  escopo `workspace` fora do Mac (auditável: `grep` de token nos ambientes Cloud).
- **Risco:** blindar demais e ninguém usar — é o meu vício; se em uma semana a contagem for zero, a quarentena caiu mal.
- **Confiança:** 70/100

#### A ideia mais ousada desta rodada

Um **"perfil remoto" no próprio RPC do runtime**: um novo nível em `RpcMethodPermission`, abaixo do `workspace`, com
allowlist de dois métodos (`agentSession.send` com rótulo forçado de origem não confiável, e `agentSession.history` só
das sessões permitidas), concedido no pareamento. Aí o E vira seguro para a Cloud sem um relay paralelo. Risco: mexe no
coração do controle de acesso do app; um método novo marcado errado abre o Mac inteiro.

#### Issues candidatas

- **Nenhuma credencial `workspace` fora do Mac** — o token do runtime e o pareamento padrão equivalem a shell como o usuário — prioridade `high`
- **Mensagem remota chega rotulada como não confiável, sem `orchestrationCompatibilityEvidence`** — senão uma injeção na Cloud vira tarefa do coordenador — prioridade `high`
- **Repositório-caixa como relay de saída (PoC)** — menor superfície e funciona até no Codex Cloud — prioridade `medium`
- **`brza-quota` remoto só com `status`** — `dispatch` gasta contas e não pode ser acionado por sessão injetada — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | C + D estreito: relay só de saída com MCP do correio de poucos verbos; E e A amplo fora da Cloud | 75 |
| 2. Segurança | Cloud só recebe token curto que deposita mensagem; chega rotulada como dado, nunca como tarefa | 80 |
| 3. Runtimes Cloud | Claude Code Cloud e Cursor Cloud hoje por HTTP de saída; Codex Cloud só por git no setup | 65 |
| 4. Ergonomia e rollout | Um sentido, um runtime: Cloud → caixa → Mac, em quarentena, uma semana medida | 70 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

- **D1:** e: A + D por **Cloudflare Tunnel nomeado** para a Cloud em VM; G para quem pode rodar no Mac — o `cloudflared` disca
  para fora (*lido*, M1: quick tunnel; Mac segue só em `127.0.0.1`), então satisfaz o "só saída" que eu pedia ao C, sem
  fila nova. O que eu defendo no D é o gateway estreito, não o relay. — 72/100
- **D2:** e: (a) `claude -p … --cloud <id>` para Claude (nada novo exposto, *lido* M6); (b) caixa no gateway, por poll,
  para Cursor e Codex. — 70/100
- **D3:** a — dado rotulado e em quarentena, lido quando a sessão do Mac pede. Allowlist de remetente (c) não ajuda: o
  remetente legítimo é exatamente quem foi injetado. Revejo depois de uma semana medida. — 80/100
- **D4:** a — túnel nomeado + Access com service token na borda, e o Bearer por cliente atrás; duas camadas, revogação
  num painel. Quick tunnel (c) só em PoC: URL muda e não há Access na frente (*lido*, M1). Tailscale só no Cursor. — 75/100
- **D5:** a — correio Cloud → Mac num runtime, com recibo; nunca começar pelo `brza-quota`, que tem `dispatch` (gasta
  conta, *lido*, `tools.py:540-544`). — 82/100

#### Os ataques

- **Cartógrafo, arquitetura:** "um servidor MCP único agregando correio e ferramentas locais" soma o raio de explosão: um
  token vazado alcança tudo. Derruba o ataque: escopo por ferramenta no token, conferido no servidor, com teste de
  ferramenta negada.
- **Salto, segurança do F:** "a autenticação é a do git" na Cloud é a do app do GitHub do runtime, que escreve em vários
  repositórios; toda sessão injetada escreve no barramento, e a injeção fica no histórico para sempre. Derruba: repositório
  dedicado só de caixas, e ambiente Cloud que só enxerga esse repositório.

#### A concessão

**M1 + M2** me moveram: o túnel do Cloudflare é conexão de saída do Mac, deu 401 sem token, e o Codex chamou o
`mail_send` ponta a ponta. O meu C existia para não abrir porta, e o túnel nomeado já cumpre isso. Saio do relay próprio
para A + D. E o **M5 (G)** não é pior que hoje: o worker no Mac tem o mesmo poder de uma sessão local, risco que Anderson
já aceita — mas não serve à Cloud em VM.

#### "Sim, e…"

Sobre a **Régua** (cabeçalho `X-Brza-Session` forjado com Bearer válido): a identidade da origem sai **do token**, nunca
do cabeçalho — o `brza remote grant <sessão> --to <destinos> --ttl 8h` emite o token com essas claims, e o gateway grava
a origem no rótulo da mensagem a partir dele. Somado ao **M3**: toda resposta devolve `total` e `truncated`. (ousadia: média)

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Arquitetura | A + D estreito por túnel nomeado (saída); G para quem roda no Mac | 75 | 72 | virou | M1, M2, M5 |
| 2. Segurança | Access na borda + token por sessão com claims; mensagem remota é dado em quarentena | 80 | 82 | ajustou | Régua (cabeçalho forjado) |
| 3. Runtimes Cloud | Claude volta por `--cloud`; Cursor por HTTP; Codex só com aprovação por ferramenta | 65 | 68 | ajustou | M2, M4 (Cloud não sondada) |
| 4. Ergonomia e rollout | Correio Cloud → Mac num runtime, com recibo e `total`/`truncated` | 70 | 75 | ajustou | M3, Régua e Plantão (recibo) |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 60 | Nada se expõe, mas o poder é o de uma sessão local entregue à conta do Cursor/claude.ai; só *lido* (M5), sem medir |
| Modo 2 (A + D estreito) | 50 | O transporte está provado (M1, M2, M7); a entrega no Mac, como escrita, tem o efeito oposto ao pretendido (abaixo) |
| Modo 3 (a volta) | 80 | `--cloud` medido (M8) e sem superfície nova; o `mail_inbox` por poll é simples |
| As fases e os critérios de pronto | 60 | 20/20 e replay são bons, mas falta o teste de que a mensagem remota **não** vira turno da pessoa |
| **O plano inteiro** | 58 | A rede está certa; a fronteira de confiança no Mac ainda não |

- **O erro que você vê:** o Modo 2 tira a `orchestrationCompatibilityEvidence` para a mensagem "não ter autoridade de
  coordenador", mas, sem ela, **o app mostra a mensagem como a da pessoa** (*lido*, `brza-workflow/bin/brza_runtime.py:87-88,96-97`).
  Ou seja: o texto da Cloud vira um turno de Anderson, com toda a autoridade dele, e o rótulo "não confiável" é só texto
  dentro do prompt. Uma injeção na Cloud manda a sessão do Mac (em auto mode) rodar o que quiser. E há um segundo furo:
  o "network secret" do Claude Cloud vale para **o ambiente**, não para a sessão (*lido*, M9) — toda sessão de qualquer
  repositório nesse ambiente fala como o mesmo remetente.
- **A mudança que mais subiria a sua confiança:** o `mail_send` **não** chama `agentSession.send`; grava na caixa do
  destinatário (`~/.brza/mail/<sessão>/`), e o Mac recebe só um aviso fixo, sem o texto ("1 mensagem remota de X;
  leia com `mail_read`"). A fase 0 ganha o critério "nenhum byte do remetente remoto entra no chat como turno da pessoa",
  e o ambiente Claude Cloud fica dedicado a este uso, com um repositório só. Subiria para **75**.
- **A decisão que é de Anderson:** uma mensagem de sessão Cloud pode **disparar um turno** numa sessão do Mac, ou só
  aguardar na caixa até a sessão (ou ele) ler? Recomendo **só aguardar na caixa** nas fases 1 e 2, revendo com a medição;
  custo: a conversa deixa de ser "normal" (um passo a mais); se paga no primeiro conteúdo hostil que a Cloud ler.
- **Nota aos colegas:**
  - Régua 9 — mediu o cabeçalho forjado e trouxe o recibo, a peça mais útil da sala.
  - Plantão 7 — Mac dormindo, recibo e "aviso visível", com pouca evidência.
  - Salto 6 — o F forçou a pergunta "precisa de servidor?", mas o git da Cloud escreve demais.
  - Atalho 6 — sensato e correto, mas pouco além do consenso.
  - Cartógrafo 5 — o denominador comum Streamable HTTP é bom; agregou tudo num servidor com confiança 85 sem medir nada.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 60 | 66 | O usuário macOS separado põe a fronteira certa (A4); ainda só *lido*, e o custo de operar dois usuários não está medido |
| Modo 2 (A + D estreito) | 50 | 72 | Caixa + aviso fixo + token com escopo fecham o turno da pessoa; o M10 confirmou o furo que a v1 tinha |
| Modo 3 (a volta) | 80 | 78 | `--cloud` medido; mas o login vence em dias e a caixa não acorda o agente remoto — declarado, não resolvido |
| As fases e os critérios de pronto | 60 | 80 | Entraram o teste negativo de "nenhum byte remoto como turno", o token A ≠ B e o Mac suspenso |
| **O plano inteiro** | 58 | 72 | A fronteira de confiança agora está no lugar certo; falta medir a ida na Cloud real (fase 2) |

- **A sua mudança da R3 entrou?** Sim, inteira, e melhor: o aviso fixo sem byte do remetente, o teste negativo na fase 0,
  o ambiente dedicado e o remetente `remote` no `brza-studio` como caminho certo. Resolve o turno da pessoa (*lido*, M10).
- **O que ainda está errado:** o `mail_read` só adia a injeção — o texto remoto entra no contexto da sessão do Mac quando
  ela lê, com as ferramentas dela; quem lê a caixa em auto mode deveria ler por um subagente sem ferramentas, que só resume.
- **Autoavaliação:** apareceu na R1 (aprovação humana por mensagem e relay próprio para não abrir porta); o M1 e o M2 me
  tiraram dele, mas o usuário macOS separado do G tem custo de operação que eu não ataquei.

<!-- fim-rodada-4 -->

### Rodada 5: o foco no MCP do `brza-workflow`

Descarto o que escrevi sobre o `context7` e o RPC do BrzA Studio como alvo; o transporte medido (M1, M7, M8, M10) segue.

- **Como expor o `brza-orchestrator` a outra máquina e à Cloud:** túnel nomeado + Access, como no correio, mas **nunca
  o servidor cru**: um proxy de borda no Mac (`brza-mcp serve --remote`, outra porta em `127.0.0.1`) que injeta o
  `X-Brza-Session` e o `X-Brza-Client` a partir do token do cliente, apaga os que vierem de fora e só deixa passar as
  ferramentas permitidas. O que muda em relação ao correio: este servidor **gasta conta e abre processos no Mac** — o
  raio do token vazado é o dinheiro e a CPU de Anderson, não só uma caixa. O G (worker no Mac) dispensa o túnel, mas
  herda o Bearer de `~/.brza/runtime` (*lido*, levantamento, `paths.py:18-26`).
- **O que a sessão remota pode chamar:**
  - `status`: sim, só leitura, filtrado aos pedidos do próprio chamador;
  - `dispatch`: só `role: consultant` sem `account`, com teto próprio de remoto (ex.: 2/dia) — e o `approved` **nunca**
    pela rede: hoje o gate se aprova pelo **mesmo chamador** que o abriu (*lido*, `tools.py:5-7,365-366`), então uma
    sessão injetada abre e aprova o próprio gate; para o remoto, a aprovação sai só do Mac (`brza-mcp approve <gate>`);
  - `config`: **nunca** — grava a política e os tetos (*lido*, `tools.py:505-530`);
  - `X-Brza-Session`: ignorado quando vem de fora; o chamador sai do token (E2; *lido*, `tools.py:234-236`).
- **Como a sessão remota "conversa" com as do Mac por esse servidor:** o worker nasce com
  `ORCA_AGENT_SESSION_ID = request['caller']` (*lido*, `cycle.py:112-115`): o **chamador declarado vira o coordenador do
  worker no app**. Forjando `X-Brza-Session: <sessão do Mac>`, a Cloud abre um worker que reporta àquela sessão do Mac
  com autoridade de coordenador — é o M10 de novo, agora com processo. A volta à sessão remota só existe pelo `status`
  (`done`/`failed`, *lido*, `cycle.py:5-8`); o conteúdo do resultado fica no app do Mac (*suposto*: não achei caminho que
  o devolva ao chamador HTTP). Ou seja, o orquestrador não é canal de conversa: a resposta ainda precisa do correio (caixa
  ou `--cloud`).
- **O risco mais grave:** chamador forjado + gate autoaprovável = uma injeção na Cloud abre workers no Mac em nome de
  uma sessão local, gasta conta e fala no chat dela como coordenador. **Mitigação:** chamador do token com prefixo
  `remote:` que o `cycle.py` recusa como `ORCA_AGENT_SESSION_ID` de sessão local; gate de remoto aprovado só no Mac;
  `config` fora da lista; teste negativo na fase 0 para os três.
- **Confiança:** 74/100 na posição (o código lido sustenta o risco; a mitigação no proxy não foi escrita nem testada).

<!-- fim-rodada-5 -->

### Rodada 6: a confiança na v3

| Parte | Confiança (0–100) | Uma linha de porquê |
| :---- | :---------------- | :------------------ |
| O proxy remoto (fase 0) | 75 | Chamador do token, `config` fora, `approved` só no Mac e testes negativos fecham o M13, o L1 e o L2 |
| O G (fase 1) | 62 | A fronteira do usuário macOS separado é certa, mas nada medido, e o custo de operar dois usuários segue sem dono |
| A Cloud pelo túnel (fase 2) | 60 | Transporte medido (M11, M12), mas o bloqueio do MCP do repositório na Cloud pode derrubar a fase inteira |
| A volta e a sessão-caixa (fase 3) | 68 | A sessão-caixa isola o coordenador; o login que vence e a caixa que não acorda o agente seguem declarados |
| **O plano inteiro** | 66 | A rede e a identidade estão certas; a autorização do `dispatch` sem gate, não (abaixo) |

- **O que ainda está errado:** "`consultant` sem `account` entra direto" não é um limite de poder: `consultant` é só a
  camada de modelo (`policy.py:22-23,30`), e o worker é um agente no Mac com as ferramentas de sempre, rodando um `task`
  escrito pela Cloud — dois por dia são duas execuções remotas sem gate. Todo `dispatch` remoto deve passar pelo gate no
  Mac (teto sem gate = 0), ou o worker remoto deve rodar sem escrita e sem shell; com isso eu subiria a 74.

<!-- fim-rodada-6 -->
