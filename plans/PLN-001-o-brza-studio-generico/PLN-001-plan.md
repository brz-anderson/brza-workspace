---
status: in_progress
phase: execution
origin: request
ready: "sim — o P62 ao P64 do pedido 32, autorizados por Anderson; o P57, o P61, o P65 e os casos manuais com Anderson"
estimate_h: 167.3
executed_h: 29.8
remaining_h: 3.9
scope:
  - brza-studio
opened: 2026-10-26
owner: Anderson
tags:
  - tooling
---

# PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat

- **Retomar:** o pedido 31 entrou em 2026-10-29, com a R48 e a R49, o D45 ao D47 e o P58 ao P61, e o pedido 32 no
  mesmo dia, com a R50 e a R51, o D48 ao D50 e o P62 ao P65. O P58 fechou em `brza-studio@9c7fcdebbb0`, com o
  resolvedor `resolveNativeChatTheme` em `src/shared/native-chat-theme.ts`, o P60 em `brza-studio@a44e84add32`, com a
  R53 e os X38 ao X40, e o P59 em `brza-studio@697ee59c0bf`, com os X41 ao X44: o pedido 31 espera só o P61 e o C15
  ao C17, num build, com Anderson. O pedido 32 fechou o P62, o P63 e o P64, na
  sessão `pln-001-pedido-32`, em `brza-studio@21f9cfe90bb`, `9564eff9368` e `ba4102b5c95`, e espera só o P65, com o C18 ao C20, num build, com Anderson. O P66 do pedido 33 fechou em `brza-studio@9118f60672b`, com a R54 e os X45 ao
  X48, e espera só o C21; o P67, que fecha o X20 com a R55 e a R56, fechou em `brza-studio@97a93f6ff57` e se
  confere junto do C6; sete arquivos de teste do transcript do mobile não carregam desde o P43 (X47). Esperam Anderson o P57, o P61, o P65 e os casos manuais (C1 ao C7, C10 ao C12 e C14, num build só, o C15 ao
  C17 depois do P60 o C18 ao C20 depois do P64 e o C21), o X10 e o P27.2 e o P27.3; o P37 fechou sem código
  (R59.4), e o P68 fechou o X47 em `brza-studio@7be19418c8f`. Do PLN-002/P9 (R12.4, R13.4),
  para o P64: o `brza sessions` abre sem o `/rename` por padrão e dá à aba o título do `--title`; sem `--rename`, a
  sessão entra no correio com o nome automático `brza-workspace-<hex>`. O P64 não lê o mapa de sessões do PLN-002 e
  casa o remetente com a aba pelo que o app guarda. Medido no P9.1, para o P62: a mensagem chegou no transcript como
  `<cross-session-message from="uds:/tmp/cc-socks/60775.sock" from-name="brza-workspace-5b" from-mode="prompting">`,
  com o `origin.name` na linha do JSONL; o nome está no `from-name=`, e não no `from=` do `<agent-message>` do D48; o P62 lê os dois (X34).
- **Dividido:** o Desenho em [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat — Desenho](PLN-001-design.md);
  a Entrevista, o Terreno e o Log até a divisão ficam no PLN-025 do workspace da Fixfy
  (`plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-interview.md` e `PLN-025-design.md`, R28.3); as rodadas
  deste plano, da R29 em diante, estão na `## Entrevista` abaixo. As R até a R28, citadas nos passos e nos itens `D`, são as do
  PLN-025 da Fixfy.

## Pedido

- **Origem:** o PLN-029 do workspace da Fixfy, movido para cá em 2026-10-27 a pedido de Anderson (rodada D, R32). O PLN-029
  nasceu da divisão do PLN-025 do workspace da Fixfy (`plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-plan.md`, "O
  Orca — Desktop, CLI, App e Web — é a ferramenta permanente da Fixfy, em um plano por repositório"), pedida por
  Anderson na sessão do checkout da raiz do workspace da Fixfy de 2026-10-26 ("divida o PLN-025 em 2, um para o
  fixfy-orca e outro para o orca-dev") e desenhada na R28 de lá; os passos e os itens `D` vieram com os IDs de antes
  (PLN-025/R28.2)

Os pedidos que o `brza-studio` executa, os 1 a 26 copiados do PLN-025 da Fixfy com o número de lá, e os 27 a 29,
de 2026-10-27, numerados aqui na sequência. O build local e o atualizador desligado
saíram do pedido 1 ("abra um plano, vamos adaptar o Orca ao nosso fluxo de trabalho, a ferramenta será adotada
permanentemente") pela R7.2, que leva ao `orca-dev` (hoje `brza-studio`) o que serviria a um projeto fora da Fixfy.

- **Pedido 5:** "arquivos de diff, quando expandido, tem 3 abas, a de diff, a versão atual e a versão passada.
  - arquivos na versão atual/anterior devem ser renderizados por ferramenta de prévisualizaçõa;
  - os arquivos markdown quando expandidos nessas abas, são renderizados como markdown formatado;
  - arquivos de código - e blocos de código - seguem o tema Islands Dark do Android Studio;
  - se possível, arquivos de código rodam analyze lint;"
- **Pedido 14:** "na barra superior do visualizador de markdown, hoje temos <> para a visualização de código e o lápis para
  visualização renderizada, mas com edição habilitada, adicione mais um, o olho, que passa a ser o padrão de
  visualização, é a visualização renderizada como o editar, mas sem permitir editar o arquivo"
- **Pedido 15:** "o orca-dev está com todas as alterações prontas para buildar no windows?", e, ao registro do passo, "sim"
- **Pedido 19 a 21:** Na barra inferior da mensagem do agente: "Botão Bifurcar: funciona como o bifurcar do claude.ai (inicia uma nova
  sessão a partir desse ponto, com tudo oq tiver acima)"; "Botão Novo Chat: abre uma nova sessão assim como o
  Bifurcar, mas levando apenas a mensagem clicada"; "Botão Fixar Capitulo: vem marcado por padrão e fixa/desafixa o
  capitulo (capitulo = prompt do usuário + resposta do agente), os marcados ficam na sessão flutuante, como já é hoje"
- **Pedido 22:** Na barra inferior do chat: "Ao lado do seletor de modelo/esforço, um seletor de conta: Seletor lista as contas
  logadas, da mesma forma que hoje lista `claude|adm` no terminal do claude code; Ao trocar de conta, continua no
  mesmo chat e o Orca inicia uma nova sessão na conta selecionada, injetando o contexto da sessão anterior, o conteúdo
  do chat apenas informa "Conta trocada - claude|adm" (assim como mostra hoje "Contexto limpo"; Para futuramente:
  adicionar uma nova opção no seletor de modelo/esforço "Selecionar automaticamente""
- **Pedido 23 e 24:** No chat em geral: "Adicionar no menu aberto pelo clique do botão direito uma lista de sugestões para palavras
  digitadas errado"; "Adicionar nas configs de chat o modo de visualização markdown, que é um switch que vem
  desabilitado, quando habilitado, a caixa de mensagem do chat renderiza como o modo de edição do visualizador de
  markdown, já formatado"
- **Pedido 25:** "nas mensagens enviadas pelo usuário, numa barra inferior, assim como a barra de mensagens do agente, adicionar os
  botões: Copiar: copia a mensagem; Enviar agora: quando estiver na fila para envio; Editar: copia a mensagem direto
  na caixa de digitação"
- **Pedido 26:** "no chat do Orca, onde aparece hoje "Claude atingiu seu limite de sessão. Ele será redefinido em ..." ao lado do botão
  Continuar, adicione os botões: Continuar em <seletor de conta>: faz a mesma coisa que o seletor de conta do chat,
  passa a conversa para a conta selecionada; Retomar automaticamente: adiciona uma tarefa agendada que dispara ao
  resetar o limite da conta, continuando a tarefa"
- **Pedido 27 (2026-10-27, sessão `fixfy-35` da Fixfy):** "melhorias para o BrzA Studio: no bloco de Perguntou: no chat, as perguntas do agente ficam da mesma cor
  do texto normal (branco); no bloco de comandos e ferramentas usadas, conseguimos adicionar mais icones/titulos
  personalizados que interajam de forma diferente? git com o icone do git, jira e etc; se for possível, sugira alguns"
- **Pedido 28 (2026-10-27, sessão `fixfy-9b` da Fixfy):** "blocos de código - ``` - e as tabelas, largura sempre de 120 colunas + padding, quando selecionado
  `largura total` nas configs de largura do conteudo"
- **Pedido 29 (2026-10-27, sessão `fixfy-9b` da Fixfy):** "e links no chat, na cor azul padrão de link, mais clarinho"
- **Pedido 30 (2026-10-28, sessão do `brza-workspace` que orquestrou o P42 e o P43):** "seria mto bom se conseguicemos
  adicionar image preview no chat"
- **Pedido 31 (2026-10-29, sessão do `brza-workspace` que orquestrou o P54 ao P56):** "o fundo do visualizador de
  markdown ficou mto escuro, deixe da mesma cor que o fundo do chat, deixe com o mesmo tema/tipografia que o chat - o
  terminal igual ao chat tbm -, trocar o tema do chat, troca de todos, trocar o tema dos outros troca só deles"
- **Pedido 32 (2026-10-29, a mesma sessão):** "faça com que as mensagens entre sessões apareçam no chat como "Mensagem
  de..." como já é na interface do `Orca` na versão mais atual"
- **Pedido 33 (2026-10-29, a mesma sessão):** "o texto do "Pensou" que aparece nos comandos executados deve aparecer
  no chat igual ao "Perguntou" com >"

### Cobertura

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 5` | O arquivo de código e o bloco de código seguem o tema Islands Dark do Android Studio | P6 | conferência no Orca (manual) |
| `Pedido 14` | Na barra do arquivo Markdown aberto no editor, o olho — renderizado e só leitura — vem antes do lápis e do código e é o modo padrão; a aba de diff não muda (R19) | P25 | teste dos modos e do padrão (unidade); conferência no Orca (manual) |
| `Pedido 15` | O `brza-studio` sai num instalador x64 de Windows, sem assinatura, por um comando, com o `mobile/` instalado e a versão `-local.<ms>.<commit>`, e o atualizador fica desligado no app instalado (R20) | P26, P27 | teste do script (unidade); instalação no Windows (manual) |
| `Pedido 19` | O Bifurcar da mensagem do agente abre uma aba nova com a sessão cortada até ela, pelo `forkSession` do SDK, e a conversa de origem não muda (R26.2) | P33 | teste do corte e do canal (unidade); bifurcar no Orca (manual) |
| `Pedido 20` | O Novo Chat abre uma aba nova com a mensagem como rascunho na caixa, sem enviar | P34 | teste do componente (unidade) |
| `Pedido 21` | O Fixar Capítulo vem marcado, fixa e desafixa, e a régua de prompts destaca os fixados, com a prévia do capítulo (R26.1) | P35 | teste do estado e da régua (unidade) |
| `Pedido 22` | Ao lado do seletor de modelo e esforço, o seletor de conta troca a conta no mesmo chat, com o contexto pelo transcript copiado e o divisor "Conta trocada - <conta>" (R26.3) | P36 | teste da cópia e do lançamento (unidade); troca `claude` → `adm` no Orca (manual) |
| `Pedido 23` | O botão direito numa palavra errada na caixa do chat mostra as sugestões e troca a palavra | P37 | conferência no Orca (manual) |
| `Pedido 24` | Com o switch das configurações de chat ligado, a caixa de texto mostra o Markdown formatado, e o que se envia segue em Markdown; desligado por padrão | P38 | teste da serialização ida e volta (unidade); conferência no Orca (manual) |
| `Pedido 26` | Na linha do aviso de limite, o "Continuar em <conta>" lista as outras contas e, num clique, troca a conta como o P36 e envia o Continuar depois que a sessão nova sobe; com a troca falha, nada é enviado (R27.1, R27.2) | P40 | teste da ordem troca → envio e da falha (unidade); limite na `claude` → continuar na `adm` (manual) |
| `Pedido 26` | O "Retomar automaticamente" agenda no main, persistido, o Continuar para o reset + 1 min, no mesmo chat; a linha mostra "Retomada às HH:MM · Cancelar", uma mensagem enviada antes cancela, e sem `resetsAt` o botão não aparece; com o Orca fechado na hora, dispara ao abrir se o chat ainda está no corte (R27.3, R27.4) | P41 | teste da agenda, do cancelamento e do disparo ao abrir (unidade); retomada com o relógio adiantado (manual) |
| `Pedido 25` | A mensagem enviada tem o Editar, que a leva à caixa, abaixo do rascunho se houver; o Copiar e o Enviar agora seguem onde estão (R25.1, R25.2) | P39 | teste do componente (unidade) |
| `Pedido 27` | O texto da pergunta no bloco "Perguntou:" usa a cor `primary` do tema, a do ✓ de opção escolhida, nos três pontos (R29.1) | P42 | teste de aparência (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | Os logos SVG de marca entram só no desktop, por um componente do BrzA: o do git, novo, e o GitHub e o Jira, que o upstream já tem; o Figma e o Firebase ficam no lucide também no desktop; o mobile cai no ícone lucide equivalente (R29.4, R35.1) | P43 | teste do mapa de categorias e do recuo no mobile (unidade) |
| `Pedido 27` | O comando `git` ganha ícone pelo subcomando, o título "git commit — <mensagem>" e o hash que abre o diff do commit (R29.2) | P44 | teste da categoria e do título (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | O comando `gh` de PR e issue ganha o ícone de PR, o título "PR #123 — <título>" e o chip que abre o PR no navegador (R29.2) | P45 | teste da categoria e do título (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | Os testes (`vitest`, `run-vitest.mjs`, `flutter test`, `pytest`) ganham o ícone de testes, com passou/falhou contado no título pela saída (R29.2) | P46 | teste da contagem por executor (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | Pacotes e build (`pnpm`, `npm`, `flutter pub`, build) ganham ícone e título, sem interação (R29.2) | P47 | teste da categoria (unidade) |
| `Pedido 27` | O Jira e o Confluence ganham o chip com a chave do card ou o título da página, que abre no navegador (R29.3) | P48 | teste do chip (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | A ferramenta Skill ganha o ícone e o título "Skill · <nome>" (R29.3) | P49 | teste do título (unidade) |
| `Pedido 27` | O Figma ganha o logo, o nome do nó e a miniatura do `get_screenshot` na linha (R29.3) | P50 | teste do nome e da miniatura (unidade); conferência no BrzA Studio (manual) |
| `Pedido 27` | O Firebase e o Context7 ganham ícone e o nome do projeto ou da biblioteca no título, sem interação (R29.3) | P51 | teste da categoria e do título (unidade) |
| `Pedido 28` | Só na largura "Total", todo bloco de código e toda tabela têm exatamente `120ch` mais o padding, e no painel estreito encolhem até 100% e rolam na horizontal, com o texto corrido na largura total (R30.1, R30.2) | P52 | teste do estilo (unidade); conferência no BrzA Studio (manual) |
| `Pedido 29` | O link do chat usa `--chat-link`, `#79C0FF` no escuro e `#0969DA` no claro, com o sublinhado a 40% (R31.1) | P53 | teste da variável (unidade); conferência nos dois temas (manual) |
| `Pedido 30` | A imagem do `Read`, do `get_screenshot` e do print do browser vira arquivo no temp, com o `image-ref` no resultado da ferramenta, ao vivo e no histórico (R36.2, R39.1) | P54 | teste da extração e dos dois decoders (unidade) |
| `Pedido 30` | A linha da ferramenta mostra, fechada, até 4 miniaturas de ~96 px e um "+N" que abre a linha; o clique amplia (R36.3, R39.4, R42.1) | P55 | teste do componente (unidade); conferência no BrzA Studio (manual) |
| `Pedido 30` | O caminho ou a URL de imagem solto no texto ganha a miniatura abaixo do parágrafo, uma vez por mensagem, só se abre e só com a mensagem terminada (R39.2, R39.3, R42.2) | P56 | teste do plugin (unidade); conferência no BrzA Studio (manual) |
| `Pedido 30` | O `![]()`, o anexo enviado e o ampliar ao clicar, que já existem, funcionam no BrzA Studio (R36.1) | P57 | conferência no BrzA Studio (manual) |
| `Pedido 31` | O chat tem um tema próprio, um par escuro e claro do catálogo do terminal, com o "Padrão do BrzA" de hoje como padrão; o "igualar ao terminal" sai, e quem o tinha ligado não vê mudança (R48.1, R48.4, R49.2, R49.3) | P58 | teste do resolvedor, da migração e da seção (unidade); conferência no BrzA Studio (manual) |
| `Pedido 31` | O terminal tem o interruptor "Seguir o chat", ligado por padrão: ligado, o fundo e as cores são os do chat, com a fonte do terminal; desligado, o tema próprio de hoje (R48.2, R48.3) | P59 | teste da aparência do terminal (unidade); conferência no BrzA Studio (manual) |
| `Pedido 31` | O visualizador de Markdown tem o interruptor "Seguir o chat", ligado por padrão: ligado, os três modos têm o fundo e o claro/escuro do chat, e o olho e o lápis, a fonte e o tamanho do chat; desligado, um seletor de tema próprio (R48.2, R48.3, R49.1, R49.4) | P60 | teste do fundo e da tipografia nos três modos (unidade); conferência no BrzA Studio (manual) |
| `Pedido 31` | Trocar o tema do chat troca os três que o seguem; trocar o do terminal ou o do Markdown troca só ele | P61 | conferência no BrzA Studio (manual) |
| `Pedido 32` | A mensagem de outra sessão (`SendMessage` do Claude Code) aparece no chat como "Mensagem de <nome>", e a devolução de subagente como "Devolução de <nome>", no histórico e ao vivo (R50.1, R50.2, R51.1) | P62 | teste do leitor (unidade); conferência no BrzA Studio (manual) |
| `Pedido 32` | As duas aparecem no cartão do Orca de 2026-10-29 (#34824), com o status do remetente (R50.1) | P63 | os testes do cartão trazidos do upstream (unidade); conferência no BrzA Studio (manual) |
| `Pedido 32` | O clique no nome do remetente abre a aba de chat da sessão dele, se aberta no app (R50.3) | P64 | teste da busca da aba (unidade); conferência no BrzA Studio (manual) |
| `Pedido 33` | A linha do raciocínio, fechada, mostra "Pensou por 3s:" e o começo do texto, cortado, no tom apagado, com a seta que abre o texto inteiro; o rótulo da pergunta passa a "Perguntou:" (R52.1 a R52.3) | P66 | teste da linha (unidade); conferência no BrzA Studio (manual) |
| `X20` | O `executeRead`, o `executeWrite` e o `executeDestructive` do MCP da Atlassian ganham o ícone do produto do `name` e o título com a ferramenta interna; o `discover` ganha o ícone do produto citado na busca, e o título com a busca entre aspas (R55.1, R55.2) | P67 | teste da categoria e do título (unidade); conferência no BrzA Studio (manual, com o C6) |

Do pedido 5, só o tema Islands Dark é daqui; as abas do diff e o lint estão no PLN-028 do workspace da Fixfy.

### Fora de escopo

- **O "Selecionar automaticamente" no seletor de modelo e esforço** (pedido 22, "para futuramente"). Volta por rodada
  própria.
- **O que é da Fixfy no fork** — o painel, o chat nativo da Fixfy, o ADM Claude e o quadro de planos. Está no
  PLN-028 do workspace da Fixfy (`plans/PLN-028-o-orca-fixfy-com-a-fixfy/PLN-028-plan.md`).
- **A sincronização em cadeia e a conferência no Orca da Fixfy.** A sincronização era o PLN-025/P4, e a conferência, o
  PLN-028/P8, com o build do `orca-fixfy`, que está congelado. A conferência de cada passo é no BrzA Studio, com
  Anderson.

## Restrições

- **O `pnpm` não está no `PATH`.** O 12.14.0 está em `~/.npm/_npx/aa4546e781591cea/node_modules/.bin`, e o hook do
  commit do `brza-studio` falha sem ele no `PATH`.
- **Os testes rodam pelo `run-vitest.mjs`, por caminho.** `node config/scripts/run-vitest.mjs run --config
  config/vitest.config.ts <caminhos>`; o `pnpm check:changed` leva `--base=origin/master`.
- **Worker em paralelo trabalha num worktree em `.worktrees/` do `brza-studio`.** Criado com `git worktree add` e passado
  ao `orchestration worker-start` por `path:`: o worktree novo do Orca cai fora do `brza_where`.
- **O instalador de Windows sai pelo runner do GitHub** (X7): `gh workflow run build-win-local.yml --repo
  brz-anderson/brza-studio --ref master`, com a conta `brz-anderson` ativa no `gh`.

## Entrevista

As R até a R28 são as rodadas do PLN-025 do workspace da Fixfy, citadas pelo número de lá; as rodadas deste plano
começam na R29. Transcritas de `/private/tmp/claude-501/brza-rodadas-2026-10-27.md`, que as sessões `fixfy-35` e
`fixfy-9b` do workspace da Fixfy gravaram com as perguntas, as opções e as respostas literais.

### Rodada 29 — o "Perguntou:" e os ícones das ferramentas (enviada 2026-10-27)

> **Apresentado antes:** o texto da pergunta usa `text-chat-foreground` em `NativeChatAwaitingInputRow.tsx:76`, `:113` e
> `:118`; a categoria do ícone sai de `src/shared/native-chat/tools/native-chat-tool-icon.ts:58`, com o precedente
> `runsOrcaBrowserCommand`; os ícones são lucide, compartilhados com o mobile; o mapa é arquivo do upstream.

Pedido de Anderson: "melhorias para o BrzA Studio: no bloco de Perguntou: no chat, as perguntas do agente ficam da mesma
cor do texto normal (branco); no bloco de comandos e ferramentas usadas, conseguimos adicionar mais icones/titulos
personalizados que interajam de forma diferente? git com o icone do git, jira e etc; se for possível, sugira alguns".
Respondida em 2026-10-27, na sessão `fixfy-35`.

1. **R29.1 — Que cor a pergunta do agente ganha no bloco "Perguntou:"?** Seleção única. Opções:
   - cor de destaque do tema (recomendada) — `primary` do tema, a mesma do ✓ — custo: ~0,3 h; se paga: na primeira
     releitura de conversa longa;
   - cinza, como as ferramentas — `text-chat-foreground-faint` — custo: ~0,3 h; se paga: se a pergunta deve incomodar
     menos que a resposta;
   - destaque mais fundo de cartão — cor, fundo sutil e borda à esquerda — custo: ~0,7 h; se paga: se a cor sozinha
     não bastar.

   **Decidido — "Cor de destaque do tema (Recomendado)".** Vai ao P42.

2. **R29.2 — Quais comandos de shell ganham ícone e título próprios?** Seleção múltipla. Opções:
   - git (recomendada) — GitBranch ou GitCommit pelo subcomando, título "git commit — <mensagem>", o hash abre o diff
     — custo: ~1 h; se paga: na primeira sessão com commits;
   - gh, PR e issue (recomendada) — GitPullRequest, "PR #123 — <título>", chip que abre o PR — custo: ~1 h; se paga:
     em toda sessão com PR;
   - testes — vitest, run-vitest.mjs, flutter test, pytest: FlaskConical, passou/falhou no título — custo: ~1,5 h; se
     paga: quando os testes são frequentes e longos;
   - pacotes e build — pnpm, npm, flutter pub, build: Package ou Hammer, só ícone e título — custo: ~0,3 h; se paga:
     só na leitura rápida.

   **Decidido — as quatro marcadas:** git, gh (PR e issue), testes e pacotes e build. Vão ao P44, P45, P46 e P47.

3. **R29.3 — Quais ferramentas de MCP e do agente ganham ícone e título próprios?** Seleção múltipla. Opções:
   - Jira e Confluence (recomendada) — chip com a chave do card ou o título da página, que abre no navegador — custo:
     ~1 h; se paga: em toda sessão com card;
   - Skill (recomendada) — Sparkles, "Skill · <nome>" — custo: ~0,3 h; se paga: na hora;
   - Figma — logo ou PenTool, nome do nó e miniatura do `get_screenshot` — custo: ~1,5 h (sem miniatura ~0,3 h); se
     paga: nas tarefas de design;
   - Firebase e Context7 — Flame e BookOpen, nome do projeto ou da biblioteca — custo: ~0,3 h; se paga: só na leitura
     rápida.

   **Decidido — as quatro marcadas:** Jira e Confluence, Skill, Figma e Firebase e Context7. Vão ao P48, P49, P50 e
   P51.

4. **R29.4 — De onde vêm os ícones?** Seleção única. Opções:
   - lucide, com logos SVG no desktop (recomendada) — SVG de marca só no desktop, o mobile cai no lucide — custo: ~0,5
     h uma vez, mais ~5 min por logo; se paga: na hora;
   - só lucide — custo: zero a mais; se paga: agora, desktop e mobile iguais.

   **Decidido — "Lucide, com logos SVG no desktop (Recomendado)".** Vai ao P43.

### Rodada 30 — os blocos de código e as tabelas em "largura total" (enviada 2026-10-27)

> **Apresentado antes:** "Total" é `width === 'full'`, que põe `--chat-content-max-width: none` em
> `native-chat-appearance-style.ts:88`; o `<pre>` usa `max-w-full` em `NativeChatCodeBlock.tsx:62`.

Pedido de Anderson: "blocos de código - ``` - e as tabelas, largura sempre de 120 colunas + padding, quando selecionado
`largura total` nas configs de largura do conteudo". Respondida em 2026-10-27, na sessão `fixfy-9b`.

1. **R30.1 — Em "largura total", o bloco ou a tabela mais curto que 120 colunas fica com quanto de largura?** Seleção
   única. Opções:
   - sempre 120 colunas (recomendada) — exatamente 120ch mais o padding; em painel estreito, até 100% com rolagem
     horizontal — custo: ~1 h; se paga: na hora, com as bordas alinhadas;
   - até 120 colunas — teto, o bloco curto encolhe — custo: ~1 h; se paga: se blocos curtos largos incomodarem mais.

   **Decidido — "Sempre 120 colunas (Recomendado)".** Vai ao P52.

2. **R30.2 — A coluna da tabela se mede em qual fonte?** Seleção única. Opções:
   - na fonte de código (recomendada) — 120ch da mono do chat, igual ao bloco — custo: incluído; se paga: na hora;
   - na fonte do texto — custo: o mesmo; se paga: só se a tabela precisar caber 120 caracteres do próprio texto.

   **Decidido — "Na fonte de código (Recomendado)".** Vai ao P52.

### Rodada 31 — os links do chat (enviada 2026-10-27)

> **Apresentado antes:** o link usa `--chat-foreground-strong` em `native-chat-markdown.css:18`.

Pedido de Anderson: "e links no chat, na cor azul padrão de link, mais clarinho". Respondida em 2026-10-27, na sessão
`fixfy-9b`.

1. **R31.1 — Qual azul para os links do chat?** Seleção única. Opções:
   - `#79C0FF` no escuro (recomendada) — `#0969DA` no claro, sublinhado a 40% — custo: ~0,3 h; se paga: na hora;
   - `#58A6FF` no escuro — `#0969DA` no claro — custo: ~0,3 h; se paga: se o `#79C0FF` parecer apagado;
   - azul claro do tema do terminal — `brightBlue` do tema — custo: ~0,5 h; se paga: se trocar de tema com frequência.

   **Decidido — "#79C0FF no escuro (Recomendado)".** Vai ao P53.

### Rodada 32 — o plano vai para o brza-workspace (enviada 2026-10-27)

Pedido de Anderson: "criei um repo pra servir de workspace do brza-studio, git:
git@github.com:brz-anderson/brza-workspace.git - clone em Projects/ ao lado de brza-studio e envie o plano de melhorias
do BrzA Studio para lá (brza-workspace)". Respondida em 2026-10-27, nas sessões `fixfy-35` e `fixfy-9b`.

1. **R32.1 — O que vai para o brza-workspace?** Seleção única. Opções:
   - o PLN-029 mais os pedidos de hoje (recomendada) — plano e desenho, com os pedidos das rodadas A, B e C como passos
     novos no F7 — custo: ~0,5 h; se paga: na hora;
   - só o PLN-029 — custo: ~0,3 h; se paga: agora, mas os pedidos ficam no `/tmp`;
   - só um plano novo com os pedidos de hoje — custo: ~0,3 h; se paga: só se o PLN-029 terminar na Fixfy.

   **Decidido — "PLN-029 + os pedidos de hoje (Recomendado)".**

2. **R32.2 — O que acontece com o PLN-029 no workspace da Fixfy?** Seleção única. Opções:
   - mover e deixar um aviso (recomendada) — fica só o `PLN-029-plan.md` com `status: dropped` e a linha de para onde
     foi — custo: ~0,3 h; se paga: na hora;
   - mover e reescrever os 18 links — custo: ~1 h; se paga: só se a Fixfy não puder ter vestígio do BrzA Studio;
   - copiar e deixar o original — custo: zero, e divergência logo; se paga: nunca.

   **Decidido — "Mover e deixar um aviso (Recomendado)".**

3. **R32.3 — Onde as sessões do brza-studio gravam worklog e evidência daqui em diante?** Seleção única. Opções:
   - no brza-workspace (recomendada) — `~/Projects/brza-workspace/work/worklogs/` — custo: ~0,2 h; se paga: no
     primeiro worklog;
   - continua na Fixfy — custo: zero; se paga: nunca.

   **Decidido — "No brza-workspace (Recomendado)".**

4. **R32.4 — Que forma o plano tem no brza-workspace, que ainda não tem norma?** Seleção única. Opções:
   - mesma norma, renumerado PLN-001 (recomendada) — copia o `plans/README.md` e a norma de `work/` sem o que é só da
     Fixfy; `plans/PLN-001-o-brza-studio-generico/`, com a linha de que veio do PLN-029 — custo: ~0,5 h; se paga: no
     próximo plano;
   - mesma norma, mantém PLN-029 — custo: ~0,4 h; se paga: agora;
   - sem norma, só o arquivo — custo: ~0,1 h; se paga: agora.

   **Decidido — "Mesma norma, renumerado PLN-001 (Recomendado)".**

### Rodada 33 — o P42, o P43, o P49 e o P51 em paralelo, por workers do Orca (enviada 2026-10-28)

> **Apresentado antes:** o P43 é a base do P49 e do P51 (`PLN-001-plan.md`, P43: "Antes do P44 ao P51"), e o P42 é
> independente; um worktree novo do Orca vai para `~/orca/workspaces/brza-studio/…`, fora do `brza_where` do
> `~/.zshrc:57`, e o `claude` dali cairia na função da Fixfy.

Pedido de Anderson: "retome o plano 001, utilize /orchestration para organizar e executar os passos em paralelo".
Respondida em 2026-10-28, na sessão do `brza-workspace` que orquestrou o pacote.

1. **R33.1 — Como dividir o pacote entre os workers?** Seleção única. Opções: 2 workers (recomendada) — o P42 num, e o
   P43, o P49 e o P51 em sequência no outro; 3 workers — o P42 e o P43 em paralelo, e o P49 com o P51 num terceiro,
   depois do P43; 4 workers — o P49 e o P51 em paralelo depois do P43.

   **Decidido — "3 workers".**

2. **R33.2 — Os workers fazem commit e push na master sozinhos?** Seleção única. Opções: commit e push com testes
   verdes (recomendada), depois de conferir a identidade com `git var GIT_AUTHOR_IDENT`, com rebase na master; commit na
   branch e push depois do aviso.

   **Decidido — "Commit e push com testes verdes (Recomendado)".**

3. **R33.3 — Que modelo cada worker usa?** Seleção única. Opções: Opus no P43 e Sonnet no P42 (recomendada); Opus nos
   dois; o padrão do agente, sem `--model`.

   **Decidido — "Opus no P43, Sonnet no P42 (Recomendado)".** O worker do P49 e do P51, mecânico, vai de Sonnet, pela
   mesma regra.

4. **R33.4 — Onde ficam os worktrees?** Seleção única. Opções: em `brza-studio/.worktrees/` (recomendada), criados com
   `git worktree add` e passados ao Orca por `path:`; worktree novo do Orca (`new-top-level`).

   **Decidido — "Em brza-studio/.worktrees/ (Recomendado)".**

### Rodada 34 — a prévia de imagem no chat (enviada 2026-10-28)

Pedido de Anderson: "seria mto bom se conseguicemos adicionar image preview no chat". Respondida em 2026-10-28, na mesma
sessão.

1. **R34.1 — Onde se registra o pedido?** Seleção única. Opções: pedido 30 no PLN-001 (recomendada), no F7, com a
   entrevista e os passos numa sessão nova; issue em `work/issues/`.

   **Decidido — "Pedido 30 no PLN-001 (Recomendado)".**

2. **R34.2 — Que imagens a prévia mostra?** Seleção múltipla. Opções: links e caminhos de imagem na mensagem; imagens
   lidas por ferramenta (o `Read` de imagem, o `get_screenshot`); anexos enviados por Anderson; ampliar ao clicar.

   **Decidido — as quatro marcadas.** O desenho, o custo de cada uma e os passos ficam para a sessão que desenhar o
   pedido 30.

### Rodada 35 — os logos de marca do P43 (enviada 2026-10-28)

> **Apresentado antes, pelo worker do P43:** o upstream já embarca o `GitHubIcon` (Octicons `mark-github`) e o
> `JiraIcon`; o logo do Git é CC BY 3.0 (Jason Long), com o traço do Simple Icons (CC0), e a política de marca do Git
> permite identificá-lo; as diretrizes do Figma proíbem modificar a marca, multicolorida, e as do Firebase proíbem mudar
> as cores e restringem o uso em produto; os glifos do chat são monocromáticos (`currentColor`) e mudam de tom com o
> estado da linha.

Respondida em 2026-10-28, na mesma sessão, duas vezes, a pedido de Anderson ("pergunta dnv"), com a mesma resposta.

1. **R35.1 — Quais logos de marca o P43 traz para o desktop?** Seleção única. Opções: o Git novo, e o GitHub e o Jira
   reusados (recomendada), com o Figma e o Firebase no lucide (`pen-tool` e `flame`) também no desktop; os cinco
   monocromáticos; o Figma e o Firebase nas cores oficiais; nenhum logo novo, nem o Git.

   **Decidido — "Git novo, GitHub e Jira reusados (Recomendado)".** Reescreve o D37; no P50, o Figma fica com o
   `pen-tool`.

### Rodada 36 — a prévia de imagem: o que falta e de onde vem a imagem da ferramenta (enviada 2026-10-28)

> **Apresentado antes**, levantado em `brza-studio@7e9e0d18948`: o `![]()` da mensagem já vira imagem, por URL ou por
> caminho local (`NativeChatMarkdown.tsx:73` → `NativeChatMarkdownImage.tsx`, com carga perto da tela e "Preview
> unavailable" na falha); o anexo enviado já tem miniatura na mensagem (`NativeChatUserMessageRow.tsx:138-164`); ampliar
> ao clicar já existe (`MarkdownImageLightbox.tsx` e `PanZoomImageDialog.tsx`, com pan e zoom). A lacuna é a imagem
> lida por ferramenta: o `resultText` de `claude-structured-item-translation.ts:127-143` fica só com os blocos `text` do
> `tool_result` e descarta o bloco `image` em base64; o `NativeChatToolResultBlock` (`native-chat-types.ts:94-104`) só
> tem `output: string`; e o journal corta o que passa do limite (`journal-payload-bounds.ts:44-51`). O caminho ou a URL
> de imagem solto no texto, fora do `![]()`, não vira imagem.

Respondida em 2026-10-28, na sessão do `brza-workspace` que desenhou o pedido 30.

1. **R36.1 — O que motivou o pedido?** Seleção única. Opções: imagem de ferramenta (recomendada) — as partes 1, 3 e 4
   viram conferência do que existe — custo: ~0,3 h; se paga: agora; nunca vi prévia nenhuma — um passo de diagnóstico
   antes — custo: +1 a 2 h; se paga: no primeiro passo, se for defeito; caminho solto no texto — custo: ~3 a 4 h; se
   paga: na primeira resposta que cite um print.

   **Decidido — "Imagem de ferramenta (Recomendado)".**

2. **R36.2 — De onde vem a imagem da ferramenta?** Seleção única. Opções: extrair para arquivo (recomendada) — o main
   tira o bloco `image` do `tool_result`, grava num arquivo e põe a referência no resultado; vale para o `Read`, o Figma e
   o browser — custo: ~4 a 5 h; se paga: na primeira ferramenta além do `Read`; só o `Read`, pelo `file_path` — custo:
   ~1,5 h; se paga: agora, sem o `get_screenshot` do P50; base64 no journal — custo: ~3 h e os limites; se paga: nunca,
   pelo corte.

   **Decidido — "Extrair para arquivo (Recomendado)".**

3. **R36.3 — Onde a miniatura aparece na linha da ferramenta?** Seleção única. Opções: com a linha fechada
   (recomendada) — ~96 px de altura, abaixo do título, o clique amplia — custo: ~1 h; se paga: na hora; só com a linha
   aberta — custo: ~0,5 h; se paga: se muitos prints poluírem; só um ícone — custo: ~0,7 h; se paga: se abrir for raro.

   **Decidido — "Com a linha fechada (Recomendado)".**

4. **R36.4 — E o mobile?** Seleção única. Opções: só desktop agora (recomendada) — o mobile segue com o anexo e o
   `image-ref`, sem a imagem de ferramenta — custo: zero; se paga: agora; mobile junto, pelo relay — custo: +4 a 6 h; se
   paga: só com sessões acompanhadas pelo celular.

   **Decidido — "Só desktop agora (Recomendado)".**

### Rodada 37 — o comando composto e a divisão do P44 ao P48 e do P50 (enviada 2026-10-28)

> **Apresentado antes:** hoje vale a primeira categoria da lista que casar com o comando inteiro
> (`brza-tool-categories.ts:48` e `:112`), e em `brza … && git commit` ganha a `brzaCli`; o `splitUnquotedSegments`
> (`orca-browser-cli-commands.ts:134`) já divide o comando por segmento, fora de aspas; o P44 ao P47 disputam a mesma
> lista, e na R33 o rebase de duas listas em paralelo deu conflito.

Pedido de Anderson: "execute o P44 ao P48 e o P50 em paralelo com /orchestration, em workers do Orca […] Antes de
disparar os workers, faça comigo as rodadas das pendências de cada passo". Respondida em 2026-10-28, na sessão
`pln-001-p44-p50` do `brza-workspace`.

1. **R37.1 — No comando composto que casa com mais de uma categoria, qual vale?** Seleção única. Opções: ordem fixa por
   peso (recomendada) — testes > gh > git > pacotes e build > `brzaCli`, casando por segmento — custo: ~0,3 h no P44;
   se paga: na hora; o último segmento — custo: ~0,3 h; se paga: em `cd x && pnpm test`, mas `git commit && git push`
   mostraria o push; o primeiro que casar, como hoje — custo: zero; composto sem categoria — custo: ~0,3 h; se paga:
   nunca mostra a errada.

   **Decidido — "Ordem fixa por peso (Recomendado)".** Vai ao P44, e o P45 ao P47 se encaixam na ordem.

2. **R37.2 — `pnpm test`, `npm test`, `pnpm vitest` e `npx vitest` são testes ou pacotes?** Seleção única. Opções:
   testes (recomendada) — gerenciador que roda `test`, `vitest`, `jest` ou o `run-vitest.mjs` é testes, e `install`,
   `add`, `build` e `run build` são pacotes e build — custo: ~0,2 h no P46; só o executor direto — custo: zero.

   **Decidido — "Testes (Recomendado)".** Vai ao P46 e ao P47.

3. **R37.3 — Como dividir os passos entre os workers?** Seleção única. Opções: 3 workers (recomendada) — o P44, o P45,
   o P46 e o P47 em sequência num worker de shell, dono da ordem da lista, e o P48 e o P50 em paralelo, um worker cada;
   4 workers — git e gh, testes e pacotes, P48 e P50; 6 workers, um por passo.

   **Decidido — "3 workers (Recomendado)".**

4. **R37.4 — Que modelo cada worker usa?** Seleção única. Opções: Opus no shell e no Figma (recomendada), Sonnet no
   P48, pela regra da R33.3; Opus só no shell; Sonnet em todos.

   **Decidido — "Opus no shell e no Figma (Recomendado)".**

### Rodada 38 — o que pede a saída da ferramenta, o site do Jira e a miniatura do Figma (enviada 2026-10-28)

> **Apresentado antes**, levantado em `brza-studio@7e9e0d18948`: o `brzaToolLineTitle(call)` só lê o input e é
> chamado em `native-chat-tool-line-label.ts:144` sem o resultado, que já chega à função (`:69-72`), e a linha
> re-renderiza quando ele chega (`NativeChatToolLine.tsx:96-102`); o hash do `git commit` só sai na saída; abrir o diff
> pelo hash não existe pronto, mas há `getRuntimeGitCommitCompare` (`runtime-git-diff-client.ts:60-73`) e
> `openCommitAllDiffs`, presos ao painel de histórico; a saída que passa de 16 KiB chega cortada na cabeça
> (`agent-session-item-wire-form.ts:21`, `structured-agent-session-projection.ts:59`), e o rodapé do teste fica no fim;
> no Claude não vem `exitCode`, só o `isError` (`transcript-record-blocks.ts:90-97`); o MCP da Atlassian traz `cloudId`
> e `issueIdOrKey`, sem a URL, e o domínio que o app conhece é o `JiraSite.siteUrl` do Jira nativo
> (`jira-types.ts:5-13`); o decoder descarta a imagem do `get_screenshot` (`transcript-record-blocks.ts:8-34`), que o
> pedido 30 extrai para arquivo (R36.2); o nome do nó do Figma não vem no input, só o `nodeId`.

Respondida em 2026-10-28, na sessão `pln-001-p44-p50` do `brza-workspace`.

1. **R38.1 — P44: o hash do `git commit`, lido da saída, abre o diff do commit no visualizador?** Seleção única.
   Opções: abre, por função nova (recomendada) — uma `openCommitByHash` do BrzA reusa o `getRuntimeGitCommitCompare` e
   o `openCommitAllDiffs`, no worktree do chat — custo: ~1 h a mais no P44; se paga: na primeira revisão de commit do
   agente; só mostra o hash — custo: zero agora; o clique copia o hash — custo: ~0,2 h.

   **Decidido — "Abre, por função nova (Recomendado)".** O P44 passa a ~2 h.

2. **R38.2 — P46: como contar passou/falhou com a saída cortada nos primeiros 16 KiB?** Seleção única. Opções: rodapé
   se houver, senão passou/falhou (recomendada) — conta pelo rodapé quando ele está na parte que chegou, e na saída
   cortada mostra só o estado, pelo `isError` ou `exitCode` — custo: ~0,3 h, dentro do P46; busca o resto da saída pelo
   `fullOutputItemId` — custo: ~1,5 h a mais e uma leitura por linha cortada; só passou/falhou — custo: ~0,1 h.

   **Decidido — "Rodapé se houver, senão passou/falhou (Recomendado)".**

3. **R38.3 — P48: de onde sai o endereço do site para o chip do Jira e do Confluence?** Seleção única. Opções: `cloudId`,
   senão o Jira do app (recomendada) — o `cloudId` quando é domínio, senão o `siteUrl` da conexão nativa do Jira, e sem
   nenhum o chip só copia a chave — custo: ~0,5 h, dentro do P48; configuração nova — custo: ~1 h e uma tela; o chip
   só copia — custo: ~0,1 h.

   **Decidido — "cloudId, senão o Jira do app (Recomendado)".**

4. **R38.4 — P50: e a miniatura do `get_screenshot`?** Seleção única. Opções: fica para o pedido 30 (recomendada) — o
   P50 entrega o `pen-tool` e o título, cai a ~0,3 h, e o P50.2 vira `[-]` com o link para o pedido 30 — custo: zero;
   o P50 espera o pedido 30; o P50 faz a extração — custo: ~4 a 5 h, em conflito com o desenho do pedido 30.

   **Decidido — "Fica para o pedido 30 (Recomendado)".**

### Rodada 39 — a prévia de imagem: o arquivo, o texto solto, a URL remota e as várias imagens (enviada 2026-10-28)

> **Apresentado antes:** a imagem colada vai para o temp do sistema (`clipboard-image-temp-file.ts:44`,
> `getPath('temp')`), e não há rotina que apague arquivo de sessão excluída; o texto já faz link do caminho de arquivo
> pelo `linkifyFilePaths` (`NativeChatMarkdown.tsx:105`); o `![]()` remoto carrega sozinho
> (`NativeChatMarkdownImage.tsx:131` e `:156`).

Respondida em 2026-10-28, na sessão do `brza-workspace` que desenhou o pedido 30.

1. **R39.1 — Onde fica o arquivo da imagem extraída, e por quanto tempo?** Seleção única. Opções: no temp, como o colar
   (recomendada) — a sessão antiga reaberta dias depois mostra "Preview unavailable", como o anexo — custo: ~0,3 h; se
   paga: agora; no app, com limpeza por idade de 30 dias — custo: ~1,5 h; se paga: na primeira sessão antiga reaberta;
   no app, sem limpeza — custo: ~0,5 h; se paga: na sessão antiga, com o disco sem teto.

   **Decidido — "No temp, como o colar (Recomendado)".**

2. **R39.2 — O caminho ou a URL de imagem solto no texto vira o quê?** Seleção única. Opções: miniatura abaixo do
   parágrafo (recomendada) — o link fica, a miniatura só se o arquivo existir, a mesma imagem uma vez por mensagem —
   custo: ~3 h; se paga: na primeira resposta que cite um print; o clique abre o visualizador, sem miniatura — custo:
   ~1 h; se paga: agora; fica como está — custo: zero; se paga: agora, com a parte 1 só no `![]()`.

   **Decidido — "Miniatura abaixo (Recomendado)".**

3. **R39.3 — A URL http(s) de imagem carrega sozinha?** Seleção única. Opções: sozinha, como hoje (recomendada) —
   custo: zero; se paga: agora; só caminho local, a URL remota solta segue link — custo: -0,5 h; se paga: agora, sem
   requisição de fora.

   **Decidido — "Sozinha, como hoje (Recomendado)".**

4. **R39.4 — Quando a ferramenta devolve mais de uma imagem, a linha mostra quantas?** Seleção única. Opções: até 4,
   com "+N" que abre o visualizador nas demais (recomendada) — custo: ~0,3 h; se paga: na primeira chamada com várias;
   todas — custo: ~0,1 h; só a primeira, com contador — custo: ~0,2 h.

   **Decidido — "Até 4, com +N (Recomendado)".** O visualizador de hoje mostra uma imagem só
   (`PanZoomImageDialog.tsx:64`), sem navegação: o que o "+N" abre vai à R42.

### Rodada 40 — o ícone do git, os títulos, o idioma e as regras da Run (enviada 2026-10-28)

> **Apresentado antes:** a R29.2 fala em "GitBranch ou GitCommit pelo subcomando", e a R35.1 trouxe o logo do Git, que
> o P43 deixou pronto como `git-logo` (`BrzaGitLogo.tsx`); na conferência da chama do BrzA, Anderson disse "o git não
> pegou"; os textos da UI do app são em inglês ("Preview unavailable"); as regras da R33.2 e da R33.4 eram da Run
> anterior, e a leitura da sessão era que valem de novo.

Respondida em 2026-10-28, na sessão `pln-001-p44-p50` do `brza-workspace`.

1. **R40.1 — P44: que ícone a linha de `git` ganha?** Seleção única. Opções: logo do Git em todo git (recomendada) —
   custo: zero; se paga: na hora; logo, e commit com GitCommit — o `git-commit-horizontal` só no `git commit` — custo:
   ~0,1 h; se paga: em sessões com muitos `git status` entre os commits; lucide pelo subcomando, sem o logo — custo:
   ~0,1 h.

   **Decidido — "Logo, e commit com GitCommit".**

2. **R40.2 — Que formato de título e de chip cada categoria usa?** Seleção única. Opções: conjunto A, com chip
   (recomendada) — custo: o estimado dos passos; conjunto B, mínimo — o texto do comando como hoje e só o chip ao lado
   — custo: ~0,5 h a menos.

   **Decidido — "Conjunto A, com chip (Recomendado)"**, na prévia escolhida:

   ```text
   git commit  git commit — <1ª linha da mensagem>   [abc1234] → diff
   git outros  o comando, como hoje (só o ícone muda)
   gh pr       PR #123 — <título>                [#123] → navegador
   gh issue    Issue #45 — <título>              [#45]  → navegador
               (número pela URL na saída; título do --title ou da saída)
   testes      vitest — 12 passed, 1 failed
               vitest — failed   (saída cortada, R38.2)
   pacotes     o comando, como hoje (só o ícone)
   Jira        FIX-123 — <resumo, se vier na saída>   [FIX-123] → navegador
   Confluence  <título da página>                [página] → navegador
   Figma       Figma · <nome do nó, ou o nodeId>
   ```

3. **R40.3 — Em que idioma vai o resultado no título?** Seleção única. Opções: inglês, como o app (recomendada) —
   custo: zero; português — "12 passaram, 1 falhou", "falhou", com as strings no i18n do BrzA — custo: ~0,3 h; se
   paga: só se o app for traduzido inteiro.

   **Decidido — "Português".** Os textos em inglês da prévia da R40.2 saem em português.

4. **R40.4 — As regras da Run e o modelo do P50, sem a miniatura?** Seleção única. Opções: R33.2 e R33.4, e P50 de
   Sonnet (recomendada) — commit e push na `master` com os testes verdes, depois do `git var GIT_AUTHOR_IDENT` e do
   rebase, e os worktrees em `brza-studio/.worktrees/`, passados por `path:`; o shell de Opus e o P48 de Sonnet; R33.2
   e R33.4, e P50 de Opus; push só depois do aviso de Anderson.

   **Decidido — "R33.2 e R33.4, e P50 de Sonnet (Recomendado)".** Reescreve a R37.4 no P50.

### Rodada 41 — o navegador no composto, a corrida de git e os chips no mobile (enviada 2026-10-28)

> **Apresentado antes:** a `brzaCli` só casa fora do comando de navegador, para o globo do upstream ficar
> (`brza-tool-categories.ts:64-65`); o ícone da corrida só sai quando todas as chamadas casam com a mesma definição
> (`runIconName`, `:117-127`), e o GitCommit do commit (R40.1) mistura dois ícones na corrida de git; o chip é
> componente do desktop (`NativeChatToolFileTarget.tsx`), e o título é compartilhado com o mobile.

Respondida em 2026-10-28, na sessão `pln-001-p44-p50` do `brza-workspace`.

1. **R41.1 — No composto com navegador (`orca browser snapshot && git status`), qual ícone vale?** Seleção única.
   Opções: o globo do upstream (recomendada) — as categorias do BrzA só entram fora dele — custo: ~0,1 h no P44; a
   ordem de peso da R37.1, com o navegador abaixo do git — custo: ~0,1 h.

   **Decidido — "O globo do upstream (Recomendado)".**

2. **R41.2 — A corrida com vários `git` e um `git commit` mostra qual ícone?** Seleção única. Opções: o logo do Git
   (recomendada) — o GitCommit fica só na linha do commit — custo: ~0,1 h no P44; GitCommit se houver commit — custo:
   ~0,2 h; terminal, como hoje — custo: zero.

   **Decidido — "O logo do Git (Recomendado)".**

3. **R41.3 — No mobile, os chips entram?** Seleção única. Opções: só o título no mobile (recomendada) — o ícone lucide e
   o título, e os chips só no desktop, como os logos (R29.4) — custo: zero; chips no mobile também — custo: ~1 a 1,5 h.

   **Decidido — "Só o título no mobile (Recomendado)".**

### Rodada 42 — a prévia de imagem: o "+N", o streaming, o corte e a ordem (enviada 2026-10-28)

> **Apresentado antes:** o `PanZoomImageDialog` mostra uma imagem só (`PanZoomImageDialog.tsx:64`); o Mermaid só
> desenha com a mensagem terminada (`NativeChatMarkdown.tsx:141`, `renderMermaid={!streaming}`); o P55 e o P50 tocam a
> linha da ferramenta e o módulo `brza`, e na R33 o rebase de duas listas em paralelo deu conflito. Os passos propostos:
> o P54 (D42, a extração no main, 3 h), o P55 (D43, a faixa na linha, 1,5 h, depois do P54), o P56 (D44, o texto solto,
> 3 h, independente) e o P57 (a conferência das quatro partes com Anderson, 0,3 h), 7,8 h ao todo. A R40 e a R41 estão
> reservadas à sessão `pln-001-p44-p50`.

Respondida em 2026-10-28, na sessão do `brza-workspace` que desenhou o pedido 30.

1. **R42.1 — O que o "+N" da linha abre?** Seleção única. Opções: abre a linha (recomendada) — o corpo mostra todas as
   imagens em faixa com quebra — custo: ~0,2 h; se paga: agora; visualizador com setas ← → — custo: +1 a 1,5 h; se paga:
   com chamadas de muitas imagens frequentes.

   **Decidido — "Abre a linha (Recomendado)".** Vai ao D43 e ao P55.

2. **R42.2 — A miniatura do texto solto aparece quando?** Seleção única. Opções: ao terminar a mensagem, como o Mermaid
   (recomendada) — custo: zero; se paga: agora; assim que o link chega — custo: +0,5 h; se paga: em respostas longas com
   o print no começo.

   **Decidido — "Ao terminar a mensagem (Recomendado)".** Vai ao D44 e ao P56.

3. **R42.3 — O corte dos passos.** Seleção única. Opções: aceitar o P54 ao P57 (recomendada) — um commit por passo —
   custo: 7,8 h; se paga: a cada passo; juntar o P54 e o P55 — custo: o mesmo; se paga: sem commit sem nada visível;
   tirar o P56 por ora — custo: 4,8 h; se paga: agora.

   **Decidido — "Aceitar P54 a P57 (Recomendado)".** É o aceite do desenho do pedido 30.

4. **R42.4 — Quando o P54 ao P56 rodam?** Seleção única. Opções: depois do P44 ao P50 (recomendada) — custo: a espera;
   se paga: no primeiro rebase sem conflito; o P54 e o P56 já, o P55 depois — custo: um worker a mais; se paga: agora,
   com ~6 h adiantadas; tudo já, em paralelo — custo: rebase provável; se paga: só com prazo apertado.

   **Decidido — "Depois do P44 ao P50 (Recomendado)".**

### Rodada 43 — o Package ou o Hammer e o ícone do Confluence (enviada 2026-10-28)

> **Apresentado antes:** a R29.2 deixou "Package ou Hammer" sem regra; o upstream só tem o logo do Jira, e o BookOpen
> já é do Context7 (P51).

Respondida em 2026-10-28, na sessão `pln-001-p44-p50` do `brza-workspace`.

1. **R43.1 — P47: Package ou Hammer?** Seleção única. Opções: Package nos pacotes, Hammer no build (recomendada) —
   `install`, `add` e `pub get` com Package, e `build`, `run build` e `flutter build` com Hammer — custo: ~0,1 h; só
   Package — custo: zero.

   **Decidido — "Package nos pacotes, Hammer no build (Recomendado)".**

2. **R43.2 — P48: que ícone o Confluence ganha?** Seleção única. Opções: lucide `file-text` (recomendada), novo nas
   tabelas de glifos do desktop e do mobile — custo: ~0,1 h; o logo do Jira nos dois — custo: zero; logo do Confluence
   — custo: ~0,3 h e as diretrizes da Atlassian.

   **Decidido — "Lucide `file-text` (Recomendado)".**

### Rodada 44 — o título e a URL da página do Confluence (enviada 2026-10-28)

> **Apresentado antes**, pelo worker do P48 na Run `run_de875fc52a75`: nas transcrições reais do MCP da Atlassian, o
> `cloudId` é UUID, e não domínio, então o site do chip sai do Jira do app (R38.3); só houve saída do
> `createConfluenceContent` (`data.content.{id,title,webUrl}` e `baseUrl`) e do `searchConfluence` (`data.results[]`,
> URL relativa); o `getConfluencePage` nunca foi chamado.

Respondida em 2026-10-28, na sessão `pln-001-p44-p50` do `brza-workspace`.

1. **R44.1 — P48: como o chip do Confluence pega o título e a URL da página?** Seleção única. Opções: leitura defensiva
   (recomendada) — o título por `data.title` ou `data.content.title`, senão o `title` do input; a URL por
   `baseUrl`+`webUrl`, senão `https://<site>/wiki/pages/viewpage.action?pageId=<id>` — custo: ~0,3 h no P48; se paga: na
   primeira página aberta pelo agente; sem URL montada pelo id — custo: ~0,2 h; só o create e o search — custo: ~0,1 h.

   **Decidido — "Leitura defensiva (Recomendado)".** A URL pelo id e a saída do `getConfluencePage` são suposição até a
   conferência.

### Rodada 45 — o sync da v1.4.242: o helper Swift, o P40 e a linha do limite (enviada 2026-10-26)

> **Apresentado antes:** a v1.4.242 corrigiu o mesmo defeito do Swift 6.4 com `--build-system native` (#21145), no
> `build-computer-macos.mjs:30-45` que o P1.1 tinha mudado; medido no merge: o build do helper em 47 s, `lipo` com
> `x86_64 arm64`, e o SwiftPM avisa que "'--build-system native' has been deprecated and will be removed in a future
> release". A v1.4.242 também tirou o Continue da linha do limite (#33392, `d249c21b7f0`): o botão, o
> `retryControl`/`continueControl` das palavras do limite, a frase "Send a message once it resets to continue." e a
> chave `interruptedContinue.usageLimitExplanation` nas 7 línguas. Manteve o `continueUsageLimit`, o
> `usageLimitTurnItemId` e o `usageLimitContinuationOfTurnItemId` do host, e com eles a agenda do main.

Respondida em 2026-10-26, por Anderson na sessão `fixfy-orca`, pelo AskUserQuestion, e levada à sessão do `orca-dev`
(`sync/v1.4.242`). Transcrita dos passos P1, P40 e P41 em 2026-10-28.

1. **R45.1 — O helper Swift do Computer Use depois da v1.4.242.** Opções:
   - a da v1.4.242 (recomendada): o arquivo volta a ser igual ao do upstream; custo: nenhum agora, e ~20 min para trazer
     de volta o `--show-bin-path` quando o SwiftPM remover o `native`; se paga: agora, sem divergência nesse arquivo nas
     próximas sincronizações;
   - manter o nosso `--show-bin-path`: custo: ~5 min agora e um conflito nesse arquivo a cada sincronização em que o
     upstream mexer nele; se paga: no dia em que o SwiftPM remover o `--build-system native`, se o upstream não migrar
     antes.

   **Decidido — "A da v1.4.242 (Recomendado)".** No merge `f57841688f5`, o `build-computer-macos.mjs` é o do upstream,
   e o conserto do Swift 6.4 passou a ser o `--build-system native` (#21145). Se o SwiftPM o remover, volta o nosso
   `--show-bin-path` (~20 min), o do commit `eabec4de25f`. Vai ao P1.

2. **R45.2 — O P40, que se apoiava no Continue da linha.** Opções:
   - botão próprio na linha (recomendada): o "Continuar em outra conta" vira botão próprio, com o menu das outras
     contas, sem o Continue; a objeção do #33392 (o Continue antes do reset bate no mesmo limite) não vale, porque a
     outra conta tem o seu próprio limite; custo: ~15 min para reescrever o P40.2, e a estimativa de 3 h fica; se paga:
     quando o P40 for executado;
   - manter o P40 ao lado do Continue: cabe só com o Continue de volta (a segunda opção da R45.3); custo: nenhum agora;
     se paga: só com essa opção;
   - tirar o P40 do plano: custo: o pedido 26 fica sem a troca de conta no aviso; se paga: nunca, a menos que Anderson
     não o queira mais.

   **Decidido — "Botão próprio na linha (Recomendado)".** O P40.2 foi reescrito, e a estimativa de 3 h fica.

3. **R45.3 — A linha do aviso de limite depois da v1.4.242.** Opções:
   - seguir a v1.4.242 (recomendada): sai o Continue manual, e o "Retomar automaticamente" fica sozinho na linha, só
     com `resetsAt`, com o "Retomada às HH:MM · Cancelar"; a objeção do #33392 não vale para a agenda, que dispara no
     reset + 1 min; sem `resetsAt`, a linha fica sem ação, como na v1.4.242; custo: ~40 min agora, nos 2 trechos da
     linha, no teste e no comentário do componente; se paga: agora, sem conflito no Continue nas próximas
     sincronizações;
   - manter o Continue do `orca-dev`: devolver o botão, a chave nas 7 línguas e o `continueControl`, e ajustar os
     testes da v1.4.242 que exigem a falta dele; custo: ~1,5 h agora, um conflito a cada sincronização que mexer na
     linha ou nas palavras do limite, e a volta do defeito que o #33392 corrigiu; se paga: só se Anderson usa o Continue
     manual depois do reset num limite sem `resetsAt`;
   - tirar também o "Retomar automaticamente": custo: ~1 h para tirar a UI, e o pedido 26 perde a metade entregue; se
     paga: nunca, a menos que Anderson desista do pedido 26.

   **Decidido — "Seguir a v1.4.242 (Recomendado)".** No merge `f57841688f5`, a `NativeChatNoticeRow` mostra o
   `NativeChatUsageLimitAutoResume` sozinho, só no corte atual (`usageLimitTurnItemId` da linha igual ao do chat) e com
   a agenda no mesmo turno; sem `resetsAt`, a linha não tem botão. A agenda do main, o canal e o disparo ao abrir não
   mudam. O teste da linha perdeu o Continue: o do "Retomar automaticamente" roda sobre a linha com as palavras atuais,
   o "sem reset" só confere a falta do botão, e o "tells a chat that has no Continue to send a message" saiu, porque a
   frase saiu do upstream. Os casos da v1.4.242 (reset futuro, passado e desconhecido, e o texto histórico) entraram.
   Vai ao P41.

### Rodada 46 — as conferências no instalado, o P53.4 e o P40 (enviada 2026-10-28)

> **Apresentado antes:** o build instalado (`de3fb921ad1`) contém o `f130a85e578`, o `52f7051a45d` e o `9d289d2b631`,
> e permite conferir o C8, o C9 e o P37.1; o C1 e o C2 pedem o `9b8a3e2e672` e o `fbff699fa58`, que ele não tem; o
> `color: var(--chat-code-foreground)` de `.native-chat-markdown code` (`native-chat-markdown.css:35`) vence a cor do
> link no P53.4; a Run `run_de875fc52a75` não toca o `NativeChatNoticeRow.tsx`, o `NativeChatInterruptedContinue.tsx`
> nem o `use-native-chat-account-switch.ts`, pré-requisitos do P40, que existem na `9a81e65c852`; o `pnpm check:changed`
> sai vermelho no import boundaries já na `9a81e65c852`.

Respondida em 2026-10-28, por Anderson na sessão `pln-001-retomar`, pelo AskUserQuestion, e gravada nos passos fora da
numeração R, para não colidir com a sessão da Run; numerada e transcrita depois da Run. As opções que perderam e o preço
de cada uma não foram gravados no plano: ficam só as escolhidas.

1. **R46.1 — Quando conferir o C8, o C9 e o P37.1.** **Decidido — "Agora, no instalado (Recomendado)".** Vai ao P37,
   ao P52 e ao P53.
2. **R46.2 — A cor do código inline dentro do link (P53.4).** **Decidido — "color: inherit (Recomendado)"**:
   `.native-chat-markdown a code { color: inherit }` no `brza-chat-link.css`; o código mantém a borda e o fundo e segue
   o tom `faint` do link. Vai ao P53.4.
3. **R46.3 — Quem executa o P53.4 e o P40.** **Decidido — "Workers do Orca daqui (Recomendado)"**: um worker Sonnet
   para o P53.4, em `.worktrees/pln-001-p53-4`, e um worker Codex para o P40, como o passo indica, em
   `.worktrees/pln-001-p40`, numa Run separada da `run_de875fc52a75`; a sessão `pln-001-retomar` grava a evidência.
4. **R46.4 — Quando conferir o C1 ao C7, o C10 e o C14.** **Decidido — "Depois da Run, num build só
   (Recomendado)"**: uma instalação para todos. Vai aos `## Casos manuais`.
5. **R46.5 — O botão do P40, à pergunta do worker.** **Decidido — "Menu sempre, como o P36 (Recomendado)"**: "Continue
   in another account" e "Continuar em outra conta", o ícone `UserRound` do `NativeChatAccountPicker` e um
   `DropdownMenu` com as outras contas, também quando só há uma. Vai ao P40.
6. **R46.6 — O push do P53.4 e do P40 com o import boundaries vermelho**, preexistente desde o `9a81e65c852`.
   **Decidido — "Seguir, e o conserto vai ao PLN-002 (Recomendado)".** Vai ao X21 e à issue do import boundaries.

### Rodada 47 — o alinhamento e os outros elementos dos 120 colunas (enviada 2026-10-27)

Respondida em 2026-10-27, por Anderson na sessão `brza-studio-chat-blocos-120-colunas`, para as pendências que o P52
deixava "a perguntar a Anderson com opções". As opções e o preço não foram gravados no plano: ficam só as respostas.

1. **R47.1 — O alinhamento do bloco e da tabela na largura "Total".** **Decidido — "À esquerda", com o texto.** Vai ao
   P52.
2. **R47.2 — Que outros elementos seguem a regra dos 120 colunas.** **Decidido:** o diff de edição (`NativeChatDiffView`
   e as linhas do `NativeChatDiffCard`) e os diagramas e visuais (o Mermaid e o `NativeChatInlineVisual`) seguem a
   regra; a saída de ferramenta não. Vai ao P52.

### Rodada 48 — o tema do chat manda no Markdown e no terminal (enviada 2026-10-29)

> **Apresentado antes:** o levantamento de um subagente Sonnet, só leitura, no `brza-studio`. O chat não tem tema
> próprio: o `NativeChatAppearanceSettings` não tem campo de tema (`src/shared/native-chat-appearance-settings.ts:3-16`)
> e segue o claro/escuro do app, ou, com o `matchTerminalInterface`, o tema do terminal
> (`native-chat-appearance-style.ts:105-158`): a herança vai do terminal ao chat. O olho do Markdown não declara fundo
> e herda o `bg-background` do `body`, `#0a0a0a` no escuro (`main.css:304`, `:662`; inferência, não conferida no app);
> o lápis usa `--editor-surface`, `#1e1e1e` (`rich-markdown-editor.css:9`); o modo código, o Islands Dark, `#191A1C`
> (`islands-dark-theme.ts:9`); o chat, `#161616`, calculado (`main.css:576-584`); e o terminal, o Ghostty Default Style
> Dark, `#282c34` (`src/shared/terminal-themes/defaults.ts:6-7`). O Markdown não tem tema configurável.

Respondida em 2026-10-29, por Anderson na sessão do `brza-workspace` que orquestrou o P54 ao P56, pelo AskUserQuestion.
Os custos são estimativa do levantamento, não medidos.

1. **R48.1 — O que passa a ser o tema do chat.** Seleção única. Opções: seletor novo, com o catálogo de temas do
   terminal (recomendada) — custo: 6 a 9 h; se paga: na hora, é o único jeito de "trocar o tema do chat troca todos";
   o tema do app, com o fundo de hoje do chat — custo: 2 a 3 h; se paga: na hora para o fundo, nunca para trocar o
   tema só do chat.
   **Decidido — "Seletor novo (Recomendado)".** Vai ao D45 e ao P58.
2. **R48.2 — Como o Markdown e o terminal guardam "segue o chat" ou "tema próprio".** Seleção única. Opções: campo
   por superfície, que passa a "próprio" ao escolher um tema (recomendada) — custo: 5 a 7 h; se paga: na hora;
   interruptor por superfície, com o seletor desabilitado enquanto ligado — custo: 4 a 6 h; se paga: na hora, com dois
   cliques para trocar.
   **Decidido — "Interruptor por superfície".** Vai ao D46, ao D47, ao P59 e ao P60.
3. **R48.3 — A tipografia do chat no terminal e no modo código.** Seleção única. Opções: só no texto — o olho e o
   lápis levam a fonte e o tamanho do chat, e o terminal e o modo código, só as cores e o fundo, com a fonte de código
   do chat, que já é a do terminal (recomendada) — custo: 3 a 4 h; se paga: na hora; em tudo — custo: 5 a 7 h; se
   paga: nunca com fonte proporcional, que desalinha o terminal.
   **Decidido — "Só no texto (Recomendado)".** Vai ao D46, ao D47, ao P59 e ao P60.
4. **R48.4 — O "igualar ao terminal" de hoje.** Seleção única. Opções: remover e migrar — quem o tinha ligado fica com
   o tema do terminal como tema do chat, e o terminal segue o chat, sem mudar a tela (recomendada) — custo: 3 a 4 h;
   se paga: na hora; manter os dois sentidos — custo: 5 a 8 h; se paga: nunca, se ninguém usar, com o ciclo chat →
   terminal → chat.
   **Decidido — "Remover e migrar (Recomendado)".** Vai ao D45 e ao P58.

### Rodada 49 — o tema próprio do Markdown, o par claro/escuro, o padrão e o modo código (enviada 2026-10-29)

Respondida em 2026-10-29, por Anderson na mesma sessão, pelo AskUserQuestion, logo depois da R48. Os custos são
estimativa, não medidos.

1. **R49.1 — O tema do Markdown com o "Seguir o chat" desligado.** Seleção única. Opções: seletor próprio, com o
   catálogo do chat e do terminal, ativo só com o interruptor desligado (recomendada) — custo: uns 2 h a mais; se paga:
   na hora; o de hoje, o claro/escuro do app — custo: nenhum; se paga: nunca para trocar o tema só do Markdown.
   **Decidido — "Seletor próprio (Recomendado)".** Vai ao D47 e ao P60.
2. **R49.2 — Um tema do chat, ou um par escuro e claro.** Seleção única. Opções: par, como o terminal, pelo
   claro/escuro do app (recomendada) — custo: uns 1 a 2 h a mais; se paga: na hora; um só — custo: nenhum; se paga: na
   hora, só para quem usa o escuro.
   **Decidido — "Par, como o terminal (Recomendado)".** Vai ao D45 e ao P58.
3. **R49.3 — O tema padrão do chat.** Seleção única. Opções: o visual de hoje, numa entrada "Padrão do BrzA" do
   catálogo, com o fundo de hoje do chat e as cores do terminal (recomendada) — custo: uns 1 h; se paga: na hora, o
   chat não muda e os outros ficam iguais a ele; o tema de hoje do terminal, `#282c34` — custo: nenhum; se paga: na
   hora, mas o chat muda de cor.
   **Decidido — "Visual atual do chat (Recomendado)".** Vai ao D45 e ao P58.
4. **R49.4 — O modo código do Markdown com o "Seguir o chat".** Seleção única. Opções: o fundo e o claro/escuro seguem
   o chat, e a sintaxe fica Islands Dark e light-plus (recomendada) — custo: 2 a 3 h; se paga: na hora, os três modos
   com o mesmo fundo; nada, fica Islands Dark — custo: nenhum; se paga: na hora, com o modo código diferente.
   **Decidido — "Fundo e claro/escuro (Recomendado)".** Vai ao D47 e ao P60.

### Rodada 50 — as mensagens entre sessões no chat (enviada 2026-10-29)

> **Apresentado antes:** o Claude Code grava a mensagem de outra sessão como um turno `isMeta`, "Another Claude session
> sent a message:" seguido de `<agent-message from="…">`, e o leitor do Claude o descarta
> (`src/main/native-chat/transcript-line-decoders-claude.ts:108`; o caso em `transcript-reader.test.ts:107-125`). O chat
> já tem a linha "Message from <nome>" (`NativeChatAgentMessageSenders.tsx:35`), só para o correio do próprio Orca, e o
> `pt.json` não tem a chave `messageFrom`, que cai no inglês. O upstream de 2026-10-29 troca essa linha por um cartão
> com o status do remetente (`7321b066e83`, #34824), também só para o correio do Orca, apoiado em
> `src/shared/agent-session/agent-message-presentation.ts` e `agent-message-display-text.ts`, que não existem no
> `brza-studio`; o `upstream/main` está 1021 commits à frente da `master`.

Respondida em 2026-10-29, por Anderson na sessão do `brza-workspace` que gravou o pedido 31, pelo AskUserQuestion. Os
custos são estimativa, não medidos.

1. **R50.1 — Como fazer.** Seleção única. Opções: um leitor do BrzA e a linha que já existe, com o "Mensagem de" no
   `pt.json` (recomendada) — custo: 3 a 4 h; se paga: agora; o mesmo leitor e o cartão do #34824 trazido agora — custo:
   8 a 12 h, mais conflito no próximo sync; se paga: agora, com o visual igual ao do Orca.
   **Decidido — "Leitor + cartão do upstream".** Vai ao D48, ao D49, ao P62 e ao P63.
2. **R50.2 — Quais mensagens.** Seleção múltipla. Opções: o correio entre sessões (recomendada) — custo: incluso; a
   devolução de subagente, com rótulo próprio — custo: uns 0,5 h a mais.
   **Decidido — "Correio entre sessões (Recomendado)" e "Devolução de subagente".** Vai ao D48 e ao P62.
3. **R50.3 — O clique no nome do remetente.** Seleção única. Opções: só texto agora (recomendada) — custo: nenhum; abre
   a aba da sessão, se aberta no app, pelo nome — custo: 1 a 2 h, não medido.
   **Decidido — "Abre a aba da sessão".** Vai ao D50 e ao P64.
4. **R50.4 — Onde fica registrado.** Seleção única. Opções: o PLN-001, pedido 32 (recomendada); só um worklog.
   **Decidido — "PLN-001, pedido 32 (Recomendado)".**

### Rodada 51 — o rótulo da devolução e quando o pedido 32 roda (enviada 2026-10-29)

Respondida em 2026-10-29, por Anderson na mesma sessão, logo depois da R50.

1. **R51.1 — O rótulo da devolução de subagente.** Seleção única. Opções: "Devolução de <nome>" (recomendada) — custo:
   o 0,5 h da R50.2; se paga: na hora; "Mensagem de <nome>" — custo: nenhum; se paga: na hora, com as duas iguais.
   **Decidido — "Devolução de <nome>" (Recomendado).** Vai ao D48 e ao P62.
2. **R51.2 — Quando o pedido 32 roda.** Seleção única. Opções: depois do pedido 31 (recomendada) — custo: a espera; se
   paga: no rebase; agora, em paralelo, num worktree — custo: uma sessão a mais e um rebase provável; se paga: agora.
   **Decidido — "Agora, em paralelo".** É a autorização do P62 ao P64.

### Rodada 52 — o "Pensou" como o "Perguntou" (enviada 2026-10-29)

> **Apresentado antes:** a linha da pergunta mostra o rótulo, a pergunta cortada na mesma linha, em `text-primary`, e a
> seta `ChevronRight` que abre a pergunta inteira, sumindo da linha (`NativeChatAwaitingInputRow.tsx:62-90`, `:117-121`).
> A linha do raciocínio mostra só o ícone `brain`, "Pensou por {{duration}}" e a seta, e o texto fica no corpo
> recolhido (`NativeChatReasoningRow.tsx`); é o mesmo componente dentro e fora da corrida de comandos
> (`NativeChatToolRunMemberList.tsx:29`). O `pt.json` diz "Perguntado:" (`:19772`).

Respondida em 2026-10-29, por Anderson na sessão do `brza-workspace` que gravou os pedidos 31 e 32, pelo
AskUserQuestion. Os custos são estimativa.

1. **R52.1 — A linha fechada.** Seleção única. Opções: "Pensou por 3s: <texto>", com a duração e o começo do raciocínio
   cortado, e a seta que abre o texto inteiro (recomendada) — custo: 1 a 1,5 h; "Pensou: <texto>", sem a duração —
   custo: o mesmo; se paga: com mais espaço, mas perde a duração.
   **Decidido — "Pensou por 3s: <texto> (Recomendado)".** Vai ao D51 e ao P66.
2. **R52.2 — A cor do texto.** Seleção única. Opções: apagada, como hoje (recomendada) — custo: nenhum; se paga: a
   pergunta segue a única linha em destaque (R29.1); destaque, como o Perguntou — custo: nenhum; se paga: com o
   raciocínio competindo com as perguntas.
   **Decidido — "Apagada, como hoje (Recomendado)".** Vai ao D51 e ao P66.
3. **R52.3 — O rótulo "Perguntado:".** Seleção única. Opções: trocar para "Perguntou:" (recomendada) — custo: uma linha
   no `pt.json`; manter — custo: nenhum; se paga: nunca.
   **Decidido — "Trocar para 'Perguntou:' (Recomendado)".** Vai ao P66.
4. **R52.4 — Quando roda.** Seleção única. Opções: agora, em paralelo, num worktree (recomendada); depois dos pedidos
   31 e 32.
   **Decidido — "Agora, em paralelo (Recomendado)".** É a autorização do P66.

### Rodada 53 — o modo código do Markdown com o esquema oposto ao do app (enviada 2026-10-29)

> **Apresentado antes:** o tema do Monaco é global: o `monaco.editor.setTheme` vale para todos os editores abertos, e o
> Monaco 0.55.1 escreve as cores em `.monaco-editor, .monaco-diff-editor, .monaco-component`
> (`standaloneThemeService.js:339`). O fundo dá para trocar só no Markdown, por variável CSS no contêiner; o esquema da
> sintaxe, Islands Dark ou `vs`, não. Esbarra quando o tema do chat, ou o próprio do Markdown, é claro com o app escuro,
> ou o contrário. Muda o R49.4 nesse caso.

Respondida em 2026-10-29, por Anderson na sessão `pln-001-p60` do `brza-studio`, pelo AskUserQuestion. Os custos são
estimativa.

1. **R53.1 — O Monaco no caso misto.** Seleção única. Opções: fica como hoje — no caso misto, o modo código mantém o
   Islands Dark ou o `vs` com o fundo do app, e com o mesmo esquema segue o fundo do chat (recomendada) — custo: ~0 h;
   se paga: na hora, só perde o caso misto; troca o tema global enquanto o código do Markdown está na tela — custo: 1 a
   2 h; se paga: só sem outro editor de código visível ao mesmo tempo; CSS de tokens por instância, pelas classes
   `mtkN` — custo: 6 a 10 h; se paga: nunca com folga, quebra em atualização do Monaco.
   **Decidido — "Fica como hoje (Recomendado)".** Vai ao D47 e ao P60 (X38).

### Rodada 54 — o "Pensou" no celular e no streaming (enviada 2026-10-29)

> **Apresentado antes:** o app do celular também mostra o "Asked: <pergunta>" na linha
> (`MobileNativeChatAwaitingInputRow.tsx`), e a linha do raciocínio de lá mostra só "Thought for 3s"
> (`MobileNativeChatReasoningRow.tsx`); o D51 só nomeia o desktop. No turno principal, o raciocínio que chega aparece
> na linha ao vivo (`NativeChatTurnActivityLine.tsx`: o spinner, "Pensando" e a seta), e não na `NativeChatReasoningRow`,
> que só aparece em andamento dentro de um subagente que ainda roda.

Respondida em 2026-10-29, por Anderson na sessão `pln-001-pedido-33` do `brza-studio`, pelo AskUserQuestion. Os
custos são estimativa.

1. **R54.1 — O mobile entra no P66?** Seleção única. Opções: mobile junto, com o texto corrido numa função de
   `src/shared` usada pelos dois (recomendada) — custo: +0,3 a 0,5 h; se paga: agora, com as duas linhas iguais nos dois
   apps; só desktop — custo: zero; se paga: quando o chat quase nunca é acompanhado pelo celular.
   **Decidido — "Mobile junto (Recomendado)".** Vai ao D51 e ao P66.
2. **R54.2 — Onde o começo do texto aparece durante o streaming?** Seleção única. Opções: só na linha do raciocínio —
   no subagente que roda, "Raciocínio: <começo>", e a linha ao vivo do turno principal segue "Pensando" com a seta
   (recomendada) — custo: zero a mais; se paga: a linha ao vivo continua mostrando a atividade; na linha ao vivo também
   — custo: +0,3 a 0,5 h; se paga: lê o raciocínio sem abrir, mas a linha muda a cada pedaço que chega.
   **Decidido — "Só na linha do raciocínio (Recomendado)".** Vai ao D51 e ao P66.

### Rodada 55 — as meta-ferramentas do MCP da Atlassian (enviada 2026-10-31)

> **Apresentado antes:** o `atlassianProduct` (`brza-atlassian-tool.ts:25-34`) escolhe o produto só pelo nome da
> ferramenta, e o `match` (`brza-tool-categories.ts:133-141`) recebe o input mas não o passa ao `matchesMcpTool`. Nos
> transcripts da Fixfy, o `executeRead` (53 chamadas), o `executeWrite` (7) e o `executeDestructive` (9), este fora do
> X20, levam `{ cloudId, name, inputs }`, com o `name` da ferramenta interna (`getJiraBoardSprintData`,
> `manageJiraSprint`, `createConfluenceAttachment`); o `discover` (49) leva só `{ query }`, em texto livre. O `inputs`
> não traz o `issueIdOrKey` em que o título do P48 se apoia.

Respondida em 2026-10-31, por Anderson na sessão do workstream `studio` do `brza-workspace`, pelo AskUserQuestion. Os
custos são estimativa.

1. **R55.1 — Até onde vão as linhas do `executeRead`, do `executeWrite` e do `executeDestructive`?** Seleção única.
   Opções: ícone e título curtos — o produto pelo `input.name` e o título com a ferramenta interna, como
   "manageJiraSprint · start" (recomendada) — custo: ~1,5 h; se paga: na primeira sessão de sprint; só o ícone —
   custo: ~1 h; se paga: já, mas a linha não diz o que fez; ícone, título e chip com a chave do card ou da página —
   custo: ~3 h; se paga: só com clique nesses chips, e a maioria das chamadas é de board e sprint.
   **Decidido — "Ícone e título curtos (Recomendado)".** Vai ao P67.
2. **R55.2 — O que fazer com o `discover`?** Seleção única. Opções: o produto pela busca — jira ou confluence na
   query dão o ícone, e o título mostra a busca entre aspas; sem produto, fica como hoje (recomendada) — custo: ~0,5 h;
   se paga: agora; deixar sem categoria — custo: nenhum; se paga: nunca; um ícone genérico da Atlassian para o resto
   do servidor — custo: ~1,5 h, com o SVG novo no desktop e no mobile; se paga: quando essas linhas forem frequentes.
   **Decidido — "Produto pela busca (Recomendado)".** Vai ao P67.

### Rodada 56 — os nomes das meta-ferramentas e a busca longa do `discover` (enviada 2026-10-31)

> **Apresentado antes:** o `implementer` do P67 deixou duas escolhas sem lastro na R55: casou só os três nomes
> (`/^execute(?:read|write|destructive)$/i`) e pôs a busca do `discover` inteira no título, sem cortar.

Respondida em 2026-10-31, por Anderson na sessão do workstream `studio` do `brza-workspace`, pelo AskUserQuestion. Os
custos são estimativa.

1. **R56.1 — Quais nomes de meta-ferramenta entram no casamento?** Seleção única. Opções: os três nomes explícitos
   (recomendada) — custo: nenhum agora; um `executeX` novo fica sem ícone até alguém acrescentar o nome; se paga:
   agora, sem pegar por engano ferramenta futura de outro formato; qualquer `execute*` — custo: ~5 min; ferramenta
   futura cujo `name` não seja a interna ganha título errado; se paga: se a Atlassian criar novos `execute*` iguais.
   **Decidido — "Os três nomes explícitos (Recomendado)".** Fica no P67.
2. **R56.2 — A busca do `discover` vai inteira no título?** Seleção única. Opções: inteira, sem cortar, com o corte do
   CSS (recomendada) — custo: nenhum; se paga: agora; cortar em ~120 caracteres — custo: ~15 min, com um teste, e a
   dica perde o texto; se paga: só com busca enorme na prática.
   **Decidido — "Inteira, sem cortar (Recomendado)".** Fica no P67.

### Rodada 57 — o próximo passo e o mock do lucide no mobile (enviada 2026-10-31)

> **Apresentado antes:** cada um dos sete testes do X47 declara o próprio `vi.mock('lucide-react-native', …)` com a
> lista de ícones à mão, e nenhuma tem os 12 que o `brza-mobile-tool-glyphs.ts` importa desde o P43; o X46 só acrescentou
> os nomes ao teste do raciocínio.

Respondida em 2026-10-31, por Anderson na sessão do workstream `studio` do `brza-workspace`, pelo AskUserQuestion. Os
custos são estimativa.

1. **R57.1 — Qual é o próximo passo?** Seleção única. Opções: o X47, os testes do mobile (recomendada) — custo: ~0,5 h,
   sem Anderson; se paga: agora, pela cobertura das linhas do P43 ao P50 e do P67; as conferências num build — custo:
   ~1 a 1,5 h, com Anderson; se paga: ao fechar o PLN-001; o P37.1 — custo: ~5 min de Anderson, e ~1 h se pedir
   conserto; se paga: agora; o Codex como subagente — custo: ~0,5 h de rodadas; se paga: só na implementação.
   **Decidido — "X47: os testes do mobile (Recomendado)".** Vai ao P68.
2. **R57.2 — Como corrigir os mocks do lucide?** Seleção única. Opções: um mock compartilhado, que devolve um componente
   simulado para qualquer ícone (recomendada) — custo: ~0,7 h, em 8 testes e um arquivo novo; se paga: no próximo glifo
   novo, que já quebrou os testes duas vezes (X46, X47); acrescentar os nomes, como no X46 — custo: ~0,3 h agora e de
   novo a cada glifo; se paga: agora, mas volta a custar.
   **Decidido — "Mock compartilhado (Recomendado)".** Vai ao P68.

### Rodada 58 — o P37 em paralelo com o P68 (enviada 2026-10-31)

> **Apresentado antes:** o menu nativo do processo principal monta as sugestões do `dictionarySuggestions` do Electron
> (`editable-context-menu.ts:208-219`), e o app não configura idioma no corretor, que no macOS é o do sistema. Uma sonda
> com o Electron 43.8.1 do `brza-studio`, num `textarea` e num `contenteditable`, com o `lang` do documento em `en` e em
> `pt-BR`, deu `ortogrfia` → "ortografia", "ortografai" e `refrence` → "refresque"; o `excessão` e o "ortografai"
> sugeridos na primeira conferência não saem marcados nela.

Respondida em 2026-10-31, por Anderson na sessão do workstream `studio` do `brza-workspace`, pelo AskUserQuestion, em
quatro perguntas seguidas. Os custos são estimativa.

1. **R58.1 — O que se faz enquanto o P68 roda?** Opções: o P37.1 (recomendada), a entrevista do Codex como subagente,
   esperar o P68. **Decidido — "P37.1: ortografia (Recomendado)".**
2. **R58.2 — O que apareceu no botão direito sobre a palavra errada?** Opções: sugestões em pt-BR; sublinha, mas sem
   sugestões; sugestões em inglês; nem sublinha. **Resposta — "Sublinha, mas sem sugestões".**
3. **R58.3 — Qual menu abriu?** Opções: o do sistema, em inglês; o do app, no tema do chat; não lembro.
   **Resposta — "Menu do sistema, em inglês".**
4. **R58.4 — Aparecia o "Add to dictionary"?** Opções: não, só Cut/Copy/Paste; sim, mas sem sugestões acima; vou olhar.
   **Resposta — "Sim, mas sem sugestões acima".** Levou à sonda com o `ortogrfia` e à R59.4.

### Rodada 59 — o fim do P68 e o reteste do P37 (enviada 2026-10-31)

> **Apresentado antes:** com o mock compartilhado, os sete arquivos do X47 carregam, e dois testes antigos falham pelo
> comportamento do P43: o `npm test` de `MobileNativeChatMessage.test.ts:697` ganha o `FlaskConical`, e o
> `pnpm vitest run` de `MobileNativeChatToolRun.test.tsx:134` vira "vitest — passou".

Respondida em 2026-10-31, por Anderson na sessão do workstream `studio` do `brza-workspace`, pelo AskUserQuestion. Os
custos são estimativa.

1. **R59.1 — Como acertar os 2 testes?** Seleção única. Opções: trocar por comandos neutros, fora das categorias do
   BrzA, mantendo o que cada teste prova (recomendada) — custo: ~15 min; se paga: agora; afirmar o comportamento novo —
   custo: ~15 min e de novo a cada mudança da linha de teste; se paga: só sem teste próprio da linha, que o P46 já tem;
   deixar vermelho, com issue — custo: 2 falhas conhecidas; se paga: nunca.
   **Decidido — "Trocar por comandos neutros (Recomendado)".** Vai ao P68.
2. **R59.2 — Os outros ~40 mocks à mão do `mobile/` migram?** Opções: sob demanda, quando quebrarem (recomendada) —
   custo: nenhum agora; todos agora — custo: ~1 h. **Decidido — "Sob demanda (Recomendado)".**
3. **R59.3 — O helper responde só a nomes de ícone?** Opções: só ícones, em PascalCase (recomendada) — custo: nenhum;
   qualquer nome — custo: ~5 min, e esconde export que não é ícone. **Decidido — "Só ícones (Recomendado)".**
4. **R59.4 — Com `ortogrfia` no BrzA Studio, vieram sugestões?** Opções: sim, "ortografia" no topo — o P37 fecha sem
   código; não, só "Add to dictionary" — o P37.2 investiga. Primeira resposta, "Sim, \"ortografia\" no topo",
   corrigida por Anderson em texto livre: "digitei errado" e "ortografia não acusa como erro" — a palavra digitada foi a
   certa, e o reteste não valeu. O reteste foi de novo à rodada, com a palavra soletrada: "Com \"ortogrfia\" sublinhada na
   caixa do chat, o que o botão direito mostrou?" — opções: "ortografia" no topo; só "Add to dictionary"; nem
   sublinhou. **Resposta — "\"ortografia\" no topo".** Fecha o P37.

## Passos

Executor "sessão do `brza-studio`" é a sessão aberta em `~/Projects/brza-studio` (antes `orca-dev`), que commita com o
`brz-anderson` e dá push na `master` do `brza-studio` (os feitos até 2026-10-26, na `main` do `orca-dev`, como a
evidência diz); "worker do Orca" é o worker que a sessão que conduz dispara, num worktree em `.worktrees/`. Cada passo
só executa a pedido explícito de Anderson, e os do chat (P33 em diante) se conferem no BrzA Studio, com ele, fora da
trava do PLN-025/P28 da Fixfy (R25.3). Os IDs são os do PLN-025 da Fixfy, e a numeração salta onde o passo foi para
outro plano (R28.2); os P42 em diante são novos, daqui.

A ordem é a de execução, e não a do número: o P34 vem antes do P33 e do P35, porque leva o id da mensagem à barra; o P40
vem depois do P36, de que reaproveita a troca, e o P41 não depende dele; o P43 vem antes do P44 ao P51, porque monta a
base dos ícones, e o P42, o P52 e o P53 não dependem de nenhum; o P54 ao P57 vêm depois do P44 ao P50 (R42.4), o P54
antes do P55, o P56 independente e o P57 por último; o P58 vem antes do P59 e do P60, que não dependem um do outro, e
o P61 por último; o pedido 32 roda em paralelo com o 31 (R51.2), o P62 antes do P63, o P64 depois do P63 e o P65 por
último; o P66 do pedido 33 roda em paralelo com os dois (R52.4).

**Outro runtime** marca o passo que o Codex ou o `agy` podem executar, e o mais indicado vem primeiro, com "indicado". É
leitura, e não decisão: o runtime de cada passo se escolhe no pedido. O Codex e o `agy` abrem só a pedido, numa sessão
interativa, e a rodada que o passo pedir volta à sessão principal do Claude. Os P42 em diante não levam a marca.

### P1 — O build local do `orca-dev` sai em um comando, assinado pela identidade configurada

Executa D1 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: 0,5 h

- [x] **1.** Os três contornos medidos no `config/scripts/build-mac-local.mjs`, só arm64, e a identidade de
      assinatura por variável, com o hardened runtime
- [x] **2.** `pnpm run build:mac` do clone limpo ao `.app`, e o teste do script (`build-mac-local.test.mjs`)
- [x] **3.** Commit e push na `main` do `orca-dev`
- [x] **4.** O build local assina sem o carimbo de tempo da Apple (`mac.timestamp: 'none'` fora do release)

**Evidência:** commit [`eabec4de25f`](https://github.com/brz-anderson/orca-dev/commit/eabec4de25f), autor
`240569289+brz-anderson@users.noreply.github.com`, na `main`. O `build:mac` virou só
`node config/scripts/build-mac-local.mjs`, que roda a cadeia: `pnpm --dir mobile install --frozen-lockfile`, o
`build:desktop`, os três helpers nativos, o `ensure:electron-runtime` e o `electron-builder --mac dir --<arch do host>`.
A identidade sai do `CSC_NAME`, ou ad hoc (`identity: '-'` do electron-builder 26), e nunca da descoberta no Keychain,
que era o que parava a medição: o `build-computer-macos.mjs` e o `electron-builder.config.cjs` achavam sozinhos o
`Apple Development`. Com o `CSC_NAME`, o hardened runtime liga no app e nos helpers, e o `--timestamp` fica só no
release. O contorno do Swift saiu diferente do medido: o `--build-system native` está depreciado no Swift 6.4, e o build
system novo grava os dois triples no mesmo `.build/out/Products/Release`; o script agora copia o produto de cada triple
pelo `--show-bin-path` antes do `lipo`, e o helper sai `x86_64 arm64`. Clone limpo no scratch, `pnpm install
--frozen-lockfile && pnpm run build:mac`: 2 min 22 s, `dist/mac-arm64/Orca.app` de 667 MB, arm64, versão
`1.4.214-local.1792864828830.eabec4de25f1`, `com.stablyai.orca`; `codesign --verify --deep --strict` passa (na medição
falhava) e a assinatura é ad hoc. O `electron-builder` acha `Apple Development: anderson@fixfy.com.br (V72RV8BZY4)` pelo
nome dado no `CSC_NAME` (conferido no `findIdentity`, sem assinar); o build assinado e o hardened runtime ficam para o
P5. Testes: `build-mac-local.test.mjs` (passos e ambiente) e o `windows-cmd-shim-spawn-boundary.test.mjs`, que perdeu a
entrada do script. O `.github/CONTRIBUTING.md` diz o novo `build:mac`. Efeito: o `build:mac` não gera mais o
`latest-mac.yml`, e o "usar build local" do upstream (`src/main/local-builds/`) fica sem entrada; no nosso fluxo o
`.app` troca à mão (D5) e o atualizador está desligado (P2).

**Evidência do item 4:** commit [`b7c21f26f11`](https://github.com/brz-anderson/orca-dev/commit/b7c21f26f11), na
`main`, mesmo autor. O primeiro build assinado do `orca-fixfy` (PLN-028/P5.1) falhou em 19 min 52 s no `codesign
--timestamp` de um `locale.pak` ("A timestamp was expected but was not found"); o `@electron/osx-sign` 1.3.3 assina
arquivo a arquivo e, sem `timestamp`, põe `--timestamp` em cada um (`sign.js:229-233`). O
`electron-builder.config.cjs` agora dá `mac.timestamp: 'none'` quando `isMacRelease` é falso, e o electron-builder
26.15.3 o repassa (`MacTargetHelper.js:183`), o que vira `--timestamp=none`; o release segue com o carimbo (o
`sign-mac-app.mjs` não lê a chave). Os dois `codesign` dos helpers no config (`signMacStandaloneHelper` e
`codesignArgs`) e o do `build-computer-macos.mjs` já só põem `--timestamp` no release, e ficam como estão: medido no
Mac de Anderson com `Apple Development: anderson@fixfy.com.br (V72RV8BZY4)`, o `codesign` sem a flag não carimba (só
`Signed Time`, sem `Timestamp=`) e custa 0,07 s por arquivo, o mesmo de `--timestamp=none`. Teste em
`electron-builder-mac-channel-config.test.mjs`: o release e o hourly sem `mac.timestamp`, o local com `'none'`. Os
testes do config e do `build-mac-local` (52) passam, o `check:code-quality:changed` e o `oxfmt` passam, e o `pnpm tc`
passa. O build assinado de novo fica com a sessão `fixfy-orca`, depois da sincronização no `orca-fixfy`.

**Rodada:** R45.1 — o helper Swift do Computer Use volta a ser o do upstream no merge `f57841688f5` da v1.4.242
(`--build-system native`, #21145); se o SwiftPM o remover, volta o `--show-bin-path` do `eabec4de25f` (~20 min).

**Evidência do X8:** commit `ee06556cb8f`, na `main` do `orca-dev`, com o `--dmg` do `build:mac` e o
`build-mac-local.yml` no `macos-latest` do fork. O teste do alvo `dmg` no `build-mac-local.test.mjs` falha antes e passa
depois, e os testes que varrem os workflows ficam verdes: `build-mac-local` (7), `ci-draft-pr-admission` (79),
`pr-preflight-gates` (42) e `workflow-ref-reachability` (5); o `ci-background-steps` saiu no upstream (#33796), com a
`v1.4.242`. O run `40432265386` saiu `success` em 12 min 3 s. O `orca-macos-arm64.dmg` tem 239 MiB (250705822 bytes),
sha256 `ed412bcdabd40cfa37ffac2a616862f6eaecedc216eb4be03a68ea44f0498145`, `hdiutil verify` válido, `codesign -dv` com
`Signature=adhoc` e `Mach-O thin (arm64)`, e o app é o `1.4.242-local.1793064322587.ee06556cb8fe`. O baixado pede o
"Abrir Mesmo Assim" (Ajustes > Privacidade e Segurança) ou `xattr -dr com.apple.quarantine /Applications/Orca.app`,
que vai às notas do release.

### P2 — O atualizador fica desligado no build local

Executa D2 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: 0,1 h

- [x] **1.** Teste que falha: com o build local, nenhum check de atualização roda
- [x] **2.** O predicado único no lugar das 6 guardas `!app.isPackaged`
- [x] **3.** Os testes de `src/main/updater/` passam; commit e push

**Evidência:** commit [`87befe5ca4e`](https://github.com/brz-anderson/orca-dev/commit/87befe5ca4e), na `main`, mesmo
autor. `isUpdaterEnabled()` em `src/main/updater/updater-enabled.ts`: falso fora do empacotado e na versão com o sufixo
`-local.<ts>.<commit>` que o `build-mac-local.mjs` já carimbava (`ORCA_LOCAL_BUILD_VERSION` → `extraMetadata.version`),
sem plumbing novo de build; troca as 6 guardas. O teste em `src/main/updater.startup-scheduling.test.ts` falhou antes
(`setFeedURL` chamado 3 vezes) e passa depois: com a versão local, nem o setup, nem o foco, nem o menu, nem 25 h de
relógio chamam `setFeedURL`, `checkForUpdates` ou o nudge, e o status remoto diz `unpackaged-build` ("Development
builds must be updated from their source checkout"), sem mexer no contrato remoto. 39 arquivos de teste do atualizador,
dos builds locais e do status remoto, 428 testes, passam; `pnpm tc:node` passa. O `.app` não foi aberto: divide o
`userData` e a trava de instância com o Orca instalado, que estava aberto.

### P6 — O tema Islands Dark no Monaco e no Shiki, no `orca-dev`

Executa D6 · executor: sessão do `brza-studio`

Estimado: 4,5 h · Executado: 0,5 h

- [x] **1.** O tema do Monaco registrado em `monaco-setup.ts`, com as cores do `patch_orca_monaco.py:49-90`, no lugar do
      `vs-dark`
- [x] **2.** O tema do Shiki no `syntax-highlighter.ts`, no lugar do `dark-plus`
- [x] **3.** Os testes do renderer tocado passam; commit e push; o `orca-fixfy` puxa na sincronização seguinte

**Evidência:** commit [`f9c5de8c183`](https://github.com/brz-anderson/orca-dev/commit/f9c5de8c183), na `main`, autor e
committer `240569289+brz-anderson@users.noreply.github.com`. Uma paleta só, em `src/renderer/src/lib/islands-dark-theme.ts`,
com cada cor ligada ao atributo da IDE, gera os dois temas: o do Monaco (`islands-dark`, as mesmas 30 regras e 15 cores
do remendo, `base: 'vs-dark'`, `inherit: false`), registrado por `defineTheme` como passo do `runMonacoSetupSteps`, e o
do Shiki, em escopos TextMate, no lugar do `dark-plus`. Os 6 `isDark ? 'vs-dark' : 'vs'` viraram `monacoThemeName(isDark)`;
o claro segue `vs` e `light-plus`. As cores foram remedidas no `IslandSchemeDark.xml` do Android Studio instalado, com a
herança do Darcula e do Default do `DefaultColorSchemesManager.xml`, e o Shiki ganhou as que o Monarch não distingue: a
declaração de função `#56A8F5`, a tag do doc comment `#67A37C` e o parâmetro de tipo `#16BAAC`. Uma sonda no Shiki
conferiu TS, Python, Kotlin, YAML, JSON, Markdown e diff: o decorator e a anotação do Kotlin em `#B3AE60`, as aspas em
verde, `${}` em laranja com o miolo na cor do texto, `string`/`number` do TS como palavra-chave, a chave do YAML laranja
e a do JSON `#C77DBB`. Testes: os de `syntax-highlighting/` e o `MonacoEditor.system-theme.test.tsx` com as cores
novas; `components/editor/`, `components/automations/` e o destacador, 493 arquivos e 3927 testes, passam; `tc:web` e
`check:code-quality:changed` passam. Achados: o bloco de código do chat só troca a cor dos tokens, e o fundo segue a
superfície do design system; o `.app` não foi aberto, porque divide o `userData` com o Orca instalado — destino de
ambos: a conferência no Orca do PLN-028/P8.

### P25 — O olho no visualizador de Markdown (pedido 14)

Executa D20 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: 0,3 h

- [x] **1.** Teste que falha: na aba do arquivo Markdown, os modos são `preview`, `rich` e `source`, nessa ordem, e o
      padrão é `preview`; na aba de diff, seguem `source` e `rich`, com o padrão `source`
- [x] **2.** `MARKDOWN_EDIT_VIEW_MODES` e `getDefaultMarkdownViewMode` em `markdown-preview-controls.ts`
- [x] **3.** Os testes do editor passam; commit e push; o `orca-fixfy` puxa na sincronização seguinte, e o olho se
      confere no Orca com o PLN-028/P8

**Evidência:** commit [`5ded04d6bd1`](https://github.com/brz-anderson/orca-dev/commit/5ded04d6bd1), na `main`
(`952a232c8ba..5ded04d6bd1`, fast-forward), autor e committer `240569289+brz-anderson@users.noreply.github.com`. Em
`markdown-preview-controls.ts`, `MARKDOWN_EDIT_VIEW_MODES = ['preview', 'rich', 'source']` e o
`getDefaultMarkdownViewMode` devolve `preview` na aba de arquivo Markdown; a aba de diff segue `['source', 'rich']`, com
o padrão `source`. O olho é o `Eye` que o `EditorViewToggle.tsx` já tinha para `preview`, e o modo guardado por arquivo
vence o padrão no `editor-panel-render-model.ts` e no `editor-save-disk-precondition.ts`, sem mudança. O teste
`markdown-preview-controls.test.ts` falhou antes (2 de 8: os modos e o padrão) e passa depois. Testes:
`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/renderer/src/components/editor src/renderer/src/store/slices`
— 7118 passam e 68 pulados (7186); `pnpm tc:web` sai com 0; `pnpm run check:code-quality:changed` sem achado novo. A
conferência no Orca fica com o PLN-028/P8.

### P26 — O build local de Windows sai em um comando (pedido 15)

Executa D21 · executor: sessão do `brza-studio`

Estimado: 2,3 h · Executado: 0,5 h

- [x] **1.** Teste que falha: os passos do build de Windows instalam o `mobile/`, rodam o `build:desktop` e o
      `ensure:electron-runtime` e chamam o `electron-builder --win --x64`, com a `ORCA_LOCAL_BUILD_VERSION` no formato
      que o `isUpdaterEnabled()` reconhece
- [x] **2.** O `config/scripts/build-win-local.mjs`, com o `createLocalBuildVersion` do `build-mac-local.mjs`
      reaproveitado, e o `build:win` apontando para ele
- [x] **3.** Os testes do script e do atualizador passam; o `.github/CONTRIBUTING.md` diz o novo `build:win`; commit e
      push
- [x] **4.** O teste de regressão do `isUpdaterEnabled()` com versão de release (`src/main/updater/updater-enabled.ts:4-9`):
      verdadeiro com `1.4.242` empacotado e falso com `1.4.242-local.1.abc`; rodada de 2026-10-28, "Marcar e levar à
      issue"; commit e push

**Evidência:** commit [`342d85f66c9`](https://github.com/brz-anderson/orca-dev/commit/342d85f66c9), na `main`
(`5ded04d6bd1..342d85f66c9`, fast-forward), autor e committer `240569289+brz-anderson@users.noreply.github.com`. O
`build:win` virou só `node config/scripts/build-win-local.mjs`, que roda a cadeia: `pnpm --dir mobile install
--frozen-lockfile`, o `build:desktop`, o launcher da CLI e o agent hook em Rust para x64 (X1), o
`ensure:electron-runtime` e o `electron-builder --win --x64 --publish never`, com o NSIS padrão do
`electron-builder.config.cjs`. A versão vem do `getLocalBuildIdentity` importado do `build-mac-local.mjs`, sem cópia, na
`ORCA_LOCAL_BUILD_VERSION`, com a `ORCA_BUILD_COMMIT`; o `pnpm` de cada passo sai do `resolvePnpmCliInvocation`, que no
Windows acha o `pnpm.exe` ou o `pnpm.cmd`. Sem assinatura: o hook de assinatura do upstream é inerte sem as variáveis
do SignPath, e os `ORCA_WIN_*` não mudaram. O `build-win-local.test.mjs` falhou antes (módulo ausente) e passa depois:
a ordem dos passos, só `--x64`, os dois executáveis antes do `electron-builder`, e a versão carimbada faz o
`isUpdaterEnabled()` devolver falso. Testes: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts
config/scripts/build-win-local.test.mjs config/scripts/build-mac-local.test.mjs
config/scripts/windows-cmd-shim-spawn-boundary.test.mjs config/scripts/pnpm-cli-invocation.test.mjs src/main/updater
src/main/updater.startup-scheduling.test.ts src/main/local-builds` — 40 arquivos, 454 testes passam;
`pnpm run check:code-quality:changed` sem achado novo. O `.github/CONTRIBUTING.md` diz o `build:win`, o Rust e o
atualizador desligado. O build de Windows não rodou aqui: é o P27.

**Evidência do 4:** commit [`8e708f9790d`](https://github.com/brz-anderson/brza-studio/commit/8e708f9790d), na `master`
do `brza-studio`, pela sessão `pln-001-p56`, autorizada por Anderson em 2026-10-29 ("P56 e os testes pendentes"). O
teste mora em `src/main/updater/updater-enabled.test.ts`, com o `electron` simulado: `1.4.242` empacotado dá verdadeiro,
e `1.4.242-local.1.abc`, falso. É regressão e passou com o código de hoje. `node config/scripts/run-vitest.mjs run
--config config/vitest.config.ts src/main/updater/updater-enabled.test.ts` → 2 passed.

### P27 — O build do `brza-studio` instalado no Windows (pedido 15)

Executa D21 · executor: o 1, a sessão do `brza-studio` num runner Windows do GitHub (X7); o 2 e o 3, Anderson, na
máquina Windows

Estimado: 1 h · Executado: 0,7 h

Pré-requisito: o P26.

- [x] **1.** Clone limpo, `pnpm install --frozen-lockfile` e `pnpm run build:win`; o tempo e o tamanho do instalador
- [ ] **2.** A instalação passa pelo SmartScreen; a versão em "Sobre" termina em `-local.`
- [ ] **3.** O app não procura atualização: o status remoto diz `unpackaged-build`, como no P2

**Evidência:** o 1, pelo runner `windows-2022` do fork, e não pela máquina Windows nem pelo Docker no Mac (X7). Commit
[`68ffa0a223d`](https://github.com/brz-anderson/orca-dev/commit/68ffa0a223d), na `main` (`6285db81bbc..68ffa0a223d`),
com o `.github/workflows/build-win-local.yml`: `workflow_dispatch`, checkout limpo, `pnpm install --frozen-lockfile`,
`pnpm run build:win` e o upload do `dist/orca-windows-setup.exe`. Os testes que varrem todo workflow passam:
`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts config/scripts/ci-draft-pr-admission.test.mjs
config/scripts/ci-background-steps.test.mjs config/scripts/pr-preflight-gates.test.mjs
config/scripts/workflow-ref-reachability.test.mjs config/scripts/build-win-local.test.mjs` — 5 arquivos, 134 testes.
`gh workflow run build-win-local.yml --repo brz-anderson/orca-dev --ref main`, como `brz-anderson`: o run
[`40425512083`](https://github.com/brz-anderson/orca-dev/actions/runs/40425512083) saiu `success` em 8 min 32 s
(00:18:04 a 00:26:36 UTC), sendo 2 min 22 s de install e 4 min 51 s de `build:win`. O log diz `[build:win] local
version 1.4.239-local.1793060470212.68ffa0a223d8`, os typechecks sem erro, `[rebuild] Forcing native rebuild for
win32-x64`, `[verify-packaged-node-pty] OK` (o ConPTY nega o breakaway do MSYS e é dono da árvore de processos),
`[verify-packaged-daemon-entry] OK`, os outros `verify-packaged-*` OK e o NSIS `target=nsis archs=x64 oneClick=true
perMachine=false`. O `[packaged-orcad-template] skipped`: o `build:win` não gera o template do `orcad`, como no Windows.
As linhas `signing with signtool.exe` são do gancho do upstream, inerte sem as variáveis do SignPath: o instalador sai
sem assinatura. O instalador está em
`~/Downloads/orca-dev-windows-1.4.239-local.1793060470212.68ffa0a223d8/orca-windows-setup.exe`, com 186.721.475 bytes
(178 MiB), "PE32 executable (GUI) Intel 80386, for MS Windows, Nullsoft Installer self-extracting archive" (o stub
do NSIS é 32 bits; o app dentro é x64), sha256
`091865ee297014e64465615f42d8b43cd0b660455817d24705dd0bcd6f703d3a`. O artifact `orca-windows-setup-x64` fica no run por
14 dias. O 2 e o 3 seguem com Anderson, no Windows.

### P34 — A barra da mensagem do agente e o Novo Chat (pedido 20)

Executa D27, D28 · executor: sessão do `brza-studio`

Estimado: 4,5 h · Executado: 0,3 h

**Outro runtime:** Codex, indicado, ou `agy` — renderer, com teste de componente

- [x] **1.** O id da mensagem na barra do `NativeChatAgentControls`, pelo `NativeChatAssistantMessageRow.tsx`
- [x] **2.** Teste que falha e o Novo Chat pelo `launchAgentInNewTab` com `promptDelivery: 'draft'`, com uma mensagem
      longa; commit e push

**Evidência:** commit [`273d2cc6420`](https://github.com/brz-anderson/orca-dev/commit/273d2cc6420), na `main`
(`342d85f66c9..273d2cc6420`, fast-forward, depois do rebase sobre o P26), autor e committer
`240569289+brz-anderson@users.noreply.github.com`. O `NativeChatAgentControls` recebe o `messageId` pelo
`NativeChatAssistantMessageRow.tsx`, para o P33 e o P35; o Novo Chat não precisa dele. O botão (`MessageSquarePlus`,
"Novo chat a partir desta mensagem", nos sete locales) chama o `openNativeChatNewChatFromMessage`
(`native-chat-new-chat-from-message.ts`), que lança pelo `launchAgentInNewTab` com `requestedSurface: 'chat'`, o host de
execução da aba (`executionHostIdForStructuredTarget`), o mesmo worktree e o mesmo grupo, e a mensagem — sem as linhas
de visual, como no Copiar — com `promptDelivery: 'draft'`. O contexto vem do `NativeChatRowActionsProvider`, que junta o
do rewind e o do Novo Chat: o `NativeChatStructuredSession.tsx` está no teto de 400 linhas do `max-lines`, e a troca não
lhe soma linha. A mensagem longa: 60 linhas não passam no `canMirrorLaunchDraftToNativeChat`, que só limita o espelho do
rascunho no terminal, e chegam inteiras, porque a rota de chat semeia a caixa sem esse teto
(`seedStructuredAgentLaunchDraft`); que o rascunho fica na caixa sem enviar, o `structured-agent-session-launch.test.ts`
já prova ("keeps launch drafts in the composer without staging or sending a turn"). Só o chat estruturado oferece o
botão (X2). O `native-chat-new-chat-from-message.test.tsx` falhou antes (2 de 3: o botão ausente) e passa depois.
Testes: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/renderer/src/components/native-chat
src/renderer/src/lib/launch-agent-in-new-tab.test.ts src/renderer/src/lib/structured-agent-session-launch.test.ts
src/renderer/src/i18n` — 405 arquivos, 4466 testes passam, antes e depois do rebase; `pnpm tc:web` sai com 0; `pnpm run
check:code-quality:changed` sem achado novo. A conferência no Orca fica com o PLN-028/P8.

### P33 — O Bifurcar (pedido 19)

Executa D27 · executor: sessão do `brza-studio`

Estimado: 18 h · Executado: 0,9 h

**Outro runtime:** Codex, indicado — main e renderer, com o mapeamento do rewind reaproveitado

- [x] **1.** Teste que falha: o id da linha vira o uuid do transcript, e o `forkSession` corta até ele
- [x] **2.** O canal que bifurca e abre a sessão nova com `resume` no fork, numa aba nova do mesmo worktree
- [x] **3.** O botão na barra; a mensagem em andamento; commit e push

**Evidência:** commit [`8eff03d0bb8`](https://github.com/brz-anderson/orca-dev/commit/8eff03d0bb8), na `main`
(`a0110f3a431..8eff03d0bb8`, fast-forward, depois do rebase sobre o P39, o P36, o P35 e o P41), autor e committer
`240569289+brz-anderson@users.noreply.github.com`. O id da linha do agente é a chave do journal
(`claude:<sessão>:<uuid>`); na resposta em streaming o uuid é o do bloco da API (`block:<message.id>:<índice>`), que o
transcript grava como `message.id` e `apiBlockIndex`, e na importada é o uuid do transcript. O
`claude-message-fork.ts` acha a entrada por um ou outro (`parseClaudeSourceBlockId`) e corta nela com o
`forkClaudeTranscript`, o `forkSession(sessionId, {upToMessageId})` que o rewind já usava, extraído do
`claude-rewind-transcript.ts`; a busca da linha (`findClaudeTranscriptRow`) e as contas do registro
(`claudeConfigDirsForRecord`) saíram do `claude-rewind-fork.ts` para os dois. A sessão nova fica ao lado da de origem,
na mesma conta, e a de origem não muda. O canal é o `agentSession.forkThroughMessage` (`sessionId`, `itemId`), sob a
capacidade `agent-session.structured.message-fork.v1`, que vale local e remoto e esconde o botão num host antigo: o
host recusa a linha que não é do agente (`invalid-target`) e a que o transcript ainda não gravou (`not-saved`), e o
adaptador do Claude (`forkThroughMessage`) faz o corte. O renderer abre a sessão nova pelo `resumeFrom` do
"Retomar no chat" do AI Vault, numa aba de chat logo depois da de origem, no mesmo worktree e host. O botão
(`GitFork`, "Bifurcar a partir desta mensagem", nos sete locales) fica na barra do `NativeChatAgentControls`, ao lado
do Novo Chat e do Fixar Capítulo, e se desabilita enquanto bifurca. A mensagem em andamento: a barra não aparece na
resposta que o agente ainda escreve, e a que o transcript ainda não gravou dá o aviso "O Claude ainda não salvou esta
mensagem" sem abrir aba. Só o chat estruturado do Claude oferece o botão (X5). O `claude-message-fork.test.ts` falhou
antes (3 de 3: a função ausente) e passa depois, com o `forkSession` real sobre um transcript em disco; o
`native-chat-fork-from-message.test.tsx` cobre o clique, o "ainda não salvo" e a mensagem em andamento. A `main` vinha
com o `structured-agent-session.test.ts` vermelho depois do P41 (44 métodos, a contagem em 41); o commit a leva a 45,
com o método novo. Testes: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts
src/main/claude/claude-message-fork.test.ts src/main/claude/claude-rewind-transcript.test.ts
src/main/runtime/rpc/methods/structured-agent-session.test.ts
src/main/runtime/rpc/methods/structured-agent-session-wire-contracts.test.ts
src/main/runtime/rpc/methods/structured-agent-session-admission.test.ts
src/main/native-chat/agent-session-wire/structured-agent-session-fork-rewind.test.ts
src/main/claude/claude-structured-session-adapter.test.ts src/shared/protocol-version-published-capabilities.test.ts
src/shared/host-operation-ownership.test.ts src/renderer/src/components/native-chat/native-chat-fork-from-message.test.tsx
src/renderer/src/components/native-chat/native-chat-new-chat-from-message.test.tsx
src/renderer/src/components/native-chat/native-chat-edit-user-message.test.tsx` — 12 arquivos, 212 testes passam; a
suíte larga (as pastas de Claude, RPC, native-chat, i18n e shared) foi interrompida pelo sistema por falta de memória,
com as outras sessões do P33 ao P41 rodando, e não voltou a rodar. `pnpm tc:node` e `pnpm tc:web` saem com 0 depois do último
rebase; `pnpm run check:code-quality:changed` sem achado novo; `verify:rpc-params-catalog`,
`verify:localization-catalogs` e `verify:localization-coverage` saem com 0. A conferência no Orca fica com o
PLN-028/P8.

### P35 — O Fixar Capítulo na régua de prompts (pedido 21)

Executa D29 · executor: sessão do `brza-studio`

Estimado: 8 h · Executado: 0,6 h

**Outro runtime:** Codex, indicado, ou `agy` — estado e componente no renderer

- [x] **1.** Teste que falha: todo capítulo nasce fixado, e o botão desafixa e fixa
- [x] **2.** O destaque dos fixados na régua e o capítulo na prévia; commit e push

**Evidência:** commit [`b0a7ade5ba7`](https://github.com/brz-anderson/orca-dev/commit/b0a7ade5ba7), na `main`
(`65a2506c3c2..b0a7ade5ba7`, fast-forward, depois do rebase sobre o P39 e o P36, com conflito só nos sete locales),
autor e committer `240569289+brz-anderson@users.noreply.github.com`. O capítulo é o turno, pela chave de turno que o
slot já carrega (`turnKey`); a linha de topo passa a chave à barra como `chapterKey`
(`NativeChatTranscriptRow.tsx` → `MessageRow` → `NativeChatAssistantMessageRow.tsx`), e o `messageId` do P34 fica para
o P33. O botão (`Pin`, "Fixar capítulo", nos sete locales) é um alternador com `aria-pressed`, marcado por padrão. O
estado mora no `native-chat-pinned-chapters.ts`: por sessão (`agente:sessionId`), no renderer, pela vida do app, e
guarda só os desafixados, porque todo capítulo nasce fixado. O `NativeChatMessageList` o entrega à barra e à régua
pelo `NativeChatTranscriptContexts`, junto do contexto de disclosure, sem reindentar a lista; por estar na lista, vale
no chat estruturado e na vista de chat sobre o terminal. Na régua, o tique de um capítulo desafixado recua (mais curto
e mais apagado) e os fixados ficam como hoje; o item carregado passa a levar o `turnKey`, como o do outline, e um
steer divide o fixado com o seu turno (`nativeChatRailChapterKey`). A prévia de um capítulo fixado abre com
"Capítulo fixado" acima do prompt e da resposta. O `native-chat-pinned-chapters.test.tsx` falhou antes (3 de 3: o
botão e a marca ausentes) e passa depois. Testes: `node config/scripts/run-vitest.mjs run --config
config/vitest.config.ts src/renderer/src/components/native-chat src/renderer/src/i18n` — 405 arquivos, 4423 testes
passam depois do último rebase (antes dele, um teste do `use-native-chat-context-menu.targets.test.tsx` falhou uma vez
sob carga e passou sozinho três vezes); `pnpm tc:web` sai com 0; `pnpm run check:code-quality:changed` sem achado
novo. A conferência no Orca fica com o PLN-028/P8.

### P36 — O seletor de conta (pedido 22)

Executa D30 · executor: sessão do `brza-studio`

Estimado: 29 h · Executado: 1,2 h

**Outro runtime:** Codex, indicado, do P36.2 ao P36.4 — o P36.1 confere as contas da máquina e fica com o Claude

- [x] **1.** Conferir se o `~/.claude-adm` entra como conta do Orca; se não, o registro dele, com rodada antes por
      somar 4 a 8 h
- [x] **2.** Teste que falha: a troca copia o `.jsonl` para o `projects/` da conta nova e lança com `resume` nela, sem
      `identityMismatch` nem `historyInOtherAccount`
- [x] **3.** O seletor ao lado do de modelo e esforço, e o divisor "Conta trocada - <conta>"
- [x] **4.** Testes; commit e push

**Evidência:** commit [`65a2506c3c2`](https://github.com/brz-anderson/orca-dev/commit/65a2506c3c2), na `main`
(`5f7fdaf68bf..65a2506c3c2`, fast-forward, depois do rebase sobre o P34 e o P39), autor e committer
`240569289+brz-anderson@users.noreply.github.com`. **1:** o login do `~/.claude-adm` (`admin@fixfy.com.br`) já é conta
do Orca instalado, na pasta gerenciada `claude-accounts/d2f4f519…`, ao lado de `anderson@fixfy.com.br`, no
`claudeManagedAccounts` do `profile-state.db`; sem registro nem rodada. As pastas de conta ligam `projects ->
~/.claude/projects`, então a cópia do transcript quase sempre acha o `.jsonl` já lá e não copia. **2:** o
`claude-account-switch.test.ts` monta duas contas com `projects/` próprios: a troca copia o `.jsonl` e a pasta da
sessão (subagentes) para a conta `b`, o registro passa a `accountHome` de `b` com o `accountSwitch`, a reserva seguinte
não leva `identityMismatch` e o lançamento retoma (`resume`) em `b` com a `a` ainda selecionada; um segundo caso cobre o
chat trocado para System default e a conta removida depois da troca (`claudeAccountFolderMissing`). Sem a exceção no
lançamento, o teste falha (relança na `a`). O desenho: o `agentSession.switchAccount` (capacidade
`agent-session.structured.account-switch.v1`) para o agente em repouso, como o `/clear`, chama o
`prepareAccountSwitch` do adaptador do Claude (`claude-account-switch.ts`), que prepara a pasta e copia o transcript, e
grava o registro e o divisor numa transação (`commitAccountSwitchRecord`, recibo no livro de operações); turno ou
pergunta em andamento recusam. A recusa `identityMismatch` segue como era: só a troca escreve a conta. O lançamento
segue o `accountSwitch` do registro em vez da seleção (`prepareClaudeAccountLaunch`), o que tira o
`historyInOtherAccount` desse caminho. **3:** o `NativeChatAccountPicker` fica antes do seletor de modelo e esforço, com
"System default" e as contas do host como o seletor da barra de status, e some sem conta salva; o divisor
`account-switched` diz "Conta trocada - <e-mail>" (pt) e o celular imprime a frase do host. A troca mora no
`useNativeChatAccountSwitch` e chega pelo transporte do composer (`structuredTransport.accountSwitch`); o `switchTo`
devolve falso quando nada mudou, o que o P40 usa para não enviar o Continuar. A sessão nova do Claude sobe no envio
seguinte, como depois do `/clear`; o P40 envia o Continuar depois que o `switchTo` resolve verdadeiro. **4:** o
`structured-agent-session-account-switch.test.ts` (host) cobre a troca com registro, divisor, replay e o envio seguinte
subindo o agente, a conta recusada sem mudar nada e a mensagem em andamento recusando sem parar o agente. Testes:
`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/main/claude/claude-account-switch.test.ts
src/main/native-chat/agent-session-wire/structured-agent-session-account-switch.test.ts
src/shared/native-chat-notice.test.ts src/main/runtime/rpc/methods/structured-agent-session.test.ts
src/main/claude-accounts src/main/claude/claude-structured-launch-account-routing.test.ts
src/main/claude/claude-structured-launch-resolution.test.ts src/renderer/src/i18n …` — 49 arquivos, 570 passam depois
do rebase (um timeout de 60 s em `language-detection-reconciliation.test.tsx`, por carga, passa sozinho). A bateria
ampla (`src/main/runtime src/main/claude src/main/claude-accounts src/main/native-chat src/shared` e o renderer do chat)
passou antes da última refatoração (1940 arquivos), fora o `claude-stop-ack-race.test.ts`, que falha igual na `main`; a
rodada final foi interrompida pelo Claude Code por falta de memória na máquina. `pnpm tc:node`, `tc:web` e `tc:cli`
saem com 0; `pnpm run check:code-quality:changed` sem achado novo; `oxlint` e o ratchet do `max-lines` limpos — o
`claude-profile-router.ts`, o host e o `NativeChatComposer.tsx` estavam no teto, e a troca saiu para módulos próprios.
Sem `.app` aberto; a troca `claude` → `adm` no Orca se confere com o PLN-028/P8.

### P37 — As sugestões de ortografia (pedido 23)

Executa D31 · executor: sessão do `brza-studio`

Estimado: 2 h · Executado: 0,8 h

- [x] **1.** Conferir, no `orca-dev` aberto, o botão direito numa palavra errada da caixa do chat, em pt-BR; se as
      sugestões aparecem, o passo fecha sem código
- [-] **2.** Se não, a correção do idioma ou do menu do chat, com teste; commit e push — sem código: as sugestões
      aparecem (R59.4)

**Rodada:** R46.1 — o 1 se confere agora, no build instalado `de3fb921ad1`; o menu do Chromium com as sugestões do
corretor já é tratado em `use-native-chat-context-menu.tsx:347`.

**Evidência:** conferido por Anderson no BrzA Studio instalado, em 2026-10-31: `ortogrfia` na caixa do chat, com o botão
direito, traz "ortografia" no topo do menu do sistema (R59.4). A primeira conferência usou `excessão`, que o corretor do
macOS marca sem sugestão, e pareceu defeito (R58.2 a R58.4); um primeiro reteste saiu com a palavra certa digitada e
não valeu. A sonda com o Electron 43.8.1 do `brza-studio`, fora do app, deu as mesmas sugestões num `textarea` e num
`contenteditable`, com o `lang` em `en` e em `pt-BR` (R58).

### P38 — O Markdown na caixa de texto (pedido 24)

Executa D32 · executor: sessão do `brza-studio`

Estimado: 18 h · Executado: 1,0 h

**Outro runtime:** Codex, indicado — o risco é a serialização ida e volta, que se testa sozinha

- [x] **1.** A chave nas configurações, desligada por padrão, e o switch em `ChatBehaviorSetting.tsx`
- [x] **2.** Teste que falha: Markdown → nós → Markdown sem perda, com as pílulas de arquivo, imagem e skill
- [x] **3.** As extensões de formatação no `NativeChatPromptEditor.tsx` com a chave ligada; commit e push

**Evidência:** commit [`6285db81bbc`](https://github.com/brz-anderson/orca-dev/commit/6285db81bbc), na `main`
(`8eff03d0bb8..6285db81bbc`, fast-forward, depois do rebase sobre o P39, o P36, o P35, o P41 e o P33), autor e
committer `240569289+brz-anderson@users.noreply.github.com`. A chave `nativeChatMarkdownComposer`, `false` em
`default-global-settings.ts`, entra no grupo `NativeChatGlobalSettings` (X6), e o switch "Modo de visualização
Markdown" fica em `ChatBehaviorSetting.tsx`, com busca, nos sete locales. Ligada, o `NativeChatPromptEditor.tsx` troca o
`StarterKit` reduzido pelo `createRichMarkdownExtensions` do modo de edição do visualizador
(`native-chat-markdown-prompt.ts`, pela escolha em `native-chat-prompt-editor-mode.ts`), com as pílulas e o
placeholder de antes, e mostra o rascunho formatado (`.native-chat-markdown-composer-editor` mantém a caixa do
composer). O que se lê, se envia e se guarda segue em Markdown: as pílulas ganharam `renderMarkdown`, e os tokens de
imagem e de texto colado voltam como pílulas pelo `markdownTokenizer`, e não como links. O cursor fica em offsets do
Markdown — o documento se serializa com um marcador na posição —, e os seletores, a skill, o recall e o valor posto de
fora (o Editar do P39) seguem pelo mesmo contrato: o valor novo entra como texto quando isso o reproduz, e se lê inteiro
como Markdown quando não. O Shift+Enter é o Enter do editor (parágrafo, item, linha de código), porque o Enter envia;
`&`, `<` e `>` chegam ao agente como digitados, e não como entidades HTML. O serializador literal do editor rico ficou
acessível para qualquer documento do schema (`serializeRichMarkdownDocument`); um rascunho guardado pelo outro modo só
se aproveita se lê como o mesmo texto. Testes: o `native-chat-markdown-prompt.test.ts` (8) falhou antes — o módulo
ausente, e depois 3 de 8 sem o Markdown das pílulas — e passa; o `NativeChatPromptEditor.markdown.test.tsx` (5) cobre
a caixa formatada, a skill pelo offset, o Shift+Enter, o valor do Editar e o rascunho do outro modo; os mocks do store
do `native-chat-composer-drop-scope` e do `native-chat-composer-mobile-hold` passaram a dar o `useAppStore` como
função. `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/renderer/src/components/native-chat
src/renderer/src/components/editor src/renderer/src/components/settings src/renderer/src/i18n` — 1053 arquivos, 9273
testes passam (2 arquivos e 3 testes pulados, como antes), sobre o P35; depois do rebase sobre o P41 e o P33, os de
`native-chat`, `settings` e `i18n` — 664 arquivos, 6245 testes; `pnpm tc:web` sai com 0; `pnpm run
check:code-quality:changed` sem achado novo. Fora do escopo: o app móvel não tem a caixa Tiptap, e o servidor remoto só
recebe o texto, que segue em Markdown. A conferência no Orca fica com o PLN-028/P8.

### P39 — O Editar na mensagem do usuário (pedido 25)

Executa D33 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: 0,4 h

**Outro runtime:** Codex, indicado, ou `agy` — botão com teste, num componente que já existe

- [x] Teste do componente; o Editar na barra da mensagem enviada, que acrescenta à caixa e dá foco; commit e push

**Evidência:** commit [`5f7fdaf68bf`](https://github.com/brz-anderson/orca-dev/commit/5f7fdaf68bf), na `main`
(`273d2cc6420..5f7fdaf68bf`, fast-forward), autor e committer `240569289+brz-anderson@users.noreply.github.com`. A barra
da mensagem enviada (`NativeChatUserMessageRow.tsx`) ganha o Editar (`Pencil`, "Editar mensagem", nos sete locales),
depois do copiar, oculto enquanto a mensagem está "Enviando…" e na mensagem de outro agente. O clique chama o
`editNativeChatUserMessage` (`native-chat-edit-user-message.ts`), que leva a mensagem à caixa pelo
`returnMessageToComposer` — o mesmo caminho do Stop, do rewind e do Editar da fila — e pede o foco pelo
`requestNativeChatComposerFocus` da aba. O texto segue a regra do `appendReturnedDraftText`: sozinho na caixa vazia,
abaixo do rascunho com uma linha em branco se houver um (R25.2); as imagens voltam como pílulas. Como a caixa lê o
rascunho do store, a inserção vale também com a chave do P38 ligada. O contexto vem do `NativeChatRowActionsProvider`,
sem linha nova no `NativeChatStructuredSession.tsx`, que está no teto do `max-lines`. O Enviar agora segue no cartão da
fila (R25.1), sem mudança. Só o chat estruturado oferece o botão (X3). O
`native-chat-edit-user-message.test.tsx` falhou antes (3 de 4: o botão ausente) e passa depois (4 de 4). Testes: `node
config/scripts/run-vitest.mjs run --config config/vitest.config.ts src/renderer/src/components/native-chat
src/renderer/src/i18n` — 404 arquivos, 4419 de 4420 testes passam; a falha, no
`use-native-chat-context-menu.targets.test.tsx`, é de tempo sob carga e passa sozinha (8 de 8), sem tocar no que
mudou; `pnpm tc:web` sai com 0; `pnpm run check:code-quality:changed` sem achado novo. A conferência no Orca fica com
o PLN-028/P8.

### P40 — O Continuar em outra conta, no aviso de limite (pedido 26)

Executa D34 · executor: worker Codex do Orca (R46.3)

Estimado: 3 h · Executado: 0,25 h

**Travado pelo P36**, de que reaproveita a troca de conta (R27.1).

**Outro runtime:** Codex, indicado — botão com menu e a ordem troca → envio, com teste

- [x] **1.** Teste que falha: o Continuar só sai depois que a sessão nova sobe na conta escolhida, e nada sai se a troca
      falha
- [x] **2.** O botão próprio "Continuar em outra conta", com o menu das outras contas, na linha do limite, ao lado do
      "Retomar automaticamente" (`NativeChatNoticeRow.tsx`, no ramo do `usageLimitAutoResume`): troca a conta pela
      troca do P36 e depois chama o `continueUsageLimit` (`NativeChatInterruptedContinue.tsx:112`), que a v1.4.242
      manteve; commit e push

**Rodadas:** R45.2 — o botão próprio na linha, sem o Continue que a v1.4.242 tirou (#33392), e as 3 h estimadas
ficam; R46.3 — um worker Codex em `.worktrees/pln-001-p40`, numa Run separada da `run_de875fc52a75`; R46.5 — o
menu sempre, como o P36, com o `UserRound` do `NativeChatAccountPicker`, também quando só há uma outra conta.

**Evidência:** commit [`15b028ba23f`](https://github.com/brz-anderson/brza-studio/commit/15b028ba23f), na `master`
do `brza-studio`, pelo worker Codex `ctx_ec0a6e1f5a6f` da Run `run_edd8afa07cbf`, com o autor conferido. O botão mora
em `src/renderer/src/components/native-chat/brza/BrzaContinueInOtherAccount.tsx`, e o `NativeChatNoticeRow.tsx` o
monta ao lado do "Retomar automaticamente". O `BrzaContinueInOtherAccount.test.tsx` falhava antes, pela falta do
componente, e cobre "hides without another saved account" e "sends Continue only after switching accounts and never
after a failed switch"; o `NativeChatNoticeRow.test.tsx` ganhou "places Continue in another account beside Resume
automatically". `ORCA_BACKGROUND_LAUNCH=1 node config/scripts/run-vitest.mjs run --config config/vitest.config.ts
src/renderer/src/components/native-chat/brza/BrzaContinueInOtherAccount.test.tsx
src/renderer/src/components/native-chat/NativeChatNoticeRow.test.tsx
src/renderer/src/components/native-chat/NativeChatInterruptedContinue.test.tsx` → 3 arquivos, 68 passed, também
depois do rebase. `pnpm tc:web`, `check:code-quality:changed`, o ratchet do `max-lines`, o `oxlint` e o `oxfmt`
passam; o `pnpm check:changed` só fica vermelho no import boundaries, preexistente, em
[O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`](../../work/issues/import-boundaries-vermelho-pelo-external-subcommand.md).
Executado 0,25 h, contra 3 h estimadas. Desvio X21. Falta o C14 com Anderson.

### P41 — O Retomar automaticamente, no aviso de limite (pedido 26)

Executa D35 · executor: sessão do `brza-studio`

Estimado: 11 h · Executado: 1,1 h

**Outro runtime:** Codex, indicado — agenda no main, canal e botão, todos testáveis sozinhos

- [x] **1.** Teste que falha: a agenda grava o reset + 1 min, sobrevive ao restart, dispara o Continuar uma vez só e
      some com uma mensagem enviada antes ou com o Cancelar
- [x] **2.** A agenda persistida no main e o canal que agenda, cancela e lista; o disparo pelo mesmo envio do Continuar
- [x] **3.** Teste que falha e o disparo ao abrir o Orca, junto da retomada do restart, só se o chat ainda está no corte
- [x] **4.** O botão ao lado do Continuar, oculto sem `resetsAt`, e a linha "Retomada às HH:MM · Cancelar"; commit e push

**Rodada:** R45.3 — o "Retomar automaticamente" fica sozinho na linha do limite, como na v1.4.242, e sem `resetsAt`
a linha não tem botão; o que o merge `f57841688f5` mudou no componente e no teste está na rodada.

**Evidência:** commit
[`a0110f3a431`](https://github.com/brz-anderson/orca-dev/commit/a0110f3a431a2a4b4e99002270f7d22d0545955b), com push na
`main` do `orca-dev` (`b0a7ade5ba7..a0110f3a431`), em `feat/native-chat-auto-resume`, rebaseado sobre o P36
(`65a2506c3c2`) e o P35 (`b0a7ade5ba7`). A agenda mora no host do main
(`structured-agent-session-usage-limit-auto-resume.ts`), persistida em `agent-session-usage-limit-auto-resume.json` no
`stateDirectory`, uma por chat, com o turno do corte e o `resetsAt` + 1 min lido da linha do limite no próprio journal;
um relógio de parede a cada minuto aguenta o Mac dormindo. Na hora, a entrada sai do disco antes do envio (uma vez só),
e o host manda o mesmo "Continue where you left off." pelo seu `send`, com `usageLimitContinuationOfTurnItemId`, que
recusa se o chat saiu do corte; um chat que andou (mensagem enviada antes) perde a agenda na leitura ou na hora. O
canal são `agentSession.usageLimitAutoResume`, `…Cancel` e `…List`, sob a capability
`agent-session.usage-limit-auto-resume.v1`; um host antigo não a anuncia, e o botão não aparece. A retomada vencida
dispara quando o host sobe ao abrir o Orca (X4). No renderer, o botão "Retomar automaticamente" fica ao lado do
Continuar só com `resetsAt`, e a linha vira "Retomada às HH:MM · Cancelar", nas 7 línguas. (1) e (3): o teste da agenda
falhou primeiro (2 de 9: o disparo na hora ficava preso) e passou depois da correção, com 9 casos — o reset + 1 min,
nada sem `resetsAt`, o envio uma vez só, o sumiço com mensagem antes, com o chat noutro corte e com o Cancelar, a agenda
no disco para o próximo Orca, o disparo ao abrir e o descarte ao abrir com o chat fora do corte. Comandos, depois do
rebase: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` em 12 arquivos (a agenda, as
capabilities publicadas, o runtime, a varredura de visuais, os limites do Claude, o restart-resume, a
`NativeChatNoticeRow`, o `NativeChatInterruptedContinue` e o Continuar do chat) — 129 passaram; `pnpm tc:node` e
`pnpm tc:web` limpos; `pnpm run check:code-quality:changed` sem achado; `verify:rpc-params-catalog`,
`verify:localization-catalogs`, `verify:localization-coverage` e `check:max-lines-ratchet` ok. Depois do rebase sobre o
P35, de novo os catálogos, o `tc:web` e os testes da linha e da agenda (52). Sem abrir o `.app`; a conferência no Orca é
o PLN-028/P8.

### P42 — O "Perguntou:" em cor de destaque (pedido 27)

Executa D36 · executor: worker do Orca (R33)

Estimado: 0,3 h · Executado: 0,3 h

- [x] **1.** Teste de aparência que falha: o texto da pergunta do agente usa a cor `primary` do tema, a mesma do ✓ de
      opção escolhida, e não o `text-chat-foreground` de hoje, nos três pontos de
      `src/renderer/src/components/native-chat/NativeChatAwaitingInputRow.tsx`: `:76` (a linha fechada), `:113` (a
      pergunta aberta) e `:118` (a lista de perguntas)
- [x] **2.** A troca da cor nos três pontos; os testes do arquivo; commit e push
- [ ] **3.** Conferir no BrzA Studio, com Anderson: uma pergunta respondida, em cor de destaque

**Evidência:** commit [`9b8a3e2e672`](https://github.com/brz-anderson/brza-studio/commit/9b8a3e2e672), na `master` do
`brza-studio`, por um worker do Orca (Sonnet, R33), no worktree `.worktrees/pln-001-p42`. Os três pontos passaram de
`text-chat-foreground` a `text-primary`, a classe do ✓ de opção escolhida (`NativeChatQuestionCard.tsx:242`); o marcador
`faint` da lista não mudou. O teste novo, `NativeChatAwaitingInputRow.test.tsx`, com 3 casos, deu 3 falhas antes e 3
passes depois; `pnpm check:changed --base=origin/master` → 21 checks verdes (sem o `--base`, ele procura `origin/main`).
Falta a conferência no BrzA Studio com Anderson (subpasso 3), também na pergunta aberta, que só aparece com a linha
recortada.

### P43 — A base dos ícones de marca: o módulo do BrzA e os logos SVG (pedido 27)

Executa D37 · executor: worker do Orca (R33); o 4, sessão do `brza-studio`

Estimado: 0,8 h · Executado: 0,85 h

Antes do P44 ao P51, que usam o mapa e o componente que ele monta.

- [x] **1.** O módulo do BrzA para as categorias novas, por exemplo `src/shared/native-chat/tools/brza/`, com uma linha
      de montagem no `CATEGORY_BY_ROW_WORD` de `src/shared/native-chat/tools/native-chat-tool-icon.ts:58`, que é arquivo
      do upstream: os merges de `stablyai/orca` seguem com conflito pequeno
- [x] **2.** O componente do BrzA que desenha o SVG de marca (git, GitHub, Jira, Figma, Firebase) só no desktop, ligado
      ao `NATIVE_CHAT_TOOL_GLYPHS` de `src/renderer/src/components/native-chat/NativeChatToolIcon.tsx`; o mobile
      (`lucide-react-native`) cai no ícone lucide equivalente, porque os ids de ícone são do lucide e compartilhados
      com ele, como diz o comentário do tipo
- [x] **3.** Conferir a licença de cada logo antes de trazer — por exemplo o Simple Icons, CC0 —, e o que o lucide não
      cobre: não tem logo de Jira nem de Firebase, e os de GitHub e Figma estão obsoletos; os testes; commit e push
- [x] **4.** O teste de regressão do recuo de cada logo de marca no mobile
      (`mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.ts`): git → `git-branch`, GitHub →
      `git-pull-request` e Jira → `square-kanban` (X10); rodada de 2026-10-28, "Marcar e levar à issue"; commit e
      push

**Evidência:** commit [`9b85279f57a`](https://github.com/brz-anderson/brza-studio/commit/9b85279f57a), na `master` do
`brza-studio`, por um worker do Orca (Opus, R33), no worktree `.worktrees/pln-001-p43`. O módulo do BrzA é
`src/shared/native-chat/tools/brza/brza-tool-categories.ts`, com o registro `BRZA_TOOL_CATEGORIES` vazio: o P44 ao P51
registram as suas categorias. Os glifos ficam em `src/renderer/src/components/native-chat/brza/brza-tool-glyphs.tsx`
(desktop) e em `mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.ts`. Os logos são o do git, novo
(`BrzaGitLogo.tsx`), e o `GitHubIcon` e o `JiraIcon` do upstream; o Figma e o Firebase ficam no lucide (R35.1). A fonte e
a licença de cada logo estão em `src/renderer/src/components/native-chat/brza/brza-brand-logos.md`. Nos arquivos do
upstream, só montagem: 16 linhas em `native-chat-tool-icon.ts`, 4 no `NativeChatToolIcon.tsx` e 4 no
`MobileNativeChatToolIcon.tsx`. Os testes novos falharam antes, porque o módulo não existia e o glifo era `undefined`.
`run-vitest` em `brza/` (shared e renderer), `native-chat-tool-icon.test.ts`, `NativeChatReasoningRow.test.tsx` e
`NativeChatAwaitingInputRow.test.tsx` → 8 arquivos, 66 passed; `pnpm check:changed --base=origin/master` → 24 checks;
`pnpm typecheck` no `mobile/` → exit 0. Desvios X9 e X10. Nada aparece no app até o P44 ao P51 registrarem categorias.

**Evidência do 4:** commit [`2e263df152f`](https://github.com/brz-anderson/brza-studio/commit/2e263df152f), na `master`
do `brza-studio`, pela sessão `pln-001-p56`. O teste mora em
`mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.test.ts`, com o `lucide-react-native` simulado
por nomes, como o `MobileNativeChatToolRun.test.tsx`: `git-logo` → `GitBranch`, `github-logo` → `GitPullRequest` e
`jira-logo` → `SquareKanban`. É regressão e passou com o código de hoje. `pnpm --dir mobile exec vitest run
src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.test.ts` → 1 passed. O X10 segue a conferir com
Anderson: o teste prende a escolha de hoje, e trocá-la muda o teste junto.

### P44 — O `git` com ícone e título próprios (pedido 27)

Executa D38 · executor: worker do Orca (R37.4); o 4, sessão do `brza-studio`

Estimado: 2,3 h · Executado: 0,9 h

O estimado passou de 1 h a 2 h com o diff pelo hash (R38.1), e a 2,3 h com o teste do 4.

- [x] **1.** Teste que falha: o comando de shell vira categoria segmento a segmento, e no composto vale a de mais peso,
      testes > gh > git > pacotes e build > `brzaCli` (R37.1), com o globo do upstream no comando de navegador (R41.1);
      o `git` ganha o `git-logo`, e o `git commit`, o `git-commit-horizontal` (R40.1); a corrida de git leva o logo
      (R41.2)
- [x] **2.** O título lê a saída (`brzaToolLineTitle(call, result)`); "git commit — <1ª linha da mensagem>", em
      português (R40.3), e o chip do hash, lido da saída, que abre o diff do commit no visualizador por uma
      `openCommitByHash` do BrzA (R38.1), só no desktop (R41.3)
- [ ] **3.** Os testes; commit e push; conferir no BrzA Studio uma linha de `git commit`, com Anderson
- [x] **4.** O teste de regressão do rótulo do upstream para o comando sem categoria do BrzA, no ramo do comando de
      `native-chat-tool-line-label.ts:94-108`: o verbo, o alvo e o título ficam os do upstream; rodada de 2026-10-28,
      "Marcar e levar à issue"; commit e push

**Pendências:** fechadas na R37, R38, R40 e R41.

**Evidência:** commit [`a1213f86859`](https://github.com/brz-anderson/brza-studio/commit/a1213f86859), na `master` do `brza-studio`,
por um worker do Orca (Opus, R37.4) na Run `run_de875fc52a75`, no worktree `.worktrees/pln-001-p44-p47`, que fez o P44 ao P47 em sequência. O
`brza-shell-segments.ts` divide o comando pelo `splitUnquotedSegments`, agora exportado (só o `export` em
`orca-browser-cli-commands.ts`, do upstream), e o `BRZA_SHELL_CATEGORIES` guarda a ordem de peso testes > gh > git >
pacotes e build > `brzaCli`; o comando com navegador fica com o globo. O `git` ganha o `git-logo`, o `git commit` o
`git-commit-horizontal`, e a corrida, o ícone da categoria. O título "git commit — <assunto>" sai do `[branch hash]
assunto` da saída, senão do `-m`. O chip do hash é o `BrzaToolLineChip.tsx` (só desktop), que abre o diff pela
`brza-open-commit-by-hash.ts` (`getRuntimeGitCommitCompare` e `openCommitAllDiffs`, no worktree do chat). Teste novo
`brza-git-category.test.ts` e `BrzaToolLineChip.test.tsx`, falhando antes; `run-vitest` em `tools/`, `brza/` do
renderer, `NativeChatToolLine` e `NativeChatToolRun` → 25 arquivos, 384 passed; `pnpm tc` e o `typecheck` do
`mobile/` → exit 0; `check:changed` → 23 de 24, com a falha no `open-uncommitted-entry.test.ts`, que já falha na
`origin/master`. Desvios X16 e X17. Falta o C3, com Anderson.

**Evidência do 4:** commit [`8850460267c`](https://github.com/brz-anderson/brza-studio/commit/8850460267c), na `master`
do `brza-studio`, pela sessão `pln-001-p56`. O caso entrou em `src/shared/native-chat/tools/brza/brza-tool-line-title.test.ts`,
e não no teste do upstream, para o merge do `stablyai/orca` seguir sem conflito: o `Bash` com `echo done && wc -l
notes.txt` dá `running` rodando e `ran` com o resultado, com o alvo e o título iguais ao comando; o comando longo dá o
alvo do `summarizeToolInput`, cortado com "…", e o título inteiro. É regressão e passou com o código de hoje.
`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts
src/shared/native-chat/tools/brza/brza-tool-line-title.test.ts` → 6 passed.

### P45 — O `gh` de PR e issue com ícone, título e chip (pedido 27)

Executa D38 · executor: worker do Orca (R37.4)

Estimado: 1 h · Executado: 0,1 h

- [x] **1.** Teste que falha: o comando `gh` de PR e issue vira categoria própria, com o ícone GitPullRequest, pelo
      mesmo caminho do P44
- [x] **2.** O título "PR #123 — <título>" e o chip que abre o PR no navegador
- [ ] **3.** Os testes; commit e push; conferir uma linha de PR no BrzA Studio, com Anderson

**Pendências:** fechadas na R37.1 e na R40.2: "PR #123 — <título>" e "Issue #45 — <título>", com o número pela URL
na saída e o título pelo `--title` ou pela saída; o chip só no desktop (R41.3).

**Evidência:** commit [`68abc3821cd`](https://github.com/brz-anderson/brza-studio/commit/68abc3821cd), na `master`, pelo mesmo worker de shell.
`brza-gh-command.ts`: `gh pr` e `gh issue` com o `git-pull-request`; o número pela URL `/pull/N` ou `/issues/N` da
saída; o título pelo `--title`/`-t` ou pela saída do `gh view`, em texto ou JSON; o chip `#N` abre a URL por
`openNativeChatWebLink`. Teste novo `brza-gh-category.test.ts`, falhando antes; `brza/` do shared → 7 arquivos, 37
passed, e do renderer → 4 arquivos, 11 passed; `check:changed` → 22 de 24, com o `format` corrigido e o `import
boundaries` vermelho pela issue das Pendências conhecidas. Desvio X15. Falta o C4, com Anderson.

### P46 — Os testes com ícone e o resultado no título (pedido 27)

Executa D38 · executor: worker do Orca (R37.4)

Estimado: 1,5 h · Executado: 0,3 h

- [x] **1.** Teste que falha: `vitest`, `run-vitest.mjs`, `flutter test` e `pytest` viram a categoria de testes, com o
      ícone FlaskConical, pelo mesmo caminho do P44
- [x] **2.** O passou/falhou contado no título a partir da saída do comando, com um teste por executor
- [ ] **3.** Os testes; commit e push; conferir uma linha de teste passando e uma falhando no BrzA Studio, com Anderson

**Pendências:** fechadas na R37.2, na R38.2 e na R40.2 e R40.3: o gerenciador que roda teste é testes; "<executor> —
12 passaram, 1 falhou" pelo rodapé, e só "passou" ou "falhou" na saída cortada.

**Evidência:** commit [`05aa8af16cc`](https://github.com/brz-anderson/brza-studio/commit/05aa8af16cc), na `master`, pelo mesmo worker de shell.
`brza-test-command.ts`: `vitest`, `jest`, `pytest`, `python -m pytest`, `flutter test`, `node … run-vitest.mjs` e o
gerenciador que roda teste ganham o `flask-conical`; o título conta pelo rodapé de cada executor, em português e com
plural ("1 passou", "2 falharam"), e sem rodapé mostra "<executor> — passou/falhou" pelo `isError`, pelo `exitCode`
ou pelo estado. Teste novo `brza-test-category.test.ts`, um caso por executor, falhando antes; o native-chat do
renderer e do mobile → 381 arquivos, 3.996 passed; depois do rebase, 28 arquivos, 409 passed. O BrzA Studio
reiniciou no meio, e a rodada perdida rodou de novo. Desvios X13 e X14. Falta o C5, com Anderson.

### P47 — Pacotes e build com ícone e título (pedido 27)

Executa D38 · executor: worker do Orca (R37.4)

Estimado: 0,3 h · Executado: 0,15 h

- [x] **1.** Teste que falha: `pnpm`, `npm`, `flutter pub` e o build viram a categoria de pacotes e build, com o ícone
      Package ou Hammer, só ícone e título, sem interação
- [x] **2.** Os testes; commit e push

**Pendências:** fechadas na R37: o lugar na ordem de peso e o `pnpm test` como testes. O Package ou o Hammer por
comando, na R43.1: Package em `install`, `add` e `pub get`, e Hammer em `build`, `run build` e `flutter build`.

**Evidência:** commit [`85469cf3b4d`](https://github.com/brz-anderson/brza-studio/commit/85469cf3b4d), na `master`, pelo mesmo worker de shell.
`brza-package-command.ts`: `package` em `install`, `i`, `ci` e `add` dos gerenciadores e em `flutter pub get|add`;
`hammer` em `build`, `build:*` e `flutter build`; o título segue o comando. Teste novo `brza-package-category.test.ts`,
falhando antes; native-chat de shared, renderer e mobile → 460 arquivos, 5.144 passed; `typecheck` do `mobile/` → exit
0. Desvio X13.

### P48 — O Jira e o Confluence com o chip que abre no navegador (pedido 27)

Executa D39 · executor: worker do Orca (R37.4)

Estimado: 1 h · Executado: 2,2 h

- [x] **1.** Teste que falha: a chamada MCP do Jira ou do Confluence, já identificada pelo `NativeChatMcpIdentity`, vira
      o chip com a chave do card (`FIX-123`, por exemplo) ou o título da página
- [x] **2.** O clique no chip abre o card ou a página no navegador
- [ ] **3.** Os testes; commit e push; conferir uma linha de cada no BrzA Studio, com Anderson

**Pendências:** fechadas na R38.3, na R40.2 e na R41.3: "FIX-123 — <resumo, se vier na saída>" e "<título da página>";
o site pelo `cloudId` quando é domínio, senão pelo `siteUrl` do Jira do app, e sem nenhum o chip só copia; o chip só
no desktop. O Confluence com o `file-text` do lucide (R43.2), e o título e a URL da página pela leitura defensiva (R44.1).

**Evidência:** commit [`fc7f07a8a1e`](https://github.com/brz-anderson/brza-studio/commit/fc7f07a8a1e), na `master`, por um worker do Orca (Sonnet, R37.4) na Run `run_de875fc52a75`,
no worktree `.worktrees/pln-001-p48`. A lógica mora em `brza-atlassian-tool.ts`; no registro, no título e no chip, só
montagem. O Jira ganha o logo do Jira, o Confluence o `file-text`, novo nos glifos do desktop e do mobile. O título é
"FIX-123 — <resumo>", com a chave do `issueIdOrKey` ou do `data.key`, e o resumo de `data.fields.summary`; no
Confluence, o título da página pela leitura defensiva (R44.1). O chip reusa o `BrzaToolLineChip` do P44 e abre por
`openNativeChatWebLink`, com o site pelo `cloudId` quando é domínio, senão pelo Jira do app, senão copia a chave. As
2,2 h são de relógio, com ~35 min de espera do `check:changed` na máquina disputada e o reinício do app. Testes novos
`brza-atlassian-tool.test.ts` e `BrzaToolLineChip.atlassian.test.tsx`, falhando antes; `src/shared/native-chat` e
`brza/` do renderer → 85 arquivos, 1.177 passed; `pnpm tc` e o `typecheck` do `mobile/` verdes. Desvios X18 a X20.
Falta o C6, com Anderson.

### P49 — A ferramenta Skill com ícone e título (pedido 27)

Executa D39 · executor: worker do Orca (R33)

Estimado: 0,3 h · Executado: 0,2 h

- [x] **1.** Teste que falha: a ferramenta Skill ganha o ícone Sparkles e o título "Skill · <nome>"
- [x] **2.** Os testes; commit e push

**Evidência:** commit [`fbff699fa58`](https://github.com/brz-anderson/brza-studio/commit/fbff699fa58), na `master` do `brza-studio`,
que fecha o P49 e o P51, por um worker do Orca (Sonnet, R33), no worktree `.worktrees/pln-001-p49-p51`. As categorias
entram no `BRZA_TOOL_CATEGORIES` do P43, e o título sai de `src/shared/native-chat/tools/brza/brza-tool-line-title.ts`,
ligado por uma atribuição em `native-chat-tool-line-label.ts` (5 linhas do upstream): o alvo e a dica da linha viram
o título, e o verbo segue o do upstream; sem o campo, a linha cai no padrão. Teste novo `brza-tool-line-title.test.ts`,
5 casos, 4 falhando antes; `run-vitest` em `src/shared/native-chat` e no `native-chat` do renderer → 451 arquivos, 5084
passed; `pnpm check:changed --base=origin/master` → 19 checks. Skill: `sparkles` e "Skill · <nome>", pelo campo `skill` ou `name` do input.
Falta conferir uma chamada real no BrzA Studio.

### P50 — O Figma com logo, nome do nó e miniatura (pedido 27)

Executa D39 · executor: worker do Orca (R40.4)

Estimado: 0,3 h · Executado: 0,3 h

Sem a miniatura, que vai ao pedido 30 (R38.4), o passo cai a ~0,3 h (R29.3).

- [x] **1.** Teste que falha: a chamada MCP do Figma vira a linha com o `pen-tool` (R35.1) e "Figma · <nome do nó, ou
      o `nodeId`>", com o nome quando a saída o traz (R40.2)
- [-] **2.** A miniatura do `get_screenshot` na linha — sai pelo pedido 30, em PLN-001/D43 e no P55 (R38.4)
- [ ] **3.** Os testes; commit e push; conferir uma linha de Figma no BrzA Studio, com Anderson

**Pendências:** fechadas na R38.4 e na R40.2.

**Evidência:** commit [`d7f4e5b5618`](https://github.com/brz-anderson/brza-studio/commit/d7f4e5b5618), na `master` do
`brza-studio`, por um worker do Orca (Sonnet, R40.4) na Run `run_de875fc52a75`, no worktree `.worktrees/pln-001-p50`.
A categoria `figma` mora em `src/shared/native-chat/tools/brza/brza-figma-tool.ts`, casada por `/figma/i` no servidor
MCP, com o `pen-tool`, que já estava nas tabelas de glifos (P43); no registro e no título, só a linha de montagem. O
commit traz a assinatura compartilhada `brzaToolLineTitle(call, result?)`, com o `result` passado em
`native-chat-tool-line-label.ts:144`. O título é "Figma · <nome>" quando a saída traz o nome, senão "Figma ·
<nodeId>"; sem nenhum, a linha cai no padrão; com `isError`, cai no `nodeId`. Teste novo `brza-figma-tool.test.ts`, 6
casos, 5 falhando antes; `run-vitest` em `src/shared/native-chat/tools` → 18 arquivos, 252 passed; `pnpm check:changed
--base=origin/master` → 19 checks; `pnpm typecheck` no `mobile/` → exit 0. Desvios X11 e X12. Falta conferir no BrzA
Studio, com Anderson, uma linha de `get_metadata` e uma de `get_design_context` reais.

### P51 — O Firebase e o Context7 com ícone e nome no título (pedido 27)

Executa D39 · executor: worker do Orca (R33)

Estimado: 0,3 h · Executado: 0,2 h

- [x] **1.** Teste que falha: o Firebase ganha o ícone Flame, e o Context7, o BookOpen, com o nome do projeto ou da
      biblioteca no título, sem interação
- [x] **2.** Os testes; commit e push

**Evidência:** o mesmo commit [`fbff699fa58`](https://github.com/brz-anderson/brza-studio/commit/fbff699fa58), na `master` do `brza-studio`,
que fecha o P49 e o P51, por um worker do Orca (Sonnet, R33), no worktree `.worktrees/pln-001-p49-p51`. As categorias
entram no `BRZA_TOOL_CATEGORIES` do P43, e o título sai de `src/shared/native-chat/tools/brza/brza-tool-line-title.ts`,
ligado por uma atribuição em `native-chat-tool-line-label.ts` (5 linhas do upstream): o alvo e a dica da linha viram
o título, e o verbo segue o do upstream; sem o campo, a linha cai no padrão. Teste novo `brza-tool-line-title.test.ts`,
5 casos, 4 falhando antes; `run-vitest` em `src/shared/native-chat` e no `native-chat` do renderer → 451 arquivos, 5084
passed; `pnpm check:changed --base=origin/master` → 19 checks. O Firebase sai com `flame` e "Firebase · <projeto>"
(`project_id`, `projectId`, `project` ou `active_project`), e o Context7 com `book-open` e "Context7 · <biblioteca>"
(`libraryName` ou `libraryId`, sem a barra inicial). Os nomes dos campos são suposição do worker: falta conferir com
chamadas reais no BrzA Studio, sobretudo o Firebase, cujas ferramentas quase não levam o projeto.

### P52 — Os blocos de código e as tabelas com 120 colunas na largura total (pedido 28)

Executa D40 · executor: sessão do `brza-studio`

Estimado: 1 h · Executado: 0,6 h

- [x] **1.** Teste que falha: só com `width === 'full'`, todo bloco de código e toda tabela têm exatamente `120ch` mais
      o padding do bloco, mesmo com conteúdo curto; "Normal" e "Larga" não mudam; o texto corrido segue na largura
      total. A variável, por exemplo `--chat-wide-block-width`, é posta só no ramo `full` do
      `nativeChatAppearanceStyle` (`src/renderer/src/components/native-chat/native-chat-appearance-style.ts`: `:77`
      `maxWidthPx = Number.POSITIVE_INFINITY` e `:88` `--chat-content-max-width: none`; as opções aparecem em
      `src/renderer/src/components/settings/chat-appearance-search.ts:134`), num módulo ou CSS do BrzA, com uma linha
      de montagem nos arquivos do upstream
- [x] **2.** O bloco: o `<pre data-native-chat-code-content>` de `NativeChatCodeBlock.tsx` (`max-w-full` em `:62`,
      dentro do `div` `data-native-chat-code-block` em `:46`) lê a variável; a tabela, na regra de
      `src/renderer/src/components/native-chat/native-chat-markdown.css` (`.native-chat-markdown :is(th, td)` em `:25`
      e o fade de bloco em `:64`) — conferir onde fica o elemento `table` e quem limita a largura dele
- [x] **3.** O `ch` das 120 colunas medido na fonte mono do chat (`--chat-code-font-size`), também para a tabela, para
      as bordas dela e do bloco se alinharem; num painel mais estreito, os dois encolhem até 100% da coluna e rolam na
      horizontal
- [ ] **4.** Os testes; commit e push; conferir no BrzA Studio, na largura "Total", com Anderson: um bloco curto e um
      longo, os dois com 120 colunas; uma tabela com a mesma largura; o painel estreito rolando na horizontal

**Rodada:** R47 — o alinhamento à esquerda, com o texto; o diff de edição, o Mermaid e o visual inline seguem a
regra, e a saída de ferramenta não.

**Evidência:** commits [`f130a85e578`](https://github.com/brz-anderson/brza-studio/commit/f130a85e578) e
[`52f7051a45d`](https://github.com/brz-anderson/brza-studio/commit/52f7051a45d), na `master` do `brza-studio`. A regra
mora em `src/renderer/src/components/native-chat/brza-chat-wide-blocks.css`, sob
`@container style(--chat-width: full)`; o `nativeChatAppearanceStyle` ganhou só `'--chat-width': width`, e os arquivos do
upstream, a moldura da tabela (`brza-chat-wide-table.tsx`) e atributos `data-native-chat-*`. Todas as molduras têm a
mesma borda externa: 120 colunas, mais o `px-3.5` do bloco com linguagem, mais 2px de borda. O bloco sem linguagem mostra
umas 113 colunas antes de rolar, por causa do `pr-16` do botão de copiar. **Desvio do texto do passo:** `120ch` puro dava
~117 colunas, porque o `body` herda `letter-spacing: 0.01em` (0,16px) e o `ch` não o conta. Cada moldura se mede por uma
régua `::before` de altura zero, com 120 zeros na fonte de código, e o diff com numeração soma o gutter por
`attr(data-native-chat-diff-gutter type(<number>))`. Medido numa fixture temporária no Chromium: conteúdo do `pre` com
886px (120 × 7,385); bloco, tabela e Mermaid com 916,2px e bordas alinhadas; os dois diffs quebram logo depois da coluna
120; no painel estreito, tudo encolhe até a coluna e rola; "Normal" não muda. O teste de unidade cobre o `--chat-width`
que a regra consulta. O layout não é testável em jsdom. O visual inline não foi medido, porque precisa de runtime.
`pnpm check:changed`: 20 checks verdes. Falta a conferência no BrzA Studio com Anderson (subpasso 4).

### P53 — Os links do chat em azul claro (pedido 29)

Executa D41 · executor: sessão do `brza-studio`; o 4, worker do Orca (R46.3)

Estimado: 0,3 h · Executado: 1,1 h

- [x] **1.** Teste que falha: o link do chat usa a variável `--chat-link`, `#79C0FF` no tema escuro e `#0969DA` no
      claro, e não o `--chat-foreground-strong` de hoje, em `.native-chat-markdown a`
      (`src/renderer/src/components/native-chat/native-chat-markdown.css:18`)
- [x] **2.** O sublinhado segue com 40% da cor (`color-mix(in srgb, currentColor 40%, transparent)`), e a mensagem com
      tom `faint` segue herdando a cor (`:55`); os testes; commit e push
- [ ] **3.** Conferir um link em azul claro nos dois temas, no BrzA Studio, com Anderson
- [x] **4.** O link sobre código inline também em azul: em 2026-10-28, numa sessão de chat do `brza-workspace`, Anderson
      viu o caminho `~/Projects/fixfy`, escrito como código inline e virado link pelo chat, em branco e não em azul
      ("nesse link, o texto ficou branco e não azul"); o `color: var(--chat-code-foreground)` de
      `.native-chat-markdown code` (`native-chat-markdown.css:35`) vence a cor que o `code` herdaria do link

**Rodada:** R46 — o C8, o C9 e o P37.1 se conferem no instalado (R46.1); o 4 com `color: inherit` no
`brza-chat-link.css` (R46.2), por um worker Sonnet em `.worktrees/pln-001-p53-4` (R46.3).

**Evidência:** commit [`9d289d2b631`](https://github.com/brz-anderson/brza-studio/commit/9d289d2b631), na `master` do
`brza-studio`. O `--chat-link` mora em `src/renderer/src/components/native-chat/brza-chat-link.css`, com o padrão do
`main.css`: `:root` e `.dark`, mais `.native-chat-appearance[data-native-chat-scheme]`, que vem do fundo do terminal no
modo "igualar ao terminal". A linha upstream de `.native-chat-markdown a` passou a ler `var(--chat-link)`; o sublinhado e
a regra do tom `faint` não mudaram, e o `faint` ganha pela especificidade. **Desvio do texto do passo:** sem teste de
unidade, porque a cor é só CSS, e o jsdom não a resolve. Conferido na fixture: `#79C0FF` no escuro e `#0969DA` no claro.
Falta a conferência no BrzA Studio com Anderson (subpasso 3).

**Evidência do 4:** commit [`1a6cbf3e14c`](https://github.com/brz-anderson/brza-studio/commit/1a6cbf3e14c), na `master`
do `brza-studio`, pelo worker Sonnet `ctx_1915e2e41676` da Run `run_edd8afa07cbf`, com o autor conferido. A regra
`.native-chat-markdown a code { color: inherit }` mora no `brza-chat-link.css`, sem arquivo do upstream tocado. O DOM é
`a > code`: o `inlineCodeFileLink` (`comment-markdown-native-chat-file-links.ts:255-269`) embrulha o `inlineCode` num
`link`. `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts
src/renderer/src/components/native-chat/brza-chat-link.test.ts` → 1 arquivo, 1 passed: o teste lê o CSS e afirma a
regra, e falhava antes dela. No Chromium, sobre os dois CSS reais do chat, o `code` dentro do link sai `#79C0FF` no
escuro e `#0969DA` no claro, a cor do `a`; o `code` sem link segue com o `--chat-code-foreground`; a borda, o fundo e o
sublinhado ficam. `pnpm check:changed --base=origin/master` → 20 de 21; o vermelho é o import boundaries, preexistente,
em [O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`](../../work/issues/import-boundaries-vermelho-pelo-external-subcommand.md).
Executado 0,5 h. Desvios X21 e X22. Falta o C10 com Anderson.

### P54 — A imagem da ferramenta extraída para arquivo (pedido 30)

Executa D42 · executor: sessão do `brza-studio`

Estimado: 3 h · Executado: 1,75 h

Depois do P44 ao P50 (R42.4), e antes do P55.

- [x] **1.** Teste que falha, em `src/main/native-chat/brza/brza-tool-result-images.test.ts`: o `brzaToolResultImages`
      de um `content` com `{ type: 'image', source: { type: 'base64', media_type: 'image/png', data } }` devolve um
      `image-ref` com o `path` no temp (`brza-tool-images/<sha256 de 16>.png`), e o arquivo tem os bytes; a mesma imagem
      duas vezes dá o mesmo caminho e um arquivo só; `source.type: 'url'` vira `image-ref` com a `url`; `media_type` fora
      de gif, jpeg, png e webp fica de fora
- [x] **2.** Teste que falha nos dois decoders: o `tool_result` com texto e imagem dá o `output` de hoje e mais o
      `images` — o ao vivo (`claudeToolResults` e `claudeToolBody`, `claude-structured-item-translation.ts:150-163` e
      `:176-187`) e o do histórico (`toolResultBlock`, `transcript-record-blocks.ts:90-97`)
- [x] **3.** O campo `images?: NativeChatImageRefBlock[]` no `NativeChatToolResultBlock` (`native-chat-types.ts:94-104`)
      e no corpo `tool-call` do journal (`agent-session-journal-types.ts:132`), uma linha de montagem em cada decoder e a
      projeção do journal ao renderer; os dois pontos "A conferir no passo" do D42
- [x] **4.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; commit e push

**Evidência:** commit [`44ed13bfec9`](https://github.com/brz-anderson/brza-studio/commit/44ed13bfec9), na `master` do
`brza-studio`, pela sessão `pln-001-p54`, autorizada por Anderson em 2026-10-28 ("siga com P54"). O
`brzaToolResultImages` mora em `src/main/native-chat/brza/brza-tool-result-images.ts`. Grava o base64 em
`<temp>/brza-tool-images/<sha256 de 16>.<ext>` (o jpeg sai `.jpg`) e devolve `image-ref` com o `path`, ou com a `url`. O
campo `images` está no `NativeChatToolResultBlock`, no corpo `tool-call` do journal e no schema do journal, no corpo e no
bloco `tool-result`. Quem o preenche: o `claudeToolResults` e o `claudeToolBody` (ao vivo), o `toolResultBlock` (histórico)
e a projeção ao renderer. Os testes do 1 e do 2 moram em `brza-tool-result-images.test.ts`, com 5 casos: antes da
montagem, os 2 da extração passaram, e os 3 dos decoders e da projeção falharam pela asserção.

`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre o teste novo, o schema e os conjuntos
fechados do journal, a projeção, a tradução do Claude, os decoders do transcript e o sanitize do RPC → 23 arquivos,
307 passed. No commit, o teste novo e o `journal-closed-sets.test.ts` → 2 arquivos, 6 passed.

`pnpm check:changed --base=origin/master` → 20 de 22. Os dois vermelhos são preexistentes:

- o import boundaries, só no `src/cli/external-subcommand.ts`, em
  [O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`](../../work/issues/import-boundaries-vermelho-pelo-external-subcommand.md);
- os unit tests, com 25 testes em 13 arquivos: o updater, os goldens do sidebar com "Orca server", o
  `open-uncommitted-entry`, o `claude-stop-ack-race` e o wire entre versões. Os mesmos 25 falham na `master` limpa, em
  `9747ac2b68d`, com o P54 no `stash`. Dos 58 570 testes relacionados, 58 402 passaram.

**Os dois pontos "A conferir no passo" do D42:**

- **A tradução ao vivo é síncrona.** O `journalClaudeMessage` não espera nada. A gravação vai ao temp do colar
  (`getPath('temp')`, ou `os.tmpdir()` sem o `AppEnvironment`), mas síncrona: `writeFileSync` num `.partial`, depois
  `renameSync`, e o arquivo que já existe não é regravado.
- **O relay ao mobile não rejeita o campo.** O `sanitizeNativeChatRpcBlock` espalha o `tool-result`, e o mobile não
  valida o bloco por schema. O campo segue no relay, e o mobile o ignora (R36.4).

Desvios X23 ao X25.

### P55 — A miniatura na linha da ferramenta (pedido 30)

Executa D43 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: 0,75 h

Depois do P54. Cobre o P50.2 (PLN-001/R38.4).

- [x] **1.** Teste que falha, em `src/renderer/src/components/native-chat/brza/BrzaToolImageStrip.test.tsx`: a linha com
      `result.images` mostra as miniaturas com a linha fechada, abaixo do título; com seis imagens, quatro miniaturas e
      um "+2", cujo clique abre o corpo da linha, com as seis em faixa com quebra; sem `images`, a linha não muda
- [x] **2.** O `BrzaToolImageStrip`, com o `ExpandableMarkdownImage` (`MarkdownImageLightbox.tsx:28`) e a leitura do
      `NativeChatMarkdownImage` (o `useLocalImageSrc` com o acesso `chat-image` e a carga perto da tela), e a linha de
      montagem em `NativeChatToolLine.tsx`, fora do corpo aberto (`:75`)
- [x] **3.** Os testes; commit e push; conferir no BrzA Studio, com Anderson: um `Read` de PNG, um `get_screenshot` do
      Figma e um print do browser, cada um com a miniatura na linha fechada e ampliando no clique — a conferência é o
      C11, aberto, no build único dos casos manuais

**Evidência:** commit [`eca0bf772ba`](https://github.com/brz-anderson/brza-studio/commit/eca0bf772ba), na `master` do
`brza-studio`, pela sessão `pln-001-p55`, autorizada por Anderson em 2026-10-28 ("siga com o P55"). O
`BrzaToolImageStrip` mora em `src/renderer/src/components/native-chat/brza/BrzaToolImageStrip.tsx`, montado por uma
linha em `NativeChatToolLine.tsx`, logo abaixo do botão da linha e fora do `NativeChatExpandable`, com o `body?.images`:
o `body` é o resultado tanto na linha da chamada quanto na do resultado solto. Cada miniatura é o
`NativeChatMarkdownImage` com o `path` ou a `url`. Ele traz o `ExpandableMarkdownImage` e o `PanZoomImageDialog`, o
`useLocalImageSrc` com o acesso `chat-image` e a carga perto da tela. O caminho absoluto do temp resolve pelo
`resolveExplicitFileLinkTargetPath`, e o `chat-image` autoriza fora das raízes pelo tipo do arquivo
(`local-file-access-resolution.ts:215-217`). O tamanho vem das variantes da faixa: `[&_img]:h-24`, `w-auto` e o
`my-0` no gatilho. O "+N" é um quadrado `size-24`, com o rótulo `brza.native-chat.showAllImages` em en e pt.

O teste do 1 mora em `BrzaToolImageStrip.test.tsx`, com 3 casos; antes do componente, os 2 com imagens falharam pela
asserção e o sem imagens passou. Conferido na fixture (`pnpm fixtures:shot`, temporária, fora do commit): 96 px de
altura pela proporção, o "+2" no lugar da quinta, e a linha aberta com as seis em faixa com quebra, acima do corpo.

`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre a pasta `native-chat/brza/`, o
`NativeChatToolLine.test.tsx` e o `NativeChatMarkdown.image-preview.test.tsx` → 9 arquivos, 119 passed.

`pnpm check:changed --base=origin/master --maxWorkers=2` → 19 de 21. Os dois vermelhos são preexistentes:

- o import boundaries, só no `src/cli/external-subcommand.ts`, na issue das Pendências;
- os unit tests, com 2 testes do `open-uncommitted-entry.test.ts` ("opens untracked/unstaged Markdown additions in the
  rich editor"). Os mesmos 2 falham na `master` limpa, em `44ed13bfec9`, com o P55 no `stash`. Dos 19 613 testes
  relacionados, 19 560 passaram.

A primeira corrida do check pegou a `key` por índice (react-doctor `no-array-index-as-key`) e o format da linha de
montagem, corrigidos antes do commit (X28).

Desvios X26 ao X28.

### P56 — A miniatura do caminho ou da URL de imagem solto no texto (pedido 30)

Executa D44 · executor: sessão do `brza-studio`

Estimado: 3 h · Executado: 1,25 h

Não depende do P54 nem do P55; roda depois do P44 ao P50 (R42.4).

- [x] **1.** Teste que falha, num teste do plugin em `src/renderer/src/components/native-chat/brza/` e num caso em
      `NativeChatMarkdown.image-preview.test.tsx`: na mensagem terminada, o `` `/abs/shot.png` `` que existe, o
      `[print](shot.png)` e o `https://…/a.png` ganham a miniatura abaixo do parágrafo, e o link fica; a mesma imagem duas
      vezes, ou já num `![]()`, dá uma miniatura só; o caminho que não existe não mostra nada; o bloco cercado não muda;
      com `streaming`, nada entra
- [x] **2.** O plugin remark do BrzA, ligado pelos `remarkPlugins` da extensão (`NativeChatMarkdown.tsx:68`), e o
      componente que desenha o nó com o `NativeChatMarkdownImage` e some na falha. Conferir a ordem dos plugins: o
      `remarkNativeChatFileLinks` entra depois dos outros (`CommentMarkdown.tsx:367-368`), e o do BrzA precisa ver o link
      que ele cria, ou ler o `inlineCode` com o mesmo teste de existência
- [x] **3.** Os testes; commit e push; conferir no BrzA Studio, com Anderson: uma resposta que cite um print por caminho
      em código inline e outra com uma URL de imagem — a conferência é o C12, aberto, no build único dos casos manuais

**Evidência:** commit [`fc43b03b9ef`](https://github.com/brz-anderson/brza-studio/commit/fc43b03b9ef), na `master` do
`brza-studio`, pela sessão `pln-001-p56`, autorizada por Anderson em 2026-10-29, na sessão do `brza-workspace` ("P56 e
os testes pendentes"). O plugin é o `remarkBrzaImageMentions`, em
`src/renderer/src/components/native-chat/brza/brza-image-mention-markdown.ts`. Ele acha o `link` e o `image` cujo alvo
termina numa extensão de `src/shared/image-file-extensions.ts`, o caminho pelo `routeNativeChatHref` e a URL http(s) pelo
`pathname`. Depois do bloco que nomeia a imagem, entra um nó `div` com o `dataBrzaImageMention`, liberado no sanitize.
O componente, o hook `useBrzaImageMentionExtension` e o `div` que delega ao do visual estão em
`src/renderer/src/components/native-chat/brza/BrzaImageMention.tsx`. Em `NativeChatMarkdown.tsx`, a montagem é o hook,
mais 7 linhas e 1 import. O plugin só entra com a mensagem terminada (`settled: !streaming`).

**A ordem dos plugins.** O `CommentMarkdown` monta a base, o `remarkNativeChatFileLinks`, o math e só então os da
extensão. O do BrzA vem por último e vê o `link` que o de links cria no código inline, só para o caminho que existe. O
caminho que não existe nunca vira link, e por isso não ganha miniatura.

**Uma vez por mensagem.** A resposta que veio em streaming fica cortada em blocos, cada um com o seu parse
(`useMarkdownBlocks`). O plugin recebe o texto da mensagem e guarda a primeira menção de cada imagem num mapa da
mensagem, identificada pela posição do bloco e pela ordem da menção nele. O `![]()` da mesma imagem também reivindica.

**A falha.** A miniatura fica montada, invisível (`invisible h-0`, `inert` e `aria-hidden`), até o `load` da imagem. A
carga perto da tela continua disparando, e o caminho ou a URL que falha não mostra nada.

**Os testes.** O teste do plugin é o `brza-image-mention-markdown.test.ts`, com 4 casos: as três formas, uma por
imagem e nenhuma quando o `![]()` veio antes, os blocos de uma mensagem, e o que não muda (caminho ausente, link que
não é imagem, bloco cercado, item de lista). O caso de `NativeChatMarkdown.image-preview.test.tsx` cobre o streaming
sem nada, os links que ficam, quatro miniaturas montadas e só a autoral visível antes do `load`, e as visíveis depois do
`load` e do `error`. Antes do plugin, o do plugin falhou pelo módulo ausente, e o caso, pela asserção: os links
existiam, sem miniatura.

`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre os dois → 2 arquivos, 39 passed;
`pnpm tc:web` → exit 0.

`pnpm check:changed --base=origin/master --maxWorkers=2` → 20 de 21. O vermelho é o import boundaries, só no
`src/cli/external-subcommand.ts`, preexistente, na issue das Pendências. Os testes unitários passaram.

Desvios X29 ao X31. O mobile não ganha a miniatura, como no P55 (R36.4).

### P57 — A conferência das quatro partes da prévia (pedido 30)

Executa D42, D43 e D44 · executor: Anderson, com a sessão que conduz

Estimado: 0,3 h · Executado: — h

Depois do P55 e do P56.

- [ ] **1.** No BrzA Studio: um `![]()` local e um remoto na resposta do agente; uma imagem colada e uma arrastada, com
      a miniatura na mensagem enviada; o clique amplia, com pan e zoom, nos quatro casos (R36.1)
- [ ] **2.** O Observado e o veredito na linha da evidência

**Evidência:** —

### P58 — O tema do chat, com o "igualar ao terminal" migrado (pedido 31)

Executa D45 · executor: sessão do `brza-studio`

Estimado: 10 h · Executado: 0,8 h

Primeiro do pedido 31; o P59 e o P60 dependem dele.

- [x] **1.** Teste que falha, junto de `native-chat-appearance-style.test.ts`: o resolvedor do tema do chat devolve o
      fundo, a frente, a paleta e o esquema do tema escuro com o app escuro e do claro com o app claro, quando o par
      claro está ligado; o "Padrão do BrzA" dá o canvas de hoje (`#161616` no escuro, `#fff` no claro); um tema do
      catálogo dá o fundo dele com o contraste aplicado pela fórmula do `--chat-canvas` — `src/shared/native-chat-theme.test.ts`,
      ao lado do resolvedor (X33), 4 casos; falhou antes pelo módulo ausente, e depois → 4 passed
- [x] **2.** Teste que falha da migração, em `normalize-loaded-global-settings.test.ts`: com o `matchTerminalInterface`
      ligado, o par de temas do terminal vira o do chat, a fonte e o tamanho do terminal viram os do chat, o contraste
      fica em 100, o terminal fica seguindo o chat e a chave sai; desligado, o chat fica no "Padrão do BrzA" — 2 casos;
      antes → 1 failed | 23 passed, depois → 24 passed. O "terminal seguindo o chat" é o padrão ligado do campo do P59
      (X32)
- [x] **3.** O campo do tema do chat no `NativeChatAppearanceSettings`, com a normalização no renderer e no main; o
      resolvedor; o `nativeChatAppearanceStyle` lendo o tema do chat no lugar do terminal; a migração; a seção do chat
      com o seletor no lugar do interruptor, e os controles de fonte, tamanho e contraste sempre ativos. Os pontos "A
      conferir no passo" do D45 — `brza-studio@9c7fcdebbb0`
- [x] **4.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; commit e push. A conferência no
      app é o C15, no build do pedido 31 — os 15 arquivos de teste tocados → 164 passed; `pnpm tc` → só o erro
      preexistente de `updater-enabled.test.ts:20`; o check, abaixo

**Evidência:** commit [`9c7fcdebbb0`](https://github.com/brz-anderson/brza-studio/commit/9c7fcdebbb0), na `master` do
`brza-studio`, pela sessão `pln-001-p58`, autorizada por Anderson em 2026-10-29, na sessão do `brza-workspace` que
gravou o pedido 31 ("e já execute os passos em paralelo").

**O contrato do resolvedor, que o P59 e o P60 leem sem mudar.** Em `src/shared/native-chat-theme.ts`:

- `resolveNativeChatTheme(settings: NativeChatThemeContext & Partial<Pick<GlobalSettings, 'nativeChatAppearance'>>,
  systemPrefersDark: boolean): NativeChatTheme` — o tema do chat, com o contraste dele. O `NativeChatThemeContext` é
  `Partial<Pick<GlobalSettings, 'theme' | 'terminalCustomThemes'>>`.
- `resolveNativeChatThemePair(pair: NativeChatThemePair | undefined, context: NativeChatThemeContext,
  systemPrefersDark: boolean, contrast = 100): NativeChatTheme` — o mesmo para qualquer par na forma do chat, como o
  tema próprio do Markdown (D47). O `NativeChatThemePair` é `{ themeDark?, useSeparateLightTheme?, themeLight? }`.
- O `NativeChatTheme` devolve: `themeName`; `scheme` (`'dark' | 'light'`) e `followsAppScheme`, verdadeiro só no
  "Padrão do BrzA"; `background` e `foreground`, as cores do tema antes da mistura; `palette`, o `ITheme` inteiro (as 16
  ANSI, o cursor e a seleção) com essas duas cores; `canvas`, o `#rrggbb` que o `--chat-canvas` pinta; `canvasMix`; e
  `foregroundMix`, `strongMix` e `text`, o contraste aplicado ao texto sobre o canvas.
- O "Padrão do BrzA" é o `NATIVE_CHAT_THEME_BRZA_DEFAULT` (`'brza:default'`), em
  `src/shared/native-chat-appearance-settings.ts`: o fundo e a frente do app (`#0a0a0a`/`#fafafa` com 5 % no escuro,
  `#fff`/`#0a0a0a` no claro) e as ANSI do tema padrão do terminal no modo do app. O tema que sumiu volta a ele.
- O seletor é o `ChatThemePairPicker` (`src/renderer/src/components/settings/ChatThemePairPicker.tsx`), com o catálogo
  do terminal mais o "Padrão do BrzA" e a prop `disabled`, para o P60 reusar.

**O resto.** A migração é o `migrateNativeChatAppearanceSettings`, chamado na carga
(`normalize-loaded-global-settings.ts`); a normalização tira a chave antiga em qualquer cliente. O estilo do chat lê o
resolvedor e remapeia as variáveis só com tema do catálogo; o "Padrão do BrzA" segue a raiz, como antes. A fonte, os
tamanhos e o contraste deixaram de ser do terminal, e o Cmd +/- vale sempre. O `mixCssColors` entrou em
`src/shared/terminal-title-contrast.ts`, ao lado do parser de cor que reusa. O web lê o campo pela normalização e não
mudou; o mobile não lê o `nativeChatAppearance`. As traduções novas entraram no `en` e no `pt`, e as quatro antigas
saíram dos sete idiomas. Os 14 testes que usavam a chave antiga passaram ao tema do chat, e os que só provavam o
comportamento retirado saíram.

**O check.** O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 23 de 27, em 1042 s. O format, de 6
arquivos, foi corrigido antes do commit (`oxfmt --check` → correct format). Os outros três vermelhos já estão na
`master` sem esta mudança: o typecheck, por `src/main/updater/updater-enabled.test.ts:20` (`'1.4.242-local.1.abc'` não
cabe no tipo, do `8e708f9790d`); o import boundaries, pelo `external-subcommand.ts`, da issue de mesmo assunto; e os
testes unitários, pelos 2 casos de `open-uncommitted-entry.test.ts` (`'preview'` em vez de `'rich-editor'`), que dão
2 failed | 3 passed com e sem a mudança (`git stash`).

### P59 — O terminal segue o chat (pedido 31)

Executa D46 · executor: sessão do `brza-studio`

Estimado: 4 h · Executado: 1,5 h

Depois do P58; não depende do P60.

- [x] **1.** Teste que falha, junto de `terminal-theme.test.ts`: com o "Seguir o chat" ligado, o tema do xterm tem o
      fundo do canvas do chat e as cores ANSI do tema do chat, e a fonte e o tamanho do terminal; desligado, o tema de
      hoje, com os overrides e a opacidade — 2 casos em
      `src/renderer/src/components/terminal-pane/terminal-appearance.test.ts`, onde o harness do xterm já estava: o
      "Padrão do BrzA" dá `#161616` com as ANSI do Ghostty, o Dracula do chat dá o fundo e o vermelho dele, a opacidade
      vale por cima, e a fonte e o tamanho são os do terminal; antes → 1 failed | 30 passed, pelo fundo do tema próprio;
      depois → 31 passed. Mais 1 caso em `terminal-theme.test.ts`, do modo e do divisor (X41)
- [x] **2.** O campo do interruptor nas configurações globais, ligado por padrão; a escolha do tema em
      `terminal-theme-selection.ts` e a aplicação em `terminal-appearance.ts` lendo o resolvedor do P58; o interruptor
      em `TerminalThemeSections.tsx`, com o seletor de hoje desabilitado enquanto ligado — o `terminalFollowsChatTheme`
      (X44); o `resolveTerminalChatTheme`, em `src/shared/terminal-chat-theme.ts`, lido pelo
      `resolveEffectiveTerminalAppearance`, por onde passam o `applyTerminalAppearance` e as outras superfícies (X43); o
      "Seguir o chat" em `TerminalThemeSections.tsx`, com o `ThemePicker` inerte e o "Match dark mode" desabilitado,
      e o caso dele em `TerminalThemeSections.lifecycle.test.ts` — `brza-studio@697ee59c0bf`
- [x] **3.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; commit e push. A conferência no
      app é o C16 — os 9 diretórios que leem o tema do terminal e as configurações → 5 failed | 3563 passed, em
      arquivos, com 20 casos vermelhos: 19 do tema próprio do upstream, ajustados (X44), e 1 preexistente em
      `runtime-environment-store.test.ts` (o "this Orca itself" do rebrand); depois do rebase sobre o P60 e o P62, 803
      arquivos → 7492 passed; o check, abaixo

**Evidência:** commit [`697ee59c0bf`](https://github.com/brz-anderson/brza-studio/commit/697ee59c0bf), na `master` do
`brza-studio`, pela sessão `pln-001-p59`, autorizada por Anderson em 2026-10-29, na sessão do `brza-workspace` que
gravou o pedido 31 ("e já execute os passos em paralelo"). O resolvedor do P58 não mudou.

**Como ficou.** Ligado, o tema do xterm é o `palette` do `resolveNativeChatTheme` com o `background` trocado pelo
`canvas`; o `composeActiveTerminalTheme` aplica por cima os overrides e a opacidade, como antes. A fonte, o tamanho, o
peso e a altura de linha continuam do terminal. Desligado, nada muda. A semente do OSC 10/11 no main, antes de o
renderer publicar, usa o `resolveSavedTerminalColors`, que segue o chat do mesmo jeito. As traduções novas entraram no
`en` e no `pt`, e a busca das configurações acha o "Seguir o chat". O mobile recebe o tema pelo
`resolveMobileTerminalTheme`, que lê a mesma função, e não ganha o interruptor.

**O check.** O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 21 de 26, em 1781 s. O oxlint e o gate de
qualidade apontaram um `as () => void` num teste novo, trocado por checagem de tipo antes do commit
(`check-changed-code-quality.mjs` → passed; `oxlint` → exit 0). Os outros três vermelhos são os do P58 e do P60, já na
`master` sem esta mudança: o typecheck, por `src/main/updater/updater-enabled.test.ts:20`; o import boundaries, pelo
`external-subcommand.ts`; e os testes unitários, pelos 2 casos de `open-uncommitted-entry.test.ts` e pelos 2 de
`cross-version-agent-session-wire.unit.test.ts`, que dão 4 failed | 43 passed num worktree limpo da `origin/master`.

### P60 — O visualizador de Markdown segue o chat (pedido 31)

Executa D47 · executor: sessão do `brza-studio`

Estimado: 8 h · Executado: 1,5 h

Depois do P58; não depende do P59.

- [x] **1.** Teste que falha, com o "Seguir o chat" ligado: o olho e o lápis têm o fundo do canvas do chat, a fonte e o
      tamanho do chat, e o esquema do chat; o modo código tem o fundo do chat e o tema de sintaxe do esquema do chat;
      desligado, os três têm o fundo e o esquema do tema próprio escolhido —
      `src/renderer/src/components/editor/markdown-surface-theme.test.ts`, 4 casos, sobre a função pura
      `markdownSurfaceTheme`; falhou antes pelo módulo ausente, e depois → 4 passed. O modo código no esquema oposto ao
      do app fica como antes (R53.1, X38)
- [x] **2.** O fundo explícito no olho (`markdown-preview.css` ou `MarkdownPreviewSurface.tsx`), o do lápis no lugar do
      `--editor-surface`, e um tema do Monaco derivado do Islands Dark e do light-plus com o fundo trocado — o olho e o
      lápis levam o estilo na raiz (`MarkdownPreviewSurface.tsx`, `RichMarkdownEditorSurface.tsx`), com o
      `backgroundColor` e o `--editor-surface` no canvas; o Monaco não ganha tema derivado, e a classe
      `.markdown-code-canvas` troca o `--vscode-editor-background` só no contêiner do Markdown (`main.css`; X38, X39) —
      `brza-studio@a44e84add32`
- [x] **3.** O hook do esquema do Markdown no lugar do `useDocumentDarkTheme` (`use-document-dark-theme.ts:4-8`), o
      interruptor e o seletor de tema próprio nas configurações do editor, ao lado do `EditorFontFamilySetting` — o
      `useMarkdownSurfaceTheme`, no olho, no bloco de código do lápis e na fonte do Monaco do Markdown; o
      `MarkdownThemeSetting`, com o `ChatThemePairPicker` inerte enquanto segue o chat, e o teste dele
      (`MarkdownThemeSetting.test.tsx` → 1 passed) — `brza-studio@a44e84add32`
- [x] **4.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; commit e push. A conferência no
      app é o C17 — os 61 arquivos de teste das áreas tocadas → 509 passed; depois do rebase sobre o P62, com os de i18n,
      70 arquivos → 555 passed; o check, abaixo

**Evidência:** commit [`a44e84add32`](https://github.com/brz-anderson/brza-studio/commit/a44e84add32), na `master` do
`brza-studio`, pela sessão `pln-001-p60`, autorizada por Anderson em 2026-10-29, na sessão do `brza-workspace` que
gravou o pedido 31 ("e já execute os passos em paralelo"). O resolvedor do P58 não mudou.

**Como ficou.** O campo é o `markdownTheme` das configurações globais, `{ followChat?, themeDark?,
useSeparateLightTheme?, themeLight? }`, em `src/shared/markdown-theme-settings.ts`; a ausência segue o chat com o
"Padrão do BrzA" no tema próprio, e o padrão não é gravado. O `resolveMarkdownTheme` chama o `resolveNativeChatTheme`
com o interruptor ligado e o `resolveNativeChatThemePair`, no contraste 100, com ele desligado. O
`markdownSurfaceTheme` (`src/renderer/src/components/editor/markdown-surface-theme.ts`) monta o estilo: o canvas, o
remapeamento das variáveis do app com tema do catálogo, e, seguindo o chat, a fonte e o tamanho do texto do chat e o
`--font-mono` na fonte de código do chat. O tamanho soma o zoom do editor. A normalização é a mesma no main, no store,
no web e na carga (X40). As traduções novas entraram no `en` e no `pt`. O mobile não lê o visualizador e não muda.

**O check.** O `pnpm check:changed --base=origin/master --maxWorkers=2` deu 24 de 27, em 1047 s. O primeiro, interrompido
pelo reinício do app, apontou o `anti-slop(no-object-parameters)` no `normalizeNativeChatThemePair(value: object)`,
corrigido com um tipo nomeado antes do commit. Os três vermelhos são os do P58, já na `master` sem esta mudança: o
typecheck, por `src/main/updater/updater-enabled.test.ts:20`; o import boundaries, pelo `external-subcommand.ts`; e os
testes unitários, pelos 2 casos de `open-uncommitted-entry.test.ts` (`'preview'` em vez de `'rich-editor'`).

### P61 — A conferência do tema do chat nos três (pedido 31)

Executa D45, D46 e D47 · executor: Anderson, com a sessão que conduz

Estimado: 0,3 h · Executado: — h

Depois do P59 e do P60.

- [ ] **1.** No BrzA Studio, o C15 ao C17: trocar o tema do chat troca o terminal e o Markdown; desligar o "Seguir o
      chat" de um e trocar o tema dele não muda os outros
- [ ] **2.** O Observado e o veredito na linha de cada caso

**Evidência:** —

### P62 — O leitor do BrzA para a mensagem de outra sessão e a devolução de subagente (pedido 32)

Executa D48 · executor: sessão do `brza-studio`, no worktree `.worktrees/pln-001-pedido-32`

Estimado: 4 h · Executado: 0,9 h

Primeiro do pedido 32; em paralelo com o pedido 31 (R51.2).

- [x] **1.** Teste que falha, junto de `transcript-reader.test.ts`: o turno `isMeta` com "Another Claude session sent a
      message:" e `<agent-message from="revisor">oi</agent-message>` vira uma mensagem do usuário com o `from` do
      remetente "revisor" e o texto "oi", sem o envelope; o de "[Subagent hand-back]" vira o mesmo, marcado como
      devolução; os outros turnos `isMeta` seguem descartados
- [x] **2.** O leitor do BrzA, ligado por uma linha no `transcript-line-decoders-claude.ts:108`, e o mesmo no caminho
      ao vivo; o rótulo "Mensagem de" e o "Devolução de" no `pt.json` e no `en.json`. Os pontos "A conferir no passo"
      do D48
- [x] **3.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; rebase na `origin/master` e
      push. A conferência no app é o C18

**Evidência:** commit [`21f9cfe90bb`](https://github.com/brz-anderson/brza-studio/commit/21f9cfe90bb), na `master` do
`brza-studio`, pela sessão `pln-001-pedido-32`, no worktree `.worktrees/pln-001-pedido-32`, autorizada por Anderson em
2026-10-29 ("Agora, em paralelo", R51.2). O leitor é o `src/main/native-chat/brza/brza-claude-peer-message.ts`: lê
primeiro o `origin` da linha (`kind: 'peer'`, `name`, `body`, `senderTaskId`) e, sem ele, o
`<agent-message from="…">` e o `<cross-session-message from="…" from-name="…">`, ambos depois de "Another Claude session
sent a message:" e só com a tag de fechamento (X34). A devolução é o corpo que abre com "[Subagent hand-back]": fica só o
relatório depois de "The report follows:", sem o recuo de dois espaços do harness. O remetente vai num
`AgentMessageSource` do upstream, com o tipo no endereço — `claude-peer:` ou `claude-hand-back:` —, em
`src/shared/native-chat/brza/brza-claude-peer-sender.ts` (X35).

**As ligações.** No `transcript-line-decoders-claude.ts`, uma chamada antes do descarte do `isMeta`; no
`journal-legacy-import.ts`, o `legacyItemBody` passa a levar o `from` (X36); no caminho ao vivo, o
`claude-message-journaling.ts` grava a mesma linha, com a mesma identidade, no escopo da thread. Na linha do remetente
(`NativeChatAgentMessageSenders.tsx`), o "Hand-back from" quando todo remetente é devolução, e o nome sem botão para o
remetente do Claude Code (X37). O `handBackFrom` entrou no `en.json` ("Hand-back from") e no `pt.json` ("Devolução de");
o `messageFrom` do `pt.json` já existia.

**A conferir no passo (D48).** O caminho ao vivo: o chat sobe o `claude` com `--replay-user-messages`
(`claude-structured-launch-resolution.ts:76`), e o eco do turno passa pelo `journalClaudeMessage`, que descartava todo
texto de usuário; se o CLI ecoa o turno `isMeta` do correio, só o C18 mostra. O tipo devolução: no endereço, sem mudar o
contrato do upstream (X35).

**Os testes.** O `brza-claude-peer-message.test.ts`, com 5 casos: o `<agent-message>`, o `<cross-session-message>` com e
sem `origin`, a devolução com e sem `origin`, os outros `isMeta` descartados, e o `from` na linha do journal pela
importação e pelo eco ao vivo. O `brza-claude-peer-sender.test.tsx`: o "Message from", o "Hand-back from" e o nome sem
botão. Antes do leitor, 3 dos 4 primeiros casos falharam pela asserção. O caso de `transcript-reader.test.ts:107`, do
upstream, segue intacto e passa. Depois do rebase em `9c7fcdebbb0`:
`node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre os testes do P62, do leitor, da tradução
ao vivo, da importação, das linhas do remetente e do i18n → 16 arquivos, 101 passed.

`pnpm check:changed --base=origin/master --maxWorkers=2` → 22 de 26, em 1514 s. O format, nos três arquivos novos, saiu
no `oxfmt` antes do commit. Os outros três vermelhos são preexistentes: o typecheck, só em
`src/main/updater/updater-enabled.test.ts:20`, do `8e708f9790d` (P26.4); o import boundaries, na issue das Pendências; e
5 testes em 3 arquivos — `runtime-workspace-launch-contracts.test.ts`, `open-uncommitted-entry.test.ts` e
`cross-version-agent-session-wire.unit.test.ts` —, que falham igual num worktree da `origin/master` em `9c7fcdebbb0`. O
`claude-stop-ack-race.test.ts` também falha sem o P62 (4 de 4).

Desvios X34 ao X37. A conferência no app é o C18, com o P65.

### P63 — O cartão do Orca para as mensagens entre agentes (pedido 32)

Executa D49 · executor: sessão do `brza-studio`, no worktree `.worktrees/pln-001-pedido-32`

Estimado: 10 h · Executado: 1,5 h

Depois do P62.

- [x] **1.** Trazer o `7321b066e83` do upstream (#34824) com `git cherry-pick -x`, com os arquivos de que ele depende e
      que faltam; os conflitos se resolvem a favor do upstream fora do código do BrzA. Registrar como `X` cada arquivo
      trazido além do commit
- [x] **2.** O cartão desenha também a mensagem do P62: a de outra sessão e a devolução, com o rótulo do P62; os testes
      do cartão trazidos passam, e um caso novo cobre a mensagem do Claude Code
- [x] **3.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; rebase na `origin/master` e
      push. A conferência no app é o C19

**Evidência:** commit [`9564eff9368`](https://github.com/brz-anderson/brza-studio/commit/9564eff9368), na `master` do
`brza-studio`, pela sessão `pln-001-pedido-32`, com `git cherry-pick -x 7321b066e83`: a mensagem do upstream, a linha
"(cherry picked from commit 7321b066e83…)" e as adaptações do BrzA. Antes do cherry-pick, uma sondagem num worktree
descartável mediu 6 conflitos e os módulos que faltavam ao cartão: só o `native-chat-prose`, que aqui mora em outro
caminho, e o harness de tooltip dos testes. Não foi preciso trazer módulo do cartão além disso, e a parada com Anderson
não se aplicou.

**Os conflitos, 7.** A linha do remetente e a linha do usuário ficaram com o upstream, mais as linhas do BrzA. A fila
(`structured-agent-session-queued-cards.ts` no renderer e `mobile-structured-queued-message-cards.ts`) ficou com a
versão do BrzA, com o `displayText` do commit portado (X51). Os testes da edição da fila do upstream ficaram de fora
(X52).

**O cartão desenha o remetente do P62.** No `NativeChatAgentMessageCard.tsx`, o título "Hand-back from" quando todo
remetente é devolução, e o "Message from" do upstream no resto; o rótulo saiu da linha do remetente para o título do
cartão, como no upstream (X54). Em `NativeChatAgentMessageSenders.tsx`, o nome do remetente do Claude Code segue sem
botão. Sem status no correio do Orca, o avatar mostra o ícone do Claude e nenhum ponto, sem erro. No mobile, a linha
diz "Hand-back from <nome>" para a devolução (`MobileNativeChatMessage.tsx`). O `pt.json` ganhou as 5 chaves novas do
cartão (X55).

**Os testes.** Os 11 arquivos de teste do commit que entraram passam, com um ajuste no caso de escala do cartão (X53). O
caso novo do Claude Code é o `brza-claude-peer-card.test.tsx`: os dois títulos, o texto e os nomes sem botão; ele
substitui o teste da linha do remetente do P62. No mobile, o `brza-mobile-peer-attribution.test.ts`. Depois do rebase em
`9118f60672b`: `pnpm tc` → exit 0; `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre os
testes do commit, os do BrzA, os da fila, os do i18n e o `src/main/runtime/orchestration` → 156 arquivos, 1263 passed;
pela `mobile/vitest.config.ts`, os do BrzA, o da atribuição e o da fila → 31 passed e 1 failed. O que falha é o
"words a host-restart returned card", que espera "Orca restarted" e recebe "BrzA Studio restarted", igual sem o P63
(num worktree em `21f9cfe90bb`: 1 failed, 25 passed). Os outros arquivos do mobile não carregam no worktree, sem o
`react-test-renderer` (X47).

`pnpm check:changed --base=origin/master --maxWorkers=2` → 23 de 26, em 1851 s. Os três vermelhos são preexistentes: o
typecheck do `updater-enabled.test.ts`, já corrigido na `master` em `586f4f69eb7`; o import boundaries, na issue das
Pendências; e os 2 casos do `open-uncommitted-entry.test.ts`.

Desvios X49 ao X55. A conferência no app é o C19, com o P65.

### P64 — O clique no remetente abre a aba da sessão (pedido 32)

Executa D50 · executor: sessão do `brza-studio`, no worktree `.worktrees/pln-001-pedido-32`

Estimado: 2 h · Executado: 0,5 h

Depois do P63.

- [x] **1.** Teste que falha: o clique no nome de uma sessão do Claude Code aberta no app foca a aba de chat dela; o
      nome que não casa com nenhuma aba aberta fica sem ação, com o cursor normal
- [x] **2.** A busca da aba pelo nome da sessão, no lugar do `openAgentMessageSender` quando o remetente é do Claude
      Code. Os pontos "A conferir no passo" do D50
- [x] **3.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; rebase na `origin/master` e
      push. A conferência no app é o C20

**Evidência:** commit [`ba4102b5c95`](https://github.com/brz-anderson/brza-studio/commit/ba4102b5c95), na `master` do
`brza-studio`, pela sessão `pln-001-pedido-32`. O componente é o `BrzaClaudePeerSenderName`, em
`src/renderer/src/components/native-chat/brza/BrzaClaudePeerSenderName.tsx`: procura, entre as abas `agent-session`
abertas em qualquer workspace, a única cujo `customLabel` ou `label` é o nome do remetente, e o clique a revela pelo
`activateAiVaultStructuredSession`, o mesmo caminho que abre um chat pelo histórico. Sem aba, ou com duas do mesmo nome,
o nome fica texto, sem botão e com o cursor normal (X56). A devolução de subagente nunca abre. Em
`NativeChatAgentMessageSenders.tsx`, o `SenderName` passa ao componente do BrzA quando o remetente é do Claude Code, no
lugar do `openAgentMessageSender`.

**A conferir no passo (D50).** O nome da aba: o `label` da aba de chat é o título que o host lista
(`frame-drawn-chat-tabs.ts:23`), que o `agentSession.rename` do `brza sessions --title` troca, e o `customLabel` é o nome
que a pessoa dá. O `/rename` do Claude Code grava o `custom-title` e o `agent-name` no transcript, que o app não lê; o
nome automático `brza-workspace-<hex>` não casa com aba nenhuma e fica sem ação (X56). O mobile não abre remetente
nenhum, nem o do Orca: a linha dele é texto.

**Os testes.** O `BrzaClaudePeerSenderName.test.tsx`: o clique no nome de uma sessão com aba aberta chama a ativação
com o workspace e a sessão da aba; o nome sem aba fica sem botão. Antes do componente, o primeiro caso falhou (sem
botão). Depois do rebase: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts` sobre os testes do
BrzA no chat, a linha do remetente e o cartão → 15 arquivos, 52 passed; `pnpm tc:web` → exit 0.

`pnpm check:changed --base=origin/master --maxWorkers=2` → 20 de 21, em 108 s. O vermelho é o import boundaries,
preexistente, na issue das Pendências.

Desvio X56. A conferência no app é o C20, com o P65.

### P65 — A conferência das mensagens entre sessões (pedido 32)

Executa D48, D49 e D50 · executor: Anderson, com a sessão que conduz

Estimado: 0,3 h · Executado: — h

Depois do P64.

- [ ] **1.** No BrzA Studio, o C18 ao C20
- [ ] **2.** O Observado e o veredito na linha de cada caso

**Evidência:** —

### P66 — O "Pensou" com o texto na linha, como o "Perguntou" (pedido 33)

Executa D51 · executor: sessão do `brza-studio`, no worktree `.worktrees/pln-001-pedido-33`

Estimado: 1,5 h · Executado: 2,0 h

Em paralelo com os pedidos 31 e 32 (R52.4).

- [x] **1.** Teste que falha, junto do teste da `NativeChatReasoningRow`: fechada, a linha mostra "Pensou por 3s:" e o
      começo do raciocínio em texto corrido, cortado numa linha, no tom apagado; aberta, o texto sai da linha e aparece
      inteiro no corpo; sem duração, "Pensou:" e o texto; o rótulo da pergunta em português é "Perguntou:"
- [x] **2.** A linha em `NativeChatReasoningRow.tsx`, com o texto corrido tirado do Markdown, e a chave nova de rótulo
      com dois-pontos no `pt.json` e no `en.json`; o "Perguntado:" vira "Perguntou:" (`pt.json:19772`). Os pontos "A
      conferir no passo" do D51
- [x] **3.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; rebase na `origin/master` e
      push. A conferência no app é o C21

**Evidência:** commit [`9118f60672b`](https://github.com/brz-anderson/brza-studio/commit/9118f60672b), na `master` do
`brza-studio`, com o [`586f4f69eb7`](https://github.com/brz-anderson/brza-studio/commit/586f4f69eb7) antes dele (X48),
pela sessão `pln-001-pedido-33`. O texto corrido é o `nativeChatReasoningPreview`, e o rótulo do mobile, o
`nativeChatReasoningLabelText`, em `src/shared/native-chat-reasoning-row.ts`; o desktop traduz as chaves novas
`reasoningLabel`, `thoughtLabel` e `thoughtForDurationLabel`, nos 7 catálogos, e cai no rótulo de hoje quando o
raciocínio é só marcação. O mobile entrou pela R54.1 (`MobileNativeChatReasoningRow.tsx`), e o streaming ficou na linha
do raciocínio pela R54.2. Antes do código, os testes deram: `NativeChatReasoningRow.test.tsx` → 9 failed, 9 passed;
`native-chat-reasoning-row.test.ts` (novo, X45) → 3 failed; `MobileNativeChatMessage.reasoning.test.ts` → 4 failed, 3
passed, depois do mock completado (X46). Depois: `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts`
nos 4 arquivos do desktop tocados → 47 passed; `pnpm exec vitest run` do teste mobile → 7 passed; `pnpm typecheck` no
`mobile/` → exit 0. O fixture temporário, apagado antes do commit, deu "Thought for 3s:" com o texto apagado e cortado
ao lado do "Asked:" em destaque, e, aberto, "Pensou:" sozinho na linha com o texto abaixo. Depois do rebase sobre o
P59, `pnpm check:changed --base=origin/master --maxWorkers=2` → 24 de 26, em 588 s, com os dois vermelhos de antes
desta mudança: o `external-subcommand.ts` nas fronteiras de import e os 2 casos de `open-uncommitted-entry.test.ts`
(19561 passed). O worktree e a branch saíram depois do push. Desvios X45 ao X48.

### P67 — As meta-ferramentas do MCP da Atlassian com ícone e título (X20)

Executa X20 · executor: `implementer` da sessão do workstream `studio`, no worktree `.worktrees/pln-001-p67` do
`brza-studio`

Estimado: 2 h · Executado: —

- [x] **1.** Teste que falha, junto do `brza-atlassian-tool.test.ts` e do `brza-tool-categories.test.ts`: o
      `executeRead`, o `executeWrite` e o `executeDestructive` com `name` de Jira ganham o logo do Jira, e com `name` de
      Confluence o `file-text`; o título é o `name`, e ` · <inputs.action>` quando a ação é texto
      ("manageJiraSprint · start"); o `discover` com jira ou confluence na `query` ganha o ícone do produto e o título
      com a busca entre aspas; sem produto no `name` ou na `query`, a linha fica como hoje (R55.1, R55.2)
- [x] **2.** O `matchesMcpTool` recebe o input como segundo argumento, que o `match` já tem; o produto das
      meta-ferramentas sai do input no `brza-atlassian-tool.ts`; o chip delas fica de fora (R55.1)
- [x] **3.** Os testes do que foi tocado, o `typecheck` do `mobile/` e o `pnpm check:changed --base=origin/master`;
      rebase na `origin/master` e push. A conferência no app vai junto do C6

**Evidência:** commit [`97a93f6ff57`](https://github.com/brz-anderson/brza-studio/commit/97a93f6ff57), na `master` do
`brza-studio`, pelo `implementer` (Sonnet) da sessão do workstream `studio`, no worktree `.worktrees/pln-001-p67`, com
o commit e o push pela sessão. O produto das meta-ferramentas sai do `metaToolSubject`, em `brza-atlassian-tool.ts`: o
`input.name` dos três `execute*` e a `query` do `discover`, pelo `productInText`, que fica com o produto citado
primeiro; o `metaToolReference` dá o título e `chip: null`. O `matchesMcpTool` recebe o input, e os chamadores do desktop
e do mobile já o passavam. A identidade chega crua nos dois caminhos — pelo nome `mcp__atlassian__executeRead` e pelo
`{ server, tool }` do Codex (`codex-structured-item-translation.ts:162`) —, e a regex dos três nomes casa (R56.1). Antes
do código: `brza-atlassian-tool.test.ts` e `brza-tool-categories.test.ts` → 11 failed, 26 passed. Depois: os dois → 37
passed; `src/shared/native-chat` → 81 arquivos, 1.182 passed; `pnpm tc` e o `typecheck` do `mobile/` → exit 0;
`pnpm check:changed --base=origin/master --maxWorkers=2` → só o vermelho de antes, o `external-subcommand.ts` nas
fronteiras de import. O worktree e a branch saíram depois do push. A conferência no app vai junto do C6.

### P68 — Os testes do transcript do mobile com o mock compartilhado do lucide (X47)

Executa X47 · executor: `implementer` da sessão do workstream `studio`, no worktree `.worktrees/pln-001-p68` do
`brza-studio`

Estimado: 0,7 h · Executado: 0,5 h

- [x] **1.** Os sete arquivos do X47 rodam e falham no carregamento, com o erro do `GitBranch`, antes da mudança
- [x] **2.** Um helper de teste no `mobile/` monta o mock do `lucide-react-native` com um componente simulado para
      qualquer ícone; os sete arquivos e o `MobileNativeChatMessage.reasoning.test.ts` passam a usá-lo, no lugar das
      listas à mão (R57.2)
- [x] **3.** Os testes do transcript do mobile, o `typecheck` do `mobile/` e o `pnpm check:changed --base=origin/master`;
      rebase na `origin/master` e push

**Evidência:** commit [`7be19418c8f`](https://github.com/brz-anderson/brza-studio/commit/7be19418c8f), na `master` do
`brza-studio`, pelo `implementer` (Sonnet) da sessão do workstream `studio`, no worktree `.worktrees/pln-001-p68`, com
o commit e o push pela sessão. O helper é o `lucideMock`, em `mobile/src/test-support/lucide-react-native-mock.ts`: um
`Proxy` que responde a qualquer nome em PascalCase com o próprio nome, que os testes procuram como tipo do nó, e aceita
sobrescritas (R59.3); os oito arquivos o usam por `import` dinâmico no `vi.mock`, com 194 linhas a menos. Com os
arquivos carregando, dois testes antigos falharam pelo P43, e trocaram de comando para `ls -la` e um `find` longo, fora
das categorias do BrzA (R59.1). Os outros ~40 mocks à mão do `mobile/` migram quando quebrarem (R59.2). Antes:
`transcript/` → 7 arquivos falhando no carregamento, 20 passando, 132 testes. Depois: `transcript/` e o teste do helper
→ 28 arquivos, 224 passed; `pnpm typecheck` e `pnpm typecheck:tests` do `mobile/` → exit 0, com o baseline vazio;
`pnpm check:changed --base=origin/master --maxWorkers=2` → só o vermelho de antes, o `external-subcommand.ts` nas
fronteiras de import. O `rpc-recording/family-recordings.test.ts` falha em 2 casos ("Recording differs") também na
`origin/master` `97a93f6ff57`, fora desta mudança. O worktree e a branch saíram depois do push.

## Regressão

Caminhos relativos à raiz do `brza-studio`. Os testes rodam como diz a `## Restrições`; em 2026-10-28, os 25 arquivos
de teste citados abaixo passaram (359 testes), na `master`. "Teste a escrever" é subpasso do passo citado, e a marca sai
da linha quando o teste entra.

- **O ícone e o título do upstream para toda ferramenta fora das categorias do BrzA** (`Read`, `Edit`, busca, web, MCP
  genérico, `ls`) ficam como estão. Como se confere: `src/shared/native-chat/tools/native-chat-tool-icon.test.ts`
  (`:60`, `:74`, `:81`, `:226`), `src/shared/native-chat/tools/brza/brza-tool-icon-mount.test.ts:25` e
  `native-chat-tool-line-label.test.ts`.
- **O comando de navegador do app (`brza snapshot`, `orca …`) mantém o globo**, e nenhuma categoria do BrzA o captura,
  nem em composto com `git` ou `gh` (R41.1). Como se confere: `native-chat-tool-icon.test.ts:180`,
  `brza/brza-cli-category.test.ts:27` e `native-chat-tool-run-sentence.test.ts:48`.
- **O comando sem categoria do BrzA segue com o verbo, o alvo e o título do upstream**, e a frase da corrida não muda.
  Como se confere: `brza/brza-tool-line-title.test.ts:48` e `native-chat-tool-run-sentence.test.ts`; o ramo do comando
  em `native-chat-tool-line-label.ts:94-108` tem o caso do P44.4 em `brza/brza-tool-line-title.test.ts`.
- **A corrida com categorias misturadas, ou só com as do upstream, mantém o glifo do upstream.** Como se confere:
  `brza/brza-tool-icon-mount.test.ts:30` e `native-chat-tool-icon.test.ts:164-219`.
- **O mobile cai no ícone lucide equivalente para todo logo de marca e mantém os glifos do upstream.** Como se confere:
  `pnpm --dir mobile typecheck`, que quebra se faltar glifo no
  `mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.ts:36`, e
  `MobileNativeChatToolRun.test.tsx`; o recuo de cada logo, por
  `mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.test.ts` (P43.4).
- **O link e o bloco de código do chat abrem, copiam e quebram linha como no upstream**; só a cor e a largura mudam.
  Como se confere, em `src/renderer/src/components/native-chat/`: `use-native-chat-link-actions.test.tsx`,
  `NativeChatPacedMarkdown.file-links.test.tsx`, `NativeChatCodeBlock.test.tsx`, `NativeChatMarkdown.code-wrap.test.tsx`
  e `NativeChatMarkdown.image-preview.test.tsx`.
- **As larguras "Normal" e "Larga" do chat não mudam, e o `120ch` só vale em "Total".** Como se confere:
  `native-chat-appearance-style.test.ts:205,230,248`, e na tela, porque o jsdom não avalia o `@container style()`.
- **A barra da mensagem do agente segue com Copiar, hora e rolar ao topo, só depois que o turno para; a do usuário
  mantém Copiar e Rewind.** Como se confere: `NativeChatMessageRow.test.tsx:92,106,118,185` e
  `NativeChatMessageTimestamp.test.tsx`.
- **O seletor de modelo e esforço funciona como antes, e a retomada de chat com a história em outra conta segue
  recusada por `historyInOtherAccount`.** Como se confere: `NativeChatModelCombobox.test.tsx:49-94`,
  `NativeChatComposerActions.test.tsx`, `src/main/claude/claude-structured-launch-account-routing.test.ts:131,160`,
  `use-native-chat-rewind.test.tsx:111` e `use-native-chat-context-clear-floor.test.tsx`.
- **O aviso de limite do upstream, na conta sem troca, segue sem o Continuar e sem "Send a message once it resets"**; o
  Retomar automaticamente e o Continuar do corte do Orca seguem iguais. O "Continuar em outra conta" do P40 entra ao
  lado, com o `BrzaContinueInOtherAccount.test.tsx`. Como se confere: `NativeChatNoticeRow.test.tsx:262-281,297,330` e
  `NativeChatInterruptedContinue.test.tsx:191,259,267`.
- **A barra do Markdown em diff mantém fonte e renderizado, com o padrão `source`; o diff combinado fica sem modos, e o
  Mermaid, o CSV e o notebook não ganham o olho.** Como se confere:
  `src/renderer/src/components/editor/markdown-preview-controls.test.ts:20,30,39,59`.
- **O build local de Mac e Linux e o atualizador do app de release ficam como estão**: só a versão
  `-local.<ms>.<commit>` desliga o atualizador (`src/main/updater/updater-enabled.ts:4-9`), e os canais `ORCA_WIN_*` do
  CI não mudam. Como se confere: `config/scripts/build-mac-local.test.mjs`, `build-win-local.test.mjs`,
  `build-linux-local.test.mjs`, `electron-builder-config.test.mjs` e, com versão de release,
  `src/main/updater/updater-enabled.test.ts` (P26.4).
- **O merge do `stablyai/orca` segue com conflito pequeno**: o BrzA toca o upstream só em linhas de montagem, e o resto
  mora em pastas `brza/`. Como se confere: `git diff $(git merge-base master upstream/main) master --numstat --` nos
  `native-chat-tool-icon.ts`, `native-chat-tool-line-label.ts`, `NativeChatMarkdown.tsx` e `NativeChatToolIcon.tsx`, que
  davam 14/2, 5/0, 4/1 e 3/1 em 2026-10-28.

## Desvios

- **X1 — O `build:win` também compila o launcher da CLI e o agent hook, em Rust, para x64.** O `afterPack` falha sem o
  `orca-agent-hook.exe`, que o `build:desktop` não compilava; afeta P26, e o P27 pede o Rust no Windows.
- **X2 — O Novo Chat aparece só no chat estruturado.** A vista de chat sobre o terminal não sabe o grupo da aba nem abre
  o chat por conta própria, como no rewind; afeta P34, e o D28 não muda.
- **X3 — O Editar na mensagem do usuário aparece só no chat estruturado.** A vista de chat sobre o terminal não tem a
  caixa do chat estruturado, como no X2; afeta P39, e o D33 não muda.
- **X4 — A retomada vencida dispara quando o host do main sobe, e não pelo store do restart.** O
  `native-chat-resume-on-restart-store.ts` é do renderer e só corre com a janela aberta; afeta P41, e o D35 não muda.
- **X5 — O Bifurcar aparece só no chat estruturado do Claude.** O corte é o `forkSession` do SDK do Claude, e a vista
  sobre o terminal não tem a sessão estruturada, como no X2; afeta P33, e o D27 não muda.
- **X6 — A chave do Markdown na caixa fica no `NativeChatGlobalSettings`, e não em `global-settings-types.ts`.** Este
  está no teto de 300 linhas do `max-lines`; afeta P38, e o D32 não muda.
- **X7 — O instalador do P27.1 sai num runner Windows do GitHub.** O `build:win` compila quatro addons C++ com MSVC, que
  não compila win32 no macOS nem no wine, e Anderson escolheu o runner; afeta P27, e o D21 não muda.
- **X8 — O instalador de Mac também sai num runner do GitHub, num DMG arm64 assinado ad hoc.** Pedido de Anderson na
  sessão da raiz de 2026-10-26 ("crie um Local Mac Installer"); afeta P1, e o D1 não muda.
- **X9 — As categorias do BrzA refinam só o ícone, sem estender o `NativeChatToolCategory` nem o
  `CATEGORY_BY_ROW_WORD`.** Estender a união do upstream mexeria nos `Record` exaustivos dele; afeta P43 e D37.
- **X10 — Os recuos de marca no mobile: git → `git-branch`, GitHub → `git-pull-request`, Jira → `square-kanban`.** O D37
  não os fixava; escolha do worker, a conferir com Anderson; afeta P43, que os testa no 4.
- **X11 — O nome do nó do Figma sai de um formato de saída suposto.** O worker não leu saída real e o tira do `name` do
  `get_metadata` e do `data-name` do `get_design_context`; afeta P50, e o ajuste fica no `nodeNameFromOutput`.
- **X12 — O `nodeId` do título sai normalizado com dois-pontos** (`12-34` vira `12:34`). Escolha do worker; afeta P50.
- **X13 — O `test:*` e o `build:*` contam, e mais gerenciadores.** O worker juntou ao D38 o `npm i`, o `npm ci`, o
  `yarn`, o `bun`, o `dart pub` e o `jest` direto; afeta P46 e P47.
- **X14 — O resultado do teste em português fica no `TEST_RESULT_COPY` do módulo compartilhado, e não no i18n (R40.3).**
  O mobile não lê esse catálogo, e o texto visto é o mesmo; afeta P46.
- **X15 — O `gh` sem número fica no padrão.** O número só vem da URL da saída: sem ela, a linha cai no padrão mesmo com
  o `--title`; com ela e sem título, diz "PR #123"; afeta P45.
- **X16 — O assunto do commit vem da saída antes do `-m`.** Assim o `--amend --no-edit` e o `-F` também ganham título;
  afeta P44.
- **X17 — O composto `git add … && git commit …` conta como commit**, com ícone, título e chip; o tooltip guarda o
  comando inteiro; afeta P44.
- **X18 — O chip da página diz "página", e o tooltip diz "Abrir no navegador" mesmo quando o clique só copia.** O chip
  reusa o `BrzaToolLineChip` do P44; afeta P48.
- **X19 — O site do Jira do app é o `activeSiteId`, senão o primeiro.** Com vários sites e o `cloudId` em UUID, o chip
  pode abrir no site errado, e o `cloudId` em prefixo não vira domínio; afeta P48.
- **X20 — As meta-ferramentas `executeRead`, `executeWrite` e `discover` do MCP da Atlassian ficam sem categoria.**
  Cobri-las pede o input no `matchesMcpTool`; decidido na R55 e na R56, com o `executeDestructive` junto, e fechado no P67
  (`brza-studio@97a93f6ff57`); afeta P48.
- **X21 — O P53.4 e o P40 foram à `master` com o import boundaries vermelho.** O vermelho é preexistente, do
  `9a81e65c852`, e Anderson mandou seguir, com o conserto no PLN-002 (R46.6); afeta P53 e P40.
- **X22 — O tom `faint` do link sobre código ficou sem medição útil.** O `native-chat-markdown.css:55` já põe `a, code`
  em `inherit` nesse tom, e a fixture não o distingue; afeta P53, e fica para o C10.
- **X23 — O `type` das imagens no schema do journal ficou aberto (`z.string()`), e não `'image-ref'`.** O literal abria
  um conjunto fechado novo, que o `journal-closed-sets.test.ts` só aceita com a versão da linha subindo; afeta P54.
- **X24 — Os testes do P54.1 e do P54.2 moram num arquivo só do BrzA**, o `brza-tool-result-images.test.ts`, com a
  projeção e o schema, e não no teste dos decoders do upstream; afeta P54.
- **X25 — Dois arquivos do upstream no teto do `max-lines` pediram mais que a montagem.** O tipo do journal usa o alias
  `BrzaToolCallMetadata` do `native-chat-types.ts`, e a projeção lê `call.callId` em vez de desestruturá-lo; afeta P54,
  e o D42 não muda.
- **X26 — O "+N" abre a linha, e as imagens todas aparecem na própria faixa, acima do corpo, e não dentro dele.** A
  faixa fica fora do `NativeChatExpandable`, como o D43 pede, e com a linha aberta mostra todas, com quebra; o corpo
  abre logo abaixo; afeta P55, e o D43 não muda.
- **X27 — A faixa quebra também fechada.** Num painel estreito, as quatro miniaturas e o "+N" passam à segunda linha,
  em vez de cortadas; afeta P55.
- **X28 — A mesma imagem duas vezes no resultado aparece uma vez.** A `key` é o `path` ou a `url`, pela regra do
  react-doctor contra o índice, e o "+N" conta as distintas; afeta P55.
- **X29 — A miniatura entra depois do bloco que nomeia a imagem, e não só do parágrafo.** No título e na tabela, vem
  depois deles; no item de lista e na citação, dentro deles, abaixo do parágrafo; afeta P56, e o D44 não muda.
- **X30 — O `![]()` que vem depois do link não apaga a miniatura da primeira menção.** A imagem aparece duas vezes: a
  miniatura no link e a autoral no `![]()`. Só o `![]()` que vem antes conta como menção que impede a miniatura; afeta
  P56 e D44.
- **X31 — A miniatura tem 96 px de altura, como a da linha da ferramenta (D43).** Fica montada invisível até a imagem
  carregar; o D44 não fixava o tamanho; afeta P56.
- **X32 — O chat migrado do "igualar ao terminal" fica no contraste 100 da fórmula, e não no texto a 100 % de antes.** O
  texto vai a 78 % no escuro e 82 % no claro, como o D45 pede ("o contraste em 100"); a R48.4 dizia "sem mudar a tela".
  Anderson tinha a chave desligada, e a tela dele não muda. O "terminal seguindo o chat" da migração é o padrão ligado do
  campo do P59, sem gravação no P58; afeta P58 e D45.
- **X33 — O teste do resolvedor fica ao lado dele, e o resolvedor e o seletor servem a qualquer par.** O teste está em
  `src/shared/native-chat-theme.test.ts`; o `resolveNativeChatThemePair` e o `ChatThemePairPicker`, com `disabled`,
  servem ao par próprio do Markdown (P60); o "Tema claro separado" é um interruptor direto, e não o "Match dark mode"
  invertido do terminal; afeta P58.
- **X34 — O correio de hoje vem no `<cross-session-message>`, com o `origin` na linha, e o nome no `from-name=`.** O
  D48 esperava o `<agent-message from="…">`, que segue só na devolução, com o ID do subagente. O leitor lê o `origin`
  primeiro e os dois envelopes depois, só com a tag de fechamento; o nome da devolução é o `origin.name`, o tipo do
  subagente (`general-purpose`), e o ID só sem `origin`. Medido em 286 linhas dos transcripts locais e no PLN-002/P9.1;
  afeta P62 e D48.
- **X35 — O tipo devolução vai no endereço do remetente, e não num campo.** O `AgentMessageSource` do upstream não
  muda: o endereço é `claude-peer:<socket>` ou `claude-hand-back:<tarefa>`; afeta P62, e o D48 não muda.
- **X36 — O `legacyItemBody` do upstream ganhou o `from`.** Sem ele, a importação do transcript para o journal perdia o
  remetente; uma linha em `journal-legacy-import.ts`; afeta P62.
- **X37 — No P62, o nome do remetente do Claude Code é texto, sem botão.** O `openAgentMessageSender` não acha a sessão
  pelo endereço do BrzA; o clique entra no P64; afeta P62.

- **X38 — O modo código do Markdown segue o chat só no esquema do app.** O tema do Monaco é global (R53.1): com o
  esquema do tema igual ao do app, o código leva o canvas, pela variável `--vscode-editor-background` no contêiner, e a
  fonte de código do chat; no esquema oposto, fica como antes. Afeta P60 e D47.
- **X39 — A sintaxe clara é o `vs`, e não o light-plus, e o Monaco não ganha tema derivado.** O `vs` é o tema claro que
  o app já usa (`monacoThemeName`, `islands-dark-theme.ts:30`), e a R49.4 manda a sintaxe não mudar; o fundo vem da
  variável CSS, sem `defineTheme` novo. Afeta P60 e D47.
- **X40 — O remapeamento de cores do chat e a normalização do par viraram funções compartilhadas.** O
  `nativeChatThemeSurfaceStyle` (`src/renderer/src/lib/native-chat-theme-surface-style.ts`) pinta o chat e o
  Markdown, com a classe `native-chat-theme-surface` na reavaliação das cores do `main.css`; o
  `normalizeNativeChatThemePair` serve ao chat e ao Markdown; o `sanitizeChatThemeSettingsUpdate` junta os dois no main
  e no store, porque o `settings-update.ts` bate no limite de 300 linhas. O contrato do resolvedor não mudou. Afeta P60.

- **X41 — O modo e o divisor do terminal seguem o esquema do tema do chat, e não o modo do app.** Com um tema claro do
  catálogo no app escuro, o terminal diz "claro" aos TUIs (modo 2031) e usa o divisor claro; no "Padrão do BrzA", os
  dois coincidem. O D46 não fixava; afeta P59.
- **X42 — A frente do terminal é a do tema do chat, sem a mistura do contraste.** O contraste do chat clareia ou
  escurece o texto do chat, e não o do terminal, que tem o piso de contraste próprio; o "com o contraste" do D46 ficou
  no canvas. Afeta P59.
- **X43 — Seguir o chat vale em toda superfície de terminal, e não só no painel.** A troca entrou no
  `resolveEffectiveTerminalAppearance`, que o painel, a prévia das configurações, a prévia do agente, o SSH simples, a
  barra lateral em "igualar ao terminal" e o tema do terminal do mobile leem, e a semente do OSC 10/11 no main também
  segue. Afeta P59.
- **X44 — O campo é o `terminalFollowsChatTheme`, no `NativeChatGlobalSettings`, e os testes do tema próprio o
  desligam.** Fica fora do `global-settings-types.ts`, como no X6. Os 19 casos do upstream, em 4 arquivos, que provavam
  o tema próprio com as configurações padrão ganharam `terminalFollowsChatTheme: false`, e o teste da tela acha o
  "Match dark mode" pelo rótulo. Afeta P59.
- **X45 — O teste do texto corrido está num `.test.ts` novo, e não no `.spec.ts`.** Os `src/shared/**/*.spec.ts` não
  entram no `UNIT_INCLUDE` do vitest e ficam fora do typecheck: o `native-chat-reasoning-row.spec.ts` não roda. Os 3
  casos foram para `src/shared/native-chat-reasoning-row.test.ts`. Afeta P66.
- **X46 — O mock do `lucide-react-native` do teste mobile do raciocínio ganhou os ícones do P43.** O
  `brza-mobile-tool-glyphs.ts` importa o `GitBranch` e outros 11 que o mock não tinha, e o arquivo nem carregava; o
  `MobileNativeChatMessage.reasoning.test.ts` ganhou os nomes. Afeta P66.
- **X47 — Sete arquivos de teste do transcript do mobile seguem sem carregar, pela mesma causa do X46.** O
  `MobileNativeChatMessage.test.ts`, o `.android`, o `.subagent-group`, o `.tool-result-availability` e o `.work-run`, o
  `MobileNativeChatToolRun.test.tsx` e o `.identity` dão `No "GitBranch" export is defined on the "lucide-react-native"
  mock`, desde o P43; ficaram fora do P66, que não os toca. Fechado no P68 (`brza-studio@7be19418c8f`), com o mock compartilhado da R57.2. Afeta
  P43.
- **X48 — O tipo do `getVersion` simulado do teste do atualizador, num commit à parte.** O `updater-enabled.test.ts:20`
  quebrava o typecheck da `master` desde o `brza-studio@8e708f9790d` (P2), porque o `vi.hoisted` inferia o literal
  `'1.4.242'`; o `brza-studio@586f4f69eb7` tipa o retorno como `string`. Afeta P2.
- **X49 — O harness de tooltip dos testes veio de fora do commit.** O
  `src/renderer/src/components/native-chat/native-chat-tooltip-test-harness.tsx`, 7 linhas, do `f150deb2266` do upstream;
  o teste do cartão depende dele; afeta P63.
- **X50 — O `agent-message-display-text.ts` importa o `../native-chat-prose`.** O upstream moveu o módulo para
  `src/shared/native-chat/transcript/` no `6bb0c14a985`, que não está aqui; afeta P63.
- **X51 — A fila fica com a projeção do BrzA, com o `displayText` do commit portado.** O upstream mudou a fila para o
  `shared/` e para o `queuedMessageCardLine`, que não estão aqui. O tipo e a projeção da fila, no desktop e no mobile,
  ganharam o `displayText`, e a linha do cartão da fila (`NativeChatQueuedMessageCard.tsx`, `MobileQueuedMessageCardRow.tsx`)
  o mostra; afeta P63.
- **X52 — Os testes da edição da fila do upstream ficaram de fora.** O
  `NativeChatQueuedMessageComposer.raw-task.test.tsx`, o `structured-queued-edit.test-fixture.tsx`, o
  `agent-message-command-contract.test.ts` e os trechos do commit no `use-mobile-structured-queued-edit.test.tsx` e no
  `structured-agent-session-queued-message-rig.test-fixture.ts` dependem da edição da fila nova do upstream; afeta P63,
  e o D49 não muda: nenhum é teste do cartão.
- **X53 — O caso de escala do cartão conta duas enumerações do status, e não três.** O BrzA não tem a "aquisição de
  autoridade visível" do store do upstream; uma linha em `NativeChatAgentMessageCard.test.tsx`; afeta P63.
- **X54 — O "Mensagem de" e o "Devolução de" passaram ao título do cartão.** O upstream tirou o rótulo da linha do
  remetente; o teste do P62 virou o `brza-claude-peer-card.test.tsx`, e o mobile ganhou o "Hand-back from"; afeta P62,
  P63 e D49.
- **X55 — O `pt.json` ganhou as 5 chaves do cartão.** "Ir para o agente", "Mensagem do seu coordenador", "Mostrar mais",
  "Tarefa do seu coordenador" e "Atualização do seu worker"; afeta P63.
- **X56 — O nome casa com o rótulo da aba, e só quando uma aba o tem.** O `customLabel` ou o `label` da aba de chat,
  o título do host; o `/rename` do Claude Code não chega ao app, e o nome automático `brza-workspace-<hex>` fica sem
  ação. Com duas abas do mesmo nome, o nome também fica sem ação, e a devolução de subagente nunca abre; afeta P64, e o
  D50 não muda.

## Worklogs

- 2026-10-26 — nasceu da divisão do PLN-025, na R28 de lá, com os passos P1, P2, P6, P25 a P27 e P33 a P41, os itens
  D1, D2, D6, D20, D21 e D27 a D35, e a evidência e as horas que já tinham; o Log até a divisão fica no PLN-025.
  Worklog `work/worklogs/2026-10-26-divisao-do-pln-025.md` do workspace da Fixfy.
- 2026-10-26 — sessão do `orca-dev` em `feat/markdown-eye-view`, a pedido da `fixfy-13`: P25 feito, com push na `main`
  do `orca-dev` (`952a232c8ba..5ded04d6bd1`); o olho é o padrão da aba do arquivo Markdown. Executado 0,3 h.
- 2026-10-26 — sessão do `orca-dev` em `feat/build-win-local`, a pedido da `fixfy-26`: P26 feito, com push na `main`
  do `orca-dev` (`5ded04d6bd1..342d85f66c9`); o `build:win` sai num instalador x64 sem assinatura e com o atualizador
  desligado, e compila os executáveis Rust do Windows (X1). Executado 0,4 h. Segue o P27, com Anderson.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-new-chat`, a pedido da `fixfy-26`: P34 feito, com push na
  `main` do `orca-dev` (`342d85f66c9..273d2cc6420`); a barra da mensagem do agente recebe o id, e o Novo Chat abre uma
  aba de chat com a mensagem como rascunho, sem enviar (X2). Executado 0,3 h. O P33 e o P35 podem abrir.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-edit-user-message`, a pedido da sessão `orca-dev` da raiz:
  P39 feito, com push na `main` do `orca-dev` (`273d2cc6420..5f7fdaf68bf`); a mensagem enviada tem o Editar, que a
  leva à caixa, abaixo do rascunho se houver, e dá foco (X3). Executado 0,4 h.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-account-switch`, a pedido da sessão `orca-dev` da raiz e
  retomada a pedido da `fixfy-22`: P36 feito, com push na `main` do `orca-dev` (`5f7fdaf68bf..65a2506c3c2`); o seletor
  de conta troca a conta no mesmo chat, com o transcript levado à conta nova, o `resume` nela e o divisor "Conta
  trocada - <conta>". Executado 1,2 h. O P40 pode abrir.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-pin-chapter`, a pedido da sessão `orca-dev` da raiz e
  retomada a pedido da `fixfy-22`: P35 feito, com push na `main` do `orca-dev` (`65a2506c3c2..b0a7ade5ba7`); a barra
  da resposta tem o Fixar Capítulo, marcado por padrão, e a régua recua os desafixados e diz "Capítulo fixado" na
  prévia. Executado 0,6 h.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-auto-resume`, a pedido da sessão `orca-dev` da raiz e
  retomada a pedido da `fixfy-22`: P41 feito, com push na `main` do `orca-dev` (`b0a7ade5ba7..a0110f3a431`); o aviso de
  limite com `resetsAt` tem o "Retomar automaticamente", que agenda no host do main o mesmo Continuar para o reset + 1
  min, com a linha "Retomada às HH:MM · Cancelar" e o disparo ao abrir (X4). Executado 1,1 h.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-fork`, a pedido da sessão `orca-dev` da raiz e retomada a
  pedido da `fixfy-22`: P33 feito, com push na `main` do `orca-dev` (`a0110f3a431..8eff03d0bb8`); o Bifurcar da
  mensagem do agente corta a conversa nela pelo `forkSession` e abre a sessão nova numa aba de chat ao lado, sem mudar
  a de origem (X5). Executado 0,9 h.
- 2026-10-26 — sessão do `orca-dev` em `feat/native-chat-markdown-composer`, a pedido da sessão `orca-dev` da raiz e
  retomada a pedido da `fixfy-22`: P38 feito, com push na `main` do `orca-dev` (`8eff03d0bb8..6285db81bbc`); o switch
  "Modo de visualização Markdown", desligado por padrão, põe na caixa do chat as extensões do visualizador, com o texto
  formatado e o envio em Markdown, pílulas incluídas (X6). Executado 1,0 h.
- 2026-10-26 — sessão do `orca-dev` em `build/win-docker`, a pedido da `fixfy-22`: P27.1 feito num runner Windows do
  GitHub (X7), com o `build-win-local.yml` em push na `main` do `orca-dev` (`6285db81bbc..68ffa0a223d`); o run
  `40425512083` gerou o instalador `1.4.239-local.1793060470212.68ffa0a223d8`, 178 MiB, em 8 min 32 s, e ele está em
  `~/Downloads/orca-dev-windows-1.4.239-local.1793060470212.68ffa0a223d8/`. O Docker não fecha o build (X7). Executado
  0,7 h. Seguem o P27.2 e o P27.3, com Anderson, no Windows.
  Worklog `work/worklogs/2026-10-26-instalador-windows-do-orca-dev-no-runner.md` do workspace da Fixfy.
- 2026-10-26 — sessão do `orca-dev` em `build/mac-local-timestamp`, a pedido da `fixfy-orca`: P1.4 feito, com push na
  `main` do `orca-dev` (`68ffa0a223d..b7c21f26f11`); o build local de Mac assina com `mac.timestamp: 'none'`, e o
  release segue com o carimbo, depois da falha do build assinado do PLN-028/P5.1 no carimbo. Executado 0,3 h.
- 2026-10-26 — sessão do `orca-dev` em `sync/v1.4.242`, a pedido da `fixfy-orca`: o merge da `v1.4.242` (PLN-025/P4,
  `f57841688f5`, push `b7c21f26f11..c552e92da92`) muda três passos, pela rodada gravada em cada um:
  - P41: o "Retomar automaticamente" fica sozinho na linha do limite, porque a v1.4.242 tirou o Continue (#33392);
  - P40: o item 2 vira um botão próprio na linha;
  - P1: o helper Swift passa a ser o do upstream (`--build-system native`).

  O P33 e o P36 mudam de lugar, sem mudar de comportamento: o registro do `agentSession.forkThroughMessage` vai à lista
  do switch-account, e o preparo do perfil vai a `claude-profile-launch-readiness.ts`, pelo `max-lines`.

- 2026-10-26 — sessão do `orca-dev` em `ci/build-mac-local`, a pedido da `fixfy-35`: o instalador de Mac num runner
  do GitHub (X8), com o `build-mac-local.yml` em push na `main` do `orca-dev` (`c552e92da92..ee06556cb8f`); o run
  `40432265386` gerou o DMG arm64 `1.4.242-local.1793064322587.ee06556cb8fe`, 239 MiB, assinado ad hoc, em 12 min 3 s.
  O app baixado pede o "Abrir Mesmo Assim" ou o `xattr -dr com.apple.quarantine`. Executado 0,6 h. O release de Windows
  e Mac segue com a `fixfy-35`.
- 2026-10-26 — sessão `fixfy-35`, no checkout da raiz do workspace: o pre-release
  [`v1.4.242-local.1793065827033.ee06556cb8fe`](https://github.com/brz-anderson/orca-dev/releases/tag/v1.4.242-local.1793065827033.ee06556cb8fe)
  do `orca-dev`, com a tag anotada em `ee06556cb8f`, como `brz-anderson`. Anderson pediu "assim que o sync da v1.4.242
  da orca-dev terminar, crie uma tag e um release para Windows no GitHub" e, na rodada, escolheu "A versão carimbada
  (Recomendado)" para a tag, "Pre-release (Recomendado)" para o release e "Mesmo release (Recomendado)" para o DMG. O
  `orca-windows-setup.exe` vem do run `40434569141` (9 min 22 s, `1.4.242-local.1793065827033.ee06556cb8fe`, sha256
  `f377232f…`), e o `orca-macos-arm64.dmg`, do run `40432265386` do X8 (sha256 `ed412bcd…`). O digest dos dois no
  GitHub bate com o local. O P27.2 e o P27.3 podem instalar pelo release.
- 2026-10-26 — worklog `work/worklogs/2026-10-26-p26-e-p34-do-pln-029-repassados.md` do workspace da Fixfy.
- 2026-10-26 — worklog `work/worklogs/2026-10-26-primeiro-build-assinado-do-orca-fixfy.md` do workspace da Fixfy.
- 2026-10-26 — worklog `work/worklogs/2026-10-26-rota-da-fixfy-no-orca-fica-no-fork.md` do workspace da Fixfy.
- 2026-10-27 — plano movido do PLN-029 da Fixfy (rodada D), na montagem do brza-workspace:
  [O brza-workspace nasce com a norma, o PLN-001, a medição e as skills de notas e de plano](../../work/worklogs/2026-10-27-o-brza-workspace-nasce.md)
- 2026-10-27 — [Os blocos de 120 colunas na largura "Total" e os links em azul claro no chat](../../work/worklogs/2026-10-27-chat-blocos-120-colunas-e-links.md):
  o P52 e o P53, com os commits `f130a85e578`, `9d289d2b631` e `52f7051a45d` do `brza-studio`.
- 2026-10-28 — [O P42, o P43, o P49 e o P51 por workers do Orca em paralelo](../../work/worklogs/2026-10-28-p42-p43-p49-p51-por-workers-do-orca.md):
  o P42, o P43, o P49 e o P51, com os commits `9b8a3e2e672`, `9b85279f57a` e `fbff699fa58`; as R33 a R35, o pedido 30 e os
  X9 e X10. Esperam a conferência com Anderson.
- 2026-10-28 — [O pedido 30, a prévia de imagem no chat, desenhado](../../work/worklogs/2026-10-28-pedido-30-previa-de-imagem-desenhada.md):
  as R36, R39 e R42, o D42 ao D44 e o P54 ao P57, sem código; o corte aceito na R42.3.
- 2026-10-28 — [O PLN-001 conferido contra a norma de planos da Fixfy e levado ao molde](../../work/worklogs/2026-10-28-pln-001-no-molde-da-fixfy.md):
  o desenho, a Cobertura, a Restrições, a Regressão, os Casos manuais, as Decisões e o Fechamento no molde; os Passos e
  os Desvios esperam a Run, na issue das Pendências.
- 2026-10-28 — [O P44 ao P48 e o P50 por workers do Orca em paralelo](../../work/worklogs/2026-10-28-p44-a-p48-e-p50-por-workers-do-orca.md):
  a Run `run_de875fc52a75`, com os commits `d7f4e5b5618`, `a1213f86859`, `68abc3821cd`, `05aa8af16cc`, `85469cf3b4d` e
  `fc7f07a8a1e`; a R44 e os X11 ao X20. Esperam os casos manuais com Anderson.
- 2026-10-28 — [Os Passos e os Desvios do PLN-001 levados ao molde, depois da Run do P44 ao P50](../../work/worklogs/2026-10-28-pln-001-passos-e-desvios-no-molde.md):
  os Passos sem fases, as R45 a R47, os X1 ao X22 em duas linhas e o P26.4, o P43.4 e o P44.4.
- 2026-10-28 — [O P54 do PLN-001, a imagem da ferramenta extraída para arquivo](../../work/worklogs/2026-10-28-pln-001-p54-imagem-da-ferramenta-extraida.md):
  o P54, com o commit `44ed13bfec9`; os dois pontos "A conferir" do D42 e os X23 ao X25. Esperam o P55 e o P56.
- 2026-10-28 — [O P55 do PLN-001, a miniatura na linha da ferramenta](../../work/worklogs/2026-10-28-pln-001-p55-miniatura-na-linha-da-ferramenta.md):
  o P55, com o commit `eca0bf772ba`, e os X26 ao X28. O C11 entra no build único dos casos manuais; espera o P56.
- 2026-10-29 — [O P56 do PLN-001 e os testes de regressão do P26.4, do P43.4 e do P44.4](../../work/worklogs/2026-10-29-pln-001-p56-miniatura-do-texto-solto-e-testes-de-regressao.md):
  o P56, com o commit `fc43b03b9ef`, os X29 ao X31 e os testes em `8e708f9790d`, `2e263df152f` e `8850460267c`, todos
  verdes com o código de hoje. O C12 entra no build único dos casos manuais; espera o P57.
- 2026-10-29 — [O pedido 31 do PLN-001, o tema do chat no Markdown e no terminal](../../work/worklogs/2026-10-29-pln-001-pedido-31-tema-do-chat.md):
  o pedido 31, a R48 e a R49, o D45 ao D47 e o P58 ao P61, sem código; o P58, depois o P59 e o P60 em paralelo.
- 2026-10-29 — [O pedido 32 do PLN-001, as mensagens entre sessões no chat](../../work/worklogs/2026-10-29-pln-001-pedido-32-mensagens-entre-sessoes.md):
  o pedido 32, a R50 e a R51, o D48 ao D50 e o P62 ao P65, sem código; o P62 ao P64 em paralelo com o pedido 31.
- 2026-10-29 — [O P58 do PLN-001, o tema do chat](../../work/worklogs/2026-10-29-pln-001-p58-tema-do-chat.md):
  o P58, com o commit `9c7fcdebbb0`, o resolvedor do tema do chat e os X32 e X33; abertas as sessões `pln-001-p59` e
  `pln-001-p60`. Vermelhos preexistentes no check: `updater-enabled.test.ts` e `open-uncommitted-entry.test.ts`.
- 2026-10-29 — [O pedido 33 do PLN-001, o "Pensou" como o "Perguntou"](../../work/worklogs/2026-10-29-pln-001-pedido-33-pensou-como-perguntou.md):
  o pedido 33, a R52, o D51 e o P66, sem código; o P66 em paralelo com os pedidos 31 e 32.
- 2026-10-29 — [O P62 ao P64 do PLN-001, as mensagens entre sessões no chat](../../work/worklogs/2026-10-29-pln-001-p62-a-p64-mensagens-entre-sessoes.md):
  o P62 em `brza-studio@21f9cfe90bb`, com os X34 ao X37, o P63 em `brza-studio@9564eff9368`, com os X49 ao X55, e o P64 em
  `brza-studio@ba4102b5c95`, com o X56; o pedido 32 espera só o P65.
- 2026-10-29 — [O P60 do PLN-001, o Markdown segue o chat](../../work/worklogs/2026-10-29-pln-001-p60-markdown-segue-o-chat.md):
  o P60 em `brza-studio@a44e84add32`, com a R53 e os X38 ao X40; o C17 espera o build do pedido 31, com Anderson.
- 2026-10-29 — [O P59 do PLN-001, o terminal segue o chat](../../work/worklogs/2026-10-29-pln-001-p59-o-terminal-segue-o-chat.md):
  o P59 em `brza-studio@697ee59c0bf`, com os X41 ao X44; o C16 e o P61 esperam o build do pedido 31, com Anderson.
- 2026-10-29 — [O P66 do PLN-001, o "Pensou" com o texto na linha](../../work/worklogs/2026-10-29-pln-001-p66-o-pensou-com-o-texto-na-linha.md):
  o P66 em `brza-studio@9118f60672b`, com a R54 e os X45 ao X48; o C21 espera o build, com Anderson.
- 2026-10-31 — [O P67 do PLN-001, as meta-ferramentas da Atlassian com ícone e título](../../work/worklogs/2026-10-31-pln-001-p67-meta-ferramentas-da-atlassian.md):
  o P67 em `brza-studio@97a93f6ff57`, com a R55 e a R56, fecha o X20; a conferência vai junto do C6, com Anderson.
- 2026-10-31 — [O P68 e o P37 do PLN-001, o mock compartilhado do lucide e a ortografia conferida](../../work/worklogs/2026-10-31-pln-001-p68-mock-do-lucide-e-p37-ortografia.md):
  o P68 em `brza-studio@7be19418c8f`, com a R57 e a R59, fecha o X47; o P37 fecha sem código, pela R58 e pela R59.4.

## Decisões

Notas de decisão do workspace da Fixfy, ao lado deste clone:

- O Orca da Fixfy substitui o original, sem atualizador, sincroniza por tag e guarda o código da Fixfy em pasta própria, no workspace da Fixfy: `work/decisions/orca-da-fixfy-substitui-o-original-e-sincroniza-por-tag.md`
  — PLN-025/R10 da Fixfy, `done`.
- O orca-dev commita com o noreply do brz-anderson, pela chave personal, com push direto na main, no workspace da Fixfy: `work/decisions/orca-dev-commita-como-brz-anderson-com-push-na-main.md`
  — PLN-025/R14 da Fixfy, `done`.

## Pendências conhecidas

- [Os Passos e os Desvios do PLN-001 no molde, depois da Run do P44 ao P50](../../work/issues/pln-001-passos-e-desvios-no-molde-depois-da-run.md)
  — da rodada de 2026-10-28 na sessão `pln-001-norma-fixfy`; resolvida em 2026-10-28, `done`.
- [O check de import boundaries está vermelho na master pelo `external-subcommand.ts` do `brza X`](../../work/issues/import-boundaries-vermelho-pelo-external-subcommand.md)
  — achado pelos workers do P53.4 e do P40, em 2026-10-28; o conserto é do PLN-002.

## Casos manuais

| ID  | Critério | Passos | Esperado | Observado | Veredito |
| :-- | :------- | :----- | :------- | :-------- | :------- |
| C1  | `Pedido 27`: a pergunta do "Perguntou:" na cor `primary` do tema (P42.3) | No build com o `fbff699fa58`, responder uma pergunta do agente | O texto da pergunta na cor do ✓, na linha fechada, na pergunta aberta e na lista | | |
| C2  | `Pedido 27`: a Skill, o Firebase e o Context7 com ícone e título (P49, P51) | No mesmo build, uma chamada real de cada | "Skill · <nome>"; o nome do projeto do Firebase e o da biblioteca do Context7 no título | | |
| C3  | `Pedido 27`: o `git` com ícone pelo subcomando e o hash que abre o diff (P44.3) | Um `git commit` do agente | "git commit — <mensagem>", e o hash abre o diff do commit | | |
| C4  | `Pedido 27`: o `gh` de PR com ícone, título e chip (P45.3) | Um `gh pr` do agente | "PR #123 — <título>", e o chip abre o PR no navegador | | |
| C5  | `Pedido 27`: os testes com passou/falhou no título (P46.3) | Uma execução de teste passando e uma falhando | As contagens de passou e falhou no título das duas linhas | | |
| C6  | `Pedido 27`: o Jira e o Confluence com chip (P48.3) | Uma chamada de cada | O chip com a chave do card ou o título da página, que abre no navegador | | |
| C7  | `Pedido 27`: o Figma com o logo e o nome do nó, sem a miniatura (P50.3, R38.4) | Uma chamada do Figma | O ícone e o nome do nó na linha | | |
| C8  | `Pedido 28`: 120 colunas na largura "Total" (P52.4) | Na largura "Total", um bloco curto, um longo e uma tabela; depois o painel estreito | Os três com `120ch` mais o padding; no painel estreito, encolhem e rolam na horizontal | | |
| C9  | `Pedido 29`: o link em azul claro (P53.3) | Um link no tema escuro e no claro | `#79C0FF` no escuro e `#0969DA` no claro, com o sublinhado a 40% | | |
| C10 | `Pedido 29`: o link sobre código inline também em azul (P53.4) | Um caminho em código inline que o chat vira link | O texto em azul, como o link comum | 2026-10-28: em branco, pelo `color` de `.native-chat-markdown code` | falha |
| C11 | `Pedido 30`: a miniatura na linha da ferramenta (P55.3) | Um `Read` de PNG, um `get_screenshot` do Figma e um print do browser | A miniatura na linha fechada de cada um, ampliando no clique | | |
| C12 | `Pedido 30`: a miniatura do caminho ou da URL solta no texto (P56.3) | Uma resposta com um print por caminho em código inline e outra com uma URL de imagem | A miniatura abaixo do parágrafo, uma vez por mensagem, com a mensagem terminada | | |
| C13 | `Pedido 30`: o que já existia funciona no BrzA Studio (P57.1, R36.1) | Um `![]()` local e um remoto; uma imagem colada e uma arrastada | A miniatura na mensagem enviada, e o clique amplia com pan e zoom nos quatro casos | | |
| C14 | `Pedido 26`: o Continuar em outra conta no aviso de limite (P40) | No aviso "Claude atingiu seu limite de sessão", abrir o "Continuar em outra conta" e escolher a outra conta | O menu com as outras contas, também com uma só; a troca, o divisor "Conta trocada - <conta>" e só então o Continuar | | |
| C15 | `Pedido 31`: o tema do chat e a migração (P58.4) | Trocar o tema do chat entre o "Padrão do BrzA" e um do catálogo, no app escuro e no claro | O chat com o fundo e as cores do tema; no "Padrão do BrzA", o visual de antes | | |
| C16 | `Pedido 31`: o terminal segue o chat (P59.3) | Com o "Seguir o chat" ligado, trocar o tema do chat; depois desligar e escolher outro tema no terminal | Ligado, o terminal com o fundo e as cores do chat e a fonte dele; desligado, só o terminal muda | | |
| C17 | `Pedido 31`: o Markdown segue o chat (P60.4) | Um `.md` no olho, no lápis e no código, com o "Seguir o chat" ligado e desligado | Ligado, os três com o fundo do chat, e o olho e o lápis com a fonte do chat; desligado, o tema próprio | | |
| C18 | `Pedido 32`: a mensagem de outra sessão e a devolução no chat (P62.3) | Mandar uma mensagem de uma sessão a outra, aberta no app; numa sessão, rodar um subagente; recarregar a aba | "Mensagem de <sessão>" e "Devolução de <subagente>", ao vivo e depois de recarregar, sem o envelope | | |
| C19 | `Pedido 32`: o cartão do Orca (P63.3) | As mesmas mensagens do C18 | O cartão, com o status do remetente | | |
| C20 | `Pedido 32`: o clique no remetente (P64.3) | Clicar no nome de uma sessão aberta e no de uma fechada | A aba da sessão aberta em foco; a fechada sem ação | | |
| C21 | `Pedido 33`: o "Pensou" com o texto na linha (P66.3) | Uma resposta com raciocínio, entre comandos e fora deles, no desktop e no app do celular (R54.1); abrir e fechar a linha | "Pensou por Xs:" e o começo do texto, apagado, cortado; aberta, o texto inteiro abaixo; a pergunta com "Perguntou:" | | |

O C1 e o C2 esperavam a Run `run_de875fc52a75`, que fechou em `fc7f07a8a1e`: o build instalado (`de3fb921ad1`) não tem o `9b8a3e2e672` nem o
`fbff699fa58`, e a coordenadora da Run roda do app instalado. Na R46.4,
Anderson escolheu "Depois da Run, num build só (Recomendado)": uma instalação para o C1 ao C7, o C10 e o C14. O C11
entra no mesmo build, pelo pedido do P55 (2026-10-28), e o C12, pelo do P56 (2026-10-29). O C15 ao C17 são do
pedido 31 e vão a um build depois do P60, com o P61; o C18 ao C20, do pedido 32, a um build depois do P64, com o P65; o C21, do pedido 33, ao mesmo build.

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um.
      Trabalho só em notas de `work/` e `plans/` não tem resumo.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão em `work/decisions/`, a
      norma do `brza-studio`, o guia.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
