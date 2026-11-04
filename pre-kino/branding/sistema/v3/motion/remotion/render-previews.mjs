// mp4_preview de cada recurso Lottie (H.264), a partir del wrapper @remotion/lottie.
import fs from 'node:fs';
import path from 'node:path';
import {getCompositions, renderMedia} from '@remotion/renderer';
import {elegidos, empaquetar, navegador, SALIDA} from './render-comun.mjs';

const serveUrl = await empaquetar();
const todas = await getCompositions(serveUrl, {browserExecutable: navegador});
const vistas = todas.filter((c) => c.id.startsWith('vista-'));
fs.mkdirSync(path.join(SALIDA, 'previews'), {recursive: true});
for (const id of elegidos(vistas.map((c) => c.id))) {
	const composition = vistas.find((c) => c.id === id);
	const outputLocation = path.join(SALIDA, 'previews', `${id.replace(/^vista-/, '')}.mp4`);
	await renderMedia({composition, serveUrl, codec: 'h264', outputLocation, browserExecutable: navegador});
	console.log('✓', outputLocation);
}
