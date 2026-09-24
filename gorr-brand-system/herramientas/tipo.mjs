// Fase 3 · Tipografía y espacio. Escala fluida con el método Utopia (utopia.fyi, Clearleft):
// dos escalas modulares —una en el viewport mínimo y otra en el máximo— interpoladas con clamp().
// El token guarda el valor mínimo como dimensión DTCG válida (fallback portable) y la interpolación
// en $extensions["com.gorr.fluido"], que construir.mjs convierte en clamp().
import { cliente, escribir } from './lib/cliente.mjs';
import { EXT, clampFluido } from './lib/dtcg.mjs';

const c = cliente(process.argv[2]);
const t = c.cfg.tipo;
if (!t) { console.log('marca.config.json sin sección "tipo": nada que generar.'); process.exit(0); }
const raiz = t.raiz ?? 16, dec = t.decimales ?? 4, neg = c.cfg.nombres?.negativo ?? 'n';
const rem = (px) => ({ value: +(px / raiz).toFixed(4), unit: 'rem' });
const fluido = (minPx, maxPx) => ({ min: rem(minPx), max: rem(maxPx), vwMin: t.vwMin, vwMax: t.vwMax, raiz, decimales: dec });

const texto = { $type: 'dimension', $description: `Utopia · ${t.min.base}px×${t.min.escala} @${t.vwMin}px → ${t.max.base}px×${t.max.escala} @${t.vwMax}px` };
const tabla = [];
for (const s of t.pasos) {
  const minPx = t.min.base * t.min.escala ** s, maxPx = t.max.base * t.max.escala ** s;
  const f = fluido(minPx, maxPx);
  texto[s < 0 ? `${neg}${-s}` : String(s)] = { $value: rem(minPx), $extensions: { [EXT.FLUIDO]: f } };
  tabla.push({ paso: s, minPx: +minPx.toFixed(2), maxPx: +maxPx.toFixed(2), clamp: clampFluido(f) });
}
const salida = { primitivo: { tipo: { texto } } };

// Espacio fluido de Utopia: múltiplos del paso 0, más pares "uno arriba" (s-m, m-l…) para saltos intencionales.
if (t.espacio) {
  const mult = t.espacio.multiplicadores ?? { '3xs': 0.25, '2xs': 0.5, xs: 0.75, s: 1, m: 1.5, l: 2, xl: 3, '2xl': 4, '3xl': 6 };
  const esp = { $type: 'dimension', $description: 'Utopia · espacio fluido' };
  const nombres = Object.keys(mult);
  nombres.forEach((k, i) => {
    esp[k] = { $value: rem(t.min.base * mult[k]), $extensions: { [EXT.FLUIDO]: fluido(t.min.base * mult[k], t.max.base * mult[k]) } };
    const sig = nombres[i + 1];
    if (sig && t.espacio.pares !== false)
      esp[`${k}-${sig}`] = { $value: rem(t.min.base * mult[k]), $extensions: { [EXT.FLUIDO]: fluido(t.min.base * mult[k], t.max.base * mult[sig]) } };
  });
  salida.primitivo.medida = { espacio: esp };
}
if (t.familias) {
  salida.primitivo.tipo.fuente = { $type: 'fontFamily' };
  for (const [k, v] of Object.entries(t.familias)) salida.primitivo.tipo.fuente[k] = { $value: v };
}

escribir(c.p('tokens', '20-primitivo-tipo.tokens.json'), salida);
escribir(c.p('reportes', 'tipo.json'), tabla);
console.log(`tipo · ${tabla.length} pasos${t.espacio ? ' + espacio fluido' : ''}`);
for (const r of tabla) console.log(`  ${String(r.paso).padStart(2)}  ${String(r.minPx).padStart(6)}→${String(r.maxPx).padEnd(6)} ${r.clamp}`);
