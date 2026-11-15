---
priority: high
tags:
  - chat
  - tooling
  - design
description: Os PRs #42789, #42784, #42783, #42776, #42775, #42740, #42695, #42710, #42704, #42705 e as issues #42736, #42706, #42720 trazem aprovação de planos A/B/C com feedback inline, skip robusto em perguntas, Steer resiliente, OpenCode slash e tolerância a downgrade.
---

# Aprovação de planos A/B/C, feedback de revisão inline e resiliência de composer no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#42789`](https://github.com/stablyai/orca/pull/42789),
[`stablyai/orca#42784`](https://github.com/stablyai/orca/pull/42784),
[`stablyai/orca#42783`](https://github.com/stablyai/orca/pull/42783),
[`stablyai/orca#42776`](https://github.com/stablyai/orca/pull/42776),
[`stablyai/orca#42775`](https://github.com/stablyai/orca/pull/42775),
[`stablyai/orca#42740`](https://github.com/stablyai/orca/pull/42740) (resolve Issue [`#42736`](https://github.com/stablyai/orca/issues/42736)),
[`stablyai/orca#42695`](https://github.com/stablyai/orca/pull/42695),
[`stablyai/orca#42710`](https://github.com/stablyai/orca/pull/42710),
[`stablyai/orca#42704`](https://github.com/stablyai/orca/pull/42704) (resolve Issue [`#42701`](https://github.com/stablyai/orca/issues/42701)),
[`stablyai/orca#42705`](https://github.com/stablyai/orca/pull/42705) (resolve Issue [`#42703`](https://github.com/stablyai/orca/issues/42703)),
além das issues [`stablyai/orca#42706`](https://github.com/stablyai/orca/issues/42706) e
[`stablyai/orca#42720`](https://github.com/stablyai/orca/issues/42720).

## O problema

1. **Aprovação de planos limitada a botões binários sem opção de auto-aceite ou feedback inline (`#42740`, resolve `#42736`):**
   Ao revisar planos propostos por agentes no Native Chat (`ExitPlanMode`), o usuário dispunha apenas de dois botões simples (*Approve plan* ou *Keep planning*). Para pedir alterações, era necessário rejeitar o plano primeiro e depois redigir as correções na caixa principal de mensagem, desacoplando o feedback do cartão de revisão e perdendo o contexto atômico da deliberação.
2. **Perda do rascunho de mensagem ao reconectar a visualização do chat (`#42695`):**
   Quando uma sessão de chat sofria reconexão transitória de RPC ou o usuário alternava entre abas com reciclagem de visualizador, o texto parcialmente digitado no composer era descartado.
3. **Consumo desnecessário de CPU por chats em segundo plano durante alternância de abas (`#42710`):**
   Sessões de chat abertas em abas ocultas continuavam processando atualizações contínuas de interface e hooks de streaming, gerando latência perceptível ao alternar rapidamente entre abas de trabalho.
4. **Travamento de abas de chat após erro transitório `-32603` na carga ou retomada de sessão (`#42704`, resolve `#42701`):**
   Falhas pontuais de RPC JSON-RPC com código `-32603` durante `session/load` ou `session/resume` deixavam a aba em estado quebrado irreversível (sem seletor de modelos e com envio desabilitado), forçando o usuário a fechar e recriar a aba do zero.
5. **Recusa silenciosa de confirmação de parada de chat em repouso de workspace (`#42705`, resolve `#42703`):**
   Ao colocar um workspace em modo sleep, chats que falharam na restauração via ACP recusavam confirmar o estado finalizado (`Done`), impedindo o sleep do workspace sem registrar nenhum log explicativo da recusa.
6. **Bloqueio do operador ao submeter intervenções imediatas (*Steer*) (`#42706`):**
   Ao disparar comandos de Steer, o operador precisava aguardar a confirmação de entrega antes de trocar de conversa, sob risco de interrupção ou perda do envio.
7. **Ausência de atalho rápido para reabrir abas de chat fechadas acidentalmente (`#42720`):**
   Enquanto navegadores e editores oferecem reabertura de abas recentes via teclado, o Native Chat não respondia a <kbd>⌘Shift+T</kbd> / <kbd>Ctrl+Shift+T</kbd>.
8. **Respostas vazias ou nulas ao pular etapas em cartões de pergunta (`#42789`):**
   Ao clicar no botão "Skip" em cartões de `ask_question` ou questionários com múltiplos passos, o cliente enviava um payload vazio ou nulo que desorientava o agente, em vez de sinalizar explicitamente a opção de pulo.
9. **Rótulo desatualizado do modelo Claude no cabeçalho após chaveamento (`#42784`):**
   Quando a conversa rolava para baixo e o cabeçalho fixo exibia o modelo, mudanças de modelo no meio do turno não eram refletidas, mostrando o nome do modelo inicial em vez do modelo da resposta mais recente.
10. **Incompatibilidade de esquema de transcripts após downgrade de versão (`#42783`):**
    Sessões gravadas por versões mais novas do app sofriam erro de parse ou corrupção silenciosa ao rodar em versões anteriores caso o usuário realizasse downgrade.
11. **Conflito de corrida entre intenções de Steer e digitação ativa (`#42776`):**
    Quando comandos de Steer eram despachados enquanto o usuário digitava no composer ou ferramentas estavam executando inserções ativas, mensagens colidiam fora de ordem.
12. **Falta de suporte a comandos slash e restauração de modo para OpenCode (`#42775`):**
    Chats do OpenCode não tinham suporte a comandos de barra (`/`) e perdiam a preferência de modo (TUI vs Native Chat) na restauração de sessões.

## O que o upstream implementa

- **Tratamento robusto de pulo em perguntas interativas (`#42789`):**
  - Garante envio de sinal padronizado `skip` estruturado no protocolo quando o operador opta por pular um cartão de perguntas.
- **Identificação dinâmica do modelo Claude a partir da última resposta (`#42784`):**
  - Atualiza o indicador visual da barra superior com o modelo inferido a partir da mensagem mais recente da conversa.
- **Compatibilidade retroativa de transcripts contra downgrade (`#42783`):**
  - Tolera campos desconhecidos e preserva estrutura de arquivos JSONL gravados por releases superiores.
- **Enfileiramento estrito de intenções de Steer atrás de inserções ativas (`#42776`):**
  - Ordena a fila de Steer garantindo que intervenções imediatas aguardem a finalização de blocos em escrita sem perda de contexto.
- **Comandos slash e retenção de modo para OpenCode (`#42775`):**
  - Registra comandos slash do runtime OpenCode e restaura fidedignamente o modo da sessão (chat ou terminal).
- **Aprovações estruturadas de planos A/B/C com feedback inline (`#42740`, resolve `#42736`):**
  - O cartão de aprovação de plano ganha três opções explícitas com atalhos numéricos (`1`, `2`, `3`) e letras (`A`, `B`, `C`):
    - `A`: Aprovar e aceitar edições automaticamente (*Approve and auto-accept edits* — `allowAcceptEdits`);
    - `B`: Aprovar e solicitar confirmação a cada edição (*Approve and ask before edits* — `allow`);
    - `C`: Continuar planejando (*Keep planning* — `deny`);
  - Campo de texto multilinha "Other" embutido diretamente no cartão, permitindo redigir instruções de revisão e submetê-las via <kbd>⌘Enter</kbd> / <kbd>Ctrl+Enter</kbd> sem fechar a deliberação;
  - Recibo de resolução consolidado exibindo a escolha selecionada acompanhada do feedback (`<opção> · <feedback>`);
  - Proteção de compatibilidade retroativa via capability `agent-session.approval-feedback.v1`.
- **Preservação de rascunhos no chat composer em reconexões (`#42695`):**
  - Armazena o rascunho de texto e anexos selecionados na store de sessão persistente, restaurando-os automaticamente caso a view do chat seja recarregada ou reconectada.
- **Pausa automática de chats ocultos (`#42710`):**
  - Suspende subscrições visuais ativas e renderizações redundantes quando a aba do chat fica fora de foco, reativando-as instantaneamente ao focar a aba.
- **Retentativa automática com backoff para erros `-32603` (`#42704`, resolve `#42701`):**
  - Implementa retry automático com retardo exponencial ao detectar falhas transitórias de RPC na inicialização e restauração de sessões, garantindo hidratação correta de modelos.
- **Telemetria de recusa de parada em ciclos de repouso (`#42705`, resolve `#42703`):**
  - Registra a causa detalhada nos logs quando um chat em repouso falha ao validar o status de parada pós-restauração.
- **Enfileiramento resiliente de Steer (`#42706`):**
  - Enfileira comandos de inserção imediata em background, liberando o usuário para alternar livremente entre conversas.
- **Atalho universal de reabertura de abas de chat (`#42720`):**
  - Habilita <kbd>⌘Shift+T</kbd> / <kbd>Ctrl+Shift+T</kbd> para restaurar a última aba de chat nativo fechada na sessão.

## O que fazer

- Padronizar respostas de skip em cartões de perguntas interativas (`#42789`).
- Exibir dinamicamente o modelo Claude da resposta mais recente no cabeçalho fixo (`#42784`).
- Garantir resiliência de transcripts JSONL contra downgrade de versão (`#42783`).
- Ordenar intenções de Steer atrás de inserções ativas em curso (`#42776`).
- Adicionar comandos slash e restauração confiável de modo para OpenCode (`#42775`).
- Incorporar os cartões de aprovação de plano A/B/C e a caixa de feedback inline de revisão (`#42740`, resolve `#42736`).
- Adotar a retenção de rascunho no composer durante reconexões (`#42695`) e pausa de chats em background (`#42710`).
- Aplicar o retry automático com backoff em erros de inicialização `-32603` (`#42704`, resolve `#42701`).
- Integrar a reabertura de abas de chat com <kbd>⌘Shift+T</kbd> (`#42720`) e o enfileiramento sem bloqueio de Steer (`#42706`).
