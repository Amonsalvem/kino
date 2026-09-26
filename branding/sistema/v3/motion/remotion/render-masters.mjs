// Maestros de las composiciones «remotion»: ProRes 4444 con alfa y secuencia PNG del póster.
// La codificación a AV1, H.264 y AVIF la hace el pipeline, no este script.
import fs from 'node:fs';
import path from 'node:path';
import {getCompositions, renderMedia, renderStill} from '@remotion/renderer';
import {elegidos, empaquetar, navegador, SALIDA} from './render-comun.mjs';

const serveUrl = await empaquetar();
const todas = await getCompositions(serveUrl, {browserExecutable: navegador});
const ids = todas.map((c) => c.id).filter((id) => !id.startsWith('vista-'));
fs.mkdirSync(path.join(SALIDA, 'masters'), {recursive: true});
for (const id of elegidos(ids)) {
	const composition = todas.find((c) => c.id === id);
	const outputLocation = path.join(SALIDA, 'masters', `${id}.mov`);
	await renderMedia({
		composition,
		serveUrl,
		codec: 'prores',
		proResProfile: '4444',
		pixelFormat: 'yuva444p10le',
		imageFormat: 'png',
		outputLocation,
		browserExecutable: navegador,
	});
	console.log('✓', outputLocation);
	if (!id.endsWith('-reducido') && typeof composition.defaultProps.poster === 'number') {
		const poster = path.join(SALIDA, 'masters', `${id}.poster.png`);
		await renderStill({composition, serveUrl, frame: composition.defaultProps.poster, output: poster, imageFormat: 'png', browserExecutable: navegador});
		console.log('✓', poster);
	}
}
