---
name: plan-runner-p11-corrections
description: P11 do PLN-021 (correções do REV-026) — armadilhas de teste e comandos que provam com o brza real, sem abrir sessão
metadata:
  type: project
---

**Valida (2026-11-10):** plan-runner 175 OK, `.claude/scripts/tests` 56, screen-artboards 55, meeting-runner 323. Código novo em inglês
(regra R6.5 de Anderson); o existente em pt-BR só se renomeia no P11.2.

- **Provar com o `brza` real sem abrir sessão:** gere o argv com `consult.py open … --dry-run` / `executor.py open … --checkout . --dry-run`,
  troque `--prompt-file X` por um arquivo existente e rode `eval "<argv> --dry-run"` (o dry-run do brza lê o arquivo). `brza quota --json`
  é `accounts[].windows[]` (a fixture real está em `tests/fixtures/quota-real.json`, rótulos de e-mail trocados). `brza sessions wait <inexistente>`
  sai rc 1 com `{"error": "0 chats abertos se chamam …"}`.
- **`brza sessions --effort` exige `--model`:** o Codex ganha `executor.CODEX_MODEL` (`gpt-6.1-sol`, do config do codex e do smoke do PLN-017;
  `xhigh` nesse modelo não foi provado, só o dry-run).
- `gera_png` do skillkit recebe `chrome_css`: o `brza shot` injeta os tokens do chat e um `:root` no HTML vence o tema dele, então o fallback
  de tokens só vai ao Chrome de reserva, num HTML temporário.
- Teste de `wait` com `FakeClock`: cada leitura avança 1 s, então "sem pausa" se mede por nº de chamadas ao `wait` falso e pela linha "em curso".
- `Pergunta.decidida` agora conta `**Resposta:**` com "lida como" (exceto "contraproposta"/"esclarecimento"); o fixture congelado do PLN-021 não
  tem a R4.9, teste isso com o plano mini.
