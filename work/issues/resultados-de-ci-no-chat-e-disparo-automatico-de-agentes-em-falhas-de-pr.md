---
status: open
description: Os PRs #39020 e #39658 (mesclados) trazem linhas e cartões de CI no chat e chegam pelo próximo merge de tag; o #38950 (fechado sem merge), o follow-up automático em falha de PR, espera o gatilho de uso.
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

Rastreado dos PRs do upstream [`stablyai/orca#39658`](https://github.com/stablyai/orca/pull/39658),
[`stablyai/orca#39020`](https://github.com/stablyai/orca/pull/39020) e
[`stablyai/orca#38950`](https://github.com/stablyai/orca/pull/38950), abertos quando a issue nasceu.

## O destino (reunião de 2026-11-09)

A reunião de verificação do [PLN-017: A reunião multiagente com personas roda como fluxo replicável: skill, `brza sessions` e painel no chat](../../plans/PLN-017-a-reuniao-multiagente-como-fluxo-replicavel/PLN-017-plan.md) (P7) decidiu o destino de cada PR. As personas foram Prumo, Trava e Relance, e houve revisor independente. Anderson decidiu em 2026-11-09: "2, 3 e 4 decididos" e "1A decidido". O registro está em [Reunião CI no chat: a coordenação](../worklogs/2026-11-09-reuniao-ci-no-chat-coordenacao.md).

**Os fatos que mudaram** (conferidos por comando em 2026-11-09):

- O `#39020` e o `#39658` foram **mesclados** em 2026-11-08 e estão na tag `v1.4.255`, junto com o `#38750`, o cartão
  "Opened PR" de que o `#39658` depende e que o fork não tem.
- O `#38950` foi **fechado sem merge**. A head real (`ed402736`) tem **163 arquivos**, +12.696. Os "1.352 arquivos" que
  o `gh pr view` mostra vêm da base empilhada na branch do `#39020`.
- O fluxo de hoje tem **0 PRs** no `brza-studio`, no `brza-workflow` e no `brza-workspace`, e o push na `master` não gera
  run. As linhas de CI e o disparo automático só têm evento quando um PR existe, como os 7 PRs do `fixfy-claude` no
  `orca-fixfy` em 24 a 27/10.

**O destino de cada item de "O que fazer no BrzA Studio":**

1. **Linhas de CI no chat (`#39020`)** e **3. cartões de uma linha (`#39658`)**: sem porte e sem cherry-pick. Chegam no
   próximo merge de tag do upstream (≥ `v1.4.255`). O aceite é `NativeChatPullRequestEventLine` em `src/` e os testes dos
   arquivos que o fork tocou, uma linha no checklist do sync, sem issue própria (decisão 2).
2. **Follow-up automático (`#38950`)**: não se porta nem se constrói agora, nem em modo sombra. O desenho de contenção
   e o gatilho de uso estão em [O follow-up automático de CI espera o gatilho de uso, com a contenção já desenhada](o-follow-up-automatico-de-ci-espera-o-gatilho-de-uso.md) (decisão 1, alternativa A).

**Achado à parte:** o CI agendado do fork falha em 20 de 100 runs sem ninguém ver, em
[O CI agendado do `brza-studio` falha sem ninguém ver](o-ci-agendado-do-brza-studio-falha-sem-ninguem-ver.md) (decisão 4).

Esta issue fica aberta (decisão 3) até o merge de tag trazer o visual e o aceite passar.

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
