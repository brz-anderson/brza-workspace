# As molduras e o fragmento

## As molduras

| `--frame` | Largura nominal | Altura do conteúdo | O que desenha | Quando |
| :-- | --: | --: | :-- | :-- |
| `macos` | 1280 | 800 | janela com os três semáforos à esquerda, barra de título com o nome do app, cantos de 10 px | desktop do BrzA Studio no macOS; padrão do desktop |
| `windows` | 1280 | 800 | janela com minimizar, maximizar e fechar à direita, barra de título reta, cantos de 8 px | o mesmo app no Windows, quando a diferença importa (barra de título, menu, atalhos) |
| `iphone` | 393 | 852 | corpo arredondado, Dynamic Island, barra de status, indicador de home | app mobile, iOS |
| `android` | 412 | 915 | corpo arredondado, câmera em furo, barra de status, barra de gestos | app mobile, Android |
| `browser` | 375, 768, 1280 (`--widths`) | livre | barra de endereço e abas, uma por largura, empilhadas | site e app web; as três larguras são celular, tablet e desktop |

- **A largura nominal é a da tela de verdade**, e o fragmento é escrito para ela: o layout de 1280 px é o de 1280 px. O
  script inline da moldura aplica `zoom = min(1, largura do contêiner / nominal)`, e a tela inteira cabe na coluna do
  chat sem corte. Sem o `zoom`, um bloco de 1280 px tirado a 736 sai cortado no meio (sonda do PLN-021, F8).
- **A altura** do desktop é a da janela; o fragmento que passa dela rola dentro da janela, como no app. No mobile, a
  altura é a da tela do aparelho. Nunca `100vh`: o chat ajusta o quadro ao conteúdo, e `100vh` cresce sem fim.
- **`--scheme both`** desenha a mesma moldura duas vezes, clara e escura, lado a lado no mobile e empilhadas no desktop.

## O fragmento

O fragmento é o conteúdo da tela, sem moldura. Regras:

- **Cores, raios, fontes e espaços só por `var(--sa-*)`** — a lista está em `references/tokens.md`. Cor fixa quebra o
  `--scheme both` e a troca de pacote.
- **Layout com flex e grid**, com `min-width: 0` nos itens e `minmax(0, 1fr)` nas colunas, para o texto longo quebrar em
  vez de estourar. É o defeito mais comum no PNG.
- **Um elemento raiz** (`<div class="tela">…</div>`) com `height: 100%` quando a tela ocupa a janela inteira; o script
  põe a moldura em volta.
- **CSS no próprio fragmento**, num `<style>` no topo, com seletores sob `.tela` para não vazar para a moldura.
- **Responsivo por `@container`, nunca por `@media`.** O viewport do quadro é o do chat (736), e não a largura da
  moldura; o mesmo fragmento entra nas três larguras do `browser`. Ponha `container-type: inline-size` na raiz `.tela`
  e escreva as quebras com `@container (min-width: 700px) { … }`. Com `@media`, as três larguras saem iguais.
- **Ícones em SVG inline**, com `stroke="currentColor"`, para seguirem o tema.
- **O estado que a alternativa quer mostrar** — o menu aberto, o erro, a lista vazia — vai no próprio fragmento. Dois
  estados da mesma alternativa são dois artboards só quando a diferença é o ponto da escolha.

Exemplo mínimo (desktop, pacote `brza-studio`):

```html
<style>
  .tela { display: grid; grid-template-columns: 240px minmax(0, 1fr); height: 100%;
          background: var(--sa-background); color: var(--sa-foreground); font-family: var(--sa-font-sans); }
  .tela aside { background: var(--sa-sidebar, var(--sa-muted)); border-right: 1px solid var(--sa-border); padding: 12px; }
  .tela main { min-width: 0; padding: 16px; }
</style>
<div class="tela">
  <aside>…</aside>
  <main>…</main>
</div>
```
