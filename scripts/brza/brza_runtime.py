"""O CLI e o runtime do BrzA Studio, para os scripts de `scripts/brza/`.

O app ainda usa os nomes do Orca por dentro: o arquivo de runtime é `orca-runtime.json` e o terminal e o chat recebem
`ORCA_CLI_COMMAND` e `ORCA_USER_DATA_PATH`. Dentro do app, esses valores vêm do ambiente; fora dele, valem os caminhos
do BrzA Studio instalado em /Applications.
"""

import json
import os
import socket
import subprocess
import uuid
from pathlib import Path

APP_BIN = Path('/Applications/BrzA Studio.app/Contents/Resources/bin')
DEFAULT_CLI = APP_BIN / 'brza'
DEFAULT_USER_DATA = Path.home() / 'Library' / 'Application Support' / 'brza-studio'
WORKSPACE = Path(os.environ.get('BRZA_WORKSPACE') or Path.home() / 'Projects' / 'brza-workspace')
LOCAL_BIN = Path.home() / '.local' / 'bin'


class BrzaError(RuntimeError):
    """O CLI ou o runtime respondeu com erro, ou não respondeu."""


def cli_command() -> str:
    return os.environ.get('ORCA_CLI_COMMAND') or str(DEFAULT_CLI)


def user_data() -> Path:
    return Path(os.environ.get('ORCA_USER_DATA_PATH') or DEFAULT_USER_DATA)


def runtime_file() -> Path:
    return user_data() / 'orca-runtime.json'


def brza(*args):
    """Roda o CLI com `--json` e devolve o `result`; erro vira BrzaError."""
    r = subprocess.run([cli_command(), *args, '--json'], capture_output=True, text=True)
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise BrzaError(f'brza {" ".join(args)} falhou: {r.stderr.strip() or r.stdout.strip()}') from None
    if not out.get('ok', False):
        raise BrzaError(f'brza {" ".join(args)} falhou: {json.dumps(out.get("error", out), ensure_ascii=False)}')
    return out['result']


def rpc(method, params=None, timeout: float = 10.0):
    """Chama um método do runtime pelo socket local, como o CLI faz; o CLI não expõe as configurações."""
    try:
        meta = json.loads(runtime_file().read_text())
        endpoint = next(t['endpoint'] for t in meta['transports'] if t['kind'] == 'unix')
    except (OSError, ValueError, KeyError, StopIteration) as e:
        raise BrzaError(f'não li o runtime em {runtime_file()} ({e})') from None
    request = {'id': str(uuid.uuid4()), 'authToken': meta['authToken'], 'method': method, 'params': params}
    try:
        with socket.socket(socket.AF_UNIX) as s:
            s.settimeout(timeout)
            s.connect(endpoint)
            s.sendall((json.dumps(request) + '\n').encode())
            buffer = b''
            while b'\n' not in buffer:
                chunk = s.recv(65536)
                if not chunk:
                    break
                buffer += chunk
    except OSError as e:
        raise BrzaError(f'{method}: o runtime não respondeu ({e})') from None
    try:
        out = json.loads(buffer.split(b'\n')[0])
    except ValueError:
        raise BrzaError(f'{method}: resposta ilegível do runtime') from None
    if not out.get('ok', False):
        raise BrzaError(f'{method}: {json.dumps(out.get("error", out), ensure_ascii=False)}')
    return out['result']
