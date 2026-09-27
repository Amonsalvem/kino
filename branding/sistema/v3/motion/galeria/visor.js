// Visor del Pase 3D (pase-3d-objeto.glb, Draco) con three.js. Versión 2.
// El GLB trae las transformaciones (subida, escala de entrada, asentamiento, barra, corte, tachado, nota) y, por cada
// pieza, un material por estado (KHR_materials_variants) con el color del token y la opacidad ya horneados.
// El visor solo interpola entre el material del estado inicial y el del final con la curva del clip (clips.json).
// Lo único que reconstruye es el latido (curva/latir), que no es un estado.
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

const D = JSON.parse(document.getElementById('visor-datos').textContent);
const lienzo = document.getElementById('visor-lienzo');
const estadoTxt = document.getElementById('visor-estado');
const botones = [...document.querySelectorAll('[data-clip]')];

const B = (u, a, b) => 3 * (1 - u) ** 2 * u * a + 3 * (1 - u) * u * u * b + u ** 3;
const bezier = ([x1, y1, x2, y2]) => (t) => {
  if (t <= 0) return 0;
  if (t >= 1) return 1;
  let lo = 0, hi = 1, u = t;
  for (let i = 0; i < 32; i++) { u = (lo + hi) / 2; if (B(u, x1, x2) < t) lo = u; else hi = u; }
  return B(u, y1, y2);
};
const curvaLatir = bezier(D.tokens_motion.curva.latir);
const tri = (p) => { const u = curvaLatir(p); return u < 0.5 ? 2 * u : 2 - 2 * u; };

// Escena: sin tone mapping, así las marcas unlit salen con el hex exacto de su token.
const renderer = new THREE.WebGLRenderer({canvas: lienzo, antialias: true, alpha: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.toneMapping = THREE.NoToneMapping;
renderer.outputColorSpace = THREE.SRGBColorSpace;
const escena = new THREE.Scene();
const camara = new THREE.PerspectiveCamera(22, 16 / 9, 0.1, 100);
const dist = 13.5, ang = THREE.MathUtils.degToRad(17);
camara.position.set(dist * Math.sin(ang), 1.1, dist * Math.cos(ang));
const controles = new OrbitControls(camara, lienzo);
controles.enableZoom = false;
controles.enablePan = false;
controles.minPolarAngle = Math.PI * 0.3;
controles.maxPolarAngle = Math.PI * 0.62;
controles.minAzimuthAngle = -0.9;
controles.maxAzimuthAngle = 0.9;
// Luz por capas como en Blender: clave arriba a la izquierda, contraluz que marca el borde superior, relleno frío.
escena.add(new THREE.HemisphereLight(0xffffff, 0x000000, 0.6));
const clave = new THREE.DirectionalLight(0xffffff, 2.4); clave.position.set(-5.5, 6, 7.5); escena.add(clave);
const contra = new THREE.DirectionalLight(0xffffff, 1.6); contra.position.set(0, 3, -2.2); escena.add(contra);

// Piezas: plantilla de cada estado (color, opacidad) leída de las variantes del GLB.
const piezas = [];
const FAMILIAS_TEXTO = ['chip', 'dato', 'nota'];
const LINEAS = ['barra', 'corte', 'tachado'];
let mezclador, acciones = [], raizModelo = null;
const draco = new DRACOLoader().setDecoderPath('galeria/draco/');
const cargador = new GLTFLoader().setDRACOLoader(draco);
const bin = Uint8Array.from(atob(D.glb), (c) => c.charCodeAt(0)).buffer;
cargador.parse(bin, '', async (gltf) => {
  raizModelo = gltf.scene;
  escena.add(gltf.scene);
  // three r169 no aplica KHR_materials_variants: deja la extensión cruda en userData.gltfExtensions (raíz y malla).
  const nombres = ((gltf.userData.gltfExtensions || {}).KHR_materials_variants || {variants: []}).variants.map((v) => v.name);
  const mallas = [];
  gltf.scene.traverse((o) => { if (o.isMesh && o.userData.gltfExtensions && o.userData.gltfExtensions.KHR_materials_variants) mallas.push(o); });
  for (const o of mallas) {
    const pieza = pieza_de(o);
    const {mappings} = o.userData.gltfExtensions.KHR_materials_variants;
    const plantilla = {};
    let vivo = null;
    for (const [i, e] of nombres.entries()) {
      const ref = mappings.find((m) => m.variants.includes(i));
      if (!ref) continue;
      const m = await gltf.parser.getDependency('material', ref.material);
      plantilla[e] = {color: m.color.clone(), opacidad: m.opacity};
      if (!vivo) vivo = m.clone();
    }
    vivo.transparent = true;
    vivo.depthWrite = pieza === 'tarjeta';
    o.material = vivo;
    // Capas como en Blender (cada marca va un poco más adelante): resplandor, tarjeta, fondos, marcas, brillo.
    o.renderOrder = pieza === 'resplandor' ? -1 : pieza === 'tarjeta' ? 0 : (pieza === 'pista' || pieza.endsWith('-fondo')) ? 1 : pieza === 'brillo' ? 3 : 2;
    piezas.push({o, pieza, plantilla, familia: pieza.split('-')[0]});
  }
  mezclador = new THREE.AnimationMixer(gltf.scene);
  acciones = gltf.animations.map((a) => { const x = mezclador.clipAction(a); x.play(); x.paused = true; return x; });
  lienzo.dataset.listo = '1';
  lienzo.dataset.variantes = String(nombres.length);
  iniciar();
}, (err) => { estadoTxt.textContent = 'No se pudo cargar el modelo: ' + err.message; });

function pieza_de(o) {
  // three nombra las primitivas «nombre_1»…; el nombre de la pieza es el del nodo de Blender.
  let n = o;
  while (n && !(n.name in D_PIEZAS)) n = n.parent;
  return n ? n.name : o.name;
}
const D_PIEZAS = new Proxy({}, {has: (_, k) => typeof k === 'string' && /^(tarjeta|resplandor|borde|borde-sin|brillo|quien|tachado|pista|barra|corte|chip-[a-z-]+-(fondo|borde|punto|texto)|dato-[a-z-]+|nota-[a-z]+)$/.test(k)});

const reducido = () => document.documentElement.dataset.reducido === '1';
const tiempo = (frame) => frame / D.fps;
function pose(frame) {
  for (const x of acciones) x.time = Math.min(tiempo(frame), x.getClip().duration);
  mezclador.update(0);
}

function aplicar(nombre, p) {
  const c = D.clips[nombre];
  const e = bezier(c.curva)(p);
  const red = reducido();
  const ini = c.estado_inicial, fin = c.estado_final;
  // Transformaciones del GLB. Reducido: pose final sin desplazamiento; la barra que se vaciaría conserva su largo y
  // funde, y las líneas que se dibujarían aparecen por fundido (misma duración y curva).
  const funde = new Set();
  if (red) {
    pose(c.desde);
    const antes = Object.fromEntries(piezas.filter((x) => LINEAS.includes(x.pieza)).map((x) => [x.pieza, x.o.scale.x]));
    pose(c.hasta);
    for (const x of piezas) {
      if (!LINEAS.includes(x.pieza) || nombre === 'aparecer') continue;
      if (x.o.scale.x < 1e-4 && antes[x.pieza] > 1e-4) { x.o.scale.x = antes[x.pieza]; funde.add(x.pieza); }
    }
  } else {
    pose(c.desde + p * (c.hasta - c.desde));
  }
  // ¿En qué familias de texto sale uno y entra otro? Esas se funden a través (mitad y mitad), como en Blender.
  const cruza = {};
  for (const f of FAMILIAS_TEXTO) {
    const fam = piezas.filter((x) => x.familia === f && x.plantilla[ini] && x.plantilla[fin]);
    cruza[f] = fam.some((x) => x.plantilla[ini].opacidad > x.plantilla[fin].opacidad) && fam.some((x) => x.plantilla[fin].opacidad > x.plantilla[ini].opacidad);
  }
  for (const x of piezas) {
    const A = x.plantilla[ini], Bm = x.plantilla[fin];
    if (!A || !Bm) continue;
    let t = e;
    if (cruza[x.familia]) {
      const salir = Bm.opacidad < A.opacidad;
      t = salir ? bezier(c.curva)(Math.min(p * 2, 1)) : bezier(c.curva)(Math.max(p * 2 - 1, 0));
    }
    let op = A.opacidad + (Bm.opacidad - A.opacidad) * t;
    if (nombre === 'aparecer') op *= e;
    if (x.pieza === 'brillo') op = nombre === 'latir' && !red ? tri(p) : 0;
    if (x.pieza === 'resplandor' && nombre === 'latir' && !red) op *= 1 + 0.18 * tri(p);
    if (funde.has(x.pieza)) op *= 1 - e;
    x.o.material.color.copy(A.color).lerp(Bm.color, t);
    x.o.material.opacity = Math.min(op, 1);
    x.o.visible = op > 0.002;
  }
  estadoTxt.textContent = `${nombre} · ${ini === fin ? ini : ini + ' → ' + fin}${c.deja ? ' · deja: ' + c.deja : ''}`;
}

// Reproducción: un clip o la secuencia; la pausa entre clips es un ciclo de latir.
const SECUENCIA = ['aparecer', 'confirmar', 'latir', 'avisar', 'caducar'];
let enBucle = true, cola = [], actual = null, inicio = 0, pausaHasta = 0, visible = true;
const duracionMs = (n) => (D.clips[n].hasta - D.clips[n].desde) / D.fps * 1000;
const pausaMs = () => D.tokens_motion.latir / D.fps * 1000;

function reproducir(lista) { cola = [...lista]; siguiente(performance.now()); }
function siguiente(ahora) {
  actual = cola.shift() || null;
  inicio = ahora;
  botones.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.clip === actual)));
}
function cuadro(ahora) {
  requestAnimationFrame(cuadro);
  if (!mezclador || !visible) return;
  if (actual) {
    const p = Math.min((ahora - inicio) / duracionMs(actual), 1);
    aplicar(actual, p);
    lienzo.dataset.clip = actual;
    if (p >= 1) {
      const fin = actual;
      actual = null;
      pausaHasta = ahora + pausaMs();
      if (!cola.length && enBucle) cola = [...SECUENCIA];
      botones.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.clip === fin)));
    }
  } else if (cola.length && ahora >= pausaHasta) {
    siguiente(ahora);
  }
  controles.update();
  renderer.render(escena, camara);
}
function iniciar() {
  aplicar('aparecer', 0);
  reproducir(SECUENCIA);
  requestAnimationFrame(cuadro);
}
botones.forEach((b) => b.addEventListener('click', () => {
  enBucle = b.dataset.clip === 'secuencia';
  reproducir(enBucle ? SECUENCIA : [b.dataset.clip]);
}));
// Para pruebas: fija un clip en un avance dado y dibuja (window.kinoVisor.fijar('confirmar', 1)).
window.kinoVisor = {fijar(n, p) { cola = []; actual = null; aplicar(n, p); renderer.render(escena, camara); }, piezas: () => piezas.length};

function ajustar() {
  const w = lienzo.clientWidth, h = lienzo.clientHeight;
  renderer.setSize(w, h, false);
  camara.aspect = w / h;
  camara.updateProjectionMatrix();
}
new ResizeObserver(ajustar).observe(lienzo);
new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(lienzo);
ajustar();
