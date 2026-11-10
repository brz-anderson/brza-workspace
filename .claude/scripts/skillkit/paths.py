"""Caminhos e o corte do anexo de medida: a raiz do git, a raiz comum e o worklog sem o `## Medida`.

Só biblioteca padrão. Extraído de `common.py` e `sessions_map.py` da `meeting-runner` (PLN-021/D1).
"""
import os
import re
import subprocess


def raiz_padrao():
    """O topo do repositório git do cwd (`git rev-parse --show-toplevel`); sem git, o cwd."""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.getcwd()


def common_root(root):
    """A raiz comum do git (o `WORKSPACE` do v2): o worktree não guarda `.sessions/`."""
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                           timeout=10)
    except (OSError, subprocess.SubprocessError):
        return os.path.abspath(root)
    if r.returncode != 0 or not r.stdout.strip():
        return os.path.abspath(root)
    return os.path.dirname(os.path.realpath(os.path.join(root, r.stdout.strip())))


MEDIDA_RE = re.compile(r"^## (?:Medida|Custo da tarefa)\s*$")
TITULO_N12_RE = re.compile(r"^#{1,2}\s")
FIM_RODADA_RE = re.compile(r"^<!-- fim-rodada-\d+ -->$")


def corta_medida(text):
    """O texto sem o anexo que o `brza note commit` acrescenta DEPOIS do marcador de fim de rodada: a seção `## Medida`
    (versão antiga) ou `## Custo da tarefa` (cabeçalho e um parágrafo, versão atual).

    Só vale o anexo que vai até o fim do arquivo e que começa DEPOIS do último marcador: outra seção de nível 1 ou 2
    depois dele, ou qualquer seção como `## O que ficou` entre o marcador e o anexo, deixa o texto como está (o marcador
    continua não valendo). Sem nenhum marcador, o anexo se corta do mesmo jeito."""
    linhas = (text or "").split("\n")
    idx = [i for i, l in enumerate(linhas) if MEDIDA_RE.match(l)]
    if not idx:
        return text or ""
    i = idx[-1]
    if any(TITULO_N12_RE.match(l) for l in linhas[i + 1:]):
        return text
    if any(FIM_RODADA_RE.match(l.rstrip()) for l in linhas[i + 1:]):
        return text   # o marcador vem depois do cabeçalho: não é anexo
    return "\n".join(linhas[:i])
