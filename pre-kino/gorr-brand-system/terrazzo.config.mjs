// Salida multiplataforma con Terrazzo (terrazzo.app), la herramienta de referencia de DTCG 2025.10.
// NO VERIFICADO: al crear el sistema (22 sep 2026) no había acceso al registro de npm. Antes de usarlo:
//   npm i -D @terrazzo/cli @terrazzo/plugin-css   y revisar la API contra la documentación vigente.
// Uso previsto: CLIENTE=kino npx tz build
// El emisor propio (herramientas/construir.mjs) sigue siendo la salida CSS por defecto; Terrazzo entra
// cuando un cliente necesita Swift, Kotlin, Tailwind u otros formatos. Las extensiones com.gorr.fluido
// y com.gorr.css-crudo no las entiende Terrazzo: el token cae a su $value (el mínimo), que es válido.
import { defineConfig } from '@terrazzo/cli';
import css from '@terrazzo/plugin-css';
import { readdirSync } from 'node:fs';

const cliente = process.env.CLIENTE ?? 'kino';
const dir = `./clientes/${cliente}/tokens`;
const tokens = readdirSync(dir).filter((f) => f.endsWith('.tokens.json')).map((f) => `${dir}/${f}`);

export default defineConfig({
  tokens: [...tokens, `${dir}/tema/oscuro.tokens.json`],
  outDir: `./clientes/${cliente}/build/terrazzo/`,
  plugins: [css({ filename: 'tokens.css' })],
});
