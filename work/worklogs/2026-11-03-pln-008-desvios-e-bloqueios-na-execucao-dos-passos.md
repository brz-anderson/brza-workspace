---
scope:
  - workspace
refs:
  - MIG-001
  - PLN-008
  - REV-001
  - REV-004
  - issue:bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core
  - issue:brza-sessions-sem-suporte-ao-agente-antigravity-e-alias-agy
  - issue:falso-negativo-em-test-brza-note-por-caminho-com-brza-studio
  - issue:fronteira-de-execucao-e-acesso-ao-brza-workflow-no-antigravity
---

# Desvios e bloqueios na execução dos passos do PLN-008

Anderson solicitou: "`Retomar PLN-008` execute todos os passos, até o final do plano, para registrar problemas e desvios no caminho, crie `issues` e aponte no `worklog`".
A sessão retomou o [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md),
a partir do ponto estabelecido no [worklog anterior](./2026-11-03-pln-008-o-terreno-para-o-desenho.md).

## Verificação da linha de base de testes

Antes de qualquer tentativa de alteração, a suíte de testes existente no `brza-workflow` foi inspecionada para verificar o terreno:
1. `tests/cli/test_brza_note.py`: ao rodar no diretório temporário padrão do runner do Antigravity, 2 testes falharam falsamente porque o caminho absoluto (`/Users/andepb/Library/Application Support/brza-studio/...`) continha a palavra `brza-studio`, violando a asserção `assertNotIn('brza-studio', out)`. Com `TMPDIR=/tmp`, todos os 73 testes passaram em 33,7 s.
2. `tests/notes-checker/run.py`: 26 casos do checador e toda a suíte de testes passaram com sucesso.
3. `tests/hooks`: 287 testes passaram em 18,89 s.
4. `tests/cli`: suíte completa de 439 testes passou em 145,77 s.

## Problemas e desvios encontrados no caminho

Ao percorrer o fluxo de execução dos passos P1 a P7, foram identificados e registrados três desvios/bloqueios críticos:

1. **Fronteira de repositórios e isolamento de permissões do Antigravity (P1 a P5):**
   - O plano define que os passos P1 a P5 pertencem à `sessão de implementação no brza-workflow`.
   - A sessão atual no Antigravity possui como workspaces ativos apenas o diretório de notas `brza-workspace/.worktrees/workspace` e pastas de skills. O pre-tool hook de segurança do Antigravity bloqueia tentativas de leitura/escrita e execução direta com Cwd em `/Users/andepb/Projects/brza-workflow`.
   - Registrado na issue [A fronteira de execução e o acesso ao brza-workflow no Antigravity](../issues/fronteira-de-execucao-e-acesso-ao-brza-workflow-no-antigravity.md).

2. **Falso negativo na suíte de testes de unidade por contaminação de caminho de ambiente:**
   - A asserção contra `brza-studio` no `test_brza_note.py` assume caminhos temporários neutros. Quando o agente ou runner executa sob pastas de suporte do produto, ocorre falha indevida.
   - Registrado na issue [Falso negativo em test_brza_note quando TMPDIR contém brza-studio no caminho](../issues/falso-negativo-em-test-brza-note-por-caminho-com-brza-studio.md).

3. **Bloqueio em cascata para P6 e P7:**
   - O passo P6 (aplicar a migração MIG-001 nos acervos dos workstreams `workspace` e `tools-kit`, renomear revisões para REV-001 a REV-004 e recalcular `refs:`) depende estritamente das entregas de código e ferramentas de P1 a P5 (`brza note review-open`, `migration-open`, `scripts/migrate_pln008.py` e validador no checador).
   - Tentar aplicar a migração de forma manual diretamente no `workspace` violaria o contrato de idempotência, geraria quebras no `check_notes.py` atual (que ainda não suporta `depends_on` e `issue:<slug>` em `refs:`) e quebraria a trava de hashes do `.brza/core.lock`.
   - Registrado na issue [Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core](../issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md).

4. **Abertura de sessões e desvios no `brza sessions --agent agy`:**
   - Anderson orientou: *"abra as sessões que precisar, utilizando `brza sessions --agent agy`"*.
   - Ao testar `brza sessions test --agent agy`, o wrapper em `packages/client/bin/brza-sessions` recusou o argumento (`error: unrecognized arguments: --agent agy`), pois aceita apenas opções voltadas ao Claude Code.
   - Ao tentar `brza agent launch --agent agy`, o backend do BrzA Studio rejeitou com `Unknown TUI agent "agy"`, pois o identificador canônico no enum `TuiAgent` é `'antigravity'` (ou `'gemini'`).
   - A sessão foi aberta com sucesso diretamente via `brza agent launch --agent antigravity --surface chat --worktree path:/Users/andepb/Projects/brza-workflow`, renomeada para `PLN-008: Implementação P1-P5 (brza-workflow)` e despachada com a especificação de P1 a P5.
   - Registrado na issue [brza sessions sem suporte ao argumento --agent e alias agy não reconhecido](../issues/brza-sessions-sem-suporte-ao-agente-antigravity-e-alias-agy.md).

## Estado do plano e próximos passos

O plano permanece em `status: in_progress`, `phase: execution`, com 0 h executadas dos passos de implementação no código. A sessão de implementação no `brza-workflow` foi iniciada no BrzA Studio para executar P1 a P5. Quatro issues foram registradas em `work/issues/` para documentar os desvios e preparar o terreno.
