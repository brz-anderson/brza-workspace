---
status: open
description: Os PRs #40743, #40345, #39162 e as issues #40492, #40343, #39177 trazem listagem de agentes por workspace, foco de terminal por plugins e autocompletion.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#40743`](https://github.com/stablyai/orca/pull/40743) (resolve Issue [`#40742`](https://github.com/stablyai/orca/issues/40742)),
[`stablyai/orca#40345`](https://github.com/stablyai/orca/pull/40345) (resolve Issue [`#40343`](https://github.com/stablyai/orca/issues/40343)),
[`stablyai/orca#39162`](https://github.com/stablyai/orca/pull/39162) e das issues
[`stablyai/orca#40492`](https://github.com/stablyai/orca/issues/40492),
[`stablyai/orca#39177`](https://github.com/stablyai/orca/issues/39177),
[`stablyai/orca#39176`](https://github.com/stablyai/orca/issues/39176) e
[`stablyai/orca#39267`](https://github.com/stablyai/orca/issues/39267).

## O problema

1. **Ausência de pilha de navegação para trás e para frente no editor (`#39162`):**
   Ao saltar para definições de símbolos, abrir referências ou inspecionar arquivos alternados, os desenvolvedores não dispunham
   de histórico de navegação no editor (equivalente ao `Cmd+[` / `Cmd+]` ou botões de avançar/voltar do VS Code e IntelliJ).
   Se o arquivo de origem tivesse sido fechado pelo fluxo de trabalho ou o foco mudasse de arquivo, não era possível retornar
   diretamente à posição exata do cursor anterior.
2. **Colisão e ambiguidade de workspaces em chamadas de plugins (`#39177`):**
   A API de extensão exposta aos plugins resolvia o contexto do workspace (`workspace.readContext`) apenas por heurística
   baseada em `displayName` e `branch`. Em ambientes com múltiplos projetos abertos onde cada um possui seu workspace padrão
   chamado `primary` apontando para o branch `main`, a chamada retornava dados misturados ou do projeto errado, quebrando
   extensões de auditoria, linters customizados e automações de build.
3. **Falta de exposição do ID e path absoluto em eventos e leituras de workspace (`#40492`):**
   Plugins não conseguiam correlacionar de forma determinística o workspace focado porque `workspace.readContext` e o
   evento `workspace.changed` omitiam o identificador unívoco e o caminho absoluto do filesystem (`path`), forçando extensões
   a adivinhar a raiz do projeto ou executar buscas frágeis pelo sistema de arquivos.
4. **Falta de API programática para criação de workspaces a partir de receitas de ambiente (`#39176`):**
   Plugins que integram ferramentas de provisionamento (ex.: contêineres Devcontainer, Nix ou receitas corporativas) precisavam
   forçar o usuário a digitar comandos manuais no chat/composer para disparar a criação de um novo workspace com o template correto,
   em vez de invocar uma API tipada do Studio (`workspace.createFromRecipe`).
5. **Spawn indesejado de terminais/PTYs ao inspecionar workspaces em repouso (`#39267`):**
   Ao clicar em um workspace que estava em repouso (*sleeping workspace*) na barra lateral apenas para consultar um arquivo
   ou verificar o histórico de commits, o runtime acordava todo o ambiente alocando imediatamente uma nova sessão PTY e
   executando o shell padrão, consumindo recursos de CPU/memória e poluindo o painel de terminais sem necessidade.
6. **Incapacidade de plugins fornecerem sugestões de autocompletar inline (ghost text) no editor (`#40345`, resolve `#40343`):**
   O editor embutido Monaco suportava autocompletar e snippets via hooks tradicionais de linguagem, mas não expunha ponto
   de extensão para sugestões inline em texto cinza (*ghost text*) aceitas via `Tab` (estilo Copilot, Supermaven ou modelos locais).
   Plugins que quisessem oferecer completude assistida por IA precisavam substituir o editor inteiro por um webview customizado.
7. **Incapacidade de plugins inspecionarem agentes de outros workspaces e focarem terminais (`#40743`, resolve `#40742`):**
   A API de plugins (`agents.list`) retornava exclusivamente os agentes do workspace ativo no momento. Extensões e pontes
   externas (como Stream Deck, hubs de monitoramento ou scripts de orquestração) ficavam cegas em relação a agentes em execução
   em outros workspaces e não dispunham de método para focar diretamente a aba/painel do terminal de um agente alvo (`terminal.focus`).

## O que o upstream implementa

- **Listagem de agentes por workspace e foco de terminal via API de plugins (`#40743`):**
  - Atualiza a Host API de plugins para v1.7, adicionando `workspaceId?` opcional em `agents.list(params?: { workspaceId? })`;
  - Adiciona o método `terminal.focus({ terminalId })` sob a permissão `workspace:write`, trazendo a aba e o painel do terminal correspondente para o primeiro plano da janela ativa do desktop.
- **Hook de plugin `editor.inlineCompletion` para sugestões de ghost text (`#40345`):**
  - Introduz o hook de worker `editor.inlineCompletion` (schema since `1.4.256`), permitindo que plugins injetem o campo mutável `suggestion`;
  - Conecta um provedor nativo no Monaco (`monaco-inline-completion-provider.ts`) com debounce de digitação de 300ms, enviando contexto delimitado do cursor (até 32 KiB de prefixo e 8 KiB de sufixo) e exibindo a resposta diretamente como texto fantasma inline aceito com `Tab`.
- **Exposição de `id` e `path` absoluto do workspace para plugins (`#40492`):**
  - Estende o payload de `workspace.readContext` e os argumentos do evento `workspace.changed` com os campos `id` e `path` (caminho absoluto do workspace no disco);
  - Permite que linters, formatadores, observadores de arquivos e ferramentas externas operem com precisão sobre o diretório raiz do workspace ativo.
- **Comandos e atalhos de histórico de navegação no editor (`#39162`):**
  - Implementa as ações globais `editor.navigateBack` e `editor.navigateForward`, mapeadas para os atalhos universais:
    - macOS: `Cmd+[` (voltar) e `Cmd+]` (avançar), além de `Ctrl+-` / `Ctrl+Shift+-`;
    - Windows e Linux: `Alt+Left` (voltar) e `Alt+Right` (avançar);
  - Mantém uma pilha de posições recentes do cursor (arquivo, linha, coluna) com limite configurável por workspace;
  - Se um arquivo visitado anteriormente tiver sido fechado, o comando reabre a aba automaticamente mantendo o scroll e
    posicionamento do cursor;
  - Descarta entradas duplicadas consecutivas e ajusta as posições quando o buffer for editado.
- **Identificador inequívoco em `workspace.readContext` para plugins (`#39177`):**
  - Refatora a resolução de contexto na API de plugins para exigir e fornecer um ID interno único (`workspaceId`),
    eliminando colisões entre workspaces com nomes ou branches idênticos em diferentes projetos.
- **API `workspace.createFromRecipe` para extensões (`#39176`):**
  - Expõe método tipado no SDK de plugins para criar workspaces programaticamente vinculando ambiente, receita e worktree,
    permitindo que extensões criem ambientes com 1 clique a partir da barra lateral ou botões de ação.
- **Acordar silencioso (*quiet wake*) para workspaces em repouso (`#39267`):**
  - Modifica o ciclo de ativação de workspaces em repouso para que a inspeção passiva (abertura de arquivo, diff no Source Control,
    leitura de notas) restaure apenas o sistema de arquivos virtual sem instanciar processos PTY ou terminais automáticos até que
    o usuário interaja explicitamente com o console ou inicie uma ação de execução.

## O que fazer

- Adotar `agents.list({ workspaceId? })` e `terminal.focus({ terminalId })` na API de plugins (`#40743`) para controle externo de agentes.
- Adotar o hook `editor.inlineCompletion` para habilitar plugins de completude de código via IA em ghost text no Monaco (`#40345`).
- Expor `id` e `path` absoluto do workspace em `workspace.readContext` e no evento `workspace.changed` (`#40492`).
- Adotar o histórico de navegação (`editor.navigateBack` / `editor.navigateForward`) no editor do `brza-studio` (`#39162`).
- Incorporar o uso de `workspaceId` único nas APIs de plugins de workspace (`#39177`).
- Disponibilizar a API programática de criação de workspaces por receita (`#39176`).
- Implementar a ativação sob demanda de terminais para workspaces em repouso (`#39267`), poupando recursos no macOS.
