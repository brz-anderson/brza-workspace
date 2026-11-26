---
name: brza-studio-mobile-web-eager-budget
description: Como medir o estouro do orçamento eager do pacote web do mobile (verify-mobile-web-app-bundle) e por que carga sob demanda de código não ajuda
metadata:
  type: project
---

O `verify-mobile-web-app-bundle.mjs` conta como eager TODO o código (rotas e chunks lazy inclusos); só fontes aprovadas, catálogos de locale e as imagens de outfit sob demanda ficam fora. Carregar código do fork sob demanda NÃO reduz o eager: só corta bytes tirar o código ou subir `MOBILE_WEB_APP_BUNDLE_MAX_EAGER_BYTES` (11 MiB no upstream, com ~4 KB de folga na v1.4.278).

**Medir sem rodar o build inteiro:** script .mjs que importa `buildMobileWebAppScripts` de `config/scripts/build/mobile-web-app/build-mobile-web-app-bundle.mjs` e `collectMobileWebAppRoutes` de `config/scripts/mobile-web-app/mobile-web-app-route-manifest.mjs` (caminhos diferentes!), chama com `collectMobileWebAppRoutes(<raiz>/mobile/app)` e soma `metafile.outputs[*].inputs[*].bytesInOutput` por input; rode no worktree do fork e no da tag e subtraia. Os `orca-route-entry:` mudam de nome por caminho do worktree (ruído, soma ~0); `locales/*.json` são catálogos (fora do eager).

**v1.4.278:** o fork soma ~16 KB; ~11,4 KB são `src/shared/native-chat/tools/brza/*` (títulos/categorias de tool: git, gh, test, atlassian, figma), mais ~1,3 KB de ícones lucide novos, ~0,6 KB de glifos e peer sender, resto é rebrand e a prévia do Pensou.

**Why:** a feature do fork é síncrona no render da linha de tool, sem alavanca barata.
**How to apply:** no próximo estouro, repetir a medição e levar a rodada (subir o orçamento no fork vs. tirar o brza/tools do mobile), em vez de procurar import a adiar.
