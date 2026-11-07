---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a contraprova de Cinza, o Cético Analítico, em outro modelo

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"), depois das sete
rodadas: "ajuste o modelo/esforço do agente/sessão, para ficar condizente com o papel dele na reunião; tente
diversificar o máximo o uso de modelo/esforço". Esta é uma sessão nova, de contexto limpo, da persona **Cinza** — o Cético Analítico —
no agente Codex, com o modelo `gpt-6-astra` e esforço `xhigh` (na reunião, gpt-6.1-sol medium). Ela refaz às cegas a rodada 1 e mede a
confiança na proposta de plano, para comparar a mesma persona em outro modelo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** mantenho `#1A1B1E` como base escura e separo a rampa de superfícies da rampa de texto; carvão claro também precisa existir.
- **Por quê:** li `.sessions/reuniao-brasa/briefing.md:30–47` e vi `material/brasa/brasa.png` sob essa mesma pasta. Recalculei com `python3 -` em memória: sRGB linearizado, luminância relativa e razão `(Lmaior+0,05)/(Lmenor+0,05)`; 03/01 = 1,778:1, `#BCBCBC`/01 = 9,068:1 e `#BCBCBC`/02 = 7,242:1.
  Medi o salto 03→04 em CIELAB D65, ΔE76 = 15,25: existe mudança cromática, não só luminosidade. Suponho que o calor localizado baste à identidade; não medi se o usuário percebe a base como fria.
- **Ideias:** (ousadia: baixa) `--text-secondary: #BCBCBC` no escuro; reservar `#454446` a divisórias decorativas, nunca presumir que “inativo” significa controle desabilitado.
  (ousadia: média) tema claro “cinza mineral”: `--surface-base: #F4F1EC`, texto principal `#1A1B1E` e secundário `#454446`, medidos em 15,286:1 e 8,596:1; tratar 04 como pigmento quente independente, não degrau obrigatório de texto.
- **Risco:** o claro proposto pode parecer bege e a base fria pode enfraquecer a metáfora; contraste não valida identidade.
- **Confiança:** 88/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** aceito 07 com texto carvão no CTA, veto branco nesse par para texto normal e mantenho erro e aviso separados da marca, inicialmente com suas cores atuais no escuro.
- **Por quê:** recalculei os HEX de `briefing.md:23,30–43`: carvão/07 = 4,854:1, branco/07 = 3,548:1, branco/06 = 4,436:1; arredondar 4,436 não autoriza 4,5. A 07 sobre 02 dá 3,877:1: passar no fundo principal não habilita texto em qualquer superfície.
  Medi ΔE76 D65 entre 07 e erro = 41,42; entre 07 e aviso = 66,09. Isso não prova distinção semântica: erro/07 têm razão de luminância com offset de apenas 1,235:1. Suponho que rótulo e forma resolvam mais que trocar vermelho por rosa; APCA e simulações de daltonismo não foram executados.
- **Ideias:** (ousadia: baixa) `--action-primary-bg: #FF3D00` e `--action-primary-fg: #1A1B1E`; texto de código em linha recebe token próprio por superfície, sem herdar a 07 automaticamente; 06 não recebe legenda branca normal.
  (ousadia: média) `--brand-text` claro em `#A83E15` sobre `#F4F1EC` (5,540:1); CTA claro pode usar 05 com branco (6,241:1). No escuro, erro `#ff6568` com ícone e “Falhou”; aviso `#eab308` com triângulo e motivo; não chamar 06 de “alerta quente”.
- **Risco:** manter vermelho pode conservar confusão em visão periférica; trocar por rosa sem ensaio apenas substituiria uma hipótese por outra. Os pares propostos não certificam componentes completos.
- **Confiança:** 86/100

#### 3. O símbolo

- **Posição:** escolho A como direção provisória do ícone grande, com versão óptica plana em 16 px e monocromática no tray; C fica como exploração editorial.
- **Por quê:** abri `material/brasa/simbolo/A.png`, `B.png` e `C.png`: A concentra a área mais acesa na base; B adiciona halo central; C acrescenta fagulhas e escurece parte da chama. As pranchas incluem 16 px, mas vê-las não é teste de reconhecimento no app.
  Suponho que A preserve mais continuidade com a chama existente (`briefing.md:9–11,54–60`) com menos informação periférica que C; não medi reconhecimento, qualidade em Retina nem legibilidade de `{}` nessa escala.
- **Ideias:** (ousadia: baixa) `brand-symbol-small`: silhueta existente em cor sólida, 07 no escuro e 05 no claro, sem halo nem tile em 16 px; conferir se circuito e `{}` sobrevivem antes de simplificá-los.
  (ousadia: média) `brand-symbol-tray` monocromático, adaptado ao fundo pelo sistema; A com calor inferior no Dock e C apenas na abertura editorial de 128 px ou mais, nunca como sinal de erro.
- **Risco:** A pode continuar parecendo fogo comum; variantes por tamanho podem divergir da marca e a silhueta plana ainda pode perder detalhes. A escolha é reversível.
- **Confiança:** 62/100

#### 4. A brasa viva na interface

- **Posição:** a brasa comunica atividade e ação disponível; Enviar habilitado fica laranja mesmo sem foco, mas foco ganha indicador próprio e Parar não parece um segundo Enviar.
- **Por quê:** vi `material/brasa/chat/brasa-chat-5-trabalhando.png`, `brasa-chat-7-composer.png` e `brasa-chat-8-avisos.png`; `briefing.md:63–67` descreve brilho de 12% e hover de 22%. Composição sRGB nominal sobre 01: 07 a 12% → `#351F1A`, 1,117:1; 05 a 22% → `#39231C`, 1,174:1, sem simular blur.
  Esses brilhos não bastam como único sinal. Suponho que “pode enviar” deva depender de conteúdo válido, não de foco; um PNG não demonstra movimento nem preferência por animação.
- **Ideias:** (ousadia: baixa) Enviar desabilitado neutro, habilitado 07; `:focus-visible` com contorno sólido de 2 px e afastamento de 2 px, `#BCBCBC` no escuro e `#1A1B1E` no claro. Parar com quadrado, nome acessível “Parar” e ícone neutro contrastante.
  (ousadia: alta) um único ponto de calor no cabeçalho do chat ativo: transição de 200 ms só ao mudar de estado, sem pulsação contínua nem fagulhas; “Trabalhando”, “Aguardando resposta” e “Falhou” persistem em texto, inclusive com movimento reduzido. Pergunta usa contorno e rótulo; aviso conserva triângulo.
- **Risco:** o ponto pode passar despercebido e o CTA constante pode disputar atenção com Continue; proponho uma ação quente dominante por contexto, não uma cota arbitrária de pixels laranja.
- **Confiança:** 78/100

#### 5. Narrativa, voz e rollout

- **Posição:** “Carvão em Brasa” orienta a identidade; a interface descreve o trabalho literalmente, e a mudança só avança com evidência de leitura e de estados.
- **Por quê:** `briefing.md:8–11,20–24` delimita mini-rebranding, quatro filhas e texto de 14 px; `material/brasa/chat/brasa-chat-3-mensagens.png` e `brasa-chat-8-avisos.png` mostram ações e problemas reais competindo por cor. Não há linha de base de usabilidade no material.
  Suponho um piloto local reversível antes da distribuição; os limites abaixo são critérios operacionais propostos, não resultados nem prova estatística.
- **Ideias:** (ousadia: baixa) mensagem de lançamento “Carvão na base. Brasa no que está em ação.”; microcópia “Trabalhando”, “Resposta necessária” e “Não foi possível enviar”. Primitivos `--coal-01`/`--ember-07` alimentam tokens funcionais como `--action-primary-bg`, com mapeamento por tema.
  (ousadia: média) flag `brand-ember-v1`: primeiro matriz claro/escuro e estados, depois piloto com retorno à paleta anterior. Métricas: zero falhas nos pares obrigatórios de texto normal ≥4,5:1 e indicadores essenciais ≥3:1; em 20 cenas equivalentes por versão, ordem contrabalançada, zero confusões ação/erro e mediana de identificação no máximo 10% pior que a atual.
  O piloto pode começar com Anderson; registrar contagem e tempos brutos, sem generalizar de uma pessoa. Se houver confusão ou regressão acima do limite, manter a flag desligada por padrão e ajustar antes de ampliar.
- **Risco:** aprendizado e familiaridade favorecem a versão conhecida; métricas funcionais também podem aprovar uma marca esquecível. Registrar associação espontânea a “brasa”, sem impor porcentagem fictícia de sucesso.
- **Confiança:** 80/100

#### A ideia mais ousada desta rodada

Concentrar o movimento da marca em um único ponto de calor no cabeçalho do chat ativo, com transição apenas na mudança de estado; o restante permanece estável e os rótulos continuam explícitos.
Suposição: menos estímulos simultâneos tornam o calor mais informativo. Risco: a marca parecer apagada e a atividade perder saliência; comparar identificação de estados com a chama atual antes de adotar.

#### Issues candidatas

- **Validar tokens por superfície e tema, inclusive transparências** — os pares aprovados no fundo 01 falham em outras superfícies; incluir APCA como diagnóstico complementar com versão declarada — prioridade `high`
- **Distinguir ação, atividade, pergunta e falha sem depender da cor** — ΔE não garante semântica; verificar rótulos, formas, foco e simulações de daltonismo — prioridade `high`
- **Validar A e variantes ópticas em 16 px e no tray** — as pranchas não comprovam reconhecimento nem adaptação aos fundos do macOS — prioridade `medium`
- **Medir a paleta atual antes do piloto reversível** — sem tempos e confusões de referência, preferência estética vira alegação de melhora — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Manter 01; separar texto de superfície e criar claro mineral. | 88 |
| 2. Brasa | 07 com carvão no CTA; semântica independente e pares por tema. | 86 |
| 3. Símbolo | A provisório; versão plana pequena e monocromática no tray. | 62 |
| 4. Interface | Enviar quente quando habilitado; foco explícito e calor por estado. | 78 |
| 5. Narrativa e rollout | Voz literal, tokens funcionais e piloto com linha de base. | 80 |

<!-- fim-rodada-1 -->

### Rodada 2: a confiança na proposta de plano

#### A confiança

| Parte | Confiança (0–100) | Uma linha |
| :---- | :---------------- | :-------- |
| O plano inteiro | 76 | Bom plano de experimento reversível; votos das personas não são validação, e piloto limitado precisa ser distinto de aprovação para virar padrão. |
| Tabela de tokens | 80 | Origem versus efetivo corrige meu raciocínio com HEX puros; mixes claros, anel e fundos reais ainda têm medições pendentes (proposta:80,87,93). |
| Fases 0–3 (tokens, ações, movimento) | 82 | A composição inline, a flag e a disponibilidade do Enviar têm fundamento descrito; a respiração de 2,4 s continua hipótese (proposta:103–106). |
| Fase 4 (símbolo) | 70 | Vi as folhas `entregas/simbolo/folha-2-1x.png` e `folha-2-2x.png`; B ajustada merece teste, mas pico luminoso não mede reconhecimento. |
| Fases 5–6 (portões, ativos) | 65 | Auditor do app e reversão são fortes; a passagem de piloto limitado a padrão está ambígua e o empacotamento nativo ainda não foi validado. |
| As medições de sucesso | 61 | Cinco pessoas por etapa dão triagem, não ausência de confusão na população; controles e pessoas diferentes melhoram o desenho. |

#### Onde a proposta diverge da sua rodada 1

- **Erro e aviso:** eu mantinha `#ff6568` e `#eab308`; aceito testar `#FF7AA2` e `#FACC15` pela melhora de ΔE2000 sob simulação relatada em R3/R4 (proposta:55–56), mantendo texto e forma. Convenceu para o piloto, não para declarar validação; não reproduzi essas simulações e meu ΔE76 da rodada 1 não é comparável diretamente.
- **Símbolo:** eu escolhia A e versão plana pequena; aceito B com rescaldo largo como candidata, sem halo no pequeno, após ver as folhas. Convenceu pela correção visual e pela saída para o símbolo atual inteiro; o pico 142 igual ao atual não basta, pois a média relatada ainda cai de 96 para 83 em 16 px (proposta:59). Reconhecimento segue não medido nesta sessão.
- **Movimento:** eu propunha transição de 200 ms somente na mudança de estado; a proposta mantém respiração de 2,4 s e resfriamento de 600 ms (proposta:61). Não convenceu: há contenção e movimento reduzido, mas nenhuma comparação demonstrando benefício da repetição; meu voto continua por transições de estado, com durações também hipotéticas.

#### O erro que a proposta ainda tem

**O resultado “piloto limitado” pode ser contado como aprovação para virar padrão.** Evidência: `.sessions/reuniao-brasa/plano-proposta.md:108` manda tornar padrão após os quatro portões; `:133–135` diz que, sem participante com deuteranopia, o portão 4 “passa só como piloto limitado”. Falta excluir expressamente esse resultado da promoção. Correção: portão 4 retorna `aprovado`, `piloto-limitado` ou `reprovado`; só `aprovado`, somado aos demais portões, habilita o padrão. Suposição declarada: “padrão” significa distribuição geral; `piloto-limitado` mantém adesão voluntária e a pendência, sem bloquear os testes locais.

#### O seu voto nas decisões de Anderson

| Decisão | Opção | Confiança |
| :------ | :---- | :-------- |
| 1. Tray e Dock | Adiar estados novos; preservar a atenção existente e o tray template. | 91 |
| 2. Símbolo | B com rescaldo largo, sem halo no pequeno, como candidata uniforme; testar contra topo claro e atual, mantendo o atual inteiro se não igualar sua leitura. | 70 |
| 3. Flag | Duas semanas no uso de Anderson, com reversão; tempo decorrido não substitui aprovação plena dos portões. | 88 |
| 4. Fundo | `#1A1B1E`; não há evidência suficiente de ganho perceptivo para trocar a base. | 90 |
| 5. Onde o plano mora | `brand`, junto do PLN-007, assumindo a localização descrita na proposta; nenhum workstream novo nesta rodada. | 86 |
| 6. Norma do rótulo da ação | WCAG 2.x com rótulo `#1A1B1E`; APCA como diagnóstico a conferir com implementação de referência, sem trocar por branco que reprova o contraste já calculado. | 87 |

<!-- fim-rodada-2 -->

## O que ficou

## Fora do workspace

Nada.
