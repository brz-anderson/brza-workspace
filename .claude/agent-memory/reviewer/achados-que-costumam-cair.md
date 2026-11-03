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
- **"`KeepAlive: {'SuccessfulExit': False}` faz o launchd reiniciar serviço após `bootout`"** (~80): o `bootout`
  descarrega o job da tabela do launchd; o KeepAlive só opera enquanto o job estiver carregado.
- **"Apagar o plist antes de descarregar quebra o `launchctl bootout`"** (~85): o `bootout` recebe o identificador lógico
  do serviço (`target()`, `gui/<uid>/<label>`), e não o caminho físico do arquivo plist.


- **"O teste passa sem a espera"** (~70, P8 do PLN-009): o `assertGreaterEqual(prints, 4)` parecia frouxo, mas o
  `assertFalse(is_loaded())` logo depois barra; a mutação sem o laço falhou em 3 testes. Mutar antes de afirmar.
- **"Teste novo de regressão deve falhar contra o código antigo"** (~80 antes de verificar, R2 do P8): quando o teste cobre
  guarda contra mutação em funcionalidade nova (ex.: não mencionar plist no CLI sem plist órfão) ou comportamento que o
  código anterior já fazia por outro motivo (reter plist em erro genérico de bootout), ele passa no código antigo e só falha
  contra o mutante do código novo. Provar a guarda por mutação na implementação nova, e não esperar falha no código antigo.

**Why:** cada um teria entrado como achado importante e sido refutado pela sessão principal em um comando.
**How to apply:** nesses três formatos, rodar o cheque antes de pôr confiança; o que cair vai como `→ falso`.
Relacionado: [[padroes-de-erro-em-planos-extraidos]].
