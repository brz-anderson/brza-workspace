---
name: ferramental-vetor-e-fonte
description: Com que ferramenta instalada se converte texto da Geist woff2 em path e se renderiza SVG nesta máquina (PLN-007, 2026-11-02)
metadata:
  type: reference
---

Texto da Geist (`brza-studio/src/renderer/src/assets/fonts/Geist-Variable.woff2`) em path: **o CoreText pelo
`swift`** (`CTFontManagerCreateFontDescriptorsFromData` + `kCTFontVariationAttribute` com `wght`), que lê o woff2 e
aplica o peso. Não servem, sem instalar nada: o `opentype.js` 2.0.0 do `node_modules` (pede decompressor de WOFF2), o
`hb-view` (não carrega o woff2), o `fontTools` e o `brotli` do Python (ausentes).

Render de SVG: `rsvg-convert`, `magick`, `iconutil`, `sips`. Ausentes em 2026-11-02: `inkscape`, `potrace`, `vtracer`,
`svgo`.

Custo que eu teria estimado errado: o pedido supunha o `opentype.js` como caminho; sem medir, o passo dos lockups
teria saído com uma ferramenta que falha. Meça a ferramenta antes de pôr o custo na opção.
