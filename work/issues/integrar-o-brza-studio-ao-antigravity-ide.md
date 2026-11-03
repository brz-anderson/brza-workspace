---
status: open
scope:
  - brza-studio
  - workspace
opened: 2026-11-03
owner: Anderson
description: Abrir arquivo na linha e sessão do agente do Antigravity IDE a partir do BrzA Studio e do brza, pela extensão-ponte provada em 2026-11-03.
tags:
  - tooling
---

# Integrar o BrzA Studio ao Antigravity IDE

## O pedido

Anderson quer clicar num arquivo de código (`.dart`, `.java`) no BrzA Studio e abri-lo no Antigravity IDE, e abrir
sessões no agente do Antigravity pelo `brza`. O levantamento e a prova estão no
[worklog de 2026-11-03](../worklogs/2026-11-03-a-ponte-do-brza-studio-para-o-antigravity.md).

Em resumo: o `antigravity-ide chat` não chega ao agente; o caminho é uma extensão-ponte com URI handler que chama o
`antigravity.sendPromptToAgentPanel`. Abrir arquivo na linha não precisa da ponte: `antigravity-ide -r -g
arquivo:linha` basta.

## O que falta

1. **Conferir a prova:** com a ponte instalada, ver no painel "Main Agent" se o prompt de teste foi enviado e
   respondido, ou só ficou na caixa. Se ficou na caixa, achar no `workbench.desktop.main.js` o comando ou parâmetro que
   envia; se nada apareceu, repetir com `new=0` ou `delay` maior.
2. **Abrir o PLN no workstream `app`**, numa sessão nova no worktree dele — Anderson escolheu "Plano no workstream
   app" na rodada de 2026-11-03. O escopo de partida:
   - preset "Antigravity" no catálogo do "Open in", com o comando `antigravity-ide`;
   - ação "Abrir em <editor>" no popover do link de arquivo, que roda `<comando> -r -g arquivo:linha:coluna`, para
     todo fork do VS Code;
   - opcional: configuração para o clique simples abrir direto no editor externo;
   - a ponte versionada, com instalação pelo `brza`, e um subcomando do `brza` que abre sessão no agente pela URL.
3. **Decidir onde a ponte mora** e o que ela aceita de quem chama, porque hoje qualquer URL `antigravity-ide://` local
   manda prompt ao agente.
