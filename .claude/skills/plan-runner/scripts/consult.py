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
do arquivo e o protocolo de fim), `consultores.json` (o manifesto: sessão, runtime, estado de cada foco) e, um por foco,
`<foco>.md`, que SÓ o consultor grava: tese, "Como fica", `Custo:` · `Se paga:` · `Reabre:` sobre os casos, o ataque às outras
duas, o que enfraquece a própria (`Risco:`) e a última linha `<!-- fim-D<n>: <foco> -->`. A sessão abre no worktree do plano.

O roster padrão (PLN-021/R5.3, confirmada): Claude Opus `high` na arquitetura limpa, Codex no maior esforço na
mudança mínima, Grok no equilíbrio. `--roster arquivo.json` troca: `{"consultores": [{"foco", "agent", "model", "effort",
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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
import executor  # noqa: E402  (o corredor de data e o relógio são os mesmos; o veredito de `close` fica lá)
import plan_md  # noqa: E402
import plan_panel  # noqa: E402
from skillkit import visual  # noqa: E402
from skillkit.paths import corta_medida  # noqa: E402
from skillkit.sessions_cli import close_argv, interpreta_abertura, open_argv, run_brza, run_sessions, wait_brza  # noqa: E402

COTA_MAX = 55
BATIDA = 180
FALLBACK = {"agent": "claude", "model": "claude-sonnet-5-5", "effort": "high"}
ROSTER_PADRAO = {"consultores": [
    {"foco": "arquitetura-limpa", "agent": "claude", "model": "claude-opus-5-5", "effort": "high",
     "fallback": {"agent": "grok", "model": None, "effort": None}},
    {"foco": "mudanca-minima", "agent": "codex", "model": executor.CODEX_MODEL, "effort": "xhigh", "fallback": FALLBACK},
    {"foco": "equilibrio", "agent": "grok", "model": None, "effort": None, "fallback": FALLBACK},
]}
FOCOS = {
    "arquitetura-limpa": "a arquitetura limpa: a estrutura que você defenderia se pudesse refazer, mesmo que custe mais agora",
    "mudanca-minima": "a mudança mínima: o menor desvio do que já existe que resolve, mesmo que deixe dívida",
    "equilibrio": "o equilíbrio: o ponto entre as duas, com o custo e o risco explícitos",
}
RUNTIME_NOME = {"claude": "Claude", "codex": "Codex", "grok": "Grok", "antigravity": "Antigravity"}
RE_ROTULO = re.compile(r"(?:^|(?<=\s))(Tese|Custo|Se paga|Reabre|Risco)\s*:\s*")


def pasta(pl, did):
    return os.path.join(plan_panel.pasta_sessoes(pl.raiz, pl.id), did)


def slug_foco(foco):
    return re.sub(r"[^a-z0-9]+", "-", foco.lower()).strip("-")


def sessao_nome(pl, did, foco):
    n = re.search(r"\d+", pl.id).group(0)
    return "pln%s-%s-%s" % (n, did.lower(), slug_foco(foco)[:22].strip("-"))


def carrega_roster(ref):
    if not ref or ref == "padrao":
        return ROSTER_PADRAO["consultores"]
    with open(ref, encoding="utf-8") as f:
        d = json.load(f)
    lista = d.get("consultores") if isinstance(d, dict) else d
    if not isinstance(lista, list) or not lista or not all(isinstance(x, dict) and x.get("foco") and x.get("agent") for x in lista):
        raise ValueError("o roster pede {\"consultores\": [{foco, agent, …}]}")
    return lista


def cotas():
    """{runtime: pct} do `brza quota --json` (`accounts[].windows[]`); {} se não leu. Vale a conta ativa de cada runtime (a
    maior, se houver mais de uma) e a janela `session`; sem ela (o Grok), a `weekly`."""
    rc, so, _ = run_brza(["quota", "--json"])
    try:
        d = json.loads(so)
    except ValueError:
        return {}
    out = {}
    contas = d.get("accounts") if isinstance(d, dict) else None
    for conta in contas if isinstance(contas, list) else []:
        if not isinstance(conta, dict) or not conta.get("active") or not conta.get("runtime"):
            continue
        janelas = {w.get("name"): w.get("used") for w in conta.get("windows") or [] if isinstance(w, dict)}
        usado = janelas.get("session", janelas.get("weekly"))
        if isinstance(usado, (int, float)):
            out[conta["runtime"]] = max(out.get(conta["runtime"], 0), usado)
    return out


def escolhe(roster, quota):
    """[(entrada efetiva, nota)]: o runtime acima da cota vira o `fallback`."""
    saida = []
    for r in roster:
        pct = quota.get(r["agent"])
        if pct is not None and pct > COTA_MAX and r.get("fallback"):
            fb = dict(r["fallback"])
            ef = {"foco": r["foco"], "agent": fb["agent"], "model": fb.get("model"), "effort": fb.get("effort")}
            saida.append((ef, "%s cortado: %s a %s%% (> %d%%); entra %s" % (r["agent"], r["agent"], pct, COTA_MAX, fb["agent"])))
        else:
            saida.append(({k: r.get(k) for k in ("foco", "agent", "model", "effort")}, None))
    return saida


def prompt(pl, did, foco, brief, arquivo):
    outros = ", ".join(f for f in FOCOS if f != foco) or "as outras alternativas"
    return """Você é consultor do Desenho de {did} do {pln}, numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você não conduz o plano, devolve uma alternativa. Responda em português do Brasil.

## O seu foco
{foco}: {desc}.

## O pedido
{brief}

## O que gravar
Grave SÓ o arquivo {arquivo} e leia o resto do repositório apenas para consulta. Não grave o plano, não commite, não pergunte a Anderson, não decida entre alternativas.

O arquivo tem, nesta ordem:
1. `Tese:` a alternativa do seu foco, numa frase;
2. `## Como fica`: o desenho da alternativa, com o que ela escreve;
3. sobre cada caso do pedido, as linhas `Custo:` · `Se paga:` · `Reabre:` (o que se gasta e quando é cobrado; quando o ganho cobre o custo, ou "nunca"; o que a escolha reabre);
4. `## Ataque às outras`: o ataque às outras alternativas ({outros});
5. `Risco:` o que enfraquece a sua própria alternativa;
6. a última linha, sozinha: `<!-- fim-{did}: {foco} -->`.

## O fim
Termine o arquivo com o marcador e envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o encerramento.
""".format(did=did, pln=pl.id, foco=foco, desc=FOCOS.get(foco, foco), brief=brief.strip(), arquivo=arquivo, outros=outros)


def le_man(pl, did):
    d = plan_panel.le_json(os.path.join(pasta(pl, did), "consultores.json"))
    d.setdefault("focos", {})
    return d


def salva_man(pl, did, m):
    p = os.path.join(pasta(pl, did), "consultores.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = "%s.%d.tmp" % (p, os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, p)


def _carrega(a, c):
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        c.err("erro: %s" % e)
        return None, None
    did = a.decisao.upper()
    if pl.desenho(did) is None:
        c.err("erro: o Desenho do %s não tem o item %s" % (pl.id, did))
        return None, None
    return pl, did


def chegou(pl, did, foco, arquivo):
    """O arquivo do foco termina no marcador `<!-- fim-D<n>: <foco> -->` (última linha não vazia)."""
    try:
        with open(arquivo, encoding="utf-8") as f:
            linhas = [l.rstrip() for l in corta_medida(f.read()).split("\n") if l.strip()]
    except OSError:
        return False
    return bool(linhas) and linhas[-1] == "<!-- fim-%s: %s -->" % (did, foco)


# ---------------------------------------------------------------- open

def cmd_open(a, c):
    pl, did = _carrega(a, c)
    if pl is None:
        return 2
    try:
        with open(a.brief, encoding="utf-8") as f:
            brief = f.read()
    except OSError as e:
        c.err("erro: não li o --brief: %s" % e)
        return 2
    try:
        roster = carrega_roster(a.roster)
    except (OSError, ValueError) as e:
        c.err("erro: roster: %s" % e)
        return 2
    quota = cotas()
    if not quota:
        c.err("⚠ não li o `brza quota --json`: nenhum runtime foi cortado por cota")
    escolhidos = escolhe(roster, quota)
    dpasta = pasta(pl, did)
    m = le_man(pl, did)
    m.update({"decisao": did, "plano": pl.id})
    linhas = []
    for ef, nota in escolhidos:
        foco = ef["foco"]
        ef["model"], ef["effort"], aviso = executor.effective_model_effort(ef["agent"], ef.get("model"), ef.get("effort"))
        if aviso:
            c.err("⚠ %s: %s" % (foco, aviso))
        nome = sessao_nome(pl, did, foco)
        arquivo = os.path.join(dpasta, "%s.md" % slug_foco(foco))
        ppath = os.path.join(dpasta, "prompt-%s.md" % slug_foco(foco))
        argv = open_argv(nome, agent=ef["agent"], checkout=pl.raiz, prompt_file=ppath, model=ef.get("model"),
                         effort=ef.get("effort"), title="%s %s: consultor %s" % (pl.id, did, foco), rename=True)
        if a.dry_run:
            c.out("[dry-run] %s" % (nota or "sem corte de cota"))
            c.out("[dry-run] prompt: %s" % ppath)
            c.out("[dry-run] brza sessions " + shlex.join(argv))
            continue
        os.makedirs(dpasta, exist_ok=True)
        with open(ppath, "w", encoding="utf-8") as f:
            f.write(prompt(pl, did, slug_foco(foco), brief, arquivo))
        rc, so, se = run_sessions(argv)
        res = interpreta_abertura(rc, so, se)
        if res in ("nao-abriu", "falha"):
            c.err("%s não abriu (%s): leia o `pending-*.json` citado antes de relançar; paro aqui.\n%s" % (
                nome, res, ((se or "") + (so or "")).strip()[:300]))
            salva_man(pl, did, m)
            return 1
        if res == "sem-id":
            c.err("⚠ %s abriu sem o id do provedor; o `wait` o grava depois. Não relance." % nome)
        if res == "ja":
            c.err("⚠ %s já estava aberta; não reabri." % nome)
        m["focos"][slug_foco(foco)] = {"sessao": nome, "agent": ef["agent"], "model": ef.get("model"), "effort": ef.get("effort"),
                                       "arquivo": os.path.relpath(arquivo, pl.raiz), "estado": "aberto", "corte": nota,
                                       "aberto_em": executor.iso(c.clock())}
        linhas.append((slug_foco(foco), nome, ef, arquivo, nota))
    if a.dry_run:
        return 0
    if a.brief and os.path.abspath(a.brief) != os.path.join(dpasta, "brief.md"):
        with open(os.path.join(dpasta, "brief.md"), "w", encoding="utf-8") as f:
            f.write(brief)
    salva_man(pl, did, m)
    c.out("| Foco | Sessão | Runtime | Modelo | Esforço | Arquivo |")
    c.out("| :-- | :-- | :-- | :-- | :-- | :-- |")
    for foco, nome, ef, arquivo, _ in linhas:
        c.out("| %s | %s | %s | %s | %s | %s |" % (foco, nome, RUNTIME_NOME.get(ef["agent"], ef["agent"]),
                                                    ef.get("model") or "padrão do runtime", ef.get("effort") or "padrão", arquivo))
    for _, _, _, _, nota in linhas:
        if nota:
            c.out("cota: %s" % nota)
    if not a.no_panel:
        plan_panel.emite(plan_panel.publica_seguro(pl), c.out, c.err)
    return 0


# ---------------------------------------------------------------- wait

def cmd_wait(a, c):
    pl, did = _carrega(a, c)
    if pl is None:
        return 2
    m = le_man(pl, did)
    focos = m["focos"]
    if not focos:
        c.err("erro: %s não tem consultores abertos (rode `open`)" % did)
        return 2
    fim = c.clock() + a.timeout
    vistos_sem = set()
    falhou = []
    erros = 0
    ultima_batida = c.clock()

    def faltam():
        return [f for f, v in focos.items() if v.get("estado") not in ("entregou", "falhou", "fechado")]

    def resumo(prefixo):
        ja = [f for f, v in focos.items() if v.get("estado") == "entregou"]
        fa = faltam()
        return "%s %d/%d — entregaram %s; faltam %s" % (prefixo, len(ja), len(focos), ", ".join(ja) or "nenhum", ", ".join(fa) or "nenhum")

    def varre():
        for f in faltam():
            v = focos[f]
            if chegou(pl, did, f, os.path.join(pl.raiz, v["arquivo"])):
                v["estado"] = "entregou"
                v["entregue_em"] = executor.iso(c.clock())
                c.out("%s · %s entregou (%s)" % (did, f, RUNTIME_NOME.get(v["agent"], v["agent"])))
                c.out(resumo("%s ·" % did))
    varre()
    while faltam() and c.clock() < fim:
        nomes = {focos[f]["sessao"]: f for f in faltam()}
        trecho = min(fim - c.clock(), BATIDA)
        ini = c.clock()
        rc, dado = wait_brza(list(nomes), trecho, any_=True)
        if dado.get("error"):
            erros += 1
            action, msg, perdida = executor.wait_error_verdict(rc, dado["error"], erros, list(nomes))
            c.err(msg)
            if action == "stop":
                salva_man(pl, did, m)
                return 1
            if action == "missing":
                focos[nomes[perdida]]["estado"] = "falhou"
                falhou.append(nomes[perdida])
                c.out("%s · %s falhou: a sessão %s não existe mais; a espera segue com as outras" % (did, nomes[perdida], perdida))
                erros = 0
            else:
                c.sleep(executor.WAIT_ERROR_PAUSE)
            continue
        erros = 0
        sem_fim = False
        for row in dado.get("done") or []:
            f = nomes.get(row.get("name"))
            if f is None:
                continue
            if row.get("outcome") == "failed":
                focos[f]["estado"] = "falhou"
                falhou.append(f)
                c.out("%s · %s falhou: `brza sessions read %s --last`" % (did, f, focos[f]["sessao"]))
            elif not chegou(pl, did, f, os.path.join(pl.raiz, focos[f]["arquivo"])):
                sem_fim = True
                if f not in vistos_sem:
                    vistos_sem.add(f)
                    c.out("%s · %s: o turno acabou sem o marcador `<!-- fim-%s: %s -->`; a espera segue" % (did, f, did, f))
        varre()
        if not faltam():
            break
        if sem_fim:
            c.sleep(min(5, max(0, fim - c.clock())))
        elif c.clock() - ini < trecho and (dado.get("timed_out") or rc == 75):
            c.sleep(max(0, trecho - (c.clock() - ini)))
        if c.clock() < fim and faltam() and c.clock() - ultima_batida >= BATIDA:
            ultima_batida = c.clock()
            c.out(resumo("%s · em curso;" % did))
    salva_man(pl, did, m)
    if falhou:
        return 1
    if faltam():
        c.out("prazo: faltam %s; `table` mostra o que há" % ", ".join(faltam()))
        return 75
    return 0


# ---------------------------------------------------------------- table

LINHAS = (("Tese", "tese"), ("Custo", "custo"), ("Se paga", "se_paga"), ("Reabre", "reabre"), ("Risco", "risco"))


def le_arquivo(texto):
    """{tese, custo, se_paga, reabre, risco}: cada rótulo pode repetir (um por caso) e as ocorrências se juntam com ` / `."""
    campos = {k: [] for _, k in LINHAS}
    atual = None
    for linha in corta_medida(texto).split("\n"):
        s = re.sub(r"\*\*|`", "", linha.strip())
        s = re.sub(r"^[-*]\s+", "", s)
        if not s or s.startswith("<!--"):
            atual = None
            continue
        if s.startswith("#"):
            atual = None
            continue
        ms = list(RE_ROTULO.finditer(s))
        achou = bool(ms)
        for i, mm in enumerate(ms):
            fim = ms[i + 1].start() if i + 1 < len(ms) else len(s)
            valor = s[mm.end():fim].strip().rstrip("·").strip()
            chave = {"tese": "tese", "custo": "custo", "se paga": "se_paga", "reabre": "reabre", "risco": "risco"}[mm.group(1).lower()]
            campos[chave].append(valor)
            atual = chave
        if not achou and atual:
            campos[atual][-1] = (campos[atual][-1] + " " + s).strip()
    return {k: " / ".join(v) for k, v in campos.items()}


def cel(v):
    return (v or "—").replace("|", "\\|").replace("\n", " ")


def tabela_md(focos, dados):
    cab = "| | " + " | ".join("%s (%s)" % (f, RUNTIME_NOME.get(focos[f]["agent"], focos[f]["agent"])) for f in focos) + " |"
    sep = "| :-- |" + " :-- |" * len(focos)
    corpo = ["| **%s** | %s |" % (rot, " | ".join(cel(dados[f].get(k) if dados[f] else ("(não entregou)" if k == "tese" else None)) for f in focos))
             for rot, k in LINHAS]
    return "\n".join([cab, sep, *corpo])


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


def render_html(did, pln, focos, dados):
    cab = "".join("<th>%s<small>%s</small></th>" % (H.escape(f), H.escape("%s%s" % (RUNTIME_NOME.get(v["agent"], v["agent"]),
                                                                                    (" · " + v["effort"]) if v.get("effort") else "")))
                  for f, v in focos.items())
    corpo = ""
    for rot, k in LINHAS:
        tds = ""
        for f in focos:
            d = dados[f]
            if d is None:
                tds += '<td class="nao">%s</td>' % ("(não entregou)" if k == "tese" else "—")
            else:
                tds += "<td>%s</td>" % H.escape(d.get(k) or "—")
        corpo += '<tr><td class="r">%s</td>%s</tr>' % (rot, tds)
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>%s %s — consultores</title><style>%s</style></head>'
            '<body><div class="eyebrow">Consultores do Desenho</div><h1>%s · %s</h1><table><thead><tr><th></th>%s</tr></thead>'
            '<tbody>%s</tbody></table></body></html>' % (H.escape(pln), did, CSS, H.escape(pln), did, cab, corpo))


def cmd_table(a, c):
    pl, did = _carrega(a, c)
    if pl is None:
        return 2
    focos = le_man(pl, did)["focos"]
    if not focos:
        c.err("erro: %s não tem consultores abertos" % did)
        return 2
    dados = {}
    for f, v in focos.items():
        arq = os.path.join(pl.raiz, v["arquivo"])
        if chegou(pl, did, f, arq):
            with open(arq, encoding="utf-8") as fh:
                dados[f] = le_arquivo(fh.read())
            for rot, k in LINHAS:
                if not dados[f].get(k):
                    c.err("⚠ %s: o arquivo não traz `%s:`" % (f, rot))
        else:
            dados[f] = None
            c.err("⚠ %s: sem arquivo com o marcador `<!-- fim-%s: %s -->`; coluna vazia" % (f, did, f))
    c.out(tabela_md(focos, dados))
    try:
        dest = plan_panel.destino_padrao(pl.raiz, pl.id, a.publish_dir)
        alvo, linha = visual.salva_visual(render_html(did, pl.id, focos, dados), pl.id.lower(), did.lower(),
                                          "%s|%s|%s" % (pl.id, did, c.hoje()), "%s %s — consultores lado a lado" % (pl.id, did),
                                          publish_dir=dest)
    except (visual.ErroPublicacao, OSError) as e:
        c.err("⚠ visual: %s" % e)
        return 0
    c.out(linha)
    if a.png:
        erro = visual.gera_png(alvo, a.png, 736)
        c.out("png: %s" % a.png) if not erro else c.err("⚠ png: %s" % erro)
    return 0


# ---------------------------------------------------------------- close

def cmd_close(a, c):
    pl, did = _carrega(a, c)
    if pl is None:
        return 2
    m = le_man(pl, did)
    if not m["focos"]:
        c.err("erro: %s não tem consultores abertos" % did)
        return 2
    codigos = []
    for f, v in m["focos"].items():
        rc, so, se = run_sessions(close_argv(v["sessao"], "close"))
        try:
            d = json.loads(so)
        except ValueError:
            d = None
        if isinstance(d, dict) and isinstance(d.get("results"), list) and d["results"]:
            d = d["results"][0]
        st = d.get("status") if isinstance(d, dict) else None
        if st in ("released", "already_released"):
            v["estado"] = "fechado"
            c.out("%s · %s fechada (%s)" % (did, f, st))
            codigos.append(0)
        elif st == "closing":
            c.out("%s · %s: pedido de encerramento enviado; NÃO está fechada (closing); rode `close` de novo depois" % (did, f))
            codigos.append(0)
        elif st in executor.INCERTOS:
            c.err("%s · %s: incerto (%s): não repita às cegas" % (did, f, st))
            codigos.append(75)
        else:
            c.err("%s · %s: não fechada (%s, rc %s)" % (did, f, st or "sem JSON", rc))
            codigos.append(1)
    salva_man(pl, did, m)
    return 1 if 1 in codigos else 75 if 75 in codigos else 0


def main(argv=None, *, out=None, err=None, clock=None, sleep=None):
    ap = argparse.ArgumentParser(prog="consult.py", description="os consultores do Desenho em sessões")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("open", "wait", "table", "close"):
        s = sub.add_parser(nome)
        s.add_argument("plano")
        s.add_argument("decisao")
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
