---
status: open
description: A issue #39563 e os PRs #39613, #39581, #39540, #39555 e #39530 trazem validação de objetivos em automações, comandos CLI de extensões, desobstrução de rate limit e resiliência de chat.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-07
tags:
  - tooling
  - infra
---

# Validação de conclusão em automações, CLI de extensões e destravamento de rate limit

Rastreado da issue aberta no upstream [`stablyai/orca#39563`](https://github.com/stablyai/orca/issues/39563),
do PR [`stablyai/orca#39613`](https://github.com/stablyai/orca/pull/39613) (resolve Issue [`#39578`](https://github.com/stablyai/orca/issues/39578)),
do PR [`stablyai/orca#39581`](https://github.com/stablyai/orca/pull/39581),
dos PRs [`stablyai/orca#39540`](https://github.com/stablyai/orca/pull/39540),
[`stablyai/orca#39555`](https://github.com/stablyai/orca/pull/39555) (atendendo à Issue [`#39122`](https://github.com/stablyai/orca/issues/39122)) e
[`stablyai/orca#39530`](https://github.com/stablyai/orca/pull/39530) (atendendo à Issue [`#39529`](https://github.com/stablyai/orca/issues/39529) e [`#32242`](https://github.com/stablyai/orca/issues/32242)).

## O problema

1. **Falso positivo de sucesso em automações não assistidas com recusa de modelo (`#39563`):**
   Em automações autônomas e rotinas agendadas (como radares periódicos, geração de relatórios e auditorias), o app
   tratava qualquer finalização de turno do modelo com `stop_reason: end_turn` como `status: completed` e `error: null`.
   Quando o modelo de backend retornava uma recusa textual simples (ex.: *"I'm sorry, but I cannot assist with that request"*)
   ou terminava sem disparar ferramentas nem produzir artefatos, a automação marcava o ciclo como bem-sucedido. Não havia
   validação de conclusão pós-execução baseada em código de saída ou existência de artefatos datados, nem suporte nativo a
   retentativas automáticas e delimitadas (*bounded retries*).
2. **Impossibilidade de recarregar extensões do navegador via CLI durante automação (`#39578`):**
   O navegador embutido do app suporta o carregamento de extensões desempacotadas (`unpacked extensions`), mas a CLI não
   oferecia comandos para listar ou recarregar as extensões instaladas. Quando um agente editava scripts de conteúdo ou código
   da extensão, o comando `orca reload` apenas atualizava a página web mantendo scripts em memória antigos, forçando a
   intervenção manual de um usuário na interface gráfica para recarregar o pacote.
3. **Deadlock no semáforo de requisições ao GitHub por expiração de rate limit (`#39581`):**
   O semáforo de processos `gh` (`src/main/github/gh-utils.ts`) possui limite de 4 slots de concorrência. Operações que
   adquiriam um slot (ex.: listagem de comentários de PR, carregamento de checks e status de hosted review) chamavam
   `assertRateLimitBudget` -> `getRateLimit()` enquanto retinham o slot. Quando o cache de 30 segundos da cota da API
   expirava, `getRateLimit()` disparava uma sondagem de `/rate_limit` que também tentava adquirir um slot no mesmo semáforo.
   Com 4 requisições aguardando a sondagem e a sondagem enfileirada atrás delas, ocorria um deadlock completo: abas de PRs,
   páginas de checks e ações de revisão ficavam travadas indefinidamente em hosts locais e remotos.
4. **Perda de miniaturas de imagens no chat após limpeza de arquivos temporários (`#39540`):**
   No chat nativo estruturado, a execução da ferramenta `Read` sobre uma imagem PNG gerava uma miniatura apontando diretamente
   para o caminho do arquivo no disco (`file_path`). Quando o agente de desenvolvimento posteriormente executava rotinas de
   limpeza (ex.: `rm -rf target/tmp`), todas as miniaturas no histórico do chat quebravam, apesar de os bytes da imagem
   terem sido transmitidos originalmente no resultado da ferramenta.
5. **Retenção visual de `/compact` no composer durante conexões de alta latência (`#39555`, `#39122`):**
   Ao submeter comandos de conversa como `/compact` ou `/clear`, o texto digitado permanecia visível no campo de entrada
   até que o host remoto respondesse. Em conexões SSH ou servidores remotos com latência, o usuário tinha a falsa impressão
   de que o comando não havia sido enviado, gerando reenvios duplicados acidentais.
6. **Composers e TUIs ilegíveis em terminais claros por falta de resposta a OSC 10/11 (`#39530`, `#39529`, `#32242`):**
   Programas de terminal como `cursor-agent`, OpenCode e Codex consultam as cores ativas de primeiro plano e fundo via
   sequências de escape OSC 10 e OSC 11 na inicialização para ajustar seu tema. Quando a pane de terminal não possuía cores
   explícitas definidas no tema (`terminal.options.theme`), as consultas ficavam sem resposta, forçando essas ferramentas
   a assumirem um tema escuro padrão com fontes escuras sobre fundo claro, tornando os campos de texto invisíveis.

## O que o upstream propõe e implementa

- **Contrato de validação e recuperação em automações autônomas (`#39563`):**
  - Desacoplamento estrito entre o ciclo de vida da sessão/turno (`end_turn`) e o sucesso do objetivo do negócio;
  - Normalização e classificação estruturada de falhas de transporte, limites de cota, sobrecarga e recusas explícitas;
  - Introdução de comando opcional de validação pós-execução (*post-run completion validator*), verificando exit code e
    integridade de artefatos gerados no diretório do relatório antes de assinalar conclusão;
  - Política delimitada de recuperação (*bounded automatic recovery*) com backoff, limite de tentativas e coordenação
    com o mecanismo interno de retry dos SDKs para evitar invocações duplicadas.
- **Comandos de gerenciamento de extensões na CLI (`#39578`):**
  - Adição de `orca extension list [--profile <id>] [--json]` para inspeção de extensões ativas;
  - Adição de `orca extension reload <extension-id | --path <folder>> [--profile <id>]` para recarga direta a partir do terminal.
- **Desobstrução do semáforo de concorrência do GitHub (`#39581`):**
  - Remoção da obrigatoriedade de aquisição de slot no semáforo para a rota de sondagem de cota `/rate_limit` em
    `src/main/github/rate-limit.ts`;
  - As sondagens de rate limit passam a ser deduplicadas globalmente sem disputar vagas no semáforo de 4 slots,
    eliminando permanentemente o deadlock em carregamentos concorrentes de PRs e checks.
- **Armazenamento de miniaturas por hash SHA-256 no chat nativo (`#39540`):**
  - Captura imediata dos bytes de imagem base64 no processo principal no recebimento do resultado da ferramenta `Read`;
  - Persistência no attachment store da sessão do agente endereçado por conteúdo (SHA-256), referenciado em `resultImagePaths`
    no diário sem sobrecarregar o tráfego IPC;
  - Garantia de exibição das miniaturas mesmo após o arquivo temporário ser removido do sistema de arquivos do projeto.
- **Liberação imediata do composer em comandos de chat (`#39555`):**
  - Repasse do callback `onSent` pelo despachante de comandos estruturados (`sendStructuredConversationCommand`), limpando o
    rascunho no momento da transmissão sem aguardar o retorno da resposta do host remoto;
  - Restauração automática do texto digitado caso o comando seja recusado pelo servidor.
- **Resolução de consultas de cor de terminal OSC 10/11 (`#39530`):**
  - Implementação de `colorQueryFallback` a partir da aparência composta do tema quando `terminal.options.theme` não contiver
    `foreground` ou `background`;
  - Semeadura inicial do tema no momento da criação da pane, garantindo respostas rápidas com formato `rgb:` e compatibilidade
    com TUIs que sondam o terminal uma única vez na inicialização.

## Impacto para o BrzA Studio e ferramental

1. **Automações de radar de 6h mais robustas e confiáveis:** a separação entre `end_turn` e validação real do objetivo
   resguarda a execução autônoma de tarefas agendadas, garantindo que execuções que não gerarem arquivos de issue ou notas
   sejam devidamente identificadas e recuperadas.
2. **Autonomia em testes de extensões e plugins web:** a disponibilização de comandos CLI para recarregar extensões destrava
   ciclos ágeis de desenvolvimento de plugins com WebViews e scripts de navegador.
3. **Estabilidade de visualização de PRs e Git no Studio:** o fim do deadlock de rate limit do GitHub previne que a interface
   desktop trave em carregamentos de painéis de pull request e verificação de status.
4. **Fidelidade visual no Native Chat e terminais:** miniaturas de imagens duráveis e compatibilidade plena com temas claros
   em ferramentas TUI (`cursor-agent`, OpenCode) evitam frustrações diárias de ergonomia visual.
