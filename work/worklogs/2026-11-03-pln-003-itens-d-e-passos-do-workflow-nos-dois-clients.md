---
scope:
  - workspace
  - brza-studio
refs:
  - PLN-003
---

# O PLN-003: os itens D e os passos

Depois da R10 e da R11 em [O PLN-003: o painel de componentes](2026-11-03-pln-003-o-painel-de-componentes.md), a sessão
retomou o PLN-003 para ajustar as regras do Desenho, consolidar os itens `D` (D1 a D9), formular os riscos da fase 0
como hipóteses (H1 a H6, R7.3) e planejar os passos de execução (P0 a P14).

## O que se fez

- **Ajustes no [Desenho](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md):**
  - O M2 e a tabela de regras ("Regra × mecanismo") foram alinhados com a decisão
    [Uma sessão por frente de trabalho, sem trava de retomada e com o cache de 1 h](../decisions/uma-sessao-por-frente-e-sem-trava-de-retomada.md):
    sai a trava de retomada e o modelo passa a ser "uma sessão por frente", com o roteador reusando a sessão da frente ativa.
  - Registradas as hipóteses **H1 a H6** para medição na fase 0 (R7.3).
  - Redigidos os itens **D1 a D9** detalhando: CLI `brza` e repo público `brz-anderson/brza` (D1), índice da `master` (D2),
    plugin do Claude (D3), servidor MCP residente (D4), fila SQLite e os três tetos (D5), política e desempatador
    `tev1`+Haiku (D6), roteador de sessões e runtimes (D7), plugin do Orca com painel TSX e integração MCP (D8) e
    norma de arquitetura (D9).
- **No [Plano](../../plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-plan.md):**
  - Frontmatter atualizado para `ready: sim — os itens D e os Passos estão escritos; P0 aguarda sessão pln-003-p0`.
  - Estimativa total de 58.0 h somada entre os passos P0 a P14.
  - Tabela de Cobertura preenchida associando os 5 pedidos aos passos e níveis de teste.
  - Seção `## Passos` redigida com P0 (fase 0, hipóteses) a P14 (revisão e encerramento).
  - Seções de Regressão e Desvios adicionadas conforme o molde da `plan-runner`.

## Retomar

Executar o passo **P0 — Medição das hipóteses da fase 0 (H1 a H6)**, que roda sob pedido explícito de Anderson numa
sessão própria `pln-003-p0`.
