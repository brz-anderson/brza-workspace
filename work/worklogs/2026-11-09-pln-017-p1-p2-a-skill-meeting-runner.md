---
scope:
  - workspace
tags:
  - tooling
refs:
  - PLN-017
---

# PLN-017 P1 e P2: a skill `meeting-runner` e o gerador do painel

Pedido da coordenação, por Anderson, em 2026-11-08 (rodada 4, pergunta 2: "P3 agora e abrir a sessão de P1+P2"): executar P1 e P2 do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md), pela skill `skill-creator`. A sessão começou em 2026-11-08 e fechou em 2026-11-09 (o `reviewer` e os dois `implementer` pararam duas vezes no limite de uso da conta). Nada além de P1 e P2 foi feito.

## O que se fez

- **A skill** em `.claude/skills/meeting-runner/`, escrita depois de acionar `/skill-creator`: `SKILL.md` (199 linhas, descrição com o gatilho negativo "não use se você é uma persona", Passos 0 a 7, narração, v1 × v2, invariantes), oito `references/` (`briefing`, `persona`, `persona-worklog`, `round-request`, `synthesis`, `proposal`, `closing`, `narration`) e `evals/evals.json`.
- **Os scripts**, por dois `implementer` com contrato fechado, com testes `unittest`: `tally.py`, `wait_round.py`, `launch_persona.py`, `runtime_memory_check.py` e `panel.py` (`collect` e `render`, a partir do `panel_proto.py`). A suíte tem **149 testes**, todos verdes (`cd .claude/skills/meeting-runner && python3 -I -m unittest discover -s scripts/tests -p 'test_*.py'`), incluindo o aceite do `tally.py` contra as tabelas de `levantamento-processo.md` (confiança R1, voto R3, nota dos colegas, sala 61,8/56,5/57,2) e contra latência e custo reais (Muralha US$ 0,22 em 41 s; Régua 155 s e 661.376 tokens; Carvão R7).
- **Os moldes de P2:** a linha `**Posição:**` em toda seção de rodada, o `sintese-N.json` (`references/synthesis.md`), o ciclo de publicação (um arquivo por rodada, republicado na abertura, a cada chegada e no fechamento) e a conferência por PNG pelo Chrome headless (`references/narration.md`).
- **A R5 e a R6** (requisito novo de Anderson, 2026-11-08): as personas abrem como workers do Orca (fecham sozinhas ~2 min depois do `worker_done`, com "manter aberta"). Implementado no `launch_persona.py` (`--via worker-start|hybrid|agent-launch`, `--send`, `--release`, `--keep-open`, `--stop`) e no `wait_round.py` (`--source mailbox|marker`); o sinal de fim é `brza orchestration send --subject "fim-rodada-N" --body "persona:<slug>"`, o marcador no worklog segue como registro que o `tally.py` lê, e o `worker_done` só vai no encerramento. Lido do plano depois de a coordenação reescrever o D1 e o D2.

## A avaliação (laço da `skill-creator`)

Três casos determinísticos, com e sem a skill, em subagentes Sonnet; notas por script; benchmark e visor estático (`generate_review.py --static`, sem navegador). O espaço de trabalho ficou no scratch da sessão (`meeting-runner-workspace/`), fora do repositório.

| Iteração | Com a skill | Sem a skill | Tempo (com × sem) | Tokens (com × sem) |
| :-- | --: | --: | :-- | :-- |
| 1 (8, 9 e 6 expectativas) | 100% (8/8, 9/9, 6/6) | 88,9% (8/8, 9/9, 4/6) | 55,7 × 45,8 s | 65.362 × 58.067 |
| 2 (9, 10 e 6 expectativas), skill final | 100% (9/9, 10/10, 6/6) | 81,8% (8/9, 9/10, 4/6) | 68,1 × 45,8 s | 73.888 × 58.067 |

- **Na iteração 1 a skill só discriminou no caso 3.** O baseline sem skill achou no repositório os briefings e worklogs das reuniões anteriores e empatou nos casos 1 e 2. As expectativas novas da iteração 2 (o sinal de fim por `brza orchestration send`; o `tally.py` como fonte) vêm de regras que o repositório não tinha; os baselines da iteração 2 são cópia dos da iteração 1, porque o prompt não mudou. Memória gravada: `skill-evals-need-rules-the-repo-lacks`.
- **A skill custa +22 s e +16 mil tokens por tarefa** na iteração 2, contra um baseline que erra o que a regra nova corrige (a explicação do Fole 8,25 pelo `--exclude-rater Faísca`; o script da skill como método).
- **Uma expectativa minha estava errada**, não a skill: escrevi "a ordem das notas não muda" ao excluir a Faísca. Os dois agentes mostraram que a ordem do meio muda (Tição passa a Faísca; Lenha passa o Fole). Corrigi `evals/evals.json`; o levantamento do processo tem a mesma frase errada.
- **O corretor da expectativa nova** tinha um `or True` que a faria passar sempre; troquei por verificação real antes de rodar a iteração 2.

## A revisão pelo `reviewer`

Um `reviewer` (camada alta) revisou a skill inteira, depois de uma primeira passada interrompida pelo limite de uso: **2 bloqueiam, 15 a corrigir antes de usar, 8 de melhoria**, mais 12 hipóteses que caíram (XSS no painel, HTML ≥ 512 KB, `:root` no tema, Antigravity na média, `shell=True`, contradições com D1 e R2, tamanho do `SKILL.md`, laço infinito). Relatório completo fora do git, no scratch (`review-meeting-runner.md`); a memória do papel guarda os cinco lugares onde o erro se escondeu.

- **Corrigidos no código e testados:** B1 (custo e latência "da rodada" eram da sessão inteira: `--closed` no `collect`, rótulo "total da sessão" sem janela), B2 (a persona aberta como worker some do mapa do `brza sessions`: aviso, ids no manifesto como sobrescrita, `--send` por `brza orchestration send --to dispatch:<id>`), C1 (atribuição da mensagem à persona só por `dispatch_id` ou o token `persona:<slug>`), C4 a C7, C9 a C11, C13, C15, M1 a M4 e M6. O `implementer` provou os testes novos por 17 mutações (cada uma revertendo uma correção); não rodou os testes no código antigo, porque os scripts eram novos e sem cópia.
- **Corrigidos na documentação por mim:** C2 (o endereço `‹ --to coordenacao›` do briefing não era válido: o worker sem `--to` já fala com a coordenação), C3 (`worker-release` só vale para worker que já enviou `worker_done`; quem não respondeu se para com `worker-stop`), C8 (os comandos do `SKILL.md` não rodavam como escritos: a raiz padrão passou a ser a do git e os comandos levam o caminho completo), C12 e M8 (papéis no mesmo modelo, o Antigravity como especialista em runtimes contra a E-1), C14 (duas linhas do molde de rodada se contradiziam).
- **Não corrigidos:** M5 (o custo da coordenação é conta à mão, com um `agrega.py` que está fora do git: o `custos_coordenacao` do painel segue preenchido pela coordenação) e M7 (a sonda P4a.0 procura o `autoReleaseAt` antes do `worker_done`, quando ele ainda não existe: vai ao texto do P4a.0, que é do `tools-kit`).
- **As correções não foram revistas de novo pelo `reviewer`.** O que as sustenta: a suíte (149), as mutações do `implementer` e três conferências minhas depois: o `tally.py` dá o mesmo resultado rodado de três diretórios, o `--dry-run` do lançador nas três vias sai com o caminho certo do worktree (achei e corrigi um caminho duplicado, `…/playground/.worktrees/playground`) e o PNG do painel fechado e parcial a 736 px.

## O que não foi verificado

- **Nenhuma via de abertura com ciclo de vida foi testada contra o Studio** (`worker-start` e a híbrida): só `--dry-run`, `--help` e fakes. O formato do JSON do recibo do `worker-start` e do `check` não foi visto; a leitura é tolerante, com as chaves candidatas no docstring. É a sonda P4a.0 do plano, do `tools-kit`.
- **O `wait_round --source mailbox`** nunca rodou contra um Run vivo.
- **Nenhuma reunião real rodou pela skill** (é o P7). A skill está em v1, e o critério de promoção ao `core/` (duas reuniões sem desvio) não começou a contar.
- **A descrição não foi otimizada** (`run_loop.py`): por decisão do pedido, fica para depois da primeira reunião.
- **O `quick_validate.py` da `skill-creator` não rodou** (falta o módulo `yaml` nesta máquina); conferi o frontmatter e o tamanho à mão.
- **O visor da iteração 2 foi gerado, mas Anderson não o abriu**, então não há `feedback.json`: a nota é só a por script, que não cobre o que exige julgamento humano.
- **Dois defeitos cosméticos do painel, sem correção:** o cartão de custo da coordenação ignora o `--at` (num retrato de 21h29 mostra "até 21:32"), e o denominador "(4/6)" da sala conta o Antigravity que está fora da média.

## Divergência com a retomada de 2026-11-09

O worklog `2026-11-09-pln-017-retomada.md`, de outra sessão, rodou a suíte no meio das correções do `implementer` e registrou 102 testes com 7 falhas e 1 erro. Era o código antigo, no meio da edição; hoje são 149 verdes. Não editei aquele worklog.

## O que ficou

O pendente está no `Retomar` do plano: a sonda P4a.0, o ponto "quem cria o Run das personas" (`worker-start` em paralelo pode criar um Run por persona; a decisão é do plano), o comportamento do `--peek --wait` com a caixa nunca consumida (a coordenação pode chamar o `brza` uma vez por segundo) e a P7.

## Fora do workspace

Nada. Os arquivos de trabalho (espaço de teste, visores, PNG de conferência) ficaram em `/private/tmp` e no scratch da sessão; o Chrome headless só gerou capturas. Nenhuma sessão do Studio foi aberta e nenhum `brza orchestration send/worker-*` rodou de verdade.

## Candidata à norma

A memória `skill-evals-need-rules-the-repo-lacks` (a expectativa de um eval só discrimina com regra que o repositório ainda não tem) vale para toda skill deste workstream; fica como memória do `playground`. A frase "a ordem das notas não muda" do levantamento do processo está errada.
