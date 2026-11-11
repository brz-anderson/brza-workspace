#!/usr/bin/env python3
"""Os pacotes de tokens visuais da skill `screen-artboards`: extrair do código do projeto, conferir a deriva, listar.

Só biblioteca padrão. O pacote é `packs/<projeto>.json`; o do `brza-studio` sai do `main.css` (blocos `:root` e `.dark`)
e do `mobile-theme.ts` por regex, sem Node. Saída: 0 sem deriva, 4 com deriva, 1 com fonte ausente, 2 para uso errado.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
PACKS = os.path.join(HERE, 'packs')

# Os 26 nomes que o chat do Orca expõe (sem o prefixo --sa-); `radius` e `font-*` não são de cor.
ORCA_NAMES = ['background', 'foreground', 'card', 'card-foreground', 'popover', 'popover-foreground', 'primary',
              'primary-foreground', 'secondary', 'secondary-foreground', 'muted', 'muted-foreground', 'accent',
              'accent-foreground', 'destructive', 'destructive-foreground', 'border', 'input', 'ring', 'radius',
              'font-sans', 'font-mono', 'chart-1', 'chart-2', 'chart-3', 'chart-4', 'chart-5']
# Os do `main.css` que não têm par na lista e que o artboard usa (entram com o nome de origem).
EXTRAS_BRZA = ['sidebar', 'sidebar-foreground', 'sidebar-primary', 'sidebar-primary-foreground', 'sidebar-accent',
               'sidebar-accent-foreground', 'sidebar-border', 'sidebar-ring', 'editor-surface', 'floating-surface',
               'worktree-sidebar', 'worktree-sidebar-foreground', 'worktree-sidebar-accent',
               'worktree-sidebar-border', 'brand-amber', 'brand-orange', 'brand-ember', 'brand-graphite',
               'brand-text', 'agent-question', 'agent-working', 'split-divider']
FONT_KEYS = {'font-sans': 'sans', 'font-mono': 'mono'}
# O Tailwind v4 define as cores em oklch; aqui vão os hex equivalentes (o `var(--color-blue-N)` do main.css).
TAILWIND = {'blue-300': '#93c5fd', 'blue-400': '#60a5fa', 'blue-500': '#3b82f6', 'blue-600': '#2563eb',
            'blue-700': '#1d4ed8', 'blue-800': '#1e40af', 'violet-400': '#a78bfa', 'violet-500': '#8b5cf6',
            'yellow-500': '#eab308'}
# O token do mobile que espelha um do desktop: no iPhone e no Android o valor do mobile vale por cima do desktop.
MOBILE_PAIRS = {'m-bg-base': 'background', 'm-bg-panel': 'sidebar', 'm-bg-raised': 'secondary',
                'm-border-subtle': 'border', 'm-editor-surface': 'editor-surface', 'm-text-primary': 'foreground',
                'm-text-secondary': 'muted-foreground', 'm-surface-bright': 'primary'}

BRZA_SOURCES = {
    'desktop': '~/Projects/brza-studio/src/renderer/src/assets/main.css',
    'mobile': '~/Projects/brza-studio/mobile/src/theme/mobile-theme.ts',
}


class SourceError(Exception):
    pass


def _read(path):
    p = os.path.expanduser(path)
    try:
        with open(p, 'rb') as f:
            raw = f.read()
    except OSError as e:
        raise SourceError(f'fonte ausente: {path} ({e.strerror})')
    return raw.decode('utf-8', 'replace'), hashlib.sha256(raw).hexdigest()


def _strip_css_comments(t):
    return re.sub(r'/\*.*?\*/', '', t, flags=re.S)


def css_block(text, selectors):
    """As declarações `--x: v` de todos os blocos de topo cujo seletor (ou um da lista separada por vírgula) é um de
    `selectors`, na ordem do arquivo: o último vence, como na cascata. {} se nenhum casa."""
    t = _strip_css_comments(text)
    wanted = {' '.join(s.split()) for s in selectors}
    out, depth, selector_at, i = {}, 0, 0, 0
    sel, body_at = '', 0
    while i < len(t):
        c = t[i]
        if c == '{':
            if depth == 0:
                sel = t[selector_at:i]
                body_at = i + 1
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                item_list = {' '.join(x.split()) for x in sel.split(',')}
                if item_list & wanted:
                    body_text = t[body_at:i]
                    for k, v in re.findall(r'--([\w-]+)\s*:\s*([^;]+);', body_text):
                        out[k] = ' '.join(v.split())
                selector_at = i + 1
        elif c == ';' and depth == 0:
            selector_at = i + 1
        i += 1
    return out


def _resolve(value, decls, depth=0):
    def sub(m):
        name = m.group(1)
        if name in decls and depth < 6:
            return _resolve(decls[name], decls, depth + 1)
        if name.startswith('color-') and name[6:] in TAILWIND:
            return TAILWIND[name[6:]]
        return m.group(0)
    return re.sub(r'var\(\s*--([\w-]+)\s*\)', sub, value)


def extract_css(text, only_names=None):
    """(esquemas, fontes) do CSS. O escuro herda do `:root` o que não redefine (a cascata)."""
    light_scheme = css_block(text, [':root', ".native-chat-appearance[data-native-chat-scheme='light']"])
    dark_raw = css_block(text, ['.dark', ':root.dark', '[data-theme=dark]', '[data-theme="dark"]',
                                     ':root[data-theme=dark]', ':root[data-theme="dark"]',
                                     ".native-chat-appearance[data-native-chat-scheme='dark']"])
    dark_scheme = {**light_scheme, **dark_raw}
    schemes = {}
    for scheme, decls in (('light', light_scheme), ('dark', dark_scheme)):
        out = {}
        for k, v in decls.items():
            if only_names is not None and k not in only_names:
                continue
            r = _resolve(v, decls)
            if 'var(' in r or k.startswith('orca-security'):
                continue
            out[k] = r
        schemes[scheme] = out
    source_list = {}
    for k, name in FONT_KEYS.items():
        if k in schemes['light']:
            source_list[name] = schemes['light'].pop(k)
            schemes['dark'].pop(k, None)
    return schemes, source_list


def _kebab(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()


def _ts_object(text, header):
    t = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    t = re.sub(r'(?m)^\s*//.*$|\s//\s.*$', '', t)
    m = re.search(header + r'[^=\n]*=\s*\{', t)
    if not m:
        return {}
    start = m.end()
    end = t.index('}', start)
    out = {}
    for k, a, n in re.findall(r"(\w+)\s*:\s*(?:'([^']*)'|(-?[\d.]+)\b)", t[start:end]):
        out[k] = a if a != '' or not n else n
    return out


def extract_mobile(text):
    """(esquemas m-*, espacos) do `mobile-theme.ts`."""
    schemes = {}
    for name, header_re in (('dark', r'const darkColors'), ('light', r'const lightColors')):
        schemes[name] = {'m-' + _kebab(k): v for k, v in _ts_object(text, header_re).items()}
    space_list = {}
    for k, v in _ts_object(text, r'export const spacing').items():
        space_list[f'm-space-{k}'] = f'{v}px'
    for k, v in _ts_object(text, r'export const radii').items():
        space_list[f'm-radius-{k}'] = f'{v}px'
    typography = _ts_object(text, r'export const typography')
    for k, v in typography.items():
        if k.endswith('Size'):
            space_list[f'm-text-{_kebab(k[:-4])}'] = f'{v}px'
    return schemes, space_list


def build_brza(css_path, ts_path):
    """O pacote do brza-studio, lido dos dois arquivos. Levanta SourceError."""
    css, h_css = _read(css_path)
    ts, h_ts = _read(ts_path)
    only_ = set(ORCA_NAMES + EXTRAS_BRZA)
    schemes, source_list = extract_css(css, only_)
    mobile_schemes, space_list = extract_mobile(ts)
    for e in ('light', 'dark'):
        schemes[e].update(mobile_schemes.get(e, {}))
    return {
        'id': 'brza-studio',
        'extracted_at': datetime.date.today().isoformat(),
        'origin': {
            'desktop': {'file': css_path, 'sha256': h_css, 'blocks': [':root', '.dark']},
            'mobile': {'file': ts_path, 'sha256': h_ts,
                       'exports': ['lightColors', 'darkColors', 'spacing', 'radii', 'typography']},
        },
        'mobile_pairs': MOBILE_PAIRS,
        'schemes': schemes, 'fonts': source_list, 'spaces': space_list,
    }


def build_generic(project, css_path):
    css, h = _read(css_path)
    schemes, source_list = extract_css(css)
    return {
        'id': project,
        'extracted_at': datetime.date.today().isoformat(),
        'origin': {'desktop': {'file': css_path, 'sha256': h, 'blocks': [':root', '.dark']}},
        'mobile_pairs': {}, 'schemes': schemes, 'fonts': source_list, 'spaces': {},
    }


def build(project, src=None, mobile_src=None):
    if project == 'brza-studio':
        return build_brza(src or BRZA_SOURCES['desktop'], mobile_src or BRZA_SOURCES['mobile'])
    if not src:
        raise SourceError(f'projeto "{project}" sem pacote: passe --src <arquivo css>')
    return build_generic(project, src)


def load(project, packs=PACKS):
    with open(os.path.join(packs, f'{project}.json'), encoding='utf-8') as f:
        return json.load(f)


def changed_tokens(old, fresh):
    """Os nomes (com `--`) que mudaram, sumiram ou apareceram entre dois pacotes."""
    name_list = set()
    for e in ('light', 'dark'):
        a, b = old['schemes'].get(e, {}), fresh['schemes'].get(e, {})
        name_list |= {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    for block in ('fonts', 'spaces'):
        a, b = old.get(block, {}), fresh.get(block, {})
        pre = 'font-' if block == 'fonts' else ''
        name_list |= {pre + k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    return sorted('--' + n for n in name_list)


def check(project, packs=PACKS, src=None, mobile_src=None):
    """(código, mensagem): 0 sem deriva, 4 com deriva, 1 com fonte ausente (ou pacote ausente)."""
    try:
        pack = load(project, packs)
    except OSError:
        return 1, f'pacote ausente: {os.path.join(packs, project + ".json")}; rode tokens.py extract {project}'
    origin = pack.get('origin') or {}
    if not origin:
        return 0, f'pacote {project} sem origem (neutro): nada a conferir'
    new_src = {'desktop': src, 'mobile': mobile_src}
    changed, read_paths = [], {}
    for key, o in origin.items():
        path = new_src.get(key) or o['file']
        try:
            _, h = _read(path)
        except SourceError as e:
            return 1, str(e)
        read_paths[key] = path
        if h != o['sha256']:
            changed.append(os.path.basename(o['file']))
    if not changed:
        return 0, f'pacote {project} em dia com o código'
    try:
        fresh = build(project, read_paths.get('desktop'), read_paths.get('mobile')) if project == 'brza-studio' \
            else build(project, read_paths.get('desktop'))
    except SourceError as e:
        return 1, str(e)
    toks = changed_tokens(pack, fresh)
    since = pack.get('extracted_at', '?')
    files = ' e '.join(changed)
    if not toks:
        return 0, f'{files} mudou desde {since}, mas nenhum token: pacote {project} segue valendo'
    shows = ', '.join(toks[:12]) + (f' (+{len(toks) - 12})' if len(toks) > 12 else '')
    return 4, (f'⚠ deriva: {files} mudou desde {since} — {len(toks)} tokens: {shows}; '
               f'rode tokens.py extract {project}')


def pack_names(pack):
    ns = set()
    for e in pack['schemes'].values():
        ns |= set(e)
    ns |= {'font-' + k for k in pack.get('fonts', {})}
    ns |= set(pack.get('spaces', {}))
    return sorted('--sa-' + n for n in ns)


def list_packs(packs=PACKS):
    output = []
    for name in sorted(f[:-5] for f in os.listdir(packs) if f.endswith('.json')):
        p = load(name, packs)
        output.append(f'{name} ({p.get("extracted_at", "?")}):')
        output.extend('  ' + n for n in pack_names(p))
    return output


def main(argv=None):
    ap = argparse.ArgumentParser(prog='tokens.py', description='Pacotes de tokens visuais dos artboards')
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('extract', 'check'):
        p = sub.add_parser(name)
        p.add_argument('project')
        p.add_argument('--src', help='o CSS (o main.css do brza-studio, por padrão)')
        p.add_argument('--mobile-src', help='o mobile-theme.ts (só do brza-studio)')
        p.add_argument('--packs-dir', default=PACKS)
    sub.add_parser('list').add_argument('--packs-dir', default=PACKS)
    a = ap.parse_args(argv)
    if a.cmd == 'list':
        print('\n'.join(list_packs(a.packs_dir)))
        return 0
    if a.cmd == 'check':
        rc, msg = check(a.project, a.packs_dir, a.src, a.mobile_src)
        print(msg, file=sys.stderr if rc else sys.stdout)
        return rc
    try:
        pack = build(a.project, a.src, a.mobile_src)
    except SourceError as e:
        print(str(e), file=sys.stderr)
        return 1
    os.makedirs(a.packs_dir, exist_ok=True)
    saved_path = os.path.join(a.packs_dir, f'{a.project}.json')
    with open(saved_path, 'w', encoding='utf-8') as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
        f.write('\n')
    n = sum(len(v) for v in pack['schemes'].values())
    print(f'{saved_path}: {n} tokens em {len(pack["schemes"])} esquemas')
    return 0


if __name__ == '__main__':
    sys.exit(main())
