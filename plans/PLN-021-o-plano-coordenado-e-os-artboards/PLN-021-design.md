# PLN-021 — Desenho

Rascunho do `designer` de 2026-11-09, registrado como está. Os pontos marcados **[sem lastro → Pn]** e
**[sem lastro, menor]** estão na rodada 4 do [PLN-021: O plano roda por uma sessão coordenadora, com scripts de apoio e artboards de tela](PLN-021-plan.md),
ainda sem resposta. A pedido de Anderson ("siga direto para escrever as skills"), a execução segue as opções
recomendadas, confirmadas na R5 (menos a R4.6, que a R5.6 trocou pela opção 2). As marcas `[F…]`/`[C…]` seguem a regra de evidência do papel. Caminhos relativos ao
worktree do playground.

## O que este desenho assume

- **R1.1:** PLN novo no playground.
- **R1.3:** a coordenação abre e acompanha executores, abre consultores em sessão e publica o painel do plano.
- **R1.4 / R2.4:** a skill própria `screen-artboards`, com pacote de tokens por projeto e molduras CSS.
- **R2.2:** `plan_state.py`, `step_request.py`, `round_log.py`, `close_check.py`.
- **R2.3:** consultores em sessão só com 3 ou mais alternativas e escolha cara de reverter, ou a pedido; no resto, `Agent`.
- **R3.1:** o `plan-runner` é reescrito com o mesmo nome, só na branch `workstream/playground`.
- **R3.2 / R3.3:** o código comum mora em `.claude/scripts/`, e a `meeting-runner` passa a importar de lá neste plano.
- **Invariantes que ficam:** o passo só executa a pedido explícito de Anderson; `[x]` sem evidência não conta; quem
  recomenda não decide; a norma de rodadas do `AGENTS.md`.

## Terreno novo (além de `/private/tmp/pln021/terreno.md`)

- **`python3 -I` não põe a pasta do script no `sys.path`**: o `print(sys.path[0])` de um script rodado com `-I` saiu
  `…/python315.zip`. Um `_kit.py` ao lado do script, que insere o caminho de `.claude/scripts/` e aceita a sobrescrita
  `SKILLKIT`, importou o pacote, e `SKILLKIT=/nope` fez o import falhar, o que prova que a variável é lida sob `-I`
  [F1 · rodado · 95].
- **Os scripts da `meeting-runner` importam por nome plano**, com `sys.path.insert(0, AQUI)` antes de `import common` e
  `import sessions_map` (`launch_persona.py:55-57`, `wait_round.py:76-78`, `tally.py:102-104`, `panel.py:40-42`)
  [F2 · lido · 95].
- **Os testes trocam funções por atribuição no módulo, sem `mock.patch`**: `wait_round.wait_brza` aparece 21 vezes e
  `panel.gera_png` 12 vezes nos testes e scripts, e o `grep` por `patch` não achou `mock.patch` [F3 · rodado · 90]. O
  import por nome (`from skillkit.sessions_cli import wait_brza`) preserva essa troca, porque o código chama o nome do
  módulo dele.
- **A suíte da `meeting-runner`:** `python3 -m unittest discover -s .` em `scripts/tests` → 323 testes, OK, 10,2 s
  [F4 · rodado · 95].
- **`.claude/scripts/` não existe** [F5 · rodado · 95].
- **O PNG do painel sai do Chrome**, com `--window-size={width},2000` fixo (`panel.py:496-506`); o `salva_visual` grava
  `<id>-<meio>-<hash4>.html`, mesmo nome para a mesma chave, e recusa ≥ 512 KB (`panel.py:519-539`)
  [F6 · lido · 95].
- **`brza shot`:** `arquivo.html destino.png [--theme light|dark] [--width 736] [--scale 2] [--wait 500] [--force]`
  [F7 · rodado · 95].
- **Sonda de largura:** um bloco de 1280 px pelo `brza shot --width 736` saiu 1472×600 e cortado (o gradiente para no
  meio); o mesmo bloco com `zoom = largura/1280` por script inline saiu 1472×346, inteiro; cada PNG levou ~1,2 s
  (`/private/tmp/pln021/sonda/`) [F8 · rodado · 92].
- **`brza sessions wait --marker ARQUIVO:REGEX`** existe; o `done` sem o marcador vira `ended_without_marker`
  (`brza-workflow/packages/client/bin/brza-sessions:16`, `:675-676`) [F9 · lido · 95].
- **A abertura com `operation` grava `last_send`**, e por isso o `wait` vale logo depois da abertura, sem `send`
  (`brza-sessions:95-96`, `:575-576`) [F10 · lido · 92].
- **A abertura anexa o protocolo de fim**: status de mailbox com `round_id` e `dispatchId`, `worker_done` só no
  encerramento (`brza-sessions:955-966`) [F11 · lido · 95]. O `wait --json` devolve `events` com as mensagens da mailbox
  (`brza-sessions:686-690`) [F12 · lido · 90].
- **`brza tree <nome> [--type feat|fix|docs|chore] [--base REF] [--chat SESSÃO]`** cria o worktree do `brza-studio` e
  abre a sessão pelo `--checkout`, sem `--prompt` [F13 · rodado · 90].
- **`brza sessions <nome>` aceita `--model` e `--effort`** [F14 · rodado · 95]. A memória de sessão
  `meeting-model-per-role` diz o contrário e está velha.
- **Hoje, a sessão do `brza-studio` grava a evidência no passo do plano e o worklog dela** (`references/conduct.md:31-35`);
  **o commit só sai com confirmação de Anderson** (`conduct.md:47-48`) [F15 · lido · 95].
- **`orca-chat-visuals`:** até 8 visuais por resposta, sem `100vh`, scripts inline permitidos, "Scope fixed-palette CSS to
  its mockup", "Never redefine Orca's tokens on `:root`"
  (`brza-studio/resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md:20-46`) [F16 · lido · 95].
- **Os tokens do `brza-studio`:** `main.css:194` abre o `:root` com os tokens da marca, e o arquivo tem 520 linhas que
  começam com `--` [F17 · rodado · 90]; o `mobile-theme.ts` diz na linha 1 que espelha os tokens do `main.css` e exporta
  `colors` (:146), `spacing` (:173), `radii` (:182), `typography` (:202) e `feedback` (:210) [F18 · lido · 92].
- **O emulador mobile do `brza-studio` não traz moldura reaproveitável:** a pasta tem só componentes do painel de
  configuração (`MobileEmulatorSettingsPane.tsx`, `…AgentControlRow.tsx`, `…Examples.tsx`), supondo que os nomes dizem o
  conteúdo [F19 · rodado · 80].
- **Custo de consultor:** o `designer` por `Agent` custa US$ 2,82 de mediana, com p90 de US$ 4,37 e 7,8 min, em 25
  medições; o primeiro turno de uma sessão nova custa US$ 0,60 de mediana, em 91 sessões desde 2026-11-01
  (`.measurements/measurements.jsonl`) [F20 · rodado · 90].
- **A calibração das horas:** no PLN-017, o P1 (skill) teve 10,5 h estimadas e ~4 h executadas, o P2 (painel) 6,5 h e ~2 h,
  os dois sem medição, e o P5, 1 h e 0,174 h pela janela da sessão executora (`PLN-017-plan.md:308`, `:321`, `:371`)
  [F21 · lido · 95].
- **Os evals da `meeting-runner`** têm 6 casos (`evals/evals.json`) [F22 · rodado · 95].
- **`.sessions/` e `.measurements/` estão no `.gitignore`** [F23 · rodado · 95].
- **O `settings.json` não tem `permissions` nem `additionalDirectories`** [F24 · rodado · 90]. Não sei se o executor
  aberto no `brza-studio` pede permissão para gravar no worktree do playground: a norma de hoje já manda ele gravar lá
  (F15), mas não achei registro de que gravou sem pedir [F25 · inferido · 55].

---

### D1 — O código comum — `.claude/scripts/skillkit/` (P1)

- **Origem:** R3.2, R3.3.
- **Contexto:** abrir, enviar, esperar, ler o mapa, medir e salvar o visual estão escritos uma vez, misturados ao manifesto
  de reunião (Terreno §1). Três skills vão precisar disso.

#### As alternativas

##### A1 — Pacote `skillkit` com `_kit.py` em cada skill (recomendada)

- **Custo:** ~3 h, com a migração e os 323 testes de novo [C1 · inferido · 70] · **Se paga:** no P3, que é o primeiro
  script do `plan-runner` a abrir sessão · **Reabre:** nada; a promoção ao `core/` leva `.claude/scripts/` ao
  `core.lock`.

##### A2 — Módulos soltos em `.claude/scripts/` (`sessions_map.py` na raiz)

- **Custo:** ~2,5 h [C2 · inferido · 65], e o nome colide: a `meeting-runner` já tem `sessions_map.py` na pasta dela, e
  o primeiro da lista em `sys.path` vence · **Se paga:** nunca, enquanto houver módulo homônimo · **Reabre:** a ordem do
  `sys.path` em cada script.

> **O que caiu no ataque:** `PYTHONPATH` no lugar do `_kit.py` cai, porque a convenção roda tudo com `python3 -I`, que
> ignora `PYTHON*` (F1). O symlink `skills/<x>/scripts/skillkit → ../../../scripts/skillkit` cai na promoção: o
> `brza sync` não levava symlink (memória `estimativa-de-norma-pelo-sync`).

#### Como fica

```
.claude/scripts/
  README.md                 o que mora aqui, a regra do import, como rodar os testes
  skillkit/
    __init__.py
    paths.py                default_root(), common_root(root), strip_measurement(text)
    sessions_map.py         o de hoje, sem dispatch_of (que fica na meeting-runner)
    sessions_cli.py         corredores e argv do `brza sessions` v2
    measure.py              load_jsonl, parse_ts, session_ids, win_bounds, measure_claude, measure_codex
    visual.py               save_visual, safe_title, render_png (brza shot; Chrome de reserva), LIMIT_HTML
  tests/
    _paths.py               põe .claude/scripts no sys.path (ou SKILLKIT)
    test_paths.py  test_sessions_map.py  test_sessions_cli.py  test_measure.py  test_visual.py
```

**O import**, idêntico nas três skills (`.claude/skills/<x>/scripts/_kit.py`):

```python
"""Põe `.claude/scripts/` no sys.path (ou `SKILLKIT`, para rodar contra outra cópia). Importar antes de `skillkit`."""
import os
import sys

KIT = os.environ.get("SKILLKIT") or os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "..", "scripts"))
if KIT not in sys.path:
    sys.path.insert(0, KIT)
```

e no script: `sys.path.insert(0, AQUI); import _kit; from skillkit import sessions_map, sessions_cli`.

**`sessions_cli.py`**, extraído de `launch_persona.py:140-212` e `wait_round.py:153-196`, sem o manifesto de reunião:

| Função | Assinatura | O que faz |
| :-- | :-- | :-- |
| `run_sessions` | `(argv) -> (rc, out, err)` | `brza sessions …` sem shell; `rc 127` sem o `brza` |
| `run_brza` | `(argv) -> (rc, out, err)` | `brza …` (o `orchestration worker-show`) |
| `open_argv` | `(name, *, agent, checkout, prompt_file, title, model=None, effort=None, rename=False) -> list` | a forma de `launch_persona.py:140-146`; o Antigravity sem modelo |
| `send_argv` | `(names, text=None, file=None, operation=None) -> list` | `send … --json` |
| `wait_argv` | `(names, timeout_s, *, any_=True, markers=()) -> list` | `wait … --json`, um `--marker` por item |
| `close_argv` | `(name, mode="close"\|"stop"\|"keep-open") -> list` | `close [--force\|--keep-open] --json` |
| `interpret_open` | `(rc, out, err) -> "aberta"\|"ja"\|"nao-abriu"\|"sem-id"\|"falha"` | a de `launch_persona.py:203-212` |
| `wait_brza` | `(names, timeout_s, markers=()) -> dict` | roda o `wait` e devolve o JSON (`done`, `pending`, `timed_out`, `events`) |
| `list_states` | `(names, list_json=None) -> {nome: estado}` | o `fetch_states` de hoje, com a lista de nomes no lugar do manifesto |

**`visual.py`:** `save_visual(doc, prefix, part, key, title, *, publish_dir=None, default_path=None)` com o
comportamento de `panel.py:519-539`; `render_png(html_path, png, width, height=None, *, theme="light", scale=1, chrome_css="")` roda o
`brza shot <html> <png> --width W --theme T --scale S --force` e só cai no Chrome headless se o `brza` faltar ou sair ≠ 0,
dizendo isso no erro. `height` só vale para o Chrome (padrão 2000); o `brza shot` mede a
altura sozinho. `chrome_css` vai só ao HTML temporário do Chrome. A escala padrão 1 mantém o tamanho do PNG do painel de hoje **[sem lastro, menor]**.

**A migração da `meeting-runner`:** cada módulo dela importa por nome do `skillkit`
(`from skillkit.sessions_map import fold_map, load_map, map_file, read_rows, epoch, common_root`); `sessions_map.py`
local vira um shim de três linhas mais o `dispatch_of`. Os nomes que os 323 testes já chamam ficam como apelido no
módulo dela: `default_root as raiz_padrao`, `strip_measurement as corta_medida`, `interpret_open` como
`interpreta_abertura`, `LIMIT_HTML as LIMITE_HTML`, `PublishError as ErroPublicacao`, e `panel.py` embrulha
`save_visual` / `render_png` em `salva_visual` / `gera_png`. `tally.py` lê o `measure` e devolve as chaves que a
reunião já gravava (`custo_usd`, `latencia_s`, `entrada`, `saida`). A troca por atribuição dos testes continua valendo (F3).

**Conferência:** os 323 testes da `meeting-runner` e os do kit, nos dois comandos:

```bash
python3 -I -m unittest discover -s ".claude/skills/meeting-runner/scripts/tests"
```

```bash
python3 -I -m unittest discover -s ".claude/scripts/tests"
```

#### Em aberto

- O nome `skillkit` **[sem lastro, menor]**.

---

### D2 — O `plan-runner` coordenador — `.claude/skills/plan-runner/` (P6)

- **Origem:** R3.1, R1.3, R2.2, Pedido 1 e 2.
- **Contexto:** hoje a skill é só prosa: SKILL.md com 211 linhas e quatro references [F26 · rodado · 95]. O passo de
  código "roda numa sessão nova" sem quem a abra nem leia a evidência (F15).

#### Como fica — a estrutura

```
.claude/skills/plan-runner/
  SKILL.md                         ≤ 300 linhas (a meeting-runner tem 278)
  references/
    plan-template.md               o molde (mantido; ganha a nota do manifesto de execução)
    open-and-plan.md               abrir, entrevistar, planejar (sai o Desenhar)
    design.md                      desenhar: Terreno, itens D, artboards pela screen-artboards
    consultants.md                 o laço consultor por Agent e por sessões (R2.3), o pedido, a devolução lado a lado
    conduct.md                     retomar e executar um passo pelo executor
    step-request.md                o molde do pedido do passo e o protocolo de fim do executor
    review.md                      pedir a revisão e a forma do achado (sai do conduct.md)
    close.md                       fechar, com o close_check.py
    narration.md                   o que vai ao chat, o painel, a hora
  scripts/
    _kit.py  plan_md.py            o leitor do plano (frontmatter, seções, IDs), comum aos scripts abaixo
    plan_state.py  step_request.py  round_log.py  close_check.py      (D6)
    executor.py                    (D3)
    consult.py                     (D4)
    plan_panel.py                  (D5)
    tests/  (_paths.py, fixtures/ com cópias de PLN-017 e PLN-021, test_*.py)
  evals/evals.json
```

#### Como fica — a SKILL.md, por seção

1. **Frontmatter**, com a descrição de hoje e o gatilho negativo novo: "Não use se você é a sessão executora de um passo
   (o seu prompt começa com 'Você executa o passo Pn do PLN-NNN')". O mesmo vale para o consultor ("Você é consultor do
   Desenho de …").
2. **Estado:** v1, protótipo na branch `workstream/playground` (R3.1); a promoção ao `core/` fica fora de escopo.
3. **Quem é quem:**
   - **a coordenação** é a sessão principal: pergunta, abre e acompanha executores e consultores, confere e grava o plano;
   - **o executor** é uma sessão aberta pelo `executor.py`, que grava só o código do passo e o worklog dele, nunca o plano,
     nunca pergunta, e para no desvio que muda o `D`;
   - **o consultor** é um `Agent` ou uma sessão (R2.3), e grava só o arquivo de alternativa dele;
   - **Anderson decide** e ordena cada passo.
4. **Os arquivos e quando ler**, no formato da `meeting-runner` (`SKILL.md:30-49`) [F27 · lido · 95]:

| Preciso de… | Leia / rode |
| :-- | :-- |
| situar o trabalho, decidir se é plano e onde mora | esta SKILL.md, Passos 0 a 2 (mantidos) |
| o molde, antes da primeira linha | `references/plan-template.md` |
| abrir, entrevistar, planejar | `references/open-and-plan.md` |
| gravar a rodada respondida na Entrevista | `$S/round_log.py PLN-NNN --from rodada.json` (o próximo R: `--next`) |
| desenhar: Terreno, itens D | `references/design.md` |
| alternativa de tela | a skill `screen-artboards` (D7) |
| consultores: Agent ou sessão, e a rodada lado a lado | `references/consultants.md`; `$S/consult.py open\|wait\|table PLN-NNN D<n>` |
| retomar: onde o plano está, o próximo passo, o que não confere | `$S/plan_state.py PLN-NNN` (`--fix` reescreve as horas) |
| executar um passo por sessão | `references/conduct.md`, `references/step-request.md`; `$S/executor.py open PLN-NNN P<n>` |
| esperar o executor, ler a evidência, fechar a sessão | `$S/executor.py wait\|evidence\|close PLN-NNN P<n>` |
| o painel do plano | sai sozinho dos scripts que mudam o estado; à mão, `$S/plan_panel.py publish PLN-NNN` |
| o que dizer no chat | `references/narration.md` |
| pedir a revisão, a forma do achado | `references/review.md` |
| fechar | `references/close.md`; `$S/close_check.py PLN-NNN` |
| conferir as notas, mover o plano | `../notes-checker/SKILL.md` |

   **Convenção:** da raiz do worktree, `python3 -I .claude/skills/plan-runner/scripts/<script>.py` (`$S`). O plano é
   resolvido pelo `PLN-NNN` (`plans/PLN-NNN-*/PLN-NNN-plan.md`) ou pelo caminho, e o manifesto de execução é
   `.sessions/pln-nnn/execucao.json`, na raiz do worktree, fora do git (F23).
5. **Passos 0 a 2** (situar, isso é plano?, uma sessão ou várias): mantidos como estão (`SKILL.md:32-88`).
6. **Quem grava, o nome, a pasta e os IDs:** mantidos (`SKILL.md:90-139`). Acrescenta: "a coordenação é a única que grava
   o plano; o executor grava o código e o worklog dele, e a evidência chega ao plano pelo `executor.py evidence`".
7. **O laço consultor:** resumo de 6 linhas, com o detalhe em `references/consultants.md` (D4).
8. **Operações:** a tabela de hoje, com as references novas.
9. **Invariantes:** as de hoje (`SKILL.md:175-200`), mais duas:
   - **"O executor não grava o plano."** Duas mãos no plano produzem dois estados (a mesma razão da invariante de hoje).
   - **"A narração e o painel saem dos scripts, não da memória"**, pela lição da R10.1 do PLN-017: a regra escrita deixou
     de ser cumprida em 3 aberturas e todas as chegadas (`meeting-runner/SKILL.md:125-130`) [F28 · lido · 95].

#### Como fica — a narração (`references/narration.md`)

Pela memória `coordination-narration-in-chat` e pela minha `decisor-quer-estado-e-numeros-no-chat`, o chat leva o estado
e os números, e o texto integral vai por caminho:

| Momento | O que vai ao chat |
| :-- | :-- |
| abertura de um executor | a tabela `Passo · executor · runtime · modelo · esforço · checkout · branch`, impressa pelo `executor.py open`, e o painel |
| cada evento do `wait` | uma linha "P3 · feito em 18 min; P5 · em curso 6 min", e o painel atualizado |
| evidência | a linha `**Evidência:**` proposta, o que a coordenação conferiu por comando ("confere: `git -C … cat-file -e a1b2c3d` → ok; `<testes>` → 42 passed") e o `Executado` medido |
| desvio | o `X` proposto, uma linha, e a rodada se ele muda um `D` |
| consultores | ver D4 e o R5.4 |
| hora | `date '+%H:%M:%S'`, rodado na hora |

#### Em aberto

- Quando a versão nova passa a conduzir o próprio PLN-021: ver o R5.7.

---

### D3 — As sessões executoras — `scripts/executor.py`, `references/step-request.md` (P3)

- **Origem:** R1.3(a).
- **Contexto:** abrir, enviar, esperar, ler a evidência e fechar, sem comando digitado por Anderson (Cobertura, linha 1).

#### Como fica — o manifesto `.sessions/pln-021/execucao.json`

```json
{
  "plan": "PLN-021",
  "plan_path": "plans/PLN-021-o-plano-coordenado-e-os-artboards/PLN-021-plan.md",
  "steps": {
    "P3": {
      "session": "pln021-p3",
      "agent": "claude", "model": "claude-opus-5-5", "effort": "high",
      "checkout": "/Users/andepb/Projects/brza-studio/.worktrees/pln-021-p3",
      "branch": "feat/pln-021-p3",
      "request": ".sessions/pln-021/P3/pedido.md",
      "worklog": "work/worklogs/2026-11-10-pln-021-p3-o-executor.md",
      "marker": "fim-P3:",
      "state": "aberto",
      "events": [{"at": "2026-11-10T14:02:11-03:00", "state": "aberto", "note": "open: pln021-p3"}],
      "evidence": null,
      "measurement": null
    }
  }
}
```

O arquivo continua `.sessions/pln-nnn/execucao.json`. O valor de `state` ∈ `aberto` → `em-curso` → `feito` | `parado` (desvio que muda o `D`) | `bloqueado` (o chat pede resposta) |
`falhou` → `evidencia-gravada` → `fechado`. O mapa de identidade (Dispatch, Run, id do provedor) continua só no
`.sessions/sessions.jsonl` da raiz comum: o manifesto guarda o nome da sessão, e o resto vem do `sessions_map`.

#### Como fica — a CLI

```
executor.py open     PLN-NNN Pn [--agent claude|codex|grok] [--model M] [--effort E]
                                [--checkout CAMINHO | --tree NOME [--type feat|fix|docs|chore]] [--no-panel] [--dry-run]
executor.py send     PLN-NNN Pn (--text T | --file F) [--operation OP]
executor.py wait     PLN-NNN [Pn …] [--timeout SEG] [--no-panel]
executor.py evidence PLN-NNN Pn [--apply] [--settle 60]
executor.py close    PLN-NNN Pn [--keep-open | --stop] [--wait-settled SEG]
executor.py status   PLN-NNN [--json]
```

- **`open`:** com `--tree`, roda `brza tree <nome> --type <t>` (F13); gera o pedido pelo `step_request.py` (D6); cria o
  worklog do executor pelo molde, com as seções a preencher e sem o marcador; abre
  `brza sessions pln021-p3 --agent … --model … --effort … --checkout <abs> --prompt-file pedido.md
  --title "PLN-021 P3: <título do passo>" --rename --wait` (F14); grava o manifesto, publica o painel e imprime a tabela.
  O padrão é `--agent claude` com o modelo da camada do passo: Sonnet para a implementação, pela tabela do `AGENTS.md`
  **[sem lastro, menor]**. A saída segue `interpret_open`: "não abriu" não se relança antes do `pending-*.json`.
- **`wait`:** `brza sessions wait <sessões> --any --marker <worklog>:<!-- fim-Pn: --timeout T --json` (F9, F10). O
  `ended_without_marker` não é fim: a linha diz "o turno acabou sem o marcador" e a espera segue até o prazo. O marcador
  com `feito` vai a `feito`; com `parado`, a `parado`; o `blocked` do `wait`, a `bloqueado`. Saída: 0 com algum feito ou
  parado, 3 com bloqueado (a coordenação lê pelo `brza sessions read --last`), 1 com falha, 75 no prazo. Cada evento
  atualiza o manifesto e republica o painel.
- **`evidence`:** lê a seção `## Evidência` do worklog do executor e confere por comando: cada commit com
  `git -C <checkout> cat-file -e <sha>`, cada comando de teste rodado de novo quando a linha traz `(≤ 2 min)`; mede o
  `Executado` pela janela da abertura ao marcador no `measurements.jsonl` (`measure.measure_claude`; Codex pelo rollout;
  Grok e Antigravity, `sem medição`). O `--settle` espera a linha do `Stop`, como no `tally.py`. Sem `--apply`, imprime a
  linha `**Evidência:**` e o `Executado` propostos; com `--apply`, grava no `### Pn` do plano, marca `[x]` nos subpassos
  que a evidência cobre, roda o `plan_state.py --fix` e publica o painel. **O `--apply` só roda depois de a coordenação
  ler a proposta** (regra da SKILL.md, não do script).
- **`close`:** o `close` do `brza sessions` e a conferência do aceite, com o `veredito` de `launch_persona.py:360-447`
  movido ao `sessions_cli`.

**O `Executado`** é a janela da abertura ao marcador, como o P5 do PLN-017 mediu (F21), com a soma dos turnos entre
parênteses: `Executado: 0,6 h (janela; 0,4 h de turnos; US$ 3,10)`. A janela acaba no marcador, antes da ida e volta do
commit, e por isso não conta a espera por Anderson.

#### Como fica — o molde do pedido (`references/step-request.md`, gerado pelo `step_request.py`)

```markdown
Você executa o passo P3 do PLN-021 numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você não
conduz o plano, executa um passo dele.

## O passo
<o ### P3 inteiro, copiado do plano: título, Executa, Estimado, subpassos>

## O que o Desenho fixou
<o texto de cada D citado no "Executa", da Origem ao Em aberto>

## O que as rodadas decidiram
<cada R citado na Origem dos D, com a pergunta, a opção escolhida e a resposta literal>

## Restrições e Regressão
<as do plano, copiadas>

## Onde trabalhar
- checkout: /Users/andepb/Projects/brza-studio/.worktrees/pln-021-p3 (branch feat/pln-021-p3)
- worklog: /Users/andepb/Projects/brza-workspace/.worktrees/playground/work/worklogs/2026-11-10-pln-021-p3-….md

## Regras
- Não grave o plano, não commite nada no brza-workspace, não pergunte a Anderson.
- Desvio local: registre no worklog como `X` proposto e siga. Desvio que muda o contrato do D: pare, registre e feche
  com `parado`.
- <o commit: pela resposta ao R5.1>

## O fim
1. Preencha `## Evidência` no worklog, uma linha por item:
   - `commit: brza-studio@<sha7>` (ou `commit: aguarda confirmação`)
   - `comando: \`<comando>\` → <resultado> (≤ 2 min)` quando roda em até dois minutos
   - `arquivos: <caminho>, …`
   - `desvios: X? — <uma linha>` ou `desvios: nenhum`
2. A última linha do worklog é `<!-- fim-P3: feito -->` ou `<!-- fim-P3: parado -->`.
3. Envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o encerramento.
```

#### As alternativas — onde o executor devolve a evidência (R5.2)

##### A1 — No worklog do executor, no workstream, com o marcador (recomendada)

- **Custo:** a coordenação cria o worklog antes de abrir (~5 min de script, já no P3) e commita o worklog junto do plano
  [C3 · inferido · 70] · **Se paga:** no primeiro passo, porque o worklog é o registro que a norma já pede ao executor
  (F15) e o `--marker` do `wait` lê dele (F9) · **Reabre:** nada.

##### A2 — Num arquivo em `.sessions/pln-nnn/Pn/evidencia.md`, fora do git

- **Custo:** o mesmo script, e um arquivo a mais que some com o `.sessions/` (F23); o worklog do executor continua
  existindo à parte [C4 · inferido · 70] · **Se paga:** só se o worklog do executor deixar de existir · **Reabre:** a
  norma do worklog do executor.

> **O que caiu:** o executor gravar direto no `### Pn` do plano, como hoje (F15), cai pela R1.3: é a coordenação que
> "traz a evidência ao plano". **O ataque à A1 que ficou de pé:** o executor do `brza-studio` grava fora do checkout dele;
> se o Claude pedir permissão para isso (F25), o executor trava em `blocked`. O mesmo vale para a A2. A sonda é o
> primeiro subpasso do P3.

#### Em aberto

- O commit do executor: R5.1.

---

### D4 — Os consultores em sessão — `scripts/consult.py`, `references/consultants.md` (P5)

- **Origem:** R1.3(b), R2.3.
- **Contexto:** o laço por `Agent` continua o padrão; a sessão entra só no gatilho da R2.3.

#### Como fica — o gatilho, escrito na reference

A coordenação abre consultores em sessão quando **as duas** condições valem: (a) 3 ou mais alternativas defensáveis, e
(b) a escolha é cara de reverter: contrato entre partes, formato de dado gravado, norma. Também abre quando Anderson pede.
No resto, `Agent`, como hoje. A coordenação narra o gatilho numa linha antes de abrir: "D4: 3 alternativas, formato do
manifesto (dado gravado) → consultores em sessão (R2.3)".

#### Como fica — a CLI e os arquivos

```
consult.py open  PLN-NNN D<n> --brief brief.md [--roster padrao|<arquivo.json>] [--dry-run]
consult.py wait  PLN-NNN D<n> [--timeout SEG]
consult.py table PLN-NNN D<n> [--publish-dir DIR]
consult.py close PLN-NNN D<n>
```

- **O pedido** (`brief.md`), que a coordenação escreve, traz o Terreno, os casos sobre os quais comparar e as rodadas
  citadas; o `open` acrescenta o foco de cada consultor e o protocolo de fim.
- **Cada consultor grava só** `.sessions/pln-nnn/D<n>/<foco>.md`, numa forma fixa: tese, "Como fica" da alternativa,
  `Custo:` · `Se paga:` · `Reabre:` sobre os casos dados, ataque às outras duas, o que enfraquece a própria e
  `<!-- fim-D<n>: <foco> -->`. Sessão aberta no worktree do playground, só leitura no resto.
- **`table`** junta os três arquivos numa tabela lado a lado (linhas: custo, se paga, reabre, risco; colunas: os focos),
  em Markdown para a mensagem e em `::orca-visual` pelo `visual.save_visual`.
- **O roster padrão:** três focos da SKILL.md de hoje (mudança mínima, arquitetura limpa, equilíbrio,
  `SKILL.md:159-161`), cada um num runtime: R5.3.

#### Em aberto

- O que vai ao chat: R5.4.

---

### D5 — O painel do plano — `scripts/plan_panel.py` (P4)

- **Origem:** R1.3(c).
- **Contexto:** "gerado por script a cada mudança de estado" (R1.3). Leio isso como os scripts que mudam o estado
  republicando sozinhos, pelo precedente da R10.1 do PLN-017 (F28).

#### Como fica

```
plan_panel.py publish PLN-NNN [--publish-dir DIR] [--png CAMINHO] [--width 736] [--at ISO]
plan_panel.py render  PLN-NNN --out arquivo.html
```

- **Quem chama:** `executor.py` (open, cada evento do `wait`, `evidence --apply`, `close`), `round_log.py` e
  `plan_state.py --fix`, por import (`plan_panel.publish_safe(...)`), com `--no-panel` para desligar. `⚠ painel: …` não muda
  o código de saída.
- **O que mostra:**
  - o cabeçalho: o PLN, o H1, `phase`/`status`, o `ready`, as horas `estimate/executed/remaining` e a soma conferida
    pelo `plan_state` (com `⚠` quando diverge);
  - uma linha por passo: ID, título curto, `Executa`, executor, estado do manifesto, Estimado × Executado, custo medido e
    a idade do último evento;
  - os executores e consultores vivos, com o estado do `brza sessions list --json`;
  - a última rodada, como `R3 — 3 perguntas, 3 decididas`.
- **O arquivo:** `pln-nnn-painel-<hash4>.html` pelo `save_visual`, com a chave `PLN-NNN|AAAA-MM-DD`: um arquivo por
  plano e dia, republicado no mesmo nome **[sem lastro, menor]**. O PNG sai na abertura e no fechamento de cada executor,
  como a R10.3 do PLN-017 fez para a reunião (`meeting-runner/SKILL.md:126-128`).
- **Os dados:** `plan_state.state(plan)` (D6), o manifesto, o `sessions_map` e o `measure`. Sem `measurements.jsonl`,
  "sem medição", nunca zero.

---

### D6 — Os quatro scripts de R2.2 — `scripts/{plan_state,step_request,round_log,close_check}.py` (P2)

- **Origem:** R2.2.
- **Contexto:** o `check_notes.py` cobre o frontmatter e os links, mas não soma as horas, não confere IDs, nem o `[x]`
  com evidência, nem a origem do `D` (Terreno §3). Os quatro scripts usam o leitor `plan_md.py`, que entende `-plan.md`,
  `-interview.md` e `-design*.md` divididos.

#### `plan_state.py`

```
plan_state.py PLN-NNN|caminho [--json] [--next] [--fix] [--strict]
```

- **Saída** (`--json`):
  `{plan, file, title, phase, status, ready, next: "P4"|null, steps: [{id, title, executes: ["D3"], executor, estimated_h,
  executed_h, state: "pendente"|"feito"|"descartado", evidence: bool}], hours: {frontmatter: {...}, summed: {...},
  matches: bool}, ids: {R: [...], D: [...], P: [...], X: [...], A: [...], C: [...]}, problems: [{code, where, msg, level, line}]}`.
  Sem `--json`, uma tela: onde o plano está, o próximo passo e os problemas.
- **Códigos:** `checked-without-evidence` (o `[x]` sem `**Evidência:**`, ou com uma que não traz commit, comando com
  `→` nem `arquivo:linha`); `checked-without-executed`; `hours-mismatch`; `step-without-design` (o passo sem
  `Executa D…`, salvo os de rodada e "a pedido"); `step-cites-unknown-design`; `design-without-origin`;
  `origin-unknown-round` (o `D` cita um `R` que a Entrevista não tem); `deviation-not-cited` (o `X` que nenhum passo cita);
  `duplicate-id`.
- **`--fix`** reescreve só as três horas do frontmatter, pela soma das linhas `Estimado`/`Executado`. **`--next`**
  imprime só o próximo passo. Saída 0 limpo, 1 com problema (com `--strict`, também os avisos), 2 uso.

#### `step_request.py`

```
step_request.py PLN-NNN Pn [--out ARQUIVO] [--worklog CAMINHO] [--checkout CAMINHO] [--branch NOME]
```

- Monta o pedido do molde do D3, com o passo, os `D` do `Executa`, os `R` das origens (pergunta, opção escolhida,
  resposta literal), as Restrições e a Regressão. Recusa, com saída 1, o passo sem `D` quando o plano tem Desenho, e o
  `R` citado que não existe. Imprime o caminho gravado.

#### `round_log.py`

```
round_log.py PLN-NNN --next
round_log.py PLN-NNN --from rodada.json [--dry-run]
```

- **`rodada.json`:**

```json
{
  "title": "o nome, o executor, os consultores",
  "sent_on": "2026-11-10",
  "presented_before": "o texto do bloco citado",
  "answered": {"data": "2026-11-10", "session": "a sessão do workstream playground"},
  "questions": [
    {
      "topic": "O commit do executor",
      "multiple": false,
      "options": [
        {"label": "o pedido do passo autoriza o commit na branch do passo", "recommended": true,
         "cost": "…", "pays_when": "…"},
        {"label": "o executor para antes do commit", "cost": "…", "pays_when": "…"}
      ],
      "answer": {"chosen": [0], "literal": null, "reading": null},
      "reopens": null
    }
  ]
}
```

- Acrescenta `### Rodada N — <título> (enviada <data>)` na Entrevista (no `-interview.md` quando ele existe), com o
  "Apresentado antes", as opções no formato do molde (`plan-template.md:127-143`), e **Decidido — …** quando há
  `chosen` sem `literal`; **Resposta:** "…" com a leitura, quando há `literal`. Com `reopens: "R1.2"`, acrescenta
  "**→ reaberta em RN.k**" à linha antiga. O N sai do maior `### Rodada` + 1. Saída 0, 1 com JSON fora da forma.
  `literal` fica; o Markdown gravado no plano continua em pt-BR.

#### `close_check.py`

```
close_check.py PLN-NNN [--json]
```

| Item de `close.md` | Como confere | Resultado |
| :-- | :-- | :-- |
| 1 — passo `[x]` com evidência ou `[-]` com motivo | `plan_state` | `ok` / `falta` |
| 2 — achado com destino que existe | cada `REV` de `## Revisões`: `### A<n>` com `→ destino` ≠ `a definir`, e o link do destino existe | `ok` / `falta` |
| 3 — o durável na casa dona | lista os `R` decididos sem `D` nem link em `## Decisões`: candidatos, não veredito | `manual` com a lista |
| 4 — decisões `done` | o `status` de cada nota de `## Decisões` | `ok` / `falta` |
| 5 — o resumo no commit ou PR | `não se aplica` sem commit do `brza-studio` na evidência; com commit, `manual` | `manual` / `n/a` |
| 6 — a Janela fechada | com `## Janela`, a linha de fecho | `ok` / `falta` / `n/a` |

Saída 0 só com tudo `ok` ou `n/a`, mais os `manual` listados; 1 com algum `falta`.

---

### D7 — A skill `screen-artboards` — `.claude/skills/screen-artboards/` (P7)

- **Origem:** R1.4, R2.4.
- **Contexto:** não há molde de tela nem moldura (Terreno §4), e o emulador do `brza-studio` não tem moldura
  reaproveitável (F19).

#### Como fica — a estrutura

```
.claude/skills/screen-artboards/
  SKILL.md
  references/
    frames.md          as molduras, a largura nominal de cada uma e quando usar
    tokens.md          o pacote, os nomes --sa-*, a extração, a deriva, o pacote neutro
    chat-rules.md      as regras do orca-chat-visuals que valem aqui e a conferência pelo PNG
    design-round.md    como o Desenho do plan-runner a aciona: letra no título, PNG à pasta do plano
  scripts/
    _kit.py  artboard.py  tokens.py
    frames/            macos.html  windows.html  iphone.html  android.html  browser.html   (CSS + HTML, sem imagem)
    packs/             brza-studio.json  neutral.json
    tests/
  evals/evals.json
```

#### Como fica — a SKILL.md, a tabela

| Preciso de… | Leia / rode |
| :-- | :-- |
| um artboard novo de tela | `references/frames.md`; `$A/artboard.py new <slug> --frame … --pack … --body tela.html` |
| os tokens de um projeto, e se derivaram | `references/tokens.md`; `$A/tokens.py check brza-studio` |
| extrair o pacote de novo | `$A/tokens.py extract brza-studio` |
| conferir pelo PNG, em cada largura | `$A/artboard.py shot <artboard>.html --out-dir <scratch>` e ler as imagens |
| levar a escolhida ao plano ou à issue | `$A/artboard.py promote <artboard>.html --plan PLN-NNN --name <assunto>` (ou `--issue <nota>`) |
| as regras do visual no chat | `references/chat-rules.md` |
| a rodada de desenho com alternativas de tela | `references/design-round.md` |

#### Como fica — a CLI

```
artboard.py new <slug> --frame macos|windows|iphone|android|browser [--widths 375,768,1280]
                [--pack brza-studio|neutral] [--scheme light|dark|both] [--letter A] [--title T]
                --body FRAGMENTO.html [--publish-dir DIR]
artboard.py shot <artboard.html> --out-dir DIR [--theme light|dark]
artboard.py promote <artboard.html> (--plan PLN-NNN | --issue CAMINHO) --name ASSUNTO [--width N]
tokens.py extract brza-studio|<projeto> [--src CAMINHO]
tokens.py check   brza-studio|<projeto>
tokens.py list
```

- **`new`:** embrulha o fragmento da tela (o HTML que o agente escreve com `var(--sa-*)`) na moldura, com o CSS do pacote
  **escopado no contêiner do mockup** (`.sa-art[data-pack=…][data-scheme=…] { --sa-background: …; }`), nunca em `:root`
  (F16). Grava `<slug>-<frame>-<hash4>.html` no `ORCA_CHAT_SCRATCH_DIR` (ou `--publish-dir`, ou o scratch) e imprime
  `::orca-visual{file="…" title="A — <título>"}`. Confere antes de gravar: < 512 KB, nenhum `http`, `100vh` nem
  `:root { --background`; o erro sai com a linha. Com `--pack brza-studio`, roda o `tokens.check` e avisa a deriva sem
  barrar.
- **O ajuste à largura do chat:** cada moldura tem a largura nominal (janela 1280×800, iPhone 393, Android 412, navegador
  375/768/1280) e um script inline aplica `zoom = min(1, largura do contêiner / nominal)`. Sem ele, 1280 px sai cortado a
  736 (F8).
- **As larguras:** um artboard por alternativa, com as larguras empilhadas; para o PNG, o `shot` gera uma variante por
  largura no scratch e tira um PNG de cada, com `--width` = a nominal + a margem da moldura (R5.5).
- **`shot`:** `brza shot` por largura e por tema (F7), `~1,2 s` cada (F8), e imprime os caminhos para a leitura.
- **`promote`:** `brza shot <artboard> plans/PLN-NNN-…/PLN-NNN-<assunto>.png --width <nominal>`, ou
  `work/issues/<nome>.png`, pela regra de `open-and-plan.md:62-65`, e imprime o link Markdown para o item `D`.

#### Como fica — o pacote (`packs/brza-studio.json`)

```json
{
  "id": "brza-studio",
  "extracted_at": "2026-11-10",
  "origin": {
    "desktop": {"file": "~/Projects/brza-studio/src/renderer/src/assets/main.css", "sha256": "…",
                "blocks": [":root", ".dark"]},
    "mobile": {"file": "~/Projects/brza-studio/mobile/src/theme/mobile-theme.ts", "sha256": "…",
               "exports": ["lightColors", "darkColors", "spacing", "radii", "typography"]}
  },
  "mobile_pairs": {"m-bg-base": "background"},
  "schemes": {
    "light": {"background": "#ffffff", "foreground": "…", "primary": "…", "border": "…", "radius": "0.625rem",
              "m-bg-panel": "…", "m-bg-raised": "…"},
    "dark":  {"background": "#0a0a0a", "...": "..."}
  },
  "fonts": {"sans": "…", "mono": "…"},
  "spaces": {"…": "…"}
}
```

- **Os nomes:** os 26 tokens que o `orca-chat-visuals` expõe (F16), com o prefixo `--sa-`, mais os do mobile que não têm
  par no desktop, com `--sa-m-` **[sem lastro, menor]**.
- **`tokens.py extract`** lê o `:root` e o `.dark` do `main.css` e os objetos do `mobile-theme.ts` por regex (sem Node),
  e grava o JSON com o `sha256` de cada fonte. **`check`** compara o hash e, se mudou, extrai de novo em memória e
  imprime os tokens que mudaram: `⚠ deriva: main.css mudou desde 2026-11-10 — 3 tokens: --primary, --ring, --chart-2;
  rode tokens.py extract brza-studio`. Saída 0 sem deriva, 4 com deriva, 1 com fonte ausente.
- **O pacote neutro:** cinzas e um acento, nos mesmos nomes, para wireframe e projeto sem tokens.

#### Como fica — como o Desenho a aciona (`plan-runner/references/design.md`)

"Opção que muda o que se vê: aciona a `screen-artboards`, um artboard por alternativa, com a letra da opção no `title`;
confere cada um pelo `shot` antes da rodada; a escolhida vai ao plano pelo `promote`, e o item `D` linka o PNG." Isso
substitui o parágrafo de `open-and-plan.md:57-65`.

#### Em aberto

- ~~O tema do artboard: R5.6.~~ Decidido em R4.6 (Rodada 5): o desktop do `brza-studio` usa os tokens vivos do
  chat (`.sa-art[data-live]` mapeia `--sa-*` para `var(--…)`, sem `--scheme`; o `shot` injeta o fallback só no PNG); o
  mobile, o navegador, o `neutral` e os outros projetos seguem com o pacote escopado. **Descartada:** o pacote em todo o
  desktop — o mockup não seguia o tema do chat, que Anderson quer ver.

---

### Os evals, pela `skill-creator`

Pela memória `skill-evals-need-rules-the-repo-lacks`, cada expectativa vem de uma regra que o repositório ainda não
registra. **A linha de base roda numa cópia do repositório sem a pasta viva da skill e sem `plans/PLN-021-*`**, porque o
PLN-021 já descreve as regras novas (R2.3, R2.2) e a linha de base as acharia.

**`plan-runner`** (o "antes" é o snapshot de hoje, em `/private/tmp/pln021/plan-runner-workspace/skill-snapshot/`, pelo modo de melhorar
skill da `skill-creator`):

| Caso | Regra nova que discrimina | Expectativas (exemplos) |
| :-- | :-- | :-- |
| 1. Retomar um plano com `[x]` sem evidência e horas que não batem (fixture) | `plan_state.py` como fonte; os códigos | roda `plan_state.py`; cita `checked-without-evidence` no passo certo; não marca o próximo como feito; propõe `--fix` e não o roda sem dizer |
| 2. "Execute o P3" de um plano com passo de código | `executor.py open` com `--marker` e o pedido do molde | o pedido não manda o executor gravar o plano; tem o marcador `fim-P3:`; o `wait` usa `--marker`; não manda `worker_done` |
| 3. Desenho com 3 alternativas de formato de dado | gatilho R2.3 → sessão | abre `consult.py open`; narra o gatilho; não decide |
| 4. Desenho com 3 alternativas baratas de reverter | gatilho R2.3 → `Agent` | não abre sessão; usa `Agent` |
| 5. Rodada respondida com texto livre que reabre R1.2 | `round_log.py` com `reopens` | o JSON tem `literal` e `reopens`; o próximo R está certo; não escreve "Decidido" |

O enunciado não nomeia o código nem o estado esperado, para a linha de base não acertar por raciocínio genérico
(memória, iteração 3/4).

**`screen-artboards`** (sem "antes": a linha de base é sem skill):

| Caso | Regra nova | Expectativas |
| :-- | :-- | :-- |
| 1. Duas alternativas de uma tela desktop do `brza-studio` | moldura macOS, `zoom` para caber, pacote escopado | nenhum `:root { --background`; o PNG a 736 sem corte; a letra no `title` |
| 2. A mesma tela em mobile e navegador | larguras empilhadas num artboard; PNG por largura | ≤ 8 linhas `::orca-visual`; 3 PNGs do navegador |
| 3. O `main.css` com um token mudado (fixture) | `tokens.py check` avisa a deriva | a saída cita o token; o artboard sai mesmo assim |

---


## Escolhas menores sem lastro

1. O nome `skillkit` (D1).
2. `render_png` com `--scale 1` por padrão, para manter o tamanho do PNG do painel (D1).
3. O padrão do `executor.py open`: Claude, Sonnet para a implementação (D3).
4. Um arquivo de painel por plano e dia (D5).
5. O prefixo `--sa-` e `--sa-m-` dos tokens (D7).
6. A conferência da evidência roda de novo só o teste marcado `(≤ 2 min)` (D3).
