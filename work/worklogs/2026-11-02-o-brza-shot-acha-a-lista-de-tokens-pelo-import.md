---
scope:
  - workspace
---

# O brza shot acha a lista de tokens pelo import do shell dos visuais

Pedido da sessão `brand-24`, a pedido de Anderson, em 2026-11-02, pela issue `work/issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md`, do workstream `brand`: o merge do upstream v1.4.246 no `brza-studio` moveu o `PANEL_DESIGN_TOKEN_ALLOWLIST` para `src/shared/plugins/frames/plugin-panel-design-tokens.ts`, e todo `brza shot` saía com "não li o shell dos visuais no brza-studio".

## O que se fez

- **`scripts/brza/brza-shot`:** o `PANEL_SHELL` fixo saiu. O `find_token_list` lê o `native-chat-visual-shell.ts`, acha o `import`/`export … from` relativo da lista e segue os reexports (até 6) até a definição. Também aceita a lista definida no próprio shell. Se não resolve, o erro diz o arquivo, o especificador e os caminhos tentados.
- **`scripts/brza/tests/test_brza_shot.py`:** aproveitado o começo da sessão anterior (o `fake_studio` com a lista fora do caminho antigo), com quatro testes: reexport, lista no próprio shell, import que não resolve e import ausente.
- **Commit na `master`:** `8d554e7`.

## A conferência

- Contra o código velho, o teste novo falha (3 falhas e 5 erros em `test_brza_shot`); com o conserto, os 98 `unittest` de `scripts/brza/tests/` passam.
- No app de verdade, `brza shot` de um artboard simples gerou o PNG (1472×160 px).
- O `brza-studio` não foi tocado.

## Retomar

A issue mora no `brand`; quem a fecha é a sessão `brand-24`.
