---
name: custos-e-premissas-que-erraram
description: Premissas e custos de rodada que a medição desmentiu no PLN-012 — ps -S no macOS e a linha do worklog sem o turno do commit
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

**Why:** as duas entraram na rodada como fato do Terreno, sem teste; o custo de "deixar de fora" foi dito sem medir.

**How to apply:** antes de pôr na rodada uma opção que depende de comportamento de ferramenta do sistema ou de "fica de
fora uma parte", rode o teste barato (um comando, um script sobre o `.measurements/`) e diga o tamanho da parte.
