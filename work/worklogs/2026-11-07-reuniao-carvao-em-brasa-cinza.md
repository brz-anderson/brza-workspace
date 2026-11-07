---
scope:
  - brza-studio
tags:
  - design
---

# Reunião Carvão em Brasa: a participação de Cinza, o Cético Analítico

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Cinza** — persona o Cético Analítico, no agente Codex —, aberto pela coordenação com
`brza sessions reuniao-brasa-cinza`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** manter `#1A1B1E` e separar a rampa de superfícies da rampa de texto; carvão não precisa ser marrom.
- **Por quê:** li o briefing e vi `material/brasa/brasa.png` (caminhos relativos a `.sessions/reuniao-brasa/`); recalculei 03/01 = 1,778:1 e `#BCBCBC`/01 = 9,068:1. Suposição: o discreto subtom frio não compromete a associação com carvão; não houve teste perceptivo.
- **Ideias:** (ousadia: baixa) `--text-secondary: #BCBCBC`, `--surface-base: #1A1B1E`, `--surface-raised: #2C2D31`; 03 fica para divisórias decorativas, sem carregar estado sozinha.
- **Ideias:** (ousadia: média) tema claro “cinza mineral”: `--surface-base: #FAF8F5`, `--text-primary: #2C2D31` (12,975:1) e `--brand-text: #A83E15` (5,887:1); 04 vira pigmento decorativo, sem obrigação de ligar duas rampas.
- **Risco:** o claro pode parecer bege; os pares propostos não validam automaticamente bordas, estados ou todos os textos.
- **Confiança:** 88/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** aceitar 07 como preenchimento com texto 01, rejeitar branco nos botões 06/07 e preservar semântica redundante por ícone e texto.
- **Por quê:** medição própria: 01/07 = 4,854:1; branco/07 = 3,548:1; branco/06 = 4,436:1; 07/02 = 3,877:1. Fonte de cores: `briefing.md`. Suposição: menos acentos simultâneos tornam a prioridade mais legível; não medi atenção.
- **Ideias:** (ousadia: baixa) `--action-primary-bg: #FF3D00` e `--action-primary-fg: #1A1B1E`; código em linha usa texto neutro, sem herdar 07 como texto de marca.
- **Ideias:** (ousadia: média) experimentar `--status-error-fg: #FF75A0` (6,810:1 na 01), sempre com ícone e descrição; manter aviso `#eab308`. A troca de erro é hipótese, não solução demonstrada para daltonismo.
- **Risco:** rosa pode continuar confundindo; 06/02 dá apenas 3,100:1 sem transparência, portanto o botão Parar a 14% precisa de medição do composto real.
- **Confiança:** 91/100

#### 3. O símbolo

- **Posição:** escolher A como tratamento principal e uma variante monocromática simplificada em 16 px e no tray.
- **Por quê:** abri `material/brasa/simbolo/{A,B,C}.png`: A dispensa as fagulhas de C e o halo central forte de B; nos exemplos de 16 px não consigo confirmar leitura de circuito e `{}`. Suposição: continuidade da silhueta vale mais que a metáfora física; não medi reconhecimento.
- **Ideias:** (ousadia: baixa) A em 32/64 px, sem depender de brilho para definir a borda; tray em máscara monocromática adaptada ao sistema, sem tile colorido.
- **Ideias:** (ousadia: alta) em 16 px retirar nós internos e preservar chama + uma abertura central; comparar com o símbolo atual a 1× e 2×, em claro/escuro, sem ampliar o estímulo para o participante.
- **Risco:** simplificar pode apagar justamente o diferencial tecnológico; A ainda pode parecer fogo genérico. Não alego que a miniatura já passou.
- **Confiança:** 62/100

#### 4. A brasa viva na interface

- **Posição:** Enviar neutro em repouso, brasa com foco e conteúdo enviável; movimento apenas enquanto há trabalho ativo.
- **Por quê:** vi `material/brasa/chat/brasa-chat-7-composer.png` e `brasa-chat-8-avisos.png`: Enviar e Continue competem com erro e anel quente. Suposição: reservar calor para ação disponível melhora a hierarquia; os PNGs não demonstram esse ganho nem comportamento de teclado.
- **Ideias:** (ousadia: baixa) `--focus-ring: #FF3D00`, contorno sólido de 2 px; sobre 02, contraste calculado de 3,877:1. Verificar visibilidade e recorte no app; glow não substitui contorno.
- **Ideias:** (ousadia: média) `--motion-ember-period: 2400ms` apenas na chama de trabalho; com redução de movimento, ícone estático + “Trabalhando”. Pergunta pendente recebe texto e contorno estático; hover usa superfície, sem fagulhas.
- **Risco:** depender do foco pode esconder Enviar de quem usa ponteiro; preservar forma, rótulo acessível e indicação de disponibilidade, e medir descoberta da ação.
- **Confiança:** 74/100

#### 5. Narrativa, voz e rollout

- **Posição:** “Carvão em Brasa” orienta a identidade; a microcópia informa estado e ação sem metáfora térmica obrigatória.
- **Por quê:** `briefing.md` define mini-rebranding e quatro filhas existentes; não fornece linha de base de uso ou evidência de associação emocional. Suposição: clareza operacional importa mais que repetir o conceito em cada mensagem.
- **Ideias:** (ousadia: baixa) voz “Trabalhando”, “Aguardando sua resposta” e “Falha ao enviar. Tentar novamente”; tokens primitivos `--ember-07` alimentam tokens funcionais como `--action-primary-bg`, sem chamar erro de brasa.
- **Ideias:** (ousadia: média) rollout reversível: matriz de componentes nos dois temas → uso interno → expansão; comparar tarefas de enviar, parar e reconhecer erro com a versão atual, em ordem alternada.
- **Ideias:** (ousadia: alta) piloto de marca em tons de cinza: retirar a cor e testar se ação, foco, erro e espera continuam identificáveis por forma e texto.
- **Risco:** amostra interna pequena superestima clareza; não vender ausência de reclamações como sucesso.
- **Confiança:** 82/100

Métricas propostas, ainda sem coleta: nenhum par de texto normal abaixo de 4,5:1 e nenhum indicador funcional aplicável abaixo de 3:1; piloto com 10 participantes, pelo menos 9/10 identificando erro e ação de envio sem ajuda. Tempo mediano de envio não deve piorar mais de 10% frente à versão atual; esses limites são suposições de aceite, não significância estatística.

#### A ideia mais ousada desta rodada

Submeter a interface inteira a um piloto sem cor antes de aprovar a brasa: se erro, foco e trabalho desaparecerem, a cor estava escondendo uma falha de estrutura. Depois devolver o calor. Risco: o ensaio subestima a contribuição emocional da marca; não serve para escolher a paleta mais memorável.

#### Issues candidatas

- **Separar tokens de texto, superfície e marca nos dois temas** — a 03 entrega apenas 1,778:1 sobre a 01 — prioridade `high`
- **Auditar contraste dos estados compostos de ação e foco** — transparência, código em linha e Parar exigem o fundo efetivo — prioridade `high`
- **Validar erro, aviso e marca com redundância semântica** — rosa novo não comprova distinção perceptiva — prioridade `high`
- **Comparar A e a variante pequena em tamanho real** — circuito e chaves ainda não têm reconhecimento demonstrado — prioridade `medium`
- **Medir o rollout reversível contra a interface atual** — definir linha de base antes de atribuir ganho ao rebranding — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Manter 01; texto e tema claro têm rampas próprias. | 88 |
| 2. Brasa | 07 com texto escuro; erro redundante, rosa experimental. | 91 |
| 3. Símbolo | A principal; variante simples e monocromática pequena. | 62 |
| 4. Interface | Calor seletivo; foco sólido e movimento só no trabalho. | 74 |
| 5. Narrativa e rollout | Voz literal, tokens funcionais e piloto reversível medido. | 82 |

Medição reproduzível nesta sessão: `python3 -` com sRGB linearizado (`c/12.92` se `c ≤ 0.04045`; senão `((c+0.055)/1.055)^2.4`), luminância `0.2126R + 0.7152G + 0.0722B` e razão `(Lmaior+0.05)/(Lmenor+0.05)`. Entradas HEX estão em cada par acima; imagens vistas são evidência visual, não medição de seus pixels. APCA, ΔE e simulações de daltonismo não foram executados; nenhuma conclusão perceptiva depende de fingir esses resultados. As posições são recomendações da persona, não decisões confirmadas de Anderson.

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

Li as rodadas 1 de Tição, Lenha, Fogareiro, Fole e a minha; Faísca ainda não tinha rodada 1 na leitura. Fonte dos ΔE e contrastes novos: `.sessions/reuniao-brasa/sintese-1.md`, “Fatos novos”; não reproduzi CIEDE2000/Machado. Distância simulada indica risco, não taxa de confusão humana; o corte aproximado de 15 não é garantia universal.

- **D1:** a — manter `#1A1B1E`; Tição calcula 4,85:1 contra 4,89:1 no carvão quente, diferença sem ganho funcional demonstrado. Suposição mantida: a base atual comporta a identidade sem aquecimento — 89/100.
- **D2:** b — aceitar `#A8A29E`: 6,83:1 na 01 e 5,45:1 na 02, segundo a síntese. Fole demonstrou alternativa quente com margem sobre 4,5; suponho melhor hierarquia, sem alegar mais conforto — 82/100.
- **D3:** b — adotar provisoriamente `#FF75A0`, com ícone e mensagem: ΔE deuteranopia 22,4 contra 10,3 do erro atual, e 6,81:1 na 01. Simulação fortalece a escolha; reconhecimento real segue pendente — 94/100.
- **D4:** c — experimentar `#FACC15`: ΔE deuteranopia 17,3 contra 12,1 do aviso atual e 13,7 de `#F5B841`. Retiro meu “manter aviso”; distinção em visão normal não resolve a disputa — 87/100.
- **D5:** b — B principal, sem halo em ≤32 px; Tição e Lenha me convenceram a concentrar o tratamento no símbolo e manter o tile grafite. A não tinha vantagem de reconhecimento medida; B tampouco tem. Pequeno chapado e tray monocromático permanecem — 70/100.
- **D6:** a — só respiração e término em 600 ms, sem animação com redução de movimento; adoto de Lenha halo decorativo animado, glifo e texto constantes. Não há benefício demonstrado para fagulhas ou mudança por horário — 86/100.
- **D7:** a — estados literais; “Em brasa” não distingue iniciar, executar e aguardar. Suposição: metáfora pode servir à comunicação da marca, mas não deve carregar estado operacional — 89/100.
- **D8:** d — teste de 5 s com e sem Claude, ordem alternada, antes de deslocar a 07. ΔE 11,8 sinaliza proximidade, não prova atribuição errada; manter a cor como candidata até medir — 92/100.
- **D9:** outra: c como ensaio curto, depois a com gate — auditoria dos pares → piloto cinza/colorido → flag reversível por duas semanas. O prazo de Fole é janela de observação; virar padrão depende dos resultados, nunca só do calendário — 89/100.

#### Os ataques

1. **Lenha — erro mantido (R1, assunto 2):** economia de escopo perdeu força com ΔE deuteranopia 10,3 do atual contra 22,4 do rosa (síntese). Ícone e texto continuam obrigatórios, mas não justificam conservar uma pista cromática mais ambígua. Derrubaria meu ataque: ensaio com usuários com deficiência de visão de cores mostrando reconhecimento equivalente ou pior com rosa, nos fundos reais e com igual redundância.
2. **Fogareiro — modo noturno adaptativo (R1, ideia ousada):** trocar HEX por horário não demonstra conforto nem mede “comprimento de onda irritante”. Recalculei em `python3 -`, pela fórmula sRGB da R1: luminância relativa 07 = 0,245975 e `#E05A20` = 0,232639, redução de 5,4%; contraste na 01 cai de 4,854 para 4,636. Isso não mede emissão do display ou fadiga. Derrubaria meu ataque: comparação controlada em sessões longas, com preferência explícita e ganho de conforto sem perda de desempenho ou contraste.

#### A concessão

- **Fole, rampa quente:** abandono `#BCBCBC` como secundário padrão por `#A8A29E`; os contrastes nos dois fundos sustentam a concessão. Não compro a alegação de conforto ou exclusividade de mercado.
- **Tição e Lenha, símbolo B:** viro de A para B pela disciplina de manter o tile grafite e simplificar os pequenos; confiança limitada a 70 porque leitura rápida ainda não foi testada.
- **Lenha, interface:** Enviar acende por disponibilidade, inclusive sem foco; retiro foco como condição de acendimento. Aceito seu anel neutro separado (`#BCBCBC` no escuro, `#1A1B1E` no claro), sujeito aos pares reais, e respiração só no halo do painel ativo.

#### "Sim, e…"

- **Sobre a brasa única de Lenha** (ousadia: média): matriz com 1, 4 e 8 painéis trabalhando; só o ativo respira, os demais mantêm glifo estático e texto. Medir tempo para localizar trabalho e pergunta pendente; “uma brasa” limita animação, sem esconder estados simultâneos.
- **Sobre o teste de 5 s de Fole** (ousadia: alta): separar associação espontânea (“o que lembra?”) de atribuição (“de qual produto é?”), com símbolo isolado, wordmark e tela com Claude. Alternar ordem e registrar contagens por condição; “quente” não prova reconhecer BrzA, e cinco pessoas não prometem significância.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | 01 mantida; secundário quente `#A8A29E`, rampas separadas. | 88 | 82 | ajustou | Fole e contrastes da coordenação |
| 2. Brasa | Rosa frio e aviso limão; redundância e validação perceptiva. | 91 | 90 | ajustou | Coordenação; risco Claude levantado por Fole |
| 3. Símbolo | B principal; pequeno chapado; tray template. | 62 | 70 | virou | Tição e Lenha |
| 4. Interface | Enviar por disponibilidade; foco neutro; só halo ativo respira. | 74 | 86 | ajustou | Lenha e Tição |
| 5. Narrativa e rollout | Voz literal; ensaio cinza, flag e gates por resultado. | 82 | 89 | ajustou | Fole e matriz de QA de Lenha |

<!-- fim-rodada-2 -->

### Rodada 3: voto final

#### O voto em cada proposta

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | Manter os fundos; nenhuma vantagem funcional medida justifica aquecer o canvas. | 90 |
| P2 | contra | Placeholder habilitado também precisa de 4,5:1: usar `#A8A29E`; 3,74 só em desabilitado, 03 decorativa. | 96 |
| P3 | apoio com ressalva | Rosa candidato nos dois temas; diff usa sinais −/+ e estrutura, com contraste sobre fundos reais. | 94 |
| P4 | apoio com ressalva | No claro, corpo/ícone em carvão com “Aviso”; tint decorativo não resolve sozinho colisão ou contraste do ícone. | 91 |
| P5 | apoio com ressalva | Token próprio essencial; lint verifica uso, mas cota por região exige renderização, incluindo ações simultâneas e overlays. | 98 |
| P6 | apoio com ressalva | `#FFB088` no escuro; no claro, tinta própria ≥4,5:1; medir também o fundo composto da caixa inline. | 92 |
| P7 | apoio com ressalva | B candidata, sem prova de reconhecimento; cobrir 33–63 px sem halo e testar 13/16/32 px reais a 1×/2×. | 76 |
| P8 | contra | Adiar: tray template segue mono; painel reflete seu agente, Dock/tray resumem todos, sem apagar enquanto houver trabalho. | 87 |
| P9 | apoio | Incluir anexo válido; validar anel contra ambos os lados e preservar nome acessível da ação. | 97 |
| P10 | contra | Trocar 05 nos painéis não focados (2,8:1 na 01) por sinal ≥3:1; só halo decorativo respira, glifo/texto constantes. | 95 |
| P11 | apoio com ressalva | Voz literal; conferir strings reais antes de corrigir “Ask Claude…”: Faísca distinguiu artboard de código não aberto. | 93 |
| P12 | apoio com ressalva | Base clara candidata; ícone 07 depende do fundo efetivo e dos estados, não só do papel. | 90 |
| P13 | contra | Qualquer atribuição à Claude abre investigação; incluir marca atual como controle, corrigir conforme achados e repetir, sem prescrever só “papel”. | 91 |
| P14 | contra | Manter portões; ΔE é triagem, não garantia; CI cinza verifica render/contraste, acompanhado de revisão de redundância e tarefas; corrigir P2/P10. | 96 |
| P15 | contra | Separar associação de atribuição; registrar contagens/tempos contra a base e desconforto perguntado; zero queixas não prova conforto, 5 pessoas não validam a população. | 94 |

#### O que me faria mudar de ideia

- **P5 (98):** demonstrar no catálogo real que `--primary` já é contrato exclusivo da marca, sem sobrescritas conflitantes, retiraria a necessidade do token separado; prioridade indevida de Allow/Submit ou contraste insuficiente reprovam a aplicação.
- **P9 (97):** comparação controlada com mais tentativas frustradas ou demora para descobrir Enviar, sobretudo com anexos, derrubaria o acendimento por disponibilidade; anel recortado ou sem contraste reprova a execução.

#### A última ideia

**Teste de “brasa presa”** (ousadia: média): interromper, cancelar, desconectar e restaurar sessões com vários agentes; comparar texto e sinal no painel/Dock/tray. Nenhum indicador continua “trabalhando” após confirmação do término; desconexão não significa ociosidade confirmada. Medir divergências e latência; supor meta inicial ≤1 s após evento recebido, a calibrar no protótipo.

#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Tição | Continuidade do símbolo/tile e auditoria cinza permanente, que ainda exige verificação semântica. | 8 |
| Faísca | Cascata de `--primary`, diff removido e cópia dos artboards; distinguiu leitura e suposição na R1, sua R2 estava ausente. | 9 |
| Lenha | Pares efetivos, anel neutro e halo separado do glifo tornaram o piloto verificável. | 9 |
| Fogareiro | Trouxe sessões longas e controle de movimento; certezas sobre conforto e percepção excederam a evidência. | 5 |
| Fole | Proximidade com Claude e regra prévia de teste; a solução não deve ficar predeterminada. | 8 |

#### Autoavaliação

Fui fiel ao separar cálculos, simulações e hipóteses; novos números vêm da `sintese-2.md`, sem reprodução minha. Li as R2 disponíveis dos colegas; preferi B pela manutenção do sistema, com confiança menor, sem ganho perceptivo medido. Não executei APCA nem teste humano; os votos são recomendações, e suponho que todo sinal necessário à tarefa exija contraste e redundância.
<!-- fim-rodada-3 -->

### Rodada 4: entrega — auditoria dos tokens v1

Medi 182 pares/estados e 20 comparações de sinais no script auxiliar abaixo, sem dependências. Hipótese: campos e caixas inline opacos sobre canvas/elevada; hover 05 a 22%/12%, mistura sRGB sem arredondamento intermediário. Não são pixels do app. Limites WCAG: texto normal ≥4,5:1; indicador funcional ≥3:1; decorativo e efetivamente desabilitado sem aprovação funcional. APCA 0.0.98G local: Lc assinado no JSON; tabela mostra menor magnitude nos quatro fundos, sem aprovação tipográfica automática.

#### Tabela preenchida e correções propostas

WCAG/Lc são mínimos em canvas, elevada e hover de ambos, salvo indicação. E/C = escuro/claro. Correções são propostas; nenhum token do app mudou.

| Papel | Escuro | Claro | WCAG mínimo E/C | APCA mínimo absoluto E/C | Veredito/condição |
| :---- | :----- | :---- | :------------- | :---------------------- | :---------------- |
| Canvas | `#1A1B1E` | `#F6F1EC` | — | — | Referências. |
| Elevada | `#2C2D31` | `#FFFFFF` | 1,25/1,12 contra canvas | 0/0 | Passa como superfície; não basta como limite funcional. |
| Divisória/inativo | `#454446` decorativo; `#8E8C90` funcional | `#D9D1C9` decorativo; `#82776D` funcional | 3,62/3,27 funcionais | 34,15/51,29 | Separar tokens; decorativo não identifica controle habilitado. |
| Primário | `#E8E2DC` | `#1A1B1E` | 9,39/12,88 | 82,88/85,13 | Passa. |
| Secundário | `#A8A29E` | `#5C5650` | 4,79/5,41 | 45,67/66,16 | Passa WCAG; não certifica qualquer tipografia por APCA. |
| Placeholder | **`#A8A29E`** | **`#625C56`** | 4,79/4,93 | 45,67/63,67 | Preenche claro e corrige escuro no hover. |
| Desabilitado | `#7A746F` | **`#9C938B`** | 2,62/2,26 | 22,83/37,94 | Exceção só se realmente desabilitado; reprova texto normal. |
| Ação fundo/rótulo | `#FF3D00` / `#1A1B1E` | idem | 4,85/4,85 rótulo/fundo | 40,87/40,87 | Passa WCAG; no hover claro, exigir contorno funcional. |
| Ícone ativo/contexto | `#D84315`; hover `#FF3D00` | `#A83E15` | 3,10 base e 3,40 hover / 4,67 | 27,67 base e 33,62 hover / 61,23 | 06 não passa em todo hover escuro. |
| Hover sutil | 05 a 22%: `#39231C`/`#47312B` | 05 a 12%: `#EDDCD2`/`#F5E8E3` | 1,14/1,19 contra base | — | Só decorativo; estado necessário exige forma/contorno. |
| Brasa textual | **`#FFB088`** | `#A83E15` | 6,79/4,67 | 63,30/61,23 | Passa; não herdar 07 como texto. |
| Foco de teclado | `#BCBCBC`, 2 px + offset 2 px | `#1A1B1E`, 2 px + offset 2 px | 6,36/12,88 contra superfícies | 59,51/85,13 | Offset revela superfície entre anel e ação; conferir recorte. |
| Erro/diff removido | `#FF75A0` | **propor `#6E3C5A` em vez de `#B4235A`** | 4,77/6,39 | 46,17/70,18 | Contraste passa; correção clara motivada por ΔE, com − e texto. |
| Aviso | `#FACC15` | texto/ícone `#1A1B1E`; tint `#FACC15` a 12% | 7,88/14,70 no tint | 71,98/93,42 no tint | Forma e rótulo “Aviso” no claro; sem ocre semântico. |
| Link | `#79C0FF` | **`#005EA8`** | 6,21/4,96 | 58,43/63,11 | Passa; sublinhado diferencia do texto sem depender da cor. |
| Código inline | `#FFB088` | **`#1A1B1E` neutro** | 6,79/12,88 | 63,30/85,13 | 05 clara também passa: 5,56/6,24 no papel/branco; neutro tem mais margem. |
| Chama foco/sem foco | degradê decorativo / `#8E8C90` | degradê decorativo / **`#625C56`** | Sem foco 3,62/4,93 | 34,15/63,67 | Funcional exige glifo sólido independente: ativo acima. |
| Trabalhando sem foco | 06 base; 07 no hover | 05 parada | 3,10 base e 3,40 hover / 4,67 | — | Glifo/texto constantes; só halo decorativo anima. |

#### ΔE2000 entre sinais

Machado 2009, severidade 1, RGB linear com clipping; Lab D65; kL=kC=kH=1. Ação = preenchimento 07; aviso claro = tinta neutra do ícone/texto. Distâncias das cores não modelam área ou forma. ΔE <15 é triagem, não decreto de indistinguibilidade humana.

| Tema/par | Normal | Deuteranopia | Protanopia | Tritanopia |
| :------- | -----: | -----------: | ---------: | ---------: |
| E erro/aviso | 56,43 | 25,96 | 40,81 | 19,27 |
| E erro/ação | 28,82 | 22,39 | 35,97 | 15,71 |
| E erro/link | 46,41 | 30,85 | 18,78 | 73,45 |
| E aviso/ação | 43,23 | 17,27 | 30,49 | 28,28 |
| E aviso/link | 59,55 | 56,76 | 53,06 | 44,88 |
| E ação/link | 53,28 | 54,51 | 55,10 | 65,07 |
| C erro corrigido/aviso | 25,70 | 17,26 | 16,30 | 25,56 |
| C erro corrigido/ação | 39,56 | 43,75 | 38,72 | 28,07 |
| C erro corrigido/link | 30,42 | 19,01 | 16,48 | 49,78 |
| C aviso/ação | 49,53 | 52,94 | 38,04 | 44,69 |
| C aviso/link | 30,19 | 29,19 | 31,45 | 30,56 |
| C ação/link | 51,90 | 62,62 | 51,62 | 66,64 |
| C erro v1 `#B4235A`/07 | 31,04 | 26,23 | 34,83 | **14,10** |
| C erro v1 `#B4235A`/05 textual | 24,49 | 15,38 | 29,61 | **3,14** |
| C erro corrigido/05 textual | 29,13 | 31,04 | 33,05 | **15,99** |

#### Reprovações e correções

- Placeholder v1 `#99938E`: 4,5314:1 na elevada escura, mas **3,9769:1 no hover**; substituir por `#A8A29E`. Claro definido como `#625C56`, mínimo 4,9326.
- 06 no hover elevado escuro: **2,7209:1**; usar 07 nesse estado. 05 como sinal escuro dá 2,7593/2,2039 na base/elevada; não sustenta glifo funcional.
- Ação 07 contra hover claro: **2,6536/2,9563:1**; contorno `#82776D` tem mínimo **3,2666** contra as superfícies. Validar lado externo; não alego contraste 3:1 entre contorno e preenchimento.
- Anel escuro em contato com 07: **1,8680:1**; offset de 2 px na superfície auditada evita contato. Branco/07 = 3,5476 e branco/06 = 4,4365: reprovam rótulo normal.
- Divisória v1 clara: **1,3448/1,5093** no papel/branco; escura: **1,7781/1,4202**. Reprovam como único limite/ícone necessário; usar bordas funcionais da tabela quando exigidas.
- Tint de hover e elevada não chegam a 3:1 contra base; reprova se forem a única pista funcional. Degradê tem trechos abaixo de 3:1; não aprovo glifo funcional sem base sólida ou redundância verificada.
- Erro claro v1 passa WCAG, mas **falha na triagem de tritanopia** contra 07 e 05; `#6E3C5A` veio de busca local e foi rechecado contra os sinais nas quatro visões, incluindo 05. É alternativa para teste, sem garantia perceptiva.
- APCA alerta para rótulo da ação (Lc **+40,87**) e secundário escuro (mínimo **−45,67**); WCAG aprovado não certifica Geist 14 px/peso. Avaliar tamanho, peso e render real.

#### Reprodução

```bash
python3 -B ".sessions/reuniao-brasa/entregas/cinza-audit-tokens.py"
```

JSON lista cada par, HEX composto aproximado, WCAG arredondado a quatro casas (veredito usa precisão integral) e Lc assinado. Autochecagens executadas: preto/branco 21:1; APCA preto/branco +106,04 e inverso −107,88; três referências CIEDE2000 de Sharma (2,0425; 2,8615; 3,4412). Machado reproduz 22,4 e 17,3 da coordenação; confere implementação, não percepção humana.

#### O que ficou de fora e por quê

Sem extração de pixels/computed styles: outras transparências, caixa inline real, fundos do diff, gradientes completos, antialiasing e temas personalizados não estão aprovados. Script conserva reprovações para comparar v1/correção; JSON não libera CI. Tray/Dock seguem pendentes de Anderson. APCA local não foi confrontado com pacote oficial nesta rodada.

**Confiança na peça:** 91/100

<!-- fim-rodada-4 -->

## O que ficou

## Fora do workspace

Nada.
