# PLN-013 — Desenho

> **O Desenho do [PLN-013](PLN-013-plan.md) (2026-11-03).** Os itens D1 a D7 saíram do Terreno, das rodadas R1 a R4 e
> da revisão do rascunho por duas sessões Grok ([REV-010](../../work/reviews/REV-010-pln-013-o-desenho-pelo-grok.md)).
> O rascunho foi de um `designer`; os passos que executam cada item estão no plano.

### O que este desenho assume

- **R1.3, R2.1, R3.2:** os três runtimes no `dispatch`; a conta ativa e a cota lidas por runtime, pelas janelas de topo
  do `rateLimits`; o Grok e o Antigravity na conta única.
- **R3.1, R4.1:** o modelo e o esforço por papel e por runtime, numa tabela do `brza.toml`, com os valores da R4.1; o
  Claude fica como está.
- **R4.2:** o Grok fica em `quota_unknown`, dentro do teto de sessões, e o `status` cita o `error` do `rateLimits.grok`.
- **R3.3, R4.4 (P7):** a troca de conta do Codex passa pelo gate só num `dispatch`; o `accounts.selectCodex` só roda
  aprovado; o ciclo não abre gate.
- **R2.2, R3.4, R4.3, R4.4 (P6):** o `--rename` e o `--wait` nos quatro runtimes; o `--wait` pelo `providerSession.id`,
  gravado como `provider_session` nos quatro, com o `claude_session` só no Claude; o `--rename` pelo que a sonda
  mostrar, e, onde ela for negativa, só a aba e o mapa, com uma linha `CHECK` e a issue aberta depois da sonda.
- **R4.4 (P3, P4):** a chave plana `policy.roles.<papel>.{model,effort}` é recusada; o alias `agy` se normaliza no
  `dispatch`.
- **R2.3:** três entregas, cada uma com commit e usável: E1 abrir e despachar, E2 a cota e a conta, E3 o `--rename` e o
  `--wait`.
- **O parecer da revisão do Desenho ([REV-010](../../work/reviews/REV-010-pln-013-o-desenho-pelo-grok.md)):** os achados
  A1 a A16 entram como correção, sem rodada; o A15 é falso.

### Terreno

Levantado em 2026-11-03 por um `collector`, só leitura; a sessão conferiu os três primeiros fatos do MCP e o do
`worker-start`.

#### O `worker-start` do app

- **Aceita `grok`, `codex` e `antigravity`.** `brza-studio/src/main/runtime/rpc/methods/orchestration/worker/worker-start-validation.ts:146-157`
  — o `--agent` passa por `isTuiAgent` e pelo `validateOrchestrationAgentLauncher`; o `settings.getAgentLaunch` deu
  `disabledTuiAgents: []`. A lista do `--help` é exemplo.
- **O `--model` e o `--effort` valem nos três.** `orchestration-worker-specs.ts:43-44`; o catálogo do app dá ao Grok os
  modelos 4.7, 4.6 e 4.5, com esforço de `low` a `xhigh`, ao Codex esforço até `ultra`, e ao Antigravity `models: []` e
  esforço `low` a `high`.
- **Chat ou terminal segue a configuração do usuário, sem flag.** `src/main/agent-launch/agent-launch-mode.ts:98-160`.
  No chat, o Grok e o Antigravity vão por ACP (`src/main/acp/acp-launch-specs.ts:297-303`); o Claude e o Codex, por
  adaptador de CLI. O valor atual por agente não sai em RPC de leitura nem nos JSON do app.

#### O MCP

- **Quatro pontos fixos no Claude.** `brza_mcp/tools.py:25` (o enum em `:32`, a recusa em `:192-193`, o padrão em
  `:217`), `cycle.py:22` (usado em `:152`), `accounts.py:24` e `limits.py:225`.
- **A conta ativa é a do Claude para qualquer runtime.** `limits.py:156` (`_active`), `:166-210` (`_account`,
  `_sessions`, `_quota`, `_account_matches`) e `tools.py:140-156` (`normalize_account`).
- **O `accounts.parse` lê só o Claude.** `accounts.py:56-76` lê `claude`, `rateLimits.claude` e
  `rateLimits.inactiveClaudeAccounts`; `usage()` (`:151`) devolve `None` aos outros, o que vira `quota_unknown`.
- **O `_windows` já lê os blocos dos outros.** Rodado contra o `account list --json` real: Codex `session` 1% e `weekly`
  0%; Antigravity `session` 37% e `weekly` 99%, com `buckets` por grupo que ele ignora; Grok `[]`, sem login.
- **A política é toda Claude.** `policy.py:28-30` dá `sonnet` e `opus` aos papéis, e `policy.py:210-215` os põe por cima
  do pedido.
- **O `pick_account` e o `switch_chat_account` não têm chamador** fora dos testes.

#### A conta do Codex

- **Hoje só há a `systemDefault`.** `account list --json`: `codex.accounts = []`, `inactiveCodexAccounts = []`.
- **A troca é global, do app.** `brza-studio/src/main/runtime/rpc/methods/accounts.ts:153-165` — `accounts.selectCodex` e
  `selectCodexForTarget`, com a permissão `accounts-admin`; não há flag de conta no `worker-start`.
- **O `switch_chat_account` não serve ao Codex.** O `prepareAccountSwitch` só existe no adaptador do Claude
  (`claude-structured-session-adapter.ts:153`), e o roteador devolve `unknown-account` aos outros
  (`brza-router-record-methods.ts:10-13`).
- **A conta do Codex vai no `CODEX_HOME`**, que o app aplica pela conta ativa; o resumo da conta Codex não traz `home`.

#### O `--rename` e o `--wait`

- **O caminho do Claude.** `brza-workflow/packages/client/bin/brza-sessions` — o `/rename` como primeiro prompt
  (`:387`), o título da aba pelo `agentSession.rename` (`:401`), o `open` no mapa (`:404`), o `--wait` pelo
  `providerSession.id` (`:193-212`) e pelo `<config>/sessions/<pid>.json` (`:127-151`, `:184-190`), o evento `session`
  (`:417`).
- **Há um id de sessão nos quatro.** O `agentSession.history` devolve `providerSession{key: 'session_id', id}`, rodado
  nos chats reais do Claude, do Codex e do Antigravity; o do Grok, sem login, não traz.
- **O `agentSession.rename` só dá o nome no app**, não no runtime.
- **O nome no runtime, por evidência fraca** (binários e ajuda, nada exercitado pelo chat): o Grok tem `/rename` e acha
  pelo título com `grok -r`; o Codex tem o slash "rename the current thread", com o nome em `~/.codex/session_index.jsonl`
  (`thread_name`); o Antigravity tem `/rename` no `strings` do `agy`.
- **Onde cada um grava a sessão:** o Grok em `~/.grok/sessions/<cwd>/<id>/summary.json`; o Codex em
  `~/.codex/sessions/AAAA/MM/DD/rollout-*.jsonl`; o Antigravity do chat em
  `<dados do app>/antigravity-chat/antigravity-acp/conversations/<uuid>.db`.
- **Bug latente no `list`.** `brza-sessions:244` lê `tab.get('agentSessionAgent')`, e as abas reais trazem `agent`.

#### Os testes

- **O `brza sessions`:** `tests/cli/test_brza_sessions.py`, com os casos fora do Claude em `:364-450`, que hoje asserem
  a recusa do `--rename` e do `--wait`. 4 dos 39 falham com o `BRZA_WORKSPACE` herdado do worktree; a base sai com o
  env limpo.
- **O MCP:** `tests/mcp/test_mcp_dispatch.py:85` (a recusa do `codex`, que a E1 inverte), `test_mcp_cycle.py:78`,
  `test_mcp_limits.py`, `test_mcp_accounts.py:391-406`, `test_brza_quota.py` e a fixture
  `fixtures/orca-account-list.json`. `python3 -m unittest discover -s tests/mcp` → 358 OK.

### D1 — A tabela de runtimes do MCP — `packages/mcp/brza_mcp/runtimes.py` (novo), `tools.py`, `cycle.py`, `limits.py` (E1, P2)

- **Origem:** R1.3, Pedido 3, R4.4 (o alias), REV-010/A4, REV-010/A6, REV-010/A10.
- **Contexto:** o runtime está fixo no Claude em `tools.py:25,32,192-193,217` e `cycle.py:22,152`. A E1 despacha aos
  três na conta padrão do runtime, como a PLN-009/R2.5, sem cota fora do Claude até a E2.

#### Como fica

```python
# packages/mcp/brza_mcp/runtimes.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Runtime:
    name: str             # o do `dispatch` e da coluna `runtime` da fila
    agent: str            # o `--agent` do `worker-start`
    efforts: tuple        # teto largo do runtime; a conferência fina é por modelo (MODEL_EFFORTS, REV-010/A6)
    accounts: str | None = None   # E2: a chave de topo do `account list` com as contas; None = conta única
    inactive: str | None = None   # E2: a chave em `rateLimits` com o uso das contas inativas
    switch: str | None = None     # E2: 'chat' (agentSession.switchAccount, H3) ou 'global' (accounts.selectCodex)

RUNTIMES = {r.name: r for r in (
    Runtime('claude', 'claude', ('low', 'medium', 'high', 'xhigh', 'max'),
            'claude', 'inactiveClaudeAccounts', 'chat'),
    Runtime('codex', 'codex', ('minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra'),
            'codex', 'inactiveCodexAccounts', 'global'),
    Runtime('grok', 'grok', ('low', 'medium', 'high', 'xhigh')),
    Runtime('antigravity', 'antigravity', ('low', 'medium', 'high')),
)}
ALIASES = {'agy': 'antigravity'}   # R4.4: normalizado antes da fila

# a escada por modelo (REV-010/A6). Fontes: o catálogo do app
# (brza-studio/src/shared/agent-session/options/agent-session-option-catalog-grok.ts:10-15,56-75) e os caches dos
# runtimes (~/.grok/models_cache.json; ~/.codex/models_cache.json). Modelo fora da tabela: vale o teto do runtime, e o
# `worker-start` é quem recusa (brza-studio/src/shared/agent-launch-model-preferences.ts:64-77).
MODEL_EFFORTS = {
    ('grok', 'grok-4.7'): ('low', 'medium', 'high', 'xhigh'),
    ('grok', 'grok-4.7-build-fast'): ('low', 'medium', 'high', 'xhigh'),
    ('grok', 'grok-4.6'): ('low', 'medium', 'high', 'xhigh'),
    ('grok', 'grok-4.5'): ('low', 'medium', 'high'),
    ('codex', 'gpt-6.1-sol'): ('low', 'medium', 'high', 'xhigh', 'max', 'ultra'),
    ('codex', 'gpt-6-astra'): ('low', 'medium', 'high', 'xhigh', 'max', 'ultra'),
    ('codex', 'gpt-6-luna'): ('low', 'medium', 'high', 'xhigh', 'max'),
}

def get(name: str | None) -> Runtime:
    """O runtime pelo nome ou alias; None é o Claude. Desconhecido levanta KeyError."""
    name = name or 'claude'
    return RUNTIMES[ALIASES.get(name, name)]

def efforts(runtime: str, model: str | None) -> tuple:
    return MODEL_EFFORTS.get((runtime, model), get(runtime).efforts)
```

```python
# tools.py — hoje
RUNTIMES = ('claude',)
'runtime': {'enum': list(RUNTIMES)},
if 'runtime' in args and args['runtime'] not in RUNTIMES:
    raise ToolError(f'runtime {args["runtime"]!r} não é aceito: só "claude" (o M4 é fase 3)')
fields.setdefault('runtime', 'claude')

# tools.py — fica
'runtime': {'enum': [*runtimes.RUNTIMES, *runtimes.ALIASES]},

# validate: o alias vira o nome canônico antes de qualquer gravação
if 'runtime' in args:
    try:
        args = {**args, 'runtime': runtimes.get(args['runtime']).name}
    except KeyError:
        raise ToolError(f'runtime {args["runtime"]!r} não é aceito: claude, codex, grok ou antigravity (agy)') from None

# dispatch, só na E1 — olha o argumento que o chamador mandou, antes de qualquer setdefault (REV-010/A4);
# a E2 troca esta recusa pela conta por runtime (D4)
if args.get('runtime', 'claude') != 'claude' and 'account' in args:
    raise ToolError('account fora do Claude entra na E2 do PLN-013: tire o account, e o worker abre na conta padrão '
                    'do runtime')
fields.setdefault('runtime', 'claude')
# a conta gravada fora do Claude (REV-010/A10): Grok e Antigravity, 'systemDefault'; Codex, o `codex.activeAccountId`
# do `account list` (a seleção do host, brza-studio/src/main/codex-accounts/codex-account-selection.ts:57), ou
# 'systemDefault' quando ele é null
if fields['runtime'] != 'claude':
    fields['account'] = self.accounts.active_id(runtime=fields['runtime'], ...) or accounts_mod.SYSTEM_DEFAULT
fields.setdefault('account', '')

# a proposta do gate leva o runtime (hoje, tools.py:252-253, não leva)
proposal = {k: fields[k] for k in ('task', 'role', 'target', 'runtime', 'model', 'effort', 'account', 'ref')
            if fields.get(k)}
```

```python
# accounts.py — o mínimo da E1: a conta ativa por runtime (a E2 a completa, D4)
def active_id(self, runtime='claude', client=None, user_data=None):
    # claude: como hoje; codex: data['codex']['activeAccountId'] ou None; grok e antigravity: 'systemDefault'

# limits.py — na E1, o `_account_matches` só confere o Claude: o pedido de outro runtime grava a própria conta
# padrão (acima), e compará-la à ativa do Claude o seguraria para sempre em `account_active`
if not account or not self.has_active or (request.get('runtime') or 'claude') != 'claude':
    return None
```

```python
# cycle.py — hoje
AGENT = 'claude'
args = ['worker-start', '--task', task, '--run', run, '--agent', AGENT]
# cycle.py — fica
args = ['worker-start', '--task', task, '--run', run, '--agent', runtimes.get(request.get('runtime')).agent]
```

- **A cota na E1:** fora do Claude, `Accounts.usage(conta, runtime)` segue devolvendo None (`accounts.py:151`), e o
  pedido entra em `quota_unknown`, só com o teto de sessões, que já conta por `(conta, runtime)`
  (`queue.py:257-265`).

#### O teste que falha antes

- `test_mcp_dispatch.py`: `test_codex_is_refused` (`:84-85`) vira
  `test_each_runtime_is_accepted_and_agy_is_stored_as_antigravity` — `grok`, `codex`, `antigravity` e `agy` entram na
  fila, e a linha da fila diz `antigravity` para o `agy`; hoje, "só claude".
- `test_mcp_dispatch.py`: `test_account_outside_claude_is_refused_until_e2` — `{'runtime': 'codex', 'account': 'x'}`
  é recusado com o motivo da E2; hoje, recusado pelo runtime, com outra mensagem.
- `test_mcp_dispatch.py`: `test_the_account_stored_outside_claude_is_the_runtime_default` — Grok e Antigravity gravam
  `systemDefault`; o Codex grava o `activeAccountId` da fixture, ou `systemDefault` quando ele é null.
- `test_mcp_dispatch.py`: a proposta do gate de um executor `grok` leva `runtime: grok`.
- `test_mcp_limits.py`: um pedido `grok` com `account: systemDefault` e a ativa do Claude noutra conta é admitido,
  sem `account_active`.
- `test_mcp_cycle.py`: `test_worker_start_uses_the_agent_of_the_runtime` — o pedido `grok` abre com `--agent grok`;
  hoje, `--agent claude` (`test_mcp_cycle.py:78`).

### D2 — O modelo e o esforço por papel e runtime — `policy.py`, `brza.toml` (E1, P2)

- **Origem:** R3.1, R4.1, R4.4 (P3), REV-010/A6, REV-010/A7.
- **Contexto:** `policy.py:28-30` dá `sonnet` e `opus` aos papéis, e `policy.py:210-215` põe a linha por cima do pedido
  em qualquer runtime: um worker Codex sairia com `--model sonnet`. Sem linha, o papel cai no `resolver`, que roda
  `claude -p --model haiku` (`resolver.py:128-132`) e gasta a conta do Claude também para um pedido Grok (REV-010/A13). Entra na E1,
  senão o despacho da E1 falha.

#### Como fica

```toml
# os padrões (DEFAULTS), na forma do brza.toml — R4.1
[policy.roles.consultant.claude]
model = "sonnet"
effort = "low"
[policy.roles.executor.claude]
model = "sonnet"
effort = "medium"
[policy.roles.architect.claude]
model = "opus"
effort = "high"

[policy.roles.consultant.codex]
model = "gpt-6.1-sol"
effort = "low"
[policy.roles.executor.codex]
model = "gpt-6.1-sol"
effort = "medium"
[policy.roles.architect.codex]
model = "gpt-6-astra"
effort = "high"

[policy.roles.consultant.grok]
model = "grok-4.7"
effort = "low"
[policy.roles.executor.grok]
model = "grok-4.7"
effort = "high"
[policy.roles.architect.grok]
model = "grok-4.7"
effort = "xhigh"          # R4.1: se o P1 vir o `worker-start` recusar, cai para "high"

[policy.roles.consultant.antigravity]
model = "gemini-4-argon-low"     # o slug traz o nível (`agy models`); sem `effort`
[policy.roles.executor.antigravity]
model = "gemini-4-argon-medium"
[policy.roles.architect.antigravity]
model = "gemini-4-argon-high"
```

```python
# policy.py — hoje
'policy.roles.consultant.model': 'sonnet', 'policy.roles.consultant.effort': 'low',   # e os outros dois papéis
_ROLE_KEY = re.compile(r'^policy\.roles\.[A-Za-z0-9_-]+\.(model|effort)$')
def role_row(self, role, config=None) -> dict | None
row = self.role_row('consultant', config) or {}          # papel sem linha, em qualquer runtime
resolved = resolver.classify(request['task'])            # o Haiku, em qualquer runtime

# policy.py — fica
DEFAULTS = {..., 'policy.roles.consultant.claude.model': 'sonnet', 'policy.roles.consultant.claude.effort': 'low',
            ...}   # a tabela acima, chave a chave
_ROLE_KEY = re.compile(rf'^policy\.roles\.[A-Za-z0-9_-]+\.({"|".join(runtimes.RUNTIMES)})\.(model|effort)$')
_FLAT_ROLE_KEY = re.compile(r'^policy\.roles\.([A-Za-z0-9_-]+)\.(model|effort)$')

def check_file_key(key, value):
    ...
    elif _ROLE_KEY.match(key):
        # texto não vazio; o esforço contra o teto do runtime
    elif m := _FLAT_ROLE_KEY.match(key):
        raise ValueError(f'{key} virou policy.roles.{m[1]}.claude.{m[2]} (PLN-013/R3.1)')

def check_role_rows(values):
    """Depois do flatten: o esforço de cada linha contra a escada do modelo dela, `runtimes.efforts(runtime, model)`
    (REV-010/A6). Fora da escada levanta ValueError com a linha, o modelo e a escada."""

def role_row(self, role, runtime='claude', config=None) -> dict | None:
    """A linha do papel NO runtime; nunca a de outro runtime."""

def decide_model(self, request, resolver=None) -> dict:
    runtime = runtimes.get(request.get('runtime')).name
    row = self.role_row(role, runtime, config)
    if row is None and runtime == 'claude':
        ...   # como hoje: o resolver, e sem resposta a linha do consultant (test_mcp_policy.py:131-150 seguem)
    elif row is None:
        # fora do Claude (REV-010/A7): sem resolver, sem a linha de outro papel; o pedido vale onde trouxe
        # model/effort, e o resto fica None, com reason 'default_role; padrão do runtime'
    # effort sem model, no fim: vai None, com a nota 'o worker-start exige --model com --effort'
    # (brza-studio/src/shared/agent-launch-model-preferences.ts:37)

def suggestion(self):   # a sessão principal é Claude: role_row('architect', 'claude')
```

#### O teste que falha antes

- `test_mcp_policy.py`: `decide_model({'role': 'executor', 'runtime': 'codex'})` dá `gpt-6.1-sol`/`medium`; hoje,
  `sonnet`/`medium`.
- `test_mcp_policy.py`: `{'role': 'architect', 'runtime': 'antigravity'}` dá `gemini-4-argon-high` e `effort` None.
- `test_mcp_policy.py`: `{'role': 'mistério', 'runtime': 'grok', 'task': 'x'}` com um resolver que falha o teste se
  for chamado dá `model` e `effort` None e o motivo com "padrão do runtime"; hoje, chama o resolver e dá `sonnet`.
- `test_mcp_policy.py`: `[policy.roles.executor]\nmodel = "sonnet"` é recusado, e a mensagem nomeia
  `policy.roles.executor.claude.model`; hoje, aceito (`policy.py:84`).
- `test_mcp_policy.py`: `[policy.roles.architect.grok]\nmodel = "grok-4.5"\neffort = "xhigh"` é recusado, e a mensagem
  nomeia o modelo e a escada `low, medium, high`; hoje, recusado só como "chave desconhecida". O assert é do texto,
  não só do `ValueError` (REV-010/A16).
- `test_mcp_cycle.py`: um executor Codex despachado abre com `--agent codex --model gpt-6.1-sol --effort medium`; um
  architect Antigravity, com `--model gemini-4-argon-high` e sem `--effort`.
- **Regressão:** `test_mcp_policy.py:131-150` (o papel sem linha no Claude vai ao resolver e, sem resposta, fica no
  consultant) passa sem mudança, salvo a chave. O `TOML` do `test_mcp_policy.py:20-53` e o `test_mcp_gates.py:180`
  passam à chave aninhada.

### D3 — O `brza sessions` abre o Grok e recusa agente fora dos quatro — `packages/client/bin/brza-sessions` (E1, P3)

- **Origem:** Pedido 1, Pedido 2, REV-010/A8.
- **Contexto:** hoje qualquer `--agent` vai ao app: o `--dry-run` com `grok` e com `cursorx` responde "abriria" e sai 0;
  o `brza-sessions:363` só traduz o `agy`.

#### Como fica

```python
# hoje (:363)
agent = 'antigravity' if args.agent == 'agy' else args.agent
# fica
AGENTS = {'claude': 'claude', 'codex': 'codex', 'grok': 'grok', 'antigravity': 'antigravity', 'agy': 'antigravity'}
agent = AGENTS.get(args.agent)
if agent is None:
    print(f'CHECK:    {args.name}: --agent {args.agent} não é claude, codex, grok nem antigravity (agy); '
          'nada foi aberto')
    return 1
```

- O docstring, o `Uso:` e o `--help` ganham o `grok`.

#### O teste que falha antes

- `test_unknown_agent_is_refused_before_any_side_effect` (`--agent cursor`, com `running`, `mapped_and_open`,
  `resolve_checkout` e o `brza` proibidos): hoje abre.
- **Regressão:** o `grok` entra nos `subTest` de `test_brza_sessions.py:364-381` e `:404-410`; eles já passam hoje e
  ficam como regressão, não como teste que falha antes (REV-010/A8).

### D4 — A conta e o uso por runtime — `accounts.py`, `limits.py`, `tools.py`, `bin/brza-quota` (E2, P5)

- **Origem:** R2.1, R3.2, R4.2, Pedido 4, REV-010/A14.
- **Contexto:** o `accounts.parse` lê só o Claude (`accounts.py:56-76`) e carimba `'runtime': RUNTIME` em toda amostra
  (`:71`, `:75`, `:240-242`); o `Limits._active` usa a ativa do Claude em qualquer runtime (`limits.py:156-210`). O id
  `systemDefault` (`accounts.py:23`) vale para a conta padrão de cada runtime, e só o par `(conta, runtime)` as separa
  na fila (`queue.py:257,284`).

#### Como fica

```python
def parse(payload) -> dict:
    """-> {runtime: {'accounts': [{id, label, email, home, system_default, active}],
                     'usage': {id: {account, runtime, windows}},
                     'error': <rateLimits.<runtime>.error ou None>}}, para os quatro do RUNTIMES.
    Toda amostra leva o runtime do bloco, nunca a constante RUNTIME, que sai."""
# claude: como hoje (claude, rateLimits.claude, rateLimits.inactiveClaudeAccounts)
# codex: codex.systemDefault.email e codex.accounts (sem home); ativa = codex.activeAccountId;
#        o uso da ativa em rateLimits.codex, o das outras em rateLimits.inactiveCodexAccounts
# grok, antigravity: uma conta, {'id': 'systemDefault', 'label': <runtime>, 'system_default': True, 'active': True},
#        com o uso das janelas de topo de rateLimits.<runtime> (R3.2); os buckets do Antigravity ficam de fora

class Accounts:
    def find(self, name, runtime='claude', data=None, client=None, user_data=None)
    def active_id(self, runtime='claude', client=None, user_data=None)
    def usage(self, account, runtime, client=None, user_data=None)    # sai o `if runtime not in (..., RUNTIME)`
    def usage_error(self, runtime, client=None, user_data=None)       # o `error` do bloco, para o `status` (R4.2)

class Limits:
    def __init__(..., active=None)   # active(runtime, client=None, user_data=None)
    def _active(self, request)       # a chave do _once ganha o runtime; volta a conferir os quatro em _account_matches
    def _quota(...)                  # sem janela: measures['quota'] = {'known': False, 'error': <usage_error>, ...}

def normalize_account(self, name, runtime, client=None, user_data=None)
    # grok e antigravity: só 'systemDefault' (ou o rótulo do runtime); outro nome ->
    #   'o <runtime> tem uma conta só no app (PLN-013/R2.1)'
    # a recusa de account fora do Claude, da E1 (D1), sai

# status: os tetos ganham o que não se lê, por runtime (R4.2)
ceilings['quota_unknown'] = {'grok': 'Grok did not report a usage percentage for this account'}   # o error lido

def quota_report(data, queue, limits, now_ms=None) -> list   # uma linha por (runtime, conta), com a chave runtime
```

- **O Antigravity:** com o `weekly` de topo em 99% em 2026-11-03, renovando em 2026-11-10 00:09 -03 (`orca account
  list --json`), todo worker dele espera em `account_quota` até lá.
- **A issue da R4.2** já existe: [O app não lê a cota do Grok](../../work/issues/o-app-nao-le-a-cota-do-grok.md).

#### O teste que falha antes

- `test_mcp_accounts.py`: o `parse` da fixture dá o uso do `codex` e do `antigravity`, cada amostra com o seu
  `runtime`, e nenhum do `grok`, com o `error` dele; hoje, só o `claude`. O
  `test_only_the_real_shape_is_read_and_the_accounts_outside_claude_are_ignored` (`:50-54`) passa a ler o Claude só
  dentro de `['claude']`.
- `test_mcp_accounts.py`: a conta `systemDefault` do Codex e a do Claude, com usos diferentes, não se misturam nas
  amostras da fila.
- `test_mcp_limits.py`: um pedido Codex com o Codex a 95% fica em `account_quota`; hoje, `quota_unknown` e admitido.
- `test_mcp_limits.py`: um pedido Antigravity com o `weekly` em 99% fica em `account_quota`; hoje, admitido.
- `test_mcp_limits.py`: um pedido Codex com `account` diferente do `codex.activeAccountId` fica em `account_active`.
- `test_mcp_dispatch.py`: `account: "x"` num pedido `grok` é recusado com o motivo da conta única (troca a recusa da
  E1); `account: "systemDefault"` entra.
- `test_mcp_dispatch.py`: o `status` traz `quota_unknown.grok` com o `error` da fixture.
- `test_brza_quota.py`: o relatório traz linhas `codex` e `antigravity`, cada uma com o `runtime`.

### D5 — A troca do Codex pelo gate — `tools.py` (`dispatch`, `approve`), `accounts.py` (`select_codex`), `queue.py` (E2, P6)

- **Origem:** R2.1, R3.3, R4.4 (P7), REV-010/A5.
- **Contexto:** a troca é global e do app — `accounts.selectCodex`, com a permissão `accounts-admin`
  (`brza-studio/src/main/runtime/rpc/methods/accounts.ts:153-157`), que não barra a chamada local sem carimbo
  (`brza-studio/src/main/runtime/rpc/rpc-caller-scope.ts:38-40`). O `switch_chat_account` não serve ao Codex. Hoje não
  há segunda conta Codex (`inactiveCodexAccounts: []`): sem prova real (R3.3).

#### Como fica

```python
# dispatch, depois da política
switch = self.codex_switch(fields, client, user_data)
# None, ou {'account': <id>, 'from': <ativa>, 'used': <% da ativa>, 'target_used': <% da proposta>};
# só com runtime codex, sem account (ou com a ativa), a ativa com janela >= quota.hard_cap_percent, e
# limits.pick_account(<inativas do Codex>, queue, runtime='codex') com conta
reasons = [r for r in (self.gate_reason(args, fields, client), switch and self.switch_reason(switch)) if r]
# o papel e a troca juntos (REV-010/A5): um executor Codex com a cota no teto leva os dois motivos num gate só
reason = '; '.join(reasons) or None
if switch:
    fields['account'] = switch['account']
# switch_reason: f'a conta ativa do Codex ({from}) está em {used:g}%; a troca para {account} ({target_used:g}%) é
#   global e vale para os próximos launches do Codex, chats e workers (R3.3)'
# sem proposta: o pedido entra e espera em account_quota

# approve — a ordem (REV-010/A5): o select_codex fica fora do queue.lock
# 1. lê o gate e o pedido, e confere chamador, uso e campos, sem o lock (como a normalização da conta hoje,
#    tools.py:274-277)
# 2. se request['runtime'] == 'codex' e request['account'] != accounts.active_id('codex', ...):
#        accounts_mod.select_codex(request['account'], client)  # falhou: ToolError, e o gate segue aberto
#        self.accounts.read(force=True, ...)
# 3. com o lock: confere de novo e faz o UPDATE de hoje (tools.py:278-304); a segunda aprovação perde ali
#    (a troca para a mesma conta é idempotente)

def select_codex(account_id, client='studio', rpc=None):
    """`accounts.selectCodex` com `accountId` (None = systemDefault). Global. Só com o gate aprovado (R3.3)."""
```

```python
# o held_reason do Codex em account_quota (R4.4/P7): o ciclo não abre gate
f'janela {name} já em {used:g}%, quota.hard_cap_percent = {cap:g}; a troca de conta do Codex só é proposta num '
'dispatch novo (PLN-013/R3.3)'
```

#### O teste que falha antes

- `test_mcp_gates.py`: consultant Codex, ativa a 95% e a inativa `b` a 10% → `{'gate': {'reason': '…troca para b…',
  'proposal': {'account': 'b', 'runtime': 'codex'}}}`; hoje, o runtime é recusado.
- `test_mcp_gates.py`: executor Codex com a cota no teto → um gate só, com o motivo do papel e o da troca.
- `test_mcp_gates.py`: a aprovação chama o `select_codex('b')` falso uma vez, sem o `queue.lock` seguro (o dublê
  confere `queue.lock` livre), e põe o pedido em `queued`; com o RPC falhando, o gate segue sem uso.
- `test_mcp_gates.py`: sem inativa (o estado real), o pedido entra e fica em `account_quota`, sem gate, e o
  `held_reason` diz que a troca só se propõe num `dispatch` novo.
- `test_mcp_accounts.py`: `select_codex('systemDefault')` manda `accounts.selectCodex` com `accountId: None`.

### D6 — A sonda do `/rename` e o `--wait` nos quatro — `brza-sessions` (E3, P8, P9)

- **Origem:** R2.2, R3.4, R4.3, REV-010/A2, REV-010/A3, REV-010/A9, REV-010/A12.
- **Contexto:** o `--wait` do Claude espera o `providerSession.id` (`brza-sessions:193-212`), e o
  `agentSession.history` dá esse id nos chats do Claude, do Codex e do Antigravity. O `--rename` e o `--wait` são
  recusados fora do Claude em `brza-sessions:363-367`. O `session_map` só guarda `claude_session` (`:99-106`). O `list`
  lê `agentSessionAgent` (`:244`), e as abas reais trazem `agent`.

#### A sonda (P8)

Para `grok`, `codex` e `agy`: `brza sessions sonda-<rt> --agent <rt> --prompt "diga oi"`; depois
`brza sessions send sonda-<rt> "/rename sonda-<rt>-nome"`. Anota, por runtime:

- se o chat **executou** o `/rename` como comando ou o mostrou ao modelo como texto (REV-010/A2: no Grok, o `/rename`
  está documentado como comando da TUI, `~/.grok/docs/user-guide/04-slash-commands.md:85-94`, e o app só manda
  `/effort` e `/model` como comando no ACP, `agent-session-option-catalog-grok.ts:43,84`);
- o nome em disco: no Grok, o `summary.json` em `<grok_home>/sessions/<cwd codificado>/<id>/`, com `generated_title`,
  `title_is_manual` e `grok_home`; no Codex, o `thread_name` em `~/.codex/session_index.jsonl`; no Antigravity, o
  `.meta` de `<dados do app>/antigravity-chat/antigravity-acp/conversations/<uuid>`;
- lado a lado, o `providerSession.id` do `agentSession.history` e o id do runtime — no Grok, o `info.id` do
  `summary.json` (REV-010/A12);
- se o `providerSession.id` sai antes do primeiro turno;
- se o `send` com `queue-if-active` espera o `/rename` terminar no chat ACP.

O resultado vai ao plano; onde for negativo, a sessão abre a issue do runtime (R4.4/P6).

#### Como fica (P9)

```python
# hoje
if agent != 'claude' and (args.rename or args.wait): ...recusa             # :364-367
if found.get('agent') not in (None, 'claude'): return None                  # :210-211
record('session', name=args.name, chat=session_id, claude_session=claude_session)   # :417
entries[chat] = {..., 'claude_session': None, ...}                          # :99-100
agent = (tab.get('agentSessionAgent') or (entry or {}).get('agent') or ('claude' if chat.startswith('claude_') else None))

# fica
# a recusa sai; o --rename segue a D7
def provider_session(chat) -> str | None:   # o id da sessão do runtime, nos quatro (R4.3)
record('session', name=args.name, chat=session_id, provider_session=sid,
       **({'claude_session': sid} if agent == 'claude' else {}))            # claude_session só no Claude
# session_map lê o campo novo (REV-010/A3)
entries[chat] = {..., 'claude_session': None, 'provider_session': None, ...}
elif chat in entries and event == 'session':
    entries[chat]['claude_session'] = row.get('claude_session')
    entries[chat]['provider_session'] = row.get('provider_session') or row.get('claude_session')
# chats(): o agente pela chave real, a legada do teste :438, o mapa e o prefixo do id do chat do app
agent = (tab.get('agent') or tab.get('agentSessionAgent') or (entry or {}).get('agent')
         or next((a for a in ('claude', 'codex', 'grok', 'antigravity') if chat.startswith(f'{a}_')), None))
# list --json ganha 'provider_session': no Claude, o do history; fora dele, só o do mapa, para o list não chamar o
# history fora do Claude (o teste :436-447)
```

- **O prefixo** é o do id do chat no app (`grok_…`, `codex_…`), e não o id que o Grok grava (`info.id`, um UUID): ele
  só desempata a aba sem `agent` e sem mapa.

#### O teste que falha antes

- `test_non_claude_wait_records_the_provider_session` (grok, codex, agy): o `--wait` grava `provider_session` e não
  `claude_session`; hoje, recusado. O `test_non_claude_rejects_rename_and_wait…` (`:383-403`) sai.
- `test_the_session_map_reads_the_provider_session`: um evento `session` com `provider_session` aparece no `list
  --json`; hoje, o campo não existe.
- `test_list_reads_the_agent_key_of_real_tabs`: aba com `agent: 'claude'` e id sem prefixo acha o nome pelo
  transcript; hoje, não (o `:244`).
- `test_brza_sessions.py:412-426` (o contrato JSON do chat mapeado fora do Claude) passa a afirmar `provider_session`
  e `claude_session: None` (REV-010/A9).
- `test_brza_sessions.py:449-451` passa a afirmar que o `provider_session` volta o id, e que o `list` não o põe em
  `claude_session`.

### D7 — O `--rename` por runtime — `brza-sessions` (E3, P10)

- **Origem:** R2.2, R3.4, R4.4 (P6), REV-010/A1, REV-010/A2.
- **Contexto:** hoje o `--rename` manda `/rename <nome>` como primeiro prompt (`brza-sessions:387`) e espera o nome
  pelo `<config>/sessions/<pid>.json` do Claude (`:141-151`, `:184-190`). Fora do Claude, nada está provado: a sonda
  da D6 decide cada runtime.

#### Como fica

```python
# como cada runtime diz que registrou o nome; a sonda confirma ou corta cada linha
NAMED = {
    'claude': lambda name, sid: running(name),                     # hoje
    'grok':   lambda name, sid: grok_manual_title(sid) == name,
    'codex':  lambda name, sid: codex_thread_name(sid) == name,    # <CODEX_HOME ou ~/.codex>/session_index.jsonl
    'antigravity': None,                                           # sem leitura conhecida até a sonda
}

def grok_manual_title(sid) -> str | None:
    """O `generated_title` do `summary.json` da sessão, só com `title_is_manual: true` (REV-010/A1): o título
    automático nasce do primeiro prompt e muda nos turnos iniciais (~/.grok/docs/user-guide/17-sessions.md:44-46),
    e coincidir com o nome não prova o `/rename`. Lê em <grok_home>/sessions/*/<sid>/summary.json."""

def wait_for_name(name, agent, sid) -> bool

# o primeiro prompt é `/rename <nome>` só no runtime em que a sonda viu o slash executado (REV-010/A2); a tarefa vai
# depois pelo send_to_chat, como no Claude
# sonda negativa, ou NAMED None (R4.4/P6): o --rename dá só a aba e o mapa, o --wait vai pelo providerSession.id, e
# sai a linha
print(f'CHECK:    {args.name}: o {agent} não recebe o /rename pelo chat do app; o nome ficou na aba e no mapa')
```

- **O `grok -r` não acha pelo título** a sessão aberta pelo app: ele procura no diretório atual, e o cwd da sessão do
  chat é o scratch do app (REV-010/A1). Quem acha a sessão Grok pelo nome é o `brza sessions`, pelo mapa.

#### O teste que falha antes

- `test_rename_grok_waits_for_the_manual_title` com um `summary.json` falso: passa com `generated_title` igual ao nome
  e `title_is_manual: true`; falha (vence o prazo) com `title_is_manual` ausente; hoje, recusado.
- `test_rename_codex_waits_for_thread_name` com um `session_index.jsonl` falso; hoje, recusado.
- `test_rename_without_a_reader_gives_tab_and_map_and_a_check_line`: o runtime com `NAMED` None não manda o
  `/rename`, dá o título da aba, grava o mapa, espera o `providerSession.id` e imprime o `CHECK`.

---
