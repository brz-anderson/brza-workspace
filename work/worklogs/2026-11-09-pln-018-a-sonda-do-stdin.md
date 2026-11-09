---
scope:
  - brza-workspace
tags:
  - tooling
refs:
  - PLN-018
  - issue:codex-e-antigravity-sem-medida-por-tarefa
  - issue:o-grok-fica-sem-medida-por-tarefa
---

# PLN-018: a sonda do stdin e o Desenho

Anderson pediu para conduzir o
[PLN-018: O turno do Grok e do Codex entra no log, e a tarefa carimba o id dessa sessão](../../plans/PLN-018-o-grok-e-o-codex-na-medicao/PLN-018-plan.md):
registrar as pendências, criar issue só quando faltar, pular o que depende de decisão dele e parar quando não houver
mais o que executar.

## O que se fez

- Sonda de stdin: um Stop do `grok agent stdio` sem `--trust`, e um Stop do `codex exec`. Só chaves e booleanos. O
  caminho da sessão chega nos dois. O detalhe está no Terreno do plano.
- Sonda do Antigravity, CLI e chat ACP distintos. A CLI tem token e não tem model nem custo na linha. O chat ACP não
  tem os três na transcrição. Sem escritor neste plano.
- O Desenho, D1 a D3, está no plano. `phase: design`, `status: open`. Hora de escritor continua zero. Não há Passos.
- As issues
  [O Grok fica sem medida por tarefa](../issues/o-grok-fica-sem-medida-por-tarefa.md) e
  [Codex e Antigravity ficam sem medida por tarefa](../issues/codex-e-antigravity-sem-medida-por-tarefa.md)
  foram atualizadas com a sonda. Nenhuma issue nova.

## O que ficou

O corte dos passos e a instalação do hook do Codex ficaram no plano, no D2. A rodada do escritor do Antigravity ficou
na issue. Nenhum dos três foi perguntado nesta sessão.

## Fora do workspace

- **O quê e onde:** json de prova em `~/.grok/hooks/`, instalado para um Stop e removido no fim. **Risco:** um hook de
  prova deixado na pasta rodaria em todo `grok agent`. **Estado:** removido; a pasta ficou com o `orca-status.json`
  que já estava. **Como desfazer:** nada a desfazer.
- **O quê e onde:** `~/.codex/hooks.json`, o command do Stop trocado pela prova e restaurado ao byte anterior no mesmo
  comando. **Risco:** restaurar mal desligaria o hook que o usuário já confia. **Estado:** a comparação com a cópia
  bateu antes de a cópia ir embora com o scratch; o arquivo vivo não foi reescrito nesta limpeza. **Como desfazer:**
  nada a desfazer.
- **O quê e onde:** git temporário em `~/Projects/_pln-018-sonda` e `~/Projects/_pln-018-sonda-codex`; o diretório de
  sessões do Grok desse primeiro cwd, com 6 sessões; cinco rollouts do Codex cujo cwd era o da prova, as cinco linhas
  em `threads` e os cinco recibos de leitura órfãos. **Risco:** apagar sessão que não era da prova. **Estado:**
  removidos; a busca seguinte não achou esse cwd. **Como desfazer:** não há cópia.
- **O quê e onde:** scratch em `/tmp/pln-018-probe`, com as chaves da sonda. **Risco:** digest de id de sessão no disco
  temporário. **Estado:** removido. **Como desfazer:** nada a desfazer.
