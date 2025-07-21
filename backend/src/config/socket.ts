import { Server } from 'socket.io';
import { pythonCommunication } from '../application/services/pythonCommunication';

export function configureSocket(io: Server) {
  io.on('connection', (socket) => {
    console.log('Cliente conectado:', socket.id);

    socket.on('send_message', async (data) => {
      try {
        console.log('Mensaje recibido desde el frontend:', data);

        const pythonResponse = await pythonCommunication.sendMessageToPython(data.message);
        socket.emit('receive_message', pythonResponse);
      } catch (error) {
        console.error('Error en socket:', error);
        socket.emit('receive_message', '❌ Error al procesar el mensaje');
      }
    });

    socket.on('disconnect', () => {
      console.log('Cliente desconectado:', socket.id);
    });
  });
}
