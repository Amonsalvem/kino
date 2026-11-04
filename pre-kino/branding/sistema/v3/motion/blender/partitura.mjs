// Vuelca a partitura.json lo que Blender necesita de @kino/motion: tokens de motion (duraciones, curvas, resortes,
// escala, latir) y la partitura del Pase (TRANSICIONES de src/nucleo/pase.ts), además de las etiquetas del chip.
// Así el 3D se mueve con los mismos datos que la web. Requiere `npm run build` en paquetes/kino-motion.
//
//   node partitura.mjs
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const PAQ = path.resolve(AQUI, '../../../../../paquetes/kino-motion');
const {TRANSICIONES, TOKENS} = await import(pathToFileURL(path.join(PAQ, 'dist/nucleo.js')));
const base = fs.readFileSync(path.join(PAQ, 'src/web/componentes/base.ts'), 'utf8');
const etiqueta = Object.fromEntries([...base.matchAll(/^\s*'?([a-z-]+)'?: '([^']+)',$/gm)].map((m) => [m[1], m[2]]));

const datos = {
	fuente: 'paquetes/kino-motion (dist/nucleo.js y src/web/componentes/base.ts)',
	tokens: TOKENS,
	transiciones: TRANSICIONES,
	etiqueta,
};
fs.writeFileSync(path.join(AQUI, 'partitura.json'), JSON.stringify(datos, null, 1) + '\n');
console.log(`✓ partitura.json · ${TRANSICIONES.length} transiciones · ${Object.keys(TOKENS.resorte).length} resortes`);
