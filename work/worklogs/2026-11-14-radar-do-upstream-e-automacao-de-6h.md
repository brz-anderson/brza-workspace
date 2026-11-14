---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-14
completed: 2026-11-14
tags:
  - tooling
refs:
  - issue:abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao
  - issue:alocacao-de-chats-sob-host-independente-admissao-de-git-e-cache-de-modelos
  - issue:alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas
  - issue:autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao
  - issue:cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat
  - issue:conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes
  - issue:cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz
  - issue:isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli
  - issue:janela-unificada-de-fork-cross-host-e-botao-compartilhado-de-envio-de-notas
  - issue:leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
  - issue:retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal
  - issue:seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-14)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-13T21:00:00Z` e `2026-11-14T03:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz](../issues/cursor-no-chat-via-acp-previa-de-links-de-imagem-bifurcacao-resiliente-e-leitura-por-voz.md):
     rastreia o PR `#42193` (e `#41494` — execução do agente Cursor no Native Chat via servidor ACP com modelos, esforço e planos),
     PR `#42227` (renderização automática de prévia visual de arquivos de imagem locais gerados que são linkados em respostas Markdown),
     PR `#42215` (resolve Issue `#41903` — enfileiramento confiável de `/fork` durante a geração de resposta para bifurcar após o término do turno),
     PR `#42168` (leitura em voz alta de respostas finalizadas com botão Speak e controles de fala/TTS nas configurações de chat),
     PR `#42211` (envelopamento de listas extensas de parâmetros de agentes em cartões com rolagem vertical),
     além das issues `#42214` (cópia rica com arquivo e linha de seleções Markdown) e `#42187` (limpeza de thread com `/new` no mobile).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Autenticação MCP no chat, alerta de turnos ativos e cache de orquestração](../issues/autenticacao-mcp-no-chat-alerta-de-turnos-ativos-e-cache-de-orquestracao.md):
     adicionados o PR `#42222` e o PR `#42224` (painel de gerenciamento de servidores MCP via `/mcp` no chat desktop e mobile para listar, reconectar e ligar/desligar servidores) e
     o PR `#42219` (cartões visuais dedicados no chat para solicitações de sign-in web requisitadas por servidores MCP e agentes).
   - [Segurança no macOS: remoção de allow-dyld-environment-variables dos entitlements e colisão de LC_UUID](../issues/seguranca-macos-remocao-de-allow-dyld-environment-variables-dos-entitlements.md):
     adicionados o PR `#42245` / Issue `#38247` (UUID de executável e assinatura dedicada para o terminal host no macOS, estabilizando permissões de Local Network no macOS Sequoia) e
     o PR `#42136` / Issue `#39405` (leitura nativa in-process do layout de teclado no macOS, eliminando processos `orca-keyboard-layout` e vazamento de portas Mach no WindowServer).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionado o PR `#42254` (limpeza imediata de referências e mapa de subagentes em memória ao fechar a aba de chat correspondente).
   - [Alocação de chats locais sob host independente, admissão de Git e cache de modelos](../issues/alocacao-de-chats-sob-host-independente-admissao-de-git-e-cache-de-modelos.md):
     adicionados o PR `#42253` (I/O assíncrono para leitura e gravação de conexões de servidores remotos fora da thread principal),
     o PR `#42247` (isolamento de slots de descoberta de modelos para impedir que CLIs travadas bloqueiem outros agentes) e
     o PR `#42189` (gravação assíncrona fora da thread principal para armazenamento de extensões do navegador).

### 2. Ciclo de 6h (06:00 BRT / 09:00 UTC em 2026-11-14)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-14T03:00:00Z` e `2026-11-14T09:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Conectores de linhagem na sidebar, cores de grupos de projeto e isolamento de extensões em perfis](../issues/conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes.md):
     rastreia o PR `#42312` (árvore visual com conectores de linhagem `├`, `╰` na sidebar para child workspaces aninhados),
     PR `#42303` (suporte a cores de grupos de projeto com linhas verticais contínuas estilo thread de e-mail),
     PR `#42324` (resolve Issue `#41906` — suspensão de background workers e alarmes de extensões em perfis de navegador inativos, eliminando churn ocioso de 2-4 GB de RAM),
     e o PR `#42261` (manutenção do posicionamento e estabilidade do menu de contexto de abas na sidebar durante a exclusão de outra aba).
3. **Atualização de 4 issues existentes em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados o PR `#42338` (resolve Issue `#42103` — restauração do objeto `run` com `coordinator_handle` na saída concisa `--json` de `run-show`, `run-current` e `run-use`),
     o PR `#42264` (resolve Issue `#19166` — liberação resiliente em `worker-release` mesmo quando o terminal PTY do worker já tiver encerrado ou sido fechado),
     e o PR `#42284` (resolve Issue `#42230` — exposição de `creatorOrcaSessionId` e `assigneeOrcaSessionId` no JSON de workers).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#42335` (preservação visível da resposta do assistente anterior a uma mensagem de steer em turnos concluídos e colapsados),
     o PR `#42278` (exibição de modelo e nível de esforço de raciocínio no tooltip do botão de modelo no composer),
     e o PR `#42271` (comando `/review` nativo do Codex com seletor de 4 escopos de revisão e instruções personalizadas).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42323` (resolve Issue `#42116` — hook `PreToolUse` emitindo `decision: allow` em vez de `ask` para ferramentas auto-aprovadas ou com política `always-proceed`),
     e o PR `#42282` (resolve Issue `#42280` — derivação de opções de esforço de raciocínio para modelos agrupados a partir de `availableModels` no cliente ACP).
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionado o PR `#42290` (resolve Issue `#42289` — retenção do bookmark de retomada de agentes restaurados em falhas prematuras de boot, impedindo conversão espúria da aba em shell plano).
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#42305` (resolve Issue `#42099` — faixa horizontal de subagentes ativos no mobile para chats em terminal),
     o PR `#42307` (preservação estável de perguntas pendentes em reinicializações do app sem disparos duplicados de modelo),
     e o PR `#42287` (resolve Issue `#42286` — correspondência exata de versão pontual do modelo Claude no banner).

### 3. Ciclo de 6h (12:00 BRT / 15:00 UTC em 2026-11-14)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-14T09:00:00Z` e `2026-11-14T15:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Isolamento de artefatos temporários de chat e estúdio de temas via CLI](../issues/isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli.md):
     rastreia o PR `#42410` (resolve Issue `#42404` — introdução de `ORCA_CHAT_TEMP_DIR` vs `ORCA_CHAT_SCRATCH_DIR`, ciclo de vida e comando `reclaim-chat-temp` para purga de builds descartáveis após 7 dias, e comando `storage:overview`),
     PR `#42360` (estúdio de temas ao vivo via CLI com `orca theme` e skills para validação de contraste/conformidade e preview sem reiniciar),
     PR `#42349` (suporte a temas definirem cor de seleção de texto no editor de código),
     e o PR `#42347` (herança consistente do tema ativo da aplicação em janelas pop-out).
3. **Atualização de 5 issues existentes em `work/issues/`:**
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionado o PR `#42357` (resolve Issue `#42356` — sincronização de títulos contextuais de resumo da conversa do Antigravity para abas de terminal).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#42370` (marcador visual de forks com prefixo `Fork:` no título e pill / notice row `Forked from <session>`),
     o PR `#42372` (resolve Issue `#40700` — configuração `Auto expand tools` para expandir execuções de ferramentas em tempo real preservando colapso manual),
     o PR `#42409` (resolve Issue `#42407` — correção de <kbd>Ctrl+A</kbd> e <kbd>Ctrl+E</kbd> no composer no macOS para navegar dentro da linha criada com Shift+Enter),
     e o PR `#42359` (polimento tipográfico do chat nativo).
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionados o PR `#42391` (resgate de agentes ociosos em sleep usando checkpoint live salvo para evitar degradação em shell plano),
     o PR `#42374` (resolve Issue `#40658` — divisão direcional de terminal via CLI com `--direction up|down|left|right`),
     e o PR `#42368` (simplificação do diálogo de fechamento de terminais em execução).
   - [Conectores de linhagem na sidebar, cores de grupos de projeto e isolamento de extensões em perfis](../issues/conectores-de-linhagem-na-sidebar-cores-de-grupos-e-isolamento-de-extensoes.md):
     adicionado o PR `#42346` (resolve Issue `#42345` — rodapé expansível `Sleeping (N)` na sidebar para acordar workspaces adormecidos sem desativar o filtro "Hide sleeping").
   - [Abertura de agentes no Chat UI pela CLI e superfície chat na orquestração](../issues/abertura-de-agentes-no-chat-ui-pela-cli-e-superficie-chat-na-orquestracao.md):
     adicionados o PR `#41354` (resolve Issue `#41351` — explicitação nos recibos de CLI de que lançamentos independentes não reportam automaticamente),
     e o PR `#42309` (resolve Issue `#42308` — suporte nativo ao agente terminal `loop` com rota `/hook/loop` para status e retomada de sessão).

### 4. Ciclo de 6h (18:00 BRT / 21:00 UTC em 2026-11-14)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e issues abertos criados ou
   atualizados entre `2026-11-14T15:00:00Z` e `2026-11-14T21:00:00Z`, comparando com as notas em `work/issues/` e o índice
   `.brza/index.jsonl`.
2. **Criação de 1 nova issue priorizada em `work/issues/`:**
   - `priority: high` — [Janela unificada de Fork cross-host e botão compartilhado de envio de notas](../issues/janela-unificada-de-fork-cross-host-e-botao-compartilhado-de-envio-de-notas.md):
     rastreia o PR `#42437` (resolve Issue `#42436` — diálogo unificado de Fork no desktop e mobile suportando destinos cross-host via extensão de protocolo `ai-vault.chat-fork-import.v1` e forks sem créditos remotos a partir do resumo local),
     o PR `#42482` (componente compartilhado `SendNotesButton` unificando toolbar de Changes, cabeçalho de diff, Source Control, markdown preview e comentários de PR, com menu Copy/Clear notes),
     o PR `#42476` (configuração `closeUnpinnedEditorTabsOnFocusLoss` para fechar abas limpas e não fixadas ao perder o foco do editor e atalho `Mod+Alt+Shift+P` para alternar fixação),
     e o PR `#42466` (indicação cromática de saúde de cotas por percentual consumido no status bar/roster e alternador Used/Left).
3. **Atualização de 6 issues existentes em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados o PR `#42455` (slide-up sheet para subagentes no chat pane sem desmontar ou rolar a conversa pai) e
     o PR `#42448` (suporte e renderização visual de subagentes no Pi Native Chat).
   - [Alternância entre TUI e Native Chat no Antigravity, auth remota e dimensionamento de abas](../issues/alternancia-entre-tui-e-native-chat-no-antigravity-auth-remota-e-dimensionamento-de-abas.md):
     adicionados o PR `#42460` (resolve Issue `#41961` — suporte a variantes completas do Gemini 4 como Hydrogen, Carbon e Argon, esforços estendidos `xhigh` e `max`, e fallback resiliente) e
     o PR `#42464` (suporte ao runtime gerenciado e chat nativo do Antigravity no Windows).
   - [Cartões de Pull Request, feedback de Steer e atalhos no Native Chat](../issues/cards-de-pull-request-e-feedback-de-steer-e-atalhos-no-native-chat.md):
     adicionados o PR `#42459` (exibição de estado explícito `waiting` / "waiting on you" para perguntas assíncronas no Codex) e
     o PR `#42445` (resolve Issue `#42187` — comando `/new` no composer de Codex como alias funcional de `/clear`).
   - [Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal](../issues/retomada-de-sessoes-gravadas-pela-cli-hosts-de-workspace-e-replay-de-terminal.md):
     adicionados o PR `#42484` (resolve Issue `#42470` — retries automáticos com backoff em probes SSH com encerramento prematuro de conexão por ProxyCommand) e
     o PR `#42481` (classificação diagnóstica detalhada de saída de terminais no log do daemon).
   - [Isolamento de artefatos temporários de chat e estúdio de temas via CLI](../issues/isolamento-de-artefatos-temporarios-de-chat-e-estudio-de-temas-via-cli.md):
     adicionados o PR `#42479` (isenção de arquivos de diário `.journal`, WAL e SHM da exclusão automática de 7 dias) e
     o PR `#42418` (resolve Issue `#42413` — descarte seguro e reconstrução automática de entradas corrompidas no cache de fontes de uso sem travar varreduras).
   - [Leitura antecipada e preservação de skills no arranque e nos plugins](../issues/leitura-antecipada-e-preservacao-de-skills-no-arranque-e-nos-plugins.md):
     adicionado o PR `#42472` (resolve Issue `#42408` — eliminação de falsos alertas "Needs attention · You edited this copy" em skills embutidas renomeadas através de verificação canônica e digests de release).
