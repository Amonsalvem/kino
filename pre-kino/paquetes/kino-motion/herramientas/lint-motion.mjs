#!/usr/bin/env node
// lint-motion: encuentra movimiento escrito a mano (duraciones, curvas, easings) en lugar de tokens.
//   node herramientas/lint-motion.mjs <carpeta o archivo> [...]
// Una línea con «motion-ok: <razón>» queda exenta (por ejemplo, la barra de vigencia que sigue al reloj real).
import fs from 'node:fs';
import path from 'node:path';

const EXT = new Set(['.css', '.scss', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.html', '.vue', '.svelte']);
const IGNORAR = /(node_modules|dist|\.tmp|tokens\.generados\.ts|\.min\.)/;
const REGLAS = [
	{id: 'curva-literal', re: /cubic-bezier\(\s*[\d.]/, msg: 'curva escrita a mano: usa var(--kino-mov-curva-…) o curvaDe()'},
	{id: 'easing-generico', re: /(?:transition|animation|easing)[^;\n]*\b(ease|ease-in|ease-out|ease-in-out)\b(?![-\w])/, msg: 'easing genérico: usa una curva o un resorte del sistema'},
	{id: 'duracion-css', re: /(?:transition|animation)(?:-duration|-delay)?\s*:[^;\n]*\b\d+(?:\.\d+)?m?s\b/, msg: 'duración escrita a mano en CSS: usa var(--kino-mov-duracion-…)'},
	{id: 'duracion-js', re: /\b(?:duration|delay)\s*:\s*\d+(?:\.\d+)?\b/, msg: 'duración escrita a mano en JS: usa ms(\'…\') o animar() con un token'},
	{id: 'lineal', re: /(?:easing|transition|animation)[^;\n]*['"\s:]linear(?![-(\w])/, msg: '«linear» solo vale para el reloj real: márcalo con motion-ok'},
];

const archivos = [];
const recorrer = (p) => {
	if (IGNORAR.test(p)) return;
	const st = fs.statSync(p);
	if (st.isDirectory()) for (const h of fs.readdirSync(p)) recorrer(path.join(p, h));
	else if (EXT.has(path.extname(p))) archivos.push(p);
};
const entradas = process.argv.slice(2);
if (!entradas.length) {
	console.error('uso: lint-motion <carpeta o archivo> [...]');
	process.exit(2);
}
entradas.forEach(recorrer);

let hallazgos = 0;
for (const f of archivos) {
	fs.readFileSync(f, 'utf8').split('\n').forEach((linea, i) => {
		if (/motion-ok:/.test(linea)) return;
		for (const r of REGLAS) {
			if (r.re.test(linea)) {
				hallazgos++;
				console.log(`${f}:${i + 1}  [${r.id}] ${r.msg}\n    ${linea.trim().slice(0, 140)}`);
			}
		}
	});
}
console.log(`\nlint-motion: ${archivos.length} archivos, ${hallazgos} hallazgos`);
process.exit(hallazgos ? 1 : 0);
