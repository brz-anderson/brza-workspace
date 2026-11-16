---
status: open
description: Os PRs #43253, #43181, #43132, #41132, #43111, #43094, #43144, #43137, #41786 trazem terminador de linha do host (CRLF/LF), expurgo de abas fechadas em partições, navegação por Cmd/Ctrl+Click e indicadores Git.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-07
tags:
  - tooling
  - design
---

# Histórico de navegação no editor e identificação de workspaces por plugins

Rastreado dos PRs abertos no upstream [`stablyai/orca#43253`](https://github.com/stablyai/orca/pull/43253) (resolve Issue [`#43216`](https://github.com/stablyai/orca/issues/43216)),
[`stablyai/orca#43181`](https://github.com/stablyai/orca/pull/43181),
[`stablyai/orca#43132`](https://github.com/stablyai/orca/pull/43132) (resolve Issue [`#43130`](https://github.com/stablyai/orca/issues/43130)),
[`stablyai/orca#41132`](https://github.com/stablyai/orca/pull/41132),
[`stablyai/orca#43111`](https://github.com/stablyai/orca/pull/43111) e
[`stablyai/orca#43103`](https://github.com/stablyai/orca/pull/43103) (ambos atendem Issue [`#43100`](https://github.com/stablyai/orca/issues/43100)),
[`stablyai/orca#43094`](https://github.com/stablyai/orca/pull/43094),
[`stablyai/orca#43144`](https://github.com/stablyai/orca/pull/43144) (resolve Issue [`#43143`](https://github.com/stablyai/orca/issues/43143)),
[`stablyai/orca#43137`](https://github.com/stablyai/orca/pull/43137) (resolve Issue [`#43136`](https://github.com/stablyai/orca/issues/43136)),
[`stablyai/orca#41786`](https://github.com/stablyai/orca/pull/41786) (resolve Issue [`#41783`](https://github.com/stablyai/orca/issues/41783)),
[`stablyai/orca#41828`](https://github.com/stablyai/orca/pull/41828) (resolve Issue [`#41827`](https://github.com/stablyai/orca/issues/41827)),
[`stablyai/orca#41768`](https://github.com/stablyai/orca/pull/41768),
[`stablyai/orca#41767`](https://github.com/stablyai/orca/pull/41767),
[`stablyai/orca#40743`](https://github.com/stablyai/orca/pull/40743) (resolve Issue [`#40742`](https://github.com/stablyai/orca/issues/40742)),
[`stablyai/orca#40345`](https://github.com/stablyai/orca/pull/40345) (resolve Issue [`#40343`](https://github.com/stablyai/orca/issues/40343)),
[`stablyai/orca#39162`](https://github.com/stablyai/orca/pull/39162) e das issues
[`stablyai/orca#40492`](https://github.com/stablyai/orca/issues/40492),
[`stablyai/orca#39177`](https://github.com/stablyai/orca/issues/39177),
[`stablyai/orca#39176`](https://github.com/stablyai/orca/issues/39176) e
[`stablyai/orca#39267`](https://github.com/stablyai/orca/issues/39267).

## O problema

1. **Ausência de navegação direta por clique em caminhos de importação (`#43132`, resolve `#43130`):**
   Ao ler arquivos de código com declarações de importação (`import { x } from './path'`), o desenvolvedor precisava procurar o arquivo manualmente na árvore lateral ou pelo Quick Open, pois clicar no caminho do módulo não abria o arquivo de destino.
2. **Falta de indicadores de modificação Git no gutter do editor (`#41132`):**
   Ao editar código, a margem esquerda (gutter) do Monaco não exibia barras coloridas indicando linhas inseridas, alteradas ou excluídas em relação ao último commit Git, dificultando a revisão pontual antes do commit.
3. **Divergência de coloração sintática de palavras-chave de controle em relação ao VS Code (`#43111`, `#43103`, resolve `#43100`):**
   Palavras-chave de controle de fluxo (`return`, `if`, `else`, `try`, `catch`, `async`, `await`) recebiam o mesmo tom genérico de identificadores no editor, perdendo a hierarquia visual familiar dos temas modernos.
4. **Ausência de contagem de palavras para documentos e seleções (`#43094`):**
   Ao revisar documentações, prompts de agentes e artigos em Markdown, não havia indicador de total de palavras do documento ou do trecho selecionado na barra de status.
5. **Perda de scroll e zoom em custom editors de plugins ao trocar de aba (`#43144`, resolve `#43143`):**
   Editores customizados providos por plugins (ex.: visualizadores de diagramas, tabelas ou canvas) perdiam a posição de rolagem e nível de zoom toda vez que o desenvolvedor alternava para outra aba e voltava.
6. **Incapacidade de plugins elevarem a janela do aplicativo (`#43137`, resolve `#43136`):**
   Quando uma extensão executava `workspace.open` ou `terminal.focus`, a janela do Studio não vinha para o primeiro plano no sistema operacional caso estivesse oculta ou em segundo plano.
7. **Ausência de pilha de navegação para trás e para frente no editor (`#39162`):**
   Ao saltar para definições de símbolos, abrir referências ou inspecionar arquivos alternados, os desenvolvedores não dispunham de histórico de navegação no editor (`Cmd+[` / `Cmd+]` ou botões de voltar/avançar).
8. **Colisão e ambiguidade de workspaces em chamadas de plugins (`#39177`):**
   A API de extensão exposta aos plugins resolvia o contexto do workspace (`workspace.readContext`) apenas por heurística baseada em `displayName` e `branch`, causando colisões entre projetos distintos com nomes padrão iguais (`main`, `primary`).
9. **Falta de exposição do ID e path absoluto em eventos de workspace (`#40492`):**
   Plugins não conseguiam correlacionar de forma determinística o workspace focado porque faltavam identificadores inequívocos e caminhos absolutos.
10. **Desorganização da barra de abas e ordenação de arquivos no Quick Open (`#41768`, `#41828`):**
    Falta de ordenação por uso mais recente (MRU) e falhas de normalização Unicode NFC em buscas com acentos.

## O que o upstream implementa

- **Abertura de arquivo importado via Cmd/Ctrl+Click no caminho do import (`#43132`, resolve `#43130`):**
  - Conecta um provedor de links de definição no Monaco que reconhece caminhos de importação relativos e absolutos, abrindo a aba do arquivo correspondente diretamente sob clique com tecla modificadora (<kbd>⌘Click</kbd> / <kbd>Ctrl+Click</kbd>).
- **Indicadores de alteração Git no gutter do editor (`#41132`):**
  - Renderiza barras visuais sutis na calha do editor (verde para linhas adicionadas, azul para linhas modificadas e triângulo vermelho para linhas excluídas) sincronizadas com o diff Git do arquivo ativo.
- **Coloração sintática precisa para palavras-chave de controle estilo VS Code (`#43111`, `#43103`, resolve `#43100`):**
  - Mapeia escopos TextMate e regras de tokenização no Monaco para destacar palavras de controle em JS, TS e linguagens comuns com o matiz correto dos temas escuro e claro.
- **Contador de palavras para documento e seleção na status bar (`#43094`):**
  - Adiciona leitor de contagem de palavras em tempo real na barra inferior do editor, exibindo o total do documento ou o número de palavras da seleção ativa.
- **Preservação de estado em custom editors de plugins (`#43144`, resolve `#43143`):**
  - Mantém em cache o estado visual (scroll, posição do viewport e zoom) de visualizadores customizados de extensões durante a troca de abas.
- **Método `raiseWindow` na API de plugins (`#43137`, resolve `#43136`):**
  - Expõe a opção `raiseWindow: true` em `terminal.focus` e `workspace.open`, trazendo a janela ativa do app para o topo na área de trabalho.
- **Terminador de linha nativo do host e configuração End of Line (`#43253`, resolve `#43216`):**
  - Novos arquivos criados no editor passam a utilizar o terminador de linha nativo do host onde o workspace reside (CRLF no Windows, LF no macOS e Linux/WSL), com introdução da configuração `files.eol` em *Settings › Editor*.
- **Expurgo de linhas de arquivos fechados em partições de múltiplos hosts (`#43181`):**
  - Ao fechar um arquivo, remove imediatamente seus registros de arquivos abertos de todas as partições de hosts, evitando vazamentos de estado e buffers fantasmas no editor.
- **Histórico de navegação no editor (`#39162`):**
  - Implementa `editor.navigateBack` (<kbd>⌘[</kbd> / <kbd>Alt+Left</kbd>) e `editor.navigateForward` (<kbd>⌘]</kbd> / <kbd>Alt+Right</kbd>) mantendo pilha de posições do cursor.
- **Hook `editor.inlineCompletion` para sugestões de ghost text (`#40345`):**
  - Provedor nativo no Monaco para aceitar sugestões inline em texto cinza via <kbd>Tab</kbd>.
- **Ordenação de abas MRU e normalização Unicode NFC (`#41768`, `#41828`):**
  - Suporte a abas organizadas por mais recentemente usadas e busca normalizada NFC no Quick Open.

## O que fazer no BrzA Studio

- Adotar a navegação por <kbd>⌘Click</kbd> / <kbd>Ctrl+Click</kbd> em caminhos de importação no editor (`#43132`, resolve `#43130`).
- Incorporar os indicadores visuais de alteração Git no gutter do Monaco (`#41132`).
- Aplicar o realce sintático de palavras-chave de controle idêntico ao VS Code (`#43111`, `#43103`).
- Adicionar o contador de palavras para documentos e seleções no rodapé do editor (`#43094`).
- Adotar o terminador de linha do host para novos arquivos com suporte a `files.eol` (`#43253`, resolve `#43216`).
- Expurgo atômico de registros de arquivos fechados nas partições de host do editor (`#43181`).
- Preservar viewport e scroll de custom editors de plugins na alternância de abas (`#43144`).
- Suportar `raiseWindow` nas chamadas de plugins para focar a janela do app (`#43137`).
- Integrar os atalhos de histórico de navegação (`editor.navigateBack` / `editor.navigateForward`) no Studio (`#39162`).
