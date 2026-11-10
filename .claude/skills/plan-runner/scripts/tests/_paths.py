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
RAIZ = os.path.join(FIXTURES, "raiz")


def fixture(*partes):
    return os.path.join(FIXTURES, *partes)


def le(*partes):
    with open(fixture(*partes), encoding="utf-8") as f:
        return f.read()


def copia_raiz():
    """Cópia da raiz de fixtures (planos reais) num diretório temporário; devolve o caminho. Quem pede apaga."""
    d = tempfile.mkdtemp(prefix="plan-runner-")
    shutil.copytree(RAIZ, os.path.join(d, "raiz"))
    return os.path.join(d, "raiz")


def plano_tmp(plan, interview=None, design=None, num=900, extra=None):
    """Monta `plans/PLN-<num>-teste/` num diretório temporário e devolve (raiz, caminho do -plan.md).

    `extra`: {caminho relativo à raiz: texto}, para notas de `work/` que o plano linka."""
    raiz = tempfile.mkdtemp(prefix="plan-runner-")
    pasta = os.path.join(raiz, "plans", "PLN-%d-teste" % num)
    os.makedirs(pasta)
    arqs = {"PLN-%d-plan.md" % num: plan}
    if interview is not None:
        arqs["PLN-%d-interview.md" % num] = interview
    if design is not None:
        arqs["PLN-%d-design.md" % num] = design
    for nome, txt in arqs.items():
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as f:
            f.write(txt)
    for rel, txt in (extra or {}).items():
        p = os.path.join(raiz, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(txt)
    return raiz, os.path.join(pasta, "PLN-%d-plan.md" % num)


def limpa(raiz):
    shutil.rmtree(raiz, ignore_errors=True)
