# Conduzir — retomar e executar pelos executores

Conduzir é executar e registrar no mesmo movimento. O checkbox marcado sem prova e a fase que não casa com os passos
nascem de executar e registrar serem atos separados — e de quem executou gravar o plano sem ninguém conferir. Na v2, o
executor executa e escreve a evidência no worklog dele; a coordenação confere por comando e a leva ao plano.

`$S` é `python3 -I .claude/skills/plan-runner/scripts`, da raiz do worktree.

## Retomar

"Retomar o PLN-NNN", "onde isso parou?", começa sempre igual, antes de tocar em qualquer arquivo:

1. **`$S/plan_state.py PLN-NNN`.** Ele lê o frontmatter, o `Retomar`, os passos e as evidências, e diz o próximo passo e
   os problemas: `checked-without-evidence`, `checked-without-executed`, `hours-mismatch`, `step-without-design`,
   `step-cites-unknown-design`, `design-without-origin`, `origin-unknown-round`, `deviation-not-cited`, `duplicate-id`.
   Passo marcado sem evidência volta a ser pendente: diga isso a Anderson e grave a correção. As horas que não somam se
   corrigem com `--fix`, dito antes de rodar.
2. **`$S/executor.py status PLN-NNN`**, se há `.sessions/pln-nnn/execucao.json`: o executor que ficou aberto, parado ou
   bloqueado desde a última sessão. Executor `feito` sem evidência gravada vai ao `evidence` antes de qualquer passo novo.
3. **Rode o checador** (`../notes-checker/scripts/check_notes.py`) e traga às seções de ponteiro as notas que ele avisa
   (`backlink-missing`).
4. **Confira os pré-requisitos de novo.** Faltando, pare e diga o que falta.
5. **Diga em uma linha onde o trabalho está** e qual passo vem, com o painel (`$S/plan_panel.py publish PLN-NNN`), antes
   de executar.

Retomar um plano de worklog numa sessão nova é o sinal de que ele atravessa sessões: promova-o a `PLN` antes de seguir.

## Executar um passo

**O passo só executa a pedido explícito de Anderson, passo a passo**: plano aceito não autoriza execução, e "execute o P3"
não autoriza o P4.

1. **Pré-requisito do passo, antes de começar.** Se não existe, é gatilho de parada.
2. **Pelo executor que a linha `Executa` nomeia:**
   - **a coordenação** — a rodada, a nota, o registro; se o passo entrevista, as rodadas acontecem aqui;
   - **uma sessão executora** — o passo de código, o protótipo, o passo longo. Siga "O ciclo do executor", abaixo. Nunca
     execute o passo de código do `brza-studio` na sessão da coordenação;
   - **um subagente** — leitura, rascunho e o passo curto que cabe numa devolução; ele devolve os arquivos tocados, os
     comandos com o resultado e cada desvio local como `X` proposto;
   - **Anderson** — o que só se prova no aparelho dele: o plano escreve os `C` e ele grava o Observado e o veredito.
3. **Registre a evidência** na linha do passo, e só então marque `[x]`, com o `Executado`; `$S/plan_state.py PLN-NNN
   --fix` reescreve as três horas.
4. **Registre o desvio** como `X`, curto, e cite-o no passo. Desvio que muda um `D` vira rodada antes de seguir.
5. **O commit.** No passo por sessão, o pedido diz o que o executor commita (`references/step-request.md`, "Regras");
   merge e push sempre pedem confirmação de Anderson. No passo da coordenação, proponha o commit com o repositório
   verde e commite só com confirmação.

## O ciclo do executor

```text
open → (wait → evento)* → evidence → evidence --apply → close
```

1. **Abrir.** `$S/executor.py open PLN-NNN P<n> (--checkout <caminho> | --tree <nome> [--type feat]) [--agent claude --model … --effort …]`.
   - Com `--tree`, o worktree do `brza-studio` nasce pelo `brza tree` (o pedido é conferido antes); sem ele, `--checkout
     <caminho>` é obrigatório, e o `open` recusa a falta dos dois. Checkout na `master`/`main` leva a branch `feat/pln-nnn-pn`,
     nunca a principal; o do próprio workspace (passo de nota) não autoriza commit.
   - O Codex com `--effort` leva o `--model` padrão (`CODEX_MODEL`); o `brza sessions` recusa o esforço sem modelo.
   - `open` não reabre passo `feito` nem com evidência gravada; passo `parado` ou `falhado` reabre, e o marcador velho do
     worklog vira comentário.
   - Ele gera o pedido pelo `step_request.py` (o passo, os `D` do `Executa`, as rodadas citadas, as restrições, as
     regras e o protocolo de fim), cria o worklog do executor no workstream, abre a sessão pelo `brza sessions <nome>
     --prompt-file … --title "PLN-NNN P<n>: …" --rename --wait`, grava o manifesto e publica o painel.
   - Cole na mensagem a tabela que ele imprime e a linha `::orca-visual`.
   - "Não abriu" não se relança antes de ler o `pending-*.json` que o `brza sessions` cita.
   - O modelo segue a camada do passo, pelo `AGENTS.md`: implementação na média, revisão e desenho na alta.
2. **Esperar.** `$S/executor.py wait PLN-NNN [P<n> …]`. Ele espera pelo `brza sessions wait --any --marker
   <worklog>:<!-- fim-P<n>:` e imprime uma linha por evento, já com o painel:
   - **`feito`** (o marcador `fim-Pn: feito`) → vá ao `evidence`;
   - **`parado`** (`fim-Pn: parado`) → o executor achou desvio que muda o `D`: leia o `X` no worklog dele e leve à rodada;
   - **`bloqueado`** (saída 3) → o chat do executor espera resposta: leia com `brza sessions read <sessão> --last`. Se é
     dúvida do passo, responda com `$S/executor.py send PLN-NNN P<n> --text …`; se é decisão de Anderson, vira rodada aqui;
   - **"o turno acabou sem o marcador"** (`ended_without_marker`) não é fim: a espera segue;
   - **prazo** (saída 75) → `status` e decida; nunca um envio novo às cegas.
3. **Ler a evidência.** `$S/executor.py evidence PLN-NNN P<n>` lê o `## Evidência` do worklog do executor, confere cada
   commit (`git cat-file -e`), roda de novo o comando marcado `(≤ 2 min)` e mede o `Executado` pela janela da abertura ao
   marcador. Ele imprime a linha `**Evidência:**` e o `Executado` propostos.
   - **A proposta não roda o comando do worklog.** `--rerun` o roda sem gravar e o `--apply` o roda e grava, por argv e sem
     shell: aceita `VAR=v` e `cd X &&` na frente, glob e `~`; recusa `;`, `|`, `>`, `$` e crase. **Isso não é segurança:**
     `bash -c "…"` e `git push --force` passam pelo filtro, que só tira o que o argv não reproduz. A proteção é você ler a
     proposta antes do `--rerun` ou do `--apply`.
   - **Leia a proposta antes de aplicar.** O que não confere (commit que não existe, teste que falha) volta ao executor
     pelo `send`, e o passo não fecha.
   - Narre o que conferiu: "confere: `git -C … cat-file -e a1b2c3d` → ok; `<testes>` → 42 passed; Executado 0,6 h".
4. **Aplicar.** `$S/executor.py evidence PLN-NNN P<n> --apply` grava a evidência no `### Pn`, marca o `[x]`, roda o
   `plan_state.py --fix` e republica o painel. Ele marca `[x]` só nos subpassos da linha `cobre:` do worklog (`cobre: todos` marca todos); sem `cobre:`, marca todos os
   pendentes e avisa: confira à mão. Os `X` propostos no worklog entram em
   `## Desvios` pela coordenação, à mão, depois de lidos. Várias linhas `cobre:` se juntam, e `todos` vence.
   - **Passo parcial** (`cobre:` não cobre tudo; sobra `[ ]`): o passo fica `evidencia-gravada`, e o ciclo continua com
     `send` do que falta (neutraliza o marcador e volta a `em-curso`), `wait`, e `evidence --apply` de novo, com o
     `cobre:` acumulado no worklog. `open` também reabre o passo com `[ ]` pendente; sem pendente, `open` e `send` não o
     reabrem.
5. **Fechar.** `$S/executor.py close PLN-NNN P<n>` pede o encerramento e confere o aceite (`--wait-settled 180`).
   `closing` não é fechado. `--keep-open` mantém a sessão para Anderson consultar.

**Executores em paralelo** — dois passos independentes pedidos juntos — abrem um a um e esperam juntos
(`wait PLN-NNN P3 P5`). No mesmo worktree, eles não commitam no workspace: a coordenação commita os caminhos de cada passo
ao fechá-lo.

## Fim de sessão

No `PLN`, gravados no mesmo commit:

- **O worklog da sessão**, em `work/worklogs/`, e os worklogs dos executores fechados nela.
- **Uma linha no `## Worklogs`**: a data, o que avançou citando IDs, o que travou e o link do worklog.
- **O `Retomar` reescrito** com o próximo passo e, se houver, o executor que ficou aberto.
- **O `phase` conferido**, e o `$S/plan_state.py PLN-NNN` limpo.
- **A issue aberta na sessão** entra em `## Pendências conhecidas`; a decisão, em `## Decisões`.
- **Arquivo acima do teto** divide por sufixo, no mesmo commit, com a linha `Dividido`.

No worklog, o fim de sessão é o registro da execução abaixo do plano aceito; trabalho que não fechou é promovido a `PLN`.
