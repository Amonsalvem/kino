import {describe, expect, it} from 'vitest';
import {
	bezier, cssLinear, curvaDe, escalonar, entradaDePantalla, estadoDelPase, eventosDesde, lineaDeTiempo, ms, reducirKeyframes,
	reducirPistas, resolver, resorteDe, salida, TOKENS, transicion, TRANSICIONES, TransicionInvalida, vigenciaRestante, type Estado, type Hechos,
} from '../src/nucleo';

describe('curvas', () => {
	it('cubic-bezier coincide con el cálculo de referencia', () => {
		// Valor verificado contra Blender en el Pase 3D: crecer en 24/49 = 0,9371.
		expect(bezier(curvaDe('curva/crecer'))(24 / 49)).toBeCloseTo(0.9371, 4);
		expect(bezier([0, 0, 1, 1])(0.3)).toBeCloseTo(0.3, 6);
	});
	it('es monótona en todas las curvas del sistema', () => {
		for (const nombre of Object.keys(TOKENS.curva)) {
			const f = bezier(curvaDe(`curva/${nombre}` as never));
			let prev = -1;
			for (let t = 0; t <= 1.0001; t += 0.01) {
				const v = f(t);
				expect(v).toBeGreaterThanOrEqual(prev - 1e-9);
				prev = v;
			}
		}
	});
	it('linear() empieza en 0 y termina en 1', () => {
		const s = cssLinear(bezier(curvaDe('curva/cortina')));
		expect(s.startsWith('linear(0,')).toBe(true);
		expect(s.endsWith(', 1)')).toBe(true);
	});
});

describe('resortes', () => {
	it('ninguno rebota más de 3 % (Kino es exacto)', () => {
		for (const nombre of Object.keys(TOKENS.resorte)) {
			expect(resolver(resorteDe(nombre as never)).rebote).toBeLessThanOrEqual(0.03);
		}
	});
	it('firme tiene amortiguación crítica y no se pasa', () => {
		const s = resolver(resorteDe('firme'));
		expect(s.zeta).toBeCloseTo(1, 6);
		expect(s.rebote).toBe(0);
	});
	it('llega al destino y arranca con la velocidad del gesto', () => {
		const s = resolver(resorteDe('hoja'), 4);
		expect(s.avance(0)).toBeCloseTo(0, 9);
		expect(s.velocidad(0)).toBeCloseTo(4, 6);
		expect(s.avance(s.asentamiento + 0.2)).toBeCloseTo(1, 2);
	});
	it('los tres regímenes son continuos en ζ = 1', () => {
		const casi = resolver({rigidez: 400, amortiguacion: 39.999, masa: 1});
		const critico = resolver({rigidez: 400, amortiguacion: 40, masa: 1});
		const sobre = resolver({rigidez: 400, amortiguacion: 40.001, masa: 1});
		for (const t of [0.05, 0.1, 0.2]) {
			expect(casi.avance(t)).toBeCloseTo(critico.avance(t), 3);
			expect(sobre.avance(t)).toBeCloseTo(critico.avance(t), 3);
		}
	});
});

describe('coreografía', () => {
	it('la cascada respeta el máximo y el tope', () => {
		// Pocos elementos: el paso es el del token.
		expect(escalonar(4)).toEqual([0, 1, 2, 3].map((i) => i * TOKENS.escalonado.tarjetas));
		// Muchos: el paso se comprime para no pasar del tope, y del máximo en adelante entran juntos.
		const r = escalonar(20);
		expect(r[0]).toBe(0);
		expect(r[1]).toBeLessThan(TOKENS.escalonado.tarjetas);
		expect(r[TOKENS.coreografia.cascadaMaximo]).toBe(r[TOKENS.coreografia.cascadaMaximo - 1]);
		expect(Math.max(...r)).toBeLessThanOrEqual(TOKENS.coreografia.cascadaTopeMs);
	});
	it('salir es más corto que entrar', () => {
		expect(salida('aparecer/duracion')).toBeLessThan(ms('aparecer/duracion'));
	});
	it('la línea de tiempo encadena, junta y desfasa', () => {
		const {tramos, total} = lineaDeTiempo([
			{id: 'a', duracion: 'duracion/corto'},
			{id: 'b', duracion: 'duracion/tarjeta'},
			{id: 'c', duracion: 'duracion/corto', junto: 'b', conDesfase: 90},
		]);
		expect(tramos.b.inicio).toBe(ms('duracion/corto'));
		expect(tramos.c.inicio).toBe(tramos.b.inicio + 90);
		expect(total).toBe(tramos.b.fin);
	});
	it('la acción entra después de la última tarjeta', () => {
		const e = entradaDePantalla(3);
		expect(e.accion).toBeGreaterThan(Math.max(...e.tarjetas));
	});
});

describe('estado honesto del Pase', () => {
	const hora = (h: number) => new Date(2026, 8, 26, h);
	const base: Hechos = {desde: hora(16), hasta: hora(18)};
	const aviso = 30 * 60 * 1000;

	it('sin confirmación del lector nunca es vigente ni por vencer', () => {
		// Recorre combinaciones de hechos sin confirmación en muchos instantes.
		let casos = 0;
		for (let i = 0; i < 20000; i++) {
			const h: Hechos = {
				desde: hora(10 + (i % 8)),
				hasta: hora(12 + (i % 9)),
				enviadoAlLector: i % 2 ? hora(9) : undefined,
				usadoEn: i % 7 === 0 ? hora(13) : undefined,
				revocacion: i % 11 === 0 ? {nombre: 'Carolina Ruiz', hora: hora(14)} : undefined,
			};
			const ahora = new Date(hora(8).getTime() + (i * 97_000) % (14 * 3600_000));
			const e = estadoDelPase(h, ahora, aviso);
			expect(['vigente', 'por-vencer']).not.toContain(e);
			casos++;
		}
		expect(casos).toBe(20000);
	});
	it('con confirmación: previsto, vigente, por vencer y vencido según la hora', () => {
		const h: Hechos = {...base, confirmacion: {lector: 'Lector Portería', hora: hora(15)}};
		expect(estadoDelPase(h, hora(15), aviso)).toBe('previsto');
		expect(estadoDelPase(h, hora(16), aviso)).toBe('vigente');
		expect(estadoDelPase(h, new Date(hora(18).getTime() - 10 * 60_000), aviso)).toBe('por-vencer');
		expect(estadoDelPase(h, hora(18), aviso)).toBe('vencido');
	});
	it('revocar y usar mandan sobre la hora', () => {
		const h: Hechos = {...base, confirmacion: {lector: 'L', hora: hora(15)}, revocacion: {nombre: 'C', hora: hora(17)}};
		expect(estadoDelPase(h, hora(17), aviso)).toBe('revocado');
	});
	it('la vigencia restante va de 1 a 0', () => {
		expect(vigenciaRestante(base, hora(16))).toBe(1);
		expect(vigenciaRestante(base, hora(17))).toBeCloseTo(0.5, 6);
		expect(vigenciaRestante(base, hora(19))).toBe(0);
	});
});

describe('transiciones', () => {
	it('solo «confirmar» lleva a vigente, y solo desde sin confirmar', () => {
		const aVigente = TRANSICIONES.filter((t) => t.a === 'vigente');
		expect(aVigente.map((t) => t.evento)).toEqual(['confirmar']);
		expect(aVigente[0].de).toEqual(['sin-confirmar']);
	});
	it('un salto imposible lanza', () => {
		expect(() => transicion('previsto', 'confirmar')).toThrow(TransicionInvalida);
		expect(() => transicion('vencido', 'revocar')).toThrow(TransicionInvalida);
	});
	it('los estados terminales no tienen salida', () => {
		for (const e of ['vencido', 'usado', 'revocado'] as Estado[]) expect(eventosDesde(e)).toEqual([]);
	});
	it('cada transición deja constancia de algo', () => {
		for (const t of TRANSICIONES) expect(t.deja).toBeTruthy();
	});
	it('solo confirmar hace latir', () => {
		expect(TRANSICIONES.filter((t) => t.late).map((t) => t.evento)).toEqual(['confirmar']);
	});
});

describe('movimiento reducido', () => {
	it('las pistas reducidas no desplazan ni escalan', () => {
		for (const t of TRANSICIONES) {
			for (const p of reducirPistas(t.pistas)) expect(['y', 'escala', 'escalaX']).not.toContain(p.propiedad);
		}
	});
	it('una línea que se dibuja pasa a aparecer por fundido', () => {
		const r = reducirPistas(transicion('vigente', 'revocar').pistas);
		expect(r).toContainEqual({parte: 'corte', propiedad: 'opacidad', de: 0, a: 1});
	});
	it('keyframes: quita transformaciones y conserva la opacidad', () => {
		expect(reducirKeyframes([{transform: 'translateY(26px)', opacity: 0}, {transform: 'none', opacity: 1}])).toEqual([{opacity: 0}, {opacity: 1}]);
		expect(reducirKeyframes([{transform: 'scale(.97)'}, {transform: 'none'}])).toEqual([]);
	});
});
