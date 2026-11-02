---
status: open
scope:
  - workspace
opened: 2026-11-02
owner: Anderson
description: Falta medir o M2 Pro no LLM local (qwen2.5 7B e 14B) e no fluxo do brza-studio, para fechar o comparativo com o M5 Pro.
tags:
  - tooling
---

# Medir o M2 Pro no LLM local e no fluxo do brza-studio

## O pedido

No [worklog de 2026-11-02](../worklogs/2026-11-02-benchmark-m5-m2-e-ollama-local.md), o M5 Pro foi medido contra o M2
Pro no kit `mac-bench`, que já cobre CPU, memória, GPU, disco e compilação. Faltam duas medições no M2 Pro, para o
comparativo ficar completo:

- **LLM local:** `qwen2.5:7b` e `qwen2.5:14b` pelo Ollama, com o `llm.py`. O M5 já foi medido: 52 e 26 tok/s de geração.
- **Fluxo do brza-studio:** `pnpm install`, `lint`, `typecheck` e `test`, no mesmo commit (`a70f63b6a92`), com a mesma
  regra de carga e tomada.

Sem o M2 Pro, a conta de "quando se paga" o investimento de R$ 13 mil segue estimada, e a razão de LLM local é só
a estimativa pela banda de memória (1,46×).

## O que falta

1. Copiar o `mac-bench.tgz` atualizado para o M2 Pro. O pacote anterior não tem o `llm.py` nem o `LC_ALL=C`. Ele sai de
   `mac-bench/` no scratch do chat, depois de recriado.
2. Instalar o Ollama no M2 Pro. Pelo mesmo caminho do M5: `brew install --cask ollama-app`, com a mesma nota no worklog
   da máquina, em `## Fora do workspace`.
3. Baixar `qwen2.5:7b` e `qwen2.5:14b`, e rodar `python3 llm.py qwen2.5:7b qwen2.5:14b`, com carga abaixo de 3.
4. Rodar o `brza-studio` em worktree descartável, como na medição do M5, e devolver a tabela por comando.

## Como saber que terminou

- Um JSON `llm-Apple-M2-Pro-<data>.json` em `results/`, com os dois modelos.
- A tabela de `brza-studio`, com os quatro comandos e as duas rodadas de cada um, com a versão de node e pnpm.
- Os dois arquivos trazidos para o `results/` do M5, para o `compare.py` rodar.

## Riscos a vigiar

- **Memória de 16 GB:** o 14B ocupa 10,4 GB na GPU, e o limite da GPU no M2 é menor que no M5. Se o modelo não couber,
  o resultado sai com a parte na CPU, e o `llm.py` mostra isso na coluna de memória. Não é falha, mas não compara com o M5.
- **Swap:** o M2 já teve swap alto sem o LLM. Rodar o modelo com o Mac ocupado pode distorcer a leitura do prompt.
- **Versão do macOS:** o M2 está em 27.0 e o M5 em 27.2. Diferença pequena, mas fica registrada no JSON.

## Refs

- Worklog: [O benchmark M5 Pro × M2 Pro e o Ollama local](../worklogs/2026-11-02-benchmark-m5-m2-e-ollama-local.md)
