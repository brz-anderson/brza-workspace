---
scope:
  - workspace
refs:
  - PLN-004
  - PLN-013
---

# O PLN-004: o Grok entra no plano

A sessão `workspace` retomou o
[PLN-004: Os runtimes Codex, `agy` e Grok trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-os-runtimes-codex-agy-e-grok-no-fluxo/PLN-004-plan.md)
no pedido de 2026-11-03 ("agora temos que inserir também o `Grok`"), que esperava a rodada sobre o levantamento do
`collector`. A sessão anterior está em
[O PLN-004: a R12.2 fecha e o plano se divide](2026-11-03-pln-004-a-12-2-fecha-e-o-plano-se-divide.md).

## O que se fez

- **A R18, respondida "as quatro recomendadas":** o Grok entra no PLN-004; a pasta fica confiada por um wrapper
  `grok-brza` com `GROK_FOLDER_TRUST=0`, que é também o `agentCmdOverrides.grok` do app; o adaptador mora em
  `.grok/rules/runtime.md`, no pacote; e os hooks do núcleo saem cedo com `GROK_HOOK_EVENT`, com um
  `.grok/hooks/runtime.json` do pacote chamando o `measure_runtimes.py grok`.
- **O plano renomeado** para "Os runtimes Codex, `agy` e Grok…", pelo `move_note.py` (7 links reescritos em 6 notas), com
  a frase de 2026-11-03 no Pedido e três linhas novas na Cobertura (`R18.2` a `R18.4`).
- **A R19:** a 19.1 (`GROK_MEMORY=0` no wrapper), a 19.2 (os papéis herdam o modelo do pai) e a 19.4 (o Grok no D12)
  na recomendada; a 19.3 voltou como "medição primeiro".
- **A medição da 19.3**, pelo `collector` (US$ 4,84, teto de US$ 6; `/private/tmp/pln004/bench/out/pontuacao-grok.md`):
  só o `--sandbox read-only` barra a escrita no sistema, sem estorvar a revisão; no banco da R12.2, o foco defeito deu os
  mesmos dois reais com `grok-4.7` em `high` (US$ 2,51) e `grok-4.6` em `medium` (US$ 1,28), recall 0,20, igual ao do
  Claude; o 4.6 na convenção deu 0 real. Três das seis corridas não rodaram, pelo teto. Conferi no disco o custo de cada
  JSON, o `ref-pln005` limpo e o "Operation not permitted".
- **A 19.3 refeita, respondida na recomendada:** `grok -p --permission-mode plan --sandbox read-only --output-format
  json -m grok-4.6 --effort medium`, nos dois tipos do `brza delegate`.

- **A R17 de volta, com o Grok:** a 17.1, a 17.2 e a 17.4 na recomendada (o `fact_audit_runtimes.py` no pacote, a
  tabela "Por runtime" no resumo do núcleo, o override conferido só por não estar vazio); a 17.3, "Sessão aplica tudo",
  contra a recomendada: a sessão aplica o `~/.zshrc` e roda o `brza install`, depois do "pode aplicar" de Anderson no
  passo, o que substitui, para o `~/.zshrc`, o "Anderson edita" da R11.2.
- **O Desenho v3**, pelo `designer` (`/private/tmp/pln004/pln-004-design-v3.md`, 1059 linhas): as R16 a R19 aplicadas,
  a revisão do Codex no D11 em `high`, e nove pontos sem lastro. Conferi no disco o que as rodadas usaram: o
  `brza-studio` em `cb573ba`, o `agy` 1.5.2, o `grok agent` sem `--rules` nem `--sandbox`, e a 15.3 ainda aberta.
- **O PLN-013 do `tools-kit`**, fechado em 2026-11-04, entregou mais do que o v3 dizia: além do `--agent` dos quatro no
  `brza sessions`, o `dispatch` do MCP aos workers do Grok, do Codex e do Antigravity, com `grok-4.7` nos três papéis
  do `brza.toml`. O PLN-004 não o tratava, e virou a 20.1.
- **A R20, respondida "as quatro recomendadas":** o `brza delegate` e o `dispatch` do MCP ficam lado a lado, com papéis
  distintos; o papel chega ao Grok por `--agent <papel>`, com um turno de prova; o Grok comita como o Claude; o `brza
  tree` copia o `.grok/rules/runtime.md` para o worktree do `brza-studio`.
- **A memória do `designer`** ganhou as trocas da R13 à R19 e o que o v2 deixou envelhecer, entre elas conferir o `git
  log` e os planos dos outros workstreams antes de reescrever um `D` que toca código comum.

## O que ficou

- **A R21, não enviada**: Anderson parou as rodadas ("sem mais rodadas por ora, apenas registre no plano"). Os cinco
  pontos — o texto dos focos (a 15.3), o núcleo e o `.brzAgents/`, o `agy` no `brza sessions`, o scratch do Grok e as
  issues de medida do `tools-kit` — estão no `Retomar` do plano, com as opções no v3.
- **A qualidade do Grok como revisor** segue sem medição separada: uma corrida por célula, e faltam o 4.7 em convenção e
  as duas em simplicidade.
- **O scratch do plano** (`/private/tmp/pln004/`, com o v2, o v3, os levantamentos e o banco) não vai ao git, e some se
  a máquina reiniciar.

## Fora do workspace

- **As sessões do Grok da medição da 19.3** (2026-11-06, 18:30 em diante): 4 pastas novas em `~/.grok/sessions` (cwd
  `grok/ro/v-plan`, `v-sandbox`, `v-both` e `bench/ref-pln005`), com 8 sessões das sondas e 3 do banco.
  - **Risco:** guardam os prompts e as revisões, fora do git.
  - **Estado:** ativos, parados.
  - **Desfazer:** `grok sessions delete <id>`, ou apagar as quatro pastas.
- **`~/.grok/managed_config.toml` e `~/.grok/requirements.toml`**, criados vazios às 18:57 pelo CLI, durante as corridas.
  - **Risco:** o Grok do app pode lê-los como configuração; vazios, não mudam nada que se tenha visto.
  - **Estado:** ativos, parados.
  - **Desfazer:** apagar os dois, de 0 byte.
- **Os arquivos que as sondas de 2026-11-03 criaram em `~/.grok`** (`sandbox.toml`, `trusted_folders.toml` e os outros
  três vazios) seguem lá, como o worklog anterior registra.
- **As sondas do `designer` para o v3** (`grok inspect --json` sem turno em `/private/tmp/pln004-cs/p8/`, um link para o
  chat-scratch, e `agy agents` em repositórios de sonda) não mexeram no `~/.grok`: o `sessions` segue com 26 pastas e o
  `trusted_folders.toml` não mudou. Nada a desfazer além do scratch.
