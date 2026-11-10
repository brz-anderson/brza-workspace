# O pedido do passo e o protocolo de fim do executor

O pedido é o único contexto do executor: ele não lê o plano inteiro, não tem a conversa com Anderson e não pode
perguntar. Por isso o pedido carrega o que o passo precisa, citado, e o protocolo que diz quando e como ele termina. O
`step_request.py` monta o pedido do plano; esta reference diz o que ele contém e por quê, para conferir antes de abrir.

```bash
python3 -I .claude/skills/plan-runner/scripts/step_request.py PLN-NNN P<n> --out .sessions/pln-nnn/P<n>/pedido.md \
  --worklog work/worklogs/AAAA-MM-DD-pln-nnn-p<n>-<assunto>.md --checkout <caminho> --branch <tipo>/pln-nnn-p<n>
```

O `executor.py open` chama o script sozinho; rode à mão só para ler o pedido antes de abrir. Ele recusa (saída 1) o
passo sem `Executa D…` num plano com Desenho e o `R` citado que a Entrevista não tem: o executor que recebe uma
referência quebrada inventa o que falta.

## O molde

```markdown
Você executa o passo P3 do PLN-021 numa sessão aberta pela coordenação. Não acione a skill `plan-runner`: você não
conduz o plano, executa um passo dele.

## O passo
<o ### P3 inteiro, copiado do plano: título, Executa, Estimado, subpassos>

## O que o Desenho fixou
<o texto de cada D citado no "Executa", da Origem ao Em aberto>

## O que as rodadas decidiram
<cada R citado na Origem dos D: a pergunta, a opção escolhida e a resposta literal>

## Restrições e Regressão
<as do plano, copiadas>

## Onde trabalhar
- checkout: <caminho absoluto> (branch <tipo>/pln-nnn-p3)
- worklog: <caminho absoluto do worklog do executor, no workstream>

## Regras
- Não grave o plano, não commite nada no brza-workspace, não pergunte a Anderson.
- Commite na branch do passo quando os testes do que você tocou passarem; não faça merge nem push.
- Desvio local: registre no worklog como `X` proposto e siga. Desvio que muda o contrato de um D: pare, registre e
  feche com `parado`.

## O fim
1. Preencha `## Evidência` no worklog, uma linha por item:
   - `commit: brza-studio@<sha7>`
   - `comando: \`<comando>\` → <resultado> (≤ 2 min)` quando roda em até dois minutos
   - `arquivos: <caminho>, …`
   - `desvios: X? — <uma linha>` ou `desvios: nenhum`
2. A última linha do worklog é `<!-- fim-P3: feito -->` ou `<!-- fim-P3: parado -->`.
3. Envie o status do protocolo que vem abaixo deste pedido. Não envie `worker_done`: a coordenação pede o encerramento.
```

## Por que cada parte

- **"Não acione a skill `plan-runner`"** — sem isso, o executor lê "PLN-021" e passa a conduzir o plano, gravando-o. A
  descrição da skill tem o mesmo gatilho negativo.
- **O passo, os `D` e as rodadas copiados, não linkados** — o executor que segue link lê o plano inteiro e decide pelo que
  achou, inclusive o que ainda está em aberto. A cópia é o recorte que vale.
- **O commit na branch do passo** — sem ele, o executor para esperando confirmação e a sessão fica parada; o ponto
  irreversível é o merge, e esse continua com Anderson (PLN-021/R5.1, confirmada).
- **A evidência no worklog do executor, e não no plano** — a coordenação é a única que grava o plano; o worklog é o
  registro que a norma já pede a toda sessão, e o marcador no fim dele é o que o `wait --marker` lê (PLN-021/R4.2).
- **`(≤ 2 min)`** — marca o comando que a coordenação roda de novo para conferir; teste longo fica pela palavra do
  executor e pelo commit.
- **Sem `worker_done`** — ele encerra a sessão, e a sessão encerrada fecha sozinha em ~2 min; a coordenação ainda pode
  precisar mandar a correção da evidência. O protocolo do status da rodada vem anexado pelo `brza sessions`, com os ids
  reais; o pedido não traz comando de mailbox próprio.

## O worklog do executor

O `executor.py open` cria `work/worklogs/AAAA-MM-DD-pln-nnn-p<n>-<assunto>.md` no workstream, com o frontmatter da
norma (`scope`, `tags`), o H1 "PLN-NNN P<n>: <título do passo>", as seções `## O que se fez`, `## Desvios` e
`## Evidência` vazias e sem o marcador. O executor o preenche; a coordenação o commita com o plano quando aplica a
evidência.
