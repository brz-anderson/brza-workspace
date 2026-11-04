---
scope:
  - workspace
refs:
  - PLN-005
  - PLN-006
  - issue:o-coordenador-le-o-indice-da-master
---

# PLN-006: a abertura do brza init

Anderson perguntou, na sessão `workspace`, se já havia mecanismo "para inicializar a norma inteira, com AGENTS CLAUDE
plans/ wiki/ work/ skills/ agents/ num repositório do zero". Não havia, e ele pediu o plano:
[PLN-006: O `brza init` monta a norma num workspace do zero](../../plans/PLN-006-o-brza-init-monta-a-norma-do-zero/PLN-006-plan.md).

## O que se levantou

- As peças de hoje — `brza note workstream`, `memory-setup`, `new`, `sync`, `brza install`, o `notes-checker` — só
  operam dentro do `brza-workspace` já montado.
- Os caminhos do par workspace/código estão fixos em `brza_runtime.py`, na função `claude` do `~/.zshrc` e no
  `claude-brza`.
- Umas 250 linhas, em ~40 arquivos da `master`, citam o que é local; a separação genérico/local custa ~4–6 h em
  qualquer caminho.

## O que se decidiu

A R1, toda na recomendada: o plano é o `PLN-006`, no `workspace`; o alvo é um workspace ao lado do código, como o par de
hoje; o mecanismo é um `brza init` determinístico; e a norma genérica acompanha a daqui por sync. O número subiu na
`master` em `0310bb4`.

O `collector` levantou o Terreno: o que é genérico e o que é local em cada arquivo, o acoplamento em código e o sync de
hoje. A sessão conferiu cinco fatos por amostra, todos de pé. Um deles contradiz o `CLAUDE.md:3-4`: pela documentação,
com `AGENTS.md` e `CLAUDE.md` juntos o Claude Code carrega só o `CLAUDE.md`. Fica para o Desenho conferir.

A R2 e a R3, todas na recomendada, menos a R2.1, respondida "repo brza-workflow" e confirmada na R3.1:
- o núcleo mora em `brz-anderson/brza-workflow`, público, e o próprio `brza-workspace` o consome pelo sync;
- a parte local se separa por placeholders e um `.brza/workspace.toml`, com as seções inteiramente locais em arquivo
  próprio;
- o núcleo leva a norma, as skills, os agents, o `brza note` e os hooks parametrizados; o CLI roda do checkout do
  `brza-workflow`, e os scripts do `brza-studio` ficam locais;
- a raiz sai do cwd, pelo manifesto; a branch e o remote também vêm do manifesto, com `master` e `origin` por padrão; a
  identidade vem por flags, com o padrão do `git config`.

## O desenho e as rodadas 4 a 6

O `designer` rascunhou D1–D12 e P1–P8 (~21,5 h), em `/private/tmp/pln006/desenho.md`. A sessão conferiu três fatos:
os hooks não importam o CLI; o `AGENTS.md` só carrega junto do `CLAUDE.md` pela opção de usuário desta máquina, e o
`CLAUDE.md:3-4` está impreciso nisso; nenhum Markdown da norma usa `{{`.

Duas respostas saíram da recomendada:
- **R4.1:** o repositório de código acha o workspace por um registro em `~/.config/brza`, e não pelo `git config`.
- **R4.3:** o contador de PLN vira um índice JSONL na `master`. A R5 o fechou: planos, issues e decisões; só
  acrescenta, com `merge=union`; gravado pelo `brza note`. O coordenador que o lê foi à issue
  [O coordenador se baseia no índice de notas da master](../issues/o-coordenador-le-o-indice-da-master.md).

O resto da R4 e a R6 inteira na recomendada: os scripts do `brza-studio` como camada local; `@AGENTS.md` no
`CLAUDE.md`; `{{tabela.chave}}` por regex; o sync recusa o arquivo editado; segue a branch, com o sha no lock; a
migração em estágios.

## O fechamento do desenho e o aceite

A revisão do `designer` com a R4–R6 abriu cinco pontos de detalhe do registro e do índice, e o rascunho trazia três
escolhas marcadas "sem lastro" que não tinham ido à rodada. A R7 e a R8 fecharam os oito, todos na recomendada: o
registro guarda o par raiz + código, pelo `brza register`; o índice é `.brza/index.jsonl`, com um campo `description`
no frontmatter e a linha levada à `master` por commit sem checkout; o id de issue e decisão é `kind:slug`; o workspace de origem sai
do núcleo; a medição datada fica como o porquê; a exceção ao índice vai numa decisão nova.

O Desenho foi ao `PLN-006-design.md` (D1–D12, 580 linhas), e os Passos, P1–P9, somam 27 h. Na R9, Anderson aceitou o
corte: "aceito e pode iniciar os passos em paralelo". O P1 começou.

## A execução, P1 a P7

Cada passo foi a um `implementer`, num worktree próprio do `brza-workflow`, e a sessão conferiu as suítes, commitou e
fez o merge. A ordem das levas mudou duas vezes, porque o parser TOML do P2 serve ao P3 (X7) e o `brza init` chama a
camada 1 do sync (X17): P1; P2 e P4; P3 e P7; P6; P5.

Depois da R10, Anderson pediu: "o restante dos passos, escolha sempre o recomendado, até o fim desse plano, vamos medir
o resultado". As R11–R16 — 31 escolhas que o desenho não fixava — foram decididas assim, cada uma gravada com as opções
e o preço.

No fim do dia, o `brza-workflow@b9210a6` tinha:
- **o núcleo:** a norma em molde, o manifesto, o lock e o render, com um teste de ouro contra a `master` daqui;
- **o CLI:** a raiz pelo cwd e pelo registro, o índice da `master`, o `brza sync`, o `brza init` e o `brza install`
  com o pacote do cliente;
- **as suítes:** 372 testes de CLI e 244 de hooks, estes também no Python 3.9.

A fumaça do `brza init` montou um workspace num diretório temporário, com o checador verde.

Sobrou o "O pedido de Anderson" no `bin/brza-note:117` (X26), para a revisão do P9. A `master` daqui também andou dois
commits do PLN-005 depois da cópia, que o P8 precisa portar antes de migrar.

## Fora do workspace

- **O repositório `brz-anderson/brza-workflow`, público, no GitHub**, criado pelo `gh repo create`, e o checkout dele
  em `~/Projects/brza-workflow`, com o `origin` em `git@personal:brz-anderson/brza-workflow.git`. **Risco:** o que for
  ao push fica público; o núcleo não pode levar nada pessoal (R2.2, R8.2). **Estado:** ativo; o P1 o povoa. **Como
  desfazer:** `gh repo delete brz-anderson/brza-workflow` e apagar a pasta.
