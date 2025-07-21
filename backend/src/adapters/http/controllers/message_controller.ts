// backend/src/adapters/http/controllers/message_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { MessageService } from '../../../application/services/message_service';

const messageService = new MessageService();

export class MessageController {
    static async create(req: Request, res: Response) {
        try {
            const messageData = req.body;
            const createdMessage = await messageService.createMessage(messageData);
            return ApiResponse.created(res, 'Mensaje creado correctamente', createdMessage);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByChatId(req: Request, res: Response) {
        try {
            const chatId = parseInt(req.params.chatId);
            if (isNaN(chatId)) {
                return ApiResponse.badRequest(res, 'Chat ID inválido');
            }

            const messages = await messageService.getMessagesByChat(chatId);
            return ApiResponse.success(res, 'Mensajes del chat obtenidos correctamente', messages);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async deleteById(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) {
                return ApiResponse.badRequest(res, 'ID inválido');
            }

            const deleted = await messageService.deleteMessage(id);
            if (!deleted) {
                return ApiResponse.notFound(res, 'Mensaje no encontrado para eliminar');
            }

            return ApiResponse.success(res, 'Mensaje eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
