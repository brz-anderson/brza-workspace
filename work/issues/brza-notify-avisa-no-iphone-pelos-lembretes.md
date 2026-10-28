---
status: open
scope:
  - workspace
opened: 2026-10-28
tags:
  - tooling
---

# O brza-notify, que avisa no iPhone pelos Lembretes do iCloud

Pedido de Anderson, em 2026-10-28: "uma issue para o comando", depois de testar se o Mac consegue mandar notificação ao
iPhone pelo sistema nativo.

## O que o teste mostrou

O macOS não repassa notificação ao iPhone, e o Atalhos não tem ação para isso. O caminho nativo que funciona é um
lembrete com alarme: o Mac cria o lembrete, o iCloud sincroniza e o iPhone toca. Em 2026-10-28, o lembrete criado com
alarme para um minuto depois tocou no iPhone na hora, segundo Anderson.

```bash
osascript -e 'tell application "Reminders" to make new reminder with properties {name:"Build pronto", remind me date:(current date) + 60}'
```

- **Permissão:** o `osascript` rodou da sessão do chat do BrzA Studio sem pedir a autorização de Automação.
- **Lista:** sem `at list`, o lembrete vai à lista padrão, que aqui é a `Lembretes`.
- **Limpeza:** o lembrete de teste foi apagado com `delete (every reminder whose name is "…")`, e não ficou nada no
  iCloud.

O ntfy, o Pushover e o Bark entregam o mesmo aviso por push de verdade, mas pedem app de terceiros no iPhone. Ficaram
fora porque o pedido era o caminho nativo.

## O que falta decidir

O comando entra em `scripts/brza/brza-notify "mensagem"`, ao lado dos outros `brza-*`. A sessão que pegar a issue
começa pela entrevista:

- **a lista:** uma lista própria no iCloud, como `Avisos`, criada pelo comando quando faltar, ou a lista padrão;
- **a antecedência do alarme:** o alarme precisa estar no futuro quando o lembrete chega ao iPhone, e o minuto do teste
  pode ser encurtado;
- **o que sobra depois:** o lembrete fica na lista até Anderson marcar, ou o comando apaga os avisos antigos a cada
  chamada;
- **quem chama:** só à mão e pelas sessões, ou também um hook, como o `Stop` de turno longo, que teria de medir a
  duração para não avisar a cada turno.
