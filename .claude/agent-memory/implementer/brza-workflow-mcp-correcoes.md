---
name: brza-workflow-mcp-correcoes
description: Armadilhas e convenções ao corrigir achados de revisão no packages/mcp do brza-workflow (PLN-009), com teste antes
metadata:
  type: project
---

- Para provar que o teste novo falha antes do conserto sem commit: `git stash push -q -- packages`, rode `python3 -m unittest discover -s tests/mcp`, anote os nomes que falham (`grep -E "^(FAIL|ERROR):"`) e `git stash pop -q`. Os testes que passam sem o conserto (guardas de mutante) se provam por mutação com `sed -i ''` + `cp` de backup. No macOS o `sed -i` pede `''`.
- `Queue.admit_next` reserva a vaga (worker `running` sem `session`) e `release` desfaz; `next_admissible` reserva e solta dentro do mesmo lock só para julgar o resto da fila com a vaga do escolhido ocupada. `mark_running` agora levanta `ValueError` se o pedido não está `queued`. `Limits.last_decision` vira a do último pedido avaliado, não a do escolhido: teste decide de novo com `limits.decide`.
- `Limits.scope()` (contexto da passada) faz o uso por (conta, runtime) e a máquina serem lidos uma vez; a fila o abre se o `limits` o tem (os dublês de `limits` dos testes podem não ter).
- O `resetsAt` guarda-se ao minuto (`_bucket`) e `record_usage` apaga amostras com `resets_at < agora`: teste de "outro reset" precisa de resets a minutos de distância e ainda no futuro do relógio do teste.
- `tools.py`: as chaves do `config` são lista fechada `_KEYS` com tipo e faixa; `check_policy()` roda no topo de dispatch/status/config e devolve `isError` com o caminho do `brza.toml` quebrado; `sync_limits` cai nos DEFAULTS em vez de levantar.
- `clients.cli_path`: o orca usa o caminho do app e `shutil.which('orca')` de reserva; o `brza` do Studio NÃO tem reserva (no PATH `brza` é o CLI do workflow).
- Não há chamada real ao `orca`: o formato dos erros do `worker-start` (`start_failed`, `start_outcome_unknown`) e o `worker-release --dispatch`, `task-update --id --status`, `worker-show --dispatch` vêm do código e dos e2e do brza-studio (leitura), e o `tev1` local (Ollama em 127.0.0.1:11434) pode ser sondado sem custo: 9/10 nos casos de camada (o L7 erra).
- `tests/cli` em ambiente limpo leva ~140 s: rode em segundo plano para um arquivo e espere com `until grep -qE "^(OK|FAILED)" arq`. `tests/mcp` ~11 s, 283 testes; `tests/hooks` 290.
