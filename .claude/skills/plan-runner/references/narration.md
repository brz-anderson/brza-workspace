# A narração no chat da coordenação

Anderson acompanha o plano pelo chat da coordenação, e não pelos chats dos executores. O que ele precisa ver ali é o
estado e os números, na hora: quem está executando o quê, o que chegou, o que foi conferido e quanto custou. O texto
integral — o worklog do executor, o arquivo de cada consultor — vai pelo caminho, salvo na rodada dos consultores
(abaixo). A regra vem das duas reuniões de 2026-11-07: a diferença entre a coordenação que "informou muito bem" e a que
"deixou a desejar" não foi silêncio, foi conteúdo nomeado (memória `coordination-narration-in-chat`).

**A narração sai dos scripts.** As linhas abaixo são o que o `executor.py`, o `consult.py` e o `plan_panel.py` imprimem;
cole como estão. Narração de cabeça erra a hora, a contagem e o custo.

| Momento | O que vai ao chat |
| :-- | :-- |
| abertura de um executor | a tabela `Passo · executor · runtime · modelo · esforço · checkout · branch`, que o `executor.py open` imprime, e a linha `::orca-visual` do painel |
| cada evento do `wait` | uma linha "P3 · feito em 18 min; P5 · em curso 6 min", e o painel atualizado |
| a cada ~3 min sem evento | a mesma linha, com a idade do último evento |
| evidência | a linha `**Evidência:**` proposta, o que a coordenação conferiu por comando ("confere: `…` → …") e o `Executado` medido |
| desvio | o `X` proposto, numa linha, e a rodada se ele muda um `D` |
| bloqueado | o que o executor perguntou, lido pelo `brza sessions read --last`, e o que a coordenação respondeu ou levou à rodada |
| consultores em sessão | a linha do gatilho ("D4: 3 alternativas, formato de dado gravado → consultores em sessão (R2.3)"), a tabela de abertura, cada chegada, e na rodada a tabela lado a lado mais a argumentação integral de cada um (memória `consultant-debate-shown-in-full`; PLN-021/R4.4 recomendada) |
| fechamento | "P3 · encerrada e aceita" só depois do `close --wait-settled`; `closing` não é encerrada |

- **A hora** de toda linha sai de `date '+%H:%M:%S'`, rodado na hora.
- **Nenhum número sem a fonte**: custo e horas saem do `executor.py evidence` e do `plan_state.py`; sem medição, "sem
  medição", nunca zero.
- **O ruído do host** — "Worker stopped without reporting" a cada fim de turno sem `worker_done` — é o normal entre o
  envio e o marcador: não se responde nem se narra como falha.

## O painel do plano

Um `::orca-visual` por plano e dia (`pln-nnn-painel-<hash>.html`), gerado pelo `plan_panel.py` e republicado no mesmo nome
pelos scripts que mudam o estado (`executor.py`, `round_log.py`, `plan_state.py --fix`). Mostra o cabeçalho do plano
(fase, `ready`, as três horas, com `⚠` quando a soma não confere), uma linha por passo (estado, executor, Estimado ×
Executado, custo, idade do último evento), os executores e consultores vivos e a última rodada. O PNG sai na abertura e
no fechamento de cada executor; leia-o para conferir o corte antes de dizer que o painel está certo. `--no-panel` só
quando o chat não mostra visual; `⚠ painel: …` não muda o código de saída.
