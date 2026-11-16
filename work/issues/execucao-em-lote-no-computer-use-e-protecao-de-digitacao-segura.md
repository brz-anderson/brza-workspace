---
priority: high
tags:
  - tooling
  - design
description: Os PRs #42859, #42861, #42855, #42842, #42863, #42826, #42816 e as issues #42850, #42849, #42848 trazem execução em lote com orca computer batch, recusa segura de input sobre digitação do usuário ou campos confidenciais, truncamento inteligente de snapshots e aceleração via eventos de acessibilidade.
---

# Execução em lote de ações no Computer Use, proteção de digitação segura e otimizações de acessibilidade

Rastreado dos PRs abertos no upstream [`stablyai/orca#42859`](https://github.com/stablyai/orca/pull/42859) (resolve Issue [`#42850`](https://github.com/stablyai/orca/issues/42850)),
[`stablyai/orca#42861`](https://github.com/stablyai/orca/pull/42861) (resolve Issue [`#42849`](https://github.com/stablyai/orca/issues/42849)),
[`stablyai/orca#42855`](https://github.com/stablyai/orca/pull/42855) (resolve Issue [`#42848`](https://github.com/stablyai/orca/issues/42848)),
[`stablyai/orca#42842`](https://github.com/stablyai/orca/pull/42842) (resolve Issue [`#42843`](https://github.com/stablyai/orca/issues/42843)),
[`stablyai/orca#42863`](https://github.com/stablyai/orca/pull/42863) (resolve Issue [`#42846`](https://github.com/stablyai/orca/issues/42846)),
[`stablyai/orca#42826`](https://github.com/stablyai/orca/pull/42826) (resolve Issue [`#42825`](https://github.com/stablyai/orca/issues/42825)),
[`stablyai/orca#42816`](https://github.com/stablyai/orca/pull/42816) (resolve Issue [`#42815`](https://github.com/stablyai/orca/issues/42815)),
[`stablyai/orca#42853`](https://github.com/stablyai/orca/pull/42853) (resolve Issue [`#42841`](https://github.com/stablyai/orca/issues/42841)) e
[`stablyai/orca#42814`](https://github.com/stablyai/orca/pull/42814) (resolve Issue [`#42813`](https://github.com/stablyai/orca/issues/42813)).

## O problema

1. **Alto custo em turnos e latência ao encadear ações sequenciais de GUI (`#42859`, resolve `#42850`):**
   Agentes operando interfaces gráficas precisavam disparar comandos CLI separados para cada tecla ou clique (ex.: digitar atalhos ou sequências de campos). Cada passo custava uma rodada completa de modelo, uma invocação de processo e uma leitura integral da árvore visual, multiplicando a latência e o consumo de tokens.
2. **Risco de injeção acidental de inputs sobre digitação humana ou campos de senha (`#42861`, resolve `#42849`):**
   Ao despachar eventos de teclado sintéticos no macOS via Computer Use, se o usuário estivesse digitando simultaneamente no mesmo aplicativo ou se o foco saltasse para um campo de senha/seguro (`NSSecureTextField`), as teclas do agente colidiam com as do operador ou expunham dados em interfaces desprotegidas.
3. **Explosão de contexto com listas longas e textos extensos em árvores de acessibilidade (`#42855`, resolve `#42848`):**
   Snapshots de janelas contendo tabelas ou editores de texto com milhares de linhas serializavam a íntegra dos nós na árvore visual do agente, estourando limites de tokens mesmo para elementos fora da tela (*off-screen*).
4. **Capturas de tela automáticas e desnecessárias a cada micro-ação (`#42842`, resolve `#42843`):**
   Ações primitivas como cliques e pressionamento de teclas geravam capturas de tela implícitas por padrão, aumentando drasticamente a carga de I/O e o tamanho dos pacotes JSON transmitidos ao agente.
5. **Latência de polling fixo de 200ms na estabilização de ações e espera por elementos (`#42863`, `#42826`, resolve `#42846`, `#42825`):**
   A confirmação de que uma ação de GUI terminou ou a espera de que um botão surgisse na tela (`orca computer wait`) realizavam laços de polling ativo a cada 200ms via CLI, sobrecarregando a CPU e impondo atrasos desnecessários em transições rápidas.
6. **Leituras repetitivas de atributos de acessibilidade por elemento (`#42816`, resolve `#42815`):**
   A inspeção da árvore no macOS chamava a API `AXUIElementCopyAttributeValue` dezenas de vezes para cada elemento isolado, tornando a captura de árvores complexas excessivamente lenta.

## O que o upstream implementa

- **Execução em lote atômica com `orca computer batch` (`#42859`, resolve `#42850`):**
  - Adiciona o subcomando `orca computer batch --app <id> --window-id <id> --steps '[{...}]'`:
    - Aceita até 50 passos pré-validados (`click`, `press-key`, `hotkey`, `type-text`, `set-value`, etc.);
    - Executa os passos sequencialmente no runtime em memória sem re-instanciar a CLI nem ler a árvore entre eles;
    - Preserva o baseline de diff visual (`keepTreeBaseline`), retornando ao final apenas o resumo de execução dos passos e o diff de estado entre o início e o fim do lote;
    - Interrompe a execução com código de erro limpo caso um passo falhe ou retorne não-verificado (`--stop-on`).
- **Guarda de foco e recusa de input sobre campos seguros ou digitação do usuário (`#42861`, resolve `#42849`):**
  - Monitora eventos de digitação física do operador no macOS e recusa a injeção de teclas automatizadas se o usuário estiver digitando ativamente no mesmo contexto;
  - Bloqueia a digitação automatizada se o elemento focado possuir o atributo de acessibilidade de campo seguro (`AXSubrole: AXSecureTextField`), protegendo senhas e segredos.
- **Filtragem de nós fora da tela em snapshots (`#42855`, resolve `#42848`):**
  - Trunca listas e blocos de texto no macOS para incluir apenas os elementos e intervalos de caracteres visíveis no viewport da janela, reduzindo o tamanho do snapshot em até 70%.
- **Omissão de screenshots por padrão em ações de GUI (`#42842`, resolve `#42843`):**
  - Desativa a captura de imagem pós-ação, exigindo a passagem explícita da flag `--screenshot` apenas quando o agente realmente necessitar da comprovação visual.
- **Sincronização reativa de ações via notificações de acessibilidade (`#42863`, `#42826`, resolve `#42846`, `#42825`):**
  - Substitui o polling arbitrário de 200ms por subscrição direta a notificações do subsistema de acessibilidade do macOS (`AXUIElementRegisterForNotification`), resolvendo `orca computer wait` e a estabilização de cliques no instante exato da mutação visual.
- **Extração consolidada de atributos AX em chamada única (`#42816`, resolve `#42815`):**
  - Utiliza `AXUIElementCopyMultipleAttributeValues` para extrair todos os atributos de interesse de um elemento de uma só vez, acelerando a montagem do snapshot da janela em até 3x.
- **Guia enxuto de Computer Use orientado a baixo custo (`#42853`, `#42814`, resolve `#42841`, `#42813`):**
  - Orienta os modelos de IA a preferirem encadeamento de lotes (`batch`), dispensarem screenshots e consultarem apenas as notas da plataforma atual.

## O que fazer

- Implementar o comando `brza computer batch` para execução atômica de múltiplos passos de GUI em uma única chamada (`#42859`, resolve `#42850`).
- Adotar a proteção contra injeção de input em campos de senha ou em conflito com digitação do operador (`#42861`, resolve `#42849`).
- Omitir capturas de tela desnecessárias em ações primitivas salvo com flag explícita `--screenshot` (`#42842`, resolve `#42843`).
- Aplicar truncamento de nós fora da tela em listas e textos longos de snapshots (`#42855`, resolve `#42848`).
- Adotar estabilização reativa de ações e esperas por eventos de acessibilidade (`#42863`, `#42826`).
- Unificar a leitura de atributos de acessibilidade via `AXUIElementCopyMultipleAttributeValues` (`#42816`).
