#!/usr/bin/env python3
"""Artboards de tela da skill `screen-artboards`: `new` (fragmento em moldura, com os tokens do pacote), `shot` (um PNG por
largura e por tema, mais um a 736) e `promote` (o PNG para a pasta do plano ou da issue).

Só biblioteca padrão e o `skillkit` (`visual.save_visual`, `visual.render_png`). Saída: 0 ok, 1 erro de regra, de arquivo
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

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import _kit  # noqa: E402,F401
import tokens  # noqa: E402
from skillkit.paths import default_root  # noqa: E402
from skillkit.visual import PublishError, render_png, save_visual  # noqa: E402

CHAT_WIDTH = 736
MARGIN = 12          # o padding do body: a margem em volta da moldura, para a sombra
GAP = 16
# Largura da tela (W), altura (H), a moldura externa (OUTER = W + o corpo do aparelho) e se é aparelho.
FRAMES = {
    'macos': {'w': 1280, 'h': 800, 'outer': 1280, 'label': 'macOS'},
    'windows': {'w': 1280, 'h': 800, 'outer': 1280, 'label': 'Windows'},
    'iphone': {'w': 393, 'h': 852, 'outer': 393 + 22, 'label': 'iPhone', 'mobile': True},
    'android': {'w': 412, 'h': 915, 'outer': 412 + 20, 'label': 'Android', 'mobile': True},
    'browser': {'w': 1280, 'h': None, 'outer': None, 'label': 'Navegador', 'widths': [375, 768, 1280]},
}
CDNS = {'cdn.jsdelivr.net', 'unpkg.com', 'cdnjs.cloudflare.com', 'esm.sh', 'fonts.googleapis.com',
        'fonts.gstatic.com'}
# O namespace do SVG inline não é requisição.
OFFLINE_HOSTS = {'www.w3.org'}
TOKENS_ORCA = tokens.ORCA_NAMES + ['sidebar', 'sidebar-foreground']
SCHEME_LABEL = {'light': 'claro', 'dark': 'escuro'}
# Os tokens que o chat do BrzA Studio injeta no :root (skill orca-chat-visuals). No desktop do brza-studio o artboard os usa
# vivos: `--sa-X` vira `var(--X)`, e o artboard segue o tema do chat.
LIVE_FLAGS = tokens.ORCA_NAMES
# O que o chat não injeta mas o `main.css` tem, com o vivo mais próximo; o que não está aqui (brand-*, agent-*) vai com o valor
# claro do pacote.
ALIAS_LIVE = {'sidebar': 'muted', 'sidebar-foreground': 'foreground', 'sidebar-primary': 'primary',
              'sidebar-primary-foreground': 'primary-foreground', 'sidebar-accent': 'accent',
              'sidebar-accent-foreground': 'accent-foreground', 'sidebar-border': 'border', 'sidebar-ring': 'ring',
              'editor-surface': 'background', 'floating-surface': 'popover', 'worktree-sidebar': 'muted',
              'worktree-sidebar-foreground': 'foreground', 'worktree-sidebar-accent': 'accent',
              'worktree-sidebar-border': 'border', 'split-divider': 'border'}


class RuleError(Exception):
    pass


def check_rules(doc):
    """Levanta RuleError com a linha do problema se o HTML quebra uma regra do `orca-chat-visuals`."""
    for m in re.finditer(r'https?://([^\s"\'<>)/:]+)', doc):
        host = m.group(1).lower()
        if host in CDNS or host in OFFLINE_HOSTS:
            continue
        line = doc.count('\n', 0, m.start()) + 1
        raise RuleError(f'linha {line}: "{m.group(0)}" — o quadro não faz requisição; só os CDNs permitidos '
                        f'({", ".join(sorted(CDNS))}); imagem em SVG inline ou data: URL')
    m = re.search(r'\b100\s*(?:vh|dvh|svh|lvh)\b', doc)
    if m:
        raise RuleError(f'linha {doc.count(chr(10), 0, m.start()) + 1}: "{m.group(0)}" — o chat ajusta o quadro ao '
                        f'conteúdo, e 100vh cresce sem fim; use a altura da moldura (height: 100%)')
    name_list = '|'.join(re.escape(n) for n in TOKENS_ORCA)
    for m in re.finditer(r':root\s*\{([^}]*)\}', doc):
        t = re.search(r'(?<![\w-])--(' + name_list + r')\s*:', m.group(1))
        if t:
            raise RuleError(f'linha {doc.count(chr(10), 0, m.start()) + 1}: ":root {{ --{t.group(1)} }}" — redefinir '
                            f'token do Orca no :root pinta o chat inteiro; escope no .sa-art e use var(--sa-*)')


def pack_css(pack, scheme, mobile):
    """O bloco CSS do pacote para um esquema, escopado em `.sa-art[data-pack][data-scheme]` (nunca `:root`)."""
    dec = dict(pack['schemes'][scheme])
    if mobile:
        for m, par in (pack.get('mobile_pairs') or {}).items():
            if m in dec:
                dec[par] = dec[m]
    lines = [f'color-scheme:{scheme}']
    lines += [f'--sa-{k}:{v}' for k, v in sorted(dec.items())]
    lines += [f'--sa-font-{k}:{v}' for k, v in sorted(pack.get('fonts', {}).items())]
    lines += [f'--sa-{k}:{v}' for k, v in sorted(pack.get('spaces', {}).items())]
    return f'.sa-art[data-pack="{pack["id"]}"][data-scheme="{scheme}"]{{' + ';'.join(lines) + '}'


def is_live(pack, frame):
    """Desktop (macos, windows) do brza-studio: tokens vivos do chat, sem o pacote escopado."""
    return pack['id'] == 'brza-studio' and frame in ('macos', 'windows')


def live_css(pack):
    """`--sa-*` apontando para os tokens vivos do chat (`var(--<token>)`), escopado em `.sa-art[data-live]`."""
    lines = []
    for k in sorted(LIVE_FLAGS):
        if k in ('font-sans', 'font-mono'):
            continue
        lines.append(f'--sa-{k}:var(--{k})')
    lines += ['--sa-font-sans:var(--font-sans)', '--sa-font-mono:var(--font-mono)']
    for k, v in sorted(ALIAS_LIVE.items()):
        lines.append(f'--sa-{k}:var(--{v})')
    light_scheme = pack['schemes']['light']
    for k in sorted(light_scheme):
        if k.startswith('m-') or k in LIVE_FLAGS or k in ALIAS_LIVE:
            continue
        lines.append(f'--sa-{k}:{light_scheme[k]}')
    lines += [f'--sa-{k}:{v}' for k, v in sorted(pack.get('spaces', {}).items())]
    return f'.sa-art[data-live]{{' + ';'.join(lines) + '}'


def live_fallback(pack, theme):
    """O `:root` que o chat injetaria, com os valores do esquema do pacote: só para o PNG fora do chat."""
    dec = pack['schemes'][theme]
    lines = [f'color-scheme:{theme}']
    for k in sorted(LIVE_FLAGS):
        if k in ('font-sans', 'font-mono'):
            v = pack.get('fonts', {}).get(k[5:])
        else:
            v = dec.get(k)
        if v:
            lines.append(f'--{k}:{v}')
    return ':root{' + ';'.join(lines) + '}'


def read_frame(name):
    with open(os.path.join(HERE, 'frames', f'{name}.html'), encoding='utf-8') as f:
        txt = f.read()
    css = '\n'.join(re.findall(r'<style>(.*?)</style>', txt, flags=re.S))
    body_text = re.sub(r'<!--.*?-->|<style>.*?</style>', '', txt, flags=re.S).strip()
    return css, body_text


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
""" % (MARGIN, GAP, GAP)

FIT_JS = """(function(){function fit(){var a=document.querySelectorAll('.sa-fit');for(var i=0;i<a.length;i++){var f=a[i],
fr=f.firstElementChild,w=parseFloat(fr.getAttribute('data-w'));fr.style.zoom=1;fr.style.zoom=Math.min(1,f.clientWidth/w);}}
fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);})();"""


def build(slug, frame, fragment, pack, schemes, widths, title_window, url, height, letter, title):
    """O documento do artboard e a meta dele."""
    f = FRAMES[frame]
    mobile = bool(f.get('mobile'))
    css_frame, tpl = read_frame(frame)
    live_flag = is_live(pack, frame)
    if live_flag:
        schemes = ['light']   # uma célula só: o tema é o do chat; 'light' é o rótulo interno dela
        css = [BASE_CSS, css_frame, live_css(pack)]
    else:
        css = [BASE_CSS, css_frame] + [pack_css(pack, e, mobile) for e in schemes]
    cells = []
    for w in widths:
        for e in schemes:
            cells.append((w, e))
    side_by_side = mobile and len(schemes) > 1
    by_line = len(schemes) if side_by_side else 1
    show_caption = len(cells) > 1
    lines = []
    for i in range(0, len(cells), by_line):
        cs = []
        for w, e in cells[i:i + by_line]:
            outer = f['outer'] or w
            avail = (CHAT_WIDTH - 2 * MARGIN - GAP * (by_line - 1)) / by_line
            zoom = round(min(1, avail / outer), 4)
            screen_w = w if frame == 'browser' else f['w']
            h = height or f['h']
            screen_style = f' style="height:{h}px"' if (frame == 'browser' and height) else ''
            marked = (tpl.replace('{{OUTERW}}', str(outer)).replace('{{W}}', str(screen_w))
                       .replace('{{H}}', str(h or ''))
                       .replace('{{TITLE}}', html.escape(title_window)).replace('{{URL}}', html.escape(url))
                       .replace('{{SCREENSTYLE}}', screen_style).replace('{{SCREEN}}', fragment))
            marked = re.sub(r'(<div class="sa-frame [^"]*" data-w="\d+" style=")', r'\g<1>zoom:%s;' % zoom,
                             marked, count=1)
            cap = ''
            if show_caption:
                pieces = []
                if frame == 'browser':
                    pieces.append(f'{w} px')
                if len(schemes) > 1:
                    pieces.append(SCHEME_LABEL[e])
                cap = f'<div class="sa-cap">{html.escape(" · ".join(pieces))}</div>'
            wide_style = f' style="flex:0 1 {outer}px"' if mobile and not side_by_side else ''
            scheme_attr = 'data-live' if live_flag else f'data-scheme="{e}"'
            cs.append(f'<div class="sa-cell" data-w="{w}" data-scheme="{e}"{wide_style}>{cap}'
                      f'<div class="sa-art" data-pack="{pack["id"]}" {scheme_attr} data-frame="{frame}">'
                      f'<div class="sa-fit">{marked}</div></div></div>')
        center = ' style="justify-content:center"' if mobile and not side_by_side else ''
        lines.append(f'<div class="sa-row"{center}>' + ''.join(cs) + '</div>')
    meta = {'slug': slug, 'frame': frame, 'pack': pack['id'], 'schemes': schemes, 'widths': widths,
            'outer': {str(w): (f['outer'] or w) for w in widths}, 'letter': letter, 'title': title}
    if live_flag:
        meta['live'] = True
    doc = ('<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{html.escape(slug)}</title>'
           f'<meta name="sa-art" content="{html.escape(json.dumps(meta, ensure_ascii=False), quote=True)}">'
           '<style>\n' + '\n'.join(css) + '\n</style></head><body>\n<div class="sa-board">\n'
           + '\n'.join(lines) + f'\n</div>\n<script>{FIT_JS}</script>\n</body></html>\n')
    return doc, meta


def read_meta(doc):
    m = re.search(r'<meta name="sa-art" content="([^"]*)"', doc)
    if not m:
        raise RuleError('o arquivo não é um artboard desta skill (falta a meta sa-art)')
    meta = json.loads(html.unescape(m.group(1)))
    if 'schemes' not in meta or 'widths' not in meta:
        raise RuleError('regere o artboard')
    return meta


def output_dir(publish_dir):
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
        pack = tokens.load(a.pack, a.packs_dir)
    except OSError:
        print(f'pacote "{a.pack}" não existe em {a.packs_dir}: tokens.py list, ou tokens.py extract {a.pack} --src …',
              file=sys.stderr)
        return 2
    if a.scheme and is_live(pack, a.frame):
        print(f'--scheme {a.scheme} não se aplica ao desktop do brza-studio: o artboard usa os tokens vivos do chat e '
              f'segue o tema dele (no PNG, shot --theme light|dark)', file=sys.stderr)
        return 2
    schemes = ['light', 'dark'] if a.scheme == 'both' else [a.scheme]
    if a.scheme is None:
        schemes = ['light', 'dark'] if pack['id'] == 'brza-studio' else ['light']
    widths = [int(x) for x in a.widths.split(',')] if a.widths else (FRAMES[a.frame].get('widths')
                                                                         or [FRAMES[a.frame]['w']])
    if a.widths and a.frame != 'browser':
        print('--widths só vale para a moldura browser', file=sys.stderr)
        return 2
    if a.body == '-':
        fragment = sys.stdin.read()
    else:
        try:
            with open(a.body, encoding='utf-8') as f:
                fragment = f.read()
        except OSError as e:
            print(f'--body: {e}', file=sys.stderr)
            return 1
    try:
        check_rules(fragment)
    except RuleError as e:
        print(f'regra do chat quebrada no fragmento, {e}', file=sys.stderr)
        return 1
    title = a.title or slug
    doc, meta = build(slug, a.frame, fragment, pack, schemes, widths, a.window_title, a.url, a.height, a.letter,
                      title)
    try:
        check_rules(doc)
    except RuleError as e:
        print(f'regra do chat quebrada, {e}', file=sys.stderr)
        return 1
    folder, no_chat = output_dir(a.publish_dir)
    label_text = f'{a.letter} — {title}' if a.letter else title
    key = hashlib.sha1(doc.encode('utf-8')).hexdigest()
    try:
        saved_path, line = save_visual(doc, slug, a.frame, key, label_text, publish_dir=folder)
    except PublishError as e:
        print(str(e), file=sys.stderr)
        return 1
    if pack.get('origin'):
        rc, msg = tokens.check(pack['id'], a.packs_dir)
        if rc:
            print(msg, file=sys.stderr)
    print(f'arquivo: {saved_path}')
    if no_chat:
        print(line)
    else:
        print('(fora do chat: sem ORCA_CHAT_SCRATCH_DIR; leve o caminho do .html e dos PNGs na mensagem)')
    return 0


def _variant(doc, hide_css):
    return doc.replace('</head>', f'<style>{hide_css}</style></head>', 1)


def _selects(width, scheme):
    return (f'.sa-cell:not([data-w="{width}"][data-scheme="{scheme}"]){{display:none}}'
            '.sa-row{display:block}.sa-cap{display:none}')


def _fallback(meta, theme, packs_dir):
    """Só o desktop do brza-studio: o `:root` do esquema do pacote, só para o Chrome de reserva do PNG. O `brza shot` já
    injeta os tokens do chat, e um `:root` no HTML venceria o tema dele."""
    if not meta.get('live'):
        return ''
    return live_fallback(tokens.load(meta['pack'], packs_dir), theme)


def render_variant(doc, meta, width, scheme, target_path, tmp_dir, scale, packs_dir=tokens.PACKS):
    """O PNG de uma largura nominal e um esquema: só essa moldura, na largura dela mais a margem."""
    os.makedirs(tmp_dir, exist_ok=True)
    name = f'{meta["slug"]}-{width}-{scheme}'
    htm = os.path.join(tmp_dir, name + '.html')
    cell = meta['schemes'][0] if meta.get('live') else scheme
    with open(htm, 'w', encoding='utf-8') as f:
        f.write(_variant(doc, _selects(width, cell)))
    png_width = meta['outer'][str(width)] + 2 * MARGIN
    return render_png(htm, target_path, png_width, theme=scheme, scale=scale, chrome_css=_fallback(meta, scheme, packs_dir))


def cmd_shot(a):
    try:
        with open(a.artboard, encoding='utf-8') as f:
            doc = f.read()
        meta = read_meta(doc)
    except (OSError, RuleError) as e:
        print(str(e), file=sys.stderr)
        return 1
    os.makedirs(a.out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.artboard))[0]
    tmp = os.path.join(a.out_dir, '_variantes')
    if meta.get('live'):
        schemes = [a.theme or 'light']
    else:
        schemes = [a.theme] if a.theme and a.theme in meta['schemes'] else meta['schemes']
    outputs, errors = [], []
    chat = os.path.join(a.out_dir, f'{base}-{CHAT_WIDTH}.png')
    theme = a.theme or 'light'
    if meta.get('live'):
        os.makedirs(tmp, exist_ok=True)
        htm = os.path.join(tmp, f'{base}-{CHAT_WIDTH}.html')
        with open(htm, 'w', encoding='utf-8') as f:
            f.write(_variant(doc, ''))
        error = render_png(htm, chat, CHAT_WIDTH, theme=theme, scale=a.scale, chrome_css=_fallback(meta, theme, a.packs_dir))
    else:
        error = render_png(a.artboard, chat, CHAT_WIDTH, theme=theme, scale=a.scale)
    (errors if error else outputs).append(f'{chat}: {error}' if error else chat)
    for w in meta['widths']:
        for e in schemes:
            target_path = os.path.join(a.out_dir, f'{base}-{w}-{e}.png')
            error = render_variant(doc, meta, w, e, target_path, tmp, a.scale, a.packs_dir)
            (errors if error else outputs).append(f'{target_path}: {error}' if error else target_path)
    for s in outputs:
        print(s)
    for e in errors:
        print(f'erro: {e}', file=sys.stderr)
    return 1 if errors else 0


def cmd_promote(a):
    try:
        with open(a.artboard, encoding='utf-8') as f:
            doc = f.read()
        meta = read_meta(doc)
    except (OSError, RuleError) as e:
        print(str(e), file=sys.stderr)
        return 1
    name = re.sub(r'[^\w-]+', '-', a.name.lower()).strip('-')
    if not name:
        print('--name vazio', file=sys.stderr)
        return 2
    root = a.root or default_root()
    if a.plan:
        m = re.fullmatch(r'(?:PLN-)?(\d+)', a.plan)
        if not m:
            print(f'--plan "{a.plan}": use PLN-NNN', file=sys.stderr)
            return 2
        num = f'PLN-{int(m.group(1)):03d}'
        folders = [p for p in glob.glob(os.path.join(root, 'plans', f'{num}-*')) if os.path.isdir(p)]
        if len(folders) != 1:
            print(f'{len(folders)} pastas plans/{num}-* em {root}; esperava 1', file=sys.stderr)
            return 1
        target_path = os.path.join(folders[0], f'{num}-{name}.png')
    else:
        issue = os.path.join(root, a.issue) if not os.path.isabs(a.issue) else a.issue
        if not os.path.isfile(issue):
            print(f'issue não encontrada: {a.issue}', file=sys.stderr)
            return 1
        target_path = os.path.join(os.path.dirname(issue), f'{os.path.splitext(os.path.basename(issue))[0]}-{name}.png')
    width = a.width or max(meta['widths'])
    if width not in meta['widths']:
        print(f'--width {width}: o artboard tem {meta["widths"]}', file=sys.stderr)
        return 2
    scheme = a.scheme or meta['schemes'][0]
    if scheme not in (['light', 'dark'] if meta.get('live') else meta['schemes']):
        print(f'--scheme {scheme}: o artboard tem {meta["schemes"]}', file=sys.stderr)
        return 2
    tmp = tempfile.mkdtemp(prefix='sa-promote-')
    error = render_variant(doc, meta, width, scheme, target_path, tmp, a.scale, a.packs_dir)
    if error:
        print(f'erro: {error}', file=sys.stderr)
        return 1
    print(f'arquivo: {target_path}')
    print(f'![{name.replace("-", " ")}]({os.path.basename(target_path)})')
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
                   help='o padrão é both no brza-studio e light nos outros pacotes; não se aplica ao desktop do brza-studio '
                        '(tokens vivos do chat)')
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
    s.add_argument('--theme', choices=['light', 'dark'], help='só este tema (e o tema do app no PNG de 736); no desktop do brza-studio, o tema do PNG')
    s.add_argument('--scale', type=float, default=1)
    s.add_argument('--packs-dir', default=tokens.PACKS)
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
    p.add_argument('--packs-dir', default=tokens.PACKS)
    return ap


def main(argv=None):
    a = parser().parse_args(argv)
    return {'new': cmd_new, 'shot': cmd_shot, 'promote': cmd_promote}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
