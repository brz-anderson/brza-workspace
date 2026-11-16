---
priority: high
tags:
  - auth
  - tooling
description: Os PRs #42856, #42917, #42891, #42887 e as issues #42899, #42887 trazem chaveamento automático de contas do Claude ao atingir limite de uso, exibição de planos e resgate de resets de cota.
---

# Chaveamento automático de contas Claude por limite de uso, planos observados e resgate de cota

Rastreado dos PRs abertos no upstream [`stablyai/orca#42856`](https://github.com/stablyai/orca/pull/42856),
[`stablyai/orca#42917`](https://github.com/stablyai/orca/pull/42917),
[`stablyai/orca#42891`](https://github.com/stablyai/orca/pull/42891) (resolve Issue [`#42887`](https://github.com/stablyai/orca/issues/42887)),
além das issues [`stablyai/orca#42899`](https://github.com/stablyai/orca/issues/42899) e
[`stablyai/orca#42887`](https://github.com/stablyai/orca/issues/42887).

## O problema

1. **Interrupção de fluxos de trabalho e automações ao esgotar cotas de uso do Claude (`#42856`):**
   Desenvolvedores com múltiplas contas ou planos corporativos/pessoais do Claude eram bloqueados subitamente quando uma conta atingia 100% de uso. As automações e tarefas em execução falhavam ou ficavam travadas aguardando que o usuário percebesse o erro, abrisse manualmente as configurações e selecionasse outra conta com saldo disponível.
2. **Falta de visibilidade sobre os planos contratados de contas salvas (`#42917`):**
   A tela de contas do Claude e Codex listava apenas e-mails ou nomes de perfis, sem indicar a categoria de assinatura vinculada (ex.: Free, Pro, Team, Enterprise), dificultando a escolha da conta mais adequada para tarefas pesadas.
3. **Impossibilidade de resgatar bônus de reset de cota diretamente no aplicativo (`#42891`, resolve `#42887`):**
   Ao atingir limites temporários, links ou créditos de reset disponibilizados pela Anthropic precisavam ser ativados fora do ambiente do Studio, sem integração no menu de uso de contas.

## O que o upstream implementa

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

## O que fazer

- Implementar o chaveamento automático de contas no BrzA Studio para Claude quando o limite de 100% for atingido (`#42856`).
- Exibir a categoria de plano associada a cada conta salva nas preferências de contas (`#42917`).
- Integrar a ação de resgate de reset de limite de uso no menu de contas (`#42891`, resolve `#42887`).
