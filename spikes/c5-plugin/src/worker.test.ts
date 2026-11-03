// A escolha do terminal do item 3 (R8.4: o worker escolhe sozinho), contra um host simulado.
import { mockHost, mountWorker, test } from 'orca/testing'
import assert from 'node:assert/strict'
import * as worker from './worker'

const ctx = {
  branch: 'workstream/tools-kit',
  displayName: 'tools-kit',
  terminals: [
    { id: 't-claude', title: '✳ Claude Code' },
    { id: 't-agente-sem-titulo' },
    { id: 't-shell', title: 'zsh' }
  ]
}
const agents = [{ terminalId: 't-agente-sem-titulo', title: null, agent: 'codex', state: 'working', stateStartedAt: 0 }]

test('escolhe o primeiro terminal sem agente e sem título de agente, e digita brza --version', async () => {
  const host = mockHost({ results: { 'workspace.readContext': ctx, 'agents.list': { agents }, 'terminal.sendText': { accepted: true } } })
  const w = await mountWorker(worker, { host })
  const seco = await w.request('terminal.run', { dryRun: true })
  assert.equal(seco.escolhido, 't-shell')
  assert.equal(host.callsOf('terminal.sendText').length, 0)
  const r = await w.request('terminal.run', { dryRun: false })
  assert.equal(r.accepted, true)
  // `callsOf` devolve os parâmetros de cada chamada, não `{ method, params }`.
  assert.deepEqual(host.callsOf('terminal.sendText')[0], { terminalId: 't-shell', text: 'brza --version', enter: true })
})

test('sem terminal livre, não digita', async () => {
  const host = mockHost({ results: { 'workspace.readContext': { ...ctx, terminals: ctx.terminals.slice(0, 2) }, 'agents.list': { agents } } })
  const w = await mountWorker(worker, { host })
  const r = await w.request('terminal.run', { dryRun: false })
  assert.equal(r.escolhido, null)
  assert.equal(host.callsOf('terminal.sendText').length, 0)
})

test('o worker alcança 127.0.0.1 (servidor do spike na 8765)', async () => {
  const w = await mountWorker(worker, { host: mockHost() })
  const r = await w.request('net.probe', { url: 'http://127.0.0.1:8765/' })
  assert.equal(r.status, 200, JSON.stringify(r))
})
