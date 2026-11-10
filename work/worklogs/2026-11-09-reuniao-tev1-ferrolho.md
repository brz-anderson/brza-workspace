---
scope:
  - workspace
  - brza-workflow
  - brza-studio
tags:
  - tooling
sessions:
  - f497c2b6-20bf-4786-8d30-73c4cec86d58
---

# Reunião tev1 nos fluxos: a participação de Ferrolho, guardião da falha silenciosa

O pedido de Anderson, em 2026-11-09, na sessão da coordenação (meeting-runner, chat do BrzA Studio): "classificar, com fatos medidos, os melhores usos do `tev1:4b` local nas seis frentes — CLI, Studio, MCP, meeting-runner, plan-runner, migration-runner —, em estilo brainstorm; saída: proposta de plano e o plano criado neste workstream, mapeando para onde ele pode evoluir". Este é o
registro de **Ferrolho** — persona guardião da falha silenciosa, no Codex `gpt-6.1-terra` `medium` —, aberto pela coordenação. A pauta e as
regras estão no briefing da reunião; cada rodada é uma seção abaixo, acrescentada no fim do arquivo.

## O que se fez

### Rodada 1: opinião inicial

- **Posição:** Classificação útil começa em sombra; nenhum erro caro pode desaparecer sem revisão.

#### 1. O ranking dos usos

- **Posição:** Primeiro votos não reconhecidos, depois gatilhos em sombra, depois triagem do Studio em sombra.
- **Por quê:** *lido* `tally.py:226-234` retorna `None` para texto livre: meeting-runner, `classify_vote`, pergunta “qual voto?”; apoio/ressalva/contra/não identificável. *Lido* `work/issues/tev1-como-classificador-nos-scripts-da-meeting-runner.md:35-40`: gatilho voto × fato, sim/não, mantém revisão pela coordenação. *Lido* `.sessions/reuniao-tev1/material/levantamento.md:35-38`: Studio, `startup-dialog-blocked-signals.ts`, “qual bloqueio?”; categorias existentes/nenhum/desconhecido. Os dois últimos são sugestões, não decisões automáticas.
- **Ideias:** `tally.py` mostra sugestão e texto original só para `None` (ousadia: baixa); `estado-rN.json` lista todos os pares e suspeitas de contradição para revisão (ousadia: média).
- **Risco:** *suposto* um falso voto altera placar ou um “não” esconde fato relevante; sempre preservar `None` e a inspeção dos pares.
- **Confiança:** 82/100 — adequação inferida das fontes; nenhum ganho de acerto foi medido aqui.

#### 2. A régua de entrada

- **Posição:** Limiares por classe e consequência, escolhidos em dados independentes; dúvida é resultado explícito.
- **Por quê:** *lido* issue `:45-59`: 4 sintéticos acertaram, mas os dois “sim” têm as menores confianças; 4 casos não calibram. *Lido* `levantamento.md:123-134`: há poucos pares reais e nenhum gold pronto; não prometer precisão a partir deles.
- **Ideias:** rotular pares cegamente por duas pessoas e resolver divergências; separar por reunião e reservar teste sem ajuste (ousadia: média). Medir matriz, cobertura, falsos negativos, intervalos e custo contra fluxo atual; proposta inicial: pelo menos 100 positivos independentes para estimar perda rara, sem tratar esse número como garantia (ousadia: média).
- **Risco:** *suposto* zero erros em amostra pequena não prova segurança; alta `confidence` não é probabilidade calibrada. Sem evidência suficiente, mantém sombra; gatilho incerto ou negativo segue à coordenação, voto incerto fica `None`; Haiku é segunda opinião, não verdade.
- **Confiança:** 83/100 — desenho prudente, tamanho mínimo proposto, não validado.

#### 3. Onde mora o cliente

- **Posição:** Cliente comum no `brza-workflow`, adaptadores por frente e fallback próprio de cada tarefa.
- **Por quê:** *lido* `~/Projects/brza-workflow/packages/mcp/brza_mcp/resolver.py:89-126`: já há chamada, limiar ausente leva ao Haiku, falhas ao fallback e opção fora da lista é rejeitada. A tabela existente serve ao roteamento de camada, não a todos os usos.
- **Ideias:** contrato tipado `choice|unknown`, confiança, versão do modelo, motivo e duração; validar finitude/faixa, perguntas e opções (ousadia: média). `brza classify` expõe JSON e saída distinta para desconhecido; sem Ollama, fila cheia ou HTTP 400 por contexto, devolve desconhecido e sinaliza, sem cortar silenciosamente (ousadia: média).
- **Risco:** *suposto* log com texto sensível vaza contexto; por padrão registrar metadados e identificadores, entrada apenas com política e retenção explícitas. O orçamento e prazo da fila precisam ser definidos por consumidor.
- **Confiança:** 80/100 — contrato proposto; comportamento existente lido na fonte.

#### 4. Além do óbvio

- **Posição:** Monitor de contradições em sombra e múltiplas perguntas com falha isolada; não automatizar autorização.
- **Por quê:** *lido* briefing `.sessions/reuniao-tev1/briefing.md` e issue `:35-38`: fato novo pode afetar voto e há erro caro em omitir gatilho. *Lido* `levantamento.md:97-109`: plan-runner e migration-runner têm escolhas em prosa, ainda sem garantia de corpus rotulado.
- **Ideias:** no plan-runner, sugerir gênero de nota/plano/issue/decisão/parecer e pedir à sessão conferir (ousadia: média); no migration-runner sugerir Criar/Revisar/Executar/desconhecido, sem executar (ousadia: média). CLI sugere interpretação de erro em `brza-run`; MCP mantém tabela e gate numérico (ousadia: média).
- **Risco:** *suposto* múltiplas perguntas podem compartilhar erro ou indução; validar cada resposta e registrar falha individual. Não substituir regex exata, regra de cota, aprovação humana ou auditoria de fatos por classificação; não tratar o system prompt como defesa comprovada contra injeção. Retreino só após corpus consentido, avaliação cega e comparação de deriva (ousadia: alta).
- **Confiança:** 75/100 — aplicações e efeitos são hipóteses a testar.

#### 5. O plano e para onde evolui

- **Posição:** Dados, sombra, piloto reversível e expansão condicionada a erro observável.
- **Por quê:** *lido* `resolver.py:95-109` já tem degradação em cascata; *lido* `levantamento.md:125-134` descreve corpus existente e suas limitações.
- **Ideias:** Fase 1: inventariar e rotular casos reais, inclusive negativos e injeções, com revisão de divergência (ousadia: baixa). Fase 2: replay em sombra por versão, medir matriz, cobertura, latência da coordenação e custo (ousadia: baixa). Fase 3: piloto só para voto não reconhecido, com fonte visível e reversão; pronto quando métricas e limites por classe forem aceitos e teste independente passar (ousadia: média). Fase 4: avaliar gatilho, Studio e demais frentes separadamente, com revalidação após mudanças (ousadia: média).
- **Risco:** *suposto* seleção enviesada e deriva de modelo/prompt tornam métricas obsoletas; alerta de versão, amostragem revisada também dos aceitos e desligamento preservam o fluxo antigo. Evoluções: lote de perguntas, segundo modelo, retreino e auditoria comparativa.
- **Confiança:** 80/100 — fases propostas; critérios numéricos dependem da medição e da decisão posterior.

#### A ideia mais ousada desta rodada

*Suposto, 60/100:* um sentinela em sombra cruza cada voto com cada fato novo e registra inclusive os pares considerados sem relação; amostras cegas de negativos vão à coordenação. Risco: volume quadrático e fadiga de revisão, exigindo orçamento e amostragem medidos antes de qualquer automatização.

#### Issues candidatas

- **Corpus rotulado e avaliação cega por reunião** — *suposto, 80/100*: mede erro antes de delegar decisão — prioridade `high`.
- **Contrato de desconhecido e degradação por consumidor** — *lido*, `resolver.py:89-126`, 90/100: evita transferir fallback de camada a outros usos — prioridade `high`.
- **Detecção de deriva e revisão de negativos** — *suposto, 70/100*: expõe regressão silenciosa após alteração — prioridade `medium`.

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. O ranking dos usos | Voto não reconhecido, gatilho em sombra, diálogo do Studio em sombra | 82 |
| 2. A régua de entrada | Métricas por classe, teste independente e revisão dos desconhecidos | 83 |
| 3. Onde mora o cliente | Cliente comum com falha explícita e fallback específico | 80 |
| 4. Além do óbvio | Sentinela e sugestões; nenhuma autorização automática | 75 |
| 5. O plano e para onde evolui | Dados, sombra, piloto reversível e expansão com revalidação | 80 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

- **Posição:** Rebaixo voto e gatilho; sombra primeiro, com negativos revisados e evidência preservada.

#### As disputas

- **D1 · o envelope do cliente:** c — *lido*, `resolver.py:89-126`: extrair módulo comum e oferecer verbo fino para processos externos; ambos preservam `unknown`, motivo e fallback específico. O custo de empacotar/instalar o módulo nos consumidores ainda é *suposto* e precisa ser medido. 81/100.
- **D2 · o primeiro uso depois da sombra:** e — *lido* síntese M5, M6 e M11: 4/98 votos escapam do regex, só 7 resoluções e 3/6 gatilhos positivos foram perdidos. Não há evidência para ligar um deles; *suposto*: priorizo reunir pares auditáveis do resolver e da auditoria sem mudar a rota. 90/100.
- **D3 · a régua:** c — *suposto*: 100 positivos independentes é meta inicial para erro caro, não garantia; escolha de limiar em conjunto separado e teste cego por reunião, intervalo de confiança e custo do erro. Na falta de casos, sombra continua; alarme sem supressão pode ter régua própria. 82/100.
- **D4 · o diálogo de startup do Studio:** b — *lido* M9: há quebra de regex, mas volume e falsos negativos não foram medidos. Primeiro contar misses e rotular telas com retenção autorizada; comparar à regra atual, sem substituir nem esconder bloqueios. 87/100.
- **D5 · retreino:** b — *lido* M8: a evidência histórica é apagada; registrar novos exemplos com autorização e retenção definida, preservar teste separado e só então comparar ajuste com baseline. Não presumir que o ajuste será útil ou executável. 89/100.

#### Os ataques

- **Balança, alarme `sim` ≥ 0,50:** *lido* M11 e sua R1: 2/6 positivos levantariam alarme; os demais continuam exigindo leitura, e um painel parcial pode transmitir cobertura falsa. Derruba meu ataque uma avaliação independente que mostre ganho líquido de revisão e exiba explicitamente todos os pares não alertados. 87/100.
- **Faro, sanitizador de injeção e LoRA histórico:** *lido* R1 de Faro e M8: instrução no system não demonstra resistência a ataque e os pares completos de auditoria não existem. Derrubam o ataque corpus recuperável confirmado e teste adversarial independente com taxa de falha medida; ainda assim não seria garantia absoluta. 92/100.

#### A concessão

- **M5 e M11, coordenação e Balança:** *lido* `.sessions/reuniao-tev1/sintese-1.md` M5/M11: retiro o voto `None` do primeiro lugar e deixo o gatilho somente em sombra; nenhum desses números autoriza supressão. *Lido* M12: a segunda pergunta `evento` marcou sim em 23/23 e não repara o filtro. 93/100.

#### "Sim, e…"

- **Sobre a ideia de Balança**, *suposto*: um painel de pares com amostragem aleatória auditável dos `não` e dos desconhecidos, além dos alertas; cada par conserva versão, justificativa da rotulagem e resultado de revisão, com orçamento para não sobrecarregar a coordenação `(ousadia: média)`. Risco: amostra pequena mascara falha; publicar denominador e intervalo. 75/100.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem ou o que te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :--------------------- |
| 1. O ranking dos usos | Nenhum piloto ativo; resolver e auditoria em sombra | 82 | 90 | virou | M5, M6, M8, M11 |
| 2. A régua de entrada | Por classe, teste independente e limites de erro | 83 | 82 | ajustou | Balança, M11 |
| 3. Onde mora o cliente | Módulo comum e verbo fino, desconhecido explícito | 80 | 81 | ajustou | Bitola e M2–M3 |
| 4. Além do óbvio | Revisar negativos; não confiar em sanitização | 75 | 85 | ajustou | Balança, Faro, M12 |
| 5. O plano e para onde evolui | Preservar evidência, medir em sombra e reavaliar | 80 | 89 | ajustou | M8 e M11 |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

- **Posição:** Apoio a sombra auditável, com rótulo independente, privacidade e falhas visíveis.
- **Fatos lidos:** M13, M14, M15; também M5, M8, M11 e M12 na síntese anterior.

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | *Suposto*: contar tokens do prompt completo com tokenizer compatível, incluindo instruções; sem contagem confiável, tratar HTTP 400 como `unknown`, sem truncar; fila limitada e prazo explícito. | 88 |
| P2 | apoio com ressalva | *Suposto*: hash não anonimiza conteúdo previsível; texto só com política e autorização para dados sensíveis, acesso restrito, retenção validada e exclusão verificável; 30 dias é proposta. | 91 |
| P3 | apoio com ressalva | *Lido* M8: preservar evidência é necessário; *suposto*: veredito do Haiku é rótulo provisório, e cópia segue a proteção de P2; pares completos e negativos permanecem visíveis. | 91 |
| P4 | apoio com ressalva | *Lido* M13: testar `layer` com task integral, sem assumir que descrições curtas representam produção; *suposto*: orçamento de fila e falha em sombra jamais atrasam o fluxo principal. | 89 |
| P5 | apoio com ressalva | *Suposto*: revisar amostra aleatória de concordâncias também; 0 FN em 30 não prova risco zero, e métricas por classe, intervalos, cobertura e custo acompanham teste independente por reunião. | 94 |
| P6 | apoio com ressalva | *Lido* M14 mostra sensibilidade à ordem; *suposto*: 20 pares e cortes 80%/10% são triagem exploratória, não prova; cobrir classes, ordens, equilíbrio e incerteza, sem vetar prevalência real alta por si só. | 90 |
| P7 | apoio | *Lido* M9: medir misses antes do Studio; *suposto*: manter regras tipadas e aprovações fora de inferência impede erro caro sem retorno. | 88 |
| P8 | apoio com ressalva | *Lido* M13/M15: destravar exige corpus apropriado; *suposto*: cada evolução também exige avaliação independente, custo e decisão sobre dados; retreino pode nunca compensar. | 86 |

#### O que me faria mudar de ideia

- **P5:** *suposto, 94/100*: uma avaliação independente que prove que a revisão apenas das divergências captura erros compartilhados por tev1 e Haiku derrubaria minha ressalva; um procedimento estatístico justificado que satisfaça o risco acordado poderia substituir a exigência de revisão aleatória.
- **P2:** *suposto, 91/100*: uma análise concreta que demonstre que estados e hashes não carregam informação sensível e que a retenção de 30 dias cumpre a política aplicável derrubaria minha ressalva para esse corpus delimitado.

#### A última ideia

**Sobre a ideia de Bitola**, *suposto, 75/100*: em `tally.py`, um modo de revisão sob demanda mostra ao coordenador os pares voto × fato ordenados pela sugestão do `tev1`, mas mantém a lista completa e o fluxo de hoje; humano confere também os últimos da lista `(ousadia: média)`. Antes, medir em replay cego tempo total, positivos perdidos e fadiga contra ordem original; só usar se melhorar sem ocultar pares. O risco é viés de atenção mesmo sem supressão.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Balança | *Lido* M11: demonstrou três falsos negativos em seis positivos reais. | 10 |
| Bitola | *Lido* síntese C9: propôs probe de discriminação antes do catálogo. | 9 |
| Fagulha | *Lido* síntese C8: levou a perda da evidência da auditoria à fase zero. | 9 |
| Faro | *Lido* síntese D5: manteve retreino como evolução após formação de corpus. | 8 |
| Lida | *Lido* síntese da rodada 2: abandonou limiar do `layer` diante da falta de dados. | 9 |

#### Autoavaliação

*Suposto, 85/100:* fui fiel ao exigir visibilidade dos negativos, falhas explícitas e revisão independente. Saí do veto por princípio ao propor uma ordenação reversível, sujeita a comparação cega e sem retirar nenhum par da leitura.

<!-- fim-rodada-3 -->

### Rodada 4: a confiança final

- **Posição:** Apoio o plano com sombra protegida; a ordem visível exige comparação antes do uso.
- **Fatos lidos:** M17, M18, M19; também M8, M11 e M13.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| O cliente (P1) | 88 | 89 | *Lido*, O desenho/P1: HTTP 400 vira `too_long`; *suposto*: falta fixar orçamento e prazo da fila. |
| A sombra, o corpus e a linha zero (P2, P3) | 91 | 86 | *Lido*, M8/M18: corpus é necessário; *suposto*: falta explicitar acesso, exclusão verificável e revisão do Haiku como rótulo provisório antes da gravação. |
| A sugestão visível e a ordem | — | 65 | *Lido*, M17: três positivos ficam nas posições 11, 15 e 16; *suposto*: lista completa não elimina ancoragem e requer replay cego comparativo antes do painel. |
| A régua e o portão (P5, P6) | 92 | 86 | *Lido*, fases 3–4 e catálogo: revisão de concordâncias entrou; *suposto*: faltam intervalos e avaliação por classe, e 30 positivos com zero erro não provam risco zero. |
| As evoluções (P8) | 86 | 86 | *Lido*, evoluções: continuam condicionadas ao corpus; *suposto*: retreino precisa também de dados autorizados, custo e teste independente. |
| **O plano inteiro** | 90 | 82 | *Lido*, classificação e desenho: o painel é proposto já; *suposto*: isso antecipa a comparação necessária e a política de dados deve preceder a linha zero. |

- **A sua mudança da rodada anterior entrou?** Em parte: *lido* em O desenho/P1, Sombra e log e Fases/4, entraram o HTTP 400, a política para texto sensível e a revisão de concordâncias; em Sugestão visível falta o replay comparativo que condicione o painel.
- **O que ainda está errado:** *lido* em Classificação dos usos e Sugestão visível, a ordem entra já apesar de M17 colocar casos importantes na cauda; *suposto*: a afirmação de que o erro custa só a ordem ignora ancoragem. Em Corpus e Linha zero, esclarecer que Haiku é rótulo provisório, e que política de dados e acesso antecedem gravação.
- **A pergunta que Anderson precisa responder:** *suposto*: qual política de retenção e acesso autoriza para os textos, incluindo dados sensíveis? Recomendo coleta mínima, acesso restrito e exclusão verificável antes da linha zero.
- **Autoavaliação:** *suposto, 85/100*: protegi os casos que somem na cauda e a evidência que pode vazar; aceitei uma sugestão reversível como hipótese, desde que demonstrado o benefício em comparação cega.

<!-- fim-rodada-4 -->

### Rodada 5: a confiança na v4

- **Posição:** A v4 corrige os bloqueios principais; retenção e limite de entrada ainda precisam de precisão.
- **Fatos lidos:** M3 revisto, M20 e o parecer do revisor independente sobre a v2.

| Parte do plano | Confiança na versão anterior | Confiança na versão atual | Uma linha de porquê |
| :------------- | :------------------------- | :------------------------ | :------------------ |
| **O plano inteiro** | 82 | 88 | *Lido*, O desenho e As fases: política antecede gravação, corpus entra na fase 0 e o painel espera replay; *suposto*: restam limites técnicos e de retenção a fechar. |

- **O revisor acertou ou errou onde?** *Lido*, `material/revisor-v2.md`, achados 1–5: acertou nas contradições de fases, catálogo, evidência do ranking, retenção e concorrência; a v4 as enfrenta. 93/100.
- **O que ainda está errado:** *Lido*, O desenho/Teto: ~5.000 caracteres é um resultado em texto real específico, não garantia de caber qualquer prompt; *suposto*: contar o prompt inteiro com tokenizer compatível ou tratar 400 explícito, sem descartar entradas apenas por esse número. Em A gravação, limpeza apenas ao escrever não garante prazo quando o sistema fica inativo; definir acesso, exclusão verificável e tratamento de falha no `finally` sem perder o veredito. 88/100.

<!-- fim-rodada-5 -->

## Custo da tarefa

Corrido 7 min — agente 5 min, quem pediu 3 min, pausa 0 s · US$ 2,48 (turnos 1,87, subagentes 0,61) · CPU 8,62 s do `claude` e 65,70 s dos comandos, RSS até 425 MB · 22 turnos, 1 sessão · dividida com 6 outros worklogs do commit · até 22:02 de 2026-11-09, pelo `brza note commit`
