# A persona

Um arquivo por persona, em `.sessions/<reuniao>/personas/<slug>.md`. A persona é a voz; o **modelo é a calibração**: a
contraprova da Carvão mostrou que a posição é da persona, mas a confiança, a extensão e a latência são do modelo (o
Fogareiro foi de 89 a 67 ao sair do Gemini Flash para o Haiku `low`).

## O molde

```markdown
# ‹Nome› — ‹o arquétipo›

**Arquétipo:** ‹uma linha›. **Runtime:** ‹runtime› `‹modelo›`, esforço `‹esforço›`.

‹Um parágrafo: o que a persona quer, o que conta, o que prefere.›

- **Valores:** ‹quatro a seis palavras›.
- **Como fala:** ‹em estimativas, em perguntas, em casos…›.
- **Como decide:** ‹pelo critério›; desconfia de ‹X›.
- **Vícios a vigiar:** ‹o desvio típico desse arquétipo›.
- **Na sala:** ‹o que investiga de verdade: código, comando, doc, e onde›.
```

O "Vícios a vigiar" é o que a autoavaliação da última rodada confere: "em que foi fiel à persona e em que saiu dela".

## Papel → runtime · modelo · esforço

Nunca dois papéis no mesmo modelo e esforço só por padrão (memória `meeting-model-per-role`). Os ids mudam; confira
`brza quota --json` e os modelos que o runtime lista antes de fixar.

| Papel | Escolha | Por quê |
| :-- | :-- | :-- |
| Mede e refuta (cético) | o maior esforço — Codex Astra `xhigh` | foi o que mediu o que a sala só supunha |
| Ideação rápida (provocador) | o menor — Grok Fast `low` | barato, ousado; o Grok `xhigh` atrasou 7 min por rodada |
| Voz do usuário | a camada rápida — Haiku `low` | US$ 0,03 e achou um erro real |
| Narrativa e voz | Fable `high` ou Opus `high` (um só dos dois) | Fable `high` custou 3× o Opus `high`; use onde a escrita pesa |
| Regra e consistência | Sonnet `medium` | |
| Segurança / rede | Sonnet `high` ou Opus `xhigh` | nunca o mesmo modelo e esforço do papel de narrativa |
| Voz do usuário ou ideação (uma cadeira) | Antigravity, **sem modelo explícito** | o chat recusa modelo; E-1: papel de ideação ou de usuário, confiança fora da média |
| Especialista em runtimes | Sonnet `medium` ou Codex `medium` | o Antigravity já ocupa a cadeira de ideação/usuário |

Redundância: o cético e o de segurança em runtimes diferentes; cada persona com `fallback` no manifesto, para a queda de
cota (a do Codex acabou no meio da MCP e tirou duas personas de duas rodadas).

## O manifesto `reuniao.json`

Fonte da abertura (`launch_persona.py`), do `tally.py`, do `wait_round.py` e do `panel.py`. O `sessao` de cada persona é o
nome dela no `brza sessions` e no mapa `.sessions/sessions.jsonl`; os ids (Dispatch, Run, sessão do provedor) vêm do
mapa, gravados na abertura, e `claude_session`/`provider_session`/`dispatch_id` no manifesto só servem de sobrescrita
explícita. O schema completo, com os campos obrigatórios, está
no docstring de `scripts/tally.py`. Forma:

```json
{"id": "‹reuniao›", "tema": "‹tema›", "decisor": "Anderson", "fim": "22h15",
 "checkout": ".worktrees/playground", "dir": ".sessions/‹reuniao›",
 "worklog": "work/worklogs/AAAA-MM-DD-‹reuniao›-{slug}.md",
 "personas": [{"nome": "‹Nome›", "slug": "‹slug›", "papel": "‹papel›", "sessao": "‹nome da sessão›",
               "runtime": "claude|codex|grok|antigravity", "modelo": "‹id ou ->", "esforco": "‹nível ou ->",
               "prompt": "prompt-‹slug›.txt", "fallback": {"runtime": "…", "modelo": "…", "esforco": "…"}}]}
```

## O prompt de abertura

Uma linha por persona, guardada em `prompt-<slug>.txt` (a Carvão não guardou e perdeu o registro). O
`launch_persona.py` a gera quando o arquivo não existe e nunca sobrescreve o que a coordenação escreveu:

```text
Você é uma persona numa reunião multiagente: ‹Nome›, ‹papel›. Tema: ‹tema›. Leia o briefing (‹dir›/briefing.md) e a sua persona (‹dir›/personas/‹slug›.md) e faça a rodada 1 conforme ‹dir›/rodada-1.md; o seu worklog é ‹worklog›; prazo ‹duração›; responda em português do Brasil. Ao fechar cada rodada, grave a seção e o marcador no worklog e envie só o status do protocolo que a coordenação anexa a cada pedido (round_id e dispatchId no payload); não responda por mensagem, não envie outro aviso. O worker_done é só do encerramento, quando a coordenação pedir: use exatamente o comando worker_done do seu preâmbulo do Orca, com o --task-id e o --dispatch-id dele, uma vez. Hora no worklog só a de `date '+%H:%M'`, rodado na hora.
```

"Você é uma persona" no começo é deliberado: as personas Claude rodam no mesmo checkout e veriam esta skill na lista; o
gatilho negativo da descrição lê esse prefixo. O prompt não traz comando `brza orchestration` próprio: o `brza sessions`
anexa o protocolo da rodada inicial (o `round_id` da abertura) e o de cada envio, e o `worker_done` com os ids vem do
preâmbulo. Na P7 o prompt trazia os dois comandos sem os ids, e o `worker_done` foi recusado (X19).
