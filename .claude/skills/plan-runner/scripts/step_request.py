#!/usr/bin/env python3
"""O pedido do passo (PLN-021/D6, molde do D3): monta, a partir do plano, o texto que a sessão executora recebe.

Uso:
    python3 -I step_request.py PLN-NNN Pn [--out ARQUIVO] [--worklog CAMINHO] [--checkout CAMINHO] [--branch NOME]

O pedido leva o `### Pn` inteiro, o texto de cada `D` do `Executa` (da `Origem` ao `Em aberto`), a pergunta, a opção
escolhida e a resposta literal de cada `R` citado na `Origem` desses `D`, as Restrições e a Regressão do plano, onde
trabalhar, as regras e o protocolo de fim (seção `## Evidência` no worklog do executor, último marcador
`<!-- fim-Pn: feito|parado -->`; o commit na branch do passo com os testes verdes, merge e push pedem confirmação).

Padrões: `--out` = `<raiz>/.sessions/pln-nnn/Pn/pedido.md`; `--worklog` = `<raiz>/work/worklogs/<hoje>-pln-nnn-pn-<slug>.md`;
`--checkout` = `<pasta do repositório>/../brza-studio/.worktrees/pln-nnn-pn`; `--branch` = `feat/pln-nnn-pn`.

Recusa, com saída 1, o passo sem `D` quando o plano tem Desenho (salvo os de rodada, revisão, aceite e fechamento) e o
`R` ou `D` citado que não existe. Imprime o caminho gravado. Saída 2: uso ou plano que não existe.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import plan_md  # noqa: E402
import plan_state  # noqa: E402


class Recusa(Exception):
    pass


def slug(txt, limite=48):
    t = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    t = re.sub(r"`", "", t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if len(t) > limite:
        t = t[:limite]
        if "-" in t:
            t = t.rsplit("-", 1)[0]
    return t.strip("-")


def _repo_principal(raiz):
    try:
        r = subprocess.run(["git", "-C", raiz, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return os.path.dirname(r.stdout.strip().rstrip("/"))
    except (OSError, subprocess.SubprocessError):
        pass
    return raiz


def _texto_d(plano, d):
    s = d["secao"]
    linhas = s.arquivo.linhas[s.ini:s.fim]
    return "\n".join(linhas).rstrip()


def _bloco_r(plano, rid):
    """O texto de uma `R<n>.<k>`: pergunta, opção escolhida, resposta literal."""
    q = plano.pergunta(rid)
    if q is None:
        raise Recusa("o R citado não existe na Entrevista: %s" % rid)
    ls = ["### %s — %s" % (rid, q.tema or "pergunta")]
    ls.append("- **Rodada:** R%d — %s%s" % (q.n, q.rodada.titulo, " (enviada %s)" % q.rodada.enviada if q.rodada.enviada else ""))
    ops = q.opcoes()
    if ops:
        ls.append("- **Opções:**")
        for o in ops:
            ls.append("  - %s%s" % (o["rotulo"], " (recomendada)" if o["recomendada"] else ""))
    dec = q.decidido
    if dec:
        ls.append("- **Escolhida:** %s" % re.sub(r"^(Decidid[oa]|Escolhid[oa])[^—:]*[—:]\s*", "", re.sub(r"\*\*", "", dec).strip()))
    elif q.rodada.sem_resposta or not q.resposta:
        rec = [o["rotulo"] for o in ops if o["recomendada"]]
        ls.append("- **Escolhida:** sem resposta na rodada%s" % (
            "; vale a recomendada, a confirmar: %s" % rec[0] if rec else ""))
    lit = q.resposta
    if lit:
        ls.append("- **Resposta literal:** %s" % re.sub(r"^\*\*Resposta[^*]*\*\*:?\s*", "", lit))
    return "\n".join(ls)


def monta(plano, pid, worklog=None, checkout=None, branch=None, hoje=None):
    """Devolve (texto, caminhos). Levanta `Recusa`."""
    pl = plan_md.carrega(plano)
    p = pl.passo(pid)
    if p is None:
        raise Recusa("o plano %s não tem o passo %s" % (pl.id, pid))
    pid = p.id
    if plan_state.passo_exige_design(pl, p):
        raise Recusa("o passo %s não tem `Executa D…` e o plano tem Desenho" % pid)
    ds = []
    for did in p.executa:
        d = pl.desenho(did)
        if d is None:
            raise Recusa("o passo %s executa %s, que o Desenho não tem" % (pid, did))
        ds.append(d)
    rs = []
    for d in ds:
        for r in d["origem_rs"]:
            if r not in rs:
                rs.append(r)
    blocos_r = []
    for r in rs:
        if "." in r:
            blocos_r.append(_bloco_r(pl, r))
        else:
            rod = pl.rodada(int(r[1:]))
            if rod is None:
                raise Recusa("o R citado não existe na Entrevista: %s" % r)
            for q in rod.perguntas:
                blocos_r.append(_bloco_r(pl, q.id))
    num = re.match(r"PLN-(\d+)", pl.id)
    pln = pl.id
    base = "%s-%s" % (pln.lower(), pid.lower())
    hoje = hoje or datetime.date.today().isoformat()
    raiz = pl.raiz
    if worklog is None:
        worklog = os.path.join(raiz, "work", "worklogs", "%s-%s-%s.md" % (hoje, base, slug(p.titulo)))
    if checkout is None:
        checkout = os.path.join(os.path.dirname(_repo_principal(raiz)), "brza-studio", ".worktrees", base)
    if branch is None:
        branch = "feat/%s" % base
    restr = pl.secao(r"^Restrições\b")
    regr = pl.secao(r"^Regressão\b")
    passo_texto = "\n".join(p.secao.linhas).rstrip()
    L = []
    L.append("Você executa o passo %s do %s numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você "
             "não conduz o plano, executa um passo dele." % (pid, pln))
    L.append("")
    L.append("## O passo")
    L.append(passo_texto)
    L.append("")
    L.append("## O que o Desenho fixou")
    if ds:
        for d in ds:
            L.append(_texto_d(pl, d))
            L.append("")
        L.pop()
    else:
        L.append("O passo não cita item do Desenho; vale o texto dele acima.")
    L.append("")
    L.append("## O que as rodadas decidiram")
    L.append("\n\n".join(blocos_r) if blocos_r else "Nenhuma rodada citada na Origem dos itens acima.")
    L.append("")
    L.append("## Restrições e Regressão")
    L.append("**Restrições do plano**")
    L.append("")
    L.append(restr.texto().strip() if restr and restr.texto().strip() else "O plano não tem `## Restrições`.")
    L.append("")
    L.append("**Regressão**")
    L.append("")
    L.append(regr.texto().strip() if regr and regr.texto().strip() else "O plano não tem `## Regressão`.")
    L.append("")
    L.append("## Onde trabalhar")
    L.append("- checkout: %s (branch %s)" % (checkout, branch))
    L.append("- worklog: %s" % worklog)
    L.append("")
    L.append("## Regras")
    L.append("- Não grave o plano, não commite nada no brza-workspace, não pergunte a Anderson.")
    L.append("- Desvio local: registre no worklog como `X` proposto e siga. Desvio que muda o contrato do D: pare, "
             "registre e feche com `parado`.")
    L.append("- O pedido autoriza o commit na branch `%s` do checkout, com os testes verdes. Merge e push pedem "
             "confirmação: não os faça." % branch)
    L.append("")
    L.append("## O fim")
    L.append("1. Preencha `## Evidência` no worklog, uma linha por item:")
    L.append("   - `commit: brza-studio@<sha7>` (ou `commit: aguarda confirmação`)")
    L.append("   - `comando: \\`<comando>\\` → <resultado> (≤ 2 min)` quando roda em até dois minutos")
    L.append("   - `arquivos: <caminho>, …`")
    L.append("   - `desvios: X? — <uma linha>` ou `desvios: nenhum`")
    L.append("2. A última linha do worklog é `<!-- fim-%s: feito -->` ou `<!-- fim-%s: parado -->`." % (pid, pid))
    L.append("3. Envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o "
             "encerramento.")
    return "\n".join(L) + "\n", {"worklog": worklog, "checkout": checkout, "branch": branch}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="step_request.py", description="monta o pedido do passo")
    ap.add_argument("plano")
    ap.add_argument("passo")
    ap.add_argument("--out")
    ap.add_argument("--worklog")
    ap.add_argument("--checkout")
    ap.add_argument("--branch")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        pl = plan_md.carrega(a.plano)
    except plan_md.PlanoNaoEncontrado as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    try:
        texto, info = monta(pl, a.passo, a.worklog, a.checkout, a.branch)
    except Recusa as e:
        print("recusado: %s" % e, file=sys.stderr)
        return 1
    out = a.out
    if not out:
        pid = pl.passo(a.passo).id
        out = os.path.join(pl.raiz, ".sessions", pl.id.lower(), pid, "pedido.md")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(texto)
    print(os.path.abspath(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
