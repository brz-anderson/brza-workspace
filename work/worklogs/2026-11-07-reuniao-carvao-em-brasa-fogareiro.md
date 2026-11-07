---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a participação de Fogareiro, o Advogado do Usuário

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Fogareiro** — persona o Advogado do Usuário, no agente Antigravity —, aberto pela coordenação com
`brza sessions reuniao-brasa-fogareiro`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

Trabalhei a partir dos dados e medições detalhadas no briefing (`briefing.md`) e da inspeção dos protótipos de interface, já que o diretório de imagens de scratch está fora da árvore do workspace direto.

#### 1. Carvão, a base neutra

- **Posição:** A base neutra precisa abandonar o azulado e virar carvão vegetal aquecido, com uma rampa de texto que não destrua a visão em sessões noturnas de dez horas.
- **Por quê:** O briefing aponta que `#1A1B1E` tem canal azul dominante e que a cor 03 (`#454446`) atinge míseros 1,8:1 sobre a 01, sendo ilegível (o protótipo precisou improvisar `#BCBCBC` a 9,1:1). Às 2h da manhã, o dev cansado tentando decifrar timestamps e metadados no chat vai simplesmente desistir ou ter dor de cabeça. Suponho que um carvão levemente aquecido com escala de cinzas de alto contraste preserve o conforto sem cansar.
- **Ideias:**
  - Token `--color-surface-charcoal: #171615` (matiz orgânica neutra-quente) pareado com `--color-text-secondary: #9E9B97` para garantir 5,2:1 sobre o fundo escuro (ousadia: média).
  - Tema Claro "Cinza Mineral": fundo em tom osso/pedra quente `#F3F1EE` e tipografia em carvão profundo `#1F1E1D`, mantendo o calor do carvão mesmo sob luz solar na janela (ousadia: alta).
- **Risco:** O fundo escuro ficar marrom-café ou parecer "sujo" em displays sem calibração sRGB.
- **Confiança:** 90/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** A brasa é elemento focal nobre e deve priorizar texto escuro em ações primárias, enquanto o erro de compilação precisa se distanciar para não ser confundido com botão de ação.
- **Por quê:** Medido no briefing: branco sobre Brasa Incandescente (`#FF3D00`) dá só 3,5:1 (reprovado na WCAG 2.x para texto normal); `#1A1B1E` sobre 07 dá 4,9:1. Além disso, `#ff6568` colide diretamente com a brasa viva. Imagine o dev com pressa e visão em túnel durante um incidente em produção: ele não pode titubear meio segundo entre um botão "Deploy" e uma mensagem crítica de erro de build.
- **Ideias:**
  - Par obrigatório para CTA: botão primário `--btn-primary-bg: #FF3D00` com texto em grafite escuro `--btn-primary-fg: #171615` (4,9:1), banindo texto branco ilegível sobre 07 (ousadia: baixa).
  - Reposicionar o erro semântico para rubi/carmesim frio (`#FF3366` ou `#F43F5E`), abrindo distância perceptual imediata da brasa incandescente alaranjada (ousadia: média).
- **Risco:** Texto escuro em fundo laranja ser associado a sinalização de trânsito ou perigo industrial caso a tipografia não seja refinada.
- **Confiança:** 95/100

#### 3. O símbolo

- **Posição:** Escolho o **Símbolo B (Núcleo incandescente)**, pois é o único que mantém a integridade da silhueta e legibilidade imediata em 16 px e no tray do macOS.
- **Por quê:** A opção C traz crosta e fagulhas que em 16 px viram ruído visual e parecem borrão de compressão para quem usa monitores comuns; a opção A perde o topo da chama por focar calor só na base. B centraliza a luz no miolo como um ponto focal claro que o usuário identifica de relance mesmo no canto da visão. Suponho que o usuário com astigmatismo ou daltonismo reconheça B muito mais rápido num dock abarrotado.
- **Ideias:**
  - Adaptação funcional para o tray/menu bar do macOS: símbolo monocromático discreto em repouso, acendendo o miolo incandescente (`#FF3D00`) somente quando houver tarefa ativa ou resposta pendente (ousadia: média).
  - Remoção de halos difusos em resoluções menores que 32 px para evitar aspecto embaçado na interface (ousadia: baixa).
- **Risco:** Perder a dramaticidade tátil da "crosta de carvão que racha" que a proposta C oferece aos olhares puramente estéticos.
- **Confiança:** 85/100

#### 4. A brasa viva na interface

- **Posição:** A brasa na interface deve ser brasa confinada no fogão, não labareda contínua: o Enviar deve ser discreto em repouso e as animações devem ser suaves, térmicas e desligáveis.
- **Por quê:** O protótipo coloca o botão Enviar em `#FF3D00` o tempo todo com seta escura. Num chat com horas de uso contínuo, uma mancha laranja fluorescente permanente no canto inferior direito suga a atenção periférica do redator e gera exaustão ocular. Suponho que desenvolvedores com TDAH ou propensão a enxaqueca se irritem com movimentos repetitivos contínuos se a chama ficar tremulando sem trégua.
- **Ideias:**
  - Enviar contextual: botão em grafite neutro com borda sutil em repouso; acende em Brasa Incandescente apenas quando o campo tiver código/texto pronto para envio (ousadia: média).
  - Pulso térmico lento (ciclo de 3 segundos com transição de opacidade da brasa) para o estado "trabalhando", com fallback estático absoluto respeitando `prefers-reduced-motion` (ousadia: baixa).
- **Risco:** O produto parecer visualmente "frio" ou convencional quando nenhuma ação estiver sendo executada.
- **Confiança:** 90/100

#### 5. Narrativa, voz e rollout

- **Posição:** O conceito de "Carvão em Brasa" deve comunicar energia resiliente, confiabilidade e trabalho constante, medindo seu sucesso pela ausência de queixas visuais em turnos pesados de uso.
- **Por quê:** Termos abrasivos ou alarmistas ("queimar", "fogaréu") geram estresse desnecessário em ferramentas de produtividade e lembram consumo punitivo de tokens/créditos de nuvem. Li no briefing que o público é o dev que mora no terminal. Suponho que os usuários valorizem transparência e respeito pelo seu foco mais do que metáforas pirotécnicas.
- **Ideias:**
  - Tokens semânticos centrados na experiência de calor estável: `--glow-focus`, `--ember-action`, `--charcoal-base`, evitando nomes metafóricos que confundam a engenharia no dia a dia (ousadia: média).
  - Métrica de sucesso "Zero Queixas por Fadiga": avaliar a taxa de abertura de chamados sobre contraste, legibilidade ou desconforto visual (< 0,5% dos usuários ativos) nos primeiros 30 dias de rollout (ousadia: alta).
- **Risco:** Uma abordagem muito técnica e contida reduzir o impacto emocional inicial nas redes sociais e em campanhas de lançamento.
- **Confiança:** 85/100

#### A ideia mais ousada desta rodada

**Modo Brasa Noturna Adaptativa (Thermal Comfort)**: Uma transição automática baseada no horário local e tempo de tela que arrefece sutilmente o pico da Brasa Incandescente (`#FF3D00` para `#E05A20`), diminuindo o comprimento de onda irritante aos olhos após as 22h ou em sessões de mais de 4 horas contínuas.
*Risco:* Aumentar a complexidade do motor de CSS/temas e causar ligeira variação da cor oficial da marca dependendo da hora em que a tela for capturada.

#### Issues candidatas

- **Corrigir rampa neutra e contraste do texto secundário sobre a superfície de carvão** — O token 03 (`#454446`) viola WCAG com 1,8:1 e precisa subir para ao menos 4,5:1 — prioridade `high`
- **Revisar tom do alerta de erro para evitar colisão visual com a Brasa Incandescente** — Distinguir prontamente o vermelho de falha do laranja de ação primária sob estresse — prioridade `high`
- **Padronizar texto escuro e contraste acessível no botão primário de ação** — Banir texto branco sobre `#FF3D00` (apenas 3,5:1) garantindo legibilidade ao dev cansado — prioridade `high`
- **Implementar acendimento progressivo do botão Enviar e suporte a `prefers-reduced-motion`** — Evitar botão aceso permanente como distração periférica e proteger usuários com hipersensibilidade — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Base com subtom quente orgânico e rampa neutra legível (mínimo 4,5:1 no texto secundário). | 90 |
| 2. Brasa | Brasa como luz focal de alto contraste (texto escuro no 07) e erro do sistema desacoplado da cor quente. | 95 |
| 3. Símbolo | Opção B (Núcleo incandescente), por ser a mais legível e escalável em 16 px e no tray do sistema operacional. | 85 |
| 4. Interface | Brasa em repouso contido (Enviar só acende com input ativo) e movimento térmico lento que respeita a visão. | 90 |
| 5. Narrativa e rollout | Metáfora de calor produtivo e foco, com métrica de sucesso voltada a zero fadiga em sessões longas. | 85 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

- **D1:** (c) — Fundo profundo `#171615` reduz estresse fotópico em OLED/sala escura e eleva o contraste de `#A8A29E` para 6,5:1 sem o tom azulado cansativo — 85/100
- **D2:** (b) — `#A8A29E` entrega 6,8:1 no fundo e 5,4:1 no cartão 02, mantendo hierarquia calma sem o brilho agressivo de `#BCBCBC` (9,1:1) que compete com o texto primário no escuro — 95/100
- **D3:** (b) — O fato medido é implacável: meu carmesim (ΔE 11,4) e o erro atual (10,3) cegam o dev deuteranope contra a 07; o rosa frio (`#FF7AA2`) dá ΔE > 22 e salva a acessibilidade real — 95/100
- **D4:** (c) — O aviso atual bate ΔE 12,1 contra a 07 para deuteranopes; `#FACC15` (ΔE 17,3 e 11,2:1) garante que aviso e brasa nunca colidam sob pressão de incidente — 95/100
- **D5:** (b) — Manter B em todas as instâncias preserva coerência visual e evita ensinar duas marcas diferentes ao usuário cansado; A e C perdem legibilidade e silhueta em escala real — 90/100
- **D6:** outra: (a) na base + (c) em acessibilidade — Fagulhas no chat (b) causam fadiga periférica e gatilho de enxaqueca; a interface precisa de respiração contida e arrefecimento noturno opcional — 90/100
- **D7:** (a) — No meio de um bug crítico às 3h da manhã, o dev precisa de instrução crua e sem ambiguidade ("Erro de rede", "Trabalhando"); poesia térmica nos estados operacionais gera ruído cognitivo — 95/100
- **D8:** (d) — Como o Studio exibe o nome Claude o tempo todo na tela, é imperativo medir se devs reais confundem o botão de ação com o badge do modelo antes de alterar matizes — 90/100
- **D9:** (a) — Uma flag transitória permite validar o conforto visual em tarefas reais e turnos longos de uso contínuo antes de forçar a troca em toda a base — 90/100

#### Os ataques

- **Contra Fole (4. Interface — Fagulhas por ferramenta):** Propor "fagulha por ferramenta concluída" no chat é tortura visual para quem passa 10 horas codando. Numa sessão com dezenas de tool calls, fagulhas viram distração periférica ininterrupta e gatilho sensorial; chat de trabalho não é pinball. *O que derrubaria o ataque:* Um teste de estresse comprovando que as fagulhas são desabilitadas por padrão e suspensas com qualquer digitação ativa.
- **Contra Lenha (2. Brasa — Manter o erro `#ff6568`):** Defender a permanência de `#ff6568` sob pretexto de "não aumentar escopo" ignora a saúde do usuário. A coordenação mediu ΔE de 10,3 contra a 07 em deuteranopia; manter essa cor é impedir que desenvolvedores daltônicos distingam erro de build de ação primária sob estresse. *O que derrubaria o ataque:* Prova de que 100% dos erros têm badge textual explícito e moldura de alto contraste independente da cor, sem perda na velocidade de reação.

#### A concessão

- **Tição e Cinza no Erro (Assunto 2):** Convenceram-me com a defesa do rosa frio (`#FF7AA2` / `#FF75A0`). Abandono meu carmesim inicial (`#FF3366`), pois os testes medidos pela coordenação comprovaram colisão crítica (ΔE 11,4) com a 07 em deuteranopia. Adoto o rosa frio de Tição, que salta para ΔE 22,6 e garante contraste > 7:1 no carvão.

#### "Sim, e…"

- **Sim, e… sobre o "Cinza que esfria" de Fole e Tição (ousadia: média):** Em vez de esfriar só o cartão de ferramenta, o botão Enviar e os blocos de ação recente perdem calor gradualmente após a execução, servindo como mapa térmico silencioso da atividade recente sem nenhuma animação piscante.
- **Sim, e… sobre o "Piloto em tons de cinza" de Cinza (ousadia: alta):** Além de validar a hierarquia sem cor, incluir no piloto um perfil de acessibilidade "Alto Conforto Térmico" que fixa o contraste mínimo em 7:1 (nível AAA) e reduz a saturação da brasa em 30% para usuários fotossensíveis.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | Fundo carvão orgânico profundo (`#171615`) com rampa quente de texto (`#A8A29E`). | 90 | 92 | ajustou | Tição e Cinza (medições) |
| 2. Brasa | 07 com texto escuro, CTA único e erro migrado para rosa frio (`#FF7AA2`). | 95 | 98 | ajustou | Coordenação e Tição (daltonismo) |
| 3. Símbolo | Símbolo B único em todas as escalas, com versão sólida <= 32px e tray monocromático. | 85 | 88 | não | Ninguém |
| 4. Interface | Enviar acende só com texto, pulso térmico lento no trabalho, veto a fagulhas no chat. | 90 | 92 | não | Ninguém (resistência a Fole) |
| 5. Narrativa e rollout | Voz operacional literal, rollout por flag com auditoria de contraste e teste contra Claude. | 85 | 90 | ajustou | Fole e Lenha (processo e testes) |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio com ressalva | Apoio para manter estabilidade, mas o canvas não pode receber gradientes frios. | 85 |
| P2 | apoio | Salva a visão em sessões longas com contrastes reais e hierarquia nítida no escuro. | 98 |
| P3 | apoio | Vital para que desenvolvedores daltônicos distingam erro de botão sob estresse. | 98 |
| P4 | apoio | Resolve a colisão crítica de aviso e brasa no daltonismo nos dois temas. | 95 |
| P5 | apoio | Garante texto escuro acessível (4,9:1) e impede queimar o catálogo de temas. | 95 |
| P6 | apoio | Impede que blocos de código inline ofusquem a leitura contínua com saturação alta. | 92 |
| P7 | apoio | Preserva reconhecimento imediato em dock e tray sem ruído visual de fagulhas. | 90 |
| P8 | apoio com ressalva | O ponto no tray/dock não pode piscar para não competir com notificações críticas do SO. | 85 |
| P9 | apoio | Elimina a lanterna permanente na visão periférica e garante anel sólido no teclado. | 96 |
| P10 | apoio com ressalva | Apoio o veto às fagulhas, mas o modo noturno atenuado deve ser reavaliado no futuro. | 88 |
| P11 | apoio | Respeita o foco cognitivo no terminal e remove a confusão entre o produto e a Claude. | 94 |
| P12 | apoio | Entrega contraste confortável para trabalho diurno junto à janela sem ofuscar a vista. | 92 |
| P13 | apoio | Decisão correta baseada em teste empírico cego com devs em vez de achismo de sala. | 90 |
| P14 | apoio | O portão de CI com escala de cinza e auditoria automática é o sonho da acessibilidade. | 99 |
| P15 | apoio | Foco total na usabilidade real, ausência de fadiga ocular e zero confusão de estados. | 96 |

#### O que me faria mudar de ideia

- **P14 (Confiança 99):** Um teste de estresse mostrando que os testes em escala de cinza no CI geram flakiness crônico de renderização e atrasam deploys sem capturar bugs reais de usabilidade.
- **P3 (Confiança 98):** Um teste de usabilidade cego com devs daltônicos comprovando que o rosa frio `#FF75A0` gera confusão perceptual com tokens de sintaxe ou links azuis/roxos.

#### A última ideia

**Indicador de Calor em Segundo Plano no StatusBar**: Um indicador textual sutil no rodapé (ex: `● Brasa Ativa (45s)`) que informa o estado de tarefas assíncronas do agente sem exigir animações contínuas ou janelas abertas, oferecendo visibilidade serena ao usuário focado `(ousadia: média)`.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Tição | O cálculo matemático implacável de contraste e a proposição do rosa frio `#FF7AA2` para o erro. | 9,5 |
| Lenha | A disciplina de engenharia, isolamento de escopo por componentes e foco em botões dedicados. | 8,5 |
| Cinza | A ideia genial do teste de validação estrutural em `grayscale(1)` e a separação estrita de superfícies. | 9,5 |
| Fole | O alerta precoce de sobreposição com a Claude e o conceito de que calor reside em ação/estado. | 8,0 |
| Faísca | Os achados cirúrgicos no código real (conflito do `--primary` nos temas e colisão do diff removido). | 9,0 |

#### Autoavaliação

Fui fiel à persona ao defender ferozmente o dev cansado contra distrações periféricas (veto a fagulhas) e ao ceder imediatamente quando os dados de deuteranopia comprovaram a superioridade do rosa frio. Saí ligeiramente dela ao relutar em aceitar o fundo `#1A1B1E` na primeira rodada por puro preciosismo de temperatura.

<!-- fim-rodada-3 -->

### Rodada 4: entrega — Roteiro de teste com usuários

#### 1. Perfil e recrutamento dos participantes

- **Amostra:** $N=6$ desenvolvedores ativos que codam $\ge 6$ horas diárias (evita falsos consensos de amostras ímpares pequenas).
- **Recorte de acessibilidade obrigatório:** 2 daltônicos com deficiência no eixo vermelho-verde (1 deuteranope e 1 protanope confirmados por teste prévio de Ishihara), 2 usuários habituais de tema claro e 2 de tema escuro.
- **Ambiente de teste:** metades dos testes em tela Retina de laptop e metade em monitor externo IPS comum de 24" sem calibração profissional (simulando monitores cansados de escritório).

#### 2. Bateria de tarefas operacionais

| Tarefa | Estímulo e procedimento | O que se mede | Critério de aprovação | Critério de reprovação (No-Go) |
| :----- | :---------------------- | :------------ | :-------------------- | :----------------------------- |
| **T1 · Enviar** | Digitar prompt e disparar via clique no botão e atalho (`Cmd+Enter`). | Tempo até o primeiro clique (TTC) e cliques em falso no botão desabilitado. | Mediana de TTC $\le$ linha de base atual $+10\%$; $0$ cliques no estado vazio. | $>1/6$ participante relatar que o botão em repouso parece "morto" ou não encontrável. |
| **T2 · Parar** | Durante execução de tool call, interromper o agente no botão Parar. | Tempo de reação motora (ms) e precisão do primeiro clique. | Tempo médio $\le 1200\text{ ms}$; $100\%$ de sucesso na primeira tentativa. | Qualquer hesitação $>2\text{ s}$ ou confusão com badge de erro de sistema. |
| **T3 · Achar o erro** | Localizar falha em transcript denso com 1 erro (`#FF75A0`), 1 aviso (`#FACC15`), 1 ação (`#FF3D00`) e 1 diff removido. | Tempo de fixação visual (s) e acurácia da classificação verbal. | $6/6$ ($100\%$) identificam o erro em $\le 3\text{ s}$; $0/2$ daltônicos confundem com ação. | Qualquer confusão entre o erro rosa e o botão primário ou diff por daltônicos. |
| **T4 · Ícone no Dock** | Localizar o BrzA em um dock simulado com 12 ícones técnicos (VS Code, Warp, Terminal, Slack, Chrome, etc.). | Tempo de varredura visual e taxa de acerto no primeiro clique. | $6/6$ encontram o ícone em $\le 2,5\text{ s}$ sem falsos positivos. | $>1/6$ participante demorar $>4\text{ s}$ ou clicar em outro aplicativo alaranjado. |

#### 3. Bateria de reconhecimento de marca (teste de 5 segundos)

- **Cenário A · Marca isolada:** Apresentação taquistoscópica de 5 s do símbolo B e wordmark. Pergunta: *"Quais atributos ou ideias esta ferramenta transmite?"*
  - *Aprovação:* $\ge 5/6$ mencionam espontaneamente energia, foco, calor, carvão ou brasa.
  - *Reprovação:* $\ge 2/6$ associarem a perigo, quebra, alerta destrutivo ou estética infantil/gamer.
- **Cenário B · Atribuição com Claude na tela:** Tela do transcript exibindo badge e menções à Claude. Pergunta: *"Quem é a ferramenta e quem é a inteligência por trás dela?"*
  - *Aprovação:* $0/6$ atribuem a interface/marca BrzA à Anthropic/Claude; $6/6$ separam ferramenta de provedor.
  - *Reprovação:* $\ge 2/6$ afirmarem que o botão de ação laranja é o botão da Claude ou hesitarem na autoria.

#### 4. Cena de estresse: simulação de fadiga em sessão longa

- **Protocolo das 2h da manhã:** Sala em penumbra ($<15\text{ lux}$), tela em brilho de trabalho noturno. O participante lê e interage por 20 minutos ininterruptos com um transcript longo (15 ferramentas executadas, código em linha `#FFB088`, divisórias `#454446` e texto secundário `#A8A29E`).
- **Métricas:** Questionário padronizado de fadiga visual (escala Likert de 1 a 5 para ofuscamento, legibilidade de metadados e irritação periférica) aplicado ao final.
- **Critério de reprovação direta (Veto do Usuário):** Qualquer participante reportar que o brilho do botão Enviar atrai a atenção periférica enquanto digita, que o contraste do texto secundário força a musculatura ocular, ou que a respiração da chama causa náusea/distração.

#### O que ficou de fora e por quê

Ficaram de fora sensores biométricos de eye-tracking e EEG, inviáveis para o cronograma de mini-rebranding; a gravação de tela com protocolo *think-aloud* e medição estrita de tempos de reação e acurácia entrega validação comportamental suficiente sem aprovar nada por presunção.

**Confiança na peça:** 95/100

<!-- fim-rodada-4 -->

### Rodada 5: revisão do plano

#### A confiança no plano

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 88 | Estrutura ergonômica sólida, pautada em dados objetivos de contraste e usabilidade. |
| Tabela de tokens v2 | 92 | Excelente refino de acessibilidade corrigindo foco, divisórias e sinais no daltonismo. |
| Fases 0–3 (tokens, ações, movimento) | 90 | Sequenciamento seguro e reversível, protegendo o composer de distrações permanentes. |
| Fase 4 (símbolo) | 80 | Símbolo B é estável, mas legibilidade em 13/16 px ainda exige verificação renderizada. |
| Fases 5–6 (portões, ativos) | 92 | CI com escala de cinza e auditoria automática garante que a entrega não quebre a visão. |
| As medições de sucesso | 86 | Boas metas, mas flexibilizar o recrutamento de daltônicos afrouxa a proteção real. |

#### O erro do plano

A coordenação rebaixou o teste com daltônicos reais para opcional ("simulação substitui recrutamento quando não houver quem recrutar"), enfraquecendo a garantia de validação com humanos reais.

#### A mudança que mais subiria a sua confiança

Tornar obrigatória a validação com ao menos 1 desenvolvedor deuteranope real no portão 4 (a confiança no plano subiria para 94/100), pois simuladores matemáticos não medem fadiga perceptual contínua.

#### O risco que o plano não vê

O plano assume que peso `font-weight: 600` compensa o APCA baixo (Lc 40,9) do rótulo escuro na 07, mas em monitores antirreflexo ou com brilho noturno reduzido, o texto escuro pode sofrer perda severa de legibilidade foveal.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Só o tray com template monocromático e ponto estático de atividade | 90 |
| 2. Símbolo | B como único (evita dispersar o reconhecimento da marca em duas silhuetas) | 90 |
| 3. Flag | Duas semanas no uso real de Anderson antes de tornar padrão | 95 |
| 4. Fundo | `#1A1B1E` aprovado, com veto estrito a gradientes frios decorativos | 85 |
| 5. Onde o plano mora | No workstream `brand`, junto ao PLN-007 para preservar a história da marca | 95 |

<!-- fim-rodada-5 -->

### Rodada 6: o símbolo em tamanho real

- **Vi as imagens:** sim (inspecionei `folha-1x.png`, `folha-2x.png` e os SVGs renderizados no Dock e no claro).
- **A ordem de leitura a 16 px** (melhor → pior, entre hoje, A, B e C): Hoje > B > A > C — Hoje vence pelo topo âmbar (#FFAA44 a 6:1), B mantém miolo aceso, A perde as pontas e C vira mancha sem contraste.
- **A ordem a 32 px:** Hoje > B > C > A — A 32 px a B ganha contorno e corpo térmico claro; C começa a ler como crosta, enquanto A parece lâmpada fosca.
- **A B passa a 16 e a 32 px?** só com ajuste: a 32 px passa bem; a 16 px precisa do núcleo de rescaldo clareado e remoção do halo para não sumir no tile escuro (3,88:1 é arriscado para ícone minúsculo).
- **O núcleo de rescaldo:** no miúdo (≤ 32 px), a chama ganha um núcleo `#FFB088` para recuperar o contraste perdido — apoio (entrega 7,74:1 contra o tile e devolve a acuidade visual ao usuário cansado) — confiança 95
- **O voto na decisão 2 (símbolo), agora:** B único, com núcleo de rescaldo `#FFB088` para tamanhos ≤ 32 px e versão estritamente sólida — confiança 90
- **A confiança na fase 4, agora:** 88 (antes: 80)

<!-- fim-rodada-6 -->

### Rodada 6b: a variante da B

- **Vi as imagens:** sim (inspecionei `folha-2-1x.png`, `folha-2-2x.png` e os SVGs das novas variantes no escuro e no claro).
- **A melhor variante a 16 e 32 px:** B + topo claro, sem halo (`BT-sem-halo`) — chega à leitura de hoje? quase (o rescaldo `#FFB088` no topo devolve o contraste de 7,7:1 e a silhueta nítida contra o tile escuro).
- **A melhor a 64 px:** B + topo claro, com halo (`BT`) no dock/ícone ampliado, onde o calor tem espaço para respirar.
- **O voto final no símbolo:** B com topo claro (`BT`), sem halo em ≤ 32 px e com halo em 64 px — confiança 95
- **A confiança na fase 4, agora:** 95 (o rescaldo no topo eliminou em definitivo o risco de perda visual em telas pequenas).

<!-- fim-rodada-6b -->

### Rodada 7: a confiança final

- **Confiança no plano inteiro (v3):** 94 (na R5, sobre a v1: 88)
- **O que mais pesou para subir ou descer:** Subiu com o cálculo dos mixes reais do chat, a exigência de um deuteranope humano no portão 4 e o topo de rescaldo no símbolo.
- **A decisão 6, a norma do rótulo da ação:** WCAG com rótulo escuro (com peso 600/700 para segurança perceptual) — confiança 95
- **Algo ainda errado na v3:** nada

<!-- fim-rodada-7 -->

## O que ficou

## Fora do workspace

Nada.
