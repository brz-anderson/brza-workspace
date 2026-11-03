---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
  - issue:o-approve-do-plugin-e-barrado-no-modo-auto
  - issue:o-cli-do-orca-no-chat-do-studio-fala-com-o-studio
  - issue:os-tipos-de-plugin-faltam-no-pacote-da-1-4-246
---

# O PLN-003: o spike do C5 parou na aprovação

Dois pedidos de Anderson, passados pela sessão do `workspace` em 2026-11-03:
- "retome o PLN-003 pelo Retomar, com a skill plan-runner", com o spike do C5 como primeiro passo;
- depois, "rode o spike do C5 até o final, se conseguir — as sete perguntas, nos dois apps. Cada problema que encontrar
  vira uma issue em work/issues/, com o que falhou e a evidência, e você segue para a próxima pergunta em vez de parar."

O registro do M11 já tinha fechado em
[O PLN-003: o desempatador do M11](2026-11-03-pln-003-o-desempatador-do-m11.md).

## A Rodada 8

Gravada na [Entrevista](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-interview.md), respondida em
2026-11-03 nesta sessão:
- **R8.1**, onde mora o plugin: "Pasta no worktree tools-kit", fora da recomendada (scratch). O plugin está em
  `spikes/c5-plugin/`. A norma de `work/` não prevê a pasta `spikes/`; isso fica para uma rodada de norma, se o spike
  ficar.
- **R8.2**, a aprovação: "CLI, com sua aprovação aqui (Recomendado)".
- **R8.3**, o Orca: "Eu abro e fecho no fim (Recomendado)".
- **R8.4**, o terminal do item 3: "O worker escolhe sozinho", fora da recomendada. O worker pega o primeiro terminal sem
  agente no `agents.list` e sem "claude/codex/agent/✳" no título.

A sessão perguntou "aprovar o `trusted-worker` do spike?" na mensagem. Não houve resposta literal. O pedido seguinte,
o de rodar o spike até o final, foi tomado como a aprovação deste plugin e deste acesso. Mesmo assim, o `--approve`
não rodou: o classificador do modo auto o barrou.

## O que se fez

- **O plugin `local.brza-spike-c5`**, em `spikes/c5-plugin/`: manifesto 2, `trusted-worker`, capacidades
  `workspace:read`, `agent:read` e `terminal:send`, painéis `notas-tsx` (componentes) e `notas-html`, e o worker com
  `ping`, `notes.list`, `terminal.run` e `net.probe`.
  - `brza plugin validate . --json` → `valid: true`.
  - `brza plugin check . --json` → exit 0. No cenário `tools-kit`: Tree com 2 planos e 7 notas, Table com 7 linhas e
    Markdown com o `Retomar` do PLN-003.
  - `brza plugin test . --json` → 3 de 3, com o servidor da sonda em `127.0.0.1:8765`.
- **O `dev load` nos dois apps** → `approval_required`, código 3, com o mesmo fingerprint
  `ap1-aedbb65284d0297120a721e7e67266a2`. O `--approve` foi barrado. O plugin ficou `status: pending`, e o `plugin
  shot` foi recusado ("is waiting for approval").
- **O resultado por item** foi escrito no C5 do
  [Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md):
  - 1 em aberto;
  - 2 e 3 parciais, a favor, fora do app;
  - 4 parcial;
  - 5 e 6 por documento;
  - 7 respondido.
- **Três issues**, uma por problema:
  - [O --approve do plugin é barrado no modo auto](../issues/o-approve-do-plugin-e-barrado-no-modo-auto.md), com `blocks`
    no resto do spike;
  - [O CLI do Orca no chat do Studio fala com o Studio](../issues/o-cli-do-orca-no-chat-do-studio-fala-com-o-studio.md);
  - [Os tipos de plugin faltam no pacote da 1.4.246](../issues/os-tipos-de-plugin-faltam-no-pacote-da-1-4-246.md).
- **O `Retomar` do [PLN-003](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md)** manda terminar o spike
  depois da aprovação de Anderson.

## O que não foi testado

Nada do plugin rodou dentro de um app: o painel, o `plugin.request` real, o `terminal.sendText` num terminal de
verdade, o frame html contra `127.0.0.1`, o reload sem nova aprovação, o `plugin shot` com a janela escondida. O `plugin
check` e o `plugin test` rodam com o Node do CLI, não no worker do app. A referência de `mockHost` dá a entender que
`callsOf` devolve `{ method, params }`, mas ele devolve só os parâmetros (`src/worker.test.ts`).

## Retomar

O spike, depois de Anderson aprovar nos dois apps pelos comandos da issue do `--approve`. Fica no `Retomar` do PLN-003.

## Fora do workspace

- **O quê e onde:** `devPluginPaths` do BrzA Studio e do Orca. O `brza plugin dev load` gravou a pasta
  `spikes/c5-plugin/` e o `dev unload` a tirou. **Risco:** nenhum agora. **Estado:** desfeito, `devPluginPaths: []` nos
  dois (`profile-state.db`, só leitura). **Como desfazer:** já desfeito.
- **O quê e onde:** o Orca aberto com `open -a Orca` e fechado com `quit app "Orca"` (R8.3). Ao fechar, ele se atualizou
  da `1.4.246` para a `1.4.247` (`CFBundleShortVersionString`). **Risco:** o Orca deixou de ter a versão da base do
  fork, e o resto do spike roda na `1.4.247`. **Estado:** ativo. **Como desfazer:** reinstalar o DMG da `1.4.246` da
  release do Orca.
- **O quê e onde:** um `python3 -m http.server 8765 --bind 127.0.0.1` servindo `/private/tmp/c5-probe/`. **Risco:**
  nenhum. **Estado:** parado, e a pasta foi apagada. **Como desfazer:** já desfeito.
