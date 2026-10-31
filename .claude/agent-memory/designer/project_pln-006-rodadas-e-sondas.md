---
name: project-pln-006-rodadas-e-sondas
description: No PLN-006 (brza init) Anderson aceitou as 11 recomendadas de R1–R3 pelo "se paga no segundo workspace"; e duas armadilhas de evidência que o Terreno não pegou
metadata:
  type: project
---

Nas rodadas R1–R3 do PLN-006 (2026-10-31), Anderson escolheu a recomendada nas 11 perguntas; a R2.1 veio em texto
livre só para dar o nome do repositório (`brza-workflow`). O critério que se repetiu nas opções aceitas foi o "se paga
no segundo workspace / no primeiro init", contra opções de custo zero que "se pagam nunca".

**Why:** sinal de calibração: com o custo e o "se paga" escritos, ele não reabre; a divergência aparece como nome ou
detalhe, não como troca de opção.

**How to apply:** no Desenho do PLN-006, não reabrir R1–R3; ponha a recomendada com o "se paga" numa fase nomeada.
Duas armadilhas achadas no Desenho, que valem para qualquer porte da norma:
- o `CLAUDE.md` "lê o `AGENTS.md` junto" só porque a opção `claude-md-and-agents-md` está no `~/.claude/settings.json`
  desta máquina; a doc ignora essa chave nos settings de projeto. Confira a configuração de usuário antes de tomar o
  comportamento do repositório como dado;
- os hooks rodam no Python 3.9 do sistema (sem `tomllib`), e o CLI não; sonde com `/usr/bin/python3` antes de pôr
  biblioteca nova no hook.
Ver também [[feedback-medir-antes-de-desenhar]] e [[feedback-mecanismo-nativo-do-runtime]].
