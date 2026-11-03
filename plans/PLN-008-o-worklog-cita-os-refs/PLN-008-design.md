# PLN-008 — Desenho

## O que este desenho assume

As respostas das R1 a R6 estão no
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](PLN-008-plan.md).
O Desenho segue em elaboração. Além do Terreno, estão confirmados:

- **R7.2 e R9:** `depends_on` opcional em planos e issues, também no índice; só `done` satisfaz; alvo inexistente,
  autorreferência e ciclo geram erro no checador.
- **R7.3:** a issue comum aparece no `refs:` como `issue:<slug>`, preservando a identidade do índice.

- **R8.1:** uma única `migration-runner` reúne criação, revisão e execução, com revisor independente.
- **R10:** refs considera prosa, crases inline, links e citações históricas fora de cercas; menção textual
  desconhecida gera aviso sem entrar no campo.
- **R11.1:** as quatro revisões recebem REV-001 a REV-004 pela primeira inclusão no git.
- **R11.2:** `session` identifica a sessão que produziu a linha do índice, inclusive no rebuild.

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

### Lacunas para as rodadas

Falta concluir os contratos de numeração, preenchimento do acervo, índice e listagem. O mapeamento das quatro REV
e a sessão no rebuild estão definidos em D4 e D5. Não houve implementação.

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

- **Origem:** R5.1; R7.2; R9.1 e R9.2.
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

**Alternativas recusadas em R9:** aceitar `dropped` como dependência satisfeita; permitir referências inválidas ou
ciclos com aviso. A escolha exige entrega e corrige a relação inválida antes do commit.

## D3 — O refs extrai as menções fora das cercas — `bin/brza-note` e checador

- **Origem:** R1.1; R7.3; R10.1 e R10.2.
- **Contexto:** o filtro atual apaga crases inline, embora elas contenham citações reais; exemplos cercados podem
  mencionar IDs sem relação com o trabalho.

### Como fica

O `brza note commit` preenche o `refs:` dos worklogs antes da conferência. A extração considera a prosa, crases
inline, links e citações históricas do corpo, excluindo blocos cercados de código.

| Entrada | Resultado |
| :------ | :-------- |
| `PLN-008/D1` fora de cerca | Referência `PLN-008`, sem validar o item D1. |
| `PLN-003` somente em bloco cercado | Não gera referência. |
| Link para issue comum existente | Referência `issue:<slug>` com a identidade do índice. |
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
