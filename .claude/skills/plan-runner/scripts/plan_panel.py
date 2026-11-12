#!/usr/bin/env python3
"""O painel do plano (PLN-021/D5): um `::orca-visual` por plano e dia, gerado do estado e republicado no mesmo nome.

Uso:
    python3 -I plan_panel.py publish PLN-NNN [--publish-dir DIR] [--png CAMINHO] [--width 736] [--at ISO]
    python3 -I plan_panel.py render  PLN-NNN --out arquivo.html [--at ISO]

`publish` grava `pln-nnn-painel-<hash4>.html` (chave `PLN-NNN|AAAA-MM-DD`: o mesmo nome o dia inteiro) em `--publish-dir`,
senão em `$ORCA_CHAT_SCRATCH_DIR`, senão em `<raiz>/.sessions/pln-nnn/painel/`, e imprime a linha `::orca-visual`. Com
`--png`, tira o PNG pelo `brza shot`.

O painel mostra o cabeçalho do plano (fase, `ready`, as três horas, com `⚠` quando a soma não confere), uma linha por passo
(estado do manifesto do executor, Estimado × Executado, custo medido, idade do último evento), as sessões vivas (executores
e consultores, com o estado do `brza sessions list --json`) e a última rodada. Sem medição, "sem medição", nunca zero.

Os scripts que mudam o estado (`executor.py`, `round_log.py`, `plan_state.py --fix`) chamam `publish_safe` por import, com
`--no-panel` para desligar; a falha vira `⚠ painel: …` e não muda o código de saída deles.

Saída: 0, 1 falha ao gravar, 2 uso ou plano que não existe.
"""
import argparse
import glob
import html as H
import json
import os
import re
import sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _kit  # noqa: E402,F401
import plan_md  # noqa: E402
import plan_state  # noqa: E402
from skillkit import measure, sessions_map, visual  # noqa: E402
from skillkit.paths import common_root  # noqa: E402
from skillkit.sessions_cli import list_states  # noqa: E402
from skillkit.visual import PublishError, render_png, save_visual  # noqa: E402,F401

LIVE_FLAGS = ("aberto", "em-curso", "bloqueado")
ABSENT = "sem medição"


def folder_sessions(root, plan_id):
    return os.path.join(root, ".sessions", plan_id.lower())


def manifest_path(root, plan_id):
    return os.path.join(folder_sessions(root, plan_id), "execucao.json")


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def clock_now(at=None):
    if at:
        d = datetime.fromisoformat(str(at).replace("Z", "+00:00"))
        return d if d.tzinfo else d.astimezone()
    return datetime.now().astimezone()


def _ts(s):
    e = sessions_map.epoch(s)
    return e


def age(at_iso, now):
    """'6 min', '2 h 10 min', 'agora'; None sem horário."""
    e = _ts(at_iso)
    if e is None:
        return None
    s = max(0, int(now.timestamp() - e))
    if s < 60:
        return "agora"
    m = s // 60
    return "%d min" % m if m < 60 else "%d h %02d min" % (m // 60, m % 60)


def _h(v):
    return "—" if v is None else plan_md.format_hours(v) + " h"


def consultants(root, plan_id):
    """Os consultores abertos pelo `consult.py`: [{decision, focus, session, agent, state}] dos `D*/consultants.json`."""
    output = []
    for f in sorted(glob.glob(os.path.join(folder_sessions(root, plan_id), "D*", "consultants.json"))):
        m = read_json(f)
        for focus, c in (m.get("focuses") or {}).items():
            if isinstance(c, dict) and c.get("session"):
                output.append({"decision": m.get("decision"), "focus": focus, "session": c["session"], "agent": c.get("agent"),
                              "state": c.get("state")})
    return output


def _cost(entry, root, mrows, srows, now):
    """O custo do executor: o do manifesto (medido no `evidence`) ou, com a sessão viva e Claude, o da janela até agora."""
    med = entry.get("measurement") or {}
    if med.get("cost_usd") is not None:
        return "US$ %.2f" % med["cost_usd"]
    if entry.get("agent", "claude") != "claude" or not mrows:
        return ABSENT
    ev = entry.get("events") or []
    open_step = _ts(ev[0].get("at")) if ev else None
    ids, _ = measure.session_ids(srows, entry.get("session"))
    if open_step is None or not ids:
        return ABSENT
    start = datetime.fromtimestamp(open_step).astimezone()
    r = measure.measure_claude(mrows, ids, (start, now + timedelta(seconds=1)))
    return "US$ %.2f" % r["cost_usd"] if r else ABSENT


def collect(plan, *, at=None, list_json=None, measurements=None, sessions=None, states=None):
    """Os dados do painel, em dicionário (o `render` só formata). `states` ({sessão: state}) dispensa o `brza sessions list`."""
    pl = plan_md.load(plan)
    now = clock_now(at)
    overview = plan_state.state(pl)
    man = read_json(manifest_path(pl.root, pl.id))
    steps_m = man.get("steps") or {}
    mpath = measurements or _find(pl.root, ".measurements/measurements.jsonl")
    spath = sessions or sessions_map.map_file(pl.root)
    mrows = measure.load_jsonl(mpath)
    srows = measure.load_jsonl(spath)
    lines = []
    for p in overview["steps"]:
        e = steps_m.get(p["id"]) or {}
        ev = e.get("events") or []
        state = e.get("state") or p["state"]
        lines.append({"id": p["id"], "title": p["title"], "executes": p["executes"],
                       "executor": e.get("session") or (p["executor"] or "—"), "state": state,
                       "estimated_h": p["estimated_h"], "executed_h": p["executed_h"],
                       "cost": _cost(e, pl.root, mrows, srows, now) if e else ABSENT,
                       "age_text": age(ev[-1].get("at"), now) if ev else None, "manual": not e})
    live_flags = []
    for pid, e in steps_m.items():
        if e.get("state") in LIVE_FLAGS and e.get("session"):
            live_flags.append({"who": "%s (%s)" % (e["session"], pid), "session": e["session"], "agent": e.get("agent"),
                          "role": "executor"})
    for c in consultants(pl.root, pl.id):
        if c.get("state") != "fechado":
            live_flags.append({"who": "%s (%s · %s)" % (c["session"], c["decision"], c["focus"]), "session": c["session"],
                          "agent": c.get("agent"), "role": "consultor"})
    if states is None:
        states = list_states([v["session"] for v in live_flags], list_json=list_json) if live_flags else {}
    for v in live_flags:
        v["state"] = states.get(v["session"])
    rounds = pl.rounds()
    last = None
    if rounds:
        r = rounds[-1]
        last = {"n": r.n, "questions": len(r.questions), "decided": sum(1 for q in r.questions if q.is_decided)}
    h = overview["hours"]
    title = re.sub(r"^PLN-\d+\s*[:—–-]\s*", "", overview["title"] or "")
    return {"plan": pl.id, "title": title, "phase": overview["phase"], "status": overview["status"], "ready": overview["ready"],
            "hours": h, "problems": [p for p in overview["problems"] if p["code"] == "hours-mismatch"],
            "steps": lines, "live": live_flags, "round": last, "at": now.isoformat(timespec="seconds"),
            "next": overview["next"]}


def _find(root, rel):
    for r in (root, common_root(root)):
        p = os.path.join(r, rel)
        if os.path.isfile(p):
            return p
    return os.path.join(root, rel)


CSS = """
html{--fb-bg:#fff;--fb-fg:#171717;--fb-card:#fafafa;--fb-mut:#6b7280;--fb-mutbg:#f1f1f3;--fb-bd:#e5e5e5;--fb-c1:#2563eb;--fb-c2:#16a34a;--fb-c4:#d97706;--fb-de:#dc2626}
html.dark{--fb-bg:#18181b;--fb-fg:#ededed;--fb-card:#232327;--fb-mut:#a1a1aa;--fb-mutbg:#2e2e33;--fb-bd:#3a3a40;--fb-c1:#60a5fa;--fb-c2:#4ade80;--fb-c4:#fbbf24;--fb-de:#f87171}
*{box-sizing:border-box}
body{margin:0;padding:14px 16px 18px;background:var(--background,var(--fb-bg));color:var(--foreground,var(--fb-fg));font:13px/1.45 var(--font-sans,-apple-system,system-ui,sans-serif)}
.mut{color:var(--muted-foreground,var(--fb-mut))} .sm{font-size:11.5px;color:var(--muted-foreground,var(--fb-mut))}
.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,var(--fb-mut))}
h1{font-size:17px;margin:2px 0 2px;line-height:1.25} .meta{font-size:12px;color:var(--muted-foreground,var(--fb-mut))}
h2{font-size:11.5px;margin:18px 0 6px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,var(--fb-mut))}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:12px}
.tile{background:var(--card,var(--fb-card));border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,10px);padding:8px 10px;min-width:0}
.tile b{display:block;font-size:19px;line-height:1.15;font-variant-numeric:tabular-nums} .tile span{font-size:11px;color:var(--muted-foreground,var(--fb-mut))}
.tile.warn{border-color:var(--chart-4,var(--fb-c4))}
.tbl{border-top:1px solid var(--border,var(--fb-bd))}
.row{display:grid;grid-template-columns:minmax(0,2.3fr) minmax(0,1.2fr) minmax(0,1fr) minmax(0,1.1fr) minmax(0,.9fr) minmax(0,.7fr);column-gap:10px;padding:7px 0;border-bottom:1px solid var(--border,var(--fb-bd));align-items:start}
.row>div{min-width:0;overflow-wrap:anywhere} .row.hd{font-size:11px;color:var(--muted-foreground,var(--fb-mut));padding:5px 0}
.row b{display:block} .row .sm{display:block} .num{font-variant-numeric:tabular-nums}
.st{display:inline-block;font-size:11px;font-weight:600;padding:0 6px;border-radius:4px;background:var(--muted,var(--fb-mutbg))}
.st.ok{background:color-mix(in srgb,var(--chart-2,var(--fb-c2)) 22%,transparent)}
.st.run{background:color-mix(in srgb,var(--chart-1,var(--fb-c1)) 22%,transparent)}
.st.alerta{background:color-mix(in srgb,var(--chart-4,var(--fb-c4)) 28%,transparent)}
.st.ruim{background:color-mix(in srgb,var(--destructive,var(--fb-de)) 22%,transparent)}
ul{margin:0;padding-left:18px} li{margin:3px 0}
.panel{container-type:inline-size}
.who{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-clamp:2;overflow:hidden}
.row>[data-l]::before{content:none}
@container (max-width:699px){
.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}
.tbl{border-top:0}
.row.hd{display:none}
.row{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"p s" "x x" "e e" "c c" "l l";row-gap:3px;padding:10px 12px;margin-bottom:8px;border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,10px)}
.who{display:inline;-webkit-line-clamp:unset;line-clamp:unset;overflow:visible}
.c-p{grid-area:p} .c-x{grid-area:x} .c-s{grid-area:s} .c-e{grid-area:e} .c-c{grid-area:c} .c-l{grid-area:l}
.row>[data-l]::before{content:attr(data-l) ": ";color:var(--muted-foreground,var(--fb-mut));font-size:11.5px}
}
"""

CLASS_NAME = {"feito": "ok", "fechado": "ok", "evidencia-gravada": "ok", "em-curso": "run", "aberto": "run",
          "bloqueado": "alerta", "parado": "alerta", "falhou": "ruim"}


def _e(s):
    return H.escape(str(s if s is not None else "—"))


def render_html(D, dark=False):
    h = D["hours"]
    fm, summed = h["frontmatter"], h["summed"]
    warning_text = not h["matches"]

    def tile_h(tile_label, k):
        v = fm.get(k)
        s = _h(v)
        extra = ""
        if warning_text and summed.get(k) is not None and (v is None or abs(v - summed[k]) > plan_state.TOL):
            extra = " ⚠ soma dos passos: %s" % _h(summed[k])
        return '<div class="tile%s"><b>%s</b><span>%s%s</span></div>' % (" warn" if extra else "", _e(s), tile_label, _e(extra))
    done_states = sum(1 for p in D["steps"] if p["state"] in ("feito", "fechado", "evidencia-gravada"))
    rows = []
    for p in D["steps"]:
        step_state = p["state"]
        short_title = p["title"].replace("`", "")
        short_title = short_title if len(short_title) <= 52 else short_title[:51].rstrip() + "…"
        who = str(p["executor"]).replace("`", "")
        exe = _h(p["estimated_h"]) + " × " + (_h(p["executed_h"]) if p["executed_h"] is not None else "—")
        rows.append('<div class="row"><div class="c-p"><b>%s</b>%s<span class="sm">Executa %s</span></div>'
                    '<div class="c-x" data-l="Executor"><span class="who" title="%s">%s</span></div>'
                    '<div class="c-s"><span class="st %s">%s</span></div><div class="c-e num" data-l="Estimado × Executado">%s</div>'
                    '<div class="c-c num" data-l="Custo">%s</div><div class="c-l num" data-l="Último evento">%s</div></div>' % (
                        _e(p["id"]), _e(short_title), _e(", ".join(p["executes"]) or "—"), _e(who), _e(who),
                        CLASS_NAME.get(step_state, ""), _e(step_state), _e(exe), _e(p["cost"]), _e(p["age_text"] or "—")))
    live_flags = "".join("<li>%s · %s · %s</li>" % (_e(v["who"]), _e(v["role"]), _e(v.get("state") or "estado desconhecido"))
                    for v in D["live"]) or '<li class="mut">nenhum aberto</li>'
    r = D["round"]
    round_line = ("R%d — %d pergunta%s, %d decidida%s" % (r["n"], r["questions"], "" if r["questions"] == 1 else "s", r["decided"],
                                                    "" if r["decided"] == 1 else "s")) if r else "sem rodada registrada"
    ready = str(D["ready"] or "—")
    ready = ready if len(ready) <= 90 else ready[:89] + "…"
    body = """<div class="panel"><header><div class="eyebrow">Painel do plano</div><h1>%s — %s</h1>
<div class="meta">fase %s · status %s · ready: %s · estado das %s</div></header>
<section class="tiles">%s%s%s<div class="tile"><b>%d/%d</b><span>passos feitos</span></div></section>
<h2>Os passos</h2>
<div class="tbl"><div class="row hd"><div>Passo</div><div>Executor</div><div>Estado</div><div>Estimado × Executado</div><div>Custo</div><div>Último evento</div></div>%s</div>
<p class="sm">Custo sem medição quando o hook não gravou a sessão (Grok e Antigravity não gravam). Passo sem executor por sessão mostra o estado do plano.</p>
<h2>As sessões vivas</h2><ul>%s</ul>
<h2>A última rodada</h2><p>%s</p></div>""" % (
        _e(D["plan"]), _e(D["title"]), _e(D["phase"]), _e(D["status"]), _e(ready), _e(D["at"][11:16]),
        tile_h("estimado", "estimate_h"), tile_h("executado", "executed_h"), tile_h("restante", "remaining_h"),
        done_states, len(D["steps"]), "".join(rows), live_flags, _e(round_line))
    return ('<!doctype html><html lang="pt-BR"%s><head><meta charset="utf-8"><title>%s — painel</title><style>%s</style>'
            '</head><body>%s</body></html>' % (" class=dark" if dark else "", _e(D["plan"]), CSS, body))


def default_target(root, plan_id, publish_dir=None):
    d = publish_dir or os.environ.get("ORCA_CHAT_SCRATCH_DIR")
    return d or os.path.join(folder_sessions(root, plan_id), "painel")


def publish(plan, *, publish_dir=None, png=None, width=736, at=None, list_json=None, measurements=None, sessions=None,
            states=None):
    """Coleta, renderiza e grava o painel; com `png` (True ou caminho), tira o PNG. Devolve {html, line, png, png_error}.
    Levanta PublishError, OSError, ValueError ou plan_md.PlanNotFound."""
    pl = plan_md.load(plan)
    D = collect(pl, at=at, list_json=list_json, measurements=measurements, sessions=sessions, states=states)
    day = clock_now(at).date().isoformat()
    dest = default_target(pl.root, pl.id, publish_dir)
    saved_path, line = save_visual(render_html(D), pl.id.lower(), "painel", "%s|%s" % (pl.id, day),
                               "%s — painel do plano" % pl.id, publish_dir=dest)
    path_png, error = None, None
    if png:
        path_png = png if isinstance(png, str) else os.path.join(dest, "%s-painel.png" % pl.id.lower())
        error = render_png(saved_path, path_png, width)
        if error:
            path_png = None
    return {"html": saved_path, "line": line, "png": path_png, "png_error": error}


def publish_safe(plan, **kw):
    """Como `publish`, mas nunca levanta: a falha volta em `warning` (`⚠ painel: …`). {html, line, png, png_error, warning}."""
    try:
        r = publish(plan, **kw)
    except (PublishError, OSError, ValueError, KeyError, plan_md.PlanNotFound) as e:
        return {"html": None, "line": None, "png": None, "png_error": None, "warning": "⚠ painel: %s" % e}
    r["warning"] = ("⚠ painel: %s" % r["png_error"]) if r["png_error"] else None
    return r


def emit(r, out=None, err=None):
    """Imprime a linha `::orca-visual` (e o PNG) em `out` e o aviso em `err`."""
    out = out or (lambda s: print(s, flush=True))
    err = err or (lambda s: print(s, file=sys.stderr, flush=True))
    if r.get("line"):
        out(r["line"])
    if r.get("png"):
        out("png: %s" % r["png"])
    if r.get("warning"):
        err(r["warning"])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plan_panel.py", description="o painel do plano")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("publish", "render"):
        s = sub.add_parser(name)
        s.add_argument("plan")
        s.add_argument("--at")
        s.add_argument("--list-json")
        s.add_argument("--measurements")
        s.add_argument("--sessions")
    sub.choices["publish"].add_argument("--publish-dir")
    sub.choices["publish"].add_argument("--png")
    sub.choices["publish"].add_argument("--width", type=int, default=736)
    sub.choices["render"].add_argument("--out", required=True)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    kw = dict(at=a.at, list_json=a.list_json, measurements=a.measurements, sessions=a.sessions)
    try:
        if a.cmd == "render":
            doc = render_html(collect(pl, **kw))
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(doc)
            print(os.path.abspath(a.out))
            return 0
        r = publish(pl, publish_dir=a.publish_dir, png=a.png, width=a.width, **kw)
    except (PublishError, OSError, ValueError) as e:
        print("plan_panel: %s" % e, file=sys.stderr)
        return 1
    print(r["line"])
    if r["png"]:
        print("png: %s" % r["png"])
    elif r["png_error"]:
        print("plan_panel: %s" % r["png_error"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
