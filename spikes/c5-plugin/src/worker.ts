// O worker do spike do C5. Lê planos e notas do worktree do workspace em foco, digita num
// terminal sem agente e sonda a rede local. Node completo, env só PATH/HOME/LANG/TZ/TMP.
import type { OrcaWorkerApi } from 'orca/worker'
import { execFile } from 'node:child_process'
import { readdir, readFile } from 'node:fs/promises'
import { join } from 'node:path'
import type { Nota, Plano } from './protocol'

const WORKSPACE = join(process.env.HOME ?? '', 'Projects', 'brza-workspace')
const AGENTE = /claude|codex|agent|gemini|agy|✳/i

function git(args: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    execFile('git', args, { timeout: 10_000 }, (err, stdout) => (err ? reject(err) : resolve(stdout)))
  })
}

/** O worktree do workspace com a branch dada, pelo `git worktree list`. */
async function worktreeDaBranch(branch: string): Promise<string | null> {
  const out = await git(['-C', WORKSPACE, 'worktree', 'list', '--porcelain'])
  let caminho: string | null = null
  for (const linha of out.split('\n')) {
    if (linha.startsWith('worktree ')) caminho = linha.slice(9)
    if (linha === `branch refs/heads/${branch}` && caminho) return caminho
  }
  return null
}

function frontmatter(texto: string): Record<string, string> {
  const m = /^---\n([\s\S]*?)\n---/.exec(texto)
  const campos: Record<string, string> = {}
  if (!m) return campos
  for (const linha of m[1].split('\n')) {
    const kv = /^([a-z_]+):\s*(.*)$/.exec(linha)
    if (kv) campos[kv[1]] = kv[2]
  }
  return campos
}

function h1(texto: string): string {
  return /^# (.+)$/m.exec(texto)?.[1] ?? '(sem título)'
}

async function listarMd(dir: string): Promise<string[]> {
  try {
    return (await readdir(dir)).filter((f) => f.endsWith('.md') && f !== 'README.md')
  } catch {
    return []
  }
}

export default function activate(orca: OrcaWorkerApi): void {
  orca.log(`ativado pid=${process.pid}`)

  orca.panels.handle('ping', async () => ({ pid: process.pid, node: process.version, at: Date.now() }))

  orca.panels.handle('notes.list', async () => {
    const vazio = { planos: [] as Plano[], notas: [] as Nota[], retomar: '' }
    const ctx = await orca.host.call('workspace.readContext')
    if (!ctx) return { branch: null, raiz: null, erro: 'nenhum workspace em foco', ...vazio }
    const raiz = await worktreeDaBranch(ctx.branch)
    if (!raiz) return { branch: ctx.branch, raiz: null, erro: 'a branch não é de um worktree do brza-workspace', ...vazio }

    const planos: Plano[] = []
    let retomar = ''
    for (const pasta of (await readdir(join(raiz, 'plans'), { withFileTypes: true })).filter((d) => d.isDirectory())) {
      const id = pasta.name.slice(0, 7)
      const caminho = join('plans', pasta.name, `${id}-plan.md`)
      try {
        const texto = await readFile(join(raiz, caminho), 'utf8')
        const fm = frontmatter(texto)
        planos.push({ id, titulo: h1(texto), status: fm.status ?? '?', phase: fm.phase ?? '?', caminho })
        if (!retomar && fm.status === 'open') {
          const r = /- \*\*Retomar:\*\*[\s\S]*?(?=\n- \*\*|\n## )/.exec(texto)
          retomar = `## ${id}\n\n${r ? r[0] : '(sem Retomar)'}`
        }
      } catch {
        /* pasta sem plano */
      }
    }

    const notas: Nota[] = []
    for (const genero of ['issues', 'decisions', 'reviews']) {
      for (const f of await listarMd(join(raiz, 'work', genero))) {
        const texto = await readFile(join(raiz, 'work', genero, f), 'utf8')
        const status = frontmatter(texto).status ?? '?'
        if (status !== 'done' && status !== 'dropped') {
          notas.push({ genero, titulo: h1(texto), status, caminho: join('work', genero, f) })
        }
      }
    }
    orca.log(`notes.list branch=${ctx.branch} planos=${planos.length} notas=${notas.length}`)
    return { branch: ctx.branch, raiz, erro: null, planos, notas, retomar }
  })

  orca.panels.handle('terminal.run', async ({ dryRun }) => {
    const ctx = await orca.host.call('workspace.readContext')
    const terminais = ctx?.terminals ?? []
    const { agents } = await orca.host.call('agents.list')
    const comAgente = new Set(agents.map((a) => a.terminalId).filter(Boolean))
    const livre = terminais.find((t) => !comAgente.has(t.id) && !AGENTE.test(t.title ?? ''))
    const base = {
      terminais,
      agentes: agents.map((a) => ({ terminalId: a.terminalId, title: a.title, agent: a.agent, state: a.state }))
    }
    if (!livre) return { ...base, escolhido: null, motivo: 'nenhum terminal sem agente', accepted: null }
    if (dryRun) return { ...base, escolhido: livre.id, motivo: 'dryRun', accepted: null }
    const { accepted } = await orca.host.call('terminal.sendText', { terminalId: livre.id, text: 'brza --version', enter: true })
    orca.log(`terminal.run ${livre.id} (${livre.title ?? ''}) accepted=${accepted}`)
    return { ...base, escolhido: livre.id, motivo: 'primeiro terminal sem agente', accepted }
  })

  orca.panels.handle('net.probe', async ({ url }) => {
    const t0 = Date.now()
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(5_000) })
      return { ok: res.ok, status: res.status, erro: null, ms: Date.now() - t0 }
    } catch (e) {
      return { ok: false, status: null, erro: String((e as Error)?.message ?? e), ms: Date.now() - t0 }
    }
  })
}
