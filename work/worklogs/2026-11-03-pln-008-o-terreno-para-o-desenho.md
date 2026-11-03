---
scope:
  - workspace
---

# O Terreno do PLN-008 para o Desenho

Anderson pediu retomar o
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md).
A leitura das branches locais não encontrou bloqueios ativos, e o checador passou sem erros nem avisos.

Um collector levantou os contratos atuais do CLI, do índice, do checador e da medição no `brza-workflow`.
O [PLN-008 — Desenho](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-design.md) registra o Terreno:
faltam suporte a listas e campos de ordenação no índice, identidades REV/MIG e extração de referências.
O rebuild usa a sessão de quem reconstrói, sem recuperar a autoria antiga.

A medição instalada já resolve `workspace` e `.claude` nesta árvore. A suíte focal de medição passou com 36 testes,
e o collector verificou os 45 testes do índice. Isso não reescreve o diagnóstico histórico da R4.

Na R7, Anderson respondeu "7.1 só `migration-runner` / 7.2.1 / 7.3.1": escolheu `depends_on` opcional em planos,
issues e índice, e `issue:<slug>` no `refs:`. A contraproposta de uma única skill nova volta em R8.1 para confirmar
se ela reúne criação, revisão e execução. Nenhum passo de implementação foi iniciado; o próximo ponto está no
Retomar do plano.

Na R8.1, Anderson confirmou com "sim" a única `migration-runner` reunindo criação, revisão e execução, com revisor
independente. O D1 registra esse contrato; as regras de dependência são o próximo ponto do Desenho.

Na R9, Anderson respondeu "ambos recomendado": só `done` satisfaz uma dependência, e o checador barra alvo
inexistente, autorreferência e ciclos, inclusive entre workstreams. O D2 registra as regras; a extração do `refs:`
é o próximo ponto do Desenho. Não houve implementação.

Na R10, Anderson respondeu "ambos recomendado": o refs considera prosa, crases inline, links e citações históricas
fora de cercas; menção textual desconhecida gera aviso sem entrar no campo. ID inexistente no próprio refs e link
quebrado continuam erros. O D3 registra o contrato; seguem o mapeamento das quatro REV e a sessão no rebuild.

Na R11, Anderson respondeu "11.1.1 / 11.2.2": a numeração REV segue a inclusão cronológica no git, e `session`
identifica a sessão da operação, inclusive no rebuild. D4 contém o mapa das quatro revisões; D5 explicita a
semântica da sessão. Nenhuma revisão foi renomeada; seguem listagem e demais contratos antes dos Passos.

Na R12, Anderson respondeu "12.3.2 / restante recomendado": ls mostra abertos, ordena por opened recente primeiro
e consulta o índice local por padrão; `--refresh` atualiza, com falha explícita. O D6 registra o contrato. A
Entrevista foi extraída para arquivo próprio, preservando R1 a R11 e acrescentando R12, para manter o plano abaixo
do teto de leitura. Segue a consolidação dos demais contratos e do corte em Passos; não houve implementação.

Anderson emendou a R12.3: "dados errados listados com frequência, o fetch vira padrão". O gatilho foi registrado
na Entrevista, no D6 e no Retomar, sem inventar um limiar numérico. O corte proposto na R13 continua sem aceite.

## Aceite da R13 em 2026-11-03

Anderson respondeu "aceito" ao corte em sete passos, com 18 h estimadas. A resposta está na Entrevista; o Desenho
consolida D1 a D10, incluindo validar refs explícito antes de recalcular, distinguir reserva de nota materializada
e preservar o gatilho da R12.3. O plano recebeu Passos, Cobertura, pré-requisitos e Regressão.

| Passo | Entrega | Estimado |
| :---- | :------ | -------: |
| P1 | Referências e dependências | 3 h |
| P2 | Reservas, índice e listagem | 4 h |
| P3 | Skills e norma | 2 h |
| P4 | Fontes de medição e sessão | 2 h |
| P5 | Script e fixture de migração | 3 h |
| P6 | Publicação, sync e aplicação no acervo | 2 h |
| P7 | Revisão independente e fechamento | 2 h |

O plano está em execution/in_progress, ready sim, com estimate_h 18, executed_h 0 e remaining_h 18. Esses números
medem os passos; nenhum foi executado. P1 aguarda pedido explícito. Conferência desta gravação: checador das notas
e diff; as suítes de implementação não foram rodadas novamente por esta alteração documental.
