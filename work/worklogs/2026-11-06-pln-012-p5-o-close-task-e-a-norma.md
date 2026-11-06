---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-018
---

# O P5 do PLN-012, o close-task e a norma

O pedido da sessão que conduz o
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md),
em 2026-11-06, na sessão `pln012-p5`: a parte de código e norma do P5, que executa o D6 e a norma do D3. Ele parte do
pedido de Anderson na sessão "Plano: medir a produtividade por tarefa (tools-kit)": "inicie os passos em paralelo". A
abertura das issues (P5.5) e o merge na `master` (P5.4) ficam com a sessão que conduz.

## O que se fez

- **O teste que falha:** o `check_pln012_p5`, em `tests/notes-checker/run.py`. Um worklog com `sessions:` e
  `## Medida` passa no checador sem erro nem aviso, e o antigo também. A `## Medida` não põe nada no `refs:`. A norma, a
  skill e o adaptador dizem o que o D3 e o D6 pedem. Antes da norma, 11 casos davam FALHA.
- **O `close-task`** (`core/.claude/skills/close-task/SKILL.md`):
  - o passo "2. O que o commit vai fechar" roda o `--by-task --pending --session "$CLAUDE_CODE_SESSION_ID"`, e as
    tarefas emendadas se fecham pelo `--until`;
  - os passos seguintes vão de 3 a 7;
  - o "Commitar" cita o carimbo `sessions:`, a `## Medida` e o `--until`;
  - o acréscimo ao worklog de hoje vai acima da `## Medida`.
- **A norma** (`core/work/README.md`):
  - a propriedade `sessions` na tabela;
  - na seção `work/worklogs/`, o `sessions:` no frontmatter, sem `opened` nem hora em `completed`, e a `## Medida` como
    última seção, escrita pelo comando e não à mão;
  - a seção "Commit" aponta para a seção `work/worklogs/`.
- **O adaptador** (`core/CLAUDE.md`):
  - os eventos `task` e `run` na tabela do hook de medição, com uma linha que diz que eles vêm dos comandos, e não do
    hook;
  - os campos novos do `turn`;
  - o `--by-task` e o `--pending` no resumo.
- **A cópia golden** `tests/hooks/fixtures/golden/master/` acompanha as três edições, como nos commits anteriores do
  `core/`.
- **A revisão** está no [REV-018: A revisão do P5 do PLN-012, o close-task e a norma](../reviews/REV-018-pln-012-p5-o-close-task-e-a-norma.md).
  Foram duas rodadas do `agy` e uma final do `reviewer`; os achados `corrigido aqui` foram a um `implementer`.

## Evidência

- **Os commits:** `brza-workflow@332c6f9` (a entrega), `brza-workflow@19509c2` (A2, A3) e `brza-workflow@22805fb`
  (A12–A15), na `feat/pln-012-p5`, com push. O autor é `brz.anderson.pereira@gmail.com`.
- `python3 tests/notes-checker/run.py` → saída 0, com todos os casos `ok`, inclusive os 14 do `check_pln012_p5`.
- `python3 -m unittest discover -s tests/hooks` → 291 testes, OK. Inclui o golden e o `test_compact_guard`.
- `python3 -m unittest discover -s tests/cli` → 492 testes, OK.
- `python3 -m unittest discover -s tests/mcp` → 389 testes, OK.
- **Executado:** 0,9 h, das 18:22 às 19:15.

## Desvios

- **A suíte do checador não é `unittest`.** O comando do plano, `python3 -m unittest discover -s tests/notes-checker`,
  roda 0 testes e sai 5. O caso foi para o `run.py`, onde moram os casos de antes. O plano deve trocar o comando no
  P5.3, na Evidência do P5 e na última linha da Regressão (A1 do REV-018).
- **O caso do checador já passava antes da norma:** o checador não tem lista fechada de chaves (F26). O que falhou
  antes foram as asserções da norma, da skill e do adaptador, no mesmo caso.
- **O `--until` leva a hora do começo do primeiro turno da tarefa seguinte.** O D6 mandava a hora do fim do último
  turno da tarefa anterior, mas o `--pending` só mostra o começo de cada turno, e o turno vai à tarefa pela hora em que
  começa. Cortada no minuto, a hora do fim pode cair antes do começo do próprio turno. Quando os dois turnos começam no
  mesmo minuto, vai a hora ISO (A15 do REV-018). A decisão da R3.4 não muda.
- **Acréscimos ao texto do D6:**
  - "Sem turno pendente, a saída é 'nada a fechar'" e "sem a `CLAUDE_CODE_SESSION_ID` … o passo não se aplica", do D1 e
    do D4;
  - o `-m` na menção do `--until` (A3);
  - "com três ou mais, repita da mais antiga para a mais nova" (A2);
  - "acima da `## Medida`" no passo 3 (A12).
- **Acréscimos no `CLAUDE.md`:** a linha `turn` ganhou os campos do D2 (`waits_s`, `prompt_head` e `machine`, com a CPU
  dos comandos), porque a tabela é editada só neste passo.

## O que ficou

- **Para o P3:** o `brza note commit` deve preservar o texto que estiver abaixo da `## Medida` ao reescrevê-la (A12).
  A linha da Medida do D3 diz "Anderson": no núcleo, o nome vem do `workspace.owner` do manifesto, porque o teste de
  ouro proíbe "Anderson" no `core/`.
- **Para a sessão que conduz:** o comando da suíte no plano (A1), o `[x]` e o `Executado` do P5, o merge na
  integração e na `master`, e o P5.5.
- **A memória do `reviewer`** no `tools-kit` (`.claude/agent-memory/reviewer/`) ficou sem commit. As rodadas deste
  passo e as dos outros passos em paralelo gravaram nela, e ela não é caminho deste passo.

## Fora do workspace

- **O quê e onde:** três commits na branch `feat/pln-012-p5` do `brza-workflow` (`332c6f9`, `19509c2`, `22805fb`), com
  push ao `origin`, no worktree `~/Projects/brza-workflow/.worktrees/pln-012-p5`. **Risco:** nenhum; a branch não está
  na integração nem na `master`. **Estado:** ativa, à espera do merge pela sessão que conduz. **Como desfazer:**
  `git push origin --delete feat/pln-012-p5`.
