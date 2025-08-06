// backend/src/adapters/http/controllers/webhook_controller.ts

import { Request, Response } from 'express';
import { CustomerService } from '../../../application/services/customer_service';
import { ChatService } from '../../../application/services/chat_service';
import { MessageService } from '../../../application/services/message_service';
import { MessageStorageService } from '../../../application/services/messageStorage_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import axios from 'axios';

const customerService = new CustomerService();
const chatService = new ChatService();
const messageService = new MessageService();
const messageStorageService = new MessageStorageService();

export class WebhookController {
  // ✅ Verificación del Webhook (GET)
  static verifyWhatsAppWebhook(req: Request, res: Response) {
    const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN;

    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      return res.status(200).send(challenge);
    } else {
      return res.sendStatus(403);
    }
  }

  // ✅ Recepción de mensajes (POST)
  static async handleWhatsAppWebhook(req: Request, res: Response) {
    try {
      const value = req.body.entry?.[0]?.changes?.[0]?.value;

      const contact = value?.contacts?.[0];
      const messageObj = value?.messages?.[0];

      const phone = Number(contact?.wa_id);
      const name = null
      const message = messageObj?.text?.body || '';
      const messageId = messageObj?.id;
      const deleted = messageObj?.type === 'deleted';

      if (!phone || isNaN(phone)) {
        return ApiResponse.badRequest(res, 'Número de teléfono inválido');
      }

      // 1. Crear o actualizar Customer
      const customer = await customerService.getCustomer(name, phone, null, null);
      if (customer.name !== name) {
        await customerService.updateCustomer(customer.id, { name });
      }

      // 2. Crear o obtener Chat
      const chat = await chatService.createChatIfNotExists(customer.id);

      // 3. Actualizar campo last_connection
      await chatService.updateChat(chat.id, { last_connection: new Date(), state: 1 });

      // 4. Manejo de eliminación de mensajes
      if (deleted && messageId) {
        await messageService.deleteMessage(messageId);
        return ApiResponse.success(res, 'Mensaje eliminado');
      }

      // 5. Procesar mensaje
      if (message && message.trim() !== '') {
        const botReply = await chatService.handleUserMessageAndResponse(customer.id, message, messageService);

        // 👇 Si deseas responder por WhatsApp automáticamente:
        await WebhookController.sendMessageToWhatsApp(phone.toString(), botReply);

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

  // ✅ Obtener mensajes almacenados
  static async getMessageStorage(req: Request, res: Response) {
    try {
      const { phone } = req.params;
      const storage = await messageStorageService.getBysession_id(Number(phone));
      return ApiResponse.success(res, 'Storage obtenido correctamente', storage);
    } catch (error) {
      return ApiResponse.error(res, error);
    }
  }

  // ✅ Enviar mensaje a WhatsApp (opcional, llamado desde POST)
  static async sendMessageToWhatsApp(to: string, message: string) {
    const url = `https://graph.facebook.com/v20.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`;

    try {
      await axios.post(
        url,
        {
          messaging_product: 'whatsapp',
          to,
          type: 'text',
          text: { body: message },
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,
            'Content-Type': 'application/json',
          },
        }
      );
    } catch (error) {
      console.error('❌ Error al enviar mensaje a WhatsApp:', error);
    }
  }
}
