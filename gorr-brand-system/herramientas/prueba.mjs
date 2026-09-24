// Prueba de humo: instancia plantilla/ en un directorio temporal y corre la cadena completa.
// Si la plantilla no pasa sus propias compuertas, ningún cliente nuevo arranca limpio.
import { cpSync, mkdtempSync, readdirSync, readFileSync, writeFileSync, statSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { RAIZ } from './lib/cliente.mjs';

const dir = join(mkdtempSync(join(tmpdir(), 'gorr-')), 'demo');
cpSync(join(RAIZ, 'plantilla'), dir, { recursive: true });
const rep = (d) => { for (const f of readdirSync(d)) { const r = join(d, f); if (statSync(r).isDirectory()) rep(r); else if (/\.(json|md)$/.test(f)) writeFileSync(r, readFileSync(r, 'utf8').replaceAll('{{id}}', 'demo').replaceAll('{{nombre}}', 'Demo')); } };
rep(dir);
const r = spawnSync(process.execPath, [join(RAIZ, 'herramientas', 'ciclo.mjs'), dir], { stdio: 'inherit' });
if (process.argv.includes('--conservar')) console.log(`\nconservado en ${dir}`); else rmSync(dir, { recursive: true, force: true });
process.exit(r.status);
