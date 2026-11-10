---
status: open
description: Os PRs #40756, #40760, #40679, #40708, #40754 trazem aprovação de workers no chat coordenador, diretório de mensagens e updates na status bar.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-10
tags:
  - chat
  - tooling
  - infra
---

# Aprovação de workers no chat, atualização de agentes e diretório de mensagens

Rastreado dos PRs abertos no upstream [`stablyai/orca#40756`](https://github.com/stablyai/orca/pull/40756) (empilhado sobre [`#40726`](https://github.com/stablyai/orca/pull/40726) e [`#40708`](https://github.com/stablyai/orca/pull/40708)),
[`stablyai/orca#40760`](https://github.com/stablyai/orca/pull/40760) (resolve Issue [`#40714`](https://github.com/stablyai/orca/issues/40714)),
[`stablyai/orca#40679`](https://github.com/stablyai/orca/pull/40679) (resolve Issue [`#24958`](https://github.com/stablyai/orca/issues/24958) e discussão `#24978`),
[`stablyai/orca#40754`](https://github.com/stablyai/orca/pull/40754) (Issue [`#40327`](https://github.com/stablyai/orca/issues/40327)),
[`stablyai/orca#40712`](https://github.com/stablyai/orca/pull/40712) (resolve Issue [`#40326`](https://github.com/stablyai/orca/issues/40326)),
[`stablyai/orca#40757`](https://github.com/stablyai/orca/pull/40757) e
[`stablyai/orca#40750`](https://github.com/stablyai/orca/pull/40750).

## O problema

1. **Necessidade de alternar manualmente para abas de workers para aprovar comandos (`#40756`, `#40726`, `#40708`):**
   Ao despachar subagentes e workers de orquestração a partir de um chat coordenador, qualquer solicitação de permissão
   ou comando de risco (ex.: `rm`, migrações de banco, scripts externos) ficava retida na aba ou terminal do worker.
   O operador no chat coordenador não recebia sinalização imediata, tendo que caçar abas em segundo plano para aprovar
   ou esperar o timeout de 2 minutos do Claude, bloqueando o fluxo de orquestração.
2. **Dificuldade de comparar e navegar entre perguntas anteriores em conversas extensas (`#40760`, `#40714`):**
   A trilha de navegação lateral (message rail) exibia apenas pequenas marcas visuais para as perguntas do usuário.
   Para inspecionar ou reler perguntas anteriores, o usuário precisava passar o mouse repetidamente sobre cada marca
   e memorizar o texto. Faltava um diretório textual expansível e persistente com navegação completa por teclado.
3. **Invisibilidade e atrito para atualizar CLIs de agentes de código instaladas (`#40679`, `#24958`):**
   Ferramentas como Claude Code, Codex, Aider e outras CLIs evoluem rapidamente com correções semanais. No Orca/Studio,
   o desenvolvedor não recebia nenhum aviso quando uma CLI instalada globalmente ficava desatualizada, descobrindo novos
   recursos ou bugs conhecidos apenas ao rodar checagens manuais no terminal fora do app.
4. **Crash global do daemon de terminais ao atingir limites de processos (`#40754`, `#40712`):**
   Em ambientes sob restrições de cgroup (ex.: contêineres, servidores compartilhados ou cotas de PID), quando o limite
   de processos era atingido durante o spawn de um novo terminal, a falha derrubava o daemon inteiro em vez de falhar apenas
   o spawn do processo requisitado, provocando a perda de todos os terminais abertos.
5. **Vazamento inadvertido de credenciais herdadas por scripts de receitas (`#40757`):**
   Scripts de provisionamento executados a partir de receitas de ambiente herdavam irrestritamente todas as variáveis de ambiente
   do processo pai (tokens de nuvem, chaves privadas), sem aviso ao usuário nem possibilidade de definir uma allowlist seletiva (`passEnv`).
6. **Rolagem travada e piscando no Claude Code em tela cheia (`#40750`):**
   No modo tela cheia do terminal com Claude Code, o redesenho constante da viewport de histórico causava engasgos e flicker
   visual durante rolagens rápidas.

## O que o upstream implementa e corrige

- **Cartões de aprovação de workers diretamente no chat coordenador (`#40756`, `#40726`, `#40708`):**
  - Roteia os prompts de escalonamento de permissões dos workers para a conversa do coordenador como cartões `NativeChatApprovalCard`;
  - Exibe faixa de contagem "N approvals · Show" acima do composer, mantendo a visibilidade mesmo enquanto o coordenador trabalha;
  - Apresenta contagem regressiva em tempo real ("Claude denies it on its own in 1:47 if nobody answers");
  - Botões de aprovação rápida (Allow/Deny) com resolução via IPC desktop `orchestration.approvalAnswer`, transformando o cartão após o fechamento em recibo detalhado ("Allowed by you", "Denied by coordinator", "Auto-denied by Claude after 2:00").
- **Diretório expansível de histórico de mensagens no Chat UI (`#40760`, resolve `#40714`):**
  - Adiciona painel lateral colapsável "Chat history" / "历史对话" ao lado do transcript;
  - Utiliza `VirtualizedList` com suporte a mais de 10.000 mensagens sem impacto na renderização;
  - Suporte completo a atalhos de teclado (Home, End, setas, Escape com restauração de foco) para salto instantâneo no transcript mantendo o diretório aberto.
- **Notificação e atualização de CLIs de agentes na barra de status (`#40679`, resolve `#24958`):**
  - Adiciona segmento na barra de status indicando atualizações disponíveis para CLIs de agentes instaladas;
  - Popover detalhado listando versões atuais, versões mais recentes e botão "Update" com 1 clique (executando o update isolado no host local ou remoto pareado);
  - Cache em memória com revalidação a cada 6 horas para poupar rede e CPU.
- **Resiliência a limites de processos em cgroups (`#40754`, `#40712`):**
  - Retém o spawn compulsório de novos terminais automáticos quando o cgroup está próximo do limite de PIDs e isola a falha para o spawn específico, mantendo o daemon estável.
- **Controle de credenciais em receitas com `passEnv` (`#40757`):**
  - Exibe no diálogo quais credenciais o script herdará e introduz allowlist explícita `passEnv`.
- **Rolagem suave no Claude Code em tela cheia (`#40750`):**
  - Sincronização de saída e buffers no fullscreen ativada por padrão para navegação fluida.

## O que fazer no BrzA Studio

1. Adotar a resolução de aprovações de workers no chat coordenador (`#40756`, `#40708`) no `brza-studio` e `brza-workflow`.
2. Integrar o diretório expansível de mensagens no Native Chat (`#40760`), aprimorando a navegação em conversas longas.
3. Incorporar o monitor de atualizações de CLIs de agentes na status bar (`#40679`).
4. Adotar o isolamento de falhas de spawn por limite de processos (`#40712`, `#40754`).
5. Adotar o controle de herança de credenciais via `passEnv` em receitas (`#40757`).
