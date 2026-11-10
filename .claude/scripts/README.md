# O código comum das skills do playground

O que mora aqui é biblioteca padrão, sem dependência, e serve a mais de uma skill: abrir, enviar, esperar e fechar sessão
pelo `brza sessions` v2, ler o mapa `.sessions/sessions.jsonl`, medir o custo de uma sessão e gravar o visual HTML com o
PNG dele. O código nasceu na `meeting-runner` e foi extraído para cá (PLN-021/D1).

## O pacote `skillkit/`

| Módulo | O que tem |
| :-- | :-- |
| `paths.py` | `raiz_padrao()`, `common_root(root)`, `corta_medida(texto)` |
| `sessions_map.py` | `fold_map`, `load_map`, `map_file`, `read_rows`, `epoch` (o mapa v2) |
| `sessions_cli.py` | `run_sessions`, `run_brza`, `open_argv`, `send_argv`, `wait_argv`, `close_argv`, `interpreta_abertura`, `wait_brza`, `list_states` |
| `measure.py` | `load_jsonl`, `parse_ts`, `session_ids`, `win_bounds`, `measure_claude`, `measure_codex` |
| `visual.py` | `salva_visual`, `titulo_seguro`, `gera_png` (`brza shot`; Chrome de reserva), `LIMITE_HTML` |

## O import

O `python3 -I` não põe a pasta do script no `sys.path` e ignora `PYTHONPATH`. Cada skill leva ao lado dos scripts um
`_kit.py`, igual em todas (`.claude/skills/<skill>/scripts/_kit.py`), que insere esta pasta no `sys.path`, ou a que a
variável `SKILLKIT` apontar, para rodar contra outra cópia:

```python
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
from skillkit import sessions_cli, visual  # noqa: E402
```

Importe por nome o que o teste da skill troca por atribuição (`from skillkit.sessions_cli import wait_brza`): o código
da skill chama o nome do módulo dela, e a troca vale.

## Os testes

```bash
python3 -I -m unittest discover -s ".claude/scripts/tests"
```

Cada módulo tem um `test_<módulo>.py`. Os testes trocam função por atribuição no módulo, sem `mock.patch`, e `SKILLKIT`
roda a suíte contra outra cópia. Depois de mexer aqui, rode também a suíte de cada skill que importa do kit.
