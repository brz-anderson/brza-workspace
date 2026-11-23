---
scope:
  - brza-studio
  - brza-workflow
  - workspace
opened: 2026-11-23
completed: 2026-11-23
tags:
  - tooling
refs:
  - issue:fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks
  - issue:gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache
  - issue:painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat
  - issue:retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot
---

# Radar de issues e PRs do upstream e automação de 6h (00h, 06h, 12h e 18h BRT)

## O que foi feito

### 1. Ciclo de 6h (00:00 BRT / 03:00 UTC em 2026-11-23)

1. **Varredura delta das últimas 6h no upstream (`stablyai/orca`):** analisados novos PRs e commits criados ou atualizados entre `2026-11-22T21:00:00Z` e `2026-11-23T03:00:00Z` (range upstream `2178e7cd95a..15407c8854f`), comparando com os registros em `work/issues/` e o índice `.brza/index.jsonl`.
2. **Atualização de 4 issues rastreadas em `work/issues/`:**
   - [Painel de atividades de subagentes e anotações visuais no Native Chat](../issues/painel-de-atividades-de-subagentes-e-anotacoes-visuais-no-native-chat.md):
     adicionados os PRs `#47200`, migrando mensagens enfileiradas ordenadamente ao substituir sessões de chat e drenando mensagens de conectores com aviso explícito de parada; `#47220`, liberando a execução do correio de terceiros no próximo turno após falhas operacionais não causadas por limite de cota (*usage limit*); e `#47191`, permitindo que agentes anexem tarefas, PRs, URLs, arquivos e comandos `worker-start --item` a itens em aberto de outros agentes na árvore do workspace com atribuição amigável ("Another agent").
   - [Retenção do banco de orquestração, despertar de coordenadores e geração de texto one-shot](../issues/retencao-do-banco-de-orquestracao-despertar-de-coordenadores-e-geracao-de-texto-one-shot.md):
     adicionados os PRs `#47135`, desvinculando (*unbinds*) Runs ativos e notificando perguntas de workers com aviso de *no reader* imediatamente quando o terminal do coordenador é encerrado ou sua pane esvaziada; e `#47081`, exibindo o estado de espera na árvore de tarefas quando um worker aguarda sua própria tarefa em segundo plano e disparando notificação única ao coordenador após 60 minutos de espera contínua.
   - [Fontes web em plugins, isolamento de atalhos e resiliência de hooks](../issues/fontes-web-em-plugins-isolamento-de-atalhos-e-resiliencia-de-hooks.md):
     adicionado o PR `#47107` (resolve `#47104`), reconhecendo rotas `/src/{branch,tag,commit}/<ref>` em repositórios Codeberg, Gitea e Forgejo no instalador Git de plugins, extraindo a URL base de clone e o ref correto.
   - [Gestão de contas Claude, chaveamento de cota e preservação de prompt cache](../issues/gestao-de-contas-claude-chaveamento-de-cota-e-preservacao-de-prompt-cache.md):
     adicionado o PR `#47209` (refs `#47146`), resolvendo raízes de perfis Claude via `realpath` para desduplicar a varredura, análise e indexação de transcripts em diretórios compartilhados de projetos globais.
