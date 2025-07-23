// backend/src/config/socket.ts

import { Server } from 'socket.io';
import { pythonCommunication } from '../application/services/pythonCommunication';
import { ChatService } from '../application/services/chat_service';

export function configureSocket(io: Server) {
  const chatService = new ChatService();

  io.on('connection', (socket) => {
    console.log('Cliente conectado:', socket.id);

    socket.on('send_message', async (data) => {
      try {
        const { message, id_session } = data;

        if (!message || !id_session) {
          socket.emit('receive_message', '❌ Faltan campos: message o id_session');
          return;
        }

        const response = await pythonCommunication.sendMessageToPython(message, id_session);
        socket.emit('receive_message', response);
      } catch (error) {
        console.error('Error en socket:', error);
        socket.emit('receive_message', '❌ Error al procesar el mensaje');
      }
    });

    socket.on('generate-summary', async (data) => {
      try {
        const { customer_id } = data;

        if (!customer_id) {
          console.warn('❌ customer_id faltante en evento generate-summary');
          return;
        }

        const updatedChat = await chatService.updateChatStateByCustomer(customer_id, 0);

        socket.emit('summary_result', {
          success: true,
          message: '✅ Resumen generado',
          chatId: updatedChat.id,
        });
      } catch (err) {
        console.error('❌ Error al generar resumen por socket:', err);
        socket.emit('summary_result', {
          success: false,
          message: '❌ Error generando resumen',
        });
      }
    });

    socket.on('disconnect', () => {
      console.log('Cliente desconectado:', socket.id);
    });
  });
}

