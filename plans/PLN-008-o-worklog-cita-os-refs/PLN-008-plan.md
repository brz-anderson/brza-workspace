---
status: in_progress
phase: execution
origin: request
description: O brza note commit preenche o refs do worklog com os IDs que ele cita, e revisão e migração ganham REV-NNN e MIG-NNN
ready: sim
estimate_h: 18
executed_h: 0
remaining_h: 18
scope:
  - workspace
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca

- **Retomar:** P6 iniciado por Anderson em 2026-11-03 ("Iniciar P6"). Regressão passou: CLI 467, hooks 288 e
  checador 26 casos. Core `a666e78` sincronizado em `5dcc2b3`; bootstrap dos cinco IDs gravado em `4bb114e`.
  MIG-001 criada para revisão prévia. Aplicação aguarda o destino do achado sobre preservação de tags/demais campos
  no critério de conclusão e, depois, execução pelas sessões donas. P1–P4 continuam sem atestado integral; horas
  históricas não aferidas e commits preservados. P7 não iniciado.
- **Histórico desta retomada:** tentativa de execução integral em 2026-11-03 encontrou a fronteira de repositório entre `workspace` e
  `brza-workflow` no Antigravity, registrando 4 issues:
  [A fronteira de execução e o acesso ao brza-workflow no Antigravity](../../work/issues/fronteira-de-execucao-e-acesso-ao-brza-workflow-no-antigravity.md),
  [Falso negativo em test_brza_note quando TMPDIR contém brza-studio no caminho](../../work/issues/falso-negativo-em-test-brza-note-por-caminho-com-brza-studio.md),
  [Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core](../../work/issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md) e
  [brza sessions sem suporte ao argumento --agent e alias agy não reconhecido](../../work/issues/brza-sessions-sem-suporte-ao-agente-antigravity-e-alias-agy.md).
  Naquela tentativa, a sessão de implementação no repositório `brza-workflow` foi aberta pelo Studio (`antigravity`)
  para conduzir P1 a P5; o plano ainda registrava 0 h executadas, sem aferição dos commits posteriores. O ls começa local e
  passa a fetch padrão se dados errados forem listados com frequência, conforme a emenda à R12.3.
- **Dividido:** [PLN-008 — Entrevista](PLN-008-interview.md) · [PLN-008 — Desenho](PLN-008-design.md)

## Pedido

- **Origem:** pedido livre, na sessão `workspace` de 2026-11-03 (bb0fd632).

"Proposta: colocar o campo tags no frontmatter do worklogs/ com tags por plano, revisão, migração e etc, afim de
facilitar a busca por conteúdo relacionado. Ex: o worklog de agora, do plano 003, tags: - pln-003 - mig-001" —
Anderson, em 2026-11-03.

Os itens, numerados para a Cobertura:

1. o worklog diz, no frontmatter, a que plano, issue, revisão e migração se refere, para achar o conteúdo relacionado;
2. a revisão tem ID próprio, `REV-NNN`, e as 4 que existem são renumeradas (R2.2);
3. a migração tem ID próprio, `MIG-NNN`, na forma da R3;
4. as skills criam, revisam e executam essas notas.

"Temos também que criar/adaptar skills para a criação, revisão e execução dessas novas notas" — Anderson, em
2026-11-03, na mesma sessão, depois da R3.

5. o frontmatter das notas e o índice servem ao coordenador do PLN-003 (R4, R5).

"E o sessionId, runtime e infos assim no frontmatter do worklogs/ ou outras notas, faça um levantamento geral de como o
frontmatter das notas pode melhorar visando um nelhor desempenhi no fluxo do coordenador" — Anderson, em 2026-11-03, na
mesma sessão.

### Cobertura

Os cenários abaixo são provas a implementar ou executar nos passos; não afirmam testes já existentes ou aprovados.

| Origem     | Critério de aceite                                                                                                   | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `Pedido 1` | o commit preenche refs a partir dos links e IDs do corpo | P1 | extração e alteração só dos caminhos pedidos (unidade CLI) |
| `Pedido 1` | refs com ID inexistente é barrado, inclusive antes do recálculo | P1 | refs antigo inválido não desaparece; alvos entre branches (unidade) |
| `Pedido 1` | worklogs existentes ganham refs automaticamente | P5, P6 | fixture de migração idempotente (unidade); acervo após aplicação (integração) |
| `Pedido 2` | revisões têm REV-NNN e as quatro existentes recebem REV-001 a REV-004 | P2, P5, P6 | reserva concorrente e mapa D4 (unidade); nomes/H1 reais (integração) |
| `Pedido 3` | MIG é issue type migration no molde; MIG-001 renumera revisões | P2, P3, P5, P6 | reserva, validação e fixture MIG (unidade); conclusão MIG-001 (integração) |
| `Pedido 4` | única migration-runner cria, revisa e executa MIG com revisor independente | P3, P7 | conferir operações e independência contra D1 (revisão documental) |
| `Pedido 4` | plan-runner escreve parecer com REV-NNN | P3, P7 | conferir conduct, molde e reserva (revisão documental e unidade CLI) |
| `R4.1` | eventos em worktree têm workstream/conta corretos e o índice resolve nome disponível | P4 | eventos em notas/código e fallback de sessão com/sem client (unidade e sonda atual) |
| `R4.2` | commit avisa sem barrar plano/issue aberto sem priority | P2 | saída de aviso e commit bem-sucedido (unidade CLI) |
| `R4.3` | índice grava campos de pressão, owner e horas; rebuild recompõe | P2 | alterar cada campo e reconstruir, incluindo listas/ausências (unidade) |
| `R5.2` | issue aceita estimate_h opcional e o índice grava número | P1, P2 | hora válida, inválida e ausente (unidade) |
| `R5.3` | date sai dos worklogs, tags fica, checador avisa date | P1, P5, P6 | aviso (unidade); preservação de campos e acervo (integração) |
| `R6.1` | ls lista issues/decisões de todos os workstreams e ordena pelos três campos | P2 | filtros, ordens, ausentes e empate por ID (unidade CLI) |
| `R7.2` | depends_on opcional em planos/issues e índice | P1, P2 | validação e serialização da lista (unidade) |
| `R9.1` | só done satisfaz; dropped exige rever a relação | P1, P7 | casos dos estados contra contrato D2 (unidade/revisão); sem novo cálculo de prontidão |
| `R9.2` | alvo inexistente, autorreferência e ciclo geram erro | P1 | grafo entre branches com diagnósticos de alvo e ciclo (unidade) |
| `R10` | extração fora de cercas preserva inline/links/histórico; desconhecido avisa | P1 | tabela de entradas D3, normalização e avisos (unidade) |
| `R11.2` | session identifica a operação, inclusive rebuild | P2, P4 | reconstrução por outra sessão e ausência de nome (unidade) |
| `R12` | ls começa local, mostra abertos/recentes e refresh falha explicitamente | P2 | nenhuma rede no padrão; refresh e falha sem fallback (unidade CLI) |
| `R12 emenda` | erros frequentes na listagem fazem fetch virar padrão | P3, P7 | gatilho qualitativo preservado na norma, sem inventar limiar (revisão documental) |

### Fora de escopo

- **Os IDs em `tags`, como na proposta.** Ficou o campo `refs:` (R1.1); o `tags` segue só para assunto, no vocabulário
  fechado do checador.
- **Uma pasta `work/migrations/` e o MIG como plano.** Perderam na R3.2.
- **`session_id`, runtime, conta e modelo no frontmatter.** Ficam na medição e no `brza sessions` (R4.1).

## Pendências conhecidas

- [MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../../work/issues/MIG-001-renumeracao-rev-e-refs-pln-008.md) — execução pendente da revisão prévia.
- [A fronteira de execução e o acesso ao brza-workflow no Antigravity](../../work/issues/fronteira-de-execucao-e-acesso-ao-brza-workflow-no-antigravity.md)
- [Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core](../../work/issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md)
- [brza sessions sem suporte ao argumento --agent e alias agy não reconhecido](../../work/issues/brza-sessions-sem-suporte-ao-agente-antigravity-e-alias-agy.md)

## Entrevista

[PLN-008 — Entrevista](PLN-008-interview.md)

## Desenho

[PLN-008 — Desenho](PLN-008-design.md) — D1 a D10, aceitos com o corte da R13.

## Restrições

- Norma comum, CLI, scripts e testes mudam no `brza-workflow`; chegam ao workspace pelo sync, sem editar cópias do core.
- O aceite da R13 não autoriza executar: cada passo aguarda pedido explícito. Outros workstreams gravam seu próprio acervo.
- Não reescrever medição histórica nem inventar datas, prioridade, autoria ou limiar do gatilho da R12.3.

## Pré-requisitos

Conferidos em 2026-11-03: `brza-workflow/bin/brza-note`, `core/.claude/skills/notes-checker/scripts/check_notes.py`,
`tests/cli/test_brza_note.py`, `tests/cli/test_brza_note_index.py`, `tests/notes-checker/run.py` e testes de medição
existem; a árvore do `brza-workflow` está limpa. Não há bloqueio ativo encontrado nas branches locais.
Revalidar antes de P1. Os demais passos dependem das entregas anteriores; colisão de reservas ou fonte de runtime
indisponível volta à rodada, conforme D7/D10.

## Passos

Corte aceito em 2026-11-03, R13: sete entregas e 18 h estimadas. P5 está entregue com evidência abaixo. Existem commits
de P1–P4 (`b7fb3d2`, `b7e8727`, `3fc3935`, `a168f73`); sua existência não atesta o cumprimento integral desses passos.
Os campos `executed_h: 0` e `remaining_h: 18` permanecem como valores legados ainda não reconciliados, não como medição
do trabalho entregue. Não há aferição recuperável de horas nesta retomada; P6 deve reconciliá-las sem inferir duração dos commits.
Cada passo fecha com
comando/resultado e commit do repositório correspondente; o plano recebe a evidência e as horas no mesmo ato.

### P1 — Referências e dependências são conferidas antes do commit

Executa D2, D3 e validações de D9 · executor: sessão de implementação no `brza-workflow`.

Estimado: 3 h · Executado: — h

- [ ] Escrever casos que falhem em `tests/cli/test_brza_note.py` e `tests/notes-checker/run.py`: refs antigo inválido,
  cercas/inline/links, citação de subitem, alvo entre branches, autorreferência/ciclo, estimate_h na issue e aviso date.
- [ ] Implementar em `bin/brza-note` e `core/.claude/skills/notes-checker/scripts/check_notes.py` o catálogo de alvos,
  validação anterior ao recálculo e atualização idempotente só dos worklogs pedidos. Preservar identidade da issue após rename.
- [ ] Rodar os testes abaixo e registrar resultados; conferir que commit com outro caminho sujo continua isolado.
- [ ] Commit no `brza-workflow`; registrar evidência e Executado neste plano.

Na raiz do `brza-workflow`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli -p 'test_brza_note.py'
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/notes-checker/run.py
```

### P2 — Reservas, índice e listagem cumprem os contratos

Executa D5, D6, D7 e D9 · executor: sessão de implementação no `brza-workflow` · depende de P1.

Estimado: 4 h · Executado: — h

- [ ] Escrever casos em `tests/cli/test_brza_note_index.py` e `test_brza_note.py`: reserva simultânea, três recusas,
  bootstrap repetido/conflitante, passagem reserva→nota, alteração de cada campo e rebuild idempotente.
- [ ] Implementar `review-open`, `migration-open`, campos aprovados, aviso priority e ls em `bin/brza-note`.
- [ ] Provar filtros/ordens/ausências, nenhuma rede por padrão, refresh com erro explícito e índice indisponível.
- [ ] Rodar CLI completa, commitar e registrar evidência/Executado.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli
```

### P3 — Skills e norma descrevem o fluxo entregue

Executa D1, D6, D7 e D9 · executor: sessão de implementação no `brza-workflow` · depende de P2.

Estimado: 2 h · Executado: — h

- [ ] Criar `core/.claude/skills/migration-runner/SKILL.md` e seu molde com as três operações de D1.
- [ ] Adaptar `plan-runner/references/conduct.md` e `plan-template.md`, `notes-checker/SKILL.md`, `close-task/SKILL.md`,
  `core/work/README.md`, `core/plans/README.md` e `README.md`: REV/MIG, refs, campos, ls e gatilho da R12.3.
- [ ] Conferir revisão independente, core sem client e coerência entre norma/checador/CLI; atualizar fixtures golden.
- [ ] Rodar hooks, commitar e registrar evidência/Executado.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/hooks
```

### P4 — Medição e nome de sessão são provados nas fontes atuais

Executa D10 e D5 · executor: sessão de implementação no `brza-workflow` · depende de P3.

Estimado: 2 h · Executado: — h

- [ ] Reproduzir entradas atuais em notas/código, branch de plano e conta configurada; registrar a sonda sem reescrever histórico.
- [ ] Acrescentar casos necessários em `tests/hooks/test_measure.py`, `test_measure_workstream.py` e testes CLI de sessão.
- [ ] Corrigir apenas falhas reproduzidas em `core/.claude/hooks/measure.py` e `bin/brza-note`; provar fallback de nome
  vazio e funcionamento com/sem client. Fonte nova de runtime volta à rodada antes de integrar.
- [ ] Rodar testes focais de medição e sessão, commitar a entrega necessária e registrar evidência/Executado.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/hooks -p 'test_measure*.py'
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli -p 'test_brza_note.py'
```

### P5 — O script migra um acervo de teste sem resíduos

Executa D4 e D8, usando D3/D7 · executor: sessão de implementação no `brza-workflow` · depende de P4.

Estimado: 3 h · Executado: concluído; horas não aferidas, sem estimativa retrospectiva.

- [x] Criar fixture de dois workstreams que prove bootstrap repetido/conflitante, mapa D4, H1, links cruzados,
  refs antigo inválido, remoção de date sem perder tags e worktree ausente.
- [x] Implementar `scripts/migrate_pln008.py` com prévia padrão e aplicação explícita por workstream; reutilizar extrator e reserva.
- [x] Provar que prévia não commita e a segunda aplicação não muda bytes nem acrescenta eventos desnecessários.
- [x] Integrar os casos à suíte CLI, rodá-la, commitar e registrar evidência/Executado.

Evidência de 2026-11-03: commit `a666e78` no `brza-workflow`, com `scripts/migrate_pln008.py` e
`tests/cli/test_migrate_pln008.py`. A suíte focal passou com 10 testes; a suíte CLI completa passou com 467 testes em 169,983 s.
Ambas rodaram com `TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1`, usando fixtures locais, sem migração real nem push de P5.
Refs explícitos inválidos são recusados antes de reservas/escritas; a MIG nasce aberta, sem datas históricas inferidas
nem conclusão automática. Trabalho alheio fora dos caminhos da entrega foi preservado.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli
```

### P6 — Publicar, sincronizar e aplicar a MIG no acervo

Executa D1 a D10 · executores: sessão do `brza-workflow` publica; sessões donas dos workstreams aplicam nas notas;
sessão principal consolida evidências · depende de P5.

Estimado: 2 h · Executado: — h

- [x] Rodar as três suítes completas da Regressão, publicar a entrega e levar a norma por `brza sync`/`brza note sync`.
- [ ] Produzir e conferir a prévia no acervo atual; só então aplicar o bootstrap e criar MIG-001 no molde aprovado.
- [ ] Aplicar o mapa REV, links e backfill em cada workstream; concluir MIG-001 pelo comando que prova os quatro
  nomes novos, os antigos ausentes e links resolvidos. Registrar mudanças fora dos repositórios no worklog quando houver.
- [ ] Rodar checador em cada árvore e rebuild duas vezes, comprovando idempotência; commitar por caminhos pelo
  `brza note commit` nas sessões donas e registrar commits, comandos/resultados e Executado neste plano.

Evidência parcial de P6 em 2026-11-03: `brza-workflow@a666e78` já publicado; CLI completa (467 testes em
199,593 s), hooks completos (288 em 21,128 s) e notes-checker (26 casos) passaram, com
`TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1`. `brza-sync --ref a666e78` publicou `brza-workspace@5dcc2b3` e levou a norma
às cinco árvores. `brza-note index --bootstrap-pln008` reservou REV-001 a REV-004 e MIG-001 em `4bb114e`.
Prévia: quatro renomeações e 97 worklogs (29 tools-kit, 21 workspace, 4 brand, 43 studio); playground sem mudanças.
Revisão prévia exige prova da preservação dos campos além de refs/date; destino em rodada antes da aplicação.
P6 ainda não concluído; horas não aferidas.

### P7 — Revisar a entrega e fechar o plano

Executa D1 a D10 · executores: revisor independente e sessão principal · depende de P6.

Estimado: 2 h · Executado: — h

- [ ] Revisor independente confere Pedido/Cobertura contra disco e evidências; devolve achados com fonte e confiança.
- [ ] Sessão principal refaz evidências, conduz rodadas de destino e grava parecer REV numerado.
- [ ] Rodar regressão final pertinente, registrar evidências/Executado e dar destino a todo achado.
- [ ] Fechar o worklog e o plano quando os itens de Fechamento forem verdadeiros; nenhum achado aberto é ocultado.

## Regressão

- Preservar plan-open e sua corrida, remote do manifesto, commit só dos caminhos pedidos e checkout sujo;
  provas em `tests/cli/test_brza_note.py` e `test_brza_note_index.py`.
- Preservar IDs após rename e `--no-push` sem gravação no índice; conferir nas mesmas suítes CLI.
- Preservar core sem client, renderização golden e medição corrente; conferir hooks e fixtures sem ampliar exceções.
- Não reescrever histórico ou inventar campos ausentes; conferir diff da prévia e segunda aplicação do script.

Suítes completas na raiz do `brza-workflow`, na integração e conforme o que a revisão exigir:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/hooks
```

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/notes-checker/run.py
```

No workspace e nos worktrees de notas afetados:

```bash
python3 .claude/skills/notes-checker/scripts/check_notes.py
```

## Revisões

- [REV-005: A revisão prévia da MIG-001 em P6 do PLN-008](../../work/reviews/REV-005-pln-008-p6-previa-da-mig-001.md) — prévia de P6; três destinos em rodada; não substitui P7.

## Worklogs

- 2026-11-03 — P6 iniciado: regressão, sync e bootstrap feitos; migração real aguarda revisão prévia.
  [O início de P6 do PLN-008: regressão, sincronização e reservas](../../work/worklogs/2026-11-03-pln-008-p6-regressao-sync-e-reservas.md)

- 2026-11-03 — P5 entregue em fixture; P6/P7 pendentes; horas e identidade histórica exigem reconciliação.
  [A conclusão de P5 do PLN-008 em acervo de teste](../../work/worklogs/2026-11-03-pln-008-p5-migracao-em-fixture.md)

- 2026-11-03 — aberto; R1 a R6 fecharam a Entrevista; parou antes do Terreno.
  [A abertura do PLN-008: o refs nos worklogs, o REV e o MIG](../../work/worklogs/2026-11-03-pln-008-a-abertura-do-refs-do-rev-e-do-mig.md)
- 2026-11-03 — retomada; R7 a R13 respondidas; D1 a D10 e corte P1–P7 aceitos; execução aguarda pedido de P1.
  [O Terreno do PLN-008 para o Desenho](../../work/worklogs/2026-11-03-pln-008-o-terreno-para-o-desenho.md)
- 2026-11-03 — tentativa de execução integral até o fim do plano; problemas e desvios registrados em 3 issues.
  [Desvios e bloqueios na execução dos passos do PLN-008](../../work/worklogs/2026-11-03-pln-008-desvios-e-bloqueios-na-execucao-dos-passos.md)

## Fechamento

- [ ] P1 a P7 feitos com evidência/Executado ou descartados com motivo; horas reconciliadas.
- [ ] Todo achado tem destino existente; parecer numerado e apontado pelo plano.
- [ ] Norma durável entregue no core, sincronizada e documentada nos commits do `brza-workflow`.
- [ ] MIG-001 concluída e acervo conferido em todos os workstreams afetados.
- [ ] Resumo da entrega com link do plano nos commits; worklog final gravado.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
