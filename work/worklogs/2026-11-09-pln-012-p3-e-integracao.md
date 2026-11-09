---
scope:
  - brza-workflow
refs:
  - PLN-012
  - REV-021
---

# PLN-012: o P3 e a integração da medida por tarefa

Anderson pediu em 2026-11-09, nesta sessão: "Retomar PLN-012, execute todos os passos, menos o P6".
Retomada do
[PLN-012: Cada tarefa sai com o tempo corrido, o custo e a máquina que gastou](../../plans/PLN-012-cada-tarefa-com-tempo-custo-e-maquina/PLN-012-plan.md).
Os bloqueios dos outros workstreams foram conferidos: nenhum alcança esta entrega.

## O que se fez

- P3 implementado em `brza-workflow@4119ec1`: `sessions:`, evento `task`, corte `--until` validado antes de alterar
  o worklog e `## Medida` acumulada pela mesma função do resumo. A prévia do turno lê transcript e CPU sem alterar
  o estado do hook. Sem sessão Claude, o evento leva `session_id: null` e a seção não é escrita.
- P5.6 no mesmo commit: `close-task` passa o workstream ao `--pending`, inclusive quando ainda não há turno fechado.
- Dois defeitos encontrados pelo revisor foram corrigidos com regressões: worklogs intactos numa pasta não
  recebem metadados novos; o evento usa o SHA resultante do rebase e conserva o marco quando fetch ou push falham.
- Integração em `fdf266d` e merge com a `master` em `d38e7b4`, sem conflito com os dois commits posteriores ao início
  do plano. Checkout principal atualizado e push atômico da `master`, da integração e da branch P3 concluído.
- O P6, incluindo `brza sync`, não foi executado. O plano continua em execução; o `.brza/core.lock` permanece em
  `ebb4e7d`.

## Revisão

A aprovação automática bloqueou a chamada ao `agy` por possível envio de código privado a serviço externo.
Anderson escolheu: "Usar somente um subagente interno nesta execução". O `reviewer` independente aprovou após as
duas correções, registradas em
[REV-021: O P3 e o ajuste do P5.6 do PLN-012](../reviews/REV-021-pln-012-p3-carimbo-e-medida.md).

## Validação

- Base da `master`: 492 testes de CLI OK. Integração: 526 testes de CLI OK. Árvore final mesclada: 528 testes de CLI
  OK, por `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/cli`.
- Note e índice: 154 testes OK; classe final `TaskCommitTest`: 22 testes OK.
- Hooks: 348 testes OK no Python 3.15 e no Python 3.9 do macOS, com cinco exclusões previstas neste último.
- Checador do workflow: 113 verificações OK. Scripts locais: 113 testes OK; o sandbox bloqueou `ps` e Chrome,
  e a execução com essas permissões passou.
- `git diff --check`: limpo. Checador das notas do workstream: zero erros, avisos ou links não resolvidos.

**Executado:** P3, cerca de 0,3 h; fechamento do P5 nesta retomada, cerca de 0,1 h. O P5 já tinha 0,9 h registradas.

## Fora do workspace

- **O quê e onde:** clones de implementação e integração em `/private/tmp/pln-012-workflow` e
  `/private/tmp/pln-012-baseline`, com logs `/private/tmp/pln-012-*.log` e fixtures temporárias dos testes.
  **Risco:** cópias locais de código privado permanecem no disco temporário. **Estado:** clones e logs preservados
  para conferir a entrega; fixtures dos testes são descartáveis. **Como desfazer:** remover esses clones e logs.
- **O quê e onde:** checkout `~/Projects/brza-workflow` atualizado, nos arquivos de código,
  norma e testes do PLN-012. **Risco:** atualizar esse checkout muda a CLI ligada por symlinks; os hooks do workspace
  só chegam pelo P6. **Estado:** merge `d38e7b4` ativo na `master`, enviado ao GitHub. **Como desfazer:** um novo commit que reverta esse merge
  e o respectivo push.
