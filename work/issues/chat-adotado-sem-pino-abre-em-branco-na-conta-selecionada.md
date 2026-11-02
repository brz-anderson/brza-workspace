---
status: open
description: Um chat do Claude adotado sem pino (importar chat do CLI) cujo transcript está noutra conta que a selecionada abre uma sessão vazia, sem aviso, porque o handle adotado nasce sem `leafUuid`.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - chat
  - auth
---

# Um chat adotado sem pino abre em branco na conta selecionada

Achado da sessão `pln-001-pedido-39-fork`, ao conferir o D57 no P74, em `brza-studio@563705a7aaf`. É o **mesmo caminho
silencioso** da issue
[O fork de um chat fixado abre na conta global e sem o contexto](o-fork-de-um-chat-fixado-abre-na-conta-global-e-sem-contexto.md),
que o P74 fecha só para o fork. Aqui fica o que o P74 não cobre.

## O defeito

1. A adoção (`resolveStructuredAgentSessionAdoptionForCreate`, `structured-agent-session-create-adoption.ts`) acha o
   transcript em qualquer conta candidata e grava o `accountHome` dela no registro. O handle nasce sem `resumeCursor`
   (`structuredAgentSessionAdoptAttach`), então o `leafUuid` é nulo.
2. O lançamento segue a seleção global, e não o `accountHome` do registro, quando o chat não tem `accountSwitch`
   (`structured-session-account-home.ts`, `claude-structured-launch-resolution.ts`).
3. Com o transcript fora da conta selecionada e o `leafUuid` nulo, `claudeLaunchResumesTranscript`
   (`claude-structured-launch-home.ts`) devolve `false` **antes** da checagem de `historyInOtherAccount`, que só roda com
   `leafUuid`. O lançamento abre `sessionId: <id>` — uma sessão nova e vazia — em vez de `resume`.

**O efeito:** o chat importado mostra o histórico (que vem da importação), mas o agente não sabe nada dele, e o uso cai
na conta selecionada. Nada avisa.

## O que não se sabe

**Não rodei o import de um chat do CLI de outra conta ponta a ponta.** O que está provado é o elo do lançamento (o teste
do `reviewer` e o do P74 exercem `claudeLaunchResumesTranscript` com handle sem cursor); que o import do CLI deixa o
`accountHome` fora da seleção foi lido nos candidatos, não rodado.

## O que resolve

Duas saídas, ambas dependem de uma decisão de Anderson (é comportamento novo para o import, fora da R65.1):
- **Pinar o chat importado à conta onde o transcript está**, como o P74 faz com o fork: o `accountSwitch` nasce do
  `adoption.accountHome` quando ele difere da seleção. Custo: o pino na adoção do import e o divisor "Conta trocada".
- **Avisar em vez de abrir em branco:** com `leafUuid` nulo e o transcript em outra conta, lançar o
  `historyInOtherAccount` (o chat pede a troca de conta) em vez de devolver `false`. Custo: uma checagem a mais no
  `claudeLaunchResumesTranscript`, sem pino.
