---
scope:
  - workspace
refs:
  - PLN-004
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

## O que ficou

- **A R17 de volta**, com o Grok no P10 (o `~/.zshrc` e o `brza install`) e no P11 (a conferência do override), e o
  **Desenho reescrito** com o `.brzAgents` e o Grok, que vai à aprovação na mensagem antes de virar
  `PLN-004-design.md`. Está no `Retomar` do plano.
- **A qualidade do Grok como revisor** segue sem medição separada: uma corrida por célula, e faltam o 4.7 em convenção e
  as duas em simplicidade.
- **O vocabulário do `.grok/rules/runtime.md`** (o que no Grok faz a pergunta com opções, o correio, o scratch) sai no
  Desenho; o levantamento mediu as 26 ferramentas do agente, sem `Skill`.

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
