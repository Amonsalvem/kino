// Construye el prototipo: build/kino-prototipo.html (tokens, estilos y JS adentro) y build/assets/ con los videos
// 3D aprobados (M3D) y sus pósters, que se publican como archivos de apoyo del artefacto.
// Uso: node construir.mjs
import {build} from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const tokens = path.resolve(aqui, '../gorr-brand-system/clientes/kino/build');
const salida = path.join(aqui, 'build');
fs.mkdirSync(salida, {recursive: true});

const js = await build({
	entryPoints: [path.join(aqui, 'src/app.tsx')],
	bundle: true,
	minify: true,
	format: 'iife',
	target: 'es2022',
	jsx: 'automatic',
	jsxImportSource: 'preact',
	write: false,
	legalComments: 'none',
});

// Tokens: primitivos y tema oscuro en :root; el claro se aplica a cualquier elemento con data-tema="claro"
// (el teléfono de la visita), no al documento entero.
const todo = fs.readFileSync(path.join(tokens, 'kino-tokens.css'), 'utf8');
const sinMedia = todo.replace(/@media \(prefers-color-scheme: light\)[\s\S]*$/, '');
const tokensCss = sinMedia.replace(':root[data-tema="claro"]', '[data-tema="claro"]');
const estilos = fs.readFileSync(path.join(aqui, 'src/estilos.css'), 'utf8');

const html = `<!doctype html>
<html lang="es" data-tema="oscuro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kino · Prototipo</title>
<meta name="description" content="Prototipo navegable de Kino: residente, visita sin cuenta, portería y administración comparten un solo estado.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>${tokensCss}\n${estilos}</style>
</head>
<body>
<div id="app"></div>
<script>${js.outputFiles[0].text.replace(/<\/script/g, '<\\/script')}</script>
</body>
</html>
`;
// Assets: pósters propios (prototipo/assets) y los videos 3D aprobados, sin copiarlos al repositorio dos veces.
const assets = path.join(salida, 'assets');
fs.mkdirSync(assets, {recursive: true});
for (const f of fs.readdirSync(path.join(aqui, 'assets'))) fs.copyFileSync(path.join(aqui, 'assets', f), path.join(assets, f));
const m3d = path.resolve(aqui, '../branding/sistema/v3/motion/entregables/conjunto-noche-lector-confirma');
for (const [de, a] of [
	['conjunto-noche-lector-confirma.vp9.webm', 'porteria.webm'],
	['conjunto-noche-lector-confirma.hevc_app.mp4', 'porteria.mp4'],
	['conjunto-noche-lector-confirma.reducido.vp9.webm', 'porteria-reducido.webm'],
	['conjunto-noche-lector-confirma.reducido.hevc_app.mp4', 'porteria-reducido.mp4'],
])
	fs.copyFileSync(path.join(m3d, de), path.join(assets, a));
const peso = fs.readdirSync(assets).reduce((t, f) => t + fs.statSync(path.join(assets, f)).size, 0);

const destino = path.join(salida, 'kino-prototipo.html');
fs.writeFileSync(destino, html);
console.log(`ok ${path.relative(process.cwd(), destino)} · ${(html.length / 1024).toFixed(0)} KB · assets ${(peso / 1024).toFixed(0)} KB`);
