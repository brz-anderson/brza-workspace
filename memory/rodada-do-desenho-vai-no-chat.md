---
name: rodada-do-desenho-vai-no-chat
description: "A rodada que fecha os pontos do Desenho de um plano vai na mensagem, em texto, sem AskUserQuestion"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 330bdc33-f82d-4dba-94d9-2b924664eb99
  modified: 2026-10-31T01:52:28.161Z
---

A rodada do Desenho de um plano vai no chat, no formato de rodada sem a ferramenta: pergunta, opções numeradas,
recomendação marcada e `Custo: … Se paga: …` em cada opção. É o mesmo tratamento da rodada que aprova o texto de uma
decisão.

**Why:** Anderson pediu em 2026-10-30, no PLN-004: "faça a rodada no chat, igual a de decisão, sem a ferramenta de
pergunta". O Desenho tem artefato escrito e alternativas lado a lado, e a caixa da ferramenta esconde o texto que
precisa estar à vista para escolher.

**How to apply:** nas rodadas de Desenho (itens `D`, alternativas), ponha na mensagem o rascunho ou o trecho que importa
e as perguntas em texto. As rodadas curtas da Entrevista continuam na `AskUserQuestion`. Se o mesmo pedido vier para
outras rodadas, a regra sobe para a norma do `AGENTS.md`.
