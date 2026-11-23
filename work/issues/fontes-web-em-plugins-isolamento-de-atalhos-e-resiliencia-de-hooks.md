---
status: open
description: Os PRs #47767 (links /blob/ no Git install), #47710 (parse de teclas + e , literais) e #47702 (componente CodeInput) expandem plugins e atalhos.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-07
tags:
  - tooling
  - design
---

# Fontes web em plugins, isolamento de atalhos e resiliência de hooks

Rastreado dos PRs abertos no upstream [`stablyai/orca#47767`](https://github.com/stablyai/orca/pull/47767) (resolve Issue [`#47766`](https://github.com/stablyai/orca/issues/47766)),
[`stablyai/orca#47710`](https://github.com/stablyai/orca/pull/47710) (resolve Issue [`#47709`](https://github.com/stablyai/orca/issues/47709)),
[`stablyai/orca#47702`](https://github.com/stablyai/orca/pull/47702),
[`stablyai/orca#47561`](https://github.com/stablyai/orca/pull/47561),
[`stablyai/orca#47586`](https://github.com/stablyai/orca/pull/47586),
[`stablyai/orca#42473`](https://github.com/stablyai/orca/pull/42473),
[`stablyai/orca#47296`](https://github.com/stablyai/orca/pull/47296) (refs Issue [`#47310`](https://github.com/stablyai/orca/issues/47310)),
[`stablyai/orca#47107`](https://github.com/stablyai/orca/pull/47107) (resolve Issue [`#47104`](https://github.com/stablyai/orca/issues/47104)),
[`stablyai/orca#47102`](https://github.com/stablyai/orca/pull/47102) (resolve Issue [`#47074`](https://github.com/stablyai/orca/issues/47074)),
[`stablyai/orca#47067`](https://github.com/stablyai/orca/pull/47067) (resolve Issue [`#47066`](https://github.com/stablyai/orca/issues/47066)),
[`stablyai/orca#43916`](https://github.com/stablyai/orca/pull/43916) (resolve Issue [`#43552`](https://github.com/stablyai/orca/issues/43552)),
[`stablyai/orca#43877`](https://github.com/stablyai/orca/pull/43877),
[`stablyai/orca#43876`](https://github.com/stablyai/orca/pull/43876),
[`stablyai/orca#43569`](https://github.com/stablyai/orca/pull/43569) (resolve Issue [`#42938`](https://github.com/stablyai/orca/issues/42938)),
[`stablyai/orca#43604`](https://github.com/stablyai/orca/pull/43604),
[`stablyai/orca#43389`](https://github.com/stablyai/orca/pull/43389) (resolve Issue [`#43379`](https://github.com/stablyai/orca/issues/43379)),
[`stablyai/orca#39416`](https://github.com/stablyai/orca/pull/39416),
[`stablyai/orca#39413`](https://github.com/stablyai/orca/pull/39413),
[`stablyai/orca#39407`](https://github.com/stablyai/orca/pull/39407),
[`stablyai/orca#39393`](https://github.com/stablyai/orca/pull/39393),
[`stablyai/orca#39348`](https://github.com/stablyai/orca/pull/39348) (Issue [`#15642`](https://github.com/stablyai/orca/issues/15642)) e
[`stablyai/orca#39383`](https://github.com/stablyai/orca/pull/39383).

## O problema

1. **Incapacidade de empacotar e utilizar tipografias customizadas via plugins (`#39416`):**
   Plugins temáticos, suítes de acessibilidade e extensões de código não podiam distribuir fontes web próprias para o
   terminal, editor de código ou elementos visuais da interface. Os usuários eram obrigados a instalar tipografias manualmente
   no sistema operacional do host antes de configurá-las no app, limitando a distribuição portátil de ambientes e temas.
2. **Perda de edições em painéis declarativos ao trocar rapidamente de workspace (`#39413`):**
   Painéis de plugins que salvam estados por workspace armazenavam valores na fila com base no workspace que estivesse
   ativo no momento em que a mensagem de persistência chegava ao processo de renderização. Se o desenvolvedor fizesse uma
   alteração em um painel e trocasse de workspace em menos de ~0,4s, o valor digitado era atribuído ao novo workspace e
   perdido no workspace de origem.
3. **Execução duplicada de ações nativas substituídas por plugins lentos (`#39407`):**
   Quando um plugin substitui um comando interno do aplicativo e a sua execução demora mais de 2 segundos, o app dispara a
   ação interna de fallback. Contudo, o comando do plugin continuava rodando em segundo plano e, ao tentar executar a mesma
   ação internamente via `commands.run`, fazia com que a operação fosse disparada em dobro.
4. **Bypass de segurança em hooks com recusa malformada (`#39393`):**
   Ganchos de segurança configurados como *fail-closed* (`onError: "deny"`) para auditar ou bloquear comandos perigosos no
   terminal eram ignorados se a resposta de recusa violasse o schema esperado (ex.: justificativa superior a 500 caracteres
   ou formato numérico inválido), permitindo a execução indevida do comando protegido.
5. **Atalhos de teclado de plugins bloqueados em terminais focados (`#39348`, `#15642`):**
   Atalhos globais registrados por extensões funcionavam apenas quando o foco do cursor estava fora do terminal interativo.
   Como a maior parte do trabalho ocorre com o terminal em foco, atalhos de plugins ficavam inacessíveis sem cliques adicionais.
6. **Sobrecarga de varreduras de terminais para eventos de status sem ouvintes (`#39383`):**
   A notificação de alteração de status de agentes executava um inventário completo de PTYs para cada evento enfileirado,
   mesmo após o fechamento do painel do plugin que solicitou o acompanhamento.
7. **Inviabilidade de declarar pilha ordenada de fontes fallback (fallback stack) (`#43569`, resolve `#42938`):**
   A configuração de fonte do Editor e do Terminal tratava o valor inserido como um único nome de família tipográfica.
   Não era possível passar uma lista separada por vírgula (ex.: `JetBrains Mono, Menk Qagan StdEx Tig`), impedindo posicionar fontes PUA ou alfabetos específicos à frente das fontes de símbolos Nerd embutidas.
8. **Ausência de armazenamento portátil de preferências para dotfiles (`#43604`):**
   Configurações eram armazenadas em registros de estado do Electron/Chromium, impedindo que desenvolvedores sincronizassem suas preferências de temas, fontes e atalhos entre múltiplas máquinas via repositórios de dotfiles.
9. **Cruzamento excessivo de conexões em diagramas Mermaid no Markdown preview (`#43552`):**
   Diagramas de arquitetura, fluxo e entidades relacionais com mais de 15 nós renderizavam de forma emaranhada no preview sob o motor padrão Dagre, sem que o engine alternativo ELK (`layout: elk`) estivesse registrado.
10. **Re-pedidos contínuos de aprovação de hooks do Codex no Windows por grafia de separador (`#43877`):**
    No Windows, o Orca gravava as chaves de confiança de hooks com ambas as grafias de separador (barra invertida `\` e barra normal `/`). O Codex consultava apenas a grafia com barra invertida em `hooks.json`, fazendo com que hooks já aprovados fossem solicitados novamente a cada novo lançamento de agente.
11. **Substituição silenciosa de links simbólicos CLI entre instâncias do Orca (`#43876`):**
    Ao executar `orca register` ou clicar em "Install CLI", se outra instalação ou versão em desenvolvimento do app já tivesse registrado o link `/usr/local/bin/orca`, a substituição ocorria sem aviso de qual aplicação anterior detinha o vínculo.
12. **Desalinhamento vertical de rótulos em RadioGroup e Checkbox declarativos de plugins (`#47102`, resolve `#47074`):**
    Em formulários declarativos de plugins, os controles de 16px (círculo de rádio ou caixa de seleção) ficavam posicionados 2px abaixo em linhas com `items-start`, enquanto o texto do rótulo utilizava `leading-none` com line-box de 14px, centralizando o texto cerca de 3px acima do centro geométrico do controle visual.
13. **Falhas EPERM e criação de links mutáveis ao instalar plugins locais a partir de diretórios com junção ou symlink (`#47067`, resolve `#47066`):**
    Ao instalar um plugin local apontando para uma pasta acessada por symlink ou junction no Windows, o processo de cópia repassava a raiz não resolvida para `cp({ verbatimSymlinks: true })`, recriando o diretório de versão como um link (gerando erro EPERM no Windows ou mantendo um link mutável no macOS/Linux).
14. **Falha na instalação de plugins a partir de URLs do Codeberg, Gitea e Forgejo com ref (`#47107`, resolve `#47104`):**
    Ao tentar instalar plugins via Git usando links de repositórios hospedados no Codeberg ou instâncias Gitea/Forgejo apontando para branches, tags ou commits específicos (contendo caminhos `/src/branch/...`, `/src/tag/...` ou `/src/commit/...`), o instalador não reconhecia o padrão de ref, falhando na extração da URL de clone e no checkout do commit desejado.
15. **Inflexibilidade e impossibilidade de reordenar ou ocultar abas da Activity Bar (`#42473`):**
    À medida que plugins e painéis adicionavam novos ícones à Activity Bar, o usuário não dispunha de opções para reordenar por drag-and-drop, ocultar abas secundárias ou navegar por itens agrupados em overflow ("More").
16. **Truncamento incorreto de branches com hífen na instalação de plugins via Git (`#47296`, refs `#47310`):**
    URLs do GitHub ou Codeberg com branches ou caminhos contendo `-` (como `/tree/feature/-/example`) eram interpretadas de forma errônea como o separador `/-/` do GitLab, cortando o nome do repositório prematuramente e descartando o ref.
17. **Declaração quebrada de CSS ao configurar listas de famílias de fontes separadas por vírgula (`#47561`):**
    Ao configurar famílias tipográficas com fallbacks no terminal ou no app (como `D2Coding, Consolas` ou `"Cascadia Mono", D2Coding`), o valor era envolto em um único par de aspas (`"D2Coding, Consolas"`). O motor de renderização CSS interpretava a string inteira como um único nome inexistente de fonte, quebrando a declaração e descartando os fallbacks.
18. **Atalhos de teclado (Cmd+W e Cmd+T) fechando e abrindo abas ocultas enquanto páginas como Settings estão abertas (`#47586`):**
    Como o workbench permanece montado por trás de telas de sobreposição completa (Settings, Activity, tela de criação de worktree), seu ouvinte de eventos de teclado continuava ativo. Pressionar Cmd+W fechava inadvertidamente a aba ativa oculta (interrompendo o agente em execução) e Cmd+T criava abas invisíveis ao usuário.
19. **Falha de alcance ao colar links de arquivos (`/blob/`) no assistente de instalação Git de plugins (`#47767`, resolve `#47766`):**
    Ao colar URLs de páginas de arquivos de repositórios no GitHub ou Gitea/Codeberg (como `https://github.com/owner/repo/blob/main/README.md`) no campo de instalação Git de plugins, o instalador mantinha o caminho inteiro da página como a URL do repositório, falhando na verificação de acessibilidade Git.
20. **Rejeição de teclas `+` e `,` literais em atalhos e listas de keybindings (`#47710`, resolve `#47709`):**
    Combinações de teclado contendo a tecla mais literal (como `Mod++`) ou listas de atalhos contendo vírgula literal (como `Ctrl+,`) eram sumariamente rejeitadas como inválidas pelo parser, porque `+` e `,` são utilizados internamente como separadores de acorde e de lista.

## O que o upstream implementa

- **Reconhecimento de URLs de arquivos `/blob/` como o repositório base no instalador Git de plugins (`#47767`, resolve `#47766`, commit `63930784bb2`):**
  - O utilitário `ownerRepoPageRef` agora lê `/owner/repo/blob/...` como o repositório `owner/repo` em forges públicas (GitHub e Gitea), omitindo ref implícito quando contém barras e mantendo `#ref` explícito para versionamento fixo, com orientações amigáveis no erro de URL inválida.
- **Parser de atalhos e keybindings com suporte a teclas `+` e `,` literais (`#47710`, resolve `#47709`, commit `c73dce43060`):**
  - Lê um `+` consecutivo após o separador como a tecla literal Plus (ex.: `Mod++`) e reconecta partes vazias após o separador `+` como a tecla Comma (ex.: `Ctrl+,`), mantendo compatibilidade com plugins legados que declaram `Plus`.
- **Componente `CodeInput` para painéis declarativos de componentes de plugins (`#47702`):**
  - Introduz o campo editável `CodeInput` para plugins, suportando syntax highlighting, numeração de linhas e edição estruturada de código em painéis de componentes.
- **Tratamento de configurações de fontes separadas por vírgula como lista tipográfica real (`#47561`):**
  - Divide a configuração de fontes em vírgulas, remove aspas espúrias de cada item, aplica aspas individuais apenas em famílias que não sejam palavras-chave CSS (como monospace ou sans-serif) e constrói declaração CSS válida com fallbacks funcionais.
- **Supressão de atalhos de abas quando telas cheias (Settings ou Activity) ocultam o workspace (`#47586`):**
  - Executa o handler de atalhos de teclado de abas (como Cmd+W e Cmd+T) estritamente quando a visão do workspace estiver visível, impedindo o fechamento ou criação acidental de abas invisíveis.
- **Reordenação, ocultação e agrupamento 'More' de abas da Activity Bar (`#42473`):**
  - Implementa suporte a arrastar e soltar (drag-and-drop) para reorganizar abas na Activity Bar, opções Hide, Move e Reset no menu de contexto, e agrupamento inteligente em menu "More" com retenção de foco acessível.
- **Parsing resiliente de refs contendo hífen para GitHub e Codeberg (`#47296`, refs `#47310`):**
  - Garante que caminhos contendo segmentos `-` continuem sendo lidos como parte legítima do ref em forges públicas (GitHub, GHE, Codeberg), preservando a regra de corte de `/-/` estritamente para o GitLab.
- **Reconhecimento de links de ref do Codeberg, Gitea e Forgejo no instalador Git (`#47107`, resolve `#47104`):**
  - Faz o parse de URLs contendo rotas `/src/{branch,tag,commit}/<ref>`, extraindo a URL base de clone e o ref correspondente para instalação correta de plugins a partir dessas plataformas.
- **Alinhamento centrado de rótulos com variante `control` em formulários de plugins (`#47102`, resolve `#47074`):**
  - Introduz a variante `control` para o componente `Label` com line-box de 20px, garantindo alinhamento perfeito do centro da primeira linha de texto com o círculo de rádio e checkbox, inclusive com quebra de linha.
- **Resolução de diretório canônico via `realpath` no staging de instalação de plugins (`#47067`, resolve `#47066`):**
  - Resolve a raiz de staging com `realpath` antes de copiar a árvore de arquivos do plugin, mantendo a cópia literal apenas para itens internos e prevenindo links simbólicos de raiz mutáveis ou erros EPERM.
- **Distribuição segura de fontes tipográficas via manifesto de plugins (`#39416`):**
  - Adiciona o campo `fonts` na especificação de plugins, permitindo declarar arquivos WOFF2 seguros com limite de 2 MB
    por arquivo e 8 MB por família;
  - Sanitiza as fontes na instalação, valida assinaturas de arquivos binários contra WOFF2 corrompidos ou disfarçados e
    serve via protocolo com cabeçalhos CORS/ACAO adequados;
  - Integração no seletor de fontes do terminal, Monaco Editor e interface geral com remensuração automática de glifos.
- **Rastreamento de hidratação de estado em painéis declarativos (`#39413`):**
  - Numera as mensagens `ui.hydrate` e vincula o identificador do workspace a cada pacote `ui.persist`;
  - Descarrega alterações pendentes no cliente antes de carregar o novo contexto e descarta persistências para hidratações
    desconhecidas, garantindo que edições fiquem estritamente no workspace onde foram digitadas.
- **Controle centralizado de deadline para comandos substituídos (`#39407`):**
  - Move a gestão do limite de 2 segundos para o processo principal (`main`), que recusa invocações tardias de `commands.run`
    do comando substituído após o fallback nativo já ter sido acionado.
- **Aplicação estrita de recusa em hooks fail-closed (`#39393`):**
  - Trata qualquer resposta malformada de um participante com `onError: "deny"` como falha fatal e bloqueia a ação protegida.
- **Ativação de atalhos de plugins no terminal sob a política do app (`#39348`):**
  - Estende os comandos de plugins para o contexto do terminal, respeitando a política configurada de precedência de teclas
    (*Orca first* / *terminal first*) e permitindo remapeamento livre pelo usuário.
- **Descarte de inventários órfãos de terminais (`#39383`):**
  - Cancela varreduras caras de PTYs se o painel ou ouvinte do plugin tiver sido fechado antes do processamento da fila.

- **Precedência de variáveis de ambiente em hooks de lançamento de agentes (`#43389`, resolve `#43379`):**
  - Ajusta o ciclo de vida do gancho `agent.launch.before` para que as variáveis de ambiente personalizadas injetadas pelo plugin sejam mescladas após o ambiente da conta do host (`host account env`), assegurando que overrides de plugins (como proxies corporativos, tokens de roteamento ou chaves de sandbox) tenham precedência efetiva sobre defaults de conta.
- **Pilha de fontes fallback separadas por vírgula no Editor e Terminal (`#43569`, resolve `#42938`):**
  - Passa a interpretar a configuração de fonte como uma pilha ordenada com fallbacks sucessivos, viabilizando fontes regionais e PUA sem perder compatibilidade com Nerd Fonts.
- **Preferências portáteis em `~/.orca/settings.json` (`#43604`):**
  - Implementa leitura no arranque e persistência bidirecional contínua de configurações em arquivo plano JSON portátil, simplificando a replicação de ambiente via dotfiles (chezmoi, nix, stow).
- **Suporte ao motor de layout ELK para diagramas Mermaid (`#43916`, resolve `#43552`):**
  - Empacota o Mermaid 11.4+ e carrega assincronamente o pacote `@mermaid-js/layout-elk` para renderizar diagramas complexos no preview com a diretiva `layout: elk`, reduzindo cruzamento de arestas e melhorando a hierarquia visual.
- **Normalização de chaves de hooks do Codex no Windows (`#43877`):**
  - Ajusta `readHookTrustTables` para permitir que a grafia com barra invertida (`\`) lida pelo Codex defina os estados `trusted_hash` e `enabled` sobre variantes com barra normal, eliminando pedidos redundantes de re-aprovação.
- **Aviso na substituição de links simbólicos CLI (`#43876`):**
  - Notifica claramente o desenvolvedor ao executar o registro da CLI (`orca register`) se o link apontava anteriormente para outra instalação ou compilação de desenvolvimento do aplicativo.

## O que fazer

- Suportar pilha ordenada de fontes fallback separadas por vírgula no Editor e Terminal (`#43569`, resolve `#42938`).
- Adotar leitura e escrita de preferências portáteis em `~/.orca/settings.json` para facilitar gestão via dotfiles (`#43604`).
- Habilitar o motor de layout Mermaid ELK no preview de Markdown para diagramas complexos (`#43916`, resolve `#43552`).
- Normalizar chaves de confiança de hooks do Codex no Windows para evitar re-aprovações redundantes (`#43877`).
- Notificar substituição de symlinks na instalação da CLI (`#43876`).
- Aplicar o ambiente de `agent.launch.before` dos plugins após as variáveis de ambiente da conta do host (`#43389`, resolve `#43379`).
- Incorporar o suporte a fontes tipográficas em plugins (`#39416`) no `brza-studio`.
- Adotar o rastreamento por `hydrationId` em formulários declarativos de plugins (`#39413`).
- Aplicar as proteções de concorrência em substituição de comandos (`#39407`) e negação fail-closed em hooks (`#39393`).
- Habilitar o disparo de atalhos de plugins dentro de terminais ativos (`#39348`).
- Utilizar a variante `control` para centralizar verticalmente labels de RadioGroup e Checkbox em plugins (`#47102`, resolve `#47074`).
- Resolver o caminho real com `realpath` no staging de instalação de plugins para evitar symlinks mutáveis ou falhas EPERM (`#47067`, resolve `#47066`).
- Reconhecer e tratar rotas `/src/...` de repositórios Codeberg, Gitea e Forgejo na instalação de plugins via Git (`#47107`, resolve `#47104`).
- Permitir reordenar, ocultar e agrupar em 'More' as abas da Activity Bar via drag-and-drop e menu (`#42473`).
- Preservar refs contendo segmentos `-` ao analisar URLs de instalação Git de plugins no GitHub e Codeberg (`#47296`, refs `#47310`).
- Tratar configurações de fontes com vírgula como lista tipográfica dividida e com aspas individuais (`#47561`).
- Ignorar atalhos de gerenciamento de abas (Cmd+W, Cmd+T) quando telas como Settings ocultarem o workspace (`#47586`).
- Reconhecer URLs de arquivos `/blob/` no instalador Git de plugins derivando o repositório correto (`#47767`, resolve `#47766`).
- Suportar teclas `+` e `,` literais em combinações de atalhos e keybindings (`#47710`, resolve `#47709`).
- Adotar o componente `CodeInput` em painéis de componentes de plugins (`#47702`).




