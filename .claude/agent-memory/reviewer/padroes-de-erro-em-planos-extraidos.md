---
name: padroes-de-erro-em-planos-extraidos
description: Onde o defeito costuma se esconder num plano extraído de outro (PLN-009 de PLN-003) e no Desenho escrito por sessão de outro runtime — itens que caem entre os planos, limiares sem rodada, achados medidos não absorvidos
metadata:
  type: project
---

Padrões que apareceram na revisão do Desenho do PLN-009 (2026-11-03), extraído do PLN-003:

- **O que cai entre os dois planos.** Quando um plano novo "fica dono" dos passos de outro (P6–P9 → PLN-009), confira
  item a item da matriz (`M…`) e das rodadas que os passos que saem executavam (`Executa D5 (M8, M13, M14)`) contra o
  plano novo. No PLN-009 sumiram M6, M7, M13, M14 e R6.4; a issue de passagem também não os listava.
- **Limiar e porta sem rodada.** Números concretos (RAM > 4 GB, CPU > 90%, confiança 0,75, porta 4242, US$ 0,01)
  entram no Desenho com uma linha "Origem" que cita rodadas que não têm número. Conferir a rodada inteira, inclusive o
  texto da opção recomendada.
- **Achado medido que não chega ao Desenho.** Worklog e `[x]` dizendo "ajustes registrados nos D3–D7" sem o diff ter
  mudado os D. Conferir com `git diff`/`git show` do Desenho, não pelo que o worklog afirma.
- **Vocabulário de papel trocado.** `implementer` (subagente por papel do `AGENTS.md`) usado no lugar de `executor`
  (a sessão-worker da R5.2) no ramo do gate: papel desconhecido fica sem regra.
- **Afirmação sobre ferramenta do `brza-workflow`** ("o `brza install` liga o pacote novo") — conferir no código do
  `bin/brza-install`; ele só liga `bin/` e `packages/client/bin/`.
- **Comando do plano que diverge do runner da suíte alvo.** O plano prescreve o padrão genérico `python3 -m unittest discover -s tests/<pasta>`
  para uma pasta que usa runner próprio (`run.py`), fazendo a evidência prometida falhar com 0 testes e código 5. Conferir a
  seção de testes do `README.md` do repositório antes de fechar o plano.
- **Comando em prosa inline que omite flag obrigatória.** Ao citar comandos rápidos no meio do texto explicativo de passos
  (ex.: `brza note commit <worklog> --until <HH:MM>`), omitir flags mandatórias como `-m "..."` que só aparecem na seção
  formal do comando gera comandos que quebram se executados diretamente pelo leitor/agente.
  *Onde se esconde:* em frases de instruções intermediárias de skills e notas que resumem ações antes do passo formal de execução.
- **Assimetria de cardinalidade entre passos sequenciais de skill.** Um passo inicial prevê "mais de uma" tarefa e prescreve ação,
  enquanto o passo posterior assume "duas", restringindo indevidamente o comportamento em cenários com 3+ itens.
  *Onde se esconde:* em skills que receberam passos novos ou desdobramentos de fluxos.

- **Seção que um comando escreve "como a última" sem a skill dizer onde o agente acrescenta.** No P5 do PLN-012, a
  `## Medida` é a última seção do worklog e o `brza note commit` a reescreve, mas o `close-task` manda "acrescente ao
  worklog de hoje o que veio depois": o texto acrescentado no fim cai dentro da seção que o comando reescreve.
  *Onde se esconde:* em skill que ganha bullet sobre seção gerada, longe do bullet antigo que manda acrescentar. Dei 80,
  com a premissa de como o comando (ainda não escrito) corta a seção.
- **Instrução de corte por hora que a saída não mostra.** "`--until` com a hora do fim do último turno" quando o aviso
  lista só a hora do começo, truncada no minuto, e o turno vai ao segmento pelo começo, em `(marco k−1, marco k]`:
  `HH:MM` truncado do fim de um turno curto cai antes do começo dele. Conferir a granularidade da saída contra a regra
  de fronteira do contrato (`task_mark`, `row_start` no `summarize_measurements.py`). Vai a rodada quando é do Desenho.

**Why:** foram os achados de maior gravidade, e todos se acham por comando em minutos.
**How to apply:** em revisão de plano extraído ou de Desenho vindo de outra sessão, rodar esses cinco cheques antes da
leitura fina. Ver também [[estado-muda-durante-a-revisao]] e [[achados-que-costumam-cair]].
