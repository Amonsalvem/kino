// Kino — construye la capa de tokens con Style Dictionary 5.
// Un build por tema: Style Dictionary no acepta `source` por plataforma, y los dos
// temas declaran los mismos nombres de token, así que no pueden compartir diccionario.
import StyleDictionary from 'style-dictionary';

const NO_NOMBRE = new Set(['primitivo', 'semantico', 'color', 'medida', 'tipo']);

StyleDictionary.registerTransform({
  name: 'kino/nombre',
  type: 'name',
  transform: (token) =>
    ['kino', ...token.path.filter((p) => !NO_NOMBRE.has(p))].join('-'),
});

const transforms = ['kino/nombre', 'color/css'];
const capa = (n) => (token) => token.path[0] === n;

const construir = async ({ source, destination, selector, filter, outputReferences }) => {
  const sd = new StyleDictionary({
    source,
    log: { verbosity: 'silent' },
    platforms: {
      css: {
        transforms,
        buildPath: 'build/',
        files: [{ destination, format: 'css/variables',
                  options: { selector, outputReferences }, filter }],
      },
    },
  });
  await sd.buildAllPlatforms();
  console.log(`  build/${destination}`);
};

await construir({
  source: ['tokens/primitivo.json'],
  destination: 'primitivos.css',
  selector: ':root',
  filter: capa('primitivo'),
  outputReferences: false,
});

for (const [id, selector] of [
  ['oscuro', ':root, :root[data-tema="oscuro"]'],
  ['claro', ':root[data-tema="claro"]'],
]) {
  await construir({
    source: ['tokens/primitivo.json', `tokens/tema/${id}.json`],
    destination: `tema-${id}.css`,
    selector,
    filter: capa('semantico'),
    outputReferences: true,
  });
}
