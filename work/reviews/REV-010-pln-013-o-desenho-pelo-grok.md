---
status: done
description: Segunda revisão do rascunho do Desenho do PLN-013, por duas sessões Grok 4.7, com 15 achados corrigidos no Desenho e um falso
scope:
  - brza-workflow
opened: 2026-11-03
completed: 2026-11-03
tags:
  - tooling
---

# REV-010: O Desenho do PLN-013, revisado pela sessão Grok

O parecer do rascunho do Desenho do
[PLN-013: O Grok, o Codex e o Antigravity abrem pelo `brza sessions` e recebem tarefas do MCP](../../plans/PLN-013-grok-codex-e-agy-no-brza-sessions-e-no-mcp/PLN-013-plan.md),
antes de qualquer passo. O rascunho, D1 a D7 com os pontos P1 a P7, foi de um `designer`. A revisora foi a sessão Grok
`pln-013-grok-revisor` (Grok 4.7, `high`), aberta pelo `brza sessions --agent grok` a pedido de Anderson ("utilize ela
como segunda revisora e para desenhar sugestões"), só leitura. O parecer completo ficou no scratch da sessão; aqui vai
cada achado com a evidência.

A sessão que conduz conferiu no código o A3, o A4, o A5 e o A7 antes da R4. Os destinos são todos `corrigido aqui`: o
achado é defeito do rascunho, e não escolha, e entra na reescrita do Desenho do PLN-013. As alternativas do revisor nos
pontos P1, P2, P4, P5, P6 e P7 foram à R4 do plano, ao lado das do `designer`, e Anderson respondeu "todos
recomendados, siga".

## Achados

### A1 — O `--wait` do Grok lê um campo de título que o `summary.json` não tem

> bug · importante · confiança 92 · → corrigido aqui

O nome que o `grok -r` usa mora em `generated_title`, e só fica estável com `title_is_manual: true`; sem ele, o
auto-título reescreve o campo nos primeiros turnos. A sessão aberta pelo app grava o cwd do scratch do app, e o
`grok -r <nome>` rodado no worktree não a acha.

**Evidência:** `~/.grok/docs/user-guide/17-sessions.md:46`, `:100-106` e `:433-434`; nos 19 `summary.json` de
`~/.grok/sessions/`, nenhum tem a chave `title`, e os 9 com título usam `generated_title`; o rascunho usava
`grok_title(sid) == name` em `summary.json`.

### A2 — O `/rename` como primeiro prompt não está provado no chat ACP do Grok

> lacuna · importante · confiança 85 · → corrigido aqui

O app sobe `grok agent stdio` e manda o texto em `session/prompt`, sem chamar `x.ai/session/rename`, e deixa vazio o
catálogo de comandos do Grok. A premissa: o `slash_exec` do ACP pode ou não executar o texto; só a sonda da R3.4 diz.

**Evidência:** `brza-studio/src/main/acp/acp-launch-specs.ts:143-151`;
`brza-studio/src/shared/native-chat/native-chat-agent-profiles.ts:55-58` e `:86-88` ("Grok remains skills-only until
its command catalog is verified"); `strings` no `grok` 1.0.70 acha `x.ai/session/rename` e `slash_exec.rs`.

### A3 — O id gravado pelo `--wait` não chega ao `list`

> bug · importante · confiança 95 · → corrigido aqui

**Evidência:** `brza-workflow/packages/client/bin/brza-sessions:105-106` — o `session_map` só copia `claude_session`
do evento `session`; conferido pela sessão.

### A4 — A recusa de `account` da E1 barraria todo despacho fora do Claude

> bug · importante · confiança 95 · → corrigido aqui

A condição `'account' in fields`, posta depois do `setdefault`, vale para todo pedido; o teste proposto só mandava
`account` explícito e ficaria verde com o defeito.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/tools.py:226` — `fields.setdefault('account', '')`; conferido pela
sessão.

### A5 — A troca do Codex disputa o motivo do gate e cai dentro do lock da fila

> bug · importante · confiança 90 · → corrigido aqui

O `gate_reason` já devolve o motivo do papel, e o rascunho o trocava pelo da troca. O `select_codex` "antes do UPDATE"
ficaria dentro do `queue.lock`, que o próprio arquivo evita para leitura de conta.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/tools.py:259-268` (`gate_reason`), `:277` (o lock) e o comentário da
leitura fora do lock na linha anterior; conferido pela sessão.

### A6 — Uma escada de esforço por runtime aceita esforço que o modelo não tem

> bug · importante · confiança 92 · → corrigido aqui

O `grok-4.5` não tem `xhigh`, e o `worker-start` recusa o esforço fora da escada do modelo. Com `--model` e sem
`--effort`, o app emite `--reasoning-effort high`.

**Evidência:** `~/.grok/models_cache.json:40-69` e `:271-293`;
`brza-studio/src/shared/agent-session/options/agent-session-option-catalog-grok.ts:71-74` e `:87`;
`brza-studio/src/shared/agent-launch-model-preferences.ts:36-37` e `:63-76`.

### A7 — O fallback do consultant fora do Claude contradiz o "padrão do runtime"

> bug · importante · confiança 92 · → corrigido aqui

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/policy.py:202-209`; `tests/mcp/test_mcp_policy.py:144-150` fixa o
papel desconhecido em `sonnet`/`low`/`default_role` no Claude; conferido pela sessão.

### A8 — Parte dos testes "que falham antes" da D3 já passa hoje

> desvio · sugestão · confiança 95 · → corrigido aqui

**Evidência:** `brza-workflow/packages/client/bin/brza-sessions:363` repassa qualquer `--agent`;
`tests/cli/test_brza_sessions.py:364-381` e `:404-410` saem verdes com `grok` hoje.

### A9 — O teste do contrato JSON do `list` quebra com o campo novo e não estava na D6

> lacuna · sugestão · confiança 92 · → corrigido aqui

**Evidência:** `brza-workflow/tests/cli/test_brza_sessions.py:412-426` compara o JSON inteiro, sem campo extra.

### A10 — A conta do Grok na E1 não casa com a da E2 no teto de sessões

> bug · sugestão · confiança 85 · → corrigido aqui

Na E1 o worker contaria na id ativa do Claude e, na E2, a conta dele vira `systemDefault`; o teto novo não veria o que
já roda. A premissa: o teto é por `(account, runtime)`.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/limits.py:177-190` (`_account` e `_sessions`).

### A11 — A soma de ~13,75 h é otimista

> desvio · sugestão · confiança 85 · → corrigido aqui

As horas não contavam o `session_map` (A3), o contrato JSON (A9), a escada por modelo (A6), o fallback que preserva o
teste do Claude (A7) e o RPC fora do lock (A5). A premissa: as horas do rascunho são as da R2.3 e da R3.

**Evidência:** a soma do rascunho, E1 ~5,25 h, E2 ~4 h e E3 ~4,5 h, contra os acréscimos acima; o revisor estima E1
~6,5 h, E2 ~4,5 h e E3 ~4 a 5,5 h.

### A12 — O `--wait` assume que o `providerSession.id` é o `info.id` do Grok

> lacuna · sugestão · confiança 80 · → corrigido aqui

A premissa: o `agentSession.history` de um chat Grok com login não foi lido; nas sessões ACP gravadas, o diretório é o
id do Grok.

**Evidência:** `~/.grok/sessions/…/01a1a45f-4311-7940-bce7-a9c1d9ed4e73/summary.json`, com `info.id` igual ao
diretório; `brza-workflow/packages/client/bin/brza-sessions:204-212` devolve None fora do Claude.

## A segunda leitura

O primeiro pedido de revisão foi à sessão Grok `grok_18ca2288…`, que estava no meio do P3 do PLN-011 e parada numa
aprovação. O pedido ficou na fila do `queue-if-active`. Anderson escolheu abrir a sessão nova, a `pln-013-grok-revisor`,
e o aviso para desconsiderar o pedido entrou na mesma fila, atrás dele. A sessão antiga também revisou o rascunho e,
às 23:47, gravou o parecer dela no caminho do primeiro, que se perdeu do scratch: os achados A1 a A12 acima foram
transcritos antes disso. Dos oito achados da segunda leitura, quatro já estavam acima (A1 → A6, A2 → A1, A3 → A2,
A7 → A11). Os outros quatro entram aqui.

### A13 — O papel sem linha fora do Claude ainda chama o desempatador Haiku

> bug · importante · confiança 93 · → corrigido aqui

O fallback do `decide_model` chama o resolver, que roda o Haiku pela conta do Claude, também para um pedido Grok.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/policy.py:202-209`; `brza-workflow/packages/mcp/brza_mcp/resolver.py:128-132`
— `argv = ['claude', '-p', '--model', 'haiku', '--effort', 'low', ...]`.

### A14 — O parse e o relatório de cota carimbam `runtime: 'claude'` em toda amostra

> bug · importante · confiança 90 · → corrigido aqui

O id `systemDefault` do Grok e do Antigravity é a mesma string da conta padrão do Claude; sem o runtime em cada
amostra, os usos se misturam.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/accounts.py:23-24` (`SYSTEM_DEFAULT`, `RUNTIME`), `:71`, `:75` e
`:240-242`; `queue.py:257` e `:284` separam por runtime quando o argumento vem.

### A15 — O fallback pelo prefixo `grok_` não casaria o id de sessão do Grok

> lacuna · sugestão · confiança 95 · → falso

**Por que é falso:** o prefixo que o `chats()` testa é o do id do chat no app, e não o `info.id` que o Grok grava em
`summary.json`.

**Evidência:** `brza sessions pln-013-grok-revisor --agent grok …` → `open: … grok_73108004_6199_43f2_b23f_3fd9a842e558`,
e o `session.tabs.listAll` dá `sessionId: "grok_18ca2288_…"` à outra aba Grok, ambos rodados nesta sessão.

### A16 — O teste do esforço recusado no Grok já falharia hoje pelo `ValueError`

> desvio · sugestão · confiança 88 · → corrigido aqui

Hoje a chave `policy.roles.<papel>.grok.effort` é recusada como desconhecida; um assert só do `ValueError` passa antes e
depois. O teste que falha antes afirma o texto da mensagem, que nomeia o modelo e a escada.

**Evidência:** `brza-workflow/packages/mcp/brza_mcp/policy.py:84` (o `_ROLE_KEY` de hoje) e o rascunho, que admitia
"hoje, recusado como chave desconhecida".
