#!/usr/bin/env python3
"""Grava a rodada na Entrevista do plano (PLN-021/D6).

Uso:
    python3 -I round_log.py PLN-NNN --next
    python3 -I round_log.py PLN-NNN --from rodada.json [--dry-run]

`--next` imprime o número da próxima rodada: o maior `### Rodada N` + 1.

`--from` lê o JSON da rodada e acrescenta `### Rodada N — <titulo> (enviada <data>)` ao fim da `## Entrevista` do
`-plan.md` — ou ao fim do `-interview.md`, quando o plano é dividido e ele existe —, com o "Apresentado antes", as
perguntas e as opções no formato do molde (rótulo, `(recomendada)`, `custo`, `se paga`) e, por pergunta:
  - `escolhidas` sem `literal`: `**Decidido — <rótulos>.**`;
  - `literal`: `**Resposta:** "…"`, com a leitura (`resposta.leitura`, ou `Lida como: <rótulos>` quando há `escolhidas`);
  - `reabre: "R1.2"`: acrescenta `**→ reaberta em R<N>.<k>**` à linha antiga (a `Decidido`/`Resposta` da R1.2, ou a
    última linha dela).
`--dry-run` imprime o bloco e o destino, sem gravar nada. Imprime o caminho gravado.

rodada.json:
    {"titulo": "...", "enviada": "AAAA-MM-DD", "apresentado_antes": "...",
     "respondida": {"data": "AAAA-MM-DD", "sessao": "..."} | null,
     "perguntas": [{"tema": "...", "multipla": false,
                    "opcoes": [{"rotulo": "...", "recomendada": true, "custo": "...", "se_paga": "..."}],
                    "resposta": {"escolhidas": [0], "literal": null} | null, "reabre": null | "R1.2"}]}

Saída 0; 1 com JSON fora da forma ou `reabre` que não existe; 2 uso ou plano que não existe.
"""
import argparse
import datetime
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import plan_md  # noqa: E402


class FormaInvalida(Exception):
    def __init__(self, erros):
        super().__init__("; ".join(erros))
        self.erros = erros


def valida(dados, plano):
    erros = []
    if not isinstance(dados, dict):
        raise FormaInvalida(["o JSON da rodada precisa ser um objeto"])
    if not isinstance(dados.get("titulo"), str) or not dados["titulo"].strip():
        erros.append("titulo: texto obrigatório")
    for chave in ("enviada", "apresentado_antes"):
        if dados.get(chave) is not None and not isinstance(dados[chave], str):
            erros.append("%s: texto" % chave)
    if dados.get("enviada") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", dados["enviada"]):
        erros.append("enviada: AAAA-MM-DD")
    resp = dados.get("respondida")
    if resp is not None:
        if not isinstance(resp, dict) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(resp.get("data", ""))):
            erros.append("respondida: {data: AAAA-MM-DD, sessao: texto} ou null")
        elif resp.get("sessao") is not None and not isinstance(resp["sessao"], str):
            erros.append("respondida.sessao: texto")
    ps = dados.get("perguntas")
    if not isinstance(ps, list) or not ps:
        erros.append("perguntas: lista com ao menos uma pergunta")
        ps = []
    for k, q in enumerate(ps, 1):
        pre = "perguntas[%d]" % (k - 1)
        if not isinstance(q, dict):
            erros.append("%s: objeto" % pre)
            continue
        if not isinstance(q.get("tema"), str) or not q["tema"].strip():
            erros.append("%s.tema: texto obrigatório" % pre)
        ops = q.get("opcoes")
        if not isinstance(ops, list) or not ops:
            erros.append("%s.opcoes: lista com ao menos uma opção" % pre)
            ops = []
        for j, o in enumerate(ops):
            if not isinstance(o, dict) or not isinstance(o.get("rotulo"), str) or not o["rotulo"].strip():
                erros.append("%s.opcoes[%d].rotulo: texto obrigatório" % (pre, j))
                continue
            for c in ("custo", "se_paga"):
                if o.get(c) is not None and not isinstance(o[c], str):
                    erros.append("%s.opcoes[%d].%s: texto" % (pre, j, c))
        r = q.get("resposta")
        if r is not None:
            if not isinstance(r, dict):
                erros.append("%s.resposta: objeto ou null" % pre)
            else:
                esc = r.get("escolhidas")
                if esc is not None:
                    if not isinstance(esc, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in esc):
                        erros.append("%s.resposta.escolhidas: lista de índices" % pre)
                    elif any(i < 0 or i >= len(ops) for i in esc):
                        erros.append("%s.resposta.escolhidas: índice fora das opções" % pre)
                    elif len(esc) > 1 and not q.get("multipla"):
                        erros.append("%s.resposta.escolhidas: mais de uma, e a pergunta não é `multipla`" % pre)
                if r.get("literal") is not None and not isinstance(r["literal"], str):
                    erros.append("%s.resposta.literal: texto ou null" % pre)
        rb = q.get("reabre")
        if rb is not None:
            if not isinstance(rb, str) or not re.fullmatch(r"R\d+\.\d+", rb):
                erros.append("%s.reabre: `R<n>.<k>` ou null" % pre)
            elif plano.pergunta(rb) is None:
                erros.append("%s.reabre: %s não existe na Entrevista" % (pre, rb))
    if erros:
        raise FormaInvalida(erros)


def proximo_n(plano):
    return max([r.n for r in plano.rodadas()] or [0]) + 1


def _rotulos(q, idxs):
    return "; ".join(q["opcoes"][i]["rotulo"].rstrip(".") for i in idxs)


def _sessao(txt):
    """`a sessão do workstream playground` -> `na sessão do workstream playground`; outro texto fica como veio."""
    t = txt.strip()
    t = re.sub(r"^(?:a\s+)?(sessão\b)", r"na \1", t)
    return t


def bloco(dados, n, nivel=3):
    """O Markdown da rodada `n`, com o heading de `nivel`."""
    enviada = dados.get("enviada") or datetime.date.today().isoformat()
    L = ["%s Rodada %d — %s (enviada %s)" % ("#" * nivel, n, dados["titulo"].strip(), enviada), ""]
    if dados.get("apresentado_antes"):
        ap = dados["apresentado_antes"].strip().split("\n")
        L.append("> **Apresentado antes:** " + ap[0])
        L.extend("> " + x if x.strip() else ">" for x in ap[1:])
        L.append("")
    resp = dados.get("respondida")
    if resp:
        L.append("Respondida em %s%s." % (resp["data"], (", " + _sessao(resp["sessao"])) if resp.get("sessao") else ""))
    else:
        L.append("Sem resposta.")
    L.append("")
    for k, q in enumerate(dados["perguntas"], 1):
        if q.get("multipla"):
            L.append("%d. **%s** (seleção múltipla). Opções:" % (k, q["tema"].strip().rstrip(".")))
        else:
            L.append("%d. **%s.** Opções:" % (k, q["tema"].strip().rstrip(".")))
        ops = q["opcoes"]
        for j, o in enumerate(ops):
            partes = o["rotulo"].strip().rstrip(".;")
            if o.get("recomendada"):
                partes += " (recomendada)"
            extra = []
            if o.get("custo"):
                extra.append("custo: %s" % o["custo"].strip().rstrip(".;"))
            if o.get("se_paga"):
                extra.append("se paga: %s" % o["se_paga"].strip().rstrip(".;"))
            linha = "   - " + partes + (" — " + "; ".join(extra) if extra else "")
            linha += "." if j == len(ops) - 1 else ";"
            L.append(linha)
        r = q.get("resposta") or {}
        esc = r.get("escolhidas") or []
        lit = r.get("literal")
        if lit:
            L.append("")
            leitura = r.get("leitura")
            if not leitura and esc:
                leitura = "Lida como: %s." % _rotulos(q, esc)
            L.append('   **Resposta:** "%s"%s' % (lit.strip(), (" " + leitura.strip()) if leitura else ""))
        elif esc:
            L.append("")
            L.append("   **Decidido — %s.**" % _rotulos(q, esc))
        L.append("")
    while L and not L[-1].strip():
        L.pop()
    return "\n".join(L) + "\n"


def _destino(plano):
    """(arquivo, índice de inserção, nível dos headings): o fim da `## Entrevista`, ou o fim do `-interview.md`."""
    inter = next((a for a in plano.arquivos if a.papel == "interview"), None)
    nivel = 3
    if inter is not None:
        rs = [r for r in plano.rodadas() if r.arquivo is inter]
        if rs:
            nivel = rs[-1].nivel
        else:
            nivel = 2
        fim = len(inter.linhas)
        while fim > 0 and not inter.linhas[fim - 1].strip():
            fim -= 1
        return inter, fim, nivel
    sec = plano.secao(r"^Entrevista\b")
    if sec is None:
        raise FormaInvalida(["o plano não tem `## Entrevista` nem `-interview.md`; abra a seção antes"])
    rs = [r for r in plano.rodadas() if r.arquivo is plano.principal]
    if rs:
        nivel = rs[-1].nivel
    fim = sec.fim
    while fim > sec.ini + 1 and not plano.principal.linhas[fim - 1].strip():
        fim -= 1
    return plano.principal, fim, nivel


def _linha_antiga(q):
    """Índice da linha da pergunta `q` que recebe `→ reaberta em`: a `Decidido`/`Resposta`, ou a última não vazia."""
    for i in (q.indice_decidido(), q.indice_resposta()):
        if i is not None:
            return i
    ult = q.fim - 1
    while ult > q.ini and not q.arquivo.linhas[ult].strip():
        ult -= 1
    return ult


def aplica(plano, dados, dry_run=False):
    """Devolve `{n, arquivo, bloco, reabertas}`; grava, salvo `dry_run`."""
    valida(dados, plano)
    n = proximo_n(plano)
    arq, pos, nivel = _destino(plano)
    texto = bloco(dados, n, nivel)
    reabertas = []
    edicoes = {}  # arquivo -> {indice: texto}
    for k, q in enumerate(dados["perguntas"], 1):
        rb = q.get("reabre")
        if rb:
            antigo = plano.pergunta(rb)
            i = _linha_antiga(antigo)
            nova = "R%d.%d" % (n, k)
            edicoes.setdefault(antigo.arquivo, {})[i] = "**→ reaberta em %s**" % nova
            reabertas.append((rb, nova))
    if dry_run:
        return {"n": n, "arquivo": arq.path, "bloco": texto, "reabertas": reabertas}
    # monta as linhas novas de cada arquivo
    alvos = set(edicoes) | {arq}
    for a in alvos:
        linhas = list(a.linhas)
        for i, marca in sorted(edicoes.get(a, {}).items()):
            linhas[i] = linhas[i].rstrip() + " " + marca
        if a is arq:
            linhas[pos:pos] = [""] + texto.rstrip("\n").split("\n")
            if linhas[-1] != "":
                linhas.append("")
        with open(a.path, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))
    return {"n": n, "arquivo": arq.path, "bloco": texto, "reabertas": reabertas}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="round_log.py", description="grava a rodada na Entrevista do plano")
    ap.add_argument("plano")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--next", action="store_true")
    g.add_argument("--from", dest="origem")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-panel", action="store_true", help="não republica o painel do plano")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if a.next:
        print(proximo_n(pl))
        return 0
    try:
        with open(a.origem, encoding="utf-8") as f:
            dados = json.load(f)
    except (OSError, ValueError) as e:
        print("erro: não li %s: %s" % (a.origem, e), file=sys.stderr)
        return 1
    try:
        res = aplica(pl, dados, dry_run=a.dry_run)
    except FormaInvalida as e:
        for x in e.erros:
            print("forma: %s" % x, file=sys.stderr)
        return 1
    if a.dry_run:
        print("# dry-run: Rodada %d, %s" % (res["n"], res["arquivo"]))
        print(res["bloco"], end="")
        for old, new in res["reabertas"]:
            print("# marcaria %s com `→ reaberta em %s`" % (old, new))
    else:
        print(res["arquivo"])
        if not a.no_panel:
            import plan_panel
            plan_panel.emite(plan_panel.publica_seguro(pl.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
