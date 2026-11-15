---
priority: high
tags:
  - chat
  - design
  - tooling
description: Os PRs #42515, #42520, #42524, #42496, #42529, #42546 e #42550 trazem novo design de cartões de resposta com barra de etapas, fila de mensagens acoplada, steer não-bloqueante no Claude e isolamento de streaming.
---

# Redesenho de cartões de resposta, progresso por etapas e fila de mensagens

Rastreado dos PRs abertos no upstream [`stablyai/orca#42515`](https://github.com/stablyai/orca/pull/42515),
[`stablyai/orca#42520`](https://github.com/stablyai/orca/pull/42520),
[`stablyai/orca#42524`](https://github.com/stablyai/orca/pull/42524),
[`stablyai/orca#42496`](https://github.com/stablyai/orca/pull/42496),
[`stablyai/orca#42529`](https://github.com/stablyai/orca/pull/42529),
[`stablyai/orca#42546`](https://github.com/stablyai/orca/pull/42546) e
[`stablyai/orca#42550`](https://github.com/stablyai/orca/pull/42550).

## O que está quebrado ou faltando

1. **Aparência de placeholder e usabilidade truncada em cartões de resposta interativos (`#42515`):**
   Os cartões de perguntas (`ask_question` / ACP question) pareciam rascunhos inacabados com caixas de contorno cinza; opções com foco de teclado pareciam selecionadas antes de qualquer clique; etapas flutuavam longe da pergunta; e em painéis curtos o cartão cobria o histórico ou cortava as opções sem permitir rolagem interna confortável.
2. **Interface de mensagens enfileiradas fragmentada e sem controles rápidos (`#42515`):**
   A fila de mensagens não possuía integração visual limpa com a caixa de texto do composer; mensagens com falha não ofereciam botão de repetição (*retry*); e filas pausadas não exibiam alertas claros nem opções rápidas de limpeza (*Clear all*) e retomada (*Resume*).
3. **Bloqueio de Steer no Claude durante subagentes ou comandos em primeiro plano (`#42520`):**
   Ao pressionar **Steer** em uma mensagem enfileirada enquanto o Claude executava um subagente em foreground ou um comando longo, a mensagem ficava travada em "Sending…" por minutos até o término daquela ferramenta, porque o Claude só consome entrada entre chamadas de ferramentas e subagentes são tratados como chamadas bloqueantes contínuas.
4. **Falta de visibilidade do motivo de falha na inicialização de chats do Claude (`#42524`):**
   Quando um chat falhava na inicialização com a mensagem *"Claude couldn't start. Send your message to try again."*, a UI não exibia o botão "Details", impedindo desenvolvedores e usuários de descobrirem qual requisição de controle do SDK falhou.
5. **Falha ao colapsar turnos concluídos sem registro em cache (`#42496`):**
   Turnos concluídos cujos dados históricos não estavam previamente carregados em memória falhavam ao recolher, mantendo blocos abertos indevidamente.
6. **Degradação de performance na alternância de abas com streaming em background (`#42529`, `#42546`, `#42550`):**
   Transmissões contínuas de respostas em chats em segundo plano forçavam re-renderizações e desperdício de ciclos da thread principal ao acordar painéis ocultos e atualizar desnecessariamente assinaturas da barra lateral.

## O que o upstream implementa

- **Redesenho integral do cartão de respostas (*Answer Card*) (`#42515`):**
  - **Ladrilhos preenchidos (*filled tiles*):** As alternativas tornam-se blocos sólidos; ao selecionar, o número vira um ícone de verificação (*check*) com anel interno, enquanto o foco de teclado fica na borda externa, eliminando a confusão visual entre foco e seleção;
  - **Destaque "(Recommended)":** O sufixo "(Recommended)" é convertido automaticamente em uma *pill* visual limpa;
  - **Barra de progresso segmentada:** Substitui abas flutuantes por uma barra sob o cabeçalho, permitindo clicar em qualquer segmento para saltar para a etapa desejada com indicação de etapas já respondidas;
  - **Navegação aprimorada:** Adiciona botões Back (a partir da etapa 2), Skip, Next ↵ e Submit ↵ (ou "Skip and submit" na última etapa pendente);
  - **Campo de digitação e animação de altura:** Linha preenchida com expansão para duas linhas no foco; o cartão ajusta suavemente sua altura entre etapas com suporte a `reduced motion`;
  - **Prevenção de submissão duplicada:** Manter pressionado <kbd>Enter</kbd> nunca avança nem responde etapas seguintes inadvertidamente;
  - **Acomodação responsiva em painéis curtos:** Dobra a fila de mensagens primeiro, limita a caixa de input a 3 linhas quando há pergunta aberta, encolhe a transcrição e, se necessário, habilita scroll suave no corpo do cartão mantendo cabeçalho e rodapé sempre visíveis.
- **Fila de mensagens acoplada e resiliente (`#42515`):**
  - Fila como aba embutida atrás do cartão de resposta ou da caixa de mensagem;
  - Botão de texto direto Send/Steer, botão Delete visível ao passar o cursor ou focar, e menu de 3 pontos (`⋯`) com opções *Edit message*, *Show full message* e *Delete*;
  - Mensagens com falha exibem "Couldn't send" e botão *Retry*;
  - Fila pausada exibe banner de aviso, *Clear all* e *Resume*.
- **Steer não-bloqueante no Claude via transferência para background (`#42520`):**
  - Ao disparar Steer em um turno do Claude em execução, move imediatamente subagentes e comandos de primeiro plano para segundo plano (com limite de espera de 5s);
  - Envia a mensagem com prioridade `now`, instruindo o Claude a encerrar a etapa atual e responder ao steer no turno imediato;
  - Atualiza o hint de Steer para *"Send now, while the agent keeps working"*.
- **Diagnóstico sob "Details" em erros de inicialização do Claude (`#42524`):**
  - Anexa o texto do erro retornado pelo runtime como log de diagnóstico, habilitando o botão "Details" no aviso visual.
- **Dobra resiliente de turnos finalizados (`#42496`):**
  - Permite colapsar turnos concluídos mesmo quando o registro individual ainda não tiver sido totalmente carregado.
- **Otimização de latência e consumo de CPU durante streaming (`#42529`, `#42546`, `#42550`):**
  - Reutiliza identidades estáveis de painéis durante transmissões de texto;
  - Isola assinaturas de painéis ocultos e linhas da sidebar para não disparar renderizações de detalhes quando estão fora de foco;
  - Agrupa publicações de status de respostas em background em lotes temporizados.

## O que fazer

- Incorporar o novo design do *Answer Card* e barra segmentada de etapas (`#42515`).
- Adotar a fila de mensagens acoplada com menu de 3 pontos e ações de *Retry* e *Clear* (`#42515`).
- Aplicar a estratégia de envio de tarefas ativas para background e prioridade `now` em intervenções de Steer no Claude (`#42520`).
- Exibir detalhes e logs de diagnóstico em falhas de inicialização do Claude (`#42524`).
- Permitir colapso limpo de turnos concluídos não cacheados (`#42496`).
- Adotar o isolamento de assinaturas e loteamento de status para eliminar lentidão na troca de abas durante streaming (`#42529`, `#42546`, `#42550`).
