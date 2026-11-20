---
status: open
description: O PR #44745 limpa worktrees de folder workspaces como grupo unificado e o PR #44905 protege pastas WSL sem acordar distros.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-12
tags:
  - tooling
  - infra
---

# Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle

Rastreado dos PRs abertos no upstream [`stablyai/orca#44745`](https://github.com/stablyai/orca/pull/44745) (resolve Issue [`#44715`](https://github.com/stablyai/orca/issues/44715)),
[`stablyai/orca#44905`](https://github.com/stablyai/orca/pull/44905),
[`stablyai/orca#44691`](https://github.com/stablyai/orca/pull/44691),
[`stablyai/orca#44763`](https://github.com/stablyai/orca/pull/44763),
[`stablyai/orca#44025`](https://github.com/stablyai/orca/pull/44025),
[`stablyai/orca#44571`](https://github.com/stablyai/orca/pull/44571),
[`stablyai/orca#44471`](https://github.com/stablyai/orca/pull/44471),
[`stablyai/orca#44209`](https://github.com/stablyai/orca/pull/44209),
[`stablyai/orca#44477`](https://github.com/stablyai/orca/pull/44477) (resolve Issue [`#37707`](https://github.com/stablyai/orca/issues/37707)),
[`stablyai/orca#44445`](https://github.com/stablyai/orca/pull/44445),
[`stablyai/orca#44275`](https://github.com/stablyai/orca/pull/44275),
[`stablyai/orca#43918`](https://github.com/stablyai/orca/pull/43918),
[`stablyai/orca#43587`](https://github.com/stablyai/orca/pull/43587) (resolve Issue [`#43539`](https://github.com/stablyai/orca/issues/43539)),
[`stablyai/orca#43563`](https://github.com/stablyai/orca/pull/43563),
[`stablyai/orca#43557`](https://github.com/stablyai/orca/pull/43557),
[`stablyai/orca#43551`](https://github.com/stablyai/orca/pull/43551) (resolve Issue [`#43523`](https://github.com/stablyai/orca/issues/43523)),
[`stablyai/orca#43532`](https://github.com/stablyai/orca/pull/43532) (resolve Issue [`#43368`](https://github.com/stablyai/orca/issues/43368)),
[`stablyai/orca#43525`](https://github.com/stablyai/orca/pull/43525) (resolve Issue [`#43523`](https://github.com/stablyai/orca/issues/43523)),
[`stablyai/orca#43498`](https://github.com/stablyai/orca/pull/43498),
[`stablyai/orca#43245`](https://github.com/stablyai/orca/pull/43245),
[`stablyai/orca#38128`](https://github.com/stablyai/orca/pull/38128),
[`stablyai/orca#43015`](https://github.com/stablyai/orca/pull/43015),
[`stablyai/orca#43000`](https://github.com/stablyai/orca/pull/43000),
[`stablyai/orca#42959`](https://github.com/stablyai/orca/pull/42959),
[`stablyai/orca#42943`](https://github.com/stablyai/orca/pull/42943),
[`stablyai/orca#42877`](https://github.com/stablyai/orca/pull/42877),
[`stablyai/orca#42905`](https://github.com/stablyai/orca/pull/42905),
além da issue [`stablyai/orca#42611`](https://github.com/stablyai/orca/issues/42611),
além da issue [`stablyai/orca#42909`](https://github.com/stablyai/orca/issues/42909) e dos PRs
[`stablyai/orca#42055`](https://github.com/stablyai/orca/pull/42055),
[`stablyai/orca#42039`](https://github.com/stablyai/orca/pull/42039),
[`stablyai/orca#41858`](https://github.com/stablyai/orca/pull/41858) (resolve Issue STA-15099),
[`stablyai/orca#41835`](https://github.com/stablyai/orca/pull/41835) (resolve Issue STA-15114),
[`stablyai/orca#41833`](https://github.com/stablyai/orca/pull/41833),
[`stablyai/orca#41765`](https://github.com/stablyai/orca/pull/41765),
[`stablyai/orca#41760`](https://github.com/stablyai/orca/pull/41760),
[`stablyai/orca#41483`](https://github.com/stablyai/orca/pull/41483),
[`stablyai/orca#41480`](https://github.com/stablyai/orca/pull/41480),
[`stablyai/orca#41457`](https://github.com/stablyai/orca/pull/41457),
[`stablyai/orca#41446`](https://github.com/stablyai/orca/pull/41446),
[`stablyai/orca#41392`](https://github.com/stablyai/orca/pull/41392),
[`stablyai/orca#41366`](https://github.com/stablyai/orca/pull/41366) (STA-14925 / STA-2380) e
[`stablyai/orca#41384`](https://github.com/stablyai/orca/pull/41384).

## O problema

1. **Perda silenciosa de arquivos locais e segredos ignorados (`.env`) na exclusão de worktrees (`#41446`):**
   - Ao excluir ou limpar um worktree pelo diálogo de cleanup ou pela barra lateral, a checagem `git status` ignorava arquivos
     desconsiderados pelo `.gitignore` (ex.: `.env`, arquivos de configuração local ou chaves privadas);
   - O comando `git worktree remove` apagava pastas e arquivos sem qualquer aviso, levando à perda irreparável de segredos
     locais que não existiam em nenhum outro checkout.
2. **Crescimento descontrolado do banco SQLite de histórico de chat com revisões intermediárias (`#41392`):**
   - No streaming de respostas no chat nativo, cada revisão parcial do texto emitido pelo modelo gravava uma linha completa
     da mensagem no banco de dados. Em conversas com centenas de turnos, o arquivo chegava a centenas de megabytes (ex.: 884 MB para 26k registros),
     gerando lentidão e fragmentação desnecessária no disco;
   - Leituras de abertura e restauração necessitam apenas da primeira versão (para evidência de admissão) e da versão mais recente
     (para exibição final), tornando todas as revisões intermediárias lixo redundante.
3. **Falso estado de prontidão (`tui-idle`) em instâncias adotadas do Claude (`#41366`, STA-14925):**
   - O PR `#40539` garantiu que o Claude só seja considerado ocioso e pronto para despachos após desenhar sua caixa de entrada
     (`❯` + NBSP após `DECSET 2031`). Porém, essa validação era aplicada exclusivamente quando o app iniciava o processo diretamente;
   - Em abas adotadas ou iniciadas por comandos externos cujo título OSC identificava o Claude, o sistema caía na checagem genérica
     de "qualquer texto visível". Mensagens emitidas por hooks de shell (ex.: `zsh-you-should-use`) enganavam o detector,
     fazendo o orquestrador despachar comandos antes do Claude estar pronto e perdendo prompts.
4. **Rajadas desnecessárias de requisições de badges do Linear ao focar a janela (`#41384`):**
   - Cada retorno de foco à janela do app revalidava todos os badges de tarefas do Linear montados na tela após 60 segundos de inatividade,
     gerando centenas de requisições à API do Linear em paralelo sem que o usuário estivesse interagindo com aquelas tarefas.
5. **Visibilidade persistente de workspaces durante cleanup demorado em background (`#41483`):**
   - Na exclusão de workspaces com grande volume de arquivos, a linha permanecia visível na barra lateral durante todo o processo de limpeza em segundo plano;
   - Caso o app sofresse encerramento ou reinicialização durante o processo, o cleanup ficava incompleto e o registro de remoção era perdido.
6. **Execuções duplicadas e concorrentes de `git worktree list` em repositórios grandes (`#41480`):**
   - Dois caches desacoplados no processo principal (um da barra lateral com TTL de 5s e outro de runtime para CLI/agentes com TTL de 30s) disparavam leituras repetidas de worktrees;
   - Em repositórios com centenas de worktrees, o app executava `git worktree list` a cada ~48s, gerando sobrecarga desnecessária de CPU e I/O.
7. **Disparo indevido de atalho de exclusão de workspace com foco no terminal ou editor (`#41457`):**
   - O atalho de teclado para exclusão de workspace não verificava se o foco estava na árvore da barra lateral, abrindo diálogos de exclusão mesmo quando o usuário estava digitando no terminal ou editor.
8. **Sobrecarga de rede e lentidão nas varreduras de cleanup de worktrees (`#41765`):**
   - A varredura de histórico Git para verificar se o trabalho de um worktree já havia sido integrado (`merged`/`squashed`) realizava downloads lentos de blobs faltantes em clones parciais (`--filter=blob:none`);
   - Em repositórios com dezenas de worktrees, a checagem demorava mais de 20s e corria o risco de expirar antes de concluir.
9. **Ausência de automação em segundo plano para aplicação de regras de limpeza de workspaces (`#41760`):**
   - A limpeza de workspaces exigia abertura manual do diálogo de cleanup a partir da barra de status, acumulando branches mesclados, checkouts inativos e diretórios órfãos ao longo do tempo.
10. **Falha na exclusão de workspaces e travamento de cleanup em servidores pareados e headless (`#41858`, STA-15099):**
    - Ao excluir workspaces hospedados por servidores pareados ou `orca serve`, o processo fechava terminais e recusava a deleção porque a lista durável de exclusões pendentes só era carregada na inicialização do desktop, deixando pastas e linhas órfãs presas na interface sem recuperação após reinício;
    - Além disso, cancelamentos de pré-checagem em desligamentos do host não protegiam checkouts e WSL sofria com timeouts prematuros de 30s.
11. **Varreduras locais de arquivos ignorados continuavam executando após fechar prévia de deleção (`#41835`, STA-15114):**
    - O fechamento ou retargeting do diálogo de exclusão de workspace abortava a requisição remota, mas o canal local descartava o sinal de cancelamento, mantendo múltiplos processos `git ls-files` concorrentes enfileirados em segundo plano consumindo CPU e I/O desnecessariamente.
12. **Perda permanente de histórico e metadados ao remover worktrees para liberar espaço em disco (`#41833`):**
    - A única forma de recuperar espaço em disco era excluir o workspace completamente, apagando anotações, comentários, PRs vinculados e linhagem da árvore de trabalho, sem um mecanismo para arquivar apenas o checkout e restaurá-lo sob demanda.
13. **Ausência de interface visual para gerenciar regras de limpeza e execuções imediatas (`#42039`):**
    - As regras de cleanup e o runner em background existiam apenas na camada de serviço ou CLI, sem uma tela dedicada nas configurações para visualizar o que foi liberado, escolher regras ativas e disparar limpezas manuais com prévia.
14. **Incapacidade de ajustar ou desativar regras de limpeza por projeto individual (`#42055`):**
    - Repositórios com dinâmicas e criticidades distintas seguiam rigidamente a política global, sem suporte em *Project Settings* para desativar a automação ou definir regras customizadas por projeto.
15. **Acúmulo de gigabytes de transcrições e rollouts de agentes pertencentes a workspaces já excluídos (`#42877`):**
    - Ao deletar um workspace, o histórico conversacional de agentes (Claude, Codex, Antigravity, OpenCode, Hermes) permanecia intacto em `~/.claude`, `~/.codex` e `agent-session-domain.db`, ocupando até dezenas de gigabytes em perfis consolidados.
16. **Falta de separação visual entre cleanup manual e automático nas configurações (`#42905`, Issue `#42909`):**
    - As regras de limpeza automática ficavam misturadas com os gatilhos manuais na interface, gerando confusão sobre quais worktrees seriam expurgados automaticamente em background e impedindo a definição declarativa de pastas regeneráveis em `orca.yaml`.
17. **Retenção de histórico de conversas específicas do Claude Code, Codex e Orca Chat após deleção (`#42959`, `#43000`, `#43015`):**
    - A política genérica de deleção não contemplava granularidade por agente: chats do Claude Code (`#42959`), histórico estruturado do Codex (`#43000`) e conversas nativas do Orca Chat (`#43015`) deixavam resíduos em diferentes diretórios de perfil.
18. **Perda de rascunhos de editor não salvos quando workspaces desaparecem com o app fechado (`#42943`):**
    - Se um workspace ou branch fosse removido externamente (ex.: por script ou git worktree prune) enquanto o aplicativo estava fechado, ao reabrir o app os buffers com rascunhos de edição pendentes eram descartados silenciosamente sem opção de recuperação.
19. **Interface monolítica de Workspace Cleanup sem cartões agrupados nem progresso em background (`#43498`):**
    - O modal de limpeza de workspace exibia uma lista única plana sem agrupar ações por repositório ou separar etapas de confirmação e deleção, e travava a interface visual sem oferecer card de progresso em background durante expurgos extensos.
20. **Vazamento de metadados em streaming e falta de dimensionamento de heap no scanner do AI Vault (`#43525`, resolve `#43523`):**
    - Sessões transmitidas no AI Vault retinham metadados indefinidamente na memória durante indexações prolongadas, e a ausência de controle de heap no scanner gerava esgotamento de memória (OOM).
21. **Falha e pedidos indevidos de reautorização ao remover worktrees externos irmãos (`#43532`, resolve `#43368`):**
    - Ao tentar remover worktrees localizados em pastas irmãs fora da raiz primária, o processo falhava ou insistia em diálogos redundantes de reautorização de sistema de arquivos.
22. **Congelamento da UI no Windows durante polling de transcripts do Codex por `openSync` síncrono (`#43587`, resolve `#43539`):**
    - A cada ciclo de polling de transcripts do Codex, o processo invocava `fs.openSync` na thread principal para reabrir arquivos de transcript em disco. No Windows, a latência de chamadas I/O síncronas no NTFS provocava engasgos e congelamentos de 5 a 9 segundos na interface.
23. **Sobrescrita maciça e desnecessária de chats salvos na inicialização (`#43557`):**
    - No boot do aplicativo, o gerenciador de sessões reescrevia indiscriminadamente o estado de todos os chats salvos no disco, gerando tempestade de I/O em workspaces com dezenas de sessões gravadas em vez de renovar apenas os leases das conversas ativas.
24. **Migração redundante de baseline em upgrades com journal de chat inalterado (`#43563`):**
    - Durante atualizações de versão, o processo de migração recalculava baselines para todo o histórico mesmo quando o arquivo de journal de chat legado permanecia idêntico, atrasando a conclusão do startup.
25. **Esgotamento de heap no scanner de sessões (`#43551`, resolve `#43523`):**
    - Ao processar repositórios massivos ou com milhares de turnos de agentes, o scanner de sessões podia exceder o limite de memória do V8 e quebrar a aplicação sem mecanismo de degradação suave ou recuperação controlada.
26. **Perda silenciosa de turnos em andamento por crash ou reinício do servidor/app (`#43918`):**
    - Quando o processo do runtime ou servidor remoto caía ou reiniciava durante a geração de uma resposta de agente (mid-turn), o chat permanecia travado em estado incompleto ou perdia o contexto do turno em execução, forçando o operador a reiniciar manualmente a conversa ou perder o raciocínio em andamento.
27. **Falha irreversível `transcriptUnreadable` ao retomar chat com pastas de projeto ilegíveis (`#44477`, resolve `#37707`):**
    - Ao retomar uma conversa no Native Chat ou a partir do histórico, o scanner buscava o transcript por ID em todos os baldes de projeto;
    - Caso encontrasse qualquer pasta ilegível (como diretórios com permissão root deixados por `sudo claude`), o scanner lançava erro `EACCES` e abortava como `transcriptUnreadable` sem tentar outros diretórios válidos.
28. **Perda da mensagem digitada na criação de worktree caso o agente falhe na inicialização (`#44445`):**
    - Ao criar um novo worktree com mensagem inicial de prompt, se o agente não conseguisse subir (por falha de binário ou ambiente), a mensagem digitada pelo usuário era descartada e perdida sem oportunidade de recuperação ou envio para um terminal substituto.
29. **Conversão quadrática lenta de chats legados rescaneando itens por mensagem (`#44275`):**
    - A rotina de conversão de chats legados rescaneava a lista inteira de itens para cada mensagem individual, resultando em complexidade $O(N^2)$ e travando a interface ao carregar conversas longas.
30. **Incompatibilidade do comando `/session` com o atalho `/resume` no menu slash e na lista de sessões (`#44471`):**
    - No ecossistema TUI (como OpenCode), o comando tradicional de seleção de sessões é `/sessions`. No Native Chat, o comando equivalente é `/resume`. Usuários que digitavam `/session` ou `/sessions` não encontravam o comando no autocompletar fora do idioma inglês. Além disso, a lista de histórico de sessões não priorizava a retomada no Native Chat quando este era a superfície padrão configurada do agente.
31. **Chat corrompido bloqueando auto-continue de limite de uso de todos os outros chats e re-lendo a cada 10s (`#44209`):**
    - Quando um chat salvo apresentava inconsistência ou corrupção em seu journal/transcript, o serviço de retomada automática de limites de uso (*usage-limit auto-continue*) era completamente bloqueado para todos os outros chats íntegros do sistema. Ademais, o leitor de status insistia em tentar reler o arquivo corrompido em loop a cada 10 segundos, consumindo CPU e I/O inutilmente.
32. **Exclusão inadvertida de conversas da pasta de importação do Codex durante cleanup de workspace (`#44691`):**
    - A rotina de expurgo de histórico de chat ao deletar um workspace varria recursivamente caminhos de rollouts sem verificar se o arquivo pertencia à pasta externa de importação do Codex (`codex-rollout-protected-roots.ts`). Links simbólicos ou subpastas de checkouts podiam levar à exclusão permanente de históricos de conversas importadas de outras ferramentas ou diretórios do usuário.
33. **Manutenção indevida de confiança (*agent trust*) de Codex e Antigravity após exclusão de worktrees (`#44763`):**
    - Ao excluir um worktree pela barra lateral, as entradas de autorização gravadas em `projects."<path>"` do Codex e `trustedWorkspaces` do Antigravity permaneciam registradas nas configurações. Se um novo checkout fosse criado posteriormente no mesmo caminho, ele já iniciava com status de confiável sem aprovação prévia do operador. Além disso, a remoção da confiança síncrona na main thread bloqueava o Electron no Windows durante retries de rename.
34. **Quebra na importação de conversas Codex de pastas externas e travamentos por pastas lentas (`#44025`):**
    - A importação de históricos de conversas Codex de pastas externas (`codex-accounts`) estava quebrada desde a versão 1.4.262. Quando a pasta de origem continha links rígidos ausentes ou respondia lentamente, o processo bloqueava a fila inteira de histórico do host, e falhas de disco cheio (`ENOSPC`) lançavam exceções não tratadas em vez de registrar a conversa como pendente de tentativa posterior.
35. **Sobrecarga de memória e scans repetidos na prova de integridade do journal legado (`#44571`):**
    - O verificador de conversão do journal legado (`journal-legacy-proof`) lia mensagens enfileiradas ordenadas em SQL, forçando o SQLite a criar B-trees temporárias para centenas de milhares de linhas e travando a inicialização por até 1s por chat. A ausência de paginação e persistência do cursor forçava re-varreduras completas a cada boot.
36. **Limpeza prematura ou parcial de worktrees em workspaces de pasta com múltiplos repositórios (`#44745`, resolve `#44715`):**
    - Quando um workspace é configurado como pasta contendo múltiplos repositórios (`folder workspace`), o mecanismo de cleanup avaliava cada worktree isoladamente com base apenas nas evidências de seu próprio repositório Git;
    - Se a regra "merged" estivesse ativa, o sistema removia o worktree do repositório A (já integrado) enquanto o worktree do repositório B (no mesmo folder workspace) ainda estava ativamente em uso e com trabalho em andamento.
37. **Inicialização desnecessária de distros WSL paradas para proteger pastas de importação do Codex (`#44905`):**
    - Durante as varreduras de limpeza de histórico de chat, a rotina de proteção de diretórios de importação do Codex tentava ler o conteúdo da pasta inspecionando o sistema de arquivos via WSL, o que forçava o boot de distribuições WSL em repouso;
    - Isso causava picos de CPU, atrasos no ciclo de cleanup e acordava instâncias Linux sem necessidade.

## O que o upstream propõe e implementa

- **Limpeza unificada de worktrees em folder workspaces como um único grupo (`#44745`, resolve `#44715`):**
  - Trata todos os worktrees vinculados a um folder workspace e suas linhagens descendentes como um único grupo indivisível;
  - Um worktree só é removido quando todos os membros do workspace de pasta forem elegíveis para remoção, mantendo o grupo intacto enquanto qualquer repositório irmão ainda estiver em uso;
  - Reavalia os irmãos locais imediatamente antes da remoção e correlaciona a linhagem persistida para evitar exclusões acidentais caso a varredura de algum repositório falhe.
- **Proteção de pasta de importação do Codex no WSL por caminho estático sem acordar distros (`#44905`):**
  - Protege pastas de importação do Codex no WSL resolvendo estaticamente o caminho da distribuição sem acessar ou ler o sistema de arquivos interno;
  - Limita as consultas ao WSL a um lease de 1 segundo e no máximo uma checagem por varredura quando a distro estiver parada, preservando as sessões sem inicializar distribuições em segundo plano.
- **Proteção estrita da pasta de importação do Codex contra exclusões no cleanup (`#44691`):**
  - Implementa proteção por identidade de pasta (`codex-rollout-protected-roots.ts`) antes de cada exclusão permanente de rollout, garantindo que nenhum arquivo sob a raiz de importação do Codex seja apagado durante o cleanup de histórico de workspaces.
- **Revogação automática de confiança de agentes ao excluir worktree via worker dedicado (`#44763`):**
  - Revoga imediatamente as entradas de permissão do Codex (`projects."<path>"`) e Antigravity (`trustedWorkspaces`) em qualquer deleção de worktree por IPC ou CLI;
  - Despacha a atualização de `settings.json` para o worker de confiança de projetos em segundo plano, evitando bloqueios na main thread do Electron no Windows.
- **Resiliência e isolamento da importação de históricos Codex em runner assíncrono (`#44025`):**
  - Restaura o fluxo de importação externa desacoplando o runner da fila principal do host (`codex-history-import-runner.ts`);
  - Realiza cópias eficientes via reflink/clone de blocos (Linux FICLONE, Windows Dev Drive ReFS, macOS `cp -c`), trata `ENOSPC`/`EROFS` com encerramento limpo e mantém registro persistente de staging (`import-staging.txt`).
- **Limitação de leitura em SQL e retomada paginada da prova do journal legado (`#44571`):**
  - Limita a leitura da fila em SQL a no máximo 2.048 linhas e 2 MiB, eliminando a ordenação desnecessária no SQLite;
  - Salva o cursor de progresso a cada 16 páginas, permitindo que inicializações subsequentes continuem a prova a partir do último ponto sem rescanear todo o histórico.
- **Alias `/session` para `/resume` e priorização de retomada no Chat (`#44471`):**
  - Mapeia `/session` e `/sessions` como aliases diretos para o comando `/resume` no autocompletar do composer;
  - Posiciona a ação "Resume in New Chat" como primeira opção no histórico de sessões do AI Vault quando o Native Chat é a superfície padrão do agente, preservando o contexto sem forçar abertura de terminal.
- **Isolamento de chats corrompidos no auto-continue e contenção de re-leituras (`#44209`):**
  - Isola arquivos de journal ou transcripts corrompidos marcando o registro na leitura de status (`corrupt-journal-reads.ts`), assegurando que a falha de um chat não paralise a fila de auto-continue dos demais chats elegíveis;
  - Memoriza a condição de corrupção pelo ciclo de leitura de status, eliminando o polling repetitivo a cada 10 segundos e mantendo a integridade das tentativas de continuação.
- **Tolerância a pastas de projeto ilegíveis no resume de chats Claude (`#44477`, resolve `#37707`):**
  - Trata pastas ilegíveis (`EACCES`) como simples ausência (*miss*), permitindo que a busca continue pelos demais baldes e conclua a retomada do chat com sucesso.
- **Preservação de mensagem inicial em falhas de inicialização de worktrees (`#44445`):**
  - Retém o texto do prompt enviado durante a criação do worktree caso o agente não consiga inicializar, preservando a mensagem no composer ou abrindo-a em um terminal fallback.
- **Conversão linear O(N) de histórico legado de chat (`#44275`):**
  - Otimiza o parser de conversas legadas para converter o histórico em tempo linear $O(N)$ em vez de rescanear todos os itens a cada nova mensagem.
- **Retomada automática de chats interrompidos por crash ou restart (`#43918`):**
  - Implementa continuação de sessões de chat cortadas (`fix(agent-session): continue chats a crash or restart cut, from the runtime`);
  - Ao reiniciar o runtime ou servidor, detecta conversas cortadas no meio de uma geração, reconstrói o estado a partir dos registros persistidos no SQLite/journal e retoma a execução sem perda de turnos ou corrupção de estado.
- **Retenção de descritor único por cursor no polling de transcripts Codex (`#43587`, resolve `#43539`):**
  - Mantém um único file descriptor aberto por cursor de leitura em vez de chamar `openSync` repetidamente na thread principal do Electron/Node, eliminando as pausas de 5–9s no Windows e normalizando a leitura em streaming contínuo.
- **Renovação estrita de leases retidos sem regravação global de chats (`#43557`):**
  - Cessa a reescrita indiscriminada de todos os chats no startup; apenas renova os leases mantidos por abas ou processos ativos, mantendo as demais conversas intactas no disco.
- **Preenchimento incremental de baselines faltantes no upgrade (`#43563`):**
  - Quando o journal legado não foi alterado, o motor de upgrade apenas injeta baselines que estejam estritamente ausentes no novo formato, evitando leituras e escritas completas desnecessárias.
- **Contenção e recuperação de heap no scanner de sessões (`#43551`, resolve `#43523`):**
  - Controla o consumo de memória do scanner paginando objetos e implementa interceptação graciosa caso a memória chegue próxima do limite, recuperando o scanner sem derrubar a aplicação.
- **Cartões agrupados, confirmação em passos e card de progresso em background no Workspace Cleanup (`#43498`):**
  - Agrupa os cartões de worktree por repositório, introduz etapas distintas para confirmação e deleção e exibe cartão de progresso não obstrutivo em segundo plano.
- **Liberação de metadados de sessões transmitidas e controle de heap no scanner do AI Vault (`#43525`, resolve `#43523`):**
  - Libera prontamente os metadados retidos após processamento e parametriza o heap do scanner para conter o footprint de memória na indexação.
- **Remoção de worktrees externos irmãos sem reautorização (`#43532`, resolve `#43368`):**
  - Permite expurgar caminhos de worktrees irmãos registrados externamente sem requisições espúrias de autorização de sistema.
- **Configurações dedicadas para exclusão granular de chats com o workspace (`#42959`, `#43000`, `#43015`):**
  - Adiciona toggles granulares em *Settings › Workspaces* para remover chats do Claude Code (`#42959`), histórico do Codex (`#43000`) e conversas nativas do Orca Chat (`#43015`) junto com o workspace;
  - Limpa caches de sessão associados sem afetar workspaces ativos ou históricos compartilhados.
- **Recuperação e reabertura de rascunhos de editor para workspaces desaparecidos (`#42943`):**
  - Preserva os rascunhos não salvos do editor caso o workspace associado tenha desaparecido enquanto o aplicativo estava fechado, reabrindo os buffers em abas de rascunho recuperadas para salvar em outro local.
- **Varredura at-risk de arquivos ignorados antes de remover worktrees (`#41446`):**
  - Implementa `readWorktreeAtRiskLocalFiles`, listando arquivos com `git ls-files -o -i --exclude-standard --directory`;
  - Descarta pastas regeneráveis (`node_modules`, `dist`, `.venv`, `.next`, `target`, `vendor`), symlinks e arquivos idênticos
    aos do checkout principal (como `.env` padrão replicado pelo setup);
  - Apresenta aviso explícito no modal de exclusão e na barra lateral ("Ignored files will be lost: .env, local/"), bloqueando
    a deleção automática sem confirmação prévia do operador.
- **Compactação contínua de histórico de chat mantendo apenas primeiro e último registro (`#41392`):**
  - Adiciona um gatilho de esquema (`journal_outcome_item_supersede`) que apaga imediatamente a revisão anterior assim que uma
    nova revisão do mesmo item é gravada, estabilizando o custo por escrita em O(1);
  - Roda uma rotina de compactação em thread de worker dedicada 2 minutos após o arranque, paginada em 64 registros com duty cycle de 10%,
    reduzindo a base de itens pela metade sem impacto no loop de eventos principal e reutilizando páginas liberadas no SQLite.
- **Corroboração de marcador de composer para instâncias do Claude identificadas por título (`#41366`):**
  - Estende a exigência do marcador de entrada `❯` para qualquer painel identificado como Claude interativo via título OSC (`paintAgent`);
  - Ignora comandos que executam em modo print (`-p`, `--output-format json`) ou pipelines com pagers (`less`, `more`), assegurando
    que ferramentas de automação e orquestração nunca enviem prompts antes do composer interativo estar pronto.
- **Desativação de refetch de badges do Linear por evento de foco (`#41384`):**
  - Remove os listeners de foco de janela para badges montados, atualizando detalhes apenas na montagem ou via notificação
    específica pós-escrita de ferramentas locais, reduzindo requisições em 83,3%.
- **Ocultação imediata de linha na UI e persistência de cleanup em tabela durável (`#41483`):**
  - Registra exclusões em tabela durável (`worktree-removal-table.ts`) e oculta a linha da visualização imediatamente (`removal-visibility.ts`);
  - Em reinicializações do app com remoções pendentes, o processo retoma o cleanup de arquivos e do registro Git sem intervenção manual.
- **Proprietário único de listagem de worktrees por repositório (`#41480`):**
  - Cria modelo centralizado por repositório e runtime Git, unificando os acessos da barra lateral e do catálogo de runtime;
  - Reutiliza leituras em andamento para requisições concorrentes e invalida o cache apenas diante de mutações ou eventos estruturais do watcher.
- **Restrição de atalhos de exclusão de workspace à seleção da barra lateral (`#41457`):**
  - Vincula o listener de teclado de exclusão estritamente ao container da barra lateral quando focado (`use-sidebar-workspace-delete-keyboard.ts`);
  - Garante que teclas pressionadas no terminal ou editor nunca acionem a caixa de confirmação de exclusão.
- **Varredura offline 4x mais rápida de cleanup de workspaces (`#41765`):**
  - Executa as checagens de merge e provas Git com `GIT_NO_LAZY_FETCH=1` e `GIT_ALLOW_PROTOCOL=none`, impedindo fetches acidentais de rede em clones parciais;
  - Memoiza referências base (`createWorkspaceCleanupRepoRefs`) por repositório durante a varredura e otimiza a busca de squashes (`git log --name-only --no-renames` + `patch-id` apenas para commits com conjunto idêntico de arquivos tocados), reduzindo o tempo de varredura de ~23s para ~5s.
- **Execução automática de regras de cleanup de workspace em background por host (`#41760`):**
  - Implementa o `WorkspaceCleanupRunner` com ciclo de avaliação compartilhada (`evaluateWorkspaceCleanup`), disparado 2 minutos após o boot, a cada hora e 10s após alterações de regras;
  - Executa isoladamente no host/processo dono do repositório (desktop local, orcad de SSH ou WSL), revalidando evidências (pins, drafts não salvos, terminais abertos, daemons e arquivos dirty) imediatamente antes da remoção segura via `queueWorkspaceDelete`.
- **Resiliência e recuperação de exclusão de workspaces em servidores pareados e headless (`#41858`, STA-15099):**
  - Carrega a tabela de exclusões duráveis pendentes tanto no desktop quanto na inicialização de instâncias servidoras (`orca serve`/orcad);
  - Valida o armazenamento de deleção antes de parar terminais, oculta a linha da visualização imediatamente, preserva o caminho e branch até o término do expurgo e retoma limpezas incompletas após reinício do host, sem limite rígido de 30s no WSL.
- **Cancelamento imediato de varreduras locais de arquivos ignorados (`#41835`, STA-15114):**
  - Conecta o `AbortController` ao canal local `getRuntimeWorktreeAtRiskLocalFiles`, interrompendo prontamente chamadas a `git ls-files` e comparações em disco assim que o diálogo de confirmação é fechado ou redirecionado.
- **Mecanismo de arquivamento e restauração de worktrees (`#41833`):**
  - Implementa `worktree.archive`, apagando o diretório de checkout para liberar espaço em disco enquanto preserva o branch, metadados (`WorktreeMeta.archivedCheckout`), notas e histórico;
  - Implementa `worktree.restore`, recriando o worktree a partir do branch preservado com reconstituição de symlinks e cópias de `.worktreeinclude`.
- **Página de configurações Workspace Cleanup com regras e ação imediata (`#42039`):**
  - Adiciona a tela *Settings > Workspace Cleanup*, permitindo configurar regras de exclusão (merged, unchanged, inactive e avançadas de automação);
  - Exibe linha de status com o resultado do último ciclo (workspaces removidos e bytes liberados) e previsão do próximo;
  - Inclui o botão **Clean up now** (`workspaceCleanup.runNow`), apresentando listagem de workspaces a serem removidos imediatamente e permitindo desmarcar individualmente qualquer um deles.
- **Regras de cleanup por projeto em Project Settings (`#42055`):**
  - Adiciona a seção *Workspace cleanup* na página de configurações do projeto, permitindo selecionar entre `Use global` (herda regras globais), `Off` (desativa cleanup no projeto) ou `Custom` (regras específicas por repositório com overrides individuais).
- **Exclusão do journal legado de chat após migração validada (`#43245`):**
  - Remove fisicamente o antigo diário de chat em disco após verificar que o novo armazenamento incorporou todas as mensagens e revisões, recuperando espaço em disco automaticamente.
- **Resiliência na remoção de worktrees com teardown de watcher desautorizado (`#38128`):**
  - Assegura que falhas de autorização de caminho durante a desativação de file watchers não bloqueiem nem abortem a exclusão de worktrees.
- **Exclusão de histórico de agentes ao remover workspaces (`#42877`):**
  - Introduz a configuração opt-in `deleteAgentHistoryWithWorkspace` em *Settings › Workspaces*;
  - Ao excluir um workspace com o toggle ativo, varre e exclui transcrições, arquivos `.jsonl.zst`, rollouts do Codex e registros do `agent-session-domain.db` vinculados a ele, além de oferecer um botão para expurgo retroativo de histórico órfão;
  - Preserva sessões ativas e arquivos tocados nas últimas 24 horas como medida de segurança.
- **Seções distintas de Cleanup Manual e Automático e regras no `orca.yaml` (`#42905`, Issue `#42909`):**
  - Reorganiza *Settings › Workspace Cleanup* em dois blocos claros com validação explícita de regras;
  - Permite declarar pastas regeneráveis (ex.: caches de build ou pastas `target/`) no `orca.yaml` do projeto para limpeza automática segura.

## O que fazer

- Tratar worktrees de repositórios vinculados a um folder workspace como grupo unificado no cleanup para evitar remoções parciais (`#44745`, resolve `#44715`).
- Proteger pastas de importação do Codex em WSL por resolução estática de caminhos sem inicializar distribuições paradas (`#44905`).
- Proteger a pasta externa de importação do Codex contra exclusões acidentais durante o cleanup de histórico de workspaces (`#44691`).
- Revogar a confiança de agentes (Codex e Antigravity) ao deletar worktrees via worker assíncrono para não travar a main thread (`#44763`).
- Isolar a importação de históricos Codex em runner desacoplado da fila principal do host com suporte a reflink e tratamento de ENOSPC (`#44025`).
- Limitar a leitura da fila em SQL e paginar a prova de integridade do journal legado para acelerar o boot (`#44571`).
- Mapear aliases `/session` e `/sessions` para o comando `/resume` e priorizar "Resume in New Chat" no histórico quando o chat for o padrão (`#44471`).
- Isolar chats corrompidos na fila de retomada automática de limites de uso e suspender re-leituras desnecessárias a cada 10s (`#44209`).
- Ignorar pastas de projetos Claude ilegíveis no resume de chat em vez de abortar com `transcriptUnreadable` (`#44477`, resolve `#37707`).
- Reter mensagens iniciais de criação de worktree quando o agente falhar no arranque (`#44445`).
- Converter histórico de chat legado em tempo linear $O(N)$ eliminando rescans repetidos (`#44275`).
- Retomar automaticamente chats cortados no meio da geração após crash ou reinício do runtime (`#43918`).
- Reter descritor de arquivo aberto por cursor no polling de transcripts do Codex, eliminando `openSync` síncrono e congelamentos de UI no Windows (`#43587`, resolve `#43539`).
- Limitar a renovação no startup aos leases de chats ativos em vez de regravar todas as sessões salvas (`#43557`).
- Otimizar migrações de upgrade para preencher apenas baselines ausentes quando o journal antigo estiver inalterado (`#43563`).
- Aplicar controle estrito de memória e recuperação suave no scanner de sessões (`#43551`, resolve `#43523`).
- Adotar interface de cartões agrupados e card de progresso em background para Workspace Cleanup (`#43498`).
- Incorporar liberação imediata de metadados e configuração de heap no scanner do AI Vault (`#43525`, resolve `#43523`).
- Habilitar remoção de worktrees irmãos externos sem disparar erros de reautorização (`#43532`, resolve `#43368`).
- Expurgo seguro do journal antigo de chat após confirmação de integridade no novo store (`#43245`).
- Não interromper a exclusão de worktrees quando o teardown de watchers perder autorização de caminho (`#38128`).
- Implementar exclusão granular de chats do Claude Code, Codex e Orca Chat vinculados a workspaces removidos (`#42959`, `#43000`, `#43015`).
- Preservar e reabrir rascunhos de arquivos não salvos de workspaces que desapareceram externamente (`#42943`).
- Adotar a exclusão segura de histórico de agentes vinculados a workspaces removidos (`#42877`).
- Separar visualmente as seções de cleanup manual e automático nas preferências (`#42905`).
- Adotar a página de configurações *Settings > Workspace Cleanup* com regras visuais, botão 'Clean up now' e prévia de exclusões iminentes (`#42039`).
- Adotar a configuração de regras de cleanup por projeto em *Project Settings* (`#42055`).
- Adotar a recuperação durável de exclusão de workspaces e suporte a cleanup seguro em servidores (`#41858`, STA-15099).
- Propagar o cancelamento de varreduras de arquivos ignorados no fechamento da prévia de exclusão (`#41835`, STA-15114).
- Incorporar o backend de arquivamento e restauração sob demanda de checkouts de worktrees (`#41833`).
- Adotar a varredura offline rápida de cleanup (`#41765`), eliminando lazy fetches do Git e acelerando o cálculo de merges e squashes.
- Incorporar o runner de background de cleanup de workspaces (`#41760`) com revalidação estrita de evidências e proteção contra deleção acidental.
- Adotar a tabela durável de cleanup com ocultação imediata de workspaces em remoção (`#41483`).
- Unificar o gerenciamento de cache de worktrees por repositório para eliminar chamadas redundantes a `git worktree list` (`#41480`).
- Restringir os atalhos de exclusão de workspace exclusivamente ao foco na barra lateral (`#41457`).
- Adotar a detecção e proteção de arquivos ignorados em risco (`readWorktreeAtRiskLocalFiles`) antes da exclusão de workspaces (`#41446`).
- Incorporar o gatilho de substituição direta de revisões de chat (`journal_outcome_item_supersede`) para estancar o crescimento do SQLite (`#41392`).
- Aplicar a corroboração do marcador do composer para instâncias adotadas do Claude no `tui-idle` (`#41366`).
- Adotar a política de cache de badges do Linear sem revalidação por foco de janela (`#41384`).
