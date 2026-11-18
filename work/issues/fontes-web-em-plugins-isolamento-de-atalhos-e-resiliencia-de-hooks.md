---
status: open
description: Os PRs #43916, #43877, #43876, #43569, #43604 trazem layouts Mermaid ELK empacotados, confiança de hooks no Windows e aviso na substituição de link CLI.
scope:
  - brza-studio
  - workspace
priority: high
opened: 2026-11-07
tags:
  - tooling
  - design
---

# Fontes web em plugins, isolamento de atalhos e resiliência de hooks

Rastreado dos PRs abertos no upstream [`stablyai/orca#43916`](https://github.com/stablyai/orca/pull/43916) (resolve Issue [`#43552`](https://github.com/stablyai/orca/issues/43552)),
[`stablyai/orca#43877`](https://github.com/stablyai/orca/pull/43877),
[`stablyai/orca#43876`](https://github.com/stablyai/orca/pull/43876),
[`stablyai/orca#43569`](https://github.com/stablyai/orca/pull/43569) (resolve Issue [`#42938`](https://github.com/stablyai/orca/issues/42938)),
[`stablyai/orca#43604`](https://github.com/stablyai/orca/pull/43604),
[`stablyai/orca#43389`](https://github.com/stablyai/orca/pull/43389) (resolve Issue [`#43379`](https://github.com/stablyai/orca/issues/43379)),
[`stablyai/orca#39416`](https://github.com/stablyai/orca/pull/39416),
[`stablyai/orca#39413`](https://github.com/stablyai/orca/pull/39413),
[`stablyai/orca#39407`](https://github.com/stablyai/orca/pull/39407),
[`stablyai/orca#39393`](https://github.com/stablyai/orca/pull/39393),
[`stablyai/orca#39348`](https://github.com/stablyai/orca/pull/39348) (Issue [`#15642`](https://github.com/stablyai/orca/issues/15642)) e
[`stablyai/orca#39383`](https://github.com/stablyai/orca/pull/39383).

## O problema

1. **Incapacidade de empacotar e utilizar tipografias customizadas via plugins (`#39416`):**
   Plugins temáticos, suítes de acessibilidade e extensões de código não podiam distribuir fontes web próprias para o
   terminal, editor de código ou elementos visuais da interface. Os usuários eram obrigados a instalar tipografias manualmente
   no sistema operacional do host antes de configurá-las no app, limitando a distribuição portátil de ambientes e temas.
2. **Perda de edições em painéis declarativos ao trocar rapidamente de workspace (`#39413`):**
   Painéis de plugins que salvam estados por workspace armazenavam valores na fila com base no workspace que estivesse
   ativo no momento em que a mensagem de persistência chegava ao processo de renderização. Se o desenvolvedor fizesse uma
   alteração em um painel e trocasse de workspace em menos de ~0,4s, o valor digitado era atribuído ao novo workspace e
   perdido no workspace de origem.
3. **Execução duplicada de ações nativas substituídas por plugins lentos (`#39407`):**
   Quando um plugin substitui um comando interno do aplicativo e a sua execução demora mais de 2 segundos, o app dispara a
   ação interna de fallback. Contudo, o comando do plugin continuava rodando em segundo plano e, ao tentar executar a mesma
   ação internamente via `commands.run`, fazia com que a operação fosse disparada em dobro.
4. **Bypass de segurança em hooks com recusa malformada (`#39393`):**
   Ganchos de segurança configurados como *fail-closed* (`onError: "deny"`) para auditar ou bloquear comandos perigosos no
   terminal eram ignorados se a resposta de recusa violasse o schema esperado (ex.: justificativa superior a 500 caracteres
   ou formato numérico inválido), permitindo a execução indevida do comando protegido.
5. **Atalhos de teclado de plugins bloqueados em terminais focados (`#39348`, `#15642`):**
   Atalhos globais registrados por extensões funcionavam apenas quando o foco do cursor estava fora do terminal interativo.
   Como a maior parte do trabalho ocorre com o terminal em foco, atalhos de plugins ficavam inacessíveis sem cliques adicionais.
6. **Sobrecarga de varreduras de terminais para eventos de status sem ouvintes (`#39383`):**
   A notificação de alteração de status de agentes executava um inventário completo de PTYs para cada evento enfileirado,
   mesmo após o fechamento do painel do plugin que solicitou o acompanhamento.
7. **Inviabilidade de declarar pilha ordenada de fontes fallback (fallback stack) (`#43569`, resolve `#42938`):**
   A configuração de fonte do Editor e do Terminal tratava o valor inserido como um único nome de família tipográfica.
   Não era possível passar uma lista separada por vírgula (ex.: `JetBrains Mono, Menk Qagan StdEx Tig`), impedindo posicionar fontes PUA ou alfabetos específicos à frente das fontes de símbolos Nerd embutidas.
8. **Ausência de armazenamento portátil de preferências para dotfiles (`#43604`):**
   Configurações eram armazenadas em registros de estado do Electron/Chromium, impedindo que desenvolvedores sincronizassem suas preferências de temas, fontes e atalhos entre múltiplas máquinas via repositórios de dotfiles.
9. **Cruzamento excessivo de conexões em diagramas Mermaid no Markdown preview (`#43552`):**
   Diagramas de arquitetura, fluxo e entidades relacionais com mais de 15 nós renderizavam de forma emaranhada no preview sob o motor padrão Dagre, sem que o engine alternativo ELK (`layout: elk`) estivesse registrado.
10. **Re-pedidos contínuos de aprovação de hooks do Codex no Windows por grafia de separador (`#43877`):**
    No Windows, o Orca gravava as chaves de confiança de hooks com ambas as grafias de separador (barra invertida `\` e barra normal `/`). O Codex consultava apenas a grafia com barra invertida em `hooks.json`, fazendo com que hooks já aprovados fossem solicitados novamente a cada novo lançamento de agente.
11. **Substituição silenciosa de links simbólicos CLI entre instâncias do Orca (`#43876`):**
    Ao executar `orca register` ou clicar em "Install CLI", se outra instalação ou versão em desenvolvimento do app já tivesse registrado o link `/usr/local/bin/orca`, a substituição ocorria sem aviso de qual aplicação anterior detinha o vínculo.

## O que o upstream implementa

- **Distribuição segura de fontes tipográficas via manifesto de plugins (`#39416`):**
  - Adiciona o campo `fonts` na especificação de plugins, permitindo declarar arquivos WOFF2 seguros com limite de 2 MB
    por arquivo e 8 MB por família;
  - Sanitiza as fontes na instalação, valida assinaturas de arquivos binários contra WOFF2 corrompidos ou disfarçados e
    serve via protocolo com cabeçalhos CORS/ACAO adequados;
  - Integração no seletor de fontes do terminal, Monaco Editor e interface geral com remensuração automática de glifos.
- **Rastreamento de hidratação de estado em painéis declarativos (`#39413`):**
  - Numera as mensagens `ui.hydrate` e vincula o identificador do workspace a cada pacote `ui.persist`;
  - Descarrega alterações pendentes no cliente antes de carregar o novo contexto e descarta persistências para hidratações
    desconhecidas, garantindo que edições fiquem estritamente no workspace onde foram digitadas.
- **Controle centralizado de deadline para comandos substituídos (`#39407`):**
  - Move a gestão do limite de 2 segundos para o processo principal (`main`), que recusa invocações tardias de `commands.run`
    do comando substituído após o fallback nativo já ter sido acionado.
- **Aplicação estrita de recusa em hooks fail-closed (`#39393`):**
  - Trata qualquer resposta malformada de um participante com `onError: "deny"` como falha fatal e bloqueia a ação protegida.
- **Ativação de atalhos de plugins no terminal sob a política do app (`#39348`):**
  - Estende os comandos de plugins para o contexto do terminal, respeitando a política configurada de precedência de teclas
    (*Orca first* / *terminal first*) e permitindo remapeamento livre pelo usuário.
- **Descarte de inventários órfãos de terminais (`#39383`):**
  - Cancela varreduras caras de PTYs se o painel ou ouvinte do plugin tiver sido fechado antes do processamento da fila.

- **Precedência de variáveis de ambiente em hooks de lançamento de agentes (`#43389`, resolve `#43379`):**
  - Ajusta o ciclo de vida do gancho `agent.launch.before` para que as variáveis de ambiente personalizadas injetadas pelo plugin sejam mescladas após o ambiente da conta do host (`host account env`), assegurando que overrides de plugins (como proxies corporativos, tokens de roteamento ou chaves de sandbox) tenham precedência efetiva sobre defaults de conta.
- **Pilha de fontes fallback separadas por vírgula no Editor e Terminal (`#43569`, resolve `#42938`):**
  - Passa a interpretar a configuração de fonte como uma pilha ordenada com fallbacks sucessivos, viabilizando fontes regionais e PUA sem perder compatibilidade com Nerd Fonts.
- **Preferências portáteis em `~/.orca/settings.json` (`#43604`):**
  - Implementa leitura no arranque e persistência bidirecional contínua de configurações em arquivo plano JSON portátil, simplificando a replicação de ambiente via dotfiles (chezmoi, nix, stow).
- **Suporte ao motor de layout ELK para diagramas Mermaid (`#43916`, resolve `#43552`):**
  - Empacota o Mermaid 11.4+ e carrega assincronamente o pacote `@mermaid-js/layout-elk` para renderizar diagramas complexos no preview com a diretiva `layout: elk`, reduzindo cruzamento de arestas e melhorando a hierarquia visual.
- **Normalização de chaves de hooks do Codex no Windows (`#43877`):**
  - Ajusta `readHookTrustTables` para permitir que a grafia com barra invertida (`\`) lida pelo Codex defina os estados `trusted_hash` e `enabled` sobre variantes com barra normal, eliminando pedidos redundantes de re-aprovação.
- **Aviso na substituição de links simbólicos CLI (`#43876`):**
  - Notifica claramente o desenvolvedor ao executar o registro da CLI (`orca register`) se o link apontava anteriormente para outra instalação ou compilação de desenvolvimento do aplicativo.

## O que fazer

- Suportar pilha ordenada de fontes fallback separadas por vírgula no Editor e Terminal (`#43569`, resolve `#42938`).
- Adotar leitura e escrita de preferências portáteis em `~/.orca/settings.json` para facilitar gestão via dotfiles (`#43604`).
- Habilitar o motor de layout Mermaid ELK no preview de Markdown para diagramas complexos (`#43916`, resolve `#43552`).
- Normalizar chaves de confiança de hooks do Codex no Windows para evitar re-aprovações redundantes (`#43877`).
- Notificar substituição de symlinks na instalação da CLI (`#43876`).
- Aplicar o ambiente de `agent.launch.before` dos plugins após as variáveis de ambiente da conta do host (`#43389`, resolve `#43379`).
- Incorporar o suporte a fontes tipográficas em plugins (`#39416`) no `brza-studio`.
- Adotar o rastreamento por `hydrationId` em formulários declarativos de plugins (`#39413`).
- Aplicar as proteções de concorrência em substituição de comandos (`#39407`) e negação fail-closed em hooks (`#39393`).
- Habilitar o disparo de atalhos de plugins dentro de terminais ativos (`#39348`).
