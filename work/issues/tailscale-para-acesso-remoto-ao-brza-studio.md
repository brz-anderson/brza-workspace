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

## A primeira rodada, em 2026-10-29

Respostas de Anderson na sessão `config-tailscale`:

- **Aparelhos:** "iPhone/iPad", "Outro Mac ou notebook pessoal" e "Windows da empresa". O BrzA Studio roda no Mac.
- **Via web:** "App móvel pela tailnet", "Remote Orca Server" e "Navegador sem Tailscale".
- **SSH:** "Login Remoto + chave (Recomendado)", com o app standalone do Tailscale, e não o Tailscale SSH, cuja parte
  servidor no macOS exige o `tailscaled` open-source, sem GUI.
- **Conta:** "GitHub brz-anderson (Recomendado)".

O BrzA Studio já tem cliente web: o `serve` imprime uma URL de navegador com o pareamento embutido
(`brza-studio/src/cli/specs/serve.ts:32`). A doc pede rede privada para o servidor remoto, que está em beta
(`brza-studio/docs/site/content/docs/remote-servers.mdx:13`).

## A segunda rodada, em 2026-10-29

- **Navegador:** "Os dois, com o Funnel ligado só quando precisar". O padrão é o cliente web pela tailnet; o Funnel
  liga à mão para uma máquina alheia e desliga em seguida.
- **Windows da empresa:** "Perguntar à TI antes (Recomendado)". Fica pendente aqui até a TI liberar.

## Retomar

Nada foi instalado: em 2026-10-29, Anderson só queria entender o Tailscale ("não vamos configurar o Tailscale hoje"). A
sessão que retomar segue esta ordem:

1. `brew install --cask tailscale-app`, que é a variante standalone e pede senha de administrador. Depois, aprovar a
   extensão de sistema e a VPN, entrar com o GitHub `brz-anderson` e instalar o CLI pelo menu do app.
2. Ligar o Login Remoto e pôr em `/etc/ssh/sshd_config.d/` um arquivo que recuse senha. O `~/.ssh/authorized_keys`
   ainda não existe e recebe a chave pública de cada aparelho que vai entrar.
3. No BrzA Studio, gerar o link em **Settings → Remote Orca Servers** com o endereço `100.x`, parear o app móvel e
   testar o cliente web pela tailnet.
4. Deixar anotados os comandos para ligar e desligar o `tailscale funnel`.
5. Instalar o Tailscale no iPhone e no Mac pessoal, com a mesma conta.

Tudo o que for instalado ou ligado na máquina (o app, o daemon, o login, o Login Remoto do macOS) entra no worklog do
dia, em `## Fora do workspace`.
