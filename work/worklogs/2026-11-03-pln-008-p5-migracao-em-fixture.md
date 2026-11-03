---
scope:
  - workspace
  - brza-workflow
refs:
  - PLN-008
  - issue:bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core
---

# A conclusão de P5 do PLN-008 em acervo de teste

## Plano aceito em 2026-11-03

Anderson pediu concluir apenas P5 do
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md),
aproveitando os arquivos existentes e preservando trabalho alheio. P6 e P7 ficam para depois; não aplicar migração
real nem publicar P5 nesta entrega. A abertura da sessão Codex pelo Studio foi autorizada após a recusa de
`brza sessions --agent codex`, pela opção 1 informada no encaminhamento.

## Entrega e evidências

- Em 2026-11-03, o Studio mostrou a sessão Antigravity `PLN-008: Implementação P1-P5 (brza-workflow)` em `done`,
  sem ferramenta ativa, com mensagem de limite de uso. Nenhuma sessão foi interrompida.
- Leitura das normas, plano, desenho, entrevista, memória e bloqueios: nenhuma nota aberta com `blocks:` nas cinco
  branches locais; a issue de P6/P7 permanece aberta. A memória de apresentação de notas foi consultada.
- O rascunho herdado falhava nos três testes por chamar um helper inexistente e apontar para `tags.yaml` ausente.
  Também apagava refs inválidos e criava a MIG como concluída; esses comportamentos foram corrigidos.
- Commit local `a666e78`, no `brza-workflow`: `scripts/migrate_pln008.py` e `tests/cli/test_migrate_pln008.py`.
  Prévia padrão, aplicação com seleção explícita, reserva/extrator reutilizados, mapa D4/H1, links cruzados nos dois
  sentidos, remoção de date preservando campos, worktree ausente e recusa antes de escrita para refs inválidos.
  A MIG nasce aberta; a sessão dona precisa registrar evidência antes de concluí-la.
- Testes novos: 10 casos focais passaram. Suíte CLI completa: 467 testes passaram em 169,983 s. Comandos executados:

```bash
TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli -p 'test_migrate_pln008.py'
```

```bash
TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli
```

A fixture comprova prévia sem alteração de arquivos/commits/índice e segunda aplicação sem mudança de bytes, HEADs
ou linhas do índice. Também comprova bootstrap repetido/conflitante e preservação de arquivo alheio já staged.
Toda aplicação de migração ocorreu em repositórios temporários com remote local, nunca no acervo real.

## Estado e retomada

P5 concluído. Executado em horas: não aferido. O plano tinha `executed_h: 0`, `remaining_h: 18` e nenhum passo marcado,
apesar dos commits `b7fb3d2`, `b7e8727`, `3fc3935` e `a168f73`; essa divergência foi registrada no plano, sem atestar
P1–P4 nem inventar horas. Os quatro usam `anderson@fixfy.com.br`, divergindo da identidade exigida
`240569289+brz-anderson@users.noreply.github.com`. Não foram reescritos; preparar o tratamento em P6.

Outra sessão, `Correção de agentes no brza sessions`, alterou e publicou `README.md`, `packages/client/bin/brza-sessions`
e `tests/cli/test_brza_sessions.py` no commit `f0f1171`, levando junto os quatro commits anteriores já presentes na
master. Foi observado `HEAD == origin/master == f0f1171` antes do commit de P5. Essa publicação ocorreu na outra tarefa;
P5 fica local. Nenhuma alteração alheia foi incluída no commit de P5.

P6/P7 continuam pendentes, conforme
[Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core](../issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md).
Conferir P1–P4, reconciliar horas e autoria, preparar publicação/sync e somente então executar a migração autorizada
pelas sessões donas. Nenhuma cópia da norma comum no workspace foi alterada nesta tarefa.

## Fora do workspace

- **O quê e onde:** abertura autorizada desta sessão Codex, `Concluir P5 do PLN-008`, diretamente no Studio, no
  checkout `brza-workflow`. **Risco:** concorrência de escrita e consumo de cota; a sessão Antigravity foi conferida
  antes das alterações. **Estado:** sessão aberta; tarefa P5 encerrada neste registro. **Como desfazer:** encerrar
  apenas esta aba pelo Studio; isso não desfaz commits nem arquivos.
