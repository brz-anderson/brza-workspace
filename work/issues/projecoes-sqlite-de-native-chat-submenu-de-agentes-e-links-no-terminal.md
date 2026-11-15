---
status: open
description: Os PRs #42738, #39256, #39106, #39569 e as issues #42730, #42673 trazem retomada de sessões no menu de agentes (+), projeções SQLite no chat e URLs no terminal.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-08
tags:
  - chat
  - tooling
---

# Projeções SQLite de Native Chat, submenu de agentes e links no terminal

Rastreado dos PRs abertos no upstream [`stablyai/orca#42738`](https://github.com/stablyai/orca/pull/42738) (resolve Issue [`#42730`](https://github.com/stablyai/orca/issues/42730)),
[`stablyai/orca#39256`](https://github.com/stablyai/orca/pull/39256),
[`stablyai/orca#39106`](https://github.com/stablyai/orca/pull/39106) (resolve Issue [`#39105`](https://github.com/stablyai/orca/issues/39105)),
[`stablyai/orca#39569`](https://github.com/stablyai/orca/pull/39569),
[`stablyai/orca#37778`](https://github.com/stablyai/orca/pull/37778),
além das issues [`stablyai/orca#42673`](https://github.com/stablyai/orca/issues/42673),
[`stablyai/orca#39704`](https://github.com/stablyai/orca/issues/39704) e
[`stablyai/orca#38825`](https://github.com/stablyai/orca/issues/38825).

## O problema

1. **Reconstrução completa de diários de Native Chat em memória (`#39256`):**
   No modelo atual, o host de execução recria e retém em memória RAM todo o estado do diário (*journal*) de conversas nativas.
   À medida que o histórico de chats se acumula com centenas de mensagens, blocos de código e ferramentas, o consumo de
   memória cresce desproporcionalmente e a abertura de sessões existentes sofre degradação sensível de latência.
2. **Conflito entre links HTTP e detecção de arquivos locais no terminal (`#39106`, `#39105`):**
   Ao clicar com `Cmd+Click` sobre URLs impressas no terminal contendo subrotas, portas ou parâmetros
   (ex.: `http://localhost:5173/settings/profile` ou `?path=/story/x`), o detector de links de arquivo local
   interceptava o clique antes do navegador. O aplicativo interpretava o segmento `/settings/profile` como caminho no disco,
   exibindo o erro espúrio `File not found: /settings/profile` em vez de abrir o link no navegador.
3. **Inoperância do botão de setup de agentes nos resultados de busca do omnibox (`#39569`):**
   No menu de criação rápida (`+`), ao digitar texto para pesquisar agentes, as linhas filtradas exibiam o glifo indicador
   `›` para configuração, mas o clique não surtia nenhum efeito. As linhas regulares usavam um submenu ao passar o mouse,
   enquanto as linhas de busca tentavam abrir um popover que falhava silenciosamente dentro da caixa de busca (*omnibox*).
4. **Tracking residual de mouse travando terminais após saída anômala de utilitários (`#37778`):**
   Quando ferramentas ou programas interativos em terminal morriam abruptamente sob shells sem suporte a sequências OSC 133,
   o modo de rastreamento de mouse permanecia ativo, capturando cliques e impedindo seleção comum de texto.
5. **Falta de hot-swapping de modelo e esforço no Cursor (`#39704`):**
   Enquanto Claude Code e Codex permitem alternar modelo e nível de esforço de raciocínio a quente durante uma sessão ativa,
   agentes rodando no Cursor exigiam encerramento completo e reinício da tarefa.
6. **Abas de terminal presas em "Reattaching terminal" em clientes desktop pareados (`#38825`):**
   Ao abrir novos terminais a partir de um cliente desktop secundário pareado com o host de desenvolvimento, o handshake de
   reattach falhava, retendo as abas em estado de espera infinito enquanto clientes iPhone e locais funcionavam.
7. **Ausência de atalho para retomar sessões anteriores no menu de lançamento `+` (`#42738`, resolve `#42730`):**
   O menu `+` permitia apenas iniciar novas conversas. Para retomar um histórico anterior, o usuário precisava navegar até o painel lateral de agentes ou abrir um chat vazio e digitar `/resume`, que substituía a aba ativa; além disso, faltava suporte a sessões do DSH Harness (`.dsh`) (`#42673`).

## O que o upstream implementa

- **Ação "Resume session…" no painel de configuração de agentes do menu `+` (`#42738`, resolve `#42730`):**
  - Adiciona o botão "Resume session…" sob as opções de inicialização (Launch chat / Launch terminal) no painel de cada agente no menu `+`;
  - Abre diretamente o diálogo de histórico de sessões do workspace ativo já pré-filtrado para o agente selecionado, permitindo restaurar a sessão em uma nova aba com o botão ▶ sem substituir a conversa corrente;
  - Suporta localização em todos os idiomas suportados (`agentPicker.resumeSession`).
- **Projeções persistidas em SQLite para Native Chat (`#39256`):**
  - Substitui o journal volátil em memória por projeções tipadas persistidas diretamente no SQLite do host;
  - Utiliza um único gravador assíncrono em segundo plano (*background writer*), procedimentos de leitura delimitados
    (*bounded reader procedures*) e paginação otimizada de histórico para frente e para trás;
  - Converte chats legados de forma transparente e em segundo plano durante períodos ociosos, sem interromper ou exibir
    avisos intrusivos na interface. Chats convertidos passam a ser servidos diretamente do SQLite com tempo constante de abertura.
- **Priorização de URLs no Cmd+Click de terminais (`#39106`):**
  - Ajusta a função `openFilePathLinkAtBufferPosition` para ceder e retornar `false` caso a célula clicada pertença a uma
    URL reconhecida por `findTerminalHttpLinkAtBufferPosition`;
  - Garante que cliques em URLs quebradas em múltiplas linhas ou com portas e subdiretórios abram a página web sem acionar o
    fallback de busca de arquivos locais.
- **Submenu flutuante para setup de agentes na busca (`#39569`):**
  - Unifica o componente `AgentLaunchSetupSubmenu` baseado em Radix `DropdownMenuSub` para linhas normais e linhas de busca;
  - Abre o painel de configuração de modelo/argumentos ao passar o mouse sobre o `›` da linha filtrada, mantendo o foco do
    teclado ativo no campo de busca para digitação contínua.
- **Reset de tracking de mouse após término de processos (`#37778`):**
  - Limpa flags obsoletas de captura de mouse quando a aplicação filho encerra sem enviar o código de escape de desativação.

## O que fazer

- Incorporar o botão "Resume session…" no painel de configuração do menu de lançamento `+` (`#42738`, resolve `#42730`) e suporte a sessões DSH Harness (`#42673`).
- Acompanhar a fusão das projeções SQLite de Native Chat (`#39256`) e planejar a migração do armazenamento de conversas no `brza-studio`.
- Incorporar a priorização de links HTTP sobre arquivos locais no terminal (`#39106`), eliminando falsos erros de `File not found`.
- Adotar o submenu unificado em hover para configuração de agentes na pesquisa rápida (`#39569`).
- Aplicar o reset automático de mouse tracking sob saída anômala de subprocessos (`#37778`).
- Avaliar a paridade de troca a quente (*hot-swapping*) de modelos para agentes Cursor (`#39704`).
- Investigar a causa do travamento de reattach de terminais remotos em clientes pareados (`#38825`).
