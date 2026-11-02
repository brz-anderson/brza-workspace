---
scope:
  - workspace
  - brza-studio
---

# O PLN-004: a revisão do plano contra a migração ao brza-workflow

Anderson pediu, na sessão `workspace`, em 2026-11-02: "revise o plano contra as mudanças feitas no `BrzA Studio`,
`brza-workspace` e `brza-workflow`". O plano é o
[PLN-004: O Codex e o `agy` trabalham no fluxo do workspace como o Claude](../../plans/PLN-004-o-codex-e-o-agy-no-fluxo/PLN-004-plan.md);
o dia anterior está em
[O PLN-004: as sondas da R6 e o Desenho do Codex e do agy](2026-10-31-pln-004-as-sondas-e-o-desenho.md).

## O que se fez

- **O levantamento**, pelo `collector`, com o agregado no scratch da sessão (`pln-004-revisao-mudancas.md`): 38
  citações do plano e do rascunho do Desenho conferidas contra o disco, 19 batem e 19 não, e uma linha por item `D1` a
  `D14` sobre onde o artefato mora hoje. Conferi por conta própria as que pesam: as linhas do app, os três focos no
  `reviewer.md`, o `brza-where` e o `~/.zshrc`.
- **O que a migração do PLN-006 mudou** para o plano:
  - **A norma comum é do núcleo.** O `AGENTS.md`, o `CLAUDE.md`, o `plans/README.md` e o `work/README.md` estão no
    `.brza/core.lock`; editá-los aqui trava o `brza sync` seguinte, e o `core/AGENTS.md` é molde, sem lugar para
    adaptador de runtime. O `README.md` é local.
  - **O sync só escreve o que é do núcleo** (`core/` e `packages/<nome>/core/`): o `.codex/` e o `.agents/` ficam
    intocados, e um pacote novo no manifesto é possível (`brza init --package`), mas só existe o `client`.
  - **O código do `brza` saiu do `brza-workspace`.** O `claude-brza`, o `brza-sessions`, o `brza-agents`, o
    `brza_runtime`, o `measure.py` com os testes e o `summarize_measurements.py` vivem no `brza-workflow`; o `repo_of`,
    o `roots` e o `inside` do `claude-brza` não existem mais, e o `brza install` só liga o `claude` como override. O
    `brza-tree` segue local.
  - **O bloco do shell é do pacote do cliente** (`packages/client/shell/brza.zsh`, com o `brza-where`): o defeito do
    `cd ""` deixou de existir, o `~/.zshrc` só faz `source` dele, e o `codex()` e o `agy()` do `~/.zshrc` continuam
    sendo só da Fixfy.
  - **O `fact_audit.py` e o `measure.py` são só do Claude:** o primeiro chama `claude -p --model haiku` e roda só no
    `SubagentStop` do `settings.json`; o segundo não tem modo `codex` nem `agy`.
  - **O `tools-kit`** não tem item do PLN-004, e o PLN-006 foi executado pela sessão `workspace` nos dois repositórios.
  - **O `brza-workflow` não tem `plans/` nem `work/`** e não cita Codex nem `agy`.
- **No app:** a issue `codex-como-subagente-no-chat-do-claude`, do `studio`, está como estava; o cartão de handoff do
  upstream (#36848) grava um `agent-handoff` quando o chat nativo roda `agent launch`, o que toca o "caminho 1" dela.
- **No plano:** o `Retomar` reescrito (dizia "R6 a R8", e a R9 já estava gravada), e a frente 4 com os três focos de
  revisão, que só estavam no `Retomar`, com a linha da Cobertura.
- **A rodada 10**, no chat, que reabriu a R1.1, a R2.1 e a R9.1: os arquivos do Codex e do `agy` vão num pacote
  `packages/runtimes` do `brza-workflow` (resposta de Anderson, não a recomendada); o código é executado pela sessão
  `workspace`, com `implementer`, e não pelo `tools-kit`; os hooks usam a `BRZA_WORKSPACE` do wrapper e, sem ela, o
  `brza-where` (42 ms de mediana, medidos); a medição dos dois runtimes vai num `measure_runtimes.py`. A rodada saiu com
  as alternativas só do Codex; Anderson perguntou por quê, e as opções foram reapresentadas para os dois runtimes.
- **Um fato do `brza-sync`**, lido e não rodado: ele só conhece os modos `100644` e `100755` (`bin/brza-sync:115`) e
  grava o blob como arquivo (`:323-331`), então um symlink do pacote chegaria como arquivo de texto. O `brza install`
  tem `packages/client/bin` fixo (`bin/brza-install:61`) e só liga `brza-*` e o `claude-brza`.

- **A rodada 11**, no chat: os papéis gerados e os links de skill vão tudo pelo sync (o `brza-sync` aprende o modo
  `120000`); o `codex()` e o `agy()` vão num `shell/runtimes.zsh` do pacote `runtimes`, e o `~/.zshrc` renomeia os da
  Fixfy. Na auditoria de fatos, Anderson pediu a medição da opção 2 antes de decidir.
- **As medições da R11.3 e da R12**, só leitura, a pedido de Anderson, em `.measurements/` daqui e da Fixfy:
  - **A auditoria custa US$ 0,0043 por fato** (US$ 1,03 por 238 fatos), ~US$ 0,10 por devolução; o `SubagentStop` do
    Codex traz `agent_type` e o caminho do transcript; o `Stop` do `agy` não traz nome de agente; o `rodado` é 34% dos
    fatos auditáveis e 61% dele sai `unknown` mesmo no Claude.
  - **Uma revisão custa** US$ 1,98 de mediana no Codex (`gpt-6-astra` em `xhigh`, 122 s, 11 revisões da Fixfy) e US$ 4,22
    no Claude (`opus-5-5`, 1.079 s, 4 revisões daqui); a do `agy` não tem linha de `reviewer` e fica estimada em US$ 0,1
    a 0,4 pelos tokens das sondas, no preço da tabela da Fixfy. As tarefas diferem, então é a forma do custo, e não a
    qualidade.
  - **A Fixfy não gravou o veredito da delegação**, que fechava em 2026-10-30: a decisão segue com o título "em medição
    até 2026-10-30" e sem nota do resultado.

- **A 11.3 e a R12**, respondidas "11.3.2 / 12.1.1 / 12.2.2": a auditoria de fatos ganha hooks nos dois runtimes
  (`SubagentStop` no Codex e `Stop` no `agy`, só `lido` e `doc`), não a recomendada, que era auditar o que o
  `brza delegate` devolve; o foco entra pelo `--focus` no pedido de cada `brza delegate --type review`; e o mapa de
  qual foco vai a qual runtime fica para depois de uma medição, não a recomendada.
- **O desenho do experimento da 12.2**, a partir do que as revisões daqui deixaram: o diff é a entrega do PLN-005 na
  `master` (`2e8ea67..13a291a`, 2.519 linhas em 22 arquivos), e a resposta conhecida é o parecer
  `work/reviews/pln-005-a-confianca-dos-fatos.md`, com 10 achados reais e 5 hipóteses conferidas e falsas. Anderson
  o confirmou ("confirmo o experimento"), e as 9 revisões rodaram em 2026-11-02, de 18:13 em diante: os três
  braços do Claude no Opus como `general-purpose`, sem a memória do `reviewer`; os três do Codex em `gpt-6-astra` com
  `xhigh`; e os três do `agy` em `gemini-4-argon-high`, em modo `plan`, todos sobre uma cópia do diff sem o histórico
  posterior, em `/private/tmp/pln004/ref-pln005`.
- **As 3 revisões do Codex usaram exatamente os 100% do limite de 5 h**, na palavra de Anderson, que viu o contador
  do app. Os rollouts mostram a janela de 5 h em 0% quando a primeira começou (21:13:48 UTC) e em 99% no último
  evento da terceira (21:34:19); o 100% que Anderson viu é posterior a esse evento. Por revisão: o defeito foi de 0%
  a 31%, a convenção de 34% a 62% e a simplicidade de 64% a 99%; a janela semanal foi de 1% a 16%. Cada revisão
  consumiu, portanto, de 28 a 35 pontos da janela de 5 h, e o experimento inteiro a esgotou: é um custo que o US$
  equivalente não mostra, e a tabela da R12 o traz.
- **O mesmo diff no `qwen2.5:14b` local (Ollama 0.40.13)**, a pedido de Anderson, para saber se um modelo local entra no
  fluxo e economiza token. O modelo não tem ferramenta: o diff foi inline, em 4 trechos de arquivos inteiros (de 8,4 a
  15,8 mil tokens), 3 focos × 4 trechos = 12 chamadas, `num_ctx` 20.480, temperatura 0,2. O script está em
  `/private/tmp/pln004/bench/scripts/run-qwen.py`; as saídas, as chamadas e as 1.022 amostras da máquina, em `out/qwen-*`.
  - **Tempo:** 1.366 s de parede (defeito 414, convenção 500, simplicidade 452); prefill de 411 tok/s e geração de 19,6
    tok/s; 4 chamadas bateram no teto de 3.072 tokens de saída. Custo em token pago: zero.
  - **A máquina** (M5 Pro, 24 GB, na tomada): GPU a 99% o tempo todo, com 12,6 GB em uso (pico 13,5); o `runner`
    (`llama-server`) usou 27% de um núcleo em média; memória *wired* de 2,9 para 14,9 GB, livre de 1,2 GB para 0,16 GB,
    swap de 0,8 para 6,0 GB (pico 11,6), compressor de 1,2 para 5,0 GB; sem aviso térmico; tudo voltou depois do
    descarregamento. **Não medi watts**: o `powermetrics` pede `sudo`. O `ps` só pegou o `serve`, e a CPU do `runner`
    vem do `top`. A linha de base não era ociosa (37% de CPU em uso por outras sessões).
  - **Acerto:** 0 de 7 itens do recall, 0 falsos positivos do gabarito, e 1 achado verdadeiro entre 80 únicos (o `736`
    do `brza-shot` sem teste, achado menor): 152 achados brutos, 72 repetições, confiança sempre 80 a 100 (75 com 100, 0
    verdadeiros). A pontuação do `collector` está em `out/qwen-pontuacao.md`; conferi por grep o que pesa (nenhuma saída
    cita `killpg`, `TEXT_LIMIT`, `--pending` nem as 120 colunas). **O desenho limita o resultado:** o trecho de testes
    de `fact_audit` não viu o `fact_audit.py`, então A1, A2 e A8 não eram achados possíveis, e a convenção não viu a
    régua do `AGENTS.md`.

## O que ficou

- **A pontuação do experimento**, que ficou por fazer porque Anderson pediu para parar e reiniciar o BrzA Studio: as 9
  revisões terminaram às 18:48, e a tabela de acerto, falso positivo, custo e tempo por runtime e foco vai a
  Anderson, e só então a R12.2 se decide. Depois, dividir o plano, reescrever o rascunho do Desenho e mandá-lo à
  aprovação. Para retomar:
  - **Onde está tudo:** `/private/tmp/pln004/bench/` (o link aponta para o `chat-scratch` do app, que sobrevive ao
    reinício): os prompts em `prompt-*.md`, o gabarito em `gabarito.md`, as saídas em `out/` — `claude-*.md`
    (condensadas na gravação), `codex-*.md` e `codex-*.jsonl`, `agy-*.json` — e a cópia do diff em `ref-pln005/`.
  - **Como pontuar:** casar cada achado de cada braço com A1 a A15 do `gabarito.md` (real, parcial, falso positivo ou
    novo), com recall sobre A1, A2, A3, A4, A6, A7 e A8; e contar os novos que mais de um braço aponta. Um `collector`
    com o gabarito faz o casamento mecânico, e a sessão confere os ambíguos.
  - **O custo, por onde sai:** o Codex, do `turn.completed` do `codex-*.jsonl` (preço da `gpt-6-astra` na tabela da
    Fixfy: US$ 10, 1 e 50 por milhão de entrada, cache e saída) e dos pontos de `rate_limits` dos rollouts em
    `~/.codex/sessions/2026/11/02/` (18-13-24, 18-19-58 e 18-24-59); o `agy`, dos passos `PLANNER_RESPONSE` do
    transcript em `~/.gemini/antigravity-cli/brain/` (o de defeito é `86119f93…`; os de convenção e simplicidade são
    os dois diretórios novos de 18:31 e 18:37), com o preço da `gemini-4-argon` (US$ 4, 0,20 e 20 por milhão); o
    Claude, das linhas `subagent` de `general-purpose` do `.measurements/measurements.jsonl` de hoje, depois das
    18:13.
  - **Os tempos medidos:** Codex 394, 301 e 561 s (defeito, convenção, simplicidade); `agy` 1.088, ~500 e 698 s, com a
    de convenção sem o log do script, que eu interrompi; Claude de 2,5 a 5 min (153, 179 e 305 s, pelo
    `duration_ms` dos subagentes).
- **Os nomes de modelo do `agy` no rascunho**, a corrigir no Desenho: o `agy models` (1.4.12) lista
  `gemini-4-argon-{low,medium,high}`, `gemini-3.8-flash-{low,medium,high}`, `claude-opus-5-5-*`, `claude-sonnet-5-5-*` e
  `gpt-oss-120b-medium`, e nenhum `pro` nem `flash`; o mapa `opus`/`sonnet` para `pro` e `haiku` para `flash`, que veio
  da Fixfy, fica sem base até se provar que o `--model pro` é alias. Os do Codex (`gpt-6-astra`, `gpt-6.1-sol`,
  `gpt-6-luna`) existem no `codex debug models`.
- **O plano passa de 400 linhas** (548 hoje), e o `plans/README.md` manda a Entrevista ao `-interview.md`; a divisão vai
  depois da R11, junto com a gravação do Desenho, para fazer uma vez.
- **O rascunho do Desenho** (556 linhas, no scratch) é reescrito depois da R10, e só então vai à aprovação.
- **As 19 citações que não batem** estão na tabela do agregado; três nunca sustentaram o fato (a linha do app para o
  `app-server` e a `permissionPolicy`, a do `agentCmdOverrides` no terminal e a do X3 do PLN-011).

## Fora do workspace

- **O `qwen2.5:14b` carregado no Ollama, pela API local** (`/api/chat`, `keep_alive` 10 min, e `keep_alive` 0 no fim).
  - **Risco:** 12,6 GB de GPU e 14,9 GB *wired* na máquina de 24 GB, com swap até 11,6 GB e memória livre de ~100 MB,
    que degrada as outras sessões e o app enquanto dura.
  - **Estado:** descarregado; `ollama ps` vazio, e o `ollama serve` do app segue.
  - **Desfazer:** `ollama stop qwen2.5:14b`; os modelos `qwen2.5:14b` e `qwen2.5:7b` ficam em disco (9,0 e 4,7 GB).
- **Os rollouts do Codex e os transcripts do `agy`** das sondas e das 9 revisões do experimento, em
  `~/.codex/sessions/2026/11/02/` e `~/.gemini/antigravity-cli/brain/`.
  - **Risco:** guardam o diff e as respostas inteiras, fora do git.
  - **Estado:** ativos, parados.
  - **Desfazer:** apagar os arquivos de 2026-11-02 dos dois diretórios, depois de pontuado o experimento.
- **A confiança de projetos no `~/.codex/config.toml`**, que o Codex gravou nos worktrees das sondas.
  - **Risco:** o Codex passa a confiar nesses caminhos.
  - **Estado:** ativo.
  - **Desfazer:** tirar as entradas `[projects."…"]` dos worktrees do PLN-004.
- **O auto-update do `agy` de 1.4.8 para 1.4.12**, feito pelo próprio `agy` durante as sondas.
  - **Risco:** o comportamento do `agy` mudou entre as sondas e o experimento.
  - **Estado:** ativo.
  - **Desfazer:** não há reversão simples; a versão fica registrada aqui.
