// Gera as variantes do símbolo BrzA a partir do traço mono de hoje (PLN-007, P1, D1 e D2).
// Uso: node brza-brand-build.mjs <pasta de saída> [resources/brza-flame-mono.svg]
// Saída: brza-symbol.svg (mestre), brza-symbol-light.svg, brza-symbol-dev.svg, brza-symbol-mono.svg (S1),
// brza-tray-template.svg (S1 preto em 22×14) e logo.svg (cópia do mestre, R5.2).
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const [out = '.', monoPath = `${process.env.HOME}/Projects/brza-studio/resources/brza-flame-mono.svg`] = process.argv.slice(2);
const d = readFileSync(monoPath, 'utf8').match(/ d="([^"]+)"/)[1];
// Os 13 subpaths do traço mono: 4 e 6 são as metades partidas do } solto, que o S1 troca pelo } na escala 1,143.
const sub = d.split(/(?=M)/).filter(Boolean);
if (sub.length !== 13) throw new Error(`o traço mono tem ${sub.length} subpaths, esperava 13`);
const BRACE = sub[3];
const FLAME = [0, 1, 2, 7, 8, 9, 10, 11, 12].map((i) => sub[i]).join('');

// Aplica a matriz [a, b, c, d, e, f] a cada par de coordenadas de um path absoluto (M, C, L, Z).
function xform(s, [a, b, c, dd, e, f]) {
  const t = s.match(/[MCLZ]|-?\d*\.?\d+/g);
  let k = 0; let x = 0;
  return t.map((tok) => {
    if (/[MCLZ]/.test(tok)) return tok;
    const v = Number(tok);
    if (k % 2 === 0) { x = v; k++; return ''; }
    k++;
    const nx = a * x + c * v + e;
    const ny = b * x + dd * v + f;
    return `${nx.toFixed(2)} ${ny.toFixed(2)}`;
  }).filter((s) => s !== '').join(' ').replace(/ ([MCLZ])/g, '$1');
}

// Os três usos do } (D1): par, { espelhado e solto na escala 1,143 em (9,06; 16,68).
const MIRROR_OPEN = [-1, 0, 0, 1, 26.81, -0.03];
const SOLTO = [1.143, 0, 0, 1.143, 9.06 - 13.57 * 1.143, 16.68 - 17.05 * 1.143];
const S1_EXTRA = [xform(BRACE, [1, 0, 0, 1, 0, 0]), xform(BRACE, MIRROR_OPEN), xform(BRACE, SOLTO)];

// S1 em paths achatados (sem <use>), para o tray e para o arquivo mono.
const S1_D = [FLAME, ...S1_EXTRA].join(' ');

const FIRE = `<stop offset="0" stop-color="#FFAA44"/><stop offset=".30" stop-color="#F4902A"/><stop offset=".65" stop-color="#F26228"/><stop offset="1" stop-color="#E04A2B"/>`;
const FLAME_T = 'translate(512 512) scale(22) translate(-12.01 -11.985)';
// No ícone com selo a chama encolhe (20,6 em vez de 22) e sobe para dar lugar ao texto; o grupo chama e texto fica
// centrado no tile, com ~125 px de margem em cima e embaixo.
const SEAL_FLAME_T = 'translate(512 453) scale(20.6) translate(-12.01 -11.985)';
const TILE = `<rect x="100" y="100" width="824" height="824" rx="185"`;

function master({ light = false, dev = false, seal = false } = {}) {
  const tileFill = light ? 'url(#brza-tile-light)' : 'url(#brza-tile-dark)';
  const devBadge = dev
    ? `<g id="dev-badge"><circle cx="800" cy="800" r="150" fill="#1447E6"/>` +
      `<path fill="#FFFFFF" fill-rule="evenodd" d="M740 720H785A80 80 0 0 1 785 880H740Z M765 745H785A55 55 0 0 1 785 855H765Z"/></g>`
    : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <title>BrzA</title>
  <defs>
    <linearGradient id="brza-fire" gradientUnits="userSpaceOnUse" x1="0" y1="0.96" x2="0" y2="23.01">${FIRE}</linearGradient>
    <linearGradient id="brza-fire-tile" x1="0" y1="0" x2="0" y2="1">${FIRE}</linearGradient>
    <linearGradient id="brza-tile-dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#373A41"/><stop offset=".6" stop-color="#2C2D32"/><stop offset="1" stop-color="#19161D"/></linearGradient>
    <linearGradient id="brza-tile-light" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F6F6F8"/></linearGradient>
    <clipPath id="brza-tile-clip"><rect x="100" y="100" width="824" height="824" rx="185"/></clipPath>
    <path id="brza-brace-close" d="${BRACE}"/>
  </defs>
  <g id="tile">
    ${TILE} fill="${tileFill}"/>
    <g clip-path="url(#brza-tile-clip)">
      ${TILE} fill="none" stroke="url(#brza-fire-tile)" stroke-width="24"/>
      ${TILE} fill="none" stroke="#FFFFFF" stroke-opacity=".07" stroke-width="8" transform="translate(0 12)"/>
    </g>
  </g>
  <g id="flame" transform="${seal ? SEAL_FLAME_T : FLAME_T}" fill="url(#brza-fire)">
    <path id="flame-glyph" fill-rule="evenodd" d="${FLAME}"/>
    <use href="#brza-brace-close"/>
    <use href="#brza-brace-close" transform="matrix(-1 0 0 1 26.81 -0.03)"/>
    <use href="#brza-brace-close" transform="matrix(1.143 0 0 1.143 ${SOLTO[4].toFixed(2)} ${SOLTO[5].toFixed(2)})"/>
  </g>
  ${seal ? sealSvg() : ''}
  ${devBadge}
</svg>
`;
}

const mono = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="${S1_D}"/>
</svg>
`;

// 22×14 do tray: a chama de 14 px de altura, centrada, em preto (template monocromático).
const tray = `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="14" viewBox="0 0 22 14">
  <path fill="#000" fill-rule="evenodd" transform="translate(11 7) scale(0.635) translate(-12.01 -11.985)" d="${S1_D}"/>
</svg>
`;

// ---- O texto em path (D3): uma chamada do CoreText por texto, em px de uma fonte de 100 px ----
const FONT = process.env.BRZA_FONT ?? `${process.env.HOME}/Projects/brza-studio/src/renderer/src/assets/fonts/Geist-Variable.woff2`;
const SWIFT = join(dirname(fileURLToPath(import.meta.url)), 'brza-brand-text.swift');
const text = (t, wght, tracking) => JSON.parse(execFileSync('swift', [SWIFT, FONT, String(wght), String(tracking), t], { encoding: 'utf8' }));
const T = {
  BrzA: text('BrzA', 750, -0.01),
  STUDIO: text('STUDIO', 500, 0.14), CLI: text('CLI', 500, 0.14), WORKSPACE: text('WORKSPACE', 500, 0.14),
};
const NAME = { STUDIO: 'Studio', CLI: 'CLI', WORKSPACE: 'Workspace' };
const n3 = (v) => (Math.round(v * 1000) / 1000).toString();
const at = (x, y, s) => `translate(${n3(x)} ${n3(y)}) scale(${n3(s)})`;
const plain = (t, x, y, s, fill) => `<path fill="${fill}" transform="${at(x, y, s)}" d="${t.d}"/>`;
// "BrzA": "Brz" na cor do tema e o "A" no degradê da marca.
const brza = (x, y, s, ink) =>
  `<path fill="${ink}" transform="${at(x, y, s)}" d="${T.BrzA.glyphs.slice(0, 3).join('')}"/>` +
  `<path fill="url(#brza-fire-tile)" transform="${at(x, y, s)}" d="${T.BrzA.glyphs[3]}"/>`;

// O selo do ícone do app: "BrzA STUDIO" sob a chama, em uma linha (tile de 824 em 100,100).
function sealSvg() {
  const [sA, sS] = [0.8, 0.608];
  const wA = T.BrzA.advance * sA, wS = T.STUDIO.advance * sS, gap = 0.5 * 80;
  const x0 = 512 - (wA + gap + wS) / 2;
  const y1 = 770 + (T.BrzA.capHeight * sA) / 2;
  return `<g id="seal">${brza(x0, y1, sA, '#FAFAFA')}${plain(T.STUDIO, x0 + wA + gap, y1, sS, '#BCBCBC')}</g>`;
}

const master_svg = master();
writeFileSync(join(out, 'brza-symbol.svg'), master_svg);
writeFileSync(join(out, 'brza-symbol-light.svg'), master({ light: true }));
writeFileSync(join(out, 'brza-symbol-dev.svg'), master({ dev: true }));
writeFileSync(join(out, 'brza-symbol-mono.svg'), mono);
writeFileSync(join(out, 'brza-tray-template.svg'), tray);
writeFileSync(join(out, 'logo.svg'), master_svg);
console.log('ok', out, 'S1 subpaths:', S1_D.split(/(?=M)/).filter(Boolean).length);

// ---- Os lockups L2 (D3): 4 nomes × horizontal e vertical × escuro e claro = 16 arquivos ----
const THEME = {
  dark: { mother: '#FAFAFA', daughter: '#BCBCBC', master: master_svg },
  light: { mother: '#0A0A0A', daughter: '#474747', master: master({ light: true }) },
};
const body = (svg) => svg.replace(/^<svg[^>]*>\s*/, '').replace(/\s*<\/svg>\s*$/, '').replace(/<title>[^<]*<\/title>\s*/, '');
const doc = (W, Hh, title, parts) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n3(W)} ${n3(Hh)}" width="${n3(W)}" height="${n3(Hh)}">\n  <title>${title}</title>\n  ${parts}\n</svg>\n`;
const H = 100; // altura do símbolo; as outras medidas são razões dela (D3)

function lockup(layout, theme, daughter) {
  const th = THEME[theme];
  const sym = (x) => `<g transform="translate(${n3(x)} 0) scale(${n3(H / 824)}) translate(-100 -100)">${body(th.master)}</g>`;
  const title = daughter ? `BrzA ${NAME[daughter]}` : 'BrzA';
  if (layout === 'horizontal') {
    const [sm, sd] = [0.62 * H / 100, 0.47 * H / 100];
    const x0 = H + 0.265 * H;
    const base = H / 2 + (T.BrzA.capHeight * sm) / 2; // o meio da caixa alta no meio do símbolo
    const wm = T.BrzA.advance * sm;
    let parts = sym(0) + brza(x0, base, sm, th.mother);
    let W = x0 + wm;
    if (daughter) {
      const xd = x0 + wm + 0.5 * (0.62 * H);
      parts += plain(T[daughter], xd, base, sd, th.daughter);
      W = xd + T[daughter].advance * sd;
    }
    return doc(W, H, title, parts);
  }
  const [sm, sd, gap] = [0.375 * H / 100, 0.29 * H / 100, 0.11 * H];
  const wm = T.BrzA.advance * sm;
  const wd = daughter ? T[daughter].advance * sd : 0;
  const W = Math.max(H, wm, wd);
  const baseM = H + gap + T.BrzA.capHeight * sm;
  let parts = sym((W - H) / 2) + brza((W - wm) / 2, baseM, sm, th.mother);
  let Hh = baseM;
  if (daughter) {
    Hh = baseM + gap + T[daughter].capHeight * sd;
    parts += plain(T[daughter], (W - wd) / 2, Hh, sd, th.daughter);
  }
  return doc(W, Hh, title, parts);
}

writeFileSync(join(out, 'brza-app-icon.svg'), master({ seal: true }));
for (const theme of ['dark', 'light']) {
  for (const layout of ['horizontal', 'vertical']) {
    for (const daughter of [null, 'STUDIO', 'CLI', 'WORKSPACE']) {
      const name = daughter ? `brza-${daughter.toLowerCase()}-lockup-${layout}-${theme}.svg` : `brza-lockup-${layout}-${theme}.svg`;
      writeFileSync(join(out, name), lockup(layout, theme, daughter));
    }
  }
}
console.log('lockups: 16 · selo: brza-app-icon.svg');
