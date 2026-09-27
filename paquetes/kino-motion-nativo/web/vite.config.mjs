import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

// Reanimated carga su puente con react-native-web con require() dentro de try/catch; en los módulos de Vite
// require no existe y el puente queda indefinido. Metro y Expo no tienen este problema: solo es del arnés.
const puenteReanimatedWeb = {
	name: 'puente-reanimated-web',
	enforce: 'pre',
	transform(codigo, id) {
		if (!id.includes('react-native-reanimated') || !/js-reanimated[\\/]webUtils\.web\.js$/.test(id)) return null;
		return `import _crear from 'react-native-web/dist/exports/StyleSheet/compiler/createReactDOMStyle';
import {createTransformValue as _t, createTextShadowValue as _s} from 'react-native-web/dist/exports/StyleSheet/preprocess';
export let createReactDOMStyle = _crear;
export let createTransformValue = _t;
export let createTextShadowValue = _s;`;
	},
};

export default defineConfig({
	root: new URL('.', import.meta.url).pathname,
	base: './',
	plugins: [puenteReanimatedWeb, react({babel: {plugins: ['react-native-reanimated/plugin']}})],
	resolve: {
		alias: {'react-native': 'react-native-web'},
		extensions: ['.web.tsx', '.web.ts', '.web.js', '.tsx', '.ts', '.js'],
	},
	define: {__DEV__: 'true', global: 'globalThis', 'process.env.NODE_ENV': '"development"', 'process.env.JEST_WORKER_ID': 'undefined'},
	optimizeDeps: {exclude: ['react-native-reanimated'], esbuildOptions: {resolveExtensions: ['.web.js', '.js', '.ts', '.tsx'], loader: {'.js': 'jsx'}}},
	build: {outDir: 'dist', emptyOutDir: true, minify: false, sourcemap: true},
});
