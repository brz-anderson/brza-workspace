---
scope:
  - brza-studio
date: 2026-10-27
tags:
  - release
---

# O BrzA Studio passa a conviver com o Orca original

Sessão `brza-studio-rebrand`, no `brza-studio`, de 2026-10-27 a 2026-10-28. O pedido veio da sessão `fixfy-35` do
workspace da Fixfy, gravado em `/private/tmp/claude-501/brza-studio-pedido.md`: terminar o rebrand para o BrzA Studio
rodar ao lado do Orca do site (`com.stablyai.orca`), com "Estado isolado + marca visível", comando `brza`, migração
"Começar limpo" e o dev separado do dev do Orca. O levantamento das colisões estava em
`/private/tmp/claude-501/brza-studio-colisoes.md`. Este worklog vem para cá, e não para a Fixfy, pela rodada R32 do
PLN-001 e pelo aviso da `fixfy-9b`.

## O que foi feito

- **Commit `de3fb921ad1`** na `master` do `brza-studio` ("feat: let BrzA Studio run side by side with upstream Orca"),
  depois de rebase sobre `41a0df162aa`. Os valores próprios do fork estão num módulo novo,
  `src/shared/brand-identity.ts`, e cada arquivo do upstream muda em poucas linhas.
- **Estado.**
  - A `userData` empacotada fica em `<appData>/brza-studio`, com `setPath` antes de qualquer leitura, também no Windows.
  - O dev usa `brza-dev` e `brza-dev-wt`, longe do `orca-dev` e do `orca-dev-wt`.
  - O app empacotado se renomeia antes do ready, e o Keychain passa a `BrzA Studio Safe Storage`.
  - O `extraMetadata.name: 'brza-studio'` do electron-builder tira do `orca` três coisas: o nome padrão do Electron, o
    cache do updater (`brza-studio-updater`) e a pasta de instalação por usuário no Windows. Esta última era a mesma do
    Orca, um achado fora do levantamento.
- **Cópias fixas do nome.** Passam a seguir a constante:
  - o CLI;
  - os hooks do Codex;
  - a coordenação de bundle;
  - os logs de host Node;
  - os scripts de dev;
  - os logs do serve.

  O script compartilhado do Command Code passou a varrer também os perfis do BrzA Studio.
- **Nomes.**
  - O executável vira `BrzA Studio`, e o bundle de mac, que até o alpha.1 se chamava `Orca.app`, vira
    `BrzA Studio.app`. O launcher de mac e o launcher nativo do Windows acompanham.
  - O comando é `brza`: `/usr/local/bin/brza` no mac e `brza.exe` no PATH do usuário no Windows.
  - O esquema é `brza-studio://`. O pareamento segue emitindo `orca://pair`.
  - A porta WS padrão é 6868, e a do dev, 6869.
- **NSIS.** O desinstalador mata processos e apaga pastas pelo caminho do próprio app: `$INSTDIR` e
  `%LOCALAPPDATA%\BrzA Studio`. Sem PowerShell, o fallback é o nome da imagem, agora exclusivo. O
  `orca-terminal-daemon.exe` e o `%LOCALAPPDATA%\Orca` saíram.
- **De carona.**
  - O título "ORCA" da tela inicial vira BrzA Studio nos 7 locales; o achado foi da sessão
    `brza-studio-itens-do-orca-fixfy`.
  - Dois testes quebrados desde o rebrand anterior, o label do serve e o texto "non-Orca", foram corrigidos.
  - Um teste novo trava a sincronia entre o `electron-builder.config.cjs` e o `brand-identity.ts`.
- **Testes.** Typecheck, lint e formato passam.
  - Nos 125 arquivos dos caminhos tocados, 1.485 testes passam e um falha: "sanitizes node env…macOS launcher".
  - Esse teste falha igual na `master` limpa, porque o `/tmp` do macOS resolve para `/private/tmp`.
  - Outros 221 arquivos que citam os nomes trocados foram rodados no rebrand e na `master` limpa. O rebrand não trouxe
    falha nova.
- **Build.** O `pnpm run build:mac --dmg` saiu do `de3fb921ad1`, na versão
  `1.4.242-alpha.1.local.1793156342359.de3fb921ad16`. A conferência no bundle confirmou:
  - o executável `BrzA Studio`;
  - `bin/brza` e `bin/orca`;
  - o esquema `brza-studio`;
  - o `name` `brza-studio` na asar;
  - a assinatura ad hoc válida.

  A pedido de Anderson, o app foi instalado em `/Applications/BrzA Studio.app`.

## O que Anderson decidiu (rodada desta sessão, 2026-10-27)

| Pergunta | Resposta |
| :-- | :-- |
| Linux e WSL, que também colidem (`orca-ide`, ponte WSL, pacote deb/rpm) | "Só mac e Windows (Recomendado)" |
| O `orca` que agentes, skills e help citam | "brza global + alias orca interno (Recomendado)" |
| `brza` num terminal do Orca segue o `ORCA_USER_DATA_PATH` dele | "Corrigir no launcher (Recomendado)" |
| O pareamento, já que o app mobile do Orca só aceita `orca://pair` | "Manter orca://pair (Recomendado)" |

Na correção do launcher, apagar só o `ORCA_USER_DATA_PATH` não bastava. Com o carimbo de origem do runtime do Orca
ainda no ambiente, o CLI recusaria com `runtime_source_mismatch`. Por isso, quando o terminal é de outro app, o launcher
também descarta o carimbo de origem e a identidade do terminal.

## O que ficou aberto

- **A conferência na máquina, com Anderson.** O pedido lista o que conferir:
  - `Orca.app` e `BrzA Studio.app` abertos ao mesmo tempo;
  - as pastas `Application Support/orca` e `Application Support/brza-studio`;
  - os dois itens no Keychain;
  - `brza` e `orca` abrindo cada um o seu app, com o `brza` registrado em Configurações → CLI;
  - um chat de agente em cada app recebendo os próprios hooks.
- **O `/Applications/Orca 2.app`** (o alpha.1, que usa a `userData` do Orca) ainda está instalado. Tirar é decisão de
  Anderson.
- **Linux e WSL** seguem colidindo com o Orca, por decisão.
- **Os links `https://app.orca.dev/skills/share/…`** são do upstream. O redirecionamento dessas páginas leva ao
  `orca://`, ou seja, ao Orca.

## Fora do workspace

- **`/Applications/BrzA Studio.app`.**
  - **O quê e onde:** o build local `…de3fb921ad16`, copiado com `ditto` de
    `~/Projects/brza-studio/dist/mac-arm64/BrzA Studio.app`.
  - **Risco:** nenhum para o Orca, porque a `userData`, o Keychain, o esquema e o executável são próprios. É assinado ad
    hoc, sem notarização.
  - **Estado:** ativo.
  - **Como desfazer:** apagar o `.app`. Os dados ficam em `~/Library/Application Support/brza-studio` e no item
    `BrzA Studio Safe Storage` do Keychain.
- **O build local.**
  - **O quê e onde:** `~/Projects/brza-studio/dist/brza-studio-macos-arm64.dmg` (468 MB) e
    `dist/mac-arm64/BrzA Studio.app`, fora do git.
  - **Risco:** só espaço em disco.
  - **Estado:** presente.
  - **Como desfazer:** `rm -rf ~/Projects/brza-studio/dist`.
- **O `node_modules` da raiz do `brza-studio`.**
  - **O quê e onde:** o `pnpm install --frozen-lockfile --offline` reescreveu os links do store. Um install feito pelo
    worktree `.worktrees/itens-orca-fixfy` tinha deixado os links apontando para `/Library/pnpm`, e não para
    `~/Library/pnpm`.
  - **Risco:** nenhum.
  - **Estado:** corrigido.
  - **Como desfazer:** não se aplica.
- **A memória da sessão.**
  - **O quê e onde:** `~/.claude/projects/-Users-andepb-Projects-brza-studio/memory/brza-orca-coexistence.md` e o índice
    `MEMORY.md`, com as decisões desta tarefa para as próximas sessões do `brza-studio`.
  - **Risco:** a memória envelhece se as decisões mudarem.
  - **Estado:** ativa.
  - **Como desfazer:** apagar o arquivo e a linha do índice.
