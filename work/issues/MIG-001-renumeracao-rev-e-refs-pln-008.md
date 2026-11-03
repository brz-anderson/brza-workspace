---
status: done
type: migration
opened: 2026-11-03
completed: 2026-11-03
owner: Anderson
description: Renomeia os quatro pareceres históricos para REV-001..REV-004 e recalcula refs dos worklogs.
scope:
  - workspace
tags:
  - tooling
---

# MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs

## Estado-alvo

Origem: [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md), D3, D4, D7 e D8.

- Os quatro pareceres históricos seguem `work/reviews/REV-NNN-<slug>.md` e H1 `# REV-NNN: <título>`:
  - `tools-kit`: `work/reviews/REV-001-pln-002-os-comandos-brza.md`
  - `workspace`: `work/reviews/REV-002-pln-005-a-confianca-dos-fatos.md`
  - `workspace`: `work/reviews/REV-003-pln-006-o-brza-init.md`
  - `workspace`: `work/reviews/REV-004-pln-006-a-migracao.md`
- Os worklogs trazem `refs:` calculado pelas menções e links do corpo (D3), sem o campo `date:` no frontmatter.

## Estado atual

- Pareceres históricos sem prefixo `REV-NNN-` no caminho e com H1 `# REV: <título>`.
- Worklogs históricos sem `refs:` consolidado pelo extrator D3 ou com `date:` no frontmatter.

Prévia de 2026-11-03: 4 pareceres e 97 worklogs em `tools-kit` (29), `workspace` (21), `brand` (4) e `studio` (43); `playground` sem alterações. Menções históricas desconhecidas geram aviso e ficam fora de refs, conforme D3.

## Passos

- [x] P1 — Conferir as reservas `REV-001`..`REV-004` e `MIG-001` no índice da master: bootstrap `4bb114e`; a aplicação respondeu "bootstrap em dia".
- [x] P2 — Aplicar em cada workstream pela sessão dona, no comando e na ordem de "Aplicação": ver "Execução".
- [x] P3 — Provar os quatro nomes novos, a ausência dos antigos e os links resolvidos nos workstreams donos:
  blocos 1 e 2 do critério, saída 0.
- [x] P4 — Conferir refs dos worklogs e remoção de date com tags e demais campos preservados, pelo bloco de
  preservação do critério: 107 notas, 98 worklogs.
- [x] P5 — Registrar os comandos, resultados e commits antes de concluir esta MIG: "Execução" e "Conclusão".

## Aplicação

Cada sessão dona roda, no worktree do próprio workstream, com `plans/`, `work/` e `wiki/` sem alteração por commitar:

```bash
python3 "$HOME/Projects/brza-workflow/scripts/migrate_pln008.py" --apply --workstream <dono>
```

O script recusa a aplicação sem `--workstream`, com nota suja ou com a branch de outro workstream. Ele mesmo commita
por caminhos, dá o push e reconstrói o índice, com o assunto `docs(pln-008): migração MIG-001 em <dono>` ou
`docs(pln-008): links cruzados em <dono>`: são esses commits que o bloco de preservação do critério compara com o pai.

A ordem, porque os links cruzados só se reescrevem quando o destino já existe na branch dona:

1. `tools-kit`: renomeia REV-001.
2. `workspace`: renomeia REV-002 a REV-004 e reescreve os links para REV-001.
3. `tools-kit` de novo: reescreve links para REV-002 a REV-004, se houver; no ensaio, nenhuma mudança.
4. `brand`, `studio` e `playground`, cada um na própria sessão, em qualquer ordem depois do item 3; `playground` não
   muda no ensaio.

Ensaio de 2026-11-03, num clone isolado em `/private/tmp/pln008-sandbox`, com remoto local e sem `BRZA_WORKSPACE`:
a ordem acima aplicou com saída 0 nas seis passagens (1 + 3 pareceres renomeados; 29, 22, 4 e 43 worklogs em
`tools-kit`, `workspace`, `brand` e `studio`), e os três blocos do critério passaram. O acervo real não foi tocado.

## Execução

- **`tools-kit`, item 1**, pela sessão `tools-kit-mig001`, em 2026-11-03: prévia igual ao ensaio (REV-001, 5 notas
  com links, 29 worklogs); `--apply` com saída 0; commit `bf36704`, com push; índice `81620e3` e reconstrução
  `6e10fd0` na master; checador com 73 arquivos, 0 erros e 0 avisos; worklog do `tools-kit` em `8600fa1`.
- **`workspace`, item 2**, pela sessão `workspace-a6`, em 2026-11-03: prévia igual ao ensaio (REV-002 a REV-004, 5
  notas com links, 22 worklogs); `--apply` com saída 0; commit `361d0d4`, com push; checador com 59 arquivos, 0
  erros e 4 avisos `unknown-ref-mention` (PLN-029 e PLN-011, menções históricas que o D3 só avisa). O bloco de
  preservação, restrito às duas árvores, conferiu 60 notas, 51 delas worklogs.
- **`tools-kit`, item 3**, pela sessão `tools-kit-mig001`: prévia e `--apply` zerados, sem commit da migração, como
  no ensaio; checador com 74 arquivos, 0 erros e 0 avisos; worklog do `tools-kit` em `57c29b5`.
- **Fora do mapa D4:** três pareceres do PLN-009 criados em 2026-11-03 no `tools-kit` (`3d94663`, `8b622f8`, `5ef53de`)
  sem `REV-NNN`. Anderson escolheu, nesta data, "Issue no tools-kit (Recomendado)": a sessão dona do PLN-009 os numera.
  Issue gravada pela sessão `tools-kit-rev-pln009` em `6292986`: [Os pareceres do PLN-009 sem número REV](os-pareceres-do-pln-009-sem-numero-rev.md).
  Não entram nesta MIG.
- **`brand`, item 4**, pela sessão `brand-mig001`: prévia igual ao ensaio (4 worklogs); commit `0e80b71`, com push;
  checador com 63 arquivos, 0 erros e 0 avisos; worklog de lá em `2a40e3a`.
- **`studio`, item 4**, pela sessão `studio-mig001`: prévia igual ao ensaio (43 worklogs); commit `d5abc5e`, com
  push; checador com 0 erros e os avisos que já havia, menos os 39 `date-on-worklog`; worklog de lá em `3aeb36d`.
- **`playground`, item 4**, pela sessão `playground-mig001`: prévia e `--apply` zerados, sem commit da migração;
  checador com 0 erros e 0 avisos; worklog de lá em `70c4a68`.
- **Texto de link:** o `refs:` dos worklogs de `brand` e `playground` pegou REV-001 e REV-004 do título desta MIG no
  texto do link ("REV-001..REV-004"), como o D3 conta. Anderson escolheu "Ponto para P7" em 2026-11-03.

## Conclusão

Concluída em 2026-11-03 pela sessão `workspace-a6`, no worktree `workspace`, com as cinco árvores atualizadas pelo
remoto: os três blocos do critério saíram com 0 — "Mapa D4 conferido", "H1, mapa D4, links, refs e ausência de date
conferidos nas cinco árvores" e "Frontmatter preservado em 107 nota(s) migrada(s), 98 worklog(s)" —, com o checador sem
erros nas cinco. Dois `brza note index --rebuild` seguidos responderam "em dia, nada a acrescentar", e a master
continuou em `e8606a4`.

## Revisão antes da aplicação

Revisão independente registrada em [REV-005: A revisão prévia da MIG-001 em P6 do PLN-008](../reviews/REV-005-pln-008-p6-previa-da-mig-001.md).
Destinos de 2026-11-03: A1 corrigido aqui, com o bloco de preservação no critério; A2 corrigido aqui, com a seção
"Aplicação"; A3 falso.

## Critério de conclusão

Rodar no worktree `workspace`, com os dois worktrees presentes:

```bash
python3 .claude/skills/notes-checker/scripts/check_notes.py
python3 .claude/skills/notes-checker/scripts/check_notes.py --root ../tools-kit
python3 - <<'PY'
from pathlib import Path
mapa = {
    '../tools-kit/work/reviews': [('001', 'pln-002-os-comandos-brza')],
    'work/reviews': [('002', 'pln-005-a-confianca-dos-fatos'),
                     ('003', 'pln-006-o-brza-init'), ('004', 'pln-006-a-migracao')],
}
for pasta, revisoes in mapa.items():
    for numero, slug in revisoes:
        antigo = Path(pasta) / (slug + '.md')
        novo = Path(pasta) / ('REV-' + numero + '-' + slug + '.md')
        assert novo.is_file(), str(novo)
        assert not antigo.exists(), str(antigo)
print('Mapa D4 conferido: quatro destinos presentes e quatro origens ausentes.')
PY
```

A execução parcial em um workstream não conclui a MIG; a sessão dona registra os comandos, resultados e commits.

Além do mapa e dos links acima, conferir H1, refs e ausência de date em todas as árvores:

```bash
python3 - <<'PYVERIFY'
from pathlib import Path
import runpy
import subprocess
flow = Path.home() / 'Projects/brza-workflow'
root = Path.cwd().parent.parent
ns = runpy.run_path(str(flow / 'scripts/migrate_pln008.py'))
ng = ns['load_note_globals']()
for owner, rev_id, old, new in ns['REV_MAP']:
    tree = root / '.worktrees' / owner
    assert not (tree / old).exists(), old
    assert (tree / new).read_text().split('# ', 1)[1].startswith(rev_id + ':'), new
for name in ('tools-kit', 'workspace', 'brand', 'studio', 'playground'):
    tree = root / '.worktrees' / name
    catalog = ng['build_target_catalog'](tree)
    for path in sorted((tree / 'work/worklogs').glob('*.md')):
        content = path.read_text()
        refs, unknown = ng['extract_worklog_refs'](content, path, tree, catalog)
        assert ng['set_frontmatter_refs'](content, refs, remove_date=True) == content, str(path)
    subprocess.run(['python3', str(tree / '.claude/skills/notes-checker/scripts/check_notes.py')], check=True)
print('H1, mapa D4, links, refs e ausência de date conferidos nas cinco árvores.')
PYVERIFY
```

Por fim, a preservação: cada nota que um commit da MIG-001 tocou mantém o frontmatter do pai, linha a linha, exceto `refs:` e
`date:` nos worklogs. A renomeação compara o caminho antigo com o novo; arquivo criado ou apagado falha.

```bash
python3 - <<'PYPRESERVE'
from pathlib import Path
import subprocess
import re

root = Path.cwd().parent.parent
SUBJECTS = ('docs(pln-008): migração MIG-001 em ', 'docs(pln-008): links cruzados em ')
EXPECTED = ('tools-kit', 'workspace', 'brand', 'studio')
WORKLOG = re.compile(r'work/worklogs/(?!README\.md$)[^/]+\.md')


def git(tree, *args):
    return subprocess.run(['git', '-C', str(tree), *args], check=True, capture_output=True, text=True).stdout


def frontmatter_lines(text, drop):
    if not text.startswith('---\n') or (end := text.find('\n---', 4)) < 0:
        return []
    kept, skipping = [], False
    for line in text[4:end].split('\n'):
        key = re.match(r'^([A-Za-z_][\w-]*):', line)
        if key:
            skipping = key.group(1) in drop
        elif not line.startswith((' ', '\t')):
            skipping = False
        if not skipping:
            kept.append(line)
    return kept


total, worklogs = 0, 0
for name in ('tools-kit', 'workspace', 'brand', 'studio', 'playground'):
    tree = root / '.worktrees' / name
    commits = [line.split(' ', 1)[0] for line in git(tree, 'log', '--format=%H %s').splitlines()
               if any(line.split(' ', 1)[1] == s + name for s in SUBJECTS)]
    assert commits or name not in EXPECTED, f'sem commit da MIG-001 em {name}'
    for c in commits:
        for row in git(tree, 'diff-tree', '-r', '-M', '--no-commit-id', '--name-status', c + '^', c,
                       '--', 'plans', 'work', 'wiki').splitlines():
            status, *paths = row.split('\t')
            old, new = paths[0], paths[-1]
            assert status[0] in 'MR', f'{name}:{c[:7]} {status} {new}: só edição ou renomeação'
            if not new.endswith('.md'):
                continue
            drop = ('refs', 'date') if WORKLOG.fullmatch(new) else ()
            before = frontmatter_lines(git(tree, 'show', f'{c}^:{old}'), drop)
            after = frontmatter_lines(git(tree, 'show', f'{c}:{new}'), drop)
            assert before == after, f'{name}:{c[:7]} {new}: frontmatter mudou além de refs/date\n{before}\n{after}'
            total += 1
            worklogs += bool(drop)
print(f'Frontmatter preservado em {total} nota(s) migrada(s), {worklogs} worklog(s): '
      'só refs/date mudaram, comparando cada commit da MIG-001 com o pai.')
PYPRESERVE
```
