---
scope:
  - brza-studio
date: 2026-11-02
tags:
  - auth
  - testing
---

# O P75.5 do PLN-001, o teste das credenciais de uso que a suíte completa pegou

A suíte completa em `origin/master@4bbaecabf18` achou `usage-credentials.test.ts` com 8 de 13 testes vermelhos: passavam
em `ecc4a13d456` e falhavam em `f7490afab9e`, o P75, que levou as credenciais de integração de `~/.orca` para `~/.brza`
sem atualizá-lo (o X83). Na R69.1, Anderson decidiu corrigir o teste antes de avisar a `brand`. A sessão
`pln-001-p75-teste` executou o subpasso 5 do P75 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
com o D58.

## O que decidi para cada teste de "outro app"

- **"never overwrites a MiniMax/GLM key the other BrzA Studio app on this machine sealed, but forgets it"** — ainda
  vale; só o caminho mudou. O "outro app" nunca foi o Orca: é o desktop (safeStorage) e o orcad (chave do host), que não
  abrem o arquivo um do outro (`saved-credential-readability.ts:5`). Os dois são do BrzA e resolvem a pasta pelo mesmo
  `getIntegrationCredentialsDir()`, a partir do `homedir()` (o X71 já dizia que o orcad grava em `~/.brza`). A recusa
  `sealed-elsewhere` segue protegendo uma chave real.
- **"does not blame the other app for a sealed MiniMax/GLM key while this host cannot decrypt at all"** — ainda vale;
  só o caminho mudou. Sem a chave do host carregada, o erro segue `unreadable`, e não "outro app selou", na mesma pasta
  que o desktop e o orcad dividem.

Nenhum dos dois perdeu o sentido, e o P75 não perdeu comportamento: não houve pergunta a Anderson. O que o `~/.orca` do
Orca garante (nada lido, nada apagado) é do `integration-credentials-location.test.ts`, que não mudou.

## O que mudou, em `brza-studio@0efb501da52`

- Só o teste: as 8 ocorrências de `'.orca'` viraram `'.brza'`, com o título do primeiro teste, e uma linha de
  comentário diz quem é o "outro app".
- Três asserções passavam à toa com a pasta nova: o cookie recusado, a chave grande demais e o "storing nothing"
  esperavam que `.orca` não existisse. Foram a `.brza`, onde uma gravação indevida cairia.
- 22 arquivos de teste de credenciais, por caminho → 316 passed, 3 skipped (ACL nativa do Windows); os 13 de
  `usage-credentials.test.ts` verdes. Jira e Linear não têm `credential-store.test.ts`: os stores deles são testados em
  `client.test.ts` e `linear-workspace-registry.test.ts`, que entraram. Nenhum outro teste de credencial esperava
  `.orca`.
- `pnpm tc:node` → exit 0; `pnpm check:changed --base=origin/master --maxWorkers=2` → 22 checks, unit tests inclusive.
  A suíte completa não repetiu (R69.1).
- Push direto na `master` (`4bbaecabf18..0efb501da52`), sem mexer na tag, no app instalado, em `~/.orca`, `~/.brza` ou
  no perfil real.

## Desvios

- **X84.** O `saved-credential-readability.ts:5` ainda diz "in ~/.orca" no comentário do `sealed-elsewhere`. O
  comportamento está certo; o passo só podia mudar teste, e o comentário ficou.

## Próximo

A `brand` gera a v1.4.246-alpha.2 de `0efb501da52`. O C28 segue com Anderson, num build novo.
