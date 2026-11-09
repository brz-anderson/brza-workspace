"""Testes do panel.py: `python3 -I -m unittest discover -s scripts/tests -p 'test_panel.py'`."""
import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(AQUI)
sys.path.insert(0, SCRIPTS)
import panel  # noqa: E402

FIXTURE = os.path.join(AQUI, 'fixtures', 'estado-r3.json')
WORKLOGS_MCP = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *(['..'] * 5)))


def estado():
    with open(FIXTURE, encoding='utf-8') as f:
        return json.load(f)


def persona(S, nome):
    return next(p for p in S['personas'] if p['nome'] == nome)


class RenderFechada(unittest.TestCase):
    def setUp(self):
        self.html = panel.render_html(estado())

    def test_cabecalho_e_personas(self):
        self.assertIn('6 de 6', self.html)
        self.assertIn('fechada às 21:30', self.html)
        for n in ('Muralha', 'Régua', 'Atalho', 'Salto', 'Plantão', 'Cartógrafo'):
            self.assertIn(n, self.html)

    def test_media_sem_antigravity(self):
        self.assertIn('<b>57,2</b>', self.html)
        self.assertIn('(5/6)', self.html)
        self.assertIn('Antigravity à parte: 85', self.html)
        self.assertNotIn('61,8', self.html.split('<h2>As medições')[0])  # a média antiga, com o Cartógrafo

    def test_sem_medicao(self):
        self.assertIn('sem medição', self.html)
        self.assertIn('Sem medição: Salto, Cartógrafo', self.html)

    def test_blocos_finais_e_sem_voto(self):
        for t in ('As medições da coordenação', 'A síntese', 'Para Anderson decidir'):
            self.assertIn(t, self.html)
        self.assertIn('Rodada sem voto.', self.html)
        self.assertNotIn('voto A', self.html)

    def test_tema_e_limites(self):
        self.assertLess(len(self.html.encode()), 512 * 1024)
        self.assertNotIn('<script', self.html)
        self.assertNotRegex(self.html, r'https?://')
        self.assertIn('html.dark{', self.html)
        self.assertNotIn(':root', self.html)
        self.assertIn('var(--background,var(--fb-bg))', self.html)


class RenderParcial(unittest.TestCase):
    def setUp(self):
        self.html = panel.render_html(estado(), at='21:29:30')

    def test_regua_falta(self):
        self.assertIn('5 de 6 responderam · falta Régua', self.html)
        self.assertIn('class="st wait">falta', self.html)
        self.assertIn('aguardando a seção da rodada', self.html)
        self.assertIn('Medições, síntese e decisões entram quando a rodada fecha.', self.html)
        for t in ('As medições da coordenação', 'A síntese', 'Para Anderson decidir'):
            self.assertNotIn(t, self.html)
        self.assertNotIn('fechada às', self.html)

    def test_nao_muta_estado(self):
        S = estado()
        panel.render_html(S, at='21:29:30')
        self.assertEqual(S, estado())

    def test_atrasado_depois_do_prazo(self):
        S = estado()
        persona(S, 'Régua').update(estado='falta', respondeu_as=None)
        S['rodada']['fechada'] = None
        self.assertIn('class="st late">atrasado', panel.render_html(S, at='21:41:00'))


class Estados(unittest.TestCase):
    def test_sem_cota_e_erro(self):
        S = estado()
        persona(S, 'Régua')['estado'] = 'sem cota'
        persona(S, 'Atalho')['estado'] = 'erro'
        h = panel.render_html(S)
        self.assertIn('class="st late">sem cota', h)
        self.assertIn('class="st late">erro', h)

    def test_voto(self):
        S = estado()
        S['rodada']['tem_voto'] = True
        persona(S, 'Muralha')['voto'] = {'apoio': 3, 'ressalva': 2, 'contra': 1}
        h = panel.render_html(S)
        self.assertIn('voto: apoio 3 · ressalva 2 · contra 1', h)
        self.assertNotIn('Rodada sem voto.', h)

    def test_sem_prazo_ninguem_atrasa(self):
        S = estado()
        S['rodada']['prazo'] = None
        persona(S, 'Régua').update(estado='falta', respondeu_as=None)
        h = panel.render_html(S, at='23:59:00')
        self.assertNotIn('atrasado', h)
        self.assertNotIn('prazo', h)
        self.assertNotIn('class="tl"', h)

    def test_escapa(self):
        S = estado()
        persona(S, 'Muralha')['posicao'] = '<b>x</b> & "y"'
        h = panel.render_html(S)
        self.assertIn('&lt;b&gt;x&lt;/b&gt; &amp; &quot;y&quot;', h)


class Fuzz(unittest.TestCase):
    def test_remover_cada_chave_opcional(self):
        base = estado()
        # chaves obrigatórias de identidade: nome da persona e o n da rodada
        for k in list(base['rodada']):
            S = copy.deepcopy(base)
            del S['rodada'][k]
            panel.render_html(S)
            panel.render_html(S, at='21:29:30')
        for k in list(base['personas'][0]):
            if k == 'nome':
                continue
            for p0 in range(len(base['personas'])):
                S = copy.deepcopy(base)
                del S['personas'][p0][k]
                panel.render_html(S)
                panel.render_html(S, at='21:29:30')
        for k in ('sala', 'medicoes', 'sintese', 'decisoes', 'custos_coordenacao', 'reuniao'):
            S = copy.deepcopy(base)
            del S[k]
            panel.render_html(S)

    def test_todos_none(self):
        base = estado()
        S = copy.deepcopy(base)
        for k in S['rodada']:
            if k != 'n':
                S['rodada'][k] = None
        for p in S['personas']:
            for k in p:
                if k not in ('nome', 'estado'):
                    p[k] = None
        S['sala'] = {k: None for k in S['sala']}
        S['custos_coordenacao'] = {k: None for k in S['custos_coordenacao']}
        panel.render_html(S)
        panel.render_html(S, at='21:29:30')


class Publicar(unittest.TestCase):
    def test_nome_estavel_e_linha(self):
        with tempfile.TemporaryDirectory() as d:
            saidas = []
            for _ in range(2):
                r = subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'render', FIXTURE,
                                    '--publish-dir', d], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                saidas.append(r.stdout.strip())
            self.assertEqual(saidas[0], saidas[1])
            m = re.fullmatch(r'::orca-visual\{file="(reuniao-mcp-remoto-r3-[0-9a-f]{4})\.html" '
                             r'title="Rodada 3 — a confiança no plano v1"\}', saidas[0])
            self.assertTrue(m, saidas[0])
            self.assertEqual(os.listdir(d), [m.group(1) + '.html'])
            self.assertEqual(len(saidas[0].splitlines()), 1)

    def test_hash_muda_na_rodada_seguinte(self):
        S = estado()
        S['rodada']['n'] = 4
        with tempfile.TemporaryDirectory() as d:
            arq = os.path.join(d, 'e.json')
            with open(arq, 'w') as f:
                json.dump(S, f)
            r = subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'render', arq,
                                '--publish-dir', d], capture_output=True, text=True)
            self.assertIn('-r4-', r.stdout)

    def test_recusa_html_grande(self):
        S = estado()
        S['sintese'] = ['x' * 600000]
        with tempfile.TemporaryDirectory() as d:
            arq = os.path.join(d, 'e.json')
            with open(arq, 'w') as f:
                json.dump(S, f)
            r = subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'render', arq,
                                '--publish-dir', d], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            self.assertEqual([x for x in os.listdir(d) if x.endswith('.html')], [])


def tally_falso(S_base=None):
    mod = types.ModuleType('tally')
    mod.chamadas = []

    def build_estado(reuniao, n, root, **kw):
        mod.chamadas.append((reuniao, n, root, kw))
        S = copy.deepcopy(S_base or estado())
        S['rodada'] = {'n': n, 'titulo': None, 'prazo': None, 'aberta': None, 'fechada': None,
                       'gerado': None, 'tem_voto': False}
        S['medicoes'], S['sintese'], S['decisoes'] = [], [], []
        S['sala'] = {}
        S['custos_coordenacao'] = {}
        return S
    mod.build_estado = build_estado
    return mod


class Collect(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.dir = os.path.join(self.root, 'reu')
        os.makedirs(self.dir)
        with open(os.path.join(self.dir, 'rodada-3.md'), 'w', encoding='utf-8') as f:
            f.write('# Rodada 3 — a confiança no plano v1 (prazo: 21h40)\n\ncorpo\n')
        self.reu = {'id': 'reuniao-x', 'tema': 'Tema X', 'fim': '22h15', 'dir': 'reu',
                    'worklog': 'w/{slug}.md', 'personas': []}

    def tearDown(self):
        self.tmp.cleanup()

    def coletar(self, S_base=None, **kw):
        return panel.collect(self.reu, 3, self.root, tally_mod=tally_falso(S_base), **kw)

    def test_cabecalho_prazo_fechada(self):
        S = self.coletar(opened='21:28:13', at='21:32:40')
        R = S['rodada']
        self.assertEqual((R['titulo'], R['prazo'], R['aberta'], R['gerado']),
                         ('a confiança no plano v1', '21:40', '21:28:13', '21:32:40'))
        self.assertEqual(R['fechada'], '21:30:48')
        self.assertFalse(R['tem_voto'])
        self.assertEqual(S['medicoes'], [])

    def test_aberta_pelo_mtime(self):
        S = self.coletar(at='21:32:40')
        self.assertRegex(S['rodada']['aberta'], r'^\d\d:\d\d:\d\d$')
        os.remove(os.path.join(self.dir, 'rodada-3.md'))
        self.assertIsNone(self.coletar(at='21:32:40')['rodada']['aberta'])

    def test_atrasado_e_refino_por_list(self):
        base = estado()
        for nome, est in (('Régua', 'falta'), ('Atalho', 'falta'), ('Salto', 'falta')):
            persona(base, nome).update(estado=est, respondeu_as=None)
        lista = os.path.join(self.root, 'list.json')
        with open(lista, 'w') as f:
            json.dump([{'name': 'mcp-atalho', 'state': 'error'}, {'name': 'mcp-salto', 'state': 'quota_exceeded'},
                       {'name': 'mcp-regua', 'state': 'working'}], f)
        S = self.coletar(base, at='21:41:00', list_json=lista)
        est = {p['nome']: p['estado'] for p in S['personas']}
        self.assertEqual((est['Régua'], est['Atalho'], est['Salto']), ('atrasado', 'erro', 'sem cota'))
        self.assertIsNone(S['rodada']['fechada'])
        S = self.coletar(base, at='21:35:00', list_json=lista)
        self.assertEqual({p['nome']: p['estado'] for p in S['personas']}['Régua'], 'falta')

    def test_sintese_sobrepoe_posicao(self):
        sj = {'medicoes': [{'tipo': 'medido', 'quem': 'coordenação', 'texto': 't'}],
              'sintese': [str(i) for i in range(8)], 'decisoes': [{'pergunta': 'p', 'quem': ['Muralha'], 'recomendacao': 'r'}],
              'sala': {'revisor': 45, 'revisor_nota': 'fora da sala'},
              'custos_coordenacao': {'coordenacao_usd': 1.0, 'revisor_usd': 0.5, 'ate': '21:32:39'},
              'posicoes': {'Muralha': 'posição da coordenação'}}
        with open(os.path.join(self.dir, 'sintese-3.json'), 'w', encoding='utf-8') as f:
            json.dump(sj, f)
        S = self.coletar(at='21:32:40')
        self.assertEqual(persona(S, 'Muralha')['posicao'], 'posição da coordenação')
        self.assertNotEqual(persona(S, 'Régua')['posicao'], 'posição da coordenação')
        self.assertEqual(len(S['sintese']), 5)
        self.assertEqual((S['sala']['revisor'], S['custos_coordenacao']['ate']), (45, '21:32:39'))
        self.assertEqual(len(S['medicoes']), 1)
        self.assertEqual(len(S['decisoes']), 1)

    def test_repasse_ao_tally(self):
        tm = tally_falso()
        panel.collect(self.reu, 3, self.root, tally_mod=tm, opened='21:28:13', closed='21:30:48',
                      measurements='m.jsonl')
        _, n, root, kw = tm.chamadas[0]
        self.assertEqual((n, root), (3, self.root))
        self.assertEqual((kw['opened'], kw['closed'], kw['measurements']), ('21:28:13', '21:30:48', 'm.jsonl'))
        self.assertNotIn('sessions', kw)

    def test_cli_exit_2_sem_id(self):
        for faltando in ('id', 'tema', 'fim'):
            reu = {k: v for k, v in self.reu.items() if k != faltando}
            arq = os.path.join(self.root, 'reuniao.json')
            with open(arq, 'w') as f:
                json.dump(reu, f)
            r = subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'collect', '3',
                                '--reuniao', arq, '--root', self.root], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, r.stderr)
            self.assertIn(faltando, r.stderr)

    def test_main_collect_grava_estado(self):
        arq = os.path.join(self.root, 'reuniao.json')
        with open(arq, 'w') as f:
            json.dump(self.reu, f)
        sys.modules['tally'] = tally_falso()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = panel.main(['collect', '3', '--reuniao', arq, '--root', self.root, '--at', '21:32:40',
                                 '--list-json', os.path.join(self.root, 'nao-existe.json')])
        finally:
            del sys.modules['tally']
        self.assertEqual(rc, 0)
        with open(os.path.join(self.dir, 'estado-r3.json'), encoding='utf-8') as f:
            self.assertEqual(json.load(f)['rodada']['prazo'], '21:40')


class IntegracaoTally(unittest.TestCase):
    def test_worklogs_reais_da_mcp(self):
        """Os worklogs reais de 2026-11-07, sem medição (arquivos inexistentes) e sem `skipTest` que esconda quebra."""
        if not os.path.exists(os.path.join(WORKLOGS_MCP, 'work/worklogs/2026-11-07-reuniao-mcp-remoto-muralha.md')):
            self.skipTest('os worklogs de 2026-11-07 não existem neste checkout')
        with open(os.path.join(AQUI, 'fixtures', 'reuniao-mcp-remoto.json'), encoding='utf-8') as f:
            reu = json.load(f)
        nada = os.path.join(AQUI, 'fixtures', 'inexistente')
        S = panel.collect(reu, 3, WORKLOGS_MCP, at='21:32:40', list_json=os.devnull, measurements=nada,
                          sessions=nada, codex_dir=nada)
        conf = sorted(p['confianca'] for p in S['personas'] if p.get('confianca') is not None)
        self.assertEqual(conf, [50, 55, 55, 58, 68, 85])


class Correcoes(unittest.TestCase):
    def test_titulo_do_molde_com_duracao_vira_prazo_pela_abertura(self):
        """C9: `(duração: ~5 min)` do molde de rodada: prazo = aberta + duração, e o título não leva o parêntese."""
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'rodada-3.md'), 'w', encoding='utf-8') as f:
                f.write('# Rodada 3 — a confiança no plano (duração: ~5 min)\n\ncorpo\n')
            self.assertEqual(panel._cabecalho_rodada(os.path.join(d, 'rodada-3.md')),
                             ('a confiança no plano', None, 5))
            reu = {'id': 'r', 'tema': 't', 'fim': '22h', 'dir': '.', 'worklog': 'w/{slug}.md', 'personas': []}
            S = panel.collect(reu, 3, d, tally_mod=tally_falso(), opened='21:28:13', at='21:32:40')
            self.assertEqual((S['rodada']['titulo'], S['rodada']['prazo']), ('a confiança no plano', '21:33'))
            S = panel.collect(reu, 3, d, tally_mod=tally_falso(), opened='21:28:13', at='21:40:00')
            self.assertEqual(S['rodada']['prazo'], '21:33')

    def test_atrasado_com_prazo_pela_duracao(self):
        S = estado()
        S['rodada'].update(aberta='21:28:13', prazo='21:33', fechada=None)
        persona(S, 'Régua').update(estado='falta', respondeu_as=None)
        self.assertIn('class="st late">atrasado', panel.render_html(S, at='21:34:00'))

    def test_media_da_sala_igual_a_do_tally(self):
        """C7: o painel usa a conta do tally, só de quem respondeu (52,5 com 2/6, e não 57 com 3/6)."""
        S = estado()
        for p in S['personas']:
            p.update(estado='falta', respondeu_as=None, confianca=None)
        for nome, c in (('Muralha', 40), ('Régua', 65)):
            persona(S, nome).update(estado='respondeu', confianca=c, respondeu_as='21:29:00')
        persona(S, 'Atalho').update(estado='falta', confianca=66)
        S['rodada']['fechada'] = None
        h = panel.render_html(S)
        self.assertIn('<b>52,5</b>', h)
        self.assertIn('(2/6)', h)
        import tally
        self.assertEqual(tally.calc_sala(S['personas'])['media'], 52.5)

    def test_rotulo_do_custo_sem_janela(self):
        S = estado()
        S['rodada']['custo_rotulo'] = 'total da sessão'
        self.assertIn('no total da sessão', panel.render_html(S))
        self.assertIn('personas Claude na rodada', panel.render_html(estado()))

    def test_virada_da_meia_noite(self):
        """M1: aberta 23:58, prazo 00:10."""
        S = estado()
        S['rodada'].update(aberta='23:58:00', prazo='00:10', fechada=None)
        persona(S, 'Régua').update(estado='falta', respondeu_as=None, trabalhando_s=None)
        r = panel.recortar(S, '23:59:00')
        self.assertEqual(persona(r, 'Régua')['estado'], 'falta')
        r = panel.recortar(S, '00:03:00')
        self.assertEqual((persona(r, 'Régua')['estado'], persona(r, 'Régua')['trabalhando_s']), ('falta', 300))
        self.assertEqual(persona(panel.recortar(S, '00:11:00'), 'Régua')['estado'], 'atrasado')
        self.assertIn('class="tl"', panel.render_html(S, at='00:03:00'))

    def test_collect_passa_a_meia_noite(self):
        """M1: a `fechada` é a última resposta DEPOIS da abertura (00:01 vem depois de 23:59), não a maior hora do dia."""
        base = estado()
        for p, h in zip(base['personas'], ('23:59:10', '00:01:00', '23:58:30', '23:59:50', '23:59:00', '23:58:50')):
            p['respondeu_as'] = h
        with tempfile.TemporaryDirectory() as d:
            reu = {'id': 'r', 'tema': 't', 'fim': '22h', 'dir': '.', 'worklog': 'w/{slug}.md', 'personas': []}
            S = panel.collect(reu, 3, d, tally_mod=tally_falso(base), opened='23:58:00', at='00:11:00')
            self.assertEqual(S['rodada']['fechada'], '00:01:00')

    def test_diferenca_do_revisor_com_sala_aninhada(self):
        """C6: o molde põe `sala.revisor` no `sintese-N.json`; o painel calcula `diferenca_revisor`."""
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'sintese-3.json'), 'w', encoding='utf-8') as f:
                json.dump({'sala': {'revisor': 45, 'revisor_nota': 'independente'}}, f)
            reu = {'id': 'r', 'tema': 't', 'fim': '22h', 'dir': '.', 'worklog': 'w/{slug}.md', 'personas': []}
            tm = tally_falso()
            orig = tm.build_estado

            def com_media(*a, **k):
                S = orig(*a, **k)
                S['sala'] = {'media': 57.2}
                return S
            tm.build_estado = com_media
            S = panel.collect(reu, 3, d, tally_mod=tm, at='21:32:40')
            self.assertEqual((S['sala']['revisor'], S['sala']['diferenca_revisor']), (45, 12.2))

    def test_publish_dir_recusa_id_com_caminho_e_sanea_o_titulo(self):
        S = estado()
        with tempfile.TemporaryDirectory() as d:
            pub = os.path.join(d, 'a', 'b')
            S['reuniao']['id'] = '../../escapou'
            arq = os.path.join(d, 'e.json')
            with open(arq, 'w') as f:
                json.dump(S, f)
            cmd = [sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'render', arq, '--publish-dir', pub]
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertEqual([x for x in os.listdir(d) if x.endswith('.html')], [])
            self.assertFalse(os.path.exists(os.path.join(d, 'a', 'escapou-r3-6754.html')))
            S['reuniao']['id'] = 'reuniao x'
            S['rodada']['titulo'] = 'título com } e "aspas"\nquebra {'
            with open(arq, 'w') as f:
                json.dump(S, f)
            r = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            linha = r.stdout.strip()
            self.assertEqual(len(linha.splitlines()), 1)
            m = re.fullmatch(r'::orca-visual\{file="(reuniao-x-r3-[0-9a-f]{4}\.html)" title="([^"{}\n]*)"\}', linha)
            self.assertTrue(m, linha)
            self.assertEqual(os.listdir(pub), [m.group(1)])

    def test_raiz_padrao_do_collect_e_erro_sem_worklog(self):
        """C8: `collect` da pasta da reunião e da raiz acham o mesmo; sem worklog nenhum, rc 2 e mensagem."""
        tmp = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        subprocess.run(['git', 'init', '-q', tmp], check=True)
        os.makedirs(os.path.join(tmp, '.sessions/x'))
        reu = {'id': 'reuniao-x', 'tema': 'T', 'fim': '22h', 'dir': '.sessions/x', 'worklog': 'work/{slug}.md',
               'personas': [{'nome': 'A', 'slug': 'a', 'sessao': 's-a', 'runtime': 'grok'}]}
        with open(os.path.join(tmp, '.sessions/x/reuniao.json'), 'w') as f:
            json.dump(reu, f)
        nada = os.path.join(tmp, 'nada')

        def roda(cwd, reuniao):
            return subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'collect', '3', '--reuniao',
                                   reuniao, '--list-json', os.devnull, '--measurements', nada, '--sessions', nada,
                                   '--codex-dir', nada], cwd=os.path.join(tmp, cwd), capture_output=True, text=True)
        for cwd, reuniao in (('.', '.sessions/x/reuniao.json'), ('.sessions/x', 'reuniao.json')):
            r = roda(cwd, reuniao)
            self.assertEqual(r.returncode, 2, r.stderr)
            self.assertIn('nenhum worklog existe', r.stderr)
        os.makedirs(os.path.join(tmp, 'work'))
        with open(os.path.join(tmp, 'work/a.md'), 'w') as f:
            f.write('### Rodada 3: x\n\ntexto\n\n<!-- fim-rodada-3 -->\n')
        for cwd, reuniao in (('.', '.sessions/x/reuniao.json'), ('.sessions/x', 'reuniao.json')):
            r = roda(cwd, reuniao)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(os.path.realpath(r.stdout.strip()), os.path.join(tmp, '.sessions/x/estado-r3.json'))


@unittest.skipUnless(os.path.exists(panel.CHROME), 'sem Chrome')
class Png(unittest.TestCase):
    def test_png(self):
        with tempfile.TemporaryDirectory() as d:
            png = os.path.join(d, 'p.png')
            r = subprocess.run([sys.executable, '-I', os.path.join(SCRIPTS, 'panel.py'), 'render', FIXTURE,
                                '--out', os.path.join(d, 'p.html'), '--png', png], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(png))


if __name__ == '__main__':
    unittest.main()
