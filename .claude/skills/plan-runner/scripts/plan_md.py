#!/usr/bin/env python3
"""O leitor do plano, comum a `plan_state.py`, `step_request.py`, `round_log.py` e `close_check.py` (PLN-021/D6).

Lê `plans/PLN-NNN-*/PLN-NNN-plan.md` e, quando o plano é dividido, junta `PLN-NNN-interview.md` e `PLN-NNN-design*.md`.
Entende: o frontmatter; as seções `##`; os passos `### Pn` (`Executa`, `Estimado`/`Executado`, checkboxes,
`**Evidência:**`, `depende de`); os itens `### D<n>` com a `Origem`; as alternativas `A<n>` de cada D; as rodadas
`### Rodada N` com as perguntas (`R<n>.<k>`), a escolha, a resposta literal e a reabertura; os desvios `X`, os casos `C`.
Heading dentro de cerca de código não conta.

Uso como módulo:

    import plan_md
    plano = plan_md.carrega("PLN-021")          # ou um caminho de `-plan.md`, ou a pasta do plano
    plano.passos(); plano.desenhos(); plano.rodadas(); plano.ids()

`python3 -I plan_md.py PLN-NNN|caminho` imprime o resumo do que foi lido (depuração). Sem dependências fora da
biblioteca padrão; não precisa do `skillkit`.
"""
import glob
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_PN = re.compile(r"^(P\d+[a-z]?)\s*[—–-]\s*(.*)$")
RE_DN = re.compile(r"^(D\d+)\s*[—–-]?\s*(.*)$")
RE_AN = re.compile(r"^(A\d+)\s*[—–-]\s*(.*)$")
RE_RODADA = re.compile(r"^Rodada\s+(\d+)\b\s*(?:[—–-]\s*)?(.*)$")
RE_DATA = re.compile(r"\d{4}-\d{2}-\d{2}")
RE_R = re.compile(r"\bR(\d+)(?:\.(\d+))?\b")
RE_HORAS = re.compile(r"^\s*[~≈]?\s*(\d+(?:[.,]\d+)?)\s*h\b")
RE_CHECK = re.compile(r"^\s*[-*]\s+\[([ xX-])\]\s*(.*)$")
RE_PLN = re.compile(r"^(?:PLN|pln)-(\d+)$")
PASSO_ID = r"P\d+[a-z]?"


class PlanoNaoEncontrado(Exception):
    pass


def parse_horas(txt):
    """Número de horas de um texto como `11,5 h`, `~4 h (…)`, `0.174 h`; `None` para `— h`, vazio ou texto livre."""
    if txt is None:
        return None
    m = RE_HORAS.match(txt)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def fmt_horas(v):
    """Número no frontmatter: ponto decimal, até 3 casas, sem zeros à direita (`41`, `34.75`, `9.516`)."""
    v = round(float(v), 3)
    if v == int(v):
        return str(int(v))
    return ("%.3f" % v).rstrip("0").rstrip(".")


def _tem_fence(linha):
    s = linha.lstrip()
    return s.startswith("```") or s.startswith("~~~")


class Arquivo:
    def __init__(self, path, papel, texto=None):
        self.path = path
        self.nome = os.path.basename(path)
        self.papel = papel
        if texto is None:
            with open(path, encoding="utf-8") as f:
                texto = f.read()
        self.texto = texto
        self.linhas = texto.split("\n")
        self.fence = []
        dentro = False
        for ln in self.linhas:
            if _tem_fence(ln):
                self.fence.append(True)
                dentro = not dentro
            else:
                self.fence.append(dentro)
        self.fm_fim = self._acha_fm()

    def _acha_fm(self):
        """Índice da linha do segundo `---` do frontmatter, ou -1."""
        if not self.linhas or self.linhas[0].strip() != "---":
            return -1
        for i in range(1, len(self.linhas)):
            if self.linhas[i].strip() == "---":
                return i
        return -1

    def headings(self):
        saida = []
        for i, ln in enumerate(self.linhas):
            if self.fence[i]:
                continue
            m = RE_HEADING.match(ln)
            if m:
                saida.append((i, len(m.group(1)), m.group(2)))
        return saida

    def secoes(self):
        hs = self.headings()
        saida = []
        for idx, (i, nivel, titulo) in enumerate(hs):
            fim = len(self.linhas)
            for (j, n2, _t) in hs[idx + 1:]:
                if n2 <= nivel:
                    fim = j
                    break
            saida.append(Secao(self, nivel, titulo, i, fim))
        return saida

    def onde(self, i):
        return "%s:%d" % (self.nome, i + 1)


class Secao:
    def __init__(self, arquivo, nivel, titulo, ini, fim):
        self.arquivo = arquivo
        self.nivel = nivel
        self.titulo = titulo
        self.ini = ini      # índice da linha do heading
        self.fim = fim      # exclusivo

    @property
    def linhas(self):
        return self.arquivo.linhas[self.ini:self.fim]

    @property
    def corpo(self):
        return self.arquivo.linhas[self.ini + 1:self.fim]

    def corpo_sem_cerca(self):
        """(índice absoluto, linha) das linhas do corpo fora de cerca de código."""
        return [(i, self.arquivo.linhas[i]) for i in range(self.ini + 1, self.fim) if not self.arquivo.fence[i]]

    def texto(self):
        return "\n".join(self.corpo).strip("\n")

    def onde(self):
        return self.arquivo.onde(self.ini)


def _frontmatter(arq):
    if arq.fm_fim < 0:
        return {}
    fm = {}
    chave = None
    for ln in arq.linhas[1:arq.fm_fim]:
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", ln)
        if m and not ln.startswith(" "):
            chave, val = m.group(1), m.group(2).strip()
            if val == "":
                fm[chave] = []
            else:
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                fm[chave] = val
            continue
        m = re.match(r"^\s+-\s+(.*)$", ln)
        if m and chave is not None and isinstance(fm.get(chave), list):
            fm[chave].append(m.group(1).strip())
    return fm


class Pergunta:
    def __init__(self, rodada, k, tema, ini, fim, arquivo, explicita=False):
        self.rodada = rodada
        self.n = rodada.n
        self.k = k
        self.id = "R%d.%d" % (rodada.n, k)
        self.tema = tema
        self.ini = ini
        self.fim = fim
        self.arquivo = arquivo
        self.explicita = explicita

    @property
    def linhas(self):
        return self.arquivo.linhas[self.ini:self.fim]

    @property
    def bloco(self):
        return "\n".join(self.linhas).rstrip()

    def _linha_que_comeca(self, regex):
        for i in range(self.ini, self.fim):
            if self.arquivo.fence[i]:
                continue
            if re.match(regex, self.arquivo.linhas[i].strip()):
                return i
        return None

    def indice_decidido(self):
        return self._linha_que_comeca(r"\*\*(Decidid[oa]|Escolhid[oa])\b")

    def indice_resposta(self):
        return self._linha_que_comeca(r"\*\*Resposta\b")

    @property
    def decidido(self):
        i = self.indice_decidido()
        return self.arquivo.linhas[i].strip() if i is not None else None

    @property
    def resposta(self):
        i = self.indice_resposta()
        if i is None:
            return None
        partes = [self.arquivo.linhas[i].strip()]
        for j in range(i + 1, self.fim):
            ln = self.arquivo.linhas[j]
            if not ln.strip() or ln.lstrip().startswith("**"):
                break
            partes.append(ln.strip())
        return " ".join(partes)

    @property
    def reaberta(self):
        m = re.search(r"reaberta em (R\d+\.\d+)", self.bloco)
        return m.group(1) if m else None

    def opcoes(self):
        """Opções em bullets `-` recuados, logo abaixo do enunciado; a linha que quebra continua a opção."""
        brutas = []
        aberta = False
        for i in range(self.ini + 1, self.fim):
            if self.arquivo.fence[i]:
                continue
            ln = self.arquivo.linhas[i]
            m = re.match(r"^\s{1,}[-*]\s+(.*)$", ln)
            if m:
                brutas.append([m.group(1).strip()])
                aberta = True
            elif not ln.strip():
                continue
            elif aberta and re.match(r"^\s{2,}\S", ln) and not ln.strip().startswith("**"):
                brutas[-1].append(ln.strip())
            else:
                aberta = False  # parágrafo fora da lista: fecha a continuação
        saida = []
        for b in brutas:
            txt = " ".join(b)
            rec = bool(re.search(r"\((recomendad[ao]|Recomendad[ao])\)", txt))
            limpo = re.sub(r"\s*\((recomendad[ao]|Recomendad[ao])\)", "", txt)
            rot = re.split(r"\s+—\s+custo\b|\s+Custo:", limpo, maxsplit=1)[0].strip(" ;.")
            saida.append({"rotulo": rot, "recomendada": rec, "texto": txt})
        return saida

    @property
    def decidida(self):
        return self.indice_decidido() is not None


class Rodada:
    def __init__(self, n, titulo, enviada, secao):
        self.n = n
        self.titulo = titulo
        self.enviada = enviada
        self.secao = secao
        self.arquivo = secao.arquivo
        self.perguntas = []
        self.respondida = None   # texto da linha "Respondida em …"
        self.sem_resposta = False

    @property
    def nivel(self):
        return self.secao.nivel


def _parse_rodada(secao, m):
    n = int(m.group(1))
    resto = m.group(2).strip()
    enviada = None
    md = RE_DATA.search(resto)
    if md:
        enviada = md.group(0)
    titulo = re.sub(r"\s*\([^()]*\)\s*$", "", resto).strip()
    rod = Rodada(n, titulo, enviada, secao)
    arq = secao.arquivo
    linhas = secao.corpo_sem_cerca()
    for i, ln in linhas:
        s = ln.strip()
        if re.match(r"^Respondida\b", s) and rod.respondida is None:
            rod.respondida = s
        elif re.match(r"^Sem resposta\b", s):
            rod.sem_resposta = True
    # perguntas explícitas `**R<n>.<k>.`
    expl = [(i, int(mm.group(2)), re.sub(r"\*\*", "", ln.strip()))
            for i, ln in linhas for mm in [re.match(r"^\*\*R(\d+)\.(\d+)\.", ln.strip())] if mm and int(mm.group(1)) == n]
    marcas = []
    if expl:
        for i, k, txt in expl:
            marcas.append((i, k, txt, True))
    else:
        for i, ln in linhas:
            mm = re.match(r"^(\d+)\.\s+\*\*(.*)$", ln)
            if mm:
                tema = mm.group(2).split("**")[0].strip().rstrip(".:") if "**" in mm.group(2) else mm.group(2).strip()
                marcas.append((i, int(mm.group(1)), tema, False))
    if not marcas:
        for i, ln in linhas:
            if re.match(r"^\*\*Pergunta:\*\*", ln.strip()):
                marcas.append((i, 1, ln.strip(), False))
                break
        # a pergunta única que se resolve na rodada inteira
        if marcas:
            i, k, tema, ex = marcas[0]
            rod.perguntas.append(Pergunta(rod, 1, re.sub(r"^\*\*Pergunta:\*\*\s*", "", tema), i, secao.fim, arq))
            return rod
    for idx, (i, k, tema, ex) in enumerate(marcas):
        fim = marcas[idx + 1][0] if idx + 1 < len(marcas) else secao.fim
        rod.perguntas.append(Pergunta(rod, k, tema, i, fim, arq, ex))
    return rod


class Passo:
    def __init__(self, id, titulo, secao):
        self.id = id
        self.titulo = titulo
        self.secao = secao
        self.arquivo = secao.arquivo
        self.executa_txt = None
        self.executa = []
        self.executor = None
        self.depende = []
        self.tem_estimado = False
        self.estimado_h = None
        self.executado_txt = None
        self.executado_h = None
        self.linha_horas = None
        self.checks = []     # (índice, marca, texto)
        self.evidencia = None
        self.evidencia_ini = None
        self.texto = secao.texto()

    @property
    def estado(self):
        marcas = [c[1].lower() for c in self.checks]
        if marcas and all(m == "-" for m in marcas):
            return "descartado"
        if marcas and all(m in "x-" for m in marcas):
            return "feito"
        return "pendente"

    @property
    def executado_preenchido(self):
        t = (self.executado_txt or "").strip()
        return bool(t) and not re.match(r"^—\s*h?\s*$", t)

    @property
    def onde(self):
        return self.arquivo.onde(self.secao.ini)


RE_EXECUTA = re.compile(r"^Executa\b(.*)$")
RE_ESTIMADO = re.compile(r"^Estimado:\s*(.*?)\s*(?:·\s*Executado:\s*(.*))?$")


def _parse_passo(secao, pid, titulo, ordem):
    p = Passo(pid, titulo, secao)
    ls = secao.corpo_sem_cerca()
    for i, ln in ls:
        s = ln.strip()
        m = RE_EXECUTA.match(s)
        if m and p.executa_txt is None:
            corpo = m.group(1)
            seg = re.split(r"\s·\s", corpo, maxsplit=1)[0]
            p.executa_txt = seg.strip()
            p.executa = sorted(set(re.findall(r"\bD\d+\b", seg)), key=lambda x: int(x[1:]))
            mm = re.search(r"executor:\s*(.*)$", corpo, re.I)
            if mm:
                p.executor = re.split(r"\s·\s", mm.group(1))[0].strip()
        elif re.match(r"^Executor:", s) and p.executor is None:
            p.executor = re.split(r"\s·\s", s[len("Executor:"):].strip())[0].strip()
        mm = re.search(r"depende de ([^·\n]*)", s)
        if mm and not p.depende:
            p.depende = _deps(mm.group(1), ordem)
        m = RE_ESTIMADO.match(s)
        if m and not p.tem_estimado:
            p.tem_estimado = True
            p.linha_horas = i
            p.estimado_h = parse_horas(m.group(1))
            p.executado_txt = m.group(2) if m.group(2) is not None else ""
            p.executado_h = parse_horas(p.executado_txt)
        mc = RE_CHECK.match(ln)
        if mc:
            p.checks.append((i, mc.group(1), mc.group(2)))
        if s.startswith("**Evidência:**") and p.evidencia is None:
            partes = [s[len("**Evidência:**"):].strip()]
            for j in range(i + 1, secao.fim):
                nxt = secao.arquivo.linhas[j]
                if not nxt.strip():
                    break
                partes.append(nxt.strip())
            p.evidencia = " ".join(x for x in partes if x)
            p.evidencia_ini = i
    return p


def _deps(txt, ordem):
    ids = re.findall(r"\b(%s)\b|\ba\s+(%s)\b" % (PASSO_ID, PASSO_ID), txt)
    saida = []
    ant = None
    for a, b in ids:
        if a:
            saida.append(a)
            ant = a
        elif b and ant and ant in ordem and b in ordem:
            i, j = ordem.index(ant), ordem.index(b)
            if i < j:
                saida.extend(ordem[i + 1:j + 1])
            else:
                saida.append(b)
    return list(dict.fromkeys(saida))


class Plano:
    def __init__(self, raiz, arquivos):
        self.raiz = raiz
        self.arquivos = arquivos
        self.principal = arquivos[0]
        self.path = self.principal.path
        self.dir = os.path.dirname(self.path)
        m = re.match(r"^(PLN-\d+)-plan\.md$", self.principal.nome)
        self.id = m.group(1) if m else os.path.basename(self.path)
        self.fm = _frontmatter(self.principal)
        self._secoes = {a.path: a.secoes() for a in arquivos}

    # -- as seções --------------------------------------------------------------------------------------------
    def todas_secoes(self):
        return [s for a in self.arquivos for s in self._secoes[a.path]]

    def secoes_plan(self):
        return self._secoes[self.principal.path]

    def secao(self, regex, nivel=2, so_plano=True):
        """Primeira seção cujo título casa com `regex`."""
        fonte = self.secoes_plan() if so_plano else self.todas_secoes()
        for s in fonte:
            if s.nivel == nivel and re.match(regex, s.titulo):
                return s
        return None

    def h1(self):
        for s in self.secoes_plan():
            if s.nivel == 1:
                return s.titulo
        return None

    def texto_total(self):
        return "\n".join(a.texto for a in self.arquivos)

    # -- os passos ---------------------------------------------------------------------------------------------
    def passos(self):
        if hasattr(self, "_passos"):
            return self._passos
        ss = []
        for s in self.secoes_plan():
            if 2 <= s.nivel <= 4:
                m = RE_PN.match(s.titulo)
                if m:
                    ss.append((s, m.group(1), m.group(2)))
        ordem = [p[1] for p in ss]
        self._passos = [_parse_passo(s, pid, t, ordem) for s, pid, t in ss]
        return self._passos

    def passo(self, pid):
        for p in self.passos():
            if p.id.lower() == pid.lower():
                return p
        return None

    # -- o Desenho ---------------------------------------------------------------------------------------------
    def desenhos(self):
        """Itens `D<n>`: `[{id, titulo, secao, origem_txt, origem_rs, alternativas}]`, em todos os arquivos."""
        if hasattr(self, "_desenhos"):
            return self._desenhos
        saida = []
        for s in self.todas_secoes():
            if 2 <= s.nivel <= 4:
                m = RE_DN.match(s.titulo)
                if m and s.arquivo.papel in ("design", "plan"):
                    saida.append(self._parse_d(s, m))
        self._desenhos = saida
        return saida

    def _parse_d(self, s, m):
        origem = None
        ls = s.corpo_sem_cerca()
        for idx, (i, ln) in enumerate(ls):
            if re.match(r"^[-*]\s+\*\*Origem:?\*\*", ln.strip()):
                partes = [re.sub(r"^[-*]\s+\*\*Origem:?\*\*:?\s*", "", ln.strip())]
                for (j, nxt) in ls[idx + 1:]:
                    if not nxt.strip() or re.match(r"^[-*#]", nxt.strip()):
                        break
                    partes.append(nxt.strip())
                origem = " ".join(partes)
                break
        rs = []
        if origem:
            for mm in RE_R.finditer(origem):
                rs.append("R%s" % mm.group(1) + (".%s" % mm.group(2) if mm.group(2) else ""))
        alts = []
        for s2 in self._secoes[s.arquivo.path]:
            if s2.ini > s.ini and s2.fim <= s.fim and s2.nivel > s.nivel:
                ma = RE_AN.match(s2.titulo)
                if ma:
                    alts.append(ma.group(1))
        return {"id": m.group(1), "titulo": m.group(2).strip(), "secao": s, "origem_txt": origem,
                "origem_rs": list(dict.fromkeys(rs)), "alternativas": alts}

    def desenho(self, did):
        for d in self.desenhos():
            if d["id"] == did:
                return d
        return None

    # -- a Entrevista -------------------------------------------------------------------------------------------
    def rodadas(self):
        if hasattr(self, "_rodadas"):
            return self._rodadas
        saida = []
        for s in self.todas_secoes():
            if s.arquivo.papel == "design":
                continue
            if 2 <= s.nivel <= 4:
                m = RE_RODADA.match(s.titulo)
                if m:
                    saida.append(_parse_rodada(s, m))
        self._rodadas = saida
        return saida

    def pergunta(self, rid):
        m = re.fullmatch(r"R(\d+)\.(\d+)", rid)
        if not m:
            return None
        n, k = int(m.group(1)), int(m.group(2))
        for r in self.rodadas():
            if r.n == n:
                for p in r.perguntas:
                    if p.k == k:
                        return p
        return None

    def rodada(self, n):
        for r in self.rodadas():
            if r.n == n:
                return r
        return None

    def ids_r(self):
        return [p.id for r in self.rodadas() for p in r.perguntas]

    # -- desvios, casos --------------------------------------------------------------------------------------------
    def desvios(self):
        """`[{id, texto, onde, passos}]`: itens `- **X<n> — …**`, linhas de tabela `| X<n> |` e headings `X<n> —`."""
        if hasattr(self, "_desvios"):
            return self._desvios
        saida = []
        for a in self.arquivos:
            sec = None
            for s in self._secoes[a.path]:
                if s.nivel == 2 and re.match(r"^Desvios\b", s.titulo):
                    sec = s
            for i, ln in enumerate(a.linhas):
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
                for nxt in a.linhas[i + 1:]:
                    if not nxt.strip() or re.match(r"^([-*]\s|#|\|)", nxt.strip()):
                        break
                    txt.append(nxt.strip())
                texto = " ".join(txt)
                for xid in ids:
                    saida.append({"id": xid, "texto": texto, "onde": a.onde(i),
                                  "passos": sorted(set(re.findall(r"\b%s\b" % PASSO_ID, texto)))})
        self._desvios = saida
        return saida

    def casos(self):
        """Linhas `| C<n> |` da tabela de `## Casos manuais`."""
        saida = []
        sec = self.secao(r"^Casos manuais\b")
        if not sec:
            return saida
        for i, ln in sec.corpo_sem_cerca():
            m = re.match(r"^\|\s*(C\d+)\s*\|", ln.strip())
            if m:
                saida.append({"id": m.group(1), "onde": sec.arquivo.onde(i)})
        return saida

    def alternativas(self):
        """`["D1/A1", …]`: as alternativas dos itens D, com o escopo do item (A1 repete em cada D)."""
        return ["%s/%s" % (d["id"], a) for d in self.desenhos() for a in d["alternativas"]]

    def ids(self):
        return {
            "R": self.ids_r(),
            "D": [d["id"] for d in self.desenhos()],
            "P": [p.id for p in self.passos()],
            "X": [x["id"] for x in self.desvios()],
            "A": self.alternativas(),
            "C": [c["id"] for c in self.casos()],
        }

    def tem_desenho(self):
        return bool(self.desenhos())

    def dividido(self):
        return len(self.arquivos) > 1


# ------------------------------------------------------------------------------------------------------------------
def raiz_git(cwd=None):
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
        pai = os.path.dirname(d)
        if pai == d:
            return cwd
        d = pai


def acha_plano(ref, raiz=None):
    """Caminho do `-plan.md` de `PLN-NNN`, de um arquivo ou da pasta do plano."""
    if os.path.isfile(ref):
        return os.path.abspath(ref)
    if os.path.isdir(ref):
        achados = sorted(glob.glob(os.path.join(ref, "PLN-*-plan.md")))
        if achados:
            return os.path.abspath(achados[0])
        raise PlanoNaoEncontrado("a pasta %s não tem PLN-NNN-plan.md" % ref)
    m = RE_PLN.match(ref.strip())
    if not m:
        raise PlanoNaoEncontrado("%s não é PLN-NNN nem um caminho existente" % ref)
    num = m.group(1)
    raiz = raiz or raiz_git()
    achados = sorted(glob.glob(os.path.join(raiz, "plans", "PLN-%s-*" % num, "PLN-%s-plan.md" % num)))
    if not achados:
        raise PlanoNaoEncontrado("não achei plans/PLN-%s-*/PLN-%s-plan.md em %s" % (num, num, raiz))
    return achados[0]


def carrega(ref, raiz=None):
    if isinstance(ref, Plano):
        return ref
    path = acha_plano(ref, raiz)
    pasta = os.path.dirname(path)
    m = re.match(r"^(PLN-\d+)-plan\.md$", os.path.basename(path))
    arquivos = [Arquivo(path, "plan")]
    if m:
        base = m.group(1)
        inter = os.path.join(pasta, "%s-interview.md" % base)
        if os.path.isfile(inter):
            arquivos.append(Arquivo(inter, "interview"))
        for d in sorted(glob.glob(os.path.join(pasta, "%s-design*.md" % base))):
            arquivos.append(Arquivo(d, "design"))
    if raiz is None:
        # a raiz do worktree é a pasta acima de `plans/`
        raiz = os.path.dirname(os.path.dirname(pasta)) if os.path.basename(os.path.dirname(pasta)) == "plans" else raiz_git(pasta)
    return Plano(raiz, arquivos)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().split("\n\n")[-1], file=sys.stderr)
        return 2
    try:
        pl = carrega(argv[0])
    except PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 1
    print(json.dumps({"arquivos": [a.nome for a in pl.arquivos], "frontmatter": pl.fm, "ids": pl.ids()},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
