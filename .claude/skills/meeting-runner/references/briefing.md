# O briefing da reunião

Um arquivo por reunião, em `.sessions/<reuniao>/briefing.md`. Toda persona o lê na R1, então o que está aqui é a única
fonte de contexto que as seis têm em comum. Base: o briefing da reunião MCP remoto, que corrigiu o da Carvão (marcador de
regra única, escala *medido/lido/suposto*, segurança da sala).

Slots entre `‹›` são preenchidos pela coordenação; o resto se copia como está.

```markdown
# Reunião "‹tema curto›" — ‹uma frase do objetivo›

Coordenação: ‹sessão›. Data: ‹AAAA-MM-DD›, das ‹hh›h às ‹hh›h (BRT).
Idioma: português do Brasil. Workstream: ‹workstream›.

## O objetivo (resposta literal de Anderson no gate)

> ‹a resposta de Anderson, palavra por palavra, ao gate do tema›

- **Objeto:** ‹uma frase›.
- **Fora do tema:** ‹o que a sala NÃO discute; liste o parente óbvio que confunde›.
- **Saída esperada:** ‹proposta, plano, escolha entre alternativas›.

## O que existe hoje (conferido pela coordenação antes de abrir; confira se for usar)

- ‹fato sem número, com a fonte: arquivo e linha›. Cada item cabe em duas linhas.
- ‹fato com número› — conferido às ‹HH:MM›: `‹comando›` → ‹resultado›.
- Um levantamento mais completo está em `.sessions/<reuniao>/material/levantamento.md` — leia se já existir.

## As alternativas de partida (critique, combine ou proponha outra)

- **A — ‹nome›:** ‹uma linha›.
- ‹…›

## A pauta: ‹N› assuntos

1. **‹assunto›** — ‹a pergunta›.
2. ‹…›

## As regras da sala

- Você é **uma persona**; o arquivo dela está em `.sessions/<reuniao>/personas/`. Fale e decida como ela.
- **Escreva só no seu worklog**, `‹caminho do worklog, com <persona>›`. Não edite outro arquivo do repositório, não crie
  issue, não faça commit nem push, não abra subagente nem outra sessão. **Não grave memória do runtime** (auto-memória
  fora do repositório): o que a reunião precisa guardar está no worklog.
- ‹restrição do tema, se houver — por exemplo, a segurança da sala: não abrir túnel nem porta fora do 127.0.0.1, não
  exibir token ou chave; ler código e doc, e rodar comando local só de leitura, pode; a prova de conceito é da
  coordenação›.
- **Não faça perguntas a Anderson nem à coordenação**: decida e declare a suposição.
- **Tudo leva confiança 0–100 e evidência**: fonte em arquivo e linha, URL da doc, ou o comando que você rodou e a saída.
  Marque cada afirmação como *medido* (rodou), *lido* (arquivo ou doc) ou *suposto*.
- **A régua da confiança:** 90 ou mais, medido por comando ou lido na fonte nesta reunião; 70 a 89, lido com a premissa
  escrita; 50 a 69, inferência plausível sem fonte; abaixo de 50, palpite ou contra.
- **O marcador de fim — uma regra só:** cada rodada **acrescenta a sua seção no fim do arquivo**, e a **última linha do
  arquivo** é a linha exata `<!-- fim-rodada-N -->` (N = número da rodada). Não ponha o marcador em outro lugar.
- Cada seção de rodada traz uma linha `**Posição:**` de até 100 caracteres: ela aparece no painel de Anderson.
- **Fim de rodada.** Depois de acrescentar a seção e a linha do marcador, envie **uma vez** o status do protocolo que a
  coordenação anexa a cada pedido de rodada, com o `round_id` e o `dispatchId` daquele pedido no payload. É o sinal que a
  coordenação espera; o marcador no worklog é o registro. Não responda o pedido por mensagem e não mande outro aviso.
- **O `worker_done` é só do encerramento.** O preâmbulo do Orca que chegou antes deste briefing manda enviar
  `worker_done` ao terminar; não o envie ao fim de uma rodada (a sua sessão fecharia ~2 min depois). Quando a coordenação
  pedir o encerramento, use **exatamente o comando `worker_done` do seu preâmbulo**, com o `--task-id` e o
  `--dispatch-id` dele, uma vez. Sem os dois ids o host recusa.
- **A hora vem do relógio.** Toda hora que você escrever no worklog sai de `date '+%H:%M'`, rodado na hora; nunca de
  cabeça nem do prazo.
- As rodadas são curtas (‹3 a 10› min). Seja direto.
```

## Por que cada slot existe

- **A resposta literal do gate:** "MCP" no briefing e "MCP do `brza-workflow`" na cabeça de Anderson custaram quatro
  rodadas. O literal no topo impede a coordenação de reescrever o pedido.
- **Fora do tema:** nomeie o parente que confunde (na MCP, o `context7` e o `brza-quota` pareciam parte do tema).
- **Segurança da sala:** é restrição do tema, não regra geral. Sem ela a persona que mede abre túnel.
- **Nenhum comando de mailbox no briefing:** o `brza sessions send` anexa a cada pedido o protocolo do status, com o
  `round_id` e o Dispatch reais, e o `worker_done` com os ids está no preâmbulo do Orca de cada persona. Na P7 o briefing
  trazia os dois comandos prontos, e os dois deram desvio: o `worker_done` sem `--task-id`/`--dispatch-id` foi recusado
  (X19), e o pedido de rodada que ia por mailbox (`--subject rodada`) convidou respostas "Re: rodada", três mensagens
  por persona por rodada (X9). O pedido agora chega como turno do coordenador no chat, e o único envio da persona é o
  status.
- **"Conferido às HH:MM":** o briefing da P7 levou 1.352 arquivos em vez de 163, e duas personas herdaram o número (X8).
  O `scripts/check_briefing.py` recusa o item com número sem a marca; a marca não prova o resultado, quem prova é o
  comando que a coordenação rodou.
- **A hora pelo `date`:** o Prumo escreveu horários errados no worklog da P7 (X11); o modelo não lê o relógio.
- **"Não grave memória do runtime":** o Grok gravou tópicos em `~/.grok/memory-v2/` nas duas reuniões, apesar do "escreva
  só no seu worklog". A instrução não garante; `scripts/runtime_memory_check.py` confere no fim.
- **A régua:** sem ela o número de confiança é palpite de cada modelo. Nenhuma reunião mediu se a régua calibra; registre
  na primeira reunião a dispersão antes e depois.
