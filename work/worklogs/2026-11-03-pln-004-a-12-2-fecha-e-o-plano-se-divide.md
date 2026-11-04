---
scope:
  - workspace
refs:
  - PLN-004
---

# O PLN-004: a R12.2 fecha e o plano se divide

Anderson respondeu "recomendado" à R12.2 revista, em 2026-11-03, na sessão `workspace`. O plano é o
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md);
o dia anterior está em
[O PLN-004: a revisão do plano contra a migração ao brza-workflow](2026-11-02-pln-004-a-revisao-contra-o-pln-006.md).

## O que se fez

- **A R12.2 decidida:** o Claude é o runtime padrão de revisão nos três focos; o `agy` e o Codex entram como segundo
  passe, pedido por quem pede, com `--runtime` além do `--focus`; não há mapa foco → runtime. A medição que a sustenta
  está no worklog de ontem: o recall do `agy` no defeito foi de 0,40 a 0,20 entre as duas execuções, e o do Claude de
  0,20 a 0,30, então a vantagem que justificaria dobrar o defeito não se repetiu; a convenção do Claude ficou em 1,00
  nas duas.
- **O plano se dividiu**, como manda o `plans/README.md` (passava de 400 linhas, e tinha 670): a Entrevista, R1 a R12,
  foi para [PLN-004 — Entrevista](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-interview.md), e o `-plan` ficou
  com 92 linhas. O `Retomar` foi reescrito, e o checador das notas passa sem erro nem aviso.

- **O `designer` reescreveu o Desenho** (`pln-004-design-v2.md`, no scratch) e devolveu 11 pontos sem lastro, em 4
  rodadas. A **R13** e a **R14** foram respondidas e gravadas na Entrevista: a norma do pacote fica no pacote, o sync
  renderiza o `.toml`, o `codex-brza` usa o `tomllib`, o mapa do `agy` vai por `pro`/`flash` no papel e
  `gemini-4-argon-high` na revisão, e o Codex revisa em `gpt-6-astra` com `high` (variante de Anderson, sem o `high`
  medido).

- **A R15 e a R16** foram respondidas e gravadas. R15: o `brza delegate` usa o papel e o `--runtime` é obrigatório. A
  15.3 virou a contraproposta de Anderson, o `.brzAgents`, e um `collector` mediu o custo (36 arquivos e 104 linhas no
  `brza-workflow`, nenhum no `brza-studio`; o Claude, o Codex e o `agy` leem `agents` e `skills` por link; o D15 falha
  na transição de diretório para link; a gravação da memória do subagente pelo link foi negada em 3 de 3 `claude -p`).
  R16: `agents`, `skills` e `memory` em `.brzAgents/`, a memória literal (16.1.3, não a recomendada), o link de
  diretório para as skills e o D15 emendado.

- **A sonda de saída da memória e a sessão interativa** (R16.5): em `claude -p` nenhuma de seis variantes gravou atrás
  de link (US$ 0,095); com um host de permissão respondendo, o link gravou nas 3 gravações, mas **perguntou 3 vezes**, sem
  como silenciar na sessão (US$ 0,041). Anderson escolheu a memória real em `.claude/agent-memory/`, com
  `.brzAgents/memory` como link para ela, e a 16.1.3 ficou substituída.

- **O levantamento do Grok** (a pedido de Anderson, "agora temos que inserir também o `Grok`"): um `collector` mediu o
  Grok Build CLI 1.0.70 eixo a eixo, em `/private/tmp/pln004/grok/levantamento.md` (103 fatos). O Grok lê `AGENTS.md` e
  `CLAUDE.md` juntos (sem `@import`), `.claude/rules`, `.claude/skills` e `.agents/skills` (link de diretório vale),
  `.claude/agents/*.md` e roda os hooks do `.claude/settings.json`; mas **sem confiança de pasta não carrega nada de
  projeto**, e o app não pré-confia o Grok. Gasto das sondas: US$ 0,509 em 6 turnos, mais os de `grok inspect` sem modelo.

## O que ficou

- **A R17**, a medição e a máquina (P8 a P11), e o **Desenho reescrito com o `.brzAgents`**, que vai à aprovação na
  mensagem, em 3 partes, antes de virar `PLN-004-design.md`; na gravação, corrigir no `-plan` o "Fora de escopo" (ainda
  manda o código ao `tools-kit`) e a Cobertura (ainda diz "um foco por runtime"), e a revisão do Codex no D11 para `high`.
- **O turno do `agy` com `model: pro`**, que lê o `modelName` do `Stop`, fica para o D7 (R14.1).
- **O `high` do Codex não foi medido:** a R12.2 mediu só `xhigh`.
- **A migração para o `.brzAgents`** muda o `core/` do `brza-workflow` (16 `git mv`, 14 fixtures do ouro, o sync) e,
  com a memória literal, `git mv` de 55 arquivos de memória em 4 branches; tudo a executar só a pedido de Anderson.

## Fora do workspace

- **O `~/.grok` mexido pelas sondas do Grok** (23:23 em diante, 2026-11-03): 16 sessões novas em `~/.grok/sessions` (dos
  diretórios de sonda em `chat-scratch/…/grok/p1`, `p4` e `p5`), mais `sessions/sandbox-events.jsonl` e cinco arquivos
  vazios, `bundles/`, `hooks/`, `hooks-paths`, `sandbox.toml` e `trusted_folders.toml`, que a primeira corrida sob
  `--sandbox` criou.
  - **Risco:** o `sandbox.toml` e o `trusted_folders.toml` vazios podem ser lidos pelo Grok do app como configuração;
    as sessões somam histórico fora do git. `auth.json` não foi aberto, e a `memory-v2` não foi tocada (`GROK_MEMORY=0`).
  - **Estado:** ativos, parados.
  - **Desfazer:** apagar os cinco arquivos vazios e as 16 sessões das sondas, que o fim do `levantamento.md` lista.
- **Os transcripts do `agy` das sondas da R16**, em `~/.gemini/antigravity-cli/brain` (ids `0ba003d1-5b11-47da-ae9c-c7f552d3d7d4`
  e `542ce7a2-3b6b-44b1-82f1-61d2643b6b9e`).
  - **Risco:** guardam os prompts das sondas, fora do git.
  - **Estado:** ativos, parados.
  - **Desfazer:** apagar os dois diretórios.
