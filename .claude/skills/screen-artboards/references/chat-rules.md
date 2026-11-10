# As regras do visual no chat do BrzA Studio

O chat mostra um `.html` inline quando a mensagem tem a linha `::orca-visual{file="<nome>.html" title="…"}`, fora de
bloco de código. As regras são da skill `orca-chat-visuals` do app
(`brza-studio/resources/native-chat-visuals/skills/orca-chat-visuals/SKILL.md`) e do `.claude/rules/brza-client.md`; o
`artboard.py new` confere as que se conferem por máquina e recusa com a linha do problema.

| Regra | Por quê | Quem confere |
| :-- | :-- | :-- |
| o arquivo no `ORCA_CHAT_SCRATCH_DIR`, nome só com letras, dígitos, `.`, `_`, `-` | o chat só lê de lá, e pelo nome puro | o script |
| até 512 KB | acima disso o chat não mostra | o script |
| sem rede: nenhum `http`, fonte só do Google Fonts ou de CDN permitida | o quadro não faz requisição | o script recusa `http` fora dos CDNs da lista; o `xmlns` do SVG inline (`http://www.w3.org/…`) passa, porque não é requisição |
| sem `100vh` | o chat ajusta o quadro ao conteúdo; `100vh` cresce sem fim | o script |
| não redefinir `--background`, `--primary`… no `:root` | pinta o chat inteiro com a cor do mockup | o script recusa `:root {` com token do Orca |
| até 8 visuais por resposta | o chat corta o resto | a sessão, ao montar a mensagem |
| nome novo a cada versão | o chat guarda o visual pelo nome | o script põe um hash no nome |
| a letra da opção no `title` ("A — …") | a rodada cita a alternativa pela letra | `--letter` |

## A conferência pelo PNG

A sessão não vê o chat. Antes de qualquer rodada, cada artboard passa pelo PNG:

```bash
python3 -I .claude/skills/screen-artboards/scripts/artboard.py shot "<artboard>.html" --out-dir "<scratch>/png"
```

O `shot` roda o `brza shot` na largura do chat (736) e, na web, uma vez por largura nominal; com `--scheme both`, os dois
temas. Leia cada imagem e procure: corte na direita ou embaixo, coluna estourada, texto sobreposto, contraste ruim no
escuro, a moldura desalinhada. Corrija no fragmento e gere de novo, com nome novo.

## Fora do chat

Sem o `ORCA_CHAT_SCRATCH_DIR`, o artboard vai ao scratch da sessão (ou ao `--publish-dir`), e a mensagem leva o caminho
do `.html` e dos PNGs em vez da linha `::orca-visual`.
