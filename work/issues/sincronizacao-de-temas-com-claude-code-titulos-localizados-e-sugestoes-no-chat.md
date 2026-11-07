---
status: open
description: Os PRs #39447, #37107, #39437 e #37190 trazem sincronização dinâmica de temas do terminal com Claude Code, sugestões no chat, títulos localizados e reabertura de chats órfãos.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-07
tags:
  - tooling
  - design
  - chat
---

# Sincronização de temas com Claude Code, títulos localizados e sugestões no chat

Rastreado dos PRs abertos no upstream [`stablyai/orca#39447`](https://github.com/stablyai/orca/pull/39447),
[`stablyai/orca#37107`](https://github.com/stablyai/orca/pull/37107) (Issue [`#22316`](https://github.com/stablyai/orca/issues/22316)),
[`stablyai/orca#39437`](https://github.com/stablyai/orca/pull/39437) (Issue [`#39281`](https://github.com/stablyai/orca/issues/39281)) e
[`stablyai/orca#37190`](https://github.com/stablyai/orca/pull/37190) (Issue [`#36722`](https://github.com/stablyai/orca/issues/36722)).

## O problema

1. **Descompasso visual entre o tema do terminal e o tema do Claude Code (`#39447`):**
   Ao utilizar o Claude Code dentro do terminal do aplicativo, o tema de cores interno do Claude Code não acompanhava
   automaticamente o tema ativo do terminal (ex.: paletas Tokyo Night, Gruvbox ou modos claro/escuro). O Claude permanecia
   com suas cores padrão ou contrastes inadequados em relação ao fundo do terminal, e a troca de tema no app não propagava
   para as sessões ativas do Claude.
2. **Perda das conveniências de sugestões de prompt (*prompt suggestions*) no Native Chat (`#37107`, `#22316`):**
   No terminal tradicional, o Claude Code gera sugestões de comandos e próximas ações com base no cache de prompts. Ao utilizar
   o Chat UI nativo, essas sugestões eram completamente suprimidas, obrigando o operador a digitar manualmente perguntas
   de continuidade ou comandos de follow-up que já haviam sido inferidos pelo modelo.
3. **Impossibilidade de exibir títulos legíveis em idiomas naturais sem quebrar nomes de branch Git (`#39437`, `#39281`):**
   A funcionalidade de nomeação automática de workspaces e branches gerava um único valor sanitizado para slugs ASCII do Git
   (ex.: `fix-korean-time-input`). Desenvolvedores em idiomas não-latinos ou que desejam títulos descritivos em português na
   barra lateral (ex.: `Correção de entrada de data`) tinham o texto descaracterizado ou eram forçados a criar branches com
   nomes incompatíveis com as convenções da equipe.
4. **Perda de navegação e atalhos em chats após readicionar pastas de projetos (`#37190`, `#36722`):**
   Quando uma pasta de projeto era removida e posteriormente readicionada ao aplicativo, as conversas nativas salvas do
   Claude e Codex continuavam visíveis no Session History com suas transcrições intactas, mas o botão "Jump to Original Pane"
   não funcionava, pois o registro da conversa permanecia vinculado ao ID de registro anterior do projeto.

## O que o upstream implementa

- **Sincronização dinâmica de tema com o Claude Code (`#39447`):**
  - Monitora o tema ativo do terminal e gera dinamicamente uma definição de tema customizada injetada no `settings.json`
    do Claude Code com trava atômica de escrita e criação de backup `.bak`;
  - Suporta troca a quente (*live switch*) refletindo alterações de paleta instantaneamente em sessões abertas do Claude Code;
  - Adiciona toggle dedicado em Configurações para ligar/desligar a sincronização, restaurando fielmente o tema original
    caso o usuário desative a opção ou utilize o comando `/theme` interativo no Claude.
- **Sugestões de prompt nativas do Claude no composer de chat (`#37107`):**
  - Captura as mensagens de `prompt_suggestion` do Claude Code e as expõe como um campo transitório `promptSuggestion`
    na timeline de sessão sem gravar entradas no diário (journal) ou sujar o histórico;
  - Renderiza o texto sugerido em tom esmaecido no composer de mensagem quando este estiver vazio e ocioso;
  - Permite aceitar a sugestão teclando <kbd>Tab</kbd> ou <kbd>Seta para a Direita</kbd>, preenchendo o rascunho sem envio
    automático para revisão antes da confirmação;
  - Limpa automaticamente a sugestão no início do próximo turno do agente.
- **Títulos de workspaces localizados independentes do branch Git (`#39437`):**
  - Introduz a configuração "Workspace title language" com opções para seguir o idioma da interface ou selecionar idioma fixo;
  - Separa a geração em dois campos (`branch` slug ASCII e `title` Unicode amigável), permitindo exibir nomes claros na barra
    lateral enquanto o Git branch mantém a padronização técnica da equipe.
- **Recuperação de associação de chats após recadastro de pastas (`#37190`):**
  - Associa automaticamente conversas órfãs ao novo registro da pasta no mesmo host ao abrir a sessão pelo histórico;
  - Preserva IDs de conversa, transcripts, rascunhos não enviados e links de retorno sem requerer migração de banco de dados.

## O que fazer

- Adotar a sincronização de temas com o Claude Code (`#39447`) no `brza-studio`.
- Incorporar as sugestões de prompt transitórias no composer do Native Chat com acionamento por <kbd>Tab</kbd> (`#37107`).
- Adotar títulos de workspaces localizados desacoplados dos branches Git (`#39437`).
- Incorporar a restauração de associação de chats nativos ao readicionar pastas no `brza-studio` (`#37190`).
