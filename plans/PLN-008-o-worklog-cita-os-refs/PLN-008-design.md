# PLN-008 — Desenho

## O que este desenho assume

As respostas das R1 a R6 estão no
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](PLN-008-plan.md).
Os itens `D` aguardam as rodadas de desenho; este arquivo registra somente o Terreno.

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

O Pedido 4 exige escolher como criar ou adaptar as skills; a R5.1 deixou `depends_on` para o Desenho.
Também faltam a identidade das issues no `refs:`, a regra para exemplos hipotéticos, o mapeamento das quatro
revisões para REV-001 a REV-004 e o tratamento da sessão no rebuild. Nenhuma proposta desses pontos foi aplicada.
