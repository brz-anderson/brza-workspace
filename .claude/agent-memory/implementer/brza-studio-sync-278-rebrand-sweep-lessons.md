---
name: brza-studio-sync-278-rebrand-sweep-lessons
description: Varredura de fallbacks Orca nos gates de idioma do sync 278 - rodar rebrand_locales.py exige rebrandar a fonte, CJK, mobile compartilhado, output do verify truncado
metadata:
  type: project
---

- **Rebrandar o catálogo en.json obriga rebrandar a fonte**: o `verify:localization-extraction` compara o fallback inline com o `en.json`; depois do `rebrand_locales.py` os ~355 pares diferem. Script: extrair a lista completa copiando `verify-localization-extraction.mjs` para um `tmpverify.mjs` na mesma pasta com `keys.slice(0, 20)` -> `keys` (apagar depois), depois trocar o literal inteiro na fonte (exige aspas/`>`/`<` nos dois lados; literal "Orca" sozinho casa em tudo, tratar à mão). Era o que o `g278/rb/apply.py` fazia.
- **`\b`/`\w` do Python não separa Orca de Hangul/kana**: o `rebrand_locales.py` deixa "Orca를"/"Orcaサーバー"; use lookarounds ASCII `(?<![A-Za-z0-9_./:-])Orca(?![A-Za-z_-])` e confira por contagem. Alemão: "Orca-X" -> "BrzA-Studio-X" e "Orcas" -> "BrzA Studios" não são tocados pelo script.
- **Mobile lê `src/shared`**: o `verify:mobile-localization` extrai fallbacks de fontes compartilhadas; o mesmo literal é do desktop (BrzA Studio) e do mobile (Orca). Já estava quebrado no HEAD; a saída foi alinhar o en.json do mobile (e locales) nessas chaves, como rodada.
- **O gate de catálogos lista chaves reusadas com `Orca` numa ocorrência e `BrzA Studio` na outra**: basta rebrandar a ocorrência que sobrou, sem chave nova. Também pode exigir `sync:localization-protected-copy`.
- **Teste que afirma texto rebrandado**: regex `/^Update Orca on/`, `toContain('update Orca on…')` e iniciais (`initial: 'O'` -> `'B'`) não casam por literal; rode os testes irmãos dos arquivos alterados.
- **oxfmt quebra `t()` longo em 4 linhas** e estoura `max-lines` de arquivo no teto (BotGitHubSetupDialog): extrair os textos para o `*-copy.ts` vizinho com `translate`, mesma chave.
