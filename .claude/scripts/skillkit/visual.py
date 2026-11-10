"""O visual HTML de uma skill: gravar o `.html` do `::orca-visual` e tirar o PNG dele.

Só biblioteca padrão. Extraído de `panel.py` da `meeting-runner` (PLN-021/D1). O PNG sai do `brza shot`, que abre o
artboard como o chat do BrzA Studio o mostra e mede a altura sozinho; o Chrome headless fica só de reserva, quando o
`brza` falta ou sai com erro. `_run` e `_chrome` são os pontos que os testes trocam por atribuição.
"""
import hashlib
import os
import re
import subprocess

LIMITE_HTML = 512 * 1024
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
BRZA = os.environ.get('BRZA_BIN', 'brza')
ALTURA_CHROME = 2000


class ErroPublicacao(Exception):
    """Falha ao gravar o visual; `rc` é o código de saída do subcomando."""
    def __init__(self, msg, rc=1):
        super().__init__(msg)
        self.rc = rc


def titulo_seguro(tit):
    tit = re.sub(r'[\x00-\x1f\x7f"{}]+', ' ', str(tit or '')).replace('\\', ' ')
    return ' '.join(tit.split())


def salva_visual(doc, prefixo, meio, chave, titulo, *, publish_dir=None, alvo_padrao=None):
    """Grava `doc`. Com `publish_dir`, o arquivo é `<prefixo>-<meio>-<hash>.html` (nome fixo para a mesma `chave`, para
    republicar no mesmo arquivo) e a linha `::orca-visual` volta; senão grava em `alvo_padrao` e a linha é None.
    Devolve (caminho, linha). Levanta ErroPublicacao."""
    if len(doc.encode('utf-8')) >= LIMITE_HTML:
        raise ErroPublicacao('HTML >= 512 KB, o visual não aceita', 1)
    if publish_dir:
        rid = str(prefixo or 'reuniao')
        if '/' in rid or '\\' in rid or '..' in rid:
            raise ErroPublicacao(f'reuniao.id "{rid}" tem caminho; recuso gravar fora de --publish-dir', 1)
        rid = re.sub(r'[^\w.-]+', '-', rid).strip('.-') or 'reuniao'
        h = hashlib.sha1(f'{prefixo}|{chave}'.encode()).hexdigest()[:4]
        nome = f'{rid}-{meio}-{h}.html'
        os.makedirs(publish_dir, exist_ok=True)
        alvo = os.path.join(publish_dir, nome)
        linha = f'::orca-visual{{file="{nome}" title="{titulo_seguro(titulo)}"}}'
    else:
        alvo, linha = alvo_padrao, None
    with open(alvo, 'w', encoding='utf-8') as f:
        f.write(doc)
    return alvo, linha


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


def _chrome(html_path, png, width, altura, scale):
    """O PNG pelo Chrome headless (a reserva). Devolve None se deu certo, ou a mensagem de erro."""
    if not os.path.exists(CHROME):
        return 'Chrome não encontrado; sem PNG'
    rc, _, err = _run([CHROME, '--headless=new', f'--screenshot={png}', f'--window-size={width},{altura}',
                       f'--force-device-scale-factor={scale:g}', 'file://' + os.path.abspath(html_path)])
    if rc == 127:
        return f'o Chrome falhou: {err}'
    return None if os.path.exists(png) else 'o Chrome não gerou o PNG'


def gera_png(html_path, png, width, altura=None, *, theme='light', scale=1):
    """Tira o PNG do HTML. Devolve None se deu certo, ou a mensagem de erro.

    Roda `brza shot <html> <png> --width W --theme T --scale S --force`; só cai no Chrome headless se o `brza` faltar ou
    sair ≠ 0, e o erro, se o Chrome também falhar, diz as duas falhas. O `brza shot` mede a altura sozinho: `altura` só
    vale para o Chrome (padrão 2000)."""
    rc, out, err = _run(shot_argv(html_path, png, width, theme, scale))
    if rc == 0 and os.path.exists(png):
        return None
    motivo = (f'o brza não gerou o PNG (rc {rc})' if rc == 0
              else f'brza shot falhou (rc {rc}): {(err or out or "").strip()[:200]}')
    erro = _chrome(html_path, png, width, altura or ALTURA_CHROME, scale)
    return None if erro is None else f'{motivo}; {erro}'
