# O fechamento: a rodada de decisão, o worklog e o encerramento

## 1. A rodada de decisões para Anderson

**Em texto, na mensagem**, com a proposta inteira à vista logo antes: a caixa da pergunta pode esconder o texto escrito
antes dela, e resposta dada sem o texto à vista não vale como aprovação (`AGENTS.md`, "Decisões pendentes"). Uma rodada
fecha antes da próxima abrir. Decisão só vale com a frase explícita ("decidido", "fechado", "pode aplicar"); sem ela, a
nota nasce como proposta.

Para cada decisão:

```markdown
**‹N›. ‹a pergunta›** (levantada por ‹personas›)

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
  prova de conceito abriu, as sessões deixadas abertas.

## 3. O encerramento

1. `python3 -I .claude/skills/meeting-runner/scripts/runtime_memory_check.py <hora da abertura>`; o que listar vai a `## Fora do workspace`.
2. **O encerramento das personas (R6):** a coordenação manda "a reunião acabou; envie `worker_done`". O host arma ~2 min e
   o chat mostra "manter aberta": Anderson guarda a persona que quiser consultar (`--keep-open` por comando). Quem não
   responder: `launch_persona.py $R --stop <persona>` (`worker-stop`; o `worker-release` só vale para worker que já enviou `worker_done`). A contraprova e a rodada a mais
   acontecem antes dessa mensagem. Persona aberta por `--via agent-launch` (sem Dispatch) fecha por
   `brza sessions close <nome>`.
3. Derrube o que a prova subiu (túnel, servidor, porta) e confira que a porta fechou.
4. Issues para o que sobra (`work/issues/`), com a origem.
5. `brza note commit` dos worklogs das personas, do worklog da coordenação e das issues, na branch do workstream; nunca
   na `master`.
6. Nas respostas ao chat, o worklog da coordenação em `<details>` (norma do `AGENTS.md`) e os das personas por link, não
   por inteiro.
