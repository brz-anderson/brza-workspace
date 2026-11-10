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

AQUI = os.path.dirname(os.path.realpath(__file__))
PACKS = os.path.join(AQUI, 'packs')

# Os 26 nomes que o chat do Orca expõe (sem o prefixo --sa-); `radius` e `font-*` não são de cor.
NOMES_ORCA = ['background', 'foreground', 'card', 'card-foreground', 'popover', 'popover-foreground', 'primary',
              'primary-foreground', 'secondary', 'secondary-foreground', 'muted', 'muted-foreground', 'accent',
              'accent-foreground', 'destructive', 'destructive-foreground', 'border', 'input', 'ring', 'radius',
              'font-sans', 'font-mono', 'chart-1', 'chart-2', 'chart-3', 'chart-4', 'chart-5']
# Os do `main.css` que não têm par na lista e que o artboard usa (entram com o nome de origem).
EXTRAS_BRZA = ['sidebar', 'sidebar-foreground', 'sidebar-primary', 'sidebar-primary-foreground', 'sidebar-accent',
               'sidebar-accent-foreground', 'sidebar-border', 'sidebar-ring', 'editor-surface', 'floating-surface',
               'worktree-sidebar', 'worktree-sidebar-foreground', 'worktree-sidebar-accent',
               'worktree-sidebar-border', 'brand-amber', 'brand-orange', 'brand-ember', 'brand-graphite',
               'brand-text', 'agent-question', 'agent-working', 'split-divider']
FONTES = {'font-sans': 'sans', 'font-mono': 'mono'}
# O Tailwind v4 define as cores em oklch; aqui vão os hex equivalentes (o `var(--color-blue-N)` do main.css).
TAILWIND = {'blue-300': '#93c5fd', 'blue-400': '#60a5fa', 'blue-500': '#3b82f6', 'blue-600': '#2563eb',
            'blue-700': '#1d4ed8', 'blue-800': '#1e40af', 'violet-400': '#a78bfa', 'violet-500': '#8b5cf6',
            'yellow-500': '#eab308'}
# O token do mobile que espelha um do desktop: no iPhone e no Android o valor do mobile vale por cima do desktop.
PARES_MOBILE = {'m-bg-base': 'background', 'm-bg-panel': 'sidebar', 'm-bg-raised': 'secondary',
                'm-border-subtle': 'border', 'm-editor-surface': 'editor-surface', 'm-text-primary': 'foreground',
                'm-text-secondary': 'muted-foreground', 'm-surface-bright': 'primary'}

ORIGENS_BRZA = {
    'desktop': '~/Projects/brza-studio/src/renderer/src/assets/main.css',
    'mobile': '~/Projects/brza-studio/mobile/src/theme/mobile-theme.ts',
}


class ErroFonte(Exception):
    pass


def _le(caminho):
    p = os.path.expanduser(caminho)
    try:
        with open(p, 'rb') as f:
            raw = f.read()
    except OSError as e:
        raise ErroFonte(f'fonte ausente: {caminho} ({e.strerror})')
    return raw.decode('utf-8', 'replace'), hashlib.sha256(raw).hexdigest()


def _sem_comentarios_css(t):
    return re.sub(r'/\*.*?\*/', '', t, flags=re.S)


def bloco_css(texto, seletores):
    """As declarações `--x: v` de todos os blocos de topo cujo seletor (ou um da lista separada por vírgula) é um de
    `seletores`, na ordem do arquivo: o último vence, como na cascata. {} se nenhum casa."""
    t = _sem_comentarios_css(texto)
    alvo = {' '.join(s.split()) for s in seletores}
    out, prof, ini_sel, i = {}, 0, 0, 0
    sel, ini_corpo = '', 0
    while i < len(t):
        c = t[i]
        if c == '{':
            if prof == 0:
                sel = t[ini_sel:i]
                ini_corpo = i + 1
            prof += 1
        elif c == '}':
            prof -= 1
            if prof == 0:
                itens = {' '.join(x.split()) for x in sel.split(',')}
                if itens & alvo:
                    corpo = t[ini_corpo:i]
                    for k, v in re.findall(r'--([\w-]+)\s*:\s*([^;]+);', corpo):
                        out[k] = ' '.join(v.split())
                ini_sel = i + 1
        elif c == ';' and prof == 0:
            ini_sel = i + 1
        i += 1
    return out


def _resolve(valor, decls, fundo=0):
    def sub(m):
        nome = m.group(1)
        if nome in decls and fundo < 6:
            return _resolve(decls[nome], decls, fundo + 1)
        if nome.startswith('color-') and nome[6:] in TAILWIND:
            return TAILWIND[nome[6:]]
        return m.group(0)
    return re.sub(r'var\(\s*--([\w-]+)\s*\)', sub, valor)


def extrai_css(texto, so_nomes=None):
    """(esquemas, fontes) do CSS. O escuro herda do `:root` o que não redefine (a cascata)."""
    claro = bloco_css(texto, [':root', ".native-chat-appearance[data-native-chat-scheme='light']"])
    escuro_bruto = bloco_css(texto, ['.dark', ':root.dark', '[data-theme=dark]', '[data-theme="dark"]',
                                     ':root[data-theme=dark]', ':root[data-theme="dark"]',
                                     ".native-chat-appearance[data-native-chat-scheme='dark']"])
    escuro = {**claro, **escuro_bruto}
    esq = {}
    for esquema, decls in (('light', claro), ('dark', escuro)):
        out = {}
        for k, v in decls.items():
            if so_nomes is not None and k not in so_nomes:
                continue
            r = _resolve(v, decls)
            if 'var(' in r or k.startswith('orca-security'):
                continue
            out[k] = r
        esq[esquema] = out
    fontes = {}
    for k, nome in FONTES.items():
        if k in esq['light']:
            fontes[nome] = esq['light'].pop(k)
            esq['dark'].pop(k, None)
    return esq, fontes


def _kebab(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()


def _objeto_ts(texto, cabecalho):
    t = re.sub(r'/\*.*?\*/', '', texto, flags=re.S)
    t = re.sub(r'(?m)^\s*//.*$|\s//\s.*$', '', t)
    m = re.search(cabecalho + r'[^=\n]*=\s*\{', t)
    if not m:
        return {}
    ini = m.end()
    fim = t.index('}', ini)
    out = {}
    for k, a, n in re.findall(r"(\w+)\s*:\s*(?:'([^']*)'|(-?[\d.]+)\b)", t[ini:fim]):
        out[k] = a if a != '' or not n else n
    return out


def extrai_mobile(texto):
    """(esquemas m-*, espacos) do `mobile-theme.ts`."""
    esq = {}
    for nome, cab in (('dark', r'const darkColors'), ('light', r'const lightColors')):
        esq[nome] = {'m-' + _kebab(k): v for k, v in _objeto_ts(texto, cab).items()}
    espacos = {}
    for k, v in _objeto_ts(texto, r'export const spacing').items():
        espacos[f'm-space-{k}'] = f'{v}px'
    for k, v in _objeto_ts(texto, r'export const radii').items():
        espacos[f'm-radius-{k}'] = f'{v}px'
    tip = _objeto_ts(texto, r'export const typography')
    for k, v in tip.items():
        if k.endswith('Size'):
            espacos[f'm-text-{_kebab(k[:-4])}'] = f'{v}px'
    return esq, espacos


def monta_brza(css_path, ts_path):
    """O pacote do brza-studio, lido dos dois arquivos. Levanta ErroFonte."""
    css, h_css = _le(css_path)
    ts, h_ts = _le(ts_path)
    so = set(NOMES_ORCA + EXTRAS_BRZA)
    esq, fontes = extrai_css(css, so)
    m_esq, espacos = extrai_mobile(ts)
    for e in ('light', 'dark'):
        esq[e].update(m_esq.get(e, {}))
    return {
        'id': 'brza-studio',
        'extraido_em': datetime.date.today().isoformat(),
        'origem': {
            'desktop': {'arquivo': css_path, 'sha256': h_css, 'blocos': [':root', '.dark']},
            'mobile': {'arquivo': ts_path, 'sha256': h_ts,
                       'exports': ['lightColors', 'darkColors', 'spacing', 'radii', 'typography']},
        },
        'pares_mobile': PARES_MOBILE,
        'esquemas': esq, 'fontes': fontes, 'espacos': espacos,
    }


def monta_generico(projeto, css_path):
    css, h = _le(css_path)
    esq, fontes = extrai_css(css)
    return {
        'id': projeto,
        'extraido_em': datetime.date.today().isoformat(),
        'origem': {'desktop': {'arquivo': css_path, 'sha256': h, 'blocos': [':root', '.dark']}},
        'pares_mobile': {}, 'esquemas': esq, 'fontes': fontes, 'espacos': {},
    }


def monta(projeto, src=None, mobile_src=None):
    if projeto == 'brza-studio':
        return monta_brza(src or ORIGENS_BRZA['desktop'], mobile_src or ORIGENS_BRZA['mobile'])
    if not src:
        raise ErroFonte(f'projeto "{projeto}" sem pacote: passe --src <arquivo css>')
    return monta_generico(projeto, src)


def carrega(projeto, packs=PACKS):
    with open(os.path.join(packs, f'{projeto}.json'), encoding='utf-8') as f:
        return json.load(f)


def tokens_mudados(velho, novo):
    """Os nomes (com `--`) que mudaram, sumiram ou apareceram entre dois pacotes."""
    nomes = set()
    for e in ('light', 'dark'):
        a, b = velho['esquemas'].get(e, {}), novo['esquemas'].get(e, {})
        nomes |= {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    for bloco in ('fontes', 'espacos'):
        a, b = velho.get(bloco, {}), novo.get(bloco, {})
        pre = 'font-' if bloco == 'fontes' else ''
        nomes |= {pre + k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    return sorted('--' + n for n in nomes)


def confere(projeto, packs=PACKS, src=None, mobile_src=None):
    """(código, mensagem): 0 sem deriva, 4 com deriva, 1 com fonte ausente (ou pacote ausente)."""
    try:
        pack = carrega(projeto, packs)
    except OSError:
        return 1, f'pacote ausente: {os.path.join(packs, projeto + ".json")}; rode tokens.py extract {projeto}'
    org = pack.get('origem') or {}
    if not org:
        return 0, f'pacote {projeto} sem origem (neutro): nada a conferir'
    novo_src = {'desktop': src, 'mobile': mobile_src}
    mudou, lidas = [], {}
    for chave, o in org.items():
        caminho = novo_src.get(chave) or o['arquivo']
        try:
            _, h = _le(caminho)
        except ErroFonte as e:
            return 1, str(e)
        lidas[chave] = caminho
        if h != o['sha256']:
            mudou.append(os.path.basename(o['arquivo']))
    if not mudou:
        return 0, f'pacote {projeto} em dia com o código'
    try:
        novo = monta(projeto, lidas.get('desktop'), lidas.get('mobile')) if projeto == 'brza-studio' \
            else monta(projeto, lidas.get('desktop'))
    except ErroFonte as e:
        return 1, str(e)
    toks = tokens_mudados(pack, novo)
    desde = pack.get('extraido_em', '?')
    arqs = ' e '.join(mudou)
    if not toks:
        return 0, f'{arqs} mudou desde {desde}, mas nenhum token: pacote {projeto} segue valendo'
    mostra = ', '.join(toks[:12]) + (f' (+{len(toks) - 12})' if len(toks) > 12 else '')
    return 4, (f'⚠ deriva: {arqs} mudou desde {desde} — {len(toks)} tokens: {mostra}; '
               f'rode tokens.py extract {projeto}')


def nomes_do_pacote(pack):
    ns = set()
    for e in pack['esquemas'].values():
        ns |= set(e)
    ns |= {'font-' + k for k in pack.get('fontes', {})}
    ns |= set(pack.get('espacos', {}))
    return sorted('--sa-' + n for n in ns)


def lista(packs=PACKS):
    saida = []
    for nome in sorted(f[:-5] for f in os.listdir(packs) if f.endswith('.json')):
        p = carrega(nome, packs)
        saida.append(f'{nome} ({p.get("extraido_em", "?")}):')
        saida.extend('  ' + n for n in nomes_do_pacote(p))
    return saida


def main(argv=None):
    ap = argparse.ArgumentParser(prog='tokens.py', description='Pacotes de tokens visuais dos artboards')
    sub = ap.add_subparsers(dest='cmd', required=True)
    for nome in ('extract', 'check'):
        p = sub.add_parser(nome)
        p.add_argument('projeto')
        p.add_argument('--src', help='o CSS (o main.css do brza-studio, por padrão)')
        p.add_argument('--mobile-src', help='o mobile-theme.ts (só do brza-studio)')
        p.add_argument('--packs-dir', default=PACKS)
    sub.add_parser('list').add_argument('--packs-dir', default=PACKS)
    a = ap.parse_args(argv)
    if a.cmd == 'list':
        print('\n'.join(lista(a.packs_dir)))
        return 0
    if a.cmd == 'check':
        rc, msg = confere(a.projeto, a.packs_dir, a.src, a.mobile_src)
        print(msg, file=sys.stderr if rc else sys.stdout)
        return rc
    try:
        pack = monta(a.projeto, a.src, a.mobile_src)
    except ErroFonte as e:
        print(str(e), file=sys.stderr)
        return 1
    os.makedirs(a.packs_dir, exist_ok=True)
    alvo = os.path.join(a.packs_dir, f'{a.projeto}.json')
    with open(alvo, 'w', encoding='utf-8') as f:
        json.dump(pack, f, ensure_ascii=False, indent=2)
        f.write('\n')
    n = sum(len(v) for v in pack['esquemas'].values())
    print(f'{alvo}: {n} tokens em {len(pack["esquemas"])} esquemas')
    return 0


if __name__ == '__main__':
    sys.exit(main())
