// Fase 4 · Compuerta de tokens. Valida contra DTCG 2025.10 cada tema (primitivos + su capa semántica).
// Sale con 1 si hay errores. Los avisos (formatos legados, CSS crudo) no bloquean pero se listan.
import { cliente } from './lib/cliente.mjs';
import { cargar, aplanar, validar } from './lib/dtcg.mjs';

const c = cliente(process.argv[2]);
const verbose = process.argv.includes('--todo');
const conjuntos = c.temas.length ? c.temas.map((t) => ({ id: t.id, archivos: [...c.archivosTokens(), t.archivo] })) : [{ id: 'base', archivos: c.archivosTokens() }];
let errores = 0;
for (const { id, archivos } of conjuntos) {
  const mapa = aplanar(cargar(archivos));
  const r = validar(mapa, { capasSinLiterales: c.cfg.capasSemanticas ?? [] });
  errores += r.errores.length;
  console.log(`validar · ${id.padEnd(7)} ${mapa.size} tokens · ${r.errores.length} errores · ${r.avisos.length} avisos`);
  for (const e of r.errores) console.log('  ERROR ' + e);
  const avisos = verbose ? r.avisos : r.avisos.slice(0, 5);
  for (const a of avisos) console.log('  aviso ' + a);
  if (!verbose && r.avisos.length > 5) console.log(`  … ${r.avisos.length - 5} avisos más (--todo para verlos)`);
}
process.exit(errores ? 1 : 0);
