# PLN-008 — Desenho

## O que este desenho assume

As respostas das R1 a R6 estão no
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](PLN-008-plan.md).
Desenho e corte em sete passos aceitos na R13, em 2026-11-03. Além do Terreno, estão confirmados:

- **R7.2 e R9:** `depends_on` opcional em planos e issues, também no índice; só `done` satisfaz; alvo inexistente,
  autorreferência e ciclo geram erro no checador.
- **R7.3:** a issue comum aparece no `refs:` como `issue:<slug>`, preservando a identidade do índice.

- **R8.1:** uma única `migration-runner` reúne criação, revisão e execução, com revisor independente.
- **R10:** refs considera prosa, crases inline, links e citações históricas fora de cercas; menção textual
  desconhecida gera aviso sem entrar no campo.
- **R11.1:** as quatro revisões recebem REV-001 a REV-004 pela primeira inclusão no git.
- **R11.2:** `session` identifica a sessão que produziu a linha do índice, inclusive no rebuild.
- **R12, com emenda:** ls mostra abertos e `opened` recente primeiro, usando inicialmente o índice local;
  `--refresh` atualiza. Dados errados listados com frequência fazem fetch passar a ser o padrão.

## Terreno

Levantamento refeito em 2026-11-03. Os caminhos de código abaixo partem do `brza-workflow`.

- **O preenchimento precisa preceder a conferência.** `bin/brza-note:291-325` chama o checador antes do `git add`;
  o commit leva só os caminhos pedidos. Não existe preenchimento de `refs:` nessa sequência.
- **A numeração tem mecanismo reaproveitável.** `bin/brza-note:454-494,553-576` reserva PLN pelo índice, com nova
  leitura e até três tentativas de push; `bin/brza-note:515-523` reconhece plano, issue e decisão, sem revisão.
  A issue tem identidade `issue:<slug>`, e não um número próprio.
- **O índice precisa de mudanças em três lugares.** `bin/brza-note:497-550` lê escalares e grava título, descrição,
  estado e fase; não lê listas como o parser do checador. `INDEX_COMPARED`, na linha 107, também precisa acompanhar
  os campos novos. `opened` ainda falta, embora a R6.1 peça ordenação por ele.
- **A extração existente não serve diretamente ao refs.** O `check_notes.py`, em
  `core/.claude/skills/notes-checker/scripts/check_notes.py:145-175`, remove crases inline e blocos de código antes
  de extrair links. O coletor de IDs terá de tratar as citações em crases. O catálogo entre workstreams, nas linhas
  178-218, guarda caminhos, não identidades, e fixa o remote `origin`.
- **O nome de sessão exige cuidado no rebuild.** `bin/brza-note:155-169` consulta variável de ambiente, mapa do client
  e provedor. `bin/brza-note:539-549,654-661` grava no índice a sessão corrente inclusive quando reconstrói uma nota
  antiga; isso não recupera a autoria histórica dela.
- **O diagnóstico histórico da medição não basta para alterar o código atual.**
  `core/.claude/hooks/measure.py:110-113,596-615` já identifica a conta pelo diretório e resolve workstream pelo
  manifesto. A sonda no hook instalado retornou `workspace` e `.claude`; os arquivos instalados conferidos são
  iguais aos do core. As contagens antigas da R4 permanecem como histórico daquela rodada.

### Verificação desta retomada

- `python3 .claude/skills/notes-checker/scripts/check_notes.py`, no workspace: 44 arquivos, zero erros e avisos.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/hooks -p 'test_measure*.py'`, no
  `brza-workflow`: 36 testes passaram em 5,319 s.
- O collector também executou a suíte `test_brza_note_index.py`: 45 testes passaram.

### Limites da execução

Colisão real de IDs reservados e integração nova de runtime sem fonte disponível voltam à rodada com evidência.
O gatilho qualitativo da R12.3 foi preservado; não se inventa limiar.
Não houve implementação; o aceite do corte não autoriza executar os passos.

## D1 — Uma única migration-runner conduz a MIG — `core/.claude/skills/migration-runner/`

- **Origem:** Pedido 4; R3.1–R3.3; R7.1 e R8.1.
- **Contexto:** Anderson substituiu a proposta de skills separadas por uma única entrada e confirmou as três operações.

### Como fica

Uma skill `migration-runner`, com um molde MIG, oferece três operações:

| Operação | Contrato |
| :------- | :------- |
| Criar | Registrar a divergência entre disco e norma ou decisão vigente como issue `type: migration`, no molde da R3.3. |
| Revisar | Pedir parecer a revisor independente, com achados e evidências; a sessão principal conduz a rodada e grava o parecer REV. |
| Executar | Conduzir os passos autorizados, registrar evidências e conferir o comando do critério de conclusão. |

O molde contém Estado-alvo, Estado atual, Passos e Critério de conclusão; Como desfazer só aparece quando a mudança
sai do git (R3.3). A numeração MIG/REV e os comandos de abertura dependem dos demais itens do Desenho.

**Alternativas recusadas em R7.1/R8.1:** três skills separadas; duas novas mais revisão pela `plan-runner`;
`migration-runner` limitada à execução. A escolha mantém as três operações numa única entrada, preservando a
independência do revisor.

## D2 — Dependência exige entrega concluída — `core/work/README.md`, checador e índice

- **Origem:** R5.1; R7.2; R9.1 e R9.2; R14.2.
- **Contexto:** referências agrupam assuntos; dependências declaram pré-requisitos e não são inferidas das citações.

### Como fica

Planos e issues aceitam a lista opcional `depends_on`, também gravada no índice:

```yaml
depends_on:
  - PLN-003
  - MIG-001
  - issue:erro-na-retomada
```

| Condição do alvo | Resultado |
| :-------------- | :-------- |
| `status: done` | Dependência satisfeita. |
| `open`, `in_progress`, `in_review`, `dropped` ou estado ausente | Dependência não satisfeita; `dropped` exige rever explicitamente a relação. |
| Alvo inexistente | Erro no checador. |
| Autorreferência ou ciclo, inclusive entre workstreams | Erro no checador. |

A validação resolve os alvos e percorre o grafo na árvore atual e nas branches conhecidas. A falta de entrega é
dependência pendente, não erro de integridade: uma nota pode declarar dependência de outra ainda aberta.
O diagnóstico identifica o alvo inválido ou o caminho do ciclo.

Esta regra não autoriza execução nem substitui o `ready` do plano. O índice fornece a relação e o estado das notas;
o despacho do coordenador continua no PLN-003. Branches desatualizadas exigem nova validação após atualização;
o checador não garante impedir ciclos introduzidos simultaneamente em workstreams isolados.

Só PLN, MIG e `issue:` são alvos de `depends_on`. A norma comum (`core/work/README.md` e `plan-template.md`) lista
os mesmos três; REV e `decision:` saem dela, porque o checador os barra (R14.2).

**Alternativas recusadas em R9:** aceitar `dropped` como dependência satisfeita; permitir referências inválidas ou
ciclos com aviso. A escolha exige entrega e corrige a relação inválida antes do commit.

## D3 — O refs extrai as menções fora das cercas — `bin/brza-note` e checador

- **Origem:** R1.1; R7.3; R10.1 e R10.2; R14.3.
- **Contexto:** o filtro atual apaga crases inline, embora elas contenham citações reais; exemplos cercados podem
  mencionar IDs sem relação com o trabalho.

### Como fica

Antes de reescrever qualquer worklog solicitado, o `brza note commit` valida o `refs:` explícito atual contra notas
existentes. ID inexistente gera erro sem reescrita, para que o recálculo não esconda a referência inválida.
Depois extrai do corpo, confere os alvos e links e atualiza somente os caminhos pedidos, antes do checador completo.
A extração considera prosa, crases inline, o destino dos links e citações históricas, excluindo blocos cercados de
código e o texto dos links (R14.3): o link conta pelo alvo, e não pelos IDs do título que ele mostra.
O resultado é ordenado e sem duplicatas; sem referências, o campo é omitido. O preenchimento do acervo reutiliza
essa sequência e é idempotente.

| Entrada | Resultado |
| :------ | :-------- |
| `PLN-008/D1` fora de cerca | Referência `PLN-008`, sem validar o item D1. |
| `PLN-003` somente em bloco cercado | Não gera referência. |
| Link para issue comum existente | Referência `issue:<slug>` com a identidade do índice. |
| ID só no texto de um link, como o título "REV-001..REV-004" de outra nota | Não gera referência; o alvo do link gera. |
| Menção textual a ID inexistente | Aviso com ID e localização; não entra no refs. |
| ID inexistente no próprio refs | Erro no checador, conforme R1.1. |
| Link relativo quebrado fora de código | Continua erro no checador. |

PLN, REV e MIG mantêm seus IDs próprios. Uma citação histórica de ID existente entra no campo mesmo quando for
exemplo: refs representa menção, sem afirmar trabalho executado ou dependência.

**Alternativas recusadas em R10:** extrair também de cercas; bloquear toda menção textual desconhecida.
A escolha preserva o texto histórico e avisa sobre possíveis erros de digitação sem gravar alvos inexistentes.

## D4 — As quatro revisões recebem IDs em ordem cronológica — `work/reviews/`

- **Origem:** R2.2; R3.4; R11.1.
- **Contexto:** a ordem segue a primeira inclusão verificável no git, sem afirmar hora de redação ou autoria.

### Como fica

Cada caminho abaixo parte de `work/reviews/` no workstream indicado:

| Workstream | Arquivo atual | Arquivo após a MIG-001 |
| :--------- | :------------ | :-------------------- |
| tools-kit | `pln-002-os-comandos-brza.md` | `REV-001-pln-002-os-comandos-brza.md` |
| workspace | `pln-005-a-confianca-dos-fatos.md` | `REV-002-pln-005-a-confianca-dos-fatos.md` |
| workspace | `pln-006-o-brza-init.md` | `REV-003-pln-006-o-brza-init.md` |
| workspace | `pln-006-a-migracao.md` | `REV-004-pln-006-a-migracao.md` |

O H1 troca somente `REV:` pelo ID correspondente seguido de dois-pontos. A MIG-001 registra este mapa, usa
`move_note.py` e corrige os links nos workstreams donos; o mover de uma árvore não atualiza as demais.

**Alternativa recusada em R11.1:** ordenar por plano e nome atual, que inverteria os dois pareceres PLN-006.
O mapa é contrato para execução posterior; nenhuma nota foi renomeada nesta rodada.

## D5 — Session identifica a operação que produziu a linha — `bin/brza-note`

- **Origem:** R4.1; R11.2.
- **Contexto:** o índice atual resolve a sessão corrente, inclusive ao reconstruir linhas de notas antigas.

### Como fica

`session` é o nome da sessão que produziu a linha do índice. Em `index --rebuild`, registra a sessão que executa
a reconstrução; não recupera nem certifica a sessão de autoria da nota. Sem nome resolvido, o campo fica ausente.
A documentação do índice explicita essa semântica. O comportamento atual de atribuição é mantido; a resolução
do nome continua sujeita à verificação de R4.1.

**Alternativa recusada em R11.2:** preservar a sessão registrada anteriormente e omitir a desconhecida no rebuild.

## D6 — A listagem consulta as pendências no índice local — `bin/brza-note`

- **Origem:** R6.1; R12.1–R12.3.
- **Contexto:** consultar o índice disponível evita rede nas consultas repetidas; a atualização é uma ação explícita.

### Como fica

`brza note ls` lista issues e decisões de todos os workstreams pelo estado vigente do índice. MIG continua issue.

| Opção | Comportamento |
| :---- | :------------ |
| Sem opções | Estados `open`, `in_progress`, `in_review`; `opened` mais recente primeiro; índice local. |
| `--status all` | Inclui os estados encerrados. |
| `--status open` | Explicita o conjunto dos três estados abertos. |
| `--sort opened` | Mais recente primeiro. |
| `--sort priority` | high → medium → low. |
| `--sort deadline` | Menor data primeiro, incluindo vencidos. |
| `--refresh` | Atualiza o índice antes de listar; falha de atualização é explícita, sem fallback silencioso. |

Em toda ordenação, campo ausente fica no fim e empate usa ID ascendente. O padrão local pode refletir dados
anteriores ao último push de outro workstream; `--refresh` é a escolha explícita para atualizar essa visão.

**Gatilho de mudança do padrão — emenda à R12.3:** se dados errados forem listados com frequência, fetch passa a
ser o padrão. O limiar numérico de frequência não foi definido; o contrato registra o gatilho qualitativo pedido.

**Alternativas recusadas como padrão inicial em R12:** listar todos os estados; mais antigos primeiro; fetch
automático com `--offline`. O fetch padrão fica condicionado ao gatilho acima. A listagem não calcula prontidão
nem autoriza execução.

## D7 — REV e MIG reservam números pelo índice — `bin/brza-note`

- **Origem:** R1.2; R2.2; R3.2 e R3.4; R11.1; contratos aceitos na R13; R14.1.
- **Contexto:** a reserva precisa suportar concorrência entre workstreams e distinguir número reservado de nota existente.

### Como fica

| Comando | Saída após reserva confirmada |
| :------ | :--------------------------- |
| `brza note review-open <slug> --title <texto> --description <texto> [--workstream <nome>]` | REV-NNN e `work/reviews/REV-NNN-<slug>.md`. |
| `brza note migration-open <slug> --title <texto> --description <texto> [--workstream <nome>]` | MIG-NNN e `work/issues/MIG-NNN-<slug>.md`. |

A skill escreve o arquivo. REV usa `kind: review`; MIG usa `kind: issue`, `type: migration`; seus IDs são REV-NNN
e MIG-NNN. Cada família tem sequência independente; máximo + 1 é recalculado no callback a cada tentativa de
fetch/push, até três tentativas. Reserva abandonada não é reciclada. Sem remote ou sucesso, recusar sem imprimir
ID utilizável. Os comandos funcionam sem client; nome de sessão ausente não impede reserva.

Antes de liberar novas reservas, uma operação atômica reserva REV-001 a REV-004 conforme D4 e MIG-001 para a
renumeração. Reexecução aceita o mesmo mapa; colisão diferente recusa e volta à rodada, sem renumerar silenciosamente.
Reserva sem arquivo não satisfaz referências/dependências nem aparece como nota materializada no ls. O primeiro
commit registra a passagem de reserva para nota mesmo quando título e estado coincidem; a ausência de `commit`
distingue a reserva inicial.

O checador avisa, sem barrar, a nota de `work/reviews/` fora de `REV-NNN-<slug>.md`, a nota `MIG-NNN-…` sem
`type: migration` e a issue `type: migration` sem número `MIG-NNN` (R14.1).

## D8 — A migração tem prévia e aplicação idempotente — `scripts/migrate_pln008.py`

- **Origem:** R1.1; R2.2; R3.4; R5.3; R11.1; contratos aceitos na R13.
- **Contexto:** o acervo atravessa workstreams; o script compartilha o extrator do commit e o mecanismo de reserva.

### Como fica

Script específico no `brza-workflow`, com prévia por padrão, aplicação explícita e seleção de workstream:

1. Reservar os IDs de D7 e criar MIG-001 no molde de D1.
2. Aplicar as quatro renomeações e H1 de D4; corrigir links nas árvores donas.
3. Recalcular refs dos worklogs pelo D3; remover date preservando tags e demais campos.
4. Conferir cada workstream; commitar por caminhos e reconstruir o índice.

A prévia informa arquivos e alterações e não commita. Worktree ausente é reportado; o script não cria workstreams.
Segunda aplicação não altera arquivos nem acrescenta eventos desnecessários. Não inferir datas ou prioridade,
nem reescrever medição histórica. A conclusão da MIG-001 prova quatro nomes novos, ausência dos antigos e links
resolvidos. A sessão dona de cada workstream grava suas notas e evidências.

## D9 — O índice preserva os campos aprovados — `bin/brza-note` e norma

- **Origem:** R4.2 e R4.3; R5.2 e R5.3; R6.1; R7.2; R11.2; R12; contratos aceitos na R13.
- **Contexto:** extração, serialização e comparação precisam acompanhar os mesmos campos para o rebuild reparar o acervo.

### Como fica

| Campo | Contrato |
| :---- | :------- |
| `opened`, `priority`, `blocks`, `deadline`, `owner`, `type`, `depends_on` | Extração, serialização e comparação; ausência permanece ausência. |
| `estimate_h` | Número em plano e issue; opcional na issue. |
| `remaining_h` | Número no plano. |
| Listas | Preservar os elementos, sem limitar o parser aos escalares. |
| `session` | Nome da sessão da operação, inclusive no rebuild, conforme D5. |

O rebuild recompõe o estado pelas branches. O commit avisa sem barrar a falta de priority em plano/issue abertos;
o checador avisa date no worklog. A norma permite priority também em planos. O ls segue D6 e exclui reservas ainda
não materializadas; índice indisponível gera diagnóstico, sem fingir fila vazia. Colunas: ID, workstream, status,
opened, priority, deadline e título. A listagem não calcula prontidão nem despacha tarefas.

## D10 — Medição e sessão são verificadas nas fontes atuais — hook e CLI

- **Origem:** R4.1; R11.2; contratos aceitos na R13.
- **Contexto:** a versão atual já identifica conta e workstream nesta árvore; dados históricos não provam defeito presente.

### Como fica

Verificar entradas atuais de eventos em worktrees de notas e código, branch de plano e conta configurada; corrigir
apenas falhas reproduzidas. O nome da sessão usa as fontes disponíveis: variável de sessão e, com client, mapa e
provedor. Nome vazio permite fallback disponível. Sem fonte, o nome fica ausente; não inventar autoria.
Não acrescentar runtime, session_id ou modelo às notas nem reconstruir a medição histórica. Integração nova de
runtime sem fonte disponível volta à rodada com evidência, sem expansão silenciosa do core.

## D11 — O workspace de origem sai dos arquivos atuais dos repositórios `brza-*` — notas, norma local, `brza-workflow` e `brza-studio`

- **Origem:** Pedido 6; R15.1 a R15.3; R16.1 a R16.4; R17.1.
- **Contexto:** o PLN-011 do `studio` colidiu com o ID de um plano do workspace de origem, citado em crase em dois worklogs do `workspace`;
  o D3 conta a crase, e o próximo commit desses worklogs ligaria o plano errado.

### Como fica

| Onde | O que muda |
| :--- | :--------- |
| Notas dos cinco workstreams (`work/`, `plans/`, `wiki/`, `memory/`, `.claude/agent-memory/`) | Toda citação ao workspace de origem vira termo neutro, como "outro workspace" ou "o workspace de origem", sem nome nem ID. Inclui planos e worklogs fechados. |
| Master do `brza-workspace` | O `README.md` e a `.claude/rules/workspace.md` ficam neutros. A regra "As notas do workspace de origem" vira uma regra sobre notas de outro workspace, que se citam sem link, sem nome e sem ID. |
| `brza-workflow` | O `FOREIGN` do `bin/brza-init` lê os nomes proibidos de um arquivo da máquina, fora do git. O `golden_differences.py` troca a chave do nome por "origem", com textos neutros. Os testes e o golden seguem. |
| `brza-studio` | Os 3 testes trocam os dados de exemplo (o identificador de sessão e o domínio do Jira de origem) por nomes neutros. |
| Histórico do git, e-mail de autor dos commits antigos, `.brza/index.jsonl` | Ficam como estão: o histórico não se reescreve, e o índice só recebe linhas novas. |
| As identidades `issue:<slug>` das duas issues renomeadas do `tools-kit` | Fica, no índice e no `refs`; o arquivo e o H1 mudam (R17.1). |

A prova é um grep sem diferenciar caixa pelo nome do workspace de origem, lido do arquivo da máquina da guarda do `brza init`, sem resultado nos arquivos atuais das cinco branches, da master, do `brza-workflow` e
do `brza-studio`, salvo o `.brza/index.jsonl` e as identidades `issue:<slug>` das duas issues renomeadas do `tools-kit`, no
`refs` e no `depends_on`.
