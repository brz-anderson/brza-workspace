---
status: open
description: Os PRs #43082, #37434, #43153, #40407 e a issue #43071 trazem card unificado de seleção de agentes com abas no topo, navegação por teclado no AI Vault e barreira de setup.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-16
tags:
  - design
  - tooling
---

# Card unificado de agentes com abas superiores, atalhos de teclado e barreira de setup

Rastreado dos PRs abertos no upstream [`stablyai/orca#43082`](https://github.com/stablyai/orca/pull/43082),
[`stablyai/orca#37434`](https://github.com/stablyai/orca/pull/37434) (resolve Issue [`#37433`](https://github.com/stablyai/orca/issues/37433)),
[`stablyai/orca#43153`](https://github.com/stablyai/orca/pull/43153) (STA-15243, STA-13006),
[`stablyai/orca#40407`](https://github.com/stablyai/orca/pull/40407),
[`stablyai/orca#39855`](https://github.com/stablyai/orca/pull/39855) e
das issues [`stablyai/orca#43071`](https://github.com/stablyai/orca/issues/43071) e
[`stablyai/orca#43126`](https://github.com/stablyai/orca/issues/43126).

## O problema

1. **Fragmentação e redundância nos seletores de agentes no Studio (`#43082`):**
   Os seletores de agente variavam drasticamente entre o diálogo de hand-off, o composer de novo workspace, as ações do Source Control e as automações. Em alguns locais eram listas soltas, em outros cartões duplicados. Para escolher um agente e configurar modelo, esforço de raciocínio e superfície de execução (Chat vs Terminal CLI), o usuário precisava navegar por múltiplos menus desarticulados e desnecessariamente largos.
2. **Dependência obrigatória de mouse para navegar e buscar sessões no painel de agentes (`#37434`, resolve `#37433`, `#43071`):**
   O painel lateral Agents / AI Vault (onde residem o histórico e a busca de sessões passadas de agentes) não possuía atalhos de teclado mapeáveis. Ao contrário das demais abas da barra lateral, não era possível focar a busca, alternar entre os escopos (Workspace, Project, All) ou retornar ao terminal sem recorrer ao cursor do mouse.
3. **Disparo prematuro de agentes e perda de rascunhos vinculados antes da conclusão do Setup (`#43153`):**
   Comandos de inicialização de workspace (`orca.yaml` setup) consomem tempo de compilação ou instalação de dependências. Em servidores pareados no Windows e ambientes complexos, chats nativos ou despachos de terminais iniciavam antes do término do setup obrigatório ou mesmo após sua falha, corrompendo rascunhos de issues vinculadas e fazendo com que agentes executassem ferramentas sobre árvores de código ainda não preparadas.
4. **Ausência de suporte ao agente MiniMax Code (`#40407`) e falhas de prontidão no agente Muse no Windows (`#43126`):**
   Novas ferramentas e modelos de código como o MiniMax Code (mcode) não dispunham de integração nativa nos seletores de agente, enquanto em plataformas Windows agentes como o Muse colavam o prompt inicial mas não recebiam sinal de draft pronto, travando a submissão inicial.

## O que o upstream implementa

1. **Card unificado de seleção de agentes com abas de ícones no topo (`#43082`):**
   - Unifica os seletores de dropdown (hand-off, criação de workspace, source control e automações) em um componente modular padronizado;
   - Renderiza abas horizontais com ícones dos agentes suportados (Claude, Codex, Antigravity, OpenCode, Hermes, etc.) no topo do card, com indicador visual sublinhado e badge de equipe quando aplicável;
   - Organiza o fluxo de seleção em passos verticais diretos: agente selecionado → caixa de busca universal → modelos disponíveis (com fold "More models") → linha única com esforço de raciocínio à esquerda e toggle Fast à direita → controle segmentado "Open in: Chat | CLI";
   - Ao selecionar o modelo ou a superfície, o dropdown fecha e atualiza concisamente o botão de disparo (ex.: `Claude (CLI) · Claude Opus 5.5 · Med`);
   - Simplifica lançamentos pontuais removendo campos avançados redundantes de permissões e argumentos (mantidos onde configuram início persistente em automações e Settings).
2. **Navegação completa por teclado no painel Agents / AI Vault (`#37434`, resolve `#37433`):**
   - Adiciona três novas ações configuráveis em *Settings > Keyboard*: `sidebar.agents.toggle` (abre/fecha o painel focando o input de busca), `sidebar.agents.scopeNext` e `sidebar.agents.scopePrevious` (alterna ciclicamente entre Workspace, Project e All);
   - Tecla <kbd>Esc</kbd> no campo de busca do painel devolve o foco imediatamente para a aba de terminal, editor ou navegador ativa sem fechar a barra lateral nem apagar a consulta;
   - Compatibiliza atalhos compartilhados para que combinações de troca de aba funcionem normalmente quando o foco estiver em um documento, atuando como troca de escopo apenas quando o foco estiver dentro do painel.
3. **Barreira rigorosa de Setup para startup de agentes e entrega de rascunhos (`#43153`):**
   - Condiciona o despacho de terminais interativos, inicialização do provedor de Native Chat e entrega de rascunhos de tarefas à confirmação de término bem-sucedido do Setup obrigatório;
   - Caso o Setup falhe ou permaneça incompleto, o sistema recusa a execução automática de ferramentas pelo agente mas preserva intactos o workspace, os prompts e os rascunhos vinculados para retentativa assistida aprovada pelo desenvolvedor.
4. **Integração do agente MiniMax Code (mcode) (`#40407`):**
   - Adiciona `mcode` ao catálogo de agentes com suporte a seleção de modelos de chat e execução configurada.

## O que fazer no BrzA Studio

- Adotar o card unificado de seleção de agentes com abas no topo (`#43082`), proporcionando consistência visual em diálogos de hand-off, source control e criação de workspaces.
- Mapear os atalhos de teclado para navegação no painel de agentes e alternância de escopo (`#37434`).
- Incorporar a barreira de prontidão de Setup (`#43153`), garantindo que nenhum agente inicie mutações ou consuma rascunhos antes da conclusão exitosa dos scripts de setup do workspace.
- Adicionar suporte nativo ao MiniMax Code (`#40407`).
