import {describe, expect, it} from 'vitest';
import {estadoHonesto, planDeTransicion, valoresDeEstado} from '../src/plan';
import {ESTADOS, ms, TOKENS, TRANSICIONES} from '../src/nucleo';

const SUBIDA = TOKENS.distancia.subida;

describe('plan de transición para la app', () => {
	it('confirmar: el borde se cierra, aparecen barra y nota, y late', () => {
		const p = planDeTransicion('sin-confirmar', 'vigente', false, SUBIDA)!;
		expect(p.duracionMs).toBe(ms('aparecer/duracion'));
		expect(p.pasos).toContainEqual({clave: 'discontinuo', de: 1, a: 0});
		expect(p.pasos).toContainEqual({clave: 'barra', de: 0, a: 1});
		expect(p.pasos).toContainEqual({clave: 'notaY', de: SUBIDA, a: 0});
		expect(p.late).toBe(true);
	});
	it('en reducido nada se desplaza ni se dibuja: solo opacidades', () => {
		for (const t of TRANSICIONES) {
			for (const de of t.de) {
				const p = planDeTransicion(de, t.a, true, SUBIDA)!;
				for (const paso of p.pasos) expect(['notaY', 'corte', 'tachado', 'barraEscala']).not.toContain(paso.clave);
			}
		}
	});
	it('revocar reducido: la línea queda a escala final y aparece por fundido', () => {
		const p = planDeTransicion('vigente', 'revocado', true, SUBIDA)!;
		expect(p.fijar.corte).toBe(1);
		expect(p.pasos).toContainEqual({clave: 'corteOp', de: 0, a: 1});
	});
	it('caducar parte de la vigencia actual', () => {
		const p = planDeTransicion('por-vencer', 'vencido', false, SUBIDA)!;
		expect(p.pasos).toContainEqual({clave: 'barraEscala', de: 'actual', a: 0});
	});
	it('sin transición no hay plan (cambio directo)', () => {
		expect(planDeTransicion('previsto', 'vigente', false, SUBIDA)).toBeNull();
	});
	it('el estado final de cada plan coincide con el reposo de su estado destino', () => {
		for (const t of TRANSICIONES) {
			const p = planDeTransicion(t.de[0], t.a, false, SUBIDA)!;
			const final = valoresDeEstado(t.a);
			for (const paso of p.pasos) expect(paso.a).toBeCloseTo(final[paso.clave], 6);
		}
	});
	it('estado honesto: vigente sin lector es sin confirmar', () => {
		expect(estadoHonesto('vigente')).toBe('sin-confirmar');
		expect(estadoHonesto('por-vencer', null)).toBe('sin-confirmar');
		expect(estadoHonesto('vigente', {lector: 'Lector Portería', hora: new Date()})).toBe('vigente');
		for (const e of ESTADOS) if (e !== 'vigente' && e !== 'por-vencer') expect(estadoHonesto(e)).toBe(e);
	});
});
