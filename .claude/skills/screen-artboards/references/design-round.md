# A rodada de Desenho com alternativas de tela

Quando o Desenho de um plano (`plan-runner`, `references/design.md`) tem opção que muda o que se vê, a rodada leva a tela
de cada alternativa, porque escolher layout pela descrição é escolher às cegas.

1. **Um artboard por alternativa**, com a letra da opção (`--letter A`, `B`, `C`) e um rótulo curto no `--title`. Mesma
   plataforma, mesmo pacote, mesmo `--scheme` e o mesmo conteúdo de exemplo em todas: a diferença entre os artboards tem
   de ser só a da alternativa.
2. **Confira cada um pelo PNG** (`artboard.py shot`) e corrija antes da rodada.
3. **A mensagem**, em texto e no formato sem a ferramenta: para cada alternativa, a linha `::orca-visual`, e logo abaixo
   o custo, quando se paga e o que reabre; depois a tabela lado a lado e a recomendação marcada. A caixa da pergunta com
   opções esconderia os artboards.
4. **Depois da escolha**, `artboard.py promote <artboard da escolhida>.html --plan PLN-NNN --name <assunto>` grava o PNG
   na pasta do plano e imprime o link para o item `D` (`- **Protótipo:** ![…](PLN-NNN-<assunto>.png)`). Para uma
   issue, `--issue work/issues/<nome>.md`, e o PNG fica ao lado dela, como `<nome>-<assunto>.png`. As que perderam ficam no scratch.

Mais de 8 artboards numa rodada (3 alternativas × 3 estados, por exemplo) é sinal de rodada grande demais: divida por
estado ou por tela.
