# ADR-003: Porta única `AgentRuntime` para o `brza sessions` e a `meeting-runner`

- **Status:** Proposta (aprovada no desenho pela sala na R2 de 2026-11-14; vira Aceita com a frase do Anderson)
- **Data:** 2026-11-14
- **Autor:** Linus (Arquiteto de Soluções)
- **Incorpora:** ADR-002 (porta de runtime da `meeting-runner`), que não terá texto próprio
- **Relaciona:** PLN-024 (R1.4, invertida pela R3), PLN-025 (registro `Execution`, P3), PLN-026, E2 (`GROK_HOME`), E5 (segredos)

## Contexto

- O `brza sessions` só sabe falar com o Studio: `list`, `read` e `usage` leem o socket de `orca-runtime.json` num caminho fixo de macOS, e a abertura exige `ORCA_AGENT_SESSION_ID` ou `ORCA_TERMINAL_HANDLE`. Na cloud nada disso existe e o comando sai com rc 1 (diagnóstico bc-1ac1c85f).
- A `meeting-runner` tem a mesma dependência: precisa do Studio aberto para abrir participantes.
- Na cloud existe `CURSOR_CONVERSATION_ID` com o `bc-…` da run. Sessões, uso e transcript ficam no servidor do Cursor (`GET /v1/agents/{bc}/usage`, `agent.getUsage()`), acessíveis só com `CURSOR_API_KEY`.
- Dois consumidores com o mesmo problema pedem uma abstração só, não duas.

## Decisão

Criar uma porta `AgentRuntime` no `brza-workflow`, consumida pelo `brza sessions` e pela `meeting-runner`, com um adaptador por ambiente.

**Contrato da porta**

| Operação | Retorno | Obrigatória |
| :-- | :-- | :-- |
| `capabilities()` | conjunto de `list`, `read`, `usage`, `open`, `send` | sim |
| `list()` | lista de `SessionRecord` | sim |
| `read(id)` | transcript ou erro explícito | sim |
| `usage(id)` | tokens e custo com origem por campo | não |
| `open(spec)` | `SessionRecord` do participante aberto | não |
| `send(id, msg)` | ack | não |

`SessionRecord`: `id`, `source` (`studio` ou `cloud`), `agent`, `title`, `status`, `started_at` e, por campo de métrica, a origem (`hook`, `note`, `api` ou ausente).

**Adaptadores**

- `StudioRuntime`: socket do `orca-runtime.json` e variáveis `ORCA_*`. Todas as capacidades. Comportamento atual, sem mudança.
- `CloudRuntime`:
  - Degrau 1 (agora): lê `CURSOR_CONVERSATION_ID`; `list` devolve a run atual com o `bc-…`; `read` e `usage` respondem "ausente". Sem chave.
  - Degrau 2 (com o E5): `CURSOR_API_KEY` habilita `list` de outras runs, `read` pelo transcript da API e `usage` com origem `api`.
  - `open`: participante headless (candidato: `cursor-agent -p` na VM, a confirmar pela pesquisa da Shelly). Só é declarada quando provada.

**Regras que passam a valer**

1. Consumidor só fala com a porta, nunca com socket, variável ou API diretamente.
2. A seleção do adaptador é por detecção (socket presente → Studio; `CURSOR_CONVERSATION_ID` presente → Cloud), com `--runtime studio|cloud` para forçar.
3. Capacidade não declarada falha com rc ≠ 0 e mensagem que nomeia o runtime e a capacidade. Proibido fallback silencioso.
4. Proibido fabricar `ORCA_*` a partir do `bc-…`.
5. Registro `cloud` nunca é escrito no JSON de abas do Studio.
6. `GROK_HOME` resolvido pela mesma regra da `resolveGrokHomeDir` do Studio (E2).
7. Métrica ausente é "ausente", nunca zero.
8. Adaptador novo é arquivo novo; o agregador e os consumidores não mudam (aberto/fechado).
9. Uma suíte de testes de contrato roda contra todos os adaptadores.

## Consequências

**Positivas**
- Um padrão só para dois problemas; a `meeting-runner` roda na cloud assim que o `CloudRuntime` declarar `open`.
- O Studio não é tocado: o `StudioRuntime` encapsula o comportamento atual.
- O degrau 1 entrega o critério de aceite sem segredo novo.
- Abre caminho para outros runtimes (Codex, Antigravity) sem refatorar consumidor.

**Negativas**
- Uma camada a mais para manter, com testes de contrato próprios.
- O `CloudRuntime` depende de uma API externa que pode mudar.
- Sem `open` provado, a reunião na cloud ainda depende de uma forma headless não validada.
- A porta precisa nascer pequena; o risco é inflar com operações específicas do Studio.

## Alternativas consideradas

- **Condicionais de ambiente dentro do `brza sessions`:** mais rápido hoje, mas espalha `if cloud` pelo código e duplica na `meeting-runner`.
- **Simular o Studio na cloud (fabricar `ORCA_*` ou socket):** frágil e mistura origens; descartada.
- **Duas portas, uma por consumidor:** dobra contrato e testes para o mesmo conceito.

## Gatilhos para revisitar

- Um terceiro runtime que não caiba no contrato sem operação nova.
- A API do Cursor mudar de forma incompatível ou expor arquivo local de transcript.
- O Studio passar a ter API remota própria que torne o `CloudRuntime` redundante.
- A `meeting-runner` precisar de operação que só um adaptador consegue cumprir.

## Critério de aceite (revisão)

- [ ] `brza sessions list --json` sai 0 na cloud sem o socket e traz a run com `bc-…`, `source: cloud`.
- [ ] `--runtime cloud` com capacidade ausente sai ≠ 0 com mensagem nomeando runtime e capacidade.
- [ ] Testes de contrato passam para os dois adaptadores.
- [ ] No Mac, o comportamento do `StudioRuntime` é idêntico ao atual (regressão do PLN-013 verde).
- [ ] Nenhum `ORCA_*` criado a partir do `bc-…`; nenhum registro `cloud` no JSON de abas.
