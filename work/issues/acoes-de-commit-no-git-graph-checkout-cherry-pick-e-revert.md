---
status: open
description: O PR #39069 e a issue #39083 trazem ações de checkout, cherry-pick e revert direto no Git Graph, filtro de worktrees e catálogo pt-BR.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-06
tags:
  - tooling
  - design
---

# Ações de commit no Git Graph (checkout, cherry-pick e revert)

Rastreado do PR aberto no upstream [`stablyai/orca#39069`](https://github.com/stablyai/orca/pull/39069), além das issues
[`stablyai/orca#39083`](https://github.com/stablyai/orca/issues/39083) e
[`stablyai/orca#39067`](https://github.com/stablyai/orca/issues/39067) (PR [`stablyai/orca#39091`](https://github.com/stablyai/orca/pull/39091)),
e do PR [`stablyai/orca#39124`](https://github.com/stablyai/orca/pull/39124).

## O problema

1. **Ausência de ações diretas no grafo de commits do Git Graph (`#39069`):**
   A visualização do Git Graph no aplicativo limitava-se à inspeção visual do histórico e à leitura de diffs. Operações
   comuns de desenvolvimento baseadas em commits específicos — como fazer checkout desanexado de um commit antigo para testes,
   aplicar cherry-pick de correções pontuais ou reverter um commit defeituoso — exigiam abrir o terminal e digitar comandos
   Git manuais, quebrando o fluxo visual e contornando as proteções contra checkouts inseguros.
2. **Insegurança e falta de confirmação em operações destrutivas sobre commits (`#39069`):**
   Aplicações de cherry-pick e revert via terminal frequentemente geram commits vazios indesejados ou conflitos silenciosos
   que deixam o repositório em estado inconsistente sem interface de orientação (*Abort* / *Continue*).
3. **Falta de filtragem de worktrees por estado de atividade (`#39083`):**
   Em projetos grandes com dezenas de worktrees simultâneos, não havia forma de filtrar na interface worktrees ativos,
   em revisão ou limpos/concluídos, dificultando a gestão da frota de branches.

## O que o upstream implementa

- **Menu de contexto e barra de confirmação no Git Graph (`#39069`):**
  - Adiciona ações de primeiro nível no menu de contexto de cada commit e no cabeçalho do painel de detalhes:
    - **Check out commit:** realiza checkout do commit selecionado em modo desanexado (`checkout --detach <oid>^{commit}`),
      garantindo que um branch local com nome similar ao OID não seja selecionado por engano;
    - **Cherry-pick:** aplica o commit selecionado no branch atual sem abrir editor (`--no-edit`), aborta automaticamente
      se o cherry-pick for vazio e proíbe merge commits acidentais;
    - **Revert:** reverte as alterações do commit selecionado com detecção precisa de conflitos e botões de *Abort* e *Continue*
      executando com `GIT_EDITOR=true` (compatível com macOS, Linux e WSL);
    - **Copy commit ID:** copia o SHA-1/SHA-256 completo do commit para a área de transferência;
  - Todas as ações exibem primeiro uma barra de confirmação embutida na aba (*confirmation strip*), prevenindo cliques acidentais
    e cancelando-se com segurança se o usuário mudar de filtro ou fechar o painel.
- **Integração com travas de segurança de branch (`#39069`):**
  - Reutiliza a rotina compartilhada de validação de branch (#38744), permitindo HEAD desanexado apenas quando o commit
    for alcançável a partir de uma tag, branch ou referência remota válida.
- **Internacionalização e catálogos em Português do Brasil (`#39124`):**
  - Atualiza as strings e mensagens das novas ferramentas com tradução completa para o idioma nativo (`pt-BR`).

## O que fazer no BrzA Studio

1. Portar as ações de commit do Git Graph (`#39069`) para o `brza-studio`, permitindo checkout, cherry-pick e revert com
   um clique e confirmação inline segura.
2. Adotar as proteções contra cherry-picks vazios e detecção de conflitos de reversão no workflow visual.
3. Incorporar as traduções dos novos fluxos no catálogo pt-BR do estúdio (`#39124`).
