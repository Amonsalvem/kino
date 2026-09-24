// Generado. Reutiliza herramientas/voz.mjs como aserción de promptfoo.
const path = require('node:path');
const { readFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
module.exports = async (salida) => {
  const { reglas, revisar } = await import(pathToFileURL(path.join(__dirname, "../../../herramientas/voz.mjs")).href);
  const voz = JSON.parse(readFileSync(path.join(__dirname, '..', 'voz.json'), 'utf8'));
  const errores = revisar(String(salida), reglas(voz)).filter((h) => h.gravedad === 'error');
  return { pass: errores.length === 0, score: errores.length ? 0 : 1,
    reason: errores.length ? errores.map((e) => `[${e.id}] «${e.fragmento}»`).join('; ') : 'sin errores de voz' };
};
