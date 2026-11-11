"""Põe no sys.path a pasta de scripts sob teste: `PR_SCRIPTS` (para rodar a mesma suíte contra um snapshot) ou a pasta
`scripts/` desta skill. Importar este módulo antes dos scripts. Os helpers montam planos em diretório temporário."""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
SCRIPTS = os.environ.get("PR_SCRIPTS") or os.path.dirname(HERE)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
FIXTURES = os.path.join(HERE, "fixtures")
ROOT_DIR = os.path.join(FIXTURES, "raiz")


def fixture(*pieces):
    return os.path.join(FIXTURES, *pieces)


def read_text(*pieces):
    with open(fixture(*pieces), encoding="utf-8") as f:
        return f.read()


def copy_root():
    """Cópia da raiz de fixtures (planos reais) num diretório temporário; devolve o caminho. Quem pede apaga."""
    d = tempfile.mkdtemp(prefix="plan-runner-")
    shutil.copytree(ROOT_DIR, os.path.join(d, "raiz"))
    return os.path.join(d, "raiz")


def plan_tmp(plan, interview=None, design=None, num=900, extra=None):
    """Monta `plans/PLN-<num>-teste/` num diretório temporário e devolve (raiz, caminho do -plan.md).

    `extra`: {caminho relativo à raiz: texto}, para notas de `work/` que o plano linka."""
    root = tempfile.mkdtemp(prefix="plan-runner-")
    folder = os.path.join(root, "plans", "PLN-%d-teste" % num)
    os.makedirs(folder)
    files = {"PLN-%d-plan.md" % num: plan}
    if interview is not None:
        files["PLN-%d-interview.md" % num] = interview
    if design is not None:
        files["PLN-%d-design.md" % num] = design
    for name, txt in files.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            f.write(txt)
    for rel, txt in (extra or {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(txt)
    return root, os.path.join(folder, "PLN-%d-plan.md" % num)


def clean(root):
    shutil.rmtree(root, ignore_errors=True)
