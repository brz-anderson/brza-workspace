---
status: open
description: Os PRs #39658, #39020 e #38950 trazem cards unificados de CI no desktop/mobile, resultados no chat e follow-up automático em falhas de PR.
scope:
  - brza-studio
  - brza-workflow
priority: high
opened: 2026-11-06
tags:
  - chat
  - tooling
---

# Resultados de CI no chat e disparo automático de agentes em falhas de PR

Rastreado dos PRs abertos no upstream [`stablyai/orca#39658`](https://github.com/stablyai/orca/pull/39658),
[`stablyai/orca#39020`](https://github.com/stablyai/orca/pull/39020) e
[`stablyai/orca#38950`](https://github.com/stablyai/orca/pull/38950).

## O problema

1. **Desconexão entre o chat que abriu o Pull Request e os resultados da integração contínua (`#39020`):**
   Quando um agente cria um PR ou faz push de commits na sessão de chat, a evolução dos testes de CI (GitHub Actions ou
   outros provedores) ficava completamente desconectada da conversa. O desenvolvedor ou operador precisava abrir o navegador
   ou consultar o painel Checks manualmente para saber se os testes passaram ou falharam, sem feedback visual contextual no chat.
2. **Dependência de ação humana para disparar correções em falhas de CI (`#38950`):**
   Ao falhar uma suíte de testes de um PR em segundo plano, nenhuma ação era tomada até que o usuário visualizasse a falha e
   clicasse no botão manual "Fix with AI" no painel Checks. Em execuções assíncronas ou quando o app estava minimizado, o
   trabalho ficava estagnado mesmo quando agentes autônomos poderiam intervir imediatamente para corrigir o erro.

## O que o upstream implementa

- **Linhas visuais de eventos de CI no Native Chat (`#39020`):**
  - Insere uma linha de status discreta no diário do chat que abriu ou enviou commits para o PR (`presentation: 'pull-request-event'`);
  - Registra vereditos finais inequívocos: "CI failing" (vermelho com links diretos para os runs com falha) ou "CI green"
    (verde após a conclusão bem-sucedida);
  - Ignora estados transitórios (cancelamentos intermediários de execuções anteriores, etapas neutras ou aguardando aprovação),
    evitando falsos positivos quando um novo push cancela a rodada anterior;
  - Compartilha requisições ao GitHub entre múltiplos checkouts e limita a paginação de checks a 10 páginas para proteger a cota da API;
  - Adiciona controle de visualização em `Settings → Chat UI → Appearance → CI result lines` e botão de ocultação rápida.
- **Disparo autônomo de agentes para correção de falhas de CI (`#38950`):**
  - Implementa a funcionalidade "Automatic follow-ups for failing checks", configurável em `Settings → Source Control AI`
    (com sobreposição opcional por projeto);
  - Quando os checks de um PR falham, inicia automaticamente o mesmo agente e prompt do fluxo "Fix with AI" no respectivo workspace;
  - **Mecanismos de contenção contra loops:**
    - Atua apenas uma vez por conjunto de falhas em um determinado commit (reexecutar a mesma falha não aciona agentes em loop);
    - Limite de até 3 agentes automáticos sucessivos por PR (zerado por pushes manuais do desenvolvedor, mas nunca por pushes de agentes automáticos);
    - Teto estrito de segurança de no máximo 6 execuções automáticas por PR em uma janela de 24 horas;
    - Fila de espera: nunca inicia um agente se outro já estiver trabalhando no workspace;
    - Exibe linha explicativa "Automatic follow-ups" no painel Checks, etiqueta "Fixing checks · auto" no cartão do workspace e
      notificação nativa de desktop caso a janela do aplicativo não esteja em foco.
- **Cartões de uma linha para CI no desktop e celular (`#39658`):**
  - Substitui o texto estático centralizado por cartões compactos de uma linha (`NativeChatPullRequestEventLine`), com o mesmo
    estilo visual (borda, cantos arredondados, padding) dos cartões de "Opened PR";
  - Exibe ícone colorido de status (verde/vermelho), texto resumido "CI failing on `repo#N` at `sha`", links diretos para o PR e commit,
    e botão de ocultação rápida no desktop;
  - No cliente móvel (iOS/Android), sincroniza o cartão ao vivo seguindo a configuração do desktop pareado (`nativeChatCiResultLines`),
    filtrando em tempo de projeção sem exigir recargas do histórico de mensagens.

## O que fazer no BrzA Studio

1. Portar a exibição de resultados de CI diretamente nos balões de eventos do chat (`#39020`), unificando o ciclo de vida
   de desenvolvimento e revisão dentro da conversa.
2. Integrar a automação de auto-healing de PRs (`#38950`) ao fluxo do `brza-workflow`, permitindo que workspaces corrijam
   testes quebrados autonomamente sob supervisão configurável.
3. Adotar o formato de cartões de uma linha de CI para desktop e mobile (`#39658`), sincronizando preferências de exibição entre dispositivos.
