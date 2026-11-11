#!/usr/bin/env python3
"""Os consultores do Desenho em sessões (PLN-021/D4): abre três sessões em runtimes diferentes, espera o arquivo de cada
uma, monta a tabela lado a lado e fecha. Só na decisão cara (R2.3); o padrão continua sendo o `Agent`.

Uso:
    consult.py open  PLN-NNN D<n> --brief brief.md [--roster padrao|arquivo.json] [--dry-run] [--no-panel]
    consult.py wait  PLN-NNN D<n> [--timeout SEG]
    consult.py table PLN-NNN D<n> [--publish-dir DIR] [--png CAMINHO]
    consult.py close PLN-NNN D<n>

Arquivos, em `.sessions/pln-nnn/D<n>/` (na raiz do worktree do plano): `brief.md` (a coordenação escreve: o Terreno, os
casos, as rodadas citadas), `prompt-<foco>.md` (o `open` o gera: "Você é consultor do Desenho de …", o brief, o foco, a forma
do arquivo e o protocolo de fim), `consultants.json` (o manifesto: sessão, runtime, estado de cada foco) e, um por foco,
`<focus>.md`, que SÓ o consultor grava: tese, "Como fica", `Custo:` · `Se paga:` · `Reabre:` sobre os casos, o ataque às outras
duas, o que enfraquece a própria (`Risco:`) e a última linha `<!-- fim-D<n>: <foco> -->`. A sessão abre no worktree do plano.

O roster padrão (PLN-021/R5.3, confirmada): Claude Opus `high` na arquitetura limpa, Codex no maior esforço na
mudança mínima, Grok no equilíbrio. `--roster arquivo.json` troca: `{"consultants": [{"focus", "agent", "model", "effort",
"fallback": {…}}]}`. Runtime com a janela `session` (ou `weekly`, no Grok) acima de 55% no `brza quota --json` não entra: o `fallback` do roster o
substitui, e a linha da abertura diz quem foi cortado.

`wait`: 0 com todos entregues, 75 no prazo (diz quem falta), 1 com falha de sessão. `table`: Markdown para a mensagem e a
linha `::orca-visual`; foco sem arquivo ou sem marcador vira "(não entregou)". Saída 2: uso ou plano que não existe.
"""
import argparse
import html as H
import json
import os
import re
import shlex
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _kit  # noqa: E402,F401
import executor  # noqa: E402  (o corredor de data e o relógio são os mesmos; o veredito de `close` fica lá)
import plan_md  # noqa: E402
import plan_panel  # noqa: E402
from skillkit import visual  # noqa: E402
from skillkit.paths import strip_measurement  # noqa: E402
from skillkit.sessions_cli import close_argv, interpret_open, open_argv, run_brza, run_sessions, wait_brza  # noqa: E402

QUOTA_MAX = 55
TICK = 180
FALLBACK = {"agent": "claude", "model": "claude-sonnet-5-5", "effort": "high"}
DEFAULT_ROSTER = {"consultants": [
    {"focus": "arquitetura-limpa", "agent": "claude", "model": "claude-opus-5-5", "effort": "high",
     "fallback": {"agent": "grok", "model": None, "effort": None}},
    {"focus": "mudanca-minima", "agent": "codex", "model": executor.CODEX_MODEL, "effort": "xhigh", "fallback": FALLBACK},
    {"focus": "equilibrio", "agent": "grok", "model": None, "effort": None, "fallback": FALLBACK},
]}
FOCUSES = {
    "arquitetura-limpa": "a arquitetura limpa: a estrutura que você defenderia se pudesse refazer, mesmo que custe mais agora",
    "mudanca-minima": "a mudança mínima: o menor desvio do que já existe que resolve, mesmo que deixe dívida",
    "equilibrio": "o equilíbrio: o ponto entre as duas, com o custo e o risco explícitos",
}
RUNTIME_NAME = {"claude": "Claude", "codex": "Codex", "grok": "Grok", "antigravity": "Antigravity"}
RE_LABEL = re.compile(r"(?:^|(?<=\s))(Tese|Custo|Se paga|Reabre|Risco)\s*:\s*")


def folder(pl, did):
    return os.path.join(plan_panel.folder_sessions(pl.root, pl.id), did)


def slug_focus(focus):
    return re.sub(r"[^a-z0-9]+", "-", focus.lower()).strip("-")


def session_name(pl, did, focus):
    n = re.search(r"\d+", pl.id).group(0)
    return "pln%s-%s-%s" % (n, did.lower(), slug_focus(focus)[:22].strip("-"))


def loads_roster(ref):
    if not ref or ref == "padrao":
        return DEFAULT_ROSTER["consultants"]
    with open(ref, encoding="utf-8") as f:
        d = json.load(f)
    roster_rows = d.get("consultants") if isinstance(d, dict) else d
    if not isinstance(roster_rows, list) or not roster_rows or not all(isinstance(x, dict) and x.get("focus") and x.get("agent") for x in roster_rows):
        raise ValueError("o roster pede {\"consultants\": [{focus, agent, …}]}")
    return roster_rows


def quotas():
    """{runtime: pct} do `brza quota --json` (`accounts[].windows[]`); {} se não leu. Vale a conta ativa de cada runtime (a
    maior, se houver mais de uma) e a janela `session`; sem ela (o Grok), a `weekly`."""
    rc, stdout, _ = run_brza(["quota", "--json"])
    try:
        d = json.loads(stdout)
    except ValueError:
        return {}
    out = {}
    accounts = d.get("accounts") if isinstance(d, dict) else None
    for account in accounts if isinstance(accounts, list) else []:
        if not isinstance(account, dict) or not account.get("active") or not account.get("runtime"):
            continue
        windows = {w.get("name"): w.get("used") for w in account.get("windows") or [] if isinstance(w, dict)}
        used = windows.get("session", windows.get("weekly"))
        if isinstance(used, (int, float)):
            out[account["runtime"]] = max(out.get(account["runtime"], 0), used)
    return out


def chooses(roster, quota):
    """[(entrada efetiva, nota)]: o runtime acima da cota vira o `fallback`."""
    output = []
    for r in roster:
        pct = quota.get(r["agent"])
        if pct is not None and pct > QUOTA_MAX and r.get("fallback"):
            fb = dict(r["fallback"])
            ef = {"focus": r["focus"], "agent": fb["agent"], "model": fb.get("model"), "effort": fb.get("effort")}
            output.append((ef, "%s cortado: %s a %s%% (> %d%%); entra %s" % (r["agent"], r["agent"], pct, QUOTA_MAX, fb["agent"])))
        else:
            output.append(({k: r.get(k) for k in ("focus", "agent", "model", "effort")}, None))
    return output


def prompt(pl, did, focus, brief, file):
    others = ", ".join(f for f in FOCUSES if f != focus) or "as outras alternativas"
    return """Você é consultor do Desenho de {did} do {pln}, numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você não conduz o plano, devolve uma alternativa. Responda em português do Brasil.

## O seu foco
{focus}: {desc}.

## O pedido
{brief}

## O que gravar
Grave SÓ o arquivo {file} e leia o resto do repositório apenas para consulta. Não grave o plano, não commite, não pergunte a Anderson, não decida entre alternativas.

O arquivo tem, nesta ordem:
1. `Tese:` a alternativa do seu foco, numa frase;
2. `## Como fica`: o desenho da alternativa, com o que ela escreve;
3. sobre cada caso do pedido, as linhas `Custo:` · `Se paga:` · `Reabre:` (o que se gasta e quando é cobrado; quando o ganho cobre o custo, ou "nunca"; o que a escolha reabre);
4. `## Ataque às outras`: o ataque às outras alternativas ({others});
5. `Risco:` o que enfraquece a sua própria alternativa;
6. a última linha, sozinha: `<!-- fim-{did}: {focus} -->`.

## O fim
Termine o arquivo com o marcador e envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o encerramento.
""".format(did=did, pln=pl.id, focus=focus, desc=FOCUSES.get(focus, focus), brief=brief.strip(), file=file, others=others)


def read_manifest(pl, did):
    d = plan_panel.read_json(os.path.join(folder(pl, did), "consultants.json"))
    d.setdefault("focuses", {})
    return d


def write_manifest(pl, did, m):
    p = os.path.join(folder(pl, did), "consultants.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = "%s.%d.tmp" % (p, os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, p)


def _loads(a, c):
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        c.err("erro: %s" % e)
        return None, None
    did = a.decision.upper()
    if pl.design_text(did) is None:
        c.err("erro: o Desenho do %s não tem o item %s" % (pl.id, did))
        return None, None
    return pl, did


def arrived(pl, did, focus, file):
    """O arquivo do foco termina no marcador `<!-- fim-D<n>: <foco> -->` (última linha não vazia)."""
    try:
        with open(file, encoding="utf-8") as f:
            lines = [l.rstrip() for l in strip_measurement(f.read()).split("\n") if l.strip()]
    except OSError:
        return False
    return bool(lines) and lines[-1] == "<!-- fim-%s: %s -->" % (did, focus)


# ---------------------------------------------------------------- open

def cmd_open(a, c):
    pl, did = _loads(a, c)
    if pl is None:
        return 2
    try:
        with open(a.brief, encoding="utf-8") as f:
            brief = f.read()
    except OSError as e:
        c.err("erro: não li o --brief: %s" % e)
        return 2
    try:
        roster = loads_roster(a.roster)
    except (OSError, ValueError) as e:
        c.err("erro: roster: %s" % e)
        return 2
    quota = quotas()
    if not quota:
        c.err("⚠ não li o `brza quota --json`: nenhum runtime foi cortado por cota")
    chosen = chooses(roster, quota)
    decision_dir = folder(pl, did)
    m = read_manifest(pl, did)
    m.update({"decision": did, "plan": pl.id})
    lines = []
    for ef, note in chosen:
        focus = ef["focus"]
        ef["model"], ef["effort"], warning_text = executor.effective_model_effort(ef["agent"], ef.get("model"), ef.get("effort"))
        if warning_text:
            c.err("⚠ %s: %s" % (focus, warning_text))
        name = session_name(pl, did, focus)
        file = os.path.join(decision_dir, "%s.md" % slug_focus(focus))
        ppath = os.path.join(decision_dir, "prompt-%s.md" % slug_focus(focus))
        argv = open_argv(name, agent=ef["agent"], checkout=pl.root, prompt_file=ppath, model=ef.get("model"),
                         effort=ef.get("effort"), title="%s %s: consultor %s" % (pl.id, did, focus), rename=True)
        if a.dry_run:
            c.out("[dry-run] %s" % (note or "sem corte de cota"))
            c.out("[dry-run] prompt: %s" % ppath)
            c.out("[dry-run] brza sessions " + shlex.join(argv))
            continue
        os.makedirs(decision_dir, exist_ok=True)
        with open(ppath, "w", encoding="utf-8") as f:
            f.write(prompt(pl, did, slug_focus(focus), brief, file))
        rc, stdout, se = run_sessions(argv)
        res = interpret_open(rc, stdout, se)
        if res in ("nao-abriu", "falha"):
            c.err("%s não abriu (%s): leia o `pending-*.json` citado antes de relançar; paro aqui.\n%s" % (
                name, res, ((se or "") + (stdout or "")).strip()[:300]))
            write_manifest(pl, did, m)
            return 1
        if res == "sem-id":
            c.err("⚠ %s abriu sem o id do provedor; o `wait` o grava depois. Não relance." % name)
        if res == "ja":
            c.err("⚠ %s já estava aberta; não reabri." % name)
        m["focuses"][slug_focus(focus)] = {"session": name, "agent": ef["agent"], "model": ef.get("model"), "effort": ef.get("effort"),
                                       "file": os.path.relpath(file, pl.root), "state": "aberto", "quota_note": note,
                                       "opened_at": executor.iso(c.clock())}
        lines.append((slug_focus(focus), name, ef, file, note))
    if a.dry_run:
        return 0
    if a.brief and os.path.abspath(a.brief) != os.path.join(decision_dir, "brief.md"):
        with open(os.path.join(decision_dir, "brief.md"), "w", encoding="utf-8") as f:
            f.write(brief)
    write_manifest(pl, did, m)
    c.out("| Foco | Sessão | Runtime | Modelo | Esforço | Arquivo |")
    c.out("| :-- | :-- | :-- | :-- | :-- | :-- |")
    for focus, name, ef, file, _ in lines:
        c.out("| %s | %s | %s | %s | %s | %s |" % (focus, name, RUNTIME_NAME.get(ef["agent"], ef["agent"]),
                                                    ef.get("model") or "padrão do runtime", ef.get("effort") or "padrão", file))
    for _, _, _, _, note in lines:
        if note:
            c.out("cota: %s" % note)
    if not a.no_panel:
        plan_panel.emit(plan_panel.publish_safe(pl), c.out, c.err)
    return 0


# ---------------------------------------------------------------- wait

def cmd_wait(a, c):
    pl, did = _loads(a, c)
    if pl is None:
        return 2
    m = read_manifest(pl, did)
    focuses = m["focuses"]
    if not focuses:
        c.err("erro: %s não tem consultores abertos (rode `open`)" % did)
        return 2
    end = c.clock() + a.timeout
    seen_without = set()
    failed_state = []
    errors = 0
    last_tick = c.clock()

    def still_missing():
        return [f for f, v in focuses.items() if v.get("state") not in ("entregou", "falhou", "fechado")]

    def summary_text(prefix):
        already_ = [f for f, v in focuses.items() if v.get("state") == "entregou"]
        missing = still_missing()
        return "%s %d/%d — entregaram %s; faltam %s" % (prefix, len(already_), len(focuses), ", ".join(already_) or "nenhum", ", ".join(missing) or "nenhum")

    def scans():
        for f in still_missing():
            v = focuses[f]
            if arrived(pl, did, f, os.path.join(pl.root, v["file"])):
                v["state"] = "entregou"
                v["delivered_at"] = executor.iso(c.clock())
                c.out("%s · %s entregou (%s)" % (did, f, RUNTIME_NAME.get(v["agent"], v["agent"])))
                c.out(summary_text("%s ·" % did))
    scans()
    while still_missing() and c.clock() < end:
        name_list = {focuses[f]["session"]: f for f in still_missing()}
        snippet = min(end - c.clock(), TICK)
        start = c.clock()
        rc, payload = wait_brza(list(name_list), snippet, any_=True)
        if payload.get("error"):
            errors += 1
            action, msg, lost_index = executor.wait_error_verdict(rc, payload["error"], errors, list(name_list))
            c.err(msg)
            if action == "stop":
                write_manifest(pl, did, m)
                return 1
            if action == "missing":
                focuses[name_list[lost_index]]["state"] = "falhou"
                failed_state.append(name_list[lost_index])
                c.out("%s · %s falhou: a sessão %s não existe mais; a espera segue com as outras" % (did, name_list[lost_index], lost_index))
                errors = 0
            else:
                c.sleep(executor.WAIT_ERROR_PAUSE)
            continue
        errors = 0
        without_marker = False
        for row in payload.get("done") or []:
            f = name_list.get(row.get("name"))
            if f is None:
                continue
            if row.get("outcome") == "failed":
                focuses[f]["state"] = "falhou"
                failed_state.append(f)
                c.out("%s · %s falhou: `brza sessions read %s --last`" % (did, f, focuses[f]["session"]))
            elif not arrived(pl, did, f, os.path.join(pl.root, focuses[f]["file"])):
                without_marker = True
                if f not in seen_without:
                    seen_without.add(f)
                    c.out("%s · %s: o turno acabou sem o marcador `<!-- fim-%s: %s -->`; a espera segue" % (did, f, did, f))
        scans()
        if not still_missing():
            break
        if without_marker:
            c.sleep(min(5, max(0, end - c.clock())))
        elif c.clock() - start < snippet and (payload.get("timed_out") or rc == 75):
            c.sleep(max(0, snippet - (c.clock() - start)))
        if c.clock() < end and still_missing() and c.clock() - last_tick >= TICK:
            last_tick = c.clock()
            c.out(summary_text("%s · em curso;" % did))
    write_manifest(pl, did, m)
    if failed_state:
        return 1
    if still_missing():
        c.out("prazo: faltam %s; `table` mostra o que há" % ", ".join(still_missing()))
        return 75
    return 0


# ---------------------------------------------------------------- table

ROWS = (("Tese", "thesis"), ("Custo", "cost"), ("Se paga", "pays_when"), ("Reabre", "reopens"), ("Risco", "risk"))


def read_text_file(text):
    """Campos `{thesis, cost, pays_when, reopens, risk}`, lidos dos rótulos `Tese`, `Custo`, `Se paga`, `Reabre`, `Risco`: cada rótulo pode repetir (um por caso) e as ocorrências se juntam com ` / `."""
    fields = {k: [] for _, k in ROWS}
    current = None
    for line in strip_measurement(text).split("\n"):
        s = re.sub(r"\*\*|`", "", line.strip())
        s = re.sub(r"^[-*]\s+", "", s)
        if not s or s.startswith("<!--"):
            current = None
            continue
        if s.startswith("#"):
            current = None
            continue
        ms = list(RE_LABEL.finditer(s))
        found = bool(ms)
        for i, mm in enumerate(ms):
            end = ms[i + 1].start() if i + 1 < len(ms) else len(s)
            value = s[mm.end():end].strip().rstrip("·").strip()
            key = {"tese": "thesis", "custo": "cost", "se paga": "pays_when", "reabre": "reopens", "risco": "risk"}[mm.group(1).lower()]
            fields[key].append(value)
            current = key
        if not found and current:
            fields[current][-1] = (fields[current][-1] + " " + s).strip()
    return {k: " / ".join(v) for k, v in fields.items()}


def escape_cell(v):
    return (v or "—").replace("|", "\\|").replace("\n", " ")


def table_md(focuses, payload):
    header = "| | " + " | ".join("%s (%s)" % (f, RUNTIME_NAME.get(focuses[f]["agent"], focuses[f]["agent"])) for f in focuses) + " |"
    sep = "| :-- |" + " :-- |" * len(focuses)
    body_text = ["| **%s** | %s |" % (row_label, " | ".join(escape_cell(payload[f].get(k) if payload[f] else ("(não entregou)" if k == "thesis" else None)) for f in focuses))
             for row_label, k in ROWS]
    return "\n".join([header, sep, *body_text])


CSS = """
html{--fb-bg:#fff;--fb-fg:#171717;--fb-card:#fafafa;--fb-mut:#6b7280;--fb-bd:#e5e5e5}
html.dark{--fb-bg:#18181b;--fb-fg:#ededed;--fb-card:#232327;--fb-mut:#a1a1aa;--fb-bd:#3a3a40}
*{box-sizing:border-box}
body{margin:0;padding:14px 16px 18px;background:var(--background,var(--fb-bg));color:var(--foreground,var(--fb-fg));font:13px/1.45 var(--font-sans,-apple-system,system-ui,sans-serif)}
.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,var(--fb-mut))}
h1{font-size:17px;margin:2px 0 10px;line-height:1.25}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th{text-align:left;font-size:11.5px;font-weight:600;padding:5px 6px;border-bottom:1px solid var(--border,var(--fb-bd))}
th small{display:block;font-weight:400;color:var(--muted-foreground,var(--fb-mut))}
td{padding:7px 6px;border-bottom:1px solid var(--border,var(--fb-bd));vertical-align:top;overflow-wrap:anywhere}
td.r{width:62px;font-size:11px;color:var(--muted-foreground,var(--fb-mut));text-transform:uppercase;letter-spacing:.04em}
td.nao{color:var(--muted-foreground,var(--fb-mut));font-style:italic}
"""


def render_html(did, pln, focuses, payload):
    header = "".join("<th>%s<small>%s</small></th>" % (H.escape(f), H.escape("%s%s" % (RUNTIME_NAME.get(v["agent"], v["agent"]),
                                                                                    (" · " + v["effort"]) if v.get("effort") else "")))
                  for f, v in focuses.items())
    body_text = ""
    for row_label, k in ROWS:
        tds = ""
        for f in focuses:
            d = payload[f]
            if d is None:
                tds += '<td class="nao">%s</td>' % ("(não entregou)" if k == "thesis" else "—")
            else:
                tds += "<td>%s</td>" % H.escape(d.get(k) or "—")
        body_text += '<tr><td class="r">%s</td>%s</tr>' % (row_label, tds)
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s %s — consultores</title><style>%s</style></head>'
            '<body><div class="eyebrow">Consultores do Desenho</div><h1>%s · %s</h1><table><thead><tr><th></th>%s</tr></thead>'
            '<tbody>%s</tbody></table></body></html>' % (H.escape(pln), did, CSS, H.escape(pln), did, header, body_text))


def cmd_table(a, c):
    pl, did = _loads(a, c)
    if pl is None:
        return 2
    focuses = read_manifest(pl, did)["focuses"]
    if not focuses:
        c.err("erro: %s não tem consultores abertos" % did)
        return 2
    payload = {}
    for f, v in focuses.items():
        file_path = os.path.join(pl.root, v["file"])
        if arrived(pl, did, f, file_path):
            with open(file_path, encoding="utf-8") as fh:
                payload[f] = read_text_file(fh.read())
            for row_label, k in ROWS:
                if not payload[f].get(k):
                    c.err("⚠ %s: o arquivo não traz `%s:`" % (f, row_label))
        else:
            payload[f] = None
            c.err("⚠ %s: sem arquivo com o marcador `<!-- fim-%s: %s -->`; coluna vazia" % (f, did, f))
    c.out(table_md(focuses, payload))
    try:
        dest = plan_panel.default_target(pl.root, pl.id, a.publish_dir)
        saved_path, line = visual.save_visual(render_html(did, pl.id, focuses, payload), pl.id.lower(), did.lower(),
                                          "%s|%s|%s" % (pl.id, did, c.on_date()), "%s %s — consultores lado a lado" % (pl.id, did),
                                          publish_dir=dest)
    except (visual.PublishError, OSError) as e:
        c.err("⚠ visual: %s" % e)
        return 0
    c.out(line)
    if a.png:
        error = visual.render_png(saved_path, a.png, 736)
        c.out("png: %s" % a.png) if not error else c.err("⚠ png: %s" % error)
    return 0


# ---------------------------------------------------------------- close

def cmd_close(a, c):
    pl, did = _loads(a, c)
    if pl is None:
        return 2
    m = read_manifest(pl, did)
    if not m["focuses"]:
        c.err("erro: %s não tem consultores abertos" % did)
        return 2
    code_list = []
    for f, v in m["focuses"].items():
        rc, stdout, se = run_sessions(close_argv(v["session"], "close"))
        try:
            d = json.loads(stdout)
        except ValueError:
            d = None
        if isinstance(d, dict) and isinstance(d.get("results"), list) and d["results"]:
            d = d["results"][0]
        st = d.get("status") if isinstance(d, dict) else None
        if st in ("released", "already_released"):
            v["state"] = "fechado"
            c.out("%s · %s fechada (%s)" % (did, f, st))
            code_list.append(0)
        elif st == "closing":
            c.out("%s · %s: pedido de encerramento enviado; NÃO está fechada (closing); rode `close` de novo depois" % (did, f))
            code_list.append(0)
        elif st in executor.UNCERTAIN:
            c.err("%s · %s: incerto (%s): não repita às cegas" % (did, f, st))
            code_list.append(75)
        else:
            c.err("%s · %s: não fechada (%s, rc %s)" % (did, f, st or "sem JSON", rc))
            code_list.append(1)
    write_manifest(pl, did, m)
    return 1 if 1 in code_list else 75 if 75 in code_list else 0


def main(argv=None, *, out=None, err=None, clock=None, sleep=None):
    ap = argparse.ArgumentParser(prog="consult.py", description="os consultores do Desenho em sessões")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("open", "wait", "table", "close"):
        s = sub.add_parser(name)
        s.add_argument("plan")
        s.add_argument("decision")
    o = sub.choices["open"]
    o.add_argument("--brief", required=True)
    o.add_argument("--roster", default="padrao")
    o.add_argument("--dry-run", action="store_true")
    o.add_argument("--no-panel", action="store_true")
    sub.choices["wait"].add_argument("--timeout", type=float, default=1800)
    sub.choices["table"].add_argument("--publish-dir")
    sub.choices["table"].add_argument("--png")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    c = executor.Ctx(out, err, clock, sleep)
    return {"open": cmd_open, "wait": cmd_wait, "table": cmd_table, "close": cmd_close}[a.cmd](a, c)


if __name__ == "__main__":
    sys.exit(main())
