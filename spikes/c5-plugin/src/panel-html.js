// O script do painel html do spike do C5: pergunta ao worker e sonda a rede direto do frame.
const $ = (id) => document.getElementById(id)
const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c])

async function carregar() {
  const t0 = performance.now()
  try {
    const { pid, node } = await orca.plugin.request('ping')
    $('ping').textContent = `worker: pid ${pid}, ${node}, ${Math.round(performance.now() - t0)} ms`
  } catch (e) {
    $('ping').innerHTML = `<span class="erro">worker: ${esc(e.code ?? e.message)}</span>`
  }
  const l = await orca.plugin.request('notes.list')
  $('planos').innerHTML = l.planos.map((p) => `<tr><td>${esc(p.id)}</td><td>${esc(p.titulo)}</td><td>${esc(p.status)} · ${esc(p.phase)}</td></tr>`).join('')
  $('notas').innerHTML = l.notas.map((n) => `<tr><td>${esc(n.genero)}</td><td>${esc(n.titulo)}</td><td>${esc(n.status)}</td></tr>`).join('') || '<tr><td>sem notas abertas</td></tr>'
  $('retomar').textContent = l.erro ? `erro: ${l.erro}` : l.retomar
}

async function sondar() {
  const t0 = performance.now()
  try {
    const r = await fetch('http://127.0.0.1:8765/', { cache: 'no-store' })
    $('rede').textContent = `frame → 127.0.0.1: HTTP ${r.status} (${Math.round(performance.now() - t0)} ms)`
  } catch (e) {
    $('rede').textContent = `frame → 127.0.0.1: bloqueado (${e.name}: ${e.message})`
  }
}

$('recarregar').addEventListener('click', carregar)
void carregar()
void sondar()
