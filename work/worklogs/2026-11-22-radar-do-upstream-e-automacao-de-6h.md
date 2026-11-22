---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-22
completed: 2026-11-22
tags:
  - tooling
refs:
  - issue:badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-22)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-21T21:00:00Z` e `2026-11-22T03:15:00Z` (range upstream `3b8cbe221f2..f5b017a8f16`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#46287`, gravando o responsável por assumir cada pergunta de agente (`taker`) e vinculando tarefas `--for <messageId>` no `worker-start`; `#46446`, ordenando `worker-read` newest-first dentro do teto de 512 KiB para não descartar mensagens recentes em logs longos; `#46448`, notificando o coordenador e liquidando o worker quando o agente em terminal encerra com shell PTY mantido aberto; `#46273`, comitando atomicamente respostas e avisos de perguntas junto com seu correio em savepoint único do SQLite; `#46517`, eliminando o teto de 6 repasses e continuando hand-offs em salas de grupos através de `@mentions` sem mensagens duplicadas; `#46602` (STA-16956), forçando permissões estritas `0600` em arquivos de instruções e contexto de bots; e `#46478`, cessando a re-leitura contínua de workers concluídos na atualização da árvore de chats de bots.
   - [Proteção de arquivos ignorados no cleanup, compactação de histórico de chat e validação de TUI idle](../issues/protecao-de-arquivos-ignorados-no-cleanup-compactacao-de-historico-de-chat-e-validacao-de-tui-idle.md):
     adicionados os PRs `#46138`, protegendo checkouts restaurados no cleanup e validando o marcador `.git` pré e pós-prova com checagem de identidade do diretório raiz via `lstatBigInt` e parse linear de padding em `gitdir`; `#46581`, adotando índice de turnos para buscas rápidas de texto e prosa por turno no journal de conversas; e `#46201`, compactando o layout do diálogo de confirmação de exclusão de workspaces.
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#45876`, implementando exclusão atômica de chat via RPC `agentSession.delete.v1` com fechamento de abas e gravação de tombstone permanente no SQLite; `#45881`, tornando as linhas de chat mais limpas com chevron dinâmico no hover e status na prévia; `#46592`, limpando a faixa de mensagens enfileiradas com ações visíveis apenas sob hover, foco ou toque; `#46570`, equipando a caixa de comentários de itens com os mesmos seletores de menções `@` e comandos slash `/` do composer; `#46583`, exibindo nomes amigáveis de agentes do catálogo no seletor de Nova Aba; e `#46608`, renderizando esqueleto (*skeleton loader*) durante o carregamento de detalhes de itens de bots.
   - [Badges de worktree para plugins, cadência de PR e redesenho de automações](../issues/badges-de-worktree-para-plugins-cadencia-de-pr-e-redesenho-de-automacoes.md):
     adicionados os PRs `#46624` (refs `#46564`) e `#46584` (resolve `#46564`), identificando duravelmente a fonte de disparo de automações em `triggeredBy` e rotulando a origem real (Webhook, GitHub, Slack) em vez de `Scheduled`; `#46593`, provendo mensagens de erro descritivas e ajuda clara na validação de agendamentos cron de automações; e `#46522`, promovendo a ação 'Import Cookies' para o topo do menu do navegador integrado.
