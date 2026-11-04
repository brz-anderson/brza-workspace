---
name: anderson-prefere-cobertura-uniforme
description: No PLN-013 (runtimes no MCP), Anderson recusou três recomendadas de corte mínimo e escolheu cobrir os runtimes por igual, pagando as horas a mais
metadata:
  type: feedback
---

No PLN-013 (2026-11-03), Anderson recusou três recomendadas que cortavam o alcance por runtime, e escolheu a opção
que cobre todos por igual, mesmo com mais horas:

- **R1.3:** a recomendada era a tabela com Claude e Grok e os outros depois (+0,5 h); ele escolheu "Os três juntos"
  (+2 h).
- **R2.2:** a recomendada era o `--rename` e o `--wait` só no Grok; ele escolheu "Nos três" (+3 h), mesmo com 1
  abertura de cada desde 2026-10-29.
- **R3.1:** a recomendada era a política só no `claude` e o padrão do runtime nos outros (~1 h); ele escolheu a
  tabela `policy.roles.<papel>.<runtime>` (~2,5 h).

Ele aceitou as recomendadas de forma e de ordem (entregas, sondas, gate da troca de conta).

Na R4 (mesmo dia), "todos recomendados, siga". A minha coluna Grok da tabela de modelo (`grok-4.7` em
`low`/`medium`/`high`) perdeu para a da segunda revisora, uma sessão Grok (`low`/`high`/`xhigh`): todo modelo Grok já
nasce em `high`, então o executor em `medium` ficava abaixo do padrão do próprio runtime. O revisor que é o runtime
leu o `~/.grok/models_cache.json`, que eu não abri.

**Why:** o argumento do "uso baixo hoje" (1 abertura, nenhum modelo por papel) não pesou: ele quer o fluxo igual nos
runtimes, e não um caso especial por runtime que volte depois.

**How to apply:** em desenho multiruntime, não recomende cortar runtime por uso baixo; recomende a cobertura igual e
corte pela ordem das entregas. O argumento de frequência de uso, sozinho, cai. Para valores de esforço, parta do
padrão do runtime (o `default` do cache de modelos dele) e escale a partir dali. Ver [[anderson-criterios-medicao]].
