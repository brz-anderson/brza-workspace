# Pedir a revisão da entrega

Com todo passo `[x]` ou `[-]` — o `$S/plan_state.py PLN-NNN` sem `checked-without-evidence` —: `phase: review`,
`status: in_review`.


1. **Chame um revisor que não executou o passo** — um subagente, de preferência do modelo mais forte, ou uma sessão
   separada —, com os caminhos do plano e do que foi entregue. Ele confere o entregue contra o `## Pedido` e a
   Cobertura, e as evidências contra o disco; revisa isolado, e não corrige: quem executou não revisa o que executou.
2. **Confira e faça a rodada dos achados**: refaça a evidência de cada achado antes de levá-lo. O que não se sustenta
   vai à rodada com `→ falso` como opção recomendada, o porquê e a evidência que o derruba — quem executou o passo não
   derruba sozinho achado sobre o próprio trabalho. Cada achado ganha o destino, escolhido por Anderson, com as opções
   e o custo.
3. **Reserve o número e grave o parecer** com `brza note review-open <slug> --title "<título>" --description "<frase>"`,
   numa nota `work/reviews/REV-NNN-<slug>.md`, com H1 `# REV-NNN: …`, e a linha dela em `## Revisões` do `PLN`; no
   worklog, na revisão abaixo do plano aceito. Achado com destino `corrigido aqui` vira passo novo; o resto vai para a
   casa dona — uma issue, uma decisão, a norma do `brza-studio`.
4. **Casos manuais**, quando algum critério só se prova em aparelho: escreva os `C` a partir do critério, peça a quem
   tem o aparelho, e grave o Observado numa linha com o veredito.

**A forma do achado**, que o checador confere (`finding-without-evidence`):

```markdown
### A1 — Título que enuncia o defeito

> tipo · gravidade · confiança 90 · → destino

**Evidência:** `arquivo:linha` ou o comando e o resultado, refeitos nesta revisão.

### A2 — Título que enuncia o defeito suposto

> tipo · gravidade · confiança 95 · → falso

**Por que é falso:** numa oração, o que derruba a hipótese.

**Evidência:** `arquivo:linha` ou o comando e o resultado que a derrubam.
```

O `tipo` diz o que é (`bug`, `desvio`, `lacuna`); a `gravidade`, o peso (`importante`, `sugestão`) — no falso, o que
ele teria se fosse real; a `confiança`, de 0 a 100, a chance de o achado ser real depois de verificado — 90 ou mais por
comando ou leitura direta, de 80 a 89 com a premissa escrita na evidência; no falso, a de ele ser falso; o `destino`,
para onde vai: `corrigido aqui`, `issue <nota>`, `decisão <nota>`, `descartado`, com o porquê, ou `falso`. **`falso`
não é `descartado`:** o descartado é real e não vale o conserto; o falso parecia defeito e não é, e fica no parecer
para a próxima revisão não o reabrir.

**Abaixo de 80 o achado não entra no parecer.** O revisor verifica até subir ou deixa de fora, e a dúvida que importa
vai à rodada como pergunta, não como achado. A confiança é do revisor e não muda na rodada; o destino, sim.

A revisão fecha quando todo achado tem destino. Então vem o fechamento.
