---
scope:
  - brza-studio
tags:
  - design
refs:
  - PLN-007
---

# Reunião Carvão em Brasa: a participação de Lenha, a Engenheira Pragmática

O pedido de Anderson, em 2026-11-07, na sessão da coordenação ("Rebranding BrzA: Carvão em Brasa"): "coordenar uma
reunião de rebranding da marca BrzA (…) se aproximar mais do tom Carvão em Brasa, com um grafite mais próximo ao carvão e
tons em brasa incandescente". Este é o registro de **Lenha** — persona a Engenheira Pragmática, no agente Codex —, aberto pela coordenação com
`brza sessions reuniao-brasa-lenha`. A pauta e as regras estão no briefing da reunião; cada rodada é uma seção abaixo.

## O que se fez

### Rodada 1: opinião inicial

#### 1. Carvão, a base neutra

- **Posição:** manter #1A1B1E como carvão e construir rampas funcionais separadas para texto e tema claro.
- **Por quê:** lido no briefing: a 03 só entrega 1,8:1 sobre a 01; #BCBCBC entrega 9,1:1. Vi o fundo na prancha `material/brasa/brasa.png`; o subtom frio não me incomoda. Suponho que estabilidade entre temas compense mais que aquecer todo o canvas.
- **Ideias:** (ousadia: baixa) `--surface-canvas: #1A1B1E`, `--surface-raised: #2C2D31`, `--text-secondary: #BCBCBC`; reservar #454446 para divisórias decorativas, nunca para informação necessária.
- **Ideias:** (ousadia: média) tema claro com `--surface-canvas: #FAF8F5`, `--surface-raised: #FFFFFF`, `--text-primary: #1A1B1E`, `--text-secondary: #6B554B`; #6B554B vira texto quente, não degrau obrigatório da rampa escura. Validar os pares antes de entregar.
- **Risco:** os mixes atuais podem alterar esses valores; aplicar tokens só no CSS global pode deixar o tema do catálogo diferente.
- **Confiança:** 91/100

#### 2. Brasa, a escala quente, a semântica e o contraste

- **Posição:** usar 07 com texto escuro em ações de marca; manter erro, aviso e link em famílias funcionais próprias.
- **Por quê:** lido no briefing: 07/#1A1B1E dá 4,9:1, branco/07 só 3,5:1; código inline cai a 4,1:1. São números do material, não medições minhas. Suponho que mudar a cor de erro agora aumentaria o escopo sem provar melhor reconhecimento.
- **Ideias:** (ousadia: baixa) `--action-brand: #FF3D00` com `--action-brand-foreground: #1A1B1E`; `--brand-text: #BCBCBC` no escuro e #A83E15 no claro para código inline, com verificação sobre a caixa real.
- **Ideias:** (ousadia: média) manter erro #FF6568 com ícone e mensagem explícita, aviso #EAB308 e link #79C0FF no escuro; proibir 06 como “alerta quente”. Nenhum estado depende só da cor.
- **Ideias:** (ousadia: baixa) preservar `--primary` durante o piloto; criar variante de botão `brand` para Enviar e Continue, sem recolorir todos os botões do aplicativo.
- **Risco:** erro e marca ainda podem parecer próximos; reprovar a combinação se a tarefa de reconhecimento mostrar confusão. A 06 não recebe texto branco normal.
- **Confiança:** 90/100

#### 3. O símbolo

- **Posição:** escolher B no ícone do app e manter a silhueta existente, com versão sólida para 16 px e tray.
- **Por quê:** vi `material/brasa/simbolo/A.png`, `B.png` e `C.png`: B concentra o calor; as fagulhas de C acrescentam detalhe que se perde pequeno. Suponho que B preserve reconhecimento com menos variantes; não testei o tray real.
- **Ideias:** (ousadia: baixa) B com núcleo #FF3D00, meio #D84315 e borda #A83E15 para o ícone do app; sem halo no arquivo de 16 px, mantendo a silhueta da chama com circuito e `{}`.
- **Ideias:** (ousadia: média) variante pequena sólida: #FF3D00 sobre carvão, #A83E15 sobre claro; no tray macOS, imagem template monocromática adaptada pelo sistema, sem tile nem brilho.
- **Risco:** circuito e `{}` podem embolar mesmo sólidos; exigir inspeção em tamanho real a 1× e 2× antes de declarar a variante pequena aprovada.
- **Confiança:** 83/100

#### 4. A brasa viva na interface

- **Posição:** Enviar aceso quando habilitado, foco com contorno próprio e movimento restrito ao trabalho em curso.
- **Por quê:** vi `material/brasa/chat/brasa-chat-7-composer.png`: o botão laranja reduz a diferença visual do foco. O levantamento F61 aponta que `native-chat-theme-surface-style.ts:12-69` sobrescreve `--primary`. Suponho que uma variante explícita reduza a dependência dessa cascata.
- **Ideias:** (ousadia: baixa) Enviar habilitado em #FF3D00 com seta #1A1B1E; foco de teclado com anel sólido de 2 px e afastamento de 2 px, #BCBCBC no escuro e #1A1B1E no claro; medir contra os dois lados do anel.
- **Ideias:** (ousadia: média) “Trabalhando” respira em 2,4 s, animando só `opacity` de um halo decorativo; símbolo e texto ficam constantes. `prefers-reduced-motion: reduce` elimina a animação; painel sem foco pausa o halo.
- **Ideias:** (ousadia: baixa) hover de marca em #A83E15 a 22% só nas ações de marca; pergunta mantém seleção e texto explícitos; Parar usa ícone #FF6568 com fundo correspondente a 14%, sujeito ao contraste composto.
- **Risco:** várias sessões trabalhando podem virar várias luzes; limitar a respiração ao painel ativo e não animar `box-shadow` nem filtros.
- **Confiança:** 87/100

#### 5. Narrativa, voz e rollout

- **Posição:** “Carvão em Brasa” orienta a identidade; a microcópia continua dizendo a ação, e a entrega vem em duas etapas reversíveis.
- **Por quê:** o briefing define mini-rebranding, preservando símbolo, logotipo e filhas. O levantamento F63 localiza os tokens de marca em `main.css:195-203`; F61 registra a segunda camada de tema. Suponho capacidade de habilitar o piloto localmente; não conferi se já existe uma chave apropriada.
- **Ideias:** (ousadia: baixa) nomes primitivos `--brand-coal-01` e `--brand-ember-07`, mapeados a tokens funcionais; usar “Enviar”, “Continuar”, “Trabalhando” e “Tentar novamente”, sem metáforas de incêndio em erro ou permissão.
- **Ideias:** (ousadia: média) etapa 1: paleta, B e variantes de ação; etapa 2: respiração e materiais das quatro filhas. Estimativa minha, sem auditoria de código: 8–16 h para piloto e QA, 3–5 arquivos de código e ativos à parte; ícones distribuídos e empacotamento exigem orçamento posterior.
- **Ideias:** (ousadia: baixa) piloto local reversível por mapa de tokens; matriz de 8 cenas × 2 temas × movimento normal/reduzido = 32 capturas. Medir texto ≥4,5:1 e ícones funcionais ≥3:1 em cada par efetivo; zero falhas bloqueantes para avançar.
- **Ideias:** (ousadia: média) comparar antes/depois com 5 pessoas nas tarefas Enviar, Parar e reconhecer erro; meta proposta: zero confusões entre erro e marca e mediana de tempo até 10% acima da base. Amostra serve como sinal inicial, sem inferência estatística.
- **Risco:** o piloto pode passar no chat e falhar em temas personalizados ou no app instalado; essas superfícies entram no aceite antes da distribuição ampla.
- **Confiança:** 82/100

#### A ideia mais ousada desta rodada

O painel ativo tem uma única brasa que respira enquanto o agente trabalha; ao terminar, ela esfria para o carvão em 600 ms, sem fagulhas.
É uma hipótese de assinatura reconhecível com um único elemento CSS. Risco: parecer falha ou chamar atenção demais; manter o estado em texto e desligar todo movimento com redução de movimento.

#### Issues candidatas

- **Separar tokens de marca, ação e texto nos dois temas** — evitar que a paleta decorativa reduza contraste e que o tema sobrescreva a ação — prioridade `high`
- **Validar B no ícone, em 16 px e no tray** — impedir que uma escolha bonita ampliada produza ruído na escala de uso — prioridade `high`
- **Distinguir foco, trabalho e erro no piloto do chat** — testar a leitura de estados antes de espalhar o laranja — prioridade `high`
- **Experimentar a respiração da brasa no painel ativo** — avaliar assinatura e distração com alternativa estática equivalente — prioridade `medium`

#### Placar da rodada 1

| Assunto | Posição em uma linha | Confiança |
| :------ | :------------------- | :-------- |
| 1. Carvão | Manter #1A1B1E; rampas próprias para texto e claro. | 91 |
| 2. Brasa | 07 com texto escuro; semântica funcional separada. | 90 |
| 3. Símbolo | B no app; sólido pequeno; template no tray. | 83 |
| 4. Interface | Enviar aceso; foco sólido; respiração só trabalhando. | 87 |
| 5. Narrativa e rollout | Voz literal; piloto reversível com contraste e tarefas medidos. | 82 |

<!-- fim-rodada-1 -->

### Rodada 2: debate

#### As disputas

Li as rodadas 1 de Tição, Cinza, Fogareiro, Fole e a minha; Faísca ainda está sem rodada 1 no arquivo consultado. Os números abaixo vêm de `.sessions/reuniao-brasa/sintese-1.md`, não de cálculo meu. Suponho o escopo restrito ao mini-rebranding, sem alteração de lógica de tarefas.

- **D1:** a — manter #1A1B1E; nenhuma medição apresentada demonstra ganho funcional ao aquecer o canvas. O efeito de calor pode vir da marca e do papel claro, poupando uma variável na comparação — 93/100.
- **D2:** a — #BCBCBC preserva margem: 9,07:1 no 01 e 7,24:1 no 02. Os quentes passam nesses fundos, mas não justificam reduzir a margem antes de auditar os mixes reais; não confundo contraste alto com conforto já comprovado — 92/100.
- **D3:** b — adotar #FF75A0 como candidato no escuro: ΔE em deuteranopia sobe de 10,3 para 22,4, com 6,81:1 no 01. Retiro minha defesa de manter #FF6568; ícone e texto continuam obrigatórios, e o claro exige variante própria — 94/100.
- **D4:** c — testar #FACC15 no escuro: ΔE em deuteranopia 17,3 contra 12,1 do aviso atual. Trocar um token custa menos que preservar uma colisão conhecida; esse resultado não aprova o texto amarelo no tema claro — 90/100.
- **D5:** b — B no ícone grande, sólido sem halo no pequeno e template no tray. Não compro que B já seja legível em 16 px: a síntese confirma a mancha nos três. Não abriria duas leituras C/B antes do teste em escala real — 86/100.
- **D6:** a — respirar e esfriar em 600 ms, apenas no painel ativo; com redução de movimento, nem o esfriar anima. Fagulha por ferramenta e relógio de cor acrescentam estados sem ganho de tarefa demonstrado — 93/100.
- **D7:** a — “Trabalhando”, “Aguardando sua resposta”, “Tentar novamente”. A identidade já chega pela paleta, símbolo e movimento; metáfora operacional cobra interpretação a cada uso — 93/100.
- **D8:** d — teste de 5 s com e sem Claude ao lado, usando também a marca atual como base. ΔE 11,8 sinaliza proximidade, não prova confusão de marca; mudar matiz antes do teste refaz contraste e ativos às cegas — 91/100.
- **D9:** a — piloto reversível de duas semanas, com ensaio em cinza como verificação anterior dentro dele, sem terceiro rollout. Não vira padrão só porque passou o prazo: exige auditoria dos dois temas e tarefas aprovadas. `brand.brasa` é chave proposta, não recurso existente verificado — 92/100.

#### Os ataques

- **Fole, interface:** rejeito fagulha por ferramenta concluída, mesmo limitada a uma por segundo. O teto limita frequência, mas não a duração da distração; pede controle de eventos, sobreposição e limpeza para decorar algo que já tem status. Suponho que o texto atual basta para localizar a conclusão. Meu ataque cai se um protótipo controlado reduzir o tempo de encontrar a última ferramenta sem aumentar erros ou distração frente à versão estática.
- **Fogareiro, movimento adaptativo:** rejeito mudar #FF3D00 para #E05A20 às 22h ou após 4 h como solução de conforto. A rodada não mediu esse benefício; horário, duração e novo acento multiplicam combinações de QA, e horário local não representa iluminação. Meu ataque cai com comparação de uso prolongado que mostre benefício e todos os pares efetivos aprovados, com controle explícito da pessoa. Não adotaria automatismo só pela metáfora térmica.

#### A concessão

Tição, Cinza e Fole me convenceram a retirar a conservação do erro: a simulação nova da coordenação dá lastro que faltava à proposta rosa. O aviso também muda pelos dados novos. Cinza me convenceu a retirar cor no ensaio de estrutura; Fole, a testar a proximidade com Claude antes de mexer na 07. Minha R1 propunha piloto reversível, mas não duas semanas: esse prazo vem de Fole, embora a síntese o tenha atribuído também a mim. Enviar aceso significa habilitado com conteúdo enviável, incluindo anexos válidos; vazio fica neutro, sem exigir foco para revelar a ação.

#### "Sim, e…"

- **Cinza, piloto sem cor → matriz comparável** (ousadia: média): capturar os mesmos estados com cor e em cinza, usando o mesmo mapa de tokens; comparar foco, erro, pergunta e disponibilidade de Enviar antes/depois. O cinza testa redundância; o par colorido testa marca. Estimativa minha: 1–2 h adicionais se a captura da R1 já estiver montada; nenhuma flag persistente nova só para esse ensaio.
- **Fole, reconhecimento de 5 s → teste que decide investimento** (ousadia: média): alternar marca atual e B proposta, isoladas e ao lado da Claude, com 5 pessoas e ordem alternada; recolher primeiro a atribuição espontânea, depois a escolha entre nomes. Uma confusão com Claude abre revisão da 07; ausência de confusão permite seguir no piloto, sem alegar prova estatística. Custo suposto: 1–2 h de preparação e síntese, mais 5 min por participante; paga-se antes de exportar as quatro filhas.

#### Placar da rodada 2

| Assunto | Posição agora | Confiança R1 | Confiança R2 | Mudou? (não, ajustou, virou) | Quem te moveu |
| :------ | :------------ | :----------- | :----------- | :--------------------------- | :------------ |
| 1. Carvão | 01 e #BCBCBC mantidos; claro com rampa própria. | 91 | 93 | não | Coordenação reforçou a margem nos cartões. |
| 2. Brasa | 07 com texto escuro; erro #FF75A0 e aviso #FACC15 candidatos no escuro. | 90 | 94 | virou | Tição, Cinza, Fole e medições da coordenação. |
| 3. Símbolo | B; pequeno sólido sujeito a teste; tray template. | 83 | 86 | não | Tição e convergência C7 reforçaram. |
| 4. Interface | Enviar com conteúdo enviável; foco próprio; respirar e esfriar só no painel ativo. | 87 | 93 | ajustou | Tição e Fole explicitaram a relação entre calor e disponibilidade. |
| 5. Narrativa e rollout | Voz literal; duas semanas reversíveis, ensaio em cinza e teste contra Claude. | 82 | 92 | ajustou | Cinza e Fole. |

<!-- fim-rodada-2 -->

### Rodada 3: voto final
#### O voto em cada proposta

Li as R2 disponíveis; Faísca segue sem R2, então considerei sua R1. Números: `sintese-2.md`, sem recálculo meu. Suponho ajustes explícitos no plano para as ressalvas; meu voto não é aceite de Anderson.

| Proposta | Voto (apoio, apoio com ressalva, contra) | Ressalva ou alternativa em uma linha | Confiança |
| :------- | :--------------------------------------- | :----------------------------------- | :-------- |
| P1 | apoio | Preservar 01/02 reduz variáveis; calor no texto e no tile basta como hipótese de marca. | 96 |
| P2 | apoio com ressalva | Aceito #A8A29E auditando mixes; #7A746F a 3,74 não serve para placeholder informativo: exigir 4,5; 03 só decorativa ou realmente desabilitada. | 92 |
| P3 | apoio com ressalva | Rosa candidato; diff mantém sinais −/+, rótulos e tokens próprios, com fundos compostos e claro auditados. | 94 |
| P4 | apoio com ressalva | No claro, texto neutro e ícone/forma explícitos; medir ícone contra o fundo tingido, sem garantir distinção só pelo limão. | 93 |
| P5 | apoio com ressalva | Token próprio, sim; lint de usos não prova cota em execução: definir se conta só ações sólidas e conferir cenas simultâneas. | 94 |
| P6 | apoio com ressalva | #FFB088 só no escuro; claro usa 05 ou neutro; medir na caixa inline real, não apenas 01/02. | 93 |
| P7 | apoio com ressalva | “Chapado 07 → 05” exige regra inequívoca: cor sólida por tema até 32 px; definir 33–63 px sem halo e conferir 16 px real. | 89 |
| P8 | contra | Adiar estado no Dock/tray: integração e sincronização sem custo levantado; manter template e ícone estáticos nesta entrega. | 92 |
| P9 | apoio | Disponibilidade inclui anexo válido; foco independente do botão, auditado contra superfícies adjacentes e recortes. | 98 |
| P10 | apoio com ressalva | Animar halo decorativo, glifo constante; 05/01 dá 2,8:1: outros painéis precisam de indicador ≥3:1 ou texto equivalente; redução de movimento inclui término. | 94 |
| P11 | apoio com ressalva | Voz literal, sim; conferir cópia real antes de trocar “Ask Claude…”: artboard não prova texto do app; preservar identificação necessária do provedor. | 95 |
| P12 | apoio | Papel e rampa próprios fecham o claro; não herdar indiscriminadamente acentos do escuro. | 93 |
| P13 | apoio com ressalva | Pré-registrar teste, sem decretar solução: 2/5 confundindo exige ajuste e reteste; 1/5 também precisa de destino para cumprir P15. | 91 |
| P14 | apoio com ressalva | CI mede pares efetivos; ΔE é triagem; cinza exige critérios verificáveis de forma/texto e revisão humana; medir manutenção antes de prometer CI perpétuo. | 94 |
| P15 | apoio com ressalva | Definir tempos e contagens por tarefa; 0 queixas é observação, não prova de conforto; explicitar tratamento de 1/5 atribuindo à Claude. | 93 |
#### O que me faria mudar de ideia

- **P9 (98):** teste com teclado, ponteiro e anexos mostrando mais falhas de descoberta ou envio que na base, apesar de foco e disponibilidade corretos, derruba meu apoio à apresentação proposta.
- **P1 (96):** comparação controlada mostrando reconhecimento melhor com carvão quente, sem piorar tarefas nem contraste e com custo levantado, derruba minha preferência por manter 01/02.
#### A última ideia

**Ensaio de reversão durante turno vivo** (ousadia: média): desligar `brand.brasa` com pergunta pendente e anexo no composer; conferir que só a aparência volta, preservando conteúdo, foco e ações disponíveis. Suponho troca da flag na sessão; se exigir reinício, ensaiar restauração nessa fronteira. Estimativa: 30–60 min com piloto pronto; paga-se ao recuar sem perder trabalho.
#### Os colegas

| Persona | A contribuição mais útil dela, em uma linha | Nota de 0 a 10 |
| :------ | :------------------------------------------ | :------------- |
| Tição | Reutilizar a chama do cabeçalho e o símbolo existente conteve a implementação. | 9 |
| Faísca | O diff removido revelou uma colisão semântica que faltava à minha matriz. | 9 |
| Cinza | Separar simulação de evidência humana e testar estrutura sem cor melhorou o aceite. | 10 |
| Fogareiro | Insistir no uso prolongado acrescentou condições reais ao piloto; conforto segue hipótese. | 8 |
| Fole | Investigar Claude antes de deslocar matiz poupou mudança sem benefício demonstrado. | 9 |
#### Autoavaliação

Fui Lenha ao cobrar tokens próprios, reversão e escopo incremental. Saí da contenção inicial ao aceitar respiração e rampa quente com condições; minha economia de escopo na R1 subestimou o risco cromático do erro.

<!-- fim-rodada-3 -->

### Rodada 4: entrega — mapa de implementação no BrzA Studio

#### Base e limites

Leitura de `~/Projects/brza-studio`, HEAD `8abbde720ce`, comparada à referência **local** `upstream/main@c5383afb6cb`; sem fetch ou alteração do app. `sintese-3.md` fornece a tabela v1 candidata, com lacunas dependentes da auditoria de Cinza. Horas são estimativas, não tempo medido. Convenções: `R` = `src/renderer/src/`; `NC` = `R/components/native-chat/`; `S` = `src/shared/`; linhas da revisão lida.

#### A cópia: nossa ou do upstream

- **“Ask Claude to do anything…” pertence ao protótipo local:** `.sessions/reuniao-brasa/material/brasa/chat/build.py:33` e `:183`; o vazio “Start a conversation with Claude” está em `:88`. Busca literal em `HEAD` e `upstream/main`, sob `src` e `resources`, não encontrou a primeira string. Não há essa troca a fazer no app lido.
- **Placeholder real herdado:** `S/native-chat/transcript/native-chat-turn-status.ts:22` contém “Ask anything, @ to mention files, / for commands”, idêntico no upstream local; `NC/native-chat-composer-target.ts:18–44` seleciona também mensagens de bloqueio/parada. `NC/NativeChatComposerField.tsx:375` o consome; `R/i18n/locales/en.json:19912` confirma a tradução inglesa. Preservar estados e comandos.
- **Texto do vazio herdado:** `S/native-chat/native-chat-empty-state.ts:10–12` usa “Start a chat with {{value0}}” e convite parametrizado, iguais no upstream local. O commit `55dffb479a8` que agrupou a cópia é ancestral de `upstream/main`. `NC/NativeChatEmptyState.tsx:101–112` injeta `formatAgentTypeLabel(agent)`: Claude ali identifica o agente.
- **Visual do vazio nosso:** `NC/NativeChatEmptyState.tsx:26–29` acrescenta chama e wordmark, conforme diff contra upstream e commit `786f4b56ff9` (PLN-007 P5). `R/components/brza/BrzaWordmark.tsx:15–22` já identifica BrzA Studio. Atualizar identidade visual, preservar identificação do provedor; nenhuma nova cópia nesta fase.

#### Segunda camada e entrada de `--action-brand`

- `R/lib/native-chat-theme-surface-style.ts:13–18` retorna só mixes quando `followsAppScheme`; no catálogo, `:26–42` remapeia superfícies e **`:38–39` define `--primary = var(--chat-foreground-strong)` e `--primary-foreground = var(--chat-canvas)`**. `:45–60` redefine fontes/mixes. A sobrescrita de primary é do ramo de catálogo, não de todos os temas.
- `NC/native-chat-appearance-style.ts:88–90` agrega o objeto; `NC/NativeChatStructuredSession.tsx:276–277` o aplica inline na raiz. Mudar primary só no CSS não vence essa declaração local. `R/components/editor/markdown-surface-theme.ts:68` reutiliza o helper: não inserir a marca indiscriminadamente nessa função compartilhada.
- **Entrada proposta:** expor `--color-action-brand` e `--color-action-brand-foreground` no `@theme inline` de `R/assets/main.css:99–103`; declarar `--action-brand: #FF3D00` e `--action-brand-foreground: #1A1B1E` no escopo do piloto. Variante `brand` consome esses tokens diretamente, nunca alias de primary. O objeto remapeado atual não declara esses nomes; mantê-los fora dele e conferir usos por lint.
- **Flag proposta:** novo `NC/brza/use-brza-brand-pilot.ts`, chave local `brand.brasa`, estado reativo sem remontar sessão; raiz e variantes recebem o mesmo booleano. CSS sob atributo do piloto e esquema resolvido do chat, não só `.dark` do documento; desligada, restaura tokens e variantes anteriores. Não encontrei `brand.brasa`/`action-brand` nos pontos de integração buscados. Não migrar tema/ANSI do terminal para implementar a flag.

#### Arquivos, linhas e mudanças planejadas

| Alvo | Linhas atuais | Mudança e cuidado |
| :--- | :------------ | :---------------- |
| `R/assets/main.css` | 194–203, 331–332, 450–529 | Primitivos e semânticos v1 por esquema, sob piloto; erro/aviso/diff locais ao chat primeiro, sem recolorir o app inteiro. |
| `R/assets/main.css` | 665–734 | Mapear canvas, textos, placeholder, superfícies, aviso, diff e foco efetivos: HEX de origem atravessam mixes e podem perder contraste. |
| `NC/native-chat-appearance-style.ts`; `R/lib/native-chat-theme-surface-style.ts` | 56–92; 12–69 | Compor mapa do piloto após a camada para BrzA padrão; catálogo conserva superfícies escolhidas e recebe marca/estados auditados. Não alterar o helper se composição local bastar. |
| `S/native-chat-theme.ts`; `S/terminal-themes/defaults.ts` | 59–61, 95–120; 7–9 | Padrão parte de #0a0a0a com mix 5%; BrzA Dark usa #24272c. Fechar 01 exato na composição do piloto; preservar defaults e temas do terminal nesta fase. |
| `R/components/ui/button.tsx` | 10–31, 61–72 | Acrescentar variante `brand`, sem trocar `default`; anel neutro 2 px sem opacidade enfraquecendo o foco. |
| `NC/NativeChatComposerActions.tsx`; `NC/NativeChatComposerField.tsx` | 95, 133–156; 404–408 | Brand só em Enviar disponível; Parar com semântica própria e rosa; preservar edição, fila, bloqueios e handlers. |
| `NC/native-chat-composer-send-state.ts` | 39–59 | Reusar `imageBlock`, `hasDraft` e `sendButtonDisabled`: imagem pendente conta como rascunho, mas pode bloquear envio. Não reimplementar disponibilidade pela cor. |
| `NC/NativeChatApprovalCard.tsx`; `NC/NativeChatQuestionCard.tsx` | 162–174; 297, 363–376 | Allow/Submit são `<button>` próprios: compartilhar receita `buttonVariants`, preservando handlers/layout; opção selecionada da pergunta não vira CTA. Auditar superfície de segurança. |
| `NC/NativeChatInterruptedContinue.tsx`; `NC/NativeChatNoticeRow.tsx` | 254–265; 354–357 | Trocar variante no Continue compartilhado, cobrindo Continue Now; não alterar lógica de retomada/limite. |
| `NC/native-chat-markdown.css`; `NC/brza-chat-link.css` | 36–43; 4, 9 | Token de inline separado de texto de marca: #FFB088 escuro e 05/neutro claro após auditoria na caixa; link claro existente #0969da é candidato. |
| `NC/NativeChatStructuredSession.tsx`; `NC/NativeChatPaneHeader.tsx` | 259–260, 279; 53–60, 134–157 | Reusar `data-native-chat-working` e foco para halo no cabeçalho; hoje o cabeçalho só conhece foco. Evitar segundo estado de execução. |
| `NC/NativeChatTurnActivityLine.tsx`; `R/assets/main.css` | 55–61; 1188–1274 | Retirar tremulação e sheen sob piloto; texto/glifo constantes, halo 2,4 s só no cabeçalho ativo; outros trabalhando 06/05 por tema; término 600 ms, nada anima em reduced-motion. |
| `R/assets/main.css` | 1199–1210 | Condicionar regra antiga: foco hoje força degradê e **branco** no Enviar; não pode vencer a variante nova nem esconder o foco neutro. |
| `config/scripts/brza-brand-build.mjs`; `resources/brza-flame-mono.svg` | 17–24, 47–65, 119–123, 174–180; 1 | Gerar B e fontes por tamanho; preservar silhueta enquanto candidata. Máscara/lockups vêm do gerador, não de edição manual de cada SVG. |
| `resources/icon-source/generate.sh` | 32–39, 45–56 | Slots 16–64 usam hoje o mesmo símbolo: escolher fonte por tamanho lógico, inclusive 16@2× sem halo; gerar ICNS/ICO/PNG e template 1×/2×. |
| `src/main/window/desktop-integration/app-icon.ts`; `src/main/tray/system-tray.ts`; `config/electron-builder.config.cjs` | 8–24; 2–3, 93, 142; 627, 712 | Consumidores a conferir após geração, sem mudança prevista de lógica; manter paths/IDs e template mono. P8 não entra. |
| `NC/NativeChatBrandMark.fixture.tsx`; `docs/STYLEGUIDE.md` | 196–205; 23–25, 58 | Estender fixture de esquemas opostos e documentar variante/cores. Não criar teste unitário que apenas espelha classes, HEX ou cópia. |

#### Fases, horas, flag e riscos

| Fase | Entrega e estimativa | Reversível por flag? | Risco e verificação |
| :--- | :------------------ | :------------------ | :----------------- |
| 0 | Base atual e fechar pares pendentes com Cinza; 2–3 h. | Sem mudança funcional. | Lacunas do claro/mixes; medir compostos antes da substituição. |
| 1 | Flag, tokens, composição de temas e variante; 4–6 h. | Sim, sem remontar editor. | Cascata/esquema oposto; comparar padrão, BrzA Dark e catálogo nos dois modos. |
| 2 | Ações, inline e foco; 3–5 h. | Sim, preservando apresentação anterior. | Disponibilidade falsa/cota; exercitar texto, anexos pendentes/válidos, fila, parada, pergunta e overlay. |
| 3 | Halo, trabalho e término; 2–4 h. | Sim, inclusive transições em curso. | Brasa presa/múltipla; verificar 1/4/8 painéis e fim sem indicador de trabalho residual. |
| 4 | Gerador B, fontes pequenas e previews; 3–5 h. | Previews sim; ícone empacotado não. | Swift/librsvg/iconutil e escala lógica; inspecionar 13/16/32 px a 1×/2× antes de instalar ativos. |
| 5 | Auditoria automatizada, 8 cenas, cinza, regressão e reversão; 4–6 h. | Sim para chat. | Cota exige cenas; forma/texto em cinza e anel contra ambos os lados precisam de aceite. |
| 6 | Após portões: ativos estáticos e empacotamento; 2–4 h. | Não; restaurar ativos e gerar build. | Cache do sistema e dev/prod; conservar originais e conferir macOS/Windows/Linux. |

**Total estimado: 20–33 h**; fases 0–5: 18–29 h. Exclui duas semanas de observação, recrutamento/testes humanos, espera de revisão e retrabalho da auditoria. Revisa minha R1 de 8–16 h: agora inclui flag reativa, botões próprios, mixes, gerador por tamanho e portões. Previsão de 15–20 arquivos de fonte/guia/fixture, além dos ativos; contagem final depende dos consumidores adicionais descobertos pela auditoria.

#### Verificação prevista e evidência desta entrega

Na execução futura: `pnpm tc:web`, lint/formato dos arquivos, auditoria de pares/uso de tokens, fixtures via `pnpm fixtures:shot <id>`; Electron só se necessário, oculto, com `ORCA_BACKGROUND_LAUNCH=1`. Exercitar envio, parada e reversão com anexo/pergunta. `pnpm check:changed` após última edição antes de eventual push, conforme AGENTS do app. Nenhum teste executado nesta rodada de leitura.
Rodei `rg`, leitura numerada, `git grep` em HEAD/upstream local, diff dos três arquivos de cópia/vazio, histórico e ancestralidade. Confirmaram protótipo separado, cópia herdada e camada inline. Não instalei dependências, gerei ativos, iniciei app ou alterei o `brza-studio`.

#### O que ficou de fora e por quê

P8 (estado dinâmico de Dock/tray), ANSI/CLI e contrato `brand.tokens.json` entre filhas pedem escopo/custo próprios. Geração cobre lockups das quatro filhas, não seus comportamentos. B continua candidata; 33–63 px e pares pendentes precisam de regra/auditoria antes da respectiva fase. Não substituo cópia herdada para corrigir frase exclusiva do protótipo.

**Confiança na peça:** 92/100

<!-- fim-rodada-4 -->



## O que ficou

## Fora do workspace

Nada.
