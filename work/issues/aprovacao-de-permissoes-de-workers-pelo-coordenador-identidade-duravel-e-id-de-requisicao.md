---
status: open
description: Os PRs #41306, #41304, #41286, #41301 trazem aprovação de permissões de workers pelo coordenador, request-id, agente durável e cópia de blocos no terminal.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-12
tags:
  - tooling
  - infra
---

# Aprovação de permissões de workers pelo coordenador, identidade durável e ID de requisição

Rastreado dos PRs abertos no upstream [`stablyai/orca#41306`](https://github.com/stablyai/orca/pull/41306),
[`stablyai/orca#41304`](https://github.com/stablyai/orca/pull/41304),
[`stablyai/orca#41286`](https://github.com/stablyai/orca/pull/41286) e
[`stablyai/orca#41301`](https://github.com/stablyai/orca/pull/41301) (resolve Issue [`#40914`](https://github.com/stablyai/orca/issues/40914)).

## O problema

1. **Falta de autonomia e bloqueio humano na aprovação de ferramentas de workers delegados (`#41306`):**
   - Ao despachar subagentes e workers de orquestração a partir de um coordenador autônomo, chamadas a ferramentas de risco
     ou comandos shell ficavam retidas indefinidamente aguardando clique manual do usuário ou atingiam timeout de 2 minutos do Claude;
   - Faltava um canal controlado e auditável onde o próprio agente coordenador pudesse aprovar ou negar o prompt com uma
     justificativa (`--reason`), mantendo o humano no loop apenas para operações estritamente sensíveis (`personOnly`).
2. **Risco de disparos duplicados de workers por perda de resposta (`#41304`):**
   - Quando um cliente CLI ou orquestrador disparava um worker (`worker-start`) e a conexão caía antes do recebimento do recibo,
     reexecutar o comando podia duplicar o worker no host;
   - Além disso, não havia diferenciação clara entre opções solicitadas pelo chamador e opções nativas efetivamente confirmadas
     pelo host de execução.
3. **Inexistência de identidade estável para agentes em abas de terminal (`#41286`):**
   - Enquanto chats nativos possuem identificador estável (`orca_session_id:<id>`), agentes rodando em terminais recebiam apenas
     chaves de painel efêmeras ou o ID de sessão do provider. Ao reiniciar o app, suspender o worktree ou retomar o terminal manualmente,
     não havia endereço canônico para citar ou enviar mensagens ao agente de terminal.
4. **Dificuldade de copiar comandos e saídas isoladas no terminal (`#41301`, resolve `#40914`):**
   - Desenvolvedores precisavam arrastar o cursor do mouse manualmente por dezenas de linhas de output no terminal para copiar
     apenas o comando executado ou sua saída limpa, sujeitos a quebras indesejadas de linha ou poluição de prompts intermediários.

## O que o upstream propõe e implementa

1. **Aprovação opt-in de prompts de permissão pelo coordenador (`#41306`):**
   - Adiciona a configuração `Settings → Orchestration → "Let coordinators approve worker permission prompts"` (desativada por padrão);
   - Quando habilitada, o texto de escalação oferece comandos para o coordenador:
     - `orchestration approve --dispatch … --prompt … --reason "<motivo>"`
     - `orchestration deny --dispatch … --prompt … --reason "<o que fazer em vez disso>"`
   - Exige `--reason` obrigatório, exibe recibo auditável no chat ("Allowed by coordinator: <reason> · <time>") e adota política
     de corrida em que a primeira resposta válida vence (pessoa ou coordenador);
   - Preserva estritamente verificações `personOnly` (operações marcadas com `requiresUserInteraction` no Claude ou diálogos onde
     hooks são desautorizados), recusando aprovações automáticas com `approval_requires_person`.
2. **IDs de requisição com chave idempotente e leitura de opções nativas (`#41304`):**
   - Introduz `worker-start --request-id <uuid>`, garantindo que retentativas com o mesmo UUID consultem o ledger existente em vez
     de criar workers redundantes;
   - Adiciona inspeção detalhada de opções do worker através do observador estruturado de sessão, diferenciando opções aceitas,
     padrões, confirmadas e relatadas pelo provedor.
3. **Identidade persistente para agentes de terminal via `Copy Agent ID` (`#41286`):**
   - Adiciona a ação "Copy Agent ID" no menu de contexto do painel de terminal, copiando `orca_session_id:<agent>_<uuid>`;
   - Persiste os mapeamentos no banco `agent-identities.db`, sobrevive a ciclos de sleep/wake, reinicializações e retomadas em
     novos splits, e expõe `orcaSessionId` em `orca worktree ps --json`.
4. **Ações de cópia escopadas por comando com limites OSC 133 (`#41301`):**
   - Insere "Copy Command", "Copy Output" e "Copy Command and Output" no menu de clique direito do terminal, utilizando
     marcadores xterm OSC 133 para extração exata e sem quebras artificiais de linha.

## O que fazer

- Adotar a configuração e comandos de aprovação de permissões de workers pelo coordenador (`orchestration approve/deny`) com
  salvaguarda `personOnly` (`#41306`).
- Incorporar `worker-start --request-id <uuid>` e o leitor estruturado de opções de execução (`#41304`).
- Adotar o identificador durável de agentes de terminal `orca_session_id` e o banco `agent-identities.db` (`#41286`).
- Incorporar as ações de cópia de comando/saída escopadas por limites OSC 133 no menu de contexto do terminal (`#41301`).
