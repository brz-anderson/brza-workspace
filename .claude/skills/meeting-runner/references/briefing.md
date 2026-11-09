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

## O que existe hoje (lido pela coordenação; confira se for usar)

- ‹fato com fonte: arquivo e linha, ou comando›. Cada item cabe em duas linhas.
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
- **Fim de rodada — dois sinais.** Depois de acrescentar a seção e a linha do marcador, rode, uma vez por rodada:
  `brza orchestration send --subject "fim-rodada-N" --body "persona:‹slug›"` (sem `--to`: o worker já fala com a coordenação). Isso é o sinal que a
  coordenação espera; o marcador no worklog é o registro.
- **O `worker_done` do preâmbulo do Orca é só do encerramento.** O preâmbulo que chega antes deste briefing manda enviar
  `worker_done` ao terminar; não o envie ao fim de uma rodada (a sua sessão fecharia ~2 min depois). Só quando a
  coordenação mandar "a reunião acabou": `brza orchestration send --type worker_done --outcome succeeded --subject
  "encerrado" --body "persona:‹slug›"` (também sem `--to`).
- As rodadas são curtas (‹3 a 10› min). Seja direto.
```

## Por que cada slot existe

- **A resposta literal do gate:** "MCP" no briefing e "MCP do `brza-workflow`" na cabeça de Anderson custaram quatro
  rodadas. O literal no topo impede a coordenação de reescrever o pedido.
- **Fora do tema:** nomeie o parente que confunde (na MCP, o `context7` e o `brza-quota` pareciam parte do tema).
- **Segurança da sala:** é restrição do tema, não regra geral. Sem ela a persona que mede abre túnel.
- **Os dois comandos prontos:** a persona é um worker do Orca e o preâmbulo dele pede `worker_done` ao terminar o turno;
  sem o aviso, a persona fecha no meio da síntese. O briefing traz os dois comandos; o `persona:<slug>` no corpo é o que a coordenação usa para saber de quem é a mensagem.
- **"Não grave memória do runtime":** o Grok gravou tópicos em `~/.grok/memory-v2/` nas duas reuniões, apesar do "escreva
  só no seu worklog". A instrução não garante; `scripts/runtime_memory_check.py` confere no fim.
- **A régua:** sem ela o número de confiança é palpite de cada modelo. Nenhuma reunião mediu se a régua calibra; registre
  na primeira reunião a dispersão antes e depois.
