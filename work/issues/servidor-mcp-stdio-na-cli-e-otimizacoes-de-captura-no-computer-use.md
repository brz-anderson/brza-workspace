---
priority: high
tags:
  - tooling
  - infra
description: Os PRs #42812, #42808, #42801, #42809 e issues #41618, #13079, #42799 trazem comando orca stats usage na CLI, servidor MCP stdio expondo 11 ferramentas nativas e automação para documentação.
---

# Servidor MCP stdio na CLI, métricas com orca stats usage e automação de documentação

Rastreado dos PRs abertos no upstream [`stablyai/orca#42812`](https://github.com/stablyai/orca/pull/42812) (resolve Issue [`#41618`](https://github.com/stablyai/orca/issues/41618)),
[`stablyai/orca#42808`](https://github.com/stablyai/orca/pull/42808) (resolve Issue [`#13079`](https://github.com/stablyai/orca/issues/13079)),
[`stablyai/orca#42801`](https://github.com/stablyai/orca/pull/42801) e
[`stablyai/orca#42809`](https://github.com/stablyai/orca/pull/42809) (resolve Issue [`#42799`](https://github.com/stablyai/orca/issues/42799)).

## O problema

1. **Incompatibilidade para conectar clientes externos de IA ao ecossistema do Studio via MCP (`#42808`, resolve `#13079`):**
   Ferramentas externas que consomem o Model Context Protocol (MCP) — como Claude Desktop, Cursor, agentes autônomos ou scripts em Python/Node — não tinham uma forma padronizada e segura de se conectar ao daemon em execução do Studio para manipular worktrees, terminais e contexto de repositórios via stdin/stdout (`stdio`).
2. **Payloads excessivos em capturas de tela no Computer Use consumindo cotas de contexto (`#42801`):**
   O comando `orca computer screenshot` gerava apenas imagens PNG completas e sem compressão. Em telas de alta densidade (Retina/4K), cada captura de tela atingia vários megabytes em Base64, gerando lentidão extrema no tráfego e estourando limites de tokens em modelos de visão.
3. **Falta de modelo padronizado de automação para tarefas periódicas de documentação (`#42809`, resolve `#42799`):**
   Usuários do Studio mantendo repositórios em evolução frequente precisavam criar scripts ad-hoc ou lembrar de rodar agentes manualmente para auditar documentação defasada, sem um template padrão de automação agendada no motor de workflows.
4. **Inacessibilidade programática aos agregados de consumo e custos de Stats & Usage (`#42812`, resolve `#41618`):**
   Agentes de linha de comando e ferramentas de automação que precisavam auditar consumo de tokens e custos estimados por modelo/projeto precisavam reconstruir cálculos a partir de transcrições brutas com risco de dupla contagem, sem acesso direto aos dados consolidados calculados pela interface do app.

## O que o upstream implementa

- **Consulta CLI a agregados de consumo via `orca stats usage` (`#42812`, resolve `#41618`):**
  - Introduz o comando `orca stats usage --provider claude|codex|opencode|muse [--range 7d|30d|90d|all] [--scope orca|all] [--sessions <n>] [--json]`;
  - Expõe o método RPC somente-leitura `stats.usage` que retorna diretamente o snapshot computado pela tela de Stats & Usage (tokens de entrada/saída/raciocínio, custo estimado em USD e detalhamento por modelo/projeto).
- **Servidor MCP stdio nativo na CLI (`#42808`, resolve `#13079`):**
  - Adiciona o subcomando `orca mcp`: inicializa um servidor Model Context Protocol via stdio compatível com a especificação 2024-11-05;
  - Expõe 11 ferramentas nativas do orca para agentes externos:
    - Gerenciamento de worktrees: `worktree_list`, `worktree_get`, `worktree_create`, `worktree_delete`;
    - Sessões e execução: `terminal_list`, `terminal_send`, `terminal_read`, `terminal_create`;
    - Repositórios e contexto: `repo_list`, `context_get`, `automation_trigger`;
  - Conecta-se automaticamente ao daemon local em execução do Studio via IPC de canal seguro autenticado.
- **Controle de compressão, formato e redimensionamento em `orca computer screenshot` (`#42801`):**
  - Adiciona flags para otimização de capturas de tela:
    - `--format <png|jpeg|webp>` (padrão: `png`);
    - `--quality <1..100>` (para jpeg e webp, padrão 80);
    - `--max-width <pixels>` e `--max-height <pixels>` com interpolação bicúbica para reduzir o tamanho da imagem antes da serialização;
  - Reduz o payload de imagens transmitidas para modelos de visão em até 85%, acelerando as iterações de Computer Use.
- **Template de automação para refresh periódico de documentação (`#42809`, resolve `#42799`):**
  - Adiciona o template de automação interna `docs-weekly-audit`: programa execução agendada para comparar commits recentes contra os diretórios `docs/` e `README.md`, identificando novos comandos ou opções CLI sem documentação correspondente e gerando um PR com a minuta atualizada.

## O que fazer

- Implementar o comando `brza stats usage` para leitura programática estruturada de métricas e custos de modelos via CLI e RPC (`#42812`, resolve `#41618`).
- Implementar o comando `brza mcp` com suporte ao protocolo MCP stdio e encaminhamento das 11 ferramentas nativas (`#42808`, resolve `#13079`).
- Suportar `--format`, `--quality`, `--max-width` e `--max-height` nas ferramentas de captura de tela de `brza computer` (`#42801`).
- Disponibilizar templates integrados de automação no Studio para auditoria e atualização de documentação (`#42809`, resolve `#42799`).
