import cron from 'node-cron';
import { ChatService } from '../application/services/chat_service';

const chatService = new ChatService();

// Ejecutar cada hora, en el minuto 0
cron.schedule('*/5 * * * *', async () => {
    console.log('⏰ Ejecutando cron job para detectar chats inactivos...');

    try {
        // Buscar chats inactivos hace más de 60 minutos
        const inactiveChats = await chatService.getChatsInactiveForMinutes(5);

        if (inactiveChats.length === 0) {
            console.log('📭 No hay chats inactivos por cerrar.');
            return;
        }

        console.log(`📦 Se encontraron ${inactiveChats.length} chats inactivos.`);

        for (const chat of inactiveChats) {
            try {
                await chatService.updateChatStateByCustomer(chat.id_customer, 0);
                console.log(`✅ Chat del cliente ${chat.id_customer} cerrado y resumen generado.`);
            } catch (error) {
                console.error(`❌ Error procesando chat del cliente ${chat.id_customer}:`, error);
            }
        }
    } catch (error) {
        console.error('❌ Error general en el cron job:', error);
    }
});
