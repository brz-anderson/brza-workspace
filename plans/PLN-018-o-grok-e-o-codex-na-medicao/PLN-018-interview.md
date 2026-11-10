# PLN-018 — Entrevista

> As rodadas do [PLN-018](PLN-018-plan.md). Só cresce: rodada nova vai ao fim.

### Rodada 1 — o corte da entrega (enviada 2026-11-09)

> **Apresentado antes:** o log de turnos visto naquele levantamento era de Claude; reusar o `measure()` não mede o
> Grok nem o Codex; o rascunho de 8 h + 4 h não comprava a linha (o começo do turno no `events.jsonl` não casa com o
> `turnNumber`, o sync não entregava o pacote nem o `.codex/hooks.json`, e o `grok agent stdio` sobe sem `--trust`);
> o carimbo lia só `CLAUDE_CODE_SESSION_ID`. O texto da rodada ainda dizia que o evento `task` não existia no código
> e que o número livre era o PLN-014. A leitura da pergunta 4 achou o contrário: o P3 do PLN-012 já grava o `task`,
> e o índice ia até o PLN-017.

Respondida em 2026-11-09, na sessão `workspace`.

1. **O que a primeira entrega grava?** Opções, cada uma com o preço apresentado:
   - só o turno (recomendada) — custo: o plano não entrega a `## Medida`; se paga: no resumo de turnos, no primeiro
     turno que o hook gravar;
   - turno e o carimbo da tarefa — custo: mistura com as 16 h do corte do PLN-012, ainda sem aceite; se paga: na
     primeira tarefa cujo commit gravar esse id;
   - nada, só a issue — custo: 0 h; se paga: nunca.

   **Decidido — turno e o carimbo da tarefa**, resposta "1. 2". O preço apresentado estava velho: o D1 já é código
   (`brza-note:719`), o PLN-012 está em execução com o P6.2 pela frente, e a emenda estende o `sessions:` e o `task`
   que o P3 grava. Não entra no corte do PLN-012.

2. **Quais runtimes entram?** Opções:
   - Grok e Codex (recomendada) — o CLI do Antigravity, o chat ACP e os outros ids ficam na issue; custo: duas
     traduções, e a hora só fecha depois da sonda; se paga: no Grok, que já tinha US$ 29 no disco de um dia;
   - Grok, Codex e o CLI do Antigravity — o chat ACP continua fora; custo: mais uma tradução, hora a conferir; se
     paga: no token do CLI, não no chat do app;
   - os 45 do catálogo do Studio — custo: um adaptador por formato, a maioria sem sessão nesta máquina; se paga:
     nunca para os que não estão instalados.

   **Resposta:** "Grok e Codex + uma sonda verificando como medir também o Antigravity" — foi à R2.

3. **Quando o código do hook começa?** Opções:
   - depois da sonda (recomendada) — um Stop do `grok agent stdio` e um do Codex, só com as chaves, antes do
     tradutor; custo: dois turnos, e hora de código 0 até a sonda; se paga: antes de um hook que o launch atual não
     carrega;
   - agora, no hook do worktree, com a pasta confiada — o scratch do Studio é outro git e fica de fora; custo: a
     hora do escritor, ainda sem o mapa do começo do turno; se paga: no CLI aberto dentro do worktree confiado;
   - mudando o launch do Studio (`--trust` e o ambiente) — custo: uma frente no `brza-studio`; se paga: no chat cujo
     cwd é o scratch.

   **Decidido — depois da sonda**, resposta "3. 1".

4. **Onde o plano mora?** Opções:
   - `tools-kit`, PLN-014, prioridade alta (recomendada) — custo: entra na frente do corte do PLN-012, que estava
     medium e sem aceite; se paga: quando esta frente rodar;
   - `tools-kit`, PLN-014, prioridade baixa — custo: 0 h até alguém puxar; se paga: nunca enquanto ficar low;
   - dentro do PLN-012 — custo: o corte dos P1–P6 para, e a R1.3 deixa de valer; se paga: só se essa rodada for
     reaberta de propósito;
   - dentro do PLN-004, no `workspace` — custo: espera o pacote que a R10 decidiu e que não está na árvore; se paga:
     com a primeira entrega desse pacote, se ela incluir o escritor.

   **Resposta:** "verifique o estado atual do planos PLN-004 e PLN-012 antes de decidir". Lidos em 2026-11-09: o
   PLN-012 está `in_progress` / `execution`, P1–P5 e P6.1 feitos, próximo o P6.2, fora de escopo ainda manda Codex e
   Antigravity à issue (R1.3); o PLN-004 está `open` / `interview`, parado em 2026-11-06 antes da R21, frente 3 com
   passo e teste em branco. **Decidido — plano novo no `tools-kit`, prioridade alta.** O número da opção 1 já estava
   tomado; o `brza note plan-open` reservou o PLN-018. Anderson não corrigiu esta casa ao responder a R2.

### Rodada 2 — a frase livre sobre o Antigravity (enviada 2026-11-09)

> **Apresentado antes:** a frase da R1.2, registrada nas palavras de Anderson, e a leitura que virou a primeira opção.

Respondida em 2026-11-09, na sessão `workspace`, com "opção 1".

1. **Quem entra neste plano?** Opções:
   - Grok e Codex na entrega, e uma sonda de como medir o Antigravity (recomendada) — CLI e chat ACP distintos; a
     sonda diz qual superfície tem o que medir; os outros ids ficam de fora; custo: uma leitura (a CLI tem token,
     sem model e sem custo; o chat ACP, nas 11 transcrições já lidas, não tem chave de token), sem escritor do
     Antigravity; se paga: agora, antes do Desenho;
   - Grok, Codex e Antigravity com escritor nesta entrega — a sonda antecede o código dos três; custo: o escritor do
     Antigravity além dos outros dois, e a hora dele só existe se a sonda achar de onde ler token ou custo; se paga:
     depois da sonda, e só nela;
   - Grok e Codex na entrega, e o Antigravity fica na issue — custo: zero de sonda; se paga: nunca para o
     Antigravity neste plano.

   **Decidido — Grok e Codex na entrega, e uma sonda de como medir o Antigravity.**

### Rodada 3 — quem grava a linha, vinda do PLN-004 (não enviada por esta sessão)

> **Apresentado antes:** o aviso da sessão `workspace` em 2026-11-09. O texto do aviso dizia que a sobreposição ainda
> não estava decidida. Lida a entrevista do
> [PLN-004](../PLN-004-os-runtimes-codex-agy-e-grok-no-fluxo/PLN-004-interview.md), o ponto 10 da R21 já tinha resposta.

Respondida em 2026-11-09, na sessão `workspace`, com "siga a recomendação". Esta sessão não perguntou de novo. O
registro de lá é o `f4e90e3`.

1. **Quem grava a linha `turn` do Grok e do Codex?** As três opções estão no ponto 10 da R21 do PLN-004.

   **Decidido — a recomendada de lá.** Este plano é o único escritor da linha `turn` do Grok e do Codex. O `D9` cede
   essa linha e fica com o `agy`, o filho fora da soma do pai, o `guardian_review` do Codex e o `metadata.runtime` da
   memória. O `.grok/hooks/runtime.json` da R18.4 chama o escritor que este plano entregar. O `D8` e o `D9` se
   reescrevem contra este Desenho; a reescrita é do PLN-004. Os leitores do `usage.json` do Grok partilham uma função:
   este plano, o `D9` e o `brza sessions usage` da issue do `playground`.

### Rodada 4 — executar o escritor aqui (não enviada por esta sessão)

> **Apresentado antes:** o Desenho já dizia que o `.grok/hooks/runtime.json` da R18.4 chama o escritor e que este plano não grava esse json.

Anderson, em 2026-11-09, nesta sessão, citou:

> "O .grok/hooks/runtime.json da R18.4, e o hook do Codex, ficam no PLN-004 e chamam o escritor daqui. Este plano não instala outro json."

e respondeu "execute aqui". Esta sessão não abriu opções.

1. **Onde o escritor roda?** A frase é o corte. O script do D1 e do D2 é executado nesta sessão. Os dois arquivos de hook ficam no PLN-004 e chamam esse script. Este plano não instala outro json. O carimbo do D3 vai junto: a R1.1 entrega o turno e o carimbo.

   **Decidido — executar o escritor nesta sessão.**
