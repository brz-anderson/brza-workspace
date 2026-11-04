---
scope:
  - workspace
refs:
  - MIG-001
  - PLN-008
  - REV-001
  - REV-004
  - issue:brza-shot-quebra-com-os-tokens-do-painel-movidos
  - issue:o-brza-sessions-abre-na-conta-ativa-do-app
---

# PLN-008 P8: o termo neutro no `brand`

O pedido da sessão `workspace-a6`, em 2026-11-03: o P8 (D11) do
[PLN-008: O worklog cita no refs os planos, issues, revisões e migrações que toca](../../plans/PLN-008-o-worklog-cita-os-refs/PLN-008-plan.md)
no workstream `brand` — tirar dos arquivos atuais o nome do workspace de origem, pelo termo neutro, e recomitar o
worklog da aplicação da MIG-001, cujo `refs` muda com o extrator novo (`brza-workflow@30b3666`, R14.3). A autorização é
de Anderson, de 2026-11-03: "sim", à pergunta "Posso abrir as sessões?" do D11. O PLN-008 mora no `workspace`; daqui
não foi editado.

## O que se fez

1. **Árvore limpa:** `git status --short` saiu vazio; nenhum arquivo sujo de outra sessão.
2. **Levantamento:** o `git grep -il` do nome, fora do `.brza/index.jsonl`, deu quatro notas, nenhuma com o nome no
   caminho e nenhuma de norma. Não há link do `brand` para os arquivos do mapa de nomes dos outros workstreams.
3. **Troca, frase a frase:**
   - O e-mail da conta de administração virou "a conta de administração (`~/.claude-adm`)", e o da conta padrão saiu,
     porque a frase já dizia "conta padrão". A citação de Anderson "em sessão própria, na conta …" ficou só com "em
     sessão própria" entre aspas, e a conta foi para fora delas.
   - "A issue das skills de documento" passou a dizer "do workspace de origem".
   - Arquivos: [O brza shot quebra com os tokens do painel movidos no brza-studio](../issues/brza-shot-quebra-com-os-tokens-do-painel-movidos.md),
     [O brza sessions abre a sessão na conta ativa do app, e não na da sessão de origem](../issues/o-brza-sessions-abre-na-conta-ativa-do-app.md),
     `2026-11-02-os-plugins-da-orca-1-4-246-e-os-planos.md` e `2026-11-02-pln-007-o-desenho-da-marca-brza.md`.
4. **Recommit do worklog da MIG-001:** `2026-11-03-mig-001-a-aplicacao-no-brand.md` perdeu REV-001 e REV-004 do
   `refs`, que só vinham do texto do link para a MIG-001; ficaram MIG-001 e PLN-008.
5. **Checador:** `check_notes.py` com 64 arquivos, 0 links não resolvidos, 0 erros e 0 avisos.
6. **Commit** `2c18797` na `origin/workstream/brand`, pelo `brza note commit`, só os cinco caminhos.
7. **Conferência final:** o `git grep -il` do nome, fora do `.brza/index.jsonl`, saiu vazio (código 1). Não sobrou
   nada, nem norma, nem `refs`/`depends_on` com as duas exceções da R17.1.

## Pendente

Nada no `brand`. Não houve link para segunda passagem; a sessão fica aberta, se a `workspace-a6` pedir.
