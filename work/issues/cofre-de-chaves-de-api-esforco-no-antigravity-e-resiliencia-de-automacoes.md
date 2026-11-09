---
status: open
description: Os PRs #40303, #40308, #40311, #40331 trazem cofre de API keys seladas, esforço no Antigravity CLI e skip estrito em automações.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-09
tags:
  - auth
  - tooling
  - infra
---

# Cofre de chaves de API, esforço no Antigravity e resiliência de automações

Rastreado dos PRs abertos no upstream [`stablyai/orca#40303`](https://github.com/stablyai/orca/pull/40303),
[`stablyai/orca#40308`](https://github.com/stablyai/orca/pull/40308) (resolve Issue [`#39556`](https://github.com/stablyai/orca/issues/39556)),
[`stablyai/orca#40311`](https://github.com/stablyai/orca/pull/40311) (resolve Issue [`#39905`](https://github.com/stablyai/orca/issues/39905)),
[`stablyai/orca#40331`](https://github.com/stablyai/orca/pull/40331),
[`stablyai/orca#40298`](https://github.com/stablyai/orca/pull/40298) (resolve Issue [`#40165`](https://github.com/stablyai/orca/issues/40165)) e
[`stablyai/orca#40295`](https://github.com/stablyai/orca/pull/40295) (resolve Issue [`#40204`](https://github.com/stablyai/orca/issues/40204)).

## O problema

1. **Exposição de chaves de API em perfis de shell em máquinas remotas (`#40303`):**
   Usuários de Claude, Codex, Gemini ou Cursor com chaves de API (Anthropic, OpenAI, Bedrock, Google AI Studio, Cursor)
   eram forçados a exportar variáveis de ambiente nos arquivos de profile (`.bashrc`, `.zshrc`) de cada máquina remota ou host SSH.
   Isso deixava segredos de longa duração em texto puro no disco de servidores remotos e em todos os shells abertos, sem controle de escopo.
2. **Conflito de parâmetro `--effort` e fallback silencioso no Antigravity CLI (`#40308`, resolve `#39556`):**
   Ao iniciar o Antigravity via terminal ou automação com `--model` e `--effort`, o seletor enviava um par conflitante que o binário
   `agy` não conseguia resolver (ex.: `--model gemini-3.8-flash-high --effort low`). Em modo interativo, o Antigravity caía silenciosamente
   para o modelo padrão (Gemini 4 Argon) sem emitir erro, surpreendendo o desenvolvedor com um modelo diferente do solicitado.
3. **Acúmulo descontrolado de sessões duplicadas em automações com `--reuse-session` (`#40311`, resolve `#39905`):**
   Automações periódicas (ex.: executadas a cada 5 minutos) configuradas para reutilizar sessões criavam uma nova sessão concorrente
   sempre que a sessão anterior ainda estava ocupada ou travada no estado `dispatched`. Com o tempo, dezenas de sessões acumulavam-se
   no mesmo workspace, consumindo recursos e gerando concorrência indevida sobre o mesmo repositório.
4. **Perda de eventos de título e sino em splits secundários em background (`#40331`):**
   Quando um terminal em segundo plano recebia um segundo painel (split), o sistema não registrava um observador de saída
   (*output watcher*) para ele. Atualizações de título de processo e alertas de campainha (`bell`) deixavam de ser propagados para a interface.
   Além disso, o ciclo global de parking recalculava indiscriminadamente todos os workspaces da aplicação após alterações locais.
5. **Incapacidade de renomear servidores Orca remotos na interface (`#40298`, resolve `#40165`):**
   Servidores remotos pareados ficavam restritos ao nome de host inicial ou endereço IP, sem opção de atribuir apelidos amigáveis em `Settings`.
6. **Bloqueio de instalação do Docker e instaladores externos por handles abertos em `.asar` (`#40295`, resolve `#40204`):**
   O observador de arquivos do aplicativo monitorava pastas de staging, `AppData` e arquivos compactados `.asar`, mantendo handles
   abertos que impediam a atualização de ferramentas externas no sistema operacional (como Docker Desktop no Windows).

## O que o upstream implementa e corrige

- **Cofre local de chaves de API seladas com injeção segura por processo (`#40303`):**
  - Cria o repositório `agent-api-key-store.ts` no `userData` do desktop, onde cada chave é selada pelo chaveiro do SO via `SecretStore`/`safeStorage` e gravada com permissões restritas (modo `0600`);
  - Recusa armazenamento inseguro caso o chaveiro do SO apenas ofusque sem criptografia real;
  - Bloqueia tokens de assinatura (`CLAUDE_CODE_OAUTH_TOKEN`, `sk-ant-oat...`) e variáveis que possam alterar a rota de execução (`PATH`, `DYLD_*`, `NODE_OPTIONS`, `GIT_*`);
  - Injeta chaves exclusivamente no processo do agente lançado:
    - Na máquina local e em hosts SSH: via variáveis de spawn do PTY (`assemblePtySpawnLaunchOptions`);
    - Em máquinas pareadas: via capability negociada `agent-session.key-env.v1` (`keyEnv`), onde o daemon remoto valida o formato e aplica no processo sem gravar credenciais no disco remoto;
  - Registra redatores de logs para ofuscar chaves em traces diagnósticos e adiciona a seção de gerenciamento em `Settings → Agent API Keys`.
- **Seleção de esforço no Antigravity CLI exclusivamente pelo ID do modelo (`#40308`):**
  - Como os IDs nativos do Antigravity já codificam o nível de esforço (`gemini-3.8-flash-high`, `gemini-3.8-flash-medium`), remove o seletor redundante de Effort para terminais em `Settings`, nos menus de lançamento e nas ações do Source Control;
  - Recusa a flag `--effort` no comando `orca agent launch` e em workers para Antigravity, orientando a escolha direta pelo ID do modelo (em conformidade com o catálogo do PR `#40175`).
- **Pulo estrito com registro de causa em automações (`#40311`, resolve `#39905`):**
  - Adiciona o argumento `--on-no-reusable-session skip` (campo `onNoReusableSession: 'skip'`) em automações com `--reuse-session`;
  - Quando a sessão anterior ainda está ativa ou bloqueada, registra o disparo como pulado com status `skipped_unavailable` e código explicativo (`sessionBusy` / `sessionNotReusable`), agregando ocorrências repetidas via `occurrenceCount` em vez de criar sessões duplicadas.
- **Escopamento de parking de terminais e cobertura de saída por workspace (`#40331`):**
  - Vincula o estado de parking e os observadores de saída individualmente a cada workspace, garantindo que novos splits secundários ativem seus próprios watchers e entreguem títulos e notificações corretamente;
  - Elimina varreduras globais redundantes de workspaces inalterados.
- **Renomeação de servidores remotos salvos (`#40298`):**
  - Permite alterar o nome de exibição de servidores remotos cadastrados diretamente na seção de configurações.
- **Filtragem de diretórios de sistema nos observadores de arquivos (`#40295`):**
  - Ignora pastas de instalação, `AppData` e arquivos `.asar` nos watchers de filesystem, liberando travas de processo desnecessárias.

## O que fazer no BrzA Studio

1. Adotar o cofre de chaves de API (`#40303`) no desktop, permitindo aos desenvolvedores injetar chaves seguras em agentes locais, SSH e servidores remotos pareados sem persistir segredos em texto puro.
2. Ajustar os seletores do Antigravity CLI para enviar o nível de esforço encapsulado no próprio ID do modelo (`#40308`), evitando regressões para o modelo default.
3. Incorporar o parâmetro `--on-no-reusable-session skip` em automações (`#40311`) para proteger rotinas periódicas de acumular processos em segundo plano.
4. Aplicar o isolamento de parking e watchers de terminal por workspace (`#40331`), garantindo integridade de títulos e alertas em splits.
5. Permitir renomear servidores remotos salvos em Settings (`#40298`).
