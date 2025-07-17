import io from 'socket.io-client';
// Conectar al servidor de Socket.IO
const socket = io('http://localhost:4000');  // Asegúrate de que esta URL sea la correcta

socket.on('connect', () => {
  console.log('Conectado al servidor WebSocket');
  
  // Enviar un mensaje al servidor
  socket.emit('send_message', { message: '¿Cómo mejorar mi flujo de trabajo con IA?' });
});

// Escuchar la respuesta del servidor
socket.on('receive_message', (data) => {
  console.log('Respuesta recibida del backend:', data);  // Aquí verás la respuesta procesada por Gemini
});
