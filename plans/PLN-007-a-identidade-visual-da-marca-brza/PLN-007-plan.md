---
status: open
phase: interview
origin: request
ready: não — faltam a entrevista, o Desenho e os Passos
scope:
  - brza-studio
  - workspace
opened: 2026-10-31
owner: Anderson
tags:
  - design
---

# PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app

- **Retomar:** R1 fechada na sessão do `workspace`; o levantamento de onde a marca aparece está em curso. Próximo: a R2,
  com as referências, a arquitetura mãe e filhas, o destino do símbolo e quem produz o vetor.

## Pedido

- **Origem:** pedido livre, na sessão do workstream `workspace` de 2026-10-31, que respondeu a R1 e abriu o
  workstream `brand`; o plano é aberto na sessão do `brand` no mesmo dia.

> "Vamos planejar a identidade visual da marca `BrzA`, partindo do ícone do app para montar a logo."

### Cobertura

> Rascunho da abertura: os critérios são propostas e se fecham no Planejar, com o passo e o teste.

| Origem     | Critério de aceite                                                                                     | Passo | Teste (nível)                         |
| :--------- | :----------------------------------------------------------------------------------------------------- | :---- | :------------------------------------ |
| `Pedido 1` | O símbolo BrzA existe em vetor de verdade, com paths, derivado da chama do ícone atual                  | —     | abrir o SVG e conferir os paths (manual) |
| `Pedido 1` | O logotipo BrzA existe em vetor, com o símbolo e a palavra, nos arranjos decididos                      | —     | conferência dos artboards (manual)    |
| `R1.2`     | BrzA Studio, o CLI `brza` e o workspace têm cada um a derivada da marca-mãe                             | —     | conferência dos artboards (manual)    |
| `R1.2`     | A paleta e a tipografia estão fixadas com os valores, e os pontos em que a marca aparece as usam        | —     | conferência no app (manual)           |
| `Pedido 1` | O ícone do app sai da mesma fonte vetorial que o símbolo, pelo `generate.sh`                            | —     | `resources/icon-source/generate.sh` (manual) |

### Fora de escopo

- **Aplicar a marca no código do `brza-studio`.** Cada aplicação é passo de código, executado numa sessão do
  `brza-studio`, na branch `<tipo>/pln-007-<slug>`; aqui fica o pedido.

## Entrevista

### Rodada 1 — workstream, alcance e destino (enviada 2026-10-31)

**Apresentado antes**, na sessão do workstream `workspace`:
- O ícone atual veio do rebrand de 2026-10-27, `brza-studio@b2918da` ("New flame icon: full artwork from 128 px up,
  the flame alone below that, a light variant, a dev badge, a monochrome tray template and title-bar mark"): uma chama
  laranja e vermelha em degradê com um grafo de commits por dentro, um `>_`, um `{}` e faíscas, sobre um quadrado
  grafite com borda laranja (`brza-studio/resources/icon.png`, 256 px). O de dev, `resources/icon-dev.png`, leva um
  selo azul "D".
- Não há fonte vetorial do ícone: o `resources/icon-source/icon.icon/Assets/logo.svg` é um PNG de 391×512 (a chama
  branca chapada) dentro de um `<image>` de SVG; o `icon.json` do Icon Composer fica ao lado, e o
  `resources/icon-source/generate.sh` gera o `.icns` e os PNGs.
- O seletor de ícone, em `src/shared/app-icon.ts:1`, oferece "Flame" (classic), "BrzA Studio ADE" (watercolor) e
  "Light Flame" (blue), mas os arquivos de `resources/app-icons/` seguem `orca-blue.png` e `orca-watercolor.png`.
- Nenhum workstream tem plano ou nota de marca.

Respondida em 2026-10-31, na sessão do workstream `workspace`.

1. **Workstream do plano.** Opções: `studio` (recomendada), workstream novo `brand`, `workspace`.

   **Decidido — "Workstream novo `brand`".** O `workstream/brand` foi criado pelo `brza note workstream brand` na
   mesma sessão.

2. **Alcance.** Opções: o guarda-chuva BrzA (recomendada) e as outras apresentadas na sessão do `workspace`.

   **Decidido — "Guarda-chuva BrzA (Recomendado)"**: uma marca-mãe BrzA, com símbolo e logotipo, e as derivadas BrzA
   Studio, o CLI `brza` e o workspace.

3. **Destino.** Opções: `PLN` (recomendada) e as outras apresentadas na sessão do `workspace`.

   **Decidido — "PLN (Recomendado)"**, o `PLN-007`.

As opções completas e os custos da R1 ficaram na sessão do `workspace`; aqui está o que chegou no pedido.

## Worklogs

- 2026-10-31 — aberto; R1 gravada como chegou da sessão do `workspace`.
  [PLN-007: a abertura da marca BrzA](../../work/worklogs/2026-10-31-pln-007-a-abertura-da-marca-brza.md)
