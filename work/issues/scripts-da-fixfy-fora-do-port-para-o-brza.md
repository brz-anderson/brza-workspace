---
status: open
scope:
  - workspace
  - brza-studio
opened: 2026-10-28
trigger: Cada script tem o próprio gatilho de revisão, na tabela abaixo.
tags:
  - tooling
---

# Os scripts de orquestração da Fixfy que ficaram fora do port para o BrzA

Em 2026-10-28, Anderson escolheu o que vinha da Fixfy para o BrzA Studio. Entraram o núcleo do `orca-sessions` e o
`orca-run`, e ele pediu para os outros: "marque gatilhos de revisão para os outros". O que entrou está em
[Os scripts do Orca da Fixfy adaptados ao BrzA Studio](../worklogs/2026-10-28-scripts-do-orca-da-fixfy-adaptados-ao-brza.md).

Os gatilhos abaixo são proposta desta sessão, e não resposta de Anderson: quando um disparar, a sessão que o notar abre
a rodada.

| Script, na Fixfy | Veredito de hoje | Gatilho de revisão |
| :--------------- | :--------------- | :----------------- |
| `scripts/orca/chat-namer` | adiado | O nome automático do chat passa a rodar com o cwd no workspace, e não em `/`, ou Anderson pede nomes no padrão `PLN-001 · P42`. Hoje o one-shot do nome roda em `/`, e o `claude-brza` o deixa no claude puro, barato e sem os plugins que custavam ~US$ 0,13 por nome na Fixfy |
| `scripts/delegate.py` | adiado | A medição da delegação da Fixfy fecha, em 2026-10-30, a favor, e Anderson quer revisão independente por Codex ou agy no BrzA. A versão daqui sai sem a `adm` e sem o `quota.py` |
| `scripts/quota.py` | adiado | O BrzA passa a usar mais de uma conta do Claude no mesmo trabalho, pelo seletor de conta do P36 ou por outra conta configurada. Hoje há uma conta só, e falta o `statusline.py` que ele lê |
| `scripts/orca/orca-close-idle` | descartado | As sessões do Claude em terminal, e não em chat, voltam a ficar paradas no BrzA Studio de forma recorrente |
| `scripts/orca/orca-restart-sessions` | descartado | A norma de sessão nova muda. O script reinicia com `--resume`, e a norma daqui manda abrir sessão nova (`AGENTS.md`, "Uma tarefa, uma sessão, um worklog") |
| `scripts/orca/orca-patch` | descartado | O BrzA Studio volta a rodar um binário de terceiros que precise de remendo. Hoje ele é build próprio, com o tema e o `ps` no código-fonte |

## O ponto solto: a telemetria do BrzA Studio

O `orca-patch` da Fixfy também conferia que a telemetria estava desligada. No perfil do BrzA Studio ela está ligada
(`optedIn: True`, no levantamento de 2026-10-28). A política da Fixfy, desligada por causa dos hooks globais, não foi
estendida ao BrzA, e a escolha é de Anderson, numa rodada própria.
