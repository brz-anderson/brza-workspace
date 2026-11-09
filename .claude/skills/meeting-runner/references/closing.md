# O fechamento: a rodada de decisão, o worklog e o encerramento

## 1. A rodada de decisões para Anderson

**Em texto, na mensagem**, com a proposta inteira à vista logo antes: a caixa da pergunta pode esconder o texto escrito
antes dela, e resposta dada sem o texto à vista não vale como aprovação (`AGENTS.md`, "Decisões pendentes"). Uma rodada
fecha antes da próxima abrir. Decisão só vale com a frase explícita ("decidido", "fechado", "pode aplicar"); sem ela, a
nota nasce como proposta.

Para cada decisão:

```markdown
**‹N›. ‹a pergunta›** (levantada por ‹personas›; quem levantou não é quem vota a favor)

1. **‹Opção recomendada› (Recomendado).** Custo: ‹o que se gasta e quando›. Se paga: ‹agora / numa fase / nunca›.
   - Votos: ‹Persona A apoio; Persona B apoio com ressalva; …›
   - **A favor, o mais forte:** ‹uma linha› — ‹Persona›, [worklog](../‹caminho›#‹âncora›).
   - **Contra, o mais forte:** ‹uma linha› — ‹Persona›, [worklog](…).
2. **‹Outra opção›.** Custo: …. Se paga: ….
   - Votos: … · **A favor:** … · **Contra:** …
```

- **O voto e o argumento mais forte a favor e contra, uma linha cada** (R2.4): a rodada cabe numa tela. A argumentação
  integral fica no worklog da persona e, na fase do painel, será lida de lá. A regra da memória
  `consultant-debate-shown-in-full` vale só para consultores disparados por `Agent`.
- Opção visual: um artboard por alternativa (`::orca-visual`), conferido por PNG antes (ver `narration.md`).
- **Toda opção diz o custo e quando se paga**, a recomendada e as outras; opção cujo custo a coordenação não sabe dizer se
  mede antes ou sai da rodada.
- O painel só mostra as decisões; a pergunta vai a Anderson no chat.

## 2. O worklog da coordenação

`work/worklogs/AAAA-MM-DD-<reuniao>-coordenacao.md`, no formato do `work/README.md`, com:

- **Tabela de rodadas:** Rodada · Aberta · Fechada · O que produziu.
- **Tabela de modelos por persona:** Persona · runtime · modelo · esforço · o `fallback` usado.
- **Tabela de medição por persona** (do `tally.py`): latência, custo ou tokens, confiança R1 → final, nota dos colegas,
  viradas. Grok e Antigravity: "sem medição".
- **A proposta final copiada inteira**, porque `.sessions/` está no `.gitignore` e não vai ao git (a MCP a copiou; a
  Carvão não e ficou só com o plano).
- **Os custos:** coordenação, revisor, `collector`, personas, contraprova; Claude em US$ pelo `measurements.jsonl`, Codex em
  tokens, e "sem medição" onde for o caso. Sempre com a base de cada número.
- `## Fora do workspace`: a memória de runtime que `runtime_memory_check.py` achou, os túneis e as sessões Cloud que a
  prova de conceito abriu, as sessões deixadas abertas, o Run e os Dispatches com o estado que o `--status` mostrou.

## 3. O encerramento

1. `python3 -I .claude/skills/meeting-runner/scripts/runtime_memory_check.py <hora da abertura>`; o que listar vai a `## Fora do workspace`.
2. **O encerramento das personas (R6 e R7):**
   - `python3 -I .claude/skills/meeting-runner/scripts/launch_persona.py $R --close` pede a cada persona o
     `worker_done` **do preâmbulo do Orca, com o `--task-id` e o `--dispatch-id` dele** (X19), e o CLI devolve
     `closing`. `closing` é o pedido, não o fechamento.
   - `launch_persona.py $R --status --wait-settled 180` confere no `worker-show` que o host aceitou o `worker_done`
     (`succeeded`/`settled`, `taskId`, `autoReleaseAt`). Só então a narração diz "encerrada": o host arma ~2 min e o chat
     mostra "manter aberta", e Anderson guarda a persona que quiser consultar (`--keep-open <persona>` faz o mesmo por
     comando).
   - Quem não respondeu: `launch_persona.py $R --stop <persona>` (parada guardada: o CLI confirma `stopped` e o
     settlement antes de liberar). `stop_unknown`, `release_unknown` e `retained` não são fechados e não autorizam repetir
     o comando: confira com `--status` e relate a incerteza no worklog.
   - Com o `--status` em "encerrada e aceita", não repita o `--close`: o host libera sozinho em ~2 min, e o `close` do v2
     ainda não reconhece o worker encerrado (lê `dispatch.status: completed` antes de `worker.state: succeeded`) e
     mandaria outro pedido.
   - "Encerrada, retida (motivo)" no `--status` não fecha sozinha (outro dono ou identidade não provada): registre no
     worklog, em `## Fora do workspace`, e deixe a decisão de fechar a aba com Anderson. Pela R7, retida não é fechada.
   - A contraprova e a rodada a mais acontecem antes do `--close`. A rodada extra automática da R8 (fato novo que
     contradiz a premissa de um voto) também: ela estende a reunião sem perguntar, mas não decide nada; a rodada de
     decisões continua de Anderson e mostra o voto de antes e o de depois da rodada extra.
3. Derrube o que a prova subiu (túnel, servidor, porta) e confira que a porta fechou.
4. Issues para o que sobra (`work/issues/`), com a origem.
5. `brza note commit` dos worklogs das personas, do worklog da coordenação e das issues, na branch do workstream; nunca
   na `master`.
6. Nas respostas ao chat, o worklog da coordenação em `<details>` (norma do `AGENTS.md`) e os das personas por link, não
   por inteiro.
