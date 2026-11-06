---
status: open
description: Os PRs #38995, #38963, #38945, #39013, #38632 e #38633 trazem agrupamento de subagentes na sidebar, ação Background para ferramentas Claude e SQLite de busca desacoplado.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-05
tags:
  - chat
  - tooling
---

# Painel de atividades de subagentes e anotações visuais no Native Chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#38995`](https://github.com/stablyai/orca/pull/38995) (Issue [`#38994`](https://github.com/stablyai/orca/issues/38994)),
[`stablyai/orca#38963`](https://github.com/stablyai/orca/pull/38963),
[`stablyai/orca#38945`](https://github.com/stablyai/orca/pull/38945),
[`stablyai/orca#39013`](https://github.com/stablyai/orca/pull/39013) (Issue [`#39010`](https://github.com/stablyai/orca/issues/39010)),
[`stablyai/orca#38632`](https://github.com/stablyai/orca/pull/38632),
[`stablyai/orca#38633`](https://github.com/stablyai/orca/pull/38633),
[`stablyai/orca#38640`](https://github.com/stablyai/orca/pull/38640),
[`stablyai/orca#38470`](https://github.com/stablyai/orca/pull/38470),
[`stablyai/orca#38452`](https://github.com/stablyai/orca/pull/38452),
[`stablyai/orca#38594`](https://github.com/stablyai/orca/pull/38594) (Issue [`#38592`](https://github.com/stablyai/orca/issues/38592)),
[`stablyai/orca#38627`](https://github.com/stablyai/orca/pull/38627),
[`stablyai/orca#38649`](https://github.com/stablyai/orca/pull/38649) e
[`stablyai/orca#38625`](https://github.com/stablyai/orca/pull/38625) (Issue [`#38624`](https://github.com/stablyai/orca/issues/38624)).

## O problema

1. **Sessões flutuantes e de subagentes dispersas na barra lateral (`#38995`, `#38994`):**
   Subagentes e sessões ad-hoc abertas fora da hierarquia primária de worktrees misturavam-se de forma plana na lista de
   workspaces da barra lateral, sem indicação visual compacta do número de subagentes trabalhando em tempo real.
2. **Travamento do chat aguardando ferramentas ou comandos Bash longos do Claude (`#38963`):**
   Comandos demorados ou subagentes executados via Claude Bash bloqueavam a continuidade do chat até o término da invocação,
   sem opção para despachar o comando em segundo plano e permitir que o operador ou o agente seguissem a conversa.
3. **Travamentos e congelamentos em históricos massivos de sessões (`#38945`):**
   O indexador e motor de busca do Agent Session History executava transações SQLite síncronas pesadas (vacuum, commits,
   queries FTS de múltiplos gigabytes) na mesma thread do Node/servidor que atende a varredura de sessões, travando a UI
   por minutos em históricos com mais de 20.000 transcrições.
4. **Processos órfãos fora de terminais invisíveis no monitor de recursos (`#39013`, `#39010`):**
   O popover Resource Usage monitorava apenas a árvore direta de processos de terminais ativos. Servidores de desenvolvimento,
   daemons ou processos desanexados iniciados pelo agente que continuavam consumindo memória e CPU após o fechamento do
   terminal não eram contabilizados em nenhum workspace.
5. **Invisibilidade e falta de inspeção de subagentes no Native Chat (`#38632`, `#38633`, `#38470`):**
   Embora o agente coordenador no Native Chat pudesse instanciar subagentes em segundo plano para delegar tarefas auxiliares,
   o chat desktop e mobile não exibia um elenco estruturado (*roster*) dos subagentes em execução.
6. **Falta de ferramentas de anotação posicional em imagens anexadas (`#38594`, `#38592`):**
   Ao debater interfaces ou capturas de tela com o agente, o usuário não tinha uma forma direta de apontar regiões específicas da imagem.
7. **Degradação de performance em conversas longas sob streaming (`#38627`):**
   Reavaliação contínua do status reescaneando dezenas de milhares de itens de diário em chats longos.

## O que o upstream implementa

- **Agrupamento de subagentes na sidebar e badges de atividade ao vivo (`#38995`):**
  - Categoriza sessões flutuantes e subagentes filhos em agrupamentos colapsáveis na barra lateral de workspaces;
  - Exibe badges compactos com contagem ao vivo e estado de atividade nos cartões de worktree e cabeçalhos de agentes.
- **Ação "Background" para ferramentas e subagentes Claude (`#38963`):**
  - Adiciona o botão "Background" ao lado da ferramenta em execução no chat e na barra expandida de tarefas;
  - Transfere o controle da invocação para segundo plano via SDK do Claude, liberando o agente e o chat para prosseguirem.
- **Worker threads dedicadas para o SQLite de Session History (`#38945`):**
  - Isola a gravação do banco em uma thread dedicada e leituras/buscas FTS em conexões WAL em threads de leitura separadas com timeout de 10s;
  - Impede que consultas lentas derrubem o processo de varredura ou travem a thread principal da interface.
- **Contabilização de processos fora de terminais no Resource Usage (`#39013`):**
  - Lê as tags de ambiente `ORCA_WORKTREE_ID` e `ORCA_PANE_KEY` para rastrear processos que desanexaram de terminais fechados,
    computando seu consumo de CPU e RAM como `outsideTerminals` no workspace que os originou.
- **Barra de atividade e visualizador de subagentes no Native Chat (`#38632`, `#38633`, `#38640`):**
  - Adiciona barra de atividade no desktop e folha expansível (*sheet*) no mobile listando todos os subagentes da conversa
    com estado vivo, pré-visualização e descarte em lote de filhos finalizados ou com erro.
- **Anotações e comentários posicionais numerados em imagens (`#38594`):**
  - Permite clicar com o botão direito em imagens de chat ou previews e selecionar "Comment on image".

## O que fazer

- Adotar o agrupamento visual de subagentes na sidebar (`#38995`) e a ação de backgrounding de ferramentas (`#38963`) no `brza-studio`.
- Portar o isolamento em threads de workers para o SQLite de histórico (`#38945`) e o rastreamento de processos órfãos (`#39013`).
- Incorporar a barra de atividade de subagentes (`#38632`) no Native Chat.
