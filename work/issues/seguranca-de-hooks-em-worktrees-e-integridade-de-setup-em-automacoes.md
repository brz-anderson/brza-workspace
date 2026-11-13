---
status: open
description: Os PRs #41823, #40978, #40976, #39229 trazem aprovação de setup a partir do branch base de criação, revisão de hooks e integridade criptográfica.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-04
tags:
  - tooling
  - infra
---

# Segurança de hooks em worktrees e integridade de setup em automações

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#41823`](https://github.com/stablyai/orca/pull/41823),
[`stablyai/orca#40978`](https://github.com/stablyai/orca/pull/40978) (resolve Issue [`#40974`](https://github.com/stablyai/orca/issues/40974)),
[`stablyai/orca#40976`](https://github.com/stablyai/orca/pull/40976),
[`stablyai/orca#39229`](https://github.com/stablyai/orca/pull/39229) (resolve Issue [`#39617`](https://github.com/stablyai/orca/issues/39617)),
[`stablyai/orca#38558`](https://github.com/stablyai/orca/pull/38558),
[`stablyai/orca#38648`](https://github.com/stablyai/orca/pull/38648),
[`stablyai/orca#38585`](https://github.com/stablyai/orca/pull/38585),
[`stablyai/orca#38128`](https://github.com/stablyai/orca/pull/38128) (Issue [`#37902`](https://github.com/stablyai/orca/issues/37902)),
[`stablyai/orca#37848`](https://github.com/stablyai/orca/pull/37848) (resolve Issue [`#37799`](https://github.com/stablyai/orca/issues/37799)),
[`stablyai/orca#37977`](https://github.com/stablyai/orca/pull/37977),
[`stablyai/orca#37978`](https://github.com/stablyai/orca/pull/37978),
[`stablyai/orca#37979`](https://github.com/stablyai/orca/pull/37979),
[`stablyai/orca#38019`](https://github.com/stablyai/orca/pull/38019),
[`stablyai/orca#38029`](https://github.com/stablyai/orca/pull/38029),
[`stablyai/orca#33492`](https://github.com/stablyai/orca/pull/33492),
[`stablyai/orca#37941`](https://github.com/stablyai/orca/pull/37941) e
[`stablyai/orca#37931`](https://github.com/stablyai/orca/pull/37931), além das issues
[`stablyai/orca#39771`](https://github.com/stablyai/orca/issues/39771),
[`stablyai/orca#39736`](https://github.com/stablyai/orca/issues/39736),
[`stablyai/orca#39714`](https://github.com/stablyai/orca/issues/39714),
[`stablyai/orca#39609`](https://github.com/stablyai/orca/issues/39609) e
[`stablyai/orca#38566`](https://github.com/stablyai/orca/issues/38566).

## O problema

1. **Ausência de hooks de sleep e wake para serviços em worktrees locais (`#38566`):**
   Ao colocar um workspace em modo sleep, o app finaliza os terminais e chats de agentes, mas processos e serviços iniciados
   no worktree (ex.: containers rodando via `docker compose up`) continuam consumindo CPU, memória RAM e portas de rede.
   O arquivo de configuração só oferecia ganchos `scripts.setup` e `scripts.archive`, não havendo evento para suspender e
   reativar containers e daemons locais.
2. **Espera de permissão travada quando o Claude encerra a solicitação internamente (`#38648`):**
   Uma aba de terminal do Claude continuava exibindo status "needs permission" indefinidamente até o fim do turno quando
   o próprio Claude cancelava uma solicitação de permissão (por timeout interno, recusa de segurança de `rm -rf` embutida
   ou decisão autônoma). Como o Claude não enviava evento `PostToolUse` nesses casos, o app não recebia evidência direta
   para liberar o estado de espera.
3. **Falta de visibilidade do código de saída de setup ao abortar agente (`#38585`):**
   Quando um script de setup falhava e o app pulava a inicialização do agente, o código exato de saída e log de erro não
   eram propagados adequadamente para o painel de status.
4. **Geração automática de texto em background com permissões amplas de escrita (`#38558`):**
   Ao abrir um chat, o app disparava agentes secundários em segundo plano para gerar títulos automáticos, mensagens de
   commit, nomes de branches e sumários de issues. Esses agentes compartilhavam a rota padrão de geração com permissões de
   build/edição/execução no worktree, com até 3 tentativas concorrentes sob timeout, criando riscos de modificações espúrias
   não solicitadas em arquivos do projeto.
5. **Falha espúria na remoção de worktrees externos por negação de acesso no watcher (`#38128`, `#37902`):** ao remover
   worktrees situados fora da pasta principal do workspace, o `git worktree remove` concluía com sucesso, mas o encerramento
   do observador de arquivos (`closeFileExplorerWatchersForPath`) tentava re-autorizar o caminho já desregistrado pelo Git.
   Isso disparava `PATH_ACCESS_DENIED_MESSAGE` e abortava com erro a rotina de exclusão, deixando o usuário em estado inconsistente.
6. **Execução cega de scripts de setup em branches untrusted (`#37977`, `#37978`):** ao alternar branches ou criar
   worktrees vinculados a PRs externos, comandos definidos em `orca.yaml` (ou ganchos equivalentes de inicialização de
   worktree) eram disparados automaticamente. Isso abria vetor de execução arbitrária de código (RCE) caso uma branch
   ou fork malicioso alterasse o script de setup.
7. **Automações e runners executando hooks alterados sem validação (`#37979`):** o runner de automações não persistia o
   hash do script de setup previamente aprovado pelo usuário. Se uma automação baixasse ou fizesse checkout de uma branch
   com hook adulterado, o hook rodava com as permissões do app.
8. **Bloqueio espúrio em disparos manuais de automações (`#38029`):** ao clicar em "Run Now" no painel de Automações,
   o disparo falhava se a verificação da ferramenta de fonte do GitHub estivesse indisponível ou desconectada.
9. **Vazamento e retenção de agentes completados em automações (`#33492`):** agentes de automações anteriores mantidos
   abertos apenas para monitoramento de término não eram reutilizados eficientemente, gerando processos órfãos.
10. **Conflito entre hooks gerenciados do Orca e recusas internas do Claude Code 2.1.319+ (`#39229`, `#39617`):**
    No Claude Code 2.1.319+, a checagem interna para pular recusas/checagens de segurança embutidas (ex.: `rm`) exige que nenhum hook
    `PermissionRequest` esteja configurado no ambiente. Como o Orca instalava incondicionalmente um hook `PermissionRequest` gerenciado
    (com matcher `*`), a flag de ignorar recusas era ineficaz mesmo em modo Full access.
11. **Relaunch de `claude --resume` no worktree errado por colisão de IDs e herança em tmux (`#37848`, resolve `#37799`, `#39609`):**
    Após atualizações do app ou quando um servidor tmux iniciado em uma aba preserva variáveis de ambiente herdadas (`ORCA_AGENT_PANE`),
    hooks de sessões em outros worktrees podiam postar com a chave de pane da aba original. No reinício, o comando `cd <outro> && claude --resume`
    era injetado na aba errada;
    - O PR `#37848` implementa a proteção `cwdInsideOtherTabbedWorktree` no host de execução: se a pasta reportada pelo hook pertencer
      a outro worktree que já possui suas próprias abas na janela, o registro de resume é rejeitado, impedindo que a sessão estranha sobrescreva
      ou capture a aba.
12. **Perda de status do agente quando `claude` no PATH é um symlink para wrapper launcher (`#39771`):**
    Quando o executável `claude` no PATH do host aponta para um script wrapper customizado via symlink, a inspeção de processos
    do gancho gerenciado não consegue casar a linha de comando com binários conhecidos, marcando o remetente como `unknown`
    e deixando a interface sem atualização de estado (thinking/tool/idle).
13. **Falha no SessionStart hook do Claude Code com `printf: write error: Permission denied` (`#39714`):**
    O hook de início de sessão falha acusando que o output não é um JSON válido após um erro de permissão de escrita no `printf`,
    interrompendo a inicialização do agente sob certos ambientes com pipes de automação ou descritores fechados.
14. **Exceção `FileNotFoundError` no hook do Hermes após limpeza de tarefas de Kanban (`#39736`):**
    Quando automações de Kanban removem o diretório de trabalho de um lote concluído, o gancho de status do Hermes falha
    no ciclo `pre_tool_call` ao tentar acessar o `cwd` inexistente, travando todas as invocações de ferramentas subsequentes.
15. **Inexistência de revisão e aprovação de hooks de repositório no Native Chat do Codex (`#40978`, resolve `#40974`):**
    No chat nativo com o Codex, não havia mecanismo para inspecionar e aprovar comandos de hooks declarados no repositório.
    O usuário precisava sair do chat para a linha de comando ou configurações para autorizá-los manualmente.
16. **Fragmentação de cartões de hooks de worktree nas configurações (`#40976`):**
    Cada hook de worktree consumia um cartão isolado na interface de configurações, gerando rolagem excessiva e desorganização visual.
17. **Alerta falso de divergência de setup ao criar workspaces a partir de branches atualizados (`#41823`):**
    A checagem de aprovação pré-criação lia o `orca.yaml` do checkout principal (geralmente desatualizado em relação a `origin/main`),
    enquanto a pós-criação lia o `orca.yaml` da branch alvo. Isso gerava o modal "This workspace's branch has different setup commands"
    em praticamente toda criação de workspace, bloqueando a execução automática do setup até um clique manual de autorização.

## O que o upstream propõe e implementa

- **Hooks `scripts.sleep` e `scripts.wake` no manifesto do worktree (`#38566`):**
  - Propõe suporte declarativo a comandos de suspensão (ex.: `docker compose stop`) e restauração (`docker compose start`)
    no manifesto `orca.yaml`, liberando recursos de máquina quando worktrees locais entram em repouso.
- **Limpeza proativa de estados de permissão no Claude (`#38648`):**
  - Utiliza o evento `PostToolBatch` enviado pelo Claude (versão 2.1.118+) para desarmar a retenção de espera de permissão
    quando o lote de ferramentas do turno for concluído, prevenindo abas presas em falsos bloqueios.
- **Propagação de status de saída de setup (`#38585`):**
  - Registra e exibe o código exato de saída quando scripts de setup de worktree falham antes da submissão do agente.
- **Isolamento estrito de tarefas de texto em background como read-only (`#38558`):**
  - Impõe sandbox estritamente somente leitura para geração de títulos de chat, nomes de branches, mensagens de commit e
    sumários de issues/PRs;
  - Restringe tarefas automáticas a uma única tentativa, nega ferramentas de escrita/execução de comandos e faz cleanup
    delimitado da sessão sem deixar processos zumbis;
  - Preserva comandos manuais do usuário com seus fluxos originais.
- **Teardown limpo de observadores sem re-autorização pós-exclusão (`#38128`, resolve `#37902`):**
  - Trata `PATH_ACCESS_DENIED_MESSAGE` no teardown de watchers como indicativo de caminho já removido, ignorando a falha
    e permitindo que `worktree.remove` conclua sem erros espúrios em layouts de worktrees irmãos.
- **Validação criptográfica de integridade de hooks (`#37977`, `#37978`, `#37979`):**
  - Calcula o hash SHA-256 normalizado do script/comando de setup configurado;
  - Bloqueia a execução automática quando o conteúdo da branch diferir do script aprovado;
  - Adiciona o fluxo `worktrees:runApprovedSetup` para que o usuário aprove explicitamente a nova versão antes da execução;
  - Automações armazenam o hash aprovado do setup e ignoram silenciosamente ou abortam quando a branch trouxer alterações
    não homologadas.
- **Robustez e agilidade no runner de automações (`#38029`, `#33492`):**
  - Permite que o comando "Run Now" dispare imediatamente sem validação desnecessária da ferramenta de repositório remoto;
  - Reutiliza de forma limpa agentes completados que estavam retidos apenas para monitoramento de conclusão.
- **Seletor compartilhado de agentes no Source Control e Automações (`#37941`, `#38019`):**
  - Unifica a escolha de modelo, reasoning effort, permissões e argumentos em todas as superfícies operadas por IA.
- **Confirmação antes de rodar `.orca/issue-command` (`#37931`):** solicita aprovação interativa antes de executar
  qualquer script comitado na pasta `.orca/`.
- **Dispensa opt-in de recusas embutidas no Claude Code sob Full Access (`#39229`, resolve `#39617`):**
  - Adiciona o campo `agentPermissionGuardSkip` nas configurações por agente;
  - Quando ativado em modo Full access, remove o hook `PermissionRequest` gerenciado pelo Orca em `~/.claude/settings.json`,
    permitindo que as checagens e recusas embutidas do Claude Code sejam dispensadas sem emitir avisos bloqueantes.
- **Revisão e confiança de hooks do Codex no Native Chat (`#40978`, resolve `#40974`):**
  - Adiciona o comando de barra `/hooks` no chat nativo com o Codex para revisar comandos de hooks do repositório e salvar
    seus hashes aprovados sem sair da conversa;
  - Rejeita comandos modificados cujo hash não coincida e preserva hooks desabilitados.
- **Cartão unificado e achatado para hooks de worktree nas configurações (`#40976`):**
  - Condensa os hooks de worktree em linhas dentro de um único cartão nas configurações, eliminando dispersão visual.
- **Aprovação pré-criação de setup a partir da branch base de origem (`#41823`):**
  - Altera a validação de segurança pré-criação para inspecionar o arquivo `orca.yaml` da branch base a partir da qual o novo workspace será criado, em vez do checkout principal da máquina;
  - Garante que os comandos apresentados para aprovação sejam rigorosamente idênticos aos que serão executados na inicialização do novo worktree, eliminando popups bloqueantes desnecessários.

## O que fazer

- Adotar a leitura pré-criação do setup a partir da branch de origem do workspace (`#41823`), eliminando falsos alertas de divergência de comandos.
- Adotar o comando `/hooks` no Native Chat para revisão e autorização de hooks do Codex (`#40978`).
- Incorporar o cartão unificado de hooks de worktree nas configurações (`#40976`).
- Resolver symlinks de executáveis na inspeção de remetentes de hooks para preservar o status de agentes sob wrappers (`#39771`).
- Tratar descritores restritivos e falhas de escrita no `printf` do SessionStart hook do Claude (`#39714`).
- Adicionar verificação defensiva de existência do `cwd` no hook do Hermes para evitar quebras em limpezas de Kanban (`#39736`).
- Adotar a opção de dispensa de recusas do Claude Code (`agentPermissionGuardSkip`, `#39229`) para agentes sob Full access.
- Validar se o diretório de execução (`cwd`) pertence estritamente ao worktree da aba ao relançar `claude --resume` via `cwdInsideOtherTabbedWorktree` (`#37848`, resolve `#37799`, `#39609`).
- Implementar ganchos de suspensão e restauração (`scripts.sleep` / `scripts.wake`, `#38566`) no orquestrador de worktrees do `brza-studio`.
- Incorporar o fix de descarte de espera de permissões do Claude (`#38648`).
- Aplicar a restrição read-only para geradores de texto em background (`#38558`) no `brza-studio` e `brza-workflow`.
- Portar as proteções de integridade de hooks (`#37977`, `#37978`, `#37979`) e o conserto de remoção de worktrees (`#38128`).
