---
name: reference-brza-studio-brand-assets
description: Onde moram os ativos de marca no brza-studio e no CLI brza, e as fontes que enganam (planos e README descrevem arquivo trocado)
metadata:
  type: reference
---

Mapa para levantamentos de marca (PLN-007, workstream `brand`), conferido em 2026-10-31.

- **Ícone**: `brza-studio/resources/build/{icon.icns,icon.ico,icon.png}` (buildResources em `config/electron-builder.config.cjs:257`), `resources/icon.png`/`icon-dev.png` (256), `resources/app-icons/orca-*.png` (arte BrzA, nome Orca), `resources/tray/orca-menu-barTemplate*.png`.
- **Marca na UI**: `resources/logo.svg` (PNG branco embrulhado, 391x512) é importado em 5 componentes (Titlebar, Landing, Onboarding, HelpMenu, settings icon); `resources/brza-flame-mono.svg` é o único vetor da chama (traçado, 24x24).
- **Fonte que engana**: `resources/icon-source/icon.icon/Assets/logo.svg` é a cauda da Orca em vetor (Inkscape), NÃO o PNG embrulhado — o texto do PLN-007 troca os dois. `generate.sh` regeneraria o ícone da Orca; o b2918da não passou por ele nem tocou `icon-source/`.
- **Tipografia/cor**: `src/renderer/src/assets/main.css` (Geist em `:14`, tokens cinza shadcn em `:192-365`); sem acento de marca; único hex de marca escrito é `F26B1D` no `README.md:11`.
- **Orca visível**: mobile inteiro (`mobile/app.json`, `OrcaLogo.tsx`), `src/renderer/index.html:9` e outros HTML, helpers do `.app` (`Orca Computer Use`, `Orca Terminal Host`), `brza --help` (`src/cli/root-help-text-primary.ts:2-4`), links `onorca.dev`, `docs/` quase todo.
- **CLI `brza` do workspace** (`brza-workspace/scripts/brza/*`): argparse em PT-BR, sem banner nem marca; o `brza` do app é o CLI da Orca renomeado.

Atalhos: contar "Orca" em `en.json` só vale com Python (`walk` sobre valores); `find` recursivo em `~/Desktop`/`~/Downloads` trava (>120 s) — use `mdfind`. `qlmanage`/`sips` não rendem SVG bem; use `rsvg-convert` e `magick` (ambos em /opt/homebrew/bin). `/private/tmp/pln-007` é o scratch da sessão, pode redirecionar para o chat-scratch do Studio.
