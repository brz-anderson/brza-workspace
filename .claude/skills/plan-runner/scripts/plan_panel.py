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

Os scripts que mudam o estado (`executor.py`, `round_log.py`, `plan_state.py --fix`) chamam `publica_seguro` por import, com
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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
import plan_md  # noqa: E402
import plan_state  # noqa: E402
from skillkit import measure, sessions_map, visual  # noqa: E402
from skillkit.paths import common_root  # noqa: E402
from skillkit.sessions_cli import list_states  # noqa: E402
from skillkit.visual import ErroPublicacao, gera_png, salva_visual  # noqa: E402,F401

VIVOS = ("aberto", "em-curso", "bloqueado")
SEM = "sem medição"


def pasta_sessoes(raiz, plan_id):
    return os.path.join(raiz, ".sessions", plan_id.lower())


def manifesto_path(raiz, plan_id):
    return os.path.join(pasta_sessoes(raiz, plan_id), "execucao.json")


def le_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def agora(at=None):
    if at:
        d = datetime.fromisoformat(str(at).replace("Z", "+00:00"))
        return d if d.tzinfo else d.astimezone()
    return datetime.now().astimezone()


def _ts(s):
    e = sessions_map.epoch(s)
    return e


def idade(at_iso, now):
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
    return "—" if v is None else plan_md.fmt_horas(v) + " h"


def consultores(raiz, plan_id):
    """Os consultores abertos pelo `consult.py`: [{decisao, foco, sessao, agent, estado}] dos `D*/consultores.json`."""
    saida = []
    for f in sorted(glob.glob(os.path.join(pasta_sessoes(raiz, plan_id), "D*", "consultores.json"))):
        m = le_json(f)
        for foco, c in (m.get("focos") or {}).items():
            if isinstance(c, dict) and c.get("sessao"):
                saida.append({"decisao": m.get("decisao"), "foco": foco, "sessao": c["sessao"], "agent": c.get("agent"),
                              "estado": c.get("estado")})
    return saida


def _custo(entry, raiz, mrows, srows, now):
    """O custo do executor: o do manifesto (medido no `evidence`) ou, com a sessão viva e Claude, o da janela até agora."""
    med = entry.get("medicao") or {}
    if med.get("custo_usd") is not None:
        return "US$ %.2f" % med["custo_usd"]
    if entry.get("agent", "claude") != "claude" or not mrows:
        return SEM
    ev = entry.get("eventos") or []
    abre = _ts(ev[0].get("at")) if ev else None
    ids, _ = measure.session_ids(srows, entry.get("sessao"))
    if abre is None or not ids:
        return SEM
    ini = datetime.fromtimestamp(abre).astimezone()
    r = measure.measure_claude(mrows, ids, (ini, now + timedelta(seconds=1)))
    return "US$ %.2f" % r["custo_usd"] if r else SEM


def coleta(plano, *, at=None, list_json=None, measurements=None, sessions=None, states=None):
    """Os dados do painel, em dicionário (o `render` só formata). `states` ({sessão: state}) dispensa o `brza sessions list`."""
    pl = plan_md.carrega(plano)
    now = agora(at)
    est = plan_state.estado(pl)
    man = le_json(manifesto_path(pl.raiz, pl.id))
    passos_m = man.get("passos") or {}
    mpath = measurements or _achar(pl.raiz, ".measurements/measurements.jsonl")
    spath = sessions or sessions_map.map_file(pl.raiz)
    mrows = measure.load_jsonl(mpath)
    srows = measure.load_jsonl(spath)
    linhas = []
    for p in est["passos"]:
        e = passos_m.get(p["id"]) or {}
        ev = e.get("eventos") or []
        estado = e.get("estado") or p["estado"]
        linhas.append({"id": p["id"], "titulo": p["titulo"], "executa": p["executa"],
                       "executor": e.get("sessao") or (p["executor"] or "—"), "estado": estado,
                       "estimado_h": p["estimado_h"], "executado_h": p["executado_h"],
                       "custo": _custo(e, pl.raiz, mrows, srows, now) if e else SEM,
                       "idade": idade(ev[-1].get("at"), now) if ev else None, "manual": not e})
    vivos = []
    for pid, e in passos_m.items():
        if e.get("estado") in VIVOS and e.get("sessao"):
            vivos.append({"quem": "%s (%s)" % (e["sessao"], pid), "sessao": e["sessao"], "agent": e.get("agent"),
                          "papel": "executor"})
    for c in consultores(pl.raiz, pl.id):
        if c.get("estado") != "fechado":
            vivos.append({"quem": "%s (%s · %s)" % (c["sessao"], c["decisao"], c["foco"]), "sessao": c["sessao"],
                          "agent": c.get("agent"), "papel": "consultor"})
    if states is None:
        states = list_states([v["sessao"] for v in vivos], list_json=list_json) if vivos else {}
    for v in vivos:
        v["state"] = states.get(v["sessao"])
    rod = pl.rodadas()
    ultima = None
    if rod:
        r = rod[-1]
        ultima = {"n": r.n, "perguntas": len(r.perguntas), "decididas": sum(1 for q in r.perguntas if q.decidida)}
    h = est["horas"]
    titulo = re.sub(r"^PLN-\d+\s*[:—–-]\s*", "", est["titulo"] or "")
    return {"plano": pl.id, "titulo": titulo, "phase": est["phase"], "status": est["status"], "ready": est["ready"],
            "horas": h, "problemas": [p for p in est["problemas"] if p["codigo"] == "hours-mismatch"],
            "passos": linhas, "vivos": vivos, "rodada": ultima, "agora": now.isoformat(timespec="seconds"),
            "proximo": est["proximo"]}


def _achar(raiz, rel):
    for r in (raiz, common_root(raiz)):
        p = os.path.join(r, rel)
        if os.path.isfile(p):
            return p
    return os.path.join(raiz, rel)


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
@media (max-width:520px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))} .row{grid-template-columns:minmax(0,1fr) minmax(0,1fr)} .row.hd{display:none}}
"""

CLASSE = {"feito": "ok", "fechado": "ok", "evidencia-gravada": "ok", "em-curso": "run", "aberto": "run",
          "bloqueado": "alerta", "parado": "alerta", "falhou": "ruim"}


def _e(s):
    return H.escape(str(s if s is not None else "—"))


def render_html(D, dark=False):
    h = D["horas"]
    fm, som = h["frontmatter"], h["somado"]
    aviso = not h["confere"]

    def tile_h(rot, k):
        v = fm.get(k)
        s = _h(v)
        extra = ""
        if aviso and som.get(k) is not None and (v is None or abs(v - som[k]) > plan_state.TOL):
            extra = " ⚠ soma dos passos: %s" % _h(som[k])
        return '<div class="tile%s"><b>%s</b><span>%s%s</span></div>' % (" warn" if extra else "", _e(s), rot, _e(extra))
    feitos = sum(1 for p in D["passos"] if p["estado"] in ("feito", "fechado", "evidencia-gravada"))
    rows = []
    for p in D["passos"]:
        est = p["estado"]
        tit = p["titulo"].replace("`", "")
        tit = tit if len(tit) <= 52 else tit[:51].rstrip() + "…"
        quem = str(p["executor"]).replace("`", "")
        quem = quem if len(quem) <= 30 else quem[:29].rstrip() + "…"
        exe = _h(p["estimado_h"]) + " × " + (_h(p["executado_h"]) if p["executado_h"] is not None else "—")
        rows.append('<div class="row"><div><b>%s</b>%s<span class="sm">Executa %s</span></div><div>%s</div>'
                    '<div><span class="st %s">%s</span></div><div class="num">%s</div><div class="num">%s</div>'
                    '<div class="num">%s</div></div>' % (
                        _e(p["id"]), _e(tit), _e(", ".join(p["executa"]) or "—"), _e(quem),
                        CLASSE.get(est, ""), _e(est), _e(exe), _e(p["custo"]), _e(p["idade"] or "—")))
    vivos = "".join("<li>%s · %s · %s</li>" % (_e(v["quem"]), _e(v["papel"]), _e(v.get("state") or "estado desconhecido"))
                    for v in D["vivos"]) or '<li class="mut">nenhum aberto</li>'
    r = D["rodada"]
    rod = ("R%d — %d pergunta%s, %d decidida%s" % (r["n"], r["perguntas"], "" if r["perguntas"] == 1 else "s", r["decididas"],
                                                    "" if r["decididas"] == 1 else "s")) if r else "sem rodada registrada"
    ready = str(D["ready"] or "—")
    ready = ready if len(ready) <= 90 else ready[:89] + "…"
    body = """<header><div class="eyebrow">Painel do plano</div><h1>%s — %s</h1>
<div class="meta">fase %s · status %s · ready: %s · estado das %s</div></header>
<section class="tiles">%s%s%s<div class="tile"><b>%d/%d</b><span>passos feitos</span></div></section>
<h2>Os passos</h2>
<div class="tbl"><div class="row hd"><div>Passo</div><div>Executor</div><div>Estado</div><div>Estimado × Executado</div><div>Custo</div><div>Último evento</div></div>%s</div>
<p class="sm">Custo sem medição quando o hook não gravou a sessão (Grok e Antigravity não gravam). Passo sem executor por sessão mostra o estado do plano.</p>
<h2>As sessões vivas</h2><ul>%s</ul>
<h2>A última rodada</h2><p>%s</p>""" % (
        _e(D["plano"]), _e(D["titulo"]), _e(D["phase"]), _e(D["status"]), _e(ready), _e(D["agora"][11:16]),
        tile_h("estimado", "estimate_h"), tile_h("executado", "executed_h"), tile_h("restante", "remaining_h"),
        feitos, len(D["passos"]), "".join(rows), vivos, _e(rod))
    return ('<!doctype html><html lang="pt-BR"%s><head><meta charset="utf-8"><title>%s — painel</title><style>%s</style>'
            '</head><body>%s</body></html>' % (" class=dark" if dark else "", _e(D["plano"]), CSS, body))


def destino_padrao(raiz, plan_id, publish_dir=None):
    d = publish_dir or os.environ.get("ORCA_CHAT_SCRATCH_DIR")
    return d or os.path.join(pasta_sessoes(raiz, plan_id), "painel")


def publica(plano, *, publish_dir=None, png=None, width=736, at=None, list_json=None, measurements=None, sessions=None,
            states=None):
    """Coleta, renderiza e grava o painel; com `png` (True ou caminho), tira o PNG. Devolve {html, linha, png, png_erro}.
    Levanta ErroPublicacao, OSError, ValueError ou plan_md.PlanoNaoEncontrado."""
    pl = plan_md.carrega(plano)
    D = coleta(pl, at=at, list_json=list_json, measurements=measurements, sessions=sessions, states=states)
    dia = agora(at).date().isoformat()
    dest = destino_padrao(pl.raiz, pl.id, publish_dir)
    alvo, linha = salva_visual(render_html(D), pl.id.lower(), "painel", "%s|%s" % (pl.id, dia),
                               "%s — painel do plano" % pl.id, publish_dir=dest)
    caminho_png, erro = None, None
    if png:
        caminho_png = png if isinstance(png, str) else os.path.join(dest, "%s-painel.png" % pl.id.lower())
        erro = gera_png(alvo, caminho_png, width)
        if erro:
            caminho_png = None
    return {"html": alvo, "linha": linha, "png": caminho_png, "png_erro": erro}


def publica_seguro(plano, **kw):
    """Como `publica`, mas nunca levanta: a falha volta em `aviso` (`⚠ painel: …`). {html, linha, png, png_erro, aviso}."""
    try:
        r = publica(plano, **kw)
    except (ErroPublicacao, OSError, ValueError, KeyError, plan_md.PlanoNaoEncontrado) as e:
        return {"html": None, "linha": None, "png": None, "png_erro": None, "aviso": "⚠ painel: %s" % e}
    r["aviso"] = ("⚠ painel: %s" % r["png_erro"]) if r["png_erro"] else None
    return r


def emite(r, out=None, err=None):
    """Imprime a linha `::orca-visual` (e o PNG) em `out` e o aviso em `err`."""
    out = out or (lambda s: print(s, flush=True))
    err = err or (lambda s: print(s, file=sys.stderr, flush=True))
    if r.get("linha"):
        out(r["linha"])
    if r.get("png"):
        out("png: %s" % r["png"])
    if r.get("aviso"):
        err(r["aviso"])


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plan_panel.py", description="o painel do plano")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("publish", "render"):
        s = sub.add_parser(nome)
        s.add_argument("plano")
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
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    kw = dict(at=a.at, list_json=a.list_json, measurements=a.measurements, sessions=a.sessions)
    try:
        if a.cmd == "render":
            doc = render_html(coleta(pl, **kw))
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(doc)
            print(os.path.abspath(a.out))
            return 0
        r = publica(pl, publish_dir=a.publish_dir, png=a.png, width=a.width, **kw)
    except (ErroPublicacao, OSError, ValueError) as e:
        print("plan_panel: %s" % e, file=sys.stderr)
        return 1
    print(r["linha"])
    if r["png"]:
        print("png: %s" % r["png"])
    elif r["png_erro"]:
        print("plan_panel: %s" % r["png_erro"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
