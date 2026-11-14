#!/usr/bin/env python3
"""tally.py: tira dos worklogs das personas e das medições o estado de uma rodada da reunião.

Uso:
    tally.py <N> --reuniao reuniao.json [--root DIR] [--measurements PATH] [--sessions PATH]
             [--codex-dir DIR] [--out PATH|-] [--exclude-rater NOME ...] [--md|--json]
             [--opened HH:MM:SS] [--closed HH:MM:SS] [--at HH:MM:SS] [--participantes NOME ...] [--settle SEG]

`--root` padrão: o topo do repositório git do cwd (`git rev-parse --show-toplevel`; sem git, o cwd); o manifesto relativo
resolve contra ele. Sem nenhum worklog sob a raiz, sai com rc 2 e erro explícito (nunca "falta" em silêncio). Sem
`--opened`/`--closed` o custo e a latência dos Claude são o TOTAL DA SESSÃO: o aviso vai a stderr, o JSON traz
`rodada.custo_rotulo: "total da sessão"` (com a janela, "da rodada") e a lista `avisos`; o turno do Codex só se mede com a
janela (por posição erraria com um turno a mais). Por persona, o manifesto aceita `claude_session`, `provider_session`
(sobrescrevem o mapa) e `dispatch_id`; sem nenhum id, `medicao_aviso`. Os ids vêm do mapa do `brza sessions` v2
(`sessions_map.fold_map`: `open` + `session` do mesmo nome, também depois do `close`); NADA aqui lê transcript.

MEDIÇÃO PENDENTE (X4): o hook grava o turno do Claude no Stop. Persona Claude que respondeu, com id, sem turno na janela e
com o fim da rodada (`--closed`, ou a hora da resposta) a menos de 120 s de `--at`/agora fica `medicao: "pendente"`,
`custo_usd: None` e o aviso "medição pendente: … rode de novo em ~1 min"; nunca 0 e nunca "sem medição". `--settle SEG`
relê o `measurements.jsonl` a cada 5 s até as pendentes ganharem a linha. Fora dos 120 s, é "sem medição".
`--participantes` (X18): quem está fora fica `estado: "fora da rodada"`, sem medição, fora da sala e do "x/n".

Só biblioteca padrão. Grava `<root>/<dir>/estado-r<N>.json` (ou `--out`; `--out -` não grava) e imprime a tabela
Markdown do chat da coordenação (`--md`, padrão) ou o JSON (`--json`).

Como biblioteca (o `panel.py` faz `sys.path.insert` e `import tally`):
    build_estado(reuniao, n, root, *, measurements=None, sessions=None, codex_dir=None,
                 exclude_raters=(), opened=None, closed=None, at=None, participantes=None, settle=0) -> dict
    render_md(estado) -> str
    parse_worklog(text, names=()) -> dict
    measure_claude(...), measure_codex(...)   # devolvem cost_usd, latency_s, end, failed e tokens; _legacy_measure traduz para as chaves que o tally grava
    stats(valores)

O MANIFESTO `reuniao.json` (caminhos relativos a `--root`):
    {"id": "reuniao-mcp-remoto", "tema": "...", "decisor": "Anderson", "fim": "22h15",
     "data": "2026-11-07",                       # opcional: o dia de `--opened/--closed` em HH:MM:SS (padrão: hoje)
     "checkout": ".worktrees/playground",
     "dir": ".sessions/reuniao-mcp-remoto",      # onde ficam prompts, sintese-N.json e estado-rN.json
     "worklog": "work/worklogs/2026-11-07-reuniao-mcp-remoto-{slug}.md",   # {slug}, {nome} e {sessao} valem
     "briefing": "briefing.md",                  # opcional, usado pelo launch_persona.py
     "personas": [{"nome": "Muralha", "slug": "muralha", "papel": "Arquiteta de Rede e Segurança",
                   "sessao": "mcp-muralha",      # o `name` do sessions.jsonl
                   "runtime": "claude",          # claude | codex | grok | antigravity
                   "modelo": "opus-5.5",         # "-" ou null: sem --model (Antigravity recusa modelo explícito)
                   "esforco": "high",            # "-" ou null: sem --effort
                   "prompt": "prompt-muralha.txt",   # relativo a `dir`; opcional
                   "fallback": {"runtime": "claude", "modelo": "sonnet-5.5", "esforco": "medium"}}]}

O ESTADO (`estado-rN.json`) tem `reuniao`, `rodada`, `personas[]`, `sala`, `custos_coordenacao` e as listas
`medicoes`, `sintese`, `decisoes` vazias, que o `panel.py` preenche. Por persona, além do que o `estado-r3.json` já
tinha: `confianca_r1`, `confianca_fonte`, `voto`, `nota_colegas`, `nota_rodada`, `posicao_fonte`, `janela`.

DE ONDE SAI A `confianca` DE UMA RODADA (a primeira regra que achar vale; `confianca_fonte` diz qual):
  1. `plano`: a linha `| O plano inteiro | ... |` de qualquer tabela da seção; vale a ÚLTIMA célula numérica (nas
     tabelas "confiança na v1 | na v2" é a da versão nova). É o caso de Carvão R5 e de MCP R3, R4 e R6.
  2. `plano-linha`: a linha `Confiança no plano inteiro (...): NN` (Carvão R7).
  3. `voto`: a média da coluna "Confiança" da tabela `#### O voto em cada proposta` (Carvão R3).
  4. `placar`: a média da última coluna "Confiança..." de `#### Placar da rodada N` (R1 e R2 das duas reuniões).
  5. `confianca-linha`: a linha `**Confiança:** NN/100` (MCP R5; o primeiro número da linha). Fica por último porque
     a R1 também tem essa linha, por assunto, e ali vale o placar.
  Rodada sem nenhuma das cinco (Carvão R4, R6, R6b; MCP R5 de quem não escreveu a linha) fica com `None`.
  `confianca_r1` é sempre a regra 4 (placar) aplicada à Rodada 1.

A `posicao` é a primeira linha `- **Posição:** ...` da seção (sem os marcadores de ênfase, até 100 caracteres com "…");
sem ela, o "porquê" da linha `O plano inteiro` (`posicao_fonte: "plano"`); sem os dois, `None`.

AS NOTAS AOS COLEGAS (extraídas da rodada mais nova ≤ N que as tenha; a rodada vai em `nota_rodada`):
  - Carvão R3: `#### Os colegas`, tabela "Persona | contribuição | nota".
  - MCP R3: a linha `**Nota aos colegas:**` e o bloco até a primeira linha em branco, em lista ou numa linha só;
    cada colega vira a primeira ocorrência `Nome <nota>[/10]` ("Régua 9 —", "**Régua (10/10):**", "Muralha: 9.").
  `--exclude-rater NOME` tira as notas que NOME deu (a conta da coordenação de Carvão não tinha as da Faísca).

ESTADO DA PERSONA: `respondeu` se a última linha não vazia do worklog (sem recuo) é `<!-- fim-rodada-M -->` com M >= N e a
seção da rodada N existe; `sem dado` se o marcador é de uma rodada adiante e não há seção N (entregou junto com a seguinte);
`falta` se não; `sem cota` se faltou e o rollout do
Codex mostra o erro de limite; persona sem worklog é `falta`. O `panel.py` refina `atrasado` e `erro`.

A MEDIÇÃO: Claude = soma de `estimated_cost_usd` e `duration_s` dos eventos `turn` e `subagent` do `measurements.jsonl`
cujo `session_id` é o `claude_session` que o `sessions.jsonl` liga ao `sessao` da persona, com `timestamp` entre
`opened` e `closed` + 60 s. Codex = o rollout `*-<provider_session>.jsonl` de `--codex-dir`: latência do turno
(`task_complete` - `task_started`) e a diferença do `total_token_usage` para o fim do turno anterior. Grok e
Antigravity não têm custo nem tokens. A latência sem turno medido sai do mtime do worklog contra `opened`, e só quando
o marcador de N é a última linha (`latencia_fonte: "≈ mtime"`). Sem janela (`opened` e `closed`), Claude devolve o total
e `janela: false`.

A SALA (`calc_sala`, a conta única que o `panel.py` também usa): só quem `respondeu` entra. `media`, `mediana`, `n`, `faixa`
e `media_todas`/`mediana_todas` (com todos). A média e a mediana tiram o
Antigravity (E-1), que fica à parte em `sala.antigravity` com `fora_da_media: true`. `sala.revisor` e `revisor_nota`
vêm de `<dir>/sintese-<N>.json` (aninhados em `sala` ou soltos) quando existir; `diferenca_revisor` = media - revisor.
"""
import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import time as _time
from datetime import date, datetime, time, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
import common  # noqa: E402  (a leitura do marcador de fim de rodada é a mesma do `wait_round.py`)
import sessions_map  # noqa: E402  (a identidade da persona vem do mapa do `brza sessions` v2, em um lugar só)
from skillkit.measure import (codex_turns, find_rollout, load_jsonl, measure_claude, measure_codex,  # noqa: E402,F401
                              parse_ts, session_ids, win_bounds)

def _legacy_measure(med):
    """Traduz o retorno em inglês do skillkit para as chaves que esta skill já grava."""
    if not med:
        return med
    tokens = med.get("tokens")
    if tokens:
        tokens = {"entrada": tokens.get("input_tokens"), "cache": tokens.get("cache"),
                  "saida": tokens.get("output_tokens")}
    return {"custo_usd": med.get("cost_usd"), "latencia_s": med.get("latency_s"), "fim": med.get("end"),
            "erro": med.get("failed"), "tokens": tokens, "events": med.get("events")}


RUNTIME_NOME = {"claude": "Claude", "codex": "Codex", "grok": "Grok", "antigravity": "Antigravity"}
NUM_CELL = re.compile(r"^\**\s*(\d+(?:[.,]\d+)?)\s*\**\s*(?:/\s*\**\s*(?:10|100)\s*\**|%)?\s*$")
MARCADOR = re.compile(r"^<!-- fim-rodada-(\d+) -->$")
H_RODADA = re.compile(r"^#{2,3}\s+Rodada\s+(\d+)\s*(?:[:—–-]\s*)?(.*?)\s*$")
PLANO_INTEIRO = re.compile(r"^o plano inteiro\b")
# nota em prosa: `N/10`, `N / 10`, ou o número solto desde que logo depois venha pontuação ou o fim (nunca "3 vezes")
NOTA_PROSA = r"(\d+(?:[.,]\d+)?)(?:\s*/\s*10\b|(?=\s*(?:[—–:.;,()\-]|$)))"


# ---------------------------------------------------------------- a raiz e o manifesto

def raiz_padrao():
    """A raiz padrão de todos os scripts: `git rev-parse --show-toplevel` do cwd; sem git, o cwd."""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return os.getcwd()


def resolve_reuniao(arg, root):
    """Caminho do manifesto: relativo, resolve contra a raiz; se não existir lá, vale o caminho como veio (cwd)."""
    if os.path.isabs(arg):
        return arg
    p = os.path.join(root, arg)
    return p if os.path.isfile(p) else arg


def worklogs_existentes(reuniao, root):
    return [p["nome"] for p in reuniao["personas"] if os.path.isfile(os.path.join(root, worklog_path(reuniao, p)))]


# ---------------------------------------------------------------- texto e tabelas

def to_num(cell):
    """Número de uma célula ('68', '**68**', '74/100', '9,5'); None se não for número."""
    m = NUM_CELL.match((cell or "").strip())
    return float(m.group(1).replace(",", ".")) if m else None


def split_cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def parse_table(lines, start):
    """Primeira tabela a partir de `start` (pula linhas em branco; para em outro título). -> (cabeçalho, linhas)."""
    i = start
    while i < len(lines) and not lines[i].lstrip().startswith("|"):
        if lines[i].startswith("#") or i - start > 6:
            return [], []
        i += 1
    header, rows = [], []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        cells = split_cells(lines[i])
        if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells if c):
            pass
        elif not header:
            header = cells
        else:
            rows.append(cells)
        i += 1
    return header, rows


def find_line(lines, pattern):
    rx = re.compile(pattern)
    for i, line in enumerate(lines):
        if rx.search(line):
            return i
    return None


def col(header, prefix, last=False):
    idx = [i for i, h in enumerate(header) if h.replace("*", "").strip().lower().startswith(prefix)]
    if not idx:
        return None
    return idx[-1] if last else idx[0]


def mean(values):
    values = [v for v in values if v is not None]
    return round(sum(values) / len(values), 1) if values else None


def clean_md(s):
    s = re.sub(r"^\*[^*]{1,40}\*\s*[:—-]\s*", "", s.strip())
    return s.replace("**", "").strip()


def truncate(s, limit=100):
    s = " ".join(s.split())
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


# ---------------------------------------------------------------- o worklog

def split_rounds(text):
    """{N: {"linha", "titulo", "lines"}}: cada `### Rodada N: ...` vai até o próximo título de nível 2 ou 3."""
    lines = text.split("\n")
    heads = [i for i, l in enumerate(lines) if re.match(r"^##{1,2}\s", l) or re.match(r"^# ", l)]
    out = {}
    for i, l in enumerate(lines):
        m = H_RODADA.match(l)
        if not m or int(m.group(1)) in out:
            continue
        fim = next((h for h in heads if h > i), len(lines))
        out[int(m.group(1))] = {"linha": i + 1, "titulo": m.group(2), "lines": lines[i + 1: fim]}
    return out


VOTO_PALAVRA = {"apoio": "apoio", "ressalva": "apoio com ressalva", "contra": "contra"}


def classify_vote(cell):
    c = cell.replace("*", "").strip().lower()
    if c.startswith("contra"):
        return "contra"
    if "ressalva" in c:
        return "ressalva"
    if c.startswith("apoio"):
        return "apoio"
    return None


def parse_notes_table(lines, avisos=None):
    """Tabela `#### Os colegas`: a coluna do nome e a da nota se acham pelo cabeçalho, não pela posição."""
    i = find_line(lines, r"^####\s+Os colegas")
    if i is None:
        return None
    header, rows = parse_table(lines, i + 1)
    ci = col(header, "nota", last=True)
    if ci is None:
        if avisos is not None:
            avisos.append("tabela 'Os colegas' sem coluna 'Nota' no cabeçalho: notas ignoradas")
        return None
    ni = next((x for x in (col(header, "persona"), col(header, "colega"), col(header, "nome")) if x is not None), 0)
    notas = {}
    for r in rows:
        if len(r) <= max(ci, ni):
            continue
        nome, v = r[ni].replace("*", "").strip(), to_num(r[ci])
        if v is None:
            continue
        if to_num(nome) is not None or not nome or v > 10:
            if avisos is not None:
                avisos.append(f"nota ignorada na tabela 'Os colegas': {truncate(' | '.join(r), 60)}")
            continue
        notas[nome] = v
    return notas or None


def parse_notes_prose(lines, names, avisos=None):
    i = find_line(lines, r"Nota aos colegas")
    if i is None or not names:
        return None
    bloco = []
    for l in lines[i:]:
        if not l.strip() and bloco:
            break
        if MARCADOR.match(l.strip()) or l.startswith("#"):
            break
        bloco.append(l)
    texto = "\n".join(bloco)
    notas = {}
    for nome in names:
        m = re.search(r"(?<!\w)" + re.escape(nome) + r"(?!\w)[\W_]{0,8}?" + NOTA_PROSA, texto)
        v = float(m.group(1).replace(",", ".")) if m else None
        if v is not None and v <= 10:
            notas[nome] = v
        elif re.search(r"(?<!\w)" + re.escape(nome) + r"(?!\w)", texto) and avisos is not None:
            avisos.append(f"nota aos colegas sem número claro para {nome}: ignorada")
    return notas or None


def parse_round(lines, names=()):
    """Extrai de uma seção de rodada: placar, voto, plano, confiança, posição e notas."""
    r = {"placar_conf": None, "virada": None, "voto": None, "plano": None, "plano_porque": None,
         "confianca": None, "confianca_fonte": None, "posicao": None, "posicao_fonte": None, "notas": None,
         "fatos_lidos": None, "voto_por_proposta": None, "avisos": []}
    # placar
    i = find_line(lines, r"^####\s+Placar da rodada")
    if i is not None:
        header, rows = parse_table(lines, i + 1)
        ci = col(header, "confian", last=True)
        if ci is not None:
            r["placar_conf"] = mean([to_num(x[ci]) for x in rows if len(x) > ci])
        mi = col(header, "mudou")
        if mi is not None:
            vals = [x[mi].replace("*", "").strip().lower() for x in rows if len(x) > mi]
            if "virou" in vals:
                r["virada"] = "virou"
            elif "ajustou" in vals:
                r["virada"] = "ajustou"
            elif vals:
                r["virada"] = "não"
    # voto
    i = find_line(lines, r"^####\s+O voto(?:\s+em cada proposta)?\s*$")
    voto_conf = None
    if i is not None:
        header, rows = parse_table(lines, i + 1)
        vi, ci = col(header, "voto"), col(header, "confian", last=True)
        if vi is not None:
            # a proposta tem qualquer rótulo (`P1`, `A`, `B`), desde que a célula de voto se classifique
            props = [x for x in rows if len(x) > vi and classify_vote(x[vi])]
            cont = {"apoio": 0, "ressalva": 0, "contra": 0}
            for x in props:
                k = classify_vote(x[vi])
                if k:
                    cont[k] += 1
            if props:
                r["voto"] = cont
                r["voto_por_proposta"] = {x[0].replace("*", "").strip(): VOTO_PALAVRA[classify_vote(x[vi])] for x in props}
                if ci is not None:
                    voto_conf = mean([to_num(x[ci]) for x in props if len(x) > ci])
    # o plano inteiro
    plano_cells = None
    for l in lines:
        if l.lstrip().startswith("|"):
            cells = split_cells(l)
            if cells and PLANO_INTEIRO.match(cells[0].replace("*", "").strip().lower()):
                plano_cells = cells
    if plano_cells:
        nums = [to_num(c) for c in plano_cells[1:]]
        nums = [n for n in nums if n is not None]
        if nums:
            r["plano"] = nums[-1]
        textos = [c for c in plano_cells[1:] if c and to_num(c) is None]
        if textos:
            r["plano_porque"] = clean_md(textos[-1])
    txt = "\n".join(lines)
    m_plano = re.search(r"Confiança no plano inteiro[^\n]*?:\**\s*(\d+(?:[.,]\d+)?)", txt)
    m_conf = re.search(r"\*\*Confiança:\*\*\s*\**\s*(\d+(?:[.,]\d+)?)", txt)
    for valor, fonte in ((r["plano"], "plano"),
                         (float(m_plano.group(1).replace(",", ".")) if m_plano else None, "plano-linha"),
                         (voto_conf, "voto"), (r["placar_conf"], "placar"),
                         (float(m_conf.group(1).replace(",", ".")) if m_conf else None, "confianca-linha")):
        if valor is not None:
            r["confianca"], r["confianca_fonte"] = valor, fonte
            break
    # posição
    j = find_line(lines, r"^\s*(?:[-*]\s*)?\*\*Posição:\*\*")
    if j is not None:
        corpo = [re.sub(r"^\s*(?:[-*]\s*)?\*\*Posição:\*\*\s*", "", lines[j])]
        for l in lines[j + 1:]:  # continuação da linha, recuada e sem marcador de lista nem tabela
            if l.strip() and l.startswith(" ") and not re.match(r"^\s*([-*]|\|)", l):
                corpo.append(l.strip())
            else:
                break
        r["posicao"], r["posicao_fonte"] = truncate(clean_md(" ".join(corpo))), "posicao"
    elif r["plano_porque"]:
        r["posicao"], r["posicao_fonte"] = truncate(r["plano_porque"]), "plano"
    # os fatos que a persona declara ter lido (`- **Fatos lidos:** M1, M6`)
    m_fatos = re.search(r"^\s*(?:[-*]\s*)?\*\*Fatos lidos:?\*\*:?[ \t]*(.*)$", txt, re.M)
    if m_fatos:
        r["fatos_lidos"] = re.findall(r"\bM\d+\w*", m_fatos.group(1))
    # notas aos colegas
    r["notas"] = parse_notes_table(lines, r["avisos"]) or parse_notes_prose(lines, names, r["avisos"])
    return r


def parse_worklog(text, names=()):
    """Lê o worklog de uma persona. `names` são os colegas, para a nota em prosa.

    -> {"ultima_linha", "marcador_final" (N ou None), "marcadores", "rodadas": {N: {...}}}
    Cada rodada: linha, titulo, confianca, confianca_fonte, placar_conf, virada, voto, posicao, posicao_fonte, notas.
    Seção ou tabela que falta vira None; nada é inventado.
    """
    text = common.corta_medida(text or "")
    nao_vazias = [l.rstrip() for l in text.split("\n") if l.strip()]
    ultima = nao_vazias[-1] if nao_vazias else None
    m = MARCADOR.match(ultima) if ultima else None
    out = {"ultima_linha": ultima, "marcador_final": int(m.group(1)) if m else None,
           "marcadores": [int(x) for x in re.findall(r"^<!-- fim-rodada-(\d+) -->$", text, re.M)], "rodadas": {}}
    for n, sec in split_rounds(text).items():
        rd = parse_round(sec["lines"], names)
        rd.update(linha=sec["linha"], titulo=sec["titulo"])
        out["rodadas"][n] = rd
    return out


# ---------------------------------------------------------------- tempo e arquivos

def parse_when(s, day=None):
    """'2026-11-07T21:28:13-03:00' ou 'HH:MM[:SS]' (no dia `day`, fuso local) -> datetime com fuso; None se vazio."""
    if not s:
        return None
    if isinstance(s, datetime):
        return s if s.tzinfo else s.astimezone()
    if re.match(r"^\d{1,2}:\d{2}(:\d{2})?$", s):
        h, m, *sec = [int(x) for x in s.split(":")]
        return datetime.combine(day or date.today(), time(h, m, sec[0] if sec else 0)).astimezone()
    d = parse_ts(s)
    return d if d.tzinfo else d.astimezone()


def hms(dt):
    return dt.astimezone().strftime("%H:%M:%S") if dt else None


def repo_roots(root):
    """A raiz dada e a raiz comum do git (o worktree não guarda `.measurements/` nem `.sessions/sessions.jsonl`)."""
    roots = [os.path.abspath(root)]
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                             timeout=10).stdout.strip()
        if out:
            common = os.path.dirname(os.path.realpath(os.path.join(root, out)))
            if common not in roots:
                roots.append(common)
    except (OSError, subprocess.SubprocessError):
        pass
    return roots


def default_file(root, rel):
    for r in repo_roots(root):
        p = os.path.join(r, rel)
        if os.path.isfile(p):
            return p
    return os.path.join(os.path.abspath(root), rel)


# ---------------------------------------------------------------- medição

def stats(values):
    """media, mediana, n e faixa de uma lista (None ignorado)."""
    v = [x for x in values if x is not None]
    if not v:
        return {"media": None, "mediana": None, "n": 0, "faixa": None}
    return {"media": round(sum(v) / len(v), 1), "mediana": round(statistics.median(v), 1), "n": len(v),
            "faixa": [min(v), max(v)]}


# ---------------------------------------------------------------- o estado

def worklog_path(reuniao, p):
    return reuniao["worklog"].format(slug=p.get("slug") or p["nome"].lower(), nome=p["nome"], sessao=p.get("sessao", ""))


def none_if_dash(v):
    return None if v in (None, "", "-") else v


def eh_antigravity(runtime):
    return str(runtime or "").strip().lower() == "antigravity"


def calc_sala(personas):
    """A conta da sala, em UM lugar (o `panel.py` a chama também): só quem `respondeu` entra; o Antigravity (E-1) fica
    fora da média e da mediana e vai à parte em `antigravity`. `personas` são os dicts do estado."""
    resp = [x for x in personas if x.get("estado") == "respondeu" and isinstance(x.get("confianca"), (int, float))
            and not isinstance(x.get("confianca"), bool)]
    s = stats([x["confianca"] for x in resp if not eh_antigravity(x.get("runtime"))])
    st = stats([x["confianca"] for x in resp])
    sala = {"media": s["media"], "mediana": s["mediana"], "n": s["n"], "faixa": s["faixa"],
            "total": len([x for x in personas if x.get("estado") != FORA]), "media_todas": st["media"], "mediana_todas": st["mediana"], "n_todas": st["n"]}
    ag = [x for x in resp if eh_antigravity(x.get("runtime"))]
    if ag:
        sala["antigravity"] = {"media": mean([x["confianca"] for x in ag]), "n": len(ag),
                               "nomes": [x["nome"] for x in ag], "fora_da_media": True}
    return sala


def ler_sintese(path):
    """(revisor, revisor_nota) do `sintese-N.json`, no nível de cima ou dentro de `sala`; (None, None) sem arquivo."""
    try:
        with open(path, encoding="utf-8") as f:
            sj = json.load(f)
    except (ValueError, OSError):
        return None, None
    if not isinstance(sj, dict):
        return None, None
    sala = sj.get("sala") if isinstance(sj.get("sala"), dict) else {}
    pega = lambda k: sala.get(k) if sala.get(k) is not None else sj.get(k)
    return pega("revisor"), pega("revisor_nota")


def aplica_revisor(sala):
    if sala.get("revisor") is not None and sala.get("media") is not None:
        sala["diferenca_revisor"] = round(sala["media"] - sala["revisor"], 1)
    else:
        sala["diferenca_revisor"] = None


FORA = "fora da rodada"
PENDENTE_S = 120  # o hook grava o turno no Stop; até 120 s depois do fim da rodada a medição pode não ter chegado
SEM_MEDICAO = "sem medição: persona sem claude_session/provider_session no mapa"


def build_estado(reuniao, n, root, *, measurements=None, sessions=None, codex_dir=None, exclude_raters=(),
                 opened=None, closed=None, at=None, participantes=None, settle=0, sleep=_time.sleep,
                 clock=_time.time):
    """Monta o estado da rodada `n`. `measurements`/`sessions` são caminhos; `opened`/`closed`/`at` aceitam
    'HH:MM:SS' (no dia `reuniao['data']`, padrão hoje), ISO ou datetime. Atravessar a meia-noite vale: `closed` e `at`
    em HH:MM:SS antes de `opened` caem no dia seguinte.

    `participantes` (nomes) restringe a rodada: quem está fora fica `fora da rodada`, sem medição e fora da sala e do
    "x/n". `settle` (s): a medição de uma persona Claude que respondeu e ainda não tem o turno do hook (`pendente`) se
    relê a cada 5 s até chegar ou o prazo acabar."""
    day = date.fromisoformat(reuniao["data"]) if reuniao.get("data") else None
    opened_dt, closed_dt = parse_when(opened, day), parse_when(closed, day)
    if opened_dt and closed_dt and closed_dt < opened_dt and isinstance(closed, str) and ":" in closed[:3]:
        closed_dt += timedelta(days=1)
    win = win_bounds(opened_dt, closed_dt)
    measurements = measurements or default_file(root, ".measurements/measurements.jsonl")
    sessions = sessions or sessions_map.map_file(root)  # o mesmo mapa do launch_persona e do wait_round
    codex_dir = codex_dir or os.path.expanduser("~/.codex/sessions")
    fim_settle = clock() + settle
    while True:
        estado = _montar(reuniao, n, root, load_jsonl(measurements), load_jsonl(sessions), codex_dir, exclude_raters,
                         opened, closed, at, day, opened_dt, closed_dt, win, participantes)
        if (not settle or clock() >= fim_settle
                or not any(p.get("medicao") == "pendente" for p in estado["personas"])):
            return estado
        sleep(5)


def _montar(reuniao, n, root, mrows, srows, codex_dir, exclude_raters, opened, closed, at, day, opened_dt, closed_dt,
            win, participantes):
    at_dt = parse_when(at, day) or datetime.now().astimezone()
    if opened_dt and at and at_dt < opened_dt and isinstance(at, str) and ":" in at[:3]:
        at_dt += timedelta(days=1)
    avisos = []
    if not win:
        avisos.append("sem a janela da rodada (--opened e --closed): o custo e a latência dos Claude são o TOTAL DA SESSÃO, "
                      "não os da rodada, e o turno do Codex não é medido")
    names = [p["nome"] for p in reuniao["personas"]]
    dentro = {p["nome"] for p in common.resolver_personas(reuniao, participantes)} if participantes else None

    parsed, mtimes = {}, {}
    for p in reuniao["personas"]:
        path = os.path.join(root, worklog_path(reuniao, p))
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                parsed[p["nome"]] = parse_worklog(f.read(), names)
            mtimes[p["nome"]] = datetime.fromtimestamp(os.path.getmtime(path)).astimezone()
        else:
            parsed[p["nome"]] = None

    # notas: a rodada mais nova <= n em que alguma persona tenha nota
    nota_rodada, recebidas = None, {}
    for r in range(n, 0, -1):
        if any(w and w["rodadas"].get(r, {}).get("notas") for w in parsed.values()):
            nota_rodada = r
            break
    if nota_rodada:
        for rater, w in parsed.items():
            if rater in exclude_raters or not w:
                continue
            for ratee, nota in (w["rodadas"].get(nota_rodada, {}).get("notas") or {}).items():
                if ratee != rater:
                    recebidas.setdefault(ratee, []).append(nota)

    personas = []
    for p in reuniao["personas"]:
        nome, w = p["nome"], parsed[p["nome"]]
        runtime = (p.get("runtime") or "").lower()
        rd = (w or {}).get("rodadas", {}).get(n) or {}
        r1 = (w or {}).get("rodadas", {}).get(1) or {}
        ant = (w or {}).get("rodadas", {}).get(n - 1) or {}
        mk = (w or {}).get("marcador_final")
        base = {"nome": nome, "papel": p.get("papel"), "sessao": p.get("sessao"),
                "runtime": RUNTIME_NOME.get(runtime, p.get("runtime")),
                "modelo": none_if_dash(p.get("modelo")), "esforco": none_if_dash(p.get("esforco")),
                "worklog": worklog_path(reuniao, p)}
        if dentro is not None and nome not in dentro:
            recs = recebidas.get(nome)
            personas.append({**base, "estado": FORA, "respondeu_as": None, "latencia_s": None, "latencia_fonte": None,
                             "confianca": None, "confianca_fonte": None, "confianca_r1": r1.get("placar_conf"),
                             "posicao": None, "posicao_fonte": None, "voto": None, "voto_por_proposta": None,
                             "virada": None, "virada_antes": f"R{n - 1}: {ant['virada']}" if n > 1 and ant.get("virada") else None,
                             "nota_colegas": round(sum(recs) / len(recs), 2) if recs else None,
                             "nota_rodada": nota_rodada if recs else None, "custo_usd": None, "tokens": None,
                             "janela": None, "medicao": None, "medicao_aviso": None, "fatos_lidos": None,
                             "linha": None})
            continue
        ids_claude, ids_prov = session_ids(srows, p.get("sessao"), p)
        med, aviso_med = None, None
        if runtime == "claude":
            med = _legacy_measure(measure_claude(mrows, ids_claude, win))
            if not ids_claude and not ids_prov:
                aviso_med = SEM_MEDICAO
        elif runtime == "codex":
            med = _legacy_measure(measure_codex(codex_dir, ids_prov, n, win))
            if not ids_prov:
                aviso_med = SEM_MEDICAO
        erro_limite = bool(med and med.get("erro"))
        if mk is not None and mk >= n:
            # o marcador de uma rodada adiante sem a seção da N: entregou junto com a seguinte, e não há dado da N
            estado = "respondeu" if n in (w or {}).get("rodadas", {}) else "sem dado"
        else:
            estado = "falta"
        if estado == "falta" and erro_limite:
            estado = "sem cota"
        latencia, fonte, fim = None, None, None
        if med:
            latencia, fonte, fim = med["latencia_s"], "turno", med.get("fim")
        if latencia is None and estado == "respondeu" and mk == n and nome in mtimes:
            fim = mtimes[nome]
            if opened_dt:
                latencia, fonte = int(round((fim - opened_dt).total_seconds())), "≈ mtime"
        tokens = med.get("tokens") if med and runtime == "codex" else None
        recs = recebidas.get(nome)
        # X4: o hook grava o turno no Stop; persona Claude que respondeu, com id, sem turno na janela e com o fim da
        # rodada a menos de 120 s de `at` está `pendente`: nunca custo 0 e nunca "sem medição"
        medicao = None
        if runtime in ("claude", "codex"):
            medicao = "medida" if med else "sem medição"
        if runtime == "claude" and not med and estado == "respondeu" and (ids_claude or ids_prov):
            ref = closed_dt or fim
            if ref is not None and 0 <= (at_dt - ref).total_seconds() < PENDENTE_S:
                medicao = "pendente"
                avisos.append(f"{nome}: medição pendente: o hook grava no Stop do turno; rode de novo em ~1 min")
        if aviso_med:
            avisos.append(f"{nome}: {aviso_med}")
        for a in rd.get("avisos") or []:
            avisos.append(f"{nome}: {a}")
        if estado == "respondeu" and rd.get("voto") and rd.get("fatos_lidos") is None:  # [] = "nenhum novo", declarado
            avisos.append(f"{nome}: votou sem declarar os fatos lidos")
        personas.append({
            **base,
            "estado": estado, "respondeu_as": hms(fim) if estado == "respondeu" else None,
            "latencia_s": latencia, "latencia_fonte": fonte,
            "confianca": rd.get("confianca"), "confianca_fonte": rd.get("confianca_fonte"),
            "confianca_r1": r1.get("placar_conf"),
            "posicao": rd.get("posicao"), "posicao_fonte": rd.get("posicao_fonte"),
            "voto": rd.get("voto"), "voto_por_proposta": rd.get("voto_por_proposta"), "virada": rd.get("virada"),
            "virada_antes": f"R{n - 1}: {ant['virada']}" if n > 1 and ant.get("virada") else None,
            "nota_colegas": round(sum(recs) / len(recs), 2) if recs else None, "nota_rodada": nota_rodada if recs else None,
            "custo_usd": med.get("custo_usd") if med and runtime == "claude" else None,
            "tokens": tokens, "janela": bool(win) if runtime in ("claude", "codex") else None,
            "medicao": medicao, "medicao_aviso": aviso_med, "fatos_lidos": rd.get("fatos_lidos"),
            "linha": rd.get("linha"),
        })

    sala = calc_sala(personas)
    sala.update({"revisor": None, "revisor_nota": "—", "diferenca_revisor": None})
    revisor, nota = ler_sintese(os.path.join(root, reuniao.get("dir", ""), f"sintese-{n}.json"))
    sala["revisor"], sala["revisor_nota"] = revisor, nota or "—"
    aplica_revisor(sala)

    titulo = next((w["rodadas"][n]["titulo"] for w in parsed.values()
                   if w and w["rodadas"].get(n, {}).get("titulo")), None)
    return {
        "reuniao": {k: reuniao.get(k) for k in ("id", "tema", "decisor", "fim")},
        "rodada": {"n": n, "total_previsto": reuniao.get("rodadas_previstas"), "titulo": titulo,
                   "aberta": hms(opened_dt), "prazo": None, "fechada": hms(closed_dt), "gerado": hms(at_dt),
                   "tem_voto": any(x["voto"] for x in personas),
                   "custo_rotulo": "da rodada" if win else "total da sessão",
                   "participantes": [x["nome"] for x in personas if x["estado"] != FORA]},
        "personas": personas,
        "sala": sala,
        "avisos": avisos,
        "medicoes": [], "sintese": [], "decisoes": [],
        "custos_coordenacao": {"coordenacao_usd": None, "revisor_usd": None, "ate": None},
    }


# ---------------------------------------------------------------- a tabela do chat

def fnum(x):
    if x is None:
        return "—"
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}".replace(".", ",")


def fdelta(x):
    s = fnum(abs(x))
    return ("+" if x > 0 else "−" if x < 0 else "±") + s


def cell(s):
    return (s or "—").replace("|", "\\|")


def render_md(estado):
    """A tabela Markdown do chat: Persona · posição em uma linha · confiança · mudou? · voto, e a linha da sala."""
    n = estado["rodada"]["n"]
    # X7: a coluna de custo só entra quando há custo (ou medição pendente) a mostrar, com o rótulo no cabeçalho
    custo = any(isinstance(p.get("custo_usd"), (int, float)) or p.get("medicao") == "pendente"
                for p in estado["personas"])
    rotulo = "total da sessão" if (estado.get("rodada") or {}).get("custo_rotulo") == "total da sessão" else "rodada"
    linhas = ["| Persona | Posição em uma linha | Confiança | Mudou? | Voto |" + (f" Custo ({rotulo}) |" if custo else ""),
              "| :-- | :-- | --: | :-- | :-- |" + (" --: |" if custo else "")]
    for p in estado["personas"]:
        conf = fnum(p.get("confianca"))
        if p.get("confianca") is not None and n > 1 and p.get("confianca_r1") is not None:
            conf += f" ({fdelta(p['confianca'] - p['confianca_r1'])})"
        pos = p.get("posicao") if p["estado"] == "respondeu" else f"— ({p['estado']})"
        v = p.get("voto")
        vp = p.get("voto_por_proposta")
        voto = (" · ".join(f"{k}: {x.replace('apoio com', 'apoio c/')}" for k, x in vp.items()) if vp else
                f"{v['apoio']}/{v['ressalva']}/{v['contra']}" if v else "—")
        celula = ""
        if custo:
            c = p.get("custo_usd")
            celula = " pendente |" if p.get("medicao") == "pendente" else \
                (f" US$ {fnum(round(c, 2))} |" if isinstance(c, (int, float)) else " — |")
        linhas.append(f"| {cell(p['nome'])} | {cell(pos)} | {conf} | {cell(p.get('virada'))} | {voto} |{celula}")
    s = estado["sala"]
    partes = [f"Sala: média {fnum(s['media'])} ({s['n']}/{s.get('total', len(estado['personas']))}), "
              f"mediana {fnum(s['mediana'])}, faixa {fnum(s['faixa'][0]) if s['faixa'] else '—'}–"
              f"{fnum(s['faixa'][1]) if s['faixa'] else '—'}"]
    if s.get("revisor") is not None:
        partes.append(f"revisor {fnum(s['revisor'])}")
        if s.get("diferenca_revisor") is not None:
            partes.append(f"sala − revisor {fdelta(s['diferenca_revisor'])}")
    if s.get("antigravity"):
        partes.append(f"Antigravity à parte: {fnum(s['antigravity']['media'])}")
    saida = "\n".join(linhas) + "\n\n" + " · ".join(partes)
    sem = [f"{p['nome']} ({p['runtime']})" for p in estado["personas"]
           if p["runtime"] in ("Grok", "Antigravity") and p["estado"] != FORA]
    if sem:
        saida += "\nSem medição de custo: " + ", ".join(sem) + "."
    for p in estado["personas"]:
        if p.get("medicao_aviso"):
            saida += f"\n{p['nome']}: {p['medicao_aviso']}."
        if p.get("medicao") == "pendente":
            saida += f"\n{p['nome']}: medição pendente: o hook grava no Stop do turno; rode de novo em ~1 min."
    # A4: a nota só sai com algum Claude entre os participantes; o rótulo do estado (o contrato) não muda
    tem_claude = any(p.get("runtime") == "Claude" and p.get("estado") != FORA for p in estado["personas"])
    if (estado.get("rodada") or {}).get("custo_rotulo") == "total da sessão" and tem_claude:
        saida += "\nCusto e latência dos Claude: total da sessão (sem a janela da rodada)."
    return saida


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="Estado de uma rodada da reunião, tirado dos worklogs e das medições.")
    ap.add_argument("n", type=int)
    ap.add_argument("--reuniao", required=True)
    ap.add_argument("--root", help="padrão: o topo do repositório git do cwd (`git rev-parse --show-toplevel`)")
    ap.add_argument("--measurements")
    ap.add_argument("--sessions")
    ap.add_argument("--codex-dir")
    ap.add_argument("--out", help="padrão <root>/<dir>/estado-r<N>.json; '-' não grava")
    ap.add_argument("--exclude-rater", action="append", default=[])
    ap.add_argument("--opened")
    ap.add_argument("--closed")
    ap.add_argument("--at", help="o instante do estado (HH:MM:SS ou ISO); padrão agora; decide a medição pendente")
    ap.add_argument("--participantes", nargs="+", metavar="NOME",
                    help="só estes nomes estão na rodada; os outros ficam `fora da rodada`")
    ap.add_argument("--settle", type=float, default=0, metavar="SEG",
                    help="relê o measurements.jsonl a cada 5 s até as medições pendentes chegarem, por até SEG")
    fmt = ap.add_mutually_exclusive_group()
    fmt.add_argument("--md", action="store_true")
    fmt.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root) if a.root else raiz_padrao()
    path = resolve_reuniao(a.reuniao, root)
    with open(path, encoding="utf-8") as f:
        reuniao = json.load(f)
    if not worklogs_existentes(reuniao, root):
        print(f"tally: nenhum worklog existe sob {root} (padrão {reuniao.get('worklog')}); confira --root e o manifesto",
              file=sys.stderr)
        return 2
    try:
        estado = build_estado(reuniao, a.n, root, measurements=a.measurements, sessions=a.sessions,
                              codex_dir=a.codex_dir, exclude_raters=tuple(a.exclude_rater),
                              opened=a.opened, closed=a.closed, at=a.at, participantes=a.participantes,
                              settle=a.settle)
    except ValueError as e:
        print(f"tally: {e}", file=sys.stderr)
        return 2
    for av in estado.get("avisos") or []:
        print(f"aviso: {av}", file=sys.stderr)
    out = a.out or os.path.join(root, reuniao.get("dir", "."), f"estado-r{a.n}.json")
    if out != "-":
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print(json.dumps(estado, ensure_ascii=False, indent=2) if a.json else render_md(estado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
