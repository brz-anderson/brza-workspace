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

## O emulador do Pixel, ajustado

Pedido de Anderson: "tente otimizar o emulador do Android, equilibrando as configs de uso da maquina da imagem,
extraindo o máximo de recurso para que o emulador rode \"liso\"".

- **A máquina:** Apple M5 Pro, com 15 núcleos (5 de desempenho e 10 de eficiência), 24 GB de RAM e GPU de 16 núcleos
  com Metal 4. O emulador é a versão 36.6.11.0, com o Hypervisor.Framework.
- **A causa:** o log da subida de 13:49 dizia "Software GL rendering will be used due to system memory pressure
  (Available Memory: 4421 MB, Required: 5120 MB)". Com o `hw.gpu.mode=auto`, o emulador caiu no `lavapipe` e no
  `swangle`, que renderizam na CPU, e o launcher travou ("Pixel Launcher isn't responding").
- **O ajuste**, no `~/.android/avd/Pixel_9_Pro_XL.avd/config.ini`:
  - `hw.gpu.mode`: de `auto` para `host`;
  - `hw.ramSize`: de `2048` para `4096`, o que o emulador já tinha escolhido sozinho;
  - `hw.cpu.ncore`: de `4` para `6`.
- **A medida**, com boot a frio pelo `-no-snapshot-load`:
  - o boot saiu em 18 s, contra 2 min 25 s antes;
  - o log passou a dizer `vulkan_mode_selected:host gles_mode_selected:host`, com o dispositivo Vulkan Apple M5 Pro;
  - o Android vê 6 núcleos (`nproc`) e 4 GB (`MemTotal: 4010096 kB`);
  - em 12 gestos de abrir e fechar a gaveta de apps, o `dumpsys gfxinfo` do launcher deu 264 quadros, 19,32% lentos,
    mediana de 17 ms, 90º percentil de 31 ms, 99º de 150 ms, e mediana de GPU de 14 ms.
- **Os quadros de antes não foram medidos**: a comparação é o boot e a impressão de Anderson, "já está bem melhor".
- **O que ainda pesa** é a GPU, numa tela de 1344×2992 a 480 dpi.

### A resolução, medida nas duas opções

A rodada sobre baixar a resolução teve duas perguntas:
- **AVD novo:** "Sim, nasce ajustado (Recomendado)";
- **Resolução:** em texto livre, "meça agora a diferença de desempenho das duas opções e tire um print cada opção pra
  mim comparar".

As duas opções foram medidas nas mesmas condições: boot a frio pelo `-no-snapshot-load`, 60 s de espera e rodadas de
12 gestos de abrir e fechar a gaveta de apps, com o `dumpsys gfxinfo` do launcher. A primeira rodada depois do boot sai
ruidosa nas duas, e não conta.

| Opção | Tela | Quadros lentos, depois de assentar | Mediana | 99º percentil | GPU, mediana |
| :-- | :-- | :-- | :-- | :-- | :-- |
| A | 1344×2992 a 480 dpi, com a moldura do Pixel | 6,81% e 5,52% | 16 ms | 32 ms | 12–13 ms |
| B | 1080×2400 a 420 dpi, sem a moldura | de 30,94% a 46,34% | 23–28 ms | 81–101 ms | 12–13 ms |

- **A B ficou pior**, com o mesmo tempo de GPU: os pixels não eram o gargalo. A causa da diferença não foi isolada.
- **A primeira tentativa da B não valeu:** só o `hw.lcd.*` foi trocado, e a moldura `pixel_9_pro_xl` manteve a tela em
  1344×2992, mudando só a densidade. A B medida foi com o `skin.name=1080x2400` e o `showDeviceFrame=no`.
- **O AVD voltou à A**, com o ajuste da GPU, da RAM e dos núcleos, e segue ligado em `emulator-5554`.
- **Os prints das duas opções** foram mostrados lado a lado no chat.

### O AVD novo nasce ajustado

- **`adf9229` no `brza-workflow`:** `feat(client): o AVD que o brza devices cria nasce na GPU do Mac`.
  - Depois do `avdmanager create`, o `config.ini` ganha `hw.gpu.mode=host`, metade da RAM da máquina até 4 GB e os
    núcleos de desempenho mais um, lidos do `sysctl`.
  - Sem o `sysctl`, valem 2 GB e metade dos núcleos.
  - O `test_brza_devices.py` foi a 23 casos, e a `tests/cli` limpa deu `OK`.
- **A conferência:** o `brza devices open "Pixel 10 Pro" --android --wait` criou o AVD com `hw.gpu.mode=host`,
  `hw.ramSize=4096` e `hw.cpu.ncore=6`. Ele subiu em `vulkan_mode_selected:host gles_mode_selected:host`, com o Pixel
  9 Pro XL ligado ao lado, e foi apagado depois.

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
- **O `config.ini` do AVD `Pixel_9_Pro_XL`**, com `hw.gpu.mode=host`, `hw.ramSize=4096` e `hw.cpu.ncore=6`.
  - **Risco:** o emulador usa até 4 GB de RAM e 6 núcleos enquanto está ligado.
  - **Estado:** ativo; o emulador segue ligado em `emulator-5554`. Na medida, o `config.ini` passou pela opção B
    (1080×2400, sem a moldura) e voltou à A, com o `diff` contra o backup mostrando só as três chaves do ajuste.
  - **Como desfazer:** `cp ~/.android/avd/Pixel_9_Pro_XL.avd/config.ini.brza-backup-2026-11-02
    ~/.android/avd/Pixel_9_Pro_XL.avd/config.ini`, com o emulador desligado.
