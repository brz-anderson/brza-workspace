---
status: open
description: Os PRs #42709, #42689, #41492, #41649, #41590 e as issues #42684, #42681, #42718 trazem proteção de base branch em worktrees, notas sem título fora do checkout e CoW.
scope:
  - brza-studio
  - workspace
  - brza-workflow
priority: high
opened: 2026-11-12
tags:
  - tooling
  - infra
---

# Worktrees com clones Copy-on-Write, prompt inicial de workspace e ack seletivo de inbox

Rastreado dos PRs abertos no upstream [`stablyai/orca#42709`](https://github.com/stablyai/orca/pull/42709),
[`stablyai/orca#42689`](https://github.com/stablyai/orca/pull/42689) (resolve Issue [`#42684`](https://github.com/stablyai/orca/issues/42684)),
[`stablyai/orca#41492`](https://github.com/stablyai/orca/pull/41492),
[`stablyai/orca#41649`](https://github.com/stablyai/orca/pull/41649) (resolve Issue [`#19555`](https://github.com/stablyai/orca/issues/19555)),
[`stablyai/orca#41590`](https://github.com/stablyai/orca/pull/41590) (resolve Issue [`#41545`](https://github.com/stablyai/orca/issues/41545)) e
[`stablyai/orca#41651`](https://github.com/stablyai/orca/pull/41651),
além das issues [`stablyai/orca#42681`](https://github.com/stablyai/orca/issues/42681) e
[`stablyai/orca#42718`](https://github.com/stablyai/orca/issues/42718).

## O problema

1. **Consumo excessivo de armazenamento e lentidão no provisionamento de novos worktrees (`#41492`):**
   - Ao criar novos worktrees via `git worktree add`, o Git descompacta todos os arquivos da árvore de trabalho a partir dos blobs de objetos;
   - Em repositórios grandes (com dezenas ou centenas de milhares de arquivos), cada worktree consome múltiplos gigabytes adicionais de espaço em disco e impõe tempo considerável de descompactação e I/O, além de forçar varreduras lentas no primeiro `git status`.
2. **Ausência de direcionamento imediato para agentes na criação de workspaces (`#41649`, resolve `#19555`):**
   - No modal de criação de novo workspace, o operador seleciona o agente (Codex, Claude, etc.), mas não dispunha de um campo nativo para instrução inicial;
   - O workspace era aberto com um terminal ou chat vazio, exigindo que o usuário aguardasse o carregamento completo da interface para digitar manualmente o primeiro prompt de trabalho, atrasando despachos automatizados.
3. **Consumo indiscriminado de mensagens na caixa postal de orquestração (`#41590`, resolve `#41545`):**
   - O subsistema de mensageria interagentes permitia apenas a leitura em lote com reconhecimento (*ack*) global de toda a caixa postal;
   - Quando múltiplos processos ou agentes coordenadores compartilhavam a inspeção de mensagens, mensagens direcionadas a tarefas específicas eram desmarcadas involuntariamente da fila antes de seu efetivo processamento, gerando perda silenciosa de despachos e requisições.
4. **Dificuldade de relacionar agentes da barra lateral com suas abas ativas (`#41651`):**
   - Na lista de workspaces e agentes da barra lateral, linhas de agentes em execução não exibiam a identificação cromática da aba correspondente no painel principal, dificultando a navegação rápida em sessões multijanela.
5. **Merge acidental no branch base ao criar workspace quando o branch base já está em checkout ativo (`#42709`):**
   - Ao criar um novo workspace a partir de um branch base que já estava aberto e com checkout ativo em outro worktree da mesma máquina, o processo tentava aplicar um merge indevido, arriscando conflitos e corrupção de estado de trabalho.
6. **Impossibilidade de abrir arquivos de rascunho de texto sem título no escopo de projeto fora do checkout (`#42689`, resolve `#42684`):**
   - O editor não permitia manter notas de trabalho e rascunhos sem título associados ao projeto sem salvá-los imediatamente no disco dentro do checkout Git.
7. **Poluição visual da estrela de worktree primário e falta de indentação hierárquica profunda (`#42681`, `#42718`):**
   - Faltava opção para omitir o badge/estrela de repositório primário e aprofundar o recuo visual de worktrees secundários, além de falha de atribuição de escopo ao criar abas com `--worktree` explícito.

## O que o upstream propõe e implementa

1. **Criação de worktrees via clones Copy-on-Write / reflink (`#41492`):**
   - Implementa clonagem em nível de bloco do checkout principal para novos worktrees em sistemas de arquivos modernos com suporte a CoW (APFS no macOS; Btrfs, XFS e ZFS no Linux);
   - Transfere os metadados de `stat` do índice limpo para a nova cópia (`worktree-index-stat-transfer.ts`), acelerando drasticamente o primeiro `git status`;
   - Reduz em mais de 90% a ocupação física de disco adicional e conta com fallback automático e transparente para o `git worktree add` tradicional em sistemas sem suporte a reflink, configurável via `git config orca.copyOnWriteCheckout false`.
2. **Campo de prompt inicial opcional no diálogo de criação de workspace (`#41649`, resolve `#19555`):**
   - Adiciona um campo de texto multilinhas entre o seletor de agentes e as opções avançadas do modal de criação de workspace;
   - Entrega o prompt inicial ao agente escolhido através do mecanismo seguro de *readiness-aware delivery* com desduplicação de tokens de lançamento, sem interpolar comandos de texto cru no shell do terminal.
3. **Reconhecimento seletivo de mensagens de inbox por ID (`#41590`, resolve `#41545`):**
   - Adiciona o comando `orchestration inbox ack <id>` e o método RPC correspondente (`selective-message-ack.ts`), permitindo que agentes confirmem mensagens específicas de forma atômica;
   - Valida cada ID selecionado contra a propriedade do destinatário e rejeita referências externas ou legadas, preservando o estado pendente das demais mensagens não abordadas no lote.
4. **Ponto cromático de cor da aba nas linhas de agentes da barra lateral (`#41651`):**
   - Renderiza um indicador visual sutil com a cor da aba associada diretamente ao lado do nome do agente nas linhas da barra lateral, facilitando o mapeamento espacial imediato entre abas e processos.
5. **Prevenção de merge em branch base com checkout ativo (`#42709`):**
   - Valida antes da criação do worktree se o branch base já está em uso em outro checkout local, impedindo merges destrutivos e garantindo ramificação limpa.
6. **Arquivos sem título com escopo de projeto (*project-scoped untitled files*) (`#42689`, resolve `#42684`):**
   - Permite criar e manter rascunhos de notas textuais associadas ao projeto sem exigir salvamento prévio no sistema de arquivos do checkout.

## O que fazer

- Bloquear a criação de workspaces que tentem mesclar branches base já em checkout ativo (`#42709`).
- Suportar notas e rascunhos sem título com escopo de projeto fora do checkout Git (`#42689`, resolve `#42684`).
- Permitir ocultar o badge/estrela de worktree primário e aprofundar a indentação na sidebar (`#42681`).
- Adotar o provisionamento Copy-on-Write (CoW) para worktrees no macOS e Linux (`#41492`), aproveitando o APFS para economizar espaço em disco e acelerar a criação de checkouts no `brza-studio`.
- Incorporar o campo de prompt inicial opcional na criação de workspaces (`#41649`, resolve `#19555`), integrando o início automatizado de contexto para coordenadores e agentes.
- Implementar o reconhecimento seletivo de mensagens de inbox por ID na CLI de orquestração (`#41590`, resolve `#41545`).
- Adotar os indicadores cromáticos de abas nas linhas de agentes da barra lateral (`#41651`).
