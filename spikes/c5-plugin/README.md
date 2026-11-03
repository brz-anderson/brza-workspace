# BrzA spike C5

O plugin mínimo do spike do C5 do PLN-003 (`plans/PLN-003-o-workflow-nos-dois-clients/PLN-003-design.md`, critério C5):
um `trusted-worker`, `engines.orca >=1.4.246`, com dois painéis — `notas-tsx` (`ui: "components"`) e `notas-html`
(`ui: "html"`) — e um worker que responde a `ping`, `notes.list`, `terminal.run` e `net.probe` (`src/protocol.ts`).

Nasceu do `plugin create --template worker-panel` em 2026-11-03, e mora aqui pela R8.1 do PLN-003. É descartável: o
plugin do PLN-003 nasce do Desenho, não deste.

```bash
brza plugin validate . --json
```

```bash
brza plugin check . --json
```

```bash
brza plugin test . --json
```

O `test` sonda `http://127.0.0.1:8765/`; suba antes um servidor descartável, como
`python3 -m http.server 8765 --bind 127.0.0.1`. O `dev load` pede aprovação: ver a issue
`work/issues/o-approve-do-plugin-e-barrado-no-modo-auto.md`.
