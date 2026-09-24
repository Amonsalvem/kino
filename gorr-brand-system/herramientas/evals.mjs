// Fase 5 · Genera la suite de evaluación de copy con IA (promptfoo) desde voz.json y la skill.
// Tres capas de aserción por caso: (1) términos prohibidos, deterministas; (2) la compuerta de voz.mjs
// como aserción JavaScript; (3) una rúbrica LLM construida con el perfil NN/g. La rúbrica es
// independiente de promptfoo: vive en evals/rubrica.md para poder cambiar de evaluador sin reescribirla.
//   node herramientas/evals.mjs <cliente>        luego, con red:  cd clientes/<id>/evals && npx promptfoo@latest eval
import { readFileSync, existsSync } from 'node:fs';
import { relative } from 'node:path';
import { cliente, escribir, salir, RAIZ } from './lib/cliente.mjs';

const c = cliente(process.argv[2]);
if (!existsSync(c.p('voz.json'))) salir('Falta voz.json (fase 2).');
const voz = JSON.parse(readFileSync(c.p('voz.json'), 'utf8'));
const skill = c.p('skill', `${c.id}-marca`, 'SKILL.md');
if (!existsSync(skill)) salir('Primero: npm run skill');
const cfgE = c.cfg.evals ?? {};
const proveedor = cfgE.proveedor ?? 'anthropic:messages:claude-sonnet-4-5';
const q = (s) => JSON.stringify(s); // YAML acepta cadenas JSON

// Rúbrica legible por humanos y por cualquier evaluador
const p = voz.perfil ?? {};
const dims = ['formalidad', 'humor', 'respeto', 'entusiasmo'].filter((d) => p[d])
  .map((d) => `- ${p[d].polos[0]} ↔ ${p[d].polos[1]}: objetivo ${p[d].valor}/5. ${p[d].nota ?? ''}`);
const rubrica = [
  `Evalúa si el texto está escrito con la voz de ${c.cfg.cliente.nombre}. Aprueba solo si cumple TODOS los criterios.`,
  '', 'Tono (escala NN/g, 1 = primer polo, 5 = segundo; tolerancia ±1):', ...dims,
  '', 'Debe ser:', ...(voz.somos ?? []).map((s) => `- ${s}`),
  '', 'No debe ser:', ...(voz.noSomos ?? []).map((s) => `- ${s}`),
  '', 'Vocabulario:', ...(voz.vocabulario?.noMezclar ?? []).map((n) => `- ${n.regla}`),
  ...(voz.vocabulario?.usar ?? []).map((u) => `- «${u.termino}»: ${u.significa}`),
  ...(voz.hechos ? ['', 'Hechos del producto que el texto PUEDE afirmar:', ...(voz.hechos.confirmado ?? []).map((h) => `- ${h}`), 'NO puede afirmar (no confirmado):', ...(voz.hechos.noConfirmado ?? []).map((h) => `- ${h}`), 'Cualquier otra afirmación sobre el producto que no esté aquí ni en el contexto del caso es falla.'] : []),
  '', 'Además: sin antítesis de efecto («no es X, es Y»), sin tríadas por inercia, sin frases de relleno ni superlativos.',
  'Devuelve el motivo concreto si falla.',
].join('\n');
escribir(c.p('evals', 'rubrica.md'), rubrica + '\n');

// Prompt: la skill completa como sistema + la tarea
const cuerpoSkill = readFileSync(skill, 'utf8').replace(/^---[\s\S]*?---\n/, '');
escribir(c.p('evals', 'prompt.json'), JSON.stringify([
  { role: 'system', content: cuerpoSkill },
  { role: 'user', content: 'Tarea: {{tarea}}\nContexto: {{contexto}}\n\nEntrega solo el texto final, sin explicaciones.' },
], null, 2) + '\n');

// Aserción JS que reutiliza la compuerta determinista (voz.mjs)
const rutaVoz = relative(c.p('evals'), `${RAIZ}/herramientas/voz.mjs`).replace(/\\/g, '/');
escribir(c.p('evals', 'voz-assert.cjs'), `// Generado. Reutiliza herramientas/voz.mjs como aserción de promptfoo.
const path = require('node:path');
const { readFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
module.exports = async (salida) => {
  const { reglas, revisar } = await import(pathToFileURL(path.join(__dirname, ${q(rutaVoz)})).href);
  const voz = JSON.parse(readFileSync(path.join(__dirname, '..', 'voz.json'), 'utf8'));
  const errores = revisar(String(salida), reglas(voz)).filter((h) => h.gravedad === 'error');
  return { pass: errores.length === 0, score: errores.length ? 0 : 1,
    reason: errores.length ? errores.map((e) => \`[\${e.id}] «\${e.fragmento}»\`).join('; ') : 'sin errores de voz' };
};
`);

const prohibidos = (voz.vocabulario?.evitar ?? []).filter((e) => !e.patron).map((e) => e.termino);
const yaml = [
  `# Generado por gorr-brand-system (herramientas/evals.mjs). No editar: cambiar voz.json y regenerar.`,
  `# Correr (requiere red y ANTHROPIC_API_KEY):  npx promptfoo@latest eval && npx promptfoo@latest view`,
  `# Umbral de producto: el copy pasa sin edición en >= ${Math.round((cfgE.umbral ?? 0.8) * 100)} % de los casos.`,
  `description: ${q(`Voz de ${c.cfg.cliente.nombre}`)}`,
  `prompts:`, `  - file://prompt.json`,
  `providers:`, `  - id: ${proveedor}`, `    config:`, `      temperature: 0.7`,
  `defaultTest:`, `  assert:`,
  ...prohibidos.map((t) => `    - type: not-icontains\n      value: ${q(t)}`),
  `    - type: javascript`, `      value: file://voz-assert.cjs`,
  `    - type: llm-rubric`, `      value: file://rubrica.md`,
  `tests:`,
  ...(voz.casos ?? []).map((k) => `  - description: ${q(k.tarea)}\n    vars:\n      tarea: ${q(k.tarea)}\n      contexto: ${q(k.contexto ?? '')}`),
  '',
].join('\n');
escribir(c.p('evals', 'promptfooconfig.yaml'), yaml);
console.log(`evals · ${voz.casos?.length ?? 0} casos · ${prohibidos.length} términos + compuerta de voz + rúbrica NN/g → evals/promptfooconfig.yaml`);
