---
name: brza-studio-contrast-review
description: Auditoria de contraste sobre HEX cru engana no chat do brza-studio, que renderiza por color-mix e estilo inline; e o que conferir nas contas de cor
metadata:
  type: project
---

Auditorias de cor das reuniões e planos medem o HEX do token sobre fundos opacos. O chat do `brza-studio` não pinta
assim, e o par renderizado sai pior que o medido:

- **Texto e placeholder são `color-mix`** da cor de origem com o canvas. No `.dark`, o faint fica em 83%. O corpo
  segue o controle de contraste do usuário, de 50 a 150, que vira um mix de 56% a 100%.
- **A segunda camada de tema é estilo inline na raiz do chat.** Folha de estilo "importada depois" não vence o inline
  em `--primary`, `--accent`, `--border` e `--ring`.
- **O BrzA Dark Theme passa pelo ramo de catálogo**, e não pelo padrão.

Antes de citar qualquer caminho daqui, confira no código: são de 2026-11-07, HEAD `8abbde720ce`.

**Why:** foi o achado de maior gravidade na revisão do plano Carvão em Brasa. O placeholder medido a 4,79 renderizava
cerca de 4,08 no 02.
**How to apply:** em plano de cor ou tema do app, peça o par efetivo (mix, controle de contraste, temas do catálogo,
inline) antes de aceitar "medido". Marque com premissa (85) quando o caminho do token não estiver escrito.

**Erro meu, que a coordenação pegou:** o mix do chat é feito com o **canvas**, e só depois a cor é pintada sobre o 02
ou o hover. Eu tinha misturado com o 02: dei 4,45 onde o certo era 4,01. Antes de devolver a conta, confira a base do
mix no `main.css`.

**Contas de cor:**

- Escreva a sua implementação, e não rode só o script da persona. Valide o CIEDE2000 nos pares de Sharma.
- O Machado 2009 de severidade 1 vai em RGB linear, com clipping.
- WCAG e APCA discordam na 07 (`#FF3D00`). Rótulo escuro: 4,85 e Lc 40,9. Rótulo branco: 3,55 e Lc −66,7. Isso é
  escolha de norma, e não teste de render.
