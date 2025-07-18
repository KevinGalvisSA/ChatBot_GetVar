// backend/src/adapters/http/controllers/message_controller.ts

import { Request, Response } from 'express';
import { MessageService } from '../../../application/services/message_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const service = new MessageService();

export const createMessageData = async (req: Request, res: Response) => {
    try {
        const msg = await service.createMessage(req.body);
        return ApiResponse.created(res, 'Mensaje creado exitosamente', msg);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al crear el mensaje');
    }
};

export const getMessagesDataByChat = async (req: Request, res: Response) => {
    try {
        const messages = await service.getMessagesByChat(Number(req.params.chatId));
        if (!messages || messages.length === 0) {
            return ApiResponse.notFound(res, 'No se encontraron mensajes para este chat');
        }
        return ApiResponse.success(res, 'Mensajes encontrados', messages);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener los mensajes');
    }
};

export const getAllMessagesData = async (_: Request, res: Response) => {
    try {
        const messages = await service.getAllMessages();
        return ApiResponse.success(res, 'Mensajes encontrados', messages);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener los mensajes');
    }
};

export const updateMessageData = async (req: Request, res: Response) => {
    try {
        const updated = await service.updateMessage(Number(req.params.id), req.body);
        if (!updated) {
            return ApiResponse.notFound(res, 'Mensaje no encontrado para actualizar');
        }
        return ApiResponse.success(res, 'Mensaje actualizado exitosamente', updated);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al actualizar el mensaje');
    }
};

export const deleteMessageData = async (req: Request, res: Response) => {
    try {
        const deleted = await service.deleteMessage(Number(req.params.id));
        if (!deleted) {
            return ApiResponse.notFound(res, 'Mensaje no encontrado para eliminar');
        }
        return ApiResponse.success(res, 'Mensaje eliminado exitosamente', deleted);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al eliminar el mensaje');
    }
};
