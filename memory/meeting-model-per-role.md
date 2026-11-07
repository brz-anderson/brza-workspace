---
name: meeting-model-per-role
description: "Em reunião multiagente com personas, cada sessão roda no modelo e esforço do papel, diversificados ao máximo"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4cbdb093-1f3d-40bc-b10e-a3f8680bae4c
  modified: 2026-11-07T23:55:30.307Z
---

Em reunião multiagente com personas, o modelo e o esforço de cada sessão seguem o papel dela, e a escolha diversifica
ao máximo entre runtimes, modelos e níveis de esforço — nunca dois papéis no mesmo modelo e esforço só por padrão.

**Why:** Anderson pediu, em 2026-11-07, depois da reunião Carvão em Brasa, em que Tição e Fole rodaram ambos no Opus
`high` e Cinza e Lenha ambos no `gpt-6.1-sol` `medium`. A contraprova mostrou que a posição é da persona, mas a
confiança, a extensão e a latência são do modelo: o Fogareiro foi de 89 a 67 de confiança ao sair do Gemini Flash
(High) para o Haiku `low`.

**How to apply:**
- O `brza sessions` não repassa `--model` nem `--effort`; abra pelo `brza agent launch --model <id> --effort <nível>`
  e registre o nome no mapa (`.sessions/sessions.jsonl`), como fez o lançador da contraprova.
- O chat do Antigravity no app recusa modelo explícito ("not available for the current authentication method"); para
  variar o modelo dessa persona, mude de runtime.
- Papel que mede e refuta: o maior esforço (Codex Astra `xhigh`); ideação rápida: o menor (Grok Fast `low`); voz do
  usuário: a camada rápida (Haiku `low`); narrativa: Fable ou Opus `high`; regra e consistência: Sonnet `medium`.
- Ver [[consultant-debate-shown-in-full]].
