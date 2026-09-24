// Crea un cliente nuevo desde plantilla/.   npm run nuevo -- <id> "<Nombre>"
import { cpSync, existsSync, readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { RAIZ, salir } from './lib/cliente.mjs';

const [, , id, nombre = id] = process.argv;
if (!id || !/^[a-z0-9-]+$/.test(id)) salir('Uso: npm run nuevo -- <id-en-minusculas> "<Nombre>"');
const destino = join(RAIZ, 'clientes', id);
if (existsSync(destino)) salir(`Ya existe clientes/${id}`);
cpSync(join(RAIZ, 'plantilla'), destino, { recursive: true });
const reemplazar = (d) => {
  for (const f of readdirSync(d)) {
    const r = join(d, f);
    if (statSync(r).isDirectory()) reemplazar(r);
    else if (/\.(json|md)$/.test(f)) writeFileSync(r, readFileSync(r, 'utf8').replaceAll('{{id}}', id).replaceAll('{{nombre}}', nombre));
  }
};
reemplazar(destino);
console.log(`clientes/${id} creado. Siguiente: llenar 00-brief.md y seguir PLAYBOOK.md desde la fase 0.`);
