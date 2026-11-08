---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
---

# Reunião MCP remoto: a participação de Atalho, o Engenheiro Pragmático

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Atalho** — persona o Engenheiro Pragmático, no
Codex gpt-6.1-terra medium —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Arquitetura

- **Posição:** A + D mínimo: um gateway MCP no Mac para correio e quota, acessível por túnel autenticado; investigar E como reaproveitamento, sem presumir que já resolve o correio.
- **Por quê:** *lido* (98/100): `brza_runtime.py:84-102` escolhe socket Unix e envia `agentSession.send`; *lido* (90/100): `brza-workflow/packages/mcp/brza_mcp/server.py:13,48-53,153-155` já oferece HTTP local para quota. *Suposto* (60/100): hospedar quota sem Mac acrescentaria adaptação de estado e operação.
- **Ideias:** 1. Adaptador MCP `send/list/inbox` junto ao socket existente, preservando origem e recibos (ousadia: média; *suposto*, 65/100). 2. Proxy de rotas para quota e correio, evitando agregar protocolos antes de medir compatibilidade (ousadia: baixa; *suposto*, 70/100).
- **Risco:** *suposto* (85/100): Mac desligado ou túnel indisponível interrompe tudo; `brza serve` headless pode apontar para outro runtime e não enxergar as sessões do app.
- **Confiança:** 70/100

#### 2. Segurança

- **Posição:** expor apenas gateway de capacidades delimitadas, com TLS e identidade revogável, mantendo sockets e tokens internos no Mac.
- **Por quê:** *lido* (95/100): o RPC local usa `authToken` e aceita método/params em `brza_runtime.py:90-102`; *lido* (90/100): `web-pairing.ts:98,149-150` trata o pareamento como material de autenticação. *Suposto* (85/100): entregar esse token geral à Cloud ampliaria o impacto de vazamento.
- **Ideias:** 1. Credencial distinta por cliente, rotação e revogação, com autorização por ferramenta (ousadia: baixa; *suposto*, 80/100). 2. Bloquear chamadas arbitrárias ao RPC e registrar metadados sem texto nem segredo (ousadia: baixa; *suposto*, 85/100).
- **Risco:** *suposto* (80/100): túnel autenticado não impede agente comprometido de abusar de permissões concedidas; revisar envio, leitura e dados pessoais antes de abrir acesso.
- **Confiança:** 85/100

#### 3. Runtimes Cloud

- **Posição:** nenhuma combinação foi comprovada de ponta a ponta hoje; priorizar Claude e Cursor como candidatos, deixando Codex Cloud condicionado a teste.
- **Por quê:** *lido* (85/100): [Claude Cloud environments](https://code.claude.com/docs/en/cloud-environments) documenta rede configurável e network secrets; não comprova aqui o carregamento do MCP específico. *Lido* (80/100): [Cursor Cloud Agent](https://cursor.com/docs/cloud-agent) descreve MCP e segredos. *Lido* (75/100): [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) documenta a CLI, sem comprovar disponibilidade no Cloud; fontes reunidas em `.sessions/reuniao-mcp-remoto/material/levantamento.md`, seção B.
- **Ideias:** 1. Testar uma ferramenta inofensiva HTTP com autenticação em cada runtime e registrar erro e latência (ousadia: baixa; *suposto*, 90/100). 2. Quando MCP custom falhar, avaliar cliente CLI por HTTPS apenas se rede e segredo estiverem disponíveis (ousadia: média; *suposto*, 65/100).
- **Risco:** *suposto* (85/100): allowlist, provisionamento de segredos ou suporte MCP da sessão podem invalidar o túnel; suporte à CLI local não prova suporte Cloud.
- **Confiança:** 80/100

#### 4. Ergonomia e rollout

- **Posição:** provar primeiro um percurso completo e observável, depois generalizar; estimativa inicial de 4–8 horas para protótipo, sem compromisso de produção.
- **Por quê:** *lido* (95/100): `brza_runtime.py:130-144` já monta a mutação e chama o envio; *suposto* (55/100): reuso reduz código, mas autenticação, compatibilidade Cloud e recibos podem multiplicar a estimativa.
- **Ideias:** 1. Primeiro passo barato: 1–2 horas para inspecionar o contrato de `brza serve` e testar localmente adaptador `list/send`, sem túnel (ousadia: baixa; *suposto*, 60/100). 2. Em experimento autorizado posterior, medir envios aceitos e efetivamente recebidos / tentativas, latência p95 e falhas explícitas por runtime; meta inicial 10/10 em teste controlado (ousadia: baixa; *suposto*, 75/100).
- **Risco:** *suposto* (85/100): aceitação não é entrega; reenvio após timeout pode duplicar mensagem. Exigir ID idempotente, recibo e erro visível antes de uso cotidiano.
- **Confiança:** 75/100

#### A ideia mais ousada desta rodada

*Suposto* (55/100): adaptar o pareamento existente do BrzA Studio para autenticar o gateway MCP e reutilizar sua gestão de dispositivos, se o contrato permitir; isso pode eliminar um segundo cadastro. Risco: acoplar permissões MCP ao acesso amplo do runtime; só avançar após verificar escopo e revogação (`brza-studio/src/renderer/src/web/web-pairing.ts:98-128`).

#### Issues candidatas

- **Provar correio entre Cloud e sessão local** — *suposto* (85/100): verificar entrega, origem, recibo e duplicação antes de generalizar — prioridade `high`.
- **Delimitar autenticação e permissões do gateway** — *suposto* (85/100): evitar que credencial remota conceda RPC irrestrito — prioridade `high`.
- **Medir compatibilidade de MCP por runtime Cloud** — *lido/suposto* (80/100): documentação não comprova o percurso completo específico; fontes na seção 3 — prioridade `high`.

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | Gateway mínimo no Mac e túnel autenticado | 70 |
| 2. Segurança | Credenciais revogáveis e capacidades delimitadas | 85 |
| 3. Runtimes Cloud | Claude e Cursor candidatos; Codex Cloud por verificar | 80 |
| 4. Ergonomia e rollout | Prova local seguida de entrega medida por runtime | 75 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

- **D1: e** — *suposto*: A + D só para correio em VM Cloud ou outra máquina; G como opção separada para quem aceita execução no Mac. *Lido* (síntese M2/M5): o túnel funcionou com Codex CLI, não Cloud; o worker promete execução local, ainda sem prova. 80/100.
- **D2: d** — *suposto*: usar `claude -p --cloud <id>` para Claude e adaptador por provedor nos demais; inbox com poll é fallback, com consumo explícito e limitação de turno visível. *Lido* (síntese M6; Régua, R1 arquitetura): enfileirar não prova consumo. 75/100.
- **D3: a** — *suposto*: entregar como dado rotulado em caixa consultada pela sessão, sem promoção automática a tarefa; testar se ainda atende à conversa normal. *Lido* (Muralha, R1 segurança; `brza_runtime.py:87-97`): o envio atual pode marcar origem de coordenador. 80/100.
- **D4: a** — *suposto*: túnel nomeado com Access e token de serviço para piloto estável, sujeito a teste de compatibilidade com headers de cada runtime; Tailscale para máquinas na tailnet. *Lido* (síntese M1): quick tunnel muda de URL e só provou Bearer no servidor de teste. 65/100.
- **D5: a** — *suposto*: uma semana para provar Cloud real → Mac e volta, com recibo de consumo e ID, reaproveitando M2; se só a ida fechar, declarar parcial. *Lido* (síntese M2–M4): CLI local passou; VM Cloud e volta não foram sondadas. 85/100.

#### Os ataques

- **Salto, git como barramento:** *suposto* (85/100): clone e escrita local não provam push nem entrega durante o turno; histórico e reconciliação adicionam operação. *Lido* (Salto, R1 runtimes): push no Cursor/Codex é hipótese. Derrubaria: demonstração bidirecional nas Clouds, com recibo, retenção e custo operacional medidos.
- **Cartógrafo, agregador e quota primeiro:** *suposto* (85/100): publicar quota junto aumenta capacidades e não prova correio nem retorno. *Lido* (Régua, R1 segurança e E2): `dispatch`/`config` existem e identidade declarada é forjável com Bearer válido. Derrubaria: proxy somente `status`, escopo validado e prova de que esse passo reduz o caminho crítico do correio.

#### A concessão

*Lido* (90/100): Régua mostrou em E2 que Bearer válido aceita identidade declarada arbitrária; retiro minha ideia de proxy genérico de quota e exijo vínculo servidor→identidade/destino. *Lido* (95/100): M3 expôs truncamento silencioso; paginação, total e indicador de corte viram critério do piloto.

#### "Sim, e…"

*Suposto* (75/100): sobre o destinatário virtual de **Régua**, manter um registro mínimo por provedor com `operation_id`, estado `queued`/`delivered`/`consumed` e capacidade de entrada durante turno; o adaptador Claude usa a CLI e os demais só ganham selo após teste `(ousadia: média)`. Risco: não haver evento de consumo confiável; nesse caso o estado fica desconhecido.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Arquitetura | Gateway só correio; G opcional no Mac | 70 | 80 | ajustou | Régua, M2, M5 |
| 2. Segurança | Identidade vinculada e mensagem em quarentena | 85 | 90 | ajustou | Régua E2, Muralha |
| 3. Runtimes Cloud | Nenhuma Cloud validada; CLI já demonstrada | 80 | 85 | ajustou | M2, M4 |
| 4. Ergonomia e rollout | Prova nos dois sentidos com consumo e corte explícito | 75 | 85 | ajustou | Régua, M3 |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 65 | *Lido*: M5 descreve os workers; falta medir se enxergam as sessões e MCPs da instalação atual e qual acesso concedem. |
| Modo 2 (A + D estreito) | 60 | *Medido pela coordenação*: M2 e M7 provam CLI e bloqueio Cloud padrão; Custom, Access e as duas credenciais juntos ainda não foram provados. |
| Modo 3 (a volta) | 65 | *Medido pela coordenação*: M8 mostra resposta no Claude; *suposto*: poll nos outros pode não acordar uma sessão durante o turno. |
| As fases e os critérios de pronto | 55 | *Lido*: fase 1 exige consumo, mas não define o evento que o comprova; a fase 2 tampouco mede quota e `context7` ponta a ponta. |
| **O plano inteiro** | 55 | *Suposto*: bom piloto de correio, ainda sem demonstrar o requisito integral nem sustentar estimativas de 1–2 dias. |

- **O erro que você vê:** *lido* (95/100): proposta, seções «O requisito», «As alternativas» e «Fica de fora agora»: A + D é declarado suficiente, mas o plano exclui `brza-quota`, cujo uso remoto integra o requisito; M7 também não prova que liberar o host ou `context7` em Custom funcione. Confiança na inferência: 95/100.
- **A mudança que mais subiria a sua confiança:** *suposto* (80/100): inserir uma fase zero curta para provar, numa Cloud real, Custom + Access + ambas credenciais, `mail_send`/resposta e leitura de quota `status` com identidade restrita; declarar `consumido` só com confirmação observável, senão `desconhecido`. Com 20 IDs em ambos os sentidos e MCPs exigidos efetivamente acessíveis, confiança do plano subiria de 55 para 80/100; 2–4 h de investigação são estimativa não medida (45/100).
- **A decisão que é de Anderson:** *suposto* (90/100): aceita um primeiro piloto que entrega apenas correio, deixando quota e os demais MCPs para fase posterior? Recomendo sim, desde que o marco seja chamado parcial e o requisito completo permaneça aberto.
- **Nota aos colegas:** *avaliação* (70/100): Muralha 9/10 — ameaça e autoridade; Régua 10/10 — medições e recibos; Salto 8/10 — alternativa sem serviço dedicado; Plantão 8/10 — visibilidade de falha; Cartógrafo 8/10 — integração e mapeamento.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 65 | 60 | *Lido* (v2, modo 1): usuário separado exige ponte ainda não demonstrada; reduz acesso direto, mas adiciona trabalho. |
| Modo 2 (A + D estreito) | 60 | 70 | *Lido* (v2, modo 2): caixa, escopo e idempotência tratam falhas; integração Cloud e aviso continuam por provar. |
| Modo 3 (a volta) | 65 | 70 | *Medido pela coordenação* (M8); *lido* (v2, modo 3): Cursor exige espera ativa, limite agora explícito. |
| As fases e os critérios de pronto | 55 | 70 | *Lido* (v2, fases 0–3): observáveis e replay melhoraram; *medido pela coordenação* (M10): aviso pode levar 14 minutos. |
| **O plano inteiro** | 55 | 65 | *Suposto*: piloto parcial mais honesto e verificável, ainda dependente de provas Cloud, isolamento e custo real. |

- **A sua mudança da R3 entrou?** *Lido* (95/100): em parte; marco parcial, recibos observáveis e teste Cloud entraram, mas quota só leitura não tem critério de pronto explícito e as duas credenciais ainda precisam ser provadas juntas.
- **O que ainda está errado:** *lido* (95/100): fase 3 prevê `brza-quota` status, mas seu pronto só exige Cursor e `context7`; acrescente consulta real de status sem acesso a `dispatch`/`config` e mantenha o requisito integral aberto (v2, «As fases»).
- **Autoavaliação:** *avaliação* (85/100): sim; minha estimativa inicial de 4–8 h subestimou isolamento, idempotência e o atraso real revelado por M10.

<!-- fim-rodada-4 -->

### Rodada 5: o foco no MCP do `brza-workflow`

- **Como expor o `brza-orchestrator` a outra máquina e à Cloud:** *suposto* (75/100): manter servidor existente em loopback e pôr um gateway MCP de autorização diante de túnel nomeado autenticado; primeiro provar outra máquina e uma Cloud real. Ao contrário do correio proposto, aqui reaproveitamos as três ferramentas existentes e sua fila, filtrando capacidades; não basta um proxy HTTP transparente. *Lido* (98/100): `packages/mcp/brza_mcp/server.py:1-4,18,48-53,153-155` mostra transporte e Bearer único; M7 só demonstrou bloqueio na configuração testada. Claude, Cursor e Codex Cloud dependem de prova por runtime.
- **O que a sessão remota pode chamar:** *suposto* (80/100): `status` limitado aos próprios pedidos e dados necessários; `dispatch` de consultor dentro de teto e papéis permitidos, com token individual revogável; `config` fica local. Gate de papel ou conta exige aprovação humana independente no Mac, jamais aceitar `approved` do mesmo token remoto. *Lido* (98/100): `tools.py:230-238,260-280,356-369,499-500,515-528` mostra gate, aprovação pelo chamador, visibilidade ampla e escrita de política. Gateway deve remover `X-Brza-Session`, `caller` e `X-Brza-Client` fornecidos pelo cliente e injetar identidade e cliente fixados pelo servidor; bloquear argumentos e headers equivalentes. Bearer local permanece no Mac.
- **Como a sessão remota “conversa” com as do Mac por esse servidor:** *lido* (95/100): `tools.py:265-271,437-452,456-501` devolve pedido e estado, e `cycle.py:112-115` passa `caller` em `ORCA_AGENT_SESSION_ID` ao worker; `status` lista metadados de concluídos, não o texto da resposta. *Suposto* (80/100): uma identidade Cloud não é automaticamente uma sessão local válida; falta ponte explícita de resultado/inbox e teste de ida e volta, inclusive entre sessões já existentes. `dispatch` sozinho não comprova conversa normal.
- **O risco mais grave:** *suposto* (90/100): Cloud comprometida falsifica chamador ou aprova gate e abre worker com poder e custo no Mac. Mitigar com vínculo autenticado, remoção de headers, autorização por ferramenta e destino, teto e aprovação independente; testar forja, replay e negação antes de expor. *Lido* (95/100): `server.py:107-113` aceita o header e `tools.py:196-200,365-366` usa a identidade para gate.
- **Confiança:** 75/100 na direção; 40/100 na viabilidade ponta a ponta até testar retorno, gates e runtime Cloud. Descarto as propostas anteriores relativas a `context7` e MCP do BrzA Studio, conforme a correção.

<!-- fim-rodada-5 -->
