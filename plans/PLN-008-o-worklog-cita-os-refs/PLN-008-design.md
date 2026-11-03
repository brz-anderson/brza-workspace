# PLN-008 — Desenho

## O que este desenho assume

As respostas das R1 a R6 estão no
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](PLN-008-plan.md).
O Desenho segue em elaboração. Além do Terreno, estão confirmados:

- **R7.2:** `depends_on` opcional em planos e issues, também no índice; semântica e validação ainda por desenhar.
- **R7.3:** a issue comum aparece no `refs:` como `issue:<slug>`, preservando a identidade do índice.

- **R8.1:** uma única `migration-runner` reúne criação, revisão e execução, com revisor independente.

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

Falta definir a semântica e a validação do `depends_on`, a regra para exemplos hipotéticos, o mapeamento das quatro
revisões para REV-001 a REV-004 e o tratamento da sessão no rebuild. Não houve implementação.

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
