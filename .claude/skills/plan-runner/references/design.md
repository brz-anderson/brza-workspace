# Desenhar — o Terreno, os itens `D`, as alternativas e a rodada

O Desenho é o que o plano vai executar, escrito antes: o contrato em código, o texto da norma, a tela. Ele existe para
que a escolha entre caminhos aconteça com o artefato à vista, e não depois, no código, quando custa refazer.

**Confira o gatilho** — o molde lista as condições que abrem o Desenho: bifurcação que precisa ser vista para ser
escolhida, mudança que toca mais de uma parte do app, remodelagem do que já existe. Sem Desenho, a ordem dos passos é a
do pedido, e o plano segue para Planejar (`references/open-and-plan.md`).

1. **Peça o Terreno a um `collector`**, que devolve o que existe — a norma, o código, o que outros trabalhos já
   decidiram — com fonte (`arquivo:linha`) e os arquivos essenciais, e grava o agregado no scratch. Ele não grava nada
   no repositório.
2. **Peça os itens `D` no molde, com o artefato escrito**, a um `designer`, no laço de `references/consultants.md`.
   Bifurcação com 3 ou mais alternativas defensáveis abre consultores com foco; **se a escolha também é cara de
   reverter** — contrato entre partes, formato de dado gravado, norma —, eles abrem **em sessões**, em modelos e runtimes
   diferentes (PLN-021/R2.3). Narre o gatilho numa linha antes de abrir.
3. **Leve as alternativas a uma rodada na mensagem, em texto**, no formato sem a ferramenta, lado a lado sobre os mesmos
   casos, com a tabela, a argumentação de cada consultor e a recomendação marcada: a caixa da pergunta com opções
   esconde o artefato que precisa estar à vista para escolher. Quem escolhe é Anderson.
4. **Opção que muda o que se vê vem com a tela à vista**: aciona a skill `screen-artboards`, um artboard por
   alternativa, com a letra da opção no `title` ("A — …"), na plataforma do pedido — janela macOS ou Windows para o
   desktop, iPhone ou Android para o mobile, navegador nas larguras do web —, com o pacote de tokens do projeto. **Confira
   cada artboard pelo PNG** (`artboard.py shot`) antes da rodada: a coordenação não vê o chat, e coluna estourada ou
   texto cortado só aparece na imagem. Até 8 visuais por resposta.
5. **Grave o vigente**, com a origem de cada item, e a rodada pelo `round_log.py`. A alternativa que perdeu fica até o
   passo que a transcreve e então sai, com uma linha **Descartada** e o porquê. No `PLN`, a crítica posterior vai para a
   Entrevista, e o item é reescrito no lugar.
   - **A tela escolhida vira PNG na pasta do plano**, para sobreviver ao scratch: `artboard.py promote <artboard>.html
     --plan PLN-NNN --name <assunto>` grava `plans/PLN-NNN-…/PLN-NNN-<assunto>.png` e imprime o link para o item `D`.
     **A escolhida que vai a uma issue** usa `--issue <caminho>` e deixa o PNG ao lado dela.
6. **Aplique o reverso**: item que vira regra durável do `brza-studio` sai para a norma dele, e o plano cita. Sem isso o
   Desenho vira uma segunda norma.

**O consultor** devolve o Terreno e os itens `D` no molde — a origem de cada item, as alternativas com custo, quando se
paga e o que reabre, cada ponto sem lastro marcado no lugar em que aparece —, e nada vai ao plano sem passar pela
coordenação.

**O `PLN` pode parar aqui** — a proposta que espera decisão: `phase: design`,
`ready: não — aguarda decisão de <quem> sobre D2`. Sai do Desenho ao virar decisão, passos ou norma do `brza-studio`, ou
ao ser rejeitado, com `status: dropped`, `phase: dropped` e a linha do porquê em `## Worklogs`. O plano de worklog não
para no Desenho: ou é aceito, ou não entra em `work/`.

**O Desenho grande** (acima de ~400 linhas no `-plan.md`) vai a `PLN-NNN-design.md`, e o `plan_md.py` dos scripts o lê
junto.
