---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Lenha, a Engenheira Pragmática, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Lenha** — a Engenheira Pragmática —
no agente Codex, com o modelo `gpt-6.1-terra` e esforço `medium` (na reunião, gpt-6.1-sol medium). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** Adoto `#1A1B1E` como carvão neutro e resolvo texto e tema claro por tokens próprios.
- **Por quê:** O briefing mede 1,8:1 para 03 sobre 01 e 9,1:1 para `#BCBCBC` sobre 01; o azul domina ligeiramente no fundo. Suponho que aquecer superfícies pontuais basta para dar caráter sem tingir toda a tela.
- **Ideias:** `--surface-base: #1A1B1E` e `--text-secondary: #BCBCBC` no escuro (ousadia: baixa); no claro, experimentar `--surface-base: #F7F5F2` e texto `#1A1B1E`, com borda quente `#D8CEC8`, medindo os pares reais (ousadia: média).
- **Risco:** A base fria pode parecer grafite genérico; o claro proposto ainda não foi testado em componentes.
- **Confiança:** 85/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** Uso 07 com conteúdo escuro no CTA e separo erro e aviso da escala de marca.
- **Por quê:** O briefing informa 4,9:1 para 01 sobre 07, 3,5:1 para branco sobre 07 e 4,4:1 para branco sobre 06. Suponho que ícone e texto de erro, além da cor, preservam a distinção em telas densas.
- **Ideias:** `--action-primary: #FF3D00` com `--on-action-primary: #1A1B1E` (ousadia: baixa); testar `--status-error: #FF8095` com ícone e rótulo, e manter aviso amarelo distinto, medindo cada combinação no fundo final (ousadia: média).
- **Risco:** Rosa pode perder gravidade e o laranja constante competir com mensagens críticas.
- **Confiança:** 89/100

#### 3. O símbolo

- **Posição:** Escolho B, núcleo incandescente, com variante simplificada para tamanhos pequenos e tray.
- **Por quê:** Em `material/brasa/simbolo/B.png`, o núcleo comunica calor sem depender das fagulhas; na visão geral `brasa.png`, o detalhe de 16 px já fica diminuto. Suponho que o desenho simplificado preserva o reconhecimento, a validar no app.
- **Ideias:** manter B com halo apenas no ícone grande (ousadia: baixa); criar versão de 16 px com chama e circuito simplificados, e máscara monocromática para tray claro/escuro (ousadia: média).
- **Risco:** A simplificação pode apagar as chaves `{}`; renderizar e comparar em tamanho real antes de substituir os assets.
- **Confiança:** 76/100

#### 4. A brasa viva na interface

- **Posição:** Enviar fica laranja quando habilitado; foco e trabalho ganham sinais distintos e movimento discreto.
- **Por quê:** Em `material/brasa/chat/brasa-chat-7-composer.png`, repouso e foco já compartilham o botão laranja e a borda é o principal diferencial. O briefing aponta o contraste insuficiente do ícone Parar com 05; suponho que uma borda de foco externa mais clara evita depender só do brilho.
- **Ideias:** anel de foco de 2 px com cor validada contra superfícies adjacentes e seta escura no Enviar (ousadia: baixa); chama de trabalho pulsa lentamente e congela com `prefers-reduced-motion`, enquanto Parar usa ícone com contraste mínimo 3:1 (ousadia: média).
- **Risco:** Animação contínua distrai e o laranja em repouso enfraquece a percepção de foco; verificar teclado e estados desabilitados.
- **Confiança:** 83/100

#### 5. Narrativa, voz e rollout

- **Posição:** Lanço por tokens e componentes do chat, com voz direta e comparação visual antes de expandir.
- **Por quê:** O briefing limita o trabalho a um mini-rebranding e lista tema claro e escuro; suponho que uma troca reversível por tokens reduz o custo de corrigir o lançamento. Estimativa inicial, não medida: 1–2 dias para protótipo e auditoria do chat, sem contar revisão de assets.
- **Ideias:** nomes semânticos `--surface-base`, `--action-primary` e `--status-error`, com mapeamentos por tema (ousadia: baixa); microcópia “Preparando a resposta…” e chama que aquece durante trabalho, sem metáfora em erros (ousadia: média).
- **Risco:** Tokens não cobrem cores fixas e a estimativa pode crescer; auditar ocorrências e capturas antes de expandir.
- **Confiança:** 80/100
- **Métrica:** 100% dos pares de texto e ícones ativos alterados passam, respectivamente, 4,5:1 e 3:1 nos fundos reais; comparar capturas dos oito estados nos dois temas e registrar regressões antes/depois.

#### A ideia mais ousada desta rodada

A chama de trabalho começa como carvão e acende progressivamente enquanto a tarefa está ativa, sem sugerir porcentagem de progresso; ao terminar, esfria uma vez. Risco: parecer indicador de progresso ou distrair; oferecer movimento reduzido e testar a interpretação.

#### Issues candidatas

- **Mapear tokens e contraste nos dois temas** — inventariar pares reais, inclusive código em linha e Parar, antes da migração — prioridade `high`
- **Separar marca de erro e aviso** — validar cor, ícone e texto em estados adjacentes — prioridade `high`
- **Preparar símbolo B para 16 px e tray** — testar legibilidade em ambos os fundos e máscara monocromática — prioridade `medium`
- **Validar foco, movimento reduzido e Enviar** — comparar estados por teclado e capturas dos oito cenários — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Base 01, texto legível e tema claro com tokens próprios. | 85 |
| 2. Brasa | CTA 07 com conteúdo escuro e estados semânticos separados. | 89 |
| 3. Símbolo | B com variantes simplificada e monocromática. | 76 |
| 4. Interface | Enviar laranja, foco distinto e movimento respeitando preferência. | 83 |
| 5. Narrativa e rollout | Migrar por tokens, medir contraste e comparar estados. | 80 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 79 | Fases reversíveis e saída para o símbolo; o contraste configurável ainda deixa uma falha. |
| Tabela de tokens | 81 | Separa origem de cor efetiva, mas há pares claros e fundos reais ainda a medir. |
| Fases 0–3 (tokens, ações, movimento) | 86 | A composição inline e a flag enfrentam o custo real de integração; horas são estimativas. |
| Fase 4 (símbolo) | 78 | Preview nativo e fallback integral reduzem risco; leitura pequena ainda depende do teste. |
| Fases 5–6 (portões, ativos) | 76 | Auditor e reversão são concretos; recrutamento e empacotamento ainda carregam incerteza. |
| As medições de sucesso | 70 | Cinco pessoas dão sinal inicial, não precisão estatística; o contraste abaixo do padrão ficou fora do aceite. |

#### Onde a proposta diverge da sua rodada 1

- Defendi simplificar a chama e o circuito em 16 px; a proposta mantém um traçado e prevê fallback integral. Convenceu: evita duas leituras e testa a legibilidade antes da troca.
- Sugeri a chama aquecer progressivamente durante o trabalho; a proposta limita a respiração ao halo focado. Convenceu: comunica atividade sem sugerir progresso e reduz custo e distração.
- Sugeri `#BCBCBC` para texto secundário; a proposta usa origem `#C4BEB9`, com mistura efetiva. Convenceu condicionalmente: o par renderizado deve passar também no claro e nos fundos reais.

#### O erro que a proposta ainda tem

O aceite exclui o contraste abaixo do padrão, embora a própria tabela e os riscos registrem que o controle permitido de 56% leva o texto primário a 4,01:1 no 02. Uma configuração oferecida pelo produto pode deixar texto normal abaixo de 4,5:1; proponho limitar o mix para esse par ou corrigir a rampa e testar toda a faixa, em vez de aceitar a falha como escolha do usuário.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Adiar o estado dinâmico. | 88 |
| 2. Símbolo | B com rescaldo largo em todos os tamanhos, sujeito ao teste e ao fallback integral. | 78 |
| 3. Flag | Duas semanas no uso de Anderson, com ensaio de reversão. | 84 |
| 4. Fundo | `#1A1B1E`. | 85 |
| 5. Onde o plano mora | `brand`, ao lado do PLN-007. | 80 |
| 6. Norma do rótulo da ação | WCAG 2.x com rótulo escuro; APCA como aviso e legibilidade observada no teste. | 76 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
