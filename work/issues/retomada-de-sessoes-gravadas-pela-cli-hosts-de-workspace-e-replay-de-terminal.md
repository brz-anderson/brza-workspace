---
status: open
description: Os PRs #42651, #42614, #42555, #42580, #41980, #41206 e as issues #40329, #30621, #42619 trazem fechamento de abas via CLI por tab-id, unificação do histórico do Codex (~/.codex), retenção de sessão e replay durável.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-11
tags:
  - tooling
  - infra
---

# Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal

Rastreado dos PRs abertos no upstream [`stablyai/orca#42651`](https://github.com/stablyai/orca/pull/42651) (resolve Issue [`#40329`](https://github.com/stablyai/orca/issues/40329)),
[`stablyai/orca#42614`](https://github.com/stablyai/orca/pull/42614) (resolve Issue [`#30621`](https://github.com/stablyai/orca/issues/30621)),
[`stablyai/orca#42555`](https://github.com/stablyai/orca/pull/42555) (resolve Issue [`#42553`](https://github.com/stablyai/orca/issues/42553)),
[`stablyai/orca#42580`](https://github.com/stablyai/orca/pull/42580) (resolve Issue [`#35719`](https://github.com/stablyai/orca/issues/35719)),
[`stablyai/orca#42504`](https://github.com/stablyai/orca/pull/42504),
[`stablyai/orca#42484`](https://github.com/stablyai/orca/pull/42484) (resolve Issue [`#42470`](https://github.com/stablyai/orca/issues/42470)),
[`stablyai/orca#42481`](https://github.com/stablyai/orca/pull/42481),
[`stablyai/orca#42391`](https://github.com/stablyai/orca/pull/42391),
[`stablyai/orca#42374`](https://github.com/stablyai/orca/pull/42374) (resolve Issue [`#40658`](https://github.com/stablyai/orca/issues/40658)),
[`stablyai/orca#42368`](https://github.com/stablyai/orca/pull/42368),
[`stablyai/orca#42290`](https://github.com/stablyai/orca/pull/42290) (resolve Issue [`#42289`](https://github.com/stablyai/orca/issues/42289)),
[`stablyai/orca#41980`](https://github.com/stablyai/orca/pull/41980),
[`stablyai/orca#41206`](https://github.com/stablyai/orca/pull/41206) (resolve Issue [`#41204`](https://github.com/stablyai/orca/issues/41204)),
[`stablyai/orca#41183`](https://github.com/stablyai/orca/pull/41183),
[`stablyai/orca#41248`](https://github.com/stablyai/orca/pull/41248),
[`stablyai/orca#41247`](https://github.com/stablyai/orca/pull/41247), além das issues
[`stablyai/orca#42619`](https://github.com/stablyai/orca/issues/42619) e
[`stablyai/orca#41184`](https://github.com/stablyai/orca/issues/41184).

## O problema

1. **Acúmulo de abas de agentes ao tentar reutilizar sessões hibernadas via CLI (`#41206`, `#41204`):**
   - O seletor de reaproveitamento de sessões exigia um processo PTY ativo e ocioso no host. Quando um agente entrava em
     hibernação para poupar recursos, o processo era deliberadamente encerrado enquanto a aba e o histórico conversacional
     permaneciam gravados;
   - Ao disparar novas automações agendadas ou prompts via CLI (`orca agent launch --reuse`), o sistema considerava a sessão
     inexistente e criava uma nova aba com outro coordenador em vez de acordar a sessão hibernada em seu painel original,
     gerando proliferação excessiva de abas e perda de continuidade de contexto.
2. **Seleção arbitrária do host padrão em workspaces com múltiplos servidores pareados (`#41183`):**
   - Na presença de múltiplos hosts pareados capazes de executar comandos de um workspace, o seletor `Run on` escolhia o
     primeiro host pela ordem bruta do array retornado pela descoberta, ignorando a preferência do usuário ou a proximidade de rede;
   - Isso provocava despachos acidentais para hosts lentos ou de testes em vez do host primário configurado.
3. **Lentidão O(N log N) ao resolver host de workspace por ordenação global de pastas (`#41248`):**
   - Durante a resolução do host responsável por um único workspace, a rotina ordenava recursivamente todas as pastas de
     projetos registradas no aplicativo, degradando a latência de troca de abas e o arranque inicial da janela.
4. **Captura inconsistente de snapshots de replay do terminal (`#41247`):**
   - O mecanismo de gravação e replay de terminal capturava snapshots de tela em posições de cursor e buffers divergentes
     durante transmissões ativas de saída, causando artefatos visuais e corrupção parcial ao restaurar sessões de agentes TUI.
5. **Invisibilidade do workspace ativo no Studio a partir da CLI (`#41184`):**
   - Scripts de workflow e integrações externas via CLI não possuíam forma de consultar qual workspace está visível no monitor
     ou qual janela de host remoto está em foco pelo operador, dificultando orquestrações conscientes de contexto.
6. **Perda e truncamento do histórico de terminal ao reconectar ou suspender o processo (`#41980`):**
   - Ao reiniciar o Orca ou reabrir abas de terminal suspensas, históricos longos (ex.: 5.000 linhas) encolhiam drasticamente
     para ~1.000 linhas se o comando redesenhasse a última linha ou caso o buffer em memória sofresse overflow;
   - Leituras de tela podiam substituir o log salvo por cópias truncadas em tempo de execução, perdendo o histórico intermediário.
7. **Perda do bookmark de retomada de agentes quando o processo falha na inicialização (`#42290`, resolve `#42289`):**
   - Quando um agente restaurado encontrava erro ou falhava imediatamente no arranque do processo, o sistema descartava o registro de retomada (*resume bookmark*) e convertia a aba em um shell comum desvinculado, impedindo novas tentativas de restauração.
8. **Agentes ociosos há muito tempo perdendo a sessão ao acordar do sleep (`#42391`):**
   - Ao colocar um workspace para dormir (*sleep*), agentes que permaneceram ociosos por tempo suficiente para que seu registro de hook expirasse não eram salvos no registro de suspensão do processo principal; ao acordar o workspace e abrir a aba, o terminal subia como shell vazio em vez de retomar o agente.
9. **Falta de controle direcional no split de terminais via CLI (`#42374`, resolve `#40658`):**
   - O comando `orca terminal split` suportava apenas divisões implícitas à direita ou abaixo, sem permitir posicionar painéis de monitoramento ou status acima ou à esquerda do terminal de trabalho sem arrastar manualmente com o mouse.
10. **Avisos verbosos e redundantes no diálogo de fechamento de terminais em execução (`#42368`):**
    - O diálogo de confirmação continha parágrafos explicativos de cancelamento de sleep e duplicação do título da aba, tornando a confirmação lenta e poluída visualmente.
11. **Falha espúria em sondas SSH por encerramento de conexão antes do handshake (`#42484`, resolve `#42470`):**
    - Sondas de conectividade SSH com servidores remotos e hosts de workspace falhavam intermitentemente quando o `ProxyCommand` encerrava o túnel precocemente (`Connection closed by UNKNOWN port 65535`), sem tentativas automáticas de repetição (*retries*).
12. **Falta de granularidade no log de encerramento de terminais pelo daemon (`#42481`):**
    - O daemon registrava saídas de processo de terminal com código de status genérico 0, ocultando se o término decorreu de saída normal (`exited`), sinal do sistema (`signaled`) ou ação do usuário (`operator_close`).
13. **Invisibilidade e falta de acompanhamento do painel focado via CLI (`#42555`, resolve `#42553`):**
    - Ferramentas e automações externas não conseguiam determinar qual painel de terminal estava em foco no workspace ativo nem acompanhar mudanças de foco sem realizar polling ineficiente de todo o inventário PTY.
14. **Acúmulo de estado de sessão e placeholders de workspaces excluídos (`#42580`, resolve `#35719`):**
    - Workspaces deletados deixavam para trás milhares de linhas de layouts, abas, scrollback e placeholders vazios no arquivo de sessão, inflando o perfil em megabytes e degradando o tempo de salvamento contínuo.
15. **Travamento de statusline do Claude no Windows em stdin infinito (`#42504`):**
    - Atualizações abandonadas da linha de status do Claude no Windows mantinham o processo bloqueado aguardando leitura de `stdin` sem teto de timeout, acumulando processos zumbis.
16. **Impossibilidade de fechar abas de terminais já parados via CLI sem interação manual (`#42651`, resolve `#40329`):**
    - Automações externas e scripts de limpeza não podiam fechar abas de terminais mortos/finalizados sem intervenção gráfica do usuário, acumulando abas inativas.
17. **Fragmentação e deriva do histórico do Codex entre múltiplas contas (`#42614`, resolve `#30621`):**
    - A separação de diretórios por perfil gerava duplicação maciça de arquivos `.jsonl` em `~/.codex` e inconsistência no histórico compartilhado de conversas.
18. **Telas congeladas em hosts de terminal legados (`#42619`):**
    - Falhas de sincronização causavam congelamento da saída do terminal em hosts com versões desatualizadas do daemon.

## O que o upstream propõe e implementa

1. **Descoberta e restauração in-place de sessões gravadas via CLI (`#41206`):**
   - Adiciona `orca agent sessions --worktree <selector> --json` para listar todas as conversas gravadas em painéis de terminal,
     incluindo sessões hibernadas (`sleeping panes`);
   - Introduz `orca agent resume --pane <paneKey>` e `--agent <id> --session <providerSessionId>`, restaurando o processo no painel
     original com os mesmos argumentos de inicialização salvos sem criar abas secundárias nem roubar foco do desktop;
   - Ajusta automações de reutilização para visarem a última execução registrada, acordando a sessão gravada antes da entrega
     do prompt e preservando evidências de falha caso a restauração seja impedida.
2. **Seleção determinística de host por preferência configurada (`#41183`):**
   - Ordena os hosts elegíveis com base nas preferências explícitas do workspace em vez da ordem aleatória do array de sockets.
3. **Resolução direta de host sem varredura completa do disco (`#41248`):**
   - Substitui a ordenação custosa de todas as pastas registradas pela verificação direta do caminho do workspace alvo.
4. **Ponto único de sincronização para snapshots de replay (`#41247`):**
   - Bloqueia a captura de snapshots em posições intermediárias, registrando apenas em pontos de repouso de saída do terminal.
5. **Relatório de workspace focado na janela via CLI (`#41184`):**
   - Exposição via RPC e CLI do estado de visualização ativa entre múltiplos hosts pareados.
6. **Preservação durável do histórico de terminal pelo processo em background (`#41980`):**
   - Transfere para o processo gerenciador do terminal a responsabilidade exclusiva de gravar a saída em ordem sem reescritas truncadas;
   - Salva o histórico retido antes de rotacionar logs de saída e valida a leitura durável no disco antes de suspender comandos em ciclos de Sleep/Wake.
7. **Retenção do bookmark de retomada em falhas de boot de agentes (`#42290`, resolve `#42289`):**
   - Mantém o bookmark de retomada e o registro do agente intactos na aba mesmo se o processo morrer durante a inicialização, permitindo reexecutar a retomada sem converter o painel em shell comum.
8. **Recuperação de agentes ociosos em sleep a partir do checkpoint live salvo (`#42391`):**
   - Caso o hook row do agente não esteja mais disponível por inatividade prévia durante a suspensão do workspace, promove o checkpoint durável `live` salvo na sessão para criar um registro normal de `worktree-sleep`, garantindo a execução do comando `--resume` ao reabrir a aba.
9. **Suporte a divisões direcionais de painel no terminal via CLI (`#42374`, resolve `#40658`):**
   - Estende `orca terminal split --direction up|down|left|right` na CLI e RPC compartilhado, permitindo posicionar o novo painel acima ou à esquerda do terminal ativo com propagação consistente de proporções e layout sincronizado.
10. **Diálogo conciso de fechamento de terminais em execução (`#42368`):**
    - Remove textos explicativos redundantes de retomada e labels repetidos no `CloseTerminalDialog`, focando a confirmação na ação direta de parada do processo.
11. **Retry automático com backoff em sondas SSH com erro transitório de ProxyCommand (`#42484`, resolve `#42470`):**
    - Adiciona lógica de novas tentativas com retardo em probes de verificação SSH ao detectar encerramentos precoces do túnel proxy antes da resposta do daemon.
12. **Classificação estruturada da razão de término de terminais (`#42481`):**
    - Emite eventos de diagnóstico detalhados registrando a causa exata do fim do terminal (`exited`, `signaled`, `operator_close` e sinais POSIX recebidos).
13. **Consulta e acompanhamento em tempo real do painel de terminal focado via CLI (`#42555`, resolve `#42553`):**
    - Adiciona o atributo `focused: boolean` em `orca terminal list --json` (verdadeiro para o painel ativo na aba de terminal visível do workspace ativo);
    - Introduz o comando `orca terminal watch-focus [--json]`, que monitora via RPC long-poll e emite o identificador do painel focado a cada transição sem polling contínuo.
14. **Limpeza profunda de estado de sessão de workspaces excluídos (`#42580`, resolve `#35719`):**
    - Remove todas as abas salvas, layouts, scrollback e registros de retomada de workspaces apagados;
    - Deixa de recriar placeholders vazios e elimina 65% das linhas do arquivo de sessão em perfis pesados, acelerando as rotinas de salvamento.
15. **Delimitação de leitura em stdin no statusline do Claude no Windows (`#42504`):**
    - Aplica limites de tempo à leitura de entrada para permitir que processos de atualização órfãos terminem adequadamente.
16. **Comando `orca terminal close --tab-id <tabId>` para fechar abas inativas via CLI (`#42651`, resolve `#40329`):**
    - Permite fechar abas de terminais já finalizados programaticamente através do seu identificador de aba (`--tab-id`);
    - Valida o estado do processo subjacente e recusa com segurança o fechamento de terminais ainda vivos (`terminal_tab_live`), protegendo processos em andamento contra interrupções acidentais.
17. **Compartilhamento unificado do histórico do Codex (`~/.codex`) via links sem duplicação (`#42614`, resolve `#30621`):**
    - Unifica o armazenamento de sessões e histórico conversacional do Codex entre diferentes contas e perfis através de junctions e links simbólicos, eliminando arquivos `.jsonl` redundantes e divergências de estado.
18. **Mitigação de telas congeladas em hosts de terminal legados (`#42619`):**
    - Detecta e recupera a transmissão de saída de tela em hosts remotos que executam versões anteriores do daemon de terminal, prevenindo congelamentos de buffer.

## O que fazer

- Implementar o comando `orca terminal close --tab-id <tabId>` com proteção `terminal_tab_live` (`#42651`, resolve `#40329`).
- Adotar o compartilhamento de `~/.codex` entre perfis sem duplicação de dados (`#42614`, resolve `#30621`).
- Mitigar o congelamento de buffers em hosts de terminal legados (`#42619`).

- Implementar o acompanhamento do terminal focado via CLI com `orca terminal watch-focus` e flag `focused` em listagens (`#42555`, resolve `#42553`).
- Aplicar a limpeza profunda de estado de sessão e eliminação de placeholders de workspaces excluídos (`#42580`, resolve `#35719`).
- Adicionar retries resilientes para probes SSH com encerramento de ProxyCommand (`#42484`, resolve `#42470`).
- Registrar causas estruturadas de encerramento de terminais nos logs do daemon (`#42481`).
- Delimitar o tempo de leitura de stdin no statusline do Claude no Windows (`#42504`).
- Resgatar agentes ociosos em sleep usando o checkpoint live salvo para evitar regressão para shell plano (`#42391`).
- Permitir divisões de terminal direcionais (`up`, `down`, `left`, `right`) via CLI e RPC (`#42374`, resolve `#40658`).
- Simplificar o diálogo de fechamento de terminais ativos com cópia enxuta (`#42368`).
- Reter o bookmark de retomada de agentes em falhas prematuras de inicialização (`#42290`, resolve `#42289`).
- Preservar o histórico completo de terminais através do processo de background em reconexões e suspensões (`#41980`).
- Incorporar a descoberta e reativação in-place de sessões gravadas de agentes (`orca agent sessions` e `orca agent resume`)
  para eliminar a proliferação de abas em automações contínuas (`#41206`).
- Adotar a seleção de host por preferências configuradas no `Run on` (`#41183`).
- Aplicar a otimização de resolução de host de workspace sem ordenação global de pastas (`#41248`).
- Adotar a sincronização consistente de snapshots de replay no terminal (`#41247`).
- Disponibilizar consulta CLI do workspace atualmente ativo no aplicativo (`#41184`).
