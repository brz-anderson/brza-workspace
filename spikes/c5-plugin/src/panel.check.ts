// `plugin check` renderiza o painel com o worker num host simulado. O cenário `tools-kit` dá ao
// worker o contexto do worktree do workstream, e o worker lê os arquivos de verdade (Node).
import { defineCheck } from 'orca/testing'

export default defineCheck({
  vazio: {},
  'tools-kit': {
    results: {
      'workspace.readContext': { branch: 'workstream/tools-kit', displayName: 'tools-kit', terminals: [{ id: 't1', title: 'zsh' }, { id: 't2', title: '✳ Claude Code' }] },
      'agents.list': { agents: [{ terminalId: 't2', title: 'Claude Code', agent: 'claude', state: 'working', stateStartedAt: 0 }] }
    }
  }
})
