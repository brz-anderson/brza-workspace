---
status: open
description: Releitura de imagens locais (#48451), pairing web resiliente (#48524), títulos reais de perguntas (#48530) e recuperação de itens recusados (#48526).
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-12
tags:
  - tooling
  - infra
references:
  - https://github.com/stablyai/orca/pull/48451
  - https://github.com/stablyai/orca/pull/48524
  - https://github.com/stablyai/orca/pull/48530
  - https://github.com/stablyai/orca/pull/48526
  - https://github.com/stablyai/orca/issues/48588
  - https://github.com/stablyai/orca/pull/48397
  - https://github.com/stablyai/orca/pull/48432
  - https://github.com/stablyai/orca/pull/48417
  - https://github.com/stablyai/orca/issues/48416
  - https://github.com/stablyai/orca/pull/48354
  - https://github.com/stablyai/orca/issues/48303
  - https://github.com/stablyai/orca/issues/48252
  - https://github.com/stablyai/orca/pull/48327
  - https://github.com/stablyai/orca/issues/48292
  - https://github.com/stablyai/orca/pull/43498
  - https://github.com/stablyai/orca/pull/48065
  - https://github.com/stablyai/orca/pull/48163
  - https://github.com/stablyai/orca/pull/48037
  - https://github.com/stablyai/orca/issues/48036
  - https://github.com/stablyai/orca/pull/48182
  - https://github.com/stablyai/orca/issues/48048
  - https://github.com/stablyai/orca/pull/47981
  - https://github.com/stablyai/orca/pull/47952
  - https://github.com/stablyai/orca/pull/47906
  - https://github.com/stablyai/orca/pull/47657
  - https://github.com/stablyai/orca/commit/70a1f42a331
  - https://github.com/stablyai/orca/commit/7c095f7e34d
---

# Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle

Rastreado dos PRs abertos no upstream [`stablyai/orca#47981`](https://github.com/stablyai/orca/pull/47981),
[`stablyai/orca#47952`](https://github.com/stablyai/orca/pull/47952) (commit `70a1f42a331`),
[`stablyai/orca#47906`](https://github.com/stablyai/orca/pull/47906),
[`stablyai/orca#47657`](https://github.com/stablyai/orca/pull/47657) (commit `7c095f7e34d`),
[`stablyai/orca#47716`](https://github.com/stablyai/orca/pull/47716) (resolve Issue [`#47703`](https://github.com/stablyai/orca/issues/47703)),
[`stablyai/orca#47409`](https://github.com/stablyai/orca/pull/47409),
[`stablyai/orca#45854`](https://github.com/stablyai/orca/pull/45854),
[`stablyai/orca#47657`](https://github.com/stablyai/orca/pull/47657),
[`stablyai/orca#47629`](https://github.com/stablyai/orca/pull/47629),
[`stablyai/orca#45918`](https://github.com/stablyai/orca/pull/45918),
[`stablyai/orca#42532`](https://github.com/stablyai/orca/pull/42532),
[`stablyai/orca#46138`](https://github.com/stablyai/orca/pull/46138),
[`stablyai/orca#46581`](https://github.com/stablyai/orca/pull/46581),
[`stablyai/orca#46201`](https://github.com/stablyai/orca/pull/46201),
[`stablyai/orca#45969`](https://github.com/stablyai/orca/pull/45969),
[`stablyai/orca#46211`](https://github.com/stablyai/orca/pull/46211),
[`stablyai/orca#46202`](https://github.com/stablyai/orca/pull/46202),
[`stablyai/orca#46028`](https://github.com/stablyai/orca/pull/46028),
[`stablyai/orca#46185`](https://github.com/stablyai/orca/pull/46185),
[`stablyai/orca#46024`](https://github.com/stablyai/orca/pull/46024),
[`stablyai/orca#45690`](https://github.com/stablyai/orca/pull/45690),
[`stablyai/orca#46003`](https://github.com/stablyai/orca/pull/46003),
[`stablyai/orca#45986`](https://github.com/stablyai/orca/pull/45986),
[`stablyai/orca#45988`](https://github.com/stablyai/orca/pull/45988),
[`stablyai/orca#45506`](https://github.com/stablyai/orca/pull/45506),
[`stablyai/orca#45912`](https://github.com/stablyai/orca/pull/45912),
[`stablyai/orca#45749`](https://github.com/stablyai/orca/pull/45749),
[`stablyai/orca#45031`](https://github.com/stablyai/orca/pull/45031),
[`stablyai/orca#46043`](https://github.com/stablyai/orca/pull/46043),
[`stablyai/orca#45221`](https://github.com/stablyai/orca/pull/45221),
[`stablyai/orca#45240`](https://github.com/stablyai/orca/pull/45240),
[`stablyai/orca#45264`](https://github.com/stablyai/orca/pull/45264),
[`stablyai/orca#45313`](https://github.com/stablyai/orca/pull/45313),
[`stablyai/orca#45840`](https://github.com/stablyai/orca/pull/45840) (resolve Issue [`#45839`](https://github.com/stablyai/orca/issues/45839)),
[`stablyai/orca#45522`](https://github.com/stablyai/orca/pull/45522),
[`stablyai/orca#44979`](https://github.com/stablyai/orca/pull/44979),
[`stablyai/orca#45053`](https://github.com/stablyai/orca/pull/45053),
[`stablyai/orca#44781`](https://github.com/stablyai/orca/pull/44781),
[`stablyai/orca#44745`](https://github.com/stablyai/orca/pull/44745) (resolve Issue [`#44715`](https://github.com/stablyai/orca/issues/44715)),
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
38. **Exclusão prematura de branch em falhas parciais de remoção de worktree (`#44979`):**
    - Quando um arquivo com lock de processo (como volumes Docker montados ou arquivos de root) impedia a exclusão física da pasta do checkout, `git worktree remove` desregistrava o worktree e o Studio apagava o branch local e o push-target imediatamente;
    - A pasta remanescente ficava órfã e sem branch associado, e tentativas posteriores de exclusão eram recusadas pelo Git e pela interface porque o repositório já não rastreava aquele diretório.
39. **Instanciação redundante de shells ociosos durante a criação de worktrees para agentes (`#45053`):**
    - Ao criar um novo worktree de agente, o sistema subia temporariamente um shell ocioso intermediário antes de abrir a aba real do agente, impondo atrasos na prontidão da interface e desperdiçando processos de PTY.
40. **Recargas completas e custosas da projeção de layout em mutações duráveis (`#44781`):**
    - Mutações de layout e admissão/descarte de painéis disparavam uma notificação ampla que forçava a recarga de todas as partições de workspaces do host, mesmo quando apenas um workspace ou painel isolado havia sido modificado.
41. **Exclusão de rollouts do Codex no cleanup quando conversas forked ainda dependem de seu histórico (`#45221`):**
    - A limpeza periódica de rollouts do Codex avaliava a elegibilidade de rollouts sem verificar se conversas bifurcadas (*forked chats*) ativas continuavam lendo o histórico original, apagando sessões ainda em uso.
42. **Deleção acidental de arquivos de configuração e login pela recuperação de escritas atômicas (`#45240`):**
    - Em interrupções de escrita de arquivos com cópia temporária retida (*held copy*), o mecanismo de recuperação sobrescrevia ou deletava o arquivo retido caso um conflito ocorresse, arriscando apagar arquivos de configuração ou credenciais de autenticação.
43. **Logout falso e perda de login no Codex diante de erro transitório de leitura em `~/.codex/auth.json` (`#45264`):**
    - Qualquer erro transitório de leitura (permissão, lock de arquivo) em `~/.codex/auth.json` era interpretado como logout definitivo pela rotina de sincronização, apagando a sessão espelhada do usuário.
44. **Perda de edições concorrentes em `config.toml` do Codex por sobrescrita cega (`#45313`):**
    - O escritor de configurações do Codex lia `config.toml`, aplicava edições e substituía o arquivo sem validar se gravações concorrentes haviam ocorrido no intervalo, sobrescrevendo alterações feitas pelo usuário ou pelo agente.
45. **Falha no comando "Stage All" do Git na presença de links compartilhados ignorados (`#45840`, resolve `#45839`):**
    - O comando `git add` falha com código 1 quando um pathspec de exclusão aponta para um caminho que as regras de ignore já ocultam. Ao preparar todas as alterações no worktree, o Studio excluía indiscriminadamente todos os links compartilhados (como `node_modules` ou junctions no Windows), falhando o staging sempre que um desses links constava no `.gitignore`.
46. **Hooks de permissão do Cursor e Command Code autorizando ferramentas fora do Orca (`#45522`):**
    - Hooks instalados pelo Orca para o Cursor respondiam `{"permission": "allow"}` para qualquer sessão do Cursor na máquina (inclusive fora do Orca), autorizando operações sensíveis sem intervenção do usuário; além disso, hooks do Command Code executavam varreduras caras de processos ancestrais (`ps`) e podiam poluir painéis alheios.
47. **Instrução de erro enganosa ao criar worktree sugerindo flag inexistente `--base` (`#45986`):**
    - Quando a criação de um novo worktree falhava por ausência de um branch base padrão no repositório, o texto de ajuda orientava o desenvolvedor a passar `--base <branch>`, quando o parâmetro suportado pela CLI é estritamente `--base-branch <branch>`, gerando falhas em cadeia na linha de comando.
48. **Falha no comando "Stage All" do Git quando links compartilhados residem dentro de submódulos (`#45988`):**
    - A rotina de exclusão de links compartilhados no Git falhava ao processar worktrees com submódulos inicializados, pois o pathspec de exclusão tentava referenciar links compartilhados internos através da fronteira do submódulo, causando erro 128 no `git add`.
49. **Exclusão de diretório substituto em sobras de remoção de worktree e perda de marcador `.git` no WSL (`#45506`):**
    - Durante a limpeza de diretórios residuais de remoções incompletas (*leftovers*), se outro checkout ou pasta fosse montada no mesmo caminho após o erro inicial, a rotina podia apagar a pasta errada; além disso, a remoção do marcador `.git` no WSL falhava em conferir a identidade real do checkout, corrompendo referências cruzadas.
50. **Exclusão de workspace ativo acordando desnecessariamente workspaces irmãos adormecidos (`#45912`):**
    - Ao deletar o workspace focado na interface, o mecanismo de transferência de foco escolhia o próximo workspace da lista e disparava imediatamente o seu despertar (*wake*), mesmo que o irmão estivesse em repouso configurado (*slept sibling*), provocando uso excessivo de memória e inicialização indesejada de processos.
51. **Varredura lenta e redundante em lookups de worktree re-indexando todos os checkouts (`#45749`):**
    - Qualquer consulta simples de existência ou caminho de um worktree acionava uma re-indexação completa de todos os checkouts registrados no repositório, penalizando comandos de terminal e automações com latências proporcionais ao número total de branches.
52. **Execução de comandos Git capturados na thread principal causando congelamentos de interface (`#45031`):**
    - Comandos do Git executados internamente para sincronização de status e conferência de branches rodavam síncronos na thread principal do processo renderer no macOS e Linux, provocando pequenos engasgos na digitação e animações durante operações de checkout.
53. **Expiração precoce de sessões de agentes inativos em painéis abertos pelo TTL de 7 dias (`#46043`):**
    - Sessões de agentes em painéis ou abas que permaneciam abertas por mais de 7 dias sem atividade recente tinham seu status de sessão expurgado pelo coletor de lixo periódico (TTL fixo de 7 dias), impossibilitando a visualização de histórico ou continuação do chat sem recarregar o workspace.
54. **Salto visual e lacuna em branco no diálogo de exclusão de workspace (`#45969`):**
    - O diálogo de exclusão sofria um salto visual exibindo uma lacuna em branco enquanto o status das evidências e arquivos em risco era calculado, em vez de exibir uma linha de status fixa e suave.
55. **Falhas em testes de links compartilhados, junctions e IPC no Windows (`#46211`, `#46202`):**
    - No Windows, symlinks compartilhados criavam links padrão que requeriam elevação de privilégios, quebrando testes de IPC, git capture e index-safety que necessitam de junctions NTFS.
56. **Remoção inadvertida de regras customizadas do Cursor em arquivos compartilhados (`#46028`):**
    - A injeção de regras operacionais para o agente Cursor sobrescrevia arquivos compartilhados de regras em vez de utilizar um arquivo exclusivo isolado, removendo customizações do usuário ao desinstalar.
57. **Watchdog de profiler concorrendo com a thread principal travada (`#46185`):**
    - Quando a thread principal do Electron sofria um congelamento (*hang*), o watchdog de detecção tentava inicializar o profiler de CPU diretamente na própria thread estagnada, impedindo a geração do relatório de diagnóstico.
58. **Degradação de performance por re-parsing JSON repetido em leituras de status de agentes (`#46024`):**
    - A cada consulta periódica de status de sessão de agente, o sistema realizava o parse repetido do JSON bruto de status de todas as linhas em vez de reutilizar os registros estruturados já em cache.
59. **Perda de turnos de chats antigos clonados do Codex ao vinculá-los às sessões originais (`#45690`):**
    - Ao restabelecer a ligação entre chats clonados e seus originais do Codex, o mecanismo de reconciliação descartava turnos intermediários de transcrições antigas, truncando o histórico da conversa.
60. **Homes de bots adotados indevidamente como workspaces pais em varreduras automáticas (`#46003`):**
    - Pastas de trabalho de bots configurados eram identificadas erroneamente como repositórios pais de workspaces em rotinas automáticas de parentesco de diretórios, poluindo a hierarquia de projetos.
61. **Risco de exclusão acidental de checkouts restaurados durante recuperação de remoção e limpeza de órfãos (`#46138`):**
    - Durante a recuperação de remoções interrompidas de worktrees e limpezas de órfãos no host e no WSL, a ausência de conferência contínua do marcador `.git` e da identidade `dev:ino` do diretório raiz permitia que diretórios recriados ou substituídos por links no mesmo caminho fossem varridos recursivamente. Além disso, o regex de padding de `gitdir` sofria retrocesso quadrático (20k espaços levavam ~190ms).
62. **Varredura sequencial lenta em buscas de prosa de turnos no journal de chat (`#46581`):**
    - Leituras de prosa de turnos específicos no Session History e no journal realizavam varreduras lineares em todo o histórico da conversa sem utilizar o índice de turnos, degradando a performance em chats longos.
63. **Layout excessivamente expandido no modal de confirmação de exclusão de workspace (`#46201`):**
    - O diálogo de confirmação de exclusão de workspaces utilizava espaçamentos e caixas excessivas que quebravam em telas menores ou diálogos densos.
64. **Interrupção de salvamentos e travamento de writes pelo helper de tidy-up em segundo plano do chat (`#45918`):**
    - Quando o processo auxiliar de checkpoint/tidy-up do chat store sofria crash ou ficava em silêncio além do deadline, a rotina de escrita ficava retida aguardando indefinidamente em vez de reiniciar o worker isolado e aplicar backoff, gerando paradas em gravações ativas.
65. **Deslocamento e reordenação abrupta de linhas na lista de limpeza enquanto o modal de exclusão está aberto (`#42532`):**
    - Se eventos em segundo plano atualizassem o estado dos workspaces durante a exibição do diálogo de confirmação de exclusão do cleanup, as linhas da tabela mudavam de posição repentinamente sob o cursor do usuário, aumentando o risco de exclusão inadvertida de worktrees errados.
66. **Falha na remoção de diretórios somente leitura gerados em recuperações de espaço no macOS sob Bun (`#47629`):**
    - No macOS, a chamada recursiva de remoção de árvore (`rm`) sob o runtime Bun rejeita diretórios somente leitura com o código de erro `ENOTEMPTY`, enquanto sob Node.js o erro reportado é `EACCES`. Como o mecanismo de recuperação de espaço (*reclaim space*) executava a rotina de desproteção de diretórios (`makeDirectoriesWritable`) e retry apenas diante de `EACCES`/`EPERM`, a limpeza falhava silenciosamente sob Bun deixando arquivos órfãos sem desalocação.
67. **Esgotamento de espaço em disco durante a conversão de journals de chat legados (`#47409`):**
    - A conversão de históricos antigos para o novo SQLite convertia diários inteiros enquanto o arquivo antigo permanecia no disco. Em journals de dezenas de gigabytes, a duplicação temporária consumia o espaço livre restante, gerando falhas catastróficas de I/O por disco cheio.
68. **Rejeição permanente de journals de chat com estruturas abandonadas da v1.4.219 e out/2026 (`#45854`, `#47657`):**
    - A prova de integridade (*proof*) descartava e recusava silenciosamente qualquer journal que contivesse colunas ou tabelas criadas por builds intermediárias (`queued_message_pauses` e `queued_messages.source_json`), impedindo sua conversão e bloqueando o expurgo seguro do arquivo antigo.
69. **Falso status "working" em panes do Claude após conclusão de turno durante compactação ociosa (`#47716`, resolve `#47703`):**
    - A compactação automática ociosa (`idleCompaction`) do Claude Code relê arquivos de contexto após o evento `Stop` do turno por meio de hooks `PreToolUse`/`PostToolUse`. Esses hooks eram normalizados incondicionalmente como atividade de trabalho, abrindo um turno novo sem fim que mantinha o spinner ativo na barra lateral e limpava `lastAssistantMessage`.
70. **Acúmulo de pastas temporárias residuais de git de plugins (`#47952`, commit `70a1f42a331`):**
    - Operações de download, empacotamento ou validação de plugins deixavam pastas temporárias de git (`.git` residuais) órfãs no sistema de arquivos, desperdiçando armazenamento ao longo do tempo.
71. **Interrupção indesejada de fluxos de trabalho por atualizações automáticas intempestivas (`#47981`):**
    - O instalador automático de atualizações disparava reinicializações do app no meio de sessões ativas com agentes, sem oferecer opção para postergar a atualização até períodos de ociosidade do desenvolvedor.
72. **Proliferação de chats abertos e ociosos de execuções finalizadas de automação (`#47906`):**
    - Execuções concluídas de automações mantinham conversas abertas na barra lateral indefinidamente, poluindo a visualização de chats ativos e consumindo recursos residuais.
73. **Execução inconsistente da auditoria de históricos legados de chat no startup (`#47657`, commit `7c095f7e34d`):**
    - A conferência do estado de conversão de journals antigos de chat não era garantida em todos os arranques, deixando instalações sem feedback claro sobre conversões pendentes.
74. **Falta de arquivamento e exclusão em lote para conversas de bots (`#48303`):**
    - Com o aumento de automações contínuas, centenas de chats de bots acumulam-se no painel de conversas sem opção de seleção múltipla para exclusão ou arquivamento em lote, exigindo remoção manual individual de cada sessão.
75. **Ausência de opção para remover a pasta home do bot na exclusão (`#48252`):**
    - Ao desinstalar ou excluir um bot configurado, o aplicativo remove apenas o registro do bot mas deixa o diretório home residual intacto em disco, sem questionar se o operador deseja expurgar os arquivos locais de configuração e dados gerados.
76. **Invalidação e re-escaneamento do File Explorer a cada troca de worktree (`#48327`, Issue `#48292`):**
    - A alternância de foco entre worktrees no File Explorer descartava o cache da árvore de arquivos e disparava varredura completa do sistema de arquivos para o novo checkout, causando atrasos de renderização e perda de pastas expandidas na navegação rápida.
77. **Falsas modificações no git status por divergência de decomposição NFD no macOS (`#48397`):**
    - No macOS/APFS, arquivos com caracteres acentuados são gravados em decomposição UTF-8 (NFD). O analisador de `git status` comparava strings em NFC contra NFD, exibindo falsos arquivos modificados e gerando conflitos ao preparar commits.
78. **Falha de estilização (dim) em arquivos ignorados com nomes em codificação NFD (`#48432`):**
    - A engine de matching do `.gitignore` não convertia paths NFD para a forma canônica antes da correspondência, fazendo com que itens ignorados fossem renderizados como arquivos normais.
79. **Sobrecarga de alocação de caminhos NFD repetidos no macOS (`#48417`, Issue `#48416`):**
    - O runtime executava normalizações e instanciações repetidas de strings NFD para cada entrada de diretório no macOS, penalizando o garbage collector em repositórios grandes.
80. **Falha de renderização de worktree ativo quando ocultado pela barra lateral (`#48354`):**
    - Ao colapsar ou expandir a barra lateral sobrepondo a janela principal, a superfície do worktree ativo era desmontada sem preservação de viewport, exigindo recálculo e provocando flickering ao retornar.
81. **Imagens locais em cache não atualizadas após refocus da janela (`#48451`):**
    - Quando um arquivo de imagem em disco era modificado por um processo externo ou script de build, o visualizador mantinha os bytes em cache mesmo após alternar o foco da janela.
82. **Travamento no arranque da interface web pareada em caso de erro de migração de banco (`#48524`):**
    - Se a migração de esquema de banco de dados encontrasse uma inconsistência transitória no host, o servidor web pareado ficava preso no estado `starting` sem reportar erro legível nem tentar recuperação.
83. **Retenção indevida do estado "Needs you" e títulos opacos de perguntas em itens (`#48530`):**
    - Após o operador responder às perguntas de um item, o selo "Needs you" continuava aceso na sidebar, e o cabeçalho exibia IDs internos em vez do enunciado textual real da pergunta.
84. **Perda de respostas digitadas em itens quando a submissão é recusada por validação (`#48526`):**
    - Se uma resposta submetida a uma pergunta de item fosse rejeitada por validação do modelo ou timeout, o formulário limpava os campos de texto, forçando o operador a redigitar o conteúdo.
85. **Proliferação de cópias efêmeras de worktrees em falhas de cleanup de automações (`#48588`):**
    - Automações abortadas mid-flight deixavam pastas temporárias de worktree sem marcação de expiração ou remoção automática no próximo ciclo de coleta.

## O que o upstream propõe e implementa

- **Invalidação de cache e recarregamento de imagens locais ao focar a janela (`#48451`):**
  - Monitora o evento de foco da janela (`refocus`) e verifica o `mtime` de imagens locais em exibição, atualizando a textura visual caso o arquivo em disco tenha mudado.
- **Recuperação e fallback em falhas de migração na web pareada (`#48524`):**
  - Encerra graciosamente o estado de startup da web pareada emitindo diagnóstico estruturado em caso de falha de migração, permitindo reinicialização sem travamento do daemon.
- **Limpeza atômica de "Needs you" e renderização de títulos reais de perguntas (`#48530`):**
  - Desativa o estado "Needs you" no momento exato em que a resposta é gravada e exibe o resumo textual formatado da pergunta na barra de progresso e cartões de itens.
- **Preservação e recuperação de rascunhos em respostas de itens recusadas (`#48526`):**
  - Mantém o texto digitado no formulário em caso de rejeição de envio, oferecendo ação imediata de reenvio ou edição.
- **Coleta programada de worktrees temporários de automações interrompidas (`#48588`):**
  - Identifica worktrees órfãos criados por automações que terminaram com falha e agenda sua remoção segura na próxima rodada de cleanup.
- **Normalização canônica de caminhos NFD no git status para macOS (`#48397`):**
  - Aplica normalização uniforme entre UTF-8 NFC e NFD nas saídas do git status, eliminando arquivos fantasmas e falsos positivos de alteração.
- **Renderização correta (dim) de arquivos ignorados em NFD (`#48432`):**
  - Normaliza os nomes de arquivos antes de conferir as regras de ignore, assegurando a exibição esmaecida padrão.
- **Reuso de modelo e deduplicação de strings para caminhos normalizados no macOS (`#48417`, Issue `#48416`):**
  - Implementa cache e compartilhamento de representações de strings NFD para caminhos de filesystem, reduzindo alocações transitórias.
- **Preservação de superfície montada de worktree ativo sob colapso da sidebar (`#48354`):**
  - Mantém o container do worktree ativo montado na árvore DOM mesmo quando ocultado temporariamente pela barra lateral.
- **Exclusão e arquivamento em lote de conversas de bots (`#48303`):**
  - Introduz seleção múltipla com ações de "Archive All" e "Delete Selected" para chats de automações e bots.
- **Opção de deleção completa da pasta home de bots (`#48252`):**
  - Adiciona checkbox opcional no diálogo de remoção de bots para expurgar a pasta home e arquivos de contexto locais.
- **Cache persistente e restauração de estado do File Explorer entre worktrees (`#48327`, resolve `#48292`):**
  - Mantém o cache de árvore e os nós expandidos por worktree, evitando re-varreduras completas ao alternar checkouts.
- **Limpeza de pastas temporárias de git deixadas por plugins (`#47952`, commit `70a1f42a331`):**
  - Implementa rotina de expurgo seguro para remover pastas temporárias residuais de git criadas por operações de plugins.
- **Auditoria de históricos antigos em todas as inicializações sem exclusões (`#47657`, commit `7c095f7e34d`):**
  - Garante que a conferência de histórico legado execute no boot e reporte detalhadamente o estado das conversões sem deletar dados.
- **Espera por ociosidade (away) para aplicação de atualizações automáticas (`#47981`):**
  - Permite configurar o atualizador automático para aplicar updates apenas quando o usuário estiver ausente.
- **Fechamento automático de chats de automações concluídas após tempo ocioso (`#47906`):**
  - Encerra silenciosamente chats de execuções terminadas de automações após timeout de inatividade configurável.


- **Retenção de status `done` durante compactação ociosa do Claude (`#47716`, resolve `#47703`):**
  - No normalizador de eventos do Claude, quando `PreCompact` chega com `trigger: "auto"` e o lead já havia reportado `done`, o painel associa o `prompt_id` do turno finalizado e restabelece o turno concluído em cache para os hooks subsequentes, impedindo a reabertura de turnos espúrios e mantendo `lastAssistantMessage`.
- **Salvaguarda de espaço em disco na conversão do journal de chat antigo (`#47409`, commit `15830ffd7e7`):**
  - Estima o espaço necessário medindo os bytes de cada chat (`octet_length`) antes da conversão, verificando se o volume livre permanece acima do piso de segurança (10 GB ou 5% do disco); abaixo do piso, a conversão é adiada com backoff e reportada como erro de armazenamento temporário sem esgotar o disco.
- **Aceitação e verificação de journals com formatos históricos da v1.4.219 e out/2026 (`#45854`, commit `ee8d885823a`, PR `#47657`):**
  - Admite tabelas históricas (`queued_message_pauses` e `queued_messages.source_json`) com colunas exatas na prova de inventário, garantindo que instalações antigas sejam convertidas e auditadas em todas as inicializações sem exclusões prematuras.
- **Retry resiliente na remoção de diretórios somente leitura sob Bun (`#47629`):**
  - Adiciona o código de erro `ENOTEMPTY` à lista de códigos elegíveis para retentativa de remoção (`makeDirectoriesWritable` + retry único de `rm`) ao desalocar diretórios gerados no macOS, mantendo as proteções de descendência e segurança de diretório intactas.
- **Reinicialização resiliente do worker de checkpoint/tidy-up do chat store sem travar salvamentos (`#45918`):**
  - Mantém o helper de tidy-up ativo em segundo plano; se o worker ficar ocioso ou silencioso além do deadline ou sofrer crash, é substituído com backoff limitado, reportando a duração e causa da indisponibilidade sem travar operações de save.
- **Estabilização da ordem de linhas durante a abertura do diálogo de exclusão no cleanup (`#42532`):**
  - Congela a ordenação das linhas da lista enquanto o modal de confirmação de deleção estiver aberto, prevenindo saltos de layout e cliques acidentais.
- **Proteção rigorosa de checkouts restaurados e validação de marcadores no cleanup (`#46138`):**
  - Vincula a prova de propriedade do órfão estritamente ao marcador `.git` pré e pós-prova, abortando a varredura caso o marcador desapareça ou seja substituído no meio do processo;
  - Revalida a identidade do diretório raiz (`dev:ino` via `lstatBigInt`) após a enumeração e antes de disparar exclusões recursivas, impedindo a travessia de symlinks substitutos;
  - Re-stat do `.git` após ler o payload `gitdir` e parse linear do padding em $O(N)$ em vez de backtracking regex quadrático;
  - Confinamento da varredura no WSL ao subshell `cwd` e proteção de checkouts Win32 com gitdir `C:/...` sob WSL.
- **Índice de turnos para buscas rápidas de prosa no journal (`#46581`):**
  - Utiliza o índice de turnos para realizar lookups pontuais de texto e prosa por turno no journal de conversas, eliminando varreduras sequenciais completas.
- **Modal de confirmação de exclusão de workspace compacto (`#46201`):**
  - Compacta o layout e os espaçamentos do diálogo de confirmação de remoção de workspace, garantindo visualização limpa e foco direto nas evidências.
- **Linha de status fixa no diálogo de exclusão (`#45969`):**
  - Mantém uma linha de status de altura fixa no modal Delete, eliminando lacunas em branco e transições abruptas de layout.
- **Suporte a junctions para links de diretório em testes no Windows (`#46211`, `#46202`):**
  - Cria fixtures de diretórios compartilhados como junctions no Windows, garantindo execução confiável dos testes de IPC e git safety sem privilégios de administrador.
- **Isolamento de regras do Cursor em arquivo exclusivo com remoção apenas de bytes inalterados (`#46028`):**
  - Grava regras do Cursor em arquivo próprio e remove estritamente os bytes padrão inseridos, preservando customizações do desenvolvedor.
- **Watchdog de profiler fora da thread principal estagnada (`#46185`):**
  - Desacopla o arranque do profiler de CPU da main thread durante congelamentos, garantindo a captura precisa de traces de diagnóstico.
- **Leitura direta de linhas de status de agentes sem re-parsing (`#46024`):**
  - Elimina parses redundantes de JSON em leituras periódicas de status de agentes, aliviando o consumo de CPU.
- **Preservação de todos os turnos de chats copiados do Codex (`#45690`):**
  - Retém a integridade de todos os turnos de conversas herdadas do Codex ao reconectá-las às sessões originais.
- **Isolamento de homes de bots contra adoção como workspace pai (`#46003`):**
  - Exclui pastas de bots das heurísticas de parentesco automático de workspaces.
- **Correção da dica de comando sugerindo `--base-branch` na criação de worktrees (`#45986`):**
  - Ajusta a mensagem de erro emitida quando o branch base padrão não é encontrado, instruindo corretamente o uso da flag `--base-branch`.
- **Suporte a links compartilhados em submódulos no Stage All do Git (`#45988`):**
  - Trata fronteiras de submódulos ao compor os pathspecs de exclusão de links compartilhados, permitindo que o `git add` prepare alterações em repositórios compostos sem colisão.
- **Validação de identidade em limpezas residuais de worktrees e proteção `.git` no WSL (`#45506`):**
  - Confere a identidade do repositório antes de apagar pastas residuais de worktrees incompletos e preserva o link `.git` no WSL até a confirmação formal da remoção.
- **Preservação do estado adormecido de workspaces irmãos na exclusão do workspace ativo (`#45912`):**
  - Ajusta a seleção do próximo workspace ativo para transferir o ponteiro de exibição sem disparar o despertar de processos em workspaces marcados como adormecidos (*slept*).
- **Lookup indexado de worktrees em $O(1)$ sem re-indexação global (`#45749`):**
  - Utiliza busca indexada por varredura pré-computada para localizar worktrees, eliminando re-indexações completas a cada chamada individual.
- **Isolamento de comandos Git em worker dedicado de processos no macOS e Linux (`#45031`):**
  - Move a execução de comandos Git capturados para um worker dedicado de processos, desonerando a thread principal e eliminando engasgos de interface.
- **Preservação de sessões de agentes inativos em painéis abertos além do TTL de 7 dias (`#46043`):**
  - Isenta sessões vinculadas a painéis e abas atualmente abertas do expurgo automático de status de 7 dias, retendo os dados enquanto o usuário mantiver o painel no workspace.

- **Preservação de rollouts do Codex lidos por chats forked e indexação em worker (`#45221`):**
  - Executa a indexação de referências de forks em worker dedicado uma vez por varredura com cache de cabeçalhos por rollout ID, preservando rollouts ancestrais enquanto houver chats derivados ativos.
- **Recuperação segura de escritas atômicas interrompidas via links por hash de conteúdo (`#45240`):**
  - Vincula arquivos retidos a nomes livres baseados em hash de conteúdo e restaura o arquivo a partir da cópia retida antes de qualquer exclusão temporária, protegendo credenciais e configurações contra perdas.
- **Tolerância a leituras inacessíveis de `auth.json` no Codex sem logout indevido (`#45264`):**
  - Trata `~/.codex/auth.json` ilegível como falha de sincronização em vez de logout automático, removendo logins espelhados apenas diante de confirmação explícita de encerramento de sessão.
- **Proteção contra sobrescrita concorrente em `config.toml` do Codex (`#45313`):**
  - Passa os bytes exatos lidos na edição e confere o conteúdo do arquivo imediatamente antes do rename atômico, repetindo a edição sobre os bytes atualizados em caso de modificação externa e rotacionando `config.toml.bak` com segurança.
- **Exclusão cirúrgica de links não-ignorados no Stage All do Git (`#45840`, resolve `#45839`):**
  - Executa uma verificação rápida (`git check-ignore`) para excluir apenas os links compartilhados que não estejam ignorados pelo repositório, garantindo que o comando "Stage All" funcione com regras de `node_modules` ou junctions no Windows.
- **Neutralidade de hooks de agentes fora do ambiente Orca (`#45522`):**
  - Faz com que os hooks de permissão do Cursor respondam `{}` (sem decisão) em sessões externas, evitando aprovação arbitrária de ferramentas, e remove varreduras pesadas de ancestrais no Command Code.
- **Preservação de branch e exclusão de `.git` por último em falhas parciais de worktree (`#44979`):**
  - Mantém o branch Git e a referência de push-target intactos caso a remoção do diretório do worktree falhe;
  - Remove o link `.git` do checkout como última operação para que a pasta remanescente ainda comprove sua vinculação ao repositório, permitindo que a ação de Delete na linha com falha finalize a exclusão com segurança assim que o bloqueador for liberado.
- **Supressão de shells ociosos redundantes no spawn de agentes (`#45053`):**
  - Ajusta o seeder de terminais iniciais para vincular diretamente o painel do agente sem instanciar shells ociosos intermediários.
- **Recarga de layout restrita aos workspaces reportados pela escrita (`#44781`):**
  - Mutações duráveis agora reportam com precisão cirúrgica quais workspaces e partições foram tocados, recarregando apenas os alvos necessários e preservando caches intactos.
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

- Proteger checkouts restaurados no cleanup e validar marcador `.git` pré e pós-prova com parse linear de `gitdir` (`#46138`).
- Utilizar índice de turnos para consultas de texto e prosa por turno no journal de conversas (`#46581`).
- Adotar layout compacto e direto no modal de confirmação de exclusão de workspaces (`#46201`).
- Manter linha de status fixa no modal Delete eliminando gaps e saltos de layout (`#45969`).
- Utilizar junctions em links de diretório no Windows para compatibilidade de testes de IPC e git (`#46211`, `#46202`).
- Isolar regras do Cursor em arquivo exclusivo preservando edições do usuário (`#46028`).
- Executar watchdog de profiler em thread separada da main thread congelada (`#46185`).
- Ler linhas de status de agentes diretamente da memória sem re-parsing JSON repetido (`#46024`).
- Preservar turnos de chats antigos do Codex ao vinculá-los às sessões originais (`#45690`).
- Isolar diretórios de bots contra adoção automática como workspaces pais (`#46003`).
- Corrigir a mensagem de erro na criação de worktrees para recomendar `--base-branch` (`#45986`).
- Tratar submódulos no comando "Stage All" do Git para não falhar na presença de links compartilhados (`#45988`).
- Proteger pastas de checkouts contra exclusão incorreta em limpezas residuais e no WSL (`#45506`).
- Evitar que a exclusão de um workspace acorde workspaces irmãos que estejam adormecidos (`#45912`).
- Adotar busca indexada direta de worktrees para eliminar re-indexações globais frequentes (`#45749`).
- Despachar a execução de comandos Git para worker de processos em background no macOS e Linux (`#45031`).
- Preservar sessões de agentes ativas em painéis abertos além do TTL de 7 dias (`#46043`).
- Preservar rollouts ancestrais do Codex no cleanup quando conversas forked ativas dependerem de seu histórico (`#45221`).
- Assegurar recuperação atômica de arquivos retidos via links baseados em hash de conteúdo (`#45240`).
- Tratar leituras inacessíveis em `~/.codex/auth.json` como falhas transitórias de sincronização sem deslogar a conta (`#45264`).
- Proteger gravações em `config.toml` do Codex contra sobrescrita concorrente comparando bytes originais e rotacionando backups com segurança (`#45313`).
- Validar caminhos ignorados via `git check-ignore` para viabilizar "Stage All" na presença de links compartilhados (`#45840`, resolve `#45839`).
- Tornar os hooks de permissão de agentes neutros (`{}`) fora do ambiente do aplicativo (`#45522`).
- Preservar branch e push-target em exclusões parciais de worktrees mantendo o link `.git` por último para permitir finalização posterior (`#44979`).
- Suprimir a criação redundante de shells ociosos durante o provisionamento de worktrees de agentes (`#45053`).
- Restringir a recarga de projeção de layout exclusivamente aos workspaces reportados por escritas duráveis (`#44781`).
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
- Reter o status `done` e preservar `lastAssistantMessage` durante compactações ociosas (`idleCompaction`) do Claude (`#47716`, resolve `#47703`).
- Aplicar guarda de disco na conversão do journal legado avaliando tamanho por chat e respeitando o piso de 10 GB livres (`#47409`, commit `15830ffd7e7`).
- Aceitar tabelas e colunas históricas (`queued_message_pauses` e `queued_messages.source_json`) para auditar e converter journals antigos em todas as inicializações sem exclusões indevidas (`#45854`, commit `ee8d885823a`, PR `#47657`).
- Adotar a detecção e proteção de arquivos ignorados em risco (`readWorktreeAtRiskLocalFiles`) antes da exclusão de workspaces (`#41446`).
- Incorporar o gatilho de substituição direta de revisões de chat (`journal_outcome_item_supersede`) para estancar o crescimento do SQLite (`#41392`).
- Aplicar a corroboração do marcador do composer para instâncias adotadas do Claude no `tui-idle` (`#41366`).
- Adotar a política de cache de badges do Linear sem revalidação por foco de janela (`#41384`).
- Reiniciar o checkpoint worker de tidy-up do chat store com backoff exponencial sem reter gravações ativas (`#45918`).
- Estabilizar a ordem de exibição das linhas da lista de cleanup durante a abertura do diálogo de exclusão (`#42532`).
- Incluir `ENOTEMPTY` nos códigos de retry para remoção de árvores somente leitura na rotina de reclaim space (`#47629`).
- Expurga pastas temporárias residuais de git deixadas por operações de plugins (`#47952`, commit `70a1f42a331`).
- Executar a verificação de integridade do histórico antigo de chat em todas as inicializações (`#47657`, commit `7c095f7e34d`).
- Permitir que atualizações automáticas aguardem até que o usuário esteja ausente (away) (`#47981`).
- Fechar automaticamente chats de execuções finalizadas de automação após tempo ocioso configurado (`#47906`).
- Adotar interface de cartões agrupados, etapas de confirmação e card de progresso em background para Workspace Cleanup (`#43498`, commit `e6f066034bc`).
- Manter o modal de revisão de deleção de workspaces em tamanho estável durante o fluxo (`#48065`, commit `8d25f6f8417`).
- Prevenir sobreposição de retentativas na limpeza de workspaces (`#48163`, commit `a779ba0f522`).
- Permitir a criação direta de novo workspace sem exibição de diálogo modal (`#48037`, resolve Issue `#48036`).
- Exibir ícone de lua e linha esmaecida para workspaces adormecidos/em repouso no mobile (`#48182`).
- Limpar dinamicamente worktrees de servidores remotos desconectados da barra lateral (`#48048`).
- Implementar arquivamento e deleção em lote para chats e sessões de bots (`#48303`).
- Oferecer opção de remoção da pasta home ao deletar bots para evitar resíduos em disco (`#48252`).
- Reter o cache e a memória de diretórios expandidos do explorador de arquivos entre trocas de worktrees (`#48327`, resolve `#48292`).
- Normalizar caminhos NFD no git status para macOS para eliminar falsas modificações e arquivos fantasmas (`#48397`).
- Corrigir a estilização esmaecida (dim) de arquivos ignorados com caracteres em decomposição NFD (`#48432`).
- Reutilizar representações de strings e modelos para caminhos NFD no macOS para conter alocações em GC (`#48417`, `#48416`).
- Preservar a montagem de superfície de worktrees ativos quando encobertos pela barra lateral (`#48354`).
- Recarregar imagens locais no visualizador de arquivos sob evento de refocus da janela (`#48451`).
- Recuperar o estado da interface web pareada reportando diagnósticos claros em falhas de migração (`#48524`).
- Limpar atomicamente o selo "Needs you" ao responder perguntas e exibir títulos descritivos em itens (`#48530`).
- Reter o rascunho de respostas de itens quando a submissão sofrer recusa ou falha de validação (`#48526`).
- Varrer e expurgar worktrees temporários órfãos de automações interrompidas no cleanup (`#48588`).




