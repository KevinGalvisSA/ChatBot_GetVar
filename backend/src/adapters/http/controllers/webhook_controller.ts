// backend/src/adapters/http/controllers/webhook_controller.ts

import { Request, Response } from 'express';
import { CustomerService } from '../../../application/services/customer_service';
import { ChatService } from '../../../application/services/chat_service';
import { MessageService } from '../../../application/services/message_service';
import { MessageStorageService } from '../../../application/services/messageStorage_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const customerService = new CustomerService();
const chatService = new ChatService();
const messageService = new MessageService();
const messageStorageService = new MessageStorageService();

export class WebhookController {
    static async handleWhatsAppWebhook(req: Request, res: Response) {
        try {
            const body = req.body;

            // Simulación de estructura de payload Meta
            const phone = Number(body.from);
            const name = body.profile?.name || 'Sin Nombre';
            const message = body.message?.text?.body || '';
            const messageId = body.message?.id;
            const deleted = body.message?.type === 'deleted';

            if (!phone || isNaN(phone)) {
                return ApiResponse.badRequest(res, 'Número de teléfono inválido');
            }

            // 1. Crear o actualizar Customer
            const customer = await customerService.getOrCreateCustomer(name, phone);
            if (customer.name !== name) {
                await customerService.updateCustomer(customer.id, { name });
            }

            // 2. Crear o obtener Chat
            const chat = await chatService.createChatIfNotExists(customer.id);

            // 3. Actualizar campo last_connection
            await chatService.updateChat(chat.id, { last_connection: new Date() });

            // 4. Manejo de eliminación de mensajes
            if (deleted && messageId) {
                await messageService.deleteMessage(messageId);
                return ApiResponse.success(res, 'Mensaje eliminado');
            }

            // 5. Procesar mensaje y obtener respuesta del bot
            if (message && message.trim() !== '') {
                const botReply = await chatService.handleUserMessageAndResponse(customer.id, message, messageService);
                return ApiResponse.success(res, 'Mensaje procesado correctamente', {
                    userMessage: message,
                    botResponse: botReply,
                });
            }

            return ApiResponse.success(res, 'Mensaje vacío o sin acción necesaria');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getMessageStorage(req: Request, res: Response) {
        try {
            const { phone } = req.params;
            const storage = await messageStorageService.getBysession_id(Number(phone));
            return ApiResponse.success(res, 'Storage obtenido correctamente', storage);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
