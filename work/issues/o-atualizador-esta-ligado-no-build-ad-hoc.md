---
status: open
description: O atualizador do app instalado (1.4.246-alpha.1, ad hoc) está ligado e aponta ao fork, que não publica o manifesto; e o onorca.dev decide quando ele consulta o feed.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - release
---

# O atualizador está ligado no build ad hoc, sem manifesto para ler

Achado do `collector` na caçada de achados da v1.4.246, em 2026-11-02, em `brza-studio@384d4b08fd6`. A nota do release da
`v1.4.246-alpha.1` diz que os builds "não se atualizam sozinhos", e o código diz o contrário.

## O que prova

- **A guarda só reconhece o sufixo `-local.<ts>.<commit>`** (`src/main/updater/updater-enabled.ts:4-9`). O app instalado
  é `1.4.246-alpha.1`, sem o sufixo, então o atualizador liga. **Provado em runtime:** o breadcrumb
  `updater_macos_installer_scheduling_configured` está no log do app (`macos-shipit-scheduling.ts:32`, chamado depois da
  guarda em `updater-setup.ts:141-146`).
- **O feed aponta ao fork, e não ao upstream** (`updater-setup.ts:161-166`, `electron-builder.config.cjs:775-781`, e o
  `app-update.yml` do bundle).
- **O fork não publica o manifesto:** `releases/latest/download/latest-mac.yml` devolve 404; nenhum release tem
  `latest-mac.yml` nem zip, e a tag `v1.4.246-alpha.1` não tem release (`gh release list/view`).
- **O `onorca.dev` comanda o momento da checagem:** o nudge faz GET periódico ao site da Orca e o JSON de lá decide
  quando o BrzA consulta o próprio feed, além de mostrar os cards de changelog da Orca (`updater-nudge.ts:12`,
  `updater/updater-nudge.ts:9-44`, `updater-changelog.ts:13,32`). Isso é diferente do link a `onorca.dev` que a issue dos
  restos da Orca registra, e some se o atualizador for desligado.

**Inferido, não rodado:** que, com um manifesto publicado, o app ofereceria o update e a instalação falharia na
assinatura, porque o bundle é ad hoc (`Signature=adhoc`, `TeamIdentifier=not set`, `hardenedRuntime` e `notarize`
desligados em `electron-builder.config.cjs:84-87,613,622-629`). Confiança do `collector`: 65 a 72.

## O que resolve

Decisão de Anderson, porque mexe numa guarda do upstream:
- **Desligar o atualizador no build ad hoc**, ampliando a guarda (o sufixo de versão, ou o `Signature=adhoc`). Custo: um
  conflito pequeno no próximo sync. Se paga: antes de qualquer release com manifesto.
- **Publicar o manifesto e assinar com identidade local estável** (`CSC_NAME` já é aceito). Custo: o fluxo de release e a
  conta de desenvolvedor para notarizar. Se paga: quando houver outro usuário além de Anderson.
- **Deixar.** Custo: nenhum agora, e o app tenta checar um feed que dá 404. Se paga: nunca, se nenhum release com
  manifesto sair.

## Resolução

Anderson decidiu **desligar o atualizador no build ad hoc** (R65.3 do PLN-001), e o P76 o fez em
`brza-studio@cdce032d264`: o `afterPack` do darwin estampa o arquivo `ad-hoc-signed` em `Resources` quando a identidade
de assinatura é `-`, e o `isUpdaterEnabled()` fica falso quando o app o lê. Um build com identidade nomeada (`CSC_NAME`) ou
de release não tem o marcador, e o atualizador dele liga. O nudge a `onorca.dev` e o `fetchChangelog` já ficavam atrás da
mesma guarda. Testado em unidade; **o marcador só se prova no bundle empacotado**, e o app instalado
(`1.4.246-alpha.1`) não o tem, então o atualizador dele segue ligado até o build novo. O `status` fica `open` até o C29,
de Anderson, no build novo: sem o breadcrumb `updater_macos_installer_scheduling_configured` no log e sem GET a
`onorca.dev`.

