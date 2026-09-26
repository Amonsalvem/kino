// Tokens de motion → src/tokens.generados.ts, dist/kino-motion.css y dist/tokens.json.
// Fuente única: los DTCG de la marca (duraciones, curvas, verbos, resortes, coreografía, colores). Aprobados en M1.
// Ningún valor se escribe a mano aquí: todo se lee o se calcula.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {build} from 'esbuild';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const PAQ = path.resolve(AQUI, '..');
const MARCA = path.resolve(PAQ, '../../gorr-brand-system/clientes/kino');
const leer = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

// El núcleo en TS se compila una vez para calcular resortes y linear().
fs.mkdirSync(path.join(PAQ, '.tmp'), {recursive: true});
await build({entryPoints: [path.join(PAQ, 'src/nucleo/calculo.ts')], bundle: true, format: 'esm', platform: 'node', outfile: path.join(PAQ, '.tmp/calculo.mjs'), logLevel: 'error'});
const {resolver, cssLinear, bezier} = await import(path.join(PAQ, '.tmp/calculo.mjs') + `?${Date.now()}`);

const mov = leer(path.join(MARCA, 'tokens/40-movimiento.tokens.json')).primitivo.movimiento;
const sem = leer(path.join(MARCA, 'tokens/50-semantico-comun.tokens.json')).semantico.movimiento;
const propio = mov; // desde el 26 sep, resortes y coreografía viven en la marca (40-movimiento)
const hojas = (n) => Object.entries(n).filter(([k]) => !k.startsWith('$'));

const duracion = Object.fromEntries(hojas(mov.duracion).map(([k, v]) => [k, v.$value.value]));
const escalonado = Object.fromEntries(hojas(mov.escalonado).map(([k, v]) => [k, v.$value.value]));
const curva = Object.fromEntries(hojas(mov.curva).map(([k, v]) => [k, v.$value]));
const distancia = Object.fromEntries(hojas(mov.distancia).map(([k, v]) => [k, v.$value.value]));
const verbo = {};
for (const [v, props] of hojas(sem)) {
	for (const [p, def] of hojas(props)) {
		const [, , familia, clave] = def.$value.slice(1, -1).split('.');
		verbo[`${v}/${p}`] = `${familia}/${clave}`;
	}
}
const resorte = {};
for (const [k, v] of hojas(propio.resorte)) {
	const params = {rigidez: v.rigidez.$value, amortiguacion: v.amortiguacion.$value, masa: v.masa.$value};
	const s = resolver(params);
	resorte[k] = {...params, asentamientoMs: Math.round(s.asentamiento * 1000), rebote: +s.rebote.toFixed(4), zeta: +s.zeta.toFixed(3), linear: cssLinear(s.easing)};
}
const coreografia = {
	cascadaMaximo: propio.coreografia['cascada-maximo'].$value,
	cascadaTopeMs: propio.coreografia['cascada-tope'].$value.value,
	salidaFactor: propio.coreografia['salida-factor'].$value,
};
// Colores semánticos resueltos a hex por tema (para la app nativa, que no lee CSS).
const resolverTema = (tema) => {
	const arbol = {};
	const fundir = (a, b) => { for (const [k, v] of Object.entries(b)) { if (v && typeof v === 'object' && !('$value' in v) && a[k] && typeof a[k] === 'object') fundir(a[k], v); else a[k] = v; } };
	for (const f of ['10-primitivo-color', '50-semantico-comun', `tema/${tema}`]) fundir(arbol, leer(path.join(MARCA, `tokens/${f}.tokens.json`)));
	const nodo = (ruta) => ruta.split('.').reduce((n, p) => n[p], arbol);
	const valor = (ruta) => { let v = nodo(ruta).$value; while (typeof v === 'string' && v.startsWith('{')) v = nodo(v.slice(1, -1)).$value; return v; };
	const salida = {};
	const recorrer = (n, pre) => { for (const [k, v] of Object.entries(n)) { if (k.startsWith('$')) continue; if (v && '$value' in v) { const x = valor(`semantico.${pre}${k}`); if (x && x.hex) salida[`${pre}${k}`.replaceAll('.', '/')] = (x.alpha ?? 1) < 1 ? 'transparent' : x.hex; } else if (v && typeof v === 'object') recorrer(v, `${pre}${k}.`); } };
	for (const grupo of ['superficie', 'texto', 'acento', 'accion', 'estado', 'borde']) recorrer({[grupo]: arbol.semantico[grupo]}, '');
	return salida;
};
const medida = leer(path.join(MARCA, 'tokens/30-primitivo-medida.tokens.json')).primitivo.medida;
const forma = {
	radio: {tarjeta: medida.radio.l.$value.value, control: medida.radio.m.$value.value, chip: medida.radio.s.$value.value},
	espacio: Object.fromEntries(hojas(medida.espacio).map(([k, v]) => [k, v.$value.value])),
};

const TOKENS = {
	fps: 60,
	duracion, escalonado, curva, distancia, verbo, resorte, coreografia,
	latirCiclos: propio.latir.ciclos.$value,
	avisoVisibleMs: propio.aviso.visible.$value.value,
	color: {oscuro: resolverTema('oscuro'), claro: resolverTema('claro')},
	forma,
	profundidad: Object.fromEntries(hojas(propio.profundidad).map(([k, v]) => [k, v.$value])),
	escala: Object.fromEntries(hojas(propio.escala).map(([k, v]) => [k, v.$value])),
};

// 1. TypeScript tipado
const ts = `// Generado por scripts/construir-tokens.mjs. No editar a mano.\nexport const TOKENS = ${JSON.stringify(TOKENS, null, '\t')} as const;\n`;
fs.writeFileSync(path.join(PAQ, 'src/tokens.generados.ts'), ts);

// 2. CSS: tokens de marca (colores, forma, tipo) + variables de motion con resortes como linear().
fs.mkdirSync(path.join(PAQ, 'dist'), {recursive: true});
const marcaCss = fs.readFileSync(path.join(MARCA, 'build/kino-tokens.css'), 'utf8');
const v = [];
for (const [k, ms] of Object.entries(duracion)) v.push(`--kino-mov-duracion-${k}: ${ms}ms;`);
for (const [k, ms] of Object.entries(escalonado)) v.push(`--kino-mov-escalonado-${k}: ${ms}ms;`);
for (const [k, c] of Object.entries(curva)) v.push(`--kino-mov-curva-${k}: cubic-bezier(${c.join(', ')});`);
for (const [k, d] of Object.entries(distancia)) v.push(`--kino-mov-distancia-${k}: ${d}px;`);
for (const [k, r] of Object.entries(resorte)) v.push(`--kino-mov-resorte-${k}: ${r.linear};`, `--kino-mov-resorte-${k}-duracion: ${r.asentamientoMs}ms;`);
for (const [nombre, destino] of Object.entries(verbo)) {
	const [fam, clave] = destino.split('/');
	v.push(`--kino-mov-${nombre.replace('/', '-')}: var(--kino-mov-${fam}-${clave});`);
}
v.push(`--kino-mov-escala-presion: ${TOKENS.escala.presion};`, `--kino-mov-escala-entrada: ${TOKENS.escala.entrada};`);
v.push('--kino-mov-velocidad: 1;');
const css = `/* Generado por scripts/construir-tokens.mjs: tokens de marca + motion. No editar a mano. */
${marcaCss}
:root {
  ${v.join('\n  ')}
}
/* Movimiento reducido: no se apaga, cambia de modo. Los componentes leen --kino-mov-reducido. */
:root { --kino-mov-reducido: 0; }
@media (prefers-reduced-motion: reduce) { :root:not([data-movimiento="completo"]) { --kino-mov-reducido: 1; } }
:root[data-movimiento="reducido"] { --kino-mov-reducido: 1; }

/* Cambio de pantalla (View Transitions). Solo se mueve la zona con view-transition-name: pantalla; la barra y la
   navegación se quedan quietas. Lo que tiene el mismo nombre en las dos vistas (pase-<id>) viaja con resorte/pase. */
::view-transition-group(*) { animation-duration: var(--kino-mov-resorte-pase-duracion); animation-timing-function: var(--kino-mov-resorte-pase); }
::view-transition-old(pantalla), ::view-transition-new(pantalla) { animation-duration: var(--kino-mov-duracion-crecer); animation-timing-function: var(--kino-mov-curva-crecer); }
html[data-transicion="adelante"]::view-transition-new(pantalla) { animation-name: kino-vt-entra-fin; }
html[data-transicion="adelante"]::view-transition-old(pantalla) { animation-name: kino-vt-sale-inicio; }
html[data-transicion="atras"]::view-transition-new(pantalla) { animation-name: kino-vt-entra-inicio; }
html[data-transicion="atras"]::view-transition-old(pantalla) { animation-name: kino-vt-sale-fin; }
html[data-transicion="hoja"]::view-transition-new(pantalla) { animation-name: kino-vt-sube; animation-duration: var(--kino-mov-resorte-hoja-duracion); animation-timing-function: var(--kino-mov-resorte-hoja); }
/* Reducido: nada viaja ni se desliza; lo viejo y lo nuevo se funden en su lugar con la duración de «crecer». */
html[data-transicion="fundido"]::view-transition-group(*) { animation-name: none; }
html[data-transicion="fundido"]::view-transition-old(*), html[data-transicion="fundido"]::view-transition-new(*) { animation-duration: var(--kino-mov-duracion-crecer); animation-timing-function: var(--kino-mov-curva-crecer); }
@keyframes kino-vt-entra-fin { from { opacity: 0; transform: translateX(var(--kino-mov-distancia-subida)); } }
@keyframes kino-vt-entra-inicio { from { opacity: 0; transform: translateX(calc(-1 * var(--kino-mov-distancia-subida))); } }
@keyframes kino-vt-sale-inicio { to { opacity: 0; transform: translateX(calc(-1 * var(--kino-mov-distancia-subida))); } }
@keyframes kino-vt-sale-fin { to { opacity: 0; transform: translateX(var(--kino-mov-distancia-subida)); } }
@keyframes kino-vt-sube { from { transform: translateY(100%); } }
`;
fs.writeFileSync(path.join(PAQ, 'dist/kino-motion.css'), css);

// 3. JSON portable (app nativa, Lottie, Figma): mismos nombres, duraciones en ms y en frames a 60 fps.
const portable = {...TOKENS, frames60: Object.fromEntries(Object.entries(duracion).map(([k, ms]) => [k, Math.floor((ms * 60) / 1000 + 0.5)]))};
fs.writeFileSync(path.join(PAQ, 'dist/tokens.json'), JSON.stringify(portable, null, 1) + '\n');

console.log(`tokens: ${Object.keys(duracion).length} duraciones, ${Object.keys(curva).length} curvas, ${Object.keys(resorte).length} resortes`);
for (const [k, r] of Object.entries(resorte)) console.log(`  resorte/${k}: ζ ${r.zeta}, ${r.asentamientoMs} ms, rebote ${(r.rebote * 100).toFixed(2)} %`);
void bezier;
