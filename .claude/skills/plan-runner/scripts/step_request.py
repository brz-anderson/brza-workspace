#!/usr/bin/env python3
"""O pedido do passo (PLN-021/D6, molde do D3): monta, a partir do plano, o texto que a sessão executora recebe.

Uso:
    python3 -I step_request.py PLN-NNN Pn [--out ARQUIVO] [--worklog CAMINHO] [--checkout CAMINHO] [--branch NOME]

O pedido leva o `### Pn` inteiro, o texto de cada `D` do `Executa` (da `Origem` ao `Em aberto`), a pergunta, a opção
escolhida e a resposta literal de cada `R` citado na `Origem` desses `D`, as Restrições e a Regressão do plano, onde
trabalhar, as regras e o protocolo de fim (seção `## Evidência` no worklog do executor, último marcador
`<!-- fim-Pn: feito|parado -->`; o commit na branch do passo com os testes verdes, merge e push pedem confirmação).

Padrões: `--out` = `<raiz>/.sessions/pln-nnn/Pn/pedido.md`; `--worklog` = `<raiz>/work/worklogs/<hoje>-pln-nnn-pn-<slug>.md`;
`--checkout` = `<pasta do repositório>/../brza-studio/.worktrees/pln-nnn-pn`; `--branch` = `feat/pln-nnn-pn`, nunca
`master`/`main` (recusa). O `executor.py open` não usa esse padrão de checkout: exige `--checkout` ou `--tree`.

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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plan_md  # noqa: E402
import plan_state  # noqa: E402


class Refusal(Exception):
    pass


def slug(txt, limit=48):
    t = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    t = re.sub(r"`", "", t).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if len(t) > limit:
        t = t[:limit]
        if "-" in t:
            t = t.rsplit("-", 1)[0]
    return t.strip("-")


def _repo_main(root):
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return os.path.dirname(r.stdout.strip().rstrip("/"))
    except (OSError, subprocess.SubprocessError):
        pass
    return root


def same_repo(path_a, path_b):
    """True se as duas pastas são do mesmo repositório git (mesmo `--git-common-dir`: raiz, subpasta ou outro worktree dele)."""
    dirs = []
    for pth in (path_a, path_b):
        try:
            r = subprocess.run(["git", "-C", pth, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                               capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            return os.path.realpath(path_a) == os.path.realpath(path_b)
        if r.returncode != 0 or not r.stdout.strip():
            return os.path.realpath(path_a) == os.path.realpath(path_b)
        dirs.append(os.path.realpath(r.stdout.strip()))
    return dirs[0] == dirs[1]


def _text_d(plan, d):
    s = d["section"]
    lines = s.file.lines[s.start:s.end]
    return "\n".join(lines).rstrip()


def _block_r(plan, rid):
    """O texto de uma `R<n>.<k>`: pergunta, opção escolhida, resposta literal."""
    q = plan.question_text(rid)
    if q is None:
        raise Refusal("o R citado não existe na Entrevista: %s" % rid)
    ls = ["### %s — %s" % (rid, q.topic or "pergunta")]
    ls.append("- **Rodada:** R%d — %s%s" % (q.n, q.round.title, " (enviada %s)" % q.round.sent_on if q.round.sent_on else ""))
    options = q.option_list()
    if options:
        ls.append("- **Opções:**")
        for o in options:
            ls.append("  - %s%s" % (o["label"], " (recomendada)" if o["recommended"] else ""))
    dec = q.decided_line
    if dec:
        ls.append("- **Escolhida:** %s" % re.sub(r"^(Decidid[oa]|Escolhid[oa])[^—:]*[—:]\s*", "", re.sub(r"\*\*", "", dec).strip()))
    elif q.round.unanswered or not q.answer:
        rec = [o["label"] for o in options if o["recommended"]]
        ls.append("- **Escolhida:** sem resposta na rodada%s" % (
            "; vale a recomendada, a confirmar: %s" % rec[0] if rec else ""))
    lit = q.answer
    if lit:
        ls.append("- **Resposta literal:** %s" % re.sub(r"^\*\*Resposta[^*]*\*\*:?\s*", "", lit))
    return "\n".join(ls)


def build(plan, pid, worklog=None, checkout=None, branch=None, on_date=None):
    """Devolve (texto, caminhos). Levanta `Recusa`."""
    pl = plan_md.load(plan)
    p = pl.step(pid)
    if p is None:
        raise Refusal("o plano %s não tem o passo %s" % (pl.id, pid))
    pid = p.id
    if plan_state.step_requires_design(pl, p):
        raise Refusal("o passo %s não tem `Executa D…` e o plano tem Desenho" % pid)
    ds = []
    for did in p.executes:
        d = pl.design_text(did)
        if d is None:
            raise Refusal("o passo %s executa %s, que o Desenho não tem" % (pid, did))
        ds.append(d)
    rs = []
    for d in ds:
        for r in d["origin_ids"]:
            if r not in rs:
                rs.append(r)
    blocks_r = []
    for r in rs:
        if "." in r:
            blocks_r.append(_block_r(pl, r))
        else:
            round_row = pl.round(int(r[1:]))
            if round_row is None:
                raise Refusal("o R citado não existe na Entrevista: %s" % r)
            for q in round_row.questions:
                blocks_r.append(_block_r(pl, q.id))
    num = re.match(r"PLN-(\d+)", pl.id)
    pln = pl.id
    base = "%s-%s" % (pln.lower(), pid.lower())
    on_date = on_date or datetime.date.today().isoformat()
    root = pl.root
    if worklog is None:
        worklog = os.path.join(root, "work", "worklogs", "%s-%s-%s.md" % (on_date, base, slug(p.title)))
    if checkout is None:
        checkout = os.path.join(os.path.dirname(_repo_main(root)), "brza-studio", ".worktrees", base)
    if branch is None:
        branch = "feat/%s" % base
    if branch in ("master", "main"):
        raise Refusal("a branch autorizada para commit não pode ser master/main; passe a branch do passo (`--branch feat/%s`)" % base)
    commit_ok = not same_repo(checkout, root)
    constraints = pl.section(r"^Restrições\b")
    regression = pl.section(r"^Regressão\b")
    step_text = "\n".join(p.section.lines).rstrip()
    L = []
    L.append("Você executa o passo %s do %s numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você "
             "não conduz o plano, executa um passo dele." % (pid, pln))
    L.append("")
    L.append("## O passo")
    L.append(step_text)
    L.append("")
    L.append("## O que o Desenho fixou")
    if ds:
        for d in ds:
            L.append(_text_d(pl, d))
            L.append("")
        L.pop()
    else:
        L.append("O passo não cita item do Desenho; vale o texto dele acima.")
    L.append("")
    L.append("## O que as rodadas decidiram")
    L.append("\n\n".join(blocks_r) if blocks_r else "Nenhuma rodada citada na Origem dos itens acima.")
    L.append("")
    L.append("## Restrições e Regressão")
    L.append("**Restrições do plano**")
    L.append("")
    L.append(constraints.text().strip() if constraints and constraints.text().strip() else "O plano não tem `## Restrições`.")
    L.append("")
    L.append("**Regressão**")
    L.append("")
    L.append(regression.text().strip() if regression and regression.text().strip() else "O plano não tem `## Regressão`.")
    L.append("")
    L.append("## Onde trabalhar")
    L.append("- checkout: %s (branch %s)" % (checkout, branch))
    L.append("- worklog: %s" % worklog)
    L.append("")
    L.append("## Regras")
    L.append("- Não grave o plano, não commite nada no brza-workspace (o worklog fica sem commit: a coordenação o commita), "
             "não pergunte a Anderson.")
    L.append("- Desvio local: registre no worklog como `X` proposto e siga. Desvio que muda o contrato do D: pare, "
             "registre e feche com `parado`.")
    if commit_ok:
        L.append("- O pedido autoriza o commit na branch `%s` do checkout `%s`, e só nele, com os testes verdes; se o "
                 "checkout estiver em outra branch, crie essa a partir do estado atual. Merge e push pedem "
                 "confirmação: não os faça." % (branch, checkout))
    else:
        L.append("- Este checkout é o do brza-workspace: não commite em lugar nenhum e registre `commit: aguarda "
                 "confirmação` na evidência.")
    L.append("")
    L.append("## O fim")
    L.append("1. Preencha `## Evidência` no worklog, uma linha por item:")
    L.append("   - `commit: brza-studio@<sha7>` (ou `commit: aguarda confirmação`)")
    L.append("   - `comando: \\`<comando>\\` → <resultado> (≤ 2 min)` quando roda em até dois minutos")
    L.append("     (a coordenação reroda o comando sem shell: escreva a forma simples, com no máximo `VAR=v` e `cd <pasta> &&` na "
             "frente; sem `;`, `|`, `>`, `$` nem crase)")
    L.append("   - `arquivos: <caminho>, …`")
    L.append("   - `cobre: <n>, <n>` (os números dos subpassos que a evidência cobre) ou `cobre: todos`; só esses viram `[x]`")
    L.append("   - `desvios: X? — <uma linha>` ou `desvios: nenhum`")
    L.append("2. A última linha do worklog é `<!-- fim-%s: feito -->` ou `<!-- fim-%s: parado -->`." % (pid, pid))
    L.append("3. Envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o "
             "encerramento.")
    return "\n".join(L) + "\n", {"worklog": worklog, "checkout": checkout, "branch": branch}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="step_request.py", description="monta o pedido do passo")
    ap.add_argument("plan")
    ap.add_argument("step")
    ap.add_argument("--out")
    ap.add_argument("--worklog")
    ap.add_argument("--checkout")
    ap.add_argument("--branch")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        pl = plan_md.load(a.plan)
    except plan_md.PlanNotFound as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    try:
        text, info = build(pl, a.step, a.worklog, a.checkout, a.branch)
    except Refusal as e:
        print("recusado: %s" % e, file=sys.stderr)
        return 1
    out = a.out
    if not out:
        pid = pl.step(a.step).id
        out = os.path.join(pl.root, ".sessions", pl.id.lower(), pid, "pedido.md")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(os.path.abspath(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
