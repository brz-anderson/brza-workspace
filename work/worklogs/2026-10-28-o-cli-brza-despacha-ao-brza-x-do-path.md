---
scope:
  - brza-studio
---

# O CLI `brza` despacha o subcomando desconhecido ao `brza-X` do PATH

O pedido de Anderson, em 2026-10-28, na sessão `brza-cli-subcomandos`: "Execute a issue
work/issues/cli-brza-manda-subcomando-desconhecido-ao-brza-x-do-path.md no brza-studio". A issue é
[O CLI brza manda o subcomando desconhecido ao brza-<sub> do PATH, como o git](../issues/cli-brza-manda-subcomando-desconhecido-ao-brza-x-do-path.md),
e o despacho é o passo 0 do
[PLN-002: Os passos manuais que se repetem entre sessões viram comandos brza](../../plans/PLN-002-os-comandos-brza/PLN-002-plan.md).

## O que se fez

**O commit:** `9a81e65c852` na `master` do `brza-studio`, com push.
- **O desvio:** `src/cli/external-subcommand.ts`, chamado no `main` de `src/cli/index.ts` antes do parse e da
  validação. Ele vale só para o `argv[0]`, e só quando nenhum comando conhecido começa por ele. Entre os conhecidos estão
  os primeiros termos das specs, o `help`, o `agent-teams-tmux` e o `claude-teams`.
- **A busca:** o `brza-<nome>` é procurado pelo `resolveCommandOnLocalPath` de `src/main/ipc/command-path-resolver.ts`,
  que já existia. O nome tem de ser palavra simples: flag, caminho e vazio ficam de fora.
- **A execução:** argumentos, stdin, stdout e código de saída passam intactos; morte por sinal vira 128 + o sinal.
  - O filho não recebe o `ELECTRON_RUN_AS_NODE`.
  - O `NODE_OPTIONS` e o `NODE_REPL_EXTERNAL_MODULE`, que o launcher guarda em `ORCA_*`, voltam ao lugar.
  - O SIGINT e o SIGQUIT do terminal já chegam ao grupo, e o pai os ignora. O SIGTERM e o SIGHUP o pai repassa.
- **O laço:** o `BRZA_EXTERNAL_SUBCOMMANDS` guarda a cadeia dos desvios em curso. O `brza-X` que chama `brza X` cai no
  `Unknown command`, e não de novo no desvio.

**Os testes:** `src/cli/external-subcommand.test.ts`, com 11 casos, todos passando. Cobrem o achado e executado, o não
achado (o `Unknown command` de hoje), o comando conhecido sem desvio (`terminal foo`), o laço, o ambiente e o sinal.
- **A suíte do CLI:** 2.126 testes passam e 3 falham, os de `src/cli/handlers/serve-service.test.ts`. Os mesmos 3
  falham na `master` sem a mudança.
- **Typecheck, lint e formato** passam.

**A conferência de ponta a ponta, sem reinstalar:** o `pnpm run build:cli` gerou o `out/cli/index.js`, rodado com o
Electron do app instalado e `ELECTRON_RUN_AS_NODE=1`.
- `sessions --help` respondeu a ajuda do `brza-sessions`;
- `naoexiste` e `terminal foo` seguiram como `Unknown command`, com saída 1;
- `sessions` com `BRZA_EXTERNAL_SUBCOMMANDS=sessions` caiu no `Unknown command`.

## O que Anderson respondeu

Esta sessão roda dentro do BrzA Studio, e reinstalar exigiria fechar o app. Isso derrubaria esta sessão, os chats e o
`orchestration check` da `run_de875fc52a75`. A issue
[Os comandos brza que viram o PLN-002](../issues/os-comandos-brza-que-viram-o-pln-002.md), na linha 30, já dava a
reinstalação ao `brza app install`.

- **Quando o app instalado ganha o desvio:** "No brza app install (Recomendado)".
- **Quando a ajuda do `brza-install` e do `brza-run` e o `CLAUDE.md` passam a citar `brza install` e `brza run`:**
  "Junto da reinstalação (Recomendado)".

## O que ficou

O pendente foi para o PLN-002, pelo correio à sessão `pln-002-comandos-brza`, que escreve o plano:
- reinstalar o app pelo `brza app install` e conferir o `brza sessions --help` do chat e do terminal;
- ligar o `~/.local/bin/brza-install` (hoje `which brza-install` falha) e fazer o `brza-install` ligar a si mesmo, para
  que o `brza install` ache o script;
- depois da reinstalação, trocar `brza-install` e `brza-run` por `brza install` e `brza run` na ajuda dos scripts e no
  `CLAUDE.md`.
