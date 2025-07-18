// backend/src/adapters/http/controllers/chat_controller.ts

import { Request, Response } from 'express';
import { ChatService } from '../../../application/services/chat_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const service = new ChatService();

export const registerChatInfo = async (req: Request, res: Response) => {
    try {
        const chat = await service.createChat(req.body);
        return ApiResponse.created(res, 'Chat creado exitosamente', chat);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al crear el chat');  
    }
};

export const getChatInfoByCustomerId = async (req: Request, res: Response) => {
    try {
        const chats = await service.getChatsByCustomer(Number(req.params.customerId));
        if (!chats || chats.length === 0) {
            return ApiResponse.notFound(res, 'Chats no encontrados para este cliente');  
        }
        return ApiResponse.success(res, 'Chats encontrados', chats);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener los chats');  
    }
};

export const getChatsInfo = async (_: Request, res: Response) => {
    try {
        const chats = await service.getAllChats();
        return ApiResponse.success(res, 'Chats encontrados', chats);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener los chats');  
    }
};

export const updateChatInfo = async (req: Request, res: Response) => {
    try {
        const updated = await service.updateChat(Number(req.params.id), req.body);
        if (!updated) {
            return ApiResponse.notFound(res, 'Chat no encontrado para actualizar');  
        }
        return ApiResponse.success(res, 'Chat actualizado exitosamente', updated);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al actualizar el chat');  
    }
};

export const deleteChatInfo = async (req: Request, res: Response) => {
    try {
        const deleted = await service.deleteChat(Number(req.params.id));
        if (!deleted) {
            return ApiResponse.notFound(res, 'Chat no encontrado para eliminar');  
        }
        return ApiResponse.success(res, 'Chat eliminado exitosamente', deleted);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al eliminar el chat');  
    }
};
