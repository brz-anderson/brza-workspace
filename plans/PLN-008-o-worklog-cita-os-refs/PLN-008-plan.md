---
status: in_progress
phase: execution
origin: request
description: O brza note commit preenche o refs do worklog com os IDs que ele cita, e revisão e migração ganham REV-NNN e MIG-NNN
ready: sim
estimate_h: 23.5
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

- **Retomar:** P8 quase feito. A parte da R14 e o D11 estão publicados e conferidos; falta o `brza-studio` corrigir o
  autor do commit e mesclar a branch dos 3 testes (R18.1), pela sessão `d11-brza-studio`. Depois, a regressão final e
  o Fechamento, com a rodada das horas.
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

"remover citações a [o workspace de origem] de todos os repos brza-*" — Anderson, em 2026-11-03, na sessão `workspace-a6`, na R15.1,
com o alcance "Tudo, inclusive código" (R15.2).

6. os arquivos atuais dos repositórios `brza-*` não citam o workspace de origem (D11).

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
| `R14.1` | checador avisa parecer fora de REV-NNN e MIG incoerente com type, sem barrar | P8 | três casos de aviso e um de nota correta (notes-checker) |
| `R14.2` | norma lista só PLN, MIG e issue em depends_on | P8 | conferir `core/work/README.md` e `plan-template.md` contra o checador (revisão documental) |
| `R14.3` | ID só no texto do link não entra no refs, nas duas cópias do extrator | P8 | caso da tabela do D3 em `run.py` e na CLI; bloco 2 da MIG-001 com 0 nas cinco árvores (unidade e integração) |
| `Pedido 6` | nenhum arquivo atual dos repositórios `brza-*` cita o workspace de origem, salvo o índice; a guarda do `brza init` continua | P8 | um grep sem diferenciar caixa pelo nome do workspace de origem, lido do arquivo da máquina da guarda do `brza init`, vazio nas cinco branches, na master, no `brza-workflow` e no `brza-studio`; teste do `FOREIGN` com o arquivo da máquina (unidade e integração) |

### Fora de escopo

- **Os IDs em `tags`, como na proposta.** Ficou o campo `refs:` (R1.1); o `tags` segue só para assunto, no vocabulário
  fechado do checador.
- **Uma pasta `work/migrations/` e o MIG como plano.** Perderam na R3.2.
- **`session_id`, runtime, conta e modelo no frontmatter.** Ficam na medição e no `brza sessions` (R4.1).

## Pendências conhecidas

- [O refs grava o slug novo quando o commit renomeia a issue](../../work/issues/o-refs-grava-o-slug-novo-quando-o-commit-renomeia-a-issue.md) — achado do P8, R18.2.
- [O extrator do refs tem duas cópias sem teste de paridade](../../work/issues/o-extrator-do-refs-tem-duas-copias-sem-teste-de-paridade.md) — A5 da REV-006.
- [O núcleo guarda o bootstrap da migração do PLN-008](../../work/issues/o-nucleo-guarda-o-bootstrap-da-migracao-do-pln-008.md) — A7 da REV-006.
- [MIG-001: Renumeração dos pareceres REV-001..REV-004 e backfill de refs nos worklogs](../../work/issues/MIG-001-renumeracao-rev-e-refs-pln-008.md) — concluída em 2026-11-03.
- [A fronteira de execução e o acesso ao brza-workflow no Antigravity](../../work/issues/fronteira-de-execucao-e-acesso-ao-brza-workflow-no-antigravity.md)
- [Bloqueio de P6 e P7 sem a entrega publicada de P1 a P5 e sincronização do core](../../work/issues/bloqueio-de-p6-e-p7-sem-entrega-e-sync-do-core.md) — resolvida em 2026-11-03 (A6 da REV-006).
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

Corte aceito em 2026-11-03, R13: sete entregas e 18 h estimadas; a R14 acrescentou o P8, com 2,5 h, e a R16 o ampliou para 5,5 h. P5 está entregue com evidência abaixo. Existem commits
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

Estimado: 2 h · Executado: concluído; horas não aferidas.

- [x] Rodar as três suítes completas da Regressão, publicar a entrega e levar a norma por `brza sync`/`brza note sync`.
- [x] Produzir e conferir a prévia no acervo atual; só então aplicar o bootstrap e criar MIG-001 no molde aprovado.
- [x] Aplicar o mapa REV, links e backfill em cada workstream; concluir MIG-001 pelo comando que prova os quatro
  nomes novos, os antigos ausentes e links resolvidos. Registrar mudanças fora dos repositórios no worklog quando houver.
- [x] Rodar checador em cada árvore e rebuild duas vezes, comprovando idempotência; commitar por caminhos pelo
  `brza note commit` nas sessões donas e registrar commits, comandos/resultados e Executado neste plano.

Evidência parcial de P6 em 2026-11-03: `brza-workflow@a666e78` já publicado; CLI completa (467 testes em
199,593 s), hooks completos (288 em 21,128 s) e notes-checker (26 casos) passaram, com
`TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1`. `brza-sync --ref a666e78` publicou `brza-workspace@5dcc2b3` e levou a norma
às cinco árvores. `brza-note index --bootstrap-pln008` reservou REV-001 a REV-004 e MIG-001 em `4bb114e`.
Prévia: quatro renomeações e 97 worklogs (29 tools-kit, 21 workspace, 4 brand, 43 studio); playground sem mudanças.
Revisão prévia em REV-005: A1 e A2 corrigidos na MIG-001, A3 falso, por rodada de 2026-11-03. Ensaio em clone
isolado (`/private/tmp/pln008-sandbox`): seis passagens de `migrate_pln008.py --apply` na ordem da MIG saíram com 0, e
os três blocos do critério passaram, o de preservação com 107 notas (98 worklogs); um commit mutante sem `tags` foi
barrado. Aplicação real em 2026-11-03: `tools-kit` em `bf36704` (prévia igual ao ensaio; segunda passagem zerada) e
`workspace` em `361d0d4` (REV-002 a REV-004, 22 worklogs); checador sem erros nas duas árvores; bloco de preservação
restrito a elas: 60 notas, 51 worklogs. Depois, `brand` em `0e80b71`, `studio` em `d5abc5e` e `playground` sem
mudança, cada um pela sessão dona, com checador sem erros. Conclusão: os três blocos do critério da MIG-001 saíram com
0 nas cinco árvores (preservação em 107 notas, 98 worklogs); dois `brza note index --rebuild` seguidos responderam "em
dia, nada a acrescentar", com a master parada em `e8606a4`. MIG-001 `done`. P6 concluído; horas não aferidas.

### P7 — Revisar a entrega e fechar o plano

Executa D1 a D10 · executores: revisor independente e sessão principal · depende de P6.

Estimado: 2 h · Executado: — h

- [x] Revisor independente confere Pedido/Cobertura contra disco e evidências; devolve achados com fonte e confiança.
  Ponto a conferir, por escolha de Anderson em 2026-11-03 ("Achado para P7 (Recomendado)"): o checador não avisa
  parecer novo sem `REV-NNN` em `work/reviews/`; três do PLN-009 no `tools-kit` nasceram assim, um deles depois do sync.
  Outro ponto, por escolha de Anderson em 2026-11-03 ("Ponto para P7"): ID no texto de link entra no `refs`, como o
  D3 conta, e o intervalo "REV-001..REV-004" marca só as pontas (worklogs da MIG-001 em `brand` e `playground`).
- [x] Sessão principal refaz evidências, conduz rodadas de destino e grava parecer REV numerado.

Evidência de 2026-11-03: subagente `reviewer` isolado, em `brza-workflow@7a18392`; `tests/cli` 468 OK em 177,9 s sem a
`BRZA_WORKSPACE`, `tests/hooks` 288 OK, notes-checker 26 casos, `scripts/brza/tests` 98 OK, checador sem erros nas
cinco árvores e os três blocos da MIG-001 com 0. Oito achados e quatro falsos; a sessão refez a evidência de A1, A2,
A3 e A6. R14 deu os destinos: A1, A2 e A4 corrigidos no P8; A5 e A7 em issues; A6 fechada aqui (as duas issues ficaram
`done`); A3 e A8 descartados. Parecer em REV-006.
- [ ] Rodar regressão final pertinente, registrar evidências/Executado e dar destino a todo achado.
- [ ] Fechar o worklog e o plano quando os itens de Fechamento forem verdadeiros; nenhum achado aberto é ocultado.
  Depende do P8.

### P8 — O checador avisa a nota fora de número, a norma volta ao D2, o refs ignora o texto do link e o workspace de origem sai

Executa D7, D2 e D3, pela R14, e D11, pelas R15 e R16 · executores: sessões de implementação no `brza-workflow` e no
`brza-studio`; a sessão principal na master; as sessões donas dos cinco workstreams nas notas · depende do P7.

Estimado: 5,5 h · Executado: — h

Evidência parcial de 2026-11-03: `brza-workflow@30b3666`, pela sessão `pln008-p8`, com e-mail do `brz-anderson`.
Ele traz os três avisos (`review-without-number`, `migration-without-type`, `migration-type-without-number`), a norma
de `depends_on` de volta ao D2, o texto do link fora das duas cópias do extrator e um teste de paridade entre elas.
`tests/cli` deu 471 OK em 197,8 s, `tests/hooks` 288 OK e o notes-checker 99 verificações, tudo sem a `BRZA_WORKSPACE`.
O `brza sync --ref 30b3666` publicou `2130026` e levou a norma aos cinco workstreams. Desvio X1: a crase dentro do
texto de um link sai com ele, como o D3 da R14.3 manda. Com o extrator novo, o `refs` muda nos 4 worklogs previstos e
em dois do `workspace`, que ganhariam o PLN-011 do `studio` (R15).

- [x] Escrever os casos que falham antes em `tests/notes-checker/run.py` e na CLI: parecer sem `REV-NNN`, `MIG-NNN`
  sem `type`, issue `type: migration` sem número (aviso, não erro) e ID só no texto do link (sem referência).
- [x] Implementar o aviso em `check_notes.py` e tirar o texto do link da extração nas duas cópias, `bin/brza-note` e
  `check_notes.py`, que a issue da A5 aponta; tirar REV e `decision:` de `depends_on` em `core/work/README.md` e
  `plan-template.md`, e acrescentar o texto do link e os avisos à norma.
- [x] Rodar as três suítes da Regressão sem a `BRZA_WORKSPACE`, commitar, publicar e levar pelo `brza sync` e
  `brza note sync`.
- [x] D11 no `brza-workflow`: `FOREIGN` lendo arquivo da máquina, golden com a chave "origem", testes sem o nome do workspace de origem;
  suítes, commit, publicação e sync.
- [ ] D11 no `brza-studio`: os 3 testes com dados neutros, pela norma de lá.
- [x] D11 na master: `README.md` e `.claude/rules/workspace.md` neutros.
- [x] D11 nas notas: cada sessão dona troca as citações ao workspace de origem por termo neutro no próprio workstream.
- [x] No mesmo commit, recomitar os worklogs cujo `refs` muda: o da MIG-001 em `brand`, `studio` e `playground`, o do
  `tools-kit` com PLN-001 e os dois do `workspace` já sem o ID do plano do workspace de origem. Depois, o bloco 2 do critério da MIG-001
  sai com 0 nas cinco árvores, e a prova do D11, o grep pelo nome do workspace de origem, sai vazia.
- [ ] Registrar commits, comandos, resultados e Executado neste plano.

Evidência do D11, em 2026-11-03:
- **`brza-workflow@ebb4e7d`**, pela sessão `d11-brza-workflow`, com o e-mail do `brz-anderson`: 18 arquivos; a guarda lê
  `~/.config/brza/foreign.txt`, criado nesta máquina. Suítes sem a `BRZA_WORKSPACE`: CLI 483 OK em 197,9 s, hooks 291
  OK, notes-checker 99 checagens e `tests/mcp` 358 OK. Desvio X2: o arquivo que existe e não se lê é recusado, aceito
  na R18.3. O sync `8098514` levou a norma aos cinco workstreams.
- **Master:** `bc4f5ba` deixou o `README.md` e a regra local neutros, e o `brza note sync` a levou às branches.
- **Notas:** `tools-kit` em `9a40746`, `ffc0cf7` e `e3fd4d2` (a segunda passagem nos links); `studio` em `3297189`;
  `brand` em `2c18797`; `playground` em `e271921`; `workspace` em `835f023`. Nove arquivos foram renomeados pelo mapa,
  e os worklogs do `refs` ganharam novo commit nos mesmos commits.
- **Conferência:** o grep pelo nome do workspace de origem não acha nada nos arquivos atuais das cinco branches, da
  master e do `brza-workflow`, salvo o índice e as identidades da R17.1. O checador dá 0 erros nas cinco árvores, e os
  três blocos do critério da MIG-001 saem com 0 com o extrator novo.
- **Pendente:** o `brza-studio`. A branch `test/pln-008-d11-dados-neutros` (`a6ef12c`) passou com os 3 testes
  neutros, mas saiu com o e-mail noreply e sem merge; na R18.1, Anderson escolheu "Corrigir autor e mesclar
  (Recomendado)".
- **Observação:** um ID citado em prosa entra no `refs` mesmo quando a frase diz que ele saiu, como o D3 manda; duas
  sessões precisaram reescrever o próprio worklog por isso.

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

- [REV-005: A revisão prévia da MIG-001 em P6 do PLN-008](../../work/reviews/REV-005-pln-008-p6-previa-da-mig-001.md) — prévia de P6; A1 e A2 corrigidos na MIG-001, A3 falso; não substitui P7.
- [REV-006: A entrega do PLN-008 contra o Pedido e a Cobertura](../../work/reviews/REV-006-pln-008-p7-a-entrega.md) — P7; A1, A2 e A4 no P8; A5 e A7 em issues; A6 fechada; A3 e A8 descartados; quatro falsos.

## Worklogs

- 2026-11-03 — P8: R14 publicada; o D11 pelas R15 a R18, em seis sessões e na master; falta o `brza-studio` mesclar.
  [O P8 do PLN-008: o checador, o refs e o termo neutro](../../work/worklogs/2026-11-03-pln-008-p8-o-checador-o-refs-e-o-termo-neutro.md)

- 2026-11-03 — P7: revisão independente, R14 com os destinos, REV-006 gravada e P8 acrescentado; aguarda pedido do P8.
  [A revisão da entrega do PLN-008 no P7](../../work/worklogs/2026-11-03-pln-008-p7-revisao-da-entrega.md)

- 2026-11-03 — P6 feito: regressão, sync e bootstrap; REV-005 com destinos; MIG-001 ensaiada, aplicada nas cinco
  árvores e concluída; dois pontos para P7.
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

- [ ] P1 a P8 feitos com evidência/Executado ou descartados com motivo; horas reconciliadas.
- [ ] Todo achado tem destino existente; parecer numerado e apontado pelo plano: REV-006 com destinos, falta o P8.
- [ ] Norma durável entregue no core, sincronizada e documentada nos commits do `brza-workflow`.
- [x] MIG-001 concluída e acervo conferido em todos os workstreams afetados.
- [ ] Resumo da entrega com link do plano nos commits; worklog final gravado.
- [ ] `status: done`, `phase: closed` e `completed` no frontmatter.
