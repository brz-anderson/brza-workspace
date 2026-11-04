---
name: reference-workspace-de-origem-chats-onde-mora
description: Onde moram as peças do plano de chats do workspace de origem (Codex/agy) e as da contraparte no brza-workspace; atalhos de leitura e fontes que envelhecem
metadata:
  type: reference
---

Mapa para levantamento de Codex/agy neste workstream (confirmado em 2026-10-30; confira que os caminhos ainda existem).

**Workspace de origem (o repositório dele, ao lado deste)**
- Plano com tudo por passo: o `plan.md` do plano de chats (926 linhas; `Desenho` :89-365, `Passos` :367-765, `Desvios` X1–X9 :767-828). A Entrevista (o `interview.md` dele, 864 linhas) só vale
  para as respostas literais: R27 :729, R28 :776, R33 :842. o `design-orca.md` é do Orca, irrelevante para o brza-workspace.
- Revisão R27 em tabela de 59 linhas: a revisão dele em `work/reviews/` (mais rápido que o plano para saber por que P4/P5/P8.5/P9 reabriram).
- Peças em disco: `.codex/{config.toml,hooks.json,agents/}`, `.agents/{rules/runtime.md,hooks.json,mcp_config.json,plugins.json,agents/}`; geradores em
  `<plugin>/scripts/generate_{codex,agy}_agents.py` + `agent_frontmatter.py`; guarda em `<plugin>/hooks/`; medição em `.claude/hooks/measure.py` (`codex_measure` :468, `agy_measure` :618) e
  testes `.claude/hooks/tests/test_measure.py`; resumo por runtime em `<plugin>/scripts/summarize_measurements.py`.
- Delegação a outro runtime (frente "só leitura"): `scripts/delegate.py` + `scripts/quota.py` e a decisão `work/decisions/delegacao-da-sessao-claude-ao-codex-ao-agy-e-a-adm.md` — NÃO é o plano de chats, é outro plano de lá.
- Funções do shell: `~/.zshrc`, a função de localização :15, `codex()` :79, `agy()` :92.

**brza-workspace (contraparte)**
- Não há `.codex/` nem `.agents/`. `measure.py` daqui não tem `runtime` nem modo codex/agy; tem `workstream`/`memory`/`rounds` (o de lá tem o inverso: `runtime`, `API_PRICES`, `origin`, cota; sem `workstream` nem `memory`).
- Fonte dos papéis: `.claude/agents/*.md` (frontmatter `memory: project`); `scripts/brza/brza_runtime.py:276 agents_json` já converte o frontmatter.

**Fontes que envelhecem**
- O texto do plano de chats diz 0.163 e agy 1.4.1/1.4.2; o Terreno fala em `token_count` mas o código usa `token_usage_record`. Confie no código e nos rollouts.
- O README do brza-workspace (bloco de funções do shell) está à frente do `~/.zshrc` instalado (`brza_where` imprime `yes` lá, `workspace|studio` no README).
- `agy` se atualiza sozinho ao rodar qualquer subcomando (1.4.8 → 1.4.12 durante um levantamento): não chame `agy` à toa e avise o worklog "Fora do workspace" se chamar.

**Atalhos**
- `codex debug prompt-input "x"` com `CODEX_HOME=$(mktemp -d)` mostra o que o Codex carrega no cwd sem tocar o estado real (sem `timeout` no macOS; redirecione a saída para arquivo e leia com python `-I`).
- Contagem de nomes de ferramenta do agy por dia: varrer `~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript_full.jsonl` (campo `tool_calls[].name`); `strings` no binário de 190 MB passa de 2 min, use `grep -a -c -F`.
- WebFetch de `developers.openai.com/codex/*` redireciona (308) para `learn.chatgpt.com/docs/…`; o `config-reference` 404.
