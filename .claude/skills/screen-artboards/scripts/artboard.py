#!/usr/bin/env python3
"""Artboards de tela da skill `screen-artboards`: `new` (fragmento em moldura, com os tokens do pacote), `shot` (um PNG por
largura e por tema, mais um a 736) e `promote` (o PNG para a pasta do plano ou da issue).

Só biblioteca padrão e o `skillkit` (`visual.salva_visual`, `visual.gera_png`). Saída: 0 ok, 1 erro de regra, de arquivo
ou de PNG, 2 uso errado.
"""
import argparse
import glob
import hashlib
import html
import json
import os
import re
import sys
import tempfile
from urllib.parse import urlparse

AQUI = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, AQUI)
import _kit  # noqa: E402,F401
import tokens  # noqa: E402
from skillkit.paths import raiz_padrao  # noqa: E402
from skillkit.visual import ErroPublicacao, gera_png, salva_visual  # noqa: E402

CHAT_LARGURA = 736
MARGEM = 12          # o padding do body: a margem em volta da moldura, para a sombra
GAP = 16
# Largura da tela (W), altura (H), a moldura externa (OUTER = W + o corpo do aparelho) e se é aparelho.
FRAMES = {
    'macos': {'w': 1280, 'h': 800, 'outer': 1280, 'rotulo': 'macOS'},
    'windows': {'w': 1280, 'h': 800, 'outer': 1280, 'rotulo': 'Windows'},
    'iphone': {'w': 393, 'h': 852, 'outer': 393 + 22, 'rotulo': 'iPhone', 'mobile': True},
    'android': {'w': 412, 'h': 915, 'outer': 412 + 20, 'rotulo': 'Android', 'mobile': True},
    'browser': {'w': 1280, 'h': None, 'outer': None, 'rotulo': 'Navegador', 'larguras': [375, 768, 1280]},
}
CDNS = {'cdn.jsdelivr.net', 'unpkg.com', 'cdnjs.cloudflare.com', 'esm.sh', 'fonts.googleapis.com',
        'fonts.gstatic.com'}
# O namespace do SVG inline não é requisição.
HOSTS_SEM_REDE = {'www.w3.org'}
TOKENS_ORCA = tokens.NOMES_ORCA + ['sidebar', 'sidebar-foreground']
ESQUEMA_NOME = {'light': 'claro', 'dark': 'escuro'}


class ErroRegra(Exception):
    pass


def confere_regras(doc):
    """Levanta ErroRegra com a linha do problema se o HTML quebra uma regra do `orca-chat-visuals`."""
    for m in re.finditer(r'https?://([^\s"\'<>)/:]+)', doc):
        host = m.group(1).lower()
        if host in CDNS or host in HOSTS_SEM_REDE:
            continue
        linha = doc.count('\n', 0, m.start()) + 1
        raise ErroRegra(f'linha {linha}: "{m.group(0)}" — o quadro não faz requisição; só os CDNs permitidos '
                        f'({", ".join(sorted(CDNS))}); imagem em SVG inline ou data: URL')
    m = re.search(r'\b100\s*(?:vh|dvh|svh|lvh)\b', doc)
    if m:
        raise ErroRegra(f'linha {doc.count(chr(10), 0, m.start()) + 1}: "{m.group(0)}" — o chat ajusta o quadro ao '
                        f'conteúdo, e 100vh cresce sem fim; use a altura da moldura (height: 100%)')
    nomes = '|'.join(re.escape(n) for n in TOKENS_ORCA)
    for m in re.finditer(r':root\s*\{([^}]*)\}', doc):
        t = re.search(r'(?<![\w-])--(' + nomes + r')\s*:', m.group(1))
        if t:
            raise ErroRegra(f'linha {doc.count(chr(10), 0, m.start()) + 1}: ":root {{ --{t.group(1)} }}" — redefinir '
                            f'token do Orca no :root pinta o chat inteiro; escope no .sa-art e use var(--sa-*)')


def css_pacote(pack, esquema, mobile):
    """O bloco CSS do pacote para um esquema, escopado em `.sa-art[data-pack][data-scheme]` (nunca `:root`)."""
    dec = dict(pack['esquemas'][esquema])
    if mobile:
        for m, par in (pack.get('pares_mobile') or {}).items():
            if m in dec:
                dec[par] = dec[m]
    linhas = [f'color-scheme:{esquema}']
    linhas += [f'--sa-{k}:{v}' for k, v in sorted(dec.items())]
    linhas += [f'--sa-font-{k}:{v}' for k, v in sorted(pack.get('fontes', {}).items())]
    linhas += [f'--sa-{k}:{v}' for k, v in sorted(pack.get('espacos', {}).items())]
    return f'.sa-art[data-pack="{pack["id"]}"][data-scheme="{esquema}"]{{' + ';'.join(linhas) + '}'


def le_moldura(nome):
    with open(os.path.join(AQUI, 'frames', f'{nome}.html'), encoding='utf-8') as f:
        txt = f.read()
    css = '\n'.join(re.findall(r'<style>(.*?)</style>', txt, flags=re.S))
    corpo = re.sub(r'<!--.*?-->|<style>.*?</style>', '', txt, flags=re.S).strip()
    return css, corpo


BASE_CSS = """*{box-sizing:border-box}
html,body{margin:0}
body{padding:%dpx;background:transparent;font-family:system-ui,-apple-system,'Segoe UI',sans-serif}
.sa-board{display:flex;flex-direction:column;gap:%dpx}
.sa-row{display:flex;gap:%dpx;align-items:flex-start}
.sa-cell{min-width:0;flex:1 1 0}
.sa-cap{font:600 11px/1 system-ui,sans-serif;margin:0 2px 8px;color:var(--muted-foreground,#6b6b6b)}
.sa-art{color:var(--sa-foreground);font-family:var(--sa-font-sans);font-size:14px;line-height:1.4}
.sa-fit{width:100%%}
.sa-frame{position:relative}
.sa-screen{overflow:hidden;background:var(--sa-background)}
.sa-screen>*{max-width:100%%}
""" % (MARGEM, GAP, GAP)

FIT_JS = """(function(){function fit(){var a=document.querySelectorAll('.sa-fit');for(var i=0;i<a.length;i++){var f=a[i],
fr=f.firstElementChild,w=parseFloat(fr.getAttribute('data-w'));fr.style.zoom=1;fr.style.zoom=Math.min(1,f.clientWidth/w);}}
fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);})();"""


def monta(slug, frame, fragmento, pack, esquemas, larguras, titulo_janela, url, altura, letra, titulo):
    """O documento do artboard e a meta dele."""
    f = FRAMES[frame]
    mobile = bool(f.get('mobile'))
    css_frame, tpl = le_moldura(frame)
    css = [BASE_CSS, css_frame] + [css_pacote(pack, e, mobile) for e in esquemas]
    celulas = []
    for w in larguras:
        for e in esquemas:
            celulas.append((w, e))
    lado_a_lado = mobile and len(esquemas) > 1
    por_linha = len(esquemas) if lado_a_lado else 1
    legenda = len(celulas) > 1
    linhas = []
    for i in range(0, len(celulas), por_linha):
        cs = []
        for w, e in celulas[i:i + por_linha]:
            outer = f['outer'] or w
            avail = (CHAT_LARGURA - 2 * MARGEM - GAP * (por_linha - 1)) / por_linha
            zoom = round(min(1, avail / outer), 4)
            tela_w = w if frame == 'browser' else f['w']
            h = altura or f['h']
            tela_style = f' style="height:{h}px"' if (frame == 'browser' and altura) else ''
            marcado = (tpl.replace('{{OUTERW}}', str(outer)).replace('{{W}}', str(tela_w))
                       .replace('{{H}}', str(h or ''))
                       .replace('{{TITLE}}', html.escape(titulo_janela)).replace('{{URL}}', html.escape(url))
                       .replace('{{SCREENSTYLE}}', tela_style).replace('{{SCREEN}}', fragmento))
            marcado = re.sub(r'(<div class="sa-frame [^"]*" data-w="\d+" style=")', r'\g<1>zoom:%s;' % zoom,
                             marcado, count=1)
            cap = ''
            if legenda:
                partes = []
                if frame == 'browser':
                    partes.append(f'{w} px')
                if len(esquemas) > 1:
                    partes.append(ESQUEMA_NOME[e])
                cap = f'<div class="sa-cap">{html.escape(" · ".join(partes))}</div>'
            largo = f' style="flex:0 1 {outer}px"' if mobile and not lado_a_lado else ''
            cs.append(f'<div class="sa-cell" data-w="{w}" data-scheme="{e}"{largo}>{cap}'
                      f'<div class="sa-art" data-pack="{pack["id"]}" data-scheme="{e}" data-frame="{frame}">'
                      f'<div class="sa-fit">{marcado}</div></div></div>')
        centro = ' style="justify-content:center"' if mobile and not lado_a_lado else ''
        linhas.append(f'<div class="sa-row"{centro}>' + ''.join(cs) + '</div>')
    meta = {'slug': slug, 'frame': frame, 'pack': pack['id'], 'esquemas': esquemas, 'larguras': larguras,
            'outer': {str(w): (f['outer'] or w) for w in larguras}, 'letra': letra, 'titulo': titulo}
    doc = ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{html.escape(slug)}</title>'
           f'<meta name="sa-art" content="{html.escape(json.dumps(meta, ensure_ascii=False), quote=True)}">'
           '<style>\n' + '\n'.join(css) + '\n</style></head><body>\n<div class="sa-board">\n'
           + '\n'.join(linhas) + f'\n</div>\n<script>{FIT_JS}</script>\n</body></html>\n')
    return doc, meta


def le_meta(doc):
    m = re.search(r'<meta name="sa-art" content="([^"]*)"', doc)
    if not m:
        raise ErroRegra('o arquivo não é um artboard desta skill (falta a meta sa-art)')
    return json.loads(html.unescape(m.group(1)))


def pasta_saida(publish_dir):
    """(pasta, no_chat): o `--publish-dir`, o ORCA_CHAT_SCRATCH_DIR, ou um scratch temporário fora do chat."""
    pd = publish_dir or os.environ.get('ORCA_CHAT_SCRATCH_DIR')
    if pd:
        return pd, True
    return os.path.join(tempfile.gettempdir(), 'screen-artboards'), False


def cmd_new(a):
    slug = re.sub(r'[^\w.-]+', '-', a.slug).strip('.-')
    if not slug:
        print('slug vazio', file=sys.stderr)
        return 2
    try:
        pack = tokens.carrega(a.pack, a.packs_dir)
    except OSError:
        print(f'pacote "{a.pack}" não existe em {a.packs_dir}: tokens.py list, ou tokens.py extract {a.pack} --src …',
              file=sys.stderr)
        return 2
    esquemas = ['light', 'dark'] if a.scheme == 'both' else [a.scheme]
    if a.scheme is None:
        esquemas = ['light', 'dark'] if pack['id'] == 'brza-studio' else ['light']
    larguras = [int(x) for x in a.widths.split(',')] if a.widths else (FRAMES[a.frame].get('larguras')
                                                                         or [FRAMES[a.frame]['w']])
    if a.widths and a.frame != 'browser':
        print('--widths só vale para a moldura browser', file=sys.stderr)
        return 2
    if a.body == '-':
        fragmento = sys.stdin.read()
    else:
        try:
            with open(a.body, encoding='utf-8') as f:
                fragmento = f.read()
        except OSError as e:
            print(f'--body: {e}', file=sys.stderr)
            return 1
    try:
        confere_regras(fragmento)
    except ErroRegra as e:
        print(f'regra do chat quebrada no fragmento, {e}', file=sys.stderr)
        return 1
    titulo = a.title or slug
    doc, meta = monta(slug, a.frame, fragmento, pack, esquemas, larguras, a.window_title, a.url, a.height, a.letter,
                      titulo)
    try:
        confere_regras(doc)
    except ErroRegra as e:
        print(f'regra do chat quebrada, {e}', file=sys.stderr)
        return 1
    pasta, no_chat = pasta_saida(a.publish_dir)
    rotulo = f'{a.letter} — {titulo}' if a.letter else titulo
    chave = hashlib.sha1(doc.encode('utf-8')).hexdigest()
    try:
        alvo, linha = salva_visual(doc, slug, a.frame, chave, rotulo, publish_dir=pasta)
    except ErroPublicacao as e:
        print(str(e), file=sys.stderr)
        return 1
    if pack.get('origem'):
        rc, msg = tokens.confere(pack['id'], a.packs_dir)
        if rc:
            print(msg, file=sys.stderr)
    print(f'arquivo: {alvo}')
    if no_chat:
        print(linha)
    else:
        print('(fora do chat: sem ORCA_CHAT_SCRATCH_DIR; leve o caminho do .html e dos PNGs na mensagem)')
    return 0


def _variante(doc, ocultar_css):
    return doc.replace('</head>', f'<style>{ocultar_css}</style></head>', 1)


def _seleciona(largura, esquema):
    return (f'.sa-cell:not([data-w="{largura}"][data-scheme="{esquema}"]){{display:none}}'
            '.sa-row{display:block}.sa-cap{display:none}')


def tira_variante(doc, meta, largura, esquema, destino, tmp_dir, scale):
    """O PNG de uma largura nominal e um esquema: só essa moldura, na largura dela mais a margem."""
    os.makedirs(tmp_dir, exist_ok=True)
    nome = f'{meta["slug"]}-{largura}-{esquema}'
    htm = os.path.join(tmp_dir, nome + '.html')
    with open(htm, 'w', encoding='utf-8') as f:
        f.write(_variante(doc, _seleciona(largura, esquema)))
    larg_png = meta['outer'][str(largura)] + 2 * MARGEM
    return gera_png(htm, destino, larg_png, theme=esquema, scale=scale)


def cmd_shot(a):
    try:
        with open(a.artboard, encoding='utf-8') as f:
            doc = f.read()
        meta = le_meta(doc)
    except (OSError, ErroRegra) as e:
        print(str(e), file=sys.stderr)
        return 1
    os.makedirs(a.out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.artboard))[0]
    tmp = os.path.join(a.out_dir, '_variantes')
    esquemas = [a.theme] if a.theme and a.theme in meta['esquemas'] else meta['esquemas']
    saidas, erros = [], []
    chat = os.path.join(a.out_dir, f'{base}-{CHAT_LARGURA}.png')
    erro = gera_png(a.artboard, chat, CHAT_LARGURA, theme=a.theme or 'light', scale=a.scale)
    (erros if erro else saidas).append(f'{chat}: {erro}' if erro else chat)
    for w in meta['larguras']:
        for e in esquemas:
            destino = os.path.join(a.out_dir, f'{base}-{w}-{e}.png')
            erro = tira_variante(doc, meta, w, e, destino, tmp, a.scale)
            (erros if erro else saidas).append(f'{destino}: {erro}' if erro else destino)
    for s in saidas:
        print(s)
    for e in erros:
        print(f'erro: {e}', file=sys.stderr)
    return 1 if erros else 0


def cmd_promote(a):
    try:
        with open(a.artboard, encoding='utf-8') as f:
            doc = f.read()
        meta = le_meta(doc)
    except (OSError, ErroRegra) as e:
        print(str(e), file=sys.stderr)
        return 1
    nome = re.sub(r'[^\w-]+', '-', a.name.lower()).strip('-')
    if not nome:
        print('--name vazio', file=sys.stderr)
        return 2
    raiz = a.root or raiz_padrao()
    if a.plan:
        m = re.fullmatch(r'(?:PLN-)?(\d+)', a.plan)
        if not m:
            print(f'--plan "{a.plan}": use PLN-NNN', file=sys.stderr)
            return 2
        num = f'PLN-{int(m.group(1)):03d}'
        pastas = [p for p in glob.glob(os.path.join(raiz, 'plans', f'{num}-*')) if os.path.isdir(p)]
        if len(pastas) != 1:
            print(f'{len(pastas)} pastas plans/{num}-* em {raiz}; esperava 1', file=sys.stderr)
            return 1
        destino = os.path.join(pastas[0], f'{num}-{nome}.png')
    else:
        issue = os.path.join(raiz, a.issue) if not os.path.isabs(a.issue) else a.issue
        if not os.path.isfile(issue):
            print(f'issue não encontrada: {a.issue}', file=sys.stderr)
            return 1
        destino = os.path.join(os.path.dirname(issue), f'{os.path.splitext(os.path.basename(issue))[0]}-{nome}.png')
    largura = a.width or max(meta['larguras'])
    if largura not in meta['larguras']:
        print(f'--width {largura}: o artboard tem {meta["larguras"]}', file=sys.stderr)
        return 2
    esquema = a.scheme or meta['esquemas'][0]
    if esquema not in meta['esquemas']:
        print(f'--scheme {esquema}: o artboard tem {meta["esquemas"]}', file=sys.stderr)
        return 2
    tmp = tempfile.mkdtemp(prefix='sa-promote-')
    erro = tira_variante(doc, meta, largura, esquema, destino, tmp, a.scale)
    if erro:
        print(f'erro: {erro}', file=sys.stderr)
        return 1
    print(f'arquivo: {destino}')
    print(f'![{nome.replace("-", " ")}]({os.path.basename(destino)})')
    return 0


def parser():
    ap = argparse.ArgumentParser(prog='artboard.py', description='Artboards de tela em moldura, com os tokens do projeto')
    sub = ap.add_subparsers(dest='cmd', required=True)
    n = sub.add_parser('new', help='embrulha o fragmento na moldura e grava o artboard')
    n.add_argument('slug')
    n.add_argument('--frame', required=True, choices=sorted(FRAMES))
    n.add_argument('--widths', help='só browser: as larguras, "375,768,1280" por padrão')
    n.add_argument('--pack', default='neutral')
    n.add_argument('--scheme', choices=['light', 'dark', 'both'], default=None,
                   help='o padrão é both no brza-studio e light nos outros pacotes')
    n.add_argument('--letter')
    n.add_argument('--title')
    n.add_argument('--body', required=True, help='o fragmento HTML da tela; "-" lê da entrada padrão')
    n.add_argument('--publish-dir')
    n.add_argument('--window-title', default='BrzA Studio', help='o título da janela (macos, windows) ou da aba')
    n.add_argument('--url', default='app.example.com', help='o endereço na barra do navegador')
    n.add_argument('--height', type=int, help='a altura da tela em px (a da moldura, por padrão)')
    n.add_argument('--packs-dir', default=tokens.PACKS)
    s = sub.add_parser('shot', help='um PNG por largura nominal e por tema, e um a 736')
    s.add_argument('artboard')
    s.add_argument('--out-dir', required=True)
    s.add_argument('--theme', choices=['light', 'dark'], help='só este tema (e o tema do app no PNG de 736)')
    s.add_argument('--scale', type=float, default=1)
    p = sub.add_parser('promote', help='o PNG da escolhida, na pasta do plano ou da issue')
    p.add_argument('artboard')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--plan')
    g.add_argument('--issue')
    p.add_argument('--name', required=True)
    p.add_argument('--width', type=int)
    p.add_argument('--scheme', choices=['light', 'dark'])
    p.add_argument('--root')
    p.add_argument('--scale', type=float, default=2)
    return ap


def main(argv=None):
    a = parser().parse_args(argv)
    return {'new': cmd_new, 'shot': cmd_shot, 'promote': cmd_promote}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
