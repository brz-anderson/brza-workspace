---
status: open
description: O PLN-008 delega P1-P5 ao brza-workflow, mas o isolamento de workspace no Antigravity barra chamadas de arquivo e comandos no core a partir do workspace.
scope:
  - workspace
  - brza-workflow
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# A fronteira de execução e o acesso ao brza-workflow no Antigravity

## O contexto

O [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md)
estabelece em suas Restrições:
"Norma comum, CLI, scripts e testes mudam no `brza-workflow`; chegam ao workspace pelo sync, sem editar cópias do core."
E define que os passos de implementação P1 a P5 têm como executor a `sessão de implementação no brza-workflow`.

Ao tentar retomar o plano e executar os passos a partir da sessão principal do Antigravity no worktree `workspace`
(`brza-workspace/.worktrees/workspace`), a ferramenta de arquivos (`view_file`, `replace_file_content`, `write_to_file`)
e o `Cwd` de execução direta em `/Users/andepb/Projects/brza-workflow` foram recusados pelo pre-tool hook de segurança:

```text
denied by pre-tool hook: Access to path "/Users/andepb/Projects/brza-workflow" is denied.
It is outside the allowed workspace directories: [/Users/andepb/Projects/brza-workspace/.worktrees/workspace, ...]
```

## O problema e o desvio

1. **Separação de papéis e repositórios:** o repositório `brza-workflow` é externo ao workspace `brza-workspace`.
   A sessão no `workspace` não tem o diretório do core em seus workspaces autorizados no Antigravity.
2. **Execução íntegra de P1 a P5:** contornar o hook de segurança via scripts ou comandos indiretos violaria as
   diretrizes de integridade e a regra de que o core evolui em sua própria sessão/worktree do `brza-workflow`, com commits
   e branch próprios, antes de sincronizar via `brza sync`.
3. **Bloqueio em cascata:** sem implementar e commitar P1 a P5 no `brza-workflow`, P6 (aplicação de MIG-001 no acervo
   dos workstreams) e P7 (revisão independente e fechamento) não possuem as ferramentas necessárias (`brza note review-open`,
   `brza note migration-open`, `scripts/migrate_pln008.py` e checador atualizado).

## O que falta decidir

- Abrir uma sessão dedicada do Antigravity apontada para `/Users/andepb/Projects/brza-workflow` para implementar P1 a P5,
  ou adicionar o caminho `/Users/andepb/Projects/brza-workflow` aos workspaces ativos da sessão de desenvolvimento.
- Após o commit no `brza-workflow`, publicar e sincronizar para o `brza-workspace` via `brza sync` para então executar P6 e P7.
