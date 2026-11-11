# Os pacotes de tokens

Um pacote é o JSON com os tokens visuais de um projeto, em `scripts/packs/<projeto>.json`, extraído do código do próprio
projeto. Ele existe para que todo artboard do projeto use as mesmas cores, raios e fontes do app, e para que a mudança no
código apareça como deriva, e não como um artboard que mente.

## Os nomes

O fragmento lê só `var(--sa-*)`. Os nomes são os 26 que o chat do Orca expõe, com o prefixo `--sa-` (de *screen
artboard*), para nunca colidir com os do chat:

`--sa-background`, `--sa-foreground`, `--sa-card`, `--sa-card-foreground`, `--sa-popover`, `--sa-popover-foreground`,
`--sa-primary`, `--sa-primary-foreground`, `--sa-secondary`, `--sa-secondary-foreground`, `--sa-muted`,
`--sa-muted-foreground`, `--sa-accent`, `--sa-accent-foreground`, `--sa-destructive`, `--sa-destructive-foreground`,
`--sa-border`, `--sa-input`, `--sa-ring`, `--sa-radius`, `--sa-font-sans`, `--sa-font-mono`, `--sa-chart-1` a
`--sa-chart-5`.

Os tokens do projeto que não têm par nessa lista entram com o nome do projeto, sem o `--` de origem: o `--sidebar` do
`main.css` vira `--sa-sidebar`. **Todos os tokens do mobile entram com `--sa-m-`** (`--sa-m-bg-panel`), e o pacote guarda o
mapa `mobile_pairs` (`m-bg-base` → `background`, `m-text-primary` → `foreground`…): nas molduras `iphone` e `android`, o
`new` sobrescreve o token do desktop pelo par do mobile, e o fragmento escrito com `var(--sa-background)` sai com a cor do
app mobile sem mudar uma linha. `tokens.py list`
imprime os nomes de cada pacote. O prefixo é a decisão da PLN-021/R5.9.

## O pacote `brza-studio`

| Fonte | O que se lê |
| :-- | :-- |
| `~/Projects/brza-studio/src/renderer/src/assets/main.css` | os blocos `:root` (claro) e `.dark` (escuro): cores, `--radius`, `--chart-*`, fontes |
| `~/Projects/brza-studio/mobile/src/theme/mobile-theme.ts` | `lightColors`, `darkColors`, `spacing`, `radii`, `typography` |

O `mobile-theme.ts` diz na primeira linha que espelha o `main.css`; onde os dois divergem, o desktop vale para os
artboards de desktop e web, e o mobile para os de iPhone e Android.

```bash
python3 -I .claude/skills/screen-artboards/scripts/tokens.py extract brza-studio
python3 -I .claude/skills/screen-artboards/scripts/tokens.py check brza-studio
```

- **`extract`** lê as fontes por regex (sem Node), grava o JSON com o `sha256` de cada fonte e a data. Rode depois de uma
  mudança de tema no app, e commite o pacote: ele é o registro de que cor o artboard usou.
- **`check`** compara o hash; se a fonte mudou, extrai de novo em memória e imprime os tokens que mudaram
  ("⚠ deriva: main.css mudou desde 2026-11-10 — 3 tokens: --primary, --ring, --chart-2; rode tokens.py extract
  brza-studio"). Saída 4 só quando um token mudou; a fonte que mudou sem mexer em token sai 0 com a nota "mudou, mas
  nenhum token" (o `main.css` muda toda semana por outros motivos). Saída 1 com fonte ausente. O `artboard.py new` roda o `check` sozinho e só
  avisa.

## O pacote `neutral`

Cinzas e um acento azul, nos mesmos nomes, claro e escuro. Para wireframe — quando a escolha é de estrutura e a cor
distrai — e para projeto que ainda não tem pacote.

## Projeto novo

`tokens.py extract <projeto> --src <arquivo css>` lê o `:root` e o `.dark` (ou `[data-theme=dark]`) de um CSS e grava
`packs/<projeto>.json` com os nomes que tiverem par; o resto entra com `--sa-` mais o nome de origem. Confira o
`tokens.py list` (lista todos os pacotes) e um artboard de teste pelo PNG antes de usá-lo numa rodada.
