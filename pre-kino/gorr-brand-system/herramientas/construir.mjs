// Fase 4 · Compila los tokens DTCG a CSS (y a un JSON resuelto que usan contraste, skill y evals).
// Emisor propio, sin dependencias: primitivos con valor, capa semántica por REFERENCIA (var(--…)),
// un bloque por tema y la variante prefers-color-scheme para el tema secundario.
// Para salidas nativas (iOS/Android) o multiplataforma, usar terrazzo.config.mjs (ver README).
import { cliente, nombreVar, escribir } from './lib/cliente.mjs';
import { cargar, aplanar, resolver, valorCss, conReferencias, colorCss } from './lib/dtcg.mjs';

const c = cliente(process.argv[2]);
const nombrar = (ruta) => nombreVar(ruta, c.cfg);
const capas = c.cfg.capasSemanticas ?? [];
const esSemantico = (t) => capas.includes(t.ruta[0]);
const bloque = (sel, lineas) => `${sel} {\n${lineas.map((l) => `  ${l}`).join('\n')}\n}\n`;

const prim = aplanar(cargar(c.archivosTokens()));
// La capa semántica común (tokens/5x-semantico-*.json) se emite en cada tema, no entre los primitivos.
const soloPrim = [...prim.values()].filter((t) => !esSemantico(t));
const lineasPrim = soloPrim.map((t) => `--${nombrar(t.ruta)}: ${valorCss(resolver(prim, t.$value), t.$type, t.$extensions)};`);
let css = `/* ${c.cfg.cliente.nombre} · tokens · generado por gorr-brand-system. No editar a mano: editar tokens/ y reconstruir. */\n\n`;
css += bloque(':root', lineasPrim);

const resuelto = { primitivos: {}, temas: {} };
for (const t of soloPrim) resuelto.primitivos[nombrar(t.ruta)] = valorCss(resolver(prim, t.$value), t.$type, t.$extensions);

const [principal, ...otros] = c.temas;
for (const tema of c.temas) {
  const mapa = aplanar(cargar([...c.archivosTokens(), tema.archivo]));
  const sem = [...mapa.values()].filter(esSemantico);
  const lineas = [];
  if (tema.esquema) lineas.push(`color-scheme: ${tema.esquema};`);
  resuelto.temas[tema.id] = {};
  for (const t of sem) {
    lineas.push(`--${nombrar(t.ruta)}: ${valorCss(conReferencias(t.$value, nombrar), t.$type, t.$extensions)};`);
    const v = resolver(mapa, t.$value);
    resuelto.temas[tema.id][nombrar(t.ruta)] = t.$type === 'color' ? colorCss(v) : valorCss(v, t.$type, t.$extensions);
  }
  tema.lineas = lineas;
  css += '\n' + bloque(tema.selector, lineas);
  escribir(c.p('build', `tema-${tema.id}.css`), bloque(tema.selector, lineas));
}
// Sin atributo de tema, se sigue la preferencia del sistema operativo.
for (const tema of otros.filter((t) => t.esquema)) css += `\n@media (prefers-color-scheme: ${tema.esquema}) {\n${bloque(':root:not([data-tema])', tema.lineas).replace(/^/gm, '  ').trimEnd()}\n}\n`;

escribir(c.p('build', 'primitivos.css'), bloque(':root', lineasPrim));
escribir(c.p('build', `${c.prefijo}-tokens.css`), css);
escribir(c.p('build', 'tokens.resuelto.json'), resuelto);
console.log(`construir · ${soloPrim.length} primitivos · ${c.temas.map((t) => `${t.id} ${Object.keys(resuelto.temas[t.id]).length}`).join(' · ')} → build/${c.prefijo}-tokens.css`);
