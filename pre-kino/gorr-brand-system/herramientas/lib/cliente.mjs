// Localiza un cliente y lee su marca.config.json.
// Uso en cada herramienta: const c = cliente(process.argv[2]);
import { readFileSync, existsSync, readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');

export function cliente(arg) {
  if (!arg) salir('Falta el cliente. Ejemplo: npm run ciclo -- kino');
  const dir = existsSync(join(RAIZ, 'clientes', arg)) ? join(RAIZ, 'clientes', arg) : resolve(arg);
  const archivo = join(dir, 'marca.config.json');
  if (!existsSync(archivo)) salir(`No encuentro ${archivo}`);
  const cfg = JSON.parse(readFileSync(archivo, 'utf8'));
  const p = (...x) => join(dir, ...x);
  const tokens = p('tokens');
  const archivosTokens = () =>
    existsSync(tokens) ? readdirSync(tokens).filter((f) => f.endsWith('.tokens.json')).sort().map((f) => join(tokens, f)) : [];
  const temas = Object.entries(cfg.temas ?? {}).map(([id, t]) => ({ id, ...t, archivo: p(t.archivo) }));
  return { dir, cfg, p, archivosTokens, temas, id: cfg.cliente.id, prefijo: cfg.cliente.prefijo ?? cfg.cliente.id };
}

export function nombreVar(ruta, cfg) {
  const omitir = new Set(cfg.nombres?.omitir ?? []);
  return [cfg.cliente.prefijo ?? cfg.cliente.id, ...ruta.filter((s) => !omitir.has(s))].join('-');
}

export function escribir(ruta, contenido) {
  mkdirSync(dirname(ruta), { recursive: true });
  writeFileSync(ruta, typeof contenido === 'string' ? contenido : JSON.stringify(contenido, null, 2) + '\n');
}

export function salir(msg, codigo = 1) {
  console.error(msg);
  process.exit(codigo);
}
