---
status: open
scope:
  - brza-studio
opened: 2026-10-28
tags:
  - infra
---

# O Tailscale para acessar o BrzA Studio de fora, pela web e por SSH

Pedido de Anderson, em 2026-10-28, na sessão do `brza-workspace` que orquestrou o PLN-001: "precisamos configurar o
Tailscale para que eu possa conectar via web e ssh futuramente". Registrado aqui, e não no PLN-001,
pela escolha "Issue em work/issues/ (Recomendado)": o Tailscale mexe na máquina (daemon, login, ACL) e não no código do
chat.

## O que falta saber

Nada foi levantado ainda. A sessão nova começa pela entrevista:

- de quais aparelhos Anderson quer entrar, e em que máquina o BrzA Studio roda;
- o que "via web" quer dizer: o pareamento remoto do próprio BrzA Studio (o `orca://pair`, os servidores conectados
  do Orca) por cima da tailnet, ou outra interface web;
- o SSH: o Tailscale SSH ou o `sshd` do macOS dentro da tailnet;
- a conta do Tailscale, que não pode ser a da Fixfy.

Tudo o que for instalado ou ligado na máquina (o app, o daemon, o login, o Login Remoto do macOS) entra no worklog do
dia, em `## Fora do workspace`.
