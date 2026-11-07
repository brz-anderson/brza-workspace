---
status: open
description: O PR #39416 e os PRs #39413, #39407, #39393 e #39348 trazem fontes web em plugins, persistência de painéis em troca de workspace, travas de substituição e fail-closed em hooks.
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

Rastreado dos PRs abertos no upstream [`stablyai/orca#39416`](https://github.com/stablyai/orca/pull/39416),
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

## O que fazer

- Incorporar o suporte a fontes tipográficas em plugins (`#39416`) no `brza-studio`.
- Adotar o rastreamento por `hydrationId` em formulários declarativos de plugins (`#39413`).
- Aplicar as proteções de concorrência em substituição de comandos (`#39407`) e negação fail-closed em hooks (`#39393`).
- Habilitar o disparo de atalhos de plugins dentro de terminais ativos (`#39348`).
