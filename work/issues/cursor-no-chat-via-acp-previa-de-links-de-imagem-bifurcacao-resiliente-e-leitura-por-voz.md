---
status: open
description: Os PRs #42227, #42215, #42193, #42168 e as issues #42214, #42187 trazem agente Cursor via ACP no chat, prévia de links de imagem, /fork resiliente e leitura por voz.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#42193`](https://github.com/stablyai/orca/pull/42193) (e [`#41494`](https://github.com/stablyai/orca/pull/41494)),
[`stablyai/orca#42227`](https://github.com/stablyai/orca/pull/42227),
[`stablyai/orca#42215`](https://github.com/stablyai/orca/pull/42215) (resolve Issue [`#41903`](https://github.com/stablyai/orca/issues/41903)),
[`stablyai/orca#42168`](https://github.com/stablyai/orca/pull/42168),
[`stablyai/orca#42211`](https://github.com/stablyai/orca/pull/42211),
além das issues [`stablyai/orca#42214`](https://github.com/stablyai/orca/issues/42214) e
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
4. **Falta de acessibilidade e leitura por voz (*text-to-speech*) de respostas de agentes (`#42168`):**
   Respostas extensas ou relatórios emitidos por agentes só podiam ser lidos visualmente na tela, sem opção de síntese de voz para
   ouvir o resultado de um turno enquanto o desenvolvedor trabalha em outro editor ou tarefa.
5. **Listas extensas de configurações de agentes estourando a tela sem rolagem interna (`#42211`):**
   Painéis de configuração com muitos parâmetros de agentes e modelos transbordavam o modal, impedindo a visualização dos botões
   de salvamento em telas menores.
6. **Ausência de formatação rica com caminho e linha ao copiar trechos de código em Markdown (`#42214`):**
   Ao copiar trechos de código do chat ou editor, a área de transferência recebia apenas texto cru, sem o cabeçalho padronizado
   contendo o caminho do arquivo e o intervalo de linhas selecionado.

## O que o upstream implementa

- **Integração do Cursor no Native Chat sobre servidor ACP (`#42193`, `#41494`):**
  - Adiciona o Cursor como agente suportado no Native Chat, conectando-se ao seu servidor ACP nativo;
  - Reutiliza a autenticação já existente do Cursor no computador do operador;
  - Habilita seleção de modelos, controle de reasoning effort e modo Fast, aprovação interativa de comandos e planos e reabertura de sessões.
- **Prévia visual automática de links de imagens em respostas (`#42227`):**
  - Detecta quando um link em Markdown aponta para um arquivo de imagem local gerado pelo agente e renderiza a prévia da imagem logo abaixo da linha de texto correspondente, preservando o hiperlink intacto.
- **Enfileiramento confiável de `/fork` durante a geração de resposta (`#42215`, resolve `#41903`):**
  - Trata o comando `/fork` emitido durante o streaming de uma resposta enfileirando a bifurcação para ocorrer imediatamente após a conclusão do turno corrente (ou após o acionamento de Stop), bifurcando através da resposta final consolidada.
- **Leitura em voz alta de respostas com botão Speak (`#42168`):**
  - Adiciona o botão **Speak** ao lado de Copy nos controles de resultado de um turno finalizado;
  - Configurações de chat permitem escolher a voz do sistema operacional, velocidade da fala e opção para leitura automática ao finalizar cada turno.
- **Envelopamento de listas longas de agentes em cartões roláveis (`#42211`):**
  - Envolve listas extensas de ajustes de agentes em cartões com rolagem vertical interna, mantendo a interface contida.

## O que fazer

- Integrar o Cursor como agente nativo de chat sobre ACP (`#42193`), suportando seleção de modelo, esforço e planos.
- Renderizar prévias inline de imagens referenciadas por links em respostas Markdown (`#42227`).
- Enfileirar bifurcações `/fork` solicitadas durante a resposta do assistente (`#42215`, resolve `#41903`).
- Adicionar o botão Speak e suporte a síntese de voz (TTS) para respostas de agentes no Native Chat (`#42168`).
- Conter listas de configurações de agentes em cartões roláveis (`#42211`).
