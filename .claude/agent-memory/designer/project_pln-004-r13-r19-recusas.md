---
name: project-pln-004-r13-r19-recusas
description: PLN-004 R13–R19 (2026-11-03/06): o que Anderson trocou da recomendada (high no Codex, .brzAgents, medir antes no Grok, a sessão aplica o ~/.zshrc) e os custos/fatos que o v2 errou ou deixou envelhecer
metadata:
  type: project
---

Nas R13–R19 do PLN-004 a maioria saiu na recomendada; as trocas foram:
- **R14.2:** aceitou a opção 1, mas com o revisor do Codex em `high`, não `xhigh`, sem dizer o porquê — a variante
  que eu tinha deixado de fora por não ter custo medido.
- **R15.3:** respondeu com contraproposta estrutural (`agents`/`skills`/`memory` em `.brzAgents/`), e a R16 a mediu; na
  16.1 escolheu a literal contra a recomendada, e na 16.5, com a medição da sessão interativa, voltou à recomendada.
- **R19.3:** "medição primeiro" antes de escolher modelo do Grok; com o banco, aceitou a recomendada mais barata.
- **R17.3:** "a sessão aplica tudo" (o `~/.zshrc` também), contra a minha "Anderson aplica" — menos passo manual, com o
  "pode aplicar" no passo e o desfazer no worklog.

**Why:** o critério segue o de [[project-pln-004-r10-r12-recusas]] e [[feedback-medir-antes-de-desenhar]]: fato medido
antes de escolher, e ferramenta neutra entre runtimes; quando a variante cara não tem medida, ele escolhe a do meio por
conta própria. Na máquina, prefere que a sessão faça, desde que peça e registre.

**How to apply:** ofereça a variante intermediária com custo honesto em vez de cortá-la; para arquivo de usuário,
recomende "a sessão aplica depois do pode aplicar, com o desfazer no worklog".

**O que o v2 errou ou deixou envelhecer (2026-11-06):**
- escrevi que o `guard_workspace` e o `commit_and_push` do sync "não mudam" com o link; mudam na transição de diretório
  para link (`git add` através do link falha). Ao propor link `120000`, sonde a transição, não só o regime.
- o `brza sessions --agent` (o D12) já tinha sido entregue por um plano de outro workstream (PLN-013, `tools-kit`)
  entre o v2 e o v3. Antes de reescrever um D que toca código comum, rode `git log` do arquivo no `brza-workflow` e
  procure o arquivo nos planos dos outros workstreams.
- o `agy` foi de 1.4.12 a 1.5.2, e o `agy agents` deixou de listar papel de projeto; o `brza-studio` andou 854 commits
  durante a escrita, com os arquivos mudando de pasta. Cite a versão e o commit junto da linha, e reconfira no fim.
