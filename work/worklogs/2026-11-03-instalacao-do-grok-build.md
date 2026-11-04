---
scope:
  - workspace
---

# Instalação do Grok Build, o agente de terminal da xAI

O pedido de Anderson, em 2026-11-03, na sessão `tools-kit-produtividade`: "homebrew install grok".

## O que se fez

- **O `grok` do Homebrew não era o da xAI.** A fórmula `grok` é o utilitário de regex do jordansissel, descontinuado
  e com remoção marcada para 2027-01-11 (`brew info grok`). O comando `grok` da xAI vem do cask `grok-build`, "Extensible
  coding agent for the terminal"; o `grok-bot` é outro produto, de "AI teammates" entre apps.
- **Instalado o `grok-build` 1.0.70**, pelo `brew install --cask grok-build`: `grok --version` → `grok 1.0.70
  (f50904eaee6c)`. Antes, `which agent` não achou nada, e o binário `agent` do cask entrou sem conflito.

## Fora do workspace

- **O quê e onde:** o cask `grok-build` 1.0.70, com os binários `/opt/homebrew/bin/grok` e `/opt/homebrew/bin/agent`.
  **Risco:** o nome genérico `agent` pode sombrear um `agent` instalado depois, mais adiante no `PATH`. **Estado:**
  ativo. **Como desfazer:** `brew uninstall --cask grok-build`.
