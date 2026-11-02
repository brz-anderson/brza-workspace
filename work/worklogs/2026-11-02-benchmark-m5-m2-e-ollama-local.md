---
scope:
  - workspace
---

# O benchmark M5 Pro × M2 Pro e o Ollama local

Anderson perguntou se o M5 Pro de R$ 13 mil mais o M2 Pro valeram o investimento, e depois quis LLM local. Foi
medido, nos dois Macs, o kit `mac-bench` (CPU, memória, GPU, disco e compilação) e o fluxo real do `brza-studio`
(install, lint, typecheck e test). O kit fica no scratch do chat, fora do git; o `mac-bench.tgz` é o pacote para o M2.

## O que se mediu

Resultados do M5 Pro (A) contra o M2 Pro (B), no mesmo clang (21.0.0), na tomada, com o `compare.py`:

- **CPU**, 1 núcleo: 1,76× (inteiro) e 1,69× (ponto flutuante). Com todos os núcleos: 2,41× e 2,77×.
- **Compilação `clang -O2`:** 2,16×. É o número mais próximo de build e testes.
- **Disco sequencial:** 3,24× (escrita) e 3,30× (leitura). **4K aleatório:** 0,95×, empate.
- **GPU:** FP32 bruto 2,24×; multiplicação de matrizes 4096 com MPS, 1,36×; banda, 1,46×. Os dois têm GPU de 16 núcleos.
- **Memória:** 1,32× em 1 núcleo, 1,49× em todos.

Os números de `brza-studio` (`pnpm install`, `lint`, `typecheck`, `test`) foram tirados pela `benchmark-m5`, em
worktree descartável. O `lint` falhou nas duas rodadas, com ~30 s cada. O `test` passou do corte de 15 min na primeira
rodada e não completou; a comparação de `test` não vale ainda.

Para LLM local, medido no M5 Pro com o Ollama 0.40.13 e um prompt de 5.267 tokens, 256 de saída, 3 rodadas (vale a melhor):

| Modelo | Leitura do prompt (tok/s) | Geração (tok/s) | Memória |
| :-- | --: | --: | :-- |
| `qwen2.5:7b` | 1.047 | 51,9 | 5,1 GB, na GPU |
| `qwen2.5:14b` | 476 | 26,2 | 10,4 GB, na GPU |

O M2 Pro ainda não foi medido em LLM local. A razão entre os dois Macs, para geração, é estimativa pela banda de memória
(1,46×), não medida.

## Decisões e pendências

- **Anderson pediu medir Qwen 7B e 14B, mas só neste Mac, por ora.** Não há rodada no M2 Pro ainda.
- **O valor do investimento ainda não foi fechado.** A conta de "quando se paga" depende de quanto tempo por dia se
  espera a máquina, e de quanto vale o M2 Pro na revenda. Isso não foi medido nem informado.
- **O M2 Pro, para as duas medições de LLM e de `brza-studio`, não está medido.** Falta o Ollama lá e o `llm.py` no
  `mac-bench.tgz`, que ainda é o pacote anterior.
- **O `bench.sh` precisa de `LC_ALL=C`**, já corrigido no kit. O JSON do M2 veio de rodada com `LC_ALL=C`.

## Fora do workspace

- **O quê e onde:** Ollama 0.40.13 pela formula do Homebrew (`brew install ollama`), com as dependências `mlx` 0.32.4,
  `mlx-c` 0.8.0, `python@3.15` 3.15.2 e `mpdecimal` 4.0.1, em `/opt/homebrew`. **Risco:** baixo, e removido em seguida.
  **Estado:** removido. **Como desfazer:** já desfeito; o item seguinte é o que ficou.
- **O quê e onde:** `brew uninstall ollama`, que levou essas quatro dependências. Nada mais dependia delas, e o `brew`
  não deixou nada órfão. **Risco:** baixo; o `python@3.15` saiu do `/opt/homebrew`, e scripts que chamavam
  `/opt/homebrew/bin/ollama` falham. **Estado:** feito. **Como desfazer:** `brew install ollama` volta a formula, mas
  o binário colide com o do app. Não recomendado.
- **O quê e onde:** `brew install --cask ollama-app`, que instalou `/Applications/Ollama.app` (0.40.13, com
  atualização automática). O app sobe um servidor na porta 11434, e o `ollama` no PATH passa pelo link
  `/usr/local/bin/ollama`, que aponta para o binário do app. **Risco:** o app se atualiza sozinho e pode mudar a versão
  sem aviso; o servidor roda enquanto o app estiver aberto. **Estado:** ativo, o app aberto. **Como desfazer:** Quit no
  ícone da barra, depois `brew uninstall --cask ollama-app`.
- **O quê e onde:** modelos `qwen2.5:7b` (4,7 GB) e `qwen2.5:14b` (9,0 GB) em `~/.ollama/models`. **Risco:** ocupam
  ~14 GB do disco. **Estado:** ativo. **Como desfazer:** `ollama rm qwen2.5:7b qwen2.5:14b`.
