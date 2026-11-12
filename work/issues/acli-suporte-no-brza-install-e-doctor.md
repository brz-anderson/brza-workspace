---
status: open
description: Adicionar suporte à instalação e diagnóstico da Atlassian CLI no brza install e brza doctor.
scope:
  - brza-studio
  - workspace
opened: 2026-11-12
priority: low
tags:
  - tooling
---

# Suporte à Atlassian CLI (`acli`) nos comandos `brza install` e `brza doctor`

## O contexto

O `brza` dispõe de comandos para gerenciar o ambiente de desenvolvimento:
- `brza install`: Automatiza a instalação de dependências, binários de suporte e plugins necessários para o ecossistema.
- `brza doctor`: Verifica a integridade da máquina, checando ferramentas instaladas, caminhos de PATH, variáveis de ambiente e estado dos clientes (BrzA Studio / Orca).

Com a incorporação de fluxos baseados na Atlassian CLI (`acli`), desenvolvedores precisam garantir que o binário esteja presente e autenticado corretamente antes de rodar comandos de Jira ou Rovo Dev.

## A proposta

1. **No `brza install`:**
   - Adicionar a opção `brza install acli` (ou incluir na rotina geral de setup).
   - Para macOS: invocar Homebrew (`brew tap atlassian/homebrew-acli && brew install acli`) ou baixar o binário standalone oficial (`https://acli.atlassian.com/darwin/...`).
2. **No `brza doctor`:**
   - Conferir se `acli` está acessível no PATH.
   - Executar checagem de integridade não-interativa do login (`acli jira auth status` e `acli rovodev auth status`).
   - Emitir aviso com orientações amigáveis se o login expirou ou não foi realizado.

## O que conferir na sessão que fizer

- Implementar a detecção em `scripts/brza/brza-doctor` ou módulo equivalente.
- Garantir que `brza doctor` não trave caso a máquina esteja sem conexão com a internet (timeout curto).
- Testar o instalador em macOS local.
