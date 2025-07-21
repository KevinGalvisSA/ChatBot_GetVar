// backend/src/adapters/http/controllers/chat_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { ChatService } from '../../../application/services/chat_service';

const chatService = new ChatService();

export class ChatController {
    static async createIfNotExists(req: Request, res: Response) {
        try {
            const { customerId } = req.body;
            if (!customerId || isNaN(Number(customerId))) {
                return ApiResponse.badRequest(res, 'customerId inválido o faltante');
            }

            const chat = await chatService.createChatIfNotExists(Number(customerId));
            return ApiResponse.success(res, 'Chat obtenido o creado correctamente', chat);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getById(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID de chat inválido');

            const chat = await chatService.getChatById(id);
            return ApiResponse.success(res, 'Chat obtenido correctamente', chat);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByCustomerId(req: Request, res: Response) {
        try {
            const customerId = parseInt(req.params.customerId);
            if (isNaN(customerId)) return ApiResponse.badRequest(res, 'ID de cliente inválido');

            const chat = await chatService.getChatByCustomerId(customerId);
            return ApiResponse.success(res, 'Chat del cliente obtenido correctamente', chat);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async update(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID de chat inválido');

            const updated = await chatService.updateChat(id, req.body);
            return ApiResponse.success(res, 'Chat actualizado correctamente', updated);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async delete(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID de chat inválido');

            await chatService.deleteChat(id);
            return ApiResponse.success(res, 'Chat eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async list(req: Request, res: Response) {
        try {
            const chats = await chatService.listChats();
            return ApiResponse.success(res, 'Listado de chats obtenido correctamente', chats);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
