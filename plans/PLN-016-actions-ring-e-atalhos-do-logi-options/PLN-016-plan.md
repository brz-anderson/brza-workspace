---
status: open
phase: interview
origin: request
description: Perfil comum e extras por app (BrzA Studio, Orca, Antigravity, Cursor) no Logi Options+, com o perfil exportado e o guia em wiki/guides.
ready: "não — falta o teste de herança, de Anderson, e a rodada 4 com o conteúdo dos slots"
estimate_h: 6
executed_h: 0.3
remaining_h: 5.5
scope:
  - workspace
opened: 2026-11-07
owner: Anderson
priority: medium
tags:
  - tooling
---

# PLN-016: O Actions Ring do MX Master 4 tem ações práticas por app no dia a dia

- **Retomar:** rodada 3 fechada; Anderson cria o perfil de Orca, Cursor e Antigravity no Options+ e diz se o ring herdou o global; depois a rodada 4 escolhe o conteúdo de cada slot (P2).
- **Dividido:** [PLN-016 — Desenho](PLN-016-design.md)

## Pedido

- **Origem:** pedido livre, na sessão `logi-options` de 2026-11-07.

> "esse workstream foi criado afim de configurarmos atalhos práticos e ações do `Actions Ring` ficado no uso do dia-a-dia tanto dentro do `BrzA Studio`, quanto em outros apps, como o `Orca`, o `Antigravity`, o `Cursor`, entre outros"

### Cobertura

Os critérios abaixo são **propostas** minhas, a confirmar na rodada 3.

| Origem | Critério de aceite | Passo | Teste (nível) |
| :----- | :----------------- | :---- | :------------ |
| `Pedido 1`, R1.1 | O MX Master 4 abre o Actions Ring em cada um dos 4 apps, com o perfil comum mais os extras do app | P3 | conferência no aparelho (manual) |
| `Pedido 1`, R2.3 | Toda ação de atalho do ring existe no app dono, conferida no keybinding ou na documentação dele | P1 | a tabela do levantamento, com fonte |
| `Pedido 1`, R1.3, R3.2 | Há ações de macro/script (`brza`, `orca` CLI, shell) que rodam a partir do ring | P4 | conferência no aparelho (manual) |
| R1.4, R3.1 | Os `ProfileInfo.json` copiados e o guia em `wiki/guides/` bastam para refazer a configuração numa máquina nova | P5 | reconfiguração a partir do guia (manual) |

### Fora de escopo

- **O MX Keys Mini.** O teclado só chega em 16/11 (R2.4); a configuração por app das teclas F e de ação vai a plano ou issue depois dessa data.
- **Apps além dos 4**, como Terminal, navegador e Finder (R2.2). Voltam como "outros apps" depois da fase 1.
- **Dictation e prompts de IA no ring** (R1.3): não foram marcados.

## Entrevista

### Rodada 1 — dispositivos, perfis, ações e entrega (enviada 2026-11-07)

**Apresentado antes:** o workstream estava vazio; o Logi Options+ está instalado, e os 4 apps estão em `/Applications`. Dois bloqueios em vigor, de outras frentes (PLN-014 e PLN-011), não tocam este trabalho.

Respondida em 2026-11-07, na sessão `logi-options`.

1. **Dispositivo.** Opções: MX Master (recomendado pela inferência; custo: confirmar o modelo; se paga: agora) · MX Creative Console (custo: desenho de dials e teclas LCD; se paga: se fosse o caso) · outro.
   **Resposta:** "mouse Mx Master 4 e teclado Mx Keys Mini". **Decidido:** MX Master 4 é o dispositivo do ring; o MX Keys Mini vira fase futura (R2.4).

2. **Variação por app.** Opções: perfil comum + extras por app (recomendado; custo: perfil base e 4 camadas; se paga: na fase 2, quando o 2º app herda o base) · um perfil por app (custo: 4 perfis em separado; se paga: só se os apps divergirem muito) · ring único e global (custo: baixo, mas sem ações por app; se paga: nunca).
   **Decidido — perfil comum + extras por app.**

3. **Tipos de ação** (múltipla). Opções: atalhos de teclado (custo baixo; fase 1) · ações de sistema/janela (baixo a médio; fase 1) · macros e scripts (médio; fase 2) · dictation e IA (médio a alto; só se já usa).
   **Decidido — atalhos de teclado, ações de sistema/janela e macros/scripts (`brza`, `orca` CLI, shell).**

4. **Entrega.** Opções: exportar o perfil + guia em `wiki/guides` (recomendado; custo: export manual a cada ajuste grande; se paga: na 1ª reinstalação ou troca de máquina) · só o guia (custo: refazer à mão; se paga: nunca, se não reconfigurar) · automatizar por script (custo alto: formato interno que pode mudar; se paga: só para sincronizar entre máquinas).
   **Decidido — exportar o perfil + guia em `wiki/guides/`.**

### Rodada 2 — destino, apps, descoberta dos atalhos e teclado (enviada 2026-11-07)

**Apresentado antes:** o estado do Options+ mora em `~/Library/Application Support/LogiOptionsPlus/`. O `settings.db` é SQLite e guarda o perfil como `BLOB` binário na tabela `data`, com backups internos em `snapshots`; o `macros.db` tem o mesmo desenho. Não há JSON de perfil editável, então a exportação precisa passar pelo backup do próprio app (a verificar em P1).

Respondida em 2026-11-07, na sessão `logi-options`.

1. **Onde mora o plano.** Opções: `PLN` em `plans/` (recomendado; custo: número e molde, ~20 min; se paga: na 2ª sessão) · worklog com plano aceito (custo menor; se paga: só se fechar hoje).
   **Decidido — `PLN`.**

2. **Apps do perfil por app.** Opções: os 4 citados (recomendado; custo: 4 camadas; se paga: fase 1) · os 4 + Terminal, navegador e Finder (custo: ~+3 h; se paga: se usa todo dia) · outra lista.
   **Decidido — os 4 citados: BrzA Studio, Orca, Antigravity IDE e Cursor.**

3. **Como descobrir os atalhos.** Opções: levantar nos próprios apps e Anderson escolhe (recomendado; custo: ~1 h e US$ pequeno; se paga: fase 1) · Anderson dita as ações (custo: lista sem conferência; se paga: só se já sabe de cabeça).
   **Decidido — levantar nos próprios apps, e Anderson escolhe.**

4. **Papel do MX Keys Mini.** Opções: teclas F e de ação por app (recomendado; custo: ~+2 h; se paga: fase 2) · só globais · fora desta fase.
   **Resposta:** "opção 1, mas para uma fase futura, o teclado só chega dia 16/11". **Leitura:** o teclado sai deste plano e vira o plano seguinte, a partir de 16/11; consta no Fora de escopo.

### Rodada 3 — export, scripts, desenho do ring e teste de herança (enviada 2026-11-07)

**Apresentado antes:** o terreno do P1 ([PLN-016-design.md](PLN-016-design.md)): o Options+ não exporta perfil em arquivo, não tem ação de shell nativa, e o BrzA Studio e o Orca não têm atalho de parar o agente nem de aceitar/rejeitar diff.

Respondida em 2026-11-07, na sessão `logi-options`.

1. **Export.** Opções: copiar os `ProfileInfo.json` + guia (recomendada; custo: ~1 h, método não documentado que pode quebrar numa atualização, o P5 testa a restauração; se paga: na 1ª troca de máquina) · só o guia com screenshots (custo: ~0,5 h + ~1 h por máquina; se paga: nunca, se não reconfigurar) · backup da nuvem + guia curto (custo: ~0,3 h, não vale entre Mac e Windows nem fica no git; se paga: se só usa este Mac).
   **Decidido — copiar os `ProfileInfo.json` + guia.** Isso emenda R1.4: o "perfil exportado" é a cópia dos JSON, e o P5 testa a restauração.

2. **Scripts.** Opções: wrapper `.app` pela ação Application (recomendada; custo: ~1,5 h no P4 e um `.app` por macro; se paga: no P4, se o teste passar) · plugin SDK em C# (custo: ~8 h ou mais; se paga: só com 10+ macros) · sem macros por ora (custo: zero, perde R1.3; se paga: se o teste falhar).
   **Decidido — testar o wrapper `.app`;** se falhar, volta à rodada.

3. **Desenho do ring.** Opções: comum = navegação, extras = agente (recomendada; custo: ~2 h no P3; se paga: no 1º dia) · comum = só sistema (custo: ~2 h; se paga: se quer o ring igual fora destes apps) · 8 slots próprios por app (custo: ~2,5 h e contradiz R1.2; se paga: nunca, a menos que a herança falhe).
   **Decidido — página 1 comum com navegação; extras do agente na página 2.** O conteúdo exato de cada slot vai à rodada 4.

4. **Teste de herança.** Opções: Anderson cria o perfil dos 3 apps e diz se herdou (recomendada; custo: ~15 min dele; se paga: antes do P3) · automação por Computer Use (custo: ~30 min meus, GUI Electron frágil; se paga: só se ele não quiser).
   **Decidido — Anderson cria o perfil de Orca, Cursor e Antigravity e informa se herdou.**

## Passos

Rascunho de ordem, a fechar na rodada 3. **Nenhum passo executa sem pedido explícito de Anderson.**

### P1 — Levantar atalhos por app e o caminho de exportação do Options+

Executa R2.3 · executor: subagente `collector`, com a sessão que conduz

Estimado: 1.5 h · Executado: 0.3 h

- [x] **1. Tabela de atalhos** de Orca, Cursor, Antigravity e BrzA Studio, com a fonte de cada um
- [x] **2. Exportação do perfil:** onde o backup nativo do Options+ grava e se o arquivo é portável
- [x] **3. Capacidades de ação do ring:** o que o Options+ aceita (atalho, app, script, Smart Action) na versão instalada

**Evidência:** dois `collector` (Sonnet), ~3,5 min cada; terreno em [PLN-016-design.md](PLN-016-design.md). Conferido por amostra: `definitions-core-4.ts:36` (`Mod+Shift+J` no darwin) e `agy/package.json` (`escape` interrompe o agente, `alt+enter` aceita). Fora do achado: perfil exportável em arquivo, ação de shell nativa, passo oficial de adicionar app ao ring.

### P2 — Rodada 3: escolher as ações do ring

Executa R2.3 · executor: sessão que conduz, com Anderson

### P3 — Montar perfil comum e extras por app

Executa o que a rodada 3 decidir · executor: Anderson, na GUI do Options+

Estimado: 2 h · Executado: — h

### P4 — Ações de macro e script

Executa R1.3 · executor: sessão que conduz, com Anderson

Estimado: 1.5 h · Executado: — h

### P5 — Copiar os `ProfileInfo.json`, testar a restauração e escrever o guia

Executa R1.4 · executor: sessão que conduz

Estimado: 1 h · Executado: — h

## Worklogs

- 2026-11-07 — R1 a R3 fechadas; P1 feito; destino `PLN`; teclado fica para depois de 16/11. Parou na rodada 4 (conteúdo dos slots), à espera do teste de herança.
  [Plano do Actions Ring: abertura e entrevista](../../work/worklogs/2026-11-07-plano-do-actions-ring-abertura-e-entrevista.md)
