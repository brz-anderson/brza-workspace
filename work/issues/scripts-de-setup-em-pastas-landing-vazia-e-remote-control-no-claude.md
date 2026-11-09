---
status: open
description: Os PRs #40034, #40024, #40020, #40017, #39992 e #39958 trazem setup para folder projects, landing vazia, Remote Control e resiliência no Claude.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-09
tags:
  - tooling
  - chat
  - infra
---

# Scripts de setup em pastas, landing vazia e Remote Control no Claude

Rastreado dos PRs abertos no upstream [`stablyai/orca#40034`](https://github.com/stablyai/orca/pull/40034),
[`stablyai/orca#40024`](https://github.com/stablyai/orca/pull/40024) (resolve Issue [`#39267`](https://github.com/stablyai/orca/issues/39267)),
[`stablyai/orca#40020`](https://github.com/stablyai/orca/pull/40020) (resolve Issue [`#37502`](https://github.com/stablyai/orca/issues/37502)),
[`stablyai/orca#40017`](https://github.com/stablyai/orca/pull/40017) (resolve Issue [`#39942`](https://github.com/stablyai/orca/issues/39942)),
[`stablyai/orca#39992`](https://github.com/stablyai/orca/pull/39992) e
[`stablyai/orca#39958`](https://github.com/stablyai/orca/pull/39958).

## O problema

1. **Incapacidade de rodar scripts de setup e archive em pastas de projeto (`#40034`):**
   Projetos baseados em pastas simples (*folder projects* sem `.git` próprio na raiz, como coleções de multirrepositórios)
   não executavam os scripts configurados de `setup` e `archive`. Isso impedia a automação de criação e amarração de
   worktrees filhos em sub-repositórios ao abrir novos workspaces de projeto.
2. **Abertura compulsória de terminais ao selecionar workspaces sem abas (`#40024`, resolve `#39267`):**
   Ao clicar em um workspace sem abas ativas ou em repouso na barra lateral, o Orca abria imediatamente um novo terminal
   PTY ou agente padrão. Em workspaces adormecidos ou multirrepositórios, isso gerava processos desnecessários de shell e
   consumo de memória antes que o desenvolvedor escolhesse o que fazer.
3. **Desconexão do Remote Control ao iniciar conversas no Native Chat (`#40020`, resolve `#37502`):**
   Usuários com a configuração `remoteControlAtStartup: true` no Claude Code tinham suas sessões conectadas ao Remote Control
   apenas quando abertas em terminais manuais. Sessões criadas pelo Native Chat UI ficavam isoladas localmente e não apareciam
   no app mobile do Claude nem na interface web do `claude.ai/code`.
4. **Fechamento prematuro de terminal ao transicionar para Chat UI sem transcript (`#40017`, resolve `#39942`):**
   Ao clicar em "Continue in Chat UI" em um terminal recém-aberto cujo Claude CLI ainda não havia salvo o primeiro
   arquivo de transcript no disco (antes da primeira resposta), a interface fechava o terminal imediatamente. A tentativa
   posterior de abrir o chat falhava com `transcriptNotFound`, travando a aba e deixando o usuário sem terminal e sem chat.
5. **Dificuldade de manter foco e acesso à janela flutuante (*floating pop-out*) (`#39992`):**
   Janelas destacadas de chat ou terminal perdiam visibilidade quando outras aplicações em tela cheia eram ativadas,
   exigindo redocking ou navegação por alternador de janelas do sistema operacional.
6. **Perda de associação de tarefas em background de subagentes após reinício (`#39958`):**
   Ao reiniciar o aplicativo, tarefas executadas em segundo plano pelo Claude Code perdiam a referência ao subagente
   criador, dificultando a reconciliação e o acompanhamento de processos assíncronos.

## O que o upstream implementa e corrige

- **Execução de scripts de setup e archive em folder projects (`#40034`):**
  - Introduz a host capability `worktree.folder-setup.v1`;
  - Permite declarar comandos `setup` e `archive` nas configurações do projeto ou em manifesto;
  - Gera os executores em `<folder>/.orca/setup-runner-<workspace>-<launch>.sh|cmd` com permissão de execução e variáveis de ambiente injetadas (`ORCA_ROOT_PATH`, `ORCA_WORKSPACE_NAME`);
  - Viabiliza scripts automatizados para criar worktrees filhos nos sub-repositórios via `orca worktree create --repo "path:$ORCA_ROOT_PATH/$r" --name "$ORCA_WORKSPACE_NAME"`;
  - Limpa com segurança os scripts auxiliares após o encerramento da execução.
- **Opção de superfície vazia (landing) para workspaces sem abas (`#40024`):**
  - Adiciona a preferência `Settings → Terminal → When a workspace has no tabs`: `Open a terminal or default agent` (padrão) vs `Show empty workspace`;
  - Quando configurado para `Show empty workspace`, renderiza o componente `SplitPaneLanding` com ações explícitas: New Agent, New Terminal, New Browser Tab e New Markdown, evitando o spawn indesejado de PTYs.
- **Conexão automática do Native Chat ao Remote Control do Claude (`#40020`):**
  - Durante o `startup.open()` de sessões de Native Chat, verifica se `remoteControlAtStartup` está ativo na configuração do Claude Code;
  - Dispara `Query.enableRemoteControl(true)`, exibindo a sessão como online e compartilhada no mobile e web com o indicador verde correspondente.
- **Guarda contra fechamento de terminal sem transcript salvo (`#40017`):**
  - Implementa verificação prévia em `agentSession.createSupport` antes de fechar a aba de terminal na transição "Continue in Chat UI";
  - Se o transcript ainda não foi materializado em disco, cancela a operação ou aguarda a sincronização do Claude CLI, prevenindo o erro `transcriptNotFound` e perda de contexto.
- **Fixação Always on Top e atalho global para janelas flutuantes (`#39992`):**
  - Adiciona suporte a fixação sobre todas as janelas do sistema operacional e atalho configurável para evocar o pop-out a partir de qualquer aplicativo.
- **Preservação de tarefas vinculadas a subagentes após restart (`#39958`):**
  - Persiste os metadados de subagente pai em tarefas ativas de background do Claude, reconectando-as aos canais corretos de streaming após reinicialização do app.

## O que fazer no BrzA Studio

1. Adotar o suporte a scripts de setup e archive em folder workspaces (`#40034`), permitindo que workspaces multirrepositório inicializem seus checkouts filhos de forma totalmente declarativa.
2. Incorporar a configuração `emptyWorkspaceSurface: 'empty'` (`#40024`) no `brza-studio`, oferecendo inicialização leve de workspaces sem disparos automáticos de terminais ociosos.
3. Integrar o Remote Control automático em sessões do Native Chat (`#40020`), permitindo continuidade transparente no celular de conversas iniciadas na UI nativa.
4. Aplicar a guarda preventiva de transcript em "Continue in Chat UI" (`#40017`), eliminando a perda de sessões recém-abertas no terminal.
5. Avaliar o comportamento de Always on Top e atalhos de invocação global para pop-outs de chat e terminais (`#39992`).
