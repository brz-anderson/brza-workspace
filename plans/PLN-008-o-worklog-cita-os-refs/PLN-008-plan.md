---
status: open
phase: design
origin: request
description: O brza note commit preenche o refs do worklog com os IDs que ele cita, e revisão e migração ganham REV-NNN e MIG-NNN
ready: não — extração de refs definida na R10; faltam renumeração, sessão no rebuild e demais contratos do Desenho
scope:
  - workspace
opened: 2026-11-03
owner: Anderson
tags:
  - tooling
---

# PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca

- **Retomar:** R10 fechou a extração do `refs:`: fora de cercas, preservando crases inline, links e citações
  históricas; menção textual desconhecida avisa e não entra no campo. D1 a D3 registram skill, dependências e refs.
  Próximo: mapear as quatro REV e definir sessão no rebuild; concluir os demais contratos e derivar os Passos.
- **Dividido:** [PLN-008 — Desenho](PLN-008-design.md)

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

> Rascunho: o passo e o teste saem do Desenho.

| Origem     | Critério de aceite                                                                                                   | Passo | Teste (nível) |
| :--------- | :------------------------------------------------------------------------------------------------------------------- | :---- | :------------ |
| `Pedido 1` | o `brza note commit` grava no `refs:` de cada worklog os IDs que o corpo linka ou cita, sem ninguém escrever à mão     | —     | —             |
| `Pedido 1` | o checador barra o `refs:` com ID que não existe em nenhum workstream                                                  | —     | —             |
| `Pedido 1` | os worklogs que existem ganham o `refs:` por um preenchimento automático                                               | —     | —             |
| `Pedido 2` | toda revisão de `work/reviews/` tem `REV-NNN`, numerado em sequência pelo índice, e as 4 de hoje são REV-001 a REV-004 | —     | —             |
| `Pedido 3` | a migração é issue `type: migration`, `work/issues/MIG-NNN-<assunto>.md`, com o molde da R3.3, e a MIG-001 é a renumeração das revisões | — | — |
| `Pedido 4` | a única `migration-runner` cria, revisa e executa a MIG até o critério de conclusão, com revisor independente (R8.1) | — | — |
| `Pedido 4` | a revisão nasce com o `REV-NNN` pela skill que a escreve, a `plan-runner` em `references/conduct.md` | — | — |
| `R4.1` | toda linha do `measurements.jsonl` dentro de um worktree tem `workstream`, a conta não sai `home`, e o `session` do índice resolve sempre que a sessão tem nome | — | — |
| `R4.2` | o `brza note commit` avisa, sem barrar, a issue ou o plano aberto sem `priority` | — | — |
| `R4.3` | a linha do índice grava `priority`, `blocks`, `deadline`, `owner`, e no plano `estimate_h` e `remaining_h`; o `index --rebuild` refaz as antigas | — | — |
| `R5.2` | a issue aceita `estimate_h` opcional, e o índice a grava | — | — |
| `R5.3` | os worklogs perdem o `date`, mantêm o `tags`, e o checador avisa o `date` | — | — |
| `R6.1` | o `brza note ls` lista issues e decisões de todos os workstreams, pelo índice, ordenadas por `opened`, `priority` ou `deadline` | — | — |
| `R7.2` | planos e issues aceitam `depends_on` opcional, também gravado no índice | — | — |
| `R9.1` | só `done` satisfaz uma dependência; `dropped` exige revisão explícita da relação | — | — |
| `R9.2` | o checador barra dependência com alvo inexistente, autorreferência ou ciclo, inclusive entre workstreams | — | — |
| `R10` | refs é extraído fora de cercas, preserva crases inline, links e citações históricas; menção textual desconhecida avisa sem entrar no campo | — | — |

### Fora de escopo

- **Os IDs em `tags`, como na proposta.** Ficou o campo `refs:` (R1.1); o `tags` segue só para assunto, no vocabulário
  fechado do checador.
- **Uma pasta `work/migrations/` e o MIG como plano.** Perderam na R3.2.
- **`session_id`, runtime, conta e modelo no frontmatter.** Ficam na medição e no `brza sessions` (R4.1).

## Entrevista

### Rodada 1 — a forma e o MIG (enviada 2026-11-03)

**Apresentado antes:** o `tags` já existe, num vocabulário fechado de 7 assuntos (`check_notes.py:39`), e a norma diz
que "tag nunca espelha campo nem caminho" e "é atalho, nunca inventário: com preenchimento opcional, buscar por tag mente
por omissão" (`work/README.md`, "As propriedades"). O plano já cita o worklog no `## Worklogs`, e o checador avisa a
falta (`plans/README.md:40`); falta o sentido do worklog para o plano. O `studio` preencheu `tags` em 39 de 45
worklogs, o `tools-kit` em 0 de 29. O `MIG-001` só aparece como exemplo de título de sessão
(`workstream/tools-kit:plans/PLN-002-os-comandos-brza/PLN-002-plan.md:49`), e a revisão não tem ID. O `work/README.md`
e o checador são norma comum (`.brza/core.lock:34`), editada no `brza-workflow`.

Respondida em 2026-11-03, na sessão `workspace`.

1. **A forma.** Opções:
   - `refs:` preenchido sozinho pelo `brza note commit`, a partir dos links e dos IDs do corpo, com o checador
     conferindo a existência (recomendada) — custo: ~3 h no `brza-workflow` e um script para os 97 worklogs; se paga:
     na primeira busca entre workstreams, sem omissão;
   - `refs:` à mão — custo: ~1,5 h; se paga: só enquanto todos preencherem;
   - em `tags`, como proposto — custo: ~1,5 h e reescrever a regra da tag; se paga: agora, mas a busca mente por
     omissão;
   - sem campo, um `brza note related <ID>` — custo: ~2 h; se paga: na primeira busca, sem a relação na nota.

   **Decidido — "refs: preenchido sozinho (Recomendado)".**

2. **O que é o MIG-001.** Opções:
   - só os IDs que existem (recomendada) — custo: 0; se paga: agora;
   - um gênero `MIG-NNN` novo — custo: ~3–4 h e uma rodada sobre o que é migração; se paga: só com várias migrações
     fora de plano;
   - `REV-NNN` e `MIG-NNN` — custo: ~5–6 h e renomear as revisões; se paga: só se as revisões forem citadas por ID.

   **Decidido — "REV-NNN e MIG-NNN".** A definição e o lugar do MIG vão à R2.1.

### Rodada 2 — o lugar do MIG, o REV e o veículo (enviada 2026-11-03)

**Apresentado antes:** são 4 revisões (3 no `workspace`, 1 no `tools-kit`); "migração" apareceu como mudança de
estrutura do workspace (o P8 do PLN-006) e como migração de configuração do app (a R48.4 do PLN-001).

Respondida em 2026-11-03, na sessão `workspace`.

1. **Onde mora a MIG-NNN.** Opções: plano com prefixo MIG, no molde do PLN, com "Como desfazer" (recomendada) — custo:
   ~3 h; se paga: na primeira migração; pasta `work/migrations/` — custo: ~3–4 h; se paga: só com migrações curtas;
   só rótulo — custo: ~1 h; se paga: agora, mas o `refs` aponta para ID sem arquivo.

   **Resposta:** "Verifique como funciona migrations/ de fixfy_flutter e flutter-template e abra dois subagentes em
   paralelo, um que defenda sua recomendação e um que rebata sua recomendação". Leitura: o lugar volta à rodada depois
   do levantamento e dos dois consultores — vai à R3.

2. **O REV nas 4 revisões existentes.** Opções: renumerar as 4 com o `move_note.py` (recomendada) — custo: ~30 min; se
   paga: agora; só as novas — custo: 0; se paga: agora, com dois formatos de ID.

   **Decidido — "Renumerar as 4 (Recomendado)".**

3. **O veículo.** Opções: abrir um PLN aqui (recomendada) — custo: ~20 min; se paga: na segunda sessão; issue e depois
   — custo: ~10 min; se paga: quando alguém pegar; fazer agora — custo: ~8–10 h nesta sessão; se paga: hoje, contra a
   norma.

   **Decidido — "Abrir um PLN aqui (Recomendado)".** Este plano.

### Rodada 3 — o MIG (enviada 2026-11-03)

**Apresentado antes:** no `flutter-template` e no `fixfy_flutter`, a migração é a "divergência entre o código em disco
e a norma em vigor", numa pasta permanente, um arquivo numerado por migração, com tabela de origem, urgência,
dependência e status; tem o tamanho de um commit ou PR, aponta um plano pelo campo `Plano:` e **sai do diretório** ao
concluir (`flutter-template/docs/migrations/README.md`; `fixfy_flutter/docs/migration/README.md`). Dois consultores
`designer` em paralelo:
- **a defesa** do MIG como plano: a migração real do brza foi trabalho de plano (o D12 do PLN-006, com a volta
  escrita); o molde do PLN já tem Terreno, Cobertura e Regressão; a fila são as issues; `kind: plan` com id `MIG-NNN`
  no índice; acrescentar "Como desfazer" e um comando que prova o fim;
- **o ataque:** a definição "mudança com antes e depois" faz o MIG competir com o PLN; o caso real foi passo de plano
  (P8 do PLN-006, P58 do PLN-001); ensinar `MIG` ao código do PLN, fixo em 24 arquivos do `brza-workflow`, custa 5–7 h;
  a contraproposta é a fila `work/migrations/`, e a MIG-001 a renumeração das revisões.

Os dois concordaram: a migração concluída fica, com `status: done` (`work/README.md:80`, `plans/README.md:34`), e a
`migration-writer` da Fixfy não serve aqui (`work/worklogs/2026-10-31-o-porte-das-skills-da-fixfy.md:24`). A síntese
apresentada: a definição do ataque, no lugar da fila que a defesa apontou, a issue.

Respondida em 2026-11-03, na sessão `workspace`.

1. **A definição.** Opções: divergência entre o disco e uma norma ou decisão em vigor, e a migração que é passo de
   plano maior segue passo (recomendada) — custo: 0; se paga: agora; mudança com antes e depois, com tabela do que não
   é MIG — custo: 0 e a tabela; se paga: só se a tabela segurar a fronteira.

   **Decidido — "Divergência disco × norma (Recomendado)".**

2. **O lugar.** Opções: issue `type: migration`, `work/issues/MIG-NNN-<assunto>.md`, que herda `priority`, `blocks`,
   `deadline` e a fila do coordenador e aponta um PLN quando precisa (recomendada) — custo: ~1,5–2 h e dois padrões de
   nome nas issues; se paga: na MIG-001; pasta `work/migrations/` com `kind: migration` — custo: ~2–3 h e a decisão de
   pasta nova; se paga: só com fila própria; plano com prefixo MIG — custo: ~3 h pela defesa, 5–7 h pelo ataque; se
   paga: só com migração que peça entrevista e desenho próprios.

   **Decidido — "Issue type: migration (Recomendado)".**

3. **O molde.** Opções: sempre Estado-alvo, Estado atual, Passos e Critério de conclusão com o comando que prova o fim,
   e "Como desfazer" só quando a mudança sai do git (recomendada) — custo: ~0,3 h; se paga: na primeira migração com
   resíduo; "Como desfazer" sempre — custo: a seção vazia nas migrações de notas; se paga: só se a maioria sair do git;
   só o molde do template — custo: ~0,2 h; se paga: agora, sem a volta escrita.

   **Decidido — "Conclusão sempre, volta às vezes (Recomendado)".**

4. **A MIG-001.** Opções: a renumeração das 4 revisões (recomendada) — custo: ~0,3 h; se paga: agora, testando o
   molde; passo do PLN — custo: 0; se paga: agora, sem caso real.

   **Decidido — "Sim (Recomendado)".**

### Rodada 4 — o frontmatter para o coordenador (enviada 2026-11-03)

**Apresentado antes:** o levantamento de um `collector` nas 4 branches `workstream/*`: 8 planos, 32 issues, 93
worklogs, 5 decisões e 4 revisões; nenhuma nota com `blocks` nem `deadline`, e `priority` em 8 de 32 issues (conferido
por `git grep`). O índice da `master` grava `ts`, `event`, `kind`, `id`, `path`, `title`, `description`, `status`,
`workstream`, `worktree`, `commit`, `phase` (só plano) e `session`, o nome da sessão, em 14 de 50 linhas
(`brza-workflow/bin/brza-note:524-551`). A medição já guarda, por turno, `session_id`, `cwd`, `workstream`, conta,
modelo e esforço, mas o `workstream` é nulo em 176 de 573 turnos e a conta sai `home` (`measure.py:84-87`; o M16 do
PLN-003); o `brza sessions list` dá o runtime pelo prefixo do id. A recomendação: o frontmatter guarda o que se julga e
o que liga as notas, e o fato da execução fica na medição.

Respondida em 2026-11-03, na sessão `workspace`.

1. **`session_id`, runtime, conta e modelo no frontmatter.** Opções: não, e consertar as fontes — o `workstream` nulo,
   a conta `home` e o `session` do índice (recomendada) — custo: ~2–3 h, estimado; se paga: no primeiro dia da fila;
   `session_id` no worklog — custo: ~1 h e um id que troca no `/clear`; se paga: só se a retomada pelo id exato virar
   requisito; todos no frontmatter — custo: ~2 h e cópias que envelhecem; se paga: nunca.

   **Decidido — "Não; consertar as fontes (Recomendado)".**

2. **O preenchimento de `priority`, `blocks` e `deadline`.** Opções: aviso no `brza note commit`, e a ausência vai ao
   fim da fila (recomendada) — custo: ~0,5 h; se paga: na primeira semana da fila; o checador barra — custo: ~0,5 h e
   atrito; se paga: só depois que a omissão atrapalhar; nada muda — custo: 0; se paga: nunca.

   **Decidido — "Aviso no commit (Recomendado)".**

3. **Os campos do índice.** Opções: os três decididos, `owner` e as horas do plano, com o `index --rebuild`
   (recomendada) — custo: ~1,5 h, estimado; se paga: no primeiro plano despachado; só os três — custo: ~1 h; se paga:
   agora, com o coordenador abrindo o plano para as horas.

   **Decidido — "Os 3 + owner e horas (Recomendado)".**

4. **O destino.** Opções: o PLN-008 (recomendada) — custo: ~4–5 h a mais, estimado; se paga: agora, com um desenho só;
   o PLN-003 — custo: um pedido ao `tools-kit` e dois planos no mesmo `brza-note`; se paga: só se a fila vier antes; um
   PLN novo — custo: ~20 min e um terceiro plano; se paga: só se o PLN-008 tiver de fechar logo.

   **Decidido — "No PLN-008 (Recomendado)".** É o item 5 do Pedido.

### Rodada 5 — dependência, estimativa e os worklogs do studio (enviada 2026-11-03)

**Apresentado antes:** os três pontos restantes do mesmo levantamento.

Respondida em 2026-11-03, na sessão `workspace`.

1. **A dependência.** Opções: esperar o `refs:` e decidir `depends_on` no Desenho daqui (recomendada) — custo: 0;
   se paga: no Desenho; `depends_on` agora — custo: ~1 h e duplica `blocks` e `refs`; se paga: só se o `refs` não
   cobrir; o agente do M11 lê `blocks` — custo: chamada e erro de prosa; se paga: nunca.

   **Decidido — "Esperar o refs (Recomendado)".** A escolha no Desenho foi respondida em R7.2.

2. **A estimativa na issue.** Opções: só no plano (recomendada) — custo: 0; se paga: agora, mas o teto não vê a issue
   sem plano; opcional na issue — custo: ~0,3 h no checador e no índice; se paga: só se a issue que vira tarefa direta
   for frequente.

   **Decidido — "Opcional na issue".**

3. **Os 40 worklogs do studio com `date` e `tags`.** Opções: tirar o `date` e manter o `tags`, com o checador avisando
   (recomendada) — custo: ~0,3 h de script; se paga: quando o coordenador consultar por data; só o `scope` — custo: o
   mesmo; se paga: nunca; deixar como está — custo: 0; se paga: agora, com duas formas.

   **Decidido — "Tirar o date, manter tags (Recomendado)".**

### Rodada 6 — a data no nome de issues e decisões (enviada 2026-11-03)

**Apresentado antes:** Anderson perguntou: "E se issues/ e decisions/ começarem a levar a data como prefixo no nome do
arquivo, pode ajudar?". A chegada já está no `ts` da linha `created` do índice e no `opened` (32 de 32 issues, 5 de 5
decisões); o id do índice é o slug da criação, que o rename não muda (`brza-workflow/bin/brza-note:61-62`); renomear
atinge 37 notas, 95 links nas 4 branches e o `origin_ref` dos planos (`check_notes.py:286`); a decisão tem duas datas,
`opened` e `decided`.

Respondida em 2026-11-03, na sessão `workspace`.

1. **A data como prefixo.** Opções: não, e um `brza note ls` que lista issues e decisões por `opened`, `priority` ou
   `deadline`, lendo o índice (recomendada) — custo: ~1 h, estimado; se paga: na primeira busca pela mais recente ou
   pela mais urgente; só nas novas — custo: ~0,5 h, dois padrões de nome e a data no id; se paga: só para o `ls`;
   renomear todas — custo: ~1,5–2 h, 95 links, o `origin_ref` e o id descolado do nome; se paga: nunca para o
   coordenador.

   **Decidido — "Não; listar pelo opened (Recomendado)".**

### Rodada 7 — skills, dependências e identidade das issues (enviada 2026-11-03)

**Apresentado antes:** o Terreno mostrou que o índice já preserva `issue:<slug>` no rename; `refs:` informa relação
temática, sem direção de dependência; a revisão substantiva exige revisor independente, enquanto o checador confere
a forma. Os custos apresentados contam alterações propostas, sem estimativa de horas.

Respondida em 2026-11-03, na sessão `workspace`: "7.1 só `migration-runner` / 7.2.1 / 7.3.1".

1. **As skills da MIG.** Opções:
   - três skills próprias, `migration-writer`, `migration-reviewer` e `migration-runner` (recomendada) — custo:
     três `SKILL.md` e um molde; se paga: na primeira MIG conduzida sem PLN;
   - duas novas e adaptar a `plan-runner` para revisar MIG — custo: dois `SKILL.md`, um molde e ampliação do fluxo
     de revisão; se paga: quando PLN e MIG compartilharem essa condução.

   **Resposta — "só `migration-runner`".** Contraproposta: uma única skill nova. A leitura de que ela reúne criação,
   revisão e execução volta para confirmação em R8.1, sem converter essa inferência em contrato aprovado.

2. **O `depends_on`.** Opções:
   - lista opcional em planos e issues, também no índice (recomendada) — custo: um campo nas notas e no índice,
     validação e documentação; se paga: quando o coordenador precisar distinguir referência de dependência;
   - concluir sem o campo — custo: nenhum campo novo, mas cada despacho dependente exige leitura dos
     pré-requisitos; se paga: agora, enquanto a fila depender dessa leitura.

   **Decidido — "7.2.1".** Entra no escopo; semântica e validação ainda vão ao Desenho.

3. **A issue comum no `refs:`.** Opções:
   - `issue:erro-na-retomada`, preservando a identidade do índice (recomendada) — custo: adotar a notação existente,
     com conversão automática dos links; se paga: na primeira referência entre workstreams;
   - `erro-na-retomada` — custo: conversão adicional para o ID do índice e regra para distinguir slug de prosa;
     se paga: apenas na leitura manual do campo.

   **Decidido — "7.3.1".** As issues comuns usam `issue:<slug>`; não ganham número nem renomeação.

### Rodada 8 — o escopo da única migration-runner (enviada 2026-11-03)

**Apresentado antes:** R7.1 pediu "só `migration-runner`". A confirmação separou a organização em uma única skill
do alcance das operações e preservou o revisor independente.

Respondida em 2026-11-03, na sessão `workspace`.

1. **A única migration-runner reúne as três operações?** Opções:
   - sim: criar, revisar e executar, com revisor independente (recomendada) — custo: uma skill com três operações
     e um molde; se paga: na primeira MIG completa, com uma única entrada;
   - só executar; criação e revisão ficam nas skills existentes — custo: uma skill nova e adaptação dos fluxos
     existentes para MIG; se paga: ao compartilhar esses fluxos com os planos.

   **Decidido — "sim".** Uma única `migration-runner` reúne criação, revisão e execução; a revisão usa revisor
   independente. Isso fecha a contraproposta de R7.1; não autoriza executar passos do plano.

### Rodada 9 — satisfação e validação de dependências (enviada 2026-11-03)

**Apresentado antes:** a norma distingue `done`, encerrado com desfecho, de `dropped`, encerrado sem desfecho por
escolha (`brza-workflow/core/work/README.md:207`). R7.2 já confirmou a presença do campo; esta rodada define as regras.

Respondida em 2026-11-03, na sessão `workspace`: "ambos recomendado".

1. **Quando uma dependência fica satisfeita?** Opções:
   - somente com `done` (recomendada) — custo: rever explicitamente a dependência quando o antecedente for
     abandonado; se paga: no primeiro cancelamento, evitando considerar entregue um pré-requisito abandonado;
   - com `done` ou `dropped` — custo: conferir o resultado antes de executar; a relação significa apenas aguardar
     encerramento; se paga: quando o trabalho puder continuar mesmo sem a entrega anterior.

   **Decidido — "ambos recomendado".** Somente `done` satisfaz; `dropped` exige revisar explicitamente a relação.

2. **Como tratar alvo inexistente, autorreferência e ciclos?** Opções:
   - erro no checador (recomendada) — custo: resolução dos IDs, percurso do grafo e correção antes do commit;
     se paga: na primeira referência errada ou circular;
   - aviso, permitindo o commit — custo: as mesmas verificações e tratamento posterior da pendência inválida;
     se paga: quando for necessário registrar dependências antes de criar suas notas.

   **Decidido — "ambos recomendado".** O checador gera erro para alvo inexistente, autorreferência e ciclo,
   inclusive entre workstreams.

### Rodada 10 — extração do refs (enviada 2026-11-03)

**Apresentado antes:** o filtro atual remove cercas e crases inline (`brza-workflow/core/.claude/skills/notes-checker/scripts/check_notes.py:145-153`).
Foi proposto preservar as crases e normalizar citações como `PLN-008/D1` para `PLN-008`.

Respondida em 2026-11-03, na sessão `workspace`: "ambos recomendado".

1. **De onde extrair as referências?** Opções:
   - prosa, crases inline, links e citações históricas, excluindo blocos cercados (recomendada) — custo: filtro de
     cercas que preserve crases inline; se paga: ao evitar que exemplos de código acrescentem referências;
   - incluir também os blocos cercados — custo: aceitar referências que aparecem apenas em exemplos; se paga:
     quando a única referência verdadeira estiver num comando cercado.

   **Decidido — "ambos recomendado".** Extrair fora de cercas, preservando crases inline, links e citações
   históricas. `PLN-008/D1` vira `PLN-008`; o refs aponta a nota, sem validar a existência do item D1.

2. **E uma menção textual a ID inexistente?** Opções:
   - avisar e não incluir no refs (recomendada) — custo: diagnóstico com ID e localização; se paga: no
     preenchimento dos worklogs antigos com exemplos hipotéticos, preservando o texto histórico;
   - gerar erro e impedir o commit — custo: corrigir cada ocorrência, inclusive exemplos históricos; se paga:
     quando a menção for um erro de digitação que esconderia uma referência real.

   **Decidido — "ambos recomendado".** Menção textual desconhecida gera aviso, sem entrar no refs. Nas duas opções,
   ID inexistente escrito no próprio refs e link relativo quebrado continuam erros.

## Worklogs

- 2026-11-03 — aberto; R1 a R6 fecharam a Entrevista; parou antes do Terreno.
  [A abertura do PLN-008: o refs nos worklogs, o REV e o MIG](../../work/worklogs/2026-11-03-pln-008-a-abertura-do-refs-do-rev-e-do-mig.md)
- 2026-11-03 — retomada; Terreno conferido; R7 a R10 respondidas; D1 a D3 registram skill, dependências e refs.
  [O Terreno do PLN-008 para o Desenho](../../work/worklogs/2026-11-03-pln-008-o-terreno-para-o-desenho.md)
