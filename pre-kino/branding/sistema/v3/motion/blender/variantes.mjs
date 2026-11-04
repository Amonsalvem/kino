// Variantes por estado del GLB del Pase (KHR_materials_variants) y compresión Draco.
// Entrada: glb/pase-3d-objeto.base.glb y glb/pase-3d-objeto.estados.json (los escribe exportar.py desde Blender).
// Salida:  glb/pase-3d-objeto.glb (Draco) y glb/pase-3d-objeto.clips.json (lo que el visor necesita para los clips).
//
// Cada pieza tiene un material por estado con el color de su token ya horneado y su opacidad en ese estado:
// - marcas (bordes, chip, textos, barra, corte): KHR_materials_unlit, salen con el hex exacto;
// - tarjeta: PBR con KHR_materials_clearcoat y KHR_materials_sheen (la membrana);
// - resplandor: textura del token resplandor/vigente, visible solo en «vigente».
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS, KHRMaterialsClearcoat, KHRMaterialsSheen, KHRMaterialsUnlit, KHRMaterialsVariants} from '@gltf-transform/extensions';
import {draco, prune} from '@gltf-transform/functions';
import draco3d from 'draco3dgltf';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const GLB = path.join(AQUI, 'glb');
const datos = JSON.parse(fs.readFileSync(path.join(GLB, 'pase-3d-objeto.estados.json'), 'utf8'));
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
	'draco3d.encoder': await draco3d.createEncoderModule(),
	'draco3d.decoder': await draco3d.createDecoderModule(),
});
const doc = await io.read(path.join(GLB, 'pase-3d-objeto.base.glb'));
const raiz = doc.getRoot();

const lineal = (hex) => {
	const c = (i) => {
		const v = parseInt(hex.slice(i, i + 2), 16) / 255;
		return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
	};
	return [c(1), c(3), c(5)];
};

const extVariantes = doc.createExtension(KHRMaterialsVariants);
const unlit = doc.createExtension(KHRMaterialsUnlit);
const laca = doc.createExtension(KHRMaterialsClearcoat);
const sheen = doc.createExtension(KHRMaterialsSheen);
const estados = Object.keys(datos.estados);
const variantes = Object.fromEntries(estados.map((e) => [e, extVariantes.createVariant(e)]));
const halo = doc.createTexture('resplandor').setImage(fs.readFileSync(path.join(GLB, 'resplandor.png'))).setMimeType('image/png');

let piezas = 0;
for (const nodo of raiz.listNodes()) {
	const nombre = nodo.getName();
	const malla = nodo.getMesh();
	if (!malla || !datos.estados.vigente[nombre]) continue;
	piezas++;
	const lista = extVariantes.createMappingList();
	let porDefecto = null;
	for (const e of estados) {
		const p = datos.estados[e][nombre];
		const m = doc.createMaterial(`${nombre}·${e}`).setBaseColorFactor([...lineal(p.hex), p.alfa]).setAlphaMode('BLEND').setDoubleSided(true);
		m.setExtras({kino_token: p.token, kino_estado: e});
		if (nombre === 'tarjeta') {
			const t = datos.pbr_tarjeta;
			m.setRoughnessFactor(t.rugosidad).setMetallicFactor(0).setAlphaMode(p.alfa < 1 ? 'BLEND' : 'OPAQUE').setDoubleSided(false);
			m.setExtension('KHR_materials_clearcoat', laca.createClearcoat().setClearcoatFactor(t.laca).setClearcoatRoughnessFactor(t.laca_rugosidad));
			m.setExtension('KHR_materials_sheen', sheen.createSheen().setSheenColorFactor(lineal(t.sheen_hex)).setSheenRoughnessFactor(t.sheen_rugosidad));
		} else {
			m.setExtension('KHR_materials_unlit', unlit.createUnlit());
			if (nombre === 'resplandor') m.setBaseColorTexture(halo).setBaseColorFactor([1, 1, 1, p.alfa]);
		}
		lista.addMapping(extVariantes.createMapping().setMaterial(m).addVariant(variantes[e]));
		if (e === 'vigente') porDefecto = m;
	}
	for (const prim of malla.listPrimitives()) {
		prim.setMaterial(porDefecto);
		prim.setExtension('KHR_materials_variants', lista);
	}
}
await doc.transform(prune({propertyTypes: ['MATERIAL', 'TEXTURE', 'ACCESSOR']}), draco({method: 'edgebreaker'}));
await io.write(path.join(GLB, 'pase-3d-objeto.glb'), doc);
const clips = {fps: datos.fps, clips: datos.clips, tokens_motion: datos.tokens_motion, estados, variantes: 'KHR_materials_variants'};
fs.writeFileSync(path.join(GLB, 'pase-3d-objeto.clips.json'), JSON.stringify(clips, null, 1) + '\n');
const kb = (fs.statSync(path.join(GLB, 'pase-3d-objeto.glb')).size / 1024).toFixed(0);
console.log(`✓ pase-3d-objeto.glb · ${piezas} piezas × ${estados.length} variantes · Draco · ${kb} KB`);
