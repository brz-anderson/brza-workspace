---
status: open
type: migration
opened: 2026-11-03
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

- [ ] P1 — Conferir as reservas `REV-001`..`REV-004` e `MIG-001` no índice da master.
- [ ] P2 — Provar os quatro nomes novos, a ausência dos antigos e os links resolvidos nos workstreams donos.
- [ ] P3 — Conferir refs dos worklogs e remoção de date com tags e demais campos preservados.
- [ ] P4 — Registrar os comandos, resultados e commits antes de concluir esta MIG.

## Revisão antes da aplicação

Revisão independente registrada em [REV-005: A revisão prévia da MIG-001 em P6 do PLN-008](../reviews/REV-005-pln-008-p6-previa-da-mig-001.md). A aplicação aguarda o destino de A1 a A3 na rodada desta sessão.

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
