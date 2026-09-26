// Arnés web: corre la pantalla de ejemplo con react-native-web + Reanimated + Gesture Handler para verla en un navegador.
import React from 'react';
import {AppRegistry} from 'react-native';
import {GestureHandlerRootView} from 'react-native-gesture-handler';
import {FuentesKino} from '../src';
import {PantallaPases} from '../ejemplo/PantallaPases';

const App = () => (
	<GestureHandlerRootView style={{flex: 1}}>
		<FuentesKino fuentes={{titulo: 'Archivo, system-ui, sans-serif', texto: 'Archivo, system-ui, sans-serif', dato: 'JetBrains Mono, ui-monospace, monospace'}}>
			<PantallaPases />
		</FuentesKino>
	</GestureHandlerRootView>
);
AppRegistry.registerComponent('kino', () => App);
AppRegistry.runApplication('kino', {rootTag: document.getElementById('raiz')});
