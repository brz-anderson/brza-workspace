---
scope:
  - brza-workflow
  - brza-studio
  - workspace
tags:
  - tooling
  - infra
refs:
  - issue:correio-remoto-por-mcp-para-sessoes-fora-do-mac
  - issue:fila-de-saida-se-o-mac-dormindo-perder-correio
  - issue:mcp-do-mac-no-codex-cloud
  - issue:perfil-remoto-de-poucos-metodos-no-rpc-do-brza-studio
  - issue:proxy-remoto-de-autorizacao-no-brza-mcp
  - issue:reuniao-multiagente-com-personas-pelo-brza-sessions
  - issue:sessao-cloud-executando-no-mac-pelo-worker
---

# Reunião MCP remoto: a coordenação e a proposta de arquitetura

O pedido de Anderson, em 2026-11-07, na sessão `reuniao-mcp-remoto` (workstream `playground`): "Encontrar maneiras de
usar o MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (Claude Code Cloud/web, Cursor
Cloud Agents, Codex Cloud, etc.). Requisito duro: as sessões remotas devem conseguir se comunicar normalmente com as
sessões rodando localmente no Mac (o correio entre sessões (…) e os servidores MCP do workspace (…))", numa reunião de
seis personas que replicasse o fluxo da [Reunião Carvão em Brasa: a coordenação e a proposta de plano](2026-11-07-reuniao-carvao-em-brasa-coordenacao.md),
com prova de conceito, revisor independente, proposta com confiança medida e issues, até as 22h15.

## O que se fez

> [!IMPORTANT]
>
> **A correção de Anderson, às 21h37:** "o MCP do tema é o do brza-workflow (o servidor MCP dele, ex.: brza_quota;
> veja ~/Projects/brza-workflow, tests/mcp/ e bin/brza-install), não o context7 nem o MCP do BrzA Studio. Foque o
> levantamento e as provas de conceito nele (…) Quem já levantou algo sobre outros MCPs, descarte." As rodadas 1 a 4 e a
> primeira prova trataram o correio entre sessões e citaram o `context7`; o que elas mediram de transporte (túnel, Cloud,
> volta, a mensagem remota como a da pessoa) segue valendo, e o resto foi descartado. As rodadas 5 e 6, a segunda prova
> e a proposta v3 são sobre o servidor do `brza-workflow`, o `brza-orchestrator`.

### O formato da reunião

Seis personas, uma por sessão de chat no checkout `.worktrees/playground`, abertas por um lançador no scratch da
reunião que importa o `brza-sessions` e repassa `--model` e `--effort` ao `brza agent launch` (o `brza sessions` não os
repassa), gravando o nome, o modelo e o esforço no mapa `.sessions/sessions.jsonl`. Conduzidas por `brza sessions send`.
Os pedidos, as sínteses, a proposta e o material ficaram em `.sessions/reuniao-mcp-remoto/`, fora do git.

| Persona | Papel | Runtime, modelo e esforço | Por quê, pelo papel | Worklog |
| :------ | :---- | :------------------------ | :------------------ | :------ |
| Muralha | a Arquiteta de Rede e Segurança | Claude Opus 5.5 `high` | modelo de ameaça e julgamento | [Reunião MCP remoto: a participação de Muralha, a Arquiteta de Rede e Segurança](2026-11-07-reuniao-mcp-remoto-muralha.md) |
| Régua | o Cético que mede | Codex `gpt-6-astra` `xhigh` | mede e refuta: o maior esforço | [Reunião MCP remoto: a participação de Régua, o Cético que mede](2026-11-07-reuniao-mcp-remoto-regua.md) |
| Atalho | o Engenheiro Pragmático | Codex `gpt-6.1-terra` `medium` | o modelo de código, sem pensar demais | [Reunião MCP remoto: a participação de Atalho, o Engenheiro Pragmático](2026-11-07-reuniao-mcp-remoto-atalho.md) |
| Salto | o Provocador | Grok `grok-4.7-build-fast` `low` | ideação rápida | [Reunião MCP remoto: a participação de Salto, o Provocador](2026-11-07-reuniao-mcp-remoto-salto.md) |
| Plantão | o Usuário cansado | Claude Haiku 5.5 `low` | a voz de quem usa | [Reunião MCP remoto: a participação de Plantão, o Usuário cansado](2026-11-07-reuniao-mcp-remoto-plantao.md) |
| Cartógrafo | o Especialista em Runtimes | Antigravity, modelo padrão (recusa modelo explícito) | um quarto runtime, com busca na web | [Reunião MCP remoto: a participação de Cartógrafo, o Especialista em Runtimes](2026-11-07-reuniao-mcp-remoto-cartografo.md) |

**A pauta:** (1) arquitetura; (2) segurança; (3) runtimes Cloud; (4) ergonomia e rollout. As alternativas de partida:
A túnel para o MCP local, B MCP hospedado, C relay só de saída, D o `brza` como servidor MCP único, E o runtime remoto
do BrzA Studio. A sala acrescentou F (o git como barramento, do Salto) e a coordenação, G (a Cloud executando no Mac).

**O marcador de fim, com uma regra só:** "cada rodada acrescenta a sua seção no fim do arquivo, e a última linha do
arquivo é `<!-- fim-rodada-N -->`", igual no briefing e em cada pedido. Monitorado por `grep`; **18 de 18 marcadores
no lugar certo** (24 de 24, conferidos pela última linha de cada worklog), contra três personas com o marcador duplicado na reunião anterior.

| Rodada | Aberta | Fechada | O que produziu |
| :----- | :----- | :------ | :------------- |
| 1 · opinião independente | 21h19 | 21h23 | 24 posições com confiança, ideias marcadas por ousadia, 16 issues candidatas; três arquiteturas em disputa (A+D, C+D, F) |
| 2 · debate | 21h23 | 21h25 | votos em cinco disputas; duas viradas por dado (Muralha C → A+D, Salto F → G) |
| 3 · confiança no plano v1 | 21h28 | 21h30 | a confiança por parte, o erro mais grave, a mudança que mais subiria, a decisão de Anderson, as notas aos colegas |
| 4 · confiança final na v2 | 21h33 | 21h35 | a confiança por parte, se a mudança pedida entrou, o que ainda está errado, a autoavaliação |
| 5 · o foco corrigido: o `brza-orchestrator` | 21h36 | 21h41 | como expô-lo, o que a sessão remota pode chamar, como a resposta volta, o risco mais grave — cinco de seis (o Régua ficou sem cota do Codex) |
| 6 · confiança na v3 | 21h45 | 21h46 | a confiança por parte na v3 — quatro de seis (Régua e Atalho, no Codex, sem cota desde 21h41) |

Um levantamento do papel `collector` (Sonnet) correu em paralelo à rodada 1 e gravou
`.sessions/reuniao-mcp-remoto/material/levantamento.md`. Um revisor independente (o papel `reviewer`) leu a v1 fora da
sala.

### A prova de conceito da coordenação

Para a disputa técnica, a coordenação provou em vez de argumentar:

- **Servidor:** um MCP streamable HTTP mínimo (Python puro, ~130 linhas, no scratch), Bearer comparado por `hmac`, só em
  `127.0.0.1:8765`, com `sessions_list` e `mail_send` (allowlist de destino: esta sessão).
- **Túnel:** `cloudflared tunnel --url` (quick tunnel). Pela URL pública: **401 sem token**; `ping` autenticado 5×,
  **121–129 ms** de ida e volta do Mac pela borda.
- **Codex CLI como cliente** (`mcp_servers.correio.url` + `bearer_token_env_var`): `initialize` e `tools/list` passaram,
  mas o `codex exec` barrou a ferramenta ("MCP tool call requires approval, but approval policy is never") até
  `tools.<tool>.approval_mode="approve"`. Depois, `sessions_list` e `mail_send` ok, ~200 ms no servidor, 13 s o `exec`;
  o `brza sessions send` respondeu "sent".
- **Claude Code como cliente** (`-p`, Haiku, `--mcp-config` com o token só no `headersHelper`): 6 s, resposta certa.
- **Falha silenciosa real:** a primeira versão cortava a saída em 4000 caracteres (a lista tem 6890), e o Codex afirmou
  "0 sessões `mcp-`" — eram 6. Com `total` e corte declarado, o Claude acertou.
- **Uma sessão Claude Code Cloud real** (`claude --cloud`, aberta num pseudo-terminal; lida pelo `get_run_log`): na rede
  padrão, o proxy de saída recusou o túnel e o `mcp.context7.com` — `403 connect_rejected`, "the host is not allowed for
  this session". A VM subiu em ~2 s; a sonda inteira, 9 s.
- **A volta Mac → Cloud:** `claude -p "…" --cloud <session-id>` enfileirou em 1,5 s, e a sessão Cloud respondeu
  "volta-ok" ~2,6 s depois. **Sem túnel.**
- **Achado no `--help`:** o `cursor-agent worker` sem `--pool` registra o Mac como "My Machines worker (no Enterprise plan
  needed)", e o Cloud Agent do Cursor executa as ferramentas aqui, só por conexão de saída; o `claude --environment
  <ccpool_…>` abre sessão Cloud num ambiente self-hosted.
- **O que não se provou:** a sessão Cloud com rede Custom ou "network secret" alcançando o túnel; o Cursor Cloud; o
  worker; o túnel nomeado com Access.
- **Derrubado às 21h28:** o túnel e o servidor parados, a porta 8765 fechada, a URL antiga devolvendo 530, o token
  apagado. A sessão Cloud da sonda ficou na conta, ociosa.

### A segunda prova: o `brza-orchestrator` real

Depois da correção, a coordenação expôs o servidor do `brza-workflow` (`packages/mcp/bin/brza-mcp serve --port 4343`,
o código do checkout `d1fa1d7`) com um `BRZA_HOME` isolado no scratch: fila vazia e token próprio, porque o `serve` liga
um agendador que abre worker para o que estiver na fila (`brza_mcp/cycle.py:1-8`), e a fila real tem 13 pedidos.

- **Pelo quick tunnel:** 401 sem token; `/health` 127–161 ms; o `GET /mcp` (SSE) fica aberto pelo túnel.
- **Claude Code** (`-p`, Haiku, `headersHelper` com o Bearer): chamou `status` pela URL pública em 6 s, com a resposta
  certa ("0 pedidos na fila, 0 gates e 0 workers abertos").
- **O chamador forjado:** pelo túnel, com o Bearer e `X-Brza-Session: claude_sessao_do_mac_forjada`, um `dispatch` de
  papel `implementer` gravou o pedido `gated` com esse chamador; nenhum worker abriu. Pelo código, o mesmo cabeçalho
  aprovaria o gate (`tools.py:5-7,365-366`), e o worker nasceria com `ORCA_AGENT_SESSION_ID` igual ao chamador
  (`cycle.py:111-116`). A coordenação não chamou a aprovação.
- **O Codex não rodou contra ele:** a conta bateu o limite de uso às 21h41 ("try again at Nov 8th, 2026 1:00 AM"), o
  que também tirou o Régua da rodada 5. (Antes disso, a coordenação perdeu 3 min com um `codex exec` esperando o stdin.)
- **Derrubada às 21h42:** o túnel e o servidor parados, a porta 4343 fechada, a URL antiga devolvendo 530, o token
  isolado apagado. O agente `com.brza.orchestrator` do launchd não foi tocado: segue carregado e sem processo, com o
  `/health` sem resposta, como estava.

### O que a sala mediu além da coordenação

- **Régua, E2:** com Bearer válido, o servidor de transporte do `brza-workflow` aceitou `Origin` de fora e um
  `X-Brza-Session: sessao-forjada` — o cabeçalho não prova identidade; ela tem de vir do token, no servidor.
- **Régua, E1:** `brza sessions list` 10/10, mediana 193 ms.
- **Régua, contraprova da rodada 3:** o `send_to_chat` gera um `clientOperationId` novo em cada chamada
  (`brza-workflow/bin/brza_runtime.py:141-145`), com a mesma impressão do conteúdo: o reenvio não se deduplica sozinho.
- **Muralha, rodada 3 (lido, conferido pela coordenação):** sem a `orchestrationCompatibilityEvidence`, "o app mostra a
  mensagem como a da pessoa" (`brza_runtime.py:87-88,96-97`). A v1 propunha tirar a autoridade de coordenador da mensagem
  remota, e isso a entregaria como **turno de Anderson** — o oposto do pretendido.
- **Cartógrafo, rodada 3 (lido):** a doc do Claude Cloud diz que o host com "network secret" fica alcançável mesmo na
  rede Trusted; a sonda M7 não tinha secret.

### As personas: como cada tipo se comportou

| Persona (runtime) | Latência R1 / R2 / R3 | Custo | Confiança R1 (média) → plano v1 (R3) → v2 (R4) | Viradas | Nota dos colegas |
| :---------------- | :-------------------- | :---- | :----------------------------------- | :------ | :--------------- |
| Muralha (Opus `high`) | 1:24 / 0:46 / 0:41 | US$ 1,04 | 72,5 → 58 → 72 | C → A+D, pelo M1/M2 | 9,0 |
| Régua (Astra `xhigh`) | 4:06 / 2:18 / 2:02 | 1,74 M tokens de entrada (95% em cache), 21 mil de saída | 78,8 → 68 → 76 | — | **9,4** |
| Atalho (Terra `medium`) | 1:18 / 1:01 / 0:35 | 0,71 M de entrada (91% em cache), 8 mil de saída | 77,5 → 55 → 65 | — | 6,6 |
| Salto (Grok Fast `low`) | ≤ 2:20 / 0:46 / 0:26 | sem medição | 63,8 → 55 → 64 | F → G, pelo M2/M5 | 6,2 |
| Plantão (Haiku `low`) | 0:37 / 0:50 / 0:24 | **US$ 0,05** | 55 → 50 → 55 | — | 7,8 |
| Cartógrafo (Antigravity) | ≤ 2:20 / 1:01 / 0:47 | sem medição | **83,8 → 85 → 88** | — | 6,0 |

- **O dado moveu quem o argumento não moveria.** As duas viradas da rodada 2 vieram da prova (M1, M2, M5): a Muralha
  largou o relay próprio porque "o túnel nomeado já cumpre" o não abrir porta; o Salto largou o git porque "atravessou,
  sem git".
- **O Antigravity repetiu o padrão da reunião anterior:** a maior confiança da sala em todas as rodadas (83,8 na R1, 85
  no plano), afirmações de "funciona hoje" antes da prova Cloud que a M7 derrubou, e as menores notas dos colegas
  ("a confiança 85 em D+A não sobreviveu ao M7"). Agora o efeito aparece num papel técnico, não no empático — reforça
  que a superconfiança é do modelo.
- **O cético e a segurança foram os mais úteis**, de novo: Régua (9,4) e Muralha (9,0). Os dois acharam os erros que
  mudaram o plano — o cabeçalho forjado, o reenvio sem deduplicação e a entrega como turno da pessoa.
- **A voz do usuário no Haiku `low` custou US$ 0,05 nas três rodadas** e trouxe o único ponto que ninguém mais levantou e
  que sobreviveu: o Mac dormindo. Foi a confiança mais baixa da sala (50), coerente com a evidência.
- **Os papéis rápidos foram rápidos:** Plantão (Haiku) e Salto (Grok Fast) fecharam as rodadas 2 e 3 em menos de um
  minuto; o Régua (`xhigh`) levou 2–4 min por rodada, e foi o único que rodou contraprova em todas.
- **A autoavaliação da rodada 4 achou o vício em cinco de seis:** a Muralha (relay e aprovação humana por mensagem),
  o Atalho (as 4–8 h subestimadas), o Salto (o barramento sem caminho), o Plantão (o "zero passo" sem pesar a segurança)
  e o Cartógrafo (a doc tomada como garantia); o Régua, "em parte" (a instrumentação antes de quem espera).
- **Na correção de foco, a sala releu o código sozinha e convergiu em 5 min:** cinco de cinco (rodada 5) recusaram
  expor a porta 4242 crua, e quatro acharam, cada uma por si, o chamador do cabeçalho e o gate aprovado pelo mesmo
  chamador. A Muralha achou o que a coordenação e o revisor não tinham escrito na v3: `consultant` é a camada de modelo,
  não um limite de poder.
- **A cota do Codex acabou no meio da reunião** (21h41, até a 1h): o Régua e o Atalho, os dois Codex, perderam as
  rodadas 5 e 6 (o Atalho fechou a 5 antes do limite). Reunião com papel crítico num runtime só tem esse ponto único de
  falha.
- **O custo:** as duas sessões Claude, US$ 1,09 nas três rodadas; o levantamento do `collector`, 75 mil tokens; o Codex,
  pelos `token_count` do rollout; o Grok e o Antigravity seguem sem medição.

### A proposta de arquitetura (v3.3, 21h50, não aprovada)

> Rascunho da coordenação. **A v3 segue a correção de Anderson às 21h37:** o MCP do tema é o servidor do
> `brza-workflow`, não o `context7` nem o do BrzA Studio; o que se levantou sobre os outros foi descartado (a v2.1, do
> correio, está em `proposta-v2.1.md`). Montada com as rodadas 1 a 5 das personas, as duas provas de conceito da
> coordenação e o revisor independente. **Nada aqui está decidido.** Evidência: **[medido]** rodou hoje, com a saída;
> **[lido]** código, doc ou `--help`; **[inferido]** ninguém testou. Origem: **R3–R6**, as rodadas; **revisor**.

#### O requisito

Expor o servidor MCP do `brza-workflow` a outras máquinas e a sessões Cloud (Claude Code, Cursor, Codex), com as
sessões remotas conversando com as sessões locais do Mac.

#### O servidor

O **`brza-orchestrator`** (`~/Projects/brza-workflow/packages/mcp/`, ligado pelo `brza install --mcp`): "O servidor MCP
residente do BrzA Studio: Python stdlib, MCP Streamable HTTP, sob o launchd" (`brza_mcp/__init__.py:1`), label
`com.brza.orchestrator`, porta 4242, só em `127.0.0.1`, Bearer em `~/.brza/runtime` (`server.py:1-20`). Três ferramentas
(`tools.py:535-546`):

- **`dispatch`** pede um worker. Só `role: consultant` sem `account` entra direto; outro papel ou troca de conta devolve um
  gate, aprovado "pelo mesmo chamador" com `approved` (`tools.py:5-7`).
- **`status`** dá a fila, os gates, os workers e os tetos.
- **`config`** lê e grava a política (`tools.py:505-530`).

Hoje o agente do launchd está carregado, mas sem processo, e o `/health` não responde.

#### O que se mediu e se leu

| # | Fato | Marca |
| :- | :--- | :---- |
| M11 | **O `brza-orchestrator` real** (código do checkout, `BRZA_HOME` isolado no scratch, fila vazia, token próprio), exposto por quick tunnel: 401 sem token; `/health` 127–161 ms pela borda; o `GET /mcp` (SSE) fica aberto pelo túnel | [medido] |
| M12 | **Claude Code** (`-p`, Haiku, `--mcp-config` com `headersHelper`) chamou `status` pela URL pública: 6 s, resposta certa ("0 pedidos, 0 gates, 0 workers") | [medido] |
| M13 | **Pelo túnel, com o Bearer e um `X-Brza-Session` forjado**, o `dispatch` de papel `implementer` gravou o pedido `gated` com `caller = claude_sessao_do_mac_forjada`; nenhum worker abriu | [medido] |
| L1 | O chamador vem do cabeçalho `X-Brza-Session` (`server.py:111`; `tools.py:234-236`); o gate só confere se quem aprova é o mesmo chamador (`tools.py:365-366`): **quem forja o cabeçalho abre e aprova o próprio gate** | [lido] (R5: Muralha, Salto, Atalho, Plantão) |
| L2 | O worker nasce com `ORCA_AGENT_SESSION_ID = caller` (`cycle.py:111-116`): **o chamador declarado vira o coordenador do worker no app** — com o cabeçalho forjado, um worker aberto da Cloud se reporta a uma sessão do Mac com autoridade de coordenador | [lido] (R5, Muralha) |
| L3 | O `status` devolve o estado e o `error` dos pedidos, não o texto do worker (`queue.py:228-231`, `tools.py:456-500`): **o orquestrador não é canal de conversa**; a resposta precisa de outro caminho | [lido] (R5, Salto, Muralha, Atalho) |
| M1–M2 | O transporte por túnel com Bearer funciona, e o Codex CLI consome MCP remoto com `bearer_token_env_var` e aprovação por ferramenta (que é automática) — medido no servidor da primeira prova; **no `brza-orchestrator` o Codex não rodou: a conta bateu o limite de uso às 21h41** | [medido] |
| M7 | Sessão Claude Code Cloud real, rede padrão, sem network secret: o proxy de saída recusou o host do túnel (`403 connect_rejected`) | [medido] |
| M8 | A volta Mac → Cloud: `claude -p "…" --cloud <id>` enfileirou em 1,5 s; a sessão Cloud respondeu ~2,6 s depois | [medido] |
| M10 | A mensagem que o `brza sessions send` entrega a partir de um processo remoto chega na virada de turno (~12 min na prova) e como mensagem **da pessoa**; o app só conhece `worker \| coordinator \| none` (`brza-studio/src/shared/agent-session/agent-session-message-source.ts:1,18`) | [medido] |
| M5 | `cursor-agent worker` ("My Machines", sem Enterprise, só conexão de saída) e `claude --environment <ccpool_…>` executam o agente Cloud **neste Mac** | [lido] |
| M9 | Claude Cloud: o "network secret" fica fora da VM, o host com secret fica alcançável em Trusted, e o secret é do ambiente; se a sessão carrega o MCP do repositório não está confirmado. Codex Cloud: internet desligada por padrão, segredos só no setup. Cursor Cloud: MCP de time, segredo injetado na VM | [lido] |

#### As alternativas

| Alternativa | Atende? | Custo | Risco | Se paga |
| :---------- | :------ | :---- | :---- | :------ |
| **Túnel direto para a porta 4242** | Tecnicamente sim (M11, M12) | Horas | **Inaceitável:** qualquer portador do Bearer forja o chamador, aprova o próprio gate, abre workers que gastam conta e falam como coordenador de uma sessão do Mac (M13, L1, L2), e grava a política pelo `config` | Nunca |
| **Proxy remoto de autorização + túnel nomeado + Access** | Sim para VM Cloud e outra máquina, com o host liberado na Cloud (M7, M9) | 2–3 dias no `brza-workflow` + o túnel; um domínio na Cloudflare | Médio: com o token vazado, abre-se só gate; nada roda sem Anderson | Na primeira semana em que uma sessão em VM precisar pedir trabalho ao Mac |
| **G — o agente Cloud executa no Mac** | Sim, sem túnel; não serve à VM | 0,5 dia, num usuário macOS separado | Nenhuma porta, mas a conta do Cursor ou do claude.ai vira credencial do Mac; o worker lê o `~/.brza/runtime` se rodar no mesmo usuário | Agora, se o caso real é abrir do celular ou da web |
| **Relay/fila só de saída** | Sim, e sobrevive ao Mac dormindo | Dias + um serviço | Baixo no Mac | Só se a medição mostrar perda com o Mac suspenso |

#### A recomendação da sala (v3)

**Nunca expor a porta 4242 crua.** Cinco de cinco personas na R5 (o Régua ficou sem cota) e a prova M13.

1. **Um proxy remoto no próprio `brza-mcp`** — por exemplo, `brza mcp serve --remote`, noutra porta em `127.0.0.1`, que
   repassa ao orquestrador:
   - **o chamador sai do token:** um token por cliente remoto, mapeado no servidor a `remote:<cliente>`; o proxy
     **reescreve** o `X-Brza-Session` a partir do token (não basta apagar: sem o cabeçalho, o `caller_of` usa o argumento
     `caller` do corpo, `tools.py:196-199`) e apaga dos argumentos o `caller` e o `approved` (E2, M13; revisor);
   - **allowlist de campos do `dispatch`:** só `task` e `ref`; o `runtime`, o `model`, o `effort`, o `account`, o
     `target` e a `priority` ficam com a política do Mac, para que quem chama de fora não escolha o que gastar (revisor);
   - **`status`:** só os pedidos do próprio chamador;
   - **`dispatch`: todo pedido remoto vira gate** (teto sem gate = 0). O `consultant` é a camada de modelo, não um limite
     de poder (`policy.py:22-23`): o worker é um agente no Mac com as ferramentas de sempre, rodando uma tarefa escrita
     pela Cloud (R6, Muralha);
   - **o gate remoto se aprova só no Mac:** o `approved` nunca vem pela rede; aprova-se por um verbo novo (`brza mcp
     approve <gate>`), que mostra o texto **no terminal, para Anderson** — nunca pela sessão principal, que leria a tarefa
     escrita de fora antes de ele decidir; e o `status` local não mostra o `task` de pedido remoto a uma sessão de
     agente (`tools.py:290,466-477`; revisor). **Isso muda o orquestrador:**
     hoje o `approve()` só aceita o mesmo chamador (`tools.py:365-366`); o gate de motivo `remote` passa a aceitar um
     aprovador local (revisor);
   - **`config`:** fora da lista.
2. **O worker de um pedido remoto não se pendura numa sessão do Mac.** O `cycle.py` recusa `remote:` como
   `ORCA_AGENT_SESSION_ID` de sessão local (L2). O pedido ganha um campo **`coordinator_chat`**, que o proxy preenche com
   o chat da **sessão-caixa** do cliente (`remote-<cliente>`, aberta no Mac); o `caller` segue `remote:<cliente>` para o
   filtro do `status` e o teto (revisor). A caixa recebe o relatório do worker **pelo app**, como coordenadora — é dela,
   e não do orquestrador, que sai o texto da volta (L3; R6, Salto).
   - **A caixa é o novo alvo de injeção (revisor):** o relatório veio de uma tarefa escrita de fora e chega como
     `worker`, com autoridade sobre ela. Por isso a caixa roda **sem Bash e sem `ORCA_AGENT_SESSION_ID`** — com Bash ela
     chamaria o `rpc('agentSession.send')` direto (`brza_runtime.py:84-117`) — e devolve só por um **verbo próprio do
     `brza-mcp`** (por exemplo, `reply`), que faz o `--cloud` ou grava o `inbox` (revisor).
3. **A conversa volta pelo correio (L3):** a sessão-caixa devolve o resultado à sessão remota pelo verbo `reply` do
   `brza-mcp` — no Claude, que faz o `claude -p … --cloud <id>` (M8), com `claude setup-token` (o login interativo vence entre 2026-11-09 e 11-12); nos
   outros, por um `inbox` que a sessão remota lê pelo proxy — o `status` não traz o texto (L3) —, que **não acorda o
   agente** (no Cursor, só com o agente em espera ativa). A mensagem remota que entra numa sessão do Mac vai como dado,
   nunca como turno da pessoa (M10); o remetente `remote` no `brza-studio` é a decisão D1.
4. **Por runtime:**
   - **Claude Cloud:** ambiente dedicado, com o token do proxy como network secret do host do túnel. **Bloqueio:** a
     sessão Cloud carregar o MCP do repositório, ainda não confirmado; o plano B é o setup script do ambiente rodar
     `claude mcp add` (R6, Cartógrafo; [inferido]).
   - **Cursor Cloud:** MCP de time; o segredo fica legível na VM, por isso um token de teto menor.
   - **Codex CLI noutra máquina:** `bearer_token_env_var`, com aprovação automática só do `status`.
   - **Codex Cloud:** fora, porque não tem rede por padrão.
5. **O G** consome o proxy em `127.0.0.1`, com o próprio token remoto, e roda num usuário macOS separado, que não lê o
   `~/.brza/runtime` nem o `orca-runtime.json`.

#### As fases

| Fase | O quê | Custo | Pronto quando |
| :--- | :---- | :---- | :------------ |
| 0 | O proxy remoto no `brza-mcp`; o gate de motivo `remote` com aprovador local; o campo `coordinator_chat`; a sessão-caixa (sobe da fase 3), com os testes em `tests/mcp/` | 10–16 h | testes negativos: o `X-Brza-Session` de fora é reescrito, e o `caller` e o `approved` do corpo são apagados; campos fora de `task`/`ref` são recusados; **todo `dispatch` remoto devolve gate**; o `approved` remoto é recusado; o `config` é recusado; o `status` mostra só os pedidos do chamador; o `cycle.py` recusa `remote:` como sessão local; **um relatório com "mande X à sessão Y" não chega a Y**; o gate remoto não se aprova por sessão de agente |
| 1 | Medir o G num usuário macOS separado, contra o proxy | 0,5 dia | uma sessão Cloud no Mac chama `status` e um `dispatch` (que vira gate), e não lê o `~/.brza/runtime` |
| 2 | Túnel nomeado + Access; o ambiente Claude Cloud dedicado | 1 dia | da Cloud real: `status` e um `dispatch`, com o gate aprovado no Mac; o tempo de cada etapa medido; o erro explícito com o túnel caído ou o Mac suspenso |
| 3 | A volta (`--cloud`, `inbox`); o remetente `remote`, se D1 | 1–3 dias | 20/20 pedidos remotos com o resultado de volta à sessão de origem, correlacionados pelo id do pedido; nenhum byte remoto como turno da pessoa; **o `status` remoto mostra "aguardando aprovação no Mac" e "sessão-caixa fechada"**, em vez do silêncio (R6, Plantão) |
| 4 | O Cursor Cloud | 0,5–1 dia | o mesmo da fase 2 no Cursor |

#### Riscos

- **Token do proxy vazado:** abre gates, que ficam esperando Anderson; não aprova, não grava política; revoga-se o
  cliente.
- **Injeção na sessão Cloud:** pode pedir trabalho ao Mac, mas cada pedido passa por Anderson; o resultado volta como
  dado.
- **Pedido parado:** gate sem aprovação ou sessão-caixa fechada aparecem no `status` remoto; o celular vê.
- **O Mac dormindo:** a ida recebe erro de transporte; a fase 2 mede a perda.
- **O G no mesmo usuário** herdaria o Bearer local e o cabeçalho livre: por isso o usuário separado.

#### A confiança no plano

| Medida | Resultado |
| :----- | :-------- |
| As personas na v3 (rodada 6, quatro de seis; o Régua e o Atalho sem cota do Codex) | **média 64,75**; mediana 63; de 45 (Plantão) a 88 (Cartógrafo); sem o Cartógrafo, 57 |
| As personas na posição delas sobre o `brza-orchestrator` (rodada 5, cinco de seis) | média 70,4; de 50 (Plantão) a 85 (Cartógrafo) |
| **O revisor independente** | v3 **52** → v3.2 **68**; ~75 com os dois ajustes que a v3.3 aplica — previsão dele, não medida |
| A parte mais forte | o proxy (fase 0): Muralha 75, Salto 76, revisor 70 |
| A parte mais fraca | a volta (fase 3): Salto 44, Plantão 45, revisor 60 — o orquestrador não traz o texto, e o canal ainda não existe |
| O histórico do foco anterior (o correio, descartado) | v1: sala 61,8, revisor 45; v2: sala 70,0; v2.1: revisor 62 |

**A confiança do plano é a do revisor, 68** (v3.2), porque o número de fora pesa mais que o da sala: nas duas
reuniões, quem leu sem ter escrito ficou abaixo dos autores. **Provado por comando:** o transporte (M1, M11), o 401, o
consumo pelo Claude (M12) e pelo Codex (M2, no servidor da primeira prova), a Cloud padrão recusando o host (M7), a
volta pelo `--cloud` (M8), a mensagem remota como a da pessoa (M10) e o chamador forjado na fila (M13). **Inferência:**
o proxy, a sessão-caixa, o G, a Cloud com network secret e o Cursor.

## O que ficou

- **A proposta v3.3 não está aprovada** (a v2.1, do correio, ficou em `.sessions/reuniao-mcp-remoto/proposta-v2.1.md`). As decisões de Anderson foram à rodada de perguntas na sessão, às 21h52:
  por onde começar (D1), o gate remoto (D2), como a mensagem remota chega às sessões do Mac (D3) e o alcance do
  primeiro marco (D4). Aprovada, ela vira plano pelo `brza note plan-open`.
- **A rodada respondida por Anderson, na sessão, na virada para 2026-11-08** — as quatro na opção recomendada:
  - **D1, por onde começar:** "Proxy, depois o G" — a fase 0 (o proxy no `brza-mcp`), depois o G num usuário macOS
    separado; túnel e domínio só depois.
  - **D2, o gate remoto:** "Sempre, no terminal" — todo `dispatch` remoto vira gate, aprovado só por `brza mcp approve
    <gate>`.
  - **D3, a chegada:** "Sessão-caixa agora" — a sessão-caixa isolada na fase 0; o remetente `remote` no `brza-studio` na
    fase 3.
  - **D4, o alcance:** "Parcial: Claude primeiro" — Claude Cloud e outra máquina; o Cursor na fase 4; o Codex Cloud fora.

  São respostas de rodada, não a aprovação da proposta: o texto da v3.3 ainda espera o aceite explícito para virar
  plano.
- **As issues abertas pela reunião:**
  - [O proxy remoto de autorização no brza-mcp](../issues/proxy-remoto-de-autorizacao-no-brza-mcp.md) — a fase 0 da v3, o trabalho principal;
  - [O correio remoto por MCP para sessões fora do Mac](../issues/correio-remoto-por-mcp-para-sessoes-fora-do-mac.md) — a volta da conversa, a fase 3;
  - [A sessão Cloud executando no Mac pelo worker](../issues/sessao-cloud-executando-no-mac-pelo-worker.md) — o modo 1 (G), a medir;
  - [O MCP do Mac no Codex Cloud](../issues/mcp-do-mac-no-codex-cloud.md) — investigação;
  - [A fila de saída, se o Mac dormindo perder correio](../issues/fila-de-saida-se-o-mac-dormindo-perder-correio.md) — com gatilho na medição;
  - [O perfil remoto de poucos métodos no RPC do BrzA Studio](../issues/perfil-remoto-de-poucos-metodos-no-rpc-do-brza-studio.md) — a alternativa E;
- **A issue do fluxo** ganhou a seção da segunda reunião: [A reunião multiagente com personas pelo `brza sessions`](../issues/reuniao-multiagente-com-personas-pelo-brza-sessions.md).
- **A limpeza fora do workspace** depende de Anderson: apagar a sessão Cloud da sonda e, se o túnel não for adiante,
  `brew uninstall cloudflared`.
- **As sessões das personas** seguem abertas (`mcp-muralha`, `mcp-regua`, `mcp-atalho`, `mcp-salto`, `mcp-plantao`,
  `mcp-cartografo`), para uma rodada a mais se as decisões pedirem.

## Fora do workspace

- `brew install cloudflared` (o binário em `/opt/homebrew/bin/cloudflared`), para o túnel da prova. Desfaz com
  `brew uninstall cloudflared`.
- Um quick tunnel do Cloudflare (`*.trycloudflare.com`) ficou no ar das 21h20 às 21h28, protegido por Bearer; derrubado.
- Um segundo quick tunnel, para o `brza-orchestrator` com `BRZA_HOME` isolado, das 21h38 às 21h42; derrubado.
- Uma sessão Claude Code Cloud (`session_01FdZC1snXduZTvgS7PdeCMT`) na conta claude.ai, aberta para a sonda de rede e
  ociosa; apaga-se em claude.ai/code.
