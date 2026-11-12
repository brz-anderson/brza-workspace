---
status: open
description: Os PRs #41642, #41635, #41359, #41333, #41337 trazem galeria lightbox de imagens no chat, confirmação Enter em cards e prévia de PRs.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-06
tags:
  - chat
  - tooling
---

# Cartões de Pull Request, feedback de Steer e atalhos no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#41642`](https://github.com/stablyai/orca/pull/41642) (resolve Issue [`#41641`](https://github.com/stablyai/orca/issues/41641)),
[`stablyai/orca#41635`](https://github.com/stablyai/orca/pull/41635),
[`stablyai/orca#41359`](https://github.com/stablyai/orca/pull/41359),
[`stablyai/orca#41333`](https://github.com/stablyai/orca/pull/41333) (resolve Issue [`#37005`](https://github.com/stablyai/orca/issues/37005)),
[`stablyai/orca#41337`](https://github.com/stablyai/orca/pull/41337) (resolve Issue [`#41134`](https://github.com/stablyai/orca/issues/41134) / STA-14852),
[`stablyai/orca#41212`](https://github.com/stablyai/orca/pull/41212) (resolve Issue [`#41211`](https://github.com/stablyai/orca/issues/41211)),
[`stablyai/orca#41224`](https://github.com/stablyai/orca/pull/41224) (resolve Issue [`#41217`](https://github.com/stablyai/orca/issues/41217)),
[`stablyai/orca#41180`](https://github.com/stablyai/orca/pull/41180) (resolve Issue [`#41178`](https://github.com/stablyai/orca/issues/41178)),
[`stablyai/orca#41242`](https://github.com/stablyai/orca/pull/41242),
[`stablyai/orca#41099`](https://github.com/stablyai/orca/pull/41099) (resolve Issue [`#41097`](https://github.com/stablyai/orca/issues/41097)),
[`stablyai/orca#41100`](https://github.com/stablyai/orca/pull/41100),
[`stablyai/orca#40823`](https://github.com/stablyai/orca/pull/40823) (resolve Issue [`#40819`](https://github.com/stablyai/orca/issues/40819)),
[`stablyai/orca#40820`](https://github.com/stablyai/orca/pull/40820),
[`stablyai/orca#39287`](https://github.com/stablyai/orca/pull/39287) (Issue [`#39286`](https://github.com/stablyai/orca/issues/39286)),
[`stablyai/orca#39309`](https://github.com/stablyai/orca/pull/39309),
[`stablyai/orca#39369`](https://github.com/stablyai/orca/pull/39369),
[`stablyai/orca#39050`](https://github.com/stablyai/orca/pull/39050) (Issue [`#37855`](https://github.com/stablyai/orca/issues/37855)),
[`stablyai/orca#39141`](https://github.com/stablyai/orca/pull/39141),
[`stablyai/orca#38877`](https://github.com/stablyai/orca/pull/38877),
[`stablyai/orca#38848`](https://github.com/stablyai/orca/pull/38848),
[`stablyai/orca#38892`](https://github.com/stablyai/orca/pull/38892),
[`stablyai/orca#38879`](https://github.com/stablyai/orca/pull/38879),
[`stablyai/orca#38883`](https://github.com/stablyai/orca/pull/38883),
[`stablyai/orca#38895`](https://github.com/stablyai/orca/pull/38895),
[`stablyai/orca#38750`](https://github.com/stablyai/orca/pull/38750),
[`stablyai/orca#38749`](https://github.com/stablyai/orca/pull/38749),
[`stablyai/orca#38727`](https://github.com/stablyai/orca/pull/38727),
[`stablyai/orca#38724`](https://github.com/stablyai/orca/pull/38724),
[`stablyai/orca#38756`](https://github.com/stablyai/orca/pull/38756),
[`stablyai/orca#38660`](https://github.com/stablyai/orca/pull/38660) e das issues
[`stablyai/orca#39516`](https://github.com/stablyai/orca/issues/39516),
[`stablyai/orca#39520`](https://github.com/stablyai/orca/issues/39520),
[`stablyai/orca#39060`](https://github.com/stablyai/orca/issues/39060),
[`stablyai/orca#38792`](https://github.com/stablyai/orca/issues/38792) e
[`stablyai/orca#38780`](https://github.com/stablyai/orca/issues/38780).

## O problema

1. **Rejeição com erro fatal ao colar capturas de tela e fotos em alta resolução (`#39050`, `#37855`):**
   Ao colar imagens grandes ou capturas de tela retina no composer do chat, a recodificação interna em PNG ultrapassava o
   limite de bytes/pixels e abortava com `Clipboard image is too large`, forçando o usuário a redimensionar a imagem manualmente
   em editores externos antes de anexar.
2. **Poluição do diário com cartões sintéticos "Ran /model" ao trocar de modelo pelo picker (`#39141`):**
   Ao trocar de modelo de IA pelo dropdown visual do composer, o app enviava o comando para o terminal e gravava um cartão
   local `Ran /model <id>` no meio da conversa. Trocas consecutivas preenchiam o histórico de chat com mensagens redundantes.
3. **Ausência de cartão estruturado quando o agente abre um Pull Request (`#38750`):**
   Ao instruir o agente a criar um PR durante uma sessão de chat, a única evidência visível era a chamada crua da ferramenta
   `gh pr create`. Faltava um cartão compacto e clicável no chat informando o número do PR, título, status e linhas `+18 −15`.
4. **Cartões de link restritos apenas ao repositório do workspace (`#38892`):**
   Quando a conversa no chat referenciava um PR ou issue de outro repositório no mesmo host (ex.: upstream de um fork), o app
   exibia apenas uma prévia genérica sem detalhes, ignorando que o token do host já tinha permissão para ler os metadados.
5. **Inércia do teclado ao tentar enviar itens da fila após interrupção (<kbd>Stop</kbd>) (`#38877`):**
   Após pressionar Stop com mensagens enfileiradas na fila de espera, a combinação <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> em um
   composer vazio não disparava o envio do primeiro cartão pausado.
6. **Envio acidental do item errado da fila ao limpar o composer (`#38848`):**
   Quando o usuário enfileirava acidentalmente uma mensagem com <kbd>Enter</kbd> e tentava enviar com <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd>
   do composer vazio, o atalho enviava a cabeça antiga da fila em vez da mensagem recém-enfileirada.
7. **Degradação de renderização no streaming de respostas com tipos genéricos (`#38879`):**
   O analisador léxico de blocos tratava menções em prosa a tipos como `Vec<T>` ou `<string>` como tags HTML brutas, forçando
   a resposta inteira a re-renderizar do início a cada novo token em vez de atualizar apenas o bloco ativo.
8. **Despertar desnecessário de todas as abas e instâncias de chat a cada evento de status (`#38883`):**
   Qualquer mudança de status em um único chat forçava a ponte de status a clonar resumos e despertar todos os chats da janela.
9. **Varredura O(N) de histórico completo na restauração de transcrições por ID de sessão (`#38895`):**
   Para localizar uma transcrição de chat ao reabrir abas, o app percorria todo o histórico de sessões em disco sequencialmente.
10. **Ambiguidade sobre o comportamento de Cmd/Ctrl+Enter em chats ocupados (`#38749`):**
    Falta de indicação sobre se Cmd/Ctrl+Enter acionaria Steer ou Queue.
11. **Falhas espúrias de timeout de 60s em inicializações lentas de agentes (`#38727`):**
    O timer rígido de startup abortava inicializações normais que demorassem mais de 60s.
12. **Atalhos globais do app bloqueados pelo foco no editor de mensagens do chat (`#38724`):**
    O composer interceptava teclas de navegação e atalhos de workspace.
13. **Renderização excessivamente pesada de texto em negrito no Chat UI (`#39060`):**
    Fontes bold renderizavam com peso de traço desproporcional sob certos temas.
14. **Desaparecimento do cartão interativo de permissão (*approval card*) do Claude (`#39287`, `#39286`):**
    Quando o Claude publica uma solicitação de permissão (`PermissionRequest` com `interactivePrompt`) e logo em seguida
    atualiza o título do terminal para o estado de permissão, a mudança de título invalidava o registro do gancho e reconstruía
    o status a partir do título cru. Isso mantinha o status como bloqueado ("Awaiting user input"), mas descartava `interactivePrompt`,
    `toolName` e `toolInput`, deixando o usuário sem nenhum cartão com botões Allow/Deny para responder.
15. **Conversão espúria de `#N` em cartões quando uma mensagem cita outro repositório (`#39309`):**
    Com a extensão de cartões para múltiplos repositórios remotos, referências simples a `#N` no texto passavam a ser
    interpretadas incorretamente como links para o repositório externo mencionado na mensagem, em vez de ficarem como texto plano.
16. **Poluição visual da barra lateral de mensagens durante leitura (`#39369`):**
    Os controles e trilhos de ação de mensagem (*message rail*) ficavam constantemente visíveis com opacidade cheia,
    distraindo a leitura de código e respostas longas no chat.
17. **Distorção de turnos em execução por seleções de modelo mid-turn e bloqueio de respostas em fila (`#39516`):**
    Ao alterar o modelo ou nível de esforço durante a execução de um turno para preparar a próxima mensagem, a escolha
    podia ser enviada junto com um steer no turno ativo, perturbando a tarefa em andamento. Além disso, quando o agente
    faz uma pergunta no meio do turno, a resposta do usuário era tratada como follow-up comum, ficando presa atrás do próprio
    turno que a aguardava quando a fila de espera (*Queue follow-ups*) estava ativada.
18. **Falta de controle para despachar comandos Bash e subagentes Claude para segundo plano (`#39520`):**
    Comandos longos de compilação, testes ou execução de subagentes bloqueavam todo o turno no Native Chat sem opção de liberação
    da conversa, enquanto no terminal do Claude Code o atalho <kbd>Ctrl+B</kbd> permite backgrounding nativo imediato.
19. **Ocultação da resposta a comandos Steer dentro do colapso de turno ("Worked for N") (`#40823`, resolve `#40819`):**
    Ao injetar uma mensagem via Steer em um turno em andamento, o assistente respondia à instrução intermediária antes de continuar.
    Porém, ao liquidar o turno (*turn settles*), o transcript preservava visível apenas o último texto final do assistente, dobrando
    a resposta do steer para dentro do disclosure "Worked for N". O usuário via sua mensagem de steer na tela, mas ficava sem a resposta
    visível, parecendo que o assistente a ignorou.
20. **Distorção geométrica do botão Send ao alternar prévia de Steer (`#40820`):**
    Ao segurar Cmd/Ctrl para inspecionar o estado de Steer no composer, o botão de envio mudava de formato e perdia o dimensionamento
    circular padronizado, causando tremor visual na barra inferior.
21. **Parada acidental de turnos de chat ao pressionar Escape (`#41099`, resolve `#41097`):**
    No composer do chat, um único pressionamento acidental da tecla <kbd>Esc</kbd> cancelava imediatamente o turno ativo do assistente
    e descartava mensagens pendentes. Faltava uma barreira de confirmação rápida para evitar cancelamentos não intencionais.
22. **Ocultação de cartões de PRs mergeados após rebase local equivalente (`#41100`):**
    Ao efetuar o rebase local de um branch sobre a `main` após o merge do PR, o Git gerava um novo SHA local para o HEAD que não
    constava nos registros do GitHub (`commits/{oid}/pulls`). Isso fazia o Source Control ocultar o cartão do PR e suprimir o
    aviso de segurança "PR #N is merged … safe to delete".

## O que o upstream implementa

- **Preservação de respostas a mensagens Steer fora do fold de turno (`#40823`, resolve `#40819`):**
  - Identifica mensagens de usuário cujo ID de turno é herdado de um turno já em execução (steer) e mantém a primeira resposta
    de prosa do assistente posterior a essa mensagem visível fora do bloco colapsado "Worked for N", além da resposta final do turno.
- **Manutenção geométrica do botão Send em previews de Steer (`#40820`):**
  - Mantém o tamanho circular e dimensões padronizadas do botão Send enquanto Cmd/Ctrl alterna entre modos de prévia.
- **Isolamento de escolhas de modelo mid-turn e entrega direta de respostas (`#39516`):**
  - Rotula os seletores de modelo/esforço durante a execução do agente como "Next turn: ...", aplicando as escolhas
    exclusivamente no envio do próximo turno sem alterar o turno corrente;
  - Roteia respostas a perguntas interativas diretamente para o turno em andamento, contornando a fila de espera.
- **Ação "Background" para comandos e subagentes Claude no chat (`#39520`):**
  - Adiciona o botão "Background" ao lado de chamadas de topo de `Bash`, `Agent` ou `Task` do Claude no chat e na barra
    expandida de tarefas, liberando a conversa para novas instruções enquanto o comando segue executando.
- **Preservação de campos de prompt em títulos de permissão do Claude (`#39287`):**
  - Mantém `interactivePrompt`, `toolName` e `toolInput` (`withWaitPrompt`) mesmo após atualizações de título do PTY que
    confirmam a espera do hook, garantindo que o cartão de aprovação (Allow/Deny) continue sempre visível e funcional.
- **Tratamento estrito de referências `#N` em mensagens (`#39309`):**
  - Garante que menções `#N` isoladas permaneçam como texto comum caso façam referência a contextos de outros repositórios
    sem URI explícita, evitando associações indevidas.
- **Esmaecimento sutil da message rail no Chat UI (`#39369`):**
  - Reduz a opacidade da barra de ações de mensagem até que o usuário passe o mouse (hover), foque ou role o chat.
- **Redimensionamento automático de imagens coladas (*auto-shrink*) (`#39050`):**
  - Implementa `encodeClipboardImageWithinLimit`: se a imagem recodificada em PNG ultrapassar os tetos de bytes ou resolução,
    aplica um ciclo de redução proporcional suave até que caiba perfeitamente no limite permitido, garantindo colagem fluida.
- **Supressão de cartões sintéticos de modelo pelo dropdown (`#39141`):**
  - Desassocia a emissão de `onSlashCommand` da seleção visual pelo seletor de modelos. Apenas comandos explicitamente
    digitados (`/model ...`) geram entradas registradas no diário.
- **Envio do primeiro cartão pausado pós-Stop (`#38877`):**
  - Com a fila pausada após <kbd>Stop</kbd>, <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> no composer vazio dispara imediatamente o primeiro cartão em espera.
- **Roteamento correto de envio da fila com composer vazio (`#38848`):**
  - <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd> envia o último cartão enfileirado quando o composer estiver vazio, enquanto
    <kbd>Cmd/Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> seleciona a cabeça da fila.
- **Cartões de PR e links em repositórios remotos arbitrários (`#38892`):**
  - Pré-visualizações de hover cards e cartões de PR abertos agora consultam qualquer repositório no mesmo host autenticado.
- **Streaming fluído para tipos genéricos (`#38879`):**
  - O analisador mantém a renderização de streaming incremental mesmo quando o texto contém `<T>`, `Vec<T>` ou parâmetros fora de backticks.
- **Isolamento de eventos e indexação O(1) de transcrições (`#38883`, `#38895`):**
  - Notificações de mudança de status acordam estritamente o chat correspondente, e a busca usa índice direto O(1).
- **Cartão compacto de Pull Request no Native Chat (`#38750`):**
  - Renderiza um cartão dedicado com link direto, contagem de linhas e status no rodapé do turno.
- **Feedback visual dinâmico em Cmd/Ctrl+Enter (`#38749`):**
  - Ao segurar <kbd>Cmd/Ctrl</kbd>, o botão de envio exibe **Steer** ou **Queue**.
- **Startup resiliente sem cancelamento prematuro por timer (`#38727`):**
  - Elimina timeouts curtos artificiais de 60s para Claude, ACP e Pi.
- **Pass-through de atalhos do aplicativo a partir do composer (`#38724`):**
  - Permite acionar atalhos de janelas e navegação mesmo com foco no editor de texto do chat.
- **Confirmação de Escape para cancelamento de turnos ativos (`#41099`, resolve `#41097`):**
  - Exige um segundo pressionamento da tecla Escape dentro de dois segundos para interromper o turno ativo, exibindo "Press Esc again to stop";
  - Limpa o estado de confirmação ao editar o rascunho, trocar de conversa ou abrir cartões; mantém o botão Stop visual com parada imediata.
- **Prova local de rebase para retenção de PRs mergeados (`#41100`):**
  - Implementa prova local via `git merge-tree --write-tree` (ou `git diff-tree` em Git < 2.38) para certificar que o HEAD rebaseado contém estritamente o trabalho do PR mergeado;
  - Marca o commit como `contained`, mantendo visível o cartão do PR no Source Control e liberando o aviso de exclusão segura do worktree.
- **Chips e hover cards para issues, PRs e tickets de rastreadores (`#41212`, resolve `#41211`):**
  - Converte menções a chaves de tickets (`KEY-123` de Linear ou Jira) e URLs de GitHub/GitLab em chips interativos compactos ou completos (`NativeChatReferenceChip`), exibindo título, status e tipo;
  - Adiciona hover cards nativos sem consultar a web, consultando os stores locais de Linear/Jira e as contas autenticadas de GitHub/GitLab;
  - Introduz a configuração `Chat > Issue and PR chips` (`Full`, `Compact` ou `Off`) e permite pré-visualizações de links github.com mesmo em workspaces de pastas avulsas sem remotos Git.
- **Indentação e recuo de listas markdown com Tab e Shift+Tab no composer (`#41224`, resolve `#41217`):**
  - Intercepta as teclas <kbd>Tab</kbd> e <kbd>Shift+Tab</kbd> no editor ProseMirror do Native Chat quando o cursor está em itens de lista, indentando ou recuando marcadores sem perder o foco nem inserir tabulações cruas.
- **Ajuste de largura do botão de branch no composer (`#41180`, resolve `#41178`):**
  - Corrige o estilo CSS do botão de branch no rodapé do composer para abraçar estritamente o texto do branch em vez de esticar por toda a largura restante.
- **Invalidação inteligente de títulos de chat em cache (`#41242`):**
  - Atualiza títulos de abas e sessões de chat em cache somente quando os inputs salvos forem modificados, eliminando recomputações cíclicas na barra lateral.
- **Envio de imagens maiores que 5 MB no Claude Chat sem recusa de mensagem (`#41333`, resolve `#37005`):**
  - Remove o bloqueio artificial de 5 MiB por imagem no envio de mensagens do Native Chat Claude: o próprio Claude Code já encolhe nativamente imagens para no máximo 2000px e ~500 KB JPEG antes de consultar a API da Anthropic;
  - Eleva os limites do despachador do Orca para concordar com o teto de upload (`AGENT_SESSION_ATTACHMENT_MAX_BYTES` de 50 MiB por imagem e 64 MiB por mensagem total), permitindo colar capturas de tela Retina e fotos em alta resolução fluidamente.
- **Clique com Cmd/Ctrl em wikilinks e citações em qualquer ponto do rótulo (`#41337`, resolve `#41134` / STA-14852):**
  - Corrige a rota de clique `getClickedNode` no editor ProseMirror de Markdown rico: cliques na metade direita de links atômicos inline (`[[wikilink]]` e `<sup><a href>`) antes eram interpretados pelo `posAtCoords` como o nó seguinte, falhando em abrir o documento alvo;
  - Agora resolve o nó atômico anterior quando o alvo DOM estiver dentro do elemento renderizado, abrindo o link independentemente de onde o usuário clicar no rótulo.
- **Pré-visualização de links de PRs do GitHub em chats de pastas sem repositório Git (`#41359`):**
  - Quando um chat é iniciado em um workspace de pasta comum (sem repositório Git registrado), links para PRs privados do GitHub caíam no fallback web anônimo gerando erro 404 e "No preview for this page";
  - Agora roteia a consulta `preview: true` através de qualquer repositório Git local registrado no mesmo host autenticado, usando a credencial do `gh` do usuário para exibir o card rico com título, autor e status do PR.
- **Galeria lightbox de imagens com navegação por teclado no chat (`#41642`, resolve `#41641`):**
  - Integra um visualizador modal (`PanZoomImageDialog`) que permite percorrer sequencialmente com as setas do teclado todas as imagens anexadas ou geradas em uma mesma linha/mensagem do chat;
  - Refina `useLocalImageSrc` para omitir flashes da imagem anterior durante trocas de fonte, carregando apenas a imagem ativa em tamanho completo e preservando desempenho.
- **Confirmação e avanço com tecla Enter em cards de perguntas de escolha única (`#41635`):**
  - Corrige o comportamento do teclado em `NativeChatQuestionCard`: ao retornar com <kbd>ArrowLeft</kbd> a uma etapa anterior com opção já marcada, pressionar <kbd>Enter</kbd> agora confirma a seleção e avança ("Next ↵" / "Submit") em vez de desselecionar a opção;
  - Mantém <kbd>Space</kbd> e cliques como alternadores de marcação e preserva o comportamento de toggle estritamente em perguntas de múltipla escolha.

## O que fazer

- Adotar o visualizador lightbox com navegação por setas para galerias de imagens no chat (`#41642`, resolve `#41641`).
- Incorporar o avanço com tecla Enter em cards de perguntas com seleção prévia (`#41635`).
- Rotear pré-visualizações de PRs em chats de pastas avulsas através de repositórios locais existentes no mesmo host GitHub (`#41359`).
- Permitir envio de imagens e capturas de tela > 5 MB no Claude Chat (`#41333`, resolve `#37005`), aproveitando o auto-shrink nativo do Claude Code.
- Corrigir a abertura de wikilinks `[[wikilink]]` e citações com Cmd/Ctrl-click em toda a extensão do rótulo (`#41337`, resolve `#41134`).
- Adotar os chips interativos e hover cards de issues/PRs no Native Chat (`#41212`, resolve `#41211`).
- Incorporar os atalhos <kbd>Tab</kbd> e <kbd>Shift+Tab</kbd> para indentar/recuar listas no composer (`#41224`, resolve `#41217`).
- Ajustar a largura do botão de branch no composer (`#41180`, resolve `#41178`) e a invalidação de títulos de chat (`#41242`).
- Adotar a confirmação de dois toques na tecla Escape antes de interromper turnos ativos no chat (`#41099`).
- Aplicar a validação local de árvore para preservar PRs mergeados após rebase no Source Control (`#41100`).
- Manter visíveis as respostas a instruções Steer fora do colapso de turno ("Worked for N") (`#40823`).
- Adotar a estabilidade visual e proporção circular do botão Send em prévias de Steer (`#40820`).
- Incorporar o auto-shrink de imagens coladas (`#39050`) e a limpeza de cartões de modelo redundantes (`#39141`) no `brza-studio`.
- Adotar a preservação contínua de cartões de aprovação de permissões do Claude (`#39287`).
- Incorporar os cartões ricos de PR (`#38750`, `#38892`) e as melhorias de teclado de Steer/Queue (`#38749`, `#38877`, `#38848`).
- Adotar as otimizações de streaming incremental de texto com genéricos (`#38879`) e despacho isolado de status (`#38883`).
- Aplicar o isolamento de escolhas de modelo mid-turn para o próximo turno e entrega direta de respostas (`#39516`).
- Habilitar o backgrounding de comandos e subagentes Claude diretamente pela interface de chat (`#39520`).
