// O contrato painel <-> worker do spike do C5 (PLN-003), declarado uma vez.
export {}

export type Plano = { id: string; titulo: string; status: string; phase: string; caminho: string }
export type Nota = { genero: string; titulo: string; status: string; caminho: string }

declare module 'orca' {
  interface PluginRequests {
    /** Item 1: o worker responde, com o pid e a hora. */
    'ping': { output: { pid: number; node: string; at: number } }
    /** Item 2: os planos e as notas abertas do worktree do workspace em foco. */
    'notes.list': {
      output: {
        branch: string | null
        raiz: string | null
        erro: string | null
        planos: Plano[]
        notas: Nota[]
        retomar: string
      }
    }
    /** Item 3: escolhe sozinho um terminal sem agente e digita `brza --version`; `dryRun` só escolhe. */
    'terminal.run': {
      input: { dryRun: boolean }
      output: {
        terminais: { id: string; title?: string }[]
        agentes: { terminalId: string | null; title: string | null; agent: string | null; state: string }[]
        escolhido: string | null
        motivo: string
        accepted: boolean | null
      }
    }
    /** Item 4: o worker tenta um GET na URL. */
    'net.probe': { input: { url: string }; output: { ok: boolean; status: number | null; erro: string | null; ms: number } }
  }
}
