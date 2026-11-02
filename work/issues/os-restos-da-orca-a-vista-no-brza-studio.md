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
- **A cauda da Orca no `icon.json`:** o `resources/icon-source/icon.icon`, o projeto do Icon Composer, segue apontando
  para a arte da Orca. O P4 do PLN-007 deixou de lê-lo e o `generate.sh` renderiza dos SVG de `resources/brand/`, então
  o arquivo fica intocado e sem uso.
- **Os nomes `orca-*` dos arquivos de ícone:** `resources/app-icons/orca-watercolor.png` e `orca-blue.png`
  (`src/main/app-icon.ts:8-25`) e `resources/tray/orca-menu-barTemplate.png` e `@2x` (`src/main/tray/system-tray.ts:2-3`).
  Ficam com o nome, porque renomear toca os imports do upstream; o conteúdo já é BrzA.
- **O que parece resto e fica:** o pareamento `orca://pair` é mantido de propósito (`src/shared/brand-identity.ts:14`).

Os restos fora do mobile foram estimados em ~3–6 h na R3.4, e muitos são identificadores de build, com risco de conflito
nos merges do `stablyai/orca`. Se paga quando houver outro usuário além de Anderson.

## O que o sistema de plugins da 1.4.246 acrescenta

O levantamento de 2026-11-02 (ver
[Os plugins da Orca 1.4.246 e o que mudam nos planos](../worklogs/2026-11-02-os-plugins-da-orca-1-4-246-e-os-planos.md))
achou mais restos, e mediu as chamadas externas no app instalado (`1.4.246-alpha.1`):

- **As mensagens do CLI** (`nextSteps` do `plugin create` e afins) ainda dizem `orca plugin …`; o guia de plugin embarcado
  (`src/main/…/bundled-skill-guides.ts`) e a URL do `$schema` apontam para a Orca. O formato (`orca-plugin.json`,
  `orca-catalog.json`, módulos `orca`, `engines.orca`) **não se troca**: quebraria o ecossistema.
- **Os catálogos oficial e da comunidade** são repositórios Git da `stablyai`, visíveis por padrão em Configurações.
- **O `kill-list.json` e o `stats.json` de `onorca.dev`:** o app empacotado busca o primeiro a cada 6 h (15 min no retry) e
  o segundo só empacotado (`main-process-plugins.ts:67`). São GET com `credentials: 'omit'`, sem corpo. O `kill-list` é a
  revogação de plugin malicioso, e vale manter; o `stats` só alimenta a contagem de instalações.
- **A telemetria `plugin_installed` está desligada no nosso build:** o `client.ts` só transmite com a identidade de build
  (`stable`|`rc`) e a chave PostHog, que só o CI oficial injeta; o `app.asar` instalado não tem nenhuma chave `phc_`. Fica
  desligada enquanto o CI do fork não definir o `ORCA_POSTHOG_WRITE_KEY` (o `release-mac-build.yml:189` já o lê de
  `secrets`; não confirmei se o segredo existe no repositório).

**Não medi:** o tráfego de rede ao vivo (nenhuma conexão aberta no momento da conferência; o `kill-list` só roda a cada 6 h)
nem o comportamento do catálogo offline.
