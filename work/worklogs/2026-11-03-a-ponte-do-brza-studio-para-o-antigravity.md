---
scope:
  - workspace
  - brza-studio
refs:
  - issue:integrar-o-brza-studio-ao-antigravity-ide
---

# A ponte do BrzA Studio para o Antigravity IDE

Anderson perguntou, em 2026-11-03: "Conseguiríamos de alguma forma integrar o `BrzA Studio` e o `Antigravity IDE`, por
exemplo, clicar para abrir um arquivo de código - .dart/.Java - e abrir direto no Antigravity ou abrir sessões no chat
do Antigravity pelo Brza CLI". A sessão levantou o que o Antigravity expõe e o que o Studio já tem, e fez a prova de
uma extensão-ponte. O pendente está na issue
[Integrar o BrzA Studio ao Antigravity IDE](../issues/integrar-o-brza-studio-ao-antigravity-ide.md).

## O que se levantou

**Antigravity IDE 2.6.0** (`/Applications/Antigravity IDE.app`, fork do VS Code 1.107):

- O CLI é o `Contents/Resources/app/bin/antigravity-ide`, fora do PATH. Aceita `-g arquivo:linha[:coluna]` e `-r`,
  como o `code`.
- O `antigravity-ide chat "<prompt>"` existe, herdado do VS Code, mas **não chega ao agente do Antigravity**: rodado
  com `-r -m ask`, a janela abriu sem pasta e o painel "Main Agent" (Gemini) ficou vazio — captura de Anderson.
- O URL scheme é `antigravity-ide://`. A extensão do agente, `google.google-antigravity`
  (`extensions/agy/vscode/extension.js`), só trata `/oauth-success`, `/auth-success` e
  `/open-conversation?cascadeId=…&path=…`, que reabre conversa existente.
- O comando que manda prompt ao agente é `antigravity.sendPromptToAgentPanel(texto)`, registrado no workbench com
  `f1:false` (`out/vs/workbench/workbench.desktop.main.js`, classe `PDh`). O `antigravity.startNewConversation` abre
  conversa nova. Nenhum dos dois se alcança de fora sem extensão.

**BrzA Studio** (`brza-studio` em `2511b6298d7`):

- O "Open in" abre a **pasta** do worktree, com lista configurável de apps: os presets são VS Code, Cursor, Zed e
  Devin Desktop (`src/renderer/src/lib/open-in-app-catalog.tsx:17`), e aceita comando customizado.
- O link de arquivo no chat (`src/renderer/src/components/native-chat/use-native-chat-file-link-click.ts`) abre no
  editor do Studio, ou no app padrão do sistema com Shift, sem linha. Não há "abrir no editor externo X na linha N".
- O Studio já confia o workspace do `agy`, o agente de terminal do Antigravity (`markAntigravityWorkspaceTrusted`, em
  `src/main/agent-trust-presets.ts`).

## A rodada

A pergunta: o que fazer com a integração, já sabendo que o `chat` não chega ao agente. Anderson marcou "Prova da ponte
(Recomendado), Plano no workstream app"; a terceira opção, "Só o atalho de hoje", ficou de fora.

## A prova da ponte

Uma extensão `brza.antigravity-bridge` 0.0.1, com `activationEvents: ["onUri"]` e um URI handler:

- `antigravity-ide://brza.antigravity-bridge/prompt?text=…` chama o `startNewConversation`, espera 400 ms (`delay=`) e
  chama o `sendPromptToAgentPanel` com o texto; `new=0` pula a conversa nova.
- `antigravity-ide://brza.antigravity-bridge/open?file=…&line=…&col=…` abre o arquivo na posição.

O VSIX foi montado à mão, sem `vsce`, e instalado com `antigravity-ide --install-extension`. O teste abriu este worktree
com `antigravity-ide -r` e mandou `open "antigravity-ide://brza.antigravity-bridge/prompt?text=Responda apenas: ok
(teste da ponte BrzA)"`.

O que deu: o Antigravity ativou a extensão pela URL (`onUri:brza.antigravity-bridge`, no `main.log` de
`~/Library/Application Support/Antigravity IDE/logs/`), e o log da ponte registrou a chamada sem erro, com retorno
`undefined`. **Não se confirmou** se o prompt foi enviado ao Gemini ou só ficou na caixa: a sessão não vê a janela, e
Anderson não respondeu antes do fechamento.

O fonte e o VSIX ficaram no scratch da sessão, em
`/private/tmp/claude-501/-Users-andepb-Projects-brza-workspace--worktrees-workspace/a9867793-b7e3-4046-b3fc-92b6b926171e/scratchpad/antigravity-bridge/`,
que some com a sessão; o `extension.js` tem 40 linhas e se refaz pela descrição acima.

## Fora do workspace

- **A extensão `brza.antigravity-bridge` 0.0.1**, em `~/.antigravity-ide/extensions/brza.antigravity-bridge-0.0.1`.
  - **Risco:** qualquer app ou página que abra uma URL `antigravity-ide://brza.antigravity-bridge/prompt?text=…` manda um
    prompt ao agente do Antigravity na janela ativa, e o `/open` abre qualquer arquivo local. Para Anderson só, nesta
    máquina.
  - **Estado:** ativa.
  - **Como desfazer:**
    `"/Applications/Antigravity IDE.app/Contents/Resources/app/bin/antigravity-ide" --uninstall-extension brza.antigravity-bridge`.
- **A janela do Antigravity** foi aberta neste worktree pelo `antigravity-ide -r`, e recebeu o prompt de teste.
  - **Risco:** nenhum além de uma conversa de teste no histórico do agente.
  - **Estado:** a janela segue aberta.
  - **Como desfazer:** fechar a janela e apagar a conversa no painel, se ela existir.
