"""O CLI e o runtime do BrzA Studio, para os scripts de `scripts/brza/`: o envio ao chat, o git e o worktree do
brza-studio.

O app ainda usa os nomes do Orca por dentro: o arquivo de runtime é `orca-runtime.json` e o terminal e o chat recebem
`ORCA_CLI_COMMAND` e `ORCA_USER_DATA_PATH`. Dentro do app, esses valores vêm do ambiente; fora dele, valem os caminhos
do BrzA Studio instalado em /Applications.
"""

import hashlib
import json
import os
import socket
import subprocess
import time
import uuid
from pathlib import Path

APP_BIN = Path('/Applications/BrzA Studio.app/Contents/Resources/bin')
DEFAULT_CLI = APP_BIN / 'brza'
DEFAULT_USER_DATA = Path.home() / 'Library' / 'Application Support' / 'brza-studio'
WORKSPACE = Path(os.environ.get('BRZA_WORKSPACE') or Path.home() / 'Projects' / 'brza-workspace')
STUDIO = Path(os.environ.get('BRZA_STUDIO') or Path.home() / 'Projects' / 'brza-studio')
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


def canonicalize(value) -> str:
    """O canonicalize do brza-studio (src/shared/structured-agent-session-mutation.ts), que a impressão digital cobre."""
    if isinstance(value, list):
        return '[' + ','.join(canonicalize(v) for v in value) + ']'
    if isinstance(value, dict):
        return '{' + ','.join(f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(v)}'
                              for k, v in sorted(value.items())) + '}'
    return json.dumps(value, ensure_ascii=False)


def send_mutation(session_id: str, text: str, fence: int, now_ms: int, entropy: str) -> dict:
    """Os parâmetros do agentSession.send, como os monta structuredAgentSessionMessageSendMutation no brza-studio."""
    body = {'kind': 'message', 'role': 'user', 'blocks': [{'type': 'text', 'text': text}]}
    fields = {'body': body, 'delivery': 'queue-if-active'}
    payload = canonicalize({'method': 'agentSession.send', 'sessionId': session_id, 'fields': fields})
    return {'envelope': {'sessionId': session_id, 'clientOperationId': f'{now_ms}-{entropy}',
                         'expectedRuntimeFence': fence,
                         'payloadFingerprint': hashlib.sha256(payload.encode()).hexdigest()},
            **fields}


def send_to_chat(session_id: str, text: str):
    """Manda uma mensagem ao chat, que espera na fila com o agente no meio de um turno."""
    page = rpc('agentSession.history', {'sessionId': session_id, 'direction': 'tail', 'limit': 1})['page']
    rpc('agentSession.send', send_mutation(session_id, text, page['fence'], int(time.time() * 1000),
                                           uuid.uuid4().hex))


def git(*args, cwd: Path | None = None) -> str:
    """Roda o git no `cwd`, ou no checkout do brza-studio, e devolve o stdout; erro vira BrzaError com o stderr."""
    r = subprocess.run(['git', '-C', str(cwd or STUDIO), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise BrzaError(f'git {" ".join(args)} falhou: {r.stderr.strip() or r.stdout.strip()}')
    return r.stdout


def worktree_add(path: Path, base: str = 'origin/master', branch: str | None = None, fetch: bool = True) -> Path:
    """`git fetch origin` (se fetch), e `git worktree add` em `path` de `base`; sem `branch`, sai detached."""
    if fetch:
        git('fetch', 'origin')
    git('worktree', 'add', *(('-b', branch) if branch else ('--detach',)), str(path), base)
    return path


def install_offline(path: Path):
    """`pnpm install --offline --frozen-lockfile` em `path`; falha vira BrzaError que diz o comando online."""
    r = subprocess.run(['pnpm', 'install', '--offline', '--frozen-lockfile'], cwd=path, capture_output=True, text=True)
    if r.returncode != 0:
        tail = '\n'.join((r.stderr.strip() or r.stdout.strip()).splitlines()[-5:])
        raise BrzaError(f'o install offline falhou em {path}; rode lá `pnpm install --frozen-lockfile`\n{tail}')


def worktree_remove(path: Path):
    """`git worktree remove` sem --force; usado no worktree temporário, que nasce limpo."""
    git('worktree', 'remove', str(path))
