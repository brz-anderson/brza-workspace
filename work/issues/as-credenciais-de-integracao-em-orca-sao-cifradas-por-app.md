---
status: done
description: Jira, Linear, Bitbucket e chaves de API gravados em ~/.orca são cifrados com o Keychain de cada app, então o BrzA Studio não lê os do Orca e reconectar num app quebra o outro.
scope:
  - brza-studio
opened: 2026-11-02
completed: 2026-11-02
tags:
  - auth
  - infra
---

# As credenciais de integração em `~/.orca` são cifradas por app

Achado independente do `reviewer` e do `collector`, na caçada de achados da v1.4.246, em 2026-11-02, em
`brza-studio@384d4b08fd6`. A decisão de coexistência de 2026-10-27 manteve `~/.orca` compartilhado ("Fica Orca") sem
considerar que a cifra das credenciais é por app. Não se confunde com os restos visuais da Orca da issue
[Os restos da Orca à vista no BrzA Studio](../../../brand/work/issues/os-restos-da-orca-a-vista-no-brza-studio.md):
aqui é estado em disco compartilhado.

## O defeito

**O que grava em `~/.orca`, cifrado pelo `safeStorage` do Electron:** Jira (`jira/site-credential-store.ts:29-42`),
Linear (`linear/linear-credential-paths.ts:8-12`), Bitbucket (`bitbucket/credential-store.ts:49-57`), a chave de OpenAI
speech, o cookie e as chaves do MiniMax, o OpenCode Go e o zcode
(`credentials/encrypted-api-key-file-store.ts:42-47`). No macOS a chave do `safeStorage` é o item `<nome do app> Safe
Storage` do Keychain, e o BrzA se renomeia antes do `ready` (`main-process-preflight.ts:212-213,269`).

**O que está na máquina de Anderson** (só leitura, sem ler segredo):
- `~/.orca/jira-tokens/*.enc`, de 2026-10-24, começa com `v10`, o formato do `safeStorage`, e `jira-sites.json` aponta
  `fixfy.atlassian.net`;
- o Keychain tem `orca Safe Storage`, criado em 2026-10-17, e `BrzA Studio Safe Storage`, criado em 2026-10-28.

**O efeito:**
- O Jira, configurado no Orca, **não funciona no BrzA**: a decifragem falha com `CredentialDecryptionError`
  (`integration-token-file-cache.ts:53-61`; `integration-credential-file.ts:123-150`).
- Reconectar no BrzA regrava o arquivo com a chave dele (`jira/client.ts:119`), e **o Orca perde o Jira**.
- Desconectar num dos dois apaga o arquivo e a entrada do `jira-sites.json` nos dois (`jira/client.ts:138-150`).
- O mesmo vale para as outras credenciais, quando forem usadas.

**Inferido, não rodado no app:** que a falha de decifrar vem da chave do Keychain; é o mecanismo do `safeStorage`, e o
`reviewer` o confere em 90 de confiança.

## O que resolve

- **Uma pasta própria para as credenciais do BrzA** (`~/.brza`, por exemplo), com os hooks de agente em `~/.orca`.
  Custo: uma constante em `brand-identity.ts` e uns 7 caminhos de store (`getOrcaDir()` se repete em ~8 arquivos), mais
  conflito pequeno nos próximos syncs; Anderson reconecta o Jira uma vez no BrzA.
- **Manter compartilhado, e conectar cada integração em só um dos apps.** Custo: nenhum código; a integração fica sem uso
  num dos dois.
- **Voltar a chave do BrzA ao item do Keychain do Orca.** Custo: desfaz a decisão de 2026-10-27, e o que o BrzA gravou
  deixa de ser lido.

## Resolução

Corrigida em 2026-11-02 pelo P75 do PLN-001 (R65.2), em `brza-studio@f7490afab9e`: os stores gravam em `~/.brza`, sem
ler nem apagar o `~/.orca`, e os hooks seguem em `~/.orca`. Falta a conferência no app (o C28, de Anderson): reconectar o
Jira no BrzA e conferir que o Orca segue com o dele.
