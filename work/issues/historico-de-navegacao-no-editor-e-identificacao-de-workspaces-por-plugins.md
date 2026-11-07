---
status: open
description: O PR #39162 e as issues #39177, #39176 e #39267 trazem navegação de histórico no editor, identificadores inequívocos de workspaces para plugins e acordar silencioso de workspaces.
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

Rastreado do PR aberto no upstream [`stablyai/orca#39162`](https://github.com/stablyai/orca/pull/39162) e das issues
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
3. **Falta de API programática para criação de workspaces a partir de receitas de ambiente (`#39176`):**
   Plugins que integram ferramentas de provisionamento (ex.: contêineres Devcontainer, Nix ou receitas corporativas) precisavam
   forçar o usuário a digitar comandos manuais no chat/composer para disparar a criação de um novo workspace com o template correto,
   em vez de invocar uma API tipada do Studio (`workspace.createFromRecipe`).
4. **Spawn indesejado de terminais/PTYs ao inspecionar workspaces em repouso (`#39267`):**
   Ao clicar em um workspace que estava em repouso (*sleeping workspace*) na barra lateral apenas para consultar um arquivo
   ou verificar o histórico de commits, o runtime acordava todo o ambiente alocando imediatamente uma nova sessão PTY e
   executando o shell padrão, consumindo recursos de CPU/memória e poluindo o painel de terminais sem necessidade.

## O que o upstream implementa

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

- Adotar o histórico de navegação (`editor.navigateBack` / `editor.navigateForward`) no editor do `brza-studio` (`#39162`).
- Incorporar o uso de `workspaceId` único nas APIs de plugins de workspace (`#39177`).
- Disponibilizar a API programática de criação de workspaces por receita (`#39176`).
- Implementar a ativação sob demanda de terminais para workspaces em repouso (`#39267`), poupando recursos no macOS.
