---
status: open
description: Ocultacao de pycache em @ (#49645), skills de projetos linkados em comentarios (#49497) e correcoes em stubs CLI (#49516, #49510).
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
references:
  - https://github.com/stablyai/orca/pull/48940
  - https://github.com/stablyai/orca/pull/48923
  - https://github.com/stablyai/orca/pull/48898
  - https://github.com/stablyai/orca/pull/48895
  - https://github.com/stablyai/orca/pull/48844
  - https://github.com/stablyai/orca/pull/48814
  - https://github.com/stablyai/orca/pull/48910
  - https://github.com/stablyai/orca/issues/49047
  - https://github.com/stablyai/orca/issues/49004
  - https://github.com/stablyai/orca/pull/48770
  - https://github.com/stablyai/orca/pull/48707
  - https://github.com/stablyai/orca/pull/48778
  - https://github.com/stablyai/orca/pull/48785
  - https://github.com/stablyai/orca/pull/48805
  - https://github.com/stablyai/orca/pull/48789
  - https://github.com/stablyai/orca/pull/48796
  - https://github.com/stablyai/orca/pull/48819
  - https://github.com/stablyai/orca/pull/48776
  - https://github.com/stablyai/orca/pull/48713
  - https://github.com/stablyai/orca/issues/48777
  - https://github.com/stablyai/orca/pull/48578
  - https://github.com/stablyai/orca/pull/48610
  - https://github.com/stablyai/orca/pull/48659
  - https://github.com/stablyai/orca/pull/48658
  - https://github.com/stablyai/orca/pull/48616
  - https://github.com/stablyai/orca/issues/48635
  - https://github.com/stablyai/orca/issues/48617
  - https://github.com/stablyai/orca/pull/48399
  - https://github.com/stablyai/orca/pull/48440
  - https://github.com/stablyai/orca/pull/48426
  - https://github.com/stablyai/orca/pull/48422
  - https://github.com/stablyai/orca/pull/48421
  - https://github.com/stablyai/orca/pull/48389
  - https://github.com/stablyai/orca/pull/48441
  - https://github.com/stablyai/orca/issues/48410
  - https://github.com/stablyai/orca/issues/48409
  - https://github.com/stablyai/orca/issues/48408
  - https://github.com/stablyai/orca/issues/48464
  - https://github.com/stablyai/orca/pull/48287
  - https://github.com/stablyai/orca/issues/48270
  - https://github.com/stablyai/orca/pull/48245
  - https://github.com/stablyai/orca/issues/48298
  - https://github.com/stablyai/orca/issues/48297
  - https://github.com/stablyai/orca/pull/48026
  - https://github.com/stablyai/orca/issues/48023
  - https://github.com/stablyai/orca/pull/48165
  - https://github.com/stablyai/orca/pull/48177
  - https://github.com/stablyai/orca/pull/47923
  - https://github.com/stablyai/orca/pull/48183
  - https://github.com/stablyai/orca/issues/48028
  - https://github.com/stablyai/orca/pull/48067
  - https://github.com/stablyai/orca/pull/47979
  - https://github.com/stablyai/orca/issues/47797
  - https://github.com/stablyai/orca/commit/0b7fe2f6f10
  - https://github.com/stablyai/orca/pull/49244
  - https://github.com/stablyai/orca/pull/49178
  - https://github.com/stablyai/orca/pull/49206
  - https://github.com/stablyai/orca/pull/49202
  - https://github.com/stablyai/orca/pull/49168
  - https://github.com/stablyai/orca/pull/49149
  - https://github.com/stablyai/orca/pull/49124
  - https://github.com/stablyai/orca/pull/49128
  - https://github.com/stablyai/orca/pull/49132
  - https://github.com/stablyai/orca/pull/49123
  - https://github.com/stablyai/orca/pull/49129
  - https://github.com/stablyai/orca/pull/49121
  - https://github.com/stablyai/orca/pull/49130
  - https://github.com/stablyai/orca/pull/49336
  - https://github.com/stablyai/orca/pull/49290
  - https://github.com/stablyai/orca/pull/49356
  - https://github.com/stablyai/orca/pull/49355
  - https://github.com/stablyai/orca/issues/49412
  - https://github.com/stablyai/orca/issues/49404
  - https://github.com/stablyai/orca/issues/49301
  - https://github.com/stablyai/orca/issues/44947
  - https://github.com/stablyai/orca/pull/49497
  - https://github.com/stablyai/orca/pull/49516
  - https://github.com/stablyai/orca/pull/49523
  - https://github.com/stablyai/orca/pull/49535
  - https://github.com/stablyai/orca/pull/49512
  - https://github.com/stablyai/orca/issues/49645
  - https://github.com/stablyai/orca/issues/49510
  - https://github.com/stablyai/orca/issues/49505
---

# Leitura antecipada e preservação de skills no arranque e nos plugins

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#47979`](https://github.com/stablyai/orca/pull/47979),
[`stablyai/orca#47895`](https://github.com/stablyai/orca/pull/47895) (commit `0b7fe2f6f10`),
além da issue [`stablyai/orca#47797`](https://github.com/stablyai/orca/issues/47797),
[`stablyai/orca#47582`](https://github.com/stablyai/orca/pull/47582),
[`stablyai/orca#47158`](https://github.com/stablyai/orca/pull/47158),
[`stablyai/orca#47154`](https://github.com/stablyai/orca/pull/47154),
[`stablyai/orca#47019`](https://github.com/stablyai/orca/pull/47019) (resolve Issue [`#47018`](https://github.com/stablyai/orca/issues/47018)),
[`stablyai/orca#46756`](https://github.com/stablyai/orca/pull/46756) (refs Issue [`#46706`](https://github.com/stablyai/orca/issues/46706)),
[`stablyai/orca#46724`](https://github.com/stablyai/orca/pull/46724),
[`stablyai/orca#46747`](https://github.com/stablyai/orca/pull/46747) (resolve Issue [`#46708`](https://github.com/stablyai/orca/issues/46708)),
[`stablyai/orca#46751`](https://github.com/stablyai/orca/pull/46751) (resolve Issue [`#46713`](https://github.com/stablyai/orca/issues/46713)),
[`stablyai/orca#46749`](https://github.com/stablyai/orca/pull/46749) (resolve Issue [`#46698`](https://github.com/stablyai/orca/issues/46698)),
[`stablyai/orca#46718`](https://github.com/stablyai/orca/pull/46718) (resolve Issue [`#46701`](https://github.com/stablyai/orca/issues/46701)),
[`stablyai/orca#46217`](https://github.com/stablyai/orca/pull/46217),
[`stablyai/orca#46405`](https://github.com/stablyai/orca/pull/46405) (resolve Issue [`#46403`](https://github.com/stablyai/orca/issues/46403)),
[`stablyai/orca#45822`](https://github.com/stablyai/orca/pull/45822),
[`stablyai/orca#45966`](https://github.com/stablyai/orca/pull/45966) (resolve Issue [`#45965`](https://github.com/stablyai/orca/issues/45965)),
[`stablyai/orca#43436`](https://github.com/stablyai/orca/pull/43436),
[`stablyai/orca#42472`](https://github.com/stablyai/orca/pull/42472) (resolve Issue [`#42408`](https://github.com/stablyai/orca/issues/42408)),
[`stablyai/orca#40812`](https://github.com/stablyai/orca/pull/40812),
[`stablyai/orca#40788`](https://github.com/stablyai/orca/pull/40788) (resolve Issue [`#40785`](https://github.com/stablyai/orca/issues/40785)),
[`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) (resolve Issue [`#40181`](https://github.com/stablyai/orca/issues/40181)),
[`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220),
[`stablyai/orca#36897`](https://github.com/stablyai/orca/pull/36897),
[`stablyai/orca#37659 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37659) e
[`stablyai/orca#19680`](https://github.com/stablyai/orca/pull/19680), além das issues
[`stablyai/orca#47785`](https://github.com/stablyai/orca/issues/47785),
[`stablyai/orca#47813`](https://github.com/stablyai/orca/issues/47813),
[`stablyai/orca#43418`](https://github.com/stablyai/orca/issues/43418),
[`stablyai/orca#41017`](https://github.com/stablyai/orca/issues/41017),
[`stablyai/orca#14690`](https://github.com/stablyai/orca/issues/14690),
[`stablyai/orca#37875`](https://github.com/stablyai/orca/issues/37875) e
[`stablyai/orca#32573`](https://github.com/stablyai/orca/issues/32573).

## O problema

1. **Lentidão na varredura de skills (`#35220`):** o processo principal lia uma pasta de skill por vez de forma
   sequencial (`src/main/skills/skill-root-file-walk.ts`). Quando o host está ocupado e há múltiplas árvores de skills e
   cache de plugins, a varredura chega a levar mais de 30 segundos.
2. **Perda de descoberta no arranque (`#36897`):** a confirmação de status após o startup descartava ou refazia a
   descoberta inicial de skills.
3. **Colisão de nomes no seletor `/` (`#19680`) e colisão com skills empacotadas (`#37659 (MERGED no upstream; não está no fork)`):** skills vindas de plugins
   perdiam o namespace `plugin:skill` nos pickers de comando `/`; além disso, a skill bundled `computer use` colidia com
   ferramentas externas de mesmo nome.
4. **Falta de ponto de contribuição para subagentes e skills em plugins (`#37875`, `#32573`):** plugins modernos
   (ex.: ecossistemas de Claude Code e Cursor) empacotam definições de subagentes (`agents/*.md`) junto às suas skills,
   disparando-os pelo nome de tipo do subagente. No runtime do app, `contributes` não aceitava subagentes nem entregava
   skills completas, quebrando plugins que delegam tarefas a subagentes específicos.
5. **Classificação falsa de bundled skills como editadas na presença de arquivos sidecar (`#40214`, resolve `#40181`):**
   Skills empacotadas distribuem apenas `SKILL.md`. O algoritmo de classificação em `bundled-skill-classification.ts` tratava
   o arquivo como atual ou lançado apenas quando `SKILL.md` era a única entrada na pasta. Como ferramentas como Codex geram
   arquivos auxiliares no mesmo diretório (ex.: `agents/openai.yaml` ou scripts locais), o digest do diretório não batia e um
   `SKILL.md` idêntico em bytes passava a ser classificado como `edited`, impedindo atualizações silenciosas automáticas.
6. **Inconsistência no hash de identidade de pacotes de skills por caminhos não ordenados (`#40812`):**
   O cálculo de identidade de pacotes de skills gerava hashes discrepantes para o mesmo conjunto de arquivos dependendo
   da ordem em que o sistema de arquivos retornava os manifestos, disparando alertas falsos de "skill out of date" e invalidações espúrias de cache.
7. **Omissão de dicas de argumentos (argument-hints) de skills no seletor do Native Chat (`#40788`, resolve `#40785`):**
   Ao abrir o picker `/` no chat para invocar uma skill (ex.: `/review`, `/test`), a interface descartava os metadados de
   `argument-hint` definidos no Claude Code, deixando o usuário sem saber quais parâmetros a ferramenta esperava.
8. **Cache infinito do picker impedindo descoberta de novas skills instaladas (`#41017`):**
   O hook `useNativeChatSkills` armazenava o resultado de varreduras bem-sucedidas em `paneDiscoveryCache` sem tempo de expiração
   nem invalidação ao reabrir o seletor. Quando uma nova skill era instalada ou linkada simbolicamente em `~/.agents/skills/`,
   o chat existente continuava afirmando que a ferramenta não existia até a reinicialização da janela do app.
9. **Falso aviso "Needs attention · You edited this copy" em skills embutidas renomeadas (`#42472`, resolve `#42408`):**
   A renomeação de skills bundled (como `orca-computer-use` vs `computer-use`) fazia o verificador de integridade comparar o nome da pasta com o catálogo antigo de lançamentos. Como o identificador divergia, o app disparava falsos alertas de "You edited this copy", ocultava atualizações limpas e não informava qual arquivo ou caminho havia supostamente sido modificado.
10. **Descarte de escopos de skills no seletor `/` do Native Chat (`#43436`):**
    Ao filtrar e selecionar skills pelo menu de barra (`/`) no chat nativo, os escopos associados (projeto, workspace ou usuário)
    eram descartados na transição para o input do chat, impedindo que a execução resolvesse a localização correta da skill.
11. **Falha na instalação por discrepância entre nome no registro bundled e repositório comunitário (`#43418`):**
    O comando `skills install` falhava ao tentar instalar `computer-use` porque o catálogo interno usava o nome curto,
    enquanto o repositório comunitário hospeda sob `orca-computer-use`, tornando a instalação impossível via CLI.
12. **Fragmentação de pastas de skills entre múltiplos agentes gerenciados (`#45822`):**
    Cada agente mantinha suas próprias skills em diretórios isolados (`.claude/skills`, `.agents/skills`), forçando duplicação de instruções e dificultando a reutilização de ferramentas compartilhadas quando o usuário alternava entre agentes no mesmo projeto ou adicionava skills de templates e links.
13. **Falha de empacotamento ao compartilhar skills cujo diretório de origem é um alias simbólico (`#45966`, resolve `#45965`):**
    O pipeline `stageSkill` copiava links simbólicos mantendo-os literais (`verbatimSymlinks`). Quando a pasta raiz da skill era um alias relativo de provedor, a cópia gerava links quebrados (*dangling symlinks*) em sistemas POSIX (`ENOENT`) ou falhava por falta de privilégios de symlink no Windows (`EPERM`).
14. **Skills consideradas desatualizadas falsamente quando agentes gravam arquivos adicionais na pasta (`#46217`):**
    Quando agentes (como Codex) geram arquivos locais ao lado de `SKILL.md` (por exemplo `agents/openai.yaml`), a verificação de frescor julgava a pasta inteira em vez do `SKILL.md` oficial, disparando alertas falsos de desatualização e corrompendo a resolução de cópias anteriores.
15. **Perda de formatação e sumiço de skills de conta Claude no menu `/` após o primeiro turno (`#46405`, resolve `#46403`):**
    O Claude Code lista skills de conta como `<name>` nos descritores de inicialização, mas passa a reportá-las como `anthropic-skills:<name>` no stream do sistema. Após o primeiro turno, o catálogo adotava o nome com namespace, perdendo descrição e dicas de argumentos, e jogando a skill para o final do menu `/`.
16. **Queda total de skills conhecidas diante de falha transitória de I/O na raiz de skills (`#46756`, refs `#46706`):**
    Quando a leitura da raiz de skills encontrava erros temporários de permissão ou I/O (`EACCES`, `EIO`, `EPERM`) em `stat`, `realpath` ou `readdir`, o sistema tratava a raiz como inexistente ou vazia, purgando instantaneamente todas as skills previamente carregadas da memória.
17. **Avisos contínuos de skills duplicadas no Gemini CLI por instalações redundantes (`#46724`):**
    O Gemini CLI lê tanto `~/.gemini/skills` quanto `~/.agents/skills` e emite alertas em cada inicialização caso o mesmo nome apareça em ambos. O aplicativo duplicava a instalação nos dois diretórios.
18. **Ignoramento de flags `--dry-run` com formato `--dry-run=true` em comandos de skills (`#46747`, resolve `#46708`):**
    A checagem estrita `=== true` no parser de flags ignorava `--dry-run=true` (tratada como string `'true'`), executando a instalação/atualização real em vez de exibir a prévia simulada.
19. **Instalação incorreta ou silenciosa em seletores incompatíveis de `plugin install` (`#46751`, resolve `#46713`):**
    O comando `plugin install` descartava silenciosamente `--ref` em IDs de catálogo ou pastas locais, e `--catalog` em pastas de plugins, instalando versões ou origens não solicitadas pelo usuário em vez de rejeitar argumentos inválidos.
20. **Saída com código 0 em falhas parciais de `plugin update --all` (`#46749`, resolve `#46698`):**
    Quando um ou mais plugins falhavam na atualização em lote via `plugin update --all`, a CLI imprimia as linhas de sucesso e retornava código 0, impossibilitando que scripts de automação e CI detectassem falhas.
21. **Descarte indevido de comandos atualizados ao descartar registros antigos (`#46718`, resolve `#46701`):**
    Em `commands.register`, o descarte de uma inscrição de comando anterior apagava o identificador do comando incondicionalmente, removendo também a nova implementação registrada para o mesmo ID.
22. **Omissão de skills do Prime Agent mantidas no diretório do projeto (`#47019`, resolve `#47018`):**
    O Prime Agent carrega skills específicas do repositório a partir de `<repo>/.prime/agent/skills`. O scanner do aplicativo varria apenas a raiz global `~/.prime/agent/skills` e a pasta padrão `.agents/skills`, deixando invisíveis skills mantidas estritamente na pasta do projeto do Prime Agent.
23. **Exibição indevida de skills de `~/.agents/skills` no menu `/` do Claude Code (`#47582`):**
    O Claude Code carrega apenas suas próprias pastas `.claude` e plugins instalados, ignorando as raízes compartilhadas `.agents/skills`. Contudo, o resolver tratava raízes com owner nulo como visíveis a todos os agentes, fazendo com que o menu `/` do Claude oferecesse skills que só existiam em `~/.agents/skills`, cujo envio falhava como comando desconhecido.
24. **Ambiguidade em atualizações de skills bundled divergentes e destino de backups (`#47158`):**
    Quando uma skill empacotada diferia da versão distribuída pelo app, o diálogo de atualização e o CLI não deixavam claro o que o botão "Replace" ou `--force` fazia, gerando receio de perda irreversível de customizações locais.
25. **Degradação de performance com re-varredura exaustiva de dezenas de milhares de arquivos no diálogo de Share (`#47154`):**
    Cada tick ou seleção de checkbox no diálogo de compartilhamento de bots disparava uma varredura completa do disco em cada projeto vinculado, lendo cada `SKILL.md` e executando mais de 32.800 chamadas `lstat` para 64 skills, congelando a interface.
26. **Invocação de skills restritas a usuários por workers disparados via spec (`#47785`):**
    Bots agendados que iniciam workers com `orchestration worker-start --spec-file` não conseguiam disparar skills marcadas com `disable-model-invocation: true`, pois a restrição impedia a execução mesmo quando explicitamente instruída pela especificação da automação.
27. **Gravação de fluxos no navegador embutido para síntese assistida de skills (`#47813`):**
    Automações repetitivas na web (download de faturas, preenchimento de formulários) demandavam tentativa e erro descritiva pelos bots; a issue propõe gravar a sessão de navegação no browser do Orca e sintetizar automaticamente uma skill reprodutível.

28. **Invalidação e inconsistência de prévias de skills em cache no diálogo Share (`#47895`, commit `0b7fe2f6f10`):**
    O cache de listagem e prévia de skills no diálogo de compartilhamento de bots não verificava se os diretórios de origem ou o build do app haviam sido alterados, exibindo metadados antigos de skills modificadas.
29. **Falha na identificação da raiz real de plugins em pacotes com `package.json` aninhados (`#47979`):**
    O localizador de pacotes interrompia a subida de diretórios no primeiro `package.json` encontrado, selecionando pastas filhas em vez da raiz verdadeira de monorrepositórios ou plugins com submódulos.
30. **Falta de integração nativa para manipulação de work items do Azure Boards (`#47797`):**
    Agentes e automações não dispunham de comandos na CLI ou skills padronizadas para leitura e atualização de itens do Azure Boards (semelhante ao suporte já existente para Jira).
31. **Barra de status desatualizada com versão antiga de CLI atualizada via terminal (`#48287`, Issue `#48270`):**
    Quando o desenvolvedor atualiza a CLI de um agente (ex.: `claude`, `codex`, `opencode`) manualmente pelo terminal integrado ou externo, o widget da barra de status continuava exibindo a versão antiga ou alerta de update pendente por não re-ler o binário após execuções no terminal.
32. **Inconsistência de strings de backup na atualização de skills (`#48245`):**
    Mensagens de log e diálogos de backup gerados durante `skill update` exibiam caminhos parciais ou strings formatadas de maneira inconsistente entre o frontend e a CLI.
33. **Revisões de segurança e confiança pendentes para skills fundamentais (`#48298`, `#48297`):**
    Auditorias de segurança para inclusão no Trust Hub das skills centrais de automação `orca-cli` (`#48298`) e `orchestration` (`#48297`) exigiam verificação estrita de permissões e ausência de escapes de sandbox.
34. **Skills de plugins ausentes no picker de comandos slash `/` antes da primeira mensagem (`#48399`):**
    Ao abrir um novo chat, a lista de sugestões de comandos `/` não incluía as skills instaladas por plugins até que o usuário enviasse o primeiro prompt, frustrando a descoberta rápida de comandos.
35. **Opacidade operacional e falta de métricas de telemetria de plugins (`#48440`):**
    Desenvolvedores e administradores não tinham visibilidade de tempos de carregamento, contagem de invocações e consumo de memória de plugins ativos.
36. **Subprocessos workers de plugins ignorando configurações corporativas de proxy (`#48426`):**
    Enquanto o app desktop respeitava variáveis de proxy HTTP/HTTPS/NO_PROXY, workers de plugins eram iniciados sem essas configurações, falhando requisições de rede em redes corporativas.
37. **Travamento silencioso quando workers de plugins falham ao inicializar (`#48422`):**
    Em caso de falha de sintaxe, dependência ausente ou crash do worker de plugin, a ferramenta ficava em estado de espera infinito sem emitir erro tipado de execução.
38. **Painéis desacoplados de plugins sem acesso ao contexto do worktree ativo (`#48421`):**
    Quando um painel de plugin era desanexado para janela própria, perdia o contexto do worktree selecionado, impedindo a execução de operações relativas ao branch.
39. **Falta de foco rápido em painéis de plugins via paleta de comandos (`#48389`):**
    Usuários precisavam usar o mouse para localizar e focar painéis de plugins específicos na interface, carecendo de atalhos no Command Palette.
40. **Diálogos de consentimento desnecessários para skills gerenciadas em instalações limpas (`#48441`, Issues `#48410`, `#48409`, `#48408`, `#48464`):**
    Skills oficiais distribuídas com o aplicativo exigiam aprovação manual em cada primeiro uso em novas instalações, prejudicando o onboarding de usuários.
41. **Status de instalação de skills executando lookups de release remotos antes de ter cópia local (`#48578`):**
    A interface de gerenciamento de skills tentava consultar repositórios remotos para checar novas releases mesmo quando a skill ainda não tinha sido clonada ou baixada localmente, travando a renderização em ambientes offline ou com firewalls.
42. **Notificação de atualização de CLI invasiva no centro da tela (`#48610`):**
    Avisos de nova versão de CLI apareciam como banners centrais bloqueantes em vez de um card sutil posicionado no canto inferior.
43. **Impossibilidade de plugins fornecerem e gerenciarem servidores MCP (`#48659`, `#48658`):**
    Plugins de terceiros não tinham ponto de extensão para registrar conexões e servidores MCP (*Model Context Protocol*), nem ferramentas de CLI para listar, migrar ou importar conexões de MCP.
44. **Vulnerabilidade a links simbólicos inseguros (cross-device symlinks) no carregamento de skills (`#48616`):**
    O validador de pacotes de skills aceitava symlinks que apontavam para fora do volume de trabalho ou para discos externos arbitrários, criando riscos de escape de sandbox.
45. **Conflito de namespaces em ferramentas registradas por múltiplos plugins MCP (`#48635`, `#48617`):**
    Quando dois plugins registravam servidores MCP com ferramentas de mesmo nome, uma sobrepunha a outra silenciosamente sem prefixação ou resolução determinística.

## O que os PRs fazem

- **Verificação local prévia antes de lookup de release em skills (`#48578`):**
  - Checa a presença da cópia física local da skill antes de disparar qualquer lookup de rede para releases upstream.
- **Card sutil de atualização de CLI no canto inferior (`#48610`):**
  - Reposiciona notificações de nova versão da CLI para um card recolhível no rodapé inferior da janela.
- **Provedor e gestão de servidores MCP por plugins (`#48659`, `#48658`):**
  - Adiciona suporte no manifesto de plugins para fornecimento de servidores MCP e comandos CLI (`mcp list`, `mcp move`, `mcp import`).
- **Recusa estrita de symlinks cross-device inseguros em skills (`#48616`):**
  - Rejeita symlinks que cruzem limites de ponto de montagem ou dispositivos físicos durante a instalação e validação de skills.
- **Resolução de namespaces e isolamento de ferramentas MCP (`#48635`, `#48617`):**
  - Aplica prefixação com o ID do plugin fornecedor nas ferramentas MCP expostas ao runtime dos agentes.
- **Carregamento antecipado de skills de plugins no picker slash `/` antes do primeiro prompt (`#48399`):**
  - Hidrata o índice de skills e comandos de plugins instalados imediatamente na montagem do chat.
- **Coleta e exposição de métricas de desempenho de plugins (`#48440`):**
  - Expõe tempos de boot, chamadas RPC e consumo de memória de workers de plugins em telemetria estruturada.
- **Propagação de variáveis de ambiente de proxy para workers de plugins (`#48426`):**
  - Herda e repassa `HTTP_PROXY`, `HTTPS_PROXY` e `NO_PROXY` para todos os subprocessos filhos e workers de plugins.
- **Emissão explícita de erro tipado de ferramenta na falha de arranque de workers (`#48422`):**
  - Interrompe a espera com erro explicativo caso o worker do plugin sofra crash prematuro ou falhe ao inicializar.
- **Injeção de contexto de worktree em painéis de plugins destacados (`#48421`):**
  - Propaga metadados de repositório, branch e worktree ativo para painéis desacoplados de plugins.
- **Comando dedicado para focar painéis de plugins na Command Palette (`#48389`):**
  - Registra ações na paleta de comandos para abrir ou focar qualquer painel de plugin instalado diretamente pelo teclado.
- **Pré-aprovação automática (pre-trust) para skills gerenciadas em instalações limpas (`#48441`):**
  - Marca skills oficiais do catálogo gerenciado como pré-confiadas em novas instalações, eliminando popups intrusivos de consentimento.
- **Releitura automática de versões de CLI na barra de status após comandos no terminal (`#48287`, resolve `#48270`):**
  - Observa saídas de comandos de atualização no terminal e invalida o cache de versão de binários na barra de status.
- **Padronização de strings e mensagens de backup em `skill update` (`#48245`):**
  - Uniformiza mensagens de substituição e caminhos de backup entre CLI e GUI.
- **Revisão de confiança e conformidade das skills `orca-cli` e `orchestration` (`#48298`, `#48297`):**
  - Estabelece checklist de segurança e conformidade para skills do Trust Hub.
- **Vinculação estrita do cache de skills do diálogo Share às pastas e build que os produziram (`#47895`, commit `0b7fe2f6f10`):**
  - Mantém o cache de skills atrelado deterministicamente às pastas e à versão de build correspondente.
- **Subida até a raiz real do pacote ultrapassando marcadores `package.json` aninhados (`#47979`):**
  - Continua a busca ascendente além de marcadores aninhados até encontrar a raiz autêntica do pacote de plugin.
- **Suporte a Azure Boards em CLI e skills (`#47797`):**
  - Especificação para leitura e alteração de work items do Azure Boards por agentes.


- **Ocultação de pastas de skills compartilhadas para o Claude (`#47582`):**
  - Introduz a flag de perfil `skipsSharedSkillFolders` para o Claude (OpenClaude/Claude Code), impedindo que o menu `/` ofereça comandos que residem apenas em `~/.agents/skills`.
- **Esclarecimento de atualizações de skills bundled e backup seguro com `--force` (`#47158`):**
  - Esclarece no diálogo e nos tooltips de Settings que a ação "Replace" move a pasta inteira modificada para uma pasta de backup antes de instalar a versão atualizada da skill, e no CLI imprime o caminho exato para onde o backup foi movido.
- **Cache de listagem de skills no diálogo de compartilhamento de bots (`#47154`):**
  - Reutiliza a listagem de skills construída na primeira montagem do diálogo Share durante a seleção de checkboxes, eliminando milhares de chamadas de disco a cada clique.

- **Descoberta de skills do Prime Agent na pasta do projeto (`#47019`, resolve `#47018`):**
  - Adiciona `.prime/agent` à lista de diretórios de skills por repositório, garantindo que `<repo>/.prime/agent/skills` seja varrido e indexado automaticamente para o Prime Agent, mantendo novas instalações direcionadas a `.agents/skills`.
- **Retenção de skills conhecidas como indisponíveis em falhas de raiz (`#46756`, refs `#46706`):**
  - Trata falhas não-ENOENT na raiz de skills lançando `SkillRootUnreadableError`, classificando a fonte como `unavailable` e mantendo em cache a última resposta válida conhecida para não perder skills.
- **Instalação unificada de skills Gemini em `~/.agents/skills` (`#46724`):**
  - Instala skills do Gemini exclusivamente no root compartilhado `~/.agents/skills`, mantendo `~/.gemini/skills` apenas para descoberta manual e aposentando cópias duplicadas antigas.
- **Validação universal de presença de flag para `--dry-run` (`#46747`, resolve `#46708`):**
  - Trata qualquer ocorrência de `--dry-run` (incluindo `--dry-run=true`) como modo preview em `skills install` e `skills update`.
- **Rejeição explícita de argumentos inválidos em `plugin install` (`#46751`, resolve `#46713`):**
  - Emite erro imediato `invalid_argument` ao receber seletores incompatíveis (`--ref` em catálogo/pasta ou `--catalog` em pasta) antes de tentar a instalação.
- **Código de erro e relatório discriminado em falhas de `plugin update --all` (`#46749`, resolve `#46698`):**
  - Retorna código 1 (ou 3 em aprovação pendente) caso algum plugin falhe no update em lote, gerando objeto `error.data.failed` com comandos de repetição específicos por plugin.
- **Descarte escopado por wrapper de comandos substituídos (`#46718`, resolve `#46701`):**
  - Associa cada registro de comando ao seu próprio wrapper único, garantindo que o descarte de um registro anterior remova o comando apenas se ele ainda for o detentor ativo daquele registro.

- **Pasta única e neutra para skills de agentes gerenciados (`#45822`):**
  - Centraliza skills em `<home>/skills/<name>/`, gerando links automáticos para `.claude/skills` e `.agents/skills` na inicialização de chats ou na troca de agentes;
  - Exibe na tela *Settings > Skills* as skills próprias do agente primeiro, rotulando claramente quais diretórios de agentes carregam cada skill e ignorando links órfãos ou duplicados.
- **Resolução de aliases com `realpath` no compartilhamento de skills (`#45966`, resolve `#45965`):**
  - Resolve caminhos de pastas de origem via `realpath` antes de copiar a skill para o staging, preservando o conteúdo real em vez de criar links simbólicos relativos quebrados, e mantendo o tratamento verbatim apenas para links internos da árvore de arquivos.
- **Julgamento de frescor de skills apenas pelo `SKILL.md` oficial (`#46217`):**
  - Julga a atualidade da skill comparando os bytes de `SKILL.md`, ignorando arquivos sidecar inseridos por agentes (como `agents/openai.yaml`), prevenindo classificações errôneas de cópia editada;
  - Mantém a exigência de pasta limpa apenas para decisões de exclusão, protegendo arquivos criados por agentes.
- **Preservação de nomes de skills de conta do Claude no menu `/` (`#46405`, resolve `#46403`):**
  - Retém a grafia desprovida de namespace (`<name>`) para skills reportadas via `anthropic-skills:<name>` no stream do sistema, mantendo a descrição, dicas de argumentos e ordenação correta no seletor de barra.
- **PR `#43436`:** retém deterministamente os escopos de cada skill (`scope`) ao selecioná-la no picker de barra (`/`) do Native Chat, mantendo o contexto de resolução intacto.
- **Issue `#43418`:** propõe alinhar o identificador do catálogo bundled (`computer-use`) com o nome canônico do repositório comunitário (`orca-computer-use`) para permitir instalação direta sem erros de resolução.
- **PR `#40812`:** ordena deterministamente os caminhos completos dos manifestos antes de computar o hash de identidade do pacote de skills, evitando discrepâncias entre sistemas de arquivos.
- **PR `#40788` (resolve `#40785`):** preserva e renderiza `argument-hint` no dropdown de seleção do Native Chat para skills do Claude Code e ferramentas de sessão.
- **PR `#40214` (resolve `#40181`):** compara o digest atual e os digests lançados especificamente para o arquivo `SKILL.md`,
  mesmo quando a pasta contém entradas adicionais. Um `SKILL.md` cujo digest não coincida com nenhum continua sendo classificado
  como `edited` apenas se o nome no frontmatter bater com a skill bundled.
- **PR `#35220`:** introduz `src/main/skills/skill-directory-read-ahead.ts`, disparando a leitura das próximas pastas
  enquanto a atual é processada e mantendo a ordem determinística; reduz o tempo de varredura de 3x a 6x.
- **PR `#36897`:** preserva a lista de skills descobertas no arranque após a confirmação de status.
- **PR `#19680`:** mantém o identificador qualificado `plugin:skill` nos seletores `/` do chat.
- **PR `#37659 (MERGED no upstream; não está no fork)`:** renomeia a skill empacotada para `orca-computer-use` na descoberta, configurações e documentação,
  mantendo links legados e aliases do CLI para evitar quebras.
- **Issues `#37875` e `#32573`:** propõem expor pontos de contribuição declarativos `skills` e `subagents` no manifesto
  do plugin para carregar arquivos de agentes e skills embutidos.
- **Issue `#41017`:** propõe limitar o snapshot em `paneDiscoveryCache` ao período em que o seletor está visível, consultando
  o runtime novamente ao reabrir o picker para detectar skills recém-instaladas sem precisar de watchers em background.
- **PR `#42472` (resolve `#42408`):** resolve nomes canônicos e aliases de skills embutidas contra o registro de digests de lançamento, reconhece symlinks e paths canônicos e exibe o caminho exato do arquivo modificado no card de aviso caso haja edição real.

## O que fazer

1. Adotar a correção de classificação de bundled skills do [`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) para não bloquear atualizações por presença de arquivos sidecar (`agents/openai.yaml`).
2. Aplicar o [`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220) (4 arquivos autocontidos em
   `src/main/skills/`) no `brza-studio`, incorporar o `#37659 (MERGED no upstream; não está no fork)` e preparar o sistema de plugins para registrar subagentes
   nativos entregues por pacotes de terceiros.
3. Adotar a ordenação determinística de caminhos no cálculo de identidade de pacotes de skills (`#40812`).
4. Exibir dicas de argumentos (`argument-hint`) no seletor de comandos/skills do chat (`#40788`).
5. Invalidar o cache do seletor de skills ao fechar ou reabrir o picker no Native Chat (`#41017`).
6. Eliminar falsos alertas de edição em skills embutidas renomeadas através da resolução de nomes canônicos e digests de lançamento (`#42472`, resolve `#42408`).
7. Preservar os escopos de contexto de cada skill ao selecioná-la no picker de barra (`/`) do Native Chat (`#43436`).
8. Harmonizar o catálogo bundled de skills (`computer-use`) com o nome no repositório comunitário (`orca-computer-use`) no CLI de instalação (`#43418`).
9. Centralizar skills de agentes gerenciados em pasta neutra `<home>/skills/<name>/` com linking automático (`#45822`).
10. Resolver aliases de provedores com `realpath` no staging de compartilhamento de skills (`#45966`, resolve `#45965`).
11. Avaliar atualidade e frescor de skills isolando o `SKILL.md` oficial de arquivos auxiliares gerados por agentes (`#46217`).
12. Preservar a grafia limpa sem prefixo de namespace para skills de conta do Claude no seletor `/` (`#46405`, resolve `#46403`).
13. Reter skills em cache marcando a raiz como `unavailable` em caso de erro temporário de I/O em vez de esvaziar catálogo (`#46756`, refs `#46706`).
14. Unificar a instalação de skills do Gemini CLI em `~/.agents/skills` sem duplicações em `~/.gemini/skills` (`#46724`).
15. Tratar qualquer formato de `--dry-run` como simulação nos comandos de skills (`#46747`, resolve `#46708`).
16. Rejeitar seletores incompatíveis ou sem valor em `plugin install` com `invalid_argument` (`#46751`, resolve `#46713`).
17. Emitir código 1 e lista de falhas por plugin em `plugin update --all` (`#46749`, resolve `#46698`).
18. Vincular registros de comandos a seus wrappers para não descartar comandos substituídos (`#46718`, resolve `#46701`).
19. Varrer e carregar skills mantidas na pasta de projeto do Prime Agent `<repo>/.prime/agent/skills` (`#47019`, resolve `#47018`).
20. Ocultar raízes de skills de `~/.agents/skills` nos seletores do Claude Code através da flag `skipsSharedSkillFolders` (`#47582`).
21. Adotar mensagens claras de backup e rotulagem neutra para cópias divergentes de skills empacotadas no diálogo de atualização e CLI (`#47158`).
22. Reutilizar a listagem em cache de skills no diálogo de compartilhamento de bots para eliminar re-varreduras com `lstat` a cada seleção (`#47154`).
23. Permitir que workers executem skills com `disable-model-invocation: true` quando invocadas explicitamente via especificação (`worker-start --spec-file`) (`#47785`).
24. Avaliar suporte a gravação de tarefas no navegador embutido para síntese assistida de skills automatizadas (`#47813`).
25. Vincular o cache de skills no diálogo Share às pastas e compilação de origem para evitar prévias defasadas (`#47895`, commit `0b7fe2f6f10`).
26. Corrigir o resolvedor de pacotes de plugins para alcançar a raiz real ultrapassando `package.json` aninhados (`#47979`).
27. Implementar comandos de CLI e skills para consulta e edição de work items do Azure Boards (`#47797`).
28. Descobrir e carregar comandos slash de extensões do Pi antes do envio da primeira mensagem (`#48026`, resolve Issue `#48023`).
29. Preservar modelos e plugins modificados do Codex durante rebuilds da cópia de configurações do WSL (`#48165`, `#48177`, refs commit `6ed63da9e1a` / `#45247`).
30. Escalonar a checagem de atualizações de CLIs de agentes após a inicialização estabilizar (`#47923`, commit `5d34df71806`).
31. Evitar falso relatório de falha no atualizador de CLI do OpenCode quando o binário já estiver atualizado (`#48183`, resolve Issue `#48028`).
32. Salvar downloads de CLI ao lado de arquivos com mesmo nome existente em vez de abortar (`#48067`, commit `30a0b6f59e7`).
33. Atualizar o cache de versão da barra de status quando CLIs forem atualizadas via terminal (`#48287`, resolve `#48270`).
34. Padronizar mensagens e rotas de backup na substituição de skills (`#48245`).
35. Adequar as skills `orca-cli` e `orchestration` às diretrizes de segurança e permissões do Trust Hub (`#48298`, `#48297`).
36. Exibir skills instaladas de plugins no autocomplete slash `/` imediatamente antes do envio da primeira mensagem (`#48399`).
37. Coletar e disponibilizar métricas de tempo de carregamento e uso de memória de workers de plugins (`#48440`).
38. Repassar variáveis de configuração de proxy (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`) para workers de plugins (`#48426`).
39. Lançar erro tipado de execução quando um worker de plugin falhar ao subir (`#48422`).
40. Fornecer contexto de worktree ativo para painéis de plugins desanexados (`#48421`).
41. Adicionar comando na Command Palette para focar diretamente painéis de plugins (`#48389`).
42. Conceder pré-confiança (pre-trust) a skills gerenciadas do sistema em novas instalações limpas (`#48441`).
43. Checar disponibilidade local de skills antes de consultar releases na rede (`#48578`).
44. Adotar card compacto de atualização de CLI no rodapé (`#48610`).
45. Suportar registro e gestão de servidores MCP diretamente por plugins (`#48659`, `#48658`).
46. Rejeitar links simbólicos cross-device inseguros em pacotes de skills (`#48616`).
47. Isolar ferramentas de servidores MCP com prefixo de namespace do plugin (`#48635`, `#48617`).
48. Executar servidor de comando compartilhado uma única vez no host para todas as sessões de agentes (`#48770`).
49. Disponibilizar os servidores MCP do host para todos os chats nativos com grupo Orca em `/mcp` (`#48707`).
50. Espelhar servidores MCP do Orca nos arquivos de configuração do Grok, Cursor e Droid (`#48778`).
51. Reiniciar chats em execução automaticamente ao alterar a lista de servidores MCP do host (`#48785`).
52. Nomear entradas de arquivos MCP do Orca com hash único de sua pasta de dados (`#48805`).
53. Tratar overrides `-c mcp_servers` do Codex em argumentos de agentes como nomes reservados (`#48789`).
54. Ajustar cancelProblems para liberar apenas o interesse do chamador em checagens compartilhadas de diagnósticos (`#48796`).
55. Embutir o SDK do MCP no binário `orca mcp connect` para empacotamento autocontido (`#48819`).
56. Gerenciar servidores MCP do host remotamente a partir de dispositivos móveis pareados (`#48776`).
57. Disponibilizar instaladores de um clique para aplicativos MCP (ClickUp, Airtable, Todoist, Zapier) (`#48713`).
58. Carregar skills criadas com symlinks na pasta `skills/` de bots e plugins corporativos do Claude Code (`#48777`).
59. Configurar servidores MCP em Repository settings com chave seletora host-servers em Tools (`#48940`).
60. Disponibilizar servidores MCP do Orca para Codex, Copilot, Amp e Pi executando em WSL (`#48923`).
61. Fornecer servidores MCP com variáveis de ambiente seguras e repassados por relay para terminais WSL (`#48898`).
62. Conectar líderes e membros de equipes de agentes do Claude aos servidores MCP do host (`#48895`).
63. Adicionar página de configurações para servidores MCP de cada host com suporte a adicionar servidores (`#48844`).
64. Disponibilizar os servidores MCP do host para terminais de agentes com `orca mcp exec` e prompt de reinício (`#48814`).
65. Retentar carregamento de arquivo de plugin após timeout transitório de transpilação (`#48910`).
66. Ajustar documentação corrigindo o nome oficial e chamada da skill `orca-computer-use` (`#49047`).
67. Encaminhar decisões de `agent.tool.before` (deny/rewrite) no Windows para o `PreToolUse` do Claude Code (`#49004`).
- Oferecer reinicialização interativa de terminais de agentes que perderam conexão com servidores MCP após reinício do Orca (`#49244`).
- Otimizar alternâncias de lista, colagens e validações de inicialização de servidores MCP para recalcular apenas o delta alterado (`#49178`).
- Compartilhar leitura de lista de hosts entre consultas concorrentes de servidores MCP compartilhados (`#49202`).
- Revalidar alcance de servidores MCP em agentes após operação de mover (`#49206`, `#49168`).
- Agrupar persistência de registros de painéis em rajadas e ler a lista de servidores uma única vez ao contar terminais obsoletos (`#49149`).
- Preservar edições concorrentes de configurações de agentes e comentários de usuários ao atualizar arquivos de servidores MCP (`#49124`, `#49130`, `#49121`).
- Otimizar consumo de leitura do cofre de credenciais e evitar releituras cíclicas da lista de hosts em servidores de comando compartilhados (`#49123`, `#49128`, `#49132`).
- Manter descoberta linear de servidores e dispensar sincronização de plugins inalterados (`#49129`).
- Disponibilizar comando `orca tab cdp` para automação ultrarrápida de abas do navegador via Chrome DevTools Protocol (`#49412`).
- Orientar agentes sandboxed no Windows a solicitar escalonamento quando a CLI do Orca for reportada como não reconhecida (`#49336`, resolve Issue `#49301`).
- Assegurar que operação Move de servidores MCP remova apenas agentes confirmados e que cópias inalteradas não recarreguem (`#49290`).
- Localizar mensagens de inspeção e criação de configurações MCP de repositório (`#49356`).
- Repassar variável `APPDATA` para workers de plugins no Windows e documentar hooks com percepção de host (`#49355`).
- Tratar subida recursiva até a raiz real de pacotes ultrapassando marcadores intermediários de `package.json` (`#47979`).
- Adicionar flag `--no-effects` na automação de navegador para omitir esperas de acomodação pós-ação (`#49404`).
- Expor identidade do chat nativo selecionado no contexto de workspace de plugins (`#44947`).
- Ocultar diretórios `__pycache__/` e arquivos `*.pyc` do menu de menção de arquivos `@` (`#49645`).
- Listar skills de projetos vinculados no menu slash de comentários de itens (`#49497`).
- Eliminar recomendação indevida de `--json` em stubs do `skills get` evitando loops de releitura na CLI (`#49516`, resolve Issue `#49510`).
- Rejeitar inclusão de blocos `[[hooks]]` no Kimi quando inviabilizarem o carregamento do `config.toml` (`#49523`, resolve Issue `#49505`).
- Encaminhar cabeçalhos completos no relay de ferramentas de agentes exceto hop-by-hop e credenciais próprias (`#49535`).
- Identificar permissões faltantes em erros 403 do Composio e oferecer ação rápida de 'Change key' (`#49512`).
