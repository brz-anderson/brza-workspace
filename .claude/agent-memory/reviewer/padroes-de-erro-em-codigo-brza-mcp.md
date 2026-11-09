---
name: padroes-de-erro-em-codigo-brza-mcp
description: Onde o defeito se esconde no código e nos testes de ciclo de vida do brza-mcp (brza-workflow, packages/mcp) — teste que passa com o comando falhando, timeout menor que o shutdown, erro externo antes da limpeza do plist
metadata:
  type: project
---

Padrões que apareceram na revisão do P8 do PLN-009 (2026-11-03, `stop` que apaga o plist):

- **Teste que chama `self.main(...)` sem conferir o código de saída.** O `test_start_after_stop_writes_the_plist_again`
  passava com o `start` saindo 1 ("o /health não respondeu em 15s"), porque o `live_server(info=True)` antes do
  `start` grava o `mcp.json` com `started` anterior ao `since`. O jeito certo é o `on_bootstrap = lambda:
  self.live_server(info=True)`. Sinal: um teste de 15 s no gate. Cheque: cronometrar os testes (>0,5 s) e sondar o
  `code` do `main`.
- **Timeout de espera menor que o pior caso do lado que encerra.** `STOP_TIMEOUT = 5.0` contra o `serve`, que no
  SIGTERM faz `scheduler.stop()` com `join(5.0)` mais o `shutdown` e o `server_close`. Comparar sempre o timeout novo
  com os `join`/`timeout` do caminho de encerramento (`cli.serve`, `cycle.Scheduler.stop`).
- **Erro do comando externo antes da limpeza.** O `stop` levanta no `bootout` com `returncode != 0` antes do
  `unlink()` do plist. O serviço só sai da tabela pelo `bootout` (o `KeepAlive` reinicia o processo que morre), então a
  janela entre o `is_loaded()` e o `bootout` só abre com outro `stop` ou `start` concorrente; vale perguntar se o erro
  de "alvo não encontrado" conta como já descarregado.
- **Mutação é barata aqui:** copiar `git ls-files` para `/private/tmp`, trocar uma linha do `launchd.py` e rodar
  `-k stop`; mostra em segundos qual teste barra o quê.
- **Resolução de TOCTOU assíncrono em comando externo via rechecagem de estado.** No `stop()`, o `launchctl bootout` falha se
  o processo sair logo antes da chamada; conferir `if r.returncode != 0 and is_loaded():` resolve a corrida sem depender
  de parsing frágil de mensagens de erro (`stderr`/código de saída) do comando externo.
- **Teste de mutação em lote:** isolar em `/private/tmp` com cópia direta dos fontes para evitar prompts interativos de
  comandos como `patch` que travam o runner.

**Why:** o teste fraco e o timeout curto foram os dois achados reais; o resto da correção estava certo.
**How to apply:** em diff do `packages/mcp`, rodar o cronômetro e a mutação antes da leitura fina; confiança 85 para o
timeout real do launchd, com a premissa (o `print` acha o serviço até o processo sair) tirada do caso manual.
Relacionado: [[achados-que-costumam-cair]].

Padrões confirmados no PLN-017/P4 (2026-11-09), também nos wrappers de sessões:

- **A inspeção depois de uma mutação incerta apaga o recibo anterior.** Se o `worker-stop` retornou `stop_unknown`,
  falhar no `worker-show` seguinte não o transforma em recusa. Conservar recibo e incerteza, com erro da observação
  separado. Confiança 90, reproduzido por sonda e mutação.
- **O fake inventa um envelope melhor que o CLI real.** `ok: false` pode conservar o fato em `result.state`, sem
  objeto `error`; conferir a projeção do CLI além do RPC. Confiança 90, fonte e teste dos dois formatos.
- **O stub aceita qualquer id e esconde que falta o id do provedor.** `lambda sid: ...` não testa o casamento com o
  rollout. Usar o leitor real com fixture e provar Claude/Codex medidos depois de a aba e o histórico sumirem;
  Grok `unmeasured` não prova esse caso. Confiança 88, regressão derrubada por mutação.
- **Erro por alvo vira erro do lote e perde efeitos já executados.** Conservar `closed`/`refused` no fechamento e
  `done`/`pending`/`events` na espera, mesmo se a observação de outro alvo falhar. Confiança 85, sonda de segundo alvo.

Evidência e destinos:
[REV-022: As primitivas do brza sessions e a exceção transitória do PLN-010](../../../work/reviews/REV-022-pln-017-sessions-e-transicao-rpc.md).
