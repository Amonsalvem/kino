// Fase 5 · Empaqueta la marca del cliente como Agent Skill (formato abierto de Anthropic, agentskills.io).
// Se GENERA desde las fuentes (marca.config.json, voz.json, tokens construidos): nunca se edita a mano,
// así la skill no se desincroniza de la marca. Salida: clientes/<id>/skill/<id>-marca/
import { readFileSync, existsSync, copyFileSync, mkdirSync } from 'node:fs';
import { cliente, escribir, salir } from './lib/cliente.mjs';
import { cargar, aplanar } from './lib/dtcg.mjs';

const c = cliente(process.argv[2]);
const cfg = c.cfg, nombre = cfg.cliente.nombre;
const idSkill = `${c.id}-marca`.toLowerCase().replace(/[^a-z0-9-]/g, '-');
if (idSkill.length > 64) salir('El nombre de la skill supera 64 caracteres.');
const voz = existsSync(c.p('voz.json')) ? JSON.parse(readFileSync(c.p('voz.json'), 'utf8')) : null;
const resArch = c.p('build', 'tokens.resuelto.json');
if (!existsSync(resArch)) salir('Primero: npm run construir');
const res = JSON.parse(readFileSync(resArch, 'utf8'));
const temaP = c.temas[0]?.id;
const vars = res.temas[temaP] ?? {};

const descripcion = `Aplica la marca ${nombre} (color, tipografía, voz y vocabulario) a cualquier pieza: deck, documento, página HTML, interfaz o texto de producto. Usar al producir o revisar cualquier entregable de ${nombre}.`;
if (descripcion.length > 1024) salir('Descripción > 1024 caracteres.');

const md = [];
md.push(`---\nname: ${idSkill}\ndescription: ${descripcion}\n---\n`);
md.push(`# Marca ${nombre}\n\n> Generado por gorr-brand-system desde las fuentes del cliente. No editar a mano: cambiar marca.config.json, voz.json o tokens/ y correr \`npm run ciclo -- ${c.id}\`.\n`);
if (cfg.reglas?.length) md.push(`## Reglas que no se negocian\n\n${cfg.reglas.map((r, i) => `${i + 1}. ${r}`).join('\n')}\n`);

// Color: familias con su significado y el problema que resuelven
const fams = { ...(cfg.color?.neutros ?? {}), ...(cfg.color?.familias ?? {}) };
if (Object.keys(fams).length) {
  md.push(`## Color\n\nCada familia significa algo. No usar una familia fuera de su significado.\n\n| Familia | Significa | Por qué existe |\n|---|---|---|`);
  for (const [k, f] of Object.entries(fams)) md.push(`| \`${k}\` | ${f.significa ?? ''} | ${f.porque ?? ''} |`);
  md.push('');
}
if (Object.keys(vars).length) {
  md.push(`### Tokens semánticos (tema ${temaP}, canónico)\n\nEn código, usar siempre la variable, nunca el hex. El hex va solo para herramientas que no leen CSS.\n\n| Variable | Valor |\n|---|---|`);
  for (const [k, v] of Object.entries(vars)) if (/^#|^oklch/.test(v)) md.push(`| \`--${k}\` | \`${v}\` |`);
  md.push('');
}
// Tipografía
const prim = aplanar(cargar(c.archivosTokens()));
const fuentes = [...prim.values()].filter((t) => t.$type === 'fontFamily');
const pasos = [...prim.values()].filter((t) => t.ruta.includes('texto') && t.$type === 'dimension');
if (fuentes.length || pasos.length) {
  md.push(`## Tipografía\n`);
  for (const f of fuentes) md.push(`- \`--${[c.prefijo, ...f.ruta.slice(-2)].join('-')}\`: ${Array.isArray(f.$value) ? f.$value.join(', ') : f.$value}`);
  if (pasos.length) md.push(`\nEscala fluida (Utopia) de ${pasos.length} pasos: \`--${c.prefijo}-texto-0\` es el cuerpo; los positivos suben, \`n1\` baja. Valores exactos en references/tokens.css.`);
  md.push('');
}
md.push(`## Cómo aplicarla en código\n\n\`\`\`html\n<link rel="stylesheet" href="${c.prefijo}-tokens.css">\n<body${c.temas.length > 1 ? ` data-tema="${temaP}"` : ''}>\n\`\`\`\n\n${c.temas.length > 1 ? `Temas: ${c.temas.map((t) => `\`${t.id}\``).join(', ')}. Sin atributo, sigue la preferencia del sistema.` : ''} El CSS completo está en references/tokens.css.\n`);

if (voz) {
  const p = voz.perfil;
  md.push(`## Voz y tono\n\nPerfil según las cuatro dimensiones de NN/g (1 = primer polo, 5 = segundo)${p.estado ? `. Estado: ${p.estado}` : ''}.\n\n| Dimensión | Valor | Cómo se nota |\n|---|---|---|`);
  for (const d of ['formalidad', 'humor', 'respeto', 'entusiasmo']) if (p[d]) md.push(`| ${p[d].polos.join(' ↔ ')} | ${p[d].valor} | ${p[d].nota ?? ''} |`);
  if (voz.somos) md.push(`\n**Somos:**\n${voz.somos.map((s) => `- ${s}`).join('\n')}`);
  if (voz.noSomos) md.push(`\n**No somos:**\n${voz.noSomos.map((s) => `- ${s}`).join('\n')}`);
  const v = voz.vocabulario ?? {};
  if (v.usar?.length) md.push(`\n### Vocabulario propio\n\n${v.usar.map((u) => `- **${u.termino}**: ${u.significa}`).join('\n')}`);
  if (v.noMezclar?.length) md.push(`\n${v.noMezclar.map((n) => `- Nunca mezclar «${n.a}» y «${n.b}»: ${n.regla}`).join('\n')}`);
  if (v.evitar?.length) md.push(`\n### Evitar\n\n| No escribir | Escribir | Por qué |\n|---|---|---|\n${v.evitar.map((e) => `| ${e.termino} | ${e.usar ?? ''} | ${e.porque} |`).join('\n')}`);
  if (voz.hechos) md.push(`\n### Lo que el producto hace\n\n${voz.hechos.$nota ?? ''}\n\n**Confirmado (se puede afirmar):**\n${(voz.hechos.confirmado ?? []).map((h) => `- ${h}`).join('\n')}${voz.hechos.noConfirmado?.length ? `\n\n**No confirmado (no se afirma):**\n${voz.hechos.noConfirmado.map((h) => `- ${h}`).join('\n')}` : ''}`);
  if (voz.patrones?.length) md.push(`\n### Patrones prohibidos\n\n${voz.patrones.map((x) => `- ${x.porque}`).join('\n')}`);
  md.push('');
}
md.push(`## Antes de entregar\n\n1. Si hay código: solo variables \`--${c.prefijo}-*\`, ningún hex suelto.\n2. Si hay texto: revisar contra la sección de voz; en el repo, \`npm run voz -- ${c.id} <archivo>\`.\n3. Si hay combinaciones nuevas de texto y fondo: agregarlas a pares.json y correr \`npm run contraste -- ${c.id}\`.\n`);

const dir = c.p('skill', idSkill);
escribir(`${dir}/SKILL.md`, md.join('\n'));
mkdirSync(`${dir}/references`, { recursive: true });
copyFileSync(c.p('build', `${c.prefijo}-tokens.css`), `${dir}/references/tokens.css`);
if (voz) copyFileSync(c.p('voz.json'), `${dir}/references/voz.json`);
console.log(`skill · ${idSkill} · ${md.join('\n').split('\n').length} líneas → skill/${idSkill}/SKILL.md`);
