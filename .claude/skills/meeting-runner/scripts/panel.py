#!/usr/bin/env python3
"""Gerador do painel da rodada da skill meeting-runner.

Dois estágios, com o JSON `estado-rN.json` como contrato:
  collect N --reuniao reuniao.json   monta (pelo tally.build_estado) e enriquece o estado da rodada
  render ESTADO.json                 estado -> HTML do ::orca-visual (tema do Orca, reserva clara e escura)

Só biblioteca padrão; roda com `python3 -I`.
"""
import argparse
import hashlib
import html as H
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import tally as _tally  # noqa: E402  (a conta da sala e a raiz padrão moram lá, em um lugar só)
import common as _common  # noqa: E402  (o prazo e a duração anunciada da rodada também: a espera lê o mesmo)
LIMITE_HTML = 512 * 1024
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
A_PARTE = 'antigravity'  # runtime que fica fora da média da sala (decisão E-1 do D1)
FORA = 'fora da rodada'  # persona fora do subconjunto da rodada (X18)


# ---------------------------------------------------------------- utilidades

def _t(s):
    """'HH:MM[:SS]' -> datetime; None se vazio ou inválido."""
    if not isinstance(s, str) or not s:
        return None
    s = s.strip().replace('h', ':')
    if s.count(':') == 1:
        s += ':00'
    try:
        return datetime.strptime(s, '%H:%M:%S')
    except ValueError:
        return None


def _e(s):
    """Escapa para HTML; o `∥` (que o visual do chat não desenha) vira `||` só aqui, nunca no JSON do estado."""
    return H.escape(str(s)).replace('∥', '||') if s is not None else ''


def _hm(s):
    """Hora para exibição: HH:MM, ou '—'."""
    t = _t(s)
    return t.strftime('%H:%M') if t else '—'


def _seg(t0, t1):
    """Segundos de t0 a t1 (HH:MM:SS sem data), pela volta mais curta do relógio: 23:58 -> 00:05 dá +420, não -85980."""
    d = (t1 - t0).total_seconds()
    if d < -43200:
        d += 86400
    elif d > 43200:
        d -= 86400
    return d


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _num(v, d=1):
    if not _isnum(v):
        return '—'
    s = f'{v:.{d}f}' if v != int(v) else str(int(v))
    return s.replace('.', ',')


def _dur(s):
    if not _isnum(s):
        return '—'
    s = int(s)
    return f'{s // 60}:{s % 60:02d}' if s >= 60 else f'{s} s'


def _mediana(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def _a_parte(p):
    return str(p.get('runtime') or '').strip().lower() == A_PARTE


# ---------------------------------------------------------------- render (funções puras)

def recortar(S, at=None):
    """Cópia do estado no instante `at` (None = o `gerado`); refina falta/atrasado. Não muta S."""
    S = json.loads(json.dumps(S))
    R = S.setdefault('rodada', {})
    now = at or R.get('gerado')
    tn, tp, ta = _t(now), _t(R.get('prazo')), _t(R.get('aberta'))
    S['_now'] = now
    for p in S.get('personas') or []:
        est = p.get('estado')
        if at and est == 'respondeu' and _t(p.get('respondeu_as')) and _t(at) and _seg(_t(at), _t(p['respondeu_as'])) > 0:
            est = 'falta'
            for k in ('confianca', 'posicao', 'custo_usd', 'tokens', 'latencia_s', 'respondeu_as'):
                p[k] = None
        if est == 'atrasado' and tn and tp and _seg(tp, tn) <= 0:
            est = 'falta'
        if est == 'falta' and tn and tp and _seg(tp, tn) > 0:
            est = 'atrasado'
        p['estado'] = est or 'falta'
        if p['estado'] not in ('respondeu', FORA) and p.get('trabalhando_s') is None and tn and ta:
            p['trabalhando_s'] = max(0, int(_seg(ta, tn)))
    fech = _t(R.get('fechada'))
    if at and fech and tn and _seg(fech, tn) < 0:
        R['fechada'] = None
    return S


def _estado_cel(p):
    if p['estado'] == 'respondeu':
        base = '' if p.get('latencia_fonte') == 'turno' or p.get('latencia_s') is None else '≈'
        return (f'<span class="st ok">respondeu</span><span class="sm">{_e(_hm(p.get("respondeu_as")))}'
                f' · {base}{_dur(p.get("latencia_s"))}</span>')
    if p['estado'] == FORA:
        return '<span class="st wait">fora da rodada</span>'
    cls = 'late' if p['estado'] in ('atrasado', 'erro', 'sem cota') else 'wait'
    ha = f'<span class="sm">há {_dur(p["trabalhando_s"])}</span>' if _isnum(p.get('trabalhando_s')) else ''
    return f'<span class="st {cls}">{_e(p["estado"])}</span>{ha}'


def _conf_cel(p):
    c = p.get('confianca')
    if not _isnum(c):
        return '<div class="cf"><div class="bar"><i style="width:0"></i></div><b class="mut">—</b></div>'
    w = max(0, min(100, c))
    r1 = p.get('confianca_r1')
    dl = ''
    if _isnum(r1):
        d = c - r1
        sinal = '+' if d > 0 else '−' if d < 0 else '±'
        dl = f'<span class="sm">{sinal}{_num(abs(d))} vs R1</span>'
    return (f'<div class="cf"><div class="bar"><i style="width:{_num(w)}%"></i></div>'
            f'<b>{_num(c)}</b></div>{dl}')


def _custo_cel(p):
    if p.get('medicao') == 'pendente':
        return '<span class="mut" title="o hook grava o turno no Stop; gere o estado de novo em ~1 min">medição pendente</span>'
    if p.get('estado') == FORA:
        return '<span class="mut">—</span>'
    if _isnum(p.get('custo_usd')):
        return f'US$ {_num(p["custo_usd"], 2)}'
    tk = p.get('tokens')
    if isinstance(tk, dict) and _isnum(tk.get('entrada')):
        ent = tk['entrada']
        cache = f'<span class="sm">{round(100 * (tk.get("cache") or 0) / ent)}% cache</span>' if ent else ''
        return f'{_num(ent / 1e6, 2)} M{cache}'
    return '<span class="mut" title="o runtime não grava tokens nem custo">sem medição</span>'


def _tags(p, tem_voto):
    out = []
    v = p.get('voto')
    vp = p.get('voto_por_proposta')
    if tem_voto and isinstance(vp, dict) and vp:
        # o voto por proposta (A, B, P1…): as palavras inteiras, sem a letra do voto colidir com a da proposta
        txt = ' · '.join(f'{k}: {str(x).replace("apoio com", "apoio c/")}' for k, x in vp.items())
        out.append(f'<span class="tg">voto {_e(txt)}</span>')
    elif tem_voto and isinstance(v, dict):
        out.append(f'<span class="tg">voto: apoio {_e(v.get("apoio", 0))} · ressalva {_e(v.get("ressalva", 0))}'
                   f' · contra {_e(v.get("contra", 0))}</span>')
    if p.get('virada'):
        rotulo = 'manteve' if p['virada'] == 'não' else p['virada']  # a etiqueta é a própria palavra, sem "virou: virou"
        out.append(f'<span class="tg vir">{_e(rotulo)}</span>')
    elif p.get('virada_antes'):
        out.append(f'<span class="tg">{_e(p["virada_antes"])}</span>')
    if p.get('worklog'):
        ref = os.path.basename(str(p['worklog'])) + (f':{p["linha"]}' if p.get('linha') is not None else '')
        out.append(f'<span class="tg mono" title="seção da rodada no worklog da persona">{_e(ref)}</span>')
    return ''.join(out)


def _linha(p, tem_voto):
    sub = ' · '.join(_e(x) for x in (p.get('runtime'), p.get('modelo'), p.get('esforco')) if x)
    pos = (_e(p['posicao']) if p.get('posicao') else '<span class="mut">fora desta rodada</span>' if p.get('estado') == FORA
           else '<span class="mut">aguardando a seção da rodada</span>')
    return (f'<div class="row"><div class="who"><b>{_e(p.get("nome"))}</b><span class="sm">{sub}</span></div>'
            f'<div>{_estado_cel(p)}</div><div>{_conf_cel(p)}</div><div class="ct">{_custo_cel(p)}</div>'
            f'<div class="pos">{pos}<div class="tgs">{_tags(p, tem_voto)}</div></div></div>')


def _faixa(S, P):
    R = S['rodada']
    a0, a1, tn = _t(R.get('aberta')), _t(R.get('prazo')), _t(S.get('_now'))
    if not (a0 and a1) or _seg(a0, a1) <= 0:
        return ''
    span = _seg(a0, a1)
    dots = ''
    for p in P:
        tr = _t(p.get('respondeu_as')) if p['estado'] == 'respondeu' else None
        if tr:
            x = max(0, min(100, 100 * _seg(a0, tr) / span))
            dots += f'<span class="dot" style="left:{x:.1f}%" title="{_e(p.get("nome"))} {_e(p.get("respondeu_as"))}"></span>'
    if tn:
        nx = max(0, min(100, 100 * _seg(a0, tn) / span))
        dots += f'<span class="now" style="left:{nx:.1f}%"></span>'
    return (f'<div class="tl"><span class="tl-l">{_e(_hm(R.get("aberta")))}</span><div class="track">{dots}</div>'
            f'<span class="tl-r">prazo {_e(_hm(R.get("prazo")))}</span></div>')


def estatisticas(P):
    """Média/mediana da sala (sem o runtime à parte), custo e lista 'sem medição'."""
    done = [p for p in P if p['estado'] == 'respondeu']
    sala = _tally.calc_sala(P)  # a MESMA conta da tabela do chat
    aparte = [p for p in done if _a_parte(p) and _isnum(p.get('confianca'))]
    return {
        'done': done, 'n_media': sala['n'], 'media': sala['media'], 'mediana': sala['mediana'],
        'aparte': aparte,
        'usd': sum(p['custo_usd'] for p in done if _isnum(p.get('custo_usd'))),
        'tok': sum(p['tokens']['entrada'] for p in done
                   if isinstance(p.get('tokens'), dict) and _isnum(p['tokens'].get('entrada'))),
        'semmed': [p.get('nome') for p in done if not _isnum(p.get('custo_usd')) and not p.get('tokens')
                   and p.get('medicao') != 'pendente'],
        'pendentes': [p.get('nome') for p in done if p.get('medicao') == 'pendente'],
    }


def render_html(S, at=None, dark=False):
    S = recortar(S, at)
    R, P = S['rodada'], S.get('personas') or []
    reu = S.get('reuniao') or {}
    sala = S.get('sala') or {}
    cc = S.get('custos_coordenacao') or {}
    now = S.get('_now')
    fechada = R.get('fechada')
    tem_voto = bool(R.get('tem_voto'))
    st = estatisticas(P)
    PP = [p for p in P if p['estado'] != FORA]  # o "n de m" é dos participantes; quem está fora não segura a rodada
    falta = [p.get('nome') for p in PP if p['estado'] != 'respondeu']
    n = R.get('n', '?')
    titulo = R.get('titulo') or ''

    if fechada:
        status = f'{len(st["done"])} de {len(PP)} responderam · fechada às {_e(_hm(fechada))}'
    elif falta:
        status = f'{len(st["done"])} de {len(PP)} responderam · falta {_e(", ".join(map(str, falta)))}'
    else:
        status = f'{len(st["done"])} de {len(PP)} responderam'
    prazo = f' · prazo {_e(_hm(R["prazo"]))}' if R.get('prazo') else ''
    meta = f'aberta {_e(_hm(R.get("aberta")))}{prazo} · {status} · estado das {_e(_hm(now))}'

    aparte = ''.join(f' · {_e(p.get("runtime"))} à parte: {_num(p["confianca"])}' for p in st['aparte'])
    rows = ''.join(_linha(p, tem_voto) for p in P)
    medicoes = [m for m in (S.get('medicoes') or []) if isinstance(m, dict)]
    sintese = [x for x in (S.get('sintese') or [])][:5]
    decisoes = [d for d in (S.get('decisoes') or []) if isinstance(d, dict)]

    med = ''.join(f'<li><span class="tp tp-{_e(m.get("tipo"))}">{_e(m.get("tipo"))}</span>'
                  f'<span class="mq">{_e(m.get("quem"))}</span> {_e(m.get("texto"))}</li>' for m in medicoes) if fechada else ''
    sin = ''.join(f'<li>{_e(x)}</li>' for x in sintese) if fechada else ''

    def _dec(d):
        # `quem` é quem LEVANTOU a decisão (o molde da síntese), não quem a recomenda; voto só sai do campo `votos`
        quem = [str(x) for x in (d.get('quem') or [])]
        lev = f'<span class="sm">levantada por {_e(", ".join(quem[:-1]) + " e " + quem[-1] if len(quem) > 1 else quem[0])}</span>' if quem else ''
        rec = f'<span class="sm">recomendação: {_e(d.get("recomendacao"))}</span>' if d.get('recomendacao') else ''
        votos = f'<span class="sm">{_e(d["votos"])}</span>' if d.get('votos') else ''
        return f'<li><b>{_e(d.get("pergunta"))}</b>{lev}{rec}{votos}</li>'
    dec = ''.join(_dec(d) for d in decisoes) if fechada else ''

    coord = (cc.get('coordenacao_usd') or 0) + (cc.get('revisor_usd') or 0)
    revisor = _num(sala.get('revisor')) if fechada and _isnum(sala.get('revisor')) else '—'
    late_open = '' if fechada else '<p class="sm mut">Medições, síntese e decisões entram quando a rodada fecha.</p>'
    sem_voto = '' if tem_voto else ' Rodada sem voto.'
    semmed = _e(', '.join(map(str, st['semmed']))) or '—'
    total = R.get('custo_rotulo') not in (None, 'da rodada')
    rotulo_custo = 'no total da sessão (sem a janela da rodada)' if total else 'na rodada'
    # X2: o cartão só fala do Codex quando há persona Codex
    tem_codex = any(str(p.get('runtime') or '').strip().lower() == 'codex' for p in P)
    codex = f' · Codex {_num(st["tok"] / 1e6, 2)} M tokens' if tem_codex else ''
    tem_claude = any(str(p.get('runtime') or '').strip().lower() == 'claude' for p in PP)
    cartao_usd = f'US$ {_num(st["usd"], 2)}' if tem_claude else '—'
    cartao_txt = f'personas Claude {rotulo_custo}{codex}' if tem_claude else f'sem persona Claude na rodada{codex}'
    cab_custo = 'Custo (total da sessão)' if total else 'Custo'
    pend = f' Medição pendente: {_e(", ".join(map(str, st["pendentes"])))} (o hook grava no Stop do turno).' if st['pendentes'] else ''
    body = f'''<header>
<div class="eyebrow">Reunião · {_e(reu.get("tema"))}</div>
<h1>Rodada {_e(n)} — {_e(titulo)}</h1>
<div class="meta">{meta}</div>
{_faixa(S, P)}
</header>
<section class="tiles">
<div class="tile"><b>{_num(st["media"])}</b><span>média da sala ({st["n_media"]}/{len(PP)}) · mediana {_num(st["mediana"])}{aparte}</span></div>
<div class="tile"><b>{revisor}</b><span>{_e(sala.get("revisor_nota"))}</span></div>
<div class="tile"><b>{cartao_usd}</b><span>{cartao_txt}</span></div>
<div class="tile"><b>US$ {_num(coord, 2)}</b><span>coordenação e revisor até {_e(_hm(cc.get("ate")))}</span></div>
</section>
<h2>As personas</h2>
<div class="tbl"><div class="row hd"><div>Persona</div><div>Estado</div><div>Confiança</div><div class="ct">{cab_custo}</div></div>{rows}</div>
<p class="sm mut">Latência com ≈: do envio ao marcador, pela coordenação (Grok e Antigravity não gravam turno). Sem medição: {semmed}.{pend}{sem_voto}</p>
{late_open}
{"<h2>As medições da coordenação</h2><ul class='med'>" + med + "</ul>" if med else ""}
{"<h2>A síntese</h2><ol class='sin'>" + sin + "</ol>" if sin else ""}
{"<h2>Para Anderson decidir</h2><ul class='dec'>" + dec + "</ul><p class='sm mut'>As perguntas vão à rodada no chat da coordenação; o painel só mostra.</p>" if dec else ""}'''

    return (f'<!doctype html><html lang="pt-BR"{" class=dark" if dark else ""}><head><meta charset="utf-8">'
            f'<title>Rodada {_e(n)} — {_e(reu.get("tema"))}</title><style>{CSS}</style></head><body>{body}</body></html>')


# ---------------------------------------------------------------- collect

_cabecalho_rodada = _common.cabecalho_rodada  # (titulo, prazo 'HH:MM', duracao_min): o mesmo que o wait_round.py lê


def _estado_da_sessao(state):
    s = str(state or '').lower()
    if any(k in s for k in ('quota', 'cota', 'rate', 'limit')):
        return 'sem cota'
    if any(k in s for k in ('error', 'erro', 'fail', 'crash')):
        return 'erro'
    return None


def _ler_list(list_json):
    """{sessao: state} de `brza sessions list --json`; tolerante a qualquer falha."""
    try:
        if list_json:
            with open(list_json, encoding='utf-8') as f:
                dado = json.load(f)
        else:
            r = subprocess.run(['brza', 'sessions', 'list', '--json'], capture_output=True, text=True, timeout=20)
            dado = json.loads(r.stdout)
        if isinstance(dado, dict):
            dado = dado.get('sessions') or dado.get('items') or []
        return {x['name']: x.get('state') for x in dado if isinstance(x, dict) and x.get('name')}
    except Exception:
        return {}


class ErroManifesto(Exception):
    pass


def collect(reuniao, n, root, *, opened=None, closed=None, list_json=None, at=None, measurements=None,
            sessions=None, codex_dir=None, tally_mod=None, participantes=None, settle=0):
    for k in ('id', 'tema', 'fim'):
        if not reuniao.get(k):
            raise ErroManifesto(f'manifesto sem "{k}" (obrigatório: id, tema, fim)')
    if tally_mod is None:
        sys.path.insert(0, AQUI)
        import tally as tally_mod
    kw = {k: v for k, v in (('measurements', measurements), ('sessions', sessions), ('codex_dir', codex_dir),
                            ('opened', opened), ('closed', closed), ('at', at), ('participantes', participantes),
                            ('settle', settle or None)) if v is not None}
    S = tally_mod.build_estado(reuniao, n, root, **kw)
    R = S.setdefault('rodada', {})
    R.setdefault('n', n)
    pasta = reuniao.get('dir') or '.'
    if not os.path.isabs(pasta):
        pasta = os.path.join(root, pasta)
    rodada_md = os.path.join(pasta, f'rodada-{n}.md')

    titulo, prazo, duracao = _cabecalho_rodada(rodada_md)
    if titulo:
        R['titulo'] = titulo
    R.setdefault('titulo', None)
    R.setdefault('prazo', None)

    if not R.get('aberta'):
        if opened:
            R['aberta'] = opened
        else:
            try:
                R['aberta'] = datetime.fromtimestamp(os.path.getmtime(rodada_md)).strftime('%H:%M:%S')
            except OSError:
                R['aberta'] = None
    if prazo:
        R['prazo'] = prazo
    elif duracao and _t(R.get('aberta')):
        R['prazo'] = (_t(R['aberta']) + timedelta(minutes=duracao)).strftime('%H:%M')
    R['gerado'] = at or datetime.now().strftime('%H:%M:%S')

    P = S.get('personas') or []
    PP = [p for p in P if p.get('estado') != FORA]  # X18: a rodada fecha quando TODOS OS PARTICIPANTES responderam
    R['fechada'] = None
    if PP and all(p.get('estado') == 'respondeu' for p in PP):
        horas = [p['respondeu_as'] for p in PP if _t(p.get('respondeu_as'))]
        if horas:
            ab = _t(R.get('aberta'))
            R['fechada'] = max(horas, key=(lambda h: _seg(ab, _t(h))) if ab else _t)
    R['tem_voto'] = any(p.get('voto') for p in P)

    estados = _ler_list(list_json)
    tn, tp = _t(R['gerado']), _t(R['prazo'])
    for p in P:
        if p.get('estado') == 'falta':
            if tn and tp and _seg(tp, tn) > 0:
                p['estado'] = 'atrasado'
            refinado = _estado_da_sessao(estados.get(p.get('sessao')))
            if refinado:
                p['estado'] = refinado

    for k in ('medicoes', 'sintese', 'decisoes'):
        S.setdefault(k, [])
    S.setdefault('sala', {})
    S.setdefault('avisos', [])
    sintese_path = os.path.join(pasta, f'sintese-{n}.json')
    if os.path.exists(sintese_path):
        with open(sintese_path, encoding='utf-8') as f:
            sj = json.load(f)
        S['medicoes'] = sj.get('medicoes') or []
        S['sintese'] = (sj.get('sintese') or [])[:5]
        S['decisoes'] = sj.get('decisoes') or []
        sala = sj.get('sala') if isinstance(sj.get('sala'), dict) else {}
        for k in ('revisor', 'revisor_nota'):
            v = sala.get(k, sj.get(k))
            if v is not None:
                S['sala'][k] = v
        if sj.get('custos_coordenacao'):
            S['custos_coordenacao'] = sj['custos_coordenacao']
        _tally.aplica_revisor(S['sala'])
        pos = sj.get('posicoes') or {}
        for p in P:
            if p.get('nome') in pos:
                p['posicao'] = pos[p['nome']]
    return S


# ---------------------------------------------------------------- CLI

def _raiz(a):
    return os.path.abspath(a.root) if a.root else _tally.raiz_padrao()


def _cmd_collect(a):
    try:
        root = _raiz(a)
        with open(_tally.resolve_reuniao(a.reuniao, root), encoding='utf-8') as f:
            reuniao = json.load(f)
        if reuniao.get('personas') and not _tally.worklogs_existentes(reuniao, root):
            print(f'panel collect: nenhum worklog existe sob {root} (padrão {reuniao.get("worklog")}); '
                  f'confira --root e o manifesto', file=sys.stderr)
            return 2
        S = collect(reuniao, a.n, root, opened=a.opened, closed=a.closed, list_json=a.list_json, at=a.at,
                    measurements=a.measurements, sessions=a.sessions, codex_dir=a.codex_dir,
                    participantes=a.participantes, settle=a.settle)
    except (ErroManifesto, OSError, ValueError) as ex:
        print(f'panel collect: {ex}', file=sys.stderr)
        return 2
    for av in S.get('avisos') or []:
        print(f'aviso: {av}', file=sys.stderr)
    pasta = reuniao.get('dir') or '.'
    pasta = pasta if os.path.isabs(pasta) else os.path.join(root, pasta)
    out = a.out or os.path.join(pasta, f'estado-r{a.n}.json')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(S, f, ensure_ascii=False, indent=2)
    print(out)
    return 0


def _png(html_path, png, width):
    if not os.path.exists(CHROME):
        print('panel render: Chrome não encontrado; sem PNG', file=sys.stderr)
        return
    subprocess.run([CHROME, '--headless=new', f'--screenshot={png}', f'--window-size={width},2000',
                    '--force-device-scale-factor=1', 'file://' + os.path.abspath(html_path)],
                   capture_output=True, timeout=60)
    print(f'png: {png}' if os.path.exists(png) else 'panel render: o Chrome não gerou o PNG', file=sys.stderr)


def _cmd_render(a):
    try:
        with open(a.estado, encoding='utf-8') as f:
            S = json.load(f)
        doc = render_html(S, a.at, a.dark)
    except (OSError, ValueError, KeyError) as ex:
        print(f'panel render: {ex}', file=sys.stderr)
        return 2
    if len(doc.encode('utf-8')) >= LIMITE_HTML:
        print('panel render: HTML >= 512 KB, o visual não aceita', file=sys.stderr)
        return 1
    R, reu = S.get('rodada') or {}, S.get('reuniao') or {}
    if a.publish_dir:
        rid = str(reu.get('id') or 'reuniao')
        if '/' in rid or '\\' in rid or '..' in rid:
            print(f'panel render: reuniao.id "{rid}" tem caminho; recuso gravar fora de --publish-dir', file=sys.stderr)
            return 1
        rid = re.sub(r'[^\w.-]+', '-', rid).strip('.-') or 'reuniao'
        h = hashlib.sha1(f'{reu.get("id")}|{R.get("n")}'.encode()).hexdigest()[:4]
        nome = f'{rid}-r{R.get("n")}-{h}.html'
        os.makedirs(a.publish_dir, exist_ok=True)
        alvo = os.path.join(a.publish_dir, nome)
        tit = f'Rodada {R.get("n")} — {R.get("titulo") or ""}'.strip(' —')
        tit = re.sub(r'[\x00-\x1f\x7f"{}]+', ' ', tit).replace('\\', ' ')
        tit = ' '.join(tit.split())
        linha = f'::orca-visual{{file="{nome}" title="{tit}"}}'
    else:
        alvo = a.out or os.path.splitext(a.estado)[0] + '.html'
        linha = None
    with open(alvo, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(linha if linha else alvo)
    if a.png:
        _png(alvo, a.png, a.width)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog='panel.py', description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('collect', help='monta e enriquece o estado-rN.json')
    c.add_argument('n', type=int)
    c.add_argument('--reuniao', required=True)
    c.add_argument('--root', help='padrão: o topo do repositório git do cwd')
    c.add_argument('--opened')
    c.add_argument('--closed')
    c.add_argument('--list-json')
    c.add_argument('--at')
    c.add_argument('--out')
    c.add_argument('--measurements')
    c.add_argument('--sessions')
    c.add_argument('--codex-dir')
    c.add_argument('--participantes', nargs='+', metavar='NOME',
                   help='só estes nomes estão na rodada; os outros ficam "fora da rodada" e não seguram o fechamento')
    c.add_argument('--settle', type=float, default=0, metavar='SEG',
                   help='relê as medições a cada 5 s até as pendentes chegarem, por até SEG')
    c.set_defaults(fn=_cmd_collect)
    r = sub.add_parser('render', help='estado -> HTML do ::orca-visual')
    r.add_argument('estado')
    g = r.add_mutually_exclusive_group()
    g.add_argument('--out')
    g.add_argument('--publish-dir')
    r.add_argument('--at')
    r.add_argument('--dark', action='store_true')
    r.add_argument('--png')
    r.add_argument('--width', type=int, default=736)
    r.set_defaults(fn=_cmd_render)
    a = ap.parse_args(argv)
    return a.fn(a)


CSS = '''
html{--fb-bg:#fff;--fb-fg:#171717;--fb-card:#fafafa;--fb-mut:#6b7280;--fb-mutbg:#f1f1f3;--fb-bd:#e5e5e5;--fb-c1:#2563eb;--fb-c2:#16a34a;--fb-c4:#d97706;--fb-de:#dc2626}
html.dark{--fb-bg:#18181b;--fb-fg:#ededed;--fb-card:#232327;--fb-mut:#a1a1aa;--fb-mutbg:#2e2e33;--fb-bd:#3a3a40;--fb-c1:#60a5fa;--fb-c2:#4ade80;--fb-c4:#fbbf24;--fb-de:#f87171}
body{margin:0;padding:14px 16px 18px;background:var(--background,var(--fb-bg));color:var(--foreground,var(--fb-fg));font:13px/1.45 var(--font-sans,-apple-system,system-ui,sans-serif)}
.mut{color:var(--muted-foreground,var(--fb-mut))} .sm{display:block;font-size:11.5px;color:var(--muted-foreground,var(--fb-mut))}
.mono{font-family:var(--font-mono,ui-monospace,monospace)}
.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,var(--fb-mut))}
h1{font-size:17px;margin:2px 0 2px;line-height:1.25} .meta{font-size:12px;color:var(--muted-foreground,var(--fb-mut))}
h2{font-size:11.5px;margin:18px 0 6px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted-foreground,var(--fb-mut))}
.tl{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px;align-items:center;margin-top:8px;font-size:11px;color:var(--muted-foreground,var(--fb-mut))}
.track{position:relative;height:8px;background:var(--muted,var(--fb-mutbg));border-radius:4px}
.dot{position:absolute;top:-1px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:var(--chart-2,var(--fb-c2));border:2px solid var(--background,var(--fb-bg));box-sizing:border-box}
.now{position:absolute;top:-4px;width:2px;height:16px;margin-left:-1px;background:var(--foreground,var(--fb-fg))}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:12px}
.tile{background:var(--card,var(--fb-card));color:var(--card-foreground,var(--fb-fg));border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,10px);padding:8px 10px;min-width:0}
.tile b{display:block;font-size:20px;line-height:1.15;font-variant-numeric:tabular-nums} .tile span{font-size:11px;color:var(--muted-foreground,var(--fb-mut))}
.tbl{border-top:1px solid var(--border,var(--fb-bd))}
.row{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr) minmax(0,1.1fr) minmax(0,.8fr);column-gap:10px;row-gap:2px;padding:7px 0;border-bottom:1px solid var(--border,var(--fb-bd));align-items:start}
.row>div{min-width:0} .row.hd{font-size:11px;color:var(--muted-foreground,var(--fb-mut));padding:5px 0}
.who b{display:block} .ct{text-align:right;font-variant-numeric:tabular-nums}
.pos{grid-column:1/-1;font-size:12.5px} .tgs{display:flex;flex-wrap:wrap;gap:4px;margin-top:3px}
.tg{font-size:10.5px;padding:1px 6px;border-radius:999px;background:var(--muted,var(--fb-mutbg));color:var(--muted-foreground,var(--fb-mut));max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tg.vir{background:color-mix(in srgb,var(--chart-4,var(--fb-c4)) 22%,transparent);color:var(--foreground,var(--fb-fg))}
.st{display:inline-block;font-size:11px;font-weight:600;padding:0 6px;border-radius:4px}
.st.ok{background:color-mix(in srgb,var(--chart-2,var(--fb-c2)) 20%,transparent)}
.st.wait{border:1px dashed var(--border,var(--fb-bd));color:var(--muted-foreground,var(--fb-mut))}
.st.late{background:color-mix(in srgb,var(--destructive,var(--fb-de)) 22%,transparent)}
.cf{display:grid;grid-template-columns:minmax(0,1fr) 26px;gap:6px;align-items:center}
.cf b{text-align:right;font-variant-numeric:tabular-nums}
.bar{height:7px;background:var(--muted,var(--fb-mutbg));border-radius:3px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--chart-1,var(--fb-c1))}
ul,ol{margin:0;padding-left:18px} li{margin:3px 0}
.med{list-style:none;padding:0} .med li{display:block}
.tp{font-size:10px;font-weight:600;text-transform:uppercase;padding:0 5px;border-radius:3px;margin-right:4px;background:var(--muted,var(--fb-mutbg))}
.tp-medido{background:color-mix(in srgb,var(--chart-2,var(--fb-c2)) 20%,transparent)}
.mq{font-size:11.5px;color:var(--muted-foreground,var(--fb-mut));margin-right:2px}
.dec{list-style:none;padding:0} .dec li{border-left:3px solid var(--chart-1,var(--fb-c1));padding:2px 0 2px 8px;margin:6px 0}
@media (max-width:520px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}
.row{grid-template-columns:minmax(0,1fr) minmax(0,1fr)} .row.hd{display:none} .ct{text-align:left} .tg.mono{display:none}}
'''

if __name__ == '__main__':
    sys.exit(main())
