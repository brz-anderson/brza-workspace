---
name: achados-que-costumam-cair
description: Hipóteses de revisão que pareciam achado e caíram ao verificar — limiar "sem lastro" que está no texto da opção, terreno que existe, despacho brza que funciona
metadata:
  type: feedback
---

Hipóteses que caíram na revisão do PLN-009 (2026-11-03), com a confiança que eu teria dado sem verificar:

- **"Limiar sem lastro" que está no texto da opção recomendada** (~90 antes de ler): o 55%/90% vinha da opção da R7.1
  ("55% e 90%, como no `quota.py`"), e a linha "Decidido" não repete o número. Ler a opção inteira, não só o "Decidido".
- **"Endpoint ou comando não existe"** (~70): `/v1/systemone` respondeu 400 "model is required" sem carregar modelo;
  `orca account list --json` traz `usedPercent`/`resetsAt`. Sondar com chamada barata antes de afirmar.
- **"`brza <sub>` não chega ao `brza-<sub>`"** (~75): o `brza` do PATH é o shim do BrzA Studio, que despacha; o
  "Unknown command" só aparece quando o `brza-<sub>` não existe. Teste com um `brza-*` que existe (`brza where --help`).

**Why:** cada um teria entrado como achado importante e sido refutado pela sessão principal em um comando.
**How to apply:** nesses três formatos, rodar o cheque antes de pôr confiança; o que cair vai como `→ falso`.
Relacionado: [[padroes-de-erro-em-planos-extraidos]].
