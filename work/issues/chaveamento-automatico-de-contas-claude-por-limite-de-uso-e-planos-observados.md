---
priority: high
tags:
  - auth
  - tooling
description: Os PRs #43190, #43135, #43145, #43105, #43087, #43118, #43223, #42856, #42917, #42891 trazem contas por workspace no Codex, import de ~/.codex, filtros de tokens em stats, fixação de contas por worktree e chaveamento por cota.
---

# Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota

Rastreado dos PRs abertos no upstream [`stablyai/orca#43190`](https://github.com/stablyai/orca/pull/43190),
[`stablyai/orca#43135`](https://github.com/stablyai/orca/pull/43135) (resolve Issue [`#9496`](https://github.com/stablyai/orca/issues/9496)),
[`stablyai/orca#43145`](https://github.com/stablyai/orca/pull/43145),
[`stablyai/orca#43105`](https://github.com/stablyai/orca/pull/43105),
[`stablyai/orca#43087`](https://github.com/stablyai/orca/pull/43087),
[`stablyai/orca#43118`](https://github.com/stablyai/orca/pull/43118),
[`stablyai/orca#43223`](https://github.com/stablyai/orca/pull/43223) (resolve Issue [`#43222`](https://github.com/stablyai/orca/issues/43222)),
[`stablyai/orca#42856`](https://github.com/stablyai/orca/pull/42856),
[`stablyai/orca#42917`](https://github.com/stablyai/orca/pull/42917),
[`stablyai/orca#42891`](https://github.com/stablyai/orca/pull/42891) (resolve Issue [`#42887`](https://github.com/stablyai/orca/issues/42887)),
[`stablyai/orca#37943`](https://github.com/stablyai/orca/pull/37943),
[`stablyai/orca#37998`](https://github.com/stablyai/orca/pull/37998),
[`stablyai/orca#23228`](https://github.com/stablyai/orca/pull/23228),
além das issues [`stablyai/orca#43214`](https://github.com/stablyai/orca/issues/43214),
[`stablyai/orca#42899`](https://github.com/stablyai/orca/issues/42899) e
[`stablyai/orca#42887`](https://github.com/stablyai/orca/issues/42887).

## O problema

1. **Interrupção de fluxos de trabalho e automações ao esgotar cotas de uso do Claude (`#42856`):**
   Desenvolvedores com múltiplas contas ou planos corporativos/pessoais do Claude eram bloqueados subitamente quando uma conta atingia 100% de uso. As automações e tarefas em execução falhavam ou ficavam travadas aguardando que o usuário percebesse o erro, abrisse manualmente as configurações e selecionasse outra conta com saldo disponível.
2. **Falta de visibilidade sobre os planos contratados de contas salvas (`#42917`):**
   A tela de contas do Claude e Codex listava apenas e-mails ou nomes de perfis, sem indicar a categoria de assinatura vinculada (ex.: Free, Pro, Team, Enterprise), dificultando a escolha da conta mais adequada para tarefas pesadas.
3. **Impossibilidade de resgatar bônus de reset de cota diretamente no aplicativo (`#42891`, resolve `#42887`):**
   Ao atingir limites temporários, links ou créditos de reset disponibilizados pela Anthropic precisavam ser ativados fora do ambiente do Studio, sem integração no menu de uso de contas.
4. **Falta de fixação de contas dedicadas por worktree (`#43135`, resolve `#9496`):**
   Desenvolvedores que atuam simultaneamente em projetos de clientes distintos ou repositórios pessoais precisavam chavear manualmente a conta global ativa repetidas vezes. A troca afetava indiscriminadamente todos os worktrees abertos, arriscando faturar chamadas na conta errada ou violar políticas de acesso corporativo.
5. **Perda de mensagens e inconsistências ao alternar de conta com turnos em fila (`#43145`, `#43105`, `#37943`):**
   Ao trocar de conta enquanto mensagens estavam sendo digitadas ou aguardando execução, os prompts podiam disparar na conta anterior ou ser rejeitados; ademais, sessões em execução ficavam em estado híbrido caso o usuário desejasse migrar o conjunto de sessões ativas.
6. **Descarte involuntário de conversas ao remover uma conta do Claude (`#43118`):**
   A remoção de uma conta do Claude das preferências do aplicativo apagava ou tornava inacessíveis as conversas históricas vinculadas a ela, sem dar ao usuário a oportunidade de preservar as notas e transcrições geradas.
7. **Atribuição incorreta de uso pela linha selecionada na interface (`#43087`):**
   O monitoramento de cotas atribuía consumos à linha atualmente destacada na UI em vez de computar o uso estritamente pela chave da conta dona do evento.

## O que o upstream implementa

- **Fixação de worktree a uma conta dedicada de Claude ou Codex (`#43135`, resolve `#9496`):**
  - Permite fixar (*pin*) um worktree a uma conta específica de Claude ou Codex;
  - Ao focar ou abrir aquele worktree, o Studio associa imediatamente a conta fixada sem interferir na conta global ativa nos demais projetos.
- **Retenção de mensagens pendentes durante troca de conta (`#43145`):**
  - Segura o despacho de mensagens recém-enviadas no composer até que a inicialização do provedor na nova conta esteja pronta e autenticada.
- **Configuração para migrar sessões em execução ao alternar de conta (`#43105`):**
  - Adiciona configuração que permite transferir automaticamente sessões em andamento para a nova conta selecionada, reiniciando-as de forma transparente (`#37943`).
- **Preservação de conversas de contas removidas (`#43118`):**
  - Mantém o arquivo histórico de conversas de contas removidas disponível para leitura, a menos que o operador solicite explicitamente sua deleção.
- **Atribuição rigorosa de métricas e planos por conta lida (`#43087`):**
  - Corrige a leitura de telemetria para vincular o consumo à conta exata do snapshot de uso.
- **Chaveamento automático inteligente de contas ao atingir o limite de uso (`#42856`):**
  - Adiciona a configuração `claudeAccountSwitchAtUsageLimit` em *Settings › Accounts › Claude*;
  - Ao detectar que a conta ativa atingiu 100% de utilização:
    - Inspeciona as leituras de uso em cache das demais contas salvas;
    - Seleciona automaticamente a conta alternativa elegível que possua cota restante ou cujo reset esteja mais próximo;
    - Notifica o desenvolvedor via toast informativo sem interromper o fluxo do workspace;
    - Em tarefas interativas, reinicia sessões de forma graciosa aplicando a nova conta sem perda de contexto.
- **Identificação do plano observado em contas salvas (`#42917`):**
  - Detecta e exibe o tipo de plano ativo (Free, Pro, Team, Enterprise) junto a cada conta nos seletores e na tela de gerenciamento de contas do Claude e Codex.
- **Exibição e resgate de resets de cota no menu de uso (`#42891`, resolve `#42887`):**
  - Expõe o botão para resgate direto de resets de limite de uso no menu de contexto de contas, permitindo restaurar a capacidade operacional com um clique.
- **Contas Codex dedicadas por workspace e importação de `~/.codex` (`#43190`):**
  - Permite configurar contas Codex individuais por workspace, suportando importação direta do ambiente e credenciais existentes em `~/.codex`.
- **Alternância de tipos de tokens no gráfico de uso diário (`#43223`, resolve `#43222`):**
  - Permite clicar nos itens da legenda do gráfico de estatísticas diárias para ocultar ou exibir categorias específicas de tokens (input, output, cache read, cache write), facilitando o diagnóstico de custos de prompt cache.
- **Proteção contra ocultação de sessões ao alternar para OpenCode gerenciado (`#43214`):**
  - Assegura que alternar para uma conta gerenciada do OpenCode não oculte silenciosamente sessões pré-existentes do usuário.
- **Perguntar e memorizar conta do Claude por projeto no primeiro arranque (`#23228`):**
  - Solicita a conta preferida na inicialização de novos projetos e persiste a associação automaticamente para as sessões subsequentes.

## O que fazer

- Permitir a fixação de worktrees a contas específicas de Claude e Codex (`#43135`, resolve `#9496`), com suporte a importação de credenciais locais de `~/.codex` (`#43190`).
- Retirar riscos de perda de mensagens em trocas de conta retendo envios até a prontidão da nova conta (`#43145`).
- Preservar o histórico de conversas pertencentes a contas removidas (`#43118`).
- Implementar o chaveamento automático de contas no BrzA Studio para Claude quando o limite de 100% for atingido (`#42856`).
- Exibir a categoria de plano associada a cada conta salva nas preferências de contas (`#42917`).
- Integrar a ação de resgate de reset de limite de uso no menu de contas (`#42891`, resolve `#42887`).
- Assegurar atribuição correta de métricas de telemetria por conta lida (`#43087`).
- Habilitar filtro interativo por tipo de token na legenda do gráfico de uso em *Stats* (`#43223`, resolve `#43222`).
- Preservar visibilidade de sessões pré-existentes ao configurar contas gerenciadas do OpenCode (`#43214`).
- Permitir fixação interativa da conta de projeto no primeiro arranque com persistência de contexto (`#23228`).
