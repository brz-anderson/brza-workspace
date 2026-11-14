# A síntese da rodada

Um arquivo por rodada, `.sessions/<reuniao>/sintese-N.md`, escrito **depois** de `tally.py N` e da conferência dos
números. A síntese compara posições; o agregado ("a sala foi de 61,8 a 70") é o que deixou o MCP no chat sem o conteúdo
que a Carvão tinha.

## O molde

```markdown
# Síntese da rodada N (coordenação, ‹hh:mm›)

## Como a sala votou nas disputas

| Disputa | Resultado | Quem ficou fora |
| :------ | :-------- | :-------------- |
| D1 · ‹assunto› | (‹letra›) ‹opção› — ‹quem›; ‹quem virou› | ‹quem votou diferente, com a posição da R1 se atrasou› |

**Mudanças de posição na rodada N:** ‹quem virou, de quê para quê, movido por quem›.

## A tabela por persona

‹a saída de `tally.py N --md`: Persona · posição · confiança (Δ vs R1) · mudou? · voto; e a linha da sala›

## Fatos novos da rodada N

- ‹M#: o fato, quem o trouxe, **conferido** pela coordenação por ‹comando› → ‹resultado›, ou "não conferi"›. **Marque os
  novos desta rodada**: a próxima rodada com voto os cita no pedido, e a persona os declara em `**Fatos lidos:**` (X10).
- ‹Número de persona que NÃO bate com a conferência: diga o valor da persona e o da coordenação›.

## Convergências

- **C1:** ‹o que quase todos aceitam›.

## Quem ficou fora

‹Persona que não respondeu, atrasou ou caiu de cota, e o que a síntese fez sem ela›.

## As propostas para o voto final (se a próxima rodada vota)

| ID | Proposta |
| :- | :------- |
| P1 | ‹a forma que a coordenação pretende levar ao plano›. |
```

**Regras:** (1) todo número da síntese tem a fonte (`tally.py`, comando ou worklog); (2) disputa técnica ou visual leva a
evidência (prova de conceito, renderização) antes do voto; (3) o número do Antigravity passa pela conferência antes de
entrar; (4) "quem ficou fora" é obrigatório quando a tabela tem n < N, porque a média sem a persona não é a da sala.

## O `sintese-N.json`: o que o painel lê

A coordenação grava `.sessions/<reuniao>/sintese-N.json` ao fechar a rodada; `panel.py collect` o funde ao
`estado-rN.json`. Sem ele, o painel mostra só as tabelas do `tally.py` e os blocos de medição, síntese e decisão somem.

```json
{
  "posicoes": {"Muralha": "Sem a evidência de coordenador, a mensagem remota vira turno de Anderson."},
  "sala": {"revisor": 45, "revisor_nota": "revisor independente na v1, fora da sala"},
  "medicoes": [
    {"tipo": "medido", "quem": "coordenação", "texto": "Cloud na rede padrão recusa o túnel: 403 connect_rejected."},
    {"tipo": "conferido", "quem": "coordenação", "texto": "6 de 6 marcadores fim-rodada-3 na última linha; média recalculada das seis tabelas."}
  ],
  "sintese": ["Até 5 linhas numeradas no painel, uma frase cada."],
  "decisoes": [
    {"pergunta": "O primeiro aceite pode ser parcial?", "quem": ["Régua", "Atalho"],
     "recomendacao": "Sim, chamado de piloto parcial.", "votos": null}
  ],
  "custos_coordenacao": {"coordenacao_usd": 4.74, "revisor_usd": 1.02, "ate": "21:32:39"},
  "rodada_extra": {"gatilho": "M6 contradiz a premissa do voto B", "participantes": ["Trava", "Relance"],
                   "motivo": "o voto A do Prumo não depende de M6"}
}
```

- `posicoes` **sobrepõe** a `**Posição:**` da persona só quando a dela não serve (longa, genérica, em outra língua).
- `medicoes[].tipo`: `medido` (a coordenação rodou), `lido` (arquivo ou doc), `conferido` (a coordenação conferiu o número
  de uma persona). Medição sem fonte não entra: `texto` termina com a fonte ou o comando.
- `decisoes` é o que vai à rodada com Anderson; o painel só mostra, e a pergunta com opções vai ao chat. `quem` é **quem
  levantou** a decisão, e o painel o mostra como "levantada por"; voto vai só em `votos` (na P7 o painel leu `quem` como
  "recomendam" e atribuiu A a quem votou B, X12).
- Rodada para parte da sala: o `estado-rN.json` traz `rodada.participantes` (do `--participantes`); a síntese diz quem
  ficou fora e por quê, e o `posicoes` não precisa de texto para quem não participou (X18).
- `custos_coordenacao` vem do `measurements.jsonl` da sessão de coordenação e dos subagentes dela (`agrega.py` do
  PLN-017 mostra a conta); sem ele o cartão some.
- `rodada_extra` só existe quando o gatilho da R8 valeu: o fato, quem participa e o motivo da escolha (R9), gravados
  **antes** do envio da rodada extra. O painel não o lê; é o registro da escolha da coordenação.
