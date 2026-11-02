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

## Fora do workspace

- **O quê e onde:** `brew upgrade python@3.14` (3.14.7 → 3.14.10), em `/opt/homebrew`; fica porque o `azure-cli`
  depende dele, e as bibliotecas Python do `openvino` e do `numpy` do Homebrew estão nele. **Risco:** baixo.
  **Estado:** ativo. **Como desfazer:** não volta por `brew`; o 3.14.7 saiu no cleanup.
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
