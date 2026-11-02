---
scope:
  - workspace
---

# PLN-006: a migração do brza-workspace

Continuação de [PLN-006: a abertura do brza init](2026-10-31-pln-006-a-abertura-do-brza-init.md), no
[PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md).
Em 2026-10-31 ficaram feitos P1–P7, no `brz-anderson/brza-workflow@b9210a6`.

## A R17

Anderson respondeu "decidido, agora": a proposta
[O índice de notas mora na `master`, a única exceção à regra da norma](../decisions/o-indice-de-notas-mora-na-master.md)
foi a `done`, e o P8 roda agora, em estágios. O "Continue where you left off." que veio antes não respondia a rodada, e
a sessão não o tomou por resposta.

## O que corre

- A revisão adversária do `brza-workflow` (parte do P9), retomada depois de parar no limite de uso.
- O porte, ao núcleo, dos dois commits que a `master` do `brza-workspace` ganhou depois da cópia do P1: `2c9a546` e
  `cfa058e`, do PLN-005, em oito arquivos.

## A revisão e os consertos

O `reviewer` achou 11 defeitos e derrubou 5 hipóteses de dano, em
[REV: o `brza-workflow` dos passos P1–P7 do PLN-006, em `b9210a6`](../reviews/pln-006-o-brza-init.md). Pela regra
da recomendada, o porte fechou o A1 (`brza-workflow@ebeb779`), um `implementer` consertou A4–A9 e A11
(`@2286f31`), e a migração fechou A2, A3 e A10.

## A migração

Os nove estágios do D12 rodaram nesta sessão, com a evidência no P8 do plano. Duas mudanças de ordem:
- **X27:** o `--local` foi para depois de os scripts movidos saírem de `scripts/brza/`, que ele religaria.
- **X28:** o README e a `.claude/rules/workspace.md` receberam antes o que o sync tira do `AGENTS.md` e do `CLAUDE.md`.

Na `master` do `brza-workspace`, a migração deixou cinco commits:
- `2e6ea1d`: o manifesto e as regras;
- `1fd3be0`: o índice, com 29 linhas;
- `a45018c`: o sync;
- `bbe723b`: os scripts e os testes;
- o merge nos quatro workstreams.

Sobraram dois `hook_error` na medição, das 12:59. São das sondas da trava do `/compact` que rodei sem o modo `pre`, e
não da trava em uso.

## Fora do workspace

- **O quê e onde:** `brew upgrade python@3.14` (3.14.7 → 3.14.10), em `/opt/homebrew`. **Risco:** baixo.
  **Estado:** desfeito, com o `azure-cli`, no item seguinte. **Como desfazer:** não volta por `brew`; o 3.14.7 saiu no cleanup.
- **O quê e onde:** `brew uninstall azure-cli`, que levou junto, por autoremove, o `python@3.14` e as dependências
  órfãs — entre elas `libsodium` e `mpdecimal`; a saída foi cortada, e a lista inteira não ficou. Sem sinal de uso: sem
  `~/.azure`, sem `az` no histórico do zsh, sem chamada em `~/Projects`. Anderson escolheu "Remover os dois
  (Recomendado)". **Risco:** as bibliotecas Python do `openvino` e do `numpy` do Homebrew, que seguem instalados,
  deixam de ser importáveis; sobram as pastas `/opt/homebrew/lib/python3.11` a `3.15`, com o que elas instalaram.
  **Estado:** ativo. **Como desfazer:** `brew install azure-cli`, que traz de volta o `python@3.14`.
- **O quê e onde:** `brew install python@3.15` (3.15.2), removido em seguida por `brew uninstall python@3.15`, porque
  repetia o 3.15.2 do python.org e nada dependia dele; Anderson escolheu "Remover (Recomendado)". Com isso, sai o
  `/opt/homebrew/bin/python3`. **Risco:** nenhum. **Estado:** desfeito.
- **O quê e onde:** o instalador do python.org 3.15.2 (`python-3.15.2-macos11.pkg`, notarizado), baixado em
  `/private/tmp/pyorg-dl/` e aberto no Installer para Anderson concluir com a senha; instala em
  `/Library/Frameworks/Python.framework/Versions/3.15` e repõe os links de `/usr/local/bin`, ao lado do 3.14.6, que
  fica. **Risco:** o `python3` do terminal passa a 3.15, sem os pacotes do 3.14 — hoje só o `pip`; quem chama `python3`
  sem `BRZA_PYTHON`, como o hook de medição, roda no 3.15. **Estado:** ativo; `python3 --version` dá 3.15.2. **Como desfazer:**
  apagar `/Library/Frameworks/Python.framework/Versions/3.15` e `/Applications/Python 3.15`, e religar os links de
  `/usr/local/bin` ao 3.14.
- **Sem mudança:** o `/usr/bin/python3` do sistema é o 3.9.6 do Xcode (`xcode-select -p`), protegido pelo SIP; só muda
  com o Xcode ou as Command Line Tools.
- **O quê e onde:** a limpeza da Microsoft, por pedido de Anderson ("desinstale os candidatos óbvios"):
  - `brew uninstall --formula powershell` (7.4.1, sem link) e `brew untap powershell/tap`; o `pwsh` segue no cask
    7.3.7, em `/usr/local/bin/pwsh`.
  - Com a senha de Anderson: `launchctl bootout` do `com.microsoft.autoupdate.helper` (system) e do
    `com.microsoft.update.agent` (gui); os dois plists, o helper de `/Library/PrivilegedHelperTools`,
    `/Library/Application Support/Microsoft` (o AutoUpdate 4.85) e o `MSTeamsAudioDevice.driver` de
    `/Library/Audio/Plug-Ins/HAL` foram para a Lixeira; `killall coreaudiod` descarregou o driver.
  - Para a Lixeira também: `~/Library/Preferences/com.microsoft.teams2.helper.plist`,
    `com.microsoft.autoupdate.fba.plist`, `com.microsoft.autoupdate2.plist` e o cache `com.microsoft.autoupdate.fba`.
  - Anderson removeu pelo Finder `~/Library/Group Containers/UBF8T346G9.com.microsoft.teams`, que o macOS protege do
    terminal.
  - **Ficaram:** `~/Library/Containers/com.microsoft.teams2*` (318 MB: cache do Teams, de 2025-08-26, e a sessão da
    conta de trabalho), que o `mv` de Anderson no terminal também não moveu; saem pelo Finder.

  **Risco:** um app do Office instalado no futuro reinstala o AutoUpdate sozinho; o Teams, o driver. **Estado:** ativo.
  **Como desfazer:** tudo está em `~/.Trash/microsoft-limpeza-2026-11-02/` (o de `/Library` em `root/`), até a Lixeira
  ser esvaziada; voltar cada item ao lugar com `sudo mv` e `launchctl bootstrap`. O PowerShell 7.4.1 volta com
  `brew install powershell/tap/powershell`.
- **O quê e onde:** o `~/.config/brza/workspaces.toml`, criado pelo `brza-register`, com o par
  `~/Projects/brza-workspace` → `~/Projects/brza-studio` (PLN-006/P8, estágio 2). **Risco:** sem ele, o `claude-brza`
  e a função `claude` no `brza-studio` sobem sem hooks nem identidade (X16). **Estado:** ativo. **Como desfazer:** apagar
  o arquivo, depois de desfazer os dois itens seguintes.
- **O quê e onde:** os links de `~/.local/bin` (estágio 5): `brza-note`, `brza-install`, `brza-agents` e os novos
  `brza-init`, `brza-sync`, `brza-register` e `brza-where` passam ao `~/Projects/brza-workflow/bin/`;
  `brza-sessions`, `brza-run`, `brza-doctor`, `brza-print` e `claude-brza`, ao `packages/client/bin/` de lá; `brza-app`,
  `brza-dev`, `brza-shot`, `brza-test` e `brza-tree` seguem no `scripts/brza/` do `brza-workspace`. O
  `agentCmdOverrides.claude` do app segue no `~/.local/bin/claude-brza`. **Risco:** toda sessão nova, do terminal ou
  do chat, roda o CLI do `brza-workflow`; um defeito dele chega a todas. **Estado:** ativo; o `brza doctor` dá `ok`.
  **Como desfazer:** a lista de antes está em `/private/tmp/pln006/links-antes.txt`; refazer cada um com `ln -sfn`
  ao `scripts/brza/` do `brza-workspace` num checkout em `a45018c`, o último commit antes de os scripts saírem de lá.
- **O quê e onde:** o `~/.zshrc`, onde as linhas 51–80 (as `BRZA_WORKSPACE` e `BRZA_STUDIO`, a `brza_where`, a
  `brza_claude` e a `claude`) dão lugar ao `source "$HOME/Projects/brza-workflow/packages/client/shell/brza.zsh"` e a
  uma `brza_claude_fallback` que chama a `fixfy_claude` (estágio 8). As `adm-claude` e `claude-adm` ficam. **Risco:**
  sem o checkout do `brza-workflow`, o `source` falha e a `claude` cai na de verdade, sem a Fixfy. **Estado:** ativo;
  `zsh -n` ok, e a `claude` roteia nos três casos. **Como desfazer:** a cópia de antes está em
  `/private/tmp/pln006/zshrc-antes`, e o bloco antigo também no README do `brza-workspace` em `d85c783`.
