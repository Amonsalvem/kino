// Arma lab/dist/kino-motion-lab.html: una sola página con el CSS del sistema y el Lab empaquetado.
import fs from 'node:fs';
import {build} from 'esbuild';
const r = await build({entryPoints: ['lab/lab.ts'], bundle: true, format: 'iife', target: 'es2022', minify: true, write: false, legalComments: 'none'});
const js = r.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');
const css = fs.readFileSync('dist/kino-motion.css', 'utf8');
const html = fs.readFileSync('lab/plantilla.html', 'utf8').replace('/*CSS_SISTEMA*/', () => css).replace('/*JS_LAB*/', () => js);
fs.mkdirSync('lab/dist', {recursive: true});
fs.writeFileSync('lab/dist/kino-motion-lab.html', html);
console.log(`lab: ${(html.length / 1024).toFixed(0)} KB`);
