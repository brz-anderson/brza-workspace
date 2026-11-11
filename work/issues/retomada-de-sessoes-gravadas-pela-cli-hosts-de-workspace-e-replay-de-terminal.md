---
status: open
description: Os PRs #41206, #41183, #41248, #41247 e a issue #41184 trazem retomada de sessões pela CLI, escolha de host de workspace e replay de terminal.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-11
tags:
  - tooling
  - infra
---

# Retomada de sessões gravadas pela CLI, hosts de workspace e replay de terminal

Rastreado dos PRs abertos no upstream [`stablyai/orca#41206`](https://github.com/stablyai/orca/pull/41206) (resolve Issue [`#41204`](https://github.com/stablyai/orca/issues/41204)),
[`stablyai/orca#41183`](https://github.com/stablyai/orca/pull/41183),
[`stablyai/orca#41248`](https://github.com/stablyai/orca/pull/41248),
[`stablyai/orca#41247`](https://github.com/stablyai/orca/pull/41247) e da issue
[`stablyai/orca#41184`](https://github.com/stablyai/orca/issues/41184).

## O problema

1. **Acúmulo de abas de agentes ao tentar reutilizar sessões hibernadas via CLI (`#41206`, `#41204`):**
   - O seletor de reaproveitamento de sessões exigia um processo PTY ativo e ocioso no host. Quando um agente entrava em
     hibernação para poupar recursos, o processo era deliberadamente encerrado enquanto a aba e o histórico conversacional
     permaneciam gravados;
   - Ao disparar novas automações agendadas ou prompts via CLI (`orca agent launch --reuse`), o sistema considerava a sessão
     inexistente e criava uma nova aba com outro coordenador em vez de acordar a sessão hibernada em seu painel original,
     gerando proliferação excessiva de abas e perda de continuidade de contexto.
2. **Seleção arbitrária do host padrão em workspaces com múltiplos servidores pareados (`#41183`):**
   - Na presença de múltiplos hosts pareados capazes de executar comandos de um workspace, o seletor `Run on` escolhia o
     primeiro host pela ordem bruta do array retornado pela descoberta, ignorando a preferência do usuário ou a proximidade de rede;
   - Isso provocava despachos acidentais para hosts lentos ou de testes em vez do host primário configurado.
3. **Lentidão O(N log N) ao resolver host de workspace por ordenação global de pastas (`#41248`):**
   - Durante a resolução do host responsável por um único workspace, a rotina ordenava recursivamente todas as pastas de
     projetos registradas no aplicativo, degradando a latência de troca de abas e o arranque inicial da janela.
4. **Captura inconsistente de snapshots de replay do terminal (`#41247`):**
   - O mecanismo de gravação e replay de terminal capturava snapshots de tela em posições de cursor e buffers divergentes
     durante transmissões ativas de saída, causando artefatos visuais e corrupção parcial ao restaurar sessões de agentes TUI.
5. **Invisibilidade do workspace ativo no Studio a partir da CLI (`#41184`):**
   - Scripts de workflow e integrações externas via CLI não possuíam forma de consultar qual workspace está visível no monitor
     ou qual janela de host remoto está em foco pelo operador, dificultando orquestrações conscientes de contexto.

## O que o upstream propõe e implementa

1. **Descoberta e restauração in-place de sessões gravadas via CLI (`#41206`):**
   - Adiciona `orca agent sessions --worktree <selector> --json` para listar todas as conversas gravadas em painéis de terminal,
     incluindo sessões hibernadas (`sleeping panes`);
   - Introduz `orca agent resume --pane <paneKey>` e `--agent <id> --session <providerSessionId>`, restaurando o processo no painel
     original com os mesmos argumentos de inicialização salvos sem criar abas secundárias nem roubar foco do desktop;
   - Ajusta automações de reutilização para visarem a última execução registrada, acordando a sessão gravada antes da entrega
     do prompt e preservando evidências de falha caso a restauração seja impedida.
2. **Seleção determinística de host por preferência configurada (`#41183`):**
   - Ordena os hosts elegíveis com base nas preferências explícitas do workspace em vez da ordem aleatória do array de sockets.
3. **Resolução direta de host sem varredura completa do disco (`#41248`):**
   - Substitui a ordenação custosa de todas as pastas registradas pela verificação direta do caminho do workspace alvo.
4. **Ponto único de sincronização para snapshots de replay (`#41247`):**
   - Bloqueia a captura de snapshots em posições intermediárias, registrando apenas em pontos de repouso de saída do terminal.
5. **Relatório de workspace focado na janela via CLI (`#41184`):**
   - Exposição via RPC e CLI do estado de visualização ativa entre múltiplos hosts pareados.

## O que fazer

- Incorporar a descoberta e reativação in-place de sessões gravadas de agentes (`orca agent sessions` e `orca agent resume`)
  para eliminar a proliferação de abas em automações contínuas (`#41206`).
- Adotar a seleção de host por preferências configuradas no `Run on` (`#41183`).
- Aplicar a otimização de resolução de host de workspace sem ordenação global de pastas (`#41248`).
- Adotar a sincronização consistente de snapshots de replay no terminal (`#41247`).
- Disponibilizar consulta CLI do workspace atualmente ativo no aplicativo (`#41184`).
