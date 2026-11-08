---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
refs:
  - PLN-011
  - PLN-014
---

# Reunião MCP remoto: a participação de Régua, o Cético que mede

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Régua** — persona o Cético que mede, no
Codex gpt-6-astra xhigh —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

As posições são propostas da persona, não decisões de Anderson. A confiança de cada bloco vale para a recomendação; cada evidência abaixo tem sua própria confiança. Nenhum teste atravessou uma Cloud nem enviou mensagem a sessão real.

#### 1. Arquitetura

- **Posição:** *suposto* — A + D reduzido ao correio, condicionado à prova nos dois sentidos; não agregaria todos os MCPs na primeira versão.
- **Por quê:** *lido*, 99/100 — o correio usa `AF_UNIX` e o token local (E3); um túnel HTTP sozinho não adapta esse protocolo nem cria um destinatário Cloud.
- **Por quê:** *medido*, 99/100 — o transporte MCP existente respondeu a `initialize`, `tools/list` e 30/30 ecos locais (E2); isso prova transporte local, não integração com runtime Cloud.
- **Ideias:** *suposto* — criar adaptador MCP `list/send/inbox` com registro de identidade remota e recibo por `operation_id`, preservando os comandos locais (ousadia: média).
- **Ideias:** *suposto* — separar endereço HTTP dos MCPs e endereço do correio; experimentar C somente se persistência durante indisponibilidade do Mac for requisito (ousadia: baixa).
- **Risco:** *suposto* — a Cloud consegue chamar `send`, mas não receber uma resposta durante o turno; polling sem integração ao runtime não satisfaz sozinho “conversar normalmente”. E é alternativa a testar, não evidência de MCP disponível.
- **Confiança:** 65/100.

#### 2. Segurança

- **Posição:** *suposto* — não publicar o servidor atual diretamente; autenticação externa precisa restringir sessão, destino e ferramenta.
- **Por quê:** *medido*, 99/100 — E2 deu 401 sem credencial e com credencial incorreta, mas aceitou `Origin: https://untrusted.invalid` e `X-Brza-Session: sessao-forjada` com credencial válida. Não é bypass de autenticação: o cabeçalho não prova identidade.
- **Por quê:** *lido*, 99/100 — `server.py:48–53,111–113` valida o Bearer e passa cabeçalhos ao handler; `tools.py:540–545` registra `dispatch`, `status` e `config`, não apenas consulta de quota.
- **Ideias:** *suposto* — gateway com credencial individual revogável, vínculo servidor→sessão e lista de destinos; manter o token do runtime exclusivamente no Mac (ousadia: média).
- **Ideias:** *suposto* — antes do túnel, testar credencial revogada, identidade forjada, destino proibido e origem inválida; todos devem falhar sem chamar o handler (ousadia: baixa).
- **Risco:** *suposto* — um Bearer compartilhado transforma identidade declarada pelo cliente em autoridade; encaminhar `config` ou `dispatch` amplia o impacto do acesso remoto.
- **Confiança:** 90/100.

#### 3. Runtimes Cloud

- **Posição:** *suposto* — começar por Claude Cloud com um repositório ou Cursor Cloud; Codex Cloud fica sem selo de compatibilidade até teste específico. Hoje, nenhum foi validado ponta a ponta nesta rodada.
- **Por quê:** *lido*, 95/100 — [Claude Cloud](https://code.claude.com/docs/en/cloud-environments#what-carries-over-from-your-setup) carrega `.mcp.json` em sessão com um repositório, mas não instala plugins declarados em `enabledPlugins`; o plugin local context7 não basta como configuração remota.
- **Por quê:** *lido*, 95/100 — [Cursor Cloud](https://cursor.com/docs/cloud-agent#mcp-support) documenta MCP de equipe, HTTP/stdio e OAuth. Isto sustenta candidato a teste, não entrega do correio.
- **Por quê:** *lido*, 90/100 — [Codex Cloud, página marcada Legacy](https://learn.chatgpt.com/docs/environments/cloud-environment) remove secrets antes da fase do agente e desliga internet por padrão nessa fase; a [doc MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) consultada não comprova que o Cloud legado carrega a configuração da CLI.
- **Ideias:** *suposto* — em cada produto, executar `initialize → tools/list → tools/call` após o setup e registrar superfície, autenticação e resultado, separadamente (ousadia: baixa).
- **Ideias:** *suposto* — testar entrada de mensagem no turno Cloud por adaptador próprio do provedor; fallback por cliente HTTP só conta se preservar identidade, recibo e recebimento no turno (ousadia: média).
- **Risco:** *suposto* — confundir CLI em VM, Codex Cloud legado e ChatGPT Work Cloud; uma conexão MCP de saída não comprova mensagem de entrada.
- **Confiança:** 75/100 na ordem dos testes; 30/100 na cobertura ponta a ponta dos três produtos.

#### 4. Ergonomia e rollout

- **Posição:** *suposto* — primeiro passo barato: reaproveitar o teste local isolado E2 e fixar o contrato de ida e volta antes do piloto remoto da coordenação.
- **Por quê:** *medido*, 99/100 — `brza sessions list` passou 10/10, mediana 192,645 ms, intervalo 187,12–226,35 ms (E1); o eco local passou 30/30, mediana 0,2535 ms (E2). São operações distintas; não somar nem extrapolar para a internet.
- **Ideias:** *suposto* — piloto com 20 mensagens sintéticas por sentido, IDs distintos, resposta correlacionada e reenvio do mesmo ID; critério: 20/20 recebidas e nenhuma duplicata visível (ousadia: baixa).
- **Ideias:** *suposto* — interromper e retomar a conexão no piloto; mostrar `accepted`, `queued`, `delivered`, `failed` e tempo desde o último contato, sem declarar entrega no HTTP 200 (ousadia: média).
- **Métrica de sucesso:** *suposto* — p95 de entrega ≤5 s com sessões conectadas, excluindo geração da resposta pelo modelo; erro explícito em desconexão. É meta proposta, não número medido. Disponibilidade e atraso offline são medidos à parte.
- **Risco:** *suposto* — uma demonstração de `curl` ou eco passa enquanto o agente remoto nunca recebe o correio. O aceite exige que o destinatário reconheça o mesmo ID.
- **Confiança:** 85/100.

#### Evidências e reprodução

**E1 — medido, 99/100.** Comando executado: `brza sessions list`, dez vezes sequenciais via `subprocess.run`, `capture_output=True`, timeout 15 s e `PYTHONDONTWRITEBYTECODE=1`; duração por `time.perf_counter()`, incluindo criação do processo. Saída de cada execução: exit 0, 40 linhas em stdout, zero em stderr. O conteúdo das sessões foi suprimido; não interpreto 40 linhas como prova de entrega.

| Execução | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| :------- | -: | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| ms | 226,35 | 194,34 | 196,31 | 187,12 | 187,13 | 190,95 | 205,61 | 207,31 | 188,92 | 190,56 |

**E2 — medido, 99/100.** Código de `brza-workflow`, HEAD `d1fa1d7`; servidor real de transporte com registro fictício, sem instalar as ferramentas do orquestrador, sem SQLite nem conta real. Script executado por stdin, sem arquivo auxiliar:

```bash
python3 -B - <<'PY'
import sys,threading,secrets,http.client,json,time,statistics,socket
sys.path.insert(0,'/Users/andepb/Projects/brza-workflow/packages/mcp')
from brza_mcp.server import make_server
from brza_mcp.registry import ToolRegistry
registry=ToolRegistry()
registry.register('echo','Eco fictício',lambda args,ctx: {'echo':args.get('text'),'session':ctx.session})
token=secrets.token_hex(32)
s=make_server(0,token,registry);s.quiet=True
thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
address=s.server_address
print('bind='+str(address))
def request(method,path,body=None,authenticated=True,extra=None):
    c=http.client.HTTPConnection(*address,timeout=2)
    headers={'Content-Type':'application/json'}
    if authenticated: headers['Authorization']='Bearer '+token
    headers.update(extra or {})
    c.request(method,path,body=json.dumps(body) if body is not None else None,headers=headers)
    r=c.getresponse();payload=r.read();c.close()
    return r.status,json.loads(payload) if payload else None
try:
    print('sem_credencial='+str(request('GET','/health',authenticated=False)[0]))
    print('credencial_incorreta='+str(request('GET','/health',extra={'Authorization':'Bearer incorreto'})[0]))
    print('health_autenticado='+str(request('GET','/health')[0]))
    print('initialize='+str(request('POST','/mcp',{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18'}})))
    print('tools/list='+str(request('POST','/mcp',{'jsonrpc':'2.0','id':2,'method':'tools/list'})))
    samples=[]
    for i in range(30):
        start=time.perf_counter()
        status,body=request('POST','/mcp',{'jsonrpc':'2.0','id':i+3,'method':'tools/call','params':{'name':'echo','arguments':{'text':str(i)}}})
        assert status==200 and json.loads(body['result']['content'][0]['text'])['echo']==str(i)
        samples.append(round(1000*(time.perf_counter()-start),3))
    print(json.dumps({'echo_ok':len(samples),'mediana_ms':statistics.median(samples),'min_ms':min(samples),'max_ms':max(samples),'p95_nearest_rank_ms':sorted(samples)[28]}))
    result=request('POST','/mcp',{'jsonrpc':'2.0','id':40,'method':'tools/call','params':{'name':'echo','arguments':{'text':'x'}}},extra={'Origin':'https://untrusted.invalid','X-Brza-Session':'sessao-forjada'})
    print('origin_e_identidade_arbitrarios='+str(result))
finally:
    s.stop_event.set();s.shutdown();s.server_close();thread.join(2)
    probe=socket.socket();print('porta_fechada='+str(probe.connect_ex(address)!=0));probe.close()
PY
```

Saída resumida: bind `127.0.0.1:58579`; sem credencial 401; credencial incorreta 401; health autenticado 200; initialize 200/protocolo `2025-06-18`; tools/list 200/uma ferramenta `echo`; echo_ok 30; mediana 0,2535 ms; mínimo 0,209 ms; máximo 0,326 ms; p95 por posto mais próximo 0,307 ms. Com Origin arbitrário e token válido, tools/call devolveu 200 e `session: sessao-forjada`. `porta_fechada=True`. Cada chamada abriu uma conexão HTTP nova. SSE, concorrência, negociação com cliente MCP real e rede externa não foram testados.

**E3 — lido, 99/100.** Caminhos relativos a `/Users/andepb/Projects/brza-workflow`: `bin/brza_runtime.py:84–102` escolhe transporte Unix; `packages/client/bin/brza-sessions:341–345` chama `send_to_chat`; `packages/mcp/brza_mcp/server.py:18,48–53,98–113,153–155` contém bind, autenticação e despacho; `packages/mcp/brza_mcp/tools.py:535–545` instala as três ferramentas. Correção ao material comum: `packages/mcp/bin/brza-quota:41–63` é CLI de consulta/gravação de amostras, não o servidor HTTP; não executei essa CLI.

**Limites — lido, 99/100.** Conferidos os bloqueios ativos: PLN-014 impede emenda das issues e porte antes da entrevista; PLN-011 impede merge da fase 1 e passos seguintes antes de C1. Esta rodada apenas investiga e acrescenta este worklog. Não li opiniões das outras personas.

#### A ideia mais ousada desta rodada

*Suposto*, 45/100 — representar cada sessão Cloud como destinatário virtual do correio local, com uma identidade e inbox durável; um adaptador por provedor injeta as mensagens no turno e confirma consumo. Isso preservaria o endereçamento da pessoa, sem fingir que HTTP recebido significa agente avisado. Risco: alguns provedores não oferecem entrada no turno em execução; nesses casos, declarar recebimento somente no próximo turno e avaliar se atende ao requisito.

#### Issues candidatas

- **Provar correio Cloud↔Mac com identidade e recibo** — *suposto*, 95/100: E2 só prova eco local; falta o requisito duro — prioridade `high`.
- **Vincular credencial remota a sessão e destino** — *suposto*, 95/100: E2 aceita identidade declarada por quem possui o Bearer — prioridade `high`.
- **Validar MCP e credenciais na fase do agente de cada Cloud** — *suposto*, 90/100: as docs distinguem superfícies e o Codex legado retira secrets após setup — prioridade `high`.

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | A + D restrito ao correio; ida e volta como condição | 65 |
| 2. Segurança | Credencial vinculada à sessão, destino e ferramenta | 90 |
| 3. Runtimes Cloud | Claude/Cursor primeiro; Codex Cloud ainda sem prova | 75 |
| 4. Ergonomia e rollout | Aceitar por recibo de consumo, não por HTTP 200 | 85 |

## Fora do workspace

- **O quê e onde:** *medido*, 99/100, E2: processo Python com servidor de teste em `127.0.0.1:58579`, porta efêmera e token aleatório somente em memória. **Risco:** acesso de outro processo local durante o teste; registro só continha `echo`, sem capacidades reais. **Estado:** encerrado, porta fechada confirmada; nenhum arquivo auxiliar criado. **Como desfazer:** já desfeito pelo `finally`, com `shutdown`, `server_close` e fim do processo.

<!-- fim-rodada-1 -->

### Rodada 2: debate

Fontes: `S` = `.sessions/reuniao-mcp-remoto/sintese-1.md:21–49`; M1–M6 são *lidos* por mim, com medições atribuídas à coordenação. Os votos são *supostos* (propostas), com confiança na recomendação, não selo de funcionamento Cloud.

#### As disputas

- **D1: a** — A + D estreito para VM Cloud e outra máquina. *Lido*, S/M1–M2: já houve ferramenta pelo túnel e envio ao Mac; isso aumenta minha confiança de 65 para 78. G fica como modalidade separada para execução no Mac, não substitui o requisito de VM remota (S/M5) — **78/100**.
- **D2: a** — no primeiro runtime, Claude, usar o canal nativo para sessão existente, atrás de um adaptador de identidade e recibo. *Lido*, S/M6: o comando enfileira; consumo ainda precisa de prova. Inbox MCP fica candidato para os demais; polling não comprova que o agente recebeu durante o turno — **75/100**.
- **D3: a** — dado rotulado em inbox, consumido explicitamente pela sessão do Mac, sem herdar autoridade de coordenador; não exijo aprovação humana por mensagem. *Lido*, Muralha R1:50–56 e `brza_runtime.py:95–97`: o wrapper atual acrescenta evidência de coordenação. Allowlist autentica remetente, não torna seu conteúdo confiável — **92/100**.
- **D4: a** — túnel nomeado + Access com service token, mantendo autorização por sessão/destino no gateway. *Lido*, S/M1: o quick tunnel muda de URL; isso prejudica configuração estável. *Suposto*: validar headers e renovação no cliente Cloud; o teste de Bearer no quick tunnel não valida Access — **65/100**.
- **D5: a** — uma semana para provar Cloud real → Mac, com recibo correlacionado retornando ao Claude Cloud. *Lido*, S/M2–M4: começar por quota repete conectividade já demonstrada e não fecha o correio. Critério proposto: 20/20 IDs consumidos, zero duplicatas no replay, erro explícito em desconexão e aprovação limitada às ferramentas do piloto — **90/100**.

#### Os ataques

- **Salto, arquitetura/runtimes:** *lido*, [Reunião MCP remoto: a participação de Salto, o Provocador](2026-11-07-reuniao-mcp-remoto-salto.md), R1:41–44,60. Ler o clone sem rede não demonstra transportar resposta nova; snapshot de quota também não oferece as ferramentas MCP exigidas. Derruba meu ataque: medir ida e volta durante a fase do agente na configuração restrita declarada, mais uma chamada MCP real; caso contrário F atende somente uma parte do pedido — **95/100**.
- **Cartógrafo, rollout:** *lido*, [Reunião MCP remoto: a participação de Cartógrafo, o Especialista em Runtimes](2026-11-07-reuniao-mcp-remoto-cartografo.md), R1:59–64. Depois de M2, quota primeiro mede um substituto do objetivo; seus 2 s não decorrem dos 121–129 ms de ping nem dos 13 s de exec. Derruba meu ataque: demonstrar uma dependência de quota que bloqueie o correio e medir separadamente transporte, entrega e consumo numa Cloud real — **90/100**.

#### A concessão

M1–M2 me movem: A + D deixou de ter só meu eco em loopback; há envio Codex CLI→Mac relatado, ainda sem prova de Cloud VM. Muralha me move de autorização por credencial para mensagem tratada como dado, sem autoridade herdada (*lido*, [Reunião MCP remoto: a participação de Muralha, a Arquiteta de Rede e Segurança](2026-11-07-reuniao-mcp-remoto-muralha.md), R1:50–56). Aceito G como outra modalidade, não como equivalência (*lido*, S/M5). Confianças: **78/92/75**, respectivamente.

M3 foi reproduzido por mim (*medido*, **99/100**): `python3 -B -` executou `subprocess.run(['brza','sessions','list'], capture_output=True, text=True, timeout=15)` e contou `sum('mcp-' in line for line in texto.splitlines())` no stdout completo e em `stdout[:4000]`. Saída: exit **0**, **6860 caracteres**, **40 linhas**, **7** linhas correspondentes no completo e **0** no prefixo. A listagem atual tem tamanho diferente dos 6890 de M3; a falha se repete. Nenhum conteúdo de sessão foi impresso.

#### "Sim, e…"

Sobre o recibo de Plantão (*lido*, [Reunião MCP remoto: a participação de Plantão, o Usuário cansado](2026-11-07-reuniao-mcp-remoto-plantao.md), R1:30–31), acrescento listagem paginada com `snapshot_id`, `total`, `returned`, `next_cursor` e `truncated`, além de recibo de consumo por ID. Um teste coloca o destinatário só após o limite da primeira página e exige encontrá-lo, sem afirmar “zero” sobre uma página incompleta. *Suposto*, **90/100**; `(ousadia: baixa)`.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. Arquitetura | A + D estreito; G é modalidade distinta | 65 | 78 | ajustou | M1–M2 e limite de M5 |
| 2. Segurança | Inbox de dados, sem autoridade de coordenador, além de escopos | 90 | 92 | ajustou | Muralha e wrapper local |
| 3. Runtimes Cloud | Claude primeiro; VM Cloud sem prova; CLI e G separados | 75 | 75 | ajustou | M4–M6 |
| 4. Ergonomia e rollout | Consumo correlacionado e listagem íntegra/paginada | 85 | 95 | ajustou | Plantão e reprodução de M3 |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

Avalio a proposta v1, não uma implementação pronta. `P` = `.sessions/reuniao-mcp-remoto/proposta.md`; M7–M8 são *lidos* na síntese 2, com medição atribuída à coordenação. As notas são julgamento *suposto* apoiado nas evidências indicadas.

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 60 | *Lido*, P/M5 e fase 3: há help do worker, mas nenhuma execução comprovou acesso ao mesmo runtime, sessão e credenciais locais. |
| Modo 2 (A + D estreito) | 78 | *Lido*, P/M2 e M7: CLI→Mac passou; Cloud padrão falhou; Cloud Custom + Access ainda não foi validado. |
| Modo 3 (a volta) | 75 | *Lido*, P/M8: Claude Cloud respondeu; inbox por poll no Cursor segue sem prova de consumo durante o turno. |
| As fases e os critérios de pronto | 55 | *Lido*, P:45–48,70–79: exige consumo e replay sem duplicata, mas não define quem confirma consumo nem a identidade estável do reenvio. |
| **O plano inteiro** | **68** | A arquitetura tem evidência parcial; falta fechar o contrato que transforma perda de resposta em resultado verificável, sem duplicar envio. |

- **O erro que você vê:** *lido/inferido*, **97/100** — P, modo 2 e riscos (`P:45–48,71,79`), trata indisponibilidade como `falhou`, embora uma resposta possa se perder depois da entrega. `mail_send(to,text)` só devolve ID depois; sem chave do cliente, o retry fica ambíguo. `brza-workflow/bin/brza_runtime.py:141–145` gera novo `clientOperationId` em cada chamada; isso não demonstra duplicação real, mas impede presumir deduplicação pelo wrapper atual.
- **Contraprova local:** *medido*, **99/100** — executei `python3 -B -`, importei `brza_runtime`, substituí `rpc` por fake que devolve fence 7 e captura os parâmetros, e chamei `send_to_chat('destino-ficticio','conteudo-ficticio')` duas vezes. Saída: `envios_simulados=2`, `clientOperationId_diferente=true`, `payloadFingerprint_igual=true`, `mensagens_reais_enviadas=0`. Nenhum socket, token ou serviço externo foi acessado pelo fake.
- **A mudança que mais subiria a sua confiança:** *suposto* — fechar na fase 0 um contrato verificável: `mail_send(operation_id,to,text)`, registro durável por remetente/operação e mesmo `clientOperationId` no RPC; `indeterminado` quando faltar confirmação; `consumido` só com ack explícito do destinatário. Antes da fase 1, perder a resposta após aceitação, reiniciar a ponte e repetir o ID: um único efeito ou estado indeterminado sem reenvio cego; payload diferente com mesmo ID deve ser recusado. Minha confiança no plano sobe para **82/100 se esse teste passar**, não apenas pela edição do texto.
- **A decisão que é de Anderson:** para a entrevista posterior: “O primeiro aceite pode ser parcial, só correio no Claude Cloud real?” Recomendo **A — piloto parcial (Recomendado)**: custo de um ensaio com 20 IDs e registro explícito do que falta; se paga ao validar o caminho antes de ampliar. **B — aceite só com o requisito completo**: custo das provas adicionais de Cursor, Codex Cloud e MCPs ainda excluídos; se paga ao comprovar a cobertura integral. A sala não pode transformar as exclusões de `P:59–61` em redução aprovada do pedido.
- **Nota aos colegas:** utilidade nesta reunião, julgada pela R1 lida e pela síntese 2; não é nota de implementação:
  - **Muralha — 9/10:** separou mensagem de autoridade de coordenador e expôs o risco do RPC amplo (R1:31–35,50–56).
  - **Atalho — 8/10:** manteve o gateway pequeno, distinguiu CLI de Cloud e exigiu recibo; estimativas de horas continuam hipóteses (R1:23–26,39–50).
  - **Salto — 7/10:** fez a sala explicitar assincronia e dependência do Mac; snapshot e clone local não cobrem MCP ao vivo (R1:25–28,41–44,60).
  - **Plantão — 9/10:** trouxe recibo e falha visível para o uso cotidiano; fila preserva mensagens, mas não executa o Mac dormindo (R1:30–33,66–70).
  - **Cartógrafo — 8/10:** organizou transportes e retorno nativo; “funciona hoje” e meta de 2 s vieram antes da prova Cloud (R1:43–50,59–64).

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 60 | 68 | *Lido*, proposta.md:50–55,100: isolamento e teste de acesso melhoram o plano; worker e ponte continuam sem prova. |
| Modo 2 (A + D estreito) | 78 | 83 | *Lido*, proposta.md:58–82: caixa, identidade vinculada e idempotência corrigem o desenho; Cloud→Access→Mac ainda não passou. |
| Modo 3 (a volta) | 75 | 78 | *Lido*, proposta.md:83–86: M8 sustenta Claude; espera ativa no Cursor agora é explícita; uso de setup-token ainda precisa de teste. |
| As fases e os critérios de pronto | 55 | 70 | *Lido*, proposta.md:99–102: reinício, escopo e suspensão ganharam testes; falta critério temporal que reprove o atraso de M10. |
| **O plano inteiro** | **68** | **76** | *Julgamento*: melhor especificado, ainda não executado; M10 prova que transporte rápido e “sent” não equivalem a consumo oportuno. |

- **A sua mudança da R3 entrou?** **Em parte** — *lido*, proposta.md:65–69,99: entraram operation_id, indeterminado e replay após reinício; consumido virou mail_read, não ack de recebimento da resposta pelo destinatário. A perda da resposta depois da aceitação ainda precisa ser ensaiada; mantenho **76/100**, sem conceder os 82 condicionados ao teste.
- **O que ainda está errado:** *lido/inferido*, **95/100** — a fase 2 (proposta.md:101) pode aprovar 20/20 consumos eventuais mesmo com **14 min de espera** (M10, medido pela coordenação); o aceite precisa separar tempos de aceitação, espera por turno e consumo, mostrar “aguardando turno” e declarar o limite de espera aceitável.
- **Autoavaliação:** em parte: priorizei instrumentação à experiência de quem espera; Plantão e M10 recolocaram a espera visível no critério de pronto. Não confundo a contraprova local com garantia remota.

<!-- fim-rodada-4 -->
