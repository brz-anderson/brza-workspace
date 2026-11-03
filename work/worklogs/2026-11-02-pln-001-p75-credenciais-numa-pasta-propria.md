---
scope:
  - brza-studio
tags:
  - auth
  - infra
refs:
  - PLN-001
  - issue:as-credenciais-de-integracao-em-orca-sao-cifradas-por-app
---

# O P75 do PLN-001, as credenciais de integração do BrzA numa pasta própria

O pedido 39, da caçada de achados da v1.4.246, na R65.2 de Anderson: "Pasta própria do BrzA". A sessão
`pln-001-pedido-39-credenciais` executou o P75 do
[PLN-001: O BrzA Studio — o build local, o tema, o visualizador, o Windows e o chat](../../plans/PLN-001-o-brza-studio-generico/PLN-001-plan.md),
com o D58. O achado e o fluxo estão na issue
[As credenciais de integração em `~/.orca` são cifradas por app](../issues/as-credenciais-de-integracao-em-orca-sao-cifradas-por-app.md).

## O que a leitura do D58 confirmou

A lista de stores do D58 se sustentou, sem ficar maior: Jira, Linear, Bitbucket, OpenAI speech, MiniMax (cookie), zcode, e
a fábrica de chave de API que serve o MiniMax e o OpenCode Go. A migração do orcad só deriva os caminhos deles. Os
arquivos de metadado (`jira-sites.json`, `linear-workspaces.json`, `linear-viewer.json`, `bitbucket-credential.json`)
foram com o store, porque deixá-los em `~/.orca` faria o BrzA listar sites do Orca sem token e o "desconectar" mexer nos
dois. Hooks, `keybindings.json` e a raiz da chave do orcad seguem em `~/.orca`. Nada do D58 caiu; não houve pergunta a
Anderson.

## O que mudou, em `brza-studio@f7490afab9e`

- `BRAND_CREDENTIALS_DIR_NAME = '.brza'` em `brand-identity.ts` e o `getIntegrationCredentialsDir()` em
  `credentials/integration-credentials-dir.ts`; os 8 `getOrcaDir()` locais saíram, e os `ensureOrcaDir` viraram
  `ensureCredentialsDir`.
- Sem migração: o arquivo do Orca tem outra chave, e o usuário reconecta uma vez no BrzA.
- Teste novo, `integration-credentials-location.test.ts`: semeia um `~/.orca` com um arquivo de cada store, mostra que
  nenhum store o lê, que os 9 arquivos nascem em `~/.brza` e que, depois de limpar tudo, o `~/.orca` está byte a byte
  como estava. Os 12 testes de store que existiam passaram a esperar `.brza`.
- A frase do diálogo da chave do OpenAI, que dizia `~/.orca`, nas 11 línguas.
- `pnpm tc` e `pnpm tc:node` com exit 0; `pnpm check:code-quality:changed` passou; 79 arquivos de teste dos diretórios
  tocados → 641 passed. Suíte inteira: roda no merge, pela coordenação. Push direto na `master`
  (`ecc4a13d456..f7490afab9e`), sem mexer na tag, no app instalado nem em `~/.orca`, no Keychain ou no perfil real.

## Desvios

- **X71.** A raiz da chave do orcad fica em `~/.orca`, e o orcad remoto também grava as credenciais em `~/.brza`.
- **X72.** A frase do diálogo da chave do OpenAI trocou o caminho nas 11 línguas.
- **X73.** O `pnpm check:changed` não terminou o passo de testes de unidade (o `brand-identity.ts` o espalha por quase
  todo o `src/main`, e passou de 29 min com a máquina cheia); rodei os diretórios por caminho. O `orcad-forked-child-paths`
  falha em 4 testes por `/tmp` contra `/private/tmp` no sandbox, sem relação com o que mudou.

## Próximo

O C28, de Anderson, num build novo: conectar o Jira no BrzA e abrir a integração no Orca. Como o `~/.brza` está vazio, o
BrzA começa sem o Jira, e o Orca segue com o dele. Não rodei o app, e o C28 segue em aberto.
