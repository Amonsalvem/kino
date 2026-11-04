// Une el arnés en un solo HTML (JS en línea) para publicarlo como artefacto: web/dist/kino-motion-nativo.html
import fs from 'node:fs';
const d = new URL('./dist/', import.meta.url).pathname;
let h = fs.readFileSync(d + 'index.html', 'utf8');
const m = h.match(/<script type="module" crossorigin src="\.\/(assets\/[^"]+\.js)"><\/script>/);
const js = fs.readFileSync(d + m[1], 'utf8').replace(/<\/script/gi, '<\\/script');
h = h.replace(m[0], () => `<script type="module">${js}</script>`);
fs.writeFileSync(d + 'kino-motion-nativo.html', h);
console.log(`kino-motion-nativo.html: ${Math.round(h.length / 1024)} KB`);
