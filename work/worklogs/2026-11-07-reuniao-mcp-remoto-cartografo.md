---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
---

# Reunião MCP remoto: a participação de Cartógrafo, o Especialista em Runtimes

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Cartógrafo** — persona o Especialista em Runtimes, no
Antigravity, modelo padrão —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Arquitetura

- **Posição:** Combinação **D + A** (servidor MCP único em Streamable HTTP agregando correio e ferramentas locais no Mac, publicado via túnel HTTPS autenticado).
- **Por quê:** O menor denominador comum de transporte entre runtimes modernos é **Streamable HTTP** (*lido*: `code.claude.com/docs/en/mcp` deprecóu SSE; `learn.chatgpt.com/docs/extend/mcp?surface=cli` não suporta SSE, só Streamable HTTP e STDIO; Cursor aceita ambos). O correio atual depende de socket Unix exclusivo do host local (*medido*: `bin/brza_runtime.py:84-110`). Um servidor MCP agregado (D) operando em Streamable HTTP elimina a necessidade de instalar daemons BrzA Studio em runtimes remotos (*suposto*), enquanto o túnel A provê conectividade sem abrir portas públicas desprotegidas no Mac (*suposto*). Alternativa E (`brza serve`) usa WebSocket proprietário (`ws://127.0.0.1:6868`, *lido*: `orca-runtime.json`), incompatível com clientes MCP padrão de agentes Cloud (*lido*).
- **Ideias:**
  - Implementar ferramentas MCP `agent_session_send` e `agent_session_inbox` dentro de `brza_mcp` repassando para o socket AF_UNIX local do Mac `(ousadia: baixa)`.
  - Unificar `brza-quota` e correio em um único endpoint Streamable HTTP `/mcp` via túnel HTTPS com Bearer token fixo `(ousadia: média)`.
- **Risco:** Suspensão/sleep do Mac ou instabilidade temporária do túnel interrompe requisições MCP ativas nos runtimes Cloud (*suposto*).
- **Confiança:** 85/100

#### 2. Segurança

- **Posição:** Isolamento estrito de capacidades no gateway MCP com autenticação Bearer via Network Secrets na Cloud e canal TLS/túnel fechado.
- **Por quê:** Claude Code Cloud suporta *network secrets* injetados pelo proxy da Anthropic sem expor credenciais na VM do agente (*lido*: `code.claude.com/docs/en/cloud-environments.md`). Cursor Cloud Agents aceita injeção de segredos por equipe ou Tailscale (*lido*: `cursor.com/docs/cloud-agent`). Codex Cloud descarta variáveis de ambiente sensíveis antes da execução do agente (*lido*: `learn.chatgpt.com/docs/environments/cloud-environment`). Jamais expor o socket Unix do runtime local diretamente, pois ele concede controle privilegiado via RPC sem granularidade de permissões (*medido*: `bin/brza_runtime.py:90-102`).
- **Ideias:**
  - Delimitar no MCP remoto apenas métodos de lista e envio de correio, bloqueando chamadas arbitrárias ao RPC do runtime `(ousadia: baixa)`.
  - Gerar tokens Bearer efêmeros por sessão com validação em tempo constante via `hmac.compare_digest` (`brza_mcp/server.py:53`) `(ousadia: média)`.
- **Risco:** Exposição inadvertida de tokens em logs de execução de agentes cloud ou vazamento da URL pública do túnel (*suposto*).
- **Confiança:** 85/100

#### 3. Runtimes Cloud

- **Posição:** O menor denominador comum (Streamable HTTP + HTTPS) funciona hoje em Claude Code e Cursor Cloud Agents; Codex Cloud está bloqueado por padrão.
- **Por quê:** Mapeamento de capacidades reais documentadas:
  | Runtime | Rede Externa | Transporte MCP | Injeção de Segredo | Suporta D+A hoje? | Fonte oficial |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **Claude Code Cloud** | Allowlist / Full | Streamable HTTP (`--transport http`) | Network Secrets / `${VAR}` | **Sim** (*lido/suposto*) | [`cloud-environments`](https://code.claude.com/docs/en/cloud-environments.md) / [`mcp`](https://code.claude.com/docs/en/mcp) |
  | **Cursor Cloud Agents** | Domínios / Tailscale | Streamable HTTP, SSE, stdio | Dashboard / env vars | **Sim** (*lido/suposto*) | [`cloud-agent`](https://cursor.com/docs/cloud-agent) / [`mcp`](https://cursor.com/docs/context/mcp) |
  | **Codex Cloud** | Bloqueada p/ agente | MCP incerto na cloud | Apenas setup script | **Não** (requer liberação de rede) | [`cloud-environment`](https://learn.chatgpt.com/docs/environments/cloud-environment) |
  | **Codex CLI (fora do Mac)** | Rede local/direta | Streamable HTTP / stdio | `config.toml` headers | **Sim** (*lido*) | [`mcp?surface=cli`](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) |
- **Ideias:**
  - Configurar script de setup para Claude Code Cloud que registra o MCP remoto com cabeçalho de autenticação via `claude mcp add --transport http` `(ousadia: baixa)`.
  - Implementar fallback CLI `brza` que consome a API HTTP do MCP quando invocado em scripts dentro da VM Cloud `(ousadia: média)`.
- **Risco:** Claude Code Cloud em modo `Trusted` rejeitar o domínio do túnel caso o host não esteja expressamente listado nos network secrets (*lido*: `code.claude.com/docs/en/cloud-environments.md`).
- **Confiança:** 85/100

#### 4. Ergonomia e rollout

- **Posição:** Rollout progressivo: validar primeiro conectividade HTTP do `brza-quota` existente via túnel, depois acoplar o correio e canal reverso.
- **Por quê:** O `brza-quota` já é um servidor HTTP funcional em Python com auth Bearer (*medido*: `packages/mcp/brza_mcp/server.py:13,48-53`), tornando-o o teste de carga e túnel de menor custo. Para comunicação reversa (Mac -> Cloud), Claude Code já oferece o canal `claude -p "msg" --cloud <session-id>` (*lido*: `code.claude.com/docs/en/claude-code-on-the-web.md`), dispensando listeners abertos na nuvem (*suposto*).
- **Ideias:**
  - Primeiro passo barato: testar chamada `curl` externa autenticada ao `brza-quota` exposto por túnel temporário em menos de 1 hora `(ousadia: baixa)`.
  - Criar utilitário `brza cloud-relay` no Mac que consome mensagens da caixa postal local e despacha para a sessão cloud usando `claude -p --cloud` `(ousadia: média)`.
- **Risco:** Latência de ida e volta (RTT) do túnel somada ao polling do agente ultrapassar 3s, degradando a dinâmica interativa. Métrica de sucesso: 100% de mensagens entregues com latência p95 < 2s entre Cloud e Mac.
- **Confiança:** 80/100

#### A ideia mais ousada desta rodada

Desenvolver um proxy MCP bidirecional que converte requisições de ferramentas remotas em chamadas de correio locais e, simultaneamente, utiliza a API do runtime (ex.: `claude -p --cloud <id>`) como canal de retorno transparente, unificando a experiência de chat local e cloud sem alterar a interface de linha de comando `brza` nem abrir portas de entrada nos ambientes Cloud (*suposto*, 75/100). Risco: dependência do ciclo de vida e estabilidade da CLI do provedor Cloud.

#### Issues candidatas

- **mcp-remote: endpoint Streamable HTTP agregador no brza_mcp** — Unificar quota e correio em servidor HTTP compatível com especificação MCP 2024-11-05 — prioridade `high`
- **mcp-remote: canal de despacho Mac->Cloud via CLI nativa (claude --cloud)** — Rotear mensagens emitidas no Mac para sessões Cloud sem exigir portas abertas no container remoto — prioridade `high`
- **mcp-remote: matriz de teste de conectividade e túnel para Claude Code e Cursor** — Validar ponta a ponta chamadas MCP autenticadas a partir de ambientes Cloud com medição de RTT — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | Combinação D+A: gateway MCP Streamable HTTP no Mac exposto por túnel HTTPS autenticado | 85 |
| 2. Segurança | Bearer token efêmero com Network Secrets (Claude) ou Tailscale (Cursor), bloqueando RPC cru | 85 |
| 3. Runtimes Cloud | Viável de imediato em Claude Code e Cursor; bloqueado por padrão no Codex Cloud | 85 |
| 4. Ergonomia e rollout | Rollout faseado a partir do brza-quota e canal reverso via claude -p --cloud com RTT < 2s | 80 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

- **D1:** (a) A + D (com G para workers self-hosted) — M1 e M2 mediram túnel funcional em 121–129 ms; F (git) quebra no Codex sem internet e gera latência excessiva para mensageria interativa — 85/100
- **D2:** (e) Híbrido: (a) `claude -p --cloud <id>` para Claude Code (M6) e (b) caixa MCP com poll/recibo para Cursor e outros runtimes — 85/100
- **D3:** (c) Depende do remetente (allowlist de sessões autorizadas) com rótulo explícito de origem remota; M2 mediu que approval policy por ferramenta já mitiga chamadas indevidas — 80/100
- **D4:** (a) Cloudflare Tunnel nomeado + Service Token — M1 provou que quick tunnel muda de URL ao reiniciar, tornando impossível fixar em Network Secrets do Claude Cloud (M6) — 85/100
- **D5:** (a) Correio Cloud → Mac no Claude Code com recibo de consumo — M2 já provou o transporte no Mac; o que resta medir de fato é M4 (alcance da VM Cloud sob rede Trusted) — 85/100

#### Os ataques

- **A Salto (Arquitetura F — git como barramento):** Supor que o agente Cloud pode usar `git push` como transporte de correio ignora que o Codex Cloud desliga a internet do agente por padrão (*lido*, levantamento B) e adiciona atrito de minutos. O ataque cai se Salto medir um `git push` automatizado pelo agente dentro do Codex Cloud com RTT < 5 s.
- **A Muralha (Quarentena onde toda mensagem vira dado passivo):** Rebaixar toda mensagem a dado inerte com aprovação manual de Anderson anula o requisito de "conversar normalmente". M2 provou que o Codex CLI suporta aprovação seletiva por ferramenta (`approval_mode="approve"`). O ataque cai se Muralha provar injeção que escape do MCP e do socket unix validado.

#### A concessão

- **M2 e M3 da síntese (Coordenação) + Régua (recibo de consumo):** M3 mediu que o corte em 4000 caracteres fez o modelo alucinar que havia zero sessões, e M2 mostrou ferramenta barrada por falta de aprovação. Abandono o aceite por simples HTTP 200: a ferramenta remota tem de retornar contagem conferível, paginação explícita e recibo de consumo reconhecido.

#### "Sim, e…"

- **Sobre a alternativa G da coordenação e os adaptadores de Atalho:** Criar um **roteador transparente de transporte** no CLI `brza` que despacha direto pelo worker/socket local quando em execução self-hosted (G), e comuta automaticamente para o gateway Streamable HTTP (D+A) quando em VM Cloud, preservando os mesmos comandos sem reconfiguração `(ousadia: média)`.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Arquitetura | A + D (com G para self-hosted) via túnel estável | 85 | 85 | ajustou | M1/M2 (túnel provado) e M5 (opção G) |
| 2. Segurança | Túnel nomeado + service token + allowlist de sessões | 85 | 85 | ajustou | Muralha (rótulo) e Régua (vínculo de destino) |
| 3. Runtimes Cloud | Prioridade Claude Cloud e Cursor; Codex condicionado à rede | 85 | 85 | não | M2 (aprovação de ferramenta) e M4 |
| 4. Ergonomia e rollout | Provar Cloud→Mac no Claude com recibo e mitigação para M3 | 80 | 85 | ajustou | M2/M3 (falha por corte) e Régua (recibo) |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 90 | Elimina a barreira de rede/túnel rodando o worker localmente sob demanda |
| Modo 2 (A + D estreito) | 80 | Conectividade robusta via Streamable HTTP, condicionada a Network Secrets na Cloud |
| Modo 3 (a volta) | 85 | M8 provou `--cloud` nativo em 2,6 s; poll no MCP fecha os demais sem portas remotas |
| As fases e os critérios de pronto | 85 | Critérios de 20/20 IDs e tolerância a corte evitam falhas silenciosas medidas em M3 |
| **O plano inteiro** | 85 | Pragmatismo baseado no menor denominador comum e medições empíricas (M1 a M8) |

- **O erro que você vê:** Afirmar na tabela 'As alternativas' e Fase 1 que o Claude Cloud exige rede Custom: a doc (*lido*: `code.claude.com/docs/en/cloud-environments.md`, levantamento B:20) estabelece que hosts com *network secrets* ficam acessíveis mesmo em rede *Trusted*; M7 falhou porque o `curl` puro não usou o proxy com secret.
- **A mudança que mais subiria a sua confiança:** Promover a Fase 3 (Modo 1 / G) para Fase 0.5: validar os workers locais de Cursor/Claude em poucas horas entrega uso imediato do celular sem custos de domínio ou túnel; subiria a confiança para **92/100**.
- **A decisão que é de Anderson:** Qual o nível de autonomia permitido na execução local pelo Modo 1 (G), já que o agente Cloud ganha poder de shell no Mac? *Recomendação:* Liberar o Modo 1 apenas para branches autorizadas e manter tarefas autônomas no Modo 2.
- **Nota aos colegas:**
  - **Régua (10/10):** Rigor exemplar com E1/E2, refutou a falsa segurança de cabeçalhos e fixou o recibo de consumo.
  - **Muralha (9/10):** Impediu a exposição do RPC bruto e garantiu que mensagem remota não vire tarefa executável.
  - **Atalho (8/10):** Pragmatismo valioso no desenho do gateway enxuto A+D e foco na entrega rápida.
  - **Plantão (8/10):** Voz necessária da ergonomia real, alertando para o Mac dormindo e a dor do silêncio operacional.
  - **Salto (6/10):** Boa provocação inicial, mas o modelo git (F) desconsiderou as restrições reais de rede e latência.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 90 | 85 | Isolar em usuário macOS separado resolve A4, mas adiciona atrito operacional local |
| Modo 2 (A + D estreito) | 80 | 85 | Caixa com aviso fixo e network secrets em Trusted eliminam injeção e o M10 |
| Modo 3 (a volta) | 85 | 80 | `setup-token` do Claude vence em dias (A10) e Cursor sem wakeup exige espera ativa |
| As fases e os critérios de pronto | 85 | 90 | G promovido para a Fase 1 e critérios com observáveis estritos (M3, M10, R3) |
| **O plano inteiro** | 85 | 88 | Separação rigorosa entre medido e inferido com roteamento específico por runtime |

- **A sua mudança da R3 entrou?** Sim, integralmente: o G foi promovido para a Fase 1 e a doc de *network secrets* alcançáveis em rede *Trusted* foi corrigida em M9/Modo 2.
- **O que ainda está errado:** No Cursor Cloud (Modo 3), a caixa não acorda o agente após o fim do turno; é preciso formalizar a restrição de espera ativa.
- **Autoavaliação:** Sim: na R1 assumi que a doc de MCP e secrets garantia o carregamento do `.mcp.json` na VM Cloud, até M7 e A3 alertarem que isso ainda é inferido.

<!-- fim-rodada-4 -->

### Rodada 5: o foco no MCP do `brza-workflow`

- **Como expor o `brza-orchestrator` a outra máquina e à Cloud:** O servidor já é Streamable HTTP nativo em `127.0.0.1:4242` com Bearer HMAC (*lido*: `brza_mcp/server.py:1-20`). Diferente do correio, não exige criar novo daemon MCP: basta expô-lo via túnel HTTPS autenticado (Cloudflare Tunnel nomeado / Tailscale) com o Bearer em Network Secrets (Claude) ou segredos de equipe (Cursor); no Modo 1 (G), o worker local consome `127.0.0.1` diretamente sem túnel.
- **O que a sessão remota pode chamar:** `status` liberado; `dispatch` permitido apenas para tarefas com gate obrigatório (aprovação humana no Mac para runtime/account que gasta); `config` com gravação **estritamente bloqueada** (*lido*: `tools.py:526-530` grava no SQLite global). O `X-Brza-Session` vindo do cliente deve ser descartado (*medido*: E2); o `CallContext` deve ser fixado pelo token do cliente no servidor.
- **Como a sessão remota "conversa" com as do Mac por esse servidor:** O `dispatch` enfileira a requisição na fila SQLite local do Mac (*lido*: `tools.py:263`, `queue.py:100`) e dispara `on_queued()` (*lido*: `tools.py:440`) para admitir o worker localmente. A resposta volta pela leitura de `status(caller)` (*lido*: `tools.py:456-465`), que consulta `recent_finished` no banco; a sincronização é via *polling* de estado (`queued -> running -> done`).
- **O risco mais grave e a mitigação:** Injeção de prompt ou token vazado chamando `config` para reescrever políticas de limites ou disparando `dispatch` em massa para esgotar quotas. Mitigação: tornar `config` somente leitura para acessos remotos, forçar gates em dispatches remotos e atrelar a identidade do caller rigidamente ao token de acesso.
- **Confiança:** 85/100

<!-- fim-rodada-5 -->

### Rodada 6: a confiança na v3

| Parte | Confiança (0–100) | Uma linha de porquê |
| :---- | :---------------- | :------------------ |
| O proxy remoto (fase 0) | 90 | M13 e L1 provaram que a porta crua é insegura; vincular o caller ao token no proxy elimina o spoofing |
| O G (fase 1) | 90 | Worker local em usuário macOS isolado acessando o proxy loopback entrega valor sem risco de túnel |
| A Cloud pelo túnel (fase 2) | 80 | M11/M12 mediram o orquestrador real via túnel, mas o carregamento de MCP na VM Cloud segue por confirmar |
| A volta e a sessão-caixa (fase 3) | 85 | Desacopla o worker remoto da autoridade local (L2) e usa canal `--cloud` validado em M8 |
| **O plano inteiro** | 88 | Alinhamento técnico exemplar ao `brza-orchestrator`, sustentado em medições reais (M11–M13, L1–L3) |

- **O que ainda está errado:** Falta prever fallback via setup script (`claude mcp add`) caso a sessão Claude Cloud não carregue o `.mcp.json` do repositório.

<!-- fim-rodada-6 -->
