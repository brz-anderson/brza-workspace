---
name: verbo-mcp-adaptador-sobre-o-cli
description: Critério de Anderson para verbos do brza-orchestrator (PLN-020, 2026-11-09) — uma fonte só, o CLI é o motor; e as armadilhas que achei ao desenhar adaptadores de escrita
metadata:
  type: project
---

Em 2026-11-09 (PLN-020, `playground`), Anderson decidiu que os verbos MCP são adaptadores sobre o `brza note`. A
skill chama o verbo e cai no CLI com o daemon fora (R1.2 mantida na R4.1). Os fluxos longos ficaram nas skills
distribuídas, e o MCP cobre só o que o client não faz sozinho (R4.1, "saem do plano").

**Why:** o critério que venceu na R1.1 foi a portabilidade entre clients, e a sonda (M1–M11) mostrou que as skills já
chegam ao Codex, ao Cursor e ao Antigravity. O que nenhum client faz sozinho é o ambiente: o `.git` fora do sandbox,
a sessão e a identidade.

**How to apply:**
- **A conferência fica no motor.** Toda conferência de verbo (frase de decisão, filtros do índice) mora num subcomando
  do CLI com `--json`; o verbo só o chama em subprocesso. Conferência só no verbo some na reserva do CLI.
- **O valor do MCP de escrita é estar fora do sandbox.** Prefira que o client escreva o arquivo e o servidor só
  commite (entrada por caminho): assim o client sem permissão de disco não ganha escrita pelo servidor.
- **A sessão vem do client.** O daemon do launchd não tem o `env` da sessão, então o client a declara em argumento.
- **Confira o daemon antes de prometer ganho.** Em 2026-11-07 e 2026-11-09 ele estava carregado sem processo, e
  nenhum client tinha o servidor configurado.

Pendente: a resposta das rodadas P1–P9 do rascunho de D3–D6. Registre aqui o que Anderson escolheu e a recomendação
recusada. Ver [[criterio-cliente-com-shell]].
