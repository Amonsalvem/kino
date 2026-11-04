import {describe, expect, it} from 'vitest';
import {formatoCifra, proyectarW, resistenciaW} from '../src/worklets';
import {proyectar, resistencia} from '../src/nucleo';

describe('worklets = núcleo', () => {
	it('resistencia y proyección dan lo mismo que en la web', () => {
		for (const x of [-300, -40, 0, 12, 90, 500]) expect(resistenciaW(x, 420)).toBeCloseTo(resistencia(x, 420), 9);
		for (const [p, v] of [[0, 0], [120, 900], [300, -1500]]) expect(proyectarW(p, v)).toBeCloseTo(proyectar(p, v), 9);
	});
	it('formato de cifras es-CO', () => {
		expect(formatoCifra(1234567)).toBe('1.234.567');
		expect(formatoCifra(3.46, 1)).toBe('3,5');
		expect(formatoCifra(-1200)).toBe('-1.200');
		expect(formatoCifra(8)).toBe('8');
	});
});
