---
status: in_progress
phase: execution
origin: request
ready: "sim — o P44 ao P48 e o P50, na Run run_de875fc52a75 em execução; o P54 ao P57 do pedido 30 depois do P44 ao P50; a conferência do P42, P49, P51, P52 e P53 com Anderson"
estimate_h: 123.6
executed_h: 10.15
remaining_h: 20.2
scope:
  - brza-studio
opened: 2026-10-26
owner: Anderson
tags:
  - tooling
---

# PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat

- **Retomar:** o plano veio do PLN-029 do workspace da Fixfy em 2026-10-27 (R32); o `orca-dev` é hoje o `brza-studio`
  (`~/Projects/brza-studio`, repo `brz-anderson/brza-studio`, branch `master`), e cada passo se confere no BrzA Studio,
  com Anderson. Evidência, horas e worklogs vão a este repositório, com `git add` por caminho e push na `master`.
  Feitos, com a evidência abaixo: P1, P2, P6, P25, P26, P33, P34, P35, P36, P38, P39, P41, P27.1, P52 e P53 (falta a
  conferência, P52.4 e P53.3) e, em 2026-10-28, por workers do Orca (R33), o P42, o P43, o P49 e o P51 (commits
  `9b8a3e2e672`, `9b85279f57a` e `fbff699fa58`). **Esperam conferência com Anderson, num build com o `fbff699fa58`:** o
  P42.3, a Skill, o Firebase e o Context7 com chamadas reais (os campos do título são suposição, sobretudo o projeto do
  Firebase) e o P52.4 e o P53.3. O P53.4, o link sobre código inline que ficou branco, é conserto a fazer.
  **Em execução:** a Run `run_de875fc52a75` do P44 ao P48 e do P50, disparada em 2026-10-28 às 01:11, na sessão
  `pln-001-p44-p50` (modo chat). As rodadas fecharam na R37, R38, R40, R41 e R43 (a R39 e a R42 são do pedido 30), e o
  D38, o D39 e o P44 ao P50 já estão reescritos por elas (`b7194b3`). São três workers (R37.3, R37.4 e R40.4), nos
  worktrees de `~/Projects/brza-studio/.worktrees/`, na `7e9e0d18948`:
  - o de shell, Opus, faz o P44 → P45 → P46 → P47 em `pln-001-p44-p47`, e é dono da ordem de peso da lista
    (`task_3a795915093f`, `ctx_663c93482e60`);
  - o do P48, Sonnet, em `pln-001-p48` (`task_1a38e7df74ee`, `ctx_4e2320de3d3c`);
  - o do P50, Sonnet, sem a miniatura (R38.4), em `pln-001-p50` (`task_dcc18ceb0b7c`, `ctx_c0edf254fd8d`).

  As especificações estão no scratch da sessão
  (`/private/tmp/claude-501/-Users-andepb-Projects-brza-workspace/e354254e-149e-463d-862e-f3e05a58e5ac/scratchpad/specs/`).
  Para retomar a coordenação de outra sessão: `orca orchestration run-use --id run_de875fc52a75` e o `check --wait`.

  A mudança compartilhada, idêntica nos três, é `brzaToolLineTitle(call, result?)`, com o `result` passado em
  `native-chat-tool-line-label.ts:144`. Os workers não editam o plano: a coordenadora grava a evidência a partir do
  `worker_done`.
  O **pedido 30**, a prévia de imagem no chat, está desenhado (R36, R39 e R42; D42 a D44) e vira o P54 ao P57, depois do P44 ao P50 (R42.4): o P54 antes do P55, o P56 independente e o P57, a conferência, por último. Abertos desde a
  Fixfy: o P37 e o P40. O P27.2 e o P27.3 seguem com Anderson, no Windows; o Sophos da máquina gerenciada pela TI barrou
  o instalador sem assinatura em 2026-10-28, e Anderson respondeu "esquece". O build de Windows é `gh workflow run
  build-win-local.yml --repo brz-anderson/brza-studio --ref master`, com a conta `brz-anderson` ativa no `gh`.
  **Execução em paralelo:** worktrees em `.worktrees/` do `brza-studio`, criados com `git worktree add` e passados ao
  `orchestration worker-start` por `path:` (o worktree novo do Orca cai fora do `brza_where`). O `pnpm` não está no
  `PATH`: o 12.14.0 está em `~/.npm/_npx/aa4546e781591cea/node_modules/.bin`, e o hook do commit pede ele no `PATH`. Os
  testes rodam com `node config/scripts/run-vitest.mjs run --config config/vitest.config.ts <caminhos>`, e o `pnpm
  check:changed` com `--base=origin/master`.
- **Dividido:** o Desenho em [PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat — Desenho](PLN-001-design.md);
  a Entrevista, o Terreno e o Log até a divisão ficam no PLN-025 do workspace da Fixfy
  (`plans/PLN-025-orca-desktop-cli-app-e-web/PLN-025-interview.md` e `PLN-025-design.md`, R28.3); as rodadas de
  2026-10-27, R29 a R32, estão na `## Entrevista` abaixo. As R até a R28, citadas nos passos e nos itens `D`, são as do
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

## Passos

> Executor "sessão do `brza-studio`" é a sessão aberta em `~/Projects/brza-studio` (antes `orca-dev`), que commita com
> o `brz-anderson` e dá push na `master` do `brza-studio`, como diz o `Retomar`. Cada passo só executa a pedido
> explícito de Anderson. Os IDs são os do PLN-025 da Fixfy, e a numeração salta onde o passo foi para outro plano
> (R28.2); os P42 a P53 são novos, daqui.
>
> **Outro runtime** marca o passo que o Codex ou o `agy` podem executar, e o mais indicado vem primeiro, com
> "indicado". É leitura, e não decisão: o runtime de cada passo se escolhe no pedido. O Codex e o `agy` abrem só a
> pedido, numa sessão interativa, e a rodada que o passo pedir volta à sessão principal do Claude. O P27 fica com
> Anderson, no Windows. Os P42 a P53 não levam a marca: o runtime se escolhe no pedido.

### F1 — A base

#### P1 — O build local do `orca-dev` sai em um comando, assinado pela identidade configurada

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

**Rodada do sync da v1.4.242 (2026-10-26):** respondida por Anderson na sessão `fixfy-orca`, pelo AskUserQuestion, e
levada à sessão do `orca-dev` (`sync/v1.4.242`). A v1.4.242 corrigiu o mesmo defeito do Swift 6.4 com
`--build-system native` (#21145), no `build-computer-macos.mjs:30-45` que o item 1 tinha mudado. Medido no merge:
`node config/scripts/build-computer-macos.mjs` em 47 s, `lipo` com `x86_64 arm64`, e o SwiftPM avisa que
"'--build-system native' has been deprecated and will be removed in a future release".

1. **O helper Swift do Computer Use depois da v1.4.242.** Opções:
   - a da v1.4.242 (recomendada): o arquivo volta a ser igual ao do upstream; custo: nenhum agora, e ~20 min para trazer
     de volta o `--show-bin-path` quando o SwiftPM remover o `native`; se paga: agora, sem divergência nesse arquivo nas
     próximas sincronizações;
   - manter o nosso `--show-bin-path`: custo: ~5 min agora e um conflito nesse arquivo a cada sincronização em que o
     upstream mexer nele; se paga: no dia em que o SwiftPM remover o `--build-system native`, se o upstream não migrar
     antes.

   **Resposta — "A da v1.4.242 (Recomendado)".** No merge `f57841688f5`, o `build-computer-macos.mjs` é o do upstream,
   e o conserto do Swift 6.4 passou a ser o `--build-system native` (#21145). Se o SwiftPM o remover, volta o nosso
   `--show-bin-path` (~20 min), o do commit `eabec4de25f`.

#### P2 — O atualizador fica desligado no build local

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

### F2 — O tema

#### P6 — O tema Islands Dark no Monaco e no Shiki, no `orca-dev`

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

### F5 — O genérico novo

#### P25 — O olho no visualizador de Markdown (pedido 14)

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

#### P26 — O build local de Windows sai em um comando (pedido 15)

Executa D21 · executor: sessão do `brza-studio`

Estimado: 2 h · Executado: 0,4 h

- [x] **1.** Teste que falha: os passos do build de Windows instalam o `mobile/`, rodam o `build:desktop` e o
      `ensure:electron-runtime` e chamam o `electron-builder --win --x64`, com a `ORCA_LOCAL_BUILD_VERSION` no formato
      que o `isUpdaterEnabled()` reconhece
- [x] **2.** O `config/scripts/build-win-local.mjs`, com o `createLocalBuildVersion` do `build-mac-local.mjs`
      reaproveitado, e o `build:win` apontando para ele
- [x] **3.** Os testes do script e do atualizador passam; o `.github/CONTRIBUTING.md` diz o novo `build:win`; commit e
      push

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

#### P27 — O build do `brza-studio` instalado no Windows (pedido 15)

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

### F7 — O chat (pedidos 19 a 30)

Todos com o executor sessão do `brza-studio`, fora da trava do PLN-025/P28 da Fixfy (R25.3), com commit e push na
`master` do `brza-studio` (os feitos até 2026-10-26, na `main` do `orca-dev`, como a evidência diz); cada um se confere
no BrzA Studio, com Anderson. O P34 vem antes do P33 e do P35, porque leva o id da mensagem à barra. O P40 vem depois do
P36, de que reaproveita a troca; o P41 não depende dele. **O P42 ao P53** (pedidos 27 a 29, R29 a R31) vêm depois: o P43
vem antes do P44 ao P51, porque monta a base dos ícones, e o P42, o P52 e o P53 não dependem de nenhum. A ordem de
entrega, se os passos não couberem numa sessão, é pendência a perguntar a Anderson.

**O P54 ao P57** (pedido 30, R36, R39 e R42) vêm depois do P44 ao P50 (R42.4): o P54 antes do P55, o P56
independente, e o P57, a conferência com Anderson, por último.

#### P34 — A barra da mensagem do agente e o Novo Chat (pedido 20)

Executa D27, D28 · Estimado: 4,5 h · Executado: 0,3 h

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

#### P33 — O Bifurcar (pedido 19)

Executa D27 · Estimado: 18 h · Executado: 0,9 h

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
com as outras sessões do F7 rodando, e não voltou a rodar. `pnpm tc:node` e `pnpm tc:web` saem com 0 depois do último
rebase; `pnpm run check:code-quality:changed` sem achado novo; `verify:rpc-params-catalog`,
`verify:localization-catalogs` e `verify:localization-coverage` saem com 0. A conferência no Orca fica com o
PLN-028/P8.

#### P35 — O Fixar Capítulo na régua de prompts (pedido 21)

Executa D29 · Estimado: 8 h · Executado: 0,6 h

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

#### P36 — O seletor de conta (pedido 22)

Executa D30 · Estimado: 29 h · Executado: 1,2 h

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

#### P37 — As sugestões de ortografia (pedido 23)

Executa D31 · Estimado: 2 h · Executado: — h

- [ ] **1.** Conferir, no `orca-dev` aberto, o botão direito numa palavra errada da caixa do chat, em pt-BR; se as
      sugestões aparecem, o passo fecha sem código
- [ ] **2.** Se não, a correção do idioma ou do menu do chat, com teste; commit e push

**Rodada de 2026-10-28, na sessão `pln-001-retomar`:** o subpasso 1 se confere "Agora, no instalado (Recomendado)", no
build `de3fb921ad1`. O menu do Chromium com as sugestões do corretor já é tratado em
`use-native-chat-context-menu.tsx:347`.

**Evidência:** —

#### P38 — O Markdown na caixa de texto (pedido 24)

Executa D32 · Estimado: 18 h · Executado: 1,0 h

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

#### P39 — O Editar na mensagem do usuário (pedido 25)

Executa D33 · Estimado: 1,5 h · Executado: 0,4 h

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

#### P40 — O Continuar em outra conta, no aviso de limite (pedido 26)

Executa D34 · Estimado: 3 h · Executado: — h

**Travado pelo P36**, de que reaproveita a troca de conta (R27.1).

**Outro runtime:** Codex, indicado — botão com menu e a ordem troca → envio, com teste

- [ ] **1.** Teste que falha: o Continuar só sai depois que a sessão nova sobe na conta escolhida, e nada sai se a troca
      falha
- [ ] **2.** O botão próprio "Continuar em outra conta", com o menu das outras contas, na linha do limite, ao lado do
      "Retomar automaticamente" (`NativeChatNoticeRow.tsx`, no ramo do `usageLimitAutoResume`): troca a conta pela
      troca do P36 e depois chama o `continueUsageLimit` (`NativeChatInterruptedContinue.tsx:112`), que a v1.4.242
      manteve; commit e push

**Rodada do sync da v1.4.242 (2026-10-26):** respondida por Anderson na sessão `fixfy-orca`, pelo AskUserQuestion, e
levada à sessão do `orca-dev` (`sync/v1.4.242`). A v1.4.242 tirou o Continue da linha do limite (#33392, `d249c21b7f0`),
ao lado do qual o item 2 punha o botão.

1. **O P40, que se apoiava no Continue da linha.** Opções:
   - botão próprio na linha (recomendada): o "Continuar em outra conta" vira botão próprio, com o menu das outras
     contas, sem o Continue; a objeção do #33392 (o Continue antes do reset bate no mesmo limite) não vale, porque a
     outra conta tem o seu próprio limite; custo: ~15 min para reescrever o item 2, e a estimativa de 3 h fica; se paga:
     quando o P40 for executado;
   - manter o P40 ao lado do Continue: cabe só com o Continue de volta (a opção 2 da rodada do P41); custo: nenhum
     agora; se paga: só com essa opção;
   - tirar o P40 do plano: custo: o pedido 26 fica sem a troca de conta no aviso; se paga: nunca, a menos que Anderson
     não o queira mais.

   **Resposta — "Botão próprio na linha (Recomendado)".** O item 2 acima é o reescrito, e a estimativa de 3 h fica.

**Rodada de 2026-10-28, na sessão `pln-001-retomar`:** quem executa — "Workers do Orca daqui (Recomendado)": um worker
Codex, como o passo indica, em `.worktrees/pln-001-p40`, numa Run separada da `run_de875fc52a75`. A Run não toca o
`NativeChatNoticeRow.tsx`, o `NativeChatInterruptedContinue.tsx` nem o `use-native-chat-account-switch.ts`, que são os
pré-requisitos do passo e existem na `9a81e65c852`. Na mesma sessão, à pergunta do worker sobre o botão, Anderson
escolheu "Menu sempre, como o P36 (Recomendado)": "Continue in another account" e "Continuar em outra conta", o ícone
`UserRound` do `NativeChatAccountPicker` e um `DropdownMenu` com as outras contas, também quando só há uma.

**Evidência:** —

#### P41 — O Retomar automaticamente, no aviso de limite (pedido 26)

Executa D35 · Estimado: 11 h · Executado: 1,1 h

**Outro runtime:** Codex, indicado — agenda no main, canal e botão, todos testáveis sozinhos

- [x] **1.** Teste que falha: a agenda grava o reset + 1 min, sobrevive ao restart, dispara o Continuar uma vez só e
      some com uma mensagem enviada antes ou com o Cancelar
- [x] **2.** A agenda persistida no main e o canal que agenda, cancela e lista; o disparo pelo mesmo envio do Continuar
- [x] **3.** Teste que falha e o disparo ao abrir o Orca, junto da retomada do restart, só se o chat ainda está no corte
- [x] **4.** O botão ao lado do Continuar, oculto sem `resetsAt`, e a linha "Retomada às HH:MM · Cancelar"; commit e push

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

**Rodada do sync da v1.4.242 (2026-10-26):** respondida por Anderson na sessão `fixfy-orca`, pelo AskUserQuestion, e
levada à sessão do `orca-dev` (`sync/v1.4.242`). A v1.4.242 tirou o Continue da linha do limite (#33392,
`d249c21b7f0`): o botão, o `retryControl`/`continueControl` das palavras do limite, a frase "Send a message once
it resets to continue." e a chave `interruptedContinue.usageLimitExplanation` nas 7 línguas. Manteve o
`continueUsageLimit`, o `usageLimitTurnItemId` e o `usageLimitContinuationOfTurnItemId` do host, e com eles a agenda
do main.

1. **A linha do aviso de limite depois da v1.4.242.** Opções:
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

   **Resposta — "Seguir a v1.4.242 (Recomendado)".** No merge `f57841688f5`, a `NativeChatNoticeRow` mostra o
   `NativeChatUsageLimitAutoResume` sozinho, só no corte atual (`usageLimitTurnItemId` da linha igual ao do chat) e com
   a agenda no mesmo turno; sem `resetsAt`, a linha não tem botão. A agenda do main, o canal e o disparo ao abrir não
   mudam. O teste da linha perdeu o Continue: o do "Retomar automaticamente" roda sobre a linha com as palavras atuais,
   o "sem reset" só confere a falta do botão, e o "tells a chat that has no Continue to send a message" saiu, porque a
   frase saiu do upstream. Os casos da v1.4.242 (reset futuro, passado e desconhecido, e o texto histórico) entraram.

#### P42 — O "Perguntou:" em cor de destaque (pedido 27)

Executa D36 · Estimado: 0,3 h · Executado: 0,3 h

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

#### P43 — A base dos ícones de marca: o módulo do BrzA e os logos SVG (pedido 27)

Executa D37 · Estimado: 0,5 h · Executado: 0,75 h

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

#### P44 — O `git` com ícone e título próprios (pedido 27)

Executa D38 · Estimado: 2 h · Executado: — h

O estimado passou de 1 h a 2 h com o diff pelo hash (R38.1).

- [ ] **1.** Teste que falha: o comando de shell vira categoria segmento a segmento, e no composto vale a de mais peso,
      testes > gh > git > pacotes e build > `brzaCli` (R37.1), com o globo do upstream no comando de navegador (R41.1);
      o `git` ganha o `git-logo`, e o `git commit`, o `git-commit-horizontal` (R40.1); a corrida de git leva o logo
      (R41.2)
- [ ] **2.** O título lê a saída (`brzaToolLineTitle(call, result)`); "git commit — <1ª linha da mensagem>", em
      português (R40.3), e o chip do hash, lido da saída, que abre o diff do commit no visualizador por uma
      `openCommitByHash` do BrzA (R38.1), só no desktop (R41.3)
- [ ] **3.** Os testes; commit e push; conferir no BrzA Studio uma linha de `git commit`, com Anderson

**Pendências:** fechadas na R37, R38, R40 e R41.

**Evidência:** —

#### P45 — O `gh` de PR e issue com ícone, título e chip (pedido 27)

Executa D38 · Estimado: 1 h · Executado: — h

- [ ] **1.** Teste que falha: o comando `gh` de PR e issue vira categoria própria, com o ícone GitPullRequest, pelo
      mesmo caminho do P44
- [ ] **2.** O título "PR #123 — <título>" e o chip que abre o PR no navegador
- [ ] **3.** Os testes; commit e push; conferir uma linha de PR no BrzA Studio, com Anderson

**Pendências:** fechadas na R37.1 e na R40.2: "PR #123 — <título>" e "Issue #45 — <título>", com o número pela URL
na saída e o título pelo `--title` ou pela saída; o chip só no desktop (R41.3).

**Evidência:** —

#### P46 — Os testes com ícone e o resultado no título (pedido 27)

Executa D38 · Estimado: 1,5 h · Executado: — h

- [ ] **1.** Teste que falha: `vitest`, `run-vitest.mjs`, `flutter test` e `pytest` viram a categoria de testes, com o
      ícone FlaskConical, pelo mesmo caminho do P44
- [ ] **2.** O passou/falhou contado no título a partir da saída do comando, com um teste por executor
- [ ] **3.** Os testes; commit e push; conferir uma linha de teste passando e uma falhando no BrzA Studio, com Anderson

**Pendências:** fechadas na R37.2, na R38.2 e na R40.2 e R40.3: o gerenciador que roda teste é testes; "<executor> —
12 passaram, 1 falhou" pelo rodapé, e só "passou" ou "falhou" na saída cortada.

**Evidência:** —

#### P47 — Pacotes e build com ícone e título (pedido 27)

Executa D38 · Estimado: 0,3 h · Executado: — h

- [ ] **1.** Teste que falha: `pnpm`, `npm`, `flutter pub` e o build viram a categoria de pacotes e build, com o ícone
      Package ou Hammer, só ícone e título, sem interação
- [ ] **2.** Os testes; commit e push

**Pendências:** fechadas na R37: o lugar na ordem de peso e o `pnpm test` como testes. O Package ou o Hammer por
comando, na R43.1: Package em `install`, `add` e `pub get`, e Hammer em `build`, `run build` e `flutter build`.

**Evidência:** —

#### P48 — O Jira e o Confluence com o chip que abre no navegador (pedido 27)

Executa D39 · Estimado: 1 h · Executado: — h

- [ ] **1.** Teste que falha: a chamada MCP do Jira ou do Confluence, já identificada pelo `NativeChatMcpIdentity`, vira
      o chip com a chave do card (`FIX-123`, por exemplo) ou o título da página
- [ ] **2.** O clique no chip abre o card ou a página no navegador
- [ ] **3.** Os testes; commit e push; conferir uma linha de cada no BrzA Studio, com Anderson

**Pendências:** fechadas na R38.3, na R40.2 e na R41.3: "FIX-123 — <resumo, se vier na saída>" e "<título da página>";
o site pelo `cloudId` quando é domínio, senão pelo `siteUrl` do Jira do app, e sem nenhum o chip só copia; o chip só
no desktop. O Confluence com o `file-text` do lucide (R43.2), e o título e a URL da página pela leitura defensiva (R44.1).

**Evidência:** —

#### P49 — A ferramenta Skill com ícone e título (pedido 27)

Executa D39 · Estimado: 0,3 h · Executado: 0,2 h

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

#### P50 — O Figma com logo, nome do nó e miniatura (pedido 27)

Executa D39 · Estimado: 0,3 h · Executado: 0,3 h

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

#### P51 — O Firebase e o Context7 com ícone e nome no título (pedido 27)

Executa D39 · Estimado: 0,3 h · Executado: 0,2 h

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

#### P52 — Os blocos de código e as tabelas com 120 colunas na largura total (pedido 28)

Executa D40 · Estimado: 1 h · Executado: 0,6 h

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

**Pendências, a perguntar a Anderson com opções:** respondidas em 2026-10-27, na sessão
`brza-studio-chat-blocos-120-colunas`:

- o alinhamento: "À esquerda", com o texto;
- os outros elementos: o diff de edição (`NativeChatDiffView` e as linhas do `NativeChatDiffCard`) e os diagramas e
  visuais (o Mermaid e o `NativeChatInlineVisual`) seguem a regra; a saída de ferramenta não.

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

#### P53 — Os links do chat em azul claro (pedido 29)

Executa D41 · Estimado: 0,3 h · Executado: 0,1 h

- [x] **1.** Teste que falha: o link do chat usa a variável `--chat-link`, `#79C0FF` no tema escuro e `#0969DA` no
      claro, e não o `--chat-foreground-strong` de hoje, em `.native-chat-markdown a`
      (`src/renderer/src/components/native-chat/native-chat-markdown.css:18`)
- [x] **2.** O sublinhado segue com 40% da cor (`color-mix(in srgb, currentColor 40%, transparent)`), e a mensagem com
      tom `faint` segue herdando a cor (`:55`); os testes; commit e push
- [ ] **3.** Conferir um link em azul claro nos dois temas, no BrzA Studio, com Anderson
- [ ] **4.** O link sobre código inline também em azul: em 2026-10-28, numa sessão de chat do `brza-workspace`, Anderson
      viu o caminho `~/Projects/fixfy`, escrito como código inline e virado link pelo chat, em branco e não em azul
      ("nesse link, o texto ficou branco e não azul"); o `color: var(--chat-code-foreground)` de
      `.native-chat-markdown code` (`native-chat-markdown.css:35`) vence a cor que o `code` herdaria do link

**Rodada de 2026-10-28, na sessão `pln-001-retomar`**, respondida por Anderson pelo AskUserQuestion, fora da numeração
R para não colidir com a sessão da Run `run_de875fc52a75`:

- a conferência do C8, do C9 e do P37.1, que o build instalado (`de3fb921ad1`, que contém o `f130a85e578`, o
  `52f7051a45d` e o `9d289d2b631`) já permite: "Agora, no instalado (Recomendado)";
- a cor do P53.4: "color: inherit (Recomendado)" — `.native-chat-markdown a code { color: inherit }` no
  `brza-chat-link.css`, e o código mantém a borda e o fundo e segue o tom `faint` do link;
- quem executa o P53.4 e o P40: "Workers do Orca daqui (Recomendado)" — um worker Sonnet para o P53.4, em
  `.worktrees/pln-001-p53-4`, numa Run separada da `run_de875fc52a75`; esta sessão grava a evidência.

**Evidência:** commit [`9d289d2b631`](https://github.com/brz-anderson/brza-studio/commit/9d289d2b631), na `master` do
`brza-studio`. O `--chat-link` mora em `src/renderer/src/components/native-chat/brza-chat-link.css`, com o padrão do
`main.css`: `:root` e `.dark`, mais `.native-chat-appearance[data-native-chat-scheme]`, que vem do fundo do terminal no
modo "igualar ao terminal". A linha upstream de `.native-chat-markdown a` passou a ler `var(--chat-link)`; o sublinhado e
a regra do tom `faint` não mudaram, e o `faint` ganha pela especificidade. **Desvio do texto do passo:** sem teste de
unidade, porque a cor é só CSS, e o jsdom não a resolve. Conferido na fixture: `#79C0FF` no escuro e `#0969DA` no claro.
Falta a conferência no BrzA Studio com Anderson (subpasso 3).

#### P54 — A imagem da ferramenta extraída para arquivo (pedido 30)

Executa D42 · executor: sessão do `brza-studio`

Estimado: 3 h · Executado: — h

Depois do P44 ao P50 (R42.4), e antes do P55.

- [ ] **1.** Teste que falha, em `src/main/native-chat/brza/brza-tool-result-images.test.ts`: o `brzaToolResultImages`
      de um `content` com `{ type: 'image', source: { type: 'base64', media_type: 'image/png', data } }` devolve um
      `image-ref` com o `path` no temp (`brza-tool-images/<sha256 de 16>.png`), e o arquivo tem os bytes; a mesma imagem
      duas vezes dá o mesmo caminho e um arquivo só; `source.type: 'url'` vira `image-ref` com a `url`; `media_type` fora
      de gif, jpeg, png e webp fica de fora
- [ ] **2.** Teste que falha nos dois decoders: o `tool_result` com texto e imagem dá o `output` de hoje e mais o
      `images` — o ao vivo (`claudeToolResults` e `claudeToolBody`, `claude-structured-item-translation.ts:150-163` e
      `:176-187`) e o do histórico (`toolResultBlock`, `transcript-record-blocks.ts:90-97`)
- [ ] **3.** O campo `images?: NativeChatImageRefBlock[]` no `NativeChatToolResultBlock` (`native-chat-types.ts:94-104`)
      e no corpo `tool-call` do journal (`agent-session-journal-types.ts:132`), uma linha de montagem em cada decoder e a
      projeção do journal ao renderer; os dois pontos "A conferir no passo" do D42
- [ ] **4.** Os testes do que foi tocado e o `pnpm check:changed --base=origin/master`; commit e push

**Evidência:** —

#### P55 — A miniatura na linha da ferramenta (pedido 30)

Executa D43 · executor: sessão do `brza-studio`

Estimado: 1,5 h · Executado: — h

Depois do P54. Cobre o P50.2 (PLN-001/R38.4).

- [ ] **1.** Teste que falha, em `src/renderer/src/components/native-chat/brza/BrzaToolImageStrip.test.tsx`: a linha com
      `result.images` mostra as miniaturas com a linha fechada, abaixo do título; com seis imagens, quatro miniaturas e
      um "+2", cujo clique abre o corpo da linha, com as seis em faixa com quebra; sem `images`, a linha não muda
- [ ] **2.** O `BrzaToolImageStrip`, com o `ExpandableMarkdownImage` (`MarkdownImageLightbox.tsx:28`) e a leitura do
      `NativeChatMarkdownImage` (o `useLocalImageSrc` com o acesso `chat-image` e a carga perto da tela), e a linha de
      montagem em `NativeChatToolLine.tsx`, fora do corpo aberto (`:75`)
- [ ] **3.** Os testes; commit e push; conferir no BrzA Studio, com Anderson: um `Read` de PNG, um `get_screenshot` do
      Figma e um print do browser, cada um com a miniatura na linha fechada e ampliando no clique

**Evidência:** —

#### P56 — A miniatura do caminho ou da URL de imagem solto no texto (pedido 30)

Executa D44 · executor: sessão do `brza-studio`

Estimado: 3 h · Executado: — h

Não depende do P54 nem do P55; roda depois do P44 ao P50 (R42.4).

- [ ] **1.** Teste que falha, num teste do plugin em `src/renderer/src/components/native-chat/brza/` e num caso em
      `NativeChatMarkdown.image-preview.test.tsx`: na mensagem terminada, o `` `/abs/shot.png` `` que existe, o
      `[print](shot.png)` e o `https://…/a.png` ganham a miniatura abaixo do parágrafo, e o link fica; a mesma imagem duas
      vezes, ou já num `![]()`, dá uma miniatura só; o caminho que não existe não mostra nada; o bloco cercado não muda;
      com `streaming`, nada entra
- [ ] **2.** O plugin remark do BrzA, ligado pelos `remarkPlugins` da extensão (`NativeChatMarkdown.tsx:68`), e o
      componente que desenha o nó com o `NativeChatMarkdownImage` e some na falha. Conferir a ordem dos plugins: o
      `remarkNativeChatFileLinks` entra depois dos outros (`CommentMarkdown.tsx:367-368`), e o do BrzA precisa ver o link
      que ele cria, ou ler o `inlineCode` com o mesmo teste de existência
- [ ] **3.** Os testes; commit e push; conferir no BrzA Studio, com Anderson: uma resposta que cite um print por caminho
      em código inline e outra com uma URL de imagem

**Evidência:** —

#### P57 — A conferência das quatro partes da prévia (pedido 30)

Executa D42, D43 e D44 · executor: Anderson, com a sessão que conduz

Estimado: 0,3 h · Executado: — h

Depois do P55 e do P56.

- [ ] **1.** No BrzA Studio: um `![]()` local e um remoto na resposta do agente; uma imagem colada e uma arrastada, com
      a miniatura na mensagem enviada; o clique amplia, com pan e zoom, nos quatro casos (R36.1)
- [ ] **2.** O Observado e o veredito na linha da evidência

**Evidência:** —

## Regressão

Caminhos relativos à raiz do `brza-studio`. Os testes rodam como diz a `## Restrições`; em 2026-10-28, os 25 arquivos
de teste citados abaixo passaram (359 testes), na `master`. "Teste a escrever" está na
[issue de depois da Run](../../work/issues/pln-001-passos-e-desvios-no-molde-depois-da-run.md).

- **O ícone e o título do upstream para toda ferramenta fora das categorias do BrzA** (`Read`, `Edit`, busca, web, MCP
  genérico, `ls`) ficam como estão. Como se confere: `src/shared/native-chat/tools/native-chat-tool-icon.test.ts`
  (`:60`, `:74`, `:81`, `:226`), `src/shared/native-chat/tools/brza/brza-tool-icon-mount.test.ts:25` e
  `native-chat-tool-line-label.test.ts`.
- **O comando de navegador do app (`brza snapshot`, `orca …`) mantém o globo**, e nenhuma categoria do BrzA o captura,
  nem em composto com `git` ou `gh` (R41.1). Como se confere: `native-chat-tool-icon.test.ts:180`,
  `brza/brza-cli-category.test.ts:27` e `native-chat-tool-run-sentence.test.ts:48`.
- **O comando sem categoria do BrzA segue com o verbo, o alvo e o título do upstream**, e a frase da corrida não muda.
  Como se confere: `brza/brza-tool-line-title.test.ts:48` e `native-chat-tool-run-sentence.test.ts`; o ramo do comando
  em `native-chat-tool-line-label.ts:94-108` não tem teste — teste a escrever, no P44.
- **A corrida com categorias misturadas, ou só com as do upstream, mantém o glifo do upstream.** Como se confere:
  `brza/brza-tool-icon-mount.test.ts:30` e `native-chat-tool-icon.test.ts:164-219`.
- **O mobile cai no ícone lucide equivalente para todo logo de marca e mantém os glifos do upstream.** Como se confere:
  `pnpm --dir mobile typecheck`, que quebra se faltar glifo no
  `mobile/src/session/native-chat/transcript/brza/brza-mobile-tool-glyphs.ts:36`, e
  `MobileNativeChatToolRun.test.tsx`; o recuo de cada logo não tem teste — teste a escrever, do P43.
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
  Retomar automaticamente e o Continuar do corte do Orca seguem iguais. O "Continuar em" do P40, ainda aberto, entra ao
  lado, com o teste dele. Como se confere: `NativeChatNoticeRow.test.tsx:262-281,297,330` e
  `NativeChatInterruptedContinue.test.tsx:191,259,267`.
- **A barra do Markdown em diff mantém fonte e renderizado, com o padrão `source`; o diff combinado fica sem modos, e o
  Mermaid, o CSV e o notebook não ganham o olho.** Como se confere:
  `src/renderer/src/components/editor/markdown-preview-controls.test.ts:20,30,39,59`.
- **O build local de Mac e Linux e o atualizador do app de release ficam como estão**: só a versão
  `-local.<ms>.<commit>` desliga o atualizador (`src/main/updater/updater-enabled.ts:4-9`), e os canais `ORCA_WIN_*` do
  CI não mudam. Como se confere: `config/scripts/build-mac-local.test.mjs`, `build-win-local.test.mjs`,
  `build-linux-local.test.mjs` e `electron-builder-config.test.mjs`; o `isUpdaterEnabled()` com versão de release não
  tem teste — teste a escrever, do P26.
- **O merge do `stablyai/orca` segue com conflito pequeno**: o BrzA toca o upstream só em linhas de montagem, e o resto
  mora em pastas `brza/`. Como se confere: `git diff $(git merge-base master upstream/main) master --numstat --` nos
  `native-chat-tool-icon.ts`, `native-chat-tool-line-label.ts`, `NativeChatMarkdown.tsx` e `NativeChatToolIcon.tsx`, que
  davam 14/2, 5/0, 4/1 e 3/1 em 2026-10-28.

## Desvios

- **X1 — O `build:win` também compila o launcher da CLI e o agent hook, em Rust, para x64.** O `afterPack` do
  `electron-builder.config.cjs` falha sem o `orca-agent-hook.exe` (`verifyPackagedWindowsAgentHook`), e nem o
  `build:desktop` nem o `build:win` antigo o compilavam; o CI os faz no `build:release`. O D21 não muda; o P27 pede o
  Rust (rustup) no Windows.
- **X2 — O Novo Chat aparece só no chat estruturado.** A vista de chat sobre o terminal (`NativeChatResolvedView`) não
  sabe o grupo da aba nem abre o chat por conta própria, e ali o botão não aparece, como o rewind. O D28 não muda: a aba
  nova é de chat, e a vista do terminal fica para um passo próprio, se Anderson pedir.
- **X3 — O Editar na mensagem do usuário aparece só no chat estruturado.** Pelo mesmo motivo do X2: a vista de chat
  sobre o terminal não tem a caixa do chat estruturado, e ali o botão não aparece, como o rewind. O D33 não muda.
- **X4 — A retomada vencida dispara quando o host do main sobe, e não pelo `native-chat-resume-on-restart-store.ts`.**
  O store do restart é do renderer e só corre com a janela aberta; a agenda é do host, que sobe ao abrir o Orca (e no
  servidor remoto, onde o chat roda), e ali dispara o que venceu com o Orca fechado, só se o chat ainda está no corte.
  O app móvel não tem o botão; a agenda no host já o serve, quando um passo pedir. O D35 não muda.
- **X5 — O Bifurcar aparece só no chat estruturado do Claude.** O corte é o `forkSession` do SDK do Claude, e a vista
  de chat sobre o terminal não tem a sessão estruturada que o canal pede, como no X2. O app móvel não tem o botão; o
  `agentSession.forkThroughMessage` já o serve, quando um passo pedir. O D27 não muda.
- **X6 — A chave do Markdown na caixa fica no `NativeChatGlobalSettings`, e não em `global-settings-types.ts`.** O
  `global-settings-types.ts` está no teto de 300 linhas do `max-lines`, e o hook do commit barra a linha a mais; o
  grupo `NativeChatGlobalSettings` (`native-chat-appearance-settings.ts`) compõe o mesmo `GlobalSettings` pelo
  `GlobalSettingsBase`, como as outras chaves do chat. O D32 não muda.
- **X7 — O instalador do P27.1 sai num runner Windows do GitHub, e não na máquina Windows nem no Docker do Mac.** O
  `build:win` compila com MSVC, pelo node-gyp e contra os headers do Electron, quatro addons C++ com patch: o
  `node-pty`, o `@vscode/windows-process-tree`, o `@orca/windows-registry` e o `@orca/windows-security`. Nem o node-gyp
  nem o `@electron/rebuild` compilam win32 a partir do macOS ou do Linux, e a imagem
  `electronuserland/builder:wine` não traz MSVC. Os prebuilds não servem: o `rebuild-native-deps.mjs` e o `afterPack`
  recusam o do `node-pty` sem a negação do breakaway e o do `windows-process-tree` com `ReadProcessMemory`. Anderson
  escolheu o runner, entre ele, a máquina Windows e o MSVC no wine, este de dias e frágil. O workflow
  `build-win-local.yml` vive só no fork (`if: github.repository != 'stablyai/orca'`), e o runner padrão sai sem custo
  no repositório público. O D21 não muda: é o mesmo `pnpm run build:win`. A instalação, o SmartScreen e o "Sobre" (P27.2
  e P27.3) seguem com Anderson, no Windows.
- **X8 — O instalador de Mac também sai num runner do GitHub, num DMG arm64 assinado ad hoc.** Anderson pediu o
  "Local Mac Installer" na sessão da raiz de 2026-10-26 ("o build com MacOS no GitHub Actions tbm é de graça em repo
  publico? se sim, crie um Local Mac Installer"), no formato DMG e no mesmo release do Windows. O `build:mac` ganhou o
  `--dmg`, que troca o `--mac dir` pelo `--mac dmg`; o padrão segue `dir`. O `build-mac-local.yml` roda no
  `macos-latest` do fork (`if: github.repository != 'stablyai/orca'`), sem custo no repositório público. O DMG é só
  arm64, como o P1 decidiu, com a versão `-local.<ms>.<commit>`, que desliga o atualizador. Sem `CSC_NAME` no runner, o
  app sai assinado ad hoc e sem notarização: o baixado pede o "Abrir Mesmo Assim" (Ajustes > Privacidade e Segurança)
  ou `xattr -dr com.apple.quarantine /Applications/Orca.app`, e isso vai às notas do release. Commit `ee06556cb8f`, com
  o teste do alvo `dmg` no `build-mac-local.test.mjs` (falha antes, passa depois) e os testes que varrem os workflows
  verdes: `build-mac-local` (7), `ci-draft-pr-admission` (79), `pr-preflight-gates` (42) e `workflow-ref-reachability`
  (5); o `ci-background-steps` saiu no upstream (#33796), com a `v1.4.242`. O run `40432265386` saiu `success` em
  12 min 3 s; o `orca-macos-arm64.dmg` tem 239 MiB (250705822 bytes), sha256
  `ed412bcdabd40cfa37ffac2a616862f6eaecedc216eb4be03a68ea44f0498145`, `hdiutil verify` válido, `codesign -dv` com
  `Signature=adhoc` e `Mach-O thin (arm64)`, e o app é o `1.4.242-local.1793064322587.ee06556cb8fe`. O D1 não muda: é o
  mesmo `pnpm run build:mac`.
- **X9 — As categorias do BrzA refinam só o ícone, sem estender o `NativeChatToolCategory` nem o `CATEGORY_BY_ROW_WORD`.**
  O D37 falava numa linha no `CATEGORY_BY_ROW_WORD`; o worker do P43 montou o módulo nos dois resolvedores de ícone
  (`nativeChatToolIconName` e `nativeChatToolRunIconName`), na união `NativeChatToolIconName` e nas tabelas de glifos do
  desktop e do mobile. Estender a união do upstream obrigaria a mexer nos `Record` exaustivos dele (as frases da corrida,
  o switch do rótulo), e o `git` deixaria de ser `unknown`, perdendo o tratamento de comando no rótulo da linha. O
  contrato do D37 segue: módulo do BrzA e uma linha de montagem por ponto do upstream. O título do P44 ao P51 sai do
  `brzaToolCategory`. Citado no P43.
- **X10 — Os recuos de marca no mobile: git → `git-branch`, GitHub → `git-pull-request`, Jira → `square-kanban`.** O D37
  não os fixava; foi escolha do worker do P43, a conferir com Anderson junto do P44 e do P48. Citado no P43.
- **X11 — O nome do nó do Figma sai de um formato de saída suposto.** O D39 não dizia onde o nome está na saída; o
  worker do P50 não leu saída real (o classificador de permissão negou ler transcrições antigas) e o tirou do
  `name` do `<frame id=… name=…>` do `get_metadata` e do `data-name` do `get_design_context`, casando pelo `nodeId`
  pedido (`1-2` e `1:2` equivalem) e lendo só as primeiras 200 tags, para a saída cortada na cabeça não atrapalhar. Se
  o formato real for outro, o ajuste fica só em `nodeNameFromOutput`. A conferir com Anderson. Citado no P50.
- **X12 — O `nodeId` do título sai normalizado com dois-pontos** (`12-34` vira `12:34`). Escolha do worker do P50.
  Citado no P50.

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

## Decisões

Notas de decisão do workspace da Fixfy, ao lado deste clone:

- [O Orca da Fixfy substitui o original, sem atualizador, sincroniza por tag e guarda o código da Fixfy em pasta própria](../../../fixfy/work/decisions/orca-da-fixfy-substitui-o-original-e-sincroniza-por-tag.md)
  — PLN-025/R10 da Fixfy, `done`.
- [O orca-dev commita com o noreply do brz-anderson, pela chave personal, com push direto na main](../../../fixfy/work/decisions/orca-dev-commita-como-brz-anderson-com-push-na-main.md)
  — PLN-025/R14 da Fixfy, `done`.

## Pendências conhecidas

- [Os Passos e os Desvios do PLN-001 no molde, depois da Run do P44 ao P50](../../work/issues/pln-001-passos-e-desvios-no-molde-depois-da-run.md)
  — da rodada de 2026-10-28 na sessão `pln-001-norma-fixfy`; espera a Run `run_de875fc52a75` fechar.

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

O C1 e o C2 esperam a Run `run_de875fc52a75`: o build instalado (`de3fb921ad1`) não tem o `9b8a3e2e672` nem o
`fbff699fa58`, e a coordenadora da Run roda do app instalado. Na rodada de 2026-10-28 da sessão `pln-001-retomar`,
Anderson escolheu "Depois da Run, num build só (Recomendado)": uma instalação para o C1 ao C7 e o C10.

## Fechamento

- [ ] Todo passo `[x]` com evidência, ou `[-]` com motivo.
- [ ] Todo achado com destino que existe.
- [ ] Um resumo por commit ou PR do `brza-studio` da entrega, com o link do plano: os achados e o destino de cada um.
      Trabalho só em notas de `work/` e `plans/` não tem resumo.
- [ ] O durável saiu para a casa dona e está em `## Decisões` e `## Documentação`: a decisão em `work/decisions/`, a
      norma do `brza-studio`, o guia.
- [ ] As decisões que o plano respondeu estão `done`, citando a rodada.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
