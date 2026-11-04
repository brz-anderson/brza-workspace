---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-04
completed: 2026-11-04
tags:
  - tooling
refs:
  - issue:abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao
  - issue:consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream
  - issue:plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados
  - issue:repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli
  - issue:seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes
  - issue:subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent
  - issue:vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos
  - issue:workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-04)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas 43 novos PRs e 17 novas issues criados ou
   atualizados entre `2026-11-03T21:00:00Z` e `2026-11-04T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl` para evitar duplicações.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md)
     (PRs `#37977`, `#37978`, `#37979`, `#37941` e `#37931`): validação de hash SHA-256 de scripts de setup antes da
     execução em novos worktrees, isolamento contra RCE em branches untrusted, homologação explícita de hooks em automações
     e seletor compartilhado de modelos/esforço/permissões.
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#37918` (entrega de correio durante turnos ativos via steering sem espera ociosa), PR `#37966` (origem
     limpa de avisos de conclusão de background sem avatar artificial), PR `#37974` (limpeza de alertas desktop reconhecidos)
     e issue `#38000` (diferenciação visual entre Coordenador e workers na árvore de sessões);
   - [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md):
     adicionados PR `#38001` (abertura limpa de novo chat caso sessão CLI retomada não tenha transcript salvo) e PR `#37984`
     (split de aba Chat UI abre terminal shell de apoio em vez de clonar sessão de IA);
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados PR `#37943` (reinício imediato de sessões e workers na nova conta ao alternar), PR `#37998` (login limpo no
     Antigravity Chat sem reusar cache local) e PR `#38010` (opção Ultracode no seletor de esforço);
   - [Workers de plugins em hosts remotos e gerenciamento CLI de SSH](../issues/workers-de-plugins-em-hosts-remotos-e-gerenciamento-cli-de-ssh.md):
     adicionados PR `#37971` / issue `#37949` (subcomando `orca host rm` para remoção de servidores SSH salvos) e PR `#37926`
     (aplicação estrita de `IdentitiesOnly` no transporte SSH nativo);
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados PR `#37965` (recuperação de respostas bloqueadas e isolamento de UI de plugins), PR `#37960` (exibição de
     arquivos propostos e diffs em aprovações Codex), PR `#37952` (navegação de abas de chat por `Ctrl+PageUp`/`PageDown`),
     PR `#37932` (cache persistente de imagens em chats) e issue `#37983` (ranking unificado no menu `/` entre skills e comandos).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-04)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas dezenas de PRs e issues criados ou
   atualizados entre `2026-11-04T03:00:00Z` e `2026-11-04T09:00:00Z`.
2. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#38077` e issue `#38015` (fim do atraso de até 10 minutos na entrega de correio de conclusão de workers,
     eliminando o bug onde o ghost text esmaecido do Claude contava como draft pendente), PR `#38079` (redução dos fundos de status),
     PR `#37744` (emparelhamento direto entre chats locais "Work together...", atendendo `#37741`) e PR `#34895` (inspeção de
     histórico de subagentes filhos diretamente no chat pai);
   - [Repositórios vinculados no Source Control e escopo de worktree na CLI](../issues/repositorios-vinculados-no-source-control-e-escopo-de-worktree-na-cli.md):
     adicionados PR `#38086` (resolve `#37899`, fazendo comandos CLI disparados fora de qualquer checkout usarem o worktree do
     terminal chamador em vez do worktree em foco na janela), PR `#38063` (canonicidade e transacionalidade de membership de
     workspaces em abas de terminal e chat nativo), PR `#38055` (preservação do workspace em comandos de browser) e PR `#38072`
     (abertura de links de arquivos remotos no workspace do clique);
   - [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md):
     adicionado PR `#31595` (alternância no mesmo slot de aba entre Chat UI e Terminal sem forking nem duplicação de abas, com
     parada ordenada com prova de saída e importação limpa da transcrição);
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados PR `#38026` (recuperação de limite de uso diretamente na pane do terminal com tempo de reset e botão Continue now)
     e issue `#38052` (subagentes disparados via CLI passam a herdar a conta Claude do painel chamador em vez de usar a conta
     global ativa, evitando gasto indevido de cotas pessoais);
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionados PR `#38019` (seletor compartilhado de modelos/permissões no Source Control), PR `#38029` (desbloqueio imediato do
     Run Now em automações sem checar ferramenta GitHub) e PR `#33492` (reutilização limpa de agentes retidos por monitoramento);
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados PR `#38089` / issue `#38017` (clarificação da hierarquia da barra lateral com rótulos de grupos, blocos visuais de
     projetos e ênfase em atividade), PR `#38092` (organização de boards e catálogos por owner), PR `#38078` (reapontamento de projetos
     de pastas movidas sem duplicações) e PR `#38049` (supressão de escape tails residuais ao trocar de workspace).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-04)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas dezenas de PRs e issues abertos criados ou
   atualizados entre `2026-11-04T09:00:00Z` e `2026-11-04T15:00:00Z`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Vazamento de memória GPU WebGL no terminal e performance no macOS](../issues/vazamento-de-memoria-gpu-webgl-no-terminal-e-performance-macos.md)
     (PR `#38120`, issue `#38108` e issue `#38150`): correção de vazamento crítico de mais de 20 GB de memória gráfica
     `IOAccelerator` no Apple Silicon causado por texturas de atlas de glifos não liberadas no `@xterm/addon-webgl`,
     limitação do tamanho de página a 2.048 × 2.048 pixels e retração imediata de slots para 1 × 1 px, além de prevenção
     de bloqueio da thread principal no macOS.
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados PR `#38149` (suporte a `claudeConfigProfiles` permitindo lançar Claude a partir de perfis em pastas locais
     como `~/.claude-a` e `~/.claude-b` com credenciais próprias sem depender do switcher global), issue `#38134` (dashboard
     Home global para limites de uso e frota de agentes) e issue `#38116` (manter computador acordado contando agentes remotos SSH);
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#37757` (resolve `#37693`, gravando e fazendo replay da receita original de launch `launch_recipe` na
     reabertura de workers para não perder permissões Full access), issue `#38111` (ajuste no preâmbulo fixo para permitir push
     de branch e criação de PRs por workers sem bloqueio), issue `#38123` (correção de erro de rollback SQLite falso em `worker_done`
     no orcad headless) e issue `#38131` (tratamento de timeout de dsh);
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados PR `#38118` (resolve `#8766`, adicionando comandos CLI `orca project-group create/rename/add/ungroup/list/rm`
     com proteção contra desvinculação acidental), issue `#38112` (criação de folder workspaces via CLI) e issue `#38138` (ações
     e atalhos de colapso/expansão de workspaces);
   - [Segurança de hooks em worktrees e integridade de setup em automações](../issues/seguranca-de-hooks-em-worktrees-e-integridade-de-setup-em-automacoes.md):
     adicionado PR `#38128` (resolve `#37902`, tratando negação de acesso no teardown de observadores durante a exclusão de
     worktrees para evitar falhas espúrias quando o Git já removeu a pasta da lista de raízes autorizadas);
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados PR `#38094` (resolve `#38090`, importando a continuação indexada mais recente em vez do arquivo canônico
     defasado no Codex Chat), PR `#37640` (remoção de comandos exclusivos de terminal na superfície de chat do Codex), issue
     `#38100` (recuperação de sessões do Antigravity ACP no Session History), issue `#38124` (suporte a blocos advisor `server_tool_use`)
     e issue `#38115` (detalhes técnicos do modelo em hover no picker).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-04)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisadas mais de 40 novas issues e PRs criados ou
   atualizados entre `2026-11-04T15:00:00Z` e `2026-11-04T21:00:00Z`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Consumo de recursos em agentes: reaper de LSP e overhead de hooks](../issues/consumo-de-recursos-em-agentes-reaper-de-lsp-e-overhead-de-hooks.md)
     (PR `#38189` / issue `#38188`, PR `#38180` / issue `#38179` e PR `#38199` / issue `#38181`): idle reaper para
     encerrar instâncias ociosas de TypeScript LSP após 1h sem arquivos abertos (evitando acúmulo de mais de 28 GB de RAM
     em múltiplos agentes), redução de 17 para 7 subprocessos por evento de hook do Claude no macOS (diminuindo contenção
     de `AppleSystemPolicy`) e preservação da pasta `runtimes/` contra evicção indevida no `orcad`.
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionados PR `#38227` (subcomando `orca account select --agent claude --account <id|system>` com suporte a `--environment`
     para alternância remota via CLI), issue `#38224` (diagnóstico de consumo 1,5× maior da cota de 5h em abas de chat nativo
     em relação a terminais) e PR `#38201` / issue `#38195` (preservação da contagem integral de tokens do Claude em transcripts forked);
   - [Subagentes nativos, limpeza de correio de orquestração e superfície de super-agent](../issues/subagentes-nativos-limpeza-de-correio-de-orquestracao-e-superficie-de-super-agent.md):
     adicionados PR `#38174` (resolve `#38123`, garantindo que falhas em `worker_done` reportem o erro SQLite real em vez de
     `cannot rollback`), PR `#38207` e issue `#38210` (keep-awake para chats Pi enquanto subagentes rodam em background e suporte
     a sessões Pi RPC), PR `#38159` (recusa de submissão automática de prompt CLI sobre rascunho não enviado do composer) e
     PR `#38222` / issue `#38172` (notificação de término de turnos OpenCode sobre OSC 7501);
   - [Melhorias de Native Chat, ACP do Gemini CLI, abas e diff no upstream](../issues/melhorias-de-native-chat-acp-do-gemini-cli-abas-e-diff-no-upstream.md):
     adicionados PR `#38190` / issue `#37906` (inclusão do comando `/mcp` no seletor de slash commands do Claude Code no Native Chat),
     PR `#38183` (detalhes técnicos de contexto e custo ao passar o mouse sobre modelos) e PR `#38215` / issue `#38185` (renderização
     automática de diagramas Mermaid em comentários de PRs no painel Checks);
   - [Plugins de cartões na barra lateral, ordem de workspaces e sub-repositórios aninhados](../issues/plugins-de-cartoes-na-barra-lateral-ordem-de-workspaces-e-sub-repositorios-aninhados.md):
     adicionados PR `#38168` / issue `#38138` (ações "Collapse all" / "Expand all" e atalhos na barra lateral), PR `#38193` / issue
     `#38134` (dashboard Home global consolidando status e limites de frota), PR `#38208` (manutenção de worktrees ocultos ao adicionar
     projetos) e issue `#38214` (criação de grupos de projetos vazios pela sidebar).

## Fora do workspace

- **O quê e onde:** automação `Radar do upstream (stablyai/orca)` (`id: f75b8281-8ae3-4558-afe4-7ab5bbc35601`) ativa no
  runtime do BrzA Studio rodando a cada 6h (`0 */6 * * *`).
- **Estado:** ciclo das 18:00 BRT processado com sucesso.
