---
status: open
description: Os PRs #46756, #46724, #46747, #46751, #46749 e #46718 preservam skills conhecidas em falhas de I/O, unificam diretório Gemini CLI e blindam comandos e plugins da CLI.
scope:
  - brza-studio
priority: high
opened: 2026-11-03
tags:
  - tooling
---

# Leitura antecipada e preservação de skills no arranque e nos plugins

<!-- pln-014-despacho -->
> **Despacho (PLN-014/R1.1):** classe `ausente` · casa `studio`
> Merge no upstream não muda `status`. PLN-014/R1, 2026-11-12.

Rastreado dos PRs abertos no upstream [`stablyai/orca#46756`](https://github.com/stablyai/orca/pull/46756) (refs Issue [`#46706`](https://github.com/stablyai/orca/issues/46706)),
[`stablyai/orca#46724`](https://github.com/stablyai/orca/pull/46724),
[`stablyai/orca#46747`](https://github.com/stablyai/orca/pull/46747) (resolve Issue [`#46708`](https://github.com/stablyai/orca/issues/46708)),
[`stablyai/orca#46751`](https://github.com/stablyai/orca/pull/46751) (resolve Issue [`#46713`](https://github.com/stablyai/orca/issues/46713)),
[`stablyai/orca#46749`](https://github.com/stablyai/orca/pull/46749) (resolve Issue [`#46698`](https://github.com/stablyai/orca/issues/46698)),
[`stablyai/orca#46718`](https://github.com/stablyai/orca/pull/46718) (resolve Issue [`#46701`](https://github.com/stablyai/orca/issues/46701)),
[`stablyai/orca#46217`](https://github.com/stablyai/orca/pull/46217),
[`stablyai/orca#46405`](https://github.com/stablyai/orca/pull/46405) (resolve Issue [`#46403`](https://github.com/stablyai/orca/issues/46403)),
[`stablyai/orca#45822`](https://github.com/stablyai/orca/pull/45822),
[`stablyai/orca#45966`](https://github.com/stablyai/orca/pull/45966) (resolve Issue [`#45965`](https://github.com/stablyai/orca/issues/45965)),
[`stablyai/orca#43436`](https://github.com/stablyai/orca/pull/43436),
[`stablyai/orca#42472`](https://github.com/stablyai/orca/pull/42472) (resolve Issue [`#42408`](https://github.com/stablyai/orca/issues/42408)),
[`stablyai/orca#40812`](https://github.com/stablyai/orca/pull/40812),
[`stablyai/orca#40788`](https://github.com/stablyai/orca/pull/40788) (resolve Issue [`#40785`](https://github.com/stablyai/orca/issues/40785)),
[`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) (resolve Issue [`#40181`](https://github.com/stablyai/orca/issues/40181)),
[`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220),
[`stablyai/orca#36897`](https://github.com/stablyai/orca/pull/36897),
[`stablyai/orca#37659 (MERGED no upstream; não está no fork)`](https://github.com/stablyai/orca/pull/37659) e
[`stablyai/orca#19680`](https://github.com/stablyai/orca/pull/19680), além das issues
[`stablyai/orca#43418`](https://github.com/stablyai/orca/issues/43418),
[`stablyai/orca#41017`](https://github.com/stablyai/orca/issues/41017),
[`stablyai/orca#14690`](https://github.com/stablyai/orca/issues/14690),
[`stablyai/orca#37875`](https://github.com/stablyai/orca/issues/37875) e
[`stablyai/orca#32573`](https://github.com/stablyai/orca/issues/32573).

## O problema

1. **Lentidão na varredura de skills (`#35220`):** o processo principal lia uma pasta de skill por vez de forma
   sequencial (`src/main/skills/skill-root-file-walk.ts`). Quando o host está ocupado e há múltiplas árvores de skills e
   cache de plugins, a varredura chega a levar mais de 30 segundos.
2. **Perda de descoberta no arranque (`#36897`):** a confirmação de status após o startup descartava ou refazia a
   descoberta inicial de skills.
3. **Colisão de nomes no seletor `/` (`#19680`) e colisão com skills empacotadas (`#37659 (MERGED no upstream; não está no fork)`):** skills vindas de plugins
   perdiam o namespace `plugin:skill` nos pickers de comando `/`; além disso, a skill bundled `computer use` colidia com
   ferramentas externas de mesmo nome.
4. **Falta de ponto de contribuição para subagentes e skills em plugins (`#37875`, `#32573`):** plugins modernos
   (ex.: ecossistemas de Claude Code e Cursor) empacotam definições de subagentes (`agents/*.md`) junto às suas skills,
   disparando-os pelo nome de tipo do subagente. No runtime do app, `contributes` não aceitava subagentes nem entregava
   skills completas, quebrando plugins que delegam tarefas a subagentes específicos.
5. **Classificação falsa de bundled skills como editadas na presença de arquivos sidecar (`#40214`, resolve `#40181`):**
   Skills empacotadas distribuem apenas `SKILL.md`. O algoritmo de classificação em `bundled-skill-classification.ts` tratava
   o arquivo como atual ou lançado apenas quando `SKILL.md` era a única entrada na pasta. Como ferramentas como Codex geram
   arquivos auxiliares no mesmo diretório (ex.: `agents/openai.yaml` ou scripts locais), o digest do diretório não batia e um
   `SKILL.md` idêntico em bytes passava a ser classificado como `edited`, impedindo atualizações silenciosas automáticas.
6. **Inconsistência no hash de identidade de pacotes de skills por caminhos não ordenados (`#40812`):**
   O cálculo de identidade de pacotes de skills gerava hashes discrepantes para o mesmo conjunto de arquivos dependendo
   da ordem em que o sistema de arquivos retornava os manifestos, disparando alertas falsos de "skill out of date" e invalidações espúrias de cache.
7. **Omissão de dicas de argumentos (argument-hints) de skills no seletor do Native Chat (`#40788`, resolve `#40785`):**
   Ao abrir o picker `/` no chat para invocar uma skill (ex.: `/review`, `/test`), a interface descartava os metadados de
   `argument-hint` definidos no Claude Code, deixando o usuário sem saber quais parâmetros a ferramenta esperava.
8. **Cache infinito do picker impedindo descoberta de novas skills instaladas (`#41017`):**
   O hook `useNativeChatSkills` armazenava o resultado de varreduras bem-sucedidas em `paneDiscoveryCache` sem tempo de expiração
   nem invalidação ao reabrir o seletor. Quando uma nova skill era instalada ou linkada simbolicamente em `~/.agents/skills/`,
   o chat existente continuava afirmando que a ferramenta não existia até a reinicialização da janela do app.
9. **Falso aviso "Needs attention · You edited this copy" em skills embutidas renomeadas (`#42472`, resolve `#42408`):**
   A renomeação de skills bundled (como `orca-computer-use` vs `computer-use`) fazia o verificador de integridade comparar o nome da pasta com o catálogo antigo de lançamentos. Como o identificador divergia, o app disparava falsos alertas de "You edited this copy", ocultava atualizações limpas e não informava qual arquivo ou caminho havia supostamente sido modificado.
10. **Descarte de escopos de skills no seletor `/` do Native Chat (`#43436`):**
    Ao filtrar e selecionar skills pelo menu de barra (`/`) no chat nativo, os escopos associados (projeto, workspace ou usuário)
    eram descartados na transição para o input do chat, impedindo que a execução resolvesse a localização correta da skill.
11. **Falha na instalação por discrepância entre nome no registro bundled e repositório comunitário (`#43418`):**
    O comando `skills install` falhava ao tentar instalar `computer-use` porque o catálogo interno usava o nome curto,
    enquanto o repositório comunitário hospeda sob `orca-computer-use`, tornando a instalação impossível via CLI.
12. **Fragmentação de pastas de skills entre múltiplos agentes gerenciados (`#45822`):**
    Cada agente mantinha suas próprias skills em diretórios isolados (`.claude/skills`, `.agents/skills`), forçando duplicação de instruções e dificultando a reutilização de ferramentas compartilhadas quando o usuário alternava entre agentes no mesmo projeto ou adicionava skills de templates e links.
13. **Falha de empacotamento ao compartilhar skills cujo diretório de origem é um alias simbólico (`#45966`, resolve `#45965`):**
    O pipeline `stageSkill` copiava links simbólicos mantendo-os literais (`verbatimSymlinks`). Quando a pasta raiz da skill era um alias relativo de provedor, a cópia gerava links quebrados (*dangling symlinks*) em sistemas POSIX (`ENOENT`) ou falhava por falta de privilégios de symlink no Windows (`EPERM`).
14. **Skills consideradas desatualizadas falsamente quando agentes gravam arquivos adicionais na pasta (`#46217`):**
    Quando agentes (como Codex) geram arquivos locais ao lado de `SKILL.md` (por exemplo `agents/openai.yaml`), a verificação de frescor julgava a pasta inteira em vez do `SKILL.md` oficial, disparando alertas falsos de desatualização e corrompendo a resolução de cópias anteriores.
15. **Perda de formatação e sumiço de skills de conta Claude no menu `/` após o primeiro turno (`#46405`, resolve `#46403`):**
    O Claude Code lista skills de conta como `<name>` nos descritores de inicialização, mas passa a reportá-las como `anthropic-skills:<name>` no stream do sistema. Após o primeiro turno, o catálogo adotava o nome com namespace, perdendo descrição e dicas de argumentos, e jogando a skill para o final do menu `/`.
16. **Queda total de skills conhecidas diante de falha transitória de I/O na raiz de skills (`#46756`, refs `#46706`):**
    Quando a leitura da raiz de skills encontrava erros temporários de permissão ou I/O (`EACCES`, `EIO`, `EPERM`) em `stat`, `realpath` ou `readdir`, o sistema tratava a raiz como inexistente ou vazia, purgando instantaneamente todas as skills previamente carregadas da memória.
17. **Avisos contínuos de skills duplicadas no Gemini CLI por instalações redundantes (`#46724`):**
    O Gemini CLI lê tanto `~/.gemini/skills` quanto `~/.agents/skills` e emite alertas em cada inicialização caso o mesmo nome apareça em ambos. O aplicativo duplicava a instalação nos dois diretórios.
18. **Ignoramento de flags `--dry-run` com formato `--dry-run=true` em comandos de skills (`#46747`, resolve `#46708`):**
    A checagem estrita `=== true` no parser de flags ignorava `--dry-run=true` (tratada como string `'true'`), executando a instalação/atualização real em vez de exibir a prévia simulada.
19. **Instalação incorreta ou silenciosa em seletores incompatíveis de `plugin install` (`#46751`, resolve `#46713`):**
    O comando `plugin install` descartava silenciosamente `--ref` em IDs de catálogo ou pastas locais, e `--catalog` em pastas de plugins, instalando versões ou origens não solicitadas pelo usuário em vez de rejeitar argumentos inválidos.
20. **Saída com código 0 em falhas parciais de `plugin update --all` (`#46749`, resolve `#46698`):**
    Quando um ou mais plugins falhavam na atualização em lote via `plugin update --all`, a CLI imprimia as linhas de sucesso e retornava código 0, impossibilitando que scripts de automação e CI detectassem falhas.
21. **Descarte indevido de comandos atualizados ao descartar registros antigos (`#46718`, resolve `#46701`):**
    Em `commands.register`, o descarte de uma inscrição de comando anterior apagava o identificador do comando incondicionalmente, removendo também a nova implementação registrada para o mesmo ID.

## O que os PRs fazem

- **Retenção de skills conhecidas como indisponíveis em falhas de raiz (`#46756`, refs `#46706`):**
  - Trata falhas não-ENOENT na raiz de skills lançando `SkillRootUnreadableError`, classificando a fonte como `unavailable` e mantendo em cache a última resposta válida conhecida para não perder skills.
- **Instalação unificada de skills Gemini em `~/.agents/skills` (`#46724`):**
  - Instala skills do Gemini exclusivamente no root compartilhado `~/.agents/skills`, mantendo `~/.gemini/skills` apenas para descoberta manual e aposentando cópias duplicadas antigas.
- **Validação universal de presença de flag para `--dry-run` (`#46747`, resolve `#46708`):**
  - Trata qualquer ocorrência de `--dry-run` (incluindo `--dry-run=true`) como modo preview em `skills install` e `skills update`.
- **Rejeição explícita de argumentos inválidos em `plugin install` (`#46751`, resolve `#46713`):**
  - Emite erro imediato `invalid_argument` ao receber seletores incompatíveis (`--ref` em catálogo/pasta ou `--catalog` em pasta) antes de tentar a instalação.
- **Código de erro e relatório discriminado em falhas de `plugin update --all` (`#46749`, resolve `#46698`):**
  - Retorna código 1 (ou 3 em aprovação pendente) caso algum plugin falhe no update em lote, gerando objeto `error.data.failed` com comandos de repetição específicos por plugin.
- **Descarte escopado por wrapper de comandos substituídos (`#46718`, resolve `#46701`):**
  - Associa cada registro de comando ao seu próprio wrapper único, garantindo que o descarte de um registro anterior remova o comando apenas se ele ainda for o detentor ativo daquele registro.

- **Pasta única e neutra para skills de agentes gerenciados (`#45822`):**
  - Centraliza skills em `<home>/skills/<name>/`, gerando links automáticos para `.claude/skills` e `.agents/skills` na inicialização de chats ou na troca de agentes;
  - Exibe na tela *Settings > Skills* as skills próprias do agente primeiro, rotulando claramente quais diretórios de agentes carregam cada skill e ignorando links órfãos ou duplicados.
- **Resolução de aliases com `realpath` no compartilhamento de skills (`#45966`, resolve `#45965`):**
  - Resolve caminhos de pastas de origem via `realpath` antes de copiar a skill para o staging, preservando o conteúdo real em vez de criar links simbólicos relativos quebrados, e mantendo o tratamento verbatim apenas para links internos da árvore de arquivos.
- **Julgamento de frescor de skills apenas pelo `SKILL.md` oficial (`#46217`):**
  - Julga a atualidade da skill comparando os bytes de `SKILL.md`, ignorando arquivos sidecar inseridos por agentes (como `agents/openai.yaml`), prevenindo classificações errôneas de cópia editada;
  - Mantém a exigência de pasta limpa apenas para decisões de exclusão, protegendo arquivos criados por agentes.
- **Preservação de nomes de skills de conta do Claude no menu `/` (`#46405`, resolve `#46403`):**
  - Retém a grafia desprovida de namespace (`<name>`) para skills reportadas via `anthropic-skills:<name>` no stream do sistema, mantendo a descrição, dicas de argumentos e ordenação correta no seletor de barra.
- **PR `#43436`:** retém deterministamente os escopos de cada skill (`scope`) ao selecioná-la no picker de barra (`/`) do Native Chat, mantendo o contexto de resolução intacto.
- **Issue `#43418`:** propõe alinhar o identificador do catálogo bundled (`computer-use`) com o nome canônico do repositório comunitário (`orca-computer-use`) para permitir instalação direta sem erros de resolução.
- **PR `#40812`:** ordena deterministamente os caminhos completos dos manifestos antes de computar o hash de identidade do pacote de skills, evitando discrepâncias entre sistemas de arquivos.
- **PR `#40788` (resolve `#40785`):** preserva e renderiza `argument-hint` no dropdown de seleção do Native Chat para skills do Claude Code e ferramentas de sessão.
- **PR `#40214` (resolve `#40181`):** compara o digest atual e os digests lançados especificamente para o arquivo `SKILL.md`,
  mesmo quando a pasta contém entradas adicionais. Um `SKILL.md` cujo digest não coincida com nenhum continua sendo classificado
  como `edited` apenas se o nome no frontmatter bater com a skill bundled.
- **PR `#35220`:** introduz `src/main/skills/skill-directory-read-ahead.ts`, disparando a leitura das próximas pastas
  enquanto a atual é processada e mantendo a ordem determinística; reduz o tempo de varredura de 3x a 6x.
- **PR `#36897`:** preserva a lista de skills descobertas no arranque após a confirmação de status.
- **PR `#19680`:** mantém o identificador qualificado `plugin:skill` nos seletores `/` do chat.
- **PR `#37659 (MERGED no upstream; não está no fork)`:** renomeia a skill empacotada para `orca-computer-use` na descoberta, configurações e documentação,
  mantendo links legados e aliases do CLI para evitar quebras.
- **Issues `#37875` e `#32573`:** propõem expor pontos de contribuição declarativos `skills` e `subagents` no manifesto
  do plugin para carregar arquivos de agentes e skills embutidos.
- **Issue `#41017`:** propõe limitar o snapshot em `paneDiscoveryCache` ao período em que o seletor está visível, consultando
  o runtime novamente ao reabrir o picker para detectar skills recém-instaladas sem precisar de watchers em background.
- **PR `#42472` (resolve `#42408`):** resolve nomes canônicos e aliases de skills embutidas contra o registro de digests de lançamento, reconhece symlinks e paths canônicos e exibe o caminho exato do arquivo modificado no card de aviso caso haja edição real.

## O que fazer

1. Adotar a correção de classificação de bundled skills do [`stablyai/orca#40214`](https://github.com/stablyai/orca/pull/40214) para não bloquear atualizações por presença de arquivos sidecar (`agents/openai.yaml`).
2. Aplicar o [`stablyai/orca#35220`](https://github.com/stablyai/orca/pull/35220) (4 arquivos autocontidos em
   `src/main/skills/`) no `brza-studio`, incorporar o `#37659 (MERGED no upstream; não está no fork)` e preparar o sistema de plugins para registrar subagentes
   nativos entregues por pacotes de terceiros.
3. Adotar a ordenação determinística de caminhos no cálculo de identidade de pacotes de skills (`#40812`).
4. Exibir dicas de argumentos (`argument-hint`) no seletor de comandos/skills do chat (`#40788`).
5. Invalidar o cache do seletor de skills ao fechar ou reabrir o picker no Native Chat (`#41017`).
6. Eliminar falsos alertas de edição em skills embutidas renomeadas através da resolução de nomes canônicos e digests de lançamento (`#42472`, resolve `#42408`).
7. Preservar os escopos de contexto de cada skill ao selecioná-la no picker de barra (`/`) do Native Chat (`#43436`).
8. Harmonizar o catálogo bundled de skills (`computer-use`) com o nome no repositório comunitário (`orca-computer-use`) no CLI de instalação (`#43418`).
9. Centralizar skills de agentes gerenciados em pasta neutra `<home>/skills/<name>/` com linking automático (`#45822`).
10. Resolver aliases de provedores com `realpath` no staging de compartilhamento de skills (`#45966`, resolve `#45965`).
11. Avaliar atualidade e frescor de skills isolando o `SKILL.md` oficial de arquivos auxiliares gerados por agentes (`#46217`).
12. Preservar a grafia limpa sem prefixo de namespace para skills de conta do Claude no seletor `/` (`#46405`, resolve `#46403`).
13. Reter skills em cache marcando a raiz como `unavailable` em caso de erro temporário de I/O em vez de esvaziar catálogo (`#46756`, refs `#46706`).
14. Unificar a instalação de skills do Gemini CLI em `~/.agents/skills` sem duplicações em `~/.gemini/skills` (`#46724`).
15. Tratar qualquer formato de `--dry-run` como simulação nos comandos de skills (`#46747`, resolve `#46708`).
16. Rejeitar seletores incompatíveis ou sem valor em `plugin install` com `invalid_argument` (`#46751`, resolve `#46713`).
17. Emitir código 1 e lista de falhas por plugin em `plugin update --all` (`#46749`, resolve `#46698`).
18. Vincular registros de comandos a seus wrappers para não descartar comandos substituídos (`#46718`, resolve `#46701`).

