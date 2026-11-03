// O painel de componentes do spike do C5: a mesma informação do painel html, no catálogo do Orca.
import { atom, Badge, Button, Callout, Heading, Markdown, plugin, read, Row, set, Stack, Table, Text, Tree, type PanelContext } from 'orca'
import type { PluginRequests } from 'orca'
import './protocol'

type Lista = PluginRequests['notes.list']['output']

const lista = atom<Lista | null>(null)
const ping = atom<string>('—')
const terminal = atom<string>('—')
const rede = atom<string>('—')

async function carregar(): Promise<void> {
  set(lista, await plugin.request('notes.list'))
}

export function setup(_ctx: PanelContext): void {
  const t0 = Date.now()
  void plugin.request('ping').then((r) => set(ping, `pid ${r.pid}, ${r.node}, ${Date.now() - t0} ms`))
  void carregar()
}

export default function Panel() {
  const l = read(lista)
  return (
    <Stack gap="md">
      <Row justify="between">
        <Heading>Spike C5 · components</Heading>
        <Badge tone="accent">{l?.branch ?? '…'}</Badge>
      </Row>
      <Text muted size="xs">worker: {read(ping)}</Text>
      {l?.erro ? <Callout tone="warning" title="notes.list">{l.erro}</Callout> : null}
      <Tree
        label="Planos e notas"
        defaultExpanded={['planos', 'notas']}
        items={[
          {
            key: 'planos',
            label: `Planos (${l?.planos.length ?? 0})`,
            icon: 'layers',
            children: (l?.planos ?? []).map((p) => ({ key: p.caminho, label: p.titulo, description: `${p.status} · ${p.phase}`, icon: 'file-text' }))
          },
          {
            key: 'notas',
            label: `Notas abertas (${l?.notas.length ?? 0})`,
            icon: 'book',
            children: (l?.notas ?? []).map((n) => ({ key: n.caminho, label: n.titulo, description: `${n.genero} · ${n.status}`, icon: 'file' }))
          }
        ]}
      />
      <Table
        label="Notas abertas"
        columns={[
          { key: 'genero', label: 'Gênero', width: 'sm' },
          { key: 'titulo', label: 'Título' },
          { key: 'status', label: 'Status', width: 'xs' }
        ]}
        rows={(l?.notas ?? []).map((n) => ({ key: n.caminho, cells: { genero: n.genero, titulo: n.titulo, status: n.status } }))}
        emptyText="sem notas abertas"
        maxHeight="md"
      />
      <Markdown content={l?.retomar || '_sem plano aberto_'} />
      <Row gap="xs" wrap>
        <Button icon="refresh" onPress={carregar}>Recarregar</Button>
        <Button
          icon="terminal"
          onPress={async () => {
            const r = await plugin.request('terminal.run', { dryRun: false })
            set(terminal, `${r.escolhido ?? 'nenhum'} · ${r.motivo} · accepted=${String(r.accepted)}`)
          }}
        >
          brza --version
        </Button>
        <Button
          icon="globe"
          onPress={async () => {
            const r = await plugin.request('net.probe', { url: 'http://127.0.0.1:8765/' })
            set(rede, r.ok ? `worker → 127.0.0.1: ${r.status}` : `worker → 127.0.0.1: ${r.erro}`)
          }}
        >
          Sondar 127.0.0.1
        </Button>
      </Row>
      <Text size="xs">terminal: {read(terminal)}</Text>
      <Text size="xs">rede: {read(rede)}</Text>
    </Stack>
  )
}
