"""O painel que sai do mecanismo: `wait_round` publica sozinho, `panel.py publish` e `panel.py sintese`, e o anexo
`## Custo da tarefa` do `brza note commit` que o `tally` e a espera toleram."""
import contextlib
import io
import json
import os
import re
import shutil
import tempfile
import unittest

import _paths  # noqa: F401
from _paths import fixture

import common
import panel
import tally
import wait_round
from test_wait_round import Base, BASE, PS, done, mapa

LINHA = re.compile(r'^::orca-visual\{file="[^"]+\.html" title="[^"]*"\}$')


class Painel(Base):
    """`run` com o `painel_fn` injetado: onde, e em que ordem, as linhas saem."""

    def roda(self, respostas, painel_fn, **kw):
        t = {"v": BASE}
        respostas = list(respostas)
        saidas = []

        def wait_fn(sessoes, timeout_s):
            r = respostas.pop(0) if respostas else (75, {"done": [], "pending": [], "events": []})
            t["v"] += 5.0 if r[1].get("done") else timeout_s
            return r
        rc = wait_round.run(PS, 2, self.tmp, source="sessions", wait_fn=wait_fn, clock=lambda: t["v"],
                            sleep=lambda s: None, out=saidas.append, entradas=mapa(), painel_fn=painel_fn, **kw)
        return rc, saidas

    def marcador(self, slug, n=2):
        self.escreve(slug, n)

    def fake(self):
        chamadas = []

        def fn(fase, opened, closed):
            chamadas.append((fase, opened, closed))
            return [f'::orca-visual{{file="p-{len(chamadas)}.html" title="R2"}}'] + (
                ["png: /x/painel-r2.png"] if fase in ("abertura", "fim") else [])
        return fn, chamadas

    def test_abertura_chegadas_e_fim_com_a_linha_logo_depois_da_narracao(self):
        for s in ("prumo", "trava", "relance"):
            self.marcador(s)
        fn, ch = self.fake()
        rc, s = self.roda([(0, {"done": [done("ci-prumo")], "events": []}),
                           (0, {"done": [done("ci-trava")], "events": []}),
                           (0, {"done": [done("ci-relance")], "events": []})], fn)
        self.assertEqual(rc, 0)
        self.assertEqual([c[0] for c in ch], ["abertura", "chegada", "chegada", "fim"])
        self.assertTrue(s[0].startswith("R2 · 0/3"))
        self.assertTrue(LINHA.match(s[1]) and s[2] == "png: /x/painel-r2.png")
        self.assertTrue(s[3].startswith("R2 · 1/3"))
        self.assertTrue(LINHA.match(s[4]))
        self.assertNotIn("png:", s[5])              # chegada: sem PNG
        self.assertTrue(s[-4].startswith("R2 · 3/3"))
        self.assertTrue(LINHA.match(s[-3]) and s[-2] == "png: /x/painel-r2.png")
        self.assertTrue(s[-1].startswith("janela: --opened "))
        self.assertEqual(sum(1 for l in s if l.startswith("::orca-visual")), 4)
        self.assertEqual(ch[0][1], wait_round.iso_local(BASE))         # --opened: o `at` do last_send, do mapa, em ISO
        self.assertEqual(ch[3][2], wait_round.iso_local(BASE + 15))    # --closed no fim: a última chegada
        self.assertRegex(ch[0][1], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d$")
        self.assertEqual(s[-1], f"janela: --opened {wait_round.iso_local(BASE)} --closed {wait_round.iso_local(BASE + 15)}")

    def test_o_limite_tambem_publica_o_fim(self):
        fn, ch = self.fake()
        rc, s = self.roda([], fn, timeout=100)
        self.assertEqual(rc, 2)
        self.assertEqual(ch[-1][0], "fim")
        self.assertTrue(LINHA.match(s[-3]) and s[-2].startswith("png: ") and s[-1].startswith("janela: "))

    def test_o_closed_do_fim_e_a_ultima_chegada_e_nao_o_agora_do_limite(self):
        self.marcador("prumo")
        fn, ch = self.fake()
        rc, s = self.roda([(0, {"done": [done("ci-prumo")], "events": []})], fn, timeout=400)
        self.assertEqual(rc, 2)
        fim = [c for c in ch if c[0] == "fim"][0]
        self.assertEqual(fim[2], wait_round.iso_local(BASE + 5))      # a chegada do Prumo, não os ~400 s do limite
        self.assertNotEqual(fim[2], ch[-1][1])
        self.assertTrue(s[-1].startswith("janela: --opened ") and wait_round.iso_local(BASE + 5) in s[-1])

    def test_once_no_limite_e_com_todas_ja_chegadas_so_painel_de_chegada(self):
        fn, ch = self.fake()
        rc, s = self.roda([], fn, once=True)
        self.assertEqual(rc, 2)
        self.assertEqual([c[0] for c in ch], ["chegada"])
        self.assertFalse(any(l.startswith("png:") or l.startswith("janela:") for l in s))
        for sl in ("prumo", "trava", "relance"):
            self.marcador(sl)
        fn, ch = self.fake()
        rc, s = self.roda([(0, {"done": [done("ci-prumo"), done("ci-trava"), done("ci-relance")], "events": []})], fn,
                          once=True)
        self.assertEqual(rc, 0)
        self.assertEqual([c[0] for c in ch], ["chegada"])
        self.assertFalse(any(l.startswith("png:") for l in s))

    def test_o_lote_de_chegadas_publica_uma_vez(self):
        for s in ("prumo", "trava"):
            self.marcador(s)
        fn, ch = self.fake()
        self.roda([(0, {"done": [done("ci-prumo"), done("ci-trava")], "events": []})], fn, timeout=30)
        self.assertEqual([c[0] for c in ch], ["abertura", "chegada", "fim"])

    def test_falha_do_painel_nao_muda_o_rc_nem_derruba_a_espera(self):
        for s in ("prumo", "trava", "relance"):
            self.marcador(s)

        def ruim(fase, opened, closed):
            raise RuntimeError("estourou")
        rc, s = self.roda([(0, {"done": [done("ci-prumo"), done("ci-trava"), done("ci-relance")], "events": []})], ruim)
        self.assertEqual(rc, 0)
        self.assertIn("⚠ painel: estourou", s)
        self.assertTrue(any(l.startswith("R2 · 3/3") for l in s))

    def test_sem_painel_fn_nada_do_painel_sai(self):
        for s in ("prumo", "trava", "relance"):
            self.marcador(s)
        rc, s = self.roda([(0, {"done": [done("ci-prumo"), done("ci-trava"), done("ci-relance")], "events": []})], None)
        self.assertFalse(any("orca-visual" in l or "png:" in l for l in s))
        self.assertEqual(len(s), 3)

    def test_main_publica_de_verdade_e_no_painel_desliga(self):
        os.makedirs(os.path.join(self.tmp, "dir"), exist_ok=True)
        reuniao = {"id": "t", "tema": "Tema", "fim": "23h", "dir": "dir", "worklog": "wl/{slug}.md",
                   "personas": PS["personas"]}
        with open(os.path.join(self.tmp, "reuniao.json"), "w", encoding="utf-8") as f:
            json.dump(reuniao, f)
        with open(os.path.join(self.tmp, "dir", "rodada-2.md"), "w", encoding="utf-8") as f:
            f.write("# Rodada 2 — debate (duração: ~1 min)\n")
        for s in ("prumo", "trava", "relance"):
            self.marcador(s)
        rows = []
        for sessao, (d, snd) in {"ci-prumo": ("p", "a"), "ci-trava": ("t", "b"), "ci-relance": ("r", "c")}.items():
            rows.append({"event": "open", "at": "2026-11-09T18:00:00-03:00", "name": sessao, "chat": "c", "dispatch": d,
                         "sender": snd, "run": "r", "operation": "o"})
        m = os.path.join(self.tmp, "m.jsonl")
        with open(m, "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(r) for r in rows) + "\n")
        pub = os.path.join(self.tmp, "pub")
        original, png_original = wait_round.wait_brza, panel.gera_png
        wait_round.wait_brza = lambda s, t: (0, {"done": [done(x) for x in s], "events": []})
        panel.gera_png = lambda h, p, w, a=2000: open(p, "wb").close()       # sem Chrome no teste
        try:
            base = ["2", "--reuniao", "reuniao.json", "--root", self.tmp, "--sessions", m]
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(io.StringIO()):
                rc = wait_round.main(base + ["--publish-dir", pub])
            linhas = saida.getvalue().splitlines()
            self.assertEqual(rc, 0, linhas)
            visuais = [l for l in linhas if l.startswith("::orca-visual")]
            self.assertEqual(len(visuais), 2)                                  # abertura e fim (todas na 1ª chamada)
            self.assertEqual(visuais[0], visuais[1])                           # o mesmo arquivo, republicado
            self.assertEqual([x for x in os.listdir(pub) if x.endswith(".html")], [re.search(r'file="([^"]+)"', visuais[0]).group(1)])
            self.assertTrue(os.path.isfile(os.path.join(self.tmp, "dir", "estado-r2.json")))
            self.assertFalse(any("⚠ painel" in l for l in linhas), linhas)
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(io.StringIO()):
                rc = wait_round.main(base + ["--no-panel"])
            self.assertEqual(rc, 0)
            self.assertNotIn("orca-visual", saida.getvalue())
        finally:
            wait_round.wait_brza, panel.gera_png = original, png_original

    def test_main_leva_o_personas_ao_painel_como_participantes(self):
        reuniao = {"id": "t", "tema": "T", "fim": "23h", "dir": "dir", "worklog": "wl/{slug}.md", "personas": PS["personas"]}
        chamado = []

        class FalsoPanel:
            pasta_da_reuniao = staticmethod(lambda r, root: os.path.join(root, "dir"))
            resolve_publish_dir = staticmethod(lambda d, p: (d or p, False))

            @staticmethod
            def publica_rodada(reu, n, root, **kw):
                chamado.append(kw)
                return {"linha": "::orca-visual{file=\"x.html\" title=\"x\"}", "png": None, "png_erro": None}
        fn = wait_round.monta_painel_fn(reuniao, 2, self.tmp, participantes=["Trava"], panel_mod=FalsoPanel)
        fn("chegada", "i", "f")
        self.assertEqual(chamado[0]["participantes"], ["Trava"])

    def test_main_com_personas_chega_ao_painel(self):
        os.makedirs(os.path.join(self.tmp, "dir"), exist_ok=True)
        reuniao = {"id": "t", "tema": "T", "fim": "23h", "dir": "dir", "worklog": "wl/{slug}.md", "personas": PS["personas"]}
        with open(os.path.join(self.tmp, "reuniao.json"), "w", encoding="utf-8") as f:
            json.dump(reuniao, f)
        for sl in ("prumo", "trava", "relance"):
            self.marcador(sl)
        m = os.path.join(self.tmp, "m.jsonl")
        with open(m, "w", encoding="utf-8") as f:
            f.write(json.dumps({"event": "open", "at": "2026-11-09T18:00:00-03:00", "name": "ci-trava", "chat": "c",
                                "dispatch": "t", "sender": "b", "run": "r", "operation": "o"}) + "\n")
        original, png_original = wait_round.wait_brza, panel.gera_png
        wait_round.wait_brza = lambda s, t: (0, {"done": [done(x) for x in s], "events": []})
        panel.gera_png = lambda h, p, w, a=2000: open(p, "wb").close()
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc = wait_round.main(["2", "--reuniao", "reuniao.json", "--root", self.tmp, "--sessions", m,
                                      "--publish-dir", os.path.join(self.tmp, "pub"), "--personas", "trava"])
        finally:
            wait_round.wait_brza, panel.gera_png = original, png_original
        self.assertEqual(rc, 0)
        with open(os.path.join(self.tmp, "dir", "estado-r2.json"), encoding="utf-8") as f:
            est = json.load(f)
        self.assertEqual(est["rodada"]["participantes"], ["Trava"])
        self.assertEqual({p["nome"]: p["estado"] for p in est["personas"]}["Prumo"], "fora da rodada")

    def test_sem_destino_grava_na_pasta_da_reuniao_e_avisa_uma_vez(self):
        os.makedirs(os.path.join(self.tmp, "dir"), exist_ok=True)
        reuniao = {"id": "t", "tema": "T", "fim": "23h", "dir": "dir", "worklog": "wl/{slug}.md", "personas": PS["personas"]}
        for s in ("prumo", "trava", "relance"):
            self.marcador(s)
        fn = wait_round.monta_painel_fn(reuniao, 2, self.tmp)
        antes = os.environ.pop("ORCA_CHAT_SCRATCH_DIR", None)
        try:
            a = fn("chegada", "18:00:00", "18:05:00")
            b = fn("chegada", "18:00:00", "18:06:00")
        finally:
            if antes is not None:
                os.environ["ORCA_CHAT_SCRATCH_DIR"] = antes
        self.assertTrue(a[0].startswith("⚠ painel: sem --publish-dir"))
        self.assertTrue(LINHA.match(a[1]))
        self.assertEqual(len(b), 1)
        self.assertTrue(any(x.endswith(".html") for x in os.listdir(os.path.join(self.tmp, "dir"))))


class Publish(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        from p7 import monta_raiz
        self.root, self.reuniao = monta_raiz(self.tmp)
        self.manifesto = os.path.join(self.root, ".sessions/reuniao-ci-no-chat/reuniao.json")
        self.nada = os.path.join(self.tmp, "nada")

    def roda(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            rc = panel.main(["publish", "3", "--reuniao", self.manifesto, "--root", self.root, "--measurements", self.nada,
                             "--sessions", self.nada, "--codex-dir", self.nada, "--opened", "18:37:02", "--closed",
                             "18:41:00", *extra])
        return rc, out.getvalue().splitlines()

    def test_imprime_a_linha_e_o_png(self):
        pub = os.path.join(self.tmp, "pub")
        original = panel.gera_png
        panel.gera_png = lambda h, p, w, a=2000: open(p, "wb").close()
        try:
            rc, l = self.roda("--publish-dir", pub)
        finally:
            panel.gera_png = original
        self.assertEqual(rc, 0, l)
        self.assertTrue(LINHA.match(l[0]), l)
        png = os.path.join(self.root, ".sessions/reuniao-ci-no-chat/painel-r3.png")
        self.assertEqual(l[1], f"png: {png}")
        self.assertTrue(os.path.isfile(os.path.join(self.root, ".sessions/reuniao-ci-no-chat/estado-r3.json")))
        self.assertEqual(len(os.listdir(pub)), 1)

    def test_no_png_e_so_a_linha(self):
        rc, l = self.roda("--publish-dir", os.path.join(self.tmp, "pub"), "--no-png")
        self.assertEqual(rc, 0)
        self.assertEqual(len(l), 1)
        self.assertTrue(LINHA.match(l[0]))

    def test_sem_worklog_rc_2(self):
        vazio = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, vazio, True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = panel.main(["publish", "3", "--reuniao", self.manifesto, "--root", vazio])
        self.assertEqual(rc, 2)


class Sintese(unittest.TestCase):
    def monta(self, final=True):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        d = os.path.join(tmp, ".sessions", "reuniao-tev1")
        os.makedirs(d)
        for nome in os.listdir(fixture("tev1")):
            if final or nome != "sintese-final.json":
                shutil.copy(fixture("tev1", nome), d)
        return tmp, os.path.join(d, "reuniao.json")

    def roda(self, tmp, manifesto, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            rc = panel.main(["sintese", "--reuniao", manifesto, "--root", tmp, *extra])
        return rc, out.getvalue().splitlines()

    def test_sem_o_final_mostra_cabecalho_cartoes_grafico_tabela_e_decisoes(self):
        tmp, man = self.monta(final=False)
        pub = os.path.join(tmp, "pub")
        rc, l = self.roda(tmp, man, "--publish-dir", pub, "--no-png")
        self.assertEqual(rc, 0, l)
        self.assertTrue(re.fullmatch(r'::orca-visual\{file="reuniao-tev1-sintese-[0-9a-f]{4}\.html" title="Síntese — [^"]*"\}',
                                     l[0]), l)
        with open(os.path.join(pub, os.listdir(pub)[0]), encoding="utf-8") as f:
            html = f.read()
        self.assertIn("6 personas · 5 rodadas", html)
        self.assertIn("21:20–21:58", html)
        self.assertIn('<div class="n">78</div>', html)    # o cartão do revisor
        self.assertIn(">82,8<", html)
        self.assertIn("23 · 25 · 0", html)                 # votos da R3
        self.assertIn("US$ 13,15", html)                   # 10,29 + 2,86
        self.assertIn("<svg", html)
        self.assertIn("#d97706", html)                     # o revisor, cor fixa
        self.assertEqual(html.count("<circle"), 5)         # a média da sala em cinco rodadas
        self.assertEqual(html.count("<rect"), 1)           # o revisor só na R5
        self.assertIn("76 → <b>82</b>", html)              # Balança, R1 → última
        self.assertIn("Para Anderson decidir", html)
        self.assertIn("R2.2 — quanto tempo", html)
        for ausente in ("A classificação", "O que se mediu", "As fases", "A próxima rodada"):
            self.assertNotIn(ausente, html)
        self.assertNotIn("100vh", html)
        self.assertIn("minmax(0,1fr)", html)

    def test_com_o_final_renderiza_conclusao_classificacao_barras_fases_e_proxima(self):
        tmp, man = self.monta(final=True)
        out = os.path.join(tmp, "s.html")
        rc, l = self.roda(tmp, man, "--out", out, "--no-png")
        self.assertEqual(rc, 0)
        self.assertEqual(l, ['::orca-visual{file="s.html" title="Síntese — Onde o tev1 local entra nos fluxos: CLI, Studio, '
                             'MCP, meeting-runner, plan-runner e migration-runner"}'])
        with open(out, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("O tev1 nos fluxos: o que se mediu", html)
        self.assertIn("nenhuma pergunta está pronta", html)
        self.assertIn('class="b b-go">fase 0', html)
        self.assertIn('class="b b-wait">após replay', html)
        self.assertIn('class="b b-out">reprovado', html)
        self.assertIn('class="b b-evo">evolução', html)
        self.assertIn("15/17", html)
        self.assertIn("width:88.2%", html)
        self.assertEqual(html.count('class="ph"'), 7)
        self.assertIn("A próxima rodada para você", html)
        self.assertIn("17 perguntas em 4 rodadas", html)

    def test_escapa_e_aceita_final_malformado(self):
        tmp, man = self.monta(final=False)
        d = os.path.dirname(man)
        with open(os.path.join(d, "sintese-final.json"), "w", encoding="utf-8") as f:
            json.dump({"conclusao": "<script>x</script>", "classificacao": "lixo", "barras": [{"rotulo": "a"}, 3],
                       "fases": None}, f)
        out = os.path.join(tmp, "s.html")
        rc, _ = self.roda(tmp, man, "--out", out, "--no-png")
        self.assertEqual(rc, 0)
        with open(out, encoding="utf-8") as f:
            html = f.read()
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_destino_pelo_scratch_do_chat_e_png_por_padrao(self):
        tmp, man = self.monta(final=False)
        scr = os.path.join(tmp, "scr")
        pngs = []
        original, antes = panel.gera_png, os.environ.get("ORCA_CHAT_SCRATCH_DIR")
        panel.gera_png = lambda h, p, w, a=2000: pngs.append((h, p, a)) or open(p, "wb").close()
        os.environ["ORCA_CHAT_SCRATCH_DIR"] = scr
        try:
            rc, l = self.roda(tmp, man)
        finally:
            panel.gera_png = original
            if antes is None:
                os.environ.pop("ORCA_CHAT_SCRATCH_DIR")
            else:
                os.environ["ORCA_CHAT_SCRATCH_DIR"] = antes
        self.assertEqual(rc, 0, l)
        self.assertTrue(l[0].startswith('::orca-visual{file="reuniao-tev1-sintese-'), l)
        self.assertEqual(len(os.listdir(scr)), 1)
        png = os.path.join(os.path.dirname(man), "sintese.png")
        self.assertEqual(l[1], f"png: {png}")
        self.assertEqual(pngs[0][1], png)
        self.assertEqual(pngs[0][0], os.path.join(scr, os.listdir(scr)[0]))

    def test_sem_destino_cai_na_pasta_da_reuniao_e_ainda_imprime_a_linha(self):
        tmp, man = self.monta(final=False)
        antes = os.environ.pop("ORCA_CHAT_SCRATCH_DIR", None)
        try:
            rc, l = self.roda(tmp, man, "--no-png")
        finally:
            if antes is not None:
                os.environ["ORCA_CHAT_SCRATCH_DIR"] = antes
        self.assertEqual(rc, 0)
        self.assertEqual(len(l), 1)
        self.assertTrue(LINHA.match(l[0]), l)
        self.assertTrue(any(x.startswith("reuniao-tev1-sintese-") for x in os.listdir(os.path.dirname(man))))

    def test_sem_estado_rc_2(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        d = os.path.join(tmp, "d")
        os.makedirs(d)
        with open(os.path.join(d, "reuniao.json"), "w") as f:
            json.dump({"id": "x", "tema": "t", "dir": "d", "personas": []}, f)
        rc, _ = self.roda(tmp, os.path.join(d, "reuniao.json"))
        self.assertEqual(rc, 2)


class AnexoCustoDaTarefa(unittest.TestCase):
    CUSTO = "\n## Custo da tarefa\n\nCorrido 7 min — agente 5 min · US$ 2,48 · até 22:02 de 2026-11-09, pelo `brza note commit`\n"

    def test_corta_o_custo_depois_do_marcador_e_recusa_outro_texto(self):
        base = "### Rodada 5: x\n\ntexto\n\n<!-- fim-rodada-5 -->\n"
        self.assertEqual(common.corta_medida(base + self.CUSTO).rstrip().splitlines()[-1], "<!-- fim-rodada-5 -->")
        for extra in ("\n## O que ficou\n\nNada.\n" + self.CUSTO, self.CUSTO + "\n## O que ficou\n\nNada.\n",
                      "\nsó um parágrafo solto\n" + self.CUSTO):
            cortado = common.corta_medida(base + extra)
            self.assertNotEqual(cortado.rstrip().splitlines()[-1], "<!-- fim-rodada-5 -->", extra)

    def test_custo_antes_do_marcador_nao_e_anexo(self):
        t = "### R5\n" + self.CUSTO + "\n<!-- fim-rodada-5 -->\n"
        self.assertEqual(common.corta_medida(t), t)

    def test_tally_e_wait_round_aceitam_o_worklog_real(self):
        texto = ("### Rodada 5: x\n\n- **Posição:** manteve\n\n<!-- fim-rodada-5 -->\n" + self.CUSTO)
        w = tally.parse_worklog(texto)
        self.assertEqual(w["marcador_final"], 5)
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        p = os.path.join(tmp, "w.md")
        for corpo, esperado in ((texto, 5), (texto.replace("\n## Custo", "\nOutra linha\n\n## Custo"), None)):
            with open(p, "w", encoding="utf-8") as f:
                f.write(corpo)
            self.assertEqual(wait_round.last_marker(p), esperado)
        self.assertIsNone(tally.parse_worklog(texto.replace(self.CUSTO, "\ntexto depois\n"))["marcador_final"])


if __name__ == "__main__":
    unittest.main()
