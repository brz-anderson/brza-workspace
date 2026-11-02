---
scope:
  - workspace
---

# O brza devices, que lista, cria e abre os simuladores e os emuladores

Pedido de Anderson nesta sessão, em 2026-11-02: "precisamos criar um comando na `BrzA CLI` que cria/abre `Android
Emulators` e `iOS Simulators` quando disponível". O pedido veio depois de dois outros:
- "mostre os prints tirados aqui no chat";
- a pergunta de como abrir o simulador pelo Xcode, quando o Device Hub listava só o iPhone Duo.

## O que se leu antes

- **Bloqueios em vigor:** nenhum, em nenhum workstream.
- **O ferramental mudou desde 2026-10-31.** O PLN-006, do workstream `workspace`, levou os comandos genéricos para o
  `~/Projects/brza-workflow`, e o `brza-print` foi para o `packages/client/bin`. O `brza-shot` ficou no
  `scripts/brza/` daqui. O PLN-006 segue `in_progress`, e o `Retomar` dele diz "Falta o P9: o README do
  `brza-workflow` e a revisão da migração".
- **iOS:** o Xcode 27.1 só trazia o runtime iOS 27.1, que aceita um modelo só, o iPhone Duo
  (`xcrun simctl list -j runtimes`, `supportedDeviceTypes`). Por isso o Device Hub mostrava só esse modelo. No meio da
  sessão, o iOS 27.0 apareceu instalado, com 62 modelos, e os simuladores dele voltaram.
- **Android:** o SDK fica em `~/Library/Android/sdk`, fora do PATH. Há um AVD, o `Pixel_9_Pro_XL`, e a imagem
  `system-images;android-36.1;google_apis_playstore;arm64-v8a`. O `avdmanager` não roda com o Java do sistema, porque o
  `/usr/bin/java` é o plugin antigo, que dá "Bad CPU type". Ele roda com o Java do Android Studio, em
  `/Applications/Android Studio.app/Contents/jbr/Contents/Home`.

## O que Anderson respondeu

- **Onde:** "brza-workflow, pacote client (Recomendado)".
- **Forma:** "brza device list | open (Recomendado)". Depois, no meio do trabalho: "`brza devices` deve ser
  independente, tanto de `brza print` quanto `brza shot` ou qualquer outro comando `brza <command>`". O nome ficou
  `brza devices`, sem importar nada dos outros comandos.
- **Download:** "Baixa com --download".
- **Espera:** "Sai logo, com --wait opcional".

## O que se fez

- **`f690ee5` no `brza-workflow`:** `feat(client): brza devices lista, cria e abre os simuladores iOS e os emuladores
  Android`.
  - **`packages/client/bin/brza-devices`**, só com a biblioteca padrão e sem importar outro comando do `brza`.
    - O `list` mostra os simuladores dos runtimes disponíveis e os AVDs, com ● para o ligado. Mostra também os modelos
      que dá para criar em cada runtime e a imagem que um AVD novo usaria. O `--profiles` acrescenta os perfis do
      `avdmanager`, e há o `--json`.
    - O `open [NOME]` compara o nome sem caixa, com espaço e `_` valendo o mesmo. A ordem da busca:
      1. o simulador ou o AVD que já existe;
      2. o modelo iOS, que ele cria no runtime mais novo que o aceita;
      3. o perfil Android, que ele cria com a imagem instalada mais nova, do Google Play e na arquitetura da máquina.
    - O emulador sobe solto do terminal, numa porta livre de 5554 a 5584, com o log no temporário.
    - O `--wait` espera pelo `simctl bootstatus` ou pelo `sys.boot_completed` do adb.
    - O `--download` roda o `xcodebuild -downloadPlatform iOS [-buildVersion]`, com a versão pelo `--runtime`, ou o
      `sdkmanager` com a imagem do `--image` ou a mais nova do Google Play.
    - O `avdmanager` e o `sdkmanager` rodam com o Java do Android Studio quando falta o `JAVA_HOME`.
  - **`tests/cli/test_brza_devices.py`**, com 20 casos, com as ferramentas trocadas por falsas e o SDK e os AVDs num
    diretório temporário.
  - O `README.md` e a ajuda do `brza install --client` passaram a citar o `brza-devices`. O `git pull --rebase` não
    deu conflito com o P9 do PLN-006.
- **Os testes:**
  - a `tests/hooks` deu `Ran 283 tests … OK`;
  - a `tests/cli` deu `Ran 433 tests … OK` num ambiente limpo, com `env -i`;
  - no chat, ela falhou fora do comando novo. O `test_brza_sessions.py` falha pelo ambiente do chat. Numa das rodadas,
    houve ainda 15 erros do `test_brza_note_index.py`, porque a sessão do PLN-006 commitava o `a313ec5` no mesmo
    checkout enquanto a suíte rodava. O achado foi para a issue
    [Os testes do brza-workflow falham quando rodam dentro do chat do BrzA Studio](../issues/testes-do-brza-workflow-falham-dentro-do-chat-do-app.md).
- **O `brza install --client`** ligou o `brza-devices`, e o `brza devices --help` respondeu pelo CLI.

## A conferência, nos aparelhos de verdade

- **`brza devices`**, sem subcomando: listou 12 simuladores e o Pixel 9 Pro XL, com os modelos para criar no iOS 27.0.
- **`open "iphone 17" --wait`:** `iPhone 17: ligado, pronto`, em 39 s.
- **`open pixel_9_pro_xl --wait`:** `Pixel 9 Pro XL: ligado, pronto (android-36.1, emulator-5554)`, em 2 min 25 s. O
  segundo `open "Pixel 9 Pro XL"` respondeu "já estava ligado" e não subiu outro emulador.
- **`open "iPhone 16e"`:** criado no iOS 27.0 e ligado. Ele foi apagado depois, pelo `simctl delete`.
- **`open "Pixel 10 Pro" --android`:** o AVD `Pixel_10_Pro` foi criado com o perfil `pixel_10_pro` e a imagem do
  Google Play, e ligou em `emulator-5556`. Foi desligado e apagado depois, pelo `avdmanager delete avd`.
- **Os erros:** o nome desconhecido, o `open` sem nome com mais de um aparelho e o `--runtime` sem `--download`
  pararam com a mensagem certa.
- **O `brza print`** tirou os prints do iPhone 17 (1206×2622 px) e do Pixel 9 Pro XL (1344×2992 px), mostrados no
  chat. O do Pixel pegou o aviso "Pixel Launcher isn't responding": o `sys.boot_completed` já era 1, mas o launcher
  ainda não respondia.

## O que ficou aberto

- **O `--download` não rodou de verdade**, porque cada runtime ou imagem tem vários GB. Os testes conferem os comandos
  com as ferramentas falsas.
- **O `--wait` do Android termina no `sys.boot_completed`**, antes de o launcher responder. Esperar também a tela
  inicial fica para quando o print cedo demais atrapalhar uma conferência.
- **A norma não cita o `brza devices`.** O passo dos casos manuais, no `plan-template.md` do `core/`, poderia dizer
  para ligar o aparelho com ele antes do `brza print`. Isso não foi pedido e fica para uma rodada.
- **Os testes no chat:** a issue acima.

## Fora do workspace

- **O link `~/.local/bin/brza-devices`**, pelo `brza install --client`.
  - **Risco:** nenhum além do comando no PATH.
  - **Estado:** ativo.
  - **Como desfazer:** `rm ~/.local/bin/brza-devices`.
- **O iPhone 17, no iOS 27.0, e o Pixel 9 Pro XL, em `emulator-5554`**, ligados pelo `brza devices open`.
  - **Risco:** memória e CPU enquanto ficam ligados.
  - **Estado:** desligados, fora desta sessão; às 15h o `simctl` não tinha nenhum ligado, e o `adb devices` estava
    vazio.
  - **Como desfazer:** nada a desfazer.
- **O simulador iPhone 16e e o AVD `Pixel_10_Pro`**, criados na conferência.
  - **Risco:** nenhum.
  - **Estado:** apagados.
  - **Como desfazer:** nada a desfazer.
