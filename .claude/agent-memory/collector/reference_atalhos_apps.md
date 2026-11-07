---
name: reference-atalhos-apps
description: Onde moram os keybindings reais de BrzA Studio, Orca, Cursor e Antigravity IDE no disco, e buscas que falharam
metadata:
  type: reference
---

- BrzA Studio/Orca: `~/Projects/brza-studio/src/shared/keybindings/definitions-core-{1..4}.ts` (id, title, defaultBindings). Orca.app traz o mesmo em `Orca.app/Contents/Resources/app.asar.unpacked/out/shared/keybindings/*.js` (legível sem extrair o asar; grep no app.asar não acha).
- Antigravity IDE: `Antigravity IDE.app/Contents/Resources/app/extensions/agy/package.json` (contributes.keybindings, legível com python json). Outros atalhos estão em workbench.desktop.main.js como `keybinding:{primary:N}` (N em código numérico do VS Code: 2048 Cmd, 1024 Shift, 512 Alt, KeyA=31).
- Cursor: sem keybindings no disco legível; usar https://cursor.com/docs/configuration/kbd. code.visualstudio.com/docs/reference/default-keybindings lista só parte.
- Não há keybindings.json de usuário em Application Support de Cursor/Antigravity IDE.
- `npx @electron/asar` é barrado pelo classificador de permissão; evitar.
