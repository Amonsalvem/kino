// Empaqueta: dist/kino-motion.js (ESM), dist/kino-motion.iife.js (global KinoMotion) y dist/nucleo.js (sin DOM).
import {build} from 'esbuild';
const comun = {bundle: true, target: 'es2022', logLevel: 'warning', legalComments: 'none'};
await build({...comun, entryPoints: ['src/index.ts'], format: 'esm', outfile: 'dist/kino-motion.js', sourcemap: true});
await build({...comun, entryPoints: ['src/index.ts'], format: 'iife', globalName: 'KinoMotion', outfile: 'dist/kino-motion.iife.js', minify: true});
await build({...comun, entryPoints: ['src/nucleo/index.ts'], format: 'esm', outfile: 'dist/nucleo.js', platform: 'neutral'});
console.log('dist: kino-motion.js, kino-motion.iife.js, nucleo.js');
