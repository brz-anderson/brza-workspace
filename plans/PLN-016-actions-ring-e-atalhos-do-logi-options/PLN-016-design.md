# PLN-016 — Desenho

## Desenho

### Terreno

O levantamento do P1, de 2026-11-07, feito por dois `collector`. Cada fato leva `[F# · tipo · confiança]`; o que é `inferido` ou abaixo de 80 não foi conferido. Conferi por amostra: `Mod+Shift+J` no `definitions-core-4.ts` (darwin) e o `Esc` e o `Alt+Enter` no `agy/package.json`.

#### Atalhos por app

##### Atalhos macOS por app (PLN-016, Actions Ring)

Legenda: Mod = Cmd. `—` = sem atalho padrão. `NÃO ACHADO` = não localizado em fonte aberta. Marca: [id · tipo · confiança].

Fontes (abertas nesta execução):
- S1 = `~/Projects/brza-studio/src/shared/keybindings/definitions-core-{1..4}.ts` (linha entre parênteses). O app instalado BrzA Studio.app é 1.4.251-alpha.1.local (mesmo commit f7b9936 do código, via Info.plist), então S1 vale para o app.
- S2 = `/Applications/Orca.app/Contents/Resources/app.asar.unpacked/out/shared/keybindings/definitions-core-{1..4}.js`: Orca 1.4.247 instalado tem os mesmos padrões de S1 para todas as ações listadas (comparei id a id).
- S3 = https://cursor.com/docs/configuration/kbd (Cursor; não há keybindings.json de usuário em `~/Library/Application Support/Cursor/User`).
- S4 = `/Applications/Antigravity IDE.app/Contents/Resources/app/extensions/agy/package.json` (contributes.keybindings) e `.../out/vs/workbench/workbench.desktop.main.js` (antigravity.openAgent, `keybinding:{primary:2592}` = Cmd+Alt+B). Não há keybindings.json de usuário.
- S5 = https://antigravity.google/docs/getting-started (app/CLI Antigravity; atenção: a tabela de "Navigation" é do app novo, não do IDE).
- S6 = https://code.visualstudio.com/docs/terminal/basics e https://code.visualstudio.com/docs/reference/default-keybindings (base VS Code: Cursor e Antigravity IDE 1.107.0).

##### Ações em comum entre os 4

| ação | BrzA Studio | Orca | Cursor | Antigravity | fonte |
|---|---|---|---|---|---|
| Abrir arquivo (quick open) | Mod+P `worktree.quickOpen` [F1 · lido · 95] | Mod+P [F2 · lido · 95] | Mod+P (VS Code) [F3 · inferido · 75] | Mod+P (VS Code; S5 lista ⌘P "File search" no app novo) [F4 · doc · 85] | S1 core-1:12; S2 core-1.js:12; S6 |
| Command palette | NÃO ACHADO (sem ação em definitions; Mod+J é paleta de worktrees) [F5 · lido · 85] | idem [F5] | Mod+Shift+P [F6 · doc · 95] | Mod+Shift+P (VS Code; S5 app novo) [F7 · doc · 95] | S1 core-1:7-12,40; S3; S6 |
| Novo terminal/aba de terminal | Mod+T `tab.newTerminal` [F8 · lido · 95] | Mod+T [F9 · lido · 95] | Ctrl+Shift+` (VS Code) [F10 · doc · 90] | Ctrl+Shift+` (VS Code) [F10 · doc · 90] | S1 core-2:74; S2 core-2.js:75; S6 |
| Alternar sidebar esquerda | Mod+B `sidebar.left.toggle` [F11 · lido · 95] | Mod+B [F12 · lido · 95] | Mod+B (VS Code) [F13 · doc · 90] | Mod+B (VS Code) [F13 · doc · 90] | S1 core-1:197; S2 core-1.js:197; S6 default-keybindings |
| Buscar nos arquivos | Mod+Shift+F `sidebar.search.toggle` [F14 · lido · 95] | Mod+Shift+F [F15 · lido · 95] | Mod+Shift+F (VS Code, não listado na página oficial) [F16 · inferido · 75] | Mod+Shift+F (idem) [F16 · inferido · 75] | S1 core-1:221; S2 core-1.js:221 |
| Trocar/mudar de aba | Mod+Shift+] / [ (todos os tipos), Mod+Alt+] / [ (mesmo tipo), Ctrl+Tab (recente), Ctrl+1..9 [F17 · lido · 95] | idem [F18 · lido · 95] | Ctrl+Tab; Cmd+Alt+←/→ [F19 · inferido · 70] | idem [F19 · inferido · 70] | S1 core-2:184-216,245; S2 core-2.js |
| Dividir editor/painel | terminal: Mod+D (direita), Mod+Shift+D (baixo) [F20 · lido · 95] | idem [F21 · lido · 95] | Mod+\ dividir editor [F22 · doc · 90] | Mod+\ [F22 · doc · 90] | S1 core-4:88-101; S2 core-4.js:77-89; S6 default-keybindings |
| Buscar no arquivo | Mod+F (editor/terminal/chat) [F23 · lido · 95] | Mod+F [F23 · lido · 95] | Mod+F [F24 · inferido · 75] | Mod+F (S5 app novo) [F25 · doc · 85] | S1 core-3:56,255; core-4:25 |
| Abrir/focar chat de IA | Mod+Shift+J `terminal.toggleNativeChat` (alterna terminal/chat nativo) [F26 · lido · 95] | Mod+Shift+J [F27 · lido · 95] | Mod+L ou Mod+I alterna painel lateral [F28 · doc · 95] | Mod+L (foco no painel agente; no editor adiciona seleção ao chat) [F29 · lido · 95] | S1 core-4:35-36; S2 core-4.js:24; S3; S4 agy/package.json keybindings |
| Novo chat/agente | Mod+Alt+T `tab.newAgent` (nova aba com agente padrão) [F30 · lido · 95] | Mod+Alt+T [F31 · lido · 95] | Mod+N ou Mod+R (no chat) [F32 · doc · 90] | Mod+Shift+L `startNewConversation` [F33 · lido · 95] | S1 core-2:83-86; S2 core-2.js:85; S3; S4 |

##### Exclusivos / sem equivalente nos 4

##### BrzA Studio e Orca (idênticos nos padrões; BrzA Studio 1.4.251, Orca 1.4.247)
| ação | atalho | fonte |
|---|---|---|
| Trocar de worktree (paleta) | Mod+J [F34 · lido · 95] | S1 core-1:39-40 |
| Worktree anterior/seguinte (lista) | Mod+Shift+↑ / Mod+Shift+↓ [F35 · lido · 95] | S1 core-1:51,61 |
| Ir ao worktree N | Mod+1..9 [F36 · lido · 95] | S1 core-1:165 |
| Criar worktree | Mod+N (e Mod+Shift+N) [F37 · lido · 95] | S1 core-1:71 |
| Voltar/avançar histórico de worktree | Mod+Alt+← / → [F38 · lido · 95] | S1 core-2:58,66 |
| Alternar sidebar direita | Mod+L [F39 · lido · 95] | S1 core-1:205 |
| Explorer / Source Control | Mod+Shift+E / Mod+Shift+G [F40 · lido · 95] | S1 core-1:213,229 |
| Terminal flutuante | Mod+Alt+A (maximizar: Mod+Alt+Shift+A) [F41 · lido · 95] | S1 core-1:285,305 |
| Foco entre painéis do terminal | Mod+] / Mod+[ ; expandir painel Mod+Shift+Enter [F42 · lido · 95] | S1 core-3:271-295 |
| Fechar aba / reabrir fechada | Mod+W / Mod+Shift+T [F43 · lido · 95] | S1 core-2:145,175 |
| Limpar terminal | Mod+K [F44 · lido · 95] | S1 core-3:263 |
| Nova aba de navegador / markdown | Mod+Shift+B / Mod+Shift+M [F45 · lido · 95] | S1 core-2:95,129 |
| Nota de revisão no diff | Mod+Shift+A (enviar notas ao agente: sem atalho) [F46 · lido · 95] | S1 core-3:131,150 |
| Próxima/anterior mudança (diff) | F7 / Shift+F7 [F47 · lido · 95] | S1 core-3:111,120 |
| Ditado por voz | Mod+E [F48 · lido · 95] | S1 core-1:173 |
| Parar o agente | NÃO ACHADO nas definições de keybinding (nenhuma ação stop/interrupt); Esc no chat nativo não foi verificado [F49 · lido · 80] | grep em src/shared/keybindings/definitions*.ts |
| Aceitar/rejeitar diff | NÃO ACHADO (só nota de revisão) [F50 · lido · 85] | S1 core-3 |
Obs.: padrões podem ser sobrescritos por Anderson nas Settings do app; o estado local não foi lido.

##### Cursor
| ação | atalho | fonte |
|---|---|---|
| Alternar layout Agent | Mod+E [F51 · doc · 95] | S3 |
| Menu de modos / alternar modelos | Mod+. / Mod+/ ; Mod+Alt+/ [F52 · doc · 95] | S3 |
| Parar geração | Mod+Shift+Backspace (sem mudanças pendentes) [F53 · doc · 90] | S3 |
| Aceitar todas as mudanças | Mod+Return (com mudanças sugeridas) [F54 · doc · 95] | S3 |
| Rejeitar todas | Mod+Shift+Backspace (com mudanças sugeridas; mesma tecla do cancelar) [F55 · doc · 95] | S3 |
| Adicionar seleção ao chat | Mod+Shift+L [F56 · doc · 95] | S3 |
| Chat anterior/próximo, fechar, nova aba de chat | Mod+[ / Mod+] , Mod+W , Mod+T [F57 · doc · 95] | S3 |
| Enviar à força / mudar modo | Mod+Return; Shift+Tab [F58 · doc · 95] | S3 |
| Configurações do Cursor / voz | Mod+Shift+J / Mod+Shift+Space [F59 · doc · 95] | S3 |
| Terminal | Ctrl+` alternar (VS Code) [F60 · doc · 90] | S6 |

##### Antigravity IDE (S4, extensão agy; padrão mac)
| ação | atalho | fonte |
|---|---|---|
| Painel do agente (alternar) | Mod+Alt+B [F61 · lido · 85, premissa: primary 2592 = CtrlCmd(2048)+Alt(512)+KeyB(32) no enum do VS Code] | workbench.desktop.main.js, `antigravity.openAgent` |
| Aceitar passo do agente / hunk / tudo | Alt+Enter [F62 · lido · 95] | agy/package.json keybindings |
| Rejeitar passo / hunk / tudo | Alt+Shift+Enter [F63 · lido · 95] | idem |
| Interromper o agente | Esc (com agente rodando e foco no painel) [F64 · lido · 95] | idem |
| Adicionar seleção do terminal ao chat | Mod+L com foco no terminal [F65 · lido · 95] | idem |
| Comentar seleção para o agente | Mod+Alt+M [F66 · lido · 95] | idem |
| Aceitar/escapar completion | Tab / Esc [F67 · lido · 95] | idem |
| App Antigravity (não o IDE): conversa anterior/próxima, ⌘K conversa | Alt+↑/↓, Mod+K [F68 · doc · 80, é o app novo, não o IDE] | S5 |
| Terminal | Ctrl+` alternar, Ctrl+Shift+` novo, Mod+\ dividir (VS Code) [F69 · doc · 90] | S6 |

##### Notas
- Cursor e Antigravity não têm `keybindings.json` de usuário no disco; as listas do Cursor vêm só da doc (o app não foi aberto para conferir). Itens `inferido` são padrões do VS Code que as páginas oficiais abertas não listam.
- Mod+Alt+B no Antigravity coincide com `tab.newBrowserSplitRight` do BrzA Studio/Orca, mas são apps distintos.

#### Logi Options+: ring, exportação e scripts

##### PLN-016 levantamento: Logi Options+ / Actions Ring (2026-11-07)

Marca: [Fn · tipo · confiança]. Os JSON do disco foram lidos em cópia (/private/tmp/pln016/cp/), nada foi alterado no original.

##### 4. Versão e MX Master 4
- F1 Options+ instalado: CFBundleShortVersionString = CFBundleVersion = 2.9.1013853 (`defaults read /Applications/logioptionsplus.app/Contents/Info`). [F1 · rodado · 95]
- F2 O settings.db registra `analytics_app_version` 2.9.1013853 e o aparelho `2b042` (MX Master 4) como onboarded (~/Library/Application Support/LogiOptionsPlus/config.json; settings.db copiado, chave `settings_backup_state_v2.knownDevices`). [F2 · lido · 92]
- F3 O Actions Ring é um dispositivo "virtual" próprio (modelId 10000000) ao lado do MX Master 4 (settings.db `migration_report.devices`). [F3 · lido · 90]
- F4 Doc oficial (hub.sync.logitech.com/mx-master-4/post/getting-started---mx-master-4-LSEt5tZXsbeMP3c): o Haptic Sense Panel, ao clicar, abre o Actions Ring; o Options+ é obrigatório para o ring. [F4 · doc · 85] Ressalva: a página também fala de "Logi Tune" para haptics/botões por app, o que pode ser texto da própria página ou erro da leitura; confirmar na UI.
- F5 No disco, a atribuição "Show Radial Menu" (`SHOW_RADIAL_MENU`, tags PRESET_TAG_MX_DIDOT_ACTION_RING e PRESET_TAG_LPS_ACTION_RING) está no slot `mx-master-4-2b042_c416`, ou seja, é um botão do mouse (provavelmente o painel háptico); o mapeamento c416 -> painel é inferido. [F5 · lido · 80]
- F6 Haptic no perfil: `hapticFeedbackLevel` 60, `isGlobalHapticsEnabled` true, `eventSourceSettings.actions_ring.isHapticsEnabled` true (settings.db, perfil default, assignment HAPTIC_SETTINGS). Doc: haptics ligado por padrão, e o modo de economia de bateria os desliga em 10% (hub.sync.logitech.com/mx-master-4/post/haptic-feedback-guide-fgAEJmLZXL9iQXK, via busca, não aberta). [F6 · lido · 90]
- F7 O ring pede Options+ 1.83 ou superior; a página oficial pede macOS 14 ou superior (futureisnow.logitech.com/en-us/software/logi-options-plus/actions-ring.html; o 1.83 veio da busca, não da página aberta). [F7 · doc · 80]

##### 1. Exportação
- F8 Backup oficial é na nuvem, não em arquivo: com conta verificada, o backup é automático (padrão ligado); há "BACKUP ALL DEVICES NOW" e, por aparelho, em Settings, "Restore Settings from backup". Fonte: hub.sync.logitech.com/k620/post/backup-device-settings-to-the-cloud-in-logitech-options-B0vjYROUUBfnL5W. [F8 · doc · 90]
- F9 O backup é por computador (rótulo com nome, modelo e hora), a restauração só lista backups compatíveis com a máquina, e não vale entre Windows e Mac. Inclui botões de mouse/teclado, Point & Scroll e configurações por app; não inclui Flow nem configurações do app Options+. Mesma fonte. [F9 · doc · 90]
- F10 Não achei exportar/importar de perfil inteiro em arquivo. Há um pedido de recurso no UserVoice ("Export/Import Settings for Logi Devices", só título visto na busca), o que indica que não existe. [F10 · inferido · 70]
- F11 Exceção oficial: Smart Actions se exportam e importam um a um como `.json` (três pontos no canto do Smart Action, Export; importar na página Smart Actions). Fonte: support.logi.com/hc/articles/14929126110743 (só pelo resumo da busca, página não aberta). [F11 · doc · 75]
- F12 No disco, `~/Library/Application Support/LogiOptionsPlus/settings.db` (SQLite, tabelas `data` e `snapshots`) guarda 1 linha em `data` com um BLOB JSON de ~62 KB (schema_version 26); `snapshots` está vazia. [F12 · rodado · 95]
- F13 Esse JSON contém `serialNumber`, `udid` e `slotPrefix` do aparelho (`ever_connected_devices.devices[0]`), e os slotIds do perfil levam o modelo (`mx-master-4-2b042_c416`). Portanto não é portável às cegas: restaurar em outra máquina exigiria trocar esses IDs; não testado. [F13 · lido · 90]
- F14 As atribuições (botões, haptics, scroll, DPI) moram no JSON do settings.db, na chave `profile-<uuid>` (hoje 1 perfil, `PROFILE_NAME_DEFAULT`, 20 assignments). Macros ficam em `macros.db` (tabelas `data`, `snapshots`). [F14 · lido · 90]
- F15 O ring/Smart Actions/plugins moram em outro lugar: `~/Library/Application Support/Logi/LogiPluginService/Applications/Loupedeck70|71|72/<app>/Profiles/<id>/ProfileInfo.json` (+ ActionIcons/ActionMetadata). `Loupedeck72` é o ring, por haver nele só 1 perfil de app: `com.brzanderson.brzastudio` ("BrzA Studio Perfil") (a identificação do 72 como ring é inferida pelo conteúdo). Arquivos em JSON texto, legíveis e versionáveis. [F15 · lido · 85]
- F16 O Plugin Service faz backup local próprio: `Applications.Backups/backup_2026-11-06_18-55-22.zip` (+ backup.date, backup.hash) com a pasta Applications inteira (ApplicationInfo.json e ProfileInfo.json de cada app). Dá um caminho de cópia/restauração manual da pasta `Applications/`; não documentado oficialmente. [F16 · rodado · 90]

##### 2. Actions Ring
- F17 Estrutura em disco do perfil de app: modo `main` > workspace "Workspace 1" > `pressPages` (1 página, "Page (1)") com 8 controles (controlId 0 a 7), cada um com `pressAction`; `rotatePages` também com 8 controles (dial). O perfil default do sistema (`@_defaultmac`, "Default General Profile") tem 8 de 8 preenchidos. Logo, 8 ações por página; o perfil BrzA Studio criado hoje (modificado 2026-11-07T15:40Z) está com 0 de 8 preenchidos. Os 8 slots coincidem com o fonte de terceiros (mx-master-4.pages.dev, "até 8 atalhos"). [F17 · lido · 90]
- F18 Páginas: o arquivo suporta lista de páginas por workspace e a oficial cita "folders" que acrescentam até 72 controles extras (futureisnow.logitech.com Logi Library, via busca, não aberta); número oficial de páginas não achado. [F18 · inferido · 65]
- F19 Perfil por app: sim. Oficial: "o ring se ajusta ao app em uso" (futureisnow.logitech.com/.../actions-ring.html). No disco, cada app é uma pasta `Applications/Loupedeck72/<bundle id>/`; o ring já tem `com.brzanderson.brzastudio`, e `LoupedeckSettings.ini` tem `CurrentApplication/Loupedeck72=com.brzanderson.brzastudio`. O BrzA Studio, portanto, já foi adicionado. [F19 · lido · 88]
- F20 Herança do global: cada perfil de app lista `additionalNativePluginNames: ["DefaultMac"]` (perfil BrzA Studio), isto é, ele carrega os plugins do sistema, mas as 8 posições do perfil de app estão vazias e o ring do app é um layout separado; não vi herança de slot por slot. A resposta fechada exige teste na UI. [F20 · inferido · 70]
- F21 Adicionar app fora da lista: o settings.db tem `applications.applications` (5 entradas, com applicationPath) e `iconsLocalPathCache` com 92 .app, entre eles Orca.app, Cursor.app, `Antigravity IDE.app` e `BrzA Studio.app`, de modo que o Options+ já indexou esses apps. O botão exato "adicionar app" na UI não foi confirmado em doc oficial. [F21 · lido · 80]
- F22 Tipos de ação em Smart Actions (que o ring aceita arrastados): AI Prompt Builder, Application, Keystroke, Text, Haptic feedback (só com MX Master 4), System actions, mais Delay; executam em ordem, reordenáveis (support.logi.com/hc/articles/14307858722327). Não há "Run script/Shell" na lista. [F22 · doc · 90]
- F23 Dos assignments no disco, o macro carrega `type` (ex.: `SYSTEM`, e no macro `keystroke`/`mouse`, com `actionName` como "Cmd + Z"), de modo que atalho de teclado é nativo. [F23 · lido · 88]
- F24 O ring também aceita ações de plugin (Smart Actions, plugins, "tools"): futureisnow.logitech.com/.../actions-ring.html. [F24 · doc · 85]

##### 3. Scripts
- F25 Nativamente a lista de ações (F22) não tem shell. Um terceiro (docs do DockDoor, via busca, não aberta) diz que no Options+ se escolhe Smart Actions e "AppleScript" como ação, o que não bate com a lista oficial; marcar como não confirmado. [F25 · inferido · 55]
- F26 Caminho garantido sem script: ação "Application" abre um app (ex.: o próprio `.app` de um wrapper); wrapper Automator/Shortcuts/.app que roda `do shell script` é a ponte, mas é inferência. [F26 · inferido · 60]
- F27 Logi Actions SDK: C# (DLL dentro do Logi Plugin Service, .NET 8, com Logi Plugin Tool) ou Node.js (alpha/beta, processo separado via IPC, funcionalidades limitadas), macOS e Windows. Dev: `dotnet build` gera `.link` em `~/Library/Application Support/Logi/LogiPluginService/Plugins/` (a pasta `Plugins/` ainda não existe nesta máquina) e hot reload com `dotnet watch build`. Distribuição: pacote `.lplug4` e marketplace com aprovação. Fontes: logitech.github.io/actions-sdk-docs/getting-started e /csharp/plugin-development/introduction. [F27 · doc · 90]
- F28 As docs abertas não dizem se o plugin pode iniciar processo externo nem tratam de Acessibilidade/sandbox. Como C# roda no Plugin Service, executar `Process.Start` é plausível, mas não verificado; o Node.js é processo normal. [F28 · inferido · 60]
- F29 Permissões: `permissions.json` tem `macOSPermissionsGranted: true`; config.json `permissionScreenStatus: permissionSuccess`. O detalhe de qual permissão (Acessibilidade, Monitoramento de Entrada) não está nesses arquivos. [F29 · lido · 85]
- F30 Aviso de plugin: `LoupedeckSettings.ini` diz para não editar com o Plugin Service rodando; e há `Applications/` + `Applications.Backups/` regenerados a cada início (backup.date 2026-11-07_00-55-22). [F30 · lido · 90]

##### Custo por caminho (estimativas, a conferir)
- Keystroke nativo: zero, só UI. Smart Action de Application: zero. Wrapper .app/Shortcuts + Application: baixo, fora do Options+. Plugin SDK C#/Node: alto (SDK, .NET, empacotar), só se precisar de lógica própria. [F31 · inferido · 60]

##### Não achado
- Arquivo de exportação de perfil completo; número oficial de páginas; ação "Run script" nativa; passo oficial "Add application" do ring; texto exato das permissões de Acessibilidade para ações de teclado.
