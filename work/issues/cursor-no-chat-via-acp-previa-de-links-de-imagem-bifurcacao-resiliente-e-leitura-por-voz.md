---
status: open
description: Os PRs #46142 e #46284 trazem auto-review em terminais do Cursor e resolução de model IDs de CLI para o chat server, enquanto #42654 traz Cursor via ACP e leitura por voz.
scope:
  - brza-studio
  - brza-workflow
  - workspace
priority: high
opened: 2026-11-14
tags:
  - chat
  - tooling
---

# Cursor no Chat via ACP, prévia de links de imagem, bifurcação resiliente e leitura por voz

Rastreado dos PRs abertos no upstream [`stablyai/orca#46142`](https://github.com/stablyai/orca/pull/46142),
[`stablyai/orca#46284`](https://github.com/stablyai/orca/pull/46284) (resolve Issue [`#46163`](https://github.com/stablyai/orca/issues/46163)),
[`stablyai/orca#42654`](https://github.com/stablyai/orca/pull/42654) (resolve Issue [`#42653`](https://github.com/stablyai/orca/issues/42653)),
[`stablyai/orca#42646`](https://github.com/stablyai/orca/pull/42646) (resolve Issue [`#42645`](https://github.com/stablyai/orca/issues/42645)),
[`stablyai/orca#42639`](https://github.com/stablyai/orca/pull/42639) (resolve Issue [`#42631`](https://github.com/stablyai/orca/issues/42631)),
[`stablyai/orca#42590`](https://github.com/stablyai/orca/pull/42590),
[`stablyai/orca#42193`](https://github.com/stablyai/orca/pull/42193) (e [`#41494`](https://github.com/stablyai/orca/pull/41494)),
[`stablyai/orca#42227`](https://github.com/stablyai/orca/pull/42227),
[`stablyai/orca#42215`](https://github.com/stablyai/orca/pull/42215) (resolve Issue [`#41903`](https://github.com/stablyai/orca/issues/41903)),
[`stablyai/orca#42168`](https://github.com/stablyai/orca/pull/42168),
[`stablyai/orca#42211`](https://github.com/stablyai/orca/pull/42211),
além das issues [`stablyai/orca#42602`](https://github.com/stablyai/orca/issues/42602),
[`stablyai/orca#42214`](https://github.com/stablyai/orca/issues/42214) e
[`stablyai/orca#42187`](https://github.com/stablyai/orca/issues/42187).

## O problema

1. **Inexistência de suporte ao agente Cursor no Native Chat via ACP (`#42193`, `#41494`):**
   Usuários do agente Cursor estavam restritos a terminais PTY puros no Orca/Studio, sem poder utilizar a interface estruturada
   do Native Chat com seletor de modelos, ajuste de esforço de raciocínio, aprovação visual de planos/ferramentas e retomada de histórico.
2. **Imagens referenciadas como links em respostas Markdown não exibiam prévia inline (`#42227`):**
   Quando um agente gerava ou manipulava uma imagem e fornecia um link Markdown de download (ex.: `[Download](out/image.png)`),
   a imagem não era exibida na tela. O operador era forçado a clicar no link para abri-la fora do fluxo do chat.
3. **Bifurcação `/fork` solicitada durante a resposta do agente nunca era executada (`#42215`, resolve `#41903`):**
   Ao digitar `/fork` enquanto o agente ainda estava respondendo, o app exibia a mensagem "Wait for the response to finish, then fork".
   O operador aguardava o término da resposta assumindo que o comando havia sido enfileirado, mas a bifurcação era simplesmente descartada.
4. **Falta de acessibilidade e leitura por voz (*text-to-speech*) de respostas de agentes (`#42168` e `#42654`, resolve `#42653`):**
   Respostas extensas ou relatórios emitidos por agentes só podiam ser lidos visualmente na tela, sem opção de síntese de voz para
   ouvir o resultado de um turno no desktop ou no app mobile enquanto o desenvolvedor trabalha em outro editor ou tarefa.
5. **Listas extensas de configurações de agentes estourando a tela sem rolagem interna (`#42211`):**
   Painéis de configuração com muitos parâmetros de agentes e modelos transbordavam o modal, impedindo a visualização dos botões
   de salvamento em telas menores.
6. **Ausência de formatação rica com caminho e linha ao copiar trechos de código em Markdown (`#42214`):**
   Ao copiar trechos de código do chat ou editor, a área de transferência recebia apenas texto cru, sem o cabeçalho padronizado
   contendo o caminho do arquivo e o intervalo de linhas selecionado.
7. **Dificuldade de leitura de blocos de código extensos em dispositivos móveis (`#42646`, resolve `#42645`):**
   No cliente mobile, blocos de código com muitas linhas ficavam confinados em pequenas caixas com rolagem dupla truncada; cercas de código sem identificador de linguagem explícito não recebiam realce ou rótulo informativo.
8. **Seleção fragmentada de anexos de contexto e fotos no mobile (`#42639`, resolve `#42631`):**
   O cliente móvel exigia abrir diálogos separados para tirar fotos, selecionar imagens da galeria ou anexar arquivos do workspace, atrasando a composição de prompts multimodais.
9. **Desvio de diretório ao reabrir chats do OpenCode após movimentação de pastas (`#42590`):**
   Ao mover pastas ou reorganizar subdiretórios de trabalho, conversas do OpenCode tentavam reiniciar no caminho antigo, falhando ou criando sessões vazias.
10. **Seletor TUI indevido em `/models` do OpenCode no mobile (`#42602`):**
    No cliente mobile, o comando `/models` tentava renderizar menus TUI não adaptados ao toque, travando a navegação.
11. **Falta de suporte ao modo auto-review do Cursor em terminais PTY (`#46142`):**
    O modo de auto-revisão e aprovação automática de ações (`--auto-review` / "Approve for me") não podia ser selecionado em terminais do Cursor, forçando intervenção manual em cada etapa de tool call ou conflitando quando argumentos já continham `--force`, `-f` ou `--yolo`.
12. **Falha `Invalid params` no envio de chat com IDs de modelo salvos da CLI do Cursor (`#46284`, resolve `#46163`):**
    Modelos configurados pela CLI do Cursor (ex.: `--model cursor-grok-4.6-high`) não eram reconhecidos pelo chat server nativo do Cursor, causando erro de parâmetro inválido no primeiro envio do chat.

## O que o upstream implementa

- **Integração do Cursor no Native Chat sobre servidor ACP (`#42193`, `#41494`):**
  - Adiciona o Cursor como agente suportado no Native Chat, conectando-se ao seu servidor ACP nativo;
  - Reutiliza a autenticação já existente do Cursor no computador do operador;
  - Habilita seleção de modelos, controle de reasoning effort e modo Fast, aprovação interativa de comandos e planos e reabertura de sessões.
- **Leitura em voz alta de respostas com botões Speak no desktop e mobile (`#42168`, `#42654`, resolve `#42653`):**
  - No desktop, adiciona o botão **Speak** ao lado de Copy nos controles de resultado de um turno finalizado, permitindo escolher a voz do SO, velocidade da fala e leitura automática;
  - No mobile (`#42654`), integra síntese de voz usando o motor de fala nativo do smartphone para ouvir respostas de agentes com controles de pausa/parada.
- **Visualização em tela cheia de blocos de código no mobile (`#42646`, resolve `#42645`):**
  - Adiciona botão para expandir blocos de código em modal de tela cheia com quebra de linha opcional e rotulagem automática de cercas sem linguagem indicada.
- **Context Sheet unificado no mobile (`#42639`, resolve `#42631`):**
  - Painel único deslizante que reúne câmera direta, fotos recentes e seletor de arquivos do repositório para enriquecer prompts do chat móvel.
- **Reabertura correta de chats do OpenCode em diretórios movidos (`#42590`):**
  - Rastreia o caminho atualizado da pasta ao reabrir sessões antigas do OpenCode, evitando falhas de diretório inexistente.
- **Prévia visual automática de links de imagens em respostas (`#42227`):**
  - Detecta quando um link em Markdown aponta para um arquivo de imagem local gerado pelo agente e renderiza a prévia da imagem logo abaixo da linha de texto correspondente, preservando o hiperlink intacto.
- **Enfileiramento confiável de `/fork` durante a geração de resposta (`#42215`, resolve `#41903`):**
  - Trata o comando `/fork` emitido durante o streaming de uma resposta enfileirando a bifurcação para ocorrer imediatamente após a conclusão do turno corrente (ou após o acionamento de Stop), bifurcando através da resposta final consolidada.
- **Envelopamento de listas longas de agentes em cartões roláveis (`#42211`):**
  - Envolve listas extensas de ajustes de agentes em cartões com rolagem vertical interna, mantendo a interface contida.
- **Suporte a Approve for me (Auto-review) em terminais do Cursor (`#46142`):**
  - Oferece o modo "Approve for me" em terminais do Cursor com a flag `--auto-review`, mantendo compatibilidade quando argumentos já contêm `--force`, `-f` ou `--yolo`;
  - Isola o modo exclusivo de terminal fora dos seletores de chat do Cursor para evitar recusas do chat server.
- **Resolução de IDs de modelo CLI para modelos e esforço do chat server (`#46284`, resolve `#46163`):**
  - Mapeia nomes salvos da CLI do Cursor (como `cursor-grok-4.6-high`) para o modelo base mais longo correspondente no chat server e decodifica sufixos de thinking, esforço e modo Fast (inclusive mapeando `xhigh` para `extra-high`).

## O que fazer

- Suportar a flag `--auto-review` ("Approve for me") em terminais do Cursor mantendo isolamento de chat (`#46142`).
- Resolver IDs de modelos CLI salvos do Cursor para parâmetros compatíveis com o servidor de chat nativo (`#46284`, resolve `#46163`).
- Integrar o Cursor como agente nativo de chat sobre ACP (`#42193`), suportando seleção de modelo, esforço e planos.
- Renderizar prévias inline de imagens referenciadas por links em respostas Markdown (`#42227`).
- Enfileirar bifurcações `/fork` solicitadas durante a resposta do assistente (`#42215`, resolve `#41903`).
- Adicionar o botão Speak e suporte a síntese de voz (TTS) para respostas de agentes no Native Chat desktop e mobile (`#42168`, `#42654`).
- Adotar visualização de código em tela cheia e Context Sheet unificado no cliente móvel (`#42646`, `#42639`).
- Corrigir a reabertura de chats do OpenCode após movimentação de pastas (`#42590`) e prevenir seletores TUI quebrados no mobile (`#42602`).
- Conter listas de configurações de agentes em cartões roláveis (`#42211`).
