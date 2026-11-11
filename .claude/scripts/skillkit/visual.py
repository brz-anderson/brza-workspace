"""O visual HTML de uma skill: gravar o `.html` do `::orca-visual` e tirar o PNG dele.

Só biblioteca padrão. Extraído de `panel.py` da `meeting-runner` (PLN-021/D1). O PNG sai do `brza shot`, que abre o
artboard como o chat do BrzA Studio o mostra e mede a altura sozinho; o Chrome headless fica só de reserva, quando o
`brza` falta ou sai com erro. `_run` e `_chrome` são os pontos que os testes trocam por atribuição.
"""
import hashlib
import os
import re
import subprocess

LIMIT_HTML = 512 * 1024
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
BRZA = os.environ.get('BRZA_BIN', 'brza')
CHROME_HEIGHT = 2000


class PublishError(Exception):
    """Falha ao gravar o visual; `rc` é o código de saída do subcomando."""
    def __init__(self, msg, rc=1):
        super().__init__(msg)
        self.rc = rc


def safe_title(raw_title):
    raw_title = re.sub(r'[\x00-\x1f\x7f"{}]+', ' ', str(raw_title or '')).replace('\\', ' ')
    return ' '.join(raw_title.split())


def save_visual(doc, prefix, part, key, title, *, publish_dir=None, default_path=None):
    """Grava `doc`. Com `publish_dir`, o arquivo é `<prefix>-<part>-<hash>.html` (nome fixo para a mesma `key`, para
    republicar no mesmo arquivo) e a linha `::orca-visual` volta; senão grava em `default_path` e a linha é None.
    Devolve (caminho, linha). Levanta PublishError."""
    if len(doc.encode('utf-8')) >= LIMIT_HTML:
        raise PublishError('HTML >= 512 KB, o visual não aceita', 1)
    if publish_dir:
        rid = str(prefix or 'reuniao')
        if '/' in rid or '\\' in rid or '..' in rid:
            raise PublishError(f'reuniao.id "{rid}" tem caminho; recuso gravar fora de --publish-dir', 1)
        rid = re.sub(r'[^\w.-]+', '-', rid).strip('.-') or 'reuniao'
        h = hashlib.sha1(f'{prefix}|{key}'.encode()).hexdigest()[:4]
        name = f'{rid}-{part}-{h}.html'
        os.makedirs(publish_dir, exist_ok=True)
        saved_path = os.path.join(publish_dir, name)
        line = f'::orca-visual{{file="{name}" title="{safe_title(title)}"}}'
    else:
        saved_path, line = default_path, None
    with open(saved_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    return saved_path, line


def _run(argv, timeout=60):
    """(rc, stdout, stderr), sem shell; binário ausente vira rc 127."""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return 127, '', str(e)
    return r.returncode, r.stdout, r.stderr


def shot_argv(html_path, png, width, theme='light', scale=1):
    return [BRZA, 'shot', os.path.abspath(html_path), png, '--width', str(width), '--theme', theme,
            '--scale', f'{scale:g}', '--force']


def _chrome(html_path, png, width, height, scale):
    """O PNG pelo Chrome headless (a reserva). Devolve None se deu certo, ou a mensagem de erro."""
    if not os.path.exists(CHROME):
        return 'Chrome não encontrado; sem PNG'
    rc, _, err = _run([CHROME, '--headless=new', f'--screenshot={png}', f'--window-size={width},{height}',
                       f'--force-device-scale-factor={scale:g}', 'file://' + os.path.abspath(html_path)])
    if rc == 127:
        return f'o Chrome falhou: {err}'
    return None if os.path.exists(png) else 'o Chrome não gerou o PNG'


def render_png(html_path, png, width, height=None, *, theme='light', scale=1, chrome_css=''):
    """Tira o PNG do HTML. Devolve None se deu certo, ou a mensagem de erro.

    Roda `brza shot <html> <png> --width W --theme T --scale S --force`; só cai no Chrome headless se o `brza` faltar ou
    sair ≠ 0, e o erro, se o Chrome também falhar, diz as duas falhas. O `brza shot` mede a altura sozinho: `height` só
    vale para o Chrome (padrão 2000). `chrome_css` (por exemplo o `:root` dos tokens) vai só ao Chrome, num HTML temporário
    ao lado do original: o `brza shot` já injeta os tokens do chat, e um `:root` no HTML venceria o tema dele."""
    rc, out, err = _run(shot_argv(html_path, png, width, theme, scale))
    if rc == 0 and os.path.exists(png):
        return None
    reason = (f'o brza não gerou o PNG (rc {rc})' if rc == 0
              else f'brza shot falhou (rc {rc}): {(err or out or "").strip()[:200]}')
    tmp = None
    if chrome_css:
        tmp = os.path.splitext(html_path)[0] + '.chrome.html'
        with open(html_path, encoding='utf-8') as f:
            doc = f.read()
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(doc.replace('</head>', f'<style>{chrome_css}</style></head>', 1) if '</head>' in doc
                    else f'<style>{chrome_css}</style>{doc}')
    try:
        error = _chrome(tmp or html_path, png, width, height or CHROME_HEIGHT, scale)
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
    return None if error is None else f'{reason}; {error}'
