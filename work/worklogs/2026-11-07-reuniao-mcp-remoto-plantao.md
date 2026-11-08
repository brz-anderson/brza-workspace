---
scope:
  - brza-workflow
  - brza-studio
tags:
  - tooling
---

# Reunião MCP remoto: a participação de Plantão, o Usuário cansado

O pedido de Anderson, em 2026-11-07, na sessão da coordenação (`reuniao-mcp-remoto`): "Encontrar maneiras de usar o
MCP remotamente: em outras máquinas e em sessões Cloud de diferentes runtimes (…) as sessões remotas devem conseguir se
comunicar normalmente com as sessões rodando localmente no Mac". Este é o registro de **Plantão** — persona o Usuário cansado, no
Claude Haiku 5.5 low —, aberto pela coordenação com `brza agent launch`. A pauta e as regras estão no briefing da reunião; cada rodada é
uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Arquitetura

- **Posição:** C (fila com recibo, o Mac só sai) como espinha, com D (um `brza` que fala MCP) na frente; A não serve para o celular.
- **Por quê:**
  - *Lido* (`.sessions/reuniao-mcp-remoto/material/levantamento.md`, linha 8): o correio só fala com o socket unix da mesma máquina; a Cloud não alcança isso.
  - *Lido* (levantamento, linha 22): `claude -p --cloud <session-id>` já leva mensagem do Mac para a Cloud. Falta o sentido contrário, da Cloud para o Mac.
  - *Lido* (levantamento, linha 4): o `brza-quota` já é HTTP em `127.0.0.1` com Bearer; falta alcançá-lo de fora.
  - *Suposto*: a pessoa abre a sessão no celular, a sessão chama uma ferramenta do `brza`, a mensagem cai na fila e o worker do Mac a pega sem nenhum passo no Mac.
- **Ideias:**
  - Recibo em dois estados, "na fila" e "entregue ao chat", devolvido pela própria ferramenta de envio (`(ousadia: baixa)`).
  - `brza sessions send --remote` que grava na fila, devolve um id, e `brza sessions status <id>` que mostra o estado (`(ousadia: média)`).
  - A fila como commits numa branch dedicada do git: sem servidor, mas com latência alta e o histórico cheio de ruído (`(ousadia: alta)`).
- **Risco:** o Mac dormindo deixa tudo parado; sem recibo visível, a fila repete o silêncio de hoje.
- **Confiança:** 55/100

#### 2. Segurança

- **Posição:** o Mac só faz conexão de saída, e nada escuta fora de `127.0.0.1`; o token da fila tem escopo de enviar e ler a própria fila.
- **Por quê:**
  - *Lido* (`CLAUDE.md`, seção do servidor MCP): o token vai por `headersHelper`, lido do disco a cada conexão, e não fica gravado no arquivo.
  - *Lido* (levantamento, linha 20): variáveis de ambiente ficam legíveis por quem usa o ambiente da Cloud; "network secrets" ficam fora da VM. Um token na variável vaza para quem lê o ambiente.
  - *Lido* (levantamento, linha 8): o `orca-runtime.json` guarda o `authToken` do correio local. Não o imprimi.
- **Três piores falhas:**
  1. Token de fila em variável de ambiente da Cloud, legível por quem tem acesso ao ambiente.
  2. Túnel com autenticação mal configurada expõe o `brza-quota` (Bearer só) para a internet.
  3. A fila guarda o texto da conversa em claro, e o operador do relay lê tudo.
- **O que a tela deveria dizer:** "token de fila vence em 7 dias, renovar" e "mensagem cifrada; o relay não lê o texto".
- **Ideias:**
  - Token de escopo mínimo, rotacionável, guardado como network secret e não como variável (`(ousadia: média)`).
  - Cifra ponta a ponta, com a chave só no Mac e na sessão (`(ousadia: alta)`).
- **Risco:** a conveniência de mandar mensagem do celular vira um canal de comando para o Mac; quem pegar o token comanda sessões.
- **Confiança:** 60/100

#### 3. Runtimes Cloud

- **Posição:** a C funciona hoje só no Cursor Cloud, com MCP por HTTP e segredos por time; no Claude Code Cloud e no Codex Cloud, ainda não.
- **Por quê:**
  - *Lido* (levantamento, linha 25): o Cursor aceita MCP HTTP com OAuth e segredos por time injetados no start; a rede tem restrição de domínio, e a doc cita Tailscale.
  - *Lido* (levantamento, linha 27): o Codex Cloud deixa a internet desligada por padrão, e segredos saem antes do agente rodar.
  - *Lido* (levantamento, linha 23, confiança 40): não confirmei se o `.mcp.json` do repositório carrega em sessão Cloud do Claude Code.
  - *Suposto*: o relay precisa estar na allowlist de domínio de cada runtime.
- **Confiança:** 50/100

#### 4. Ergonomia e rollout

- **Posição:** o primeiro passo é um recibo de entrega, antes de qualquer túnel; sem ele, nenhuma das alternativas é usável no celular.
- **Por quê:** o caso do dia a dia é "abri a sessão, mandei X, nada aconteceu". O recibo responde essa pergunta, e o resto é detalhe.
- **Primeiro passo barato:** uma fila de poucas centenas de linhas, num host pequeno, com o worker do Mac puxando por polling; a primeira entrega é só o recibo "entregue ao chat".
- **Métrica de sucesso:** no mínimo 95% das mensagens com recibo "entregue ao chat" em até 60 s, e zero comandos digitados no Mac por mensagem.
- **Falha silenciosa a evitar:** worker parado sem aviso. Ideia: se uma mensagem passa de 2 min sem entrega, o `PushNotification` (deferida, disponível nesta sessão) avisa no celular. (`(ousadia: média)`)
- **Confiança:** 55/100

#### A ideia mais ousada desta rodada

A sessão remota mostra o estado da própria mensagem em tempo real, e o Mac avisa no celular quando a fila para. O risco é ruído: notificação demais e a pessoa desliga tudo, ou alarme falso quando o Mac só está dormindo.

#### Issues candidatas

- **Recibo de entrega visível para a sessão remota** — sem ele, a pessoa não sabe se a mensagem chegou — prioridade `high`
- **Token de escopo mínimo para a fila, fora de variável de ambiente** — o risco de segurança maior desta rodada — prioridade `high`
- **Prova de conceito da fila com o Mac só em conexão de saída** — valida a C antes de qualquer túnel — prioridade `medium`
- **Alerta no celular quando a fila para** — evita a falha silenciosa — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Arquitetura | C (fila com recibo, Mac só sai), com D na frente; A descartado para o celular | 55 |
| 2. Segurança | Mac só em saída, token de escopo mínimo fora de variável de ambiente | 60 |
| 3. Runtimes Cloud | Cursor Cloud hoje; Claude Code e Codex, não confirmados | 50 |
| 4. Ergonomia e rollout | Recibo de entrega primeiro, depois a fila | 55 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

- **D1:** b — C+D: relay só de saída, com recibo em cinco estados (aceito, na fila, entregue, consumido, falhou). Sem fila, o Mac dormindo vira erro na Cloud e a mensagem se perde; o M1 mediu o túnel só com o Mac acordado. — 65/100
- **D2:** e: a + b — `claude -p --cloud <id>` como entrada, com caixa de entrada como reserva. Só (a) não tem recibo medido; só (b) depende de o modelo lembrar de consultar a caixa. — 55/100
- **D3:** e: b, com aviso de chegada visível no chat de destino ("chegou de X, não confiável: ler / ignorar"). A (a), "só lê quando pede", é a mensagem que some para quem mandou. — 70/100
- **D4:** d agora; se um dia houver túnel, (a) nomeado. O quick tunnel do M1 troca de URL a cada reinício, e a configuração da Cloud aponta para a URL antiga sem avisar. — 75/100
- **D5:** a — o correio Cloud → Mac com recibo, medido ponta a ponta. É o único passo que responde "chegou?" antes de qualquer outro. — 70/100

#### Os ataques

- **Régua (arquitetura, A+D):** o `queued` que Régua pede não existe em A. Com túnel, o Mac dormindo vira erro na Cloud, sem fila, e a mensagem não tem para onde voltar. Cai se Régua mostrar retentativa com o mesmo ID dentro do turno da Cloud, o que a doc não garante.
- **Cartógrafo (runtimes, "Sim" no Claude Code Cloud):** o "Sim" é suposto. O M4 diz que a sessão Cloud não foi sondada, e a própria tabela de Cartógrafo marca o risco de allowlist do Trusted. Confiança de 85 não cabe aí. Cai com uma sessão Cloud medida alcançando a URL do túnel.

#### A concessão

- **M3 e M2 (síntese):** M3 mostrou o Codex respondendo "0 sessões mcp-" com 7 presentes, por corte silencioso de 4000 caracteres. É o pior caso que eu descrevi, e me fez exigir contagem conferível e corte declarado no recibo. M2 mostrou a chamada barrada por aprovação, sem erro visível para quem pediu. Subi a confiança em ergonomia por isso.
- **Régua, E2:** `X-Brza-Session` aceito com Bearer válido. Eu tinha escrito "token curto por sessão"; um token sem vínculo no servidor não prova a sessão. Ajustei a segurança.

#### "Sim, e…"

Régua (os estados `accepted`/`queued`/`delivered`/`failed`) + Muralha (mensagem é dado, em quarentena): o destino recebe um cartão de chegada no chat, com um toque para ler ou ignorar. Quem mandou vê o estado no celular, e nada roda sozinho. `(ousadia: média)`

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :----- | :--------------------- |
| 1. Arquitetura | b: C+D com recibo; A só com URL nomeada | 55 | 65 | ajustou | M1 e M2; Régua (fila) |
| 2. Segurança | Token por sessão vinculado à rota no servidor, não ao cabeçalho | 60 | 55 | ajustou | Régua (E2: `X-Brza-Session` aceito) |
| 3. Runtimes Cloud | Cursor e Claude como candidatos; sem selo até sessão Cloud medida | 50 | 40 | ajustou | M4; Cartógrafo (ataque) |
| 4. Ergonomia e rollout | Recibo com contagem e corte declarados, e aviso de chegada | 55 | 70 | ajustou | M3 e M2 |

<!-- fim-rodada-2 -->

### Rodada 3: a confiança no plano

| Parte do plano | Confiança (0–100) | Uma linha de porquê |
| :------------- | :---------------- | :------------------ |
| Modo 1 (G, a Cloud no Mac) | 45 | Zero passo para quem manda, mas só com o Mac acordado e o worker de pé; o worker morto calado é a falha que eu mais temo, e o plano não diz o que o celular mostra nesse caso. |
| Modo 2 (A + D estreito) | 60 | Recibo, `total`/corte e erro explícito estão no plano; M7 e M9 dão o caminho da rede Custom. Falta medir o Mac dormindo. |
| Modo 3 (a volta) | 60 | M8 mediu 2,6 s no Claude; nos outros, o `mail_inbox` por poll depende de o modelo lembrar de consultar, o que é silencioso. |
| As fases e os critérios de pronto | 55 | A fase 1 tem os critérios certos (20/20, zero duplicata, erro com o Mac dormindo); a fase 0 "testes locais" não diz nada do que o usuário vê. |
| **O plano inteiro** | 50 | Modo 2 sólido, mas os modos 1 e 3 para os runtimes que não são Claude são suposição. |

- **O erro que você vê:** "Mac dormindo ou túnel caído: a Cloud recebe erro, não silêncio; o recibo diz `falhou`. Se a perda aparecer na medição, entra a fila (C)" (proposta, §Riscos). Com erro, a pessoa reenvia à mão, o que quebra o "zero passo manual" do requisito. E a perda não é medida antes: a fase 1 só pede o erro explícito, não quantas mensagens somem com o Mac suspenso. Fonte de ideia: §Riscos e fase 1 da proposta.
- **A mudança que mais subiria a sua confiança:** na fase 1, suspender o Mac por 10 min com 20 mensagens na fila de envio, e contar quantas chegam sem reenvio e quantas viram duplicata. Se der zero perda e zero duplicata, o Modo 2 sobe de 60 para cerca de 75; se der perda, o C entra antes da fase 2, e o plano diz isso com o número.
- **A decisão que é de Anderson:** aceita que, com o Mac dormindo, a mensagem falhe e ele reenvie à mão até a medição, ou quer a fila já na fase 1? **Recomendação:** aceitar o reenvio na fase 1, com a medição de perda como critério de pronto; a fila entra só se a medição mandar. O plano hoje deixa essa escolha para depois, sem dizer que ela é dele.
- **Nota aos colegas (utilidade de 0 a 10):**
  - Muralha: 9. O modelo de ameaça e a quarentena são o que o plano usou de melhor.
  - Régua: 9. O E2 e o critério de recibo por consumo são as partes que mais mexeram no plano.
  - Atalho: 5. O gateway mínimo repete o Modo 2 sem trazer dado novo.
  - Salto: 4. O git como barramento sobrou só como ideia para o Codex Cloud sem rede.
  - Cartógrafo: 4. A matriz ajudou, mas o "Sim" para o Claude Code Cloud sem medição foi o que a rodada 2 derrubou.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

| Parte do plano | Confiança na v1 (R3) | Confiança na v2 | Uma linha de porquê |
| :------------- | :------------------- | :-------------- | :------------------ |
| Modo 1 (G) | 45 | 50 | O usuário macOS separado e o "o que o celular mostra com o worker morto" entraram; o Mac dormindo continua derrubando tudo, e isso segue a medir. |
| Modo 2 (A + D estreito) | 60 | 55 | Caixa, recibo e `operation_id` entraram, mas o aviso fixo ainda chega como turno (M10) e o Claude depende de ambiente dedicado com o MCP do repositório ainda não confirmado. |
| Modo 3 (a volta) | 60 | 55 | O verbo único `send remote:<id>` ajuda, mas o login do claude.ai vence entre 11-09 e 11-12 e o `setup-token` não foi testado; o Cursor "não acorda o agente". |
| As fases e os critérios de pronto | 55 | 70 | A perda com o Mac suspenso (20 mensagens, 10 min) entrou na fase 2, como eu pedi, e o worker morto entrou na fase 1. |
| **O plano inteiro** | 50 | 55 | Melhorou nos critérios; os modos 1 e 3 seguem com a parte que o celular mostra sem medição. |

- **A sua mudança da R3 entrou?** Em parte. A medição do Mac dormindo entrou na fase 2 com os números que eu pedi (20 mensagens, 10 min, perda e duplicata). A decisão de aceitar o reenvio à mão não entrou como pergunta para Anderson: a proposta só diz "se houver perda, a fila entra". A forma que entrou mede; não decide.
- **O que ainda está errado:** o teste negativo da fase 0 ("nenhum byte do remetente chega ao chat como turno") passa com o aviso fixo, que o M10 mostra chegando como turno; a proposta não diz se o aviso conta como byte do remetente.
- **Autoavaliação:** apareceu, sim: na R1 eu puxei pelo "zero passo manual" e só vi o custo de segurança do Modo 1 quando o revisor o pôs na mesa.

<!-- fim-rodada-4 -->

### Rodada 5: o foco no MCP do `brza-workflow`

- **Como expor o `brza-orchestrator` a outra máquina e à Cloud:** túnel nomeado só se a sessão Cloud for o requisito; antes disso, o G (o worker no Mac) resolve o celular sem expor nada. O `brza-orchestrator` não é como o correio: ele é HTTP com Bearer desde o início (`packages/mcp/brza_mcp/server.py:1-20`), então o que muda é quem recebe o Bearer, e não o transporte. Para a sessão Cloud, a ponte é um proxy próprio que valida o token por cliente antes de repassar, e não o servidor exposto direto. [lido]
- **O que a sessão remota pode chamar:** `status` é a única ferramenta que eu liberaria, com o token de leitura. `dispatch` (`tools.py:230`) entra na fila e pode abrir worker com gasto de conta, então só com gate humano na conta do Mac (o `approved` do gate, que a sessão principal pede a Anderson). `config` (`tools.py:546`) grava a política do `brza.toml`; não sai do Mac. O `X-Brza-Session` não pode vir do cliente remoto: o chamador tem de ser derivado do token, no servidor, porque `tools.py:234-236` aceita o cabeçalho ou o argumento `caller`, e o E2 mostrou que ele é aceito forjado com Bearer válido. [lido]
- **Como a sessão remota "conversa" com as do Mac:** pelo `dispatch`, o pedido vira um registro na fila (`queue.enqueue`, `state='gated'` ou enfileirado, `tools.py:275`), e o worker do Mac o pega. Como a resposta volta ao chamador remoto não está lido: o caminho provável é o `status` por polling, o que é suposto. Não rodei nada para confirmar. [suposto]
- **O risco mais grave:** um Bearer só, com o `caller` vindo do cabeçalho, deixa quem tem o token se passar por qualquer sessão do Mac, e aprovar gate em nome dela (`dispatch` com `approved`, `tools.py:237-238`). Mitigação: um token por cliente, `caller` fixado no servidor pelo token, `approved` recusado para o token remoto, e teste negativo com `X-Brza-Session` forjado, como a fase 0 da proposta já pede. Derruba-se se o código mostrar que `approve` não confere o chamador.
- **Confiança:** 50/100 na minha posição. Sobe para cerca de 70 se o levantamento confirmar que o `approve` confere o chamador e que o `status` traz a resposta de um `dispatch`.

<!-- fim-rodada-5 -->

### Rodada 6: a confiança na v3

| Parte | Confiança (0–100) | Uma linha de porquê |
| :---- | :---------------- | :------------------ |
| O proxy remoto (fase 0) | 60 | Os testes negativos cobrem o que me assustou (cabeçalho de fora ignorado, `approved` recusado, `config` fora); falta o caso do gate parado, que o celular precisa ver. |
| O G (fase 1) | 45 | Zero passo no uso, mas o Mac dormindo derruba tudo, e o usuário macOS separado é trabalho de setup que ninguém mediu. |
| A Cloud pelo túnel (fase 2) | 50 | M7 mostra que a rede padrão recusa o host, e o MCP do repositório na Cloud ainda é bloqueio; o caminho só se testa com a rede liberada. |
| A volta e a sessão-caixa (fase 3) | 45 | M8 mostra a volta no Claude, mas a sessão-caixa só responde se estiver aberta no Mac; se Anderson fechá-la, o pedido fica parado e calado. |
| **O plano inteiro** | 45 | A ordem está certa, mas o que o usuário vê quando o Mac, o gate ou a caixa param ainda não tem critério de pronto. |

- **O que ainda está errado:** a fase 0 não testa o caso em que a sessão-caixa está fechada nem o gate remoto parado; o pedido fica no Mac sem aviso para quem está no celular, e a fase 3 só mede o caminho feliz.

<!-- fim-rodada-6 -->
