#!/usr/bin/env python3
"""Gerador do painel da rodada da skill meeting-runner.

Dois estágios, com o JSON `estado-rN.json` como contrato, e dois atalhos:
  collect N --reuniao reuniao.json   monta (pelo tally.build_estado) e enriquece o estado da rodada
  render ESTADO.json                 estado -> HTML do ::orca-visual (tema do Orca, reserva clara e escura)
  publish N --reuniao reuniao.json   collect + render + PNG de uma vez; imprime a linha `::orca-visual` e `png: <caminho>`
                                     (o mesmo que o `wait_round.py` faz sozinho; use depois de gravar o `sintese-N.json`).
                                     `--publish-dir` padrão `$ORCA_CHAT_SCRATCH_DIR`, senão a pasta da reunião (avisa);
                                     PNG padrão `<pasta da reunião>/painel-rN.png`, `--png ARQ` troca, `--no-png` tira.
                                     Aceita os argumentos do `collect` (`--opened`, `--closed`, `--participantes`,
                                     `--root`, `--sessions`, `--measurements`, `--at`, `--settle`…).
  sintese --reuniao reuniao.json     o visual da reunião inteira: lê da pasta da reunião todos os `estado-rN.json` e
                                     `sintese-N.json` e o `sintese-final.json` opcional; arquivo `<id>-sintese-<hash>.html`,
                                     `--publish-dir` (padrão `$ORCA_CHAT_SCRATCH_DIR`, senão a pasta da reunião com aviso, como no `publish`), `--out` (grava
                                     ali e imprime a linha com o nome do arquivo); imprime SEMPRE a linha `::orca-visual`; PNG por
                                     padrão em `<pasta da reunião>/sintese.png` (`--png ARQ`, `--no-png`), com `png: …`. Mostra cabeçalho, cartões
                                     (revisor, sala, votos, custo), o gráfico da média da sala e do revisor por rodada, a
                                     tabela por persona, a síntese e as decisões do último `sintese-N.json`.

O `sintese-final.json` (todas as chaves opcionais) é escrito pela coordenação: `titulo`, `conclusao` (texto),
`classificacao` [{uso, frente, hoje, fato, hoje_tipo?}] (`hoje` vira selo; `hoje_tipo` = go|wait|sh|evo|out força a cor),
`barras` [{rotulo, detalhe, valor, maximo, texto, tom?}] (`tom` = ok|ruim|alerta|neutro), `fases` [{nome, estimado, rotulo?}],
`proxima_rodada` [{pergunta, recomendacao}], `rodape` (texto).

Só biblioteca padrão; roda com `python3 -I`.
"""
import argparse
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
import _kit  # noqa: E402,F401
import tally as _tally  # noqa: E402  (a conta da sala e a raiz padrão moram lá, em um lugar só)
import common as _common  # noqa: E402  (o prazo e a duração anunciada da rodada também: a espera lê o mesmo)
from skillkit import visual as _visual  # noqa: E402
from skillkit.visual import CHROME, ErroPublicacao, LIMITE_HTML  # noqa: E402,F401  (o PNG e o visual moram no kit)
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
    # X2/A4: o cartão só fala do Codex quando há persona Codex entre os participantes da rodada
    tem_codex = any(str(p.get('runtime') or '').strip().lower() == 'codex' for p in PP)
    codex = f' · Codex {_num(st["tok"] / 1e6, 2)} M tokens' if tem_codex else ''
    tem_claude = any(str(p.get('runtime') or '').strip().lower() == 'claude' for p in PP)
    cartao_usd = f'US$ {_num(st["usd"], 2)}' if tem_claude else '—'
    cartao_txt = f'personas Claude {rotulo_custo}{codex}' if tem_claude else f'sem persona Claude na rodada{codex}'
    cab_custo = 'Custo (total da sessão)' if total and tem_claude else 'Custo'  # A4: o total é o dos Claude
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
            try:
                R['aberta'] = _tally.hms(_tally.parse_when(opened))
            except ValueError:
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


def gera_png(html_path, png, width, altura=2000):
    """Tira o PNG do HTML (`brza shot`, com o Chrome de reserva). Devolve None se deu certo, ou a mensagem de erro."""
    return _visual.gera_png(html_path, png, width, altura)


def _png(html_path, png, width, altura=2000):
    erro = gera_png(html_path, png, width, altura)
    print(f'panel render: {erro}' if erro else f'png: {png}', file=sys.stderr)


_titulo_seguro = _visual.titulo_seguro


def salva_visual(doc, reu_id, meio, chave, titulo, *, publish_dir=None, alvo_padrao=None):
    """Grava `doc` (ver `skillkit.visual.salva_visual`); devolve (caminho, linha). Levanta ErroPublicacao."""
    return _visual.salva_visual(doc, reu_id, meio, chave, titulo, publish_dir=publish_dir, alvo_padrao=alvo_padrao)


def _cmd_render(a):
    try:
        with open(a.estado, encoding='utf-8') as f:
            S = json.load(f)
        doc = render_html(S, a.at, a.dark)
    except (OSError, ValueError, KeyError) as ex:
        print(f'panel render: {ex}', file=sys.stderr)
        return 2
    R, reu = S.get('rodada') or {}, S.get('reuniao') or {}
    try:
        alvo, linha = salva_visual(doc, reu.get('id'), f'r{R.get("n")}', f'{R.get("n")}',
                                   f'Rodada {R.get("n")} — {R.get("titulo") or ""}'.strip(' —'),
                                   publish_dir=a.publish_dir, alvo_padrao=a.out or os.path.splitext(a.estado)[0] + '.html')
    except ErroPublicacao as ex:
        print(f'panel render: {ex}', file=sys.stderr)
        return ex.rc
    print(linha if linha else alvo)
    if a.png:
        _png(alvo, a.png, a.width)
    return 0


def pasta_da_reuniao(reuniao, root):
    pasta = reuniao.get('dir') or '.'
    return pasta if os.path.isabs(pasta) else os.path.join(root, pasta)


def resolve_publish_dir(publish_dir, pasta):
    """(destino, caiu_no_padrao): `--publish-dir`, senão `$ORCA_CHAT_SCRATCH_DIR`, senão a pasta da reunião (True)."""
    d = publish_dir or os.environ.get('ORCA_CHAT_SCRATCH_DIR')
    return (d, False) if d else (pasta, True)


def publica_rodada(reuniao, n, root, *, publish_dir, png=None, width=736, estado_out=None, **kw_collect):
    """collect + grava o `estado-rN.json` + render + PNG opcional, tudo em processo. `kw_collect` vai ao `collect`
    (`opened`, `closed`, `participantes`, `measurements`, `sessions`, `list_json`, `at`, `settle`…).
    Devolve {'estado', 'html', 'linha', 'png', 'png_erro', 'avisos'}. Levanta ErroManifesto, OSError, ValueError ou
    ErroPublicacao; o PNG que falha NÃO levanta: vira `png_erro`."""
    S = collect(reuniao, n, root, **kw_collect)
    pasta = pasta_da_reuniao(reuniao, root)
    est = estado_out or os.path.join(pasta, f'estado-r{n}.json')
    os.makedirs(os.path.dirname(os.path.abspath(est)), exist_ok=True)
    with open(est, 'w', encoding='utf-8') as f:
        json.dump(S, f, ensure_ascii=False, indent=2)
    doc = render_html(S)
    R, reu = S.get('rodada') or {}, S.get('reuniao') or {}
    alvo, linha = salva_visual(doc, reu.get('id'), f'r{n}', f'{n}', f'Rodada {n} — {R.get("titulo") or ""}'.strip(' —'),
                               publish_dir=publish_dir, alvo_padrao=os.path.splitext(est)[0] + '.html')
    erro = gera_png(alvo, png, width) if png else None
    return {'estado': est, 'html': alvo, 'linha': linha, 'png': png if png and not erro else None, 'png_erro': erro,
            'avisos': list(S.get('avisos') or [])}


def _cmd_publish(a):
    try:
        root = _raiz(a)
        with open(_tally.resolve_reuniao(a.reuniao, root), encoding='utf-8') as f:
            reuniao = json.load(f)
        if reuniao.get('personas') and not _tally.worklogs_existentes(reuniao, root):
            print(f'panel publish: nenhum worklog existe sob {root} (padrão {reuniao.get("worklog")}); '
                  f'confira --root e o manifesto', file=sys.stderr)
            return 2
        pasta = pasta_da_reuniao(reuniao, root)
        destino, padrao = resolve_publish_dir(a.publish_dir, pasta)
        if padrao:
            print(f'aviso: sem --publish-dir nem ORCA_CHAT_SCRATCH_DIR: o HTML fica em {destino}, e o chat não o abre',
                  file=sys.stderr)
        png = None if a.no_png else (a.png or os.path.join(pasta, f'painel-r{a.n}.png'))
        r = publica_rodada(reuniao, a.n, root, publish_dir=destino, png=png, width=a.width, opened=a.opened,
                           closed=a.closed, list_json=a.list_json, at=a.at, measurements=a.measurements,
                           sessions=a.sessions, codex_dir=a.codex_dir, participantes=a.participantes, settle=a.settle)
    except (ErroManifesto, OSError, ValueError) as ex:
        print(f'panel publish: {ex}', file=sys.stderr)
        return 2
    except ErroPublicacao as ex:
        print(f'panel publish: {ex}', file=sys.stderr)
        return ex.rc
    for av in r['avisos']:
        print(f'aviso: {av}', file=sys.stderr)
    print(r['linha'])
    if r['png']:
        print(f'png: {r["png"]}')
    elif r['png_erro']:
        print(f'panel publish: {r["png_erro"]}', file=sys.stderr)
    return 0


# ---------------------------------------------------------------- sintese (a reunião inteira)

COR_REVISOR = '#d97706'   # fixa: no tema do Studio `--chart-1` e `--chart-4` saem parecidos, e o revisor tem de se achar
COR_SALA = 'var(--chart-1,#2563eb)'
TONS = {'ok': 'var(--chart-2,#16a34a)', 'ruim': 'var(--destructive,#dc2626)', 'alerta': COR_REVISOR,
        'neutro': 'var(--chart-1,#2563eb)'}
SELOS = ('go', 'wait', 'sh', 'evo', 'out')


def _lista_de(v):
    return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []


def _ler_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def _rodadas_da_pasta(pasta):
    """{N: (estado|None, sintese|None)} dos `estado-rN.json` e `sintese-N.json` da pasta, em ordem de N."""
    ns = set()
    for nome in os.listdir(pasta):
        m = re.fullmatch(r'estado-r(\d+)\.json|sintese-(\d+)\.json', nome)
        if m:
            ns.add(int(m.group(1) or m.group(2)))
    return {n: (_ler_json(os.path.join(pasta, f'estado-r{n}.json')), _ler_json(os.path.join(pasta, f'sintese-{n}.json')))
            for n in sorted(ns)}


def _selo_tipo(hoje, tipo=None):
    if tipo in SELOS:
        return tipo
    h = str(hoje or '').strip().lower()
    if re.search(r'reprov|fora|nunca|descart', h):
        return 'out'
    if re.search(r'evolu', h):
        return 'evo'
    if re.search(r'ap[óo]s|depois|aguarda|espera|bloquead', h):
        return 'wait'
    if re.search(r'sombra|pend|talvez', h):
        return 'sh'
    if re.search(r'^fase\b|^agora|^j[áa]\b|^pronto|^sim\b|^go\b', h):
        return 'go'
    return 'sh'


def dados_sintese(reuniao, rodadas, final):
    """Os números da síntese, de funções puras sobre o que está nos arquivos (sem tocar o disco)."""
    estados = {n: e for n, (e, _) in rodadas.items() if e}
    sinteses = {n: s for n, (_, s) in rodadas.items() if s}
    ult = estados[max(estados)] if estados else {}
    prim = estados[min(estados)] if estados else {}
    reu = {**(ult.get('reuniao') or {}), **{k: v for k, v in reuniao.items() if k in ('tema', 'id', 'data')}}
    personas = ult.get('personas') or prim.get('personas') or []
    nper = len([p for p in personas if p.get('estado') != FORA]) or len(reuniao.get('personas') or [])
    # janela: da primeira abertura ao último fechamento (cai no `gerado` da última rodada sem fechamento)
    aberta = (prim.get('rodada') or {}).get('aberta')
    fim = (ult.get('rodada') or {}).get('fechada') or (ult.get('rodada') or {}).get('gerado')
    # o revisor: o último `sala.revisor` numérico dos sintese-N
    revisor = rev_n = None
    for n in sorted(sinteses):
        sala = sinteses[n].get('sala') if isinstance(sinteses[n].get('sala'), dict) else {}
        v = sala.get('revisor', sinteses[n].get('revisor'))
        if _isnum(v):
            revisor, rev_n = v, n
    # a média da sala por rodada e o revisor por rodada (para o gráfico)
    serie_sala = [(n, e['sala']['media']) for n, e in estados.items()
                  if isinstance(e.get('sala'), dict) and _isnum(e['sala'].get('media'))]
    serie_rev = []
    for n in sorted(sinteses):
        sala = sinteses[n].get('sala') if isinstance(sinteses[n].get('sala'), dict) else {}
        v = sala.get('revisor', sinteses[n].get('revisor'))
        if _isnum(v):
            serie_rev.append((n, v))
    # votos: a última rodada que tem voto
    votos = vot_n = None
    for n, e in estados.items():
        if (e.get('rodada') or {}).get('tem_voto'):
            tot = {'apoio': 0, 'ressalva': 0, 'contra': 0}
            for p in e.get('personas') or []:
                v = p.get('voto')
                if isinstance(v, dict):
                    for k in tot:
                        tot[k] += v.get(k) or 0
            votos, vot_n = tot, n
    # o custo: custos_coordenacao do último sintese-N que tiver (senão do último estado que tiver)
    custo = None
    for n in sorted(sinteses):
        c = sinteses[n].get('custos_coordenacao')
        if isinstance(c, dict) and (c.get('coordenacao_usd') is not None or c.get('revisor_usd') is not None):
            custo = c
    if custo is None:
        for n in sorted(estados):
            c = estados[n].get('custos_coordenacao')
            if isinstance(c, dict) and (c.get('coordenacao_usd') is not None or c.get('revisor_usd') is not None):
                custo = c
    # por persona: R1 -> última, virada, nota dos colegas
    linhas = []
    for p in personas:
        nome = p.get('nome')
        confs = [(n, (next((q for q in (e.get('personas') or []) if q.get('nome') == nome), {}) or {}))
                 for n, e in estados.items()]
        r1 = next((q.get('confianca_r1') for _, q in confs if _isnum(q.get('confianca_r1'))), None)
        if r1 is None:
            r1 = next((q.get('confianca') for _, q in confs if _isnum(q.get('confianca'))), None)
        ultima = next((q.get('confianca') for _, q in reversed(confs) if _isnum(q.get('confianca'))), None)
        virada = next((q.get('virada') for _, q in reversed(confs) if q.get('virada') and q.get('virada') != 'não'), None)
        nota = next((q.get('nota_colegas') for _, q in reversed(confs) if _isnum(q.get('nota_colegas'))), None)
        linhas.append({'nome': nome, 'runtime': p.get('runtime'), 'modelo': p.get('modelo'), 'papel': p.get('papel'),
                       'r1': r1, 'ultima': ultima, 'virada': virada, 'nota': nota})
    ult_s = sinteses[max(sinteses)] if sinteses else {}
    return {'reu': reu, 'nper': nper, 'nrod': len(rodadas), 'aberta': aberta, 'fim': fim, 'revisor': revisor,
            'rev_n': rev_n, 'sala': (ult.get('sala') or {}), 'sala_n': max(estados) if estados else None,
            'serie_sala': serie_sala, 'serie_rev': serie_rev, 'votos': votos, 'vot_n': vot_n, 'custo': custo,
            'linhas': linhas, 'sintese': ult_s.get('sintese') or [], 'decisoes': _lista_de(ult_s.get('decisoes')),
            'revisor_nota': ((sinteses[rev_n].get('sala') or {}).get('revisor_nota') if rev_n and isinstance(
                sinteses[rev_n].get('sala'), dict) else None), 'rotulos': sorted(rodadas),
            'final': final or {}}


def _grafico(d):
    """SVG inline: a média da sala (linha, `--chart-1`) e os pontos do revisor (quadrados na cor fixa)."""
    sala, rev = d['serie_sala'], d['serie_rev']
    rot = d['rotulos']
    if not rot or not (sala or rev):
        return ''
    W, H, L, Rr, T, B = 560, 200, 40, 14, 22, 28
    valores = [v for _, v in sala + rev]
    lo = max(0, int(min(valores) // 10) * 10 - 10)
    hi = min(100, int(-(-max(valores) // 10)) * 10 + 10)
    if hi - lo < 20:
        lo = max(0, hi - 20)
    n0, n1 = rot[0], rot[-1]

    def X(n):
        return L + (W - L - Rr) * (0.5 if n0 == n1 else (n - n0) / (n1 - n0))

    def Y(v):
        return T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    g = ['<g font-size="11" fill="var(--muted-foreground,#6b7280)">']
    passo = 10 if hi - lo <= 40 else 20
    v = lo
    while v <= hi:
        g.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - Rr}" y2="{Y(v):.1f}" stroke="var(--border,#e5e7eb)"/>'
                 f'<text x="{L - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
        v += passo
    for n in rot:
        g.append(f'<text x="{X(n):.1f}" y="{H - 8}" text-anchor="middle">R{n}</text>')
    g.append('</g>')
    if len(sala) > 1:
        pts = ' '.join(f'{X(n):.1f},{Y(v):.1f}' for n, v in sala)
        g.append(f'<polyline fill="none" stroke="{COR_SALA}" stroke-width="2.5" points="{pts}"/>')
    if len(rev) > 1:
        pts = ' '.join(f'{X(n):.1f},{Y(v):.1f}' for n, v in rev)
        g.append(f'<polyline fill="none" stroke="{COR_REVISOR}" stroke-width="2" stroke-dasharray="5 4" points="{pts}"/>')
    for n, v in sala:
        g.append(f'<circle cx="{X(n):.1f}" cy="{Y(v):.1f}" r="4" fill="{COR_SALA}"/>'
                 f'<text x="{X(n):.1f}" y="{Y(v) - 8:.1f}" text-anchor="middle" font-size="11" font-weight="600" '
                 f'fill="var(--foreground,#171717)">{_num(v)}</text>')
    for n, v in rev:
        g.append(f'<rect x="{X(n) - 5:.1f}" y="{Y(v) - 5:.1f}" width="10" height="10" rx="2" fill="{COR_REVISOR}"/>'
                 f'<text x="{X(n):.1f}" y="{Y(v) + 18:.1f}" text-anchor="middle" font-size="11" font-weight="600" '
                 f'fill="var(--foreground,#171717)">{_num(v)}</text>')
    legenda = (f'<span><span class="dot" style="background:{COR_SALA}"></span>média da sala</span>'
               + (f'<span><span class="dot" style="background:{COR_REVISOR};border-radius:2px"></span>revisor independente</span>'
                  if rev else ''))
    return (f'<h2>A confiança ao longo das rodadas</h2><div class="chart"><svg viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Confiança da sala e do revisor por rodada">{"".join(g)}</svg>'
            f'<div class="legend">{legenda}</div></div>')


def render_sintese(reuniao, rodadas, final=None, dark=False):
    d = dados_sintese(reuniao, rodadas, final)
    F = d['final']
    reu = d['reu']
    sala = d['sala']
    janela = f'{_hm(d["aberta"])}–{_hm(d["fim"])}' if d['aberta'] and d['fim'] else ''
    eyebrow = ' · '.join(x for x in ('Reunião multiagente', reu.get('data'), janela) if x)
    titulo = F.get('titulo') or f'Síntese — {reu.get("tema") or reu.get("id") or ""}'
    rt = d['rotulos']
    meta = f'{d["nper"]} personas · {d["nrod"]} rodadas' + (f' (R{rt[0]}–R{rt[-1]})' if len(rt) > 1 else '')
    if janela:
        meta += f' · das {_hm(d["aberta"])} às {_hm(d["fim"])}'
    # cartões
    c = d['custo']
    usd = (c.get('coordenacao_usd') or 0) + (c.get('revisor_usd') or 0) if c else None
    media = sala.get('media')
    ap = sala.get('antigravity') if isinstance(sala.get('antigravity'), dict) else None
    sala_txt = f'rodada R{d["sala_n"]} · mediana {_num(sala.get("mediana"))} · {sala.get("n", "?")}/{sala.get("total", "?")}'
    if ap and _isnum(ap.get('media')):
        sala_txt += f' (Antigravity à parte: {_num(ap["media"])})'
    v = d['votos']
    cartoes = [
        (_num(d['revisor']) if d['revisor'] is not None else '—',
         d['revisor_nota'] or ('revisor independente' if d['revisor'] is not None else 'sem revisor independente')),
        (_num(media) if _isnum(media) else '—', 'média da sala, ' + sala_txt),
        (f'{v["apoio"]} · {v["ressalva"]} · {v["contra"]}' if v else '—',
         f'apoio · ressalva · contra (R{d["vot_n"]})' if v else 'sem voto nas rodadas'),
        (f'US$ {_num(usd, 2)}' if usd is not None else '—',
         'coordenação e revisor' + (f' até {_hm(c.get("ate"))}' if c and c.get('ate') else '') if usd is not None
         else 'custo da coordenação não informado'),
    ]
    cards = ''.join(f'<div class="card"><div class="n">{_e(n)}</div><div class="l">{_e(l)}</div></div>' for n, l in cartoes)
    partes = [f'<div class="eyebrow">{_e(eyebrow)}</div><h1>{_e(titulo)}</h1><div class="meta">{_e(meta)}</div>',
              f'<div class="cards">{cards}</div>']
    if F.get('conclusao'):
        partes.append(f'<div class="lead">{_e(F["conclusao"])}</div>')
    cls = _lista_de(F.get('classificacao'))
    if cls:
        trs = ''.join(
            f'<tr><td class="uso">{_e(r.get("uso"))}' + (f'<span class="front">{_e(r.get("frente"))}</span>' if r.get('frente') else '')
            + f'</td><td><span class="b b-{_selo_tipo(r.get("hoje"), r.get("hoje_tipo"))}">{_e(r.get("hoje"))}</span></td>'
            f'<td>{_e(r.get("fato"))}</td></tr>' for r in cls)
        partes.append('<h2>A classificação</h2><table class="cl"><colgroup><col style="width:43%"><col style="width:20%">'
                      '<col style="width:37%"></colgroup><thead><tr><th>Uso</th><th>Hoje</th><th>O fato que decide</th></tr>'
                      f'</thead><tbody>{trs}</tbody></table>')
    bars = _lista_de(F.get('barras'))
    if bars:
        itens = []
        for r in bars:
            val, mx = r.get('valor'), r.get('maximo')
            pct = max(0, min(100, 100 * val / mx)) if _isnum(val) and _isnum(mx) and mx else 0
            cor = TONS.get(r.get('tom'), TONS['neutro'])
            txt = r.get('texto') if r.get('texto') is not None else _num(val)
            itens.append(f'<div class="hb"><div class="t">{_e(r.get("rotulo"))}'
                         + (f'<small>{_e(r.get("detalhe"))}</small>' if r.get('detalhe') else '')
                         + f'</div><div class="trk"><div class="fill" style="width:{pct:.1f}%;background:{cor}"></div></div>'
                         f'<div class="v">{_e(txt)}</div></div>')
        partes.append(f'<h2>O que se mediu</h2><div class="bars">{"".join(itens)}</div>')
    partes.append(_grafico(d))
    fases = _lista_de(F.get('fases'))
    if fases:
        fs = ''.join(f'<div class="ph"><div class="k">{_e(f.get("rotulo") or f"fase {i}")}</div>'
                     f'<div class="nm">{_e(f.get("nome"))}</div><div class="h">{_e(f.get("estimado"))}</div></div>'
                     for i, f in enumerate(fases))
        partes.append(f'<h2>As fases</h2><div class="phases">{fs}</div>')
    if d['linhas']:
        trs = ''
        for p in d['linhas']:
            sub = ' · '.join(_e(x) for x in (p.get('runtime'), p.get('modelo')) if x)
            delta = ''
            if _isnum(p['r1']) and _isnum(p['ultima']):
                dl = p['ultima'] - p['r1']
                delta = f' <span class="mut">({"+" if dl > 0 else "−" if dl < 0 else "±"}{_num(abs(dl))})</span>'
            trs += (f'<tr><td><b>{_e(p["nome"])}</b>' + (f'<span class="front">{sub}</span>' if sub else '') + '</td>'
                    f'<td>{_num(p["r1"])} → <b>{_num(p["ultima"])}</b>{delta}</td>'
                    f'<td>{_e(p["virada"]) if p["virada"] else "—"}</td><td>{_num(p["nota"])}</td></tr>')
        partes.append('<h2>As personas</h2><table class="pe"><colgroup><col style="width:34%"><col style="width:34%">'
                      '<col style="width:16%"><col style="width:16%"></colgroup><thead><tr><th>Persona</th>'
                      '<th>Confiança R1 → última</th><th>Virada</th><th>Nota dos colegas</th></tr></thead>'
                      f'<tbody>{trs}</tbody></table>')
    if d['sintese']:
        partes.append('<h2>A síntese</h2><ol class="sin">' + ''.join(f'<li>{_e(x)}</li>' for x in d['sintese']) + '</ol>')
    if d['decisoes']:
        dec = ''
        for x in d['decisoes']:
            quem = [str(q) for q in (x.get('quem') or [])]
            lev = (f'<div class="rec">levantada por {_e(", ".join(quem[:-1]) + " e " + quem[-1] if len(quem) > 1 else quem[0])}</div>'
                   if quem else '')
            rec = f'<div class="rec"><b>recomendação:</b> {_e(x.get("recomendacao"))}</div>' if x.get('recomendacao') else ''
            vt = f'<div class="rec">{_e(x["votos"])}</div>' if x.get('votos') else ''
            dec += f'<div class="q"><div class="qt">{_e(x.get("pergunta"))}</div>{lev}{rec}{vt}</div>'
        partes.append(f'<h2>Para Anderson decidir</h2>{dec}')
    prox = _lista_de(F.get('proxima_rodada'))
    if prox:
        qs = ''.join(f'<div class="q"><div class="qt">{_e(x.get("pergunta"))}</div>'
                     + (f'<div class="rec"><b>Recomendado:</b> {_e(x.get("recomendacao"))}</div>' if x.get('recomendacao') else '')
                     + '</div>' for x in prox)
        partes.append(f'<h2>A próxima rodada para você</h2>{qs}')
    if F.get('rodape'):
        partes.append(f'<div class="foot">{_e(F["rodape"])}</div>')
    return (f'<!doctype html><html lang="pt-BR"{" class=dark" if dark else ""}><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Síntese — {_e(reu.get("tema") or reu.get("id"))}</title><style>{CSS_SINTESE}</style></head>'
            f'<body>{"".join(partes)}</body></html>')


def _cmd_sintese(a):
    try:
        root = _raiz(a)
        with open(_tally.resolve_reuniao(a.reuniao, root), encoding='utf-8') as f:
            reuniao = json.load(f)
        pasta = pasta_da_reuniao(reuniao, root)
        rodadas = _rodadas_da_pasta(pasta)
        if not any(e for e, _ in rodadas.values()):
            print(f'panel sintese: nenhum estado-rN.json em {pasta}; rode `panel.py collect` ou `publish` das rodadas',
                  file=sys.stderr)
            return 2
        doc = render_sintese(reuniao, rodadas, _ler_json(os.path.join(pasta, 'sintese-final.json')), a.dark)
    except (OSError, ValueError, KeyError) as ex:
        print(f'panel sintese: {ex}', file=sys.stderr)
        return 2
    destino, padrao = (None, False) if a.out else resolve_publish_dir(a.publish_dir, pasta)
    if padrao:
        print(f'aviso: sem --publish-dir nem ORCA_CHAT_SCRATCH_DIR: o HTML fica em {destino}, e o chat não o abre',
              file=sys.stderr)
    try:
        alvo, linha = salva_visual(doc, reuniao.get('id'), 'sintese', 'sintese',
                                   f'Síntese — {reuniao.get("tema") or reuniao.get("id") or ""}',
                                   publish_dir=destino, alvo_padrao=a.out or os.path.join(pasta, 'sintese.html'))
    except ErroPublicacao as ex:
        print(f'panel sintese: {ex}', file=sys.stderr)
        return ex.rc
    print(linha or f'::orca-visual{{file="{os.path.basename(alvo)}" title="{_titulo_seguro("Síntese — " + str(reuniao.get("tema") or reuniao.get("id") or ""))}"}}')
    if not a.no_png:
        png = a.png or os.path.join(pasta, 'sintese.png')
        erro = gera_png(alvo, png, a.width, 4200)
        if erro:
            print(f'panel sintese: {erro}', file=sys.stderr)
        else:
            print(f'png: {png}')
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
    pu = sub.add_parser('publish', help='collect + render + PNG de uma vez; imprime a linha ::orca-visual e o png:')
    pu.add_argument('n', type=int)
    pu.add_argument('--reuniao', required=True)
    pu.add_argument('--root', help='padrão: o topo do repositório git do cwd')
    pu.add_argument('--opened')
    pu.add_argument('--closed')
    pu.add_argument('--list-json')
    pu.add_argument('--at')
    pu.add_argument('--measurements')
    pu.add_argument('--sessions')
    pu.add_argument('--codex-dir')
    pu.add_argument('--participantes', nargs='+', metavar='NOME')
    pu.add_argument('--settle', type=float, default=0, metavar='SEG')
    pu.add_argument('--publish-dir', help='padrão: $ORCA_CHAT_SCRATCH_DIR; sem ele, a pasta da reunião (com aviso)')
    g2 = pu.add_mutually_exclusive_group()
    g2.add_argument('--png', help='padrão: <pasta da reunião>/painel-rN.png')
    g2.add_argument('--no-png', action='store_true')
    pu.add_argument('--width', type=int, default=736)
    pu.set_defaults(fn=_cmd_publish)
    sy = sub.add_parser('sintese', help='o visual de síntese da reunião inteira')
    sy.add_argument('--reuniao', required=True)
    sy.add_argument('--root', help='padrão: o topo do repositório git do cwd')
    g3 = sy.add_mutually_exclusive_group()
    g3.add_argument('--out')
    g3.add_argument('--publish-dir')
    sy.add_argument('--dark', action='store_true')
    g4 = sy.add_mutually_exclusive_group()
    g4.add_argument('--png', help='padrão: <pasta da reunião>/sintese.png')
    g4.add_argument('--no-png', action='store_true')
    sy.add_argument('--width', type=int, default=736)
    sy.set_defaults(fn=_cmd_sintese)
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

CSS_SINTESE = '''
* { box-sizing: border-box; }
html{--fb-bg:#fff;--fb-fg:#171717;--fb-card:#fafafa;--fb-mut:#6b7280;--fb-mutbg:#f1f1f3;--fb-bd:#e5e5e5;--fb-c1:#2563eb;--fb-c2:#16a34a;--fb-de:#dc2626}
html.dark{--fb-bg:#18181b;--fb-fg:#ededed;--fb-card:#232327;--fb-mut:#a1a1aa;--fb-mutbg:#2e2e33;--fb-bd:#3a3a40;--fb-c1:#60a5fa;--fb-c2:#4ade80;--fb-de:#f87171}
body{margin:0;padding:16px;background:var(--background,var(--fb-bg));color:var(--foreground,var(--fb-fg));font:13px/1.45 var(--font-sans,-apple-system,system-ui,sans-serif)}
.mut{color:var(--muted-foreground,var(--fb-mut))}
.eyebrow{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground,var(--fb-mut))}
h1{font-size:19px;margin:2px 0 4px;line-height:1.25}
h2{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground,var(--fb-mut));margin:22px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--border,var(--fb-bd))}
.meta{color:var(--muted-foreground,var(--fb-mut));font-size:12px}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:14px}
.card{background:var(--card,var(--fb-card));color:var(--card-foreground,var(--fb-fg));border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,10px);padding:10px 12px;min-width:0}
.card .n{font-size:22px;font-weight:650;line-height:1.1;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
.card .l{font-size:11.5px;color:var(--muted-foreground,var(--fb-mut));margin-top:4px;overflow-wrap:anywhere}
.lead{margin:14px 0 0;padding:10px 12px;border-left:3px solid var(--chart-1,var(--fb-c1));background:var(--muted,var(--fb-mutbg));border-radius:0 var(--radius,8px) var(--radius,8px) 0}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th{text-align:left;font-weight:500;font-size:11.5px;color:var(--muted-foreground,var(--fb-mut));padding:4px 6px;border-bottom:1px solid var(--border,var(--fb-bd))}
td{padding:6px;border-bottom:1px solid var(--border,var(--fb-bd));vertical-align:top;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}
td.uso{font-weight:550}
.front{display:block;font-size:11.5px;color:var(--muted-foreground,var(--fb-mut));font-weight:400}
.b{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:999px;max-width:100%;overflow-wrap:anywhere}
.b-go{background:var(--chart-2,var(--fb-c2));color:#fff}
.b-wait{background:var(--chart-1,var(--fb-c1));color:#fff}
.b-sh{background:var(--secondary,var(--fb-mutbg));color:var(--secondary-foreground,var(--fb-fg))}
.b-evo{border:1px dashed var(--border,var(--fb-bd));color:var(--muted-foreground,var(--fb-mut))}
.b-out{border:1px solid var(--destructive,var(--fb-de));color:var(--destructive,var(--fb-de))}
.bars{display:grid;grid-template-columns:minmax(0,1fr);gap:9px}
.hb{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr) 54px;gap:10px;align-items:center}
.hb .t{font-size:12.5px;min-width:0;overflow-wrap:anywhere}
.hb .t small{display:block;color:var(--muted-foreground,var(--fb-mut));font-size:11px}
.trk{height:10px;border-radius:6px;background:var(--muted,var(--fb-mutbg));position:relative;overflow:hidden}
.fill{position:absolute;left:0;top:0;bottom:0;border-radius:6px}
.hb .v{font-variant-numeric:tabular-nums;font-weight:600;text-align:right;min-width:0;overflow-wrap:anywhere}
.phases{display:grid;grid-template-columns:repeat(auto-fit,minmax(88px,1fr));gap:6px}
.ph{border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,8px);padding:8px;min-width:0;background:var(--card,var(--fb-card))}
.ph .k{font-size:11px;color:var(--muted-foreground,var(--fb-mut))}
.ph .nm{font-weight:600;font-size:12px;margin:2px 0;line-height:1.25;overflow-wrap:anywhere}
.ph .h{font-size:11.5px;font-variant-numeric:tabular-nums}
.chart svg{width:100%;max-width:640px;height:auto;display:block}
.legend{display:flex;gap:14px;font-size:11.5px;color:var(--muted-foreground,var(--fb-mut));margin-top:4px;flex-wrap:wrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.q{border:1px solid var(--border,var(--fb-bd));border-radius:var(--radius,8px);padding:9px 11px;margin-bottom:7px;min-width:0}
.q .qt{font-weight:600;overflow-wrap:anywhere}
.q .rec{color:var(--muted-foreground,var(--fb-mut));font-size:12px;margin-top:2px;overflow-wrap:anywhere}
.q .rec b{color:var(--foreground,var(--fb-fg));font-weight:600}
.sin{margin:0;padding-left:18px} .sin li{margin:3px 0}
.foot{margin-top:18px;font-size:11.5px;color:var(--muted-foreground,var(--fb-mut))}
@media (max-width:560px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}
.hb{grid-template-columns:minmax(0,1fr) 46px} .hb .trk{grid-column:1/-1;grid-row:2}}
'''

if __name__ == '__main__':
    sys.exit(main())
