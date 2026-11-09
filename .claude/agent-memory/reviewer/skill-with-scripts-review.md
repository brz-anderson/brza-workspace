---
name: skill-with-scripts-review
description: Onde erram as skills do playground que trazem scripts com contrato JSON entre si (meeting-runner, 2026-11-08), e quais hipóteses de revisão costumam cair
metadata:
  type: project
---

Na revisão da `meeting-runner` (tally → estado-rN.json → panel; wait_round sobre o `brza orchestration`), o erro real
morou em cinco lugares, todos achados por comando e não por leitura:

- **Dois scripts calculam o mesmo número, ou leem o mesmo arquivo, de jeitos diferentes.** O tally e o painel davam
  médias da sala diferentes a partir do mesmo JSON. O molde do `sintese-N.json` aninhava `sala.revisor`, e um dos
  leitores só lia o nível de cima. Rode os dois sobre o mesmo insumo e compare a saída.
- **O molde muda, e quem o consome não acompanha.** O pedido passou de "prazo" a "duração", e o painel seguiu lendo
  `(prazo: …)`. Os testes passaram porque a fixture ainda era do molde velho. Alimente cada parser com o molde
  **atual** da reference.
- **O comando do SKILL.md com caminho relativo e `--root` = cwd.** De um dos diretórios plausíveis, o comando quebra; de
  outro, responde "todos falta" com rc 0. Rode cada comando como está escrito, da raiz, da pasta do artefato e do
  diretório da skill.
- **Parâmetro opcional que muda o significado do número.** Sem `--opened/--closed`, o "custo da rodada" virava o da
  sessão inteira, e o painel nem tinha a flag. Procure flag opcional que tira a janela ou o filtro.
- **A leitura tolerante de um formato não sondado falha em silêncio.** A atribuição por nome em qualquer string pegou
  a persona errada (nomes que são palavras comuns). A chave de dedupe incluía um id de lote. A caixa vazia sem Run
  ligado dava `ok`. A `--help` do CLI instalado (`brza orchestration <verbo> --help`) é a fonte barata, e muitas vezes
  já contradiz o script: `worker-release` só vale para worker settled; `--terminal` pede `--worktree`; `worker_done`
  sem `--to`.

**Nos testes:** procure `except Exception: skipTest` e teste cujo invariante outra linha do código já garante (o teste
de dedupe passava sem a dedupe). O aceite "contra o gabarito" costuma conferir só as colunas fáceis; confira se a
medição (latência, custo) entra.

**Hipóteses que caíram (não gastar confiança alta):** XSS no HTML gerado (escapava tudo), `shell=True`, o teto de
512 KB, `:root` no tema, laço infinito, a mensagem de rodada antiga contando na nova (havia o `m < n`), a corrida
entre a escrita parcial e o marcador na última linha.

**Why:** a skill nasce de protótipos de scratch, e cada script é endurecido em separado; o contrato entre eles e os
moldes das references é o que ninguém roda junto.
**How to apply:** em toda revisão de skill com `scripts/`, rode os comandos do SKILL.md como estão escritos, passe o
molde atual de cada reference pelo parser e compare os dois consumidores do mesmo JSON, antes de ler o mérito.

Ver também [[meeting-plan-review-patterns]].
