// Visor del Pase 3D (pase-3d-objeto.glb, Draco) con three.js.
// El GLB trae las transformaciones (subida del root, escala de barra y corte). glTF no anima materiales, así que
// los fundidos y colores de cada estado se aplican aquí con los datos de clips.json y las curvas de los tokens.
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
const curva = (nombre) => bezier(D.curvas[(D.verbos[nombre] || nombre).split('/')[1]]);
const color = (token) => new THREE.Color(D.tokens[token]);

// Escena
const renderer = new THREE.WebGLRenderer({canvas: lienzo, antialias: true, alpha: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const escena = new THREE.Scene();
const camara = new THREE.PerspectiveCamera(28, 16 / 9, 0.1, 100);
const dist = 7.2, ang = THREE.MathUtils.degToRad(14);
camara.position.set(dist * Math.sin(ang), 0.9, dist * Math.cos(ang));
const controles = new OrbitControls(camara, lienzo);
controles.enableZoom = false;
controles.enablePan = false;
controles.minPolarAngle = Math.PI * 0.3;
controles.maxPolarAngle = Math.PI * 0.62;
controles.minAzimuthAngle = -0.9;
controles.maxAzimuthAngle = 0.9;
escena.add(new THREE.HemisphereLight(color('texto/primario'), color('superficie/abismo'), 1.4));
const clave = new THREE.DirectionalLight(color('texto/primario'), 2.2);
clave.position.set(-2.5, 4, 4);
escena.add(clave);

// Piezas y materiales por token
const piezas = {};
let mezclador, acciones = [];
const draco = new DRACOLoader().setDecoderPath('galeria/draco/');
const cargador = new GLTFLoader().setDRACOLoader(draco);
const bin = Uint8Array.from(atob(D.glb), (c) => c.charCodeAt(0)).buffer;
cargador.parse(bin, '', (gltf) => {
  escena.add(gltf.scene);
  gltf.scene.traverse((o) => {
    if (!o.isMesh) return;
    const nombre = D.token_pieza[o.name] ? o.name : o.parent && o.parent.name;
    if (!D.token_pieza[nombre]) return;
    o.material = nombre === 'tarjeta'
      ? new THREE.MeshStandardMaterial({color: color(D.token_pieza[nombre]), roughness: 0.35, transparent: true})
      : new THREE.MeshBasicMaterial({color: color(D.token_pieza[nombre]), transparent: true, depthWrite: false, side: THREE.DoubleSide});
    // Las marcas planas vienen con la cara hacia atrás desde Blender (allí se dibujan igual): doble cara.
    o.renderOrder = nombre === 'tarjeta' ? 0 : 1;
    piezas[nombre] = o;
  });
  mezclador = new THREE.AnimationMixer(gltf.scene);
  acciones = gltf.animations.map((a) => { const x = mezclador.clipAction(a); x.play(); x.paused = true; return x; });
  lienzo.dataset.listo = '1';
  iniciar();
}, (err) => { estadoTxt.textContent = 'No se pudo cargar el modelo: ' + err.message; });

const reducido = () => document.documentElement.dataset.reducido === '1';
const visibles = (estado) => new Set(D.piezas_por_estado[estado]);
const colorDe = (estado, pieza) => (D.color_por_estado[estado] || {})[pieza] || D.token_pieza[pieza];
const tiempo = (frame) => frame / D.fps;

function aplicar(nombre, p) {
  const c = D.clips[nombre];
  const e = curva(c.curva)(p);
  const red = reducido();
  // Transformaciones del GLB. Reducido: sin desplazamiento ni escala (se quedan en su estado de reposo).
  let frame = c.desde + p * (c.hasta - c.desde);
  if (red) frame = nombre === 'aparecer' ? c.hasta : c.desde;
  // setTime() reinicia las acciones a 0 y, en pausa, no avanzan: se fija el tiempo de cada una y se evalúa.
  for (const x of acciones) x.time = Math.min(tiempo(frame), x.getClip().duration);
  mezclador.update(0);
  const A = visibles(c.estado_inicial), Bv = visibles(c.estado_final);
  for (const [n, o] of Object.entries(piezas)) {
    let op = (A.has(n) ? 1 : 0) + ((Bv.has(n) ? 1 : 0) - (A.has(n) ? 1 : 0)) * e;
    if (n === 'brillo') op = nombre === 'latir' && !red ? (p < 0.5 ? curva('latir/curva')(p * 2) : curva('latir/curva')((1 - p) * 2)) : 0;
    if (n === 'corte') op = nombre === 'revocar' && !red ? 1 : 0;
    if (n === 'barra' && nombre === 'caducar' && red) op = 1 - e;
    if (nombre === 'aparecer') op *= e;
    o.material.opacity = op;
    o.visible = op > 0.001;
    const ca = color(colorDe(c.estado_inicial, n)), cb = color(colorDe(c.estado_final, n));
    o.material.color.copy(ca).lerp(cb, e);
  }
  estadoTxt.textContent = `${nombre} · ${c.estado_inicial === c.estado_final ? c.estado_inicial : c.estado_inicial + ' → ' + c.estado_final} · ${c.duracion}, ${c.curva}`;
}

// Reproducción: un clip o la secuencia; la pausa entre clips es un ciclo de latir (convención del borrador).
const SECUENCIA = ['aparecer', 'confirmar', 'latir', 'caducar'];
let enBucle = true, cola = [], actual = null, inicio = 0, pausaHasta = 0, visible = true;
const duracionMs = (n) => (D.clips[n].hasta - D.clips[n].desde) / D.fps * 1000;
const pausaMs = () => D.duracion_latir / D.fps * 1000;

function reproducir(lista) {
  cola = [...lista];
  siguiente(performance.now());
}
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

function ajustar() {
  const w = lienzo.clientWidth, h = lienzo.clientHeight;
  renderer.setSize(w, h, false);
  camara.aspect = w / h;
  camara.updateProjectionMatrix();
}
new ResizeObserver(ajustar).observe(lienzo);
new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(lienzo);
ajustar();
