---
status: open
scope:
  - brza-studio
opened: 2026-10-31
tags:
  - design
---

# Os restos da Orca à vista no BrzA Studio

O que ainda mostra o nome ou a arte da Orca a quem usa o BrzA Studio, e que o
[PLN-007: A marca BrzA tem símbolo, logotipo e derivadas a partir da chama do app](../../plans/PLN-007-a-identidade-visual-da-marca-brza/PLN-007-plan.md)
deixou de fora na R3.4, respondida em 2026-10-31 na sessão do `brand`: a marca entra no app desktop, no CLI e nos
READMEs; o mobile e estes restos ficam aqui.

O levantamento é o do `collector` para a R2 do plano, com as fontes no `brza-studio` de 2026-10-31:

- **O app mobile, inteiro:** o `mobile/app.json:3-18,77` (nome "Orca", slug, scheme `orca`, bundle
  `com.stably.orca.mobile`), os ícones e o splash com a cauda da Orca, o `mobile/src/components/OrcaLogo.tsx` (usado em
  `about-screen.tsx` e `MobileHomeTopBar.tsx`) e 103 strings com "Orca" em `mobile/src` e `mobile/app`. Estimado em
  ~4–8 h, sem medir; se paga quando o mobile entrar no uso.
- **Os helpers do `.app`:** `Orca Computer Use.app` e `Orca Terminal Host.app`, com os textos de permissão de
  Acessibilidade e Gravação de Tela dizendo "Orca", e os binários `orca-*` em `MacOS/`.
- **Os títulos dos HTML:** `index.html:9`, `popout.html:5`, `web-index.html:6`, `space.html:5`.
- **Os pacotes Linux:** `orca-ide` no `config/electron-builder.config.cjs:683,726,746`, e os lançadores `orca`,
  `orca-ide` e `orca.cmd` empacotados ao lado do `brza`.
- **Os links ao site da Orca:** `onorca.dev` e `app.orca.dev`, em `SidebarSettingsHelpMenu.tsx:48-49` e outros 5
  arquivos.
- **O que parece resto e fica:** o pareamento `orca://pair` é mantido de propósito (`src/shared/brand-identity.ts:14`).

Os restos fora do mobile foram estimados em ~3–6 h na R3.4, e muitos são identificadores de build, com risco de conflito
nos merges do `stablyai/orca`. Se paga quando houver outro usuário além de Anderson.
