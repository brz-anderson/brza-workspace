---
name: custos-e-premissas-que-erraram
description: Premissas de rodada que a medição desmentiu no PLN-012 (ps -S, turno do commit) e no PLN-013 (catálogo de modelos do app, cota do Grok)
metadata:
  type: project
---

Duas premissas que foram à rodada do PLN-012 (R1.2, R1.4) com preço apresentado caíram quando medidas, em 2026-11-03:

- **`ps -S` não soma a CPU dos filhos de outro processo no macOS** (Darwin 27): `ps -S -o time -p <pid>` sai igual sem
  o `-S`. O que funciona é `proc_pid_rusage(pid, RUSAGE_INFO_V4)` da `libproc`, por `ctypes`: `ri_child_user_time` e
  `ri_child_system_time` contam filhos e netos colhidos, em unidades de `mach_timebase_info`. Para quem espera o comando,
  `getrusage(RUSAGE_CHILDREN)`, com `ru_maxrss` em bytes.
- **"A linha não traz o turno do próprio commit" parecia barato e não é**: a mediana da tarefa tem ~77% do custo e ~88%
  da duração no turno que commita, e ~44% das tarefas são de um turno só, porque a rodada segura o turno aberto.

No PLN-013 (mesmo dia), duas premissas do Terreno e das rodadas caíram quando conferidas no Desenho:

- **O catálogo de modelos do app fica atrás do runtime.** O seed do Codex no `brza-studio` lista `gpt-5.6-*`; o
  `~/.codex/models_cache.json` e o `~/.codex/config.toml` de Anderson já estão em `gpt-6.1-sol`. Para valores de
  modelo, a fonte é a lista do próprio runtime: `~/.codex/models_cache.json`, `grok models`, `agy models`.
- **Login não dá cota.** A R1.2 e a R2.1 contavam com a cota do Grok "depois do `grok login`"; com o login feito, o
  `rateLimits.grok` sai `status: unavailable`, sem janela, e o Grok fica em `quota_unknown`.

**Why:** as duas entraram na rodada como fato do Terreno, sem teste; o custo de "deixar de fora" foi dito sem medir.

**How to apply:** antes de pôr na rodada uma opção que depende de comportamento de ferramenta do sistema ou de "fica de
fora uma parte", rode o teste barato (um comando, um script sobre o `.measurements/`) e diga o tamanho da parte.
