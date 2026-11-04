// Pantalla de ejemplo: cómo se usa el adaptador en la app. Es también la que se prueba en web (web/main.tsx).
import React, {useState} from 'react';
import {ScrollView, StyleSheet, Text, View} from 'react-native';
import Animated from 'react-native-reanimated';
import {
	BotonKino, EsperaLectorKino, eventosDesde, HojaKino, NumeroKino, PaseKino, transicion, useCascada, useMovimientoReducido,
	useTemaKino, EntraKino, salidaKino, disposicionKino, type Estado, type Evento,
} from '../src';

const min = (m: number) => new Date(Date.now() + m * 60_000);
const NOMBRE: Record<Evento, string> = {enviar: 'Enviar al lector', confirmar: 'El lector confirma', avisar: 'Entra en aviso', caducar: 'Vence', usar: 'Se usa', revocar: 'Revocar'};

type Item = {id: number; quien: string; casa: string; estado: Estado};

export function PantallaPases() {
	const {color} = useTemaKino();
	const reducido = useMovimientoReducido();
	// Un Pase vivo que recorre sus estados con eventos del núcleo.
	const [estado, setEstado] = useState<Estado>('previsto');
	const [enviado, setEnviado] = useState<Date>();
	const [evidencia, setEvidencia] = useState<{lector: string; hora: Date} | null>(null);
	const [revocacion, setRevocacion] = useState<{nombre: string; hora: Date} | null>(null);
	const aplicar = (ev: Evento) => {
		const t = transicion(estado, ev);
		if (ev === 'enviar') setEnviado(new Date());
		if (ev === 'confirmar') setEvidencia({lector: 'Lector Portería', hora: new Date()});
		if (ev === 'revocar') setRevocacion({nombre: 'Carolina Ruiz', hora: new Date()});
		setEstado(t.a);
	};
	const reiniciar = () => {
		setEstado('previsto');
		setEvidencia(null);
		setRevocacion(null);
	};
	// Lista con entrada en cascada, salida y reacomodo con resorte.
	const [items, setItems] = useState<Item[]>([
		{id: 1, quien: 'Luz Marina', casa: 'Casa 3', estado: 'previsto'},
		{id: 2, quien: 'Técnico del gas', casa: 'Casa 22', estado: 'sin-confirmar'},
		{id: 3, quien: 'Jardinería', casa: 'Casa 31', estado: 'previsto'},
	]);
	const retrasos = useCascada(items.length);
	const [hoja, setHoja] = useState(false);
	const [confirmados, setConfirmados] = useState(3);
	const [espera, setEspera] = useState<{enviado: Date; confirmado?: Date}>({enviado: min(-2)});
	const posibles = new Set(eventosDesde(estado));

	return (
		<View style={[s.raiz, {backgroundColor: color('superficie/abismo')}]}>
			<ScrollView contentContainerStyle={s.contenido}>
				<Text style={[s.titulo, {color: color('texto/primario')}]}>Pases de la Casa 14</Text>

				<PaseKino testID="pase-vivo" quien="Andrés Gómez" casa="Casa 14" desde={min(-20)} hasta={min(100)} estado={estado} enviado={enviado} evidencia={evidencia} revocacion={revocacion} />
				<View style={s.fila}>
					{(Object.keys(NOMBRE) as Evento[]).map((ev) => (
						<BotonKino key={ev} variante="secundaria" onPress={() => posibles.has(ev) && aplicar(ev)} style={!posibles.has(ev) && {opacity: 0.35}}>
							{NOMBRE[ev]}
						</BotonKino>
					))}
					<BotonKino variante="secundaria" onPress={reiniciar}>Reiniciar</BotonKino>
				</View>

				<Text style={[s.sub, {color: color('texto/secundario')}]}>Lista</Text>
				{items.map((it, i) => (
					<Animated.View key={it.id} exiting={salidaKino(reducido)} layout={disposicionKino(reducido)}>
						<EntraKino retraso={retrasos[i] ?? 0}>
							<PaseKino quien={it.quien} casa={it.casa} desde={min(-10)} hasta={min(60 + it.id * 30)} estado={it.estado} enviado={min(-5)} />
						</EntraKino>
					</Animated.View>
				))}
				<View style={s.fila}>
					<BotonKino onPress={() => setItems((x) => [{id: Date.now(), quien: 'Paula Vélez', casa: 'Casa 12', estado: 'previsto'}, ...x])}>Agregar un Pase</BotonKino>
					<BotonKino variante="secundaria" onPress={() => setItems((x) => x.slice(1))}>Quitar el primero</BotonKino>
				</View>

				<Text style={[s.sub, {color: color('texto/secundario')}]}>Esperar al lector</Text>
				<EsperaLectorKino lector="Lector Portería" enviado={espera.enviado} confirmado={espera.confirmado} />
				<View style={s.fila}>
					<BotonKino variante="secundaria" onPress={() => setEspera((e) => ({...e, confirmado: new Date()}))}>El lector confirma</BotonKino>
				</View>

				<View style={s.numero}>
					<NumeroKino valor={confirmados} style={[s.cifra, {color: color('texto/primario')}]} />
					<Text style={{color: color('texto/secundario')}}>de 8 Pases confirmados por el lector</Text>
				</View>
				<View style={s.fila}>
					<BotonKino variante="secundaria" onPress={() => setConfirmados((n) => Math.min(8, n + 1))}>Confirmar uno más</BotonKino>
					<BotonKino onPress={() => setHoja(true)}>Ver el Pase de Andrés</BotonKino>
				</View>
				<Text style={[s.sub, {color: color('texto/secundario')}]}>Estado honesto</Text>
				<Text style={{color: color('texto/tenue'), fontSize: 13}}>Se pide «vigente» sin evidencia del lector: se muestra «sin confirmar».</Text>
				<PaseKino testID="pase-honesto" quien="Visita sin confirmar" casa="Casa 14" desde={min(-5)} hasta={min(55)} estado="vigente" enviado={min(-3)} />
			</ScrollView>
			<HojaKino abierta={hoja} alCerrar={() => setHoja(false)} altura={360}>
				<Text style={[s.sub, {color: color('texto/primario')}]}>Pase de Andrés Gómez</Text>
				<PaseKino quien="Andrés Gómez" casa="Casa 14" desde={min(-20)} hasta={min(100)} estado="vigente" evidencia={{lector: 'Lector Portería', hora: min(-18)}} />
			</HojaKino>
		</View>
	);
}

const s = StyleSheet.create({
	raiz: {flex: 1},
	contenido: {padding: 16, gap: 12, maxWidth: 480, width: '100%', alignSelf: 'center'},
	titulo: {fontSize: 26, fontWeight: '800'},
	sub: {fontSize: 16, fontWeight: '700', marginTop: 12},
	fila: {flexDirection: 'row', flexWrap: 'wrap', gap: 8},
	numero: {flexDirection: 'row', alignItems: 'baseline', gap: 10, marginTop: 12},
	cifra: {fontSize: 40, fontWeight: '800'},
});
