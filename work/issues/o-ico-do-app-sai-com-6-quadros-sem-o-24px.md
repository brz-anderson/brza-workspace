---
status: open
description: O `.ico` do app saiu do pipeline novo com 6 quadros, sem o de 24 px que o arquivo antigo tinha; acrescentar o 24 é editar script e teste do upstream.
scope:
  - brza-studio
opened: 2026-11-02
priority: low
tags:
  - design
---

# O .ico do app sai com 6 quadros, sem o de 24 px

O `resources/build/icon.ico` que o `generate.sh` gera depois do P4 do
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md)
tem 6 quadros: 256, 128, 64, 48, 32 e 16 px, pelo `ICO_FRAME_SIZES` do `config/scripts/trim-windows-icon-source.mjs`. O
arquivo que estava commitado antes tinha 7, com o de 24 px, e vinha de um pipeline antigo, do ImageMagick. O plano
esperava 7, porque a conta saiu do arquivo commitado, e não do script, que já emitia 6.

O 24 px é o tamanho do ícone pequeno da barra de tarefas do Windows a 150% de escala; sem ele o Windows escala o de 32
ou o de 16, e pode borrar. O efeito não foi visto: o app não foi aberto no Windows.

## O pedido

Decidir se o `.ico` ganha o quadro de 24 px.

- **Acrescentar o 24 ao `ICO_FRAME_SIZES`** e atualizar o teste do script. Custo: editar um script e um teste do upstream, que
  entram nos merges do próximo sync; ~0,25 h, não medido. Se paga: no C7 do plano, ao ver a barra de tarefas do Windows a 150%.
- **Deixar com 6.** Custo: nenhum agora. Se paga: se o C7 não mostrar diferença.

Anderson decide, de preferência depois de ver o Windows.
