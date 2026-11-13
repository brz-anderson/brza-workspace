---
status: open
description: Os PRs #42133, #42127, #42104, #42061, #41949 e #42045 trazem badge do Dock com chats não lidos e atenção, serialização incremental de sessões e alívio de GC.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-13
tags:
  - tooling
  - infra
---

# Contagem de atenção no Dock, serialização incremental e alívio de GC

Rastreado dos PRs abertos no upstream [`stablyai/orca#42133`](https://github.com/stablyai/orca/pull/42133),
[`stablyai/orca#42127`](https://github.com/stablyai/orca/pull/42127),
[`stablyai/orca#42104`](https://github.com/stablyai/orca/pull/42104),
[`stablyai/orca#42061`](https://github.com/stablyai/orca/pull/42061) (resolve Issue [`#42060`](https://github.com/stablyai/orca/issues/42060)),
[`stablyai/orca#41949`](https://github.com/stablyai/orca/pull/41949),
[`stablyai/orca#42045`](https://github.com/stablyai/orca/pull/42045),
[`stablyai/orca#42024`](https://github.com/stablyai/orca/pull/42024),
[`stablyai/orca#42132`](https://github.com/stablyai/orca/pull/42132) (resolve Issue [`#42096`](https://github.com/stablyai/orca/issues/42096)),
além das issues [`stablyai/orca#41918`](https://github.com/stablyai/orca/issues/41918) e
[`stablyai/orca#42069`](https://github.com/stablyai/orca/issues/42069).

## O problema

1. **Badge do Dock contando workspaces em vez de chats concluídos não lidos (`#42061`, resolve `#42060`):**
   No macOS, o número exibido no ícone do aplicativo no Dock contava o total de workspaces com itens pendentes, e não os chats reais
   aguardando leitura. Se múltiplos agentes terminavam suas tarefas dentro de um mesmo workspace, o badge exibia `1` em vez da contagem
   real de conversas não lidas, ocultando o volume de trabalho entregue até a abertura do aplicativo.
2. **Ausência de sinalização no Dock quando agentes estão bloqueados aguardando input (`#41949`):**
   Quando um agente interrompia a execução aguardando permissão de ferramenta sensível ou resposta a uma pergunta interativa, o Dock
   não exibia nenhuma indicação. Operadores trabalhando em outros aplicativos só descobriam que o agente estava ocioso e bloqueado
   ao alternar manualmente a janela de volta para o BrzA Studio.
3. **Congelamentos periódicos de interface por coleta de lixo forçada a cada 30 segundos (`#42133`):**
   Sob uso elevado de memória, o módulo de telemetria e diagnóstico ativava um gravador de alocações. A cada 30 segundos, a leitura desse
   registro forçava uma coleta síncrona completa de memória (`window.gc()`) no processo do Chromium, congelando a janela por 500 ms a 1 s
   de forma cíclica.
4. **Sobrecarga de serialização JSON de perfil completo ao salvar abas (`#42127`):**
   Em sessões com dezenas de abas e perfis extensos, qualquer alteração pontual em uma única aba levava a thread principal do Electron a
   serializar todo o estado da sessão em um bloco maciço de JSON antes de repassá-lo ao gravador em segundo plano, gerando picos de
   consumo de CPU e quedas de taxa de quadros na digitação.
5. **Reconstrução e republicação do grafo completo de sessões a cada batimento de status (`#42104`):**
   Com centenas de workspaces abertos, cada alteração de status de agente (running, done, idle) fazia a janela reconstruir todo o grafo
   de sessões (~196 KB) e transmiti-lo via IPC para o processo principal, sobrecarregando os canais de mensagens e a sincronização com
   clientes pareados.
6. **Atraso na inicialização do gravador de diário de chat e contenção em inicializações (`#42045`):**
   O gravador de diário de chat demorava a subir e executava tarefas de manutenção e limpeza concorrentemente com o arranque dos serviços
   de chat, gerando contenção de disco no exato momento em que o operador tentava enviar suas primeiras instruções.
7. **Erros ENOENT contínuos em segundo plano por rotinas do Codex quando o binário não está presente (`#42132`, resolve `#42096`):**
   Tarefas agendadas de manutenção do Codex continuavam tentando varrer diretórios e índices mesmo em ambientes onde o Codex havia sido
   removido ou nunca instalado, inundando os logs do sistema com mensagens de erro desnecessárias.
8. **Inexistência de método para focar uma aba de chat específica via CLI ou plugins (`#42069`):**
   Utilitários de linha de comando e plugins não dispunham de um comando ou chamada RPC para ativar e trazer para o primeiro plano uma
   aba de chat estruturada (`agent-session`) pelo seu identificador, dificultando integrações com lançadores externos e scripts de automação.

## O que o upstream implementa

- **Contagem de chats não lidos no badge do Dock (`#42061`, resolve `#42060`):**
  - Altera a métrica do Dock no macOS para computar o número de chats não lidos (as mesmas linhas destacadas na página de Atividades);
  - Cada chat aberto decrementa o contador imediatamente, refletindo com fidelidade as conversas finalizadas pendentes de revisão.
- **Marcação visual de atenção no Dock com ponto de exclamação (`#41949`):**
  - Adiciona o indicador `!` ao ícone do Dock enquanto houver pelo menos um agente aguardando input, resposta interativa ou autorização de ferramenta;
  - Desaparece assim que a pendência for respondida ou o chat for focado.
- **Interrupção de GC forçado em alto uso de memória (`#42133`):**
  - Desativa a chamada repetitiva a `window.gc()` durante a leitura do gravador de diagnósticos em condições de memória elevada;
  - Elimina as pausas periódicas de 500 ms a 1 s no Chromium sem prejudicar a captura de dados essenciais para relatórios pós-falha.
- **Serialização incremental ao salvar abas (`#42127`):**
  - Converte em JSON apenas a entrada da aba que sofreu modificações e repassa essa fatia ao gravador assíncrono em background;
  - Elimina a serialização redundante de todo o perfil da janela na thread principal.
- **Emissão pontual de alterações de status sem republicar o grafo completo (`#42104`):**
  - Interrompe a re-derivação global do grafo a cada ping de status de agentes, transmitindo apenas as atualizações chaveadas por agente (`keyed status`);
  - Poupa centenas de KB por segundo sob rajadas de atividade multiagente.
- **Inicialização antecipada do chat journal writer com manutenção adiada (`#42045`, `#42024`):**
  - Sobe o escritor do diário de chat nos primeiros instantes do processo e adia limpezas e expurgos de diários legados convertidos até que o serviço esteja completamente pronto para responder.
- **Verificação de presença do binário para rotinas de manutenção do Codex (`#42132`, resolve `#42096`):**
  - Pula silenciosamente as rotinas periódicas de manutenção quando a CLI do Codex não estiver presente e trata pastas de datas vazias como ausência esperada.

## O que fazer

- Adotar a contagem de chats pendentes no badge do Dock e o sinalizador de atenção `!` para agentes aguardando input (`#42061`, `#41949`).
- Avaliar suporte a indicadores equivalentes no Linux via D-Bus LauncherEntry (`#41918`).
- Incorporar o fim de coletas forçadas de GC no renderer em condições de memória elevada (`#42133`).
- Adotar a serialização incremental de abas alteradas para o background writer (`#42127`).
- Suprimir a republicação contínua do grafo completo de sessões na thread principal em mudanças de status (`#42104`).
- Antecipar a inicialização do chat journal writer e adiar manutenções (`#42045`, `#42024`).
- Pular tarefas de manutenção do Codex quando a CLI não estiver instalada (`#42132`, `#42096`).
- Expor método de foco programático de abas de chat na CLI do BrzA (`#42069`).
