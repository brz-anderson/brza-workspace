---
name: project-pln-004-r10-r12-recusas
description: PLN-004 R10–R12 (2026-11-02/03): as recomendadas que Anderson recusou (local→pacote, núcleo→measure_runtimes, auditar o delegate→hooks, mapa por inferência→medir) e o critério provável
metadata:
  type: project
---

Nas R10–R12 do PLN-004 Anderson recusou quatro recomendadas da sessão, sempre sem dar o porquê:
- **R10.1:** arquivos locais do workspace (recomendado, "se paga agora") perderam para o pacote `packages/runtimes` do
  `brza-workflow`, que eu tinha posto como "se paga com um segundo workspace".
- **R10.4:** os modos no `measure.py` do núcleo perderam para um `measure_runtimes.py` no pacote.
- **R11.3:** auditar a devolução do `brza delegate` (~40 linhas) perdeu para hooks nativos nos dois runtimes (~140
  linhas), depois de ele pedir "meça a opção 2".
- **R12.2:** o mapa foco → runtime por inferência perdeu para "medir antes" (9 + 6 revisões, ~US$ 25); com a medição,
  ele aceitou a recomendada (Claude padrão, os outros como segundo passe).

**Why:** o padrão é o mesmo das memórias [[feedback-mecanismo-nativo-do-runtime]] e [[feedback-medir-antes-de-desenhar]]:
ele paga código e sonda para ter o mecanismo nativo (hook, pacote reusável) e fato no lugar de inferência, e não
escolhe pelo menor custo de agora. O pacote isola o que é de runtime do núcleo comum, mesmo com um workspace só.

**How to apply:** ao desenhar o que é de um runtime, recomende o lugar que não contamina o núcleo (pacote, arquivo à
parte) e diga o custo de tocar o núcleo (uma entrada no `golden_differences.py` por edição de texto). Quando a
recomendada repousa em inferência de qualidade, ofereça a medição com custo, e espere que ela ganhe.

**Custo que estimei errado (2026-11-03):** a sessão marcou o mapa `pro`/`flash` do `agy` como "sem base" porque o
`agy models` não lista esses nomes; a sonda sem turno (`agy --settings '{"trustedWorkspaces":[…]}' agents`) mostrou que
o frontmatter do papel só aceita `pro`, `flash`, `inherit` ou nada, e descarta calado o nome completo. Antes de julgar
um nome, confira o validador da superfície certa (o papel ≠ o `--model` da chamada). Outra armadilha: o `tests/cli` do
`brza-workflow` só passa com `env -u BRZA_WORKSPACE` (20 falhas com a variável da sessão).
