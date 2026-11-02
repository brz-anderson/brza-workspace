---
status: open
description: Bifurcar a partir de uma mensagem de um chat fixado numa conta (P36) abre o chat novo na conta global, e o Claude começa uma sessão vazia sem aviso.
scope:
  - brza-studio
opened: 2026-11-02
tags:
  - chat
  - auth
---

# O fork de um chat fixado abre na conta global e sem o contexto

Achado do `reviewer` na caçada de achados da v1.4.246, em 2026-11-02, em `brza-studio@384d4b08fd6`. O "Fork from message"
entrou na v1.4.246 (`8eff03d0bb8`); o pino do P36 é do fork, e os dois não se conhecem. O defeito é silencioso, e vem a
par da issue
[O chat fixado numa conta pelo P36 entra na conta global](chat-fixado-na-conta-entra-na-conta-global.md), que é outro
caminho do mesmo pino.

## O defeito

**O cenário normal do P36:** o chat A foi trocado para a conta B no limite de uso (`record.accountSwitch`), e a seleção
global é a conta A. Anderson bifurca uma mensagem desse chat.

1. A cópia do transcript do fork fica ao lado da fonte, no home da conta B (`claude-rewind-transcript.ts:80`).
2. O renderer abre o chat novo só com `resumeFrom`, sem conta nem pino (`native-chat-fork-from-message.ts:56-64`).
3. A adoção grava o `accountHome` de B (`structured-session-create-support.ts:197-229`), mas o handle nasce sem
   `resumeCursor` (`structured-agent-session-create-adoption.ts:233-238`), e o registro, sem `accountSwitch`.
4. No lançamento, o home segue a seleção global (`structured-session-account-home.ts:58-66`) e o recibo falta
   (`claude-receiving-account.ts:38-40`): o Claude sobe na conta A.
5. O transcript não está em A e o `leafUuid` é nulo, então `claudeLaunchResumesTranscript` devolve `false`
   (`claude-structured-launch-home.ts:46-48`) e o lançamento abre uma sessão **nova e vazia** com o mesmo id
   (`claude-structured-launch-resolution.ts:292-294`).

**O efeito:** o chat novo mostra o histórico bifurcado, que vem da importação, mas o agente não sabe nada dele, e o uso
cai na conta global, que pode ser a que bateu no limite. Com o `leafUuid` presente o app avisaria
(`historyInOtherAccount`, `claude-structured-launch-account-routing.test.ts:167`); a adoção não o grava, e por isso aqui
nada avisa.

**O que provou:** um teste temporário no worktree `sync-v1.4.246` (`zz-reviewer-fork-blank.test.ts`, apagado depois; cópia
em `/private/tmp/reviewer-fork-tests/`) afirma `claudeConfigDir` = home da conta global, `resumesTranscript === false` e
`options.sessionId === 'forked-under-b'` → 1 passed. **Inferido, não rodado ponta a ponta:** que o registro do chat
bifurcado nasce sem `accountSwitch`; foi lido. Confiança do `reviewer`: 85.

## O que resolve

Duas saídas, ambas com um teste do caminho:
- **Na conta fixada da origem (recomendada pelo `reviewer`):** o renderer passa o pino de origem, e o main grava o
  `accountSwitch` no registro adotado, com o divisor "Conta trocada". Custo: o pino na criação e no registro adotado.
- **Na conta global, com a cópia do transcript para o home dela**, como a troca do P36 já faz. Custo: uma cópia entre
  contas.
