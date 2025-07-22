// backend/src/adapters/http/controllers/message_storage_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { MessageStorageService } from '../../../application/services/messageStorage_service';

const messageStorageService = new MessageStorageService();

export class MessageStorageController {
    static async create(req: Request, res: Response) {
        try {
            const data = req.body;
            const result = await messageStorageService.createStorageMessage(data);
            return ApiResponse.created(res, 'Mensaje almacenado correctamente', result);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByCustomerId(req: Request, res: Response) {
        try {
            const customerId = parseInt(req.params.customerId);
            if (isNaN(customerId)) {
                return ApiResponse.badRequest(res, 'ID de cliente inválido');
            }

            const message = await messageStorageService.getByCustomerId(customerId);
            if (!message) {
                return ApiResponse.notFound(res, 'Mensaje no encontrado para el cliente');
            }

            return ApiResponse.success(res, 'Mensaje obtenido correctamente', message);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getBySessionId(req: Request, res: Response) {
        try {
            const sessionId = parseInt(req.params.sessionId);
            if (isNaN(sessionId)) {
                return ApiResponse.badRequest(res, 'Session ID inválido');
            }

            const message = await messageStorageService.getBySessionId(sessionId);
            if (!message) {
                return ApiResponse.notFound(res, 'Mensaje no encontrado para la sesión');
            }

            return ApiResponse.success(res, 'Mensaje obtenido correctamente', message);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async deleteByCustomerId(req: Request, res: Response) {
        try {
            const customerId = parseInt(req.params.customerId);
            if (isNaN(customerId)) {
                return ApiResponse.badRequest(res, 'ID de cliente inválido');
            }

            const deleted = await messageStorageService.deleteByCustomerId(customerId);
            if (!deleted) {
                return ApiResponse.notFound(res, 'No se encontró un mensaje para eliminar');
            }

            return ApiResponse.success(res, 'Mensaje eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
