// backend/src/scripts/test_summary.ts

import { io } from 'socket.io-client';

type GenerateSummaryPayload = {
    customer_id: number;
};

// Conexión al servidor de sockets (ajusta la URL si es necesario)
const socket = io('http://localhost:4000', {
    transports: ['websocket'],
});

// Cliente conectado
socket.on('connect', () => {
    console.log('✅ Conectado al socket server con ID:', socket.id);

    // Emitimos el evento para generar resumen del customer 1
    const payload: GenerateSummaryPayload = {
        customer_id: 1,
    };

    console.log('📤 Enviando solicitud de resumen para customer_id:', payload.customer_id);
    socket.emit('generate-summary', payload);
});

// Manejamos errores del cliente
socket.on('connect_error', (err) => {
    console.error('❌ Error de conexión:', err.message);
});

// Opcional: cerrar después de un tiempo para no dejarlo colgado
setTimeout(() => {
    socket.disconnect();
    console.log('🔌 Desconectado del socket');
}, 5000);
