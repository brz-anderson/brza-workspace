#!/usr/bin/env python3
"""O leitor do plano, comum a `plan_state.py`, `step_request.py`, `round_log.py` e `close_check.py` (PLN-021/D6).

Lê `plans/PLN-NNN-*/PLN-NNN-plan.md` e, quando o plano é dividido, junta `PLN-NNN-interview.md` e `PLN-NNN-design*.md`.
Entende: o frontmatter; as seções `##`; os passos `### Pn` (`Executa`, `Estimado`/`Executado`, checkboxes,
`**Evidência:**`, `depende de`); os itens `### D<n>` com a `Origem`; as alternativas `A<n>` de cada D; as rodadas
`### Rodada N` com as perguntas (`R<n>.<k>`), a escolha, a resposta literal e a reabertura; os desvios `X`, os casos `C`.
Heading dentro de cerca de código não conta.

Uso como módulo:

    import plan_md
    plano = plan_md.load("PLN-021")          # ou um caminho de `-plan.md`, ou a pasta do plano
    plano.steps(); plano.design_list(); plano.rounds(); plano.ids()

`python3 -I plan_md.py PLN-NNN|caminho` imprime o resumo do que foi lido (depuração). Sem dependências fora da
biblioteca padrão; não precisa do `skillkit`.
"""
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_PN = re.compile(r"^(P\d+[a-z]?)\s*[—–-]\s*(.*)$")
RE_DN = re.compile(r"^(D\d+)\s*[—–-]?\s*(.*)$")
RE_AN = re.compile(r"^(A\d+)\s*[—–-]\s*(.*)$")
RE_ROUND = re.compile(r"^Rodada\s+(\d+)\b\s*(?:[—–-]\s*)?(.*)$")
RE_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
RE_R = re.compile(r"\bR(\d+)(?:\.(\d+))?\b")
RE_HOURS = re.compile(r"^\s*[~≈]?\s*(\d+(?:[.,]\d+)?)\s*h\b")
RE_CHECK = re.compile(r"^\s*[-*]\s+\[([ xX-])\]\s*(.*)$")
RE_PLN = re.compile(r"^(?:PLN|pln)-(\d+)$")
STEP_ID = r"P\d+[a-z]?"


class PlanNotFound(Exception):
    pass


def parse_hours(txt):
    """Número de horas de um texto como `11,5 h`, `~4 h (…)`, `0.174 h`; `None` para `— h`, vazio ou texto livre."""
    if txt is None:
        return None
    m = RE_HOURS.match(txt)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def format_hours(v):
    """Número no frontmatter: ponto decimal, até 3 casas, sem zeros à direita (`41`, `34.75`, `9.516`)."""
    v = round(float(v), 3)
    if v == int(v):
        return str(int(v))
    return ("%.3f" % v).rstrip("0").rstrip(".")


def _in_fence(line):
    s = line.lstrip()
    return s.startswith("```") or s.startswith("~~~")


class PlanFile:
    def __init__(self, path, role, text=None):
        self.path = path
        self.name = os.path.basename(path)
        self.role = role
        if text is None:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        self.text = text
        self.lines = text.split("\n")
        self.fence = []
        inside = False
        for ln in self.lines:
            if _in_fence(ln):
                self.fence.append(True)
                inside = not inside
            else:
                self.fence.append(inside)
        self.fm_end = self._finds_fm()

    def _finds_fm(self):
        """Índice da linha do segundo `---` do frontmatter, ou -1."""
        if not self.lines or self.lines[0].strip() != "---":
            return -1
        for i in range(1, len(self.lines)):
            if self.lines[i].strip() == "---":
                return i
        return -1

    def headings(self):
        output = []
        for i, ln in enumerate(self.lines):
            if self.fence[i]:
                continue
            m = RE_HEADING.match(ln)
            if m:
                output.append((i, len(m.group(1)), m.group(2)))
        return output

    def sections(self):
        hs = self.headings()
        output = []
        for idx, (i, level, title) in enumerate(hs):
            end = len(self.lines)
            for (j, n2, _t) in hs[idx + 1:]:
                if n2 <= level:
                    end = j
                    break
            output.append(Section(self, level, title, i, end))
        return output

    def where(self, i):
        return "%s:%d" % (self.name, i + 1)


class Section:
    def __init__(self, file, level, title, start, end):
        self.file = file
        self.level = level
        self.title = title
        self.start = start      # índice da linha do heading
        self.end = end      # exclusivo

    @property
    def lines(self):
        return self.file.lines[self.start:self.end]

    @property
    def body_text(self):
        return self.file.lines[self.start + 1:self.end]

    def body_outside_fences(self):
        """(índice absoluto, linha) das linhas do corpo fora de cerca de código."""
        return [(i, self.file.lines[i]) for i in range(self.start + 1, self.end) if not self.file.fence[i]]

    def text(self):
        return "\n".join(self.body_text).strip("\n")

    def where(self):
        return self.file.where(self.start)


def _frontmatter(plan_file):
    if plan_file.fm_end < 0:
        return {}
    fm = {}
    key = None
    for ln in plan_file.lines[1:plan_file.fm_end]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", ln)
        if m and not ln.startswith(" "):
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                fm[key] = []
            else:
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                fm[key] = val
            continue
        m = re.match(r"^\s+-\s+(.*)$", ln)
        if m and key is not None and isinstance(fm.get(key), list):
            fm[key].append(m.group(1).strip())
    return fm


class Question:
    def __init__(self, round, k, topic, start, end, file, explicit=False):
        self.round = round
        self.n = round.n
        self.k = k
        self.id = "R%d.%d" % (round.n, k)
        self.topic = topic
        self.start = start
        self.end = end
        self.file = file
        self.explicit = explicit

    @property
    def lines(self):
        return self.file.lines[self.start:self.end]

    @property
    def block(self):
        return "\n".join(self.lines).rstrip()

    def _line_starting(self, regex):
        for i in range(self.start, self.end):
            if self.file.fence[i]:
                continue
            if re.match(regex, self.file.lines[i].strip()):
                return i
        return None

    def index_decided_line(self):
        return self._line_starting(r"\*\*(Decidid[oa]|Escolhid[oa])\b")

    def answer_index(self):
        return self._line_starting(r"\*\*Resposta\b")

    @property
    def decided_line(self):
        i = self.index_decided_line()
        return self.file.lines[i].strip() if i is not None else None

    @property
    def answer(self):
        i = self.answer_index()
        if i is None:
            return None
        pieces = [self.file.lines[i].strip()]
        for j in range(i + 1, self.end):
            ln = self.file.lines[j]
            if not ln.strip() or ln.lstrip().startswith("**"):
                break
            pieces.append(ln.strip())
        return " ".join(pieces)

    @property
    def reopened(self):
        m = re.search(r"reaberta em (R\d+\.\d+)", self.block)
        return m.group(1) if m else None

    def option_list(self):
        """Opções em bullets `-` recuados, logo abaixo do enunciado; a linha que quebra continua a opção."""
        raw = []
        open_state = False
        for i in range(self.start + 1, self.end):
            if self.file.fence[i]:
                continue
            ln = self.file.lines[i]
            m = re.match(r"^\s{1,}[-*]\s+(.*)$", ln)
            if m:
                raw.append([m.group(1).strip()])
                open_state = True
            elif not ln.strip():
                continue
            elif open_state and re.match(r"^\s{2,}\S", ln) and not ln.strip().startswith("**"):
                raw[-1].append(ln.strip())
            else:
                open_state = False  # parágrafo fora da lista: fecha a continuação
        output = []
        for b in raw:
            txt = " ".join(b)
            rec = bool(re.search(r"\((recomendad[ao]|Recomendad[ao])\)", txt))
            clean = re.sub(r"\s*\((recomendad[ao]|Recomendad[ao])\)", "", txt)
            option_label = re.split(r"\s+—\s+custo\b|\s+Custo:", clean, maxsplit=1)[0].strip(" ;.")
            output.append({"label": option_label, "recommended": rec, "text": txt})
        return output

    @property
    def answered_with_reading(self):
        """True se a `**Resposta:**` em texto livre traz a leitura "lida como" que nomeia a opção (e não é contraproposta)."""
        text = self.answer
        return bool(text) and bool(re.search(r"[Ll]ida como", text)) and not re.search(r"contraproposta|esclarecimento", text)

    @property
    def is_decided(self):
        """Decidida: a linha `**Decidido**`, ou a resposta em texto livre (também a de seleção múltipla) lida como opção."""
        return self.index_decided_line() is not None or self.answered_with_reading


class Round:
    def __init__(self, n, title, sent_on, section):
        self.n = n
        self.title = title
        self.sent_on = sent_on
        self.section = section
        self.file = section.file
        self.questions = []
        self.answered = None   # texto da linha "Respondida em …"
        self.unanswered = False

    @property
    def level(self):
        return self.section.level


def _parse_round(section, m):
    n = int(m.group(1))
    remainder = m.group(2).strip()
    sent_on = None
    md = RE_DATE.search(remainder)
    if md:
        sent_on = md.group(0)
    title = re.sub(r"\s*\([^()]*\)\s*$", "", remainder).strip()
    round_row = Round(n, title, sent_on, section)
    plan_file = section.file
    lines = section.body_outside_fences()
    for i, ln in lines:
        s = ln.strip()
        if re.match(r"^Respondida\b", s) and round_row.answered is None:
            round_row.answered = s
        elif re.match(r"^Sem resposta\b", s):
            round_row.unanswered = True
    # perguntas explícitas `**R<n>.<k>.`
    expl = [(i, int(mm.group(2)), re.sub(r"\*\*", "", ln.strip()))
            for i, ln in lines for mm in [re.match(r"^\*\*R(\d+)\.(\d+)\.", ln.strip())] if mm and int(mm.group(1)) == n]
    mark_texts = []
    if expl:
        for i, k, txt in expl:
            mark_texts.append((i, k, txt, True))
    else:
        for i, ln in lines:
            mm = re.match(r"^(\d+)\.\s+\*\*(.*)$", ln)
            if mm:
                topic = mm.group(2).split("**")[0].strip().rstrip(".:") if "**" in mm.group(2) else mm.group(2).strip()
                mark_texts.append((i, int(mm.group(1)), topic, False))
    if not mark_texts:
        for i, ln in lines:
            if re.match(r"^\*\*Pergunta:\*\*", ln.strip()):
                mark_texts.append((i, 1, ln.strip(), False))
                break
        # a pergunta única que se resolve na rodada inteira
        if mark_texts:
            i, k, topic, ex = mark_texts[0]
            round_row.questions.append(Question(round_row, 1, re.sub(r"^\*\*Pergunta:\*\*\s*", "", topic), i, section.end, plan_file))
            return round_row
    for idx, (i, k, topic, ex) in enumerate(mark_texts):
        end = mark_texts[idx + 1][0] if idx + 1 < len(mark_texts) else section.end
        round_row.questions.append(Question(round_row, k, topic, i, end, plan_file, ex))
    return round_row


class Step:
    def __init__(self, id, title, section):
        self.id = id
        self.title = title
        self.section = section
        self.file = section.file
        self.executes_txt = None
        self.executes = []
        self.executor = None
        self.depends = []
        self.has_estimate = False
        self.estimated_h = None
        self.executed_txt = None
        self.executed_h = None
        self.line_hours = None
        self.checks = []     # (índice, marca, texto)
        self.evidence = None
        self.evidence_at = None
        self.text = section.text()

    @property
    def state(self):
        mark_texts = [c[1].lower() for c in self.checks]
        if mark_texts and all(m == "-" for m in mark_texts):
            return "descartado"
        if mark_texts and all(m in "x-" for m in mark_texts):
            return "feito"
        return "pendente"

    @property
    def executed_filled(self):
        t = (self.executed_txt or "").strip()
        return bool(t) and not re.match(r"^—\s*h?\s*$", t)

    @property
    def where(self):
        return self.file.where(self.section.start)


RE_EXECUTES = re.compile(r"^Executa\b(.*)$")
RE_ESTIMATED = re.compile(r"^Estimado:\s*(.*?)\s*(?:·\s*Executado:\s*(.*))?$")


def _parse_step(section, pid, title, order):
    p = Step(pid, title, section)
    ls = section.body_outside_fences()
    for i, ln in ls:
        s = ln.strip()
        m = RE_EXECUTES.match(s)
        if m and p.executes_txt is None:
            body_text = m.group(1)
            seg = re.split(r"\s·\s", body_text, maxsplit=1)[0]
            p.executes_txt = seg.strip()
            p.executes = sorted(set(re.findall(r"\bD\d+\b", seg)), key=lambda x: int(x[1:]))
            mm = re.search(r"executor:\s*(.*)$", body_text, re.I)
            if mm:
                p.executor = re.split(r"\s·\s", mm.group(1))[0].strip()
        elif re.match(r"^Executor:", s) and p.executor is None:
            p.executor = re.split(r"\s·\s", s[len("Executor:"):].strip())[0].strip()
        mm = re.search(r"depende de ([^·\n]*)", s)
        if mm and not p.depends:
            p.depends = _deps(mm.group(1), order)
        m = RE_ESTIMATED.match(s)
        if m and not p.has_estimate:
            p.has_estimate = True
            p.line_hours = i
            p.estimated_h = parse_hours(m.group(1))
            p.executed_txt = m.group(2) if m.group(2) is not None else ""
            p.executed_h = parse_hours(p.executed_txt)
        mc = RE_CHECK.match(ln)
        if mc:
            p.checks.append((i, mc.group(1), mc.group(2)))
        if s.startswith("**Evidência:**") and p.evidence is None:
            pieces = [s[len("**Evidência:**"):].strip()]
            for j in range(i + 1, section.end):
                nxt = section.file.lines[j]
                if not nxt.strip():
                    break
                pieces.append(nxt.strip())
            p.evidence = " ".join(x for x in pieces if x)
            p.evidence_at = i
    return p


def _deps(txt, order):
    ids = re.findall(r"\b(%s)\b|\ba\s+(%s)\b" % (STEP_ID, STEP_ID), txt)
    output = []
    prior = None
    for a, b in ids:
        if a:
            output.append(a)
            prior = a
        elif b and prior and prior in order and b in order:
            i, j = order.index(prior), order.index(b)
            if i < j:
                output.extend(order[i + 1:j + 1])
            else:
                output.append(b)
    return list(dict.fromkeys(output))


class Plan:
    def __init__(self, root, files):
        self.root = root
        self.files = files
        self.main_file = files[0]
        self.path = self.main_file.path
        self.dir = os.path.dirname(self.path)
        m = re.match(r"^(PLN-\d+)-plan\.md$", self.main_file.name)
        self.id = m.group(1) if m else os.path.basename(self.path)
        self.fm = _frontmatter(self.main_file)
        self._sections = {a.path: a.sections() for a in files}

    # -- as seções --------------------------------------------------------------------------------------------
    def all_sections(self):
        return [s for a in self.files for s in self._sections[a.path]]

    def sections_plan(self):
        return self._sections[self.main_file.path]

    def section(self, regex, level=2, only_plan=True):
        """Primeira seção cujo título casa com `regex`."""
        source_text = self.sections_plan() if only_plan else self.all_sections()
        for s in source_text:
            if s.level == level and re.match(regex, s.title):
                return s
        return None

    def h1(self):
        for s in self.sections_plan():
            if s.level == 1:
                return s.title
        return None

    def text_total(self):
        return "\n".join(a.text for a in self.files)

    # -- os passos ---------------------------------------------------------------------------------------------
    def steps(self):
        if hasattr(self, "_steps"):
            return self._steps
        ss = []
        for s in self.sections_plan():
            if 2 <= s.level <= 4:
                m = RE_PN.match(s.title)
                if m:
                    ss.append((s, m.group(1), m.group(2)))
        order = [p[1] for p in ss]
        self._steps = [_parse_step(s, pid, t, order) for s, pid, t in ss]
        return self._steps

    def step(self, pid):
        for p in self.steps():
            if p.id.lower() == pid.lower():
                return p
        return None

    # -- o Desenho ---------------------------------------------------------------------------------------------
    def design_list(self):
        """Itens `D<n>`: `[{id, title, section, origin_text, origin_ids, alternatives}]`, em todos os arquivos."""
        if hasattr(self, "_designs"):
            return self._designs
        output = []
        for s in self.all_sections():
            if 2 <= s.level <= 4:
                m = RE_DN.match(s.title)
                if m and s.file.role in ("design", "plan"):
                    output.append(self._parse_d(s, m))
        self._designs = output
        return output

    def _parse_d(self, s, m):
        origin_key = None
        ls = s.body_outside_fences()
        for idx, (i, ln) in enumerate(ls):
            if re.match(r"^[-*]\s+\*\*Origem:?\*\*", ln.strip()):
                pieces = [re.sub(r"^[-*]\s+\*\*Origem:?\*\*:?\s*", "", ln.strip())]
                for (j, nxt) in ls[idx + 1:]:
                    if not nxt.strip() or re.match(r"^[-*#]", nxt.strip()):
                        break
                    pieces.append(nxt.strip())
                origin_key = " ".join(pieces)
                break
        rs = []
        if origin_key:
            for mm in RE_R.finditer(origin_key):
                rs.append("R%s" % mm.group(1) + (".%s" % mm.group(2) if mm.group(2) else ""))
        alts = []
        for s2 in self._sections[s.file.path]:
            if s2.start > s.start and s2.end <= s.end and s2.level > s.level:
                ma = RE_AN.match(s2.title)
                if ma:
                    alts.append(ma.group(1))
        return {"id": m.group(1), "title": m.group(2).strip(), "section": s, "origin_text": origin_key,
                "origin_ids": list(dict.fromkeys(rs)), "alternatives": alts}

    def design_text(self, did):
        for d in self.design_list():
            if d["id"] == did:
                return d
        return None

    # -- a Entrevista -------------------------------------------------------------------------------------------
    def rounds(self):
        if hasattr(self, "_rounds"):
            return self._rounds
        output = []
        for s in self.all_sections():
            if s.file.role == "design":
                continue
            if 2 <= s.level <= 4:
                m = RE_ROUND.match(s.title)
                if m:
                    output.append(_parse_round(s, m))
        self._rounds = output
        return output

    def question_text(self, rid):
        m = re.fullmatch(r"R(\d+)\.(\d+)", rid)
        if not m:
            return None
        n, k = int(m.group(1)), int(m.group(2))
        for r in self.rounds():
            if r.n == n:
                for p in r.questions:
                    if p.k == k:
                        return p
        return None

    def round(self, n):
        for r in self.rounds():
            if r.n == n:
                return r
        return None

    def round_ids(self):
        return [p.id for r in self.rounds() for p in r.questions]

    # -- desvios, casos --------------------------------------------------------------------------------------------
    def deviations(self):
        """`[{id, text, where, steps}]`: itens `- **X<n> — …**`, linhas de tabela `| X<n> |` e headings `X<n> —`."""
        if hasattr(self, "_deviations"):
            return self._deviations
        output = []
        for a in self.files:
            sec = None
            for s in self._sections[a.path]:
                if s.level == 2 and re.match(r"^Desvios\b", s.title):
                    sec = s
            for i, ln in enumerate(a.lines):
                if a.fence[i]:
                    continue
                s = ln.strip()
                ids = []
                m = re.match(r"^[-*]\s+\*\*(X\d+)\b", s)
                if m:
                    ids = [m.group(1)]
                else:
                    m = re.match(r"^\|\s*((?:X\d+)(?:\s*,\s*X\d+)*)\s*\|", s)
                    if m:
                        ids = re.findall(r"X\d+", m.group(1))
                    else:
                        m = re.match(r"^#{2,6}\s+(X\d+)\s*[—–-]", s)
                        if m:
                            ids = [m.group(1)]
                if not ids:
                    continue
                txt = [s]
                for nxt in a.lines[i + 1:]:
                    if not nxt.strip() or re.match(r"^([-*]\s|#|\|)", nxt.strip()):
                        break
                    txt.append(nxt.strip())
                text = " ".join(txt)
                for xid in ids:
                    output.append({"id": xid, "text": text, "where": a.where(i),
                                  "steps": sorted(set(re.findall(r"\b%s\b" % STEP_ID, text)))})
        self._deviations = output
        return output

    def cases(self):
        """Linhas `| C<n> |` da tabela de `## Casos manuais`."""
        output = []
        sec = self.section(r"^Casos manuais\b")
        if not sec:
            return output
        for i, ln in sec.body_outside_fences():
            m = re.match(r"^\|\s*(C\d+)\s*\|", ln.strip())
            if m:
                output.append({"id": m.group(1), "where": sec.file.where(i)})
        return output

    def alternatives(self):
        """`["D1/A1", …]`: as alternativas dos itens D, com o escopo do item (A1 repete em cada D)."""
        return ["%s/%s" % (d["id"], a) for d in self.design_list() for a in d["alternatives"]]

    def ids(self):
        return {
            "R": self.round_ids(),
            "D": [d["id"] for d in self.design_list()],
            "P": [p.id for p in self.steps()],
            "X": [x["id"] for x in self.deviations()],
            "A": self.alternatives(),
            "C": [c["id"] for c in self.cases()],
        }

    def has_design(self):
        return bool(self.design_list())

    def is_split(self):
        return len(self.files) > 1


# ------------------------------------------------------------------------------------------------------------------
def git_root(cwd=None):
    """Raiz do worktree: `git rev-parse --show-toplevel`; sem git, sobe até achar uma pasta com `plans/`."""
    cwd = os.path.abspath(cwd or os.getcwd())
    try:
        r = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    d = cwd
    while True:
        if os.path.isdir(os.path.join(d, "plans")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return cwd
        d = parent


def find_plan(ref, root=None):
    """Caminho do `-plan.md` de `PLN-NNN`, de um arquivo ou da pasta do plano."""
    if os.path.isfile(ref):
        return os.path.abspath(ref)
    if os.path.isdir(ref):
        findings = sorted(glob.glob(os.path.join(ref, "PLN-*-plan.md")))
        if findings:
            return os.path.abspath(findings[0])
        raise PlanNotFound("a pasta %s não tem PLN-NNN-plan.md" % ref)
    m = RE_PLN.match(ref.strip())
    if not m:
        raise PlanNotFound("%s não é PLN-NNN nem um caminho existente" % ref)
    num = m.group(1)
    root = root or git_root()
    findings = sorted(glob.glob(os.path.join(root, "plans", "PLN-%s-*" % num, "PLN-%s-plan.md" % num)))
    if not findings:
        raise PlanNotFound("não achei plans/PLN-%s-*/PLN-%s-plan.md em %s" % (num, num, root))
    return findings[0]


def load(ref, root=None):
    if isinstance(ref, Plan):
        return ref
    path = find_plan(ref, root)
    folder = os.path.dirname(path)
    m = re.match(r"^(PLN-\d+)-plan\.md$", os.path.basename(path))
    files = [PlanFile(path, "plan")]
    if m:
        base = m.group(1)
        inter = os.path.join(folder, "%s-interview.md" % base)
        if os.path.isfile(inter):
            files.append(PlanFile(inter, "interview"))
        for d in sorted(glob.glob(os.path.join(folder, "%s-design*.md" % base))):
            files.append(PlanFile(d, "design"))
    if root is None:
        # a raiz do worktree é a pasta acima de `plans/`
        root = os.path.dirname(os.path.dirname(folder)) if os.path.basename(os.path.dirname(folder)) == "plans" else git_root(folder)
    return Plan(root, files)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().split("\n\n")[-1], file=sys.stderr)
        return 2
    try:
        pl = load(argv[0])
    except PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 1
    print(json.dumps({"files": [a.name for a in pl.files], "frontmatter": pl.fm, "ids": pl.ids()},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
