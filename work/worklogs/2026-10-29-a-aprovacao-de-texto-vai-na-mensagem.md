---
scope:
  - workspace
---

# A aprovação de texto vai na mensagem, e não na caixa de perguntas

O pedido de Anderson, em 2026-10-29, na sessão `pln-002-sessions-rename`, no Fechamento do PLN-002: "o texto não está
aparecendo no chat, pra mim poder ler pra decidir"; depois, "a rodada de decidido das notas que hoje vem em caixa de
perguntas, deve passar a ser assim como vc fez agora" e "ajuste a norma do workspace".

## O que se fez

- **O que aconteceu:** o texto da nota da PLN-002/R13.4 foi escrito antes de uma chamada ao `AskUserQuestion`; no chat
  do BrzA Studio, a caixa o escondeu, e a resposta "Decidido, pode gravar" veio sem o texto lido. O commit do Fechamento,
  ainda sem push, foi desfeito, e o texto foi mostrado de novo na mensagem, com as opções numeradas.
- **A norma:** o `AGENTS.md`, em "Decisões pendentes vão em rodadas de perguntas", ganhou o item "A rodada que aprova um
  texto vai na mensagem, e não na ferramenta", aprovado com "1.1", na mensagem, à opção "Decidido, pode aplicar
  (Recomendado)".
- **A memória do Claude Code** ganhou a mesma regra, para valer antes de a norma ser relida.

## Fora do workspace

- **A memória `aprovacao-de-texto-em-mensagem-e-nao-na-caixa`.**
  - **O quê e onde:** um arquivo novo em `~/.claude/projects/-Users-andepb-Projects-brza-workspace/memory/` e a linha
    dele no `MEMORY.md` dali.
  - **O risco:** nenhum; repete a norma do `AGENTS.md`.
  - **Estado:** ativo.
  - **Como desfazer:** apagar o arquivo e a linha do `MEMORY.md`.
