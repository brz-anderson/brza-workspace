---
scope:
  - workspace
  - brza-workflow
refs:
  - MIG-001
  - PLN-008
  - REV-005
---

# O início de P6 do PLN-008: regressão, sincronização e reservas

## Plano aceito em 2026-11-03

Anderson respondeu literalmente "Iniciar P6" nesta sessão, autorizando o passo de publicação, sincronização e
migração do acervo do [PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
P7 permanece fora desta execução; cada workstream aplica suas notas pela sessão dona.

## Evidências desta etapa

- Bloqueios ativos: consulta em todas as branches locais retornou vazia. Checador inicial do workspace: 54 arquivos,
  zero erros e avisos.
- P1–P5 já publicados em `brza-workflow@a666e78`. Nenhum push do repositório de ferramentas foi necessário.
- CLI completa: 467 testes em 199,593 s; hooks completos: 288 em 21,128 s; notes-checker: 26 casos, todos passaram.
  Os comandos do plano rodaram com `TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1`. Saídas da sessão no scratch:
  `/tmp/pln008-p6-cli.log`, `/tmp/pln008-p6-hooks.log`, `/tmp/pln008-p6-checker.log`.
- `brza-sync --dry-run` conferiu a versão publicada. `brza-sync --ref a666e78` publicou `5dcc2b3` no workspace e
  sincronizou os cinco workstreams. As quatro alterações locais de norma/golden e o commit local `9f51cda` do
  brza-workflow ficaram fora dessa operação. Outra sessão posteriormente publicou `c527e42` e sincronizou `1f56808`;
  essa segunda operação não é entrega desta tarefa.
- `brza-note index --bootstrap-pln008`: cinco reservas gravadas, commit `4bb114e`, sem colisão.
- Prévia sem aplicação: quatro pareceres e 97 worklogs a atualizar em tools-kit (29), workspace (21), brand (4) e
  studio (43); playground sem alterações. Menções históricas desconhecidas apenas avisam, conforme D3.
- [MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../issues/MIG-001-renumeracao-rev-e-refs-pln-008.md)
  criada para revisão prévia independente, antes de qualquer migração real.

## Reconciliação de P1–P4

O collector conferiu os commits `b7fb3d2`, `b7e8727`, `3fc3935` e `a168f73`: há implementação e testes correspondentes,
mas isso não certifica todo o aceite. P2 não demonstra alteração/remoção de cada campo isoladamente; P4 tem fixtures,
sem artefato de sonda real atual no commit. A sonda complementar em `/tmp/pln008-p6-index-probe.py` comprovou 68/68 cenários de alteração/remoção e 68/68 rebuilds subsequentes idempotentes. O checador da fixture é stub: a prova é do índice, não da validação semântica. Os helpers nas fontes atuais resolveram workspace como `workspace` e código na master sem workstream; conta `.claude` e identidade noreply corretas. Não há worktree atual de código em branch de plano, cujo caso segue somente em fixture. Nenhuma medição histórica foi reescrita. O fechamento da reconciliação segue em P6.
Os quatro commits usam `anderson@fixfy.com.br`, divergente da identidade exigida quando esta tarefa foi aberta;
histórico preservado, sem reescrita. Horas históricas não aferidas; timestamps não foram convertidos em duração.

## Ponto de parada desta etapa

A revisão prévia encontrou que o critério da MIG não prova a preservação de tags e dos demais campos. A sonda do
revisor removeu tags em memória e o critério aprovou; não demonstra defeito no migrador. O destino está em rodada
com Anderson antes da aplicação. P6 permanece parcial e a MIG aberta; nenhuma nota histórica foi migrada nesta etapa.

A revisão prévia está em [REV-005: A revisão prévia da MIG-001 em P6 do PLN-008](../reviews/REV-005-pln-008-p6-previa-da-mig-001.md):
A1, prova de preservação; A2, comando e ordem por sessões; A3, hipótese recomendada como falsa sobre a raiz do checador.
Todos os destinos aguardam a mesma rodada antes da aplicação.

## Fora do workspace

- **O quê e onde:** logs, relatórios, baseline de HEADs e sonda complementar temporários em `/tmp/pln008-p6-*`,
  incluindo repositórios e remotes locais de fixture. **Risco:** consumo temporário de disco; nenhum acervo real
  foi migrado pelas sondas. **Estado:** artefatos locais para conferência. **Como desfazer:** remover apenas esses
  artefatos temporários depois de consolidar as evidências; isso não desfaz commits do workspace.
