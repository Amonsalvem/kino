// Bundle compartido por render-previews.mjs y render-masters.mjs.
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const SALIDA = path.join(AQUI, 'salida');
// Si Remotion no puede descargar su navegador, usa el Chromium del entorno: KINO_CHROMIUM=/ruta/chrome
export const navegador = process.env.KINO_CHROMIUM ?? null;

export const empaquetar = () =>
	bundle({entryPoint: path.join(AQUI, 'src/index.ts'), publicDir: path.join(AQUI, '../lottie')});

/** Filtro opcional por argumentos: node render-previews.mjs pase-latir hero */
export const elegidos = (ids) => {
	const filtros = process.argv.slice(2);
	return filtros.length ? ids.filter((id) => filtros.some((f) => id.includes(f))) : ids;
};
