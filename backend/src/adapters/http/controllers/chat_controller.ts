// backend/src/adapters/http/controllers/chat_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { ChatService } from '../../../application/services/chat_service';

const chatService = new ChatService();

export class ChatController {
    static async createIfNotExists(req: Request, res: Response) {
        try {
            const { id_customer } = req.body;
            if (!id_customer || isNaN(Number(id_customer))) {
                return ApiResponse.badRequest(res, 'id_customer inválido o faltante');
            }

            const chat = await chatService.createChatIfNotExists(Number(id_customer));
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

    static async getByid_customer(req: Request, res: Response) {
        try {
            const id_customer = parseInt(req.params.id_customer);
            if (isNaN(id_customer)) return ApiResponse.badRequest(res, 'ID de cliente inválido');

            const chat = await chatService.getChatByid_customer(id_customer);
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

    static async updateState(req: Request, res: Response) {
        try {
            const id = Number(req.params.id);
            const { state } = req.body;

            if (!Number.isInteger(id) || id <= 0) {
                return ApiResponse.badRequest(res, 'ID de chat inválido');
            }

            if (state === undefined || (state !== 0 && state !== 1)) {
                return ApiResponse.badRequest(res, 'El campo "state" es requerido y debe ser 0 o 1');
            }

            const chat = await chatService.getChatById(id);
            if (!chat) {
                return ApiResponse.notFound(res, 'Chat no encontrado');
            }

            if (chat.state === state) {
                return ApiResponse.success(res, 'El estado ya está establecido en ese valor', chat);
            }

            const updatedChat = await chatService.updateChatStateByCustomer(id, state);
            return ApiResponse.success(res, 'Estado actualizado correctamente', updatedChat);
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
