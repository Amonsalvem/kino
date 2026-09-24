// ============================================================================
// Arnés de verificación, NO el build oficial.
//
// `build.mjs` usa esbuild y es el que manda. Este script existe solo para poder
// construir y comprobar el runtime en un entorno sin red, donde esbuild no se
// puede instalar: resuelve los imports relativos a mano, concatena en orden
// topológico, deja que `tsc` quite los tipos y envuelve en un IIFE.
//
// Si los dos difieren, gana build.mjs. Ejecuta `npm run build` antes de publicar.
//
//   node build-sin-red.mjs [salida.html]
// ============================================================================
import { readFile, writeFile, mkdtemp, rm } from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve, basename } from "node:path";
import { tmpdir } from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(__dirname, "src");
const ENTRY = "main.ts";
const CSS_MARK = "/*__CSS__*/";
const ENGINE_MARK = "/*__ENGINE__*/";

const leer = (f) => readFile(resolve(SRC, f), "utf8");

/** Módulos de los que depende un archivo, en orden de aparición. */
function deps(codigo) {
  const out = [];
  const re = /^\s*import\s+(?:type\s+)?[^"']*from\s+["']\.\/([\w.-]+)\.js["'];?\s*$/gm;
  let m;
  while ((m = re.exec(codigo))) out.push(`${m[1]}.ts`);
  return out;
}

/** Orden topológico por profundidad: las hojas primero. */
async function orden(entrada) {
  const visto = new Set();
  const salida = [];
  async function visita(f) {
    if (visto.has(f)) return;
    visto.add(f);
    const codigo = await leer(f);
    for (const d of deps(codigo)) await visita(d);
    salida.push(f);
  }
  await visita(entrada);
  return salida;
}

/**
 * Quita import/export dejando las declaraciones, que al concatenar quedan en un
 * solo ámbito. Las llaves pueden abarcar varias líneas (`core.ts` reexporta así),
 * de modo que esos bloques se tratan con `[\s\S]` y no línea por línea.
 */
function aplana(codigo) {
  return codigo
    // import / export con llaves, en una o varias líneas, y reexports
    .replace(/^[ \t]*(?:import|export)\s+type\s*\{[\s\S]*?\}\s*from\s*["'][^"']+["'];?[ \t]*$/gm, "")
    .replace(/^[ \t]*(?:import|export)\s*\{[\s\S]*?\}\s*from\s*["'][^"']+["'];?[ \t]*$/gm, "")
    .replace(/^[ \t]*export\s*\{[\s\S]*?\};?[ \t]*$/gm, "")
    // import por defecto o namespace
    .replace(/^[ \t]*import\s+[^;{]*from\s*["'][^"']+["'];?[ \t]*$/gm, "")
    // lo que queda: `export const`, `export function`, `export type X = {`...
    .replace(/^([ \t]*)export\s+(default\s+)?/gm, "$1");
}

async function main() {
  const archivos = await orden(ENTRY);
  const fuente = (await Promise.all(archivos.map(async (f) => `// ---- ${basename(f)} ----\n${aplana(await leer(f))}`))).join("\n");

  const dir = await mkdtemp(resolve(tmpdir(), "kino-build-"));
  const ts = resolve(dir, "bundle.ts");
  await writeFile(ts, fuente);
  // cwd = el temporal: si no, tsc encuentra el tsconfig.json del motor y se niega (TS5112).
  execFileSync("tsc", ["bundle.ts", "--target", "ES2019", "--module", "none", "--ignoreDeprecations", "6.0", "--skipLibCheck", "--removeComments", "--lib", "ES2020,DOM,DOM.Iterable"], { stdio: "pipe", cwd: dir });
  const js = await readFile(resolve(dir, "bundle.js"), "utf8");
  await rm(dir, { recursive: true, force: true });

  const [tpl, cssBase, cssKino] = await Promise.all([
    readFile(resolve(__dirname, "template.src.html"), "utf8"),
    readFile(resolve(SRC, "styles.css"), "utf8"),
    readFile(resolve(SRC, "styles-kino.css"), "utf8"),
  ]);
  if (!tpl.includes(CSS_MARK) || !tpl.includes(ENGINE_MARK)) throw new Error("faltan los marcadores en template.src.html");

  const html = tpl
    .replace(CSS_MARK, () => `${cssBase}\n${cssKino}`)
    .replace(ENGINE_MARK, () => `"use strict";(()=>{\n${js}\n})();`);

  const salida = resolve(process.argv[2] || resolve(__dirname, "../skills/research-deck/assets/deck-template.html"));
  await writeFile(salida, html);
  console.log(`${archivos.length} módulos · ${(html.length / 1024).toFixed(0)} KB → ${salida}`);
}

main().catch((e) => {
  console.error(String(e.stdout || e.message || e).slice(0, 2000));
  process.exit(1);
});
