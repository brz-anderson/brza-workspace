---
name: host-feature-review-patterns
description: Onde o erro se esconde numa feature do fork no host de agent-session do brza-studio (pedido em memória, sinal empurrado, wrapper de RPC), e o método que o achou
metadata:
  type: project
---

Visto na fase 1 do PLN-026 (2026-11-26, o Continuar em outra conta adiado):

- **Fixture que grava o journal na ordem inversa à do provider.** O teste dirigido por publicação de
  status (sem `tick` manual) fica intermitente quando o fixture grava o turno `completed` antes da
  linha que o qualifica (o status de limite). A Claude grava a falha terminal antes do `settle`
  (`claude-result-journaling.ts`). Rode o teste-chave 3 a 8 vezes sozinho. Para achar a janela,
  embrulhe os `deps` privados da classe num teste temporário (`(x as any).deps.readCut = …`) e registre
  o que cada volta leu.
- **Pedido que sai do `Map` antes do envio e não confere o desfecho**: o `readCut` nulo e a recusa só
  vão ao log. Procure o `end()`/`forget()` antes do `await send`.
- **Wrapper de método do upstream que reage a todo chamador.** O `agentSession.cancel` é o Stop do
  chat, o Stop de uma tarefa (`scope: 'background-tasks'`) e o cancelar de um cartão (`prompt`). O
  wrapper do fork que não olha os params pega os três. Procure os chamadores no renderer (`git grep
  "'agentSession.<método>'"`) e o `*Plan` do upstream, que separa os casos.
- **Sinal empurrado no lugar de timer** (X9): o gatilho que não publica status do chat (a troca de
  seleção que mantém o agente) só é visto na próxima publicação ou no prazo. Teste sem `tick` manual.
- **Hipótese que caiu:** "a primeira volta não roda no arm porque o publish vem antes do subscribe".
  O `subscribe` do status feed emite um `snapshot` na assinatura. Não gaste tempo nela.

Visto de novo no P5 do PLN-026 (2026-11-27, o chat fixado e os consertos da fase 1):

- **Decisão sob o `serialize` e ação fora dele, sem conferir de novo.** O `check` decide `fire`, sai
  do `serialize` e chama uma operação que pega o `serialize` sozinha (o `switchAccount`). O Cancelar
  ou o Stop que entra na fila nesse meio roda antes, e a troca acontece mesmo assim. A janela é a
  operação inteira, porque o `run` dela fica no `serialize`. Prova em 1 s: embrulhe o `deps.readCut`
  para soltar o `cancel()` sem `await` no meio do veredito.
- **Estado novo do host que o renderer nunca mostra.** O status ganhou um motivo (`turnFailed`) para
  um caso em que nenhuma linha de limite fica ativa (o `usageLimitTurnItemId` é nulo sem corte novo),
  e o componente do fork só monta no slot da linha ativa. Para cada estado novo, siga até o ponto em
  que ele monta: `latest…Cut` → `active` → `slotKey`.
- **Caso de teste que passa pelo motivo errado.** Um conserto com dois portões (excluir o `prompt` e
  só cancelar com `ok`) e um caso cujo cancel o host recusa (`promptGone`) prova só o segundo
  portão. Rode a chamada do caso num teste temporário e veja o `ok`.
- **O relógio parado do rig (`now: () => NOW`) esconde todo ramo com `now < prazo`** (o `retryAt`
  de 2 s nunca vence). Ramo assim sem caso costuma ser ramo que o rig não consegue rodar.

Os testes temporários `zz-reviewer-*` no worktree da branch rodam em ~6 s cada, com
`--silent=false` para ver o `console.log`. Apague-os no mesmo passo e confira o `git status`.

Related: [[reviewer-confidence-calibration]], [[sync-review-patterns]]
